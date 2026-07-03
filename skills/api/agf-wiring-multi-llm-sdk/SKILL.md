---
name: agf-wiring-multi-llm-sdk
description: Use when wiring up or switching between China-domestic LLM providers (DeepSeek, Doubao/Volc Ark, Qwen/DashScope, MiniMax). Provides OpenAI-compatible adapter pattern, env-var contracts, fallback strategy, cost guardrails, and minimum verifications before declaring integration done.
---

# Wiring Multi-LLM SDK (DeepSeek / Doubao / Qwen / MiniMax)

Use this skill when:

- You add a new LLM provider to `backend/app/agents/` or any backend module
- You switch the default provider (e.g. DeepSeek → Doubao for cost reasons)
- You wire fallback / retry logic between providers
- You suspect a provider mismatch is the cause of a bug

## Decision: which SDK style?

All four providers expose **OpenAI-compatible endpoints**. Default to the `openai` Python SDK with a custom `base_url` rather than each vendor's bespoke SDK — fewer dependencies, easier to swap, less drift.

Bespoke SDK exceptions:
- Doubao multimodal (image/video gen): use `volcengine-python-sdk` for Ark image API
- MiniMax video / TTS: use `minimax` official SDK
- Streaming nuance: confirm OAI-compat client handles vendor's stream chunk format

Before wiring any SDK, pull its **current** docs via Context7 (`resolve-library-id` → `get-library-docs`) — all four vendors iterate fast and training-data memory of their APIs is likely stale. Context7 coverage of domestic SDKs varies; if a library isn't indexed, fall back to WebFetch on official docs.

## Env var contract (locked)

All providers follow the same pattern. **Never hardcode keys.** Each is read from environment at module init; a missing key raises early.

| Provider | Endpoint env | Key env | Default model env |
|---|---|---|---|
| DeepSeek | `DEEPSEEK_BASE_URL` (default `https://api.deepseek.com/v1`) | `DEEPSEEK_API_KEY` | `DEEPSEEK_MODEL` (e.g. `deepseek-chat`) |
| Doubao (Volc Ark) | `ARK_BASE_URL` (default `https://ark.cn-beijing.volces.com/api/v3`) | `ARK_API_KEY` | `ARK_MODEL_ENDPOINT_ID` (vendor-specific endpoint id, NOT model name) |
| Qwen (DashScope) | `DASHSCOPE_BASE_URL` (default `https://dashscope.aliyuncs.com/compatible-mode/v1`) | `DASHSCOPE_API_KEY` | `QWEN_MODEL` (e.g. `qwen-plus`) |
| MiniMax | `MINIMAX_BASE_URL` (default `https://api.minimaxi.com/v1`) | `MINIMAX_API_KEY` | `MINIMAX_MODEL` (e.g. `abab6.5s-chat`) |

> **Doubao gotcha:** the "model name" in OAI-compat call is actually the Ark endpoint id (`ep-2024xxxx`), not a public model id like `doubao-pro-32k`. Get the endpoint id from Volc Ark console.

## Adapter skeleton (Python / FastAPI)

```python
# backend/app/agents/llm_clients.py
import os
from openai import OpenAI

def get_client(provider: str) -> tuple[OpenAI, str]:
    if provider == "deepseek":
        return OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        ), os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    if provider == "doubao":
        return OpenAI(
            api_key=os.environ["ARK_API_KEY"],
            base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
        ), os.environ["ARK_MODEL_ENDPOINT_ID"]
    if provider == "qwen":
        return OpenAI(
            api_key=os.environ["DASHSCOPE_API_KEY"],
            base_url=os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        ), os.getenv("QWEN_MODEL", "qwen-plus")
    if provider == "minimax":
        return OpenAI(
            api_key=os.environ["MINIMAX_API_KEY"],
            base_url=os.getenv("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1"),
        ), os.getenv("MINIMAX_MODEL", "abab6.5s-chat")
    raise ValueError(f"unknown provider: {provider}")
```

## Fallback strategy

Default order (tunable in CLAUDE.md per project): **DeepSeek → Doubao → Qwen → MiniMax**.

- 5xx / network → next provider
- 4xx (auth / quota) → DO NOT failover; raise (signals config bug)
- Latency P95 breach (> 5s for non-streaming) → tier down silently, log warning

Implement with `tenacity` retry + a thin orchestrator that walks the list. **Never silently swap models** without telemetry — every failover emits a structured log line per `observability.md`.

## Token + cost telemetry

Every call must record the LLM fields mandated by `observability.md:17` plus `provider`. DeepSeek + Doubao support prompt caching — read `cache_hit_ratio` off the response usage object.

## Verifications before "done"

Before claiming the integration works, run this checklist explicitly. **Verify outputs match expectations — do not assume.**

- [ ] Smoke: each enabled provider answers "你好" with non-empty text and >0 token usage
- [ ] Streaming: chunk delivery is real (not buffered all-at-once); first-token latency logged
- [ ] Failover: simulate one provider down (point base_url at `localhost:1`) and confirm auto-fallback + log line
- [ ] Cost: token usage written to log + DB on every call
- [ ] Secrets: no key appears in logs / git diff (run `git diff | grep -iE 'api[_-]?key|secret|token'` before commit)
- [ ] Unit test mocks at the OpenAI SDK boundary (not at HTTP level) — survives base_url changes
- [ ] SDK surface: API calls cross-checked against current docs (Context7 or official site) — not from training memory

## Anti-patterns

- ❌ Hardcoding `base_url` strings — always read from env
- ❌ Passing public model id to Doubao — use endpoint id
- ❌ Catching all exceptions and returning empty string — masks auth failures and quota issues
- ❌ Assuming all providers return the same `usage` shape — validate and normalize
- ❌ Storing keys in CLAUDE.md / settings.json — only `.env` (gitignored) or secret manager

## References

- DeepSeek: https://platform.deepseek.com/api-docs
- Doubao / Volc Ark: https://www.volcengine.com/docs/82379
- Qwen / DashScope: https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope
- MiniMax: https://platform.minimaxi.com/document/ChatCompletion
