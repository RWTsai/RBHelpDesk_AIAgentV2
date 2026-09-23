# tools.py
"""
Agent 工具註冊表（To-Be 新增）
---------------------------------------------------
每個工具是一個 dict：{"description", "parameters"(JSON Schema), "func"}
skill 的 tool.py 也用同樣格式。

內建工具：
- search_qa_kb      QA 知識庫（IT_KB_Graph，三元組擴展＋hybrid，走記憶體快取）
- search_documents  文件 GraphRAG（doc_graph_client.local_search）
- explore_entity    實體關係探索
- web_search        Google 搜尋（SERPAPI_API_KEY 為空時不註冊）
- sql_query         唯讀 SQL（.env 沒設定任何 SQL 來源時不註冊；多個資料庫用 source 參數區分）
- describe_table    查白名單某張表的欄位（白名單表數多時才註冊，和 sql_query 成對）
- load_skill        載入 Skill（由 agent_node 特別處理，func 為 None）

統一回傳格式：
{"ok": bool, "items": [{"source_id", "source_type", "title", "text", "url"}], "note": str, ...}
"""

import os
import re
import json
import time
import hashlib
import datetime
import decimal
import threading

import pyodbc
import sqlglot
from sqlglot import exp

from config import (
    RAG_QA_TOP_K,
    RAG_MIN_SCORE,
    QA_TRIPLE_EXPAND,
    AGENT_TOOL_RESULT_MAX_CHARS,
    SERPAPI_API_KEY,
    ENV_SQL_SOURCES,
    SQL_MAX_ROWS,
    SQL_TIMEOUT_SEC,
    SQL_SCHEMA_INLINE_MAX,
)
from database import doc_graph_client
from database.graph_ragc_client import graph_rag_query
from agents import skill_loader
from utils.logger import log_info, log_error


def _short_hash(text: str) -> str:
    return hashlib.md5((text or "").encode("utf-8")).hexdigest()[:6]


# =====================================================
# 1) QA 知識庫
# =====================================================
def search_qa_kb(query: str) -> dict:
    """
    沿用舊版 AI_Text 的查法：問題本身 + 三元組擴展 → 多個向量 → 每個向量做 hybrid 查詢 → 依 RowID 合併
    """
    texts = [query]
    if QA_TRIPLE_EXPAND:
        try:
            # 延後 import，避免 AGENT_MODE=on 時也在啟動就載入舊節點
            from agents.nodes.ai_text_node import tripleExtractService, triple_dict_to_text
            texts += [triple_dict_to_text(t) for t in tripleExtractService(query)]
        except Exception as e:
            log_error(f"[tools.search_qa_kb] 三元組擴展失敗，只用原問題查詢：{e}")

    vecs = doc_graph_client.embed_texts(texts)

    rows = {}  # RowID → row（保留最高分）
    for vec in vecs:
        kb = graph_rag_query(vec, mode="hybrid") or {}
        semantic = kb.get("semantic_top_k", [])
        top_sim = semantic[0]["similarity"] if semantic else 0
        for r in semantic:
            if r.get("similarity", 0) < RAG_MIN_SCORE:
                continue
            old = rows.get(r["RowID"])
            if not old or r["similarity"] > old.get("similarity", 0):
                rows[r["RowID"]] = r
        # 結構查詢沒有分數，給它 top1 的分數打 9 折
        for r in kb.get("structural_matches", []):
            if top_sim >= RAG_MIN_SCORE and r["RowID"] not in rows:
                rows[r["RowID"]] = dict(r, similarity=top_sim * 0.9)

    # 同一段 ChunkText（同一筆 QA）的多個三元組合併成一個 item
    groups = {}
    for r in sorted(rows.values(), key=lambda x: x.get("similarity", 0), reverse=True):
        key = (r.get("ChunkText") or "").strip()
        if not key:
            continue
        g = groups.setdefault(key, {"rowid": r["RowID"], "score": r.get("similarity", 0), "triples": []})
        if r.get("Entity1") and r.get("Relation") and r.get("Entity2"):
            g["triples"].append(f"{r['Entity1']} {r['Relation']} {r['Entity2']}")

    items = []
    for text, g in list(groups.items())[: RAG_QA_TOP_K + 1]:
        body = text
        if g["triples"]:
            body += "\n[相關三元組] " + "；".join(dict.fromkeys(g["triples"]))
        items.append({
            "source_id": f"QA-{g['rowid']}",
            "source_type": "qa",
            "title": "QA 知識庫",
            "text": body,
            "score": round(g["score"], 4),
        })

    return {"ok": True, "items": items, "note": "" if items else "QA 知識庫沒有找到相關資料"}


