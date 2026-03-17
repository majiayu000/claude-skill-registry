---
name: task
description: Implement a single task by ID using TDD.
version: 1.1.0
tags: [implementation, tdd, tasks]
owner: orchestration
status: active
---

# Task Skill

Implement a single task by ID using TDD.

## Overview

This skill implements one task from the plan. It:
1. Shows the task scope to the user
2. Confirms before starting
3. Implements with TDD (tests first)
4. Reports completion status
5. Updates task status in state

## Usage

```
/task T1
/task T1-a
```

## Prerequisites

- Plan exists in `phase_outputs` (type=plan)
- Task ID exists in the plan
- Dependencies are completed

## Purpose

**Focused implementation** - One task at a time with clear boundaries.

By working task-by-task:
- Progress is visible
- Errors are localized
- Rollback is simple
- Review is focused

## Workflow Steps

### Step 1: Load Task

Read the plan from `phase_outputs` and find the task:

```json
{
  "id": "T1",
  "title": "Create user model and database schema",
  "description": "...",
  "acceptance_criteria": [...],
  "files_to_create": [...],
  "files_to_modify": [...],
  "test_files": [...],
  "dependencies": [...],
  "status": "pending"
}
```

### Step 2: Check Dependencies

Verify all dependencies are completed:
```
Dependencies: T1, T2
  T1: completed
  T2: completed
Ready to proceed.
```

If dependencies are incomplete:
```
Cannot start T3 - dependencies not met:
  T1: completed
  T2: pending  <- Not done

Run /task T2 first, or use /status to see progress.
```

### Step 3: Show Task Scope

Present the task details to the user:

```markdown
## Task T1: Create user model and database schema

### Description
Create the User model with TypeScript types and database migration.

### Acceptance Criteria
- [ ] User model with id, email, password_hash, created_at
- [ ] Email must be unique
- [ ] Database migration for users table

### Files to Create
- src/models/user.ts
- prisma/migrations/001_users.sql

### Files to Modify
- (none)

### Test Files
- tests/models/user.test.ts

### Ready to implement?
```

### Step 4: Confirm Start

Wait for user confirmation before implementing.

If user confirms, proceed. If not, wait for instructions.

### Step 5: Implement with TDD

Use the Task tool to spawn a worker for implementation:

```
Task(
  subagent_type="general-purpose",
  prompt="""
  ## Task: {task.title}

  ## Acceptance Criteria
  {criteria_list}

  ## Files to Create
  {files_to_create}

  ## Files to Modify
  {files_to_modify}

  ## Test Files
  {test_files}

  ## Instructions

  1. Read CLAUDE.md for coding standards
  2. Write failing tests FIRST:
     - Create test file
     - Write tests for each acceptance criterion
     - Run tests (should fail)
  3. Implement code:
     - Create/modify source files
     - Write minimal code to pass tests
     - Run tests (should pass)
  4. Refactor if needed (keep tests green)
  5. Final verification:
     - All tests pass
     - No lint errors
     - Code follows CLAUDE.md standards

  ## Constraints
  - ONLY modify files listed above
  - Follow existing code patterns
  - No security vulnerabilities
  - Do NOT add features beyond acceptance criteria

  Signal completion with: TASK_COMPLETE
  """,
  run_in_background=false
)
```

### Step 6: Verify Completion

After worker completes:
1. Run tests to confirm they pass
2. Check all files were created/modified
3. Verify acceptance criteria met

### Step 7: Report Status

Show completion report:

```markdown
## Task T1 Complete

### Files Created
- src/models/user.ts (45 lines)
- prisma/migrations/001_users.sql (23 lines)

### Files Modified
- (none)

### Tests
- tests/models/user.test.ts
  - 4 tests passing

### Acceptance Criteria
- [x] User model with id, email, password_hash, created_at
- [x] Email must be unique
- [x] Database migration for users table

---

Next: /task T2 or /status to see progress
```

### Step 8: Update State

Update `workflow_state` in SurrealDB:
```json
{
  "current_task_id": null,
  "tasks_completed": 1,
  "tasks_total": 6
}
```

## Error Handling

### Test Failures

If tests fail after implementation:
1. Show failing test output
2. Ask user how to proceed:
   - Fix the issues (retry implementation)
   - Skip for now (mark as blocked)
   - Modify acceptance criteria

### Implementation Errors

If worker encounters errors:
1. Show error context
2. Suggest possible fixes
3. Offer to retry with different approach

### Dependency Failures

If a dependency task failed:
1. Show dependency status
2. Suggest fixing dependency first
3. Offer to skip if acceptable

## Key Behaviors

### DO
- Show task scope before starting
- Wait for confirmation
- Use TDD (tests first)
- Report clear completion status
- Update state after completion
- Check dependencies before starting

### DON'T
- Start without confirmation
- Skip writing tests
- Modify files outside task scope
- Add features beyond acceptance criteria
- Leave task in indeterminate state

## Task States

| State | Meaning |
|-------|---------|
| `pending` | Not started |
| `in_progress` | Currently being implemented |
| `completed` | Successfully finished |
| `blocked` | Cannot proceed (dependency/error) |
| `failed` | Failed after max retries |

## Outputs

Task implementation updates:
- Source files in `src/` or equivalent
- Test files in `tests/` or equivalent
- `workflow_state` updates in SurrealDB (task status / overall progress)

## Transition

After task completion:

```
Task T1 complete!

Progress: 1/6 tasks (17%)

Next steps:
  /task T2 - Continue to next task
  /status  - View full progress

Or for code review:
  /verify-code  - Run Cursor + Gemini review
```

## Example Session

```
User: /task T1

Claude: ## Task T1: Create user model and database schema

### Description
Create the User model with TypeScript types and database migration.

### Acceptance Criteria
- [ ] User model with id, email, password_hash, created_at
- [ ] Email must be unique
- [ ] Database migration for users table

### Files to Create
- src/models/user.ts
- prisma/migrations/001_users.sql

### Test Files
- tests/models/user.test.ts

Ready to implement?

User: Yes, go ahead.

Claude: Starting implementation with TDD...

[Worker implements the task]

## Task T1 Complete

### Files Created
- src/models/user.ts (45 lines)
- prisma/migrations/001_users.sql (23 lines)

### Tests
- tests/models/user.test.ts: 4 tests passing

### Acceptance Criteria
- [x] User model with id, email, password_hash, created_at
- [x] Email must be unique
- [x] Database migration for users table

---

Progress: 1/6 tasks (17%)

Next: /task T2 or /status
```

## Parallel Tasks

If multiple tasks have no dependencies, you can suggest parallel execution:

```
Tasks T1, T2, T3 have no dependencies and can run in parallel.

Would you like to:
1. Run them sequentially (/task T1, then T2, then T3)
2. Run them in parallel (experimental)

Sequential is safer. Parallel is faster but may have merge conflicts.
```

## Related Skills

- `/plan` - Create the task breakdown
- `/status` - View progress
- `/verify-code` - Run code review on completed tasks
- `/discover` - Go back to discovery if requirements unclear
