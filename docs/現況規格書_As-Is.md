# RBIT 改版 V2 — 現行版本規格書與運作情景（As-Is）

> 版本：現況基準　　文件狀態：待審核　　產出日期：2026-07-24

## 背景與目的

本文件為皇基資訊（RoyalBase）IT 知識助理系統「改版 V2」現行版本的**技術規格書**與**運作情景**整理。目的是在提出新的改版需求前，先建立雙方對「現況如何運作、數據如何流動」的共同基準。

本文件為**現況描述（As-Is）**，不含任何改動建議。經審核通過後，才會據此提出新的改版需求（To-Be）。

> 註：本專案目錄非 git 倉庫，內含兩個獨立子系統。以下內容以實際程式碼為準（已逐檔驗證聊天模型、RAG 路徑、Supabase 使用狀態等關鍵事實）。

---

## 1. 系統總覽

系統由兩個獨立子系統組成，透過同一個 SQL Server 資料庫（`RBDev_TEST` @ `10.1.1.11`）串接：

| 子系統 | 目錄 | 技術 | 角色 |
|--------|------|------|------|
| **LINE 知識助理**（前端） | `RBHelpDesk_AIAgent/` | Python 3.10 + Flask + LangGraph | 即時處理 LINE 使用者訊息、RAG 檢索、GPT 回覆、人工客服切換 |
| **後端知識管理** | `RBITQAContent/` | ASP.NET Core 8.0 MVC + Dapper | 知識庫 QA 維護、AI 擴增問法、Embedding／三元組生成 |

**共同資料層**：SQL Server，三張核心表 `IT_KB_Document`、`IT_KB_Graph`、`IT_KB_UserMemory`。

```
LINE 使用者
   │ webhook
   ▼
RBHelpDesk_AIAgent (Flask :8098, LangGraph)
   │  讀寫
   ▼
SQL Server (IT_KB_Document / IT_KB_Graph / IT_KB_UserMemory)
   ▲
   │  維護、生成 Embedding+三元組
RBITQAContent (.NET MVC 後台)
   ▲
   │
後台管理員（AD 網域登入）
```

**開發風格（兩子系統一致）**：商業邏輯直接寫在 node／controller，不做 Repository Pattern／過度分層；中文註解、單檔完整流程、快速迭代優先、容許適度重複碼。

---

## 2. LINE 知識助理（RBHelpDesk_AIAgent）

### 2.1 進入點
- `app.py`：Flask，`POST /webhook/LINE_IT`（正式）與 `/webhook/line_dev`（測試）共用同一 handler；`GET /` 健康檢查；預設 port `8098`；每 5 分鐘印一次 heartbeat。
- 逐筆 event 呼叫 `agents/graph_main.py :: run_graph_for_line_event(event)`。
- **註記**：目前 webhook 未做 LINE 簽章驗證。

### 2.2 LangGraph 流程（`agents/graph_main.py`）
state 為單純 dict。節點與連線：

```
Input → MemoryLoad → HumanCheck ──(_skip_ai=True)──► Reply → END
                          │
                          └(continue)► Router ─┬─ text  → AI_Text  → MemorySave → Reply → END
                                               ├─ image → AI_Image → MemorySave → Reply → END
                                               ├─ news  → AI_News  ──────────────► Reply → END
                                               └─ else  → Reply_Unsupported ─────────────► END
```

各節點（`agents/nodes/`）：

| 節點 | 檔案 | 職責 |
|------|------|------|
| Input | `input_line.py` | 解析 LINE event → `user_id`、`message_type`、`message_text`、`image_id`、`reply_token` |
| MemoryLoad | `memory_load_node.py` | 從 `IT_KB_UserMemory` 讀該使用者 chat_history 與人工模式狀態 |
| HumanCheck | `human_check_node.py` | 真人客服狀態機（early-stop node，見 2.4） |
| Router | `router.py` | 依訊息內容分派：含「今日科技新聞」→ news；text→text；image→image；其他→unsupported |
| AI_Text | `ai_text_node.py` | 核心：三元組抽取 → embedding → GraphRAG → 組 prompt → GPT 回覆（見 2.3） |
| AI_Image | `ai_image_node.py` | 下載 LINE 圖片 → GPT-4o Vision 分析 |
| AI_News | `news_node.py` | 爬 iThome／AI Magazine 新聞，組成文字回覆 |
| MemorySave | `memory_save_node.py` | UPSERT 回 `IT_KB_UserMemory`（chat_history 保留最後 10 輪） |
| Reply | `reply_line_node.py` | 依 `message_type` 組 text 或 flex payload，呼叫 LINE Reply API |

> 預留未接線節點：`vector_node.py`、`google_node.py`、`database/supabase_client.py`。

