# ask.py
"""
在命令列直接問 Agent，不經過 LINE（測試、調提示詞用）

    python ask.py "工號 A1234 的帳號被鎖了嗎"     # 問一題
    python ask.py                                  # 進入連續問答，輸入 q 離開
    python ask.py -v "..."                         # additionally 印出每一步用了什麼工具

不會送 LINE loading 動畫、不會回覆訊息（user_id 留空），
但會照常寫 IT_KB_AgentTrace，方便和正式流量一起看。
"""

import io
import sys
import time
import argparse

# Windows 主控台預設 cp950，印 emoji／⚠ 會炸，這裡統一轉 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0])

from agents.nodes import agent_node
from database import doc_graph_client


def ask(question: str, history: list, verbose: bool) -> str:
    state = {
        "message_text": question,
        "user_id": "",                       # 空的就不會呼叫 LINE API
        "memory": {"chat_history": history},
        "_t_start": time.time(),
    }
    t0 = time.time()
    out = agent_node.process_text(state)
    reply = out.get("reply_text") or "（沒有產生回覆）"

    print(f"\n{reply}\n")
    print(f"--- {time.time() - t0:.1f} 秒 ---")
    if verbose:
        for s in (out.get("_trace") or {}).get("steps", []):
            detail = {k: v for k, v in s.items() if k not in ("type", "ms")}
            print(f"  [{s.get('ms', 0):>6} ms] {s.get('type'):<14} {detail}")
    return reply


def main():
    p = argparse.ArgumentParser()
    p.add_argument("question", nargs="*", help="要問的問題；不給就進入連續問答")
    p.add_argument("-v", "--verbose", action="store_true", help="印出每一步用了哪些工具")
    args = p.parse_args()

    print("載入向量快取…")
    doc_graph_client.warmup()

    history = []
    if args.question:
        ask(" ".join(args.question), history, args.verbose)
        return

    print("輸入問題開始測試，q 或 Ctrl+C 離開；輸入 clear 清掉對話記憶\n")
    while True:
        try:
            q = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if q.lower() in ("q", "quit", "exit"):
            break
        if q.lower() == "clear":
            history.clear()
            print("（已清除對話記憶）")
            continue
        if not q:
            continue
        reply = ask(q, history, args.verbose)
        history.append({"user": q, "assistant": reply})
        history[:] = history[-10:]


if __name__ == "__main__":
    main()
