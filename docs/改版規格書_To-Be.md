# RBIT 改版 V2 — 改版規格書（To-Be）

> 版本：To-Be v1.8　　文件狀態：已審核、實作中（第 12 章為上線步驟）　　產出日期：2026-09-23　　基準文件：`現況規格書_As-Is.md`
>
> v1.8 變更：同步規則（重複同步、改名搬移、刪除、刪除後放回、失敗重試）整理成 `scheduler/README.md`；資料夾來源加上「掃不到任何檔案就不刪除」的防呆。
>
> v1.7 變更：Skill 用到的資料庫改為**跟著 Skill 走**（skill 資料夾內的 `db.json` + SKILL.md 的 `db:`／`tables:`），`.env` 不必設定；`.env` 只保留「IT 接管某個來源」與「DENY 擋表」兩種用途。設定方式見 `skills/README.md`。
>
> v1.6 變更：Skill 與資料庫的綁定改由 **Skill 自己宣告**（SKILL.md 標頭 `db: <來源>`），`.env` 不必填 Skill 名稱；啟動時會列出 Skill 要求但尚未設定的來源。
>
> v1.5 變更：白名單可由 Skill 自己宣告（SKILL.md 的 `tables:` + `.env` 寫 `@skill`）或交給唯讀帳號權限（`*`），另加 `DENY_TABLES`；外部取得的 Skill 不必由 IT 逐一抄表名。
>
> v1.4 變更：唯讀 SQL 改為**多資料庫具名來源**（`SQL_SOURCES` + `SQL_<名稱>_CONN/TABLES/DESC/SKILL`），白名單各自獨立、不可互查；所有 DB 帳密（含日後 Skill 用到的）統一寫在 `.env`。
>
> v1.3 變更：`SQL_ALLOWED_TABLES` 預設帶入 PMM 的 129 張表／檢視，`skills/db-query/SKILL.md` 補上對應說明；白名單過大時工具描述只列表名，新增 `describe_table` 工具現查欄位。
>
> v1.2 變更：新增文件來源「Microsoft 365 OneDrive／SharePoint 分享目錄」（透過 Microsoft Graph API，設定放 env）。
>
> v1.1 變更：依第 10 章回覆修訂，包括 SQL 白名單與 Drive 改由 env 設定、跨主機改為檔案存入 DB、新增快速路徑以符合延遲目標、各項參數集中到 `.env`／`appsettings.json`。

## 背景與目的

現行 `AI_Text` 是一條**固定管線**：三元組抽取 → embedding → 全表 cosine → `gpt-5.1` 一次回覆。它有三個限制：

1. **只能查 QA 知識庫**（`IT_KB_Graph`，1 doc = 1 chunk），SOP、操作手冊這類長文件無法納入。
2. **不會自己判斷**「要去哪裡找、要不要再查、答案對不對」，查不到就直接用 LLM 自身知識作答。
3. **業務規則全寫死在 `config.py`**（`KNOWLEDGE_BASE_PROMPT`），每新增一項能力都要改程式。

本次改版目標：

| # | 目標 | 說明 |
|---|------|------|
| G1 | **文件 GraphRAG** | PDF／Word／Excel／PPT／MD／TXT＋Google Drive 資料夾＋M365 OneDrive 分享目錄 → 分塊、實體／關係圖譜、向量，存 MSSQL＋記憶體快取 |
| G2 | **Agent 手腳** | AI_Text 改成「規劃 → 呼叫工具 → 判斷是否繼續 → 驗證」的迴圈 |
| G3 | **Skill 擴充** | `skills/<名稱>/SKILL.md`（可附 `tool.py`），放進資料夾就能載入 |

**已確認的決策**

| 項目 | 決策 |
|------|------|
| 文件來源 | PDF／Word／Excel／PPT、Markdown／TXT、Google Drive 資料夾、企業 M365 OneDrive／SharePoint 分享目錄 |
| 上傳入口 | 兩者都要：RBITQAContent 後台上傳，以及資料夾／Drive 批次匯入 |
| 部署 | .NET 後台與 Python 匯入程式**不在同一台主機** → 後台上傳的檔案**存入 DB**，不使用共用資料夾 |
| 儲存層 | 續用 MSSQL，向量載入記憶體快取（不新增基礎設施） |
| Agent 工具 | QA 知識庫、文件 GraphRAG、Google 搜尋、唯讀 DB 查詢 |
| 模型設定 | 全部改走 `.env`（Python）／`appsettings.json`（.NET） |
| DB 查詢 | LLM 產生 SQL，搭配唯讀帳號與程式檢查；可查的表**由 env 設定**，**不依員工身分控管** |
| Google Drive | 使用 service account，同步的資料夾**由 env 設定** |
| M365 OneDrive | 透過 Microsoft Graph API（Entra ID 應用程式註冊，app-only 驗證），同步的分享目錄**由 env 設定** |
| 延遲目標 | 一般 SQL 檢索（QA 知識庫、唯讀 SQL）**< 5 秒**；文件檢索、多步 Agent 查詢可以較久 |
| 成本 | 使用計量 API，暫不考量 token 用量 |
| 設定原則 | 模型、門檻、上限、逾時、路徑等參數**儘量放 `.env`／`appsettings.json`**，程式內不寫死；提示詞維持在 `config.py` |
| Skill 格式 | 資料夾＋`SKILL.md`（仿 Claude Skills），可附 `tool.py` |

**開發風格延續**：邏輯直接寫在 node／單一檔案、中文註解、dict state、Dapper 原生 SQL、不引入重型分層，先求能動。

---

## 1. 系統總覽（To-Be）

```
LINE 使用者
   │ webhook
   ▼
RBHelpDesk_AIAgent (Flask :8098, LangGraph)
   │   AI_Text → 【Agent 迴圈】──┬─ search_qa_kb      → IT_KB_Graph（既有 QA）
   │                              ├─ search_documents  → 文件 GraphRAG（新）
   │                              ├─ explore_entity    → 實體／關係圖譜（新）
   │                              ├─ web_search        → SerpAPI Google
   │                              ├─ sql_query         → MSSQL 唯讀帳號
   │                              └─ load_skill        → skills/*/SKILL.md (+tool.py)
   ▼
SQL Server RBDev_TEST（文件原檔也存在 DB：IT_KB_SourceDoc.FileContent）
   ▲                    ▲
   │ 讀原檔/寫圖譜      │ 上傳文件(寫入 DB)、QA 維護
ingest_docs.py（新，    RBITQAContent (.NET 後台，新增「文件管理」)
獨立排程程序，           ▲                         ← 與 Python 不同主機
與 Flask 同主機）        │
   ▲                     後台管理員（AD 登入）
   └─ 資料夾 / Google Drive / M365 OneDrive（Microsoft Graph）
```

