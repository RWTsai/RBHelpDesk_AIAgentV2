# config.py
"""
全域設定檔，所有連線字串、API 金鑰、資料庫連線都放在這裡。

重點：
- 不做複雜分層
- 不做 class Config
- 快速取得環境變數，用得到才吃
- MSSQL 使用 pyodbc + with 自動釋放
- LINE、OpenAI、Supabase 管理

使用方式（在哪裡都一樣）：
    from config import get_mssql_conn, OPENAI_API_KEY, LINE_CHANNEL_TOKEN

"""

import os
import re
import pyodbc
from dotenv import load_dotenv

# ============================================
# 1. 載入 .env
# ============================================

# 會自動讀取專案根目錄的 .env
load_dotenv()


# ============================================
# 2. 讀取環境變數（統一集中）
#    原則：模型、門檻、上限、逾時、路徑、清單都從 .env 讀，程式內只留預設值
# ============================================

def _env_str(key, default=""):
    """讀字串，空白視為未設定"""
    val = os.getenv(key)
    return val.strip() if val and val.strip() else default

def _env_int(key, default):
    try:
        return int(_env_str(key, str(default)))
    except ValueError:
        return default

def _env_float(key, default):
    try:
        return float(_env_str(key, str(default)))
    except ValueError:
        return default

def _env_bool(key, default):
    """on/true/1/yes 視為 True"""
    val = _env_str(key, "")
    if not val:
        return default
    return val.lower() in ("on", "true", "1", "yes")

def _env_list(key, default=""):
    """逗號分隔清單 → list（去空白、去空值）"""
    return [x.strip() for x in _env_str(key, default).split(",") if x.strip()]


# --- OpenAI 模型 ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_EMBED = _env_str("OPENAI_MODEL_EMBED", "text-embedding-3-small")
OPENAI_MODEL_CHAT = _env_str("OPENAI_MODEL_CHAT", "gpt-5.1")          # Agent 主控（規劃＋回覆）
OPENAI_MODEL_FAST = _env_str("OPENAI_MODEL_FAST", OPENAI_MODEL_CHAT)  # 快速路徑，空值＝沿用 CHAT
OPENAI_MODEL_VERIFY = _env_str("OPENAI_MODEL_VERIFY", "gpt-4o-mini")  # 答案驗證
OPENAI_MODEL_EXTRACT = _env_str("OPENAI_MODEL_EXTRACT", "gpt-4o")     # 三元組／實體關係抽取
OPENAI_MODEL_VISION = _env_str("OPENAI_MODEL_VISION", "gpt-4o")       # 圖片分析
AGENT_REASONING_EFFORT = _env_str("AGENT_REASONING_EFFORT", "low")    # 推理強度，空值＝不帶此參數

# --- Agent ---
AGENT_MODE = _env_bool("AGENT_MODE", True)                    # False＝退回舊的 ai_text_node 管線
AGENT_MAX_STEPS = _env_int("AGENT_MAX_STEPS", 4)              # 最多幾輪工具呼叫
AGENT_MAX_VERIFY_RETRY = _env_int("AGENT_MAX_VERIFY_RETRY", 1)  # 驗證 needs_more 時最多補查幾次
AGENT_TOOL_RESULT_MAX_CHARS = _env_int("AGENT_TOOL_RESULT_MAX_CHARS", 4000)
AGENT_FAST_PATH = _env_bool("AGENT_FAST_PATH", True)
QA_FAST_PATH_MIN_SCORE = _env_float("QA_FAST_PATH_MIN_SCORE", 0.80)
QA_TRIPLE_EXPAND = _env_bool("QA_TRIPLE_EXPAND", True)        # search_qa_kb 是否先做三元組擴展
VERIFY_ENABLED = _env_bool("VERIFY_ENABLED", True)
VERIFY_EVIDENCE_MAX_CHARS = _env_int("VERIFY_EVIDENCE_MAX_CHARS", 12000)