# =====================================================
# 2) 文件 GraphRAG
# =====================================================
def search_documents(query: str) -> dict:
    res = doc_graph_client.local_search(query)
    items = []
    for c in res["chunks"]:
        items.append({
            "source_id": f"DOC-{c['ChunkID']}",
            "source_type": "document",
            "title": f"{c['FileName']}（{c['SectionPath']}）" if c["SectionPath"] else c["FileName"],
            "url": c.get("SourceUrl", ""),
            "text": c["ChunkText"],
            "score": c["score"],
        })
    out = {"ok": True, "items": items}
    if res["relations"]:
        out["graph_relations"] = res["relations"]
    if res["entities"]:
        out["related_entities"] = [f"{e['Name']}（{e['EntityType']}）" for e in res["entities"]]
    out["note"] = "" if items else "文件庫沒有找到相關資料"
    return out


def explore_entity(name: str, hops: int = 1) -> dict:
    res = doc_graph_client.explore_entity(name, hops=hops)
    if not res["found"]:
        return {"ok": False, "items": [], "note": f"圖譜中找不到實體「{name}」"}
    ent = res["entity"]
    items = [{
        "source_id": f"ENT-{ent['EntityID']}",
        "source_type": "entity",
        "title": f"實體：{ent['Name']}（{ent['EntityType']}）",
        "text": ent.get("Description") or "",
    }]
    # 關係所在的文件片段也列為可引用來源
    for r in res["relations"]:
        if r.get("chunk_id"):
            items.append({
                "source_id": f"DOC-{r['chunk_id']}",
                "source_type": "document",
                "title": r.get("source_doc", ""),
                "text": f"{r['source']} --{r['relation']}--> {r['target']}：{r['description']}",
                "url": (doc_graph_client.get_chunk(r["chunk_id"]) or {}).get("SourceUrl", ""),
            })
    return {"ok": True, "items": items, "neighbors": res["neighbors"], "note": ""}


# =====================================================
# 3) 網路搜尋
# =====================================================
def web_search(query: str) -> dict:
    from agents.nodes.google_node import google_search_items
    results = google_search_items(query)
    items = [{
        "source_id": f"WEB-{_short_hash(r['link'])}",
        "source_type": "web",
        "title": r["title"],
        "url": r["link"],
        "text": r["snippet"],
    } for r in results]
    return {"ok": True, "items": items, "note": "以下為網路搜尋結果，回答時請註明來自網路" if items else "網路搜尋沒有結果"}


# =====================================================
# 3b) Skill 參考文件
# =====================================================
REF_MAX_CHARS = 8000          # 整份讀取時的上限
REF_MAX_HITS = 40             # 關鍵字搜尋最多回傳幾處


def read_reference(skill: str, file: str = "", keyword: str = "", context: int = 2) -> dict:
    """
    讀 Skill 附帶的參考文件。
    不給 file → 列出該 Skill 有哪些參考文件
    給 keyword → 只回傳含關鍵字的段落（大檔案請一定要用）
    """
    refs = skill_loader.skill_references(skill)
    if not refs:
        return {"ok": False, "items": [], "note": f"Skill「{skill}」沒有參考文件"}

    if not file:
        lines = [f"- {rel}（{size // 1024} KB）" for rel, size in refs]
        return {"ok": True, "items": [{
            "source_id": f"REF-{skill}",
            "source_type": "reference",
            "title": f"{skill} 的參考文件",
            "text": "\n".join(lines) + "\n\n檔案較大時請加 keyword 搜尋，不要整份讀。",
        }], "note": ""}

    try:
        text = skill_loader.read_reference(skill, file)
    except Exception as e:
        return {"ok": False, "items": [], "note": str(e)}

    if keyword:
        lines = text.splitlines()
        context = max(0, min(int(context or 0), 10))
        hits, used = [], set()
        for i, line in enumerate(lines):
            if keyword.lower() not in line.lower():
                continue
            lo, hi = max(0, i - context), min(len(lines), i + context + 1)
            block = range(lo, hi)
            if used.issuperset(block):          # 與前一段重疊就不重複貼
                continue
            used.update(block)
            hits.append(f"[第 {i + 1} 行]\n" + "\n".join(lines[lo:hi]))
            if len(hits) >= REF_MAX_HITS:
                break
        if not hits:
            return {"ok": False, "items": [], "note": f"{file} 裡找不到「{keyword}」"}
        body = "\n---\n".join(hits)
        note = f"找到 {len(hits)} 處" + ("（已達上限，可換更精確的關鍵字）" if len(hits) >= REF_MAX_HITS else "")
    else:
        body = text[:REF_MAX_CHARS]
        note = "" if len(text) <= REF_MAX_CHARS else f"檔案共 {len(text)} 字，只顯示前 {REF_MAX_CHARS} 字，請用 keyword 搜尋"

    return {"ok": True, "items": [{
        "source_id": f"REF-{skill}/{file}",
        "source_type": "reference",
        "title": f"{skill} / {file}" + (f"（搜尋「{keyword}」）" if keyword else ""),
        "text": body,
    }], "note": note}


