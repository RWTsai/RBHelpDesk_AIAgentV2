# logger.py
"""
簡易版專案 Logger（不使用複雜 logging 設定）
- 自動在 /logs 建立每日 log 檔
- 提供 log_info(), log_error() 兩種方法
- 專案任何地方引入即可使用
- 優先考慮可讀性，而不是 logging 最佳實務
"""

import os
import re
import sys
from datetime import datetime

# 建立 logs 資料夾（若不存在）
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


# ---- 密鑰遮蔽 ----
# 外部 API 的錯誤訊息常把金鑰原樣回傳（例如 OpenAI 401），不遮就會留在 log 裡
_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_*\-]{6,}"), "sk-***"),                      # OpenAI 類金鑰
    (re.compile(r"(?i)\b(pwd|password)\s*=\s*[^;,\s\"']+"), r"\1=***"),     # 連線字串密碼
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._\-]{8,}"), "Bearer ***"),      # Authorization 標頭
]
# .env 裡的密鑰整串出現時直接換掉（例如 LINE token）
_SECRET_ENV = ("OPENAI_API_KEY", "LINE_CHANNEL_TOKEN", "LINE_CHANNEL_SECRET",
               "SERPAPI_API_KEY", "M365_CLIENT_SECRET", "GDRIVE_SA_JSON", "SUPABASE_KEY")
_secrets = []


def mask_secrets(message) -> str:
    """把訊息裡的金鑰、密碼換成 ***（log 與 print 都會先經過這裡）"""
    global _secrets
    if not _secrets:          # config 載入 .env 之前可能還拿不到，之後每次再試
        _secrets = [v for v in (os.getenv(k, "") for k in _SECRET_ENV) if len(v) >= 8]

    text = str(message)
    for s in _secrets:
        text = text.replace(s, "***")
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def _get_log_path():
    """依日期產生 log 檔案，例如 logs/2025-02-11.log"""
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"{today}.log")


def _write(level: str, message: str):
    """
    寫入 log 檔案，格式：
    [2025-02-11 12:33:12][INFO] 訊息內容
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"[{timestamp}][{level}] {message}\n"

    try:
        with open(_get_log_path(), "a", encoding="utf-8") as f:
            f.write(log_text)
    except Exception as e:
        print(f"[logger] 寫入日誌失敗：{e}")
        print("原始訊息：", log_text)


def _safe_print(text: str):
    """
    Windows 主控台常是 cp950，遇到 ⚠、emoji、日文等字元會丟 UnicodeEncodeError。
    log 不該讓主流程掛掉，所以印不出來的字元一律換成 ?（寫進檔案的仍是完整 UTF-8）。
    """
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        enc = getattr(sys.stdout, "encoding", None) or "utf-8"
        print(text.encode(enc, errors="replace").decode(enc, errors="replace"), flush=True)
    except Exception:
        pass


def log_info(message: str):
    """一般訊息用"""
    text = mask_secrets(message)
    _safe_print(f"[INFO] {text}")
    _write("INFO", text)


def log_error(message: str):
    """錯誤訊息用"""
    text = mask_secrets(message)
    _safe_print(f"[ERROR] {text}")
    _write("ERROR", text)
