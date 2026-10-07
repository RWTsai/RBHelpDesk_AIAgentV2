# app.py
"""
RoyalBase IT HelpDesk AI — Flask 主程式

功能：
- 提供 /line/webhook 給 LINE Messaging API 呼叫
- 接收到的 event 逐筆丟給 LangGraph 的 run_graph_for_line_event()
- 每筆 event 執行後即回覆使用者（reply node 負責呼叫 LINE API）

風格：
- 不做 Service Layer
- 不做過度抽象
- 商業邏輯直接寫在 routes 內
- 適度重複碼先允許（快速迭代）

注意：
- 此檔案目前不做資料庫存取，如需 DB 可在頂部初始化 pyodbc。
"""

import os
import json
from flask import Flask, request, abort
#避免 Flask 啟動時卡住輸出
# 這是因為 Flask 的輸出默認是緩衝的，
import threading
import time
import sys

# 載入 LangGraph 的主流程（你已經建立在 agents/graph_main.py）
from agents.graph_main import run_graph_for_line_event
from agents.nodes.utils_line import verify_line_signature, line_secret_fingerprint
from config import print_config_status, LINE_VERIFY_SIGNATURE
from database import doc_graph_client


app = Flask(__name__)

# ================================
# 1. HEALTH CHECK
# ================================

@app.get("/")
def home():
    return {"status": "ok", "service": "RoyalBase LINE AI Bot"}


# ================================
# 2. LINE Webhook 入口
# ================================

@app.post("/webhook/LINE_IT")  #正式
@app.post("/webhook/line_dev")
def line_webhook():
    """
    這是 LINE 官方會呼叫的 endpoint。

    收到的 JSON 格式為：
    {
        "destination": "xxxx",
        "events": [
            {...event1...},
            {...event2...}
        ]
    }

    我們：
    1. 解析 JSON
    2. 對每個 event 呼叫 LangGraph
    3. Graph 會自動處理 reply
    """

