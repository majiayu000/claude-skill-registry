---
name: test-audit
description: Zero-assumption test suite audit. Measures real confidence, not coverage percentage. Finds tests that test nothing, tests that test mocks, tests that give false confidence, and the critical paths with no tests at all. Coverage is a number. This skill tells you if that number means anything.
user-invocable: true
argument-hint: "[test directory, specific test files, or 'full suite']"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- 90% coverage with 0% edge case coverage is 0% useful coverage.
- A green test suite that doesn't cover failure modes is a confidence trick.
- Tests that break on every refactor test the implementation, not the behavior. They're maintenance cost disguised as safety.
- The most dangerous test is the one that passes when the code is wrong.
- "We have tests" is not the same as "we have confidence." Prove the difference.

## What you're measuring

You are not measuring coverage percentage. You are measuring **real confidence** — the probability that a bug in production would have been caught by this test suite before shipping.

A suite with 40% coverage that tests every error path in the payment service provides more confidence than a suite with 95% coverage that only tests happy paths and trivial getters.

## Audit process

### 1. Inventory the test suite

Before evaluating quality, understand the shape:

- **Test runner and framework** — what's configured, what version
- **Test count** — total, by type (unit, integration, e2e)
- **Test location pattern** — co-located, separate directory, both
- **Run time** — total suite time, slowest tests
- **Flaky tests** — any known or suspected
- **Coverage config** — is it measured? Thresholds? Enforced in CI?

### 2. Map tests to risk

For each major module/service in the codebase:

| Module | Risk level | Test count | Test quality | Confidence |
|---|---|---|---|---|
| Payment service | Critical | X | (below) | High/Med/Low |
| Auth middleware | Critical | X | | |
| User API | High | X | | |
| Utils | Low | X | | |

**Risk-weighted coverage** matters more than raw coverage. 0 tests on payment code is worse than 0 tests on a date formatter.

### 3. Classify every test file

For each test file, classify:

**Valuable tests** — test real behavior, would catch real bugs, survive refactors.

**Decoration tests** — exist for coverage numbers but catch nothing. Signs:
- Only test the happy path
- Assert that a function "was called" but not what it did
- Assert on implementation details (internal state, method call order)
- Test framework behavior, not application behavior
- Snapshot tests with no human review process

**False confidence tests** — worse than no tests because they make people think code is verified. Signs:
- Mock everything including the thing being tested
- Assert on mock return values (testing your setup, not your code)
- Pass even when the underlying code is broken
- Catch-all assertions (`expect(result).toBeTruthy()`)

**Maintenance burden tests** — break on every refactor, slow the suite, add friction. Signs:
- Tightly coupled to implementation details
- Brittle selectors/locators in UI tests
- Slow (>5s per test) without justification
- Duplicate existing test coverage

**Tests that should be deleted** — actively harmful. Removing them improves the suite.

### 4. Identify critical gaps

The most important part of the audit. What's NOT tested that SHOULD be:

- **Error paths** — what happens when things fail? Network errors, validation failures, auth rejection, timeout, malformed data
- **Edge cases** — empty inputs, boundary values, concurrent access, race conditions
- **Security paths** — auth bypass, privilege escalation, injection, IDOR
- **Data integrity** — what happens on partial failure, duplicate submission, stale reads
- **Integration seams** — where modules meet, where data changes shape, where trust boundaries exist

### 5. Evaluate test infrastructure

- **Factories/fixtures** — do they exist? Are they maintained? Do they reflect real data or fantasy data?
- **Test database** — real or mocked? If mocked, what's the divergence risk?
- **CI integration** — do tests run on every PR? Is there a quality gate? Can tests be skipped?
- **Flakiness** — is there a flaky test tracker? What's the rerun rate? Flaky tests erode trust in the entire suite.

## Per-test-file evaluation

For each test file worth examining:

- **What it claims to test** (from describe/context blocks)
- **What it actually tests** (from assertions)
- **What it misses** (paths not covered)
- **Mock health** — are mocks accurate? Do they drift from real implementations?
- **Assertion quality** — specific or vague? Behavior or implementation?
- **Verdict:** Valuable / Decoration / False confidence / Delete

## Output format

### Test suite health

| Metric | Value |
|---|---|
| Total tests | X |
| Valuable tests | X (Y%) |
| Decoration tests | X (Y%) |
| False confidence tests | X (Y%) |
| Tests to delete | X (Y%) |
| Suite run time | Xs |
| Flaky tests | X known |
| Real confidence level | High / Medium / Low / False |

### Risk-weighted coverage

| Module | Risk | Tests | Quality | Confidence | Verdict |
|---|---|---|---|---|---|
| (name) | Critical/High/Med/Low | count | Valuable/Mixed/Decoration | High/Med/Low | (action) |

### Critical gaps

The paths with no test coverage that have the highest blast radius. Each gap includes:

- **What's untested** — specific behavior/path
- **Why it matters** — what breaks if this path has a bug
- **Blast radius** — function → module → service → user-facing
- **Suggested test** — one-line description of the test that should exist

### False confidence report

Tests that are actively misleading. Each includes:

- **File:line** — the test
- **What it claims to verify** — from the test name/description
- **Why it doesn't** — what makes it a false positive
- **Verdict:** Fix or Delete

### Tests to delete

Specific tests that make the suite worse by existing. File:line, why they should go.

### Test infrastructure assessment

Factories, fixtures, mocking patterns, CI integration, flakiness. What's working, what's broken.

### Devil's advocate

For your harshest verdicts: could there be context you're missing? Were these tests valuable once and rotted? Is the team aware and choosing to accept the debt?

### What I didn't check

Types of testing I couldn't evaluate (e2e, performance, visual regression, manual QA processes).

### Recommended test plan

Priority-ordered list of tests to write, grouped by:

1. **Stop the bleeding** — tests for critical untested paths
2. **Build confidence** — tests that replace false confidence with real confidence
3. **Clean up** — tests to delete, mocks to replace, flakiness to fix
