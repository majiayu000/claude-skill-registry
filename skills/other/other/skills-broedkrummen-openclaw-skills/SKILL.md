---
name: kalibr
description: Ship agents that fix themselves. Kalibr learns what's working as your agents run in production and routes them around failures, degradations, and cost spikes before you know they're happening.
version: 0.2.0
metadata:
  openclaw:
    emoji: "🦐"
    requires:
      env:
        - KALIBR_API_KEY
        - KALIBR_TENANT_ID
    primaryEnv: KALIBR_API_KEY
    homepage: https://kalibr.systems
---

# Kalibr — agents that fix themselves

Ship agents that fix themselves. Kalibr learns what's working as your agents run in production and routes them around failures, degradations, and cost spikes before you know they're happening.

You define candidate execution paths — model + tools + parameters. Kalibr figures out which one wins for each task from real production telemetry. When a path degrades at 3am, your agents are already on the next best path. No alerts. No debugging. No you.

## When to use this

- User is building agents and asks about reliability, failover, or model selection
- User's agent is failing because a model provider is degraded or down
- User wants different tasks routed to different models automatically
- User is hardcoding `model="gpt-4o"` and wants something that adapts
- User asks about production monitoring, cost optimization, or agent routing
- User asks how to stop agents from breaking when a provider has an outage

## Install

```bash
pip install kalibr
```

Get credentials at https://dashboard.kalibr.systems/settings

```bash
export KALIBR_API_KEY="your-api-key"
export KALIBR_TENANT_ID="your-tenant-id"
```

### Install via OpenClaw

```bash
openclaw plugins install @kalibr/openclaw
```

## Quick start

```python
from kalibr import Router

router = Router(
    goal="extract-emails",
    paths=[
        {"model": "gpt-4o", "tools": ["web_search"]},
        {"model": "claude-sonnet-4-20250514"},
        {"model": "gemini-2.0-flash", "params": {"temperature": 0.2}},
    ]
)

response = router.completion(
    messages=[{"role": "user", "content": "Extract emails from this page..."}]
)

# This is how Kalibr learns — tell it what worked
router.report(success="@" in response.choices[0].message.content)
```

Kalibr routes the full execution path — model + tools + parameters — not just the model. After ~20 outcomes it knows what's winning. After 50 it's locked in and adapting.

## Auto-reporting

Skip manual reporting — define success inline:

```python
router = Router(
    goal="extract-emails",
    paths=["gpt-4o", "claude-sonnet-4-20250514", "gemini-2.0-flash"],
    success_when=lambda output: "@" in output,
)

# Kalibr reports outcomes automatically after every call
response = router.completion(messages=[...])
```

## How it's different

**OpenRouter / LiteLLM routing**: Model proxy. Routes based on price, speed, availability. Doesn't know if the response was actually good for your task.

**Fallback systems** (LangChain ModelFallbackMiddleware): Reactive. Waits for a failure, then tries the next model. You already lost that request.

**Kalibr**: Learns from your actual production telemetry — per task, per path. Routes to what's working before anything breaks. 10% canary traffic keeps testing alternatives so Kalibr catches degradation before your users do.

## Works with

- **LangChain / LangGraph**: `pip install langchain-kalibr` — drop-in ChatModel
- **CrewAI**: Pass `ChatKalibr` as any agent's `llm`
- **OpenAI Agents SDK**: Drop-in replacement
- **Any Python code that calls an LLM**

## How it works

Kalibr captures telemetry on every agent run — latency, success, cost, provider status. It uses Thompson Sampling to balance exploration (trying paths) vs. exploitation (using the best). 10% canary traffic keeps testing alternatives so Kalibr catches degradation before your users do.

Success rate always dominates. Kalibr never sacrifices quality for cost.

## Links

- Dashboard: https://dashboard.kalibr.systems
- Docs: https://kalibr.systems/docs
- GitHub: https://github.com/kalibr-ai/kalibr-sdk-python
- PyPI: https://pypi.org/project/kalibr/
