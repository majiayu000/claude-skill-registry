---
name: debug
description: Use when the user reports an error, unexpected behavior, test failure, or asks to trace or diagnose a problem. Applies 6-step structured debugging.
invocation: agent
---

# Debug

Systematic debugging using the `persona-debugger` agent methodology. Apply six steps to find and fix the root cause.

## 6-Step Methodology

### Step 1: Reproduce

Understand and reproduce the issue from the given input:
- Parse error messages, stack traces, or symptom descriptions
- Identify reproduction steps
- Confirm the failure is consistent or intermittent

### Step 2: Isolate

Narrow down the root cause:
- Identify the failing code path
- Use bisection or elimination to isolate the component
- Check recent changes with `git log --oneline -20`

### Step 3: Analyze

Examine code, logs, and state:
- Read the relevant source files
- Check error handling and edge cases
- Trace data flow through the failure path

### Step 4: Hypothesize

Form theories about the bug:
- List 2-3 candidate root causes
- Rank by likelihood based on evidence
- Identify what evidence would confirm/reject each

### Step 5: Test

Validate hypotheses:
- Add strategic debug output or assertions
- Test each hypothesis against the evidence
- Confirm root cause with high confidence

### Step 6: Fix

Implement and verify the solution:
- Apply the minimal fix that addresses the root cause
- Add a regression test to prevent recurrence
- Run existing tests to verify no regressions

## Report

```
## Debug Complete

**Issue**: <brief description>
**Root Cause**: [file:line] - <explanation>
**Confidence**: [High/Medium/Low]
**Fix Applied**: Yes/No

### Evidence
- <key evidence supporting diagnosis>

### Prevention
- <regression test added>
- <recommendations to prevent similar issues>

Next Steps:
- `/arc:core:verify --post` to run full verification
- `/arc:specialized:bug` for deeper investigation if fix didn't resolve
```
