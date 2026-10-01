# -*- coding: utf-8 -*-
"""
本機測 LINE webhook 用：自己算 X-Line-Signature 再送出。
簽章驗證開著也能測，不需要開「驗證關閉」的後門。

    python tools/post_webhook.py "今日科技新聞"
    python tools/post_webhook.py "密碼怎麼重設" --user U1234 --no-reply-token
    python tools/post_webhook.py "測試" --url http://127.0.0.1:8098/webhook/line_dev

--no-reply-token 會讓回覆走 Push 路徑（用來驗 Push 備援）。
注意：Push 會真的發到 --user 指定的 LINE 帳號，請填自己的 userId。
"""

import os
import sys
import hmac
import time
import json
import base64
import hashlib
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import LINE_CHANNEL_SECRET


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text", help="要送的訊息文字")
    ap.add_argument("--url", default="http://127.0.0.1:8098/webhook/line_dev")
    ap.add_argument("--user", default="Utest0000000000000000000000000000", help="來源 userId")
    ap.add_argument("--no-reply-token", action="store_true", help="不帶 replyToken，強制走 Push")
    ap.add_argument("--bad-signature", action="store_true", help="故意送錯的簽章，應該被回 403")
    args = ap.parse_args()

    if not LINE_CHANNEL_SECRET:
        sys.exit("LINE_CHANNEL_SECRET 沒設定，無法算簽章")

    event = {
        "type": "message",
        "message": {"id": "0", "type": "text", "text": args.text},
        "timestamp": int(time.time() * 1000),
        "source": {"type": "user", "userId": args.user},
        "mode": "active",
    }
    if not args.no_reply_token:
        event["replyToken"] = "0" * 32

    # body 要用送出去的那一份原始位元組來算簽章，不能重新 dumps
    body = json.dumps({"destination": "test", "events": [event]}, ensure_ascii=False).encode("utf-8")
    digest = hmac.new(LINE_CHANNEL_SECRET.encode("utf-8"), body, hashlib.sha256).digest()
    sig = base64.b64encode(digest).decode("utf-8")
    if args.bad_signature:
        sig = base64.b64encode(b"x" * 32).decode("utf-8")

    res = requests.post(
        args.url,
        data=body,
        headers={"Content-Type": "application/json", "X-Line-Signature": sig},
        timeout=30,
    )
    print(f"HTTP {res.status_code}  {res.text[:200]}")
    if res.status_code == 403:
        print("（簽章被拒 — 若不是用 --bad-signature，請確認 .env 的 LINE_CHANNEL_SECRET 與伺服器一致）")


if __name__ == "__main__":
    main()
