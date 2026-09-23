# memory_save_node.py
import json
from datetime import datetime
from utils.logger import log_info, log_error
from config import get_mssql_conn

def save_memory(state):

    user_id = state.get("user_id")
    mem = state.get("memory", {})

    chat_history = mem.get("chat_history", [])
    reply_text = state.get("reply_text")

    # 新的對話存入歷史
    if reply_text:
        chat_history.append({
            "user": state.get("message_text"),  # 原本讀 state["text"]（不存在）
            "assistant": reply_text,
            "ts": datetime.now().isoformat(),
        })

    # 保留最後 10 輪
    chat_history = chat_history[-10:]

    # 寫入資料庫
    sql = """
        MERGE IT_KB_UserMemory AS T
        USING (SELECT ? AS UserID) AS S
        ON T.UserID = S.UserID
        WHEN MATCHED THEN
            UPDATE SET
                ChatHistory = ?,
                HumanHandling = ?,
                HumanActivatedAt = ?,
                HumanLastMsgAt = ?,
                UpdatedAt = GETDATE()
        WHEN NOT MATCHED THEN
            INSERT(UserID, ChatHistory, 
                   HumanHandling, HumanActivatedAt, HumanLastMsgAt)
            VALUES(?, ?, ?, ?, ?);
    """
    # 配合MERGE語法，需要提供兩組參數
    params = [
        user_id,
        json.dumps(chat_history),
        mem.get("human_handling"),
        mem.get("activated_at"),
        mem.get("last_human_msg_at"),

        user_id,
        json.dumps(chat_history),
        mem.get("human_handling"),
        mem.get("activated_at"),
        mem.get("last_human_msg_at"),
    ]

    try:
        with get_mssql_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
    except Exception as e:
        log_error(f"[node_memory_save] 錯誤：{str(e)}")

    state["memory"]["chat_history"] = chat_history
    return state
