# news_node.py
"""
簡單版「今日科技新聞」查詢工具。

目前先實作一個非常直白的版本：
- 直接抓固定幾個網站（例如 ithome, AIMagazine）
- 用 requests + BeautifulSoup 把標題抓出來
- 回傳整理好的文字，給 AI 當 context 或直接回覆使用者

注意：這只是範例，實務上你可以再做更多錯誤處理與過濾。
"""

from typing import List
import requests
from bs4 import BeautifulSoup
from utils.logger import log_info, log_error


def fetch_ithome_news(limit: int = 5) -> List[str]:
    """抓取 iThome 新聞"""
    url = "https://www.ithome.com.tw/news"
    log_info(f"[news_node] 抓取 ithome 最新新聞：{url}")
    
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 選擇器：找到所有 .channel-item
        items = soup.select("div.channel-item")[:limit]
        
        log_info(f"[DEBUG] 找到 {len(items)} 個新聞項目")

        results: List[str] = []
        for item in items:
            # 標題在 p.title > a
            title_el = item.select_one("p.title a")
            if not title_el:
                continue
                
            title = title_el.get_text(strip=True)
            href = title_el.get("href") or ""
            
            # 處理相對路徑
            if href.startswith("/"):
                link = f"https://www.ithome.com.tw{href}"
            elif not href.startswith("http"):
                link = f"https://www.ithome.com.tw/{href}"
            else:
                link = href
            
            # 取得摘要
            summary_el = item.select_one("div.summary")
            summary = summary_el.get_text(strip=True) if summary_el else ""
            
            # 組合結果
            if summary:
                results.append(f"{title}\n{summary}\n{link}")
            else:
                results.append(f"{title} - {link}")
            
        log_info(f"[news_node] ithome 成功抓取 {len(results)} 筆新聞")
        return results
        
    except Exception as e:
        log_error(f"[news_node] fetch_ithome_news 錯誤: {e}")
        return []


def fetch_ai_magazine_news(limit: int = 5) -> List[str]:
    """抓取 AI Magazine 文章"""
    url = "https://aimagazine.com/articles"
    log_info(f"[news_node] 抓取 AI Magazine 最新文章：{url}")
    
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # ✅ 正確的選擇器：找到文章卡片
        items = soup.select("div.Card_Card__1TVz0")[:limit]
        
        log_info(f"[DEBUG] 找到 {len(items)} 個文章項目")

        results: List[str] = []
        for item in items:
            # 標題在 h3 > a
            title_el = item.select_one("h3 a")
            if not title_el:
                continue
                
            title = title_el.get_text(strip=True)
            href = title_el.get("href") or ""
            
            # 處理相對路徑
            if href.startswith("/"):
                link = f"https://aimagazine.com{href}"
            elif not href.startswith("http"):
                link = f"https://aimagazine.com/{href}"
            else:
                link = href
            
            # 取得摘要（可選）
            summary_el = item.select_one("div.Card_CardDescription__24Xbo p")
            summary = summary_el.get_text(strip=True) if summary_el else ""
            
            # 組合結果
            if summary:
                results.append(f"{title}\n{summary}\n{link}")
            else:
                results.append(f"{title} - {link}")
            
        log_info(f"[news_node] AI Magazine 成功抓取 {len(results)} 篇文章")
        return results
        
    except Exception as e:
        log_error(f"[news_node] fetch_ai_magazine_news 錯誤: {e}")
        return []

def process_news(state: dict) -> dict:
    """
    LangGraph node 函數：查詢科技新聞並更新 state
    
    Args:
        state: LangGraph 狀態字典
        
    Returns:
        更新後的 state，包含 reply_text
    """
    log_info("[NEWS_NODE] 開始查詢科技新聞")
    
    lines: List[str] = []
    
    try:
        ithome_list = fetch_ithome_news()
        if ithome_list:
            lines.append("【iThome 最新科技新聞】")
            lines.extend(f"- {x}" for x in ithome_list)
    except Exception as e:
        log_error(f"抓取 ithome 失敗：{e}")

    try:
        ai_list = fetch_ai_magazine_news()
        if ai_list:
            lines.append("\n【AI Magazine 最新文章】")
            lines.extend(f"- {x}" for x in ai_list)
    except Exception as e:
        log_error(f"抓取 AI Magazine 失敗：{e}")

    if not lines:
        reply_text = "目前無法取得最新科技新聞，請稍後再試。"
    else:
        reply_text = "\n".join(lines)

    log_info(f"[NEWS_NODE] 新聞查詢完成，共 {len(lines)} 筆")
    
    return {
        **state,
        "reply_text": reply_text
    }