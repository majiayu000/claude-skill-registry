---
name: test-task-direct
description: Direct test - just call TaskList and TaskCreate, no introspection
context: fork
allowed-tools:
  - TaskCreate
  - TaskList
  - Write
---

# Direct Task Tool Test

DO NOT check if tools are available. DO NOT introspect. Just CALL them directly.

## Instructions

1. **IMMEDIATELY call TaskList** - just use the tool, don't check anything first
2. **IMMEDIATELY call TaskCreate** with subject "DIRECT-TEST-$ARGUMENTS" and description "Direct test from $ARGUMENTS"
3. Write the ACTUAL results (or errors) to `earnings-analysis/test-outputs/direct-test-$ARGUMENTS.txt`

Format:
```
CALLER: $ARGUMENTS
TIMESTAMP: {now}
TASKLIST_RESULT: {paste the actual tool output or error message}
TASKCREATE_RESULT: {paste the actual tool output or error message}
```

DO NOT say "tool not available" unless you actually tried to call it and got an error. JUST CALL THE TOOLS.