# --- 檢索 ---
RAG_QA_TOP_K = _env_int("RAG_QA_TOP_K", 5)
RAG_DOC_TOP_K = _env_int("RAG_DOC_TOP_K", 6)
RAG_ENTITY_TOP_K = _env_int("RAG_ENTITY_TOP_K", 5)
RAG_MIN_SCORE = _env_float("RAG_MIN_SCORE", 0.30)
RAG_CACHE_REFRESH_SEC = _env_int("RAG_CACHE_REFRESH_SEC", 60)

# --- 唯讀 SQL 工具 ---
MSSQL_READONLY_CONN = _env_str("MSSQL_READONLY_CONN")         # 舊版單一資料庫設定（仍相容）
SQL_ALLOWED_TABLES = _env_list("SQL_ALLOWED_TABLES")
SQL_MAX_ROWS = _env_int("SQL_MAX_ROWS", 50)
SQL_TIMEOUT_SEC = _env_int("SQL_TIMEOUT_SEC", 10)
# 白名單表數超過此值時，工具說明只列表名，欄位改由 describe_table 工具現查（避免提示詞過長）
SQL_SCHEMA_INLINE_MAX = _env_int("SQL_SCHEMA_INLINE_MAX", 20)


def _load_sql_sources():
    """
    .env 這邊設定的唯讀資料庫來源（選配）。

    一般情況**不用設**：Skill 自己在資料夾裡帶連線設定與表清單（見 skills/README.md），
    服務會自動接上。這裡只給兩種情況用：
      1. 不屬於任何 Skill、由 IT 直接維護的資料庫
      2. 要覆蓋某個 Skill 的連線或白名單（同名時 .env 優先）

    .env 寫法（來源名稱只能用英數與底線）：
        SQL_SOURCES=pmm,erp
        SQL_PMM_CONN=DRIVER={...};SERVER=...;DATABASE=RBMS;UID=;PWD=
        SQL_PMM_TABLES=CFOrder,CFOrderDetail,...      # 白名單，各資料庫分開設定
        SQL_PMM_DESC=PMM 蝴蝶蘭產銷管理系統            # 給 AI 判斷該查哪個資料庫
        SQL_PMM_DENY_TABLES=Salary*,BIPersonel        # 選填，永遠不給查（可用結尾 *）
        SQL_PMM_SKILL=db-pmm                          # 選填，只認這一個 Skill（見下）

    名稱（上面的 PMM）是自己取的，程式不認得特定名字：SQL_SOURCES 寫什麼，
    就去找 SQL_<那個名字大寫>_CONN／_TABLES／_DESC…。要接新資料庫就加一個名字再複製一組。

    `SQL_<名稱>_TABLES` 有三種寫法，可以混用（逗號分隔）：
        明列表名     CFOrder,CFOrderDetail        最嚴格，IT 自己維護
        @skill       用「宣告要查這個來源」的 Skill 自己列的 tables
                     （Skill 在 SKILL.md 寫 `db: pmm` + `tables:`，IT 不必知道它叫什麼名字）
        *            唯讀帳號 SELECT 得到的表全部可查（白名單交給 DB 權限決定）
    三種寫法都會再扣掉 DENY_TABLES。
    SQL_<名稱>_SKILL 平常不用設；設了就只認這一個 Skill，其他宣告要查本來源的一律不採用。
    """
    out = {}
    for raw in _env_list("SQL_SOURCES"):
        name = raw.strip().lower()
        if not name or not re.fullmatch(r"[a-z0-9_]+", name):
            print(f"[config] 略過不合法的 SQL 來源名稱：{raw}（只能用英數與底線）")
            continue
        prefix = f"SQL_{name.upper()}_"
        conn = _env_str(prefix + "CONN")
        tables = _env_list(prefix + "TABLES")
        if not conn or not tables:
            print(f"[config] SQL 來源 {name} 未啟用：{prefix}CONN 或 {prefix}TABLES 是空的")
            continue
        out[name] = {
            "conn": conn,
            "tables": tables,
            "deny": _env_list(prefix + "DENY_TABLES"),
            "desc": _env_str(prefix + "DESC") or name,
            "skill": _env_str(prefix + "SKILL"),   # 空＝接受所有宣告 db: <名稱> 的 Skill
        }
    # 舊版單一資料庫設定 → 視為名為 default 的來源
    if MSSQL_READONLY_CONN and SQL_ALLOWED_TABLES:
        out.setdefault("default", {
            "conn": MSSQL_READONLY_CONN,
            "tables": SQL_ALLOWED_TABLES,
            "deny": _env_list("SQL_DEFAULT_DENY_TABLES"),
            "desc": _env_str("SQL_DEFAULT_DESC") or "公司內部資料庫",
            "skill": _env_str("SQL_DEFAULT_SKILL"),
        })
    return out


