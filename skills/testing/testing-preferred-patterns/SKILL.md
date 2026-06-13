---
name: testing-preferred-patterns
description: "Identify and fix testing mistakes: flaky, brittle, over-mocked tests."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
routing:
  category: testing
  triggers:
    - flaky test
    - brittle test
    - test smell
    - test quality issue
    - slow tests
    - skipped test
    - test depends on order
    - over-mocking
    - fragile test
    - testing implementation details
  pairs_with:
    - test-driven-development
    - go-patterns
    - vitest-runner
  complementary: test-driven-development
---

# Testing Pattern Quality Skill

## Overview

This skill identifies and fixes common testing mistakes across unit, integration, and E2E test suites. Tests should verify behavior, be reliable, run fast, and fail for the right reasons.

**Scope:** This skill focuses on improving test quality and reliability. It complements `test-driven-development` by addressing what goes wrong with tests, complementing how to write them correctly from scratch.

**Out of scope:** Writing new tests from scratch (use `test-driven-development`), fixing fundamental architectural issues (use `systematic-refactoring`), or profiling test performance with external tools.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| BAD/GOOD code examples for all 10 testing failure modes | `preferred-pattern-catalog.md` | Loads detailed guidance from `preferred-pattern-catalog.md`. |
| auditing coverage gaps: concurrency, boundaries, security, error recovery | `blind-spot-taxonomy.md` | Loads detailed guidance from `blind-spot-taxonomy.md`. |
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |
| fixing review feedback | `fix-strategies.md` | Loads detailed guidance from `fix-strategies.md`. |
| tests | `load-test-scenarios.md` | Loads detailed guidance from `load-test-scenarios.md`. |
| classifying test-quality failure modes found during SCAN | `quality-catalog.md` | Loads detailed guidance from `quality-catalog.md`. |
| fast pattern-symptom-fix lookup | `quick-reference.md` | Loads detailed guidance from `quick-reference.md`. |

## Instructions

### Phase 1: SCAN

**Goal**: Identify quality issues present in the target test code.

**Step 1: Locate test files**

Use Grep/Glob to find test files in the relevant area. If user pointed to specific files, start there. Common patterns:
- Go: `*_test.go`
- Python: `test_*.py` or `*_test.py`
- JavaScript/TypeScript: `*.test.ts`, `*.spec.ts`, `*.test.js`, `*.spec.js`

**Step 2: Read CLAUDE.md**

Check for project-specific testing conventions before flagging quality issues. Some projects intentionally deviate from general best practices. This prevents false positives based on organizational standards.

**Step 3: Classify quality issues**

For each test file, scan for these 10 categories (detailed examples in `references/preferred-pattern-catalog.md`):

| # | Pattern to Fix | Detection Signal |
|---|-------------|-----------------|
| 1 | Testing implementation details | Asserts on private fields, internal regex, spy on private methods |
| 2 | Over-mocking / brittle selectors | Mock setup > 50% of test code, CSS nth-child selectors |
| 3 | Order-dependent tests | Shared mutable state, class-level variables, numbered test names |
| 4 | Incomplete assertions | `!= nil`, `> 0`, `toBeTruthy()`, no value checks |
| 5 | Over-specification | Exact timestamps, hardcoded IDs, asserting every default field |
| 6 | Ignored failures | `@skip`, `.skip`, `xit`, empty catch blocks, `_ = err` |
| 7 | Poor naming | `testFunc2`, `test_new`, `it('works')`, `it('handles case')` |
| 8 | Missing edge cases | Only happy path, no empty/null/boundary/error tests |
| 9 | Slow test suites | Full DB reset per test, no parallelization, no fixture sharing |
| 10 | Flaky tests | `sleep()`, `time.Sleep()`, `setTimeout()`, unsynchronized goroutines |

**Step 4: Document findings**

```markdown
## Pattern Quality Report

### [File:Line] - [Pattern Name]
- **Severity**: HIGH / MEDIUM / LOW
- **Issue**: [What is wrong]
- **Impact**: [Flaky / slow / false-confidence / maintenance burden]
```

**Gate**: At least one quality issue identified with file:line reference. Proceed only when gate passes.

### Phase 2: PRIORITIZE

**Goal**: Rank findings by impact to fix the most damaging patterns first.

**Priority order:**
1. **HIGH** - Flaky tests, order-dependent tests, ignored failures (erode trust in suite)
2. **MEDIUM** - Over-mocking, incomplete assertions, missing edge cases (false confidence)
3. **LOW** - Poor naming, over-specification, slow suites (maintenance burden)

