# text_cleaner.py
"""
文字清洗工具（簡易版）
- 專案中任何地方需要處理文字，都可以使用這裡的方法
- 只有函式，不做複雜結構
- 主要用於 embedding、AI 回覆、向量資料前處理
"""

import re
import html
from bs4 import BeautifulSoup


def clean_basic(text: str) -> str:
    """
    基本清理：
    - 去除 HTML
    - 去除多餘換行
    - 去除 tab、特殊空白
    - 去除奇怪控制字元
    """

    if not text:
        return ""

    # 1. 若有 HTML，移除所有標籤
    try:
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text("\n")   # ← 保留換行
    except:
        pass  # 就算失敗也不要報錯，保持魯棒性

    # 2. HTML escape（如 &nbsp; → 空白）
    text = html.unescape(text)

    # 3. 去除控制字元與過多空白
    text = re.sub(r"\s+", " ", text)

    # 45. 保留段落，但合併 3 行以上空行

    text = re.sub(r"\n{3,}", "\n\n", text)

    # 5. 去除前後空白
    return text.strip()


def split_for_embedding(text: str, chunk_size: int = 500):
    """
    把長文本切成 embedding-friendly 的段落。
    chunk_size：每段最大字數
    """

    text = clean_basic(text)

    chunks = []
    while len(text) > chunk_size:
        chunk = text[:chunk_size]
        chunks.append(chunk)
        text = text[chunk_size:]

    if text:
        chunks.append(text)

    return chunks


def clean_ai_reply(text: str) -> str:
    """
    清理 AI 回覆：
    - 去除開頭的技術性標記 (例如 'Sure, here is...' 類型)
    - 去除多餘換行
    """

    if not text:
        return ""

    text = clean_basic(text)

    # 刪除 AI 回覆常見的多餘「開場白」
    remove_prefix = [
        "當然，以下是",
        "Sure",
        "Here is",
        "Below is",
        "以下內容",
        "Here are",
    ]

    for prefix in remove_prefix:
        if text.startswith(prefix):
            text = text[len(prefix):]

    return text.strip()


def extract_keywords(text: str, max_len: int = 50) -> str:
    """
    從文字擷取關鍵詞（簡易版）
    - 不做 NLP，只做簡單字元過濾
    - 用於 log 或 metadata 產生
    """

    text = clean_basic(text)

    # 只保留中英數
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff ]", "", text)

    # 限制長度
    return text[:max_len].strip()
