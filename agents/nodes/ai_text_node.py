# ai_text_node.py
"""
AI 文字訊息處理節點（GPT + RAG）
---------------------------------------------------
此 node 的流程：

1. 從 state 取得使用者文字 → state["message_text"]
2. 清洗文字,產生三元組 Triplet
3. 產生 embedding
4. 用 embedding 查 MSSQL 向量知識庫
5. 組合 Prompt（包含：問題 + 相關知識）
6. 呼叫 GPT
7. 將回答寫入 state["reply_text"]
"""

from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL_EMBED, OPENAI_MODEL_CHAT, OPENAI_MODEL_EXTRACT
from database.graph_ragc_client import graph_rag_query
from utils.text_cleaner import clean_basic, clean_ai_reply
from utils.openai_compat import parse_structured
from utils.logger import log_info, log_error


# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

# load config Knowledge Base 提示語
from config import (
    SYSROLE_PROMPT,
    SYSTEM_BASE_PROMPT,
    KNOWLEDGE_BASE_PROMPT,
    TRIPLE_EXTRACTION_PROMPT
)


def process_text(state: dict) -> dict:
    """
    主流程：
    1. 取得使用者輸入
    2. 取得記憶 chat_history / preferences
    3. GraphRAG 搜尋內部知識
    4. 組合 prompt
    5. GPT 回覆
    """


    log_info("[AI_TEXT] 開始處理文字訊息")




    user_text = state.get("message_text", "").strip()

    if not user_text:
        log_error("[AI_TEXT] message_text 是空值")
        state["reply_text"] = "我沒有收到文字訊息，可以再傳一次嗎？"
        return state

    user_id = state.get("user_id")
    memory = state.get("memory", {})

    # ========== 1. 讀出記憶 ==========
    history = memory.get("chat_history", [])


    # 將歷史對話轉人類可讀格式
    history_str = ""
    for h in history[-10:]:  # 保留10輪
        history_str += (
            f"User：{h.get('user')}\n"
            f"Assistant：{h.get('assistant')}\n"
        )

    
    # -----------------------------------------
    # 1) 基本清洗
    # -----------------------------------------
    clean_text = clean_basic(user_text)
    log_info(f"[AI_TEXT] 使用者輸入：{clean_text}")


    # -----------------------------------------
    # 1.1) 將使用者訊息萃取三元組Triplet
    # -----------------------------------------

    triples = tripleExtractService(clean_text)
    triple_texts = [triple_dict_to_text(t) for t in triples]

    # 若沒有抽到 triples 就 fallback 使用 原使用者問題clean_text
    if not triple_texts:
        triple_texts = [clean_text]





    # -----------------------------------------
    # 2) 產生 embedding（用於 RAG 查詢）
    #    20251025 新增使用者問題三元組進行查詢
    # -----------------------------------------
    # log_info(f"[DEBUG] 使用的模型: {OPENAI_MODEL_EMBED}") 

    # try:
    #     embed = client.embeddings.create(
    #         model= OPENAI_MODEL_EMBED, 
    #         input=clean_text
    #     )
    #     query_vector_data = embed.data[0].embedding

    # except Exception as e:
    #     log_error(f"[AI_TEXT] Embedding 失敗：{e}")
    #     state["reply_text"] = "我在理解你的問題時遇到錯誤，可以稍後再試試嗎？"
    #     return state

    try:
        embed = client.embeddings.create(
            model=OPENAI_MODEL_EMBED,
            input=triple_texts
        )

        query_vector_data = [item.embedding for item in embed.data]

    except Exception as e:
        log_error(f"[AI_TEXT] Embedding 多筆失敗：{e}")
        state["reply_text"] = "我在理解你的問題時遇到錯誤，可以稍後再試試嗎？"
        return state


    log_info(f"[AI_TEXT] 文字處理完成階段 2：產生 問題Embedding...")

    # -----------------------------------------
    # 3) 查詢向量知識庫
    # -----------------------------------------

    
    
    all_results = []  

    # 20251125新增多筆向量查詢
    try:
        for vec in query_vector_data:
            kb_results = graph_rag_query(vec, mode="hybrid")

            # 取 semantic / structural 結果
            semantic_results = kb_results.get("semantic_top_k", [])
            structural_results = kb_results.get("structural_matches", [])

            # 合併
            all_results.extend(semantic_results)
            all_results.extend(structural_results)

            log_info(
                f"[AI_TEXT] 單筆 Triplet 查詢：semantic {len(semantic_results)} 筆, structural {len(structural_results)} 筆"
            )

        log_info(f"[AI_TEXT] 全部 GraphRAG 查詢完成，共 {len(all_results)} 筆知識命中")

    except Exception as e:
        log_error(f"[AI_TEXT] GraphRAG 查詢失敗：{e}")
        all_results = []

    # all_results 內容為多筆多來源查詢延伸後的 dict list
    unique = {}

    for r in all_results:
        rid = r.get("RowID")             # ← 最安全唯一 key
        if rid is None:
            continue
        unique[rid] = r                  # 若有重複，自然覆蓋

    # 去重後的列表
    final_results = list(unique.values())

    # # 單筆查詢多向量
    # try:
    #     kb_results = graph_rag_query(query_vector_data, mode="hybrid")
        
    #     #取出實際的結果列表,包含語意(semantic_top_k)和結構化(structural_matches)結果
    #     semantic_results = kb_results.get("semantic_top_k", [])
    #     structural_results = kb_results.get("structural_matches", [])
        
    #     # 合併兩種結果
    #     all_results = semantic_results + structural_results
        
    #     log_info(f"[AI_TEXT] 知識庫查詢結果：語意 {len(semantic_results)} 筆，結構 {len(structural_results)} 筆")


    # except Exception as e:
    #     log_error(f"[AI_TEXT] RAG 查詢失敗：{e}")
    #     kb_results = []


    # 組成 Knowledge 文本
    kb_text = ""

    if final_results:
        # 分離三元組和原始文本
        triplets = []
        chunks = []
        
        for item in final_results:
            # 提取三元組資訊
            entity1 = item.get('Entity1', '')
            relation = item.get('Relation', '')
            entity2 = item.get('Entity2', '')
            
            # 如果有完整的三元組，加入列表
            if entity1 and relation and entity2:
                triplets.append(f"{entity1} {relation} {entity2}")
            
            # 提取原始文本
            chunk_text = item.get('ChunkText', '').strip()
            if chunk_text and chunk_text not in chunks:  # 避免重複
                chunks.append(chunk_text)
        
        # 組合知識文本
        if triplets or chunks:
            kb_text = "以下是系統中找到的相關事實（請依照這些事實回答）：\n\n"
            
            # 加入三元組
            if triplets:
                kb_text += "[事實三元組]\n"
                for i, triplet in enumerate(triplets, 1):
                    kb_text += f"{i}. {triplet}\n"
                kb_text += "\n"
            
            # 加入原始知識來源
            if chunks:
                kb_text += "[原始知識來源]\n"
                for chunk in chunks:
                    kb_text += f"- {chunk}\n"
        else:
            kb_text = "（知識庫沒有找到相關資訊）"
    else:
        kb_text = "（知識庫沒有找到相關資訊）"

    log_info(f"[AI_TEXT] 知識庫內容：{kb_text}")



    log_info(f"[AI_TEXT] 使用者問題三元組：{triple_texts}" )

    # -----------------------------------------
    # 4) 呼叫 GPT
    # -----------------------------------------

    try:
        prompt = f"""{SYSTEM_BASE_PROMPT}

            【使用者問題】
            {clean_text}

            【使用者問題三元組】
            {triple_texts}

            [歷史對話]
            {history_str}

            [公司知識庫]
            {kb_text}

            【回答要求】
            1. 優先參考「事實三元組」中的結構化知識
            2. 結合「原始知識來源」提供完整的操作步驟
            3. 語氣要專業但友善，避免使用過於技術性的術語
            4. 直接給出解決方案，不需要說明推論過程
            5. {KNOWLEDGE_BASE_PROMPT}

            所有沒有找到知識庫內容時，也請用你自身知識協助回答，但避免捏造內部知識庫資料。
            當回覆內容較多或涉及步驟、多個重點時，請務必以分點、分段的方式呈現。可以使用編號、項目符號來條列說明，並適當運用空行與小標題來組織內容，以提升可讀性。
            請開始你的回答："""

        gpt_res = client.chat.completions.create(
                model=OPENAI_MODEL_CHAT,  # 改讀 .env
                messages=[
                    {"role": "system", "content": SYSROLE_PROMPT},
                    {"role": "user", "content": prompt}
                 ]
                #  5.1不使用溫度
                # ,temperature=0.2
        )

        
        reply_raw = gpt_res.choices[0].message.content

        log_info(f"[AI_TEXT] GPT 生成回覆OK")

    except Exception as e:
        log_error(f"[AI_TEXT] GPT 錯誤：{e}")
        state["reply_text"] = "AI 回覆時發生問題，請稍後再試。"
        return state

    # -----------------------------------------
    # 5) 清洗 AI 回覆
    # -----------------------------------------
    # reply_text = clean_ai_reply(reply_raw)
    reply_text = reply_raw

    # 寫回 state
    state["reply_text"] = reply_text
    log_info("[AI_TEXT] 文字處理完成寫回state。")

    # 對話記憶統一由 MemorySave 節點寫入（原本這裡也 append 一次，會造成重複）


    return state