ENV_SQL_SOURCES = _load_sql_sources()                         # .env 設的來源（通常是空的）


def get_sql_source(name: str) -> dict:
    """
    給 Skill 的 tool.py 取用連線設定：from config import get_sql_source
    回傳合併後的結果（Skill 資料夾內的設定 + .env 覆蓋）。
    """
    from agents.tools import sql_sources          # 延遲載入，避免循環 import
    return sql_sources().get((name or "").strip().lower())

# --- 網路搜尋 ---
SERPAPI_API_KEY = _env_str("SERPAPI_API_KEY")                 # 空＝停用 web_search
WEB_SEARCH_NUM = _env_int("WEB_SEARCH_NUM", 5)

# --- Skill ---
SKILLS_DIR = _env_str("SKILLS_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills"))

# --- 文件匯入 ---
# 視覺解析：投影片／PDF 頁面文字太少（多為截圖、掃描版）時，把圖片送視覺模型轉成文字再分塊
DOC_VISION_ENABLED = _env_bool("DOC_VISION_ENABLED", False)
DOC_VISION_MIN_CHARS = _env_int("DOC_VISION_MIN_CHARS", 100)   # 該頁文字少於這個字數才送
DOC_VISION_MAX_IMAGES = _env_int("DOC_VISION_MAX_IMAGES", 4)   # 每頁最多送幾張圖
DOC_VISION_MIN_PIXELS = _env_int("DOC_VISION_MIN_PIXELS", 40000)  # 小於這個像素數的圖（logo、圖示）跳過
DOC_VISION_PDF_DPI = _env_int("DOC_VISION_PDF_DPI", 150)       # PDF 頁面算繪解析度
DOC_DROP_FOLDER = _env_str("DOC_DROP_FOLDER")                 # 空＝不掃資料夾
DOC_ALLOWED_EXT = [x.lower().lstrip(".") for x in _env_list("DOC_ALLOWED_EXT", "pdf,docx,xlsx,pptx,md,txt")]
INGEST_INTERVAL_SEC = _env_int("INGEST_INTERVAL_SEC", 300)
INGEST_WORKERS = _env_int("INGEST_WORKERS", 4)                # 圖譜抽取並行數
CHUNK_TOKENS = _env_int("CHUNK_TOKENS", 800)
CHUNK_OVERLAP = _env_int("CHUNK_OVERLAP", 100)
EXCEL_ROWS_PER_CHUNK = _env_int("EXCEL_ROWS_PER_CHUNK", 50)
ENTITY_DESC_MAX_CHARS = _env_int("ENTITY_DESC_MAX_CHARS", 1500)  # 實體描述超過就用 LLM 摘要

# --- Google Drive ---
GDRIVE_SA_JSON = _env_str("GDRIVE_SA_JSON")
GDRIVE_FOLDER_IDS = _env_list("GDRIVE_FOLDER_IDS")            # 空＝不同步