# =====================================================
# 4) 唯讀 SQL
# =====================================================
# 關鍵字黑名單（第二道防線；sqlglot 解析是第一道程式防線，DB 權限才是根本）
_FORBIDDEN_RE = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|EXEC|EXECUTE|DROP|ALTER|CREATE|TRUNCATE|GRANT|REVOKE|DENY|"
    r"OPENROWSET|OPENQUERY|OPENDATASOURCE|OPENXML|BULK|SHUTDOWN|WAITFOR|DBCC|INTO|BACKUP|RESTORE|"
    r"KILL|RECONFIGURE|USE)\b|\b(XP|SP)_\w+",
    re.IGNORECASE,
)


def _odbc_conn_str(cfg: dict) -> str:
    """
    把 Skill 的 db.json 轉成 pyodbc 連線字串。
    支援兩種寫法：
      {"connectionString": "DRIVER={...};SERVER=...;DATABASE=...;UID=...;PWD=..."}
      {"driver","host","port","database","user","password","trustServerCertificate"}
    .NET 風格的 connectionString（Server=/Database=/User Id=/Password=）也會自動轉換。
    """
    raw = (cfg.get("connectionString") or "").strip()
    if raw:
        if "driver=" in raw.lower():
            return raw
        # .NET 風格 → ODBC
        parts = dict()
        for seg in raw.split(";"):
            if "=" in seg:
                k, v = seg.split("=", 1)
                parts[k.strip().lower()] = v.strip()
        cfg = {
            "driver": cfg.get("driver"),
            "host": parts.get("server") or parts.get("data source"),
            "port": parts.get("port"),
            "database": parts.get("database") or parts.get("initial catalog"),
            "user": parts.get("user id") or parts.get("uid"),
            "password": parts.get("password") or parts.get("pwd"),
            "trustServerCertificate": parts.get("trustservercertificate", "yes"),
        }

    host = (cfg.get("host") or "").strip()
    if not host:
        return ""
    port = str(cfg.get("port") or "").strip()
    server = f"{host},{port}" if port and "," not in host else host
    out = [f"DRIVER={{{cfg.get('driver') or 'ODBC Driver 17 for SQL Server'}}}", f"SERVER={server}"]
    if cfg.get("database"):
        out.append(f"DATABASE={cfg['database']}")
    if cfg.get("user"):
        out.append(f"UID={cfg['user']}")
        out.append(f"PWD={cfg.get('password') or ''}")
    else:
        out.append("Trusted_Connection=yes")
    if str(cfg.get("trustServerCertificate", "yes")).lower() in ("1", "true", "yes"):
        out.append("TrustServerCertificate=yes")
    return ";".join(out)


# Skill 資料夾裡的連線設定檔（依序尋找）
_SKILL_DB_FILES = ("db.json", os.path.join("config", "connection.json"))


def _skill_conn(skill) -> str:
    for rel in _SKILL_DB_FILES:
        path = os.path.join(skill["dir"], rel)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                return _odbc_conn_str(json.load(f))
        except Exception as e:
            log_error(f"[tools] 讀取 {skill['name']}/{rel} 失敗：{e}")
    return ""


def sql_sources() -> dict:
    """
    目前可查的資料庫來源 = Skill 自帶的設定 + .env 設的來源（同名時 .env 優先）。
    Skill 只要在自己的資料夾放 db.json、SKILL.md 寫 db: 與 tables:，丟進 skills/ 就會生效。
    """
    out = {}
    for skill in skill_loader.get_skills().values():
        name = skill_loader.skill_db_source(skill)
        if not name or not skill["tables"]:
            continue
        if not re.fullmatch(r"[a-z0-9_]+", name):
            log_error(f"[tools] Skill {skill['name']} 的 db 代號不合法：{name}（只能用英數與底線）")
            continue
        conn = _skill_conn(skill)
        if not conn:
            continue                      # 沒有連線設定檔，等 .env 提供（check_sql_sources 會提醒）
        src = out.setdefault(name, {"conn": conn, "tables": [], "deny": [],
                                    "desc": skill["description"], "skill": "", "from": "skill"})
        src["tables"] += skill["tables"]

    for name, env_src in ENV_SQL_SOURCES.items():
        out[name] = dict(env_src, **{"from": "env"})

    # .env 的 DENY 一律套用（就算來源是 Skill 給的，IT 仍可擋表）
    for name, src in out.items():
        deny = _env_deny(name)
        if deny:
            src["deny"] = sorted(set(src.get("deny", [])) | set(deny))
    return out


