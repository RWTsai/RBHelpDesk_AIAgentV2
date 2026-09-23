# google_node.py
"""
使用 SerpAPI 做 Google 搜尋的簡單工具。

說明：
- 需要 .env 的 SERPAPI_API_KEY（空值時 Agent 不會註冊 web_search 工具）
- google_search_items()：回傳結構化結果，給 Agent 工具 web_search 使用（To-Be 新增）
- google_search()：回傳摘要字串（保留舊介面）
"""

from typing import List
import requests

from config import SERPAPI_API_KEY, WEB_SEARCH_NUM
from utils.logger import log_info, log_error


def google_search_items(query: str, num_results: int = None) -> list:
    """
    回傳 [{title, link, snippet}]；失敗時 raise，讓呼叫端決定怎麼處理
    """
    if not SERPAPI_API_KEY:
        raise RuntimeError("系統尚未設定 SERPAPI_API_KEY")

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": num_results or WEB_SEARCH_NUM,
        "hl": "zh-tw",
    }

    log_info(f"[google_node] 搜尋關鍵字：{query}")
    resp = requests.get("https://serpapi.com/search", params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    items = []
    for item in data.get("organic_results", [])[: params["num"]]:
        items.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })
    return items


def google_search(query: str, num_results: int = None) -> str:
    """舊介面：回傳拼好的文字"""
    try:
        items = google_search_items(query, num_results)
    except Exception as e:
        log_error(f"[google_node] 呼叫 SerpAPI 失敗：{e}")
        return "呼叫 Google 搜尋服務時發生錯誤，請稍後再試。"

    if not items:
        return f"找不到與「{query}」相關的搜尋結果。"

    results: List[str] = []
    for i, item in enumerate(items, start=1):
        results.append(f"[{i}] {item['title']}\n{item['snippet']}\n{item['link']}")
    return "\n\n".join(results)
