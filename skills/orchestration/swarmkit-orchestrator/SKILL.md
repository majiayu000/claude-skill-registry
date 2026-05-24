---
name: swarmkit-orchestrator
description: |
  Orchestrate multi-agent workflows using SwarmKit Python SDK. Use when tasks benefit from: (1) Parallel processing - analyzing many documents/items simultaneously, (2) Quality competition - running multiple agents and picking best result, (3) Synthesis - combining multiple analyses into unified output, (4) Multi-model workflows - using Claude for reasoning, Codex for code, Gemini for multimodal. Triggers: "analyze these N files", "try multiple approaches", "compare solutions", "process in parallel", "use different models", batch operations, quality-critical tasks.
---

# SwarmKit Orchestrator

Spawn parallel AI agents for batch processing, quality competition, and multi-model workflows.

> **Repo:** https://github.com/brandomagnani/swarmkit — cookbooks in `cookbooks/`, skills in `skills/`

## Setup

```bash
source scripts/setup.sh  # Creates .venv, installs swarmkit
```

Requires `SWARMKIT_API_KEY` (or provider keys + `E2B_API_KEY` for BYOK).

> **Note:** In Gateway mode, `SWARMKIT_API_KEY` is automatically injected into this sandbox by the parent SwarmKit process. The SDK picks it up from the environment—no manual configuration needed. This enables recursive orchestration: agents can spawn agents.

## Boilerplate

```python
import asyncio
from pydantic import BaseModel
from swarmkit import (
    Swarm, SwarmConfig, AgentConfig,
    BestOfConfig, VerifyConfig, RetryConfig,
    Pipeline, MapConfig, FilterConfig, ReduceConfig,
)

async def main():
    swarm = Swarm(SwarmConfig(
        agent=AgentConfig(type="claude", model="sonnet"),
        concurrency=4,           # Max parallel sandboxes
        timeout_ms=3_600_000,    # 1 hour per worker
        tag="my-pipeline",       # Observability prefix
    ))

    # ... operations here ...

asyncio.run(main())
```

## Operation Choice

| Signal | Operation | Output |
|--------|-----------|--------|
| N similar items | `map` | List of results |
| Quality critical | `best_of` | Single best result |
| Filter/gate | `filter` | Filtered list |
| Combine many → one | `reduce` | Single synthesized result |

## Operations

### map

```python
class Summary(BaseModel):
    title: str
    points: list[str]

results = await swarm.map(
    items=[{"doc.pdf": pdf_bytes}, {"doc2.pdf": pdf2_bytes}],
    prompt="Summarize this document",
    schema=Summary,                    # Optional: structured output
    agent=AgentConfig(type="claude", model="haiku"),
)

# Handle results
for r in results:
    if r.status == "success":
        print(r.data.title)            # Parsed schema
        print(r.files)                 # Output files dict
    elif r.status == "error":
        print(r.error)                 # Error message

# Convenience accessors
results.success   # List of successful
results.error     # List of failed
```

### filter

Schema and condition are **required**.

```python
class Eval(BaseModel):
    severity: str  # 'critical', 'warning', 'info'

results = await swarm.filter(
    items=documents,
    prompt="Assess severity of issues in this document",
    schema=Eval,                       # Required
    condition=lambda d: d.severity == "critical",  # Required
)

# results.success = passed condition (original input files)
# results.filtered = evaluated but didn't pass
# results.error = agent errors
```

### reduce

```python
report = await swarm.reduce(
    items=results.success,             # From map or filter
    prompt="Create unified report from all analyses",
    schema=ReportSchema,               # Optional
)

if report.status == "success":
    print(report.data)                 # Parsed schema
    print(report.files)                # Output files
else:
    print(report.error)
```

### best_of

Run N candidates, judge picks best.

```python
result = await swarm.best_of(
    item={"task.txt": "Complex problem..."},
    prompt="Solve this problem",
    config=BestOfConfig(
        n=3,
        judge_criteria="Most accurate and well-explained solution",
        # task_agents=[agent1, agent2, agent3],  # Different agents per candidate
        # judge_agent=AgentConfig(...),          # Override judge
    ),
)

print(result.winner.files)
print(result.winner.data)              # If schema provided
print(result.winner_index)             # 0, 1, or 2
print(result.judge_reasoning)
print(result.candidates)               # All candidate results
```