def _env_deny(name: str):
    raw = os.getenv(f"SQL_{name.upper()}_DENY_TABLES", "")
    return [x.strip() for x in raw.split(",") if x.strip()]


def _pick_source(source: str):
    """
    決定要用哪個資料庫來源。回傳 (來源名稱, 錯誤訊息)
    只有一個來源時可以不指定；多個來源時一定要指定。
    """
    names = list(sql_sources())
    if not names:
        return None, "沒有設定任何唯讀資料庫"
    key = (source or "").strip().lower()
    if not key:
        if len(names) == 1:
            return names[0], ""
        return None, f"請指定 source（可用：{', '.join(names)}）"
    if key not in sql_sources():
        return None, f"沒有這個資料庫來源：{source}（可用：{', '.join(names)}）"
    return key, ""


def _source_skills(source: str):
    """
    哪些 Skill 屬於這個資料庫來源：由 Skill 在 SKILL.md 寫 `db: <來源>`（或取名 db-<來源>）自己宣告，
    IT 不必知道外來 Skill 的名稱。.env 若有設 SQL_<來源>_SKILL，就只認那一個。
    """
    pin = sql_sources().get(source, {}).get("skill")
    if pin:
        s = skill_loader.get_skill(pin)
        if not s:
            log_error(f"[tools] {source} 指定的 Skill 不存在：{pin}")
        return [s] if s else []
    return skill_loader.skills_for_db(source)


def _table_key(name: str):
    """'dbo.CFOrder' → (('dbo','cforder'), 'dbo.CFOrder')；沒寫 schema 視為 dbo"""
    parts = [p.strip("[] ") for p in name.split(".")]
    if len(parts) == 1:
        return ("dbo", parts[0].lower()), parts[0]
    return (parts[-2].lower(), parts[-1].lower()), f"{parts[-2]}.{parts[-1]}"


# `*` 模式：唯讀帳號看得到的表（快取 10 分鐘）
_AUTO_CACHE = {}


def _auto_tables(source: str):
    cache = _AUTO_CACHE.get(source)
    if cache and time.time() - cache["at"] < 600:
        return cache["names"]
    names = []
    try:
        with pyodbc.connect(sql_sources()[source]["conn"], timeout=SQL_TIMEOUT_SEC) as conn:
            cursor = conn.cursor()
            # 只列唯讀帳號真的有 SELECT 權限的表／檢視
            cursor.execute(
                "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES t "
                "WHERE TABLE_TYPE IN ('BASE TABLE', 'VIEW') "
                "AND HAS_PERMS_BY_NAME(QUOTENAME(TABLE_SCHEMA) + '.' + QUOTENAME(TABLE_NAME), "
                "'OBJECT', 'SELECT') = 1 ORDER BY TABLE_SCHEMA, TABLE_NAME"
            )
            names = [f"{r[0]}.{r[1]}" for r in cursor.fetchall()]
    except Exception as e:
        log_error(f"[tools] {source} 自動取得可查表清單失敗：{e}")
        return (cache or {}).get("names", [])
    _AUTO_CACHE[source] = {"names": names, "at": time.time()}
    log_info(f"[tools] {source} 依唯讀帳號權限取得 {len(names)} 張可查的表／檢視")
    return names


def _denied(key, deny_list):
    """拒絕清單：可寫 表名、schema.表名，結尾 * 為前綴比對"""
    schema, table = key
    for d in deny_list:
        d = d.strip().strip("[] ").lower()
        if not d:
            continue
        target = f"{schema}.{table}" if "." in d else table
        if d.endswith("*"):
            if target.startswith(d[:-1]):
                return True
        elif target == d:
            return True
    return False


def _allowed_map(source: str):
    """
    該來源的白名單 → {(schema, table) 小寫: 原始寫法}
    支援三種來源：明列表名、@skill（Skill 自己宣告）、*（唯讀帳號權限）
    """
    src = sql_sources().get(source)
    if not src:
        return {}

    names = []
    for entry in src["tables"]:
        e = entry.strip()
        if e == "*":
            names += _auto_tables(source)
        elif e.lower().startswith("@skill"):
            if ":" in e:                      # @skill:某skill → 只認這一個
                skill = skill_loader.get_skill(e.split(":", 1)[1].strip())
                bound = [skill] if skill else []
            else:
                bound = _source_skills(source)
            if not bound:
                log_error(f"[tools] {source} 設為 @skill，但沒有任何 Skill 宣告 db: {source}")
            for s in bound:
                names += s["tables"]
        else:
            names.append(e)

    out = {}
    for n in names:
        key, display = _table_key(n)
        if not _denied(key, src["deny"]):
            out[key] = display
    return out


