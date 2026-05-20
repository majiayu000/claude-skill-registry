---
name: verify
description: Run the complete verification suite: build → typecheck → lint → tests → coverage → git status. Produces a pass/fail report with PR readiness assessment. Use before committing or creating PRs.
allowed-tools: Bash, Read, Glob
---

# Verify

Run all quality gates and produce a comprehensive pass/fail report.

## Full Verification Sequence

Execute in this order (stop at first critical failure):

### 1. TypeScript Check
```bash
pnpm typecheck 2>&1
```
Reports type errors without building.

### 2. Lint
```bash
pnpm lint 2>&1
```
oxlint checks for code quality and potential bugs.

### 3. Format Check
```bash
pnpm format 2>&1
```
oxfmt verifies formatting is consistent.

### 4. Tests
```bash
pnpm test 2>&1
```
Runs all Vitest tests.

### 5. Coverage
```bash
pnpm test:coverage 2>&1 | tail -20
```
Checks coverage thresholds (80%+ lines, functions, branches, statements).

### 6. Build
```bash
pnpm build 2>&1
```
Verifies tsup produces valid output.

### 7. Git Status
```bash
git status --short
git diff --stat HEAD
```
Shows what changed and what's uncommitted.

## Quick Modes

```bash
# Quick check — typecheck + lint only (fast, ~5s)
pnpm typecheck && pnpm lint

# Pre-commit — typecheck + lint + tests (no coverage, ~15s)
pnpm check

# Full — everything including coverage + build (~45s)
pnpm check && pnpm test:coverage && pnpm build
```

## Output Report Format

```markdown
## Verification Report

| Check | Status | Details |
|-------|--------|---------|
| TypeScript | ✅ PASS / ❌ FAIL | [error count or "no errors"] |
| Lint (oxlint) | ✅ PASS / ❌ FAIL | [warnings/errors] |
| Format (oxfmt) | ✅ PASS / ❌ FAIL | [files needing format] |
| Tests | ✅ PASS / ❌ FAIL | [X passed, Y failed] |
| Coverage | ✅ PASS / ❌ FAIL | [lines: X%, functions: X%] |
| Build | ✅ PASS / ❌ FAIL | [output size] |

**Overall**: ✅ ALL PASSING — Ready for PR / ❌ BLOCKED — Fix issues above

### Issues Found
- [TypeScript] `src/path/file.ts:L42` — [error message]
- [Tests] `src/path/test.ts` — [failure reason]

### Uncommitted Changes
- M src/path/file.ts
- A src/path/new-file.ts

### PR Readiness
[READY / NOT READY — [blocking reason]]
```

## Thresholds (corbat-coco)

| Metric | Threshold |
|--------|-----------|
| Lines coverage | ≥80% |
| Functions coverage | ≥80% |
| Branches coverage | ≥80% |
| TypeScript errors | 0 |
| Lint errors | 0 |
| Test failures | 0 |

## Usage

```
/verify          # full suite
/verify quick    # typecheck + lint only
/verify pre-pr   # everything + security scan
```
