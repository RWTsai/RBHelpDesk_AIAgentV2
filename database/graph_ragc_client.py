# client_graph_rag.py
"""
GraphRAG 版本的資料庫客戶端：
- 專門查詢 IT_KB_Graph 這張表（Triplet 知識庫）
- 支援三種查詢邏輯：
    1) 向量相似度搜尋 (embedding)
    2) 直接查 head / relation / tail
    3) 混合查詢 (先向量 → 再查圖)

此檔案完全符合快速開發風格：
- 中文註解
- 不做過度抽象
- 所有邏輯集中在同一檔案
- 可接受重複 SQL 程式碼
"""

import pyodbc
import numpy as np
import json

from config import (
    MSSQL_CONN_STR,
    RAG_QA_TOP_K,
)
from database.doc_graph_client import search_qa_by_vector

from utils.logger import log_info, log_error


# ================================
# 建立資料庫連線
# ================================
def get_conn():
    """建立 MSSQL 連線"""
    return pyodbc.connect(MSSQL_CONN_STR)


# ================================
# 1) 向量相似度搜尋 Triplet
#    To-Be：改用 doc_graph_client 的記憶體快取（numpy 矩陣一次算完 cosine），
#    不再每次全表掃描 IT_KB_Graph。回傳格式與舊版相同。
# ================================
def search_by_embedding(query_embedding, top_k=None):
    """
    用 cosine similarity 搜尋最相似的 triplet_text。
    IT_KB_Graph.embedding 是 VARBINARY(MAX) → float32 array（快取載入時已轉好）
    """
    try:
        results = search_qa_by_vector(query_embedding, top_k=top_k or RAG_QA_TOP_K)
        log_info(f"[search_by_embedding] 取前 {len(results)} 筆，相似度最高為 {results[0]['similarity'] if results else 'N/A'}")
        return results
    except Exception as e:
        log_error(f"search_by_embedding (快取) 失敗:{str(e)}")
        return []

# ================================
# 2) 依 Triplet 結構查詢
# ================================
def search_by_triplet(Entity1=None, Relation=None, Entity2=None):
    """
    提供依 Entity1(head) / Relation(relation) / Entity2(tail) 的結構化查詢。

    可部分給參數：
        - search_by_triplet(Entity1="RB-Mobile")
        - search_by_triplet(Entity1="RB-Mobile", Relation="需要")
        - search_by_triplet(Entity2="解決方案")
    """


    sql = """
        SELECT TOP 20 RowID,ChunkID,ChunkText,Entity1,Relation,Entity2,Confidence
        FROM IT_KB_Graph
        WHERE 1=1
    """

    params = []

    if Entity1:
        sql += " AND Entity1 = ?"
        params.append(Entity1)

    if Relation:
        sql += " AND Relation = ?"
        params.append(Relation)

    if Entity2:
        sql += " AND Entity2 = ?"
        params.append(Entity2)

    sql += " ORDER BY Confidence DESC"

    log_info(f"[search_by_triplet] SQL: {sql} , Params: {params}")
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [
                {
                "RowID": row.RowID,
                "ChunkID": row.ChunkID,
                "ChunkText": row.ChunkText,
                "Entity1": row.Entity1,
                "Relation": row.Relation,
                "Entity2": row.Entity2,
                "Confidence": row.Confidence
                }
                for row in rows
            ]

    except Exception as e:
        log_error(f"search_by_triplet 失敗:{str(e)}")
        return []


# ================================
# 3) 混合查詢：語意 + 結構
# ================================
def hybrid_search(query_embedding, top_k=None):
    """
    混合查詢：

    Step 1) 先做向量搜尋 → 找最相似的 Triplet
    Step 2) 取出 top1 的 Entity1 / Relation
    Step 3) 再依 Entity1 / Relation 做第二次 DB 結構查詢
    """
    top_results = search_by_embedding(query_embedding, top_k)

    log_info(f"[graph_rag_query] 語意查詢結果：{top_results}")

    if not top_results:
        # 原本回傳 []，呼叫端用 .get() 會出錯；改成空的 dict 結構
        return {"semantic_top_k": [], "structural_matches": []}
    


    top_1 = top_results[0]
    h = top_1.get("Entity1")
    r = top_1.get("Relation")
    t = top_1.get("Entity2")

    # 進一步查詢可能相關的 Triplet
    structure_results = search_by_triplet(Entity1=h, Relation=r,Entity2=t)
    log_info(f"[graph_rag_query] 結構查詢結果：{structure_results}")

    log_info(f"[graph_rag_query] 混合查詢結果：語意 Top {len(top_results)} 筆，結構查詢 {len(structure_results)} 筆")
    # log_info(f"[graph_rag_query] semantic_top_k={top_results} ,structural_matches={structure_results}")

    return {
        "semantic_top_k": top_results,
        "structural_matches": structure_results
    }


# ================================
# graph_rag_query() → 給 ai_text_node 用
# ================================
def graph_rag_query(question_embedding, mode="hybrid"):
    """
    ai_text_node.py 調用入口。

    mode = "semantic"  → 單純語意向量比對
    mode = "struct"    → 結構查詢（需 question 另提供 Entity1/Relation/Entity2）
    mode = "hybrid"    → 推薦：語意 → 結構（GraphRAG）
    """
    if mode == "semantic":
        return search_by_embedding(question_embedding)

    if mode == "struct":
        # 這裡假設 ai_text_node 會提供 structure_query = {head, relation, tail}
        # 若你要自動 LLM 轉 triplet，可再擴充
        return {"error": "struct 模式需要提供結構參數"}

    # 預設用 GraphRAG 混合策略
    return hybrid_search(question_embedding)