**不變的部分**：Input、MemoryLoad、HumanCheck（真人客服狀態機）、Router、AI_Image、AI_News、MemorySave、Reply 的流程與行為；既有 `IT_KB_Document`／`IT_KB_Graph`／`IT_KB_UserMemory` 三張表。

---

## 2. 設定集中管理（`.env`／`appsettings.json`）

**原則**：模型、門檻、上限、逾時、路徑、清單等參數一律從設定檔讀取，程式內只留預設值。提示詞（`SYSROLE_PROMPT`、`AGENT_SYSTEM_PROMPT` 等）屬於內容，維持在 `config.py`；Skill 規則放 `SKILL.md`。

### 2.1 Python `.env`（`config.py` 統一載入）

| 分類 | env 參數 | 用途 | 預設值 |
|------|----------|------|--------|
| 模型 | `OPENAI_MODEL_CHAT` | Agent 主控（規劃＋回覆） | `gpt-5.1` |
| | `OPENAI_MODEL_VERIFY` | 答案驗證 | `gpt-4o-mini` |
| | `OPENAI_MODEL_EXTRACT` | 問題三元組／文件實體關係抽取 | `gpt-4o` |
| | `OPENAI_MODEL_VISION` | 圖片分析 | `gpt-4o` |
| | `OPENAI_MODEL_EMBED` | 向量化（既有） | `text-embedding-3-small` |
| | `AGENT_REASONING_EFFORT` | 主控模型推理強度（影響速度） | `low` |
| Agent | `AGENT_MODE` | `on`＝Agent 迴圈；`off`＝退回舊管線 | `on` |
| | `AGENT_MAX_STEPS` | 最多幾輪工具呼叫 | `4` |
| | `AGENT_TOOL_RESULT_MAX_CHARS` | 單一工具結果截斷長度 | `4000` |
| | `AGENT_FAST_PATH` | 是否啟用快速路徑（見 4.7） | `on` |
| | `OPENAI_MODEL_FAST` | 快速路徑專用模型（空＝沿用 CHAT） | 空 |
| | `QA_FAST_PATH_MIN_SCORE` | QA 命中分數高於此值可走快速路徑 | `0.80` |
| | `VERIFY_ENABLED` | 是否啟用驗證器 | `on` |
| 檢索 | `RAG_QA_TOP_K`／`RAG_DOC_TOP_K`／`RAG_ENTITY_TOP_K` | 各類檢索筆數 | `5`／`6`／`5` |
| | `RAG_MIN_SCORE` | 低於此相似度視為未命中 | `0.30` |
| | `RAG_CACHE_REFRESH_SEC` | 向量快取檢查更新間隔 | `60` |
| 唯讀 SQL | （通常不設） | 資料庫設定跟著 Skill 走：`skills/<名>/db.json` + SKILL.md 的 `db:`／`tables:` | 見 `skills/README.md` |
| | `SQL_SOURCES` | 選配，IT 直接維護或接管某個來源時才設 | 空 |
| | `SQL_<名稱>_CONN` | 該來源的唯讀連線字串 | — |
| | `SQL_<名稱>_TABLES` | 該來源的白名單：明列表名／`@skill`（用 Skill 宣告的 `tables:`）／`*`（唯讀帳號權限）；可混用 | — |
| | `SQL_<名稱>_DENY_TABLES` | 永遠不給查的表（結尾 `*` 為前綴比對），優先於上面 | 空 |
| | `SQL_<名稱>_DESC` | 該資料庫的用途（給 AI 判斷要查哪個） | 來源名稱 |
| | `SQL_<名稱>_SKILL` | 選填，只認指定的那一個 Skill | 空＝接受所有宣告 `db: <名稱>` 的 Skill |
| | `MSSQL_READONLY_CONN`／`SQL_ALLOWED_TABLES` | 舊版單一資料庫設定（相容，視為 `default` 來源） | — |
| | `SQL_MAX_ROWS` | 自動加上的 `TOP N` | `50` |
| | `SQL_TIMEOUT_SEC` | 查詢逾時 | `10` |
| | `SQL_SCHEMA_INLINE_MAX` | 白名單超過此表數時，工具描述只列表名，欄位改由 `describe_table` 現查 | `20` |
| 網路搜尋 | `SERPAPI_API_KEY` | Google 搜尋（SerpAPI） | — |
| | `WEB_SEARCH_NUM` | 搜尋結果筆數 | `5` |
| Skill | `SKILLS_DIR` | Skill 資料夾位置 | `./skills` |
| 文件匯入 | `DOC_DROP_FOLDER` | 批次匯入資料夾（Python 主機本機路徑） | — |
| | `GDRIVE_SA_JSON` | service account 金鑰檔路徑 | — |
| | `GDRIVE_FOLDER_IDS` | 要同步的 Drive 資料夾 ID（逗號分隔） | 空＝不同步 |
| | `M365_TENANT_ID` | Entra ID 租用戶 ID | — |
| | `M365_CLIENT_ID`／`M365_CLIENT_SECRET` | 應用程式註冊的用戶端 ID／密碼 | — |
| | `ONEDRIVE_SHARE_URLS` | 要同步的 OneDrive／SharePoint 資料夾分享連結（逗號分隔） | 空＝不同步 |
| | `ONEDRIVE_RECURSIVE` | 是否包含子資料夾 | `on` |
| | `INGEST_INTERVAL_SEC` | 匯入輪詢間隔 | `300` |
| | `CHUNK_TOKENS`／`CHUNK_OVERLAP` | 分塊大小／重疊 | `800`／`100` |
| | `EXCEL_ROWS_PER_CHUNK` | Excel 每塊列數 | `50` |
| | `DOC_ALLOWED_EXT` | 允許的副檔名 | `pdf,docx,xlsx,pptx,md,txt` |
| LINE | `LINE_PUSH_FALLBACK_SEC` | 處理超過此秒數改用 Push API | `50` |
| 真人客服 | `ARTIFICIAL_TIMEOUT_MINUTES` | 人工模式逾時（既有常數改讀 env） | `15` |

### 2.2 .NET `appsettings.json`

