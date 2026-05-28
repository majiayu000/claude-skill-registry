---
name: autonomous-skill
description: >-
  Execute long-running, multi-session tasks autonomously using Claude Code headless mode
  or in-session hook-based loops. Supports structured task decomposition (for complex projects)
  and lightweight Ralph-style iteration (for TDD, bug fixing, refactoring).
  Use this skill whenever the user says "autonomous", "long-running task", "multi-session",
  "run this in the background", "keep working on this", "batch process", "iterate until done",
  "ralph loop", or wants any task that requires sustained, unattended execution.
---

# Autonomous Skill - Multi-Session Task Execution

Execute complex tasks across multiple Claude Code sessions with automatic continuation,
progress tracking, and two completion mechanisms (promise tags + checkbox counting).

## Two Execution Modes

### Headless Mode (default)
Spawns `claude -p` child sessions in a bash loop. Best for background/unattended work.
```bash
bash <skill-dir>/scripts/run-session.sh "Build a REST API" --max-sessions 10
```

### Hook Mode (in-session)
Uses a Stop hook to intercept session exit and feed the prompt back. Runs inside
the current interactive session — no nesting issues.
```bash
bash <skill-dir>/scripts/setup-loop.sh "Build a REST API" --max-iterations 10
```

## Two Task Strategies

### Structured (default)
Full task decomposition: Initializer creates `task_list.md` with phased sub-tasks,
Executor picks up and completes them one by one. Best for complex, multi-phase projects.
```bash
bash <skill-dir>/scripts/run-session.sh "Build a REST API for todo app"
```

### Lightweight (`--lightweight`)
Ralph-style iteration: same prompt repeated each session, no task decomposition.
Best for iterative tasks with clear success criteria (TDD, bug fixing, refactoring).
```bash
bash <skill-dir>/scripts/run-session.sh "Fix all failing tests in src/" --lightweight
```

## Completion Detection

Two complementary mechanisms — whichever triggers first wins:

1. **Promise tags** (both modes): The agent outputs `<promise>DONE</promise>` when
   work is genuinely complete. Default promise is `DONE`; customize with
   `--completion-promise`. The agent is instructed to only output the promise when
   the work is truly finished — not to escape the loop.

2. **Checkbox counting** (structured mode only): All `[ ]` items in `task_list.md`
   are marked `[x]`.

## Directory Layout

```
project-root/
├── .autonomous/
│   └── <task-name>/
│       ├── task_list.md      # Master checklist (structured mode)
│       ├── progress.md       # Per-session progress log
│       ├── .mode             # "structured" or "lightweight"
│       ├── sessions/         # Transcript logs per session
│       │   ├── session-001.log
│       │   └── session-002.log
│       └── run.lock          # Prevents concurrent runs
└── .claude/
    └── autonomous-loop.local.md  # Hook mode state (when active)
```

## Headless Mode — CLI Reference

```bash
bash <skill-dir>/scripts/run-session.sh "task description" [OPTIONS]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--lightweight` | Ralph-style iteration (no task decomposition) | structured |
| `--task-name <name>` | Explicit task name | Auto-generated |
| `--continue, -c` | Continue most recent or named task | — |
| `--list, -l` | List all tasks with progress | — |
| `--completion-promise TEXT` | Promise phrase for completion | DONE |
| `--max-sessions N` | Stop after N sessions | Unlimited |
| `--max-budget N.NN` | Per-session dollar budget | 5.00 |
| `--model <model>` | Model alias or full name | sonnet |
| `--fallback-model <m>` | Fallback if primary overloaded | — |
| `--effort <level>` | Thinking effort (low/medium/high) | high |
| `--no-auto-continue` | Run one session only | — |
| `--permission-mode <m>` | Permission mode | auto |
| `--add-dir <dirs>` | Extra directories to allow | — |

## Hook Mode — Setup

For in-session loops (no child process spawning):

```bash
bash <skill-dir>/scripts/setup-loop.sh "task description" [OPTIONS]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--mode structured\|lightweight` | Task strategy | structured |
| `--max-iterations N` | Max loop iterations | Unlimited |
| `--completion-promise TEXT` | Promise phrase | DONE |
| `--task-name NAME` | Explicit task name | Auto-generated |

The hook is registered in `hooks/hooks.json`. When active, the Stop hook reads
`.claude/autonomous-loop.local.md` and blocks exit until the promise is detected
or max iterations reached.

To cancel an active hook-mode loop: `rm .claude/autonomous-loop.local.md`

## Workflow Detail

### Structured Mode

1. **Initializer Agent** — analyzes task, creates phased `task_list.md`, begins work
2. **Executor Agent** — reads task list + progress, verifies previous work, completes next task
3. **Auto-Continue** — checks promise tags + checkboxes; if not done, spawns next session

### Lightweight Mode

1. Same prompt fed each iteration
2. Agent sees its previous work in files and git history
3. Iterates until work is complete and promise tag is output
4. No task_list.md — completion is purely promise-based

### When to Use Which

| Scenario | Strategy | Mode |
|----------|----------|------|
| Build a full application | Structured | Headless |
| Fix all failing tests | Lightweight | Either |
| Refactor a module | Lightweight | Either |
| Multi-phase project | Structured | Headless |
| Quick iterative fix | Lightweight | Hook |
| Overnight batch work | Structured | Headless |

## Important Constraints

1. **task_list.md is append-only for completions**: Only change `[ ]` → `[x]`
2. **One runner per task**: Lock file prevents concurrent sessions on same task
3. **Project files stay in project root**: `.autonomous/` is only for tracking
4. **Promise integrity**: The agent must not output `<promise>DONE</promise>` until genuinely complete
5. **Cost awareness**: Default per-session budget is $5. Adjust with `--max-budget`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Lock file exists" | Previous run crashed. Remove `.autonomous/<task>/run.lock` |
| Session keeps failing | Check `sessions/session-NNN.log` for errors |
| Nested session error | Script auto-unsets CLAUDECODE; use hook mode as alternative |
| Hook loop won't stop | Delete `.claude/autonomous-loop.local.md` |
| Task not found | Run `--list` to see available tasks |
| Want to restart | Delete the task directory and start fresh |
| Cost too high | Lower `--max-budget` or use `--model sonnet` |
