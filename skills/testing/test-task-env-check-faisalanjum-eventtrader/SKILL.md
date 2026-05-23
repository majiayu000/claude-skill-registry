---
name: test-task-env-check
description: Check CLAUDE_CODE_TASK_LIST_ID environment variable in forked skill
context: fork
allowed-tools:
  - Bash
  - TaskList
  - TaskCreate
  - Write
---

# Test: Environment Variable Propagation

**Objective**: Check if CLAUDE_CODE_TASK_LIST_ID is visible in forked skill context.

## Instructions

1. Check the CLAUDE_CODE_TASK_LIST_ID environment variable
2. List current tasks
3. Create a task with a unique identifier
4. Write results to output file

## Output

Write to: `earnings-analysis/test-outputs/task-env-check-result.txt`

Format:
```
TEST: task-env-check (forked skill)
TIMESTAMP: {ISO timestamp}

ENVIRONMENT:
CLAUDE_CODE_TASK_LIST_ID: {value or "NOT SET"}

TASK LIST BEFORE:
{output from TaskList}

CREATED TASK:
Subject: "ENV_TEST_FROM_FORK_{random-id}"
Task ID: {id}

TASK LIST AFTER:
{output from TaskList}

CONCLUSION: {findings}
```

Return a summary of findings.
