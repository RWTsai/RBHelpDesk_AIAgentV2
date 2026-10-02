# agent_node.py
"""
Agent 文字處理節點（To-Be：取代 ai_text_node 的固定管線）
---------------------------------------------------
流程：
0. AGENT_MODE=off → 直接走舊的 ai_text_node.process_text（安全開關）
1. 快速路徑：問題直接 embedding → 查 QA 快取 → 分數 ≥ QA_FAST_PATH_MIN_SCORE → 一次呼叫模型作答
2. Agent 迴圈（OpenAI function calling）：
     規劃／行動 → 執行工具（同一輪多個工具並行）→ 判斷要不要繼續查 → 產生草稿
3. 驗證：OPENAI_MODEL_VERIFY 檢查草稿是否有證據支持
     pass → 回覆；needs_more → 帶著驗證意見再查一次；fail → 保守改寫＋提示真人客服
4. 附上參考來源、寫 IT_KB_AgentTrace

state 仍是普通 dict；對話記憶統一由 MemorySave 節點寫入。
"""

import re
import json
import time
import datetime
from typing import List, Literal
from concurrent.futures import ThreadPoolExecutor

from openai import OpenAI
from pydantic import BaseModel, Field

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL_CHAT,
    OPENAI_MODEL_FAST,
    OPENAI_MODEL_VERIFY,
    AGENT_REASONING_EFFORT,
    AGENT_MODE,
    AGENT_MAX_STEPS,
    AGENT_MAX_VERIFY_RETRY,
    AGENT_FAST_PATH,
    AGENT_NOTICE_SEC,
    AGENT_TIME_BUDGET_SEC,
    OPENAI_STORE_RESPONSES,
    QA_FAST_PATH_MIN_SCORE,
    QA_PREFETCH_MIN_SCORE,
    VERIFY_ENABLED,
    VERIFY_EVIDENCE_MAX_CHARS,
    SYSROLE_PROMPT,
    SYSTEM_BASE_PROMPT,
    KNOWLEDGE_BASE_PROMPT_CORE,
    AGENT_SYSTEM_PROMPT,
    FAST_PATH_PROMPT,
    VERIFY_PROMPT,
    CONSERVATIVE_PROMPT,
    get_mssql_conn,
)
from agents import tools as agent_tools
from agents import skill_loader
from database import doc_graph_client
from utils.text_cleaner import clean_basic
from utils.logger import log_info, log_error
from utils.openai_compat import parse_structured
from .utils_line import start_loading, push_messages

client = OpenAI(api_key=OPENAI_API_KEY)

# 驗證略過的情況：只用了這些工具（結果本身就是依據）
_SELF_EVIDENT_TOOLS = {"sql_query", "load_skill"}

# 進度訊息用：工具名稱 -> 講給使用者聽的說法（不要出現工具名或資料表名）
_TOOL_PHRASE = {
    "search_qa_kb": "翻 QA 知識庫",
    "search_documents": "翻手冊和簡報",
    "explore_entity": "追相關的項目",
    "web_search": "查網路上的資料",
    "sql_query": "查資料庫",
    "describe_table": "確認資料庫欄位",
    "load_skill": "調出處理規則",
    "read_reference": "查參考文件",
}

_SOURCES_RE = re.compile(r"^\s*SOURCES\s*[:：]\s*(.*)$", re.IGNORECASE | re.MULTILINE)


class VerifyResult(BaseModel):
    """驗證器的結構化輸出"""
    verdict: Literal["pass", "needs_more", "fail"] = Field(description="判定結果")
    unsupported_claims: List[str] = Field(default_factory=list, description="沒有證據支持的敘述")
    missing_info: str = Field(default="", description="還缺什麼資訊")
    feedback: str = Field(default="", description="給 Agent 的修正建議")


