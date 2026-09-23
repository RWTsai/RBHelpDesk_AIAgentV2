# memory_load_node.py
import json
from utils.logger import log_info, log_error
from config import get_mssql_conn

def load_memory(state):
    user_id = state.get("user_id")

    sql = """
        SELECT TOP 1
            ChatHistory, 
            HumanHandling, HumanActivatedAt, HumanLastMsgAt
        FROM IT_KB_UserMemory
        WHERE UserID = ?
    """

    try:
        with get_mssql_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, user_id)
            row = cursor.fetchone()

        if row:
            state["memory"] = {
                "chat_history": json.loads(row.ChatHistory or "[]"),
                "human_handling": bool(row.HumanHandling),
                "activated_at": row.HumanActivatedAt,
                "last_human_msg_at": row.HumanLastMsgAt,
            }
        else:
            state["memory"] = {
                "chat_history": [],
                "human_handling": False,
            }

        return state

    except Exception as e:
        log_error(f"[node_memory_load] 錯誤：{str(e)}")

        state["memory"] = {}
        return state
