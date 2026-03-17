---
name: plan
description: Create an interactive implementation plan and task breakdown from PRODUCT.md.
version: 1.1.0
tags: [planning, workflow, tasks]
owner: orchestration
status: active
---

# Plan Skill

Create an implementation plan from PRODUCT.md with interactive task breakdown.

## Overview

This skill creates a task breakdown from PRODUCT.md and gets user approval before proceeding. It's more interactive than `/plan-feature` - designed for human-guided workflow.

## Usage

```
/plan
```

## Prerequisites

- `PRODUCT.md` must exist with feature specification
- Recommended: `CONTEXT.md` from `/discover` phase

## Purpose

**Human-guided planning** - Present the plan for review and modification.

Break down the feature into small, focused tasks that can be:
- Implemented independently (where possible)
- Tested in isolation
- Reviewed incrementally

## Workflow Steps

### Step 1: Read Context

Read these files:
- `PRODUCT.md` - Feature specification (required)
- `CONTEXT.md` - Decisions from discovery (if exists)
- `CLAUDE.md` - Coding standards (if exists)
- Existing codebase structure (if not greenfield)

### Step 2: Analyze Requirements

Extract from PRODUCT.md:
- Feature scope
- Acceptance criteria
- Technical constraints
- Testing requirements
- Definition of done

### Step 3: Create Task Breakdown

Break the feature into tasks following these rules:

**Task Size Limits**:
- Max 5 files to create per task
- Max 8 files to modify per task
- Max 7 acceptance criteria per task
- Target complexity score < 5

**Task Structure**:
```json
{
  "id": "T1",
  "title": "Short descriptive title",
  "description": "What this task accomplishes",
  "user_story": "As a [user], I want [goal], so that [benefit]",
  "acceptance_criteria": [
    "Criterion 1",
    "Criterion 2"
  ],
  "files_to_create": ["path/to/new/file.ts"],
  "files_to_modify": ["path/to/existing/file.ts"],
  "test_files": ["path/to/test.ts"],
  "dependencies": [],
  "estimated_complexity": "low|medium|high"
}
```

### Step 4: Present Plan to User

Show the plan in a readable format:

```markdown
## Implementation Plan

Based on PRODUCT.md, here are the tasks:

### T1: Create user model and database schema
- **Complexity**: Low
- **Creates**: src/models/user.ts, src/db/migrations/001_users.sql
- **Tests**: tests/models/user.test.ts
- **Dependencies**: None

### T2: Implement password hashing service
- **Complexity**: Low
- **Creates**: src/services/password.ts
- **Modifies**: None
- **Tests**: tests/services/password.test.ts
- **Dependencies**: None

### T3: Build authentication endpoints
- **Complexity**: Medium
- **Creates**: src/routes/auth.ts
- **Modifies**: src/routes/index.ts
- **Tests**: tests/routes/auth.test.ts
- **Dependencies**: T1, T2

---

**Total**: 3 tasks
**Estimated Files**: 5 new, 1 modified

Does this plan look correct? Would you like to modify any tasks?
```

### Step 5: Get Approval

Wait for user response:
- **Approve**: Save plan and proceed
- **Modify**: Adjust tasks as requested
- **Split**: Break large tasks into smaller ones
- **Merge**: Combine related tasks
- **Reorder**: Change task sequence

### Step 6: Save Plan

After approval, save to `phase_outputs` (type=plan):

```json
{
  "feature_name": "User Authentication",
  "created_at": "2026-01-22T12:00:00Z",
  "source": "PRODUCT.md",
  "tasks": [
    {
      "id": "T1",
      "title": "...",
      ...
    }
  ],
  "metadata": {
    "total_tasks": 3,
    "files_to_create": 5,
    "files_to_modify": 1,
    "approved_by": "user",
    "approved_at": "2026-01-22T12:05:00Z"
  }
}
```

Update `workflow_state` in SurrealDB:
```json
{
  "current_phase": 2,
  "phase_status": {
    "planning": "completed"
  }
}
```

## Task Decomposition Guidelines

### Good Task Characteristics

- **Focused**: Does one thing well
- **Testable**: Has clear test criteria
- **Independent**: Minimal dependencies
- **Small**: Can be implemented in one session
- **Clear**: Obvious when it's done

### When to Split a Task

- More than 5 files to create
- More than 8 files to modify
- Touches multiple architectural layers
- Multiple distinct features bundled together
- Estimated time > 30 minutes

