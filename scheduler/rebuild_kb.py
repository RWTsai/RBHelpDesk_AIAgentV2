# rebuild_kb.py
"""
重建 RAG 知識庫
- 從 MSSQL 抓取 KB 內容
- 清洗文字
- 切段 (chunk)
- 產生 embedding
- 寫入 Supabase Vector Store

設計原則：
- 單檔案完成
- 不做 class，不做 service layer
- 白話易讀、方便 debug
- 商業邏輯直接寫這裡
"""

import time
from openai import OpenAI
from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL_EMBED,
)
from mssql_client import query
from supabase_client import insert_vector, delete_all
from text_cleaner import clean_basic, split_for_embedding
from logger import log_info, log_error


# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)


def rebuild_kb():
    """主流程：重建 Supabase RAG 知識庫"""

    log_info("開始重建知識庫...")

    # Step 1: 清空 table
    try:
        delete_all("rag_documents")
        log_info("已清空 rag_documents 資料表")
    except Exception as e:
        log_error(f"清空資料表失敗：{e}")
        return

    # Step 2: 從 MSSQL 讀取 KB 內容
    sql = """
    SELECT DocID, Instruction, InputText, OutputText, SourceKey
    FROM IT_KB_Document
    ORDER BY DocID
    """

    try:
        rows = query(sql)
        log_info(f"已取得 {len(rows)} 筆 KB 資料")
    except Exception as e:
        log_error(f"MSSQL 查詢失敗：{e}")
        return

    # Step 3: 逐筆處理寫入 Supabase
    for row in rows:
        doc_id = row["DocID"]

        # 合併內容
        raw_text = f"""
        Instruction: {row.get('Instruction', '')}
        InputText: {row.get('InputText', '')}
        OutputText: {row.get('OutputText', '')}
        """

        # 清洗 text
        clean_text = clean_basic(raw_text)

        # 切成 chunks（避免 embedding 太長）
        chunks = split_for_embedding(clean_text)

        for idx, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_{idx}"

            try:
                # Step 4: 產生 embedding
                embed = client.embeddings.create(
                    model=OPENAI_MODEL_EMBED,
                    input=chunk
                )

                vector = embed.data[0].embedding

            except Exception as e:
                log_error(f"產生 embedding 失敗 DocID={doc_id}, error={e}")
                continue

            # Step 5: 寫入 Supabase
            record = {
                "id": chunk_id,
                "content": chunk,
                "embedding": vector,
                "metadata": {
                    "DocID": doc_id,
                    "SourceKey": row.get("SourceKey", ""),
                }
            }

            try:
                insert_vector("rag_documents", record)
                log_info(f"已寫入 chunk DocID={doc_id}, chunk={idx}")

            except Exception as e:
                log_error(f"寫入 Supabase 失敗 DocID={doc_id}, chunk={idx}, error={e}")

        time.sleep(0.3)  # 保護 OpenAI API（避免流量爆衝）

    log_info("知識庫重建完成！")


if __name__ == "__main__":
    rebuild_kb()