# --- M365 OneDrive / SharePoint ---
M365_TENANT_ID = _env_str("M365_TENANT_ID")
M365_CLIENT_ID = _env_str("M365_CLIENT_ID")
M365_CLIENT_SECRET = _env_str("M365_CLIENT_SECRET")
ONEDRIVE_SHARE_URLS = _env_list("ONEDRIVE_SHARE_URLS")        # 空＝不同步
ONEDRIVE_RECURSIVE = _env_bool("ONEDRIVE_RECURSIVE", True)

# --- 真人客服 ---
ARTIFICIAL_TIMEOUT_MINUTES = _env_int("ARTIFICIAL_TIMEOUT_MINUTES", 15)

# --- LINE ---
LINE_CHANNEL_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_PUSH_FALLBACK_SEC = _env_int("LINE_PUSH_FALLBACK_SEC", 50)  # 處理超過此秒數改用 Push API
LINE_LOADING_SECONDS = _env_int("LINE_LOADING_SECONDS", 30)      # loading 動畫秒數（5 的倍數，最多 60）

# LINE API URL
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"
LINE_LOADING_URL = "https://api.line.me/v2/bot/chat/loading/start"

# LINE Get Image URL
LINE_GET_IMAGE_URL = "https://api-data.line.me/v2/bot/message/{message_id}/content"

# --- Supabase（向量知識庫） ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- MSSQL ---
MSSQL_CONN_STR = os.getenv("MSSQL_CONN")


# ============================================
# 3. 資料庫連線
# ============================================

def get_mssql_conn():
    """
    建立 MSSQL 連線（使用 pyodbc）。  
    使用方式：
        with get_mssql_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT GETDATE()")
                row = cursor.fetchone()
                print(row)

    注意：
    - 若環境變數沒設定會直接 raise
    """
    if not MSSQL_CONN_STR:
        raise RuntimeError("尚未設定 MSSQL_CONN 環境變數")

    try:
        conn = pyodbc.connect(MSSQL_CONN_STR)
        return conn
    except Exception as e:
        print(f"[config] MSSQL 連線失敗：{e}")
        raise


# ============================================
# 4. 基礎診斷
# ============================================

def print_config_status():
    """
    認哪些設定有載入成功。
    在 app 啟動時手動呼叫。
    """
    print("=== Config Status ===")
    print(f"OPENAI_API_KEY: {'OK' if OPENAI_API_KEY else 'MISSING'}")
    print(f"LINE_CHANNEL_TOKEN: {'OK' if LINE_CHANNEL_TOKEN else 'MISSING'}")
    print(f"LINE_CHANNEL_SECRET: {'OK' if LINE_CHANNEL_SECRET else 'MISSING'}")
    print(f"SUPABASE_URL: {'OK' if SUPABASE_URL else 'MISSING'}")
    print(f"SUPABASE_KEY: {'OK' if SUPABASE_KEY else 'MISSING'}")
    print(f"MSSQL_CONN_STR: {'OK' if MSSQL_CONN_STR else 'MISSING'}")
    print(f"AGENT_MODE: {AGENT_MODE}  CHAT={OPENAI_MODEL_CHAT}  FAST={OPENAI_MODEL_FAST}  VERIFY={OPENAI_MODEL_VERIFY}")
    # SQL 來源含 Skill 自帶的設定，詳細狀況由 agents.tools.check_sql_sources() 印出
    print(f"sql_query: {'.env 來源：' + ', '.join(ENV_SQL_SOURCES) if ENV_SQL_SOURCES else '.env 未設來源（看下方 Skill 來源）'}")
    print(f"web_search: {'ON' if SERPAPI_API_KEY else 'OFF'}")
    print(f"GDrive 同步: {'ON' if GDRIVE_FOLDER_IDS and GDRIVE_SA_JSON else 'OFF'}")
    print(f"OneDrive 同步: {'ON' if ONEDRIVE_SHARE_URLS and M365_CLIENT_ID else 'OFF'}")
    print("======================")

