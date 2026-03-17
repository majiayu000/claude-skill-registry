---
name: mapreduce
description: The MapReduce skill enables parallel task execution across multiple AI providers or agent instances, followed by intelligent consolidation of results. This produces higher-quality outputs by levera...
---

# MapReduce Skill

> **Skill ID**: mapreduce
> **Purpose**: Fan-out tasks to multiple providers/agents, then consolidate results
> **Category**: Orchestration

## Overview

The MapReduce skill enables parallel task execution across multiple AI providers
or agent instances, followed by intelligent consolidation of results. This
produces higher-quality outputs by leveraging diverse model strengths and
cross-validating findings.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MAIN THREAD (Orchestrator)                          │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 1: MAP (Parallel Fan-Out)                                │    │
│  │                                                                 │    │
│  │  Task(worker-1) ──→ output-1.md                                │    │
│  │  Task(worker-2) ──→ output-2.md                                │    │
│  │  Task(worker-3) ──→ output-3.md                                │    │
│  │  bash(codex)   ──→ output-codex.md                             │    │
│  │  bash(gemini)  ──→ output-gemini.md                            │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 2: COLLECT (Timeout-Based)                               │    │
│  │                                                                 │    │
│  │  TaskOutput(worker-1, timeout=120s)                            │    │
│  │  TaskOutput(worker-2, timeout=120s)                            │    │
│  │  TaskOutput(worker-3, timeout=120s)                            │    │
│  │  Verify: output-codex.md, output-gemini.md exist               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PHASE 3: REDUCE (Consolidation)                                │    │
│  │                                                                 │    │
│  │  Task(reducer) ──→ reads all outputs ──→ consolidated.md       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Constraint

**Subagents cannot spawn other subagents.** All orchestration happens in the
main thread. Workers and reducers are subagents that operate on files.

## Use Cases

### 1. Parallel Planning

Fan out planning task to multiple providers with different strategic biases:

```
Workers:
  - planner-conservative: Low-risk, proven patterns
  - planner-aggressive: Fast-track, modern patterns
  - planner-security: Security-first approach

Reducer: plan-reducer
Output: specs/ROADMAP.md
```

See: `cookbook/parallel-planning.md`

### 2. Multi-Implementation

Generate the same feature with multiple models, pick best:

```
Workers:
  - impl-claude: Claude's implementation
  - impl-codex: OpenAI's implementation
  - impl-gemini: Gemini's implementation

Reducer: code-reducer
Output: src/feature/implementation.ts
```

See: `cookbook/multi-impl.md`

### 3. Debug Consensus

Get multiple diagnoses of a bug, verify and select best fix:

```
Workers:
  - debug-claude: Claude's diagnosis
  - debug-codex: Codex's diagnosis
  - debug-gemini: Gemini's diagnosis

Reducer: debug-reducer
Output: Applied fix + documentation
```

See: `cookbook/debug-consensus.md`

## Available Reducers

| Reducer | Agent Path | Purpose |
|---------|------------|---------|
| `plan-reducer` | `agents/orchestration/reducers/plan-reducer.md` | Consolidate plans |
| `code-reducer` | `agents/orchestration/reducers/code-reducer.md` | Compare/merge code |
| `debug-reducer` | `agents/orchestration/reducers/debug-reducer.md` | Verify fixes |

## Provider Integration

### Claude Subagents (via Task tool)

```
Task(subagent_type="Plan", prompt="...", run_in_background=true)
```

### External CLI Providers (via spawn skill)

```bash
# Codex
codex -m gpt-5.1-codex -a full-auto "${PROMPT}" > output.md

# Gemini
gemini -m gemini-3-pro "${PROMPT}" > output.md

# Cursor
cursor-agent --mode print "${PROMPT}" > output.md

# OpenCode
opencode --provider anthropic "${PROMPT}" > output.md
```

See: `skills/spawn/agent/cookbook/` for detailed CLI patterns.

## File Conventions

All MapReduce operations follow standard file conventions:

| Type | Location | Naming |
|------|----------|--------|
| Plan outputs | `specs/plans/` | `planner-{name}.md` |
| Code outputs | `implementations/` | `impl-{name}.{ext}` |
| Debug outputs | `diagnoses/` | `debug-{name}.md` |
| Consolidated | Specified in prompt | `ROADMAP.md`, `implementation.ts` |

See: `reference/file-conventions.md`

## Scoring Rubrics

Each reducer uses a specific scoring rubric:

- **Plans**: Completeness, Feasibility, Risk, Clarity, Innovation
- **Code**: Correctness, Readability, Maintainability, Performance, Security
- **Debug**: Correctness, Minimality, Safety, Clarity, Root Cause

See: `reference/scoring-rubrics.md`

## Commands

| Command | Purpose |
|---------|---------|
| `/ai-dev-kit:mapreduce` | Full MapReduce workflow |
| `/ai-dev-kit:map` | Just the fan-out phase |
| `/ai-dev-kit:reduce` | Just the consolidation phase |

## Example: Full MapReduce

```markdown
# In main thread:

## Step 1: MAP

Launch planners in a single message (enables parallelism):

Task(subagent_type="Plan", prompt="""
  Create implementation plan for: User Authentication
  Write to: specs/plans/planner-conservative.md
  Strategy: Conservative - proven patterns, minimal risk
""", run_in_background=true)

Task(subagent_type="Plan", prompt="""
  Create implementation plan for: User Authentication
  Write to: specs/plans/planner-aggressive.md
  Strategy: Aggressive - fast, modern patterns
""", run_in_background=true)

Bash("codex -m gpt-5.1-codex -a full-auto 'Create auth plan' > specs/plans/planner-codex.md")

## Step 2: COLLECT

TaskOutput(task_id=conservative-id, block=true, timeout=120000)
TaskOutput(task_id=aggressive-id, block=true, timeout=120000)

# Verify codex output exists
Read("specs/plans/planner-codex.md")

## Step 3: REDUCE

Task(subagent_type="ai-dev-kit:orchestration:plan-reducer", prompt="""
  Consolidate plans in specs/plans/*.md
  Output: specs/ROADMAP.md
  Priority: Security over speed
""")
```

## Cookbook

- `parallel-planning.md`: Multi-provider planning workflows
- `multi-impl.md`: Code generation with selection
- `debug-consensus.md`: Multi-diagnosis bug fixing

## Reference

- `scoring-rubrics.md`: Detailed scoring criteria
- `file-conventions.md`: Output file standards

## Related Skills

- `spawn`: Provider-specific CLI invocation patterns
- `multi-agent-orchestration`: General multi-agent patterns
- `research`: Parallel research with synthesis
