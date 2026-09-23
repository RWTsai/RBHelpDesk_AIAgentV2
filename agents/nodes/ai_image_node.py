# ai_image_node.py
"""
AI 圖片辨識節點（GPT-4o Vision）
---------------------------------------------------
流程：

1. 從 state 取得 image_id
2. 用 LINE API 抓取圖片 bytes
3. 呼叫 GPT-4o（Vision 模型）
4. 將描述結果寫入 state["reply_text"]
"""
import base64 
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL_VISION
from .utils_line import fetch_line_image_bytes
from utils.logger import log_info, log_error


client = OpenAI(api_key=OPENAI_API_KEY)


def process_image(state: dict) -> dict:
    """處理圖片訊息。輸入 state 必須包含 message_id。"""

    log_info("[AI_IMAGE] 開始處理圖片訊息")
    log_info(f"[AI_IMAGE] state 內容：{state}")

    image_id = state.get("image_id")


    if not image_id:
        log_error("[AI_IMAGE] 缺少 message id")
        state["reply_text"] = "我沒有收到圖片資訊，可以再傳一次嗎？"
        return state

    # -----------------------------------------
    # 1) 從 LINE 下載圖片 bytes
    # -----------------------------------------
    try:
        img_bytes = fetch_line_image_bytes(image_id)
        log_info("[AI_IMAGE] 成功從 LINE 抓到圖片 bytes")

    except Exception as e:
        log_error(f"[AI_IMAGE] 下載圖片失敗：{e}")
        state["reply_text"] = "我無法取得你的圖片，請再試一次。"
        return state


    # -----------------------------------------
    # 2) 呼叫 GPT-4o Vision 解析圖片
    # -----------------------------------------
    try:

        # load config Knowledge Base 提示語
        from config import (
            SYSROLE_IMAGEPROMPT,
            IMAGE_BASE_PROMPT
        )


        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        gpt_res = client.chat.completions.create(
            model=OPENAI_MODEL_VISION,  # 改讀 .env
            messages=[
                {
                    "role": "system",
                    "content": SYSROLE_IMAGEPROMPT,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": IMAGE_BASE_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"  
                            }
                        }
                    ]
                }
            ]
        )


        reply_raw = gpt_res.choices[0].message.content 
        log_info("[AI_IMAGE] GPT圖片解析完成")

    except Exception as e:
        log_error(f"[AI_IMAGE] GPT-4o Vision 解析錯誤：{e}")
        state["reply_text"] = "AI 無法解析這張圖片，請再試一次。"
        return state

    # -----------------------------------------
    # 3) 完成 → 將結果寫回 state
    # -----------------------------------------
    state["reply_text"] = reply_raw.strip()
    log_info("[AI_IMAGE] 已寫入 state.reply_text")

    return state
