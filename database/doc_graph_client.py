# doc_graph_client.py
"""
文件 GraphRAG 檢索 + 向量記憶體快取（To-Be 新增）
---------------------------------------------------
解決 As-Is「每次查詢都全表掃描、Python 逐筆算 cosine」的問題：
- 啟動時把 IT_KB_Graph（QA）、IT_KB_Chunk（文件）、IT_KB_Entity（實體）的向量
  一次載入成 numpy 矩陣（先做 L2 正規化），查詢時一次矩陣乘法就算完全部 cosine
- 每 RAG_CACHE_REFRESH_SEC 秒檢查一次各表「筆數＋最大 ID/更新時間」，有變才重載

提供給 Agent 工具使用的函式：
- search_qa_by_vector(vec)   → QA 知識庫語意查詢（graph_ragc_client 也改用這個）
- local_search(query)        → 文件 GraphRAG：chunk 向量 + 實體向量 + 1-hop 關係擴展
- explore_entity(name)       → 查某實體的鄰居與關係

風格：module 層級 dict 當快取、不做 class、中文註解。
新表還沒建立（DDL 未執行）時，文件部分自動當作空的，QA 查詢不受影響。
"""

import re
import time
import threading
import unicodedata

import numpy as np
from openai import OpenAI

from config import (
    get_mssql_conn,
    OPENAI_API_KEY,
    OPENAI_MODEL_EMBED,
    RAG_QA_TOP_K,
    RAG_DOC_TOP_K,
    RAG_ENTITY_TOP_K,
    RAG_MIN_SCORE,
    RAG_CACHE_REFRESH_SEC,
)
from utils.logger import log_info, log_error

client = OpenAI(api_key=OPENAI_API_KEY)

# ================================
# 快取本體（module 層級 dict）
# ================================
_CACHE = {
    "loaded": False,
    "last_check": 0.0,
    "signature": None,
    # QA 知識庫（IT_KB_Graph）
    "qa_rows": [],            # list of dict（不含 Embedding）
    "qa_mat": None,           # np.ndarray (N, dim)，已正規化
    # 文件 chunk
    "chunk_rows": [],
    "chunk_mat": None,
    "chunk_index": {},        # ChunkID → chunk_rows 的索引
    # 實體
    "entity_rows": [],
    "entity_mat": None,
    "entity_index": {},       # EntityID → entity_rows 的索引
    "entity_by_norm": {},     # NormName → EntityID
    # 圖：鄰接表與實體→chunk
    "adj": {},                # EntityID → list of relation dict
    "entity_chunks": {},      # EntityID → list of ChunkID
}
_LOCK = threading.Lock()


# ================================
# 共用小工具
# ================================
def norm_name(name: str) -> str:
    """實體名稱正規化：全形轉半形、轉小寫、去掉所有空白（ingest 與查詢共用）"""
    if not name:
        return ""
    s = unicodedata.normalize("NFKC", name)
    s = re.sub(r"\s+", "", s).lower()
    return s[:400]


def decode_vec(data):
    """VARBINARY → float32 陣列（與 .NET Buffer.BlockCopy 格式相同）"""
    if data is None:
        return None
    try:
        return np.frombuffer(data, dtype=np.float32)
    except Exception:
        return None


def encode_vec(vec) -> bytes:
    """float list → VARBINARY bytes"""
    return np.asarray(vec, dtype=np.float32).tobytes()


def embed_texts(texts):
    """批次 embedding，回傳 list of list[float]"""
    if not texts:
        return []
    res = client.embeddings.create(model=OPENAI_MODEL_EMBED, input=texts)
    return [d.embedding for d in res.data]


