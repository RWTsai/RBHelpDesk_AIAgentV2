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
from .utils_line import start_loading

client = OpenAI(api_key=OPENAI_API_KEY)

# 驗證略過的情況：只用了這些工具（結果本身就是依據）
_SELF_EVIDENT_TOOLS = {"sql_query", "load_skill"}

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
            reply, sources = _agent_loop(question, history, kw_skills, skill_text, trace, qa_hits)

    except Exception as e:
        log_error(f"[AGENT] 執行失敗：{e}")
        trace["verdict"] = "error"
        _step(trace, "error", 0, message=str(e))
        reply = "AI 回覆時發生問題，請稍後再試。若急需協助，請輸入「真人客服」。"

    # ---------- 4) 參考來源 ----------
    if sources:
        reply = reply.rstrip() + "\n\n參考來源：\n" + "\n".join(sources)

    state["reply_text"] = reply
    state["_trace"] = trace          # 給 ask.py -v 看每一步用了什麼工具；LINE 流程用不到
    latency_ms = int((time.time() - t0) * 1000)
    log_info(f"[AGENT] 完成，verdict={trace['verdict']}，耗時 {latency_ms} ms")
    _write_trace(user_id, question, trace, reply, latency_ms)
    return state


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
    trace["verdict"] = "fast_path"
    return res.choices[0].message.content or "", hits


# =====================================================
# 2) Agent 迴圈
# =====================================================
def _agent_loop(question, history, kw_skills, skill_text, trace, qa_hits=()):
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

    messages = [{"role": "system", "content": system}]
    for h in history:
        if h.get("user"):
            messages.append({"role": "user", "content": str(h["user"])})
        if h.get("assistant"):
            messages.append({"role": "assistant", "content": str(h["assistant"])})
    messages.append({"role": "user", "content": question})

    evidence = {}      # source_id → item（去重後的全部證據）
    tools_used = []    # 依序記錄用過的工具名稱

    # 快速路徑已經查過 QA 知識庫（分數不夠才會走到這裡），把命中結果直接當成證據帶進來：
    # 向量搜尋已經跑完是免費的，省掉一次 search_qa_kb 往返，也避免模型完全不查就憑自身知識作答
    prefetch = agent_tools.qa_items(qa_hits, min_score=QA_PREFETCH_MIN_SCORE)
    if prefetch:
        for it in prefetch:
            evidence[it["source_id"]] = it
        tools_used.append("search_qa_kb")      # 讓驗證器照樣檢查這批證據
        messages.append({"role": "user", "content": (
            "[系統訊息，使用者看不到] 已經先幫你查過 QA 知識庫（等同 search_qa_kb），結果如下，"
            "不要重複呼叫 search_qa_kb：\n"
            + agent_tools.result_to_text({"ok": True, "items": prefetch})
            + "\n若這些內容不足以完整回答使用者的問題，請依工具使用規則第 2 條呼叫 search_documents。"
        )})
        _step(trace, "qa_prefetch", 0, items=len(prefetch), top_score=prefetch[0]["score"])

    steps = 0
    verify_retry = 0
    draft = None

    while True:
        # ---------- 規劃／行動 ----------
        force_answer = steps >= AGENT_MAX_STEPS  # 步數用完：禁止再呼叫工具，直接作答
        t = time.time()
        kwargs = {"model": OPENAI_MODEL_CHAT, "messages": messages}
        if registry:
            kwargs["tools"] = agent_tools.to_openai_tools(registry)
            kwargs["tool_choice"] = "none" if force_answer else "auto"
        res = _chat(**kwargs)
        msg = res.choices[0].message
        _step(trace, "llm", t, round=steps + 1, tool_calls=[tc.function.name for tc in (msg.tool_calls or [])])

        if msg.tool_calls and not force_answer:
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in msg.tool_calls
                ],
            })
            for tc, out_text in _run_tool_calls(msg.tool_calls, registry, loaded_skills, evidence, tools_used, trace):
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": out_text})
            steps += 1
            continue

        draft = msg.content or ""

        # ---------- 3) 驗證 ----------
        if not VERIFY_ENABLED or not tools_used or set(tools_used) <= _SELF_EVIDENT_TOOLS:
            # 沒用工具（問安、閒聊、範圍外）或只用 SQL（結果本身即依據）→ 略過驗證
            trace["verdict"] = "pass_skip"
            break

        t = time.time()
        v = _verify(question, evidence, draft)
        _step(trace, "verify", t, verdict=v.verdict, unsupported=v.unsupported_claims, missing=v.missing_info)
        trace["verdict"] = v.verdict

        if v.verdict == "pass":
            break

        if v.verdict == "needs_more" and verify_retry < AGENT_MAX_VERIFY_RETRY:
            verify_retry += 1
            steps = min(steps, AGENT_MAX_STEPS - 1)  # 至少再給一輪工具呼叫
            messages.append({"role": "assistant", "content": draft})
            messages.append({"role": "user", "content": (
                f"[系統品質檢查回饋，使用者看不到] 草稿還缺少：{v.missing_info or '關鍵資訊'}。"
                f"建議：{v.feedback}。請再查詢補足後重新回答；若確實查不到，請明確說明查不到的部分。"
            )})
            continue

        # fail，或 needs_more 已用完補查次數 → 保守改寫
        draft = _conservative_rewrite(messages, draft, v, trace)
        trace["verdict"] = "fail" if v.verdict == "fail" else "needs_more"
        break

    answer, cited = _split_sources(draft)
    return answer, _format_sources(cited, evidence)