## Quality Options

### verify - LLM-as-judge with retry

```python
results = await swarm.map(
    items=documents,
    prompt="Analyze thoroughly",
    schema=AnalysisSchema,
    verify=VerifyConfig(
        criteria="Analysis must include specific evidence",
        max_attempts=3,                # Retry with feedback if fails
        # verifier_agent=AgentConfig(...),  # Override verifier
    ),
)

# Check verification info
for r in results.success:
    print(r.verify.passed)             # True
    print(r.verify.reasoning)          # Verifier's reasoning
    print(r.verify.attempts)           # How many attempts
```

### retry - Auto-retry on error

```python
results = await swarm.map(
    items=documents,
    prompt="Process document",
    retry=RetryConfig(
        max_attempts=3,
        backoff_ms=1000,
        backoff_multiplier=2,
    ),
)
```

### map + best_of - Quality at scale

```python
results = await swarm.map(
    items=documents,
    prompt="Analyze document",
    best_of=BestOfConfig(
        n=3,
        judge_criteria="Most thorough analysis",
    ),
)
# Each item gets 3 candidates, judge picks best per item
```

## Pipeline

Chain operations with clear data flow. Reusable across batches.

```
items → .map() → .map() → .filter() → .map() → .reduce()
           ↓        ↓          ↓          ↓         ↓
       [transform] [transform] [gate]  [transform] [synthesize]
```

Chain any sequence of `.map()` and `.filter()`. End with `.reduce()` (terminal).

**Why Pipeline vs Swarm:**
- Pipeline: chains of operations - cleaner, reusable
- Swarm: standalone operations or best_of on single item

```python
pipeline = (
    Pipeline(swarm)
    .map(MapConfig(
        name="analyze",
        prompt="Analyze document",
        schema=AnalysisSchema,
        verify=VerifyConfig(criteria="Must include evidence"),
    ))
    .filter(FilterConfig(
        name="critical",
        prompt="Rate severity",
        schema=Eval,
        condition=lambda d: d.severity == "critical",
    ))
    .reduce(ReduceConfig(
        name="report",
        prompt="Synthesize findings",
        schema=ReportSchema,
    ))  # Terminal - no steps after reduce
)

# Reusable across batches
result1 = await pipeline.run(batch1)
result2 = await pipeline.run(batch2)

# Access results
result.output                    # Final ReduceResult or list[SwarmResult]
result.steps[0].results          # Per-step results
result.steps[0].duration_ms
result.total_duration_ms
```

## Result Types

```python
# SwarmResult (from map, filter, best_of candidates)
r.status      # 'success' | 'filtered' | 'error'
r.data        # Parsed schema (Pydantic instance) or None
r.files       # dict[str, bytes] output files
r.error       # Error message if status == 'error'
r.raw_data    # Raw result.json if parse failed

# SwarmResultList (from map, filter)
results.success    # list[SwarmResult]
results.filtered   # list[SwarmResult]
results.error      # list[SwarmResult]

# ReduceResult (from reduce)
report.status      # 'success' | 'error'
report.data        # Parsed schema or None
report.files       # Output files
report.error       # Error message

# BestOfResult (from best_of)
result.winner           # SwarmResult
result.winner_index     # int
result.judge_reasoning  # str
result.candidates       # list[SwarmResult]
```

## Agent Types

| Type | Models | Default |
|------|--------|---------|
| `claude` | `opus`, `sonnet`, `haiku` | `opus` |
| `codex` | `gpt-5.2`, `gpt-5.2-codex` | `gpt-5.2` |
| `gemini` | `gemini-3-pro-preview`, `gemini-3-flash-preview` | `gemini-3-flash-preview` |
| `qwen` | `qwen3-coder-plus` | `qwen3-coder-plus` |

## Full Reference

For streaming, sessions, Composio, MCP servers: [references/api.md](references/api.md)
