---
name: pmm
description: RoyalBase PMM（蝴蝶蘭產銷管理系統）領域工作流程，供 AI agent 處理以 MS SQL 為後端的生產、庫存異動、訂單、配貨、出貨、客戶、人員與蘭花作物資料。當 Codex、Claude 或其他 agent 需要讀取、新增或更新 PMM 紀錄；將使用者需求對應到 PMM 資料表/欄位；撰寫安全的 JSON payload 或 SQL；查閱 PMM 資料庫 schema/參考文件；或執行不可刪除、更新前必須先讀取並確認等 PMM 安全規則時使用。
---

# PMM

## 目的

使用此 Skill 在 RoyalBase PMM 中安全作業。PMM 是運行於 Windows Server、以 ASP.NET Core 開發、MS SQL 為後端資料庫的 Web 系統。PMM 以產線與流水帳式庫存異動記錄蝴蝶蘭生產流程，涵蓋苗株、盆花、切花、採購、契作、訂單、配貨、出貨、客戶、人員與基礎主檔資料。

請將本 Skill 內的本地參考文件視為資料表名稱、欄位、關聯與查詢模式的唯一可信來源。

## 資料庫連線設定檔

在嘗試任何即時 SQL 或透過工具執行的資料庫操作前，先從本地設定檔讀取 PMM 資料庫連線資訊。

可攜式設定慣例：

- `config/connection.json.example`：可隨 Skill 一起移動的範本檔。
- `config/connection.json`：本地保存真實 PMM 連線資訊的秘密設定檔。

不要把真實帳密寫進 `SKILL.md`、`agents/openai.yaml` 或參考文件。

建議的設定檔格式：

```json
{
  "driver": "ODBC Driver 18 for SQL Server",
  "connectionString": "Server=YOUR_SQL_HOST,1433;Database=YOUR_PMM_DATABASE;User Id=YOUR_USERNAME;Password=YOUR_PASSWORD;Encrypt=true;TrustServerCertificate=true;",
  "host": "YOUR_SQL_HOST",
  "port": 1433,
  "database": "YOUR_PMM_DATABASE",
  "user": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD",
  "encrypt": true,
  "trustServerCertificate": true
}
```

連線資訊的判斷順序：

1. 若 `config/connection.json` 存在且包含 `connectionString`，直接使用。
2. 否則由 `config/connection.json` 內的拆分欄位組合連線資訊。
3. 若檔案不存在或欄位不完整，停止執行並向使用者索取缺少的連線資訊，不可自行猜測。

除非使用者明確要求顯示實際設定值，否則不要將密碼或完整 connection string 回顯給使用者。回報設定狀態時，只說明必要欄位是已提供或缺少。

可攜式設定流程：

1. 將 `config/connection.json.example` 複製成 `config/connection.json`。
2. 在本機填入真實的 PMM 連線資訊。
3. 讓 PMM 工具、script 或 MCP layer 直接讀取 `config/connection.json` 建立 SQL 連線。
4. 以 `python scripts/query_pmm.py --test-connection` 或一筆小型唯讀查詢驗證 SQL 可用性。只要 PMM 腳本能成功連線或成功查詢，就以此作為 SQL 可用性的判定標準。
5. 不要只依賴 `Test-NetConnection` 來判斷 PMM SQL 是否可達。對 `10.1.1.40:1433` 的 TCP 探測可能失敗，但 `query_pmm.py` 仍可能成功連線並執行真實 SQL。

## Session 約定

此環境的有效桌面路徑以 `G:\OneDrive\Desktop` 為準。不要把 `.NET` 或 shell API，例如 `GetFolderPath('Desktop')`，當作這個 session 的唯一判定來源，因為它可能無法正確解析被重導的桌面資料夾。

## 必讀參考文件

僅在需要時載入參考文件：

- `references/pmm-skill-spec.md`：PMM 讀取、新增、更新操作的核心行為規則。
- `references/database-query-guide.md`：資料表清單、模組前綴、常見查詢範例與模組分類。
- `references/database-relationships.md`：跨資料表關聯、JOIN 與進階查詢範例。
- `references/database-design-spec.md`：完整資料庫設計規格書。此檔案較大，閱讀段落前應先用 `rg` 搜尋資料表名稱、欄位名稱、ID 或中文業務詞彙。

常用搜尋範例：

```bash
rg -n "BICustomer|CFOrder|PPOrder|YPProductionBatch|TransferRecord|Ship|Distribution" references/
rg -n "<table-or-field-name>" references/database-design-spec.md
```

## 安全規則

絕對不可刪除 PMM 紀錄。若使用者要求刪除資料，必須明確告知此服務不提供刪除功能。若情境適合，可建議透過更新操作將紀錄標記為封存、停用、失效或其他狀態型處理。

不可自行編造資料表名稱、欄位名稱、ID、必填欄位或資料表關聯。建立查詢、payload 或更新前，必須先從參考文件驗證。

在撰寫任何即時 SQL 前，必須先檢查目標 schema。先用本地參考文件找候選資料表，再用 `scripts/query_pmm.py --find-table` 與 `scripts/query_pmm.py --describe-table` 對 live PMM 資料庫確認正確的資料表名稱、欄位名稱、型別與是否允許空值。

執行操作前，若缺少關鍵參數，必須先詢問使用者。常見必要參數包含目標模組、資料表/實體、日期範圍、狀態、ID 或唯一識別鍵、客戶、產線、批次、訂單編號、出貨/配貨單號，以及要變更的欄位值。

