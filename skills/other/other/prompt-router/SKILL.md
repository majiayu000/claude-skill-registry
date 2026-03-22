---
name: prompt-router
description: "Route a classified request to the right skills, agent strategy, Context7 directives, and output format. Use this skill whenever you need to decide which skills to load for a task, choose between solo agent vs subagent dispatch vs tmux agent team, determine if Context7 library docs are needed, or select the right output format for a prompt. Trigger on: any request that has been classified and needs routing, when someone asks 'what skills should I use for this', 'should I use subagents', 'do I need tmux mode', or any prompt generation workflow that needs skill selection and strategy planning."
---

# Prompt Router

Maps a classified request to the optimal skill set, agent strategy, Context7 directives, and output format. Outputs a `PromptPlan` JSON consumed by the downstream prompt-generator skill.

## When to Use

- After running `/request-classifier` and you have a `RequestClassification` object
- When a user asks "what skills should I use for this task?"
- When a user asks "should I use subagents or a tmux team?"
- When a user asks "do I need Context7 for this?"
- As Step 3 in the full `/generate-prompt` pipeline

---

## Quick Routing Guide

| If you have... | Route to... |
|---|---|
| `feature` + complexity > 6 | Tmux team + planning-with-files + parallel dispatch |
| `feature` + complexity 4-6 | Subagent dispatch + planning-with-files |
| `feature` + complexity 1-3 | Solo agent + domain skills only |
| `bug-fix` (any complexity) | Solo focused agent + systematic-debugging |
| `research` (any complexity) | Parallel subagents + planning-with-files + Context7 |
| `improvement` + complexity > 6 | Subagent dispatch with gates + verification-before-completion |
| `improvement` + complexity 1-6 | Solo agent + verification-before-completion |
| `pipeline` (any complexity) | Tmux team + langgraph-fundamentals + acm-observability + Context7 |
| `frontend` + complexity > 6 | Tmux team + frontend skills + maybe Context7 |
| `frontend` + complexity 1-6 | Solo agent + frontend skills |
| `quick-task` | Solo agent, minimal or no extra skills |
| `documentation` | Solo agent, no extra skills |

---

## Routing Steps

### Step 1: Read the classification

Accept a `RequestClassification` object from `/request-classifier` or extract it inline from the user's request:

```json
{
  "type": "feature|bug-fix|research|improvement|pipeline|frontend|quick-task|documentation",
  "complexity": 1-10,
  "plan_mode": true|false,
  "domain_signals": ["extraction", "graph", "model", "debug", ...],
  "scope": "single-file|multi-file|cross-cutting",
  "estimated_files": 0
}
```

If no classification is available, run the classification heuristics from `/request-classifier` taxonomy before proceeding.

### Step 2: Read the routing matrix

Open `references/routing-rules.md` and locate the row matching `type + complexity_band`:
- **Simple**: complexity 1-3
- **Medium**: complexity 4-6
- **Complex**: complexity 7-10

### Step 3: Match classification to routing matrix row

Find the exact row. If the type is ambiguous (e.g., a feature with pipeline signals), use the more specific type (`pipeline` beats `feature`).

Priority order when multiple types match:
1. `pipeline` — most specific, always wins
2. `frontend` — specific domain
3. `bug-fix` — has fixed strategy
4. `feature` / `improvement` / `research` — use complexity band
5. `quick-task` / `documentation` — fallback

### Step 4: Apply domain skill selection logic

Check `domain_signals` array from the classification and append additional skills:

| Signal | Additional Skills |
|---|---|
| "extraction", "pipeline", "graph", "node" | `/langgraph-fundamentals`, `/acm-observability` |
| "agent", "tool", "chain" | `/langchain-fundamentals` |
| "model", "schema", "pydantic", "validation" | `/pydantic-models-py` |
| "debug", "error", "trace", "failing" | `/systematic-debugging`, `/acm-observability` |
| "component", "page", "UI", "React", "css" | `/react-best-practices`, `/next-best-practices` |
| "streaming", "SSE", "websocket" | `/sse-streaming` |
| "test", "coverage", "pytest", "playwright" | `/test-driven-development`, `/verification-before-completion` |
| No specific signal | No additional skills |

Deduplicate the final skill list (routing matrix skills + domain signal skills).

### Step 5: Build Context7 directives if needed

Check the `context7` column of the matched routing row. If yes (or conditional and condition is met), build directives using the templates in `references/routing-rules.md`:

