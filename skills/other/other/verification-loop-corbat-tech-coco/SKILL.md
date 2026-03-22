---
name: verification-loop
description: Run verify → identify failures → fix → verify again until all checks pass. Iterative quality enforcement loop for reaching a clean state before committing or releasing.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Verification Loop

Iterative loop: run all checks → fix failures → repeat until clean.

## Loop Structure

```
while (not all passing):
  1. Run full verification suite
  2. If all pass → DONE ✅
  3. Identify the first/most critical failure
  4. Fix it (minimal change)
  5. Go to 1
```

Maximum iterations: **10** (if not clean after 10, report blockers and stop)

## Step 1: Initial State

```bash
pnpm format:fix 2>&1
pnpm typecheck 2>&1 | head -30
pnpm lint 2>&1 | head -30
pnpm test 2>&1 | tail -20
```

Count failures per category to plan the fix order.

## Step 2: Fix Priority Order

Fix in this order (each category may create/expose the next):

1. **Formatting** — run `pnpm format:fix` to auto-fix style issues before anything else
2. **TypeScript import errors** — missing `.js` extensions, wrong paths
3. **TypeScript type errors** — incorrect types, missing returns
4. **Lint errors** — oxlint violations
5. **Test failures** — logic errors, unhandled cases

## Step 3: Fix One Category at a Time

### TypeScript Errors
```bash
pnpm typecheck 2>&1
```
Fix each error, re-run, confirm count decreases.

### Lint Errors
```bash
pnpm lint 2>&1
```
Fix each oxlint error. Common fixes:
- `no-explicit-any` → use proper type or `unknown`
- `no-unused-vars` → remove or prefix with `_`
- `prefer-const` → change `let` to `const`

### Test Failures
```bash
pnpm test 2>&1
```
For each failing test:
1. Read the failure message
2. Read the test to understand expected behavior
3. Read the implementation to find the bug
4. Fix the implementation (not the test, unless test is wrong)

## Step 4: Verify Clean

```bash
pnpm check
```

If output shows 0 errors across typecheck + lint + test → **DONE**.

## Circuit Breaker

Stop and report to user if:
- Same error persists after 3 fix attempts
- Fix introduces more errors than it resolves
- Error requires architectural change (not a simple fix)
- Missing dependency needs `pnpm add`

## Final Report

```markdown
## Verification Loop Complete

### Iterations: N

### Fixed
- TypeScript: N errors fixed
- Lint: N errors fixed
- Tests: N failures fixed

### Status
✅ pnpm check — ALL PASSING
Coverage: X%

### Remaining Issues (if any)
- [blocker requiring user decision]
```
