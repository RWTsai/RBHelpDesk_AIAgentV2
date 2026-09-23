# 🧩 RoyalBase IT HelpDesk AI — LangGraph 版本

這是以 **LangGraph** 框架重構的 RoyalBase IT HelpDesk AI 助理。
它將原本在 **n8n.io** 平台上運行的多節點工作流（Webhook、AI Agent、向量查詢、新聞搜尋、圖片辨識、回覆等）
改寫為可維護、可測試、可追蹤的 Python 程式架構，
同時保留所有原有功能：LINE 聊天互動、知識庫檢索、AI 推理與圖片辨識。

## 🧠 為什麼改用 LangGraph？

| 功能層面 | n8n 版本 | LangChain 版本 | LangGraph 版本（本方案） |
|-----------|-----------|----------------|----------------------------|
| 工具調用流程 | 節點可視化但難自定義 | 自動 chain，但黑箱難控 | 明確圖式流程（Graph） |
| 多工具協作 | 節點連線複雜 | 需人工控制順序 | Graph 自動管理節點依賴 |
| 對話記憶 | 外部 node | Memory 物件 | Graph state 內建 |
| 錯誤處理 | 節點層控制 | try/except | 節點重試 + 狀態回復 |
| 擴充性 | 需複製 workflow | 修改 Graph 結構即可 | ✅ 高擴充、易除錯 |

## 📦 專案架構

```bash
rb_it_helpdesk/
├── app.py                # 主入口：FastAPI Webhook server
├── config.py             # API Keys, DB 連線
├── agents/
│   ├── graph_main.py     # LangGraph 主流程控制
│   ├── nodes/
│   │   ├── input_line.py       # 接收 LINE webhook
│   │   ├── router.py           # 訊息類型判斷
│   │   ├── ai_text_node.py     # 一般文字問題處理
│   │   ├── ai_image_node.py    # 圖片辨識處理
│   │   ├── vector_node.py      # 內部知識庫查詢
│   │   ├── news_node.py        # 新聞查詢工具
│   │   ├── google_node.py      # Google 搜尋工具
│   │   └── reply_line_node.py  # 回覆 LINE 訊息
├── database/
│   ├── mssql_client.py
│   └── supabase_client.py
├── scheduler/
│   └── rebuild_kb.py
├── utils/
│   ├── text_cleaner.py
│   └── logger.py
└── requirements.txt
```

## 🧰 環境設定（Anaconda）

```bash
conda create -n rb_helpdesk python=3.10
conda activate rb_helpdesk
pip install -r requirements.txt
```

### 📋 requirements.txt

```text
fastapi
uvicorn
requests
langgraph
langchain
langchain-openai
langchain-community
supabase
sqlalchemy
pyodbc
pandas
APScheduler
beautifulsoup4
html2text
python-dotenv
pillow
```

## ⚙️ 設定環境變數（.env）

```bash
OPENAI_API_KEY=sk-xxxxxx
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=xxxxx
MSSQL_CONN=DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.x.x;DATABASE=RoyalBaseDB;UID=xxxx;PWD=xxxx
LINE_CHANNEL_TOKEN=xxxxx
LINE_CHANNEL_SECRET=xxxxx
```

## 🚀 啟動方式

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Webhook URL: `http://<server_ip>:8000/line/webhook`

## 🧩 核心流程說明

整個 AI 流程被定義為一張 **狀態圖 (Graph)**，每個節點代表一個功能：
1. **InputNode**：接收 LINE webhook 訊息  
2. **RouterNode**：判斷訊息類型（文字、圖片、其它）  
3. **AITextNode**：呼叫 GPT-4o + 向量知識庫查詢回答  
4. **AIImageNode**：呼叫 GPT-4 Vision 解析圖片內容  
5. **NewsNode / GoogleNode**：輔助查詢外部資料  
6. **ReplyNode**：組合回覆內容並回傳給 LINE API  

### 🔹 1. Graph 主流程

`graph_main.py`
```python
from langgraph.graph import StateGraph, END
from langgraph.graph.message import MessageState
from agents.nodes import input_line, router, ai_text_node, ai_image_node, reply_line_node

graph = StateGraph(MessageState)

graph.add_node("Input", input_line.handle)
graph.add_node("Router", router.route_message)
graph.add_node("AI_Text", ai_text_node.process_text)
graph.add_node("AI_Image", ai_image_node.process_image)
graph.add_node("Reply", reply_line_node.reply_user)

graph.add_edge("Input", "Router")
graph.add_edge("Router", "AI_Text", condition=lambda s: s["type"] == "text")
graph.add_edge("Router", "AI_Image", condition=lambda s: s["type"] == "image")
graph.add_edge("AI_Text", "Reply")
graph.add_edge("AI_Image", "Reply")

graph.set_entry_point("Input")
graph.set_finish_point(END)

def run_graph(event):
    state = MessageState(messages=[event])
    return graph.invoke(state)
```

### 🔹 2. 路由節點範例

`router.py`
```python
def route_message(state):
    msg = state["messages"][-1]
    msg_type = msg["message"]["type"]
    state["type"] = msg_type
    return state
```

### 🔹 3. 文字 AI Node

`ai_text_node.py`
```python
def process_text(state):
    from langchain.chat_models import ChatOpenAI
    from langchain.embeddings import OpenAIEmbeddings
    from langchain.vectorstores import SupabaseVectorStore
    from supabase import create_client
    import os

    question = state["messages"][-1]["message"]["text"]
    client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vs = SupabaseVectorStore(client, embeddings, table_name="rag_documents")

    docs = vs.similarity_search(question, k=3)
    context = "\n".join([d.page_content for d in docs])

    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    reply = llm.predict(f"以下是知識庫資料：{context}\n\n問題：{question}")
    state["reply_text"] = reply
    return state
```

### 🔹 4. 圖片 AI Node

`ai_image_node.py`
```python
def process_image(state):
    import base64, os
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    image_bytes = state["messages"][-1]["image_bytes"]
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": [
            {"type": "text", "text": "請協助理解這張圖片的內容，並以繁體中文說明"},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64}"}
        ]}]
    )
    state["reply_text"] = result.choices[0].message.content
    return state
```

### 🔹 5. 回覆節點

`reply_line_node.py`
```python
import requests, os

def reply_user(state):
    reply_token = state["messages"][-1]["replyToken"]
    text = state.get("reply_text", "我收到您的訊息囉！")
    headers = {
        "Authorization": f"Bearer {os.getenv('LINE_CHANNEL_TOKEN')}",
        "Content-Type": "application/json"
    }
    body = {"replyToken": reply_token, "messages": [{"type": "text", "text": text}]}
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)
    return state
```

## 🕒 每週知識庫自動更新

`scheduler/rebuild_kb.py` 使用 APScheduler 定期呼叫 Supabase API，
重新寫入最新 SQL 資料與向量。

## ✅ 設計原則

1. 每個 node 僅做一件事：**輸入 → 處理 → 更新 state → 回傳**
2. 所有邏輯直述、可在單檔案追蹤。
3. 不使用多層 class 或抽象工廠，避免「除錯時要轉三個檔」。
4. 所有流程皆由 `graph_main.py` 管理，開發與測試容易。

## 🧑‍💻 作者註

> 本版本以 LangGraph 為核心，完全重現 n8n AI 工作流邏輯，
> 並以「清晰流程、少封裝、可維護」為開發準則。
> 任何節點的新增、調整都只需修改單一檔案即可。
