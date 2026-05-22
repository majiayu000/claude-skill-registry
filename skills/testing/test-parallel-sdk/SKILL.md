---
name: test-parallel-sdk
description: Test if Task tool (parallel subagents) works in SDK context
context: fork
allowed-tools:
  - Task
  - Write
  - Read
---

# Test Parallel Task Tool in SDK

Test whether the Task tool (subagent spawner) is available and works for parallel execution.

## Instructions

1. **Try to spawn TWO Task subagents in parallel** using the Task tool:
   - Task A: Use Explore agent to count files in `.claude/skills/`
   - Task B: Use Explore agent to count files in `scripts/`

2. **Write results** to `earnings-analysis/test-outputs/parallel-test-$ARGUMENTS.txt`:

```
CALLER: $ARGUMENTS
TIMESTAMP: {current time}
TASK_TOOL_AVAILABLE: YES or NO
PARALLEL_EXECUTION: SUCCESS or FAILED
TASK_A_RESULT: {result or error}
TASK_B_RESULT: {result or error}
ERROR_IF_ANY: {exact error message if Task tool failed}
```

IMPORTANT: Actually TRY to use the Task tool. Don't just check if it exists - call it.
