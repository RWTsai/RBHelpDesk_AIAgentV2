# -*- coding: utf-8 -*-
"""
吸收 openai SDK 版本差異的小工具。

結構化輸出（傳 Pydantic 類別當 response_format）原本只在 beta 命名空間，
後來才升到正式的 client.chat.completions.parse。兩者簽名相同。

為什麼需要這層：測試區與正式區的 SDK 版本不一定同步，少了它舊版環境會丟
'Completions' object has no attribute 'parse'。而這個例外原本被 _verify 當成
「驗證器失敗，視為通過」吞掉，結果驗證器整個靜默停用、答案都沒經過查核，
從 log 上只看到 verdict=pass，非常難發現。
"""


def parse_structured(client, **kwargs):
    """呼叫結構化輸出，自動挑該 SDK 版本有的那個入口。"""
    fn = getattr(client.chat.completions, "parse", None)
    if fn is None:
        # 舊版 SDK（Responses API 已有、parse 還在 beta 的那段區間）
        fn = client.beta.chat.completions.parse
    return fn(**kwargs)


def has_structured_parse(client) -> bool:
    """啟動時自我檢查用。"""
    if hasattr(client.chat.completions, "parse"):
        return True
    try:
        return hasattr(client.beta.chat.completions, "parse")
    except Exception:
        return False