- For each library relevant to the request, add one directive:
  `resolve-library-id for "{library}" → query-docs for "{topic from request}"`

Always include Context7 for:
- `pipeline` type → LangGraph + LangChain
- `research` type → any library mentioned in the request
- `feature` with explicit library version in request → that library

### Step 6: Select agent strategy template

Use `references/agent-strategies.md` and select the template matching the routing matrix `agent_strategy` column:
- `solo` → Template A
- `subagent-dispatch` → Template B
- `tmux-team` → Template C

Fill in the `{placeholder}` variables from the classification data.

### Step 7: Determine output format and path

| Output Format | When | Path |
|---|---|---|
| `prompt-pack` (markdown file) | Complex requests, plan mode ON, tmux or subagent strategy | `docs/sprint-artifacts/prompt-packs/YYYY-MM-DD-{slug}.md` |
| `copy-paste` (terminal print) | Medium requests, solo or subagent, plan mode optional | Print to terminal |
| `terminal` (inline response) | Simple requests, quick-task, documentation | Respond inline |

If user explicitly requested "save" or "prompt-pack" → always use `prompt-pack` format.
If user requested "no plan" → downgrade from `prompt-pack` to `copy-paste` unless still complex.

### Step 8: Output the PromptPlan JSON

Assemble and return the complete `PromptPlan` object:

```json
{
  "classification": {
    "type": "...",
    "complexity": 0,
    "plan_mode": true,
    "domain_signals": [],
    "scope": "...",
    "estimated_files": 0
  },
  "selected_skills": ["/planning-with-files", "/langgraph-fundamentals"],
  "agent_strategy": "tmux-team|subagent-dispatch|solo",
  "agent_config": {
    "panes": [],
    "subagents": [],
    "solo": true
  },
  "context7_directives": [],
  "output_format": "prompt-pack|copy-paste|terminal",
  "output_path": "docs/sprint-artifacts/prompt-packs/",
  "plan_mode": true,
  "plan_type": "full|debug|research|refactor|none",
  "verification_items": [
    "uv run ruff check .",
    "uv run pytest tests/",
    "cd frontend && npm run build"
  ]
}
```

The `PromptPlan` JSON is passed directly to the `/prompt-generator` skill (S4) as its primary input.

---

## Verification Items by Type

Always include these base verification items in `verification_items`:

| Type | Verification Commands |
|---|---|
| Backend only | `uv run ruff check .`, `uv run pytest tests/` |
| Frontend only | `cd frontend && npm run lint`, `cd frontend && npm run build` |
| Full stack | `uv run ruff check .`, `uv run pytest tests/`, `cd frontend && npm run build` |
| Pipeline / LangGraph | All backend + `uv run pytest tests/test_extraction*` |
| Quick-task | `uv run ruff check .` (lint only) |
| Documentation | None required |

---

## Common Routing Scenarios

**"Add a new extraction provider for MinerU v3"**
→ type=`pipeline`, complexity=7, skills=[`/langgraph-fundamentals`, `/acm-observability`, `/planning-with-files`, `/pydantic-models-py`], strategy=tmux-team, Context7=LangGraph+LangChain, format=prompt-pack

**"Fix the timeout error in the building extraction graph"**
→ type=`bug-fix`, complexity=5, skills=[`/systematic-debugging`, `/acm-observability`, `/langgraph-fundamentals`], strategy=solo, Context7=conditional (LangGraph if API-related), format=copy-paste

**"Rename the extract_all_rows function"**
→ type=`quick-task`, complexity=1, skills=[], strategy=solo, Context7=no, format=terminal

**"Investigate why correction LLM calls are spiking"**
→ type=`research`, complexity=6, skills=[`/acm-observability`, `/planning-with-files`, `/langgraph-fundamentals`], strategy=subagent-dispatch (parallel research panes), Context7=LangGraph, format=prompt-pack

**"Add the building summary panel to the source detail page"**
→ type=`frontend`, complexity=5, skills=[`/react-best-practices`, `/next-best-practices`], strategy=solo, Context7=no, format=copy-paste

**"Refactor all pre-extraction stages to reduce LLM calls"**
→ type=`improvement`, complexity=8, skills=[`/planning-with-files`, `/subagent-driven-development`, `/verification-before-completion`, `/systematic-debugging`], strategy=subagent-dispatch-with-gates, Context7=conditional (LangGraph if graph patterns change), format=prompt-pack