def validate_sql(sql: str, source: str = None):
    """
    檢查 LLM 產生的 SQL（白名單依 source 而定）。
    回傳 (True, 要執行的 SQL, [表名]) 或 (False, 拒絕原因, [])
    """
    src, err = _pick_source(source)
    if err:
        return False, err, []

    raw = (sql or "").strip().rstrip(";").strip()
    if not raw:
        return False, "SQL 是空的", []
    if ";" in raw:
        return False, "不允許多個語句", []
    if "--" in raw or "/*" in raw:
        return False, "不允許 SQL 註解", []
    m = _FORBIDDEN_RE.search(raw)
    if m:
        return False, f"不允許的關鍵字：{m.group(0)}", []

    try:
        stmts = [s for s in sqlglot.parse(raw, read="tsql") if s is not None]
    except Exception as e:
        return False, f"SQL 語法無法解析：{e}", []
    if len(stmts) != 1:
        return False, "只允許單一 SELECT 語句", []
    stmt = stmts[0]
    if not isinstance(stmt, (exp.Select, exp.SetOperation)):
        return False, "只允許 SELECT", []

    # 任何寫入類節點都拒絕（包含 SELECT ... INTO）
    for node in stmt.walk():
        if isinstance(node, (exp.Insert, exp.Update, exp.Delete, exp.Merge, exp.Into,
                             exp.Command, exp.Drop, exp.Create, exp.Alter)):
            return False, f"不允許的語法：{type(node).__name__}", []

    # 表白名單（CTE 名稱不算）；每個來源的白名單各自獨立，不能互查
    allowed = _allowed_map(src)
    all_tables = sorted(allowed.values())
    cte_names = {c.alias_or_name.lower() for c in stmt.find_all(exp.CTE)}
    tables = []
    for t in stmt.find_all(exp.Table):
        name = (t.name or "").lower()
        if not name:
            return False, "不支援的資料來源（只能查一般資料表／檢視）", []
        if name in cte_names and not t.db:
            continue
        if t.catalog:
            return False, f"不允許跨資料庫查詢：{t.sql(dialect='tsql')}", []
        key = ((t.db or "dbo").lower(), name)
        if key not in allowed:
            hint = ", ".join(all_tables[:20])
            if len(all_tables) > 20:
                hint += f" …等 {len(all_tables)} 張"
            return False, (
                f"{src} 不在允許清單的表：{key[0]}.{key[1]}（可查：{hint}）。"
                f"若這張表是必要的，請 IT 在 .env 的 SQL_{src.upper()}_TABLES 加入"
            ), []
        tables.append(f"{key[0]}.{key[1]}")

    # 自動加上 / 限縮 TOP
    if isinstance(stmt, exp.Select):
        limit = stmt.args.get("limit")
        try:
            n = int(limit.expression.this) if limit is not None else None
        except Exception:
            n = None
        if n is None or n > SQL_MAX_ROWS:
            stmt = stmt.limit(SQL_MAX_ROWS)

    return True, stmt.sql(dialect="tsql"), sorted(set(tables))


def _json_value(v):
    if isinstance(v, (datetime.datetime, datetime.date, datetime.time)):
        return v.isoformat()
    if isinstance(v, decimal.Decimal):
        return float(v)
    if isinstance(v, (bytes, bytearray)):
        return f"<binary {len(v)} bytes>"
    return v


def sql_query(sql: str, source: str = None) -> dict:
    src, err = _pick_source(source)
    if err:
        return {"ok": False, "items": [], "rejected": True, "note": err, "sql": sql}

    ok, result, tables = validate_sql(sql, src)
    if not ok:
        log_error(f"[tools.sql_query] 拒絕執行（{src}）：{result}｜SQL={sql}")
        return {"ok": False, "items": [], "rejected": True, "note": f"SQL 被拒絕：{result}", "sql": sql, "source": src}

    run_sql = result
    log_info(f"[tools.sql_query] 執行（{src}）：{run_sql}")
    with pyodbc.connect(sql_sources()[src]["conn"], timeout=SQL_TIMEOUT_SEC) as conn:
        conn.timeout = SQL_TIMEOUT_SEC  # 查詢逾時（秒）
        cursor = conn.cursor()
        cursor.execute(run_sql)
        cols = [c[0] for c in cursor.description]
        rows = [[_json_value(v) for v in r] for r in cursor.fetchmany(SQL_MAX_ROWS)]

    # 轉成 Markdown 表格給 LLM 讀
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        lines.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return {
        "ok": True,
        "sql": run_sql,
        "source": src,
        "row_count": len(rows),
        "items": [{
            "source_id": f"SQL-{_short_hash(run_sql)}",
            "source_type": "sql",
            "title": f"{src} 資料庫查詢（{', '.join(tables)}）",
            "text": "\n".join(lines) if rows else "（查無資料）",
        }],
        "note": "" if rows else "查詢成功，但沒有符合條件的資料",
    }


