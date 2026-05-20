---
name: dk-breadcrumb-creator
description: "Traces a workflow end-to-end through the harness-kit monorepo and creates a breadcrumb analysis doc in docs/breadcrumb_analysis/. Use this skill whenever the user wants to document a flow, trace a workflow, understand how a feature works across layers (frontend → backend → worker → CLI), or create debugging guides for a specific flow. Also use when the user mentions 'breadcrumb', 'trace this flow', 'how does X work end to end', 'document this workflow', or /dk-breadcrumb-creator."
argument-hint: "<flow name or description, e.g. 'spec execution' or 'task creation from board view'>"
allowed-tools: Bash, Read, Edit, Write, Task, Grep, Glob
---

# /dk-breadcrumb-creator — Workflow Breadcrumb Analysis

Traces a workflow through the harness-kit monorepo and produces a compact debugging reference. The output is for devs and agents who need to find where things break — not for onboarding docs or architecture overviews.

## Context

<flow_context> $ARGUMENTS </flow_context>

If the context above is empty, ask: "Which flow do you want to trace? Describe it in terms of the user action or system event that kicks it off."

## Step 0: Check existing breadcrumbs

Before scoping anything, read `docs/breadcrumb_analysis/_INDEX.md` to see what already exists. This file lists every breadcrumb folder and what it traces.

Compare the user's request against the existing entries and make one of three decisions:

1. **Already covered** — The flow is substantially documented in an existing breadcrumb. Tell the user which one covers it and what it contains. Ask if they want to update/extend that existing doc instead of creating a new one.

2. **Partially overlapping** — An existing breadcrumb covers part of the flow (e.g., user asks about "task execution" and `spec-task-lifecycle/02-execute-and-dispatch/` covers the dispatch side but not the harness execution internals). Options:
   - **Extend** the existing breadcrumb (add sections to its FLOW/DETAILS/DEBUG files, or add a new sub-flow folder)
   - **Create a new breadcrumb** that covers the non-overlapping portion, cross-referencing the existing one

3. **New territory** — Nothing in the index covers this flow. Proceed to Step 1.

When extending an existing breadcrumb, read its current FLOW.md first so you don't duplicate content. Add new information that complements what's there — don't rewrite sections that are already accurate.

When creating a new breadcrumb that's adjacent to an existing one, add cross-references in both directions (a "See also" line in the new doc pointing to the existing one, and optionally a note in the existing doc pointing to the new one).

Present your decision to the user before proceeding. Something like:

```
Existing breadcrumbs I checked:
- spec-task-lifecycle/02-execute-and-dispatch — covers DAG dispatch, task status transitions
- harness-isolation-testing — covers harness CLI construction, MCP config, streaming

Your request overlaps with <X> in these areas: <list>.
I recommend: <extend existing / create new focused on Y / already covered>.
```

## Step 1: Scope the flow

Before touching any code, define the boundaries:

```
FLOW: <name — short, kebab-case, used as folder name>
TRIGGER: <what kicks it off — button click, API call, CLI command, cron>
LAYERS: <which layers it touches — fe, api, celery, odin, db>
END STATE: <what the user/system sees when it completes>
```

If the flow is large (touches 5+ files per layer, or has multiple independent branches), break it into sub-flows. Each sub-flow gets its own folder. Create a parent `_INDEX.md` that links them.

Example of when to split:
- "spec execution" → split into: `spec-planning`, `spec-task-dispatch`, `spec-task-execution`, `spec-assembly`
- "task creation" → probably fine as one flow (FE form → API → DB → response)

Ask the user to confirm the scope before proceeding.

## Step 2: Trace the flow

Work through each layer the flow touches, in execution order. For each hop, record:

1. **Source file and function** — where the action originates
2. **What it does** — one line, no fluff
3. **What it passes** — key data (payload shape, IDs, status values)
4. **Where it goes next** — the next file/function/service in the chain