### When to Merge Tasks

- Trivially small (< 5 minutes)
- Tightly coupled files
- Same test file covers both
- Sequential and can't be parallelized

## Dependency Management

Tasks should list dependencies explicitly:
```json
{
  "id": "T3",
  "dependencies": ["T1", "T2"]
}
```

This ensures:
- T1 and T2 complete before T3 starts
- Clear execution order
- Parallel execution of independent tasks

## Key Behaviors

### DO
- Read PRODUCT.md thoroughly before planning
- Break into small, focused tasks
- Show the plan for user review
- Wait for approval before saving
- Explain rationale for task breakdown
- Identify dependencies clearly

### DON'T
- Auto-proceed without user approval
- Create overly large tasks
- Skip dependency analysis
- Ignore existing codebase structure
- Make assumptions about implementation

## Output Files

| File | Purpose |
|------|---------|
| `phase_outputs` (plan) | Task breakdown and metadata |
| `workflow_state` | Updated workflow state |

## State Update

After plan approval:
- Set `phase_status.planning = "completed"`
- Set `current_phase = 2` (or 3 if skipping validation)
- Store `plan` in state

## Transition

When plan is approved:

```
Plan saved to SurrealDB `phase_outputs` (type=plan)

Summary:
  - {N} tasks created
  - {M} files to create
  - {K} files to modify

Next steps:
  /task T1 - Start implementing the first task
  /status  - View progress anytime

Or for full validation:
  /validate-plan - Run Cursor + Gemini review on the plan
```

## Example Session

```
User: /plan

Claude: I'll create an implementation plan from PRODUCT.md.

Reading PRODUCT.md...

## Implementation Plan

Based on the User Authentication feature, here are the tasks:

### T1: Create user model and database schema
- **Complexity**: Low
- **Creates**: src/models/user.ts, prisma/migrations/001_users.sql
- **Tests**: tests/models/user.test.ts
- **Dependencies**: None
- **Criteria**: User model with id, email, password_hash, created_at

### T2: Implement password hashing service
- **Complexity**: Low
- **Creates**: src/services/password.ts
- **Tests**: tests/services/password.test.ts
- **Dependencies**: None
- **Criteria**: Hash and verify functions using bcrypt

### T3: Create JWT token service
- **Complexity**: Low
- **Creates**: src/services/jwt.ts
- **Tests**: tests/services/jwt.test.ts
- **Dependencies**: None
- **Criteria**: Sign and verify JWT tokens

### T4: Build login endpoint
- **Complexity**: Medium
- **Creates**: src/routes/auth/login.ts
- **Modifies**: src/routes/index.ts
- **Tests**: tests/routes/auth/login.test.ts
- **Dependencies**: T1, T2, T3
- **Criteria**: POST /auth/login, validates credentials, returns JWT

### T5: Build registration endpoint
- **Complexity**: Medium
- **Creates**: src/routes/auth/register.ts
- **Tests**: tests/routes/auth/register.test.ts
- **Dependencies**: T1, T2
- **Criteria**: POST /auth/register, creates user, returns JWT

### T6: Add authentication middleware
- **Complexity**: Low
- **Creates**: src/middleware/auth.ts
- **Tests**: tests/middleware/auth.test.ts
- **Dependencies**: T3
- **Criteria**: Validates JWT, adds user to request

---

**Total**: 6 tasks
**Estimated**: 8 new files, 1 modified
**Parallel opportunities**: T1, T2, T3 can run in parallel

Does this plan look correct? Would you like to:
- Approve as-is
- Split any tasks
- Merge any tasks
- Reorder tasks
- Add/remove tasks

User: Looks good, approve it.

Claude: Plan approved and saved to SurrealDB `phase_outputs` (type=plan)

Summary:
  - 6 tasks created
  - 8 files to create
  - 1 file to modify

Next steps:
  /task T1 - Start with the user model
  /status  - View progress anytime
```

## Outputs

- `phase_outputs` entries for `plan` and `task_breakdown`.

## Error Handling

- If `PRODUCT.md` is missing or invalid, stop and request a valid spec before planning.
- If task complexity is too high, split tasks before seeking approval.

## Related Skills

- `/discover` - Previous step (create PRODUCT.md)
- `/task <id>` - Implement individual tasks
- `/validate-plan` - Run agent validation on plan (optional)
- `/status` - Check progress
