---
name: decompose-plan
description: Use when starting plan execution to decompose implementation plans into Claude Code Task tool tasks at H2 (Task) granularity - creates one task per plan task with citation-manager directives, keeping plan as source of truth
---

# Decompose Plan into Tasks

## Overview

Parse implementation plan and create one Task tool task per H2 Task header. Tasks reference plan via citation-manager, keeping plan authoritative.

**Core principle:** Plan is source of truth. Tasks are pointers, not copies.

**Announce at start:** "I'm using the decompose-plan skill to create tasks from this plan."

## When to Use

- Before executing any implementation plan
- When `/executing-plans` or similar workflow starts
- When plan has `## Task N` structure with `### Step` sub-headers

## The Process

### Step 1: Parse Plan Structure

Use citation-manager to extract H2 headers (Tasks):

```bash
citation-manager extract header "{plan_path}" "Task 1"
```

Each `## Task N` becomes one Claude Code Task.

### Step 2: Create One Task Per H2

For EACH `## Task N` header, create a Task tool task:

```typescript
TaskCreate({
  subject: "Task {N}: {task_title}",
  description: `Fetch task details:\n\`citation-manager extract header "${plan_path}" "Task {N} - {task_title}"\`\n\nPlan: ${plan_path}`,
  activeForm: "{task_title}"
})
```

### Step 3: Set Dependencies

- Task N+1 blocked by Task N (linear chain)
- If plan specifies non-linear dependencies, follow plan

## Task Description Template

```markdown
Fetch task details:
`citation-manager extract header "{plan_path}" "Task N - {task_title}"`

Plan: {plan_path}
```

**Why citation directive:** Plan may be updated. Task fetches current content at execution time.

## Granularity Rules

| Level | What to Create | Example |
|-------|---------------|---------|
| `## Task N` | ONE Task | Unit of work with steps inside |
| `### Step N` | Part of parent Task | Executed within Task, not split |
| `#### Sub-step` | Part of parent Step | Don't split further |

## Common Rationalizations (STOP These)

| Excuse | Reality |
|--------|---------|
| "I'll split into steps" | Steps execute within their Task. One Task per H2. |
| "I'll copy content inline" | Copies go stale. Citation directive fetches current content. |
| "Citation adds overhead" | One command. Guarantees current content. Worth it. |
| "I need fewer tasks" | One per H2 is the right granularity. Don't merge Tasks. |

## Red Flags - You're About to Violate

- Creating 22 tasks for a plan with 6 Tasks (too granular)
- Merging multiple `## Task` into one task (too coarse)
- Copying task content into descriptions
- Ignoring dependency chain

## Example Output

For a plan with 6 Tasks:

```text
Task #1: Task 1: Create shared library lib/status-helpers.sh
Task #2: Task 2: Refactor task-status-sync.sh to use library  (blockedBy: #1)
Task #3: Task 3: Refactor stop-sync.sh to use library         (blockedBy: #2)
Task #4: Task 4: Enhance plan-path-sync.sh for multi-plan     (blockedBy: #3)
Task #5: Task 5: Create /set-plan slash command                (blockedBy: #4)
Task #6: Task 6: Verification                                 (blockedBy: #5)
```

## Verification

After decomposition, verify:

```bash
# Count tasks created
ls ~/.claude/tasks/{session_id}/*.json | wc -l
# Should match number of H2 Task headers in plan
```

## Quick Reference

| Input | Output |
|-------|--------|
| Plan with 6 `## Task` | 6 tasks |
| Each task description | Citation directive to plan |
| Dependencies | Task-to-task chain |