Use the codebase directly. Read the actual code. Don't guess from file names.

### Tracing tips

- **Frontend → Backend**: Search for the API URL in the frontend service files (`src/services/`). Match it to the Django URL conf and view.
- **Backend → Celery**: Search for `.delay(` or `.apply_async(` calls. Check `config/celery.py` and any `tasks.py` files.
- **Backend → Odin**: Look for `subprocess` calls to `odin` CLI or check `dag_executor.py` for execution strategy routing.
- **Odin internals**: Follow from `cli.py` → `orchestrator.py` → harness `execute()` methods.
- **Signal/hook chains**: Check Django signals, DRF `perform_create`/`perform_update` overrides, and model `save()` methods for side effects.

## Step 3: Create the breadcrumb docs

Create the folder: `docs/breadcrumb_analysis/<flow-name>/`

Generate three files:

### File 1: `FLOW.md` — High-level flow

This is the "where does data go" overview. Should be readable in 30 seconds.

Format:

```markdown
# <Flow Name>

Trigger: <what starts it>
End state: <what the outcome is>

## Flow

<component/file> :: <function>
  → <what it sends / does>
<next component/file> :: <function>
  → <what it sends / does>
<next component/file> :: <function>
  → ...

## Sub-flows

(if applicable — link to sub-flow folders)
```

Example of the flow notation:

```
BoardView.tsx :: handleCreateTask()
  → POST /tasks/ {title, board_id, priority, status}
tasks/views.py :: TaskViewSet.create()
  → validates, saves to DB, returns TaskReadSerializer response
tasks/models.py :: Task.save()
  → triggers TaskHistory creation via signal
```

Keep it linear. If there's branching (e.g., different execution strategies), show each branch with a label:

```
tasks/dag_executor.py :: maybe_execute_task()
  → checks ODIN_EXECUTION_STRATEGY

  [strategy=local]
  dag_executor.py :: _execute_local()
    → subprocess: odin exec <task_id>

  [strategy=celery_dag]
  execution/celery_dag.py :: poll_and_execute()
    → picks up task on next poll cycle (every 5s)
```

### File 2: `DETAILS.md` — Detailed trace

This is the "I need to understand what's actually happening" doc. File/function level, with the key logic noted.

Format:

```markdown
# <Flow Name> — Detailed Trace

## 1. <Layer/Step Name>

**File**: `path/to/file.py`
**Function**: `function_name()`
**Called by**: <what triggers this>
**Calls**: <what this triggers next>

Key logic:
- <important conditional, validation, transformation>
- <side effects — signals, logs, cache updates>
- <error handling — what happens on failure>

Data in: <shape of input>
Data out: <shape of output>

---

## 2. <Next Layer/Step>
...
```

Include only details that matter for debugging. Skip boilerplate (imports, standard DRF validation, obvious CRUD). Focus on:
- Conditionals that change behavior (if/else branches, feature flags, env vars)
- Data transformations (where shape changes, fields get renamed, data gets enriched)
- Side effects (signals, async tasks, external calls)
- Error paths (what exceptions get raised, what gets logged)

### File 3: `DEBUG.md` — Debugging guide

This is the "something broke in this flow, where do I look" doc.

Format:

```markdown
# <Flow Name> — Debug Guide

## Log locations

| Layer | Log file | What's in it |
|-------|----------|-------------|
| Django | `taskit/taskit-backend/logs/taskit_detail.log` | Request/response, view errors |
| DAG exec | `taskit/taskit-backend/logs/dag_exec_<task_id>.log` | Per-task execution log |
| Odin | `.odin/logs/run_<run_id>.jsonl` | Structured execution events |
| Celery | terminal output / broker | Task dispatch and results |
| Frontend | browser console | API call errors, state updates |

(include only rows relevant to this flow)

## What to search for

| Symptom | Where to look | Search term |
|---------|--------------|-------------|
| <common failure mode> | <file or log> | <grep pattern> |
| <another failure mode> | <file or log> | <grep pattern> |

## Quick commands

```bash
# <description of what this checks>
<command>

