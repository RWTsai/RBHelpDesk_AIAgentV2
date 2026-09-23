# input_line.py
"""
解析 LINE Webhook Event
- 從 raw_event 中擷取關鍵欄位
- 統一整理成 state 字典格式
- 供後續 LangGraph nodes 使用

採用完全白話風格、單檔案寫完全部流程。
"""

from utils.logger import log_info, log_error


def handle(raw_event: dict) -> dict:
    """
    將 LINE event 轉換成統一的 state 格式。

    輸入：Webhook 單一筆 event（dict）
    輸出：state（dict）
    """

    log_info("[INPUT] 開始解析 LINE event")

    state = {
        "raw_event": raw_event,   # 保留原始資料
        "message_type": None,     # 文字 or 圖片 or 其他
        "message_text": None,     # 若為文字
        "image_id": None,         # 若為圖片 message id
        "user_id": None,
        "reply_token": None,
    }

    # --- 使用者 ID ---
    try:
        state["user_id"] = raw_event["source"]["userId"]
    except Exception:
        log_error("[INPUT] 解析 userId 失敗")
        state["user_id"] = None

    # --- replyToken ---
    state["reply_token"] = raw_event.get("replyToken")

    # --- message 內容 ---
    message = raw_event.get("message", {})

    msg_type = message.get("type")
    state["message_type"] = msg_type  # text / image / sticker / video...

    # ------ 文字訊息 ------
    if msg_type == "text":
        state["message_text"] = message.get("text", "")
        log_info(f"[INPUT] 收到文字訊息：{state['message_text']}")

    # ------ 圖片訊息 ------
    elif msg_type == "image":
        state["image_id"] = message.get("id")
        state["message_text"] = ""
        log_info(f"[INPUT] 收到圖片訊息 messageId={state['image_id']}")

    # ------ 其他型別 ------
    else:
        state["message_text"] = ""
        log_info(f"[INPUT] 收到不支援的訊息型別：{msg_type}")

    log_info("[INPUT] LINE event 解析完成")
    return state
