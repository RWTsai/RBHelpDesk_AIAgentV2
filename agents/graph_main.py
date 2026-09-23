# graph_main.py
"""
這支檔案負責定義整張 LangGraph 的流程。

設計重點：
- 不做過度抽象，每個節點就是呼叫我們剛剛寫好的那幾支 node 函式
- state 就用普通的 dict，容易 print / debug
- 目前只處理：
  - LINE 的 text 訊息 → 文字 AI + 向量知識庫
  - LINE 的 image 訊息 → 圖片辨識 AI
  - 其他型別 → 回覆「目前不支援」

 FastAPI / Flask 的 Webhook：
    from agents.graph_main import run_graph_for_line_event
    state = run_graph_for_line_event(line_event)

"""

import time
from typing import Dict, Any

from langgraph.graph import StateGraph, END

# 匯入可用的node 模組
from .nodes import (
    input_line,
    router,
    agent_node,
    ai_image_node,
    reply_line_node,
    news_node,
    human_check_node,
    memory_load_node,
    memory_save_node,

)


# =============================
# 1. 定義「狀態」型別（其實就是 dict）
# =============================


State = Dict[str, Any]


# =============================
# 2. 包一層 node wrapper，給 LangGraph 用
#    （LangGraph 的 node 函式會接 state，回傳 state）
# =============================


def node_input(state: State) -> State:
    """
    Input 節點：
    - 這裡 state 裡面已經有 key: "raw_event"
    - 我們把 raw_event 丟給 input_line.handle 做整理
    """
    raw_event = state.get("raw_event")
    if not raw_event:
        # 這裡理論上不會發生，Webhook 那邊要先處理好
        print("[node_input] 缺少 raw_event")
        return state

    new_state = input_line.handle(raw_event)

    # 把原本 state 的其他東西補回去
    new_state["_meta"] = state.get("_meta", {})
    new_state["_t_start"] = state.get("_t_start", time.time())  # 收到 webhook 的時間（Reply 判斷是否改用 Push）
    return new_state


def node_router(state: State) -> State:
    """呼叫 router.route_message 做類型判斷"""
    return router.route_message(state)

def node_ai_text(state: State) -> State:
    """
    處理文字問題
    To-Be：改走 agent_node（規劃→工具→驗證）；.env AGENT_MODE=off 時 agent_node 內部會退回舊的 ai_text_node
    """
    return agent_node.process_text(state)

def node_ai_image(state: State) -> State:
    """處理圖片問題"""
    return ai_image_node.process_image(state)

def node_reply(state: State) -> State:
    """最後回覆 LINE 使用者"""
    return reply_line_node.reply_user(state)

def node_news(state: State) -> State:
    """處理科技新聞問題"""
    return news_node.process_news(state)

def node_reply_unsupported(state: State) -> State:
    """
    當訊息型別不是 text / image 時，走這條路，
    統一回覆一段「目前不支援」的說明。
    """
    state["reply_text"] = (
        "目前這個 知識助理暫時只支援「文字訊息」與「圖片訊息」，"
        "如果是影片或其他檔案，麻煩改用截圖或文字描述問題，謝謝 🙏"
    )
    return reply_line_node.reply_user(state)


def node_memory_load(state: State) -> State:
    """載入使用者記憶體"""
    return memory_load_node.load_memory(state)

def node_human_check(state: State) -> State:
    """人工客服檢查"""
    return human_check_node.check_memory(state)

def node_memory_save(state: State) -> State:
    """儲存使用者記憶"""
    return memory_save_node.save_memory(state)

# 條件式節點判斷函式(人工客服檢查後決定走向)
def after_human_check(state: State) -> str:
    """
    判斷 HumanCheck 後要走哪條路
    
    Returns:
        "skip": 跳過 AI，直接回覆
        "continue": 繼續走 Router
    """
    if state.get("_skip_ai"):
        return "skip"
    else:
        return "continue"

# =============================
# 3. 建立 Graph
# =============================


