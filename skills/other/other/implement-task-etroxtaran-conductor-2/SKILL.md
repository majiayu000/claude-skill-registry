---
name: implement-task
description: Implement individual tasks using Task tool workers with TDD.
version: 1.1.0
tags: [implementation, tdd, tasks]
owner: orchestration
status: active
---

# Implement Task Skill

Implement individual tasks using Task tool worker with TDD.

## Overview

This skill handles Phase 3 (Implementation) by spawning worker Claude instances via the Task tool. Each task is implemented using Test-Driven Development (TDD).

## Token Efficiency

| Method | Token Cost |
|--------|-----------|
| Old (subprocess spawn) | ~13,000 tokens overhead |
| New (Task tool) | ~4,000 tokens overhead |
| **Savings per task** | **~70%** |

For a project with 10 tasks: 90,000 tokens saved!

## Task Selection

Before implementing, select the next task:

1. Read plan from `phase_outputs` (type=plan)
2. Read `workflow_state` for task statuses
3. Find tasks where:
   - `status` is "pending" or "in_progress"
   - All `dependencies` are "completed"
4. Prioritize by: `priority` > `estimated_complexity` (low first)

## Task Tool Invocation

For each task, spawn a worker:

```
Task(
  subagent_type="general-purpose",
  prompt="""
  # Implementation Task: {task.id} - {task.title}

  ## Your Role
  You are a senior developer implementing this task using TDD.

  ## Context Files to Read First
  1. CLAUDE.md - Coding standards and guidelines
  2. CONTEXT.md - Developer preferences (if exists)
  3. Existing code in files you'll modify

  ## Task Details

  ### User Story
  {task.user_story}

  ### Acceptance Criteria
  {task.acceptance_criteria - as checklist}

  ### Files to Create
  {task.files_to_create}

  ### Files to Modify
  {task.files_to_modify}

  ### Test Files
  {task.test_files}

  ## TDD Process (MANDATORY)

  1. **Write Failing Tests First**
     - Create test file(s) listed above
     - Write tests for ALL acceptance criteria
     - Run tests - they MUST fail initially

  2. **Implement Code**
     - Write minimal code to pass tests
     - Follow patterns in existing codebase
     - Respect CLAUDE.md guidelines

  3. **Verify Tests Pass**
     - Run: pytest {test_files} or npm test
     - ALL tests must pass
     - Fix any failures before proceeding

  4. **Refactor if Needed**
     - Clean up code while keeping tests green
     - No new functionality during refactor

  ## Constraints

  - ONLY modify files listed above
  - Follow existing code patterns and style
  - No security vulnerabilities (validate inputs, escape outputs)
  - No hardcoded secrets or credentials
  - Proper error handling
  - Meaningful variable/function names

  ## Completion Signal

  When done, output:

  TASK_COMPLETE
  {
    "task_id": "{task.id}",
    "status": "completed",
    "tests_passed": true,
    "files_created": [...],
    "files_modified": [...],
    "test_results": "X passed, 0 failed"
  }

  If blocked, output:

  TASK_BLOCKED
  {
    "task_id": "{task.id}",
    "reason": "Why blocked",
    "needs": "What's needed to unblock"
  }
  """,
  run_in_background=false
)
```

## Ralph Wiggum Loop (Iterative TDD)

For complex tasks, use iterative execution:

```
MAX_ITERATIONS = 5

for iteration in 1..MAX_ITERATIONS:
  1. Spawn worker with task prompt
  2. Check for TASK_COMPLETE signal
  3. If complete: break
  4. If tests fail:
     - Extract error message
     - Create retry prompt with error context
     - Continue to next iteration
  5. If blocked:
     - Log block reason
     - Escalate to human
     - break
```

### Retry Prompt Enhancement

On retry, include previous error:

```
## Previous Attempt Failed

Error from last attempt:
{error_message}

Test output:
{test_output}

Please fix the issue and ensure all tests pass.
```

## State Updates

### During Implementation

Update task status in `workflow_state`:

```json
{
  "tasks": [
    {
      "id": "T1",
      "status": "in_progress",
      "attempts": 1,
      "started_at": "2026-01-22T12:00:00Z"
    }
  ],
  "current_task_id": "T1"
}
```

### On Task Completion

```json
{
  "tasks": [
    {
      "id": "T1",
      "status": "completed",
      "attempts": 1,
      "completed_at": "2026-01-22T12:05:00Z",
      "test_results": {
        "passed": 5,
        "failed": 0
      }
    }
  ],
  "current_task_id": null
}
```

### On All Tasks Complete

```json
{
  "current_phase": 4,
  "phase_status": {
    "implementation": "completed",
    "verification": "in_progress"
  }
}
```

## Parallel Implementation (Optional)

For independent tasks (no shared dependencies), spawn multiple workers:

```
# Tasks T3, T4, T5 have no dependencies on each other
# Spawn all three in parallel:

Task(prompt="Implement T3...", run_in_background=true)
Task(prompt="Implement T4...", run_in_background=true)
Task(prompt="Implement T5...", run_in_background=true)

# Wait for all to complete
# Merge results
```

**Caution**: Only parallelize if tasks don't modify the same files!

## Error Handling

### Test Failures

1. Capture test output
2. Include in retry prompt
3. Max 3 retries per task
4. If still failing: Mark as blocked

### Worker Timeout

- Default: 600 seconds per task
- On timeout: Retry with 900 seconds
- If still times out: Mark as blocked

### Blocked Task

1. Log block reason
2. Check if dependencies can be reordered
3. If truly blocked: Escalate to human

## Outputs

| File | Purpose |
|------|---------|
| `phase_outputs` (type=task_result) | Task completion record |
| `logs` (type=implementation_log) | Worker output log |

## UAT Document Generation

After task completion, generate UAT document:

```markdown
# UAT: {task.title}

## Acceptance Criteria Verification

- [x] Criterion 1 - Verified by test_foo.py::test_criterion_1
- [x] Criterion 2 - Verified by test_foo.py::test_criterion_2

## Test Results

- Tests Run: 5
- Passed: 5
- Failed: 0
- Coverage: 85%

## Files Changed

### Created
- src/feature.py

### Modified
- src/app.py
```

Save to `logs` (type=uat_document)

## Related Skills

- `/validate-plan` - Previous phase
- `/verify-code` - Next phase
- `/orchestrate` - Main workflow
