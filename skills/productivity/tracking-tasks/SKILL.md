---
name: tracking-tasks
description: Enforces disciplined task tracking across context boundaries. Use when starting any coding task, receiving a new user request mid-work, planning multi-step work, discovering sub-tasks or issues, before context compaction, switching between tasks, or resuming a previous session. Skip for purely informational questions with no code changes.
---

# Tracking Tasks

## Overview

**Every action must be tracked.** The task list is your memory across context boundaries. No mental notes. No exceptions. If it's not written down, it will be lost at the next compaction.

Use `TaskCreate` to create tasks, `TaskUpdate` to change status, `TaskList` to review all tasks.

## Core Rules

### RULE 1: Track Before Acting

```
NEVER start work without creating a task first.
"I'll just quickly..." → CREATE TASK FIRST
```

### RULE 2: Never Delete

```
NEVER delete tasks. EVER.

Done?        → Mark completed
Not needed?  → Mark completed + note why
Wrong?       → Mark completed + create corrected task
```

Deleted tasks lose history. Completed tasks preserve context for future sessions.

### RULE 3: One In-Progress at a Time

```
Maximum ONE task as in_progress at any time.
Starting new work? Complete or pause current first.
```

### RULE 4: Deviation Protocol

When you discover something unexpected while working:

```
1. KEEP current task as in_progress
2. CREATE new task (pending) for the discovery
3. Note in description: "Discovered while working on #N"
4. DECIDE: handle now (switch in_progress) or defer
5. RETURN to original task when done
```

This includes when the user asks for something new mid-task — don't drop the current task. Track the new request, decide priority, and proceed.

### RULE 5: Pre-Compaction Checkpoint

Before context compaction:

```
1. ALL discovered work captured as tasks
2. Current task status accurate
3. Blocked tasks have reason noted in description
4. NO mental notes — everything tracked
```

## Task Lifecycle

```
pending ──→ in_progress ──→ completed
```

There is no separate "blocked" status. Keep blocked tasks as `pending` and note the blocker in the description.

## Resuming a Session

When continuing work after compaction or in a new session:

1. Run `TaskList` to see all existing tasks
2. If no tasks exist (first session), create initial tasks from user request
3. Review `in_progress` and `pending` tasks — are statuses still accurate?
4. Update any stale statuses
5. Resume the highest-priority `pending` task or continue the `in_progress` one
6. If all tasks are completed, report to user and await new instructions

## Red Flags — STOP

| Thought | Action |
|---------|--------|
| "I'll just quickly fix this" | CREATE TASK FIRST |
| "This is too small to track" | CREATE TASK ANYWAY |
| "I'll remember to come back" | CREATE TASK NOW |
| "Let me clean up old tasks" | NEVER DELETE |
| "I have two things in progress" | PAUSE ONE |
| "I'll batch-add tasks later" | ADD EACH AS DISCOVERED |
| "User asked something new, let me just do it" | CREATE TASK, THEN DECIDE PRIORITY |

## Anti-Patterns

**Batching discoveries:** Add each task as discovered, not in batches later. Waiting means forgetting.

**Vague descriptions:** "Fix bug" vs "Fix null pointer in UserService.getById at line 45"
