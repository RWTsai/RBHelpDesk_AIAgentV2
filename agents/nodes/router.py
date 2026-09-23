# router.py
"""
Router Node
-------------------------------------
負責判斷訊息類型，讓 LangGraph 知道下一步要走「文字 AI」或「圖片 AI」。

輸入 state（由 input_line.py 已處理後的格式）：
    {
        "message_type": "text" / "image" / ...,
        ...
    }

輸出：
    state["route_type"] = "text" / "image" / "unsupported"
"""

from utils.logger import log_info, log_error


def route_message(state: dict) -> dict:
    """
    根據 state["message_type"] 判斷要用哪個 AI node。

    最終會將：
        state["route_type"]
    設定成：
        - "text"
        - "image"
        - "news"
        - "unsupported"
    """

    msg_type = state.get("message_type")

    log_info(f"[ROUTER] 開始判斷訊息型別：{msg_type}")

    # --------------------------------------------------------
    # 1. 文字訊息 不等於"今日科技新聞"
    # --------------------------------------------------------
    if msg_type == "text" and state.get("message_text") != "今日資訊科技新聞":
        state["route_type"] = "text"
        log_info("[ROUTER] 訊息屬於文字 → route_type = text")
        return state

    # --------------------------------------------------------
    # 2. 圖片訊息
    # --------------------------------------------------------
    if msg_type == "image":
        # ai_image_node 會使用 state["image_id"]
        state["route_type"] = "image"
        log_info("[ROUTER] 訊息屬於圖片 → route_type = image")
        return state

    # --------------------------------------------------------
    # 3. 科技新聞訊息
    # --------------------------------------------------------
    if msg_type == "text" and (state.get("message_text") == "今日資訊科技新聞" or state.get("message_text") == "今日科技新聞"):
        state["route_type"] = "news"
        log_info("[ROUTER] 訊息屬於科技新聞 → route_type = news")
        return state

    # --------------------------------------------------------
    # 3. 不支援的訊息類型
    # --------------------------------------------------------
    log_info(f"[ROUTER] 收到不支援的訊息型別：{msg_type}")
    state["route_type"] = "unsupported"

    return state