| 參數 | 用途 | 預設值 |
|------|------|--------|
| `OpenAI:ChatModel` | QA 問法擴增（`OpenAIService.cs:73` 目前寫死） | `gpt-4o-mini` |
| `OpenAI:TripleModel` | 三元組抽取（`TripleExtractService.cs:43/111/256` 目前寫死） | `gpt-4o-mini` |
| `OpenAI:EmbedModel` | 向量化（`EmbeddingService.cs:29` 目前寫死） | `text-embedding-3-small` |
| `DocUpload:AllowedExt` | 允許上傳的副檔名 | `pdf,docx,xlsx,pptx,md,txt` |
| `DocUpload:MaxSizeMB` | 單檔大小上限 | `50` |

> 註：As-Is 規格書寫 .NET 三元組抽取使用 `gpt-4o`，實際程式碼為 `gpt-4o-mini`，本次一併改成讀設定。

### 2.3 其他
- 移除硬編碼：`ai_text_node.py:275`（`gpt-5.1`）、`ai_text_node.py:343`（`gpt-4o`）、`ai_image_node.py:63`（`gpt-4o`），以及上表的 .NET 模型字串。
- **唯讀帳號**：每個 SQL 來源都請 DBA 另建登入帳號，只對該來源白名單內的表／檢視授予 SELECT；不得沿用 sa 或應用程式帳號。DB 權限與 env 白名單兩邊都要設定（雙重防線）。

---

## 3. 文件 GraphRAG（G1）

### 3.1 新資料表（DDL：`RBHelpDesk_AIAgent/sql/tobe_schema.sql`）

**IT_KB_SourceDoc**（文件來源）
`DocumentID(PK)`、`FileName`、`SourceType`（`upload`／`folder`／`gdrive`／`onedrive`）、`SourceRef`（資料夾相對路徑、Drive fileId，或 OneDrive `driveId:itemId`；後台上傳為空）、`SourceUrl`（雲端檔案的網頁連結，回覆引用出處時附上）、`FileContent VARBINARY(MAX)`（**後台上傳的原檔**，因兩台主機不共用檔案系統；其他來源不存）、`FileHash`、`Status`（`Pending`／`Processing`／`Done`／`Failed`／`Deleting`）、`ErrorMsg`、`ChunkCount`、`UploadedBy`、`CreatedAt`、`UpdatedAt`

**IT_KB_SyncState**（雲端來源同步進度，v1.2 新增）
`SourceKey(PK)`（例如 `onedrive:<分享連結 hash>`、`gdrive:<folderId>`）、`DeltaLink`／`PageToken`、`LastSyncAt`、`LastError`

**IT_KB_Chunk**（文件分塊）
`ChunkID(PK)`、`DocumentID(FK)`、`Seq`、`SectionPath`（標題階層／頁碼／工作表名）、`ChunkText`、`Embedding VARBINARY(MAX)`（float32）、`TokenCount`、`CreatedAt`

**IT_KB_Entity**（實體）
`EntityID(PK)`、`Name`、`NormName`（唯一索引）、`EntityType`、`Description`、`Embedding`、`UpdatedAt`

**IT_KB_Relation**（關係）
`RelationID(PK)`、`SrcEntityID`、`DstEntityID`、`Relation`、`Description`、`Weight`、`ChunkID`、`DocumentID`

**IT_KB_EntityChunk**（實體出現在哪些 chunk）
`EntityID`、`ChunkID`、`DocumentID`

**IT_KB_AgentTrace**（Agent 執行紀錄）
`TraceID(PK)`、`UserID`、`Question`、`StepsJson`（每輪工具呼叫、參數、結果摘要）、`Verdict`、`Answer`、`LatencyMs`、`CreatedAt`

> Embedding 格式與現行一致：float32 → `VARBINARY(MAX)`，Python `np.frombuffer(dtype=float32)`、.NET `Buffer.BlockCopy`。

### 3.2 匯入流程（新檔 `scheduler/ingest_docs.py`，獨立程序）

> 各來源的同步規則（怎麼判斷重複／變更／刪除、刪除後放回去會怎樣、失敗如何重試）詳見 `scheduler/README.md`。

獨立於 Flask 執行（與 Flask 同一台主機；`python scheduler/ingest_docs.py --loop` 常駐，或 `--once` 跑一次），避免匯入大檔時拖慢 LINE 回覆。

1. **收件**（每 `INGEST_INTERVAL_SEC` 秒一輪）
   - 後台上傳：`IT_KB_SourceDoc` 中 `Status=Pending` 的記錄，從 `FileContent` 讀出原檔（不需要共用資料夾）。
   - 後台刪除：`Status=Deleting` 的記錄 → 刪除其 chunk／relation／EntityChunk 後刪除該筆。
   - 資料夾：掃描 `DOC_DROP_FOLDER`，新檔或 hash 變更 → 新增／更新記錄。
   - Google Drive：以 `GDRIVE_SA_JSON` 的 service account 列出 `GDRIVE_FOLDER_IDS` 內的檔案（資料夾需先分享給該 service account 的 email，唯讀即可），依 `modifiedTime`／md5 判斷變更；Google Docs／Sheets／Slides 先匯出成 docx／xlsx／pptx；Drive 端已刪除的檔案同步刪除。
   - M365 OneDrive／SharePoint：
     1. 以 `msal` 用 `M365_TENANT_ID`／`M365_CLIENT_ID`／`M365_CLIENT_SECRET` 取得 app-only token。
     2. 對每個 `ONEDRIVE_SHARE_URLS`：將分享連結編碼後呼叫 `GET /shares/{encoded}/driveItem`，取得資料夾的 `driveId`／`itemId`。
     3. 用 **delta 查詢**（`GET /drives/{driveId}/items/{itemId}/delta`）取得新增、修改、刪除的檔案；`deltaLink` 存入新表 `IT_KB_SyncState`（`SourceKey`、`DeltaLink`、`UpdatedAt`），下一輪只取變更部分。`ONEDRIVE_RECURSIVE=off` 時只處理第一層。
     4. 依 `eTag`／`quickXorHash` 判斷內容變更，以 `GET /drives/{driveId}/items/{id}/content` 下載原檔；Office 檔本身就是 docx／xlsx／pptx，不需轉檔。
     5. 被刪除的項目 → 同步刪除 chunk／relation／EntityChunk。
     6. 權限：Graph「應用程式權限」`Files.Read.All`（若分享目錄在 SharePoint 網站，建議改用範圍更小的 `Sites.Selected`，只授權該網站）；需要 M365 管理員同意。
