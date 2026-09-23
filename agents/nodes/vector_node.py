# vector_node.py
"""
內部知識庫（Supabase 向量表）查詢節點。

職責：
- 連線 Supabase
- 使用 OpenAI Embeddings
- 從 rag_documents 向量表做 similarity search
- 回傳整理好的 context 字串，給 ai_text_node 當提示用

注意：這裡寫得很直白，連線每次都 new，之後要最佳化再重構即可。
"""

from typing import List
import os

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client


def _get_supabase_vector_store() -> SupabaseVectorStore:
    """建立 SupabaseVectorStore 物件（簡單暴力版，每次都重建）"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("缺少 SUPABASE_URL 或 SUPABASE_KEY 環境變數")

    supabase = create_client(url, key)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # 注意：不同版本的 SupabaseVectorStore 建構子可能略有差異
    # 若報錯，請依實際使用的 langchain-community 版本調整參數
    vs = SupabaseVectorStore(
        client=supabase,
        table_name="rag_documents",
        embedding=embeddings,
    )
    return vs


def query_knowledge(question: str, k: int = 3) -> str:
    """
    對向量知識庫做相似度查詢，回傳拼接好的文字 context

    :param question: 使用者問題（自然語言）
    :param k: 要取回的文件數量
    :return: 多筆文件內容拼成的一段文字
    """
    if not question:
        return ""

    print(f"[vector_node] 查詢知識庫，問題：{question}")
    vs = _get_supabase_vector_store()
    docs = vs.similarity_search(question, k=k)

    if not docs:
        print("[vector_node] 知識庫沒有找到相關內容")
        return ""

    contents: List[str] = []
    for i, d in enumerate(docs, start=1):
        # d.page_content 會包含原始文件內容
        contents.append(f"[文件{i}]\n{d.page_content}")

    context = "\n\n".join(contents)
    return context