def _build_matrix(vecs):
    """把多個向量疊成矩陣並做 L2 正規化；維度不一致的會被略過（回傳保留的索引）"""
    if not vecs:
        return None, []
    dims = {}
    for v in vecs:
        if v is not None:
            dims[len(v)] = dims.get(len(v), 0) + 1
    if not dims:
        return None, []
    dim = max(dims, key=dims.get)  # 取最多數的維度
    keep = [i for i, v in enumerate(vecs) if v is not None and len(v) == dim]
    if not keep:
        return None, []
    mat = np.vstack([vecs[i] for i in keep]).astype(np.float32)
    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-9
    return mat / norms, keep


def _normalize_query(vec):
    q = np.asarray(vec, dtype=np.float32)
    return q / (np.linalg.norm(q) + 1e-9)


# ================================
# 快取載入 / 更新檢查
# ================================
def _read_signature(cursor):
    """各表的「筆數＋最大 ID/更新時間」，任何一個變了就重載"""
    sig = []
    cursor.execute("SELECT COUNT_BIG(*), MAX(RowID) FROM IT_KB_Graph")
    sig.append(tuple(cursor.fetchone()))
    for sql in (
        "SELECT COUNT_BIG(*), MAX(ChunkID) FROM IT_KB_Chunk",
        "SELECT COUNT_BIG(*), MAX(UpdatedAt) FROM IT_KB_Entity",
        "SELECT COUNT_BIG(*), MAX(RelationID) FROM IT_KB_Relation",
        "SELECT COUNT_BIG(*), MAX(UpdatedAt) FROM IT_KB_SourceDoc WHERE Status = 'Done'",
    ):
        try:
            cursor.execute(sql)
            sig.append(tuple(cursor.fetchone()))
        except Exception:
            sig.append(None)  # 新表尚未建立
    return tuple(str(x) for x in sig)