**Constraint: Fix one pattern at a time.** Mechanical bulk fixes (applying the same pattern to 50 tests without running them) miss context-specific nuances and cause regressions. Fix one, verify it works, then move to the next.

**Constraint: Preserve test intent.** When fixing quality issues, maintain what the test was originally trying to verify. Preserve the original test coverage scope.

**Constraint: Prevent over-engineering.** Fix the specific quality issue identified; make targeted fixes to the specific failure mode or delete tests and write new ones from scratch. Institutional knowledge lives in the existing tests.

**Gate**: Findings ranked. User agrees on scope of fixes. Proceed only when gate passes.

### Phase 3: FIX

**Goal**: Apply targeted fixes to identified quality issues.

**Step 1: For each quality issue (highest priority first):**

```markdown
ISSUE: [Name]
Location: [file:line]
Issue: [What is wrong]
Impact: [Flaky/slow/false-confidence/maintenance burden]

Current:
[problematic code snippet]

Fixed:
[improved code snippet]

Priority: [HIGH/MEDIUM/LOW]
```

**Step 2: Apply fix**

**Constraint: Show real examples.** Point to actual code when identifying quality issues, not abstract descriptions. Check for rationalization — if a test breaks during refactoring, that test was relying on buggy behavior. Investigate and fix the root cause, investigate and fix the root cause.

**Constraint: Guide toward behavior testing.** Always recommend testing observable behavior, not implementation internals. For example:
- ISSUE: Test asserts on private fields → FIX: Test the public behavior that those fields enable
- ISSUE: Test spies on `_getUser()` → FIX: Test what happens when a user exists or doesn't exist
- ISSUE: Test checks exact regex → FIX: Test that validation succeeds/fails for representative inputs

Change only what is needed to fix the failure mode. Consult `references/fix-strategies.md` for language-specific patterns.

**Step 3: Run tests after each fix**

- Run the specific fixed test first to confirm it passes
- Run the full file or package to check for interactions
- If a fix makes a previously-passing test fail, the test was likely depending on buggy behavior — investigate before proceeding

**Gate**: Each fix verified individually. Tests pass after each change.

### Phase 4: VERIFY

**Goal**: Confirm all fixes work together and suite is healthier.

**Step 1**: Run full test suite — all pass

**Step 2**: Verify previously-flaky tests are now deterministic (run 3x if applicable)
- Go: `go test -count=3 -run TestFixed ./...`
- Python: `pytest --count=3 tests/test_fixed.py`
- JS: Run test file 3 times sequentially

**Step 3**: Confirm no test was accidentally deleted or skipped
- Compare test count before and after fixes
- Search for any new `@skip` or `.skip` annotations introduced

**Step 4**: Summary report

```markdown
## Fix Summary
Anti-patterns fixed: [count]
Files modified: [list]
Tests affected: [count]
Suite status: all passing / [details]
Remaining issues: [any deferred items]
```

**Gate**: Full suite passes. All fixes verified. Summary delivered.

---

## Pattern Quality Catalog

See `references/quality-catalog.md` for detailed descriptions of all 10 failure modes (signals, why each is problematic, and fixes).

---

## Error Handling

See `references/error-handling.md` for handling ambiguous patterns, fixes that change test behavior, and suites with hundreds of quality issues.

---

## References

See `references/quick-reference.md` for the quick reference table, red flags during review, and TDD relationship notes.

### Reference Files

- `${CLAUDE_SKILL_DIR}/references/quality-catalog.md`: Detailed descriptions of all 10 failure modes
- `${CLAUDE_SKILL_DIR}/references/error-handling.md`: Ambiguous patterns and large-scale cleanup guidance
- `${CLAUDE_SKILL_DIR}/references/quick-reference.md`: Quick reference table, red flags, TDD relationship
- `${CLAUDE_SKILL_DIR}/references/preferred-pattern-catalog.md`: Detailed code examples for all 10 failure modes (Go, Python, JavaScript)
- `${CLAUDE_SKILL_DIR}/references/fix-strategies.md`: Language-specific fix patterns and tooling
- `${CLAUDE_SKILL_DIR}/references/blind-spot-taxonomy.md`: 6-category taxonomy of what high-coverage test suites commonly miss (concurrency, state, boundaries, security, integration, resilience)
- `${CLAUDE_SKILL_DIR}/references/load-test-scenarios.md`: 6 load test scenario types (smoke, load, stress, spike, soak, breakpoint) with configurations and critical endpoint priorities
