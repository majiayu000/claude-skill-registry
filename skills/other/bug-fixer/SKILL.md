---
name: bug-fixer
description: Diagnose bugs through iterative investigation, apply a type-safe fix, and generate a regression test. Use when asked to fix a bug, debug an error, diagnose a crash, investigate a failing test, or resolve an exception.
---

# Bug Fixer Agent

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

This agent diagnoses and fixes bugs through iterative investigation. Follow this process:

## Step 1: Intake

Read the error message, stack trace, or bug description. Identify the entry point file and line number if available.

## Step 2: First Pass

Read the identified file and its immediate imports. Form a hypothesis about the root cause.

## Step 3: Decision Point

- If root cause is **clear** → proceed to step 5.
- If root cause is **unclear** → **WIDEN SEARCH**. Read files upstream (who calls this function?) and downstream (what does this function call?). Check recent git changes in the affected area with `git log -10 --oneline -- <file>` if available. Reform hypothesis.
- If **still unclear** after widening → ask the user for reproduction steps or additional context. Do not guess.

## Step 4: Validate Hypothesis

Before fixing, explain the root cause to the user and ask for confirmation. A wrong diagnosis leads to a wrong fix.

## Step 5: Apply Fix

Use `typescript-refactorer` principles to apply a type-safe fix:
- Fix addresses the root cause, not just the symptom
- Types are correct and narrowed (no `any`, no unsafe casts)
- Null/undefined cases are handled with proper guards
- No new code smells introduced

If the fix touches Prisma queries, validate with `prisma-query-optimizer` principles.

If the fix changes a function signature, check all call sites for compatibility.

## Step 6: Generate Test

Use `test-generator` principles to create a regression test that:
- Reproduces the exact original bug scenario (should fail without the fix)
- Verifies the fix works (should pass with the fix)
- Covers edge cases around the bug

## Step 7: Run Test

Execute the regression test. If it fails, re-examine the fix. Repeat up to 3 times.

## Step 8: Report

```
## Bug Fix Report

### Root Cause
[One-paragraph explanation]

### Fix Applied
**File**: `path/to/file.ts`
[Code diff or before/after]

### Regression Test
**File**: `path/to/file.test.ts`
[Generated test code]

### Confidence: [high/medium/low]
- high: root cause confirmed, test passes, fix is minimal
- medium: root cause likely, test passes, fix touches multiple files
- low: root cause uncertain, ask user to verify behavior
```

## Skill Dependencies

- `skills/code-reviewer` — root cause analysis patterns
- `skills/typescript-refactorer` — type-safe fix
- `skills/prisma-query-optimizer` — query-related bugs (conditional)
- `skills/test-generator` — regression test generation
