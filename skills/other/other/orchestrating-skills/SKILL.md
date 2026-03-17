---
name: orchestrating-skills
description: >-
  Skill-aware orchestration with context routing. Decomposes complex tasks into
  skill-typed subtasks, extracts targeted context subsets, executes subagents in
  parallel, and synthesizes results. Self-answers trivial lookups inline. No SDK
  dependency — uses raw HTTP via httpx. Use when tasks require multiple analytical
  perspectives, when context is large and subtasks only need portions, or when
  orchestrating-agents spawns too many redundant subagents.
metadata:
  version: 0.3.0
  depends_on: []
---

# Skill-Aware Orchestration

Orchestrate complex multi-step tasks through a four-phase pipeline that eliminates
redundant context processing and reflexive subagent spawning.

## When to Use

- Task requires **multiple analytical perspectives** (e.g., compare + critique + synthesize)
- Context is large and **subtasks only need portions** of it
- Simple lookups should be **self-answered** without spawning subagents

## When NOT to Use

- Single-skill tasks (just use the skill directly)
- Tasks requiring tool use or code execution (this is text-analysis orchestration)
- Real-time streaming requirements (this is batch-oriented)

## Quick Start

```python
import sys
sys.path.insert(0, "/mnt/skills/user/orchestrating-skills/scripts")
from orchestrate import orchestrate

result = orchestrate(
    context=open("report.md").read(),
    task="Compare the two proposed architectures, extract cost figures, and recommend one",
    verbose=True,
)
print(result["result"])
```

## Dependencies

- **httpx** (usually pre-installed; `pip install httpx` if not)
- **No Anthropic SDK required**
- API key: reads `ANTHROPIC_API_KEY` env var or `/mnt/project/claude.env`

## Four-Phase Pipeline

### Phase 1: Planning (LLM)

The orchestrator reads the full context **once** and produces a JSON plan:

```json
{
  "subtasks": [
    {
      "task": "Compare architecture A vs B on scalability, cost, and complexity",
      "skill": "analytical_comparison",
      "context_pointers": {"sections": ["Architecture A", "Architecture B"]}
    },
    {
      "task": "What is the project budget?",
      "skill": "self",
      "answer": "$2.4M"
    }
  ]
}
```

Key behaviors:
- Assigns one skill per subtask from the built-in library
- Uses `"self"` for direct lookups (numbers, names, dates) — no subagent spawned
- Self-answering is an LLM judgment call, not a sentence-count heuristic
- Context pointers use **section headers** (structural, edit-resilient)

### Phase 2: Assembly (Deterministic Code)

No LLM calls. Extracts context subsets using section headers or line ranges,
pairs each with the assigned skill's system prompt, builds prompt dicts.

### Phase 3: Execution (Parallel LLM)

Delegated subtasks run in parallel via `concurrent.futures.ThreadPoolExecutor`.
Each subagent receives **only its context slice** and **skill-specific instructions**.

### Phase 4: Synthesis (LLM)

Collects all results (self-answered + subagent), synthesizes into a coherent
response that reads as if a single expert wrote it.

## Built-in Skill Library

Eight analytical skills plus one pipeline skill:

| Skill | Purpose |
|-------|---------|
| `analytical_comparison` | Compare items along dimensions with trade-offs |
| `fact_extraction` | Extract facts with source attribution |
| `structured_synthesis` | Combine multiple sources into narrative |
| `causal_reasoning` | Identify cause-effect chains |
| `critique` | Evaluate arguments for soundness |
| `classification` | Categorize items with rationale |
| `summarization` | Produce concise summaries |
| `gap_analysis` | Identify missing information |
| `remember` | Persist key findings to long-term memory via `remembering` skill (pipeline-only, runs post-synthesis) |

## API Reference

### `orchestrate(context, task, **kwargs) -> dict`

Returns:

```python
{
    "result": "Final synthesized response",
    "plan": {...},
    "subtask_count": 4,
    "self_answered": 1,
    "delegated": 3,
    "memory_ids": ["abc123"],  # populated when remember subtasks ran
}
```

Parameters:
- `context` (str): Full context to process
- `task` (str): What to accomplish
- `model` (str): Claude model, default `claude-sonnet-4-6`
- `max_tokens` (int): Per-subagent token limit, default 2048
- `synthesis_max_tokens` (int): Synthesis token limit, default 4096
- `max_workers` (int): Parallel subagent limit, default 5
- `skills` (dict): Custom skill library (merged with built-in)
- `persist` (bool): Auto-append a `remember` subtask to store findings, default False
- `verbose` (bool): Print progress to stderr

### CLI

```bash
python orchestrate.py \
    --context-file report.md \
    --task "Analyze this report" \
    --verbose --json
```

## Extending the Skill Library

```python
from skill_library import SKILLS

custom_skills = {
    **SKILLS,
    "code_review": {
        "description": "Review code for bugs, style, and security",
        "system_prompt": "You are a code review specialist...",
        "output_hint": "issues_list with severity and fix suggestions",
    }
}

result = orchestrate(context=code, task="Review this PR", skills=custom_skills)
```

## Persisting Findings with `remember`

`remember` is a **pipeline skill** — it executes in Phase 4 after synthesis, not as a
parallel subagent. It uses LLM distillation to extract the key insight from the synthesized
result, then writes it to long-term memory via the `remembering` skill.

### Two ways to activate persistence

**1. `persist=True` (automatic)**

```python
result = orchestrate(
    context=open("report.md").read(),
    task="Compare approaches A and B",
    persist=True,  # auto-injects a remember subtask
    verbose=True,
)
print(result["memory_ids"])  # ['abc123']
```

**2. Planner-emitted (explicit)**

The orchestrator planner can emit `remember` as a subtask when the task description
implies storage:

```json
{
  "task": "Store the key findings from this analysis",
  "skill": "remember",
  "context_pointers": {}
}
```

### Requirements

- `remembering` skill must be installed (`/mnt/skills/user/remembering` or
  `/home/user/claude-skills/remembering`)
- Turso credentials must be available (auto-detected by the remembering skill)
- If unavailable, persistence is skipped silently and `memory_ids` returns `[]`

## Architecture Details

See [references/architecture.md](references/architecture.md) for design decisions,
token efficiency analysis, and comparison with SkillOrchestra (arXiv 2602.19672).
