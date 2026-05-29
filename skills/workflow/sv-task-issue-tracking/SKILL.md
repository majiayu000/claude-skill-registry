---
name: sv-issue-tracking
description: Use sv task to manage work items and keep .tasks/ in sync with code changes.
---

Use `sv task` for issue tracking in this repo.

- List ready work with `sv task ready` or `sv task list --status open`.
- View details with `sv task show <id>`.
- Mark work in progress with `sv task start <id>`.
- Close work with `sv task close <id>`.
- Tasks live in `.tasks/tasks.jsonl` (tracked) and should be committed with related code changes.

Reference: `references/sv-task-quickref.md`.