2. **解析**
   | 格式 | 套件 | 切法 |
   |------|------|------|
   | PDF | `pymupdf` | 逐頁，SectionPath＝頁碼 |
   | Word | `python-docx` | 保留標題階層，SectionPath＝標題路徑 |
   | Excel | `openpyxl` | 每個工作表轉 Markdown 表格，每 N 列一塊（保留表頭） |
   | PPT | `python-pptx` | 逐張投影片＋備註 |
   | MD／TXT | 直接讀 | MD 依標題切 |
3. **分塊**：`CHUNK_TOKENS`（800）token、重疊 `CHUNK_OVERLAP`（100），以 `tiktoken` 計算。
4. **抽取圖譜**：每個 chunk 呼叫 `OPENAI_MODEL_EXTRACT`＋Structured Output（沿用 `ai_text_node.py` 的 Pydantic＋`client.chat.completions.parse` 寫法），產出 entities（name／type／description）與 relations（src／dst／relation／description）。
5. **實體合併**：`NormName`（轉小寫、去空白、全形轉半形）相同即合併；描述過長時由 LLM 摘要。
6. **向量化**：chunk 文字與實體描述批次 embedding。
7. **寫入**：同一個 transaction 內先刪除該 DocumentID 的舊 chunk／relation／EntityChunk，再寫入新資料；成功 `Status=Done`＋`ChunkCount`，失敗 `Status=Failed`＋`ErrorMsg`。

### 3.3 檢索（新檔 `database/doc_graph_client.py`）

- **記憶體快取**：啟動時把 `IT_KB_Chunk`、`IT_KB_Entity`、`IT_KB_Graph` 的向量載入 numpy 矩陣，一次矩陣乘法算完所有 cosine；每 `RAG_CACHE_REFRESH_SEC` 秒檢查各表 `MAX(UpdatedAt)`／筆數，有變化才重新載入。`graph_ragc_client.search_by_embedding` 同步改用此快取（解決 As-Is 第 7 章「全表掃描」問題）。
- **`local_search(query)`**：query 向量 → top-k 實體＋top-k chunk → 由實體擴展 1-hop 關係與鄰居 → 取回關聯 chunk → 合併排序。回傳 `[{source_id, doc_name, section, text, score}]`，附**出處**供回覆引用。
- **`explore_entity(name, hops=1)`**：查某實體的鄰居與關係，供 Agent 追問使用。
- **`global_search`（選配，第 8 章）**：以社群摘要回答整體性問題。

---

## 4. Agent 迴圈（G2）

### 4.1 流程（新檔 `agents/nodes/agent_node.py`）

`graph_main.py` 的 `AI_Text` 節點改呼叫 `agent_node.process_text`，其他節點不變。`AGENT_MODE=off` 時仍呼叫舊的 `ai_text_node.process_text`（保留作為安全開關）。

```
Router=text
   │
   ▼
[快速路徑檢查]（見 4.7）問題直接 embedding → 查 QA 快取
   ├─ 最高分 ≥ QA_FAST_PATH_MIN_SCORE → 一次呼叫主模型作答（不跑迴圈、不驗證）→ MemorySave
   └─ 否則 ↓
[準備] system = SYSROLE_PROMPT + AGENT_SYSTEM_PROMPT(工具使用規則) + Skill 清單(名稱+描述)
       messages = system + 歷史對話(10 輪) + 使用者問題
   │   同時送出 LINE loading 動畫
   ▼
┌─► [規劃／行動] OPENAI_MODEL_CHAT + tools
│      ├─ 有 tool_calls → 執行工具 → 結果(含 source_id)附進 messages ──┐   ← 去哪裡找
│      │                                                                │   ← 要不要繼續查
│      └─ 沒有 tool_calls → 產生草稿答案                                │
│                 │                               （未達 AGENT_MAX_STEPS 則回到規劃）
│                 ▼
│      [驗證] OPENAI_MODEL_VERIFY + Structured Output                        ← 如何驗證
│         ├─ pass       → 最終回覆（附「參考來源」）
└─────────├─ needs_more → 驗證意見加回 messages，仍有步數則再跑一輪
          └─ fail／步數用完 → 保守回覆：說明已查到／不確定的部分，提示可輸入「真人客服」
   │
   ▼
寫入 IT_KB_AgentTrace → MemorySave → Reply
```

### 4.2 工具使用規則（`config.py :: AGENT_SYSTEM_PROMPT`）

1. 內部問題先查內部：`search_qa_kb` → `search_documents`（必要時 `explore_entity` 追關係）。
2. **`search_qa_kb` 的結果不足以完整回答時，一定要再呼叫 `search_documents`**（v1.9 補強）。沒命中、只是題目相近、只查到結論而缺少操作步驟／畫面位置／設定值，或問的是某系統的操作方式與流程，都算不足——這類完整說明通常寫在手冊或簡報裡，QA 知識庫往往只有摘要。
3. 內部查不到，或明顯需要外部／最新資訊時，才使用 `web_search`；回覆要標明來自網路。
4. 需要即時資料（例如帳號狀態）時使用 `sql_query`（可查的表與欄位說明已寫在工具描述中，不必先載入 Skill）。
5. 同樣的查詢不重複呼叫；證據足夠就停止查詢並作答。
6. 符合某個 Skill 的描述時，先 `load_skill` 再依其指示處理。
7. 內部系統資訊只能依據工具取得的證據，不得捏造。
8. 非繁體中文提問時，查詢先轉繁體中文關鍵字，回覆用使用者的語言。

### 4.3 驗證器 `verify()`

輸入：使用者問題、全部工具證據、草稿答案。輸出（Pydantic）：

```
verdict: "pass" | "needs_more" | "fail"
unsupported_claims: [草稿中沒有證據支持的敘述]
missing_info: 還缺什麼資訊
feedback: 給 Agent 的修正建議
```

檢查項目：每個重點都有證據支持、沒有捏造內部系統資料、確實回答了問題、符合 `KNOWLEDGE_BASE_PROMPT` 的規則（分點、語氣等）。

**略過驗證**（程式判斷，不呼叫驗證器）：沒有呼叫任何工具的回覆（問安、閒聊、範圍外拒絕）、快速路徑、證據只來自 `sql_query` 的回覆（資料庫結果本身即為依據）。`VERIFY_ENABLED=off` 時全部略過。

### 4.4 工具清單（新檔 `agents/tools.py`）

