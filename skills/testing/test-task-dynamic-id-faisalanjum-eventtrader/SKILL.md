---
name: test-task-dynamic-id
description: Test if we can dynamically set CLAUDE_CODE_TASK_LIST_ID
context: fork
allowed-tools:
  - Bash
  - TaskList
  - TaskCreate
  - Write
---

# Test: Dynamic Task List ID Setting

**Objective**: Can we change CLAUDE_CODE_TASK_LIST_ID dynamically within a skill?

## Instructions

1. Check current CLAUDE_CODE_TASK_LIST_ID
2. List current tasks (baseline)
3. Try to set CLAUDE_CODE_TASK_LIST_ID via export
4. Create a task AFTER setting the env var
5. Check if task goes to new list or same list
6. Write results

## Output

Write to: `earnings-analysis/test-outputs/task-dynamic-id-result.txt`

Execute these exact steps:

```bash
# Step 1: Check current env
echo "BEFORE: CLAUDE_CODE_TASK_LIST_ID=$CLAUDE_CODE_TASK_LIST_ID"

# Step 2: Set new ID
export CLAUDE_CODE_TASK_LIST_ID="dynamic-test-list"

# Step 3: Verify it's set in bash
echo "AFTER EXPORT: CLAUDE_CODE_TASK_LIST_ID=$CLAUDE_CODE_TASK_LIST_ID"
```

Then use TaskList to see current tasks.
Then use TaskCreate to create: "DYNAMIC_ID_TEST_TASK"
Then use TaskList again.

Report:
- Did the env var change affect which task list is used?
- Can tasks be isolated by dynamically setting the ID?