除非實際工具或系統回應已確認操作成功，不可宣稱已執行資料庫操作。若目前沒有 `read_records`、`create_record` 或 `update_record` 可用，應提供已準備好的查詢/payload，並說明仍需 PMM 資料工具或 API 執行。

`scripts/query_pmm.py` 僅能用於唯讀查詢，不可用於新增、更新或刪除操作。腳本會在真正執行前先用 SQL Server metadata 做 preflight 驗證，提早擋下不存在的資料表或欄位名稱。

## 操作判斷

接觸資料前，先分類使用者需求：

- 讀取：搜尋、查找、顯示、列出、檢視、確認狀態、報表、摘要、追蹤、計數。
- 新增：新增、建立、登錄、加入、建立新任務/訂單/客戶/批次/紀錄。
- 更新：修改、變更、更正、調整、核准、標記停用/封存、局部更新特定欄位。
- 刪除：拒絕刪除，並建議改用狀態型更新替代。

## 讀取流程

1. 判斷業務模組與可能的資料表/檢視表。
   - `BI`：基礎主檔，例如品種、客戶、人員、產線。
   - `BS`：角色與權限。
   - `LC`：版本與已執行 SQL 紀錄。
   - `CF`：切花作業。
   - `PP`：盆花作業。
   - `YP`：苗株作業。
   - `SC`：採購與契作作業。
2. 讀取 `database-query-guide.md` 選擇資料表；若需跨表追蹤或報表，讀取 `database-relationships.md`。
3. 需要精確欄位、ID、必填值或資料表細節時，搜尋 `database-design-spec.md`。
4. 撰寫 SQL 前，先確認 live table schema：
   - `python scripts/query_pmm.py --find-table Customer`
   - `python scripts/query_pmm.py --describe-table BICustomer`
5. 從使用者需求擷取篩選條件：日期範圍、狀態、客戶、訂單編號、批次、產線、人員、品種、花色、製程或 ID。
6. 若 `read_records` 可用，呼叫該工具；否則用 `scripts/query_pmm.py` 執行經過驗證的唯讀 SQL 查詢。
7. 以精簡清單或表格回報結果。包含 ID 與可讀名稱，方便後續更新時鎖定正確紀錄。

本地查詢腳本範例：

```bash
python scripts/query_pmm.py --check-config
python scripts/query_pmm.py --test-connection
python scripts/query_pmm.py --find-table Customer
python scripts/query_pmm.py --describe-table BICustomer
python scripts/query_pmm.py --sql "SELECT TOP 20 ID, Code, NameShort, Name FROM BICustomer ORDER BY ID"
python scripts/query_pmm.py --file sql/customer_list.sql --format json
```

## 新增流程

1. 從參考文件確認目標資料表/實體與必填欄位。
2. 準備新增操作前，先向使用者詢問缺少的必填欄位。
3. 使用已驗證的欄位名稱，整理成清楚的 JSON payload。
4. 若 `create_record` 可用，呼叫該工具。
5. 回報新增成功的紀錄 ID、關鍵欄位，以及工具/API 回傳的任何警告。

若沒有更嚴格的本地慣例，優先使用以下 payload 形狀：

```json
{
  "table": "VerifiedTableName",
  "data": {
    "VerifiedFieldName": "value"
  }
}
```

## 更新流程

1. 必須具備目標 ID 或唯一查詢條件。若目標不明確，先執行讀取/搜尋，請使用者選擇。
2. 呼叫 `update_record` 前，必須一律先呼叫 `read_records`。
3. 展示目前紀錄值與精確的預計變更欄位。
4. 執行更新前，請使用者確認。
5. 只有在使用者確認後，才呼叫 `update_record`。
6. 回報已更新的 ID、變更欄位與最終狀態。

若沒有更嚴格的本地慣例，優先使用以下 patch 形狀：

```json
{
  "table": "VerifiedTableName",
  "id": "record-id-or-primary-key",
  "data": {
    "FieldToChange": "new value"
  }
}
```

## 查詢指引

當既有檢視表符合報表需求時，優先使用檢視表，尤其是訂單-配貨-出貨追蹤、移轉彙總、生產批次彙總、權限彙總等關聯複雜的情境。

處理單頭/單身文件時，應刻意區分兩層資料：

- 單頭資料表通常保存單號、日期、客戶、建立者、狀態與高階 metadata。
- 單身資料表通常保存數量、品種/規格/製程/批次參照、包裝設定與項目層級事實。
- `Map` 資料表通常表示多對多關係，可能造成資料列倍增；做總量報表時，視需要使用 `GROUP BY`、`SUM()` 或明確 key 去重。

跨模組問題應先從業務鏈出發：

- 切花訂單：`CFOrder` -> `CFOrderDetail` -> 配貨 map/detail -> 出貨 map/detail。
- 盆花訂單：使用平行的 `PP` 訂單、配貨、包裝與出貨資料表。
- 苗株庫存：檢查 `YPProductionBatch`、挑苗、進貨、移轉與出貨紀錄。
- 人員權限：`BIPersonel` -> 角色 map -> `BSRole` -> 角色功能 map；若需操作範圍，另查產線 map。

## 回應標準

清楚說明已讀取、新增或更新了什麼。除非使用者另有要求，面對 PMM 業務使用者時使用中文。

操作失敗時，以白話說明原因並給出下一個具體修正方式，例如缺少必填欄位、ID 無效、目標不明確、不支援刪除或 schema 不相符。

對於高風險或範圍過大的變更，先縮小到特定欄位與特定紀錄，再請使用者確認。
