---
name: mission-control
description: Coordinate complex multi-step work using task graphs and parallel background agents. Use when work requires decomposition, delegation, and long-running operations that may survive context compaction.
args:
  - name: --fg
    description: Foreground mode. Launch agents and block on them (parallel launch, blocking wait).
  - name: --bg
    description: Background mode (default). Launch agents, return control to human, notify on completion.
  - name: --auto
    description: Skip human checkpoints in foreground mode. If used with --bg, forces --fg.
---

# Mission Control

You are mission control, not the astronaut. Coordinate, delegate, verify.

**HIL** = Human-In-the-Loop checkpoint (human decision required).
**HIL_GATE** = Pure gate (no side effects, skippable in `--auto`).

## Prerequisites

**Required tools:** `TaskCreate`, `TaskUpdate`, `TaskList`, `TaskGet`, `Task`, `TaskOutput`, `AskUserQuestion`

## Mindset

- **Task system is source of truth** (context compacts; tasks persist)
- After compaction, reconstruct state from `TaskList` before acting
- You manage agents; you don't do their jobs

## Modes

| Mode             | Behavior                                                            |
| ---------------- | ------------------------------------------------------------------- |
| `--bg` (default) | Launch agents, return control to human, resume on notification      |
| `--fg`           | Launch agents, block until complete, continue to next batch         |
| `--auto`         | With `--fg`: skip HIL on nominal; exits to HIL on any failure/NO-GO |

## Rules

@RULES.md

## Phases (Hierarchical)

@lib/setup/PHASE.md
@lib/preflight/PHASE.md
@lib/execution/PHASE.md
@lib/control/PHASE.md

---

## Quick Reference

| Phase         | Sub-phases                                                            | Purpose                        |
| ------------- | --------------------------------------------------------------------- | ------------------------------ |
| **setup**     | INITIALIZE, BOOTSTRAP, DECOMPOSE, HIL_GATE_PLAN_APPROVAL, MATERIALIZE | Initialize and plan work       |
| **preflight** | EVALUATE, HIL_HOLD, FIX                                               | Go/no-go checks before launch  |
| **execution** | DELEGATE, MONITOR, VERIFY                                             | Launch agents, collect results |
| **control**   | HIL_ANOMALY, CHECKPOINT, REPORT, HIL_NEXT_ACTION, HANDOFF             | Handle failures, decide next   |

## Mission Flow (Top Level)

```
┌─────────┐     ┌────────────┐     ┌───────────┐     ┌─────────┐
│  SETUP  │ ──► │ PREFLIGHT  │ ──► │ EXECUTION │ ──► │ CONTROL │
└─────────┘     └────────────┘     └───────────┘     └─────────┘
     │                │                  │                │
     │                │                  │                │
     │           (loop on               (--bg mode       (loop on
     │            NO-GO fix)             returns to       continue)
     │                │                  human)           │
     │                │                  │                │
     └────────────────┴──────────────────┴────────────────┘
                            ▲
                            │
                      (resume points)
```

**Normal flow:** SETUP → PREFLIGHT → EXECUTION → CONTROL → (continue?) → PREFLIGHT...

**Entry points after resume (first match wins):**

- Tasks in-progress → execution/MONITOR
- Ready tasks (pending with empty blockedBy) → preflight/EVALUATE
- Tasks pending but all blocked → control/REPORT
- All tasks completed/ABORTED → control/REPORT
- No tasks + work-related history → setup/BOOTSTRAP
  _(Work-related = action requests, file paths for requested work, or recorded decisions)_
- No tasks + no work-related history → setup/DECOMPOSE

See each phase's PHASE.md for internal flow details.

---

## Task Lifecycle

```
pending --> in_progress --> completed
   ^                   \-> ABORTED - [reason]
   └─── (on Retry)
```

- To abort: update subject to `ABORTED - [reason]`, mark completed
  Example: `TaskUpdate(taskId: X, subject: "ABORTED - reason", status: "completed")`
- Never delete task data; always leave a trail in descriptions/metadata

## Delegation Philosophy

**Default to delegating.** Delegate tasks that involve:

- Writing or editing files
- Running commands to verify something
- Research or exploration
- Any substantive work

**Do directly:**

- Checking if a file exists
- Reading a single line to confirm content
- Other trivial verification checks

**You are the coordinator, not the worker.**

## Anti-patterns

- Doing work yourself that an agent could do
- Trusting agent summaries without verification
- Forgetting to check `TaskList` after compaction
- Creating tasks too large or vague for a single agent
- Sequential execution when parallel is possible
- Losing state by relying on context instead of tasks
- Downgrading agents to cheaper/faster models

---

Begin at setup/INITIALIZE. Follow phase flows. Honor HIL unless `--auto` with all GO.

**Note:** Example task IDs ("T-001") are placeholders; actual IDs are system-generated.