def build_graph():
    """
    建立一張 LangGraph StateGraph

    節點流程設計：
    1) Input   : 把 raw_event 整理成統一 state
    2) Router  : 看 route_type 是 text / image / unknown
    3) AI_Text : 若是文字，就進文字 AI
    4) AI_Image: 若是圖片，就進圖片 AI
    5) News    : 若是科技新聞，就進新聞節點
    6) Reply   : AI 結束後，統一走 Reply 回 LINE
    7) Reply_Unsupported: 不支援型別的回覆
    """
    workflow = StateGraph(State)

    # --- 註冊節點 ---
    workflow.add_node("Input", node_input)
    workflow.add_node("Router", node_router)
    workflow.add_node("AI_Text", node_ai_text)
    workflow.add_node("AI_Image", node_ai_image)
    workflow.add_node("AI_News", node_news)
    workflow.add_node("Reply", node_reply)
    workflow.add_node("Reply_Unsupported", node_reply_unsupported)

    # --- 註冊記憶與人工客服節點 --- 
    workflow.add_node("MemoryLoad", node_memory_load)
    workflow.add_node("HumanCheck", node_human_check)
    workflow.add_node("MemorySave", node_memory_save)

    # --- 節點連線 ---
    # 起點：一定先 Input
    workflow.set_entry_point("Input")

    # Input 之後，一定走 MemoryLoad
    workflow.add_edge("Input", "MemoryLoad")
    workflow.add_edge("MemoryLoad", "HumanCheck")

    # HumanCheck 決定是否跳過 AI
    workflow.add_conditional_edges(
        "HumanCheck",
        # 我不喜歡lambda，改用命名函式
        # lambda state: "skip" if state.get("_skip_ai") else "continue",
        after_human_check,
        {
            "skip": "Reply",
            "continue": "Router"
        }
    )

    # # Input 跑完，一定走 Router
    # workflow.add_edge("Input", "Router")

    # Router 之後，根據 state["route_type"] 決定走哪邊
    def route_from_router(state: State) -> str:
        """
        Graph 會根據這個函式回傳的字串，
        決定要走到哪個下一個節點（branch name 要跟下方 edge 名稱對應）
        """
        route_type = state.get("route_type")
        if route_type == "text":
            return "text"
        elif route_type == "image":
            return "image"
        elif route_type == "news":
            return "news"
        else:
            return "unsupported"

    # 依Router 定義的節點回傳結果，決定下一步
    workflow.add_conditional_edges(
        "Router",
        route_from_router,
        {
            "text": "AI_Text",
            "image": "AI_Image",
            "news": "AI_News",
            "unsupported": "Reply_Unsupported",
        },
    )

    # 文字 / 圖片處理完，統一走 Reply
    workflow.add_edge("AI_Text", "MemorySave")
    workflow.add_edge("AI_Image", "MemorySave")
    workflow.add_edge("MemorySave", "Reply")
    workflow.add_edge("AI_News", "Reply")

    # Reply / Reply_Unsupported 都是流程終點
    workflow.add_edge("Reply", END)
    workflow.add_edge("Reply_Unsupported", END)

    # 建立可執行的 graph 物件
    app = workflow.compile()

    return app


# 建立 graph 實例
graph_app = build_graph()


# =============================
# 4. 對外呼叫函式
# =============================


def run_graph_for_line_event(event: Dict[str, Any]) -> State:
    """
    給 Webhook 的入口：

    呼叫方式（例如在 Flask / FastAPI 裡）：
        from agents.graph_main import run_graph_for_line_event
        state = run_graph_for_line_event(line_event)

    :param event: 單一筆 LINE webhook event（已經是 dict）
    :return: 最終 state（含有 reply 的內容）
    """
    # 一開始先把 raw_event 塞進 state，其他先給空
    initial_state: State = {
        "raw_event": event,
        "_t_start": time.time(),
    }

    # graph_app.invoke 執行流程，最後回傳所有 state
    final_state: State = graph_app.invoke(initial_state)
    return final_state