# =====================================================
# 主流程
# =====================================================
def process_text(state: dict) -> dict:
    if not AGENT_MODE:
        from . import ai_text_node
        return ai_text_node.process_text(state)

    t0 = time.time()
    user_text = (state.get("message_text") or "").strip()
    user_id = state.get("user_id")
    trace = {"steps": [], "verdict": None}

    if not user_text:
        state["reply_text"] = "我沒有收到文字訊息，可以再傳一次嗎？"
        return state

    # 向量快取還在載入（剛重啟）→ 立刻回覆，不要讓使用者等整個載入跑完。
    # 要擺在 loading 動畫之前，否則會先顯示「輸入中」再秒回，看起來很怪。
    if not doc_graph_client.is_ready():
        log_info("[AGENT] 向量快取尚未載入完成，先請使用者稍後再試")
        state["reply_text"] = ("系統剛啟動，正在載入知識庫（約需 1 分鐘），"
                              "請稍後再問一次。若急需協助，請輸入「真人客服」。")
        return state

    # 先送 loading 動畫，讓使用者知道正在處理
    start_loading(user_id)

    question = clean_basic(user_text)
    history = (state.get("memory") or {}).get("chat_history", [])[-10:]
    log_info(f"[AGENT] 開始處理：{question}")

    # 命中關鍵字的 skill 直接注入本文（快速路徑與 Agent 迴圈都用）
    kw_skills = skill_loader.match_keywords(question)
    skill_text = ""
    if kw_skills:
        skill_text = "\n\n".join(f"【Skill：{s['name']}】\n{s['body']}" for s in kw_skills)
        _step(trace, "skill_keyword", 0, skills=[s["name"] for s in kw_skills])

    reply, sources = None, []
    qa_hits = []               # 快速路徑查到的 QA 命中；分數不夠時轉給 Agent 迴圈當證據
    try:
        # ---------- 1) 快速路徑 ----------
        if AGENT_FAST_PATH:
            reply, qa_hits = _fast_path(question, history, skill_text, trace)

        # ---------- 2) Agent 迴圈 + 3) 驗證 ----------
        if reply is None:
            notify = _progress_notifier(user_id, t0, trace)
            reply, sources = _agent_loop(question, history, kw_skills, skill_text, trace, qa_hits, notify, t0)

    except Exception as e:
        log_error(f"[AGENT] 執行失敗：{e}")
        trace["verdict"] = "error"
        _step(trace, "error", 0, message=str(e))
        reply = "AI 回覆時發生問題，請稍後再試。若急需協助，請輸入「真人客服」。"

    # ---------- 4) 參考來源 ----------
    # 空字串在 reply 節點代表「人工客服模式，AI 靜默」，會整則不送。所以這裡
    # 絕對不能讓其他原因產生的空回覆漏過去，否則使用者什麼都收不到也沒人知道。
    if not (reply or "").strip():
        log_error("[AGENT] 產出空回覆，改送提示訊息（verdict=%s）" % trace.get("verdict"))
        _step(trace, "empty_reply", 0, verdict=trace.get("verdict"))
        trace["verdict"] = "empty"
        reply = ("這題我沒有組出完整的答案，可以換個說法或把條件說得更具體一點嗎？\n"
                 "若需要資訊部同事協助，請輸入「真人客服」。")
        sources = []

    if sources:
        reply = reply.rstrip() + "\n\n參考來源：\n" + "\n".join(sources)

    state["reply_text"] = reply
    state["_trace"] = trace          # 給 ask.py -v 看每一步用了什麼工具；LINE 流程用不到
    latency_ms = int((time.time() - t0) * 1000)
    log_info(f"[AGENT] 完成，verdict={trace['verdict']}，耗時 {latency_ms} ms")
    _write_trace(user_id, question, trace, reply, latency_ms)
    return state


def _progress_notifier(user_id, t0, trace):
    """
    回傳一個 notify(tool_names) 函式：處理太久時推播一則進度訊息。

    為什麼需要：問題越複雜、工具輪數越多就越慢（實測可到 30 秒以上），
    使用者看不到任何回應會以為當掉而重複發問。loading 動畫最多只撐 60 秒
    而且什麼都沒說，所以超過門檻就直接告訴他「我讀懂了，正在查什麼」。
    一題只送一次；CLI（沒有 user_id）與關閉時都直接略過。
    """
    sent = []

    def notify(tool_names):
        if sent or not AGENT_NOTICE_SEC or not user_id:
            return
        if time.time() - t0 < AGENT_NOTICE_SEC:
            return
        sent.append(True)
        # 用這一輪實際叫到的工具組句子，不另外呼叫 LLM（那會讓它更慢）
        acts = [_TOOL_PHRASE[n] for n in dict.fromkeys(tool_names) if n in _TOOL_PHRASE]
        what = "、".join(acts) if acts else "多查幾個地方"
        text = f"收到，你的問題我需要{what}，還要一點時間，請稍等一下不用重複發問。"
        push_messages(user_id, [{"type": "text", "text": text}])
        start_loading(user_id)      # 動畫續命，避免「輸入中」先消失
        _step(trace, "progress_notice", 0, tools=acts)

    return notify