# ===========================================
# 5.知識庫提示詞注意事項
# ===========================================
SYSROLE_PROMPT = """你是皇基資訊部的RBIT AI智能助理，擅長快速解決企業內部的技術問題，我的 LINE 官方帳號 ID 是：**@389eqwdx**，除此之外的問題都要委婉拒絕，且在專業問題上你的回答需要準確、清晰、實用。
"""

SYSROLE_IMAGEPROMPT="""你是一位專業 IT 內部客服人員，擅長理解螢幕截圖與錯誤畫面。你的回答需要準確、清晰、實用。
"""

IMAGE_BASE_PROMPT="""
    請協助解讀這張圖片，說明它看起來是什麼並嘗試提供可能的解決方案。
    """

SYSTEM_BASE_PROMPT="""
    請根據使用者提問與公司知識庫內容，提供清楚、專業且貼近人類的自然語言回答，當使用者詢問時的語言不是繁體中文時，你需要先翻譯爲繁體中文再進行知識庫檢索，回答時再依據使用者原發問語言翻譯回覆。
    """

# 通用規則（Agent 與舊管線共用）；密碼、權限等專項規則已搬到 skills/，見下方 LEGACY_SKILL_RULES
KNOWLEDGE_BASE_PROMPT_CORE = """
    --當使用者訊息僅是問安,打招呼等詞彙時，請禮貌回覆"您好！有什麼我可以幫您解決的資訊系統問題嗎？"。
    --當使用者詢問電腦系統,資訊系統以外的問題時請委婉拒絕使用者，說明不在你可理解的知識範圍內，除了'切花配貨','盆花配貨','切花配銷'等字眼是在知識庫的內部系統範圍內。
    -調用今日科技新聞與文章查詢工具請確保與檢查新聞訊息內[閱讀更多]的URL可以正確點擊，避免在URL出現")","("等無意義的字元。
    -調用知識查詢工具時,你需依據提供的知識庫內容進行回應，並整合吸收後給出明確、實用的回答。
    -當使用者詢問時的語言不是繁體中文時，你需要先翻譯爲繁體中文再進行知識庫檢索，回答式再依據使用者原發問語言翻譯回覆。
    -當在知識庫找不到解答時,你將優先使用本身LLM的知識回答,並且善加利用上下文來優化回覆，避免直接告知使用者無法回答。
    -當使用者詢問的訊息如果不是感謝詞彙而且資訊過於精簡無法理解時，請回覆"我雖然是 AI助理，但還不是萬能的神仙😂。如果你沒有提供更詳細的資訊（例如操作前因後果、錯誤訊息、操作步驟或畫面截圖），不然就算我想幫，也只能猜測喔～麻煩你再補充一下細節，我才能精準協助你解決問題"。
    -當使用者傳送的是經由AI從圖片中的訊息，請使用嘗試使用內容瞭解使用者的問題，提出解決方案建議，並且回覆中要包含使用者傳送中解析的圖片訊息。
    -當使用者回覆的訊息表示很急的時候，可以回覆-"哎呀～現在才開始急喔？早點動工的話，這會兒就能優雅地喝茶啦～☕」"
    -當使用者要求資訊部同事服務時，請回覆"若您需要資訊部同事協助處理，請留言"真人客服"，我會記錄您的問題並會再指派專人回覆，請耐心等待不要重複留言。"
    -當回覆內容較多或涉及步驟、多個重點時，請務必以分點、分段的方式呈現。可以使用編號、項目符號來條列說明，並適當運用空行與小標題來組織內容，以提升可讀性。回覆時若內容較多請幫我章節、條列清晰，讓訊息可讀性好一點。
    【回覆規範】
    -拒絕過度延伸： 「嚴禁提供任何未被要求的建議（Unsolicited advice）。如果我沒有問，請不要教我怎麼做。」
    -零冗餘： 刪除所有「建議」、「提醒」、「注意」或「總結」段落。
    -專業冷淡： 保持語氣中立客觀，像說明書一樣精簡，不要表現出「助手」的熱情。
    -直擊重點： 輸出使用者詢問的解答內容，不需重複我的問題，也不需解釋原因。
    -    -只回答問題本身： 「請僅針對提問內容進行回答，若問題不在知識庫內或非公衆可檢索的內部系統問題，請不要自行捏造訊息。」
"""

