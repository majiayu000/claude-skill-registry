---
name: status
description: Show current workflow progress at a glance.
version: 1.1.0
tags: [status, workflow, summary]
owner: orchestration
status: active
---

# Status Skill

Show current workflow progress at a glance.

## Overview

A simple status check showing:
- Current phase
- Task progress (completed/total)
- Any blockers
- Next recommended action

## Usage

```
/status
```

## Prerequisites

- SurrealDB connection configured for the project namespace.

## Purpose

**Quick progress check** - See where you are and what's next.

This is the go-to command for:
- Resuming work after a break
- Checking progress mid-workflow
- Deciding what to do next

## State Sources

Check these sources:
- `workflow_state` in SurrealDB - Overall workflow state
- `phase_outputs` in SurrealDB - Task breakdown and validation/verification

## Status Display

### Minimal (No Workflow Started)

```
## Project Status

No workflow started yet.

Quick start:
  /discover - Explore the project and create PRODUCT.md
  /plan     - Create task breakdown (requires PRODUCT.md)
```

### With Active Workflow

```
## Project Status

### Current Phase: Implementation

### Progress
| Phase | Status |
|-------|--------|
| Discovery | completed |
| Planning | completed |
| Validation | skipped |
| Implementation | in_progress (3/6 tasks) |
| Verification | pending |
| Completion | pending |

### Task Progress

Completed: 3/6 (50%)

| Task | Title | Status |
|------|-------|--------|
| T1 | Create user model | completed |
| T2 | Password hashing service | completed |
| T3 | JWT token service | completed |
| T4 | Login endpoint | in_progress |
| T5 | Registration endpoint | pending |
| T6 | Auth middleware | pending |

### Next Action

Continue with: /task T4

Or: /status -v for detailed view
```

### With Blockers

```
## Project Status

### Current Phase: Implementation (BLOCKED)

### Blocker
Task T3 failed after 3 attempts:
  Error: Cannot find module '@prisma/client'

Suggested fix:
  Run: npm install @prisma/client

### Progress
Completed: 2/6 tasks (33%)

### Next Action
Fix the blocker, then: /task T3
```

## Status Levels

### Quick Status (default)
Shows:
- Current phase
- Task progress bar
- Next action

### Detailed Status (`/status -v`)
Shows:
- Full phase breakdown
- All task details
- Recent feedback scores
- Error history
- File changes

## Reading State

```python
# Pseudocode
if not workflow_state_exists():
    show "No workflow started"
    return

state = workflow_state_repo.get(project)
plan = phase_outputs_repo.get_by_type(phase=1, output_type="plan")

current_phase = state.get("current_phase", 0)
phase_status = state.get("phase_status", {})
tasks = state.get("tasks", [])  # task statuses tracked in state
errors = state.get("errors", [])
```

## Phase Mapping

| Phase | Name | Next Skill |
|-------|------|------------|
| 0 | Discovery | `/discover` |
| 1 | Planning | `/plan` |
| 2 | Validation | `/validate-plan` |
| 3 | Implementation | `/task <id>` |
| 4 | Verification | `/verify-code` |
| 5 | Completion | (done) |

## Task Status Summary

Calculate and display:
```
Total: {total}
Completed: {completed} ({percentage}%)
In Progress: {in_progress}
Pending: {pending}
Blocked: {blocked}
Failed: {failed}
```

## Next Action Logic

Determine recommended action based on state:

```python
if no_workflow:
    if exists("PRODUCT.md"):
        suggest "/plan"
    else:
        suggest "/discover"
elif phase == "implementation":
    next_task = find_next_pending_task()
    if next_task:
        suggest f"/task {next_task.id}"
    else:
        suggest "/verify"
elif phase == "blocked":
    show blocker and fix suggestion
else:
    suggest next phase command
```

## Example Output: Fresh Project

```
User: /status

Claude: ## Project Status

No workflow started.

Found:
  - Documents/ folder with 3 files
  - No PRODUCT.md

Suggested: /discover to read documents and create PRODUCT.md
```

## Example Output: Mid-Workflow

```
User: /status

Claude: ## Project Status

### Current Phase: Implementation

### Progress

[====================----------] 50%

Completed: 3/6 tasks

| Task | Title | Status |
|------|-------|--------|
| T1 | User model | done |
| T2 | Password service | done |
| T3 | JWT service | done |
| T4 | Login endpoint | pending |
| T5 | Register endpoint | pending |
| T6 | Auth middleware | pending |

### Next

Continue with: /task T4
```

## Example Output: Completed

```
User: /status

Claude: ## Project Status

### Workflow Complete!

All 6 tasks implemented and verified.

### Summary
- Files created: 8
- Files modified: 2
- Tests: 24 passing
- Review scores: Cursor 8.5, Gemini 8.0

### Artifacts
- phase_outputs: summary
- logs: uat_document

Ready to commit? The changes are in your working directory.
```

## Outputs

- Quick or detailed status report for the current project.

## Error Handling

- If SurrealDB is unreachable, show a degraded report and warn about missing data.

## Related Skills

- `/discover` - Start discovery phase
- `/plan` - Create task breakdown
- `/task <id>` - Implement a task
- `/verify` - Run code review
- `/orchestrate` - Full automated workflow