# =====================================================
# 1) 快速路徑
# =====================================================
def _fast_path(question, history, skill_text, trace):
    t = time.time()
    vec = doc_graph_client.embed_texts([question])[0]
    hits = doc_graph_client.search_qa_by_vector(vec, min_score=0.0)
    top = hits[0]["similarity"] if hits else 0.0
    _step(trace, "fast_path_check", t, top_score=round(top, 4), threshold=QA_FAST_PATH_MIN_SCORE)
    if top < QA_FAST_PATH_MIN_SCORE:
        # 分數不夠走不了快速路徑，但這批命中已經查好了，交給 Agent 迴圈當預先證據，不要重查
        return None, hits

    # 只取夠接近的命中（與 top1 差距 0.1 以內），依 ChunkText 去重
    chunks, triples = [], []
    for h in hits:
        if h["similarity"] < top - 0.1:
            continue
        if h.get("Entity1") and h.get("Relation") and h.get("Entity2"):
            triples.append(f"{h['Entity1']} {h['Relation']} {h['Entity2']}")
        c = (h.get("ChunkText") or "").strip()
        if c and c not in chunks:
            chunks.append(c)

    kb_text = "以下是系統中找到的相關事實（請依照這些事實回答）：\n\n"
    if triples:
        kb_text += "[事實三元組]\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(dict.fromkeys(triples), 1)) + "\n\n"
    kb_text += "[原始知識來源]\n" + "\n".join(f"- {c}" for c in chunks)

    prompt = FAST_PATH_PROMPT.format(
        system_base=SYSTEM_BASE_PROMPT,
        question=question,
        history=_history_text(history),
        kb_text=kb_text,
        skill_text=skill_text,
        rules=KNOWLEDGE_BASE_PROMPT_CORE,
    )
    t = time.time()
    res = _chat(
        model=OPENAI_MODEL_FAST,
        messages=[{"role": "system", "content": SYSROLE_PROMPT}, {"role": "user", "content": prompt}],
    )
    _step(trace, "fast_path_answer", t, model=OPENAI_MODEL_FAST)
    answer = res.choices[0].message.content or ""
    if not answer.strip():
        # 模型沒給內容。回 None 讓它落到 Agent 迴圈，不要把空字串當成有效答案
        # ——reply 節點看到空字串會整則不送，使用者會以為機器人死了。
        log_error("[AGENT] 快速路徑回了空內容，改走 Agent 迴圈")
        return None, hits
    trace["verdict"] = "fast_path"
    return answer, hits