# =============================

from pydantic import BaseModel, Field  
from typing import List  
class Triple(BaseModel):
    """外部類別：定義資料結構三元組結構"""
    Entity1: str = Field(description="主體實體", alias="entity1") 
    Relation: str = Field(description="關係", alias="relation")
    Entity2: str = Field(description="客體實體", alias="entity2")

    """內部類別：配置外部類別的行為"""
    class Config:
        populate_by_name = True  # 允許使用 alias 解析

class TripleExtractionResponse(BaseModel):
    """三元組抽取的回應結構"""
    triples: List[Triple] = Field(description="抽取的三元組列表")

def tripleExtractService(text: str) -> dict:
    """
    呼叫 LLM進行三元組抽取
    """

    trip_prompt = TRIPLE_EXTRACTION_PROMPT
     
    try:

        prompt = trip_prompt.replace("*user_question*", text)
        gpt_res = parse_structured(
            client,
            model=OPENAI_MODEL_EXTRACT,  # 改讀 .env
            messages=[
                {"role": "system", "content": "你是一個企業級 IT HelpDesk 智能助理，負責將使用者的問題轉換成可搜尋的結構化查詢"},
                {"role": "user", "content": prompt}
            ],
            response_format=TripleExtractionResponse
                       
                )
        log_info(f"[AI_TEXT] Triple Extract 回覆:{gpt_res}")
        
        # reply_raw = gpt_res.choices[0].message.content
        reply_raw = gpt_res.choices[0].message.parsed

        if reply_raw is None or not reply_raw.triples:
            log_info("[AI_TEXT] 未抽取到問題的三元組")
            return []

        
        log_info(f"[AI_TEXT] Triple Extract 回覆內容：{reply_raw}")
        # 轉成 dict
        triplet_list = [
            {
                "Entity1": tri.Entity1,
                "Relation": tri.Relation,
                "Entity2": tri.Entity2
            }
            for tri in reply_raw.triples
        ]

        return triplet_list

    except Exception as e:
        log_error(f"[AI_TEXT] Triple Extract 錯誤：{e}")

        return []

def triple_dict_to_text(tri: dict) -> str:
    """
    將三元組 dict 轉成自然語言，適合做 embedding：
    {Entity1, Relation, Entity2} → "Entity1 Relation Entity2"
    """
    h = tri.get("Entity1", "").strip()
    r = tri.get("Relation", "").strip()
    t = tri.get("Entity2", "").strip()

    # 若 tail 為空就不要加
    if t:
        return f"{h} {r} {t}"
    else:
        return f"{h} {r}".strip()


# graph_main.py