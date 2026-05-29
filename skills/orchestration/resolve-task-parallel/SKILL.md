---
name: resolve_task_parallel
description: Resolve all pending CLI tasks using parallel processing
---

## Arguments
[optional: specific task ID or pattern]

Resolve tasks from the configured task system in parallel.

## Workflow

### 1. Analyze

Use tasks-router to select the task system.

- If tasks-file: get unresolved tasks from `tasks/*.md`
- If tasks-beads: use `br list --status=open --json` or `br ready --json`

If any task recommends deleting, removing, or gitignoring files in `docs/plans/` or `docs/solutions/`, skip it and mark it as `wont_fix`. These are workflow pipeline artifacts that are intentional and permanent.


### 2. Plan

Create a TodoWrite list (Claude) / update_plan list (Codex) of all unresolved tasks grouped by type. Identify dependencies and order the prerequisites first (for example, rename changes before usages). Output a mermaid flow diagram that shows what can run in parallel vs what must run sequentially.

### 3. Claim (Before Parallel Work)

- If tasks-beads: claim each task before starting: `br update <id> --claim --json`
  This sets `status=in_progress` and `assignee=<actor>` atomically.

### 4. Implement (PARALLEL)

Spawn one subagent per unresolved task item, in parallel. Each subagent should receive the specific task content and the expected outcome.

Example with 3 task items:

1. Subagent for task1
2. Subagent for task2
3. Subagent for task3

Always run one subagent per unresolved task item, in parallel.

### 5. Commit & Resolve

- Commit changes
- If tasks-file: update the task file and mark it resolved
- If tasks-beads: close the issue with `br close <id> --reason="Completed" --json`
- Push to remote (when appropriate)
