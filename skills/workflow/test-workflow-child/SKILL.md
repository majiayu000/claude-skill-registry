---
name: test-workflow-child
description: Simple child skill for workflow continuation test - writes file and returns
allowed-tools: Write
context: fork
---

# Workflow Test Child

**Purpose**: Be a simple child that completes and returns, to test if parent continues after.

## Task

1. Get current timestamp
2. Write to: `earnings-analysis/test-outputs/workflow-child.txt`

Content:
```
CHILD_EXECUTED
Timestamp: [current ISO timestamp]
Message: Child skill completed successfully
```

3. Return this exact text: "CHILD_RETURN_VALUE_12345"

Do NOT do anything else. Just write the file and return the value.
