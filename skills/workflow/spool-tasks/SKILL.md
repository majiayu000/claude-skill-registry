---
name: spool-tasks
description: Use Spool tasks CLI to manage tasks.md (status/next/start/complete/shelve/add).
---

Use the `spool tasks` CLI to track and update implementation tasks for a change.

**Rules**

- Prefer `spool tasks ...` over manual editing of `tasks.md`.
- Enhanced tasks.md supports `start`, `shelve`, `unshelve`, and `add`.
- Checkbox-only tasks.md is supported in compat mode (supports in-progress via `[~]` / `spool tasks start`, but no shelving); start/complete tasks by 1-based index.

**Common Commands**

```bash
spool tasks status <change-id>
spool tasks next <change-id>
spool tasks ready                               # Show ready tasks across ALL changes
spool tasks ready <change-id>                   # Show ready tasks for a specific change
spool tasks ready --json                        # JSON output for automation
spool tasks start <change-id> <task-id>
spool tasks complete <change-id> <task-id>
spool tasks complete <change-id> <index>
spool tasks shelve <change-id> <task-id>
spool tasks unshelve <change-id> <task-id>
spool tasks add <change-id> "<task name>" --wave <n>
spool tasks show <change-id>
```

**If tasks.md is missing**

- Create enhanced tracking file: `spool tasks init <change-id>`

**If the user asks "what should I do next?"**

- If working on a specific change: Run `spool tasks next <change-id>`
- If looking for any ready work: Run `spool tasks ready` to see all actionable tasks
- Follow the printed Action/Verify/Done When for the chosen task.

**Guardrails**

- If a task is blocked, run `spool tasks status <change-id>` and either resolve blockers or shelve the task (enhanced only).
- If `spool tasks shelve` fails because the file is checkbox-only, explain that checkbox compat mode does not support shelving.
- If `spool tasks start` fails in compat mode, it is usually because the task id is not a 1-based index, or another task is already in-progress.