def _load_all(cursor):
    """把三類向量與圖結構全部載入（呼叫前已持有 _LOCK）"""
    t0 = time.time()

    # ---------- QA 知識庫 ----------
    cursor.execute("""
        SELECT RowID, DocID, ChunkID, ChunkText, Embedding, Entity1, Relation, Entity2, Confidence
        FROM IT_KB_Graph
        WHERE Embedding IS NOT NULL
    """)
    rows, vecs = [], []
    for r in cursor.fetchall():
        rows.append({
            "RowID": r.RowID, "DocID": r.DocID, "ChunkID": r.ChunkID, "ChunkText": r.ChunkText,
            "Entity1": r.Entity1, "Relation": r.Relation, "Entity2": r.Entity2, "Confidence": r.Confidence,
        })
        vecs.append(decode_vec(r.Embedding))
    mat, keep = _build_matrix(vecs)
    _CACHE["qa_rows"] = [rows[i] for i in keep]
    _CACHE["qa_mat"] = mat

    # ---------- 文件 chunk / 實體 / 關係（新表不存在時清空） ----------
    try:
        cursor.execute("""
            SELECT c.ChunkID, c.DocumentID, c.SectionPath, c.ChunkText, c.Embedding,
                   d.FileName, d.SourceUrl, d.SourceType
            FROM IT_KB_Chunk c
            JOIN IT_KB_SourceDoc d ON d.DocumentID = c.DocumentID
            WHERE d.Status = 'Done' AND c.Embedding IS NOT NULL
        """)
        rows, vecs = [], []
        for r in cursor.fetchall():
            rows.append({
                "ChunkID": r.ChunkID, "DocumentID": r.DocumentID, "SectionPath": r.SectionPath or "",
                "ChunkText": r.ChunkText, "FileName": r.FileName, "SourceUrl": r.SourceUrl or "",
                "SourceType": r.SourceType,
            })
            vecs.append(decode_vec(r.Embedding))
        mat, keep = _build_matrix(vecs)
        _CACHE["chunk_rows"] = [rows[i] for i in keep]
        _CACHE["chunk_mat"] = mat
        _CACHE["chunk_index"] = {row["ChunkID"]: i for i, row in enumerate(_CACHE["chunk_rows"])}

        cursor.execute("SELECT EntityID, Name, NormName, EntityType, Description, Embedding FROM IT_KB_Entity")
        rows, vecs = [], []
        for r in cursor.fetchall():
            rows.append({
                "EntityID": r.EntityID, "Name": r.Name, "NormName": r.NormName,
                "EntityType": r.EntityType or "", "Description": r.Description or "",
            })
            vecs.append(decode_vec(r.Embedding))
        # 實體沒有向量也要保留在名稱索引中（explore_entity 用名稱查）
        _CACHE["entity_by_norm"] = {row["NormName"]: row["EntityID"] for row in rows}
        mat, keep = _build_matrix(vecs)
        all_rows = rows
        _CACHE["entity_rows"] = [all_rows[i] for i in keep]
        _CACHE["entity_mat"] = mat
        _CACHE["entity_index"] = {row["EntityID"]: row for row in all_rows}  # EntityID → row（含無向量者）

        cursor.execute("SELECT SrcEntityID, DstEntityID, Relation, Description, ChunkID FROM IT_KB_Relation")
        adj = {}
        for r in cursor.fetchall():
            rel = {"src": r.SrcEntityID, "dst": r.DstEntityID, "relation": r.Relation,
                   "description": r.Description or "", "chunk_id": r.ChunkID}
            adj.setdefault(r.SrcEntityID, []).append(rel)
            adj.setdefault(r.DstEntityID, []).append(rel)
        _CACHE["adj"] = adj

        cursor.execute("SELECT EntityID, ChunkID FROM IT_KB_EntityChunk")
        ec = {}
        for r in cursor.fetchall():
            ec.setdefault(r.EntityID, []).append(r.ChunkID)
        _CACHE["entity_chunks"] = ec

    except Exception as e:
        log_info(f"[doc_graph] 文件圖譜表尚未就緒，只載入 QA 知識庫：{e}")
        for k in ("chunk_rows", "entity_rows"):
            _CACHE[k] = []
        for k in ("chunk_mat", "entity_mat"):
            _CACHE[k] = None
        for k in ("chunk_index", "entity_index", "entity_by_norm", "adj", "entity_chunks"):
            _CACHE[k] = {}

    _CACHE["loaded"] = True
    log_info(
        f"[doc_graph] 快取載入完成：QA {len(_CACHE['qa_rows'])} 筆、chunk {len(_CACHE['chunk_rows'])} 筆、"
        f"實體 {len(_CACHE['entity_index'])} 個，耗時 {time.time() - t0:.2f}s"
    )


def ensure_cache(force=False):
    """每次查詢前呼叫：第一次會載入；之後每 RAG_CACHE_REFRESH_SEC 秒檢查一次有沒有變動"""
    now = time.time()
    if not force and _CACHE["loaded"] and now - _CACHE["last_check"] < RAG_CACHE_REFRESH_SEC:
        return
    with _LOCK:
        # 取得鎖之後再檢查一次（避免多執行緒同時重載）
        if not force and _CACHE["loaded"] and time.time() - _CACHE["last_check"] < RAG_CACHE_REFRESH_SEC:
            return
        try:
            with get_mssql_conn() as conn:
                cursor = conn.cursor()
                sig = _read_signature(cursor)
                if force or not _CACHE["loaded"] or sig != _CACHE["signature"]:
                    _load_all(cursor)
                    _CACHE["signature"] = sig
        except Exception as e:
            log_error(f"[doc_graph] 快取載入/檢查失敗：{e}")
        finally:
            _CACHE["last_check"] = time.time()


def warmup():
    """app 啟動時在背景執行緒呼叫，讓第一個使用者不用等載入"""
    ensure_cache(force=True)


def is_ready() -> bool:
    """
    向量快取載入完了沒。

    為什麼需要：載入實測要 15～57 秒，而 app.py 是用背景執行緒預熱、Flask 同時就
    開始收請求。這段期間進來的請求會卡在 _LOCK 上等整個載入跑完，整題可能超過 80
    秒、遠超 LINE 的 reply token 視窗，只能改走 Push，Push 再失敗使用者就什麼都
    收不到。所以寧可先用一句話把人擋回來，不要讓他等到訊息消失。
    """
    return bool(_CACHE.get("loaded"))


