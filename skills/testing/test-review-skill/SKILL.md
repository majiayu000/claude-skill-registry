---
name: test-review
description: Use to review test coverage for completeness and quality
---

# Test Review Skill

Two-phase review: First analyze coverage gaps, then add approved tests.

**Preset Configuration:**
- Focus: Test completeness, edge cases, quality
- Quality Gate: No new gaps found for 1 iteration (review comprehensive)
- Reviewer Type: Test Coverage Analyst
- Max Iterations: 4

## When to Use

- After implementing a feature to verify test coverage
- Before release to check critical paths are tested
- When adding tests to existing code
- Periodic test health checks

## Required Information

1. **Target** - code module to check coverage for (e.g., `src-tauri/src/calculations.rs`)
2. **Reference** (optional) - business rules or plan defining what should be tested

---

## Phase 1: Review (Findings Only)

### Step 1: Identify Test Files

Find tests for target:
```bash
# Rust - find test module
grep -l "test_" src-tauri/src/*_tests.rs

# Check inline tests
grep -A5 "#\[cfg(test)\]" src-tauri/src/{module}.rs
```

### Step 2: Run Tests (Baseline)

```bash
npm run test:backend
```

Note current test count and status.

### Step 3: Create Review Document

Create `{TARGET_DIR}/_test-review.md`:

```markdown
# Test Coverage Review

**Target:** {TARGET}
**Reference:** {REFERENCE}
**Started:** YYYY-MM-DD
**Status:** In Progress
**Focus:** Completeness, edge cases, test quality

**Baseline:** N tests, [Pass / Fail]

## Iteration 1

### Findings

[To be filled by review agent]
```

### Step 4: Execute Review Loop

For each iteration (max 4):

**Spawn Review Agent:**

```
Task tool (general-purpose):
  description: "Test review iteration N"
  prompt: |
    You are a Test Coverage Analyst reviewing tests for {TARGET}.

    Reference (if provided): {REFERENCE}
    Previous findings (if any): [summary from _test-review.md]

    Your job:

    1. **Coverage Analysis**
       - What functions/methods exist in {TARGET}?
       - Which have corresponding tests?
       - Which are missing tests?

    2. **Edge Case Analysis**
       - Are boundary conditions tested?
       - Are error paths tested?
       - Are empty/null inputs tested?

    3. **Test Quality**
       - Do tests test actual logic (not mocks)?
       - Are assertions meaningful?
       - Are tests independent?

    4. **Business Logic**
       - Are calculation formulas verified?
       - Are business rules from {REFERENCE} tested?

    Focus on GAPS not on what's already well-tested.
    We don't want filler tests - only meaningful coverage.

    Categorize findings as Critical/Important/Minor.
    Note any NEW gaps not in previous iterations.
```

**Update Review Document:** Append findings to `_test-review.md`:
```markdown
## Iteration N

### New Coverage Gaps
- [Critical] Function X has no tests - handles Y logic
- [Important] Edge case Z not covered in test_foo
- [Minor] Could add test for rare path W

### Test Quality Issues
[Any issues with existing tests]

### Coverage Assessment
[Areas reviewed / Areas remaining]
```

**Commit Review Only:**
```bash
git add {TARGET_DIR}/_test-review.md
git commit -m "review(test): iteration N findings for {TARGET}"
```

**Quality Gate:** Exit when no new gaps found for 1 iteration (review is comprehensive).

### Step 5: Finalize Review Document

Update `_test-review.md` with summary:

```markdown
## Review Summary

**Status:** Ready for User Review
**Iterations:** N
**Total Gaps:** X Critical, Y Important, Z Minor

### All Coverage Gaps (Consolidated)

#### Critical (Missing tests for core logic)
1. [ ] Gap description - What test to add

#### Important (Edge cases / error paths)
1. [ ] Gap description - What test to add

#### Minor (Nice to have)
1. [ ] Gap description - What test to add

### Test Quality Issues
- [ ] Issue description - Suggested improvement

### Coverage Assessment
[Sparse / Adequate / Comprehensive]
```

**Commit:**
```bash
git add {TARGET_DIR}/_test-review.md
git commit -m "review(test): complete findings for {TARGET}"
```

### Step 6: Present Review for Approval

Inform user:

> **Test coverage review complete.**
>
> Please review `{TARGET_DIR}/_test-review.md` for findings.
>
> After your review, let me know:
> - Which tests to add
> - Which gaps to skip (acceptable risk)
> - Any questions about coverage

**STOP and wait for user direction.**

---

## Phase 2: Add Approved Tests

*Only proceed after user approval.*

### Step 7: Add Approved Tests

For each user-approved gap:

1. Write the test following TDD principles
2. Check the gap as addressed in `_test-review.md`: `[x]`

### Step 8: Run Tests

```bash
npm run test:backend
```

Verify:
- All new tests pass
- No existing tests broken
- Test count increased as expected

### Step 9: Commit Changes

```bash
git add src-tauri/src/*_tests.rs
git commit -m "test: add coverage for {TARGET}

Added:
- [list of new tests]"
```

### Step 10: Final Assessment

Update `_test-review.md`:

```markdown
## Resolution

**Tests Added:** N
**Gaps Skipped:** M (user decision)
**Final Test Count:** X (was Y)
**Status:** Complete

### Added Tests
- test_foo: covers [what]
- test_bar: covers [what]

### Skipped Gaps
- Gap X: [user's reason - acceptable risk]
```

---

## Domain-Specific Checklist

Review should verify:
- [ ] Core business logic has tests
- [ ] Edge cases covered (empty, null, boundary)
- [ ] Error paths tested
- [ ] No tests that only test mocks
- [ ] Tests are independent (can run in any order)
- [ ] Tests have meaningful assertions

## Example

```
User: /test-review src-tauri/src/calculations.rs against DECISIONS.md

Claude: [Executes Phase 1 - analyzes coverage, creates _test-review.md, iterates until comprehensive]
Claude: Test coverage review complete. Please review _test-review.md for findings.

User: Add Critical and Important tests. Skip Minor - we're time constrained.

Claude: [Executes Phase 2 - adds approved tests, runs tests, commits]
```