# 白名單各表欄位（從唯讀連線讀 INFORMATION_SCHEMA，快取 10 分鐘）
_SCHEMA_CACHE = {}       # 來源 → {"text", "at"}
_COL_CACHE = {}          # (來源, schema, table) → "欄位(型別), ..."
_SCHEMA_LOCK = threading.Lock()


def _read_columns(cursor, schema, table):
    cursor.execute(
        "SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? ORDER BY ORDINAL_POSITION",
        (schema, table),
    )
    return [f"{r.COLUMN_NAME}({r.DATA_TYPE})" for r in cursor.fetchall()]


def _sql_schema_text(source: str):
    """
    白名單表少（<= SQL_SCHEMA_INLINE_MAX）時：直接把每張表的欄位寫進工具說明。
    表多時（例如整套 PMM 一百多張表）：只列表名，欄位讓模型用 describe_table 現查，
    否則每次請求都要塞進幾萬字的欄位清單。
    """
    amap = _allowed_map(source)
    allowed = sorted(amap)
    if len(allowed) > SQL_SCHEMA_INLINE_MAX:
        names = [amap[k] for k in allowed]
        return (
            f"（共 {len(names)} 張，欄位請先用 describe_table 查）\n"
            + "、".join(names)
        )

    cache = _SCHEMA_CACHE.get(source)
    if cache and time.time() - cache["at"] < 600:
        return cache["text"]
    with _SCHEMA_LOCK:
        lines = []
        try:
            with pyodbc.connect(sql_sources()[source]["conn"], timeout=SQL_TIMEOUT_SEC) as conn:
                cursor = conn.cursor()
                for schema, table in allowed:
                    cols = _read_columns(cursor, schema, table)
                    lines.append(f"- {schema}.{table}：{', '.join(cols) if cols else '（讀不到欄位，可能沒有權限）'}")
        except Exception as e:
            log_error(f"[tools] 讀取 {source} 白名單表結構失敗：{e}")
            lines = [f"- {amap[k]}" for k in allowed]
        _SCHEMA_CACHE[source] = {"text": "\n".join(lines), "at": time.time()}
        return _SCHEMA_CACHE[source]["text"]


def describe_table(table: str, source: str = None) -> dict:
    """查白名單內某張表／檢視的欄位；可一次給多張（逗號分隔）"""
    src, err = _pick_source(source)
    if err:
        return {"ok": False, "items": [], "note": err}

    wanted, unknown = [], []
    allowed = _allowed_map(src)
    for raw in (table or "").split(","):
        parts = [p.strip("[] ").lower() for p in raw.strip().split(".") if p.strip()]
        if not parts:
            continue
        key = ("dbo", parts[0]) if len(parts) == 1 else (parts[-2], parts[-1])
        (wanted if key in allowed else unknown).append(key if key in allowed else raw.strip())
    if not wanted:
        return {"ok": False, "items": [], "note": f"{src} 不在允許清單的表：{', '.join(unknown)}。請改用清單內的表名"}

    items, missing = [], []
    with _SCHEMA_LOCK:
        need = [k for k in wanted if (src,) + k not in _COL_CACHE]
        if need:
            with pyodbc.connect(sql_sources()[src]["conn"], timeout=SQL_TIMEOUT_SEC) as conn:
                cursor = conn.cursor()
                for key in need:
                    _COL_CACHE[(src,) + key] = ", ".join(_read_columns(cursor, *key))
        for key in wanted:
            cols = _COL_CACHE.get((src,) + key)
            name = allowed[key]
            if cols:
                items.append({
                    "source_id": f"SCHEMA-{src}.{name}",
                    "source_type": "schema",
                    "title": f"{src} {name} 欄位",
                    "text": cols,
                })
            else:
                missing.append(name)

    note = ""
    if missing:
        note = f"查不到欄位（表不存在或唯讀帳號沒有權限）：{', '.join(missing)}"
    if unknown:
        note = (note + "；" if note else "") + f"不在允許清單：{', '.join(unknown)}"
    return {"ok": bool(items), "items": items, "note": note}


