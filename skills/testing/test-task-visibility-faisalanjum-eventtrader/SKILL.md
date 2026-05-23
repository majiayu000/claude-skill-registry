---
name: test-task-visibility
description: Test if forked skill can see tasks created by parent/main conversation
context: fork
allowed-tools:
  - TaskList
  - TaskGet
  - Write
---

# Test: Cross-Context Task Visibility

**Objective**: Check if this forked skill can see tasks created in the main conversation.

## Instructions

1. Run TaskList immediately (DO NOT create any tasks first)
2. Record what you see
3. If any tasks exist, use TaskGet on the first one to see details
4. Write results to output file

## Output

Write results to: `earnings-analysis/test-outputs/task-visibility-result.txt`

Format:
```
TEST: task-visibility (forked skill seeing parent's tasks)
TIMESTAMP: {ISO timestamp}

TASKLIST RESULT:
{exact output from TaskList}

TASK COUNT: {n}

VISIBLE TASKS:
{list each task ID, subject, status if any exist}
{or "NONE - forked skill cannot see parent's tasks"}

CONCLUSION: Forked skill {CAN|CANNOT} see tasks from main conversation
```

Return a brief summary.
