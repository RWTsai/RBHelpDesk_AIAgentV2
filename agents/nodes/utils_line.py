# utils_line.py
"""
LINE API 工具方法
- 提供圖片下載、簽名驗證等常用功能
- 不做 class、不抽象化
- 所有功能都是白話易讀的函式
"""

import hmac
import hashlib
import base64
import requests

from config import LINE_CHANNEL_TOKEN, LINE_CHANNEL_SECRET
from utils.logger import log_info, log_error


def fetch_line_image_bytes(message_id: str) -> bytes:
    """
    下載 LINE 使用者傳來的圖片（回傳 bytes）
    - message_id：LINE event 裡的 message.id
    - 會自動加上 Authorization: Bearer {token}

    LINE API：
    GET https://api-data.line.me/v2/bot/message/{messageId}/content
    """

    if not message_id:
        log_error("fetch_line_image_bytes(): 未提供 message_id")
        return None

    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"

    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            log_error(f"LINE 圖片下載失敗 status={response.status_code}")
            return None

        log_info(f"LINE 圖片下載成功 message_id={message_id}")
        return response.content  # ← 回傳 byte array（給 AI 模型用）

    except Exception as e:
        log_error(f"LINE 圖片下載錯誤: {e}")
        return None


def verify_line_signature(body: bytes, signature: str) -> bool:
    """
    驗證 LINE Webhook 的 X-Line-Signature。
    - body：原始 request.data
    - signature：request.headers['X-Line-Signature']

    Flask 用法範例：
        if not verify_line_signature(request.data, request.headers.get("X-Line-Signature", "")):
            return "invalid signature", 403
    """

    if not signature:
        log_error("verify_line_signature(): signature 空值")
        return False

    try:
        hash_value = hmac.new(
            LINE_CHANNEL_SECRET.encode("utf-8"),
            body,
            hashlib.sha256
        ).digest()

        computed_signature = base64.b64encode(hash_value).decode("utf-8")

        return computed_signature == signature

    except Exception as e:
        log_error(f"LINE signature 驗證失敗: {e}")
        return False


# ================================
# To-Be 新增：loading 動畫、Push 訊息
# ================================
def start_loading(user_id: str, seconds: int = None) -> None:
    """
    顯示「對方輸入中」loading 動畫（只支援一對一聊天）。
    POST https://api.line.me/v2/bot/chat/loading/start
    loadingSeconds 必須是 5 的倍數、最多 60；送出回覆後動畫會自動消失。
    """
    from config import LINE_LOADING_URL, LINE_LOADING_SECONDS

    if not user_id:
        return
    sec = seconds or LINE_LOADING_SECONDS
    sec = max(5, min(60, int(sec) // 5 * 5))
    try:
        requests.post(
            LINE_LOADING_URL,
            json={"chatId": user_id, "loadingSeconds": sec},
            headers={"Authorization": f"Bearer {LINE_CHANNEL_TOKEN}", "Content-Type": "application/json"},
            timeout=5,
        )
    except Exception as e:
        log_error(f"[LINE] loading 動畫失敗（不影響回覆）：{e}")


def push_messages(user_id: str, messages: list) -> bool:
    """
    主動推播（reply token 失效或處理太久時的備援）。
    POST https://api.line.me/v2/bot/message/push
    注意：Push 會計入 LINE 官方帳號的訊息則數。
    """
    from config import LINE_PUSH_URL

    if not user_id:
        log_error("[LINE] push 缺少 user_id")
        return False
    try:
        res = requests.post(
            LINE_PUSH_URL,
            json={"to": user_id, "messages": messages},
            headers={"Authorization": f"Bearer {LINE_CHANNEL_TOKEN}", "Content-Type": "application/json"},
            timeout=10,
        )
        if res.status_code != 200:
            log_error(f"[LINE] push 失敗：{res.status_code} {res.text}")
            return False
        return True
    except Exception as e:
        log_error(f"[LINE] push HTTP Error：{e}")
        return False