def _sql_tool_description():
    """多個來源時，每個來源各列一段；並附上該來源指定的 Skill 說明"""
    names = list(sql_sources())
    head = (
        "對公司資料庫執行唯讀查詢，取得即時資料（例如訂單、庫存、出貨狀態）。"
        f"只能寫單一 SELECT（T-SQL），系統會自動限制最多 {SQL_MAX_ROWS} 筆。"
        "不確定欄位名稱時，先用 describe_table 查，不要自己猜。"
    )
    if len(names) > 1:
        head += f"\n有 {len(names)} 個資料庫可查，用 source 參數指定；各資料庫不能互相 JOIN。"

    blocks = []
    for name in names:
        src = sql_sources()[name]
        block = f"\n【source={name}】{src['desc']}\n可查的表：\n" + _sql_schema_text(name)
        for skill in _source_skills(name):      # 該來源的表說明（通常一個）
            if skill["body"]:
                block += "\n" + skill["body"]
        blocks.append(block)

    desc = head + "\n" + "\n".join(blocks)
    # db-query 是共通撰寫規則（各來源自己的說明已在上面）
    used = {s["name"] for n in names for s in _source_skills(n)}
    common = skill_loader.get_skill("db-query")
    if common and common["body"] and common["name"] not in used:
        desc += "\n\n" + common["body"]
    return desc


# =====================================================
# 5) 註冊表
# =====================================================
def _str_param(desc):
    return {"type": "string", "description": desc}


def build_base_tools() -> dict:
    """每次請求呼叫一次（skill / 白名單有變動時自動反映）"""
    tools = {
        "search_qa_kb": {
            "description": "查詢公司 IT QA 知識庫（常見問題與標準答案）。公司內部 IT 問題優先使用。",
            "parameters": {"type": "object", "properties": {"query": _str_param("查詢內容（繁體中文）")}, "required": ["query"]},
            "func": search_qa_kb,
        },
        "search_documents": {
            "description": "查詢公司文件庫（SOP、操作手冊、規範等長文件），結果附文件名稱與章節。",
            "parameters": {"type": "object", "properties": {"query": _str_param("查詢內容（繁體中文）")}, "required": ["query"]},
            "func": search_documents,
        },
        "explore_entity": {
            "description": "在知識圖譜中查某個系統／設備／流程的相關實體與關係，適合追查「A 跟 B 有什麼關係」「X 需要什麼」。",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": _str_param("實體名稱，例如 VPN、FortiClient、ERP"),
                    "hops": {"type": "integer", "description": "擴展層數 1 或 2，預設 1"},
                },
                "required": ["name"],
            },
            "func": explore_entity,
        },
        "load_skill": {
            "description": "載入指定 Skill 的詳細作法（以及它提供的額外工具）。",
            "parameters": {"type": "object", "properties": {"name": _str_param("Skill 名稱")}, "required": ["name"]},
            "func": None,  # agent_node 特別處理
        },
    }
    # 有 Skill 附參考文件時才註冊
    with_refs = [s["name"] for s in skill_loader.get_skills().values()
                 if skill_loader.skill_references(s["name"])]
    if with_refs:
        tools["read_reference"] = {
            "description": (
                "讀 Skill 附帶的參考文件（規格書、對照表等）。"
                f"目前有參考文件的 Skill：{', '.join(with_refs)}。"
                "先不給 file 看有哪些檔案；檔案大就一定要用 keyword 搜尋，不要整份讀。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "skill": _str_param("Skill 名稱"),
                    "file": _str_param("參考文件的相對路徑，例如 references/database-design-spec.md；不給就列出清單"),
                    "keyword": _str_param("只取含這個關鍵字的段落，例如資料表名稱、欄位名稱"),
                    "context": {"type": "integer", "description": "關鍵字前後各取幾行，預設 2"},
                },
                "required": ["skill"],
            },
            "func": read_reference,
        }

    if SERPAPI_API_KEY:
        tools["web_search"] = {
            "description": "Google 網路搜尋。只在公司內部資料查不到，或需要外部／最新公開資訊時使用。",
            "parameters": {"type": "object", "properties": {"query": _str_param("搜尋關鍵字")}, "required": ["query"]},
            "func": web_search,
        }
    if sql_sources():
        names = list(sql_sources())
        # 只有一個來源時不必讓模型指定 source（少一個出錯機會）
        source_param = {}
        if len(names) > 1:
            source_param = {"source": {
                "type": "string",
                "enum": names,
                "description": "要查哪個資料庫：" + "；".join(f"{n}＝{sql_sources()[n]['desc']}" for n in names),
            }}

        sql_props = {"sql": _str_param("單一 SELECT 語句")}
        sql_props.update(source_param)
        tools["sql_query"] = {
            "description": _sql_tool_description(),
            "parameters": {
                "type": "object",
                "properties": sql_props,
                "required": ["sql"] + (["source"] if source_param else []),
            },
            "func": sql_query,
        }

        # 表多的時候欄位不會放進 sql_query 說明，要靠這支現查
        if any(len(_allowed_map(n)) > SQL_SCHEMA_INLINE_MAX for n in names):
            desc_props = {"table": _str_param("表名，可逗號分隔一次查多張，例如 CFOrder,CFOrderDetail")}
            desc_props.update(source_param)
            tools["describe_table"] = {
                "description": "查資料表／檢視的欄位名稱與型別，寫 SQL 前先用它確認欄位，不要自己猜。",
                "parameters": {
                    "type": "object",
                    "properties": desc_props,
                    "required": ["table"] + (["source"] if source_param else []),
                },
                "func": describe_table,
            }
    return tools