def _top_k(mat, q, k, min_score):
    """回傳 [(索引, 分數)]，依分數由高到低"""
    if mat is None or k <= 0:
        return []
    if mat.shape[1] != q.shape[0]:
        log_error(f"[doc_graph] 向量維度不符：DB {mat.shape[1]} vs Query {q.shape[0]}")
        return []
    scores = mat @ q
    k = min(k, len(scores))
    idx = np.argpartition(-scores, k - 1)[:k]
    idx = idx[np.argsort(-scores[idx])]
    return [(int(i), float(scores[i])) for i in idx if scores[i] >= min_score]


# ================================
# 1) QA 知識庫語意查詢
# ================================
def search_qa_by_vector(query_vec, top_k=None, min_score=0.0):
    """回傳格式與舊版 search_by_embedding 相同（多一個 similarity）"""
    ensure_cache()
    q = _normalize_query(query_vec)
    hits = _top_k(_CACHE["qa_mat"], q, top_k or RAG_QA_TOP_K, min_score)
    return [dict(_CACHE["qa_rows"][i], similarity=s) for i, s in hits]


# ================================
# 2) 文件 GraphRAG local search
# ================================
def local_search(query: str, top_k=None, query_vec=None):
    """
    流程：
    1. query 向量 → top-k chunk（直接語意命中）
    2. query 向量 → top-k 實體
    3. 從命中實體擴展 1-hop 關係，並把實體出現過的 chunk 也拉進來（分數打 0.9 折）
    4. 合併排序取前 top_k

    回傳：
    {
      "chunks":    [{ChunkID, FileName, SectionPath, SourceUrl, ChunkText, score, via}],
      "entities":  [{EntityID, Name, EntityType, Description, score}],
      "relations": ["A --需要--> B：說明", ...]
    }
    """
    ensure_cache()
    top_k = top_k or RAG_DOC_TOP_K
    result = {"chunks": [], "entities": [], "relations": []}
    if _CACHE["chunk_mat"] is None and _CACHE["entity_mat"] is None:
        return result

    if query_vec is None:
        query_vec = embed_texts([query])[0]
    q = _normalize_query(query_vec)

    # 1) chunk 直接命中
    picked = {}  # ChunkID → (score, via)
    for i, s in _top_k(_CACHE["chunk_mat"], q, top_k, RAG_MIN_SCORE):
        picked[_CACHE["chunk_rows"][i]["ChunkID"]] = (s, "semantic")

    # 2) 實體命中
    ent_hits = _top_k(_CACHE["entity_mat"], q, RAG_ENTITY_TOP_K, RAG_MIN_SCORE)
    rel_lines, seen_rel = [], set()
    for i, s in ent_hits:
        ent = _CACHE["entity_rows"][i]
        eid = ent["EntityID"]
        result["entities"].append({
            "EntityID": eid, "Name": ent["Name"], "EntityType": ent["EntityType"],
            "Description": ent["Description"][:300], "score": round(s, 4),
        })

        # 3) 1-hop 關係
        for rel in _CACHE["adj"].get(eid, [])[:15]:
            key = (rel["src"], rel["dst"], rel["relation"])
            if key in seen_rel:
                continue
            seen_rel.add(key)
            src = _CACHE["entity_index"].get(rel["src"], {}).get("Name", "?")
            dst = _CACHE["entity_index"].get(rel["dst"], {}).get("Name", "?")
            line = f"{src} --{rel['relation']}--> {dst}"
            if rel["description"]:
                line += f"：{rel['description']}"
            rel_lines.append(line)
            # 關係所在的 chunk 也納入
            cid = rel.get("chunk_id")
            if cid and cid not in picked and cid in _CACHE["chunk_index"]:
                picked[cid] = (s * 0.85, f"relation:{ent['Name']}")

        # 實體出現過的 chunk
        for cid in _CACHE["entity_chunks"].get(eid, [])[:5]:
            if cid not in picked and cid in _CACHE["chunk_index"]:
                picked[cid] = (s * 0.9, f"entity:{ent['Name']}")

    # 4) 合併排序
    ranked = sorted(picked.items(), key=lambda x: x[1][0], reverse=True)[:top_k]
    for cid, (s, via) in ranked:
        row = _CACHE["chunk_rows"][_CACHE["chunk_index"][cid]]
        result["chunks"].append(dict(row, score=round(s, 4), via=via))
    result["relations"] = rel_lines[:20]
    return result