| 工具 | 參數 | 實作 |
|------|------|------|
| `search_qa_kb` | query | 包裝現有 `graph_rag_query`（三元組擴展＋hybrid，改用快取） |
| `search_documents` | query | `doc_graph_client.local_search` |
| `explore_entity` | name | `doc_graph_client.explore_entity` |
| `web_search` | query | 接上現有 `google_node.google_search`（SerpAPI） |
| `sql_query` | sql | 唯讀 SQL（見 4.5） |
| `load_skill` | name | 載入 Skill 本文＋工具（見第 5 章） |

統一回傳格式：`{ok, items: [{source_id, source_type, title, text}], note}`；每個工具的結果截斷到 `AGENT_TOOL_RESULT_MAX_CHARS`，避免 context 過大。`SQL_SOURCES` 為空時不註冊 `sql_query`；`SERPAPI_API_KEY` 為空時不註冊 `web_search`。

### 4.5 唯讀 SQL 工具的安全防線

| 層級 | 措施 |
|------|------|
| 1. DB 權限 | 只用各來源的 `SQL_<名稱>_CONN`，帳號只有白名單表的 SELECT 權限 |
| 2. 語法檢查 | `sqlglot`（tsql 方言）解析：只允許**單一 SELECT**；拒絕 INSERT／UPDATE／DELETE／MERGE／EXEC／DROP／ALTER／`SELECT INTO`／`OPENROWSET`／`OPENQUERY`／多語句 |
| 3. 表白名單 | 只能查該來源白名單內的表／檢視（解析出的每個表名都要在內）；`@skill`／`*` 兩種來源仍由 `.env` 決定是否採用，且一律再扣掉 `DENY_TABLES`；來源之間不共用白名單、不能互相 JOIN |
| 4. 結果限制 | 自動加上 `TOP {SQL_MAX_ROWS}`、查詢逾時 `SQL_TIMEOUT_SEC`。實際執行時會多抓一筆（`TOP N+1`，v1.9），多出來的不回傳，只用來判斷有沒有被截斷；被截斷時 `note` 會明確告知「這是前 N 筆、不是全部，上限無法提高，要總數請用 COUNT()／GROUP BY」，避免模型把截斷結果當成完整清單，或承諾使用者做不到的完整匯出 |
| 5. 稽核 | 每句 SQL（含被拒絕的）記錄到 `IT_KB_AgentTrace` |

- **不依員工身分控管**：所有 LINE 使用者可查的範圍相同，因此各來源的白名單只應放入允許全員查看的表／檢視；含個資、薪資等敏感欄位的表建議改建檢視（只露出可公開欄位）再列入白名單。
- **表結構說明**：白名單在 `SQL_SCHEMA_INLINE_MAX` 張以內時，啟動時由唯讀連線讀取各表欄位（`INFORMATION_SCHEMA.COLUMNS`）寫進 `sql_query` 的工具描述；超過時只列表名，改註冊 `describe_table(table)` 工具讓模型寫 SQL 前現查欄位（快取），避免上百張表的欄位清單每次請求都塞進提示詞。兩種情況都會把 `skills/db-query/SKILL.md` 的表意義、關聯與撰寫規則併入工具描述。
- **設定跟著 Skill 走**：Skill 會被分享、也可能從外部取得，IT 不一定知道它要用哪些表、連哪個庫，因此連線（`skills/<名>/db.json`，另附 `db.json.example`）與表清單（SKILL.md 的 `db:`／`tables:`）都放在 Skill 資料夾內，丟進 `skills/` 就生效、改 `db.json` 即換連線，**`.env` 不用動**。`.env` 只剩兩種用途：`SQL_<名稱>_DENY_TABLES` 擋表，以及 `SQL_SOURCES`＋`SQL_<名稱>_CONN/TABLES` 由 IT 接管（同名時 `.env` 優先）；也可以寫 `*` 讓唯讀帳號的 SELECT 權限直接決定範圍。兩種情況的**開關仍在 `.env`**，且 `DENY_TABLES` 與 DB 權限仍是後兩道防線。服務啟動時會列出每個來源綁到哪些 Skill、設定來自哪裡、缺哪幾張表，以及「要查資料庫但沒有連線設定」的 Skill（裝外來 Skill 最常見）；AI 查到被擋的表，訊息也會提示請 IT 加入。
- **多資料庫**：每個資料庫是一個具名來源，`sql_query(sql, source)`／`describe_table(table, source)` 用 `source` 指定；只有一個來源時可省略。新增資料庫只要在 `.env` 加 `SQL_SOURCES` 名稱與四個參數，再寫一份 `skills/db-<名稱>/SKILL.md`，**不用改程式**。Skill 的 `tool.py` 要連資料庫時用 `config.get_sql_source("<名稱>")` 取連線，不得自行保存帳密。
- **預設白名單**：`skills/db-pmm/SKILL.md` 宣告的 129 張 PMM 表／檢視（DB `RBMS`，整理自 PMM Skill 文件）。該檔本文同時寫入表的中文意義、單頭／單身與配貨／出貨關聯；`skills/db-query/SKILL.md` 則是各來源共通的撰寫規則。不想開放的表（例如 `BIPersonel`、`BSRole`、`View_PersonelPermission` 等帳號權限相關）填到 `SQL_PMM_DENY_TABLES` 即可。

### 4.6 LINE 回覆時效

- 開始處理時呼叫 LINE loading 動畫 API（`POST /v2/bot/chat/loading/start`）。
- `reply_line_node.py` 在 reply token 失效（或處理時間超過 `LINE_PUSH_FALLBACK_SEC`）時改用 Push API（`/v2/bot/message/push`，對象為 state 中的 `user_id`）。

### 4.6a Webhook 簽章驗證（v1.9 新增）

`app.py` 的 webhook 在解析 JSON 之前先驗 `X-Line-Signature`：以 `LINE_CHANNEL_SECRET` 對**原始 body** 算 HMAC-SHA256、base64 後比對（`utils_line.verify_line_signature`，用 `hmac.compare_digest` 定時比對），不符就回 **403**，由 `LINE_VERIFY_SIGNATURE`（預設 `on`）控制。

**為什麼是必要的**：這個 endpoint 必須對網際網路開放（LINE 平台要連得到）且沒有其他身分驗證，簽章是唯一能確認請求來自 LINE 的手段。缺少驗證時，任何知道網址的人都能偽造事件：**只要不帶 `replyToken`，回覆就會依 4.6 的規則改走 Push，推送到偽造事件自己指定的 `userId`**，等於把 QA 知識庫、文件庫與唯讀 SQL（180 張 PMM 表／檢視）變成對外服務。4.5「不依員工身分控管、全員可查範圍相同」這個決議的隱含前提就是「只有公司 LINE 的使用者進得來」，簽章沒驗則前提不成立。