def check_sql_sources():
    """
    啟動時印出各 SQL 來源綁了哪些 Skill、實際可查幾張表，並指出兩種落差：
    - Skill 宣告要用、但白名單沒開放的表
    - Skill 宣告要查、但 .env 根本沒設定的資料庫來源（裝了外來 Skill 最常見）
    """
    for name, src in sql_sources().items():
        allowed = _allowed_map(name)
        bound = _source_skills(name)
        where = "Skill 自帶設定" if src.get("from") == "skill" else ".env"
        print(f"  - {name}：{len(allowed)} 張可查（設定來自 {where}）"
              f"{'，Skill：' + ', '.join(s['name'] for s in bound) if bound else '，沒有對應的 Skill'}")
        if src.get("deny"):
            print(f"    - 已擋下：{', '.join(src['deny'])}")
        if not bound:
            print(f"    [注意] 沒有 Skill 宣告 db: {name}，表的中文意義不會出現在工具說明裡")
        for skill in bound:
            missing = [t for t in skill["tables"] if _table_key(t)[0] not in allowed]
            if missing:
                print(f"    [注意] Skill {skill['name']} 宣告但不在白名單的表（{len(missing)} 張）："
                      f"{', '.join(missing[:10])}{'…' if len(missing) > 10 else ''}")
                print(f"      → 檢查 .env 的 SQL_{name.upper()}_TABLES／SQL_{name.upper()}_DENY_TABLES")

    # Skill 要查資料庫，但連線設定還沒放
    sources = sql_sources()
    for skill in skill_loader.get_skills().values():
        want = skill_loader.skill_db_source(skill)
        if want and want not in sources:
            print(f"  [注意] Skill {skill['name']} 要查資料庫「{want}」，但沒有連線設定")
            print(f"      → 把 {skill['name']}/db.json.example 複製成 db.json 並填入連線"
                  f"（或在 .env 設 SQL_SOURCES={want} 由 IT 統一管理）")


def to_openai_tools(registry: dict) -> list:
    return [
        {"type": "function", "function": {"name": name, "description": t["description"], "parameters": t["parameters"]}}
        for name, t in registry.items()
    ]


def run_tool(name: str, args: dict, registry: dict) -> dict:
    """執行工具；任何例外都轉成 ok=False，讓 Agent 自己決定下一步"""
    t = registry.get(name)
    if not t or not t.get("func"):
        return {"ok": False, "items": [], "note": f"沒有這個工具：{name}"}
    try:
        res = t["func"](**(args or {}))
        if not isinstance(res, dict):
            res = {"ok": True, "items": [], "note": str(res)}
        res.setdefault("ok", True)
        res.setdefault("items", [])
        return res
    except TypeError as e:
        return {"ok": False, "items": [], "note": f"參數錯誤：{e}"}
    except Exception as e:
        log_error(f"[tools] {name} 執行失敗：{e}")
        return {"ok": False, "items": [], "note": f"工具執行失敗：{e}"}


def result_to_text(res: dict, max_chars: int = None) -> str:
    """
    工具結果轉 JSON 字串給 LLM；超過長度時平均截斷每個 item 的 text
    """
    max_chars = max_chars or AGENT_TOOL_RESULT_MAX_CHARS
    text = json.dumps(res, ensure_ascii=False, default=str)
    if len(text) <= max_chars:
        return text
    res = json.loads(text)
    items = res.get("items", [])
    overhead = len(json.dumps(dict(res, items=[]), ensure_ascii=False))
    per = max(200, (max_chars - overhead) // max(1, len(items)) - 150)
    for it in items:
        if len(it.get("text", "")) > per:
            it["text"] = it["text"][:per] + "…（截斷）"
    text = json.dumps(res, ensure_ascii=False)
    return text[:max_chars]
