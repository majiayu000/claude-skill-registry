---
name: test-sdk-task-tools
description: Test if forked skill called from SDK has TaskCreate/List/Get/Update tools
context: fork
allowed-tools:
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - Write
  - Read
---

# Test SDK Task Tools Availability

Check if TaskCreate, TaskList, TaskGet, TaskUpdate tools are available in this forked skill context.

## Arguments

Output filename passed via: `$ARGUMENTS`

- If arguments provided, use that as output filename
- If no arguments, use default: `sdk-task-tools-DEFAULT.txt`

## Task

1. Determine output filename from arguments: `$ARGUMENTS`
2. Try to use TaskList to list all tasks
3. If TaskList works, try TaskCreate to create a task with subject "TASK-TOOL-TEST-{output_filename}"
4. Write results to `earnings-analysis/test-outputs/{output_filename}`

Report format:
```
CALLER: {the argument passed, or DEFAULT if none}
TIMESTAMP: {current ISO timestamp}
TASKLIST_AVAILABLE: YES/NO
TASKLIST_OUTPUT: {output or error}
TASKCREATE_AVAILABLE: YES/NO
TASKCREATE_OUTPUT: {output or error}
```