# 測試模擬請求收到的 JSON
    # payload = {
    #     "destination": "xxxx",
    #     "events": [
    #         {
    #             "type": "message",              
    #             "message": {
    #                 "id": "587652291982000198",
    #                 "type": "text",
    #                 "quoteToken": "ioq7urSFySGHr4JoPDduxCDxivg_j2lWUXPFIrQcwvIbG3Tw3tBPm1zO8njMBB9Q6tn8kTfx157vtze3Dxl9rpGcJLZl5RumNUzokPbDxvZRbAyz14McJjgEE8MLKwv2GN9izq0dwaJRxOlafPGr1w",
    #                 "markAsReadToken":"qkBLQAVQ6-eQbGigUWTJw2X4F8hjOJIOWckDcXHlv4PTOIRyW9-AB6k41SBFx4gOAd9nEOaSNMOkF0Zw_hPc2BlZ6ZiMdb2vUxqv0gM2yD-8AhTtlxZrv_kkxbokJgt2ejRWnlOrhr09NOauloAjUHPWxS95uoLqDubxUtUeYsdbrs8j-tgbp9orgDDh0Stgh4LSoZFBoo17CYGieiISeQ",
    #                 "text": "今日科技新聞"
    #             },
    #             "webhookEventId":"01KA0EJM99ZAPZBG4P3GE3VKAZ",
    #             "deliveryContext": 
    #             {
    #             "isRedelivery": "false"
    #             },
    #             "timestamp": 1763099365163,
    #             "source": {
    #                 "type": "user",
    #                 "userId": "Ua549c47176f8d469b15ec4767d34ce7d"
    #             },
    #             "replyToken": "290776f4ad0c489bb9e96b9cd8b4ec80",
    #             "mode": "active"
    #         }
    #     ]
    # }

    # request.json = payload

    print("[Webhook] 收到請求")

    # ---- 驗證 X-Line-Signature ----
    # 這個 endpoint 對網際網路開放（LINE 平台要連得到），沒有其他身分驗證，
    # 所以簽章是唯一能確認「請求真的來自 LINE」的手段。少了它，任何人都能偽造
    # 事件讓機器人查內部知識庫與資料庫，再把答案 push 到自己填的 userId。
    # 必須在 get_json() 之前讀原始 body（get_data 會快取，之後 get_json 仍可用）。
    if LINE_VERIFY_SIGNATURE:
        raw_body = request.get_data()
        sig = request.headers.get("X-Line-Signature", "")
        if not verify_line_signature(raw_body, sig):
            # 原本只印「驗證失敗」，分不出是沒帶標頭、secret 換錯頻道、還是
            # 前面的 IIS 反向代理改過 body。這三種的處理方式完全不同。
            # Content-Length 和實際讀到的長度不一致 → 就是中間層動過 body；
            # 兩者一致但簽章不符 → secret 是另一個頻道的。
            print(f"[Webhook] 簽章驗證失敗，拒絕請求（path={request.path} "
                  f"標頭={'無' if not sig else '有'} "
                  f"body={len(raw_body)} bytes/Content-Length={request.content_length} "
                  f"secret指紋={line_secret_fingerprint()} "
                  f"來源={request.headers.get('X-Forwarded-For') or request.remote_addr}）")
            return "invalid signature", 403

    ## 正式接收請求時使用下面這段程式碼
    try:
        # request.get_json 方法True強制將 body 當作 JSON 解析
        # 當物件根結構爲'{}'時payload型別爲dict,根結構爲陣列[]則爲list
        payload = request.get_json(force=True)
        print(f"[Webhook] 請求內容：{payload}")

    except Exception:
        abort(400, description="Invalid JSON")

    # 檢查payload 中的events 內容是否爲陣列結構,"events": [...]
    events = payload.get("events", [])
    if not events:
        return "no events", 200

    print(f"[Webhook] 收到 {len(events)} 筆事件")

    # 每筆 event 各自獨立處理（符合 LINE 規範）
    # To-Be：Agent 可能要十幾秒，改在背景執行緒處理，webhook 立即回 200，
    #        避免 LINE 等太久判定逾時而重送（重送會造成重複回覆）
    for event in events:
        print(f"\n[Webhook] 處理事件：{json.dumps(event, ensure_ascii=False)}")
        threading.Thread(target=_process_event, args=(event,), daemon=True).start()

    return "ok", 200


def _process_event(event):
    """背景執行單一 event 的 LangGraph 流程"""
    try:
        final_state = run_graph_for_line_event(event)
        print(f"[Webhook] Graph 執行完畢，回覆：{final_state.get('reply_text')}")
    except Exception as e:
        print(f"[Webhook] Graph 執行錯誤：{e}")


# 測試用：直接呼叫
# line_webhook()

# ----- 保證所有 print() 自動 flush，不會卡住輸出 -----
sys.stdout.reconfigure(line_buffering=True)

def heartbeat():
    while True:
        print("[Heartbeat] Agent still alive", flush=True)
        time.sleep(300) # 每5分鐘輸出一次心跳訊息

# 啟動心跳執行緒避免CMD凍結（daemon 表示主程式結束後自動關閉）
threading.Thread(target=heartbeat, daemon=True).start()

# To-Be：啟動時在背景預先載入向量快取，第一個使用者不用等
print_config_status()
try:
    from agents.tools import check_sql_sources
    check_sql_sources()          # 印出各 SQL 來源可查幾張表、Skill 需要但沒開放的表
except Exception as e:
    print(f"[啟動] SQL 來源檢查失敗：{e}")
threading.Thread(target=doc_graph_client.warmup, daemon=True).start()


# ================================
# 3. 啟動 Flask
# ================================
if __name__ == "__main__":
    # 若未設定 FLASK_ENV，預設為 development
    port = int(os.getenv("PORT", 8098))

    print(f"啟動 Flask（port={port}）...")
    app.run(host="0.0.0.0", port=port, debug=True)


