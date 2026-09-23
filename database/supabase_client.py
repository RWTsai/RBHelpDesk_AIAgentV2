# supabase_client.py
"""
Supabase 客戶端（簡化版）
- 專門提供向量寫入與查詢
- 不做過度封裝，只提供最常用的 2~3 個功能
- 所有商業邏輯寫在 vector_node.py，不寫在這裡
"""

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client, Client


# 初始化 supabase client（整個專案共享）
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_vector(table: str, record: dict):
    """
    插入向量資料：
    record 範例：
    {
        "id": "abc",
        "content": "...",
        "embedding": [0.1, 0.2, ...],
        "metadata": {}
    }
    """

    try:
        result = supabase.table(table).insert(record).execute()
        return result.data

    except Exception as e:
        print(f"[supabase_client] insert_vector 失敗: {e}")
        raise


def query_vector(table: str, query_embedding: list, limit: int = 5):
    """
    使用向量查詢（match_documents）。
    - query_embedding：OpenAI embedding list
    - limit：取幾筆最相關資料
    """

    try:
        response = (
            supabase.rpc(
                "match_documents",
                {
                    "query_embedding": query_embedding,
                    "match_count": limit
                }
            )
            .execute()
        )

        return response.data

    except Exception as e:
        print(f"[supabase_client] query_vector 失敗: {e}")
        raise


def delete_all(table: str):
    """
    清空 vector table（類似 n8n 裡的 deleteTable）
    """

    try:
        result = supabase.table(table).delete().neq("id", "").execute()
        return result.data

    except Exception as e:
        print(f"[supabase_client] 無法清除資料表 {table}: {e}")
        raise
