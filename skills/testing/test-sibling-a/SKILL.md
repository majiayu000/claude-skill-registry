---
name: test-sibling-a
description: Sibling A for isolation test - writes secret, checks for sibling B's secret
allowed-tools: Write, Read, Glob
context: fork
---

# Sibling A Test

**Goal**: Test if sibling skills share context.

## Task

1. Write "SIBLING_A_SECRET = red" to `earnings-analysis/test-outputs/sibling-a-secret.txt`
2. Try to find any evidence of "SIBLING_B_SECRET" in your context
3. Check if file `earnings-analysis/test-outputs/sibling-b-secret.txt` exists
4. Report findings

Write to: `earnings-analysis/test-outputs/sibling-a-result.txt`

Return: "SIBLING_A_DONE: red | SAW_B: [yes/no]"
