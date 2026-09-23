# reply_line_node.py
"""
回覆 LINE 訊息
-------------------------------------------
由 LangGraph 最後一站呼叫，負責把 state["reply_text"]
傳回 LINE 使用者。

輸入 state 必須包含：
- reply_token
- reply_text
- user_id    (Push 備援與記錄 Log 用)
- _t_start   (可選，收到 webhook 的時間；To-Be 新增)

To-Be 新增 Push 備援：
- 處理時間超過 LINE_PUSH_FALLBACK_SEC，或沒有 reply_token → 直接改用 Push API
- Reply 失敗且原因是 reply token 無效/過期 → 改用 Push API 再送一次
"""

import time
import requests
from config import LINE_CHANNEL_TOKEN, LINE_REPLY_URL, LINE_PUSH_FALLBACK_SEC
from utils.logger import log_info, log_error
from .utils_line import push_messages


def _build_messages(state: dict) -> list:
    """依 message_type 組 LINE messages"""
    reply_text = state.get("reply_text", "（我沒有找到適合的內容）")
    if state.get("message_type") == "flex":
        return [{
            "type": "flex",
            "altText": "確認真人客服",
            "contents": state.get("reply_flex", {})
        }]
    # LINE 單則文字上限 5000 字
    return [{"type": "text", "text": reply_text[:5000]}]


def reply_user(state: dict) -> dict:
    """統一對 LINE 回覆文字"""

    reply_token = state.get("reply_token")
    reply_text = state.get("reply_text", "（我沒有找到適合的內容）")
    user_id = state.get("user_id", "unknown")

    # 人工模式中 AI 靜默（reply_text 為空字串）→ 不送任何訊息
    if state.get("message_type") != "flex" and not reply_text:
        log_info("[REPLY] reply_text 為空，不回覆")
        return state

    messages = _build_messages(state)
    elapsed = time.time() - state.get("_t_start", time.time())

    # 處理太久或沒有 reply_token → 直接 Push
    if not reply_token or elapsed > LINE_PUSH_FALLBACK_SEC:
        log_info(f"[REPLY] 改用 Push（耗時 {elapsed:.1f}s，reply_token={'有' if reply_token else '無'}）")
        if push_messages(user_id, messages):
            log_info("[REPLY] Push 成功")
        return state

    log_info(f"[REPLY] 回覆給 {user_id}（耗時 {elapsed:.1f}s）：{reply_text}")

    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"replyToken": reply_token, "messages": messages}

    try:
        res = requests.post(LINE_REPLY_URL, json=payload, headers=headers, timeout=10)
        if res.status_code == 200:
            log_info("[REPLY] 回覆成功")
        elif res.status_code == 400 and "reply token" in res.text.lower():
            # reply token 無效或過期 → Push 備援
            log_error(f"[REPLY] reply token 失效，改用 Push：{res.text}")
            push_messages(user_id, messages)
        else:
            log_error(f"[REPLY] LINE 回覆失敗：{res.status_code} {res.text}")
            log_error(f"[REPLY] 回覆內容：{payload}")

    except Exception as e:
        log_error(f"[REPLY] HTTP Error：{e}")

    return state