> 此驗證在改版前的 V1 不存在（`verify_line_signature()` 已寫好但 `app.py` 從未呼叫，V1 全部 commit 皆是），屬補強而非回歸。
> 本機測試改用 `tools/post_webhook.py`（會用 `.env` 的 Channel Secret 自行算簽章），不開「驗證關閉」的後門。

### 4.7 延遲目標與快速路徑

| 問題類型 | 目標（收到訊息 → 送出回覆） | 做法 |
|----------|------------------------------|------|
| 一般 QA 知識庫檢索 | **< 5 秒** | 快速路徑：問題直接 embedding（不做三元組抽取）→ 查記憶體快取 → 分數 ≥ `QA_FAST_PATH_MIN_SCORE` 就一次呼叫主模型作答，不跑迴圈、不驗證（約 1 次 embedding＋1 次 LLM） |
| 唯讀 SQL 查詢 | **< 5 秒** | 工具描述已含表結構（不需 `load_skill`）→ 第 1 輪產生 SQL → 執行 → 第 2 輪作答，不驗證（約 2 次 LLM＋1 次查詢） |
| 文件檢索、多步查詢、網路搜尋 | 可較久（預估 10–30 秒） | 完整 Agent 迴圈＋驗證器；超過 `LINE_PUSH_FALLBACK_SEC` 改用 Push |

快速路徑沒過門檻時（v1.9 補強）：那批 QA 命中**不丟掉**，直接當成「已呼叫過 `search_qa_kb`」的證據帶進 Agent 迴圈（分數 ≥ `QA_PREFETCH_MIN_SCORE`，預設 0.50；低於此視為雜訊不帶入，例如問安）。理由：向量檢索已經跑完等於免費，可省掉一次工具往返，也避免分數落在 0.5～0.8 這個「QA 有料但不夠高分」的區間時，模型完全不查就憑自身知識作答。帶入後會計入 `tools_used`，因此驗證器照樣檢查這批證據。

其他加速措施：
- 主控模型以 `AGENT_REASONING_EFFORT`（預設 `low`）呼叫，減少推理時間。
- 所有向量檢索都走記憶體快取（毫秒級），不再每次全表掃描。
- 同一輪有多個 tool_calls 時以執行緒並行執行。
- `IT_KB_AgentTrace.StepsJson` 記錄每個階段的耗時（embedding、各次 LLM、各工具、驗證），用來找出瓶頸、調整門檻。

> 5 秒目標取決於 OpenAI API 當下的回應速度，需以實測數據驗證；若主模型太慢，可另外設定較快的模型給快速路徑使用（預留 `OPENAI_MODEL_FAST`，空值＝沿用 `OPENAI_MODEL_CHAT`）。

---

## 5. Skill 擴充（G3）

### 5.1 格式

```
RBHelpDesk_AIAgent/skills/
  password-reset/
    SKILL.md          # 必要
  system-permission/
    SKILL.md
  db-query/
    SKILL.md          # 唯讀 SQL 的 schema 說明＋表白名單＋範例
  <自訂 skill>/
    SKILL.md
    tool.py           # 選配：提供可執行工具
```

`SKILL.md`：
```markdown
---
name: password-reset
description: 使用者詢問 AD／Email／系統密碼重設、帳號鎖定時使用
keywords: [密碼, 改密, 重設, 鎖定, password]   # 選填：問題含關鍵字時直接注入本文
---
（詳細作法、規則、話術、範例…）
```

`tool.py`（選配）：定義 `TOOLS = {"工具名": {"description": "...", "parameters": {JSON Schema}, "func": fn}}`，格式與 `agents/tools.py` 相同（範例見 `skills/README.md`）。

### 5.2 載入機制（新檔 `agents/skill_loader.py`）

1. 啟動時掃描 `skills/*/SKILL.md`，解析 YAML 標頭（`pyyaml`）。
2. **漸進揭露**：system prompt 只放各 Skill 的 `name＋description`，不放全文，節省 token。
3. **關鍵字直接注入**：問題文字命中某 Skill 的 `keywords` 時，直接把該 Skill 本文放進 prompt（快速路徑與 Agent 迴圈都適用），省下一輪 `load_skill`，讓密碼、權限這類常見問題也能維持 5 秒內。
4. 沒有命中關鍵字、但 Agent 判斷需要時呼叫 `load_skill(name)` → 回傳 SKILL.md 本文；若有 `tool.py`，把其中工具加入本次對話可用的工具清單（工具名自動加上 `<skill名>__` 前綴避免撞名）。
5. 每次請求檢查資料夾修改時間，有變動即重新載入，**不用重啟服務**。Skill 資料夾位置由 `SKILLS_DIR` 設定（預設 `RBHelpDesk_AIAgent/skills`）。
6. 安全：`tool.py` 是程式碼，只能由 IT 開發人員放到伺服器，**不提供網頁上傳**。

### 5.3 第一批內建 Skill

| Skill | 內容來源 |
|-------|----------|
| `password-reset` | 從 `KNOWLEDGE_BASE_PROMPT` 移出：`https://pass.royalbase.com` 自助改密、同步約 15 分鐘提示 |
| `system-permission` | 從 `KNOWLEDGE_BASE_PROMPT` 移出：權限問題導向電子表單申請 |
| `db-query` | 各 SQL 來源共通的撰寫規則（自動併入 `sql_query` 工具描述） |
| `db-pmm` | PMM 資料表的中文意義與關聯（對應 `SQL_PMM_SKILL`，併入 `sql_query` 的 `source=pmm` 段落） |

`KNOWLEDGE_BASE_PROMPT` 保留通用規則（問安、範圍外拒絕、多語言、輸出格式等）。

---

## 6. 後台知識管理（RBITQAContent 新增）