# <description>
<command>
```

## Env vars that affect this flow

| Variable | Effect | Default |
|----------|--------|---------|
| <VAR_NAME> | <what it changes in this flow> | <default value> |

## Common breakpoints

Where to put breakpoints or print statements when debugging this flow:

- `path/to/file.py:function_name()` — <why this is a good breakpoint>
- `path/to/other.py:other_func()` — <why>
```

### Quick commands section guidance

Include commands that are actually useful for this specific flow. Examples:

```bash
# Check if a task exists and its current state
python taskit/taskit-backend/testing_tools/task_inspect.py <task_id> --brief

# Tail the backend log filtered to a specific task
grep "task_id" taskit/taskit-backend/logs/taskit_detail.log | tail -20

# Check celery worker status
celery -A config inspect active

# Check what odin logged for a spec run
cat .odin/logs/run_<id>.jsonl | python -m json.tool
```

Don't include generic commands. Every command should be specific to debugging THIS flow.

## Step 4: Verify completeness

Before finishing, check:

- [ ] Every layer the flow touches has at least one entry in FLOW.md
- [ ] DETAILS.md covers every hop in FLOW.md with file/function specifics
- [ ] DEBUG.md has log locations for every layer involved
- [ ] DEBUG.md has at least 3 "what to search for" entries based on realistic failure modes
- [ ] Quick commands actually work (test them if possible)
- [ ] No fluff — every line earns its place
- [ ] `docs/breadcrumb_analysis/_INDEX.md` is updated (new folder → add row to the Flows table AND relevant entries to Quick Navigation)

## Step 5: Output summary

After creating the docs, tell the user:

```
Created breadcrumb analysis for: <flow name>
Location: docs/breadcrumb_analysis/<flow-name>/
Files:
  FLOW.md    — high-level flow (<N> steps)
  DETAILS.md — detailed trace (<N> sections)
  DEBUG.md   — debug guide (<N> log sources, <N> search patterns, <N> commands)

Updated: docs/breadcrumb_analysis/_INDEX.md (added to Flows table + Quick Navigation)
```

If you extended an existing breadcrumb rather than creating a new folder, adjust the summary accordingly (mention which files were updated and what was added).

## Style rules

These docs are dev-to-dev notes. They exist so someone (human or agent) can quickly find where to look when something breaks.

- No intro paragraphs. No "this document describes...". Jump straight to content.
- No emoji, no bold-for-emphasis-everywhere, no decorative headers.
- Use code formatting for file paths, function names, commands, env vars.
- One line per concept. If a sentence has "and" in it, consider splitting.
- Prefer tables over prose for structured data (log locations, env vars, search patterns).
- Use `monospace` for anything that appears in code or terminal.
- If you're unsure about something, mark it with `[?]` rather than guessing.

## When to split into sub-flows

Split when:
- The flow has distinct phases that can fail independently (planning vs execution vs assembly)
- Different teams/agents own different parts
- A single FLOW.md would exceed ~50 lines of flow notation

When splitting, create:
```
docs/breadcrumb_analysis/<parent-flow>/
├── _INDEX.md          # Lists sub-flows, brief description of each, execution order
├── <sub-flow-1>/
│   ├── FLOW.md
│   ├── DETAILS.md
│   └── DEBUG.md
└── <sub-flow-2>/
    ├── FLOW.md
    ├── DETAILS.md
    └── DEBUG.md
```

The `_INDEX.md` format:

```markdown
# <Parent Flow Name>

Split into sub-flows because: <one-line reason>

## Sub-flows (execution order)

1. **<sub-flow-1>** — <what this phase does>
2. **<sub-flow-2>** — <what this phase does>

## Shared context

<any env vars, config, or state that spans all sub-flows>
```
