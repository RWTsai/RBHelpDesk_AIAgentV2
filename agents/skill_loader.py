# skill_loader.py
"""
Skill 載入器（To-Be 新增）
---------------------------------------------------
格式（放在 SKILLS_DIR，預設 RBHelpDesk_AIAgent/skills/）：

    skills/
      password-reset/
        SKILL.md      ← 必要：YAML 標頭（name / description / keywords / db / tables）＋本文
        tool.py       ← 選配：TOOLS = {"工具名": {"description", "parameters", "func"}}

機制：
- 漸進揭露：system prompt 只放 name + description（skill_catalog_text）
- 關鍵字直接注入：問題含 keywords 時直接把本文放進 prompt（match_keywords），省一輪 load_skill
- Agent 呼叫 load_skill(name) 時回傳本文，並把 tool.py 的工具加進可用清單
- 每次呼叫 get_skills() 都會比對資料夾修改時間，有變就重載，不用重啟服務

安全：tool.py 是程式碼，只能由 IT 開發人員放到伺服器，不提供網頁上傳。
"""

import os
import re
import threading
import importlib.util

import yaml

from config import SKILLS_DIR
from utils.logger import log_info, log_error

_STATE = {"signature": None, "skills": {}}
_LOCK = threading.Lock()


def _dir_signature():
    """skills 資料夾內所有檔案的（路徑, 修改時間）清單，任何變動都會不同"""
    sig = []
    if not os.path.isdir(SKILLS_DIR):
        return tuple()
    for root, dirs, files in os.walk(SKILLS_DIR):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            if f.endswith((".md", ".py", ".yaml", ".yml")):
                p = os.path.join(root, f)
                try:
                    sig.append((p, os.path.getmtime(p)))
                except OSError:
                    pass
    return tuple(sorted(sig))