def _run_tool_calls(tool_calls, registry, loaded_skills, evidence, tools_used, trace):
    """同一輪的多個工具並行執行；load_skill 在主執行緒處理（會修改 registry）"""
    results = {}
    normal = []
    for tc in tool_calls:
        name = tc.function.name
        try:
            args = json.loads(tc.function.arguments or "{}")
        except Exception:
            args = {}
        if name == "load_skill":
            t = time.time()
            results[tc.id] = _load_skill(args.get("name", ""), registry, loaded_skills)
            tools_used.append(name)
            _step(trace, "tool", t, tool=name, args=args, ok=results[tc.id].get("ok"))
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
                results[tc.id] = res
                tools_used.append(name)
                _step(trace, "tool", t, **detail)
                for it in res.get("items", []):
                    if it.get("source_id"):
                        evidence[it["source_id"]] = it

    # 依原本順序回傳
    return [(tc, agent_tools.result_to_text(results[tc.id])) for tc in tool_calls]


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
        res = client.chat.completions.parse(
            model=OPENAI_MODEL_VERIFY,
            messages=[{"role": "user", "content": VERIFY_PROMPT.format(question=question, evidence=ev_text, draft=answer)}],
            response_format=VerifyResult,
        )
        parsed = res.choices[0].message.parsed
        if parsed:
            return parsed
    except Exception as e:
        log_error(f"[AGENT] 驗證器失敗，視為通過：{e}")
    # 驗證器本身出錯時不擋回覆
    return VerifyResult(verdict="pass")


def _conservative_rewrite(messages, draft, v, trace):
    t = time.time()
    try:
        res = _chat(
            model=OPENAI_MODEL_CHAT,
            messages=messages + [
                {"role": "assistant", "content": draft},
                {"role": "user", "content": CONSERVATIVE_PROMPT.format(
                    unsupported="；".join(v.unsupported_claims) or "（無）",
                    missing=v.missing_info or "（無）",
                )},
            ],
        )
        out = res.choices[0].message.content or ""
        _step(trace, "conservative_rewrite", t)
        return out
    except Exception as e:
        log_error(f"[AGENT] 保守改寫失敗：{e}")
        return ("目前知識庫查無足夠資訊可以確認這個問題的答案。\n"
                "若需要資訊部同事協助，請輸入「真人客服」。\nSOURCES: 無")


# =====================================================
# 小工具
# =====================================================
def _chat(**kwargs):
    """
    呼叫 Chat Completions；有設定 AGENT_REASONING_EFFORT 時帶上，
    若模型不支援此參數（例如 gpt-4o）自動拿掉重試。
    """
    if AGENT_REASONING_EFFORT:
        try:
            return client.chat.completions.create(reasoning_effort=AGENT_REASONING_EFFORT, **kwargs)
        except Exception as e:
            if "reasoning" not in str(e).lower():
                raise
            log_info(f"[AGENT] 模型 {kwargs.get('model')} 不支援 reasoning_effort，改用預設")
    return client.chat.completions.create(**kwargs)


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
