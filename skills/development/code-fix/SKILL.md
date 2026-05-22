---
name: code-fix
description: Apply prioritized code fixes based on review findings. Single pass - fixes P0 first, then P1, P2, P3. Use after /code-review.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task
---

# Code Fix

Apply code fixes based on review findings, prioritized by severity. This is a **single pass** — it applies fixes once and verifies them.

## How it works

This skill is **agent-implemented** — the agent reads the steps below and executes them autonomously. There is no standalone bash script.

```
/code-fix
/code-fix "P0 only"
/code-fix security
```

## Input

- `$ARGUMENTS` = optional focus (e.g., "P0 only", "security", "tests", or a file path)
- If empty, fixes all issues found by `/code-review`, prioritized P0 -> P1 -> P2 -> P3

## Prerequisites

This skill works best after running `/code-review` to identify issues. If no review has been run, it performs a quick assessment first.

## Step 1: Identify Issues

If a `/code-review` was run recently, use its findings. Otherwise, do a quick assessment:

```bash
# Check for obvious issues
git diff --stat HEAD~3..HEAD 2>/dev/null
```

Read the recently changed files and identify issues using the same 12-dimension framework from `/code-review`.

## Step 2: Prioritize and Plan

Create a fix plan sorted by severity:

```
## Fix Plan

### P0 Critical (must fix)
1. [file:line] Issue description -> Planned fix

### P1 High (fix before merge)
1. [file:line] Issue description -> Planned fix

### P2 Medium (should fix)
1. [file:line] Issue description -> Planned fix

### P3 Low (nice to have)
1. [file:line] Issue description -> Planned fix
```

Present the plan to the user before proceeding. Wait for confirmation.

> **Automated context exception**: if this skill is invoked as a subagent from an automated loop (e.g., `/coco-fix-iterate`), skip the confirmation step and proceed directly with the fix plan.

## Step 3: Apply Fixes (P0 first)

For each priority level, starting with P0:

1. **Read** the file containing the issue
2. **Fix** the issue using Edit tool
3. **Verify** the fix doesn't break anything:
   ```bash
   # Quick verification after each fix
   pnpm typecheck 2>&1 || npm run typecheck 2>&1 || true
   ```
4. **Move** to the next issue

### Fix Guidelines

- **Minimal changes** — fix only what's broken, don't refactor surrounding code
- **One issue at a time** — don't batch unrelated fixes in the same edit
- **Preserve style** — match the existing code style and patterns
- **Test after critical fixes** — run tests after P0 and P1 fixes:
  ```bash
  pnpm test 2>&1 || npm test 2>&1 || cargo test 2>&1 || pytest 2>&1 || true
  ```

### Common Fix Patterns

**Security (P0)**
- Hardcoded secrets -> environment variables
- SQL injection -> parameterized queries
- XSS -> output encoding
- Missing auth checks -> add middleware/guard

**Error Handling (P1)**
- Empty catch blocks -> proper error handling with logging
- Missing null checks -> add guards
- Unhandled promises -> add .catch() or try/catch
- Broad exceptions -> specific error types

**Test Coverage (P1-P2)**
- Missing tests for critical paths -> add focused tests
- Weak assertions -> strengthen with specific checks
- Missing edge cases -> add boundary tests

**Code Quality (P2-P3)**
- Long functions -> extract helper functions
- Duplicated code -> extract shared utility
- Complex conditionals -> simplify or extract
- Missing types -> add type annotations

## Step 4: Run Full Checks

After all fixes are applied:

```bash
# Run the project's full check suite
if [ -f "pnpm-lock.yaml" ]; then
  pnpm check 2>&1 || pnpm test 2>&1
elif [ -f "yarn.lock" ]; then
  yarn test 2>&1
elif [ -f "package-lock.json" ]; then
  npm test 2>&1
elif [ -f "Cargo.toml" ]; then
  cargo test 2>&1
elif [ -f "pyproject.toml" ]; then
  pytest 2>&1
fi
```

If checks fail, fix the regression and re-run (max 3 attempts).

## Step 5: Report

```
## Code Fix Report

### Fixes Applied
- [x] P0: [file:line] Description (FIXED)
- [x] P1: [file:line] Description (FIXED)
- [ ] P2: [file:line] Description (SKIPPED - reason)

### Verification
- Typecheck: PASS/FAIL
- Lint: PASS/FAIL
- Tests: PASS/FAIL (N passed, N failed)

### Files Modified
- path/to/file1.ts (3 changes)
- path/to/file2.ts (1 change)

### Remaining Issues
- P3: [file:line] Description (not fixed - cosmetic only)
```

## Important

- Always fix P0 issues — these are non-negotiable
- Ask the user before fixing P3 issues (they may not be worth the churn)
- If a fix introduces new issues, revert it and try a different approach
- Run `/code-review` after fixing to see the updated score
- Run `/coco-fix-iterate` instead if you want automatic review-fix loops until a target score
