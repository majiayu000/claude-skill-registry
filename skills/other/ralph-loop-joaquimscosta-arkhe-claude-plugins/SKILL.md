---
name: ralph-loop
description: Execute an autonomous development loop that picks one task per iteration, implements it, verifies it, and commits the result — each iteration in a fresh context window. Use when user runs /ralph, mentions "ralph loop", "autonomous loop", "builder verifier", "run tasks automatically", "iterate on tasks", "develop autonomously", or wants an automated build-verify-commit cycle with task tracking.
---

# Ralph Loop Execution Protocol

Autonomous development with fresh context per iteration and Hat-lite builder/verifier workflow.

## Quick Start

```bash
# From project directory (after /create-prd)
./ralph.sh 20          # Run up to 20 iterations
./ralph.sh 5           # Quick test with 5 iterations
```

## How It Works

Each iteration runs in a **fresh context window**:

```
┌─────────────────────────────────────────────────────┐
│ ITERATION (Fresh Context)                           │
├─────────────────────────────────────────────────────┤
│ 1. ORIENT: Read activity.log + tasks.json + memories│
│ 2. BUILD:  Pick ONE task, implement, verify        │
│ 3. VERIFY: Review, update status, commit           │
│ 4. LEARN:  (Optional) Save insights to memories    │
│ 5. DECIDE: All done? → RALPH_COMPLETE              │
└─────────────────────────────────────────────────────┘
```

## Hat-Lite System

| Role | When | Responsibility |
|------|------|----------------|
| **Builder** | ~65% of iteration | Implement ONE task |
| **Verifier** | ~35% of iteration | Review, update, commit |

## Key Files

| File | Purpose |
|------|---------|
| `.ralph/current-taskset/tasks.json` | Task state (source of truth) |
| `.ralph/current-taskset/activity.log` | Iteration history |
| `.ralph/current-taskset/memories.md` | Persistent learnings |
| `.ralph/current-taskset` | Symlink to active task set |
| `PROMPT.md` | Instructions per iteration |
| `ralph.sh` | Loop runner script |

## Task JSON Format

Tasks are stored in `.ralph/current-taskset/tasks.json`:

```json
{
  "tasks": [
    {
      "id": "setup-001",
      "description": "Initialize project",
      "verificationTier": "build",
      "passes": false,
      "iteration_completed": null
    }
  ]
}
```

Valid `verificationTier` values: `"build"` (default), `"visual"`, `"api"`, `"e2e"`. See [WORKFLOW.md](WORKFLOW.md) for details.

## Completion Signal

When all tasks pass, output:

```
RALPH_COMPLETE: All tasks verified
```

## Commands

Subcommands: `/ralph run [N]`, `/ralph status`, `/ralph init`, `/ralph taskset <new|list|switch|delete>`, `/ralph add-task`, `/ralph remember`, `/ralph memories`.

## Workflow Details

See [WORKFLOW.md](WORKFLOW.md) for the 5-phase iteration lifecycle (Orient, Build, Verify, Learn, Decide) and Hat-Lite role definitions.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for web app, API, resumption, and mid-loop status checking scenarios.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for immediate exit, premature completion, infinite loop, and context issues.