# 舊管線（AGENT_MODE=off）仍需要的專項規則；Agent 模式改由 skills/password-reset、skills/system-permission 提供
LEGACY_SKILL_RULES = """
    -當使用者詢問無法登入,密碼過期類似問題時，除了知識庫內容之外，你要再附加一個使用者自助式恢復密碼的系統服務(網址:https://pass.royalbase.com)並且提示使用者密碼修改完需要等待15分鐘同步所有系統，不要重複嘗試避免帳號又被鎖定。
    -當使用者詢問關於各類系統權限開通設定問題，例如:ERP系統權限、電子表單系統權限、遠端桌面連線權限、PMM權限、NAS資料夾權限、網路連線WiFi 等公司系統權限時，請回覆"請您至電子表單系統 填寫並送出資訊服務需求申請單。"
"""

# 舊管線使用的完整規則（與改版前內容相同）
KNOWLEDGE_BASE_PROMPT = KNOWLEDGE_BASE_PROMPT_CORE + LEGACY_SKILL_RULES


# ===========================================
# 6. Agent 提示詞（To-Be 新增）
# ===========================================

# Agent 主控的工具使用規則；{skill_catalog}、{today} 由 agent_node 代入
AGENT_SYSTEM_PROMPT = """
【你的工作方式】
你可以呼叫工具查資料，自己決定去哪裡找、要不要繼續查，查夠了再回答。

【工具使用規則】
1. 公司內部問題先查內部：search_qa_kb（QA 知識庫）→ search_documents（SOP、手冊等文件）；需要追查某個系統／設備的關聯時用 explore_entity。
2. 內部查不到，或明顯需要外部、最新資訊（例如軟體版本、公開的錯誤碼說明）時，才用 web_search；回答時要說明資訊來自網路。
3. 需要即時資料（例如帳號狀態）時用 sql_query；只能寫單一 SELECT，只能查工具說明中列出的表。
4. 同樣的查詢不要重複呼叫；證據足夠就停止查詢並作答。問安、閒聊、範圍外的問題不需要呼叫工具。
5. 問題符合下方某個 Skill 的描述時，先呼叫 load_skill 取得作法再處理（已直接提供內容的 Skill 不必再載入）。
6. 公司內部系統、流程、帳號的資訊只能依據工具取得的證據，不得捏造；一般 IT 常識可以用你自己的知識補充。
7. 使用者不是用繁體中文發問時，查詢時先轉成繁體中文關鍵字，回答時用使用者的語言。

【引用來源】
回答的最後一行固定輸出「SOURCES: 」加上你實際引用的來源編號（工具結果中的 source_id，例如 DOC-12, WEB-3），以逗號分隔；沒有引用任何來源時輸出「SOURCES: 無」。這一行系統會自動移除，使用者看不到。

【可用 Skill】
{skill_catalog}

今天日期：{today}
"""

# 快速路徑：QA 知識庫高分命中時直接作答
FAST_PATH_PROMPT = """{system_base}

【使用者問題】
{question}

[歷史對話]
{history}

[公司知識庫]
{kb_text}

{skill_text}

【回答要求】
1. 依照公司知識庫內容回答，結合原始知識來源提供完整的操作步驟
2. 直接給出解決方案，不需要說明推論過程
3. {rules}

請開始你的回答："""

