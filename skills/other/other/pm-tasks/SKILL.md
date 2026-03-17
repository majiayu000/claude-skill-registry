---
name: pm-tasks
description: Manage the ops/tasks.md task stack — add, complete, stall, or clear tasks. Tasks are explicit coordination TODOs separate from the processing queue. Use for tracking multi-session coordination work that doesn't fit in the pipeline. Triggers on "/pm-tasks", "add task", "show tasks", "complete task", "task list".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: show current task list
- If "add [task description]": add new task
- If "complete [task name]": mark task complete
- If "stall [task name] [reason]": mark as stalled with reason
- If "clear": remove all completed tasks

**START NOW.**

---

## Philosophy

**The task stack prevents important coordination work from disappearing between sessions.**

The processing pipeline (queue.json) tracks source material moving through /pm-document → /pm-link → /pm-update. But some coordination tasks don't fit that pipeline — they are open-ended research, multi-session investigations, or explicit commitments made during sprint planning.

ops/tasks.md is the PM's personal task list. It is not a project management system — it is a session-to-session memory for things that need explicit tracking. It is read during the Orient phase every session.

Tasks should be specific enough to be actionable and time-bounded enough to not live forever on the list. A task that stays stalled for 3+ sessions should either be escalated or abandoned.

---

## Task Format

```markdown
## Active Tasks

### [Task Title]
- Added: YYYY-MM-DD
- Status: active | stalled | complete
- Stall reason: [if stalled]
- Context: [1-2 sentences]
- Next action: [specific next step]

---
```

---

## Workflow

### Show Current Tasks

Read ops/tasks.md and display all active and stalled tasks.

```bash
cat ops/tasks.md
```

### Add Task

Append a new task entry to ops/tasks.md with today's date.

### Complete Task

Update the task's status to `complete`. When running "clear", remove all completed tasks.

### Stall Task

Update the task's status to `stalled` and add the stall reason. Stalled tasks remain visible — they are not removed, because a stall reason is itself valuable information.

---

## Output Format

```
## Task Stack — YYYY-MM-DD

### Active (N)
1. [Task A] — added YYYY-MM-DD — Next: [action]
2. [Task B] — added YYYY-MM-DD — Next: [action]

### Stalled (N)
1. [Task C] — stalled YYYY-MM-DD — Reason: [why stalled]

### Recently Completed (N)
1. [Task D] — completed YYYY-MM-DD

---
Action taken: [added / completed / stalled / showed]
```

---

## Task Lifecycle Rules

- Tasks created here should not duplicate queue.json entries
- If a task is "process sprint N output", it belongs in the queue, not here
- Tasks here are coordination commitments: "investigate SA-3 root cause", "confirm QF-1A is truly resolved", "migrate KNOWN_ISSUES.md to decision notes"
- A task that has been stalled for 3+ sessions should be flagged in /pm-next as a priority
- Completed tasks may be cleared to keep the list focused; archive in ops/sessions/ if the completion has context worth preserving