def _parse_skill_md(path):
    """解析 SKILL.md：--- YAML 標頭 --- 本文"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    meta, body = {}, text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2]
    return meta, body.strip()


def _load_tool_module(skill_name, path):
    """載入 tool.py，取出 TOOLS dict"""
    mod_name = f"rbit_skill_{skill_name.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tools = getattr(mod, "TOOLS", {}) or {}
    ok = {}
    for tname, t in tools.items():
        if callable(t.get("func")) and isinstance(t.get("parameters"), dict):
            ok[tname] = t
        else:
            log_error(f"[skill] {skill_name}/tool.py 的工具 {tname} 格式不正確（需要 description / parameters / func）")
    return ok


def _scan():
    """掃描全部 skill；單一 skill 壞掉不影響其他 skill"""
    skills = {}
    if not os.path.isdir(SKILLS_DIR):
        log_info(f"[skill] 找不到 SKILLS_DIR：{SKILLS_DIR}")
        return skills

    for d in sorted(os.listdir(SKILLS_DIR)):
        folder = os.path.join(SKILLS_DIR, d)
        md = os.path.join(folder, "SKILL.md")
        if not os.path.isfile(md):
            continue
        try:
            meta, body = _parse_skill_md(md)
            name = str(meta.get("name") or d).strip()
            kw = meta.get("keywords") or []
            if isinstance(kw, str):
                kw = [k.strip() for k in kw.split(",")]
            # tables：Skill 自己宣告會用到的資料表（從外部取得的 Skill 常常只有它自己知道）
            tbl = meta.get("tables") or []
            if isinstance(tbl, str):
                tbl = re.split(r"[,\n]", tbl)
            skill = {
                "name": name,
                "description": str(meta.get("description") or "").strip(),
                "keywords": [str(k).lower() for k in kw if str(k).strip()],
                # db：這個 Skill 要查哪個 SQL 來源（.env 的 SQL_SOURCES 名稱）；沒寫則看名稱是不是 db-<來源>
                "db": str(meta.get("db") or "").strip().lower(),
                "tables": [str(t).strip() for t in tbl if str(t).strip()],
                "body": body,
                "dir": folder,
                "tools": {},
            }
            tool_py = os.path.join(folder, "tool.py")
            if os.path.isfile(tool_py):
                try:
                    skill["tools"] = _load_tool_module(name, tool_py)
                except Exception as e:
                    log_error(f"[skill] 載入 {name}/tool.py 失敗：{e}")
            skills[name] = skill
        except Exception as e:
            log_error(f"[skill] 解析 {md} 失敗：{e}")

    log_info(f"[skill] 已載入 {len(skills)} 個 skill：{list(skills.keys())}")
    return skills


def get_skills():
    """取得全部 skill（資料夾有變動會自動重載）"""
    sig = _dir_signature()
    if sig != _STATE["signature"]:
        with _LOCK:
            if sig != _STATE["signature"]:
                _STATE["skills"] = _scan()
                _STATE["signature"] = sig
    return _STATE["skills"]


def get_skill(name):
    return get_skills().get(name)


def skill_catalog_text():
    """給 system prompt 的清單（只有名稱＋描述）"""
    skills = get_skills()
    if not skills:
        return "（目前沒有 Skill）"
    lines = []
    for s in skills.values():
        extra = f"（附工具：{', '.join(s['tools'].keys())}）" if s["tools"] else ""
        lines.append(f"- {s['name']}：{s['description']}{extra}")
    return "\n".join(lines)


def match_keywords(text):
    """問題文字命中 keywords 的 skill 清單"""
    t = (text or "").lower()
    return [s for s in get_skills().values() if any(k in t for k in s["keywords"])]


# db-query 是各資料庫共通的撰寫規則，不屬於任何來源
RESERVED_DB_SKILL = "db-query"


def skill_db_source(skill):
    """這個 skill 要查哪個 SQL 來源：標頭的 `db:`，或名稱 db-<來源> 的慣例；都沒有就回空字串"""
    if skill["db"]:
        return skill["db"]
    name = skill["name"].strip().lower()
    if name.startswith("db-") and name != RESERVED_DB_SKILL:
        return name[3:]
    return ""


def skills_for_db(source):
    """
    綁到某個 SQL 來源的 skill：標頭寫 `db: <來源>`，或名稱就叫 db-<來源>。
    由 Skill 自己宣告要查哪個資料庫，IT 不必事先知道外來 Skill 的名稱。
    """
    source = (source or "").strip().lower()
    if not source:
        return []
    return [s for s in get_skills().values() if skill_db_source(s) == source]


# Skill 資料夾內可以給 AI 讀的參考文件（只開放純文字類；config/ 與 db.json 有帳密，不開放）
REFERENCE_EXTS = (".md", ".txt", ".csv", ".sql")
_REFERENCE_SKIP_DIRS = {"__pycache__", "config", "logs", ".git"}


def skill_references(name):
    """[(相對路徑, 位元組)]，不含 SKILL.md 本身"""
    s = get_skill(name)
    if not s:
        return []
    out = []
    for root, dirs, files in os.walk(s["dir"]):
        dirs[:] = [d for d in dirs if d.lower() not in _REFERENCE_SKIP_DIRS]
        for f in files:
            if f.lower() == "skill.md" or not f.lower().endswith(REFERENCE_EXTS):
                continue
            path = os.path.join(root, f)
            rel = os.path.relpath(path, s["dir"]).replace("\\", "/")
            try:
                out.append((rel, os.path.getsize(path)))
            except OSError:
                pass
    return sorted(out)


def read_reference(name, rel_path):
    """讀取參考文件內容；路徑限制在該 skill 資料夾內"""
    s = get_skill(name)
    if not s:
        raise ValueError(f"沒有這個 Skill：{name}")
    base = os.path.realpath(s["dir"])
    target = os.path.realpath(os.path.join(base, rel_path))
    if not target.startswith(base + os.sep):
        raise ValueError("不允許讀取 Skill 資料夾以外的檔案")
    if os.path.basename(target).lower() == "skill.md" or not target.lower().endswith(REFERENCE_EXTS):
        raise ValueError(f"不是可讀取的參考文件：{rel_path}")
    if not os.path.isfile(target):
        raise ValueError(f"找不到檔案：{rel_path}")
    with open(target, encoding="utf-8", errors="ignore") as f:
        return f.read()


def skill_tools(name):
    """
    取得某 skill 的工具，名稱加上「skill名__」前綴避免撞名；
    OpenAI 工具名稱只允許英數、底線、連字號，這裡一併轉換。
    """
    s = get_skill(name)
    if not s:
        return {}
    prefix = "".join(c if c.isalnum() or c in "_-" else "_" for c in s["name"])
    return {f"{prefix}__{tname}": t for tname, t in s["tools"].items()}