# 驗證器
VERIFY_PROMPT = """你是 IT 客服回覆的品質檢查員。請檢查「草稿答案」是否可以直接回覆給使用者。

【檢查項目】
1. 草稿中關於公司內部系統、流程、帳號、網址、聯絡方式等內部資訊，是否都能在「證據」中找到依據（一般 IT 常識不需要證據）。
2. 是否確實回答了使用者的問題。
3. 是否符合回覆規則（分點清楚、不捏造）。

【判定】
- pass：可以直接回覆。
- needs_more：方向正確，但缺少關鍵資訊，再查一次可能補足（請在 feedback 寫出建議查什麼）。
- fail：草稿含有沒有證據支持的內部資訊，或證據明顯不足以回答。

【使用者問題】
{question}

【證據】
{evidence}

【草稿答案】
{draft}
"""

# 驗證失敗時的保守改寫
CONSERVATIVE_PROMPT = """品質檢查發現草稿有問題：
- 沒有證據支持的內容：{unsupported}
- 缺少的資訊：{missing}

請重寫答案：只保留有證據支持的內容；不確定的部分明確說明「目前知識庫查無此資訊」；
結尾提示使用者「若需要資訊部同事協助，請輸入『真人客服』」。最後一行照樣輸出 SOURCES。"""


# ===========================================
# 7. 文件 GraphRAG 抽取提示詞（To-Be 新增，給 scheduler/ingest_docs.py）
# ===========================================
DOC_GRAPH_EXTRACTION_PROMPT = """你是企業 IT 知識圖譜建構助理。請從下面的文件片段抽取「實體」與「關係」。

【實體】系統、軟體、設備、網站、帳號類型、部門、角色、流程、表單、設定項目、錯誤訊息等。
- name：實體名稱（使用文件中的原始寫法，不要翻譯）
- type：System / Software / Device / Website / Account / Department / Role / Process / Form / Setting / Error / Other
- description：依本片段內容，用一到兩句話說明這個實體

【關係】實體之間的關聯
- source、target：必須是上面實體清單中的 name
- relation：簡短動詞片語（例如：需要、屬於、設定於、導致、申請方式、負責）
- description：一句話說明這個關係

【規則】
- 只抽取片段中明確寫到的內容，不要推論
- 片段沒有實質內容時回傳空清單

【文件】{doc_name}
【章節】{section}
【片段】
{text}
"""

DOC_VISION_PROMPT = """你正在把企業內部教育訓練文件的圖片轉成文字，讓知識庫可以檢索。
圖片多半是系統操作畫面截圖、流程圖或表格。

請**只轉錄畫面上真的看得見的內容**，用繁體中文條列：
- 系統名稱、功能路徑、交易代碼（例如「SAP > 銷售 > VA01」）
- 欄位名稱與其中填入的值、按鈕與選單文字
- 表格的欄位與資料列
- 流程圖的節點與箭頭方向（寫成「A → B」）
- 畫面上的說明文字、提示、紅框標註的重點

規則：
- 看不清楚就寫「（看不清楚）」，**絕對不要猜測或自行補上沒看到的欄位名稱、代碼**。
- **不要轉錄個人資料**：人名、登入帳號、電子郵件、電話、手機、身分證號、地址一律略過，
  需要提到時寫「（使用者）」代替。截圖裡的測試帳號也一樣不要寫出來。
  這包含畫面右上角的使用者名稱、以及「○○○ 您好」這類含名字的問候語——
  問候語請寫成「（使用者）您好…」，不要保留原本的名字。
- 不要描述版面、顏色、截圖美醜，也不要寫「這張圖顯示了…」這種開場白。
- 如果圖片只是裝飾、logo 或沒有資訊量，只回覆「（無內容）」。
- 直接輸出條列內容，不要加標題或結語。

這一頁的標題是：{title}"""