# =====================================================
# 2) Agent 迴圈
# =====================================================
def _agent_loop(question, history, kw_skills, skill_text, trace, qa_hits=(), notify=None, t0=None):
    registry = agent_tools.build_base_tools()
    loaded_skills = {s["name"] for s in kw_skills}
    # 已注入的 skill 若帶工具，直接加進可用工具
    for name in loaded_skills:
        registry.update(skill_loader.skill_tools(name))

    system = SYSROLE_PROMPT + AGENT_SYSTEM_PROMPT.format(
        skill_catalog=skill_loader.skill_catalog_text(),
        today=datetime.date.today().isoformat(),
    ) + "\n【回覆規則】\n" + KNOWLEDGE_BASE_PROMPT_CORE
    if skill_text:
        system += "\n\n【已載入的 Skill（依此處理）】\n" + skill_text

    # Responses API 的系統提示走 instructions 參數，不放在 input 裡
    conv = []
    for h in history:
        if h.get("user"):
            conv.append({"role": "user", "content": str(h["user"])})
        if h.get("assistant"):
            conv.append({"role": "assistant", "content": str(h["assistant"])})
    conv.append({"role": "user", "content": question})

    evidence = {}      # source_id → item（去重後的全部證據）
    tools_used = []    # 依序記錄用過的工具名稱

    # 快速路徑已經查過 QA 知識庫（分數不夠才會走到這裡），把命中結果直接當成證據帶進來：
    # 向量搜尋已經跑完是免費的，省掉一次 search_qa_kb 往返，也避免模型完全不查就憑自身知識作答
    prefetch = agent_tools.qa_items(qa_hits, min_score=QA_PREFETCH_MIN_SCORE)
    if prefetch:
        for it in prefetch:
            evidence[it["source_id"]] = it
        tools_used.append("search_qa_kb")      # 讓驗證器照樣檢查這批證據
        conv.append({"role": "user", "content": (
            "[系統訊息，使用者看不到] 已經先幫你查過 QA 知識庫（等同 search_qa_kb），結果如下，"
            "不要重複呼叫 search_qa_kb：\n"
            + agent_tools.result_to_text({"ok": True, "items": prefetch})
            + "\n若這些內容不足以完整回答使用者的問題，請依工具使用規則第 2 條呼叫 search_documents。"
        )})
        _step(trace, "qa_prefetch", 0, items=len(prefetch), top_score=prefetch[0]["score"])

    steps = 0
    verify_retry = 0
    draft = None
    forced_notice = False      # 強制作答的說明只插一次

    def over_budget():
        """時間是否用完。要能在迴圈各處重新評估，不能只在頂端算一次。"""
        return bool(AGENT_TIME_BUDGET_SEC and t0 and (time.time() - t0) > AGENT_TIME_BUDGET_SEC)

    while True:
        # ---------- 規劃／行動 ----------
        # 步數或時間任一用完，就禁止再呼叫工具、直接用手上的證據作答。
        # 只看步數不夠——每一輪的耗時差很多，複雜問題會整題超出 LINE 的回覆視窗。
        timed_out = over_budget()
        if timed_out and steps < AGENT_MAX_STEPS and not forced_notice:
            _step(trace, "time_budget", 0, elapsed=round(time.time() - t0, 1),
                  budget=AGENT_TIME_BUDGET_SEC, round=steps + 1)
        force_answer = steps >= AGENT_MAX_STEPS or timed_out
        if force_answer and not forced_notice:
            # 光把 tool_choice 設成 none，模型不知道發生什麼事；實測它會自己掰
            # 「無法連到公司系統」再給一篇通用教學。必須明講原因與要求。
            forced_notice = True
            conv.append({"role": "user", "content": (
                "[系統訊息，使用者看不到] 查詢次數或時間已用完，這一輪不要再呼叫任何工具，"
                "直接用上面已經查到的資料作答。要求："
                "(1) 已經查到的部分照實給出數字與結論；"
                "(2) 還沒查到的部分明確說「這部分還沒查到」，並說明需要什麼條件才能查；"
                "(3) 不可以說你無法連線、沒有資料庫權限或查不到系統——你有這些權限，"
                "只是這次時間不夠；"
                "(4) 若需要使用者補條件，直接問他。"
            )})
        t = time.time()
        kwargs = {"model": OPENAI_MODEL_CHAT, "instructions": system, "input": conv}
        if registry:
            kwargs["tools"] = agent_tools.to_responses_tools(registry)
            kwargs["tool_choice"] = "none" if force_answer else "auto"
        res = _respond(**kwargs)
        calls = [o for o in res.output if o.type == "function_call"]
        _step(trace, "llm", t, round=steps + 1, tool_calls=[c.name for c in calls])

        if calls and not force_answer:
            if notify:
                notify([c.name for c in calls])
            # 把這一輪模型自己產生的 output 原封不動接回去（含 reasoning 項目——
            # 少了它們，下一輪的 function_call_output 會對不上它的 function_call）
            conv += [o.to_dict() for o in res.output]
            for c, out_text in _run_tool_calls(calls, registry, loaded_skills, evidence, tools_used, trace):
                conv.append({"type": "function_call_output", "call_id": c.call_id, "output": out_text})
            steps += 1
            continue

        draft = res.output_text or ""

        # ---------- 3) 驗證 ----------
        if not VERIFY_ENABLED or not tools_used or set(tools_used) <= _SELF_EVIDENT_TOOLS:
            # 沒用工具（問安、閒聊、範圍外）或只用 SQL（結果本身即依據）→ 略過驗證
            trace["verdict"] = "pass_skip"
            break

        t = time.time()
        v = _verify(question, evidence, draft)
        if v is None:
            # 驗證器壞了（SDK 不相容、API 掛掉…）。不擋回覆，但紀錄要寫實話。
            _step(trace, "verify", t, verdict="error")
            trace["verdict"] = "verify_error"
            break
        _step(trace, "verify", t, verdict=v.verdict, unsupported=v.unsupported_claims, missing=v.missing_info)
        trace["verdict"] = v.verdict

        if v.verdict == "pass":
            break

        if v.verdict == "needs_more" and verify_retry < AGENT_MAX_VERIFY_RETRY and not over_budget():
            verify_retry += 1
            steps = min(steps, AGENT_MAX_STEPS - 1)  # 至少再給一輪工具呼叫
            conv += [o.to_dict() for o in res.output]
            conv.append({"role": "user", "content": (
                f"[系統品質檢查回饋，使用者看不到] 草稿還缺少：{v.missing_info or '關鍵資訊'}。"
                f"建議：{v.feedback}。請再查詢補足後重新回答；若確實查不到，請明確說明查不到的部分。"
            )})
            continue

        if over_budget() and v.verdict != "fail" and draft.strip():
            # 時間已用完，草稿也不是「有幻覺」等級的問題 → 直接用草稿，
            # 省下保守改寫那一次 LLM 呼叫（約 5～10 秒），讓訊息趕得上 LINE 的回覆視窗。
            _step(trace, "skip_rewrite", 0, reason="time_budget")
            trace["verdict"] = "needs_more"
            break

        # fail，或 needs_more 已用完補查次數 → 保守改寫
        draft = _conservative_rewrite(system, conv, draft, v, trace)
        trace["verdict"] = "fail" if v.verdict == "fail" else "needs_more"
        break

    answer, cited = _split_sources(draft)
    return answer, _format_sources(cited, evidence)


