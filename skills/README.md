# Skills 資料夾

每個子資料夾是一個 Skill，放進來就會自動載入（不用重啟服務）。

```
skills/<名稱>/
  SKILL.md   必要
  tool.py    選配
```

## SKILL.md
```markdown
---
name: printer-setup                 # 唯一名稱（英數與連字號）
description: 使用者詢問印表機安裝、驅動、無法列印時使用   # AI 依這句判斷何時使用
keywords: [印表機, 列印, printer]   # 選填：問題含關鍵字時直接注入本文（較快）
db: pmm                             # 選填：要查的資料庫代號（見下方「Skill 要查資料庫時」）
tables: [V_Printer, V_PrintQueue]   # 選填：這個 Skill 需要查的資料表
---
（給 AI 看的作法、規則、話術、範例）
```

## tool.py（選配）
```python
def list_printers(floor: str) -> dict:
    # 回傳 dict；可包含 items: [{source_id, source_type, title, text, url}]
    return {"ok": True, "items": [...]}

TOOLS = {
    "list_printers": {
        "description": "依樓層列出印表機名稱與 IP",
        "parameters": {
            "type": "object",
            "properties": {"floor": {"type": "string", "description": "樓層，例如 3F"}},
            "required": ["floor"],
        },
        "func": list_printers,
    }
}
```
- AI 呼叫 `load_skill("printer-setup")` 後，工具會以 `printer-setup__list_printers` 的名稱加入可用清單。
- tool.py 是程式碼，只能由 IT 開發人員放到伺服器上。

## Skill 要查資料庫時

資料庫設定跟著 Skill 走，`.env` 不用動。一個 Skill 要查資料庫，資料夾長這樣：

```
skills/db-pmm/
  SKILL.md            宣告要查哪個資料庫、哪些表，本文寫表的意義
  db.json             連線設定（含密碼，不要外流、不要放進版控）
  db.json.example     範本，可以跟著 Skill 一起分享
```

`SKILL.md` 的標頭：

```markdown
---
name: db-pmm
description: PMM 蝴蝶蘭產銷管理系統（生產批次、庫存、訂單、配貨、出貨）
db: pmm                              # 資料庫代號
tables: >-                           # 這個 Skill 會用到的表
  CFOrder, CFOrderDetail, CFDistribution, BICustomer
---
（表的中文意義、關聯、範例查詢 → 會自動併進 sql_query 的工具說明）
```

#### `db:` 這個代號是什麼

**一個自己取的短名字，代表「一個資料庫連線」。** 它不是資料庫名稱，也不用跟 SQL Server 上的
DB 名稱一樣（上面的代號是 `pmm`，實際資料庫叫 `RBMS`）。同一個名字在三個地方串起來：

| 在哪裡 | 長什麼樣 | 誰用 |
|---|---|---|
| `SKILL.md` 的 `db:` | `db: pmm` | Skill 宣告「我要查這個資料庫」 |
| `db.json` 所在的資料夾 | 同一個 Skill 資料夾內 | 程式據此找到連線設定 |
| AI 呼叫工具時 | `sql_query(sql, source="pmm")` | AI 指定要查哪個資料庫 |
| `.env`（選配） | `SQL_PMM_CONN`、`SQL_PMM_DENY_TABLES` | IT 要接管或擋表時 |

命名規則：**英數與底線**，建議小寫、短、看得懂，例如 `pmm`、`erp`、`hr`、`mes`。
不要用中文、空白或連字號（`-`），因為它要能接成 `.env` 的參數名稱。

#### AI 怎麼知道該查哪一個

`sql_query` 的 `source` 參數是一份下拉選單，選項就是所有代號，每個代號後面附上說明文字，
而**說明文字就是該 Skill 的 `description`**。所以 AI 看到的是：

```
source: pmm＝PMM 蝴蝶蘭產銷管理系統（生產批次、庫存、訂單、配貨、出貨）
        erp＝ERP 進銷存（採購單、庫存異動、供應商）
```

它靠這句話判斷使用者的問題屬於哪個資料庫。**`description` 要寫這個庫裡有什麼資料**，
不要寫「PMM 相關查詢」這種看不出內容的句子，否則問題一多就會挑錯資料庫。

只有一個資料庫時，`source` 參數根本不會出現，AI 不用選也不會選錯。

#### 幾個代號就是幾個資料庫

- **多個 Skill 寫同一個代號** → 視為同一個資料庫，表清單自動合併。
  例如自家的 `db-pmm` 加上廠商給的 `vendor-pmm-report`，兩邊的 `tables:` 會併起來。
  這時來源說明取最先載入的那個 Skill 的 `description`（依資料夾名稱排序）。