# ================================
# 3) 實體探索
# ================================
def explore_entity(name: str, hops: int = 1, max_relations: int = 30):
    """
    依名稱找實體（先正規化完全比對，再找名稱包含，最後用向量），回傳鄰居與關係。
    hops 最多 2，避免結果爆量。
    """
    ensure_cache()
    hops = max(1, min(hops, 2))
    n = norm_name(name)
    eid = _CACHE["entity_by_norm"].get(n)

    if eid is None and n:
        # 名稱包含比對（取最短的，通常最接近）
        cands = [(norm, e) for norm, e in _CACHE["entity_by_norm"].items() if n in norm or norm in n]
        if cands:
            cands.sort(key=lambda x: abs(len(x[0]) - len(n)))
            eid = cands[0][1]

    if eid is None and _CACHE["entity_mat"] is not None:
        hits = _top_k(_CACHE["entity_mat"], _normalize_query(embed_texts([name])[0]), 1, RAG_MIN_SCORE)
        if hits:
            eid = _CACHE["entity_rows"][hits[0][0]]["EntityID"]

    if eid is None:
        return {"found": False, "entity": None, "relations": [], "neighbors": []}

    center = _CACHE["entity_index"].get(eid, {})
    relations, neighbors, seen = [], {}, set()
    frontier, visited = [eid], {eid}
    for _ in range(hops):
        nxt = []
        for cur in frontier:
            for rel in _CACHE["adj"].get(cur, []):
                key = (rel["src"], rel["dst"], rel["relation"])
                if key in seen:
                    continue
                seen.add(key)
                src = _CACHE["entity_index"].get(rel["src"], {})
                dst = _CACHE["entity_index"].get(rel["dst"], {})
                relations.append({
                    "source": src.get("Name", "?"), "relation": rel["relation"], "target": dst.get("Name", "?"),
                    "description": rel["description"], "chunk_id": rel["chunk_id"],
                })
                other = rel["dst"] if rel["src"] == cur else rel["src"]
                if other not in visited:
                    visited.add(other)
                    nxt.append(other)
                    o = _CACHE["entity_index"].get(other, {})
                    neighbors[other] = {"Name": o.get("Name", "?"), "EntityType": o.get("EntityType", ""),
                                        "Description": (o.get("Description") or "")[:200]}
                if len(relations) >= max_relations:
                    break
        frontier = nxt

    # 關係出處（文件名稱）
    for r in relations:
        cid = r.pop("chunk_id", None)
        if cid in _CACHE["chunk_index"]:
            row = _CACHE["chunk_rows"][_CACHE["chunk_index"][cid]]
            r["source_doc"] = f"{row['FileName']}（{row['SectionPath']}）"
            r["chunk_id"] = cid

    return {
        "found": True,
        "entity": {"EntityID": eid, "Name": center.get("Name"), "EntityType": center.get("EntityType"),
                   "Description": center.get("Description")},
        "relations": relations,
        "neighbors": list(neighbors.values())[:20],
    }


def get_chunk(chunk_id):
    """依 ChunkID 取 chunk（給工具組出處用）"""
    ensure_cache()
    i = _CACHE["chunk_index"].get(chunk_id)
    return _CACHE["chunk_rows"][i] if i is not None else None