def _run_tool_calls(tool_calls, registry, loaded_skills, evidence, tools_used, trace):
    """
    同一輪的多個工具並行執行；load_skill 在主執行緒處理（會修改 registry）。
    tool_calls 是 Responses API 的 function_call 項目，欄位為 call_id／name／arguments
    （Chat Completions 那套是 id／function.name／function.arguments）。
    """
    results = {}
    normal = []
    for tc in tool_calls:
        name = tc.name
        try:
            args = json.loads(tc.arguments or "{}")
        except Exception:
            args = {}
        if name == "load_skill":
            t = time.time()
            results[tc.call_id] = _load_skill(args.get("name", ""), registry, loaded_skills)
            tools_used.append(name)
            _step(trace, "tool", t, tool=name, args=args, ok=results[tc.call_id].get("ok"))
        else:
            normal.append((tc, name, args))

    def _one(item):
        tc, name, args = item
        t = time.time()
        res = agent_tools.run_tool(name, args, registry)
        detail = {"tool": name, "args": args, "ok": res.get("ok"), "items": len(res.get("items", []))}
        if name == "sql_query":  # SQL 一律完整記錄（含被拒絕的）供稽核
            detail["sql_executed"] = res.get("sql")
            detail["rejected"] = res.get("rejected", False)
            detail["note"] = res.get("note")
        return tc, name, res, detail, t

    if normal:
        with ThreadPoolExecutor(max_workers=min(4, len(normal))) as pool:
            for tc, name, res, detail, t in pool.map(_one, normal):
                results[tc.call_id] = res
                tools_used.append(name)
                _step(trace, "tool", t, **detail)
                for it in res.get("items", []):
                    if it.get("source_id"):
                        evidence[it["source_id"]] = it

    # 依原本順序回傳
    return [(tc, agent_tools.result_to_text(results[tc.call_id])) for tc in tool_calls]


