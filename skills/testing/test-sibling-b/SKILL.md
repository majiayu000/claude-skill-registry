---
name: test-sibling-b
description: Sibling B for isolation test - writes secret, checks for sibling A's secret
allowed-tools: Write, Read, Glob
context: fork
---

# Sibling B Test

**Goal**: Test if sibling skills share context.

## Task

1. Write "SIBLING_B_SECRET = blue" to `earnings-analysis/test-outputs/sibling-b-secret.txt`
2. Try to find any evidence of "SIBLING_A_SECRET" in your context
3. Check if file `earnings-analysis/test-outputs/sibling-a-secret.txt` exists (from filesystem, not context)
4. Report findings

Write to: `earnings-analysis/test-outputs/sibling-b-result.txt`

Return: "SIBLING_B_DONE: blue | SAW_A: [yes/no] | FILE_A_EXISTS: [yes/no]"