- **代號不同** → 是不同的連線，白名單各自獨立，**不能互相 JOIN**。
  需要兩邊的資料就查兩次再自己對照。
- **沒寫 `db:`** → 看資料夾名稱，叫 `db-pmm` 就等於 `db: pmm`。
  `db-query` 是保留字（共通撰寫規則），不會被當成代號。
- **寫了 `db:` 但沒有 `db.json` 也沒在 `.env` 設定** → 這個來源不會啟用，
  啟動時會印出「要查資料庫 xxx，但沒有連線設定」。

`db.json`（兩種寫法都可以）：

```json
{
  "driver": "ODBC Driver 17 for SQL Server",
  "host": "10.1.1.40",
  "port": 1433,
  "database": "RBMS",
  "user": "唯讀帳號",
  "password": "",
  "trustServerCertificate": "yes"
}
```

```json
{ "connectionString": "Server=10.1.1.40,1433;Database=RBMS;User Id=ro;Password=x;TrustServerCertificate=yes" }
```

`connectionString` 寫 ODBC 格式（`DRIVER={...};SERVER=...`）或 .NET 格式（`Server=...;User Id=...`）都會自動處理。
沒填 `user` 時用 Windows 整合驗證。

### 常見操作

| 要做什麼 | 怎麼做 |
|---|---|
| 新增一個會查資料庫的 Skill | 建資料夾，放 `SKILL.md`（寫 `db:` 與 `tables:`）與 `db.json`，丟進 `skills/` |
| 換連線／換帳密／換伺服器 | 改該 Skill 的 `db.json`，不用重啟服務 |
| 暫時停用某個資料庫 | 把該 Skill 的 `db.json` 改名或刪掉，`sql_query` 就不會出現這個來源 |
| 裝了外來 Skill，不知道要設什麼 | 直接啟動服務，它會印出「要查資料庫 xxx，但沒有連線設定」並指出要複製哪個 `db.json.example` |
| 同一個資料庫有多個 Skill | `db:` 寫同一個代號即可，表清單自動合併 |

### IT 可以介入的地方（選配，寫在 `.env`）

平常不用設，但這兩個仍然有效：

```ini
# 擋表：不論 Skill 宣告了什麼，這裡列的一律不給查（結尾 * 為前綴比對）
SQL_PMM_DENY_TABLES=BIPersonel,BSPersonalRoleMap,BSRole,BSRoleFunctionMap,PersonelPermission

# 接管：由 IT 統一管理某個資料庫，設了就蓋過 Skill 自己的 db.json
SQL_SOURCES=pmm
SQL_PMM_CONN=DRIVER={ODBC Driver 17 for SQL Server};SERVER=...;DATABASE=RBMS;UID=;PWD=
SQL_PMM_TABLES=@skill        # 或直接列表名、或 *（唯讀帳號 SELECT 得到的全部）
```

參數名稱由資料庫代號推出：代號 `erp` 就是 `SQL_ERP_CONN`、`SQL_ERP_TABLES`…，程式裡沒有寫死任何名字。

### 注意

- `db.json` 裡有密碼。Skill 分享出去時只帶 `db.json.example`，不要帶 `db.json`。
- `db.json` 和 `tool.py` 一樣是伺服器上的檔案，只能由 IT 人員放置，不提供網頁上傳——放進去就等於信任它。
- **連線請一律用唯讀帳號**，不要用應用程式帳號。程式的語法檢查與白名單只是前兩道防線，DB 權限才是根本。
- 服務啟動時會列出每個資料庫實際可查幾張表、設定來自哪裡、有沒有被 DENY 擋掉，對不上一眼就看得出來。

設好之後 `sql_query(sql, source="pmm")` 就多一個可查的資料庫，**不用寫任何程式**。
共通的 SQL 撰寫規則放在 `skills/db-query/SKILL.md`，各資料庫共用。

自己在 tool.py 寫固定查詢時，這樣取連線，不要自己再讀一次設定檔：

```python
import pyodbc
from config import get_sql_source

def order_status(order_no: str) -> dict:
    src = get_sql_source("pmm")
    if not src:
        return {"ok": False, "items": [], "note": "尚未設定 pmm 資料庫連線"}
    with pyodbc.connect(src["conn"], timeout=10) as conn:
        row = conn.cursor().execute(
            "SELECT TOP 1 OrderNo, OrderDate FROM CFOrder WHERE OrderNo = ?", order_no
        ).fetchone()
    ...
```

固定 SQL 請用 `?` 參數，不要用字串相接。若要讓 AI 自由下 SQL，直接用內建的 `sql_query`（有語法檢查與白名單），不要自己再包一支。
