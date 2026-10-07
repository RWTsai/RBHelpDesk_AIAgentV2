# -*- coding: utf-8 -*-
"""
用正確的簽章打 webhook，確認簽章驗證這一關本身是通的。

用途：前面有 IIS URL Rewrite 反向代理時，分辨「簽章驗證失敗」是 Python 這邊的
問題還是中間那一層改了東西。同一個請求打兩個位址比對即可：

    # 1) 直接打 Python 主機（繞過 IIS）
    python tools/test_webhook_signature.py http://localhost:8098/webhook/LINE_IT

    # 2) 走 IIS 對外網址
    python tools/test_webhook_signature.py https://對外網址/webhook/LINE_IT

  兩個都 200  → 簽章這一關沒問題，失敗的請求不是這條路徑來的
  1 通 2 不通 → IIS 那一層動了 body 或沒轉發 X-Line-Signature
  兩個都 403  → secret 不對（但這支用的就是 .env 裡的 secret，所以更可能是
                 Python 那邊讀到的 .env 和你看的不是同一份）

送的是 {"events":[]}，webhook 驗完簽章就直接回「no events」，不會觸發任何
查詢、不會回訊息給任何人。
"""
import sys
import os
import hmac
import base64
import hashlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import LINE_CHANNEL_SECRET

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)

url = sys.argv[1]
body = b'{"events":[]}'
sig = base64.b64encode(
    hmac.new(LINE_CHANNEL_SECRET.encode("utf-8"), body, hashlib.sha256).digest()
).decode("ascii")

print("目標      ：%s" % url)
print("secret指紋：%s" % hashlib.sha256(LINE_CHANNEL_SECRET.encode("utf-8")).hexdigest()[:8])
print("body      ：%d bytes" % len(body))
print("簽章      ：%s…" % sig[:12])
print()

try:
    r = requests.post(url, data=body, timeout=30, headers={
        "Content-Type": "application/json",
        "X-Line-Signature": sig,
    })
except Exception as e:
    print("連不上：%s" % e)
    sys.exit(1)

print("HTTP %s" % r.status_code)
print("回應  %s" % r.text[:300])
print()
if r.status_code == 200:
    print("簽章驗證通過。")
elif r.status_code == 403:
    print("簽章被拒。看 Python 主機的 console，新版會印出 body 長度與 Content-Length，")
    print("兩者不一致就是中間層動過 body。")
else:
    print("非預期的狀態碼，可能根本沒到 Flask（IIS 自己回的）。")