- 新增 `Controllers/DocumentController.cs` 與 `Views/Document/List.cshtml`、`Upload.cshtml`，沿用 `QAController` 的 Dapper 原生 SQL 與 AD Session 登入。
- **Upload**：多檔上傳（副檔名依 `DocUpload:AllowedExt`、大小依 `DocUpload:MaxSizeMB`）→ 原檔直接寫入 `IT_KB_SourceDoc.FileContent`（`SourceType=upload`、`Status=Pending`、`FileHash`、`UploadedBy`=登入者）。**不寫本機檔案、不需要共用資料夾**，因為 .NET 與 Python 在不同主機。同名且 hash 相同的檔案不重複建立。
- **List**：分頁列出文件名稱、來源、狀態、chunk 數、錯誤訊息、更新時間（查詢不選 `FileContent` 欄位，避免載入大量資料）；提供「重新索引」（改回 Pending）、「刪除」（改成 `Deleting`，由 Python 匯入程式清掉 chunk／relation／EntityChunk 後刪除該筆）、「下載原檔」（僅後台上傳的文件）。
- folder／gdrive／onedrive 來源的文件也會顯示在列表（唯讀，雲端來源附原始連結），但刪除要從來源端處理，否則下一輪同步會再匯入。
- 既有 QA 維護功能（`QAController`）不變；`OpenAIService`／`TripleExtractService`／`EmbeddingService` 的模型改讀 `appsettings.json :: OpenAI:*`。
- （選配）`AgentTrace` 查詢頁：查看每個問題走了哪些工具、驗證結果、耗時。

---

## 7. 運作情景（To-Be）

**情景 A' — 一般 IT 問題（QA 知識庫）**
使用者問「如何重設 RB-Mobile 密碼？」→ 關鍵字「密碼」命中 `password-reset` Skill，本文直接注入 → 快速路徑：QA 快取命中且分數 ≥ 門檻 → 一次呼叫主模型作答並附 `pass.royalbase.com` → 回覆（目標 < 5 秒）。若分數未達門檻，改走完整 Agent 迴圈。

**情景 G — 文件問題（新）**
使用者問「新進人員電腦領用流程？」→ `search_qa_kb` 無命中 → `search_documents` 命中《IT 資產管理 SOP.pdf》第 3 頁 → 驗證 pass → 分點回覆，文末附「參考來源：IT 資產管理 SOP.pdf（第 3 頁）」。

**情景 H — 多步查詢（新）**
使用者問「VPN 連不上，跟 FortiClient 版本有關嗎？」→ `search_documents` 找到 VPN 手冊 → `explore_entity("FortiClient")` 找到「FortiClient 需要 7.x 以上」的關係 → 證據足夠即停止 → 回覆。

**情景 I — 外部資訊（新）**
使用者問「Windows 11 24H2 已知問題有哪些？」→ 內部查無資料 → `web_search` → 回覆並標明資訊來自網路。

**情景 J — 即時資料查詢（新）**
使用者問「工號 A1234 的帳號被鎖了嗎？」→ 第 1 輪直接呼叫 `sql_query("SELECT TOP 50 ... WHERE EmpNo = 'A1234'")`（表結構已在工具描述中）→ 第 2 輪依查詢結果作答，不跑驗證 → 回覆（目標 < 5 秒）。若查詢的表不在該來源白名單，或 Agent 被誘導產生 `DELETE`／多語句 → 語法檢查拒絕並記錄到 Trace。

**情景 F' — 查無資料**
內部問題在 QA、文件都找不到 → 草稿若包含內部細節，驗證器判定 fail → 保守回覆：「目前知識庫查無此資訊…可輸入『真人客服』由專人協助」。

**情景 K — 文件上架（新）**
管理員在後台上傳《VPN 手冊.docx》→ 原檔寫入 DB，狀態 Pending → Python 主機上的 `ingest_docs.py` 下一輪從 DB 讀出原檔，解析、分塊、抽圖譜、向量化 → Done → `RAG_CACHE_REFRESH_SEC` 內快取更新，情景 G／H 即可查到。放到 `DOC_DROP_FOLDER`、Google Drive 資料夾或 M365 OneDrive 分享目錄的檔案走相同流程；OneDrive 上修改或刪除檔案後，下一輪 delta 同步就會更新或移除。回覆引用雲端文件時附上 `SourceUrl`，使用者可以直接點開原檔（開啟時仍套用 M365 權限）。

**情景 L — 新增自訂 Skill（新）**
IT 人員新增 `skills/printer-setup/SKILL.md`（＋`tool.py` 查印表機清單）→ 不重啟服務 → 使用者問印表機設定時，Agent 自動載入並使用。

**情景 B／C／D（圖片、今日科技新聞、轉真人客服）**：流程不變。

---

## 8. 選配項目（先不做，確認有需求再加）

- **全域搜尋（社群摘要）**：匯入批次完成後以 `networkx` Louvain 分群 → LLM 產生社群摘要 → 存 `IT_KB_Community`（含向量）→ 提供 `global_search` 工具，回答「整體性」問題（例如「我們有哪些系統會用到 AD 驗證？」）。
- **`tech-news` Skill**：把 `news_node` 包成 Skill 工具（Router 的「今日科技新聞」路徑保留）。
- **AgentTrace 後台查詢頁**。

---

## 9. 檔案異動一覽

| 類型 | 檔案 |
|------|------|
| 新增（Python） | `scheduler/ingest_docs.py`、`database/doc_graph_client.py`、`agents/nodes/agent_node.py`、`agents/tools.py`、`agents/skill_loader.py`、`skills/*/SKILL.md`、`sql/tobe_schema.sql` |
| 修改（Python） | `config.py`（載入第 2.1 節全部 env、`AGENT_SYSTEM_PROMPT`、驗證提示詞、精簡 `KNOWLEDGE_BASE_PROMPT`）、`.env`（新增參數）＋新增 `.env.example`（不含密鑰的參數範本）、`agents/graph_main.py`、`database/graph_ragc_client.py`（改用快取）、`agents/nodes/google_node.py`、`agents/nodes/reply_line_node.py`（loading／Push 備援）、`agents/nodes/ai_image_node.py`、`agents/nodes/ai_text_node.py`（模型改讀 env）、`agents/nodes/human_check_node.py`（逾時改讀 env）、`requirements.txt` |
| 新增套件 | `pymupdf`、`python-docx`、`openpyxl`、`python-pptx`、`tiktoken`、`sqlglot`、`pyyaml`、`google-api-python-client`、`google-auth`、`msal`（M365 取得 token，Graph API 用既有的 `requests` 呼叫）（選配：`networkx`） |
| 新增（.NET） | `Controllers/DocumentController.cs`、`Views/Document/List.cshtml`、`Views/Document/Upload.cshtml` |
| 修改（.NET） | `appsettings.json`（`OpenAI:*`、`DocUpload:*`）、`OpenAIService.cs`／`TripleExtractService.cs`／`EmbeddingService.cs`（模型改讀設定）、`Program.cs`（上傳大小上限對應 `DocUpload:MaxSizeMB`）、版面選單加入「文件管理」 |

**實作順序**：規格書審核 → 設定／唯讀帳號 → 資料表＋匯入＋檢索（先用資料夾測試）→ Agent 迴圈（`AGENT_MODE` 開關，先在 `/webhook/line_dev` 測試）→ Skill → .NET 後台 → 選配項目。