def _load_skill(name, registry, loaded_skills):
    s = skill_loader.get_skill(name)
    if not s:
        return {"ok": False, "note": f"沒有這個 Skill：{name}。可用：{list(skill_loader.get_skills().keys())}"}
    new_tools = skill_loader.skill_tools(name)
    registry.update(new_tools)
    loaded_skills.add(name)
    out = {"ok": True, "skill": name, "instructions": s["body"], "new_tools": list(new_tools.keys())}
    refs = skill_loader.skill_references(name)
    if refs:
        out["references"] = [rel for rel, _ in refs]
        out["note"] = f"這個 Skill 附有參考文件，需要細節時用 read_reference(skill='{name}', file=…, keyword=…) 查"
    return out


# =====================================================
# 3) 驗證
# =====================================================
def _verify(question, evidence, draft) -> VerifyResult:
    ev_lines = []
    for sid, it in evidence.items():
        ev_lines.append(f"[{sid}] {it.get('title', '')}\n{it.get('text', '')}")
    ev_text = "\n\n".join(ev_lines)[:VERIFY_EVIDENCE_MAX_CHARS] or "（沒有取得任何證據）"
    answer, _ = _split_sources(draft)

    try:
        res = parse_structured(
            client,
            model=OPENAI_MODEL_VERIFY,
            messages=[{"role": "user", "content": VERIFY_PROMPT.format(question=question, evidence=ev_text, draft=answer)}],
            response_format=VerifyResult,
        )
        parsed = res.choices[0].message.parsed
        if parsed:
            return parsed
        log_error("[AGENT] 驗證器沒有回傳結構化結果")
    except Exception as e:
        log_error(f"[AGENT] 驗證器失敗：{e}")
    # 驗證器自己壞掉時不擋使用者的回覆，但**不可以謊報成驗證通過**——
    # 回 None 讓呼叫端把 verdict 記成 verify_error，否則稽核紀錄會顯示
    # 「已驗證通過」，而其實一次都沒驗到。
    return None


def _conservative_rewrite(system, conv, draft, v, trace):
    t = time.time()
    try:
        res = _respond(
            model=OPENAI_MODEL_CHAT,
            instructions=system,
            input=conv + [
                {"role": "assistant", "content": draft},
                {"role": "user", "content": CONSERVATIVE_PROMPT.format(
                    unsupported="；".join(v.unsupported_claims) or "（無）",
                    missing=v.missing_info or "（無）",
                )},
            ],
        )
        out = res.output_text or ""
        _step(trace, "conservative_rewrite", t)
        return out
    except Exception as e:
        log_error(f"[AGENT] 保守改寫失敗：{e}")
        return ("目前知識庫查無足夠資訊可以確認這個問題的答案。\n"
                "若需要資訊部同事協助，請輸入「真人客服」。\nSOURCES: 無")


# =====================================================
# 小工具
# =====================================================
# 每個（API, 模型, 有沒有帶工具）組合該怎麼給推理強度，試成功一次就記起來。
# 不記的話每一次呼叫都要先失敗一輪，白白多等一趟 HTTP。
_REASONING_MODE = {}

# 三種給法，依序退讓：
#   effort = 照 AGENT_REASONING_EFFORT 帶
#   omit   = 完全不帶（gpt-4o／gpt-4o-mini 這類不認識這個參數的模型）
#   none   = 明確帶 "none"。**省略不等於 none** —— 省略時模型會沿用自己的預設推理強度，
#            所以有些模型省略還是會被拒，要明確給 none 才行；但也有模型（gpt-6-astra）
#            反過來不接受 none，因此放在最後一個才試
_REASONING_ORDER = {
    "effort": ("effort", "omit", "none"),
    "omit": ("omit", "none"),
    "none": ("none",),
}