### 2.3 AI_Text 核心處理（`ai_text_node.py` — 最關鍵路徑）
1. `clean_basic()` 清洗使用者文字。
2. **三元組抽取** `tripleExtractService()`：呼叫 **`gpt-4o`** + Structured Output（Pydantic `TripleExtractionResponse`），依 `TRIPLE_EXTRACTION_PROMPT` 先 Query Expansion 再抽 `(entity1, relation, entity2)`；抽不到則 fallback 用原問題字串。
3. **Embedding**：對「每個三元組文字」批次呼叫 **`text-embedding-3-small`**，得到多個查詢向量（多向量查詢）。
4. **GraphRAG 查詢** `graph_rag_query(vec, mode="hybrid")`（`database/graph_ragc_client.py`）：
   - `search_by_embedding`：**全表掃描** `IT_KB_Graph`，將 `VARBINARY` 還原成 float32，用 numpy 逐筆算 cosine similarity，取 top_k=5。
   - `hybrid_search`：取語意 top1 的 `Entity1/Relation/Entity2` 再做 `search_by_triplet` 結構查詢。
   - 每個查詢向量各查一次，所有 semantic+structural 結果**依 `RowID` 合併去重**。
5. **組 Prompt**：`SYSROLE_PROMPT`（system）+ `SYSTEM_BASE_PROMPT` + 使用者問題 + 三元組 + 歷史對話 + 知識庫（事實三元組＋原始 ChunkText）+ `KNOWLEDGE_BASE_PROMPT`（業務規則集）。
6. **回覆生成**：呼叫 **`gpt-5.1`**（硬編碼，`ai_text_node.py:275`，不帶 temperature）。
7. 回覆寫回 `state["reply_text"]`，並把本輪對話 append 進 chat_history（保留最後 10 輪）。

> **模型分工小結**：三元組＝`gpt-4o`；主回覆＝`gpt-5.1`；圖片＝GPT-4o Vision；Embedding＝`text-embedding-3-small`。

### 2.4 真人客服狀態機（`human_check_node.py`）
- 觸發關鍵字 `真人客服|真人|人工客服|轉人工` → `human_handling=True`，回覆雙語（中／越）Flex 卡片（`LINE_FLEX_BUBBLE_TEXT`），`_skip_ai=True` 略過 AI。
- 人工模式中：**逾時 15 分鐘**（`ARTIFICIAL_TIMEOUT_MINUTES`）自動恢復 AI；或使用者輸入 `結束人工|回到AI|恢復AI|結束真人客服|謝謝` 恢復 AI。
- 人工模式中一般訊息：AI 不回應（`reply_text=""`），交由 LINE 官方後台真人處理。

### 2.5 業務規則（`config.py :: KNOWLEDGE_BASE_PROMPT` 摘要）
問安禮貌回覆、範圍外委婉拒絕（但「切花配貨／盆花配貨／切花配銷」屬內部系統）、多語言先譯繁中再檢索、查無知識庫時用 LLM 自身知識但不捏造內部資料、密碼問題附自助改密系統 `https://pass.royalbase.com`（提示同步 15 分鐘）、系統權限問題導向電子表單申請、輸出需分點分段、專業冷淡零冗餘。

---

## 3. 後端知識管理（RBITQAContent）

- **技術**：ASP.NET Core 8.0 MVC + Dapper + 原生 SQL；AD／LDAP（royalbase.com 網域）+ Session 登入；`ApiTokenAuthAttribute` 做 API 鑑權。
- **核心 `QAController`**：
  - `Input()`：輸入 QA → `OpenAIService.GenerateAugmentedQAAsync()` 用 `gpt-4o-mini` 生成 10+ 個問法變種（答案不變）→ 寫入 `IT_KB_Document` → 匯出 JSONL 到 `finetune_data/`。
  - `List()`：分頁（OFFSET/FETCH）＋搜尋＋排序。
  - `Edit()／Delete()／DeleteBatch()`：QA 維護。
  - `GenerateTriplesAndEmbedding()／RebuildGraph()`：對文件生成 Embedding（`EmbeddingService`，`text-embedding-3-small` → float32 序列化 byte[]）與三元組（`TripleExtractService`，`gpt-4o`），寫入 `IT_KB_Graph`。
- **Services**：`OpenAIService`、`TripleExtractService`、`EmbeddingService`、`ITKBGraphService`、`LoggerService`。
- **Embedding 存法**：`Buffer.BlockCopy(float[] → byte[])` 存進 MSSQL `VARBINARY(MAX)`，與 Python 端 `np.frombuffer(dtype=float32)` 對應一致。

---

## 4. 數據架構（SQL Server `RBDev_TEST`）

**IT_KB_Document**（QA 主表）
`DocID(PK)`、`Instruction`、`InputText`(問)、`OutputText`(答)、`SourceKey`、`CreatedAt`、`UpdatedAt`。供微調與 RAG 來源。

**IT_KB_Graph**（GraphRAG 三元組＋向量）
`RowID(PK)`、`DocID(FK)`、`ChunkID`、`ChunkText`、`Embedding(VARBINARY)`、`Entity1`、`Relation`、`Entity2`、`Confidence`、`CreatedAt`；索引：DocID/ChunkID/Entity1/Entity2/Relation。目前 1 doc 多為 1 chunk（未做長文分塊）。