ENTITY_SUMMARY_PROMPT = """以下是同一個實體「{name}」在不同文件中的多段描述，請整合成一段不超過 300 字的繁體中文說明，保留所有具體事實（系統名稱、步驟、網址、條件），刪除重複內容：

{descriptions}
"""
TRIPLE_EXTRACTION_PROMPT= """
      你是一個企業級 IT HelpDesk 智能助理，負責將使用者的問題轉換成可搜尋的結構化查詢。

      === 任務分為兩階段 ===
      (1) Query Expansion（擴充問題）
      (2) Query Triple Extraction（抽取三元組）

      --------------------------------
      【步驟 1：Query Expansion】
      --------------------------------
      請將使用者原始問題改寫成：
      - 完整句子
      - 清楚的主詞、行為、對象
      - 移除口語化、模糊代稱
      - 保留原本的意圖
      - 如果使用者問題片段、不完整，請自動補完整語意

      避免添加使用者沒有提到的新資訊。

      格式：
      ExpandedQuery: <改寫後的完整句子>

      --------------------------------
      【步驟 2：Query Triple Extraction】
      --------------------------------
      根據 ExpandedQuery，抽取其語意對應的三元組：

      三元組格式：
      (entity1, relation, entity2)

      原則：
      - entity1：問題的主體（設備、系統、人員、文件）
      - relation：使用自然語言描述（例如：無法、需要、設定、啟用、登入）
      - entity2：行為的目標（如：登入、啟用、憑證、帳號、VPN、WIFI）

      若 ExpandedQuery 有多個語意，請抽取多筆三元組。

      格式請使用 JSON：

      {
        "triples": [
          { "entity1": "...", "relation": "...", "entity2": "..." }
        ]
      }

      --------------------------------
      【注意】
      - 不要加入推論或想像的內容
      - 不要回答問題，只做擴充與三元組抽取
      - 若無法形成三元組，請將 entity1 設為 "UserIssue"，relation 設為 "related_to"，entity2 設為 ExpandedQuery 的核心名詞

      --------------------------------
      【使用者問題】
      *user_question*

      --------------------------------
"""

LINE_FLEX_BUBBLE_TEXT = """
{
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://www.royalbase.com/images/LINE/human2.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://line.me/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "真人客服需求",
                "wrap": true,
                "scaling": true,
                "size": "lg",
                "color": "#4D487A",
                "weight": "bold"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "請接下來簡述你的問題，例如操作前因後果、錯誤訊息、操作步驟或畫面截圖等，不然就算我想幫，也只能猜測喔😭～\\n\\n資訊服務提示：\\n若未使用需求單提出申請，因資訊部工作量較大，將優先處理已正式派工之案件，僅於有餘力或完成既有工作後，才會處理一般申請。\\n\\n如遇緊急狀況，請直接以電話或其他通訊方式聯絡資訊部，並清楚說明情況，資訊人員將依緊急程度進行處理。因資訊部人力有限，需支援多位同仁，建議提前提出需求，以利安排並提供即時協助。\\n\\nVui lòng mô tả chi tiết vấn đề của bạn, chẳng hạn như nguyên nhân, thông báo lỗi, các bước thao tác hoặc ảnh chụp màn hình,… Nếu không, dù tôi rất muốn giúp đỡ nhưng cũng chỉ có thể đoán mò thôi 😭~\\n\\nCác yêu cầu không qua phiếu sẽ được xử lý sau, khi bộ phận CNTT có thời gian rảnh. Trường hợp khẩn cấp, vui lòng gọi điện hoặc liên hệ trực tiếp để được hỗ trợ nhanh hơn. Do nhân lực CNTT hạn chế, bạn nên gửi yêu cầu sớm để được hỗ trợ kịp thời.",
                "wrap": true,
                "color": "#666666",
                "size": "sm",
                "flex": 4
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "我確定要找真人客服",
          "text": "我確定要找資訊部同仁,問題詳述如下："
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "還是聰明的AI助理好了",
          "text": "恢復AI"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0
  }
}
"""