def _call_model(create, api, effort_param, **kwargs):
    """
    呼叫模型，並吸收各家模型對推理強度參數的差異。

    create       = client.chat.completions.create 或 client.responses.create
    api          = "chat" / "responses"，只用來分開快取
    effort_param = 把強度值包成該 API 的參數形狀：
                   Chat Completions → {"reasoning_effort": "low"}
                   Responses        → {"reasoning": {"effort": "low"}}
    """
    model = kwargs.get("model")
    key = (api, model, bool(kwargs.get("tools")))   # 限制常常只在「帶工具」時才出現
    start = _REASONING_MODE.get(key, "effort" if AGENT_REASONING_EFFORT else "omit")

    last, errors = None, []
    for mode in _REASONING_ORDER[start]:
        extra = {}
        if mode == "effort":
            extra = effort_param(AGENT_REASONING_EFFORT)
        elif mode == "none":
            extra = effort_param("none")
        try:
            res = create(**kwargs, **extra)
        except Exception as e:
            last = e
            errors.append(str(e))
            if "reasoning" not in str(e).lower():
                raise                              # 跟 reasoning 無關的錯誤不要吞掉
            continue
        if _REASONING_MODE.get(key) != mode:
            _REASONING_MODE[key] = mode
            log_info(f"[AGENT] {api}／{model}{'（含工具）' if key[2] else ''} 的推理強度用法：{mode}")
        return res

    # 每種寫法都被拒。帶工具時最常見的原因是這個模型在 Chat Completions 不支援
    # function tools（Astra／Sol 的 tool calling 只支援 Responses API）。
    if api == "chat" and key[2] and any("/v1/responses" in m for m in errors):
        raise RuntimeError(
            f"模型 {model} 在 Chat Completions 不支援 function tools。"
            f"Agent 迴圈已改走 Responses API，若仍看到這個錯誤表示有程式走了舊路徑。原始錯誤：{last}"
        ) from last
    raise last


def _respond(**kwargs):
    """Responses API。Agent 迴圈用這支——新模型的 tool calling 只支援這個 API。"""
    kwargs.setdefault("store", OPENAI_STORE_RESPONSES)
    return _call_model(
        client.responses.create, "responses",
        lambda v: {"reasoning": {"effort": v}},
        **kwargs,
    )


def _chat(**kwargs):
    """Chat Completions。快速路徑與保守改寫用這支（都不帶工具）。"""
    return _call_model(
        client.chat.completions.create, "chat",
        lambda v: {"reasoning_effort": v},
        **kwargs,
    )


def _split_sources(text):
    """拆出最後的 SOURCES 行 → (答案, [source_id])"""
    text = text or ""
    matches = list(_SOURCES_RE.finditer(text))
    if not matches:
        return text.strip(), []
    m = matches[-1]
    ids = [x.strip().strip("[]") for x in re.split(r"[,，、\s]+", m.group(1)) if x.strip()]
    ids = [x for x in ids if x and x != "無"]
    answer = (text[:m.start()] + text[m.end():]).strip()
    return answer, ids


def _format_sources(cited, evidence, limit=5):
    """只列文件與網路來源（QA／SQL 不列），附連結"""
    out, seen = [], set()
    for sid in cited:
        it = evidence.get(sid)
        if not it or it.get("source_type") not in ("document", "web"):
            continue
        key = it.get("url") or it.get("title")
        if key in seen:
            continue
        seen.add(key)
        prefix = "🌐 " if it["source_type"] == "web" else "📄 "
        line = prefix + (it.get("title") or sid)
        if it.get("url"):
            line += f"\n{it['url']}"
        out.append(line)
        if len(out) >= limit:
            break
    return out


def _history_text(history):
    return "".join(f"User：{h.get('user')}\nAssistant：{h.get('assistant')}\n" for h in history)


def _step(trace, kind, t_start, **detail):
    """記錄一個步驟；t_start=0 表示不計時"""
    item = {"type": kind}
    if t_start:
        item["ms"] = int((time.time() - t_start) * 1000)
    item.update(detail)
    trace["steps"].append(item)


def _write_trace(user_id, question, trace, answer, latency_ms):
    """寫 IT_KB_AgentTrace；表不存在或失敗都不影響回覆"""
    try:
        with get_mssql_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO IT_KB_AgentTrace (UserID, Question, StepsJson, Verdict, Answer, LatencyMs) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, question, json.dumps(trace["steps"], ensure_ascii=False, default=str),
                 trace.get("verdict"), answer, latency_ms),
            )
            conn.commit()
    except Exception as e:
        log_error(f"[AGENT] 寫入 AgentTrace 失敗（不影響回覆）：{e}")
