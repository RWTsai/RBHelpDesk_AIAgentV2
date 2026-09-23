# human_check_node.py
"""
真人客服模式的流程控制節點：

功能：
1. 使用者輸入「真人客服」→ human_handling = True
2. 在人工模式中：
   - AI 不回應
   - RAG 不會被使用
   - LangGraph 不進入 Router/AI 處理
   - 所有訊息交給 LINE 官方後台人員處理

3. 自動恢復 AI 模式條件：
   • 超過 15 分鐘人工無回覆
   • 使用者輸入：結束人工 / 回到 AI / 不用人工了


這是 LangGraph 的 early-stop node。
"""

import json
import re
from datetime import datetime, timedelta

from utils.logger import log_info, log_error
from agents.nodes.memory_save_node import save_memory

from config import ARTIFICIAL_TIMEOUT_MINUTES  # 改讀 .env（預設 15 分鐘）


def check_memory(state):
    """
    所有訊息都會先走這裡，確定是否要跳過 AI。
    """
    user_text = state.get("message_text", "")
    mem = state.get("memory", {})

    # 初始化若不存在
    mem.setdefault("human_handling", False)
    mem.setdefault("activated_at", None)
    mem.setdefault("last_human_msg_at", None)

    # 轉人工的關鍵字
    HUMAN_KEYWORDS = r"(真人客服|真人|人工客服|轉人工)"

    # 結束人工的關鍵字
    END_KEYWORDS = r"(結束人工|回到AI|恢復AI|結束真人客服|謝謝)"

    # 系統後台工程師關鍵字
    ENGINEER_CMD_END = r"^/(end|ai|finish)$"

    log_info("[HUMAN_CHECK] 檢查是否進入人工客服模式")

    # load config FLEX_MSG
    from config import (
        LINE_FLEX_BUBBLE_TEXT,
    )

    # ============ 1. 是否觸發人工客服模式 ============
    if re.search(HUMAN_KEYWORDS, user_text):
        
        mem["human_handling"] = True
        mem["activated_at"] = datetime.now()
        mem["last_human_msg_at"] = datetime.now()

        state["memory"] = mem
        # state["reply_text"] = (
        #     "已為你轉接真人客服，請耐心等候資訊部同仁的回覆。\n"
        #     "如果要恢復 AI 模式，請輸入：「結束人工」。"
        # )
        state["reply_flex"] = json.loads(LINE_FLEX_BUBBLE_TEXT)
        state["message_type"]= "flex" 


        state["_skip_ai"] = True  # 不給 AI 回覆

        log_info("[HUMAN_CHECK] 進入人工客服模式，跳過 AI 回覆。")
        
        # 更新資料庫狀態
        save_memory(state)


        return state

    # ============ 2. 如果是人工客服模式 ============
    if mem["human_handling"]:

        # (2-1) 判斷是否超時（自動恢復 AI）
        last = mem.get("activated_at")
        if last:
            delta = datetime.now() - last
            if delta.total_seconds() > ARTIFICIAL_TIMEOUT_MINUTES * 60:
                mem["human_handling"] = False
                state["memory"] = mem
                state["reply_text"] = (
                    "因為同仁可能還在忙碌無暇處理，我已先恢復 AI 模式。\n"
                    "資訊部同仁會再抽空回覆你，再麻煩稍後，請多包涵！"
                )
                # state["message_type"]= "text" 

                log_info("[HUMAN_CHECK] 人工客服模式超時，自動恢復 AI 模式。")
                
                # 寫回資料庫
                state["memory"] = mem
                save_memory(state)
                return state
            else:
                # 更新最後人工訊息時間
                mem["last_human_msg_at"] = datetime.now()
                state["message_type"]= "text" 

        # (2-2) 使用者要求結束人工
        if re.search(END_KEYWORDS, user_text):
            mem["human_handling"] = False
            state["memory"] = mem
            state["reply_text"] = "已為你恢復聰明的助理模式，有什麼需要我協助嗎？😊"
            state["_skip_ai"] = True
            # state["message_type"]= "text" 

            log_info("[HUMAN_CHECK] 使用者結束人工客服模式，恢復 AI 模式。")

            # 寫回資料庫
            state["memory"] = mem
            save_memory(state)


            return state


        # (2-4) 人工模式下 → 不應有 AI 回覆
        state["reply_text"] = ""
        state["_skip_ai"] = True

        # 如果state["message_type"]= "text" 沒有被設定，則設定為 text
        if "message_type" not in state:
            state["message_type"]= "text"

        log_info("[HUMAN_CHECK] 人工客服模式中，跳過 AI 回覆。")

        # 立即寫回資料庫
        save_memory(state)
        return state

    # ============ 3. 非人工模式 → 繼續正常流程 ============
    state["memory"] = mem
    # state["message_type"]= "text"
    return state
