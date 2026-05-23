---
name: reality-verification
description: This skill should be used when the user asks to "verify a fix", "reproduce failure", "diagnose issue", "check BEFORE/AFTER state", "VF task", "reality check", "check test quality", "mock-only tests", or needs guidance on verifying fixes by reproducing failures before and after implementation, or detecting mock-heavy test anti-patterns.
version: 0.2.0
user-invocable: false
---

# Reality Verification

For fix goals: reproduce the failure BEFORE work, verify resolution AFTER.

## Goal Detection

Classify user goals to determine if diagnosis is needed. See `references/goal-detection-patterns.md` for detailed patterns.

**Quick reference:**
- Fix indicators: fix, repair, resolve, debug, patch, broken, failing, error, bug
- Add indicators: add, create, build, implement, new
- Conflict resolution: If both present, treat as Fix

## Command Mapping

| Goal Keywords | Reproduction Command |
|---------------|---------------------|
| CI, pipeline | `gh run view --log-failed` |
| test, tests | project test command |
| type, typescript | `pnpm check-types` or `tsc --noEmit` |
| lint | `pnpm lint` |
| build | `pnpm build` |
| E2E, UI | Playwright MCP browser tools |
| API, endpoint | WebFetch tool |

For E2E/deployment verification, use MCP tools (Playwright MCP browser tools for UI, WebFetch tool for APIs).

## BEFORE/AFTER Documentation

### BEFORE State (Diagnosis)

Document in `.progress.md` under `## Reality Check (BEFORE)`:

```markdown
## Reality Check (BEFORE)

**Goal type**: Fix
**Reproduction command**: `pnpm test`
**Failure observed**: Yes
**Output**:
```
FAIL src/auth.test.ts
  Expected: 200
  Received: 401
```
**Timestamp**: 2026-01-16T10:30:00Z
```

### AFTER State (Verification)

Document in `.progress.md` under `## Reality Check (AFTER)`:

```markdown
## Reality Check (AFTER)

**Command**: `pnpm test`
**Result**: PASS
**Output**:
```
PASS src/auth.test.ts
All tests passed
```
**Comparison**: BEFORE failed with 401, AFTER passes
**Verified**: Issue resolved
```

## VF Task Format

Add as task 4.3 (after PR creation) for fix-type specs:

```markdown
- [ ] 4.3 VF: Verify original issue resolved
  - **Do**:
    1. Read BEFORE state from .progress.md
    2. Re-run reproduction command: `<command>`
    3. Compare output with BEFORE state
    4. Document AFTER state in .progress.md
  - **Verify**: `grep -q "Verified: Issue resolved" ./specs/<name>/.progress.md`
  - **Done when**: AFTER shows issue resolved, documented in .progress.md
  - **Commit**: `chore(<name>): verify fix resolves original issue`
```

## Test Quality Checks

When verifying test-related fixes, check for mock-only test anti-patterns. See `references/mock-quality-checks.md` for detailed patterns.

**Quick reference red flags:**
- Mock declarations > 3x real assertions
- Missing import of actual module under test
- All assertions are mock interaction checks (toHaveBeenCalled)
- No integration tests
- Missing mock cleanup (afterEach)

## Why This Matters

| Without | With |
|---------|------|
| "Fix CI" spec completes but CI still red | CI verified green before merge |
| Tests "fixed" but original failure unknown | Before/after comparison proves fix |
| Silent regressions | Explicit failure reproduction |
| Manual verification required | Automated verification in workflow |
| Tests pass but only test mocks | Tests verify real behavior, not mock behavior |
| False sense of security from green tests | Confidence that tests catch real bugs |