**IT_KB_UserMemory**（使用者記憶）
`UserID(PK, LINE userId)`、`ChatHistory(JSON)`、`HumanHandling(bit)`、`HumanActivatedAt`、`HumanLastMsgAt`、`UpdatedAt`。

---

## 5. 外部服務

| 服務 | 用途 | 端點／模型 |
|------|------|-----------|
| OpenAI Chat | 主回覆 | `gpt-5.1` |
| OpenAI Chat | 三元組抽取／問法擴增 | `gpt-4o`／`gpt-4o-mini` |
| OpenAI Vision | 圖片分析 | GPT-4o Vision |
| OpenAI Embedding | 向量化 | `text-embedding-3-small` |
| LINE Messaging API | 收訊／回覆／取圖 | webhook、`/v2/bot/message/reply`、`/v2/bot/message/{id}/content` |
| 爬蟲 | 科技新聞 | iThome、AI Magazine（BeautifulSoup） |
| Supabase | 向量庫（**已配置但實際未使用**，RAG 走 MSSQL） | 預留 |

**設定**：Python 走 `.env`（`config.py` 載入）；.NET 走 `appsettings.json`。敏感資訊（OpenAI／LINE／MSSQL sa 密碼）目前明文存於設定檔。

---

## 6. 運作情景（Scenarios）

**情景 A — 一般 IT 問題（文字＋RAG）**
使用者問「如何重設 RB-Mobile 密碼？」→ MemoryLoad → 非人工 → Router=text → 抽三元組 `(RB-Mobile, 密碼重設, 帳號)` → embedding → GraphRAG 命中知識 → `gpt-5.1` 依知識庫作答並附 `pass.royalbase.com` 自助改密提示 → 存記憶 → LINE 回覆。

**情景 B — 圖片報障**
使用者傳錯誤畫面截圖 → Router=image → 下載圖片 → GPT-4o Vision 解析畫面並給建議 → 回覆。

**情景 C — 今日科技新聞**
使用者輸入「今日科技新聞」→ Router=news → 爬 iThome／AI Magazine → 組標題＋摘要＋連結回覆（規則要求 URL 可正確點擊）。

**情景 D — 轉真人客服**
使用者輸入「真人客服」→ HumanCheck 觸發 → 回雙語 Flex 卡片、進人工模式、略過 AI → 期間 AI 靜默 → 使用者輸入「恢復AI」或逾時 15 分鐘 → 自動恢復 AI。

**情景 E — 知識庫維護（後台）**
管理員在 RBITQAContent 新增一組 QA → AI 擴增 10+ 問法寫入 `IT_KB_Document` → 對該筆生成 Embedding＋三元組寫入 `IT_KB_Graph` → 立即可被情景 A 的 GraphRAG 檢索到。

**情景 F — 查無知識庫**
GraphRAG 無命中 → prompt 標示「知識庫沒有找到相關資訊」→ `gpt-5.1` 改用自身知識作答，但依規則不捏造內部系統資料；資訊過於精簡則回覆請補充細節的固定話術。

---

## 7. 現況觀察（供後續改版參考，非本次改動）

- **RAG 效能**：`search_by_embedding` 每次全表掃描 `IT_KB_Graph` 並在 Python 逐筆算 cosine，資料量增大時線性變慢，無向量索引／快取。多向量查詢會放大掃描次數。
- **模型設定**：主回覆 `gpt-5.1` 為程式碼硬編碼（未走 `OPENAI_MODEL_CHAT` env）；env 預設值與實際使用不一致。
- **Supabase／google_node／vector_node**：已配置或建檔但未接入流程。
- **安全性**：webhook 無簽章驗證；設定檔明文密鑰；MSSQL 使用 sa。
- **記憶**：chat_history 固定保留最後 10 輪，未做摘要壓縮。
- **分塊**：多為 1 doc = 1 chunk，長文未切割。

---

## 8. 驗證方式（確認本規格與實際系統相符）

1. **靜態核對**：對照 `agents/graph_main.py` 節點連線、`ai_text_node.py` 模型字串（`gpt-4o` / `gpt-5.1`）、`config.py` 提示詞與 Flex、`human_check_node.py` 逾時常數，確認與本文件一致。
2. **前端實測**：啟動 `python app.py`（:8098），對 `/webhook/line_dev` POST 模擬 event（app.py 內註解已附 sample payload），分別以文字、`今日科技新聞`、`真人客服`、`恢復AI` 觸發，觀察 log 走過的節點與 LINE 回覆是否符合情景 A/C/D。
3. **資料層核對**：查 `IT_KB_Document`／`IT_KB_Graph`／`IT_KB_UserMemory` 三表結構與內容，確認 Embedding 為 float32 VARBINARY、UserMemory 記錄人工狀態。
4. **後台實測**：在 RBITQAContent 新增一筆 QA 並生成三元組＋Embedding，回前端提問驗證情景 E 端到端可檢索。

---

> 本規格書為現況（As-Is）基準。請審核；通過後即可據此提出改版需求（To-Be）。