---

## 10. 確認事項（v1.1 已回覆）

| # | 事項 | 決議 | 規格反映 |
|---|------|------|----------|
| 1 | SQL 可查範圍 | 由 env 設定，不依員工身分控管 | `SQL_<名稱>_TABLES`（2.1、4.5） |
| 2 | Google Drive | 可建 service account，由 env 設定 | `GDRIVE_SA_JSON`、`GDRIVE_FOLDER_IDS`（2.1、3.2） |
| 2b | M365 OneDrive 分享目錄（v1.2 新增） | 透過 Microsoft Graph，由 env 設定 | `M365_*`、`ONEDRIVE_SHARE_URLS`、新表 `IT_KB_SyncState`（2.1、3.1、3.2） |
| 3 | 共用儲存路徑 | .NET 與 Python 不在同一台主機 | 後台上傳原檔存入 `IT_KB_SourceDoc.FileContent`，不用共用資料夾（3.1、6） |
| 4 | 延遲 | 一般 SQL 檢索 < 5 秒；文件檢索／Agent 可較久 | 快速路徑、SQL 略過驗證、Skill 關鍵字注入（4.7、5.2） |
| 5 | 成本 | 計量 API，暫不考量 | — |
| 6 | 設定位置 | 儘量放 `.env`／`appsettings.json` | 第 2 章參數總表 |

**剩餘待辦（實作時需要你提供）**
- 各 SQL 來源的唯讀帳號（填到該 Skill 的 `db.json`），以及白名單要不要保留帳號權限相關的表。
- service account 金鑰檔與要同步的 Drive 資料夾 ID（資料夾需分享給 service account email）。
- `SERPAPI_API_KEY`。
- M365：在 Entra ID 註冊應用程式，授予 Graph 應用程式權限 `Files.Read.All`（或 SharePoint 用 `Sites.Selected`）並由管理員同意，提供 Tenant ID／Client ID／Client Secret，以及要同步的資料夾分享連結。

---

## 11. 驗證方式

1. **匯入**：在 `DOC_DROP_FOLDER` 放 PDF／Word／Excel／PPT／MD 各一份，執行 `python scheduler/ingest_docs.py --once`；確認 `IT_KB_SourceDoc` 為 Done，`IT_KB_Chunk`／`IT_KB_Entity`／`IT_KB_Relation` 有資料，向量長度＝1536×4 bytes。修改檔案後重跑，確認舊 chunk 已被取代。Drive 端放一份 Google Doc 驗證同步。OneDrive 分享目錄：新增、修改、刪除各一個檔案，確認下一輪同步分別新增、更新、移除，且 `IT_KB_SyncState.DeltaLink` 有更新（第二輪只抓到變更的檔案）。
2. **檢索**：直接呼叫 `local_search("某份 SOP 內的問題")`，確認命中且出處正確；比較快取前後的查詢耗時。
3. **Agent 端到端**（POST `/webhook/line_dev`，檢查 log 與 `IT_KB_AgentTrace`）：依序驗證情景 A'、G、H、I、J、F'；對 `sql_query` 做提示詞注入測試（`DELETE`、多語句、`SELECT INTO`），確認都被擋下並有記錄；確認情景 B／C／D 行為不變；`AGENT_MODE=off` 可退回舊管線。
4. **Skill**：新增 `skills/test-skill/SKILL.md`＋`tool.py`，不重啟服務，提問觸發後確認有 `load_skill` 並呼叫到 skill 工具。
5. **後台**：上傳文件 → 狀態由 Pending 變 Done → LINE 端可查到；刪除後查不到。
6. **延遲**：各跑 10 題並統計 AgentTrace `LatencyMs`：QA 快速路徑題與 SQL 題的 P90 **< 5 秒**；文件／多步題記錄實際耗時；刻意讓處理超過 `LINE_PUSH_FALLBACK_SEC`，確認 Push 備援正常。未達 5 秒目標時，依 StepsJson 各階段耗時調整 `QA_FAST_PATH_MIN_SCORE`、`AGENT_REASONING_EFFORT` 或設定 `OPENAI_MODEL_FAST`。
7. **設定**：搜尋程式碼確認沒有寫死的模型名稱、門檻或路徑（Python 與 .NET 皆同）；移除 Skill 的 `db.json`、清空 `GDRIVE_FOLDER_IDS`／`ONEDRIVE_SHARE_URLS`，確認對應工具／同步會自動停用而不報錯。

---

## 12. 上線步驟

1. **資料庫**：在 `RBDev_TEST` 執行 `RBHelpDesk_AIAgent/sql/tobe_schema.sql`（可重複執行，已存在的表會略過）。
2. **唯讀帳號**（要用 SQL 工具才需要）：每個資料庫各請 DBA 建立登入帳號，只對該來源白名單表授予 SELECT，連線填到該 Skill 的 `db.json`（由 `db.json.example` 複製）。
3. **Python 套件**：`pip install -r requirements.txt`（新增 pymupdf、python-docx、openpyxl、python-pptx、tiktoken、sqlglot、pyyaml、google-api-python-client、google-auth、msal）。
4. **Python 設定**：參考 `.env.example` 補齊 `.env`（現有 `.env` 已附加新參數的預設值；密鑰類留空＝該功能停用）。
5. **Skill**：`skills/db-pmm/SKILL.md` 已依 PMM 文件寫好表說明，複製 `skills/db-pmm/db.json.example` 成 `db.json` 並填入唯讀帳號即可啟用。要接其他資料庫時，新增一個 Skill 資料夾（SKILL.md 寫 `db:`／`tables:` + `db.json`）即可，詳見 `skills/README.md`。
6. **啟動**：
   - LINE 助理：`python app.py`（啟動時會印出各功能 ON/OFF，並在背景載入向量快取）。
   - 文件匯入：`python scheduler/ingest_docs.py --loop`（另一個常駐程序，與 Flask 同一台主機）。
7. **.NET 後台**：發佈 RBITQAContent（新增「文件管理」選單；`appsettings.json` 已加入 `OpenAI:*`、`DocUpload:*`；`web.config` 已放寬 IIS 上傳大小）。
8. **回退**：`.env` 設 `AGENT_MODE=off` 並重啟 `app.py`，即退回改版前的固定管線。

> 本規格書為改版（To-Be）方案 v1.9，已納入第 10 章的回覆與 OneDrive 來源。審核通過後即依第 9 章順序開始實作。
