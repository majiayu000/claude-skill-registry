---
name: test-context-parent
description: Parent skill for context sharing test - creates context, calls child
allowed-tools: Read, Write, Skill
model: claude-opus-4-5
context: fork
---

# Context Parent Test

## Task

1. First, read this file to create some context: `earnings-analysis/predictions.csv` (first 5 lines)
2. Note: "PARENT_SECRET = banana" (remember this)
3. Call child skill: `/test-context-child` with args: "parent_says_hello ticker=AAPL"
4. Capture the child's return value
5. Write report to: `earnings-analysis/test-outputs/context-parent-report.txt`

Include in report:
- What you read from predictions.csv
- The PARENT_SECRET value
- The EXACT return value from the child (copy it verbatim)
- Whether the child's return mentioned the number 42
