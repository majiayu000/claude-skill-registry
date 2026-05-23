---
name: review-testing
description: Review test code for quality, design, and completeness after implementing a feature or fixing a bug. Use when the user asks to "review my tests", "check my test quality", "are these tests good enough", "review testing", or after completing a feature implementation that includes tests. Also use when tests feel brittle, flaky, or superficial. Cross-references production code to find coverage gaps.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "0.1"
license: MIT
---

You are reviewing test code written alongside a feature implementation or bug fix. Ensure the tests are well-designed, thorough, and maintainable — not just that they pass. Tests that merely mirror implementation details create false confidence and become a maintenance burden during refactoring.

## Review Scope

Identify what to review:

1. **Find changed test files** on the current branch (relative to the base branch).
2. **Find the production code** those tests cover — trace imports, function calls, and file naming conventions to map tests to their targets.
3. **Find related existing tests** for the same modules or functions that weren't changed — these may need updates or reveal gaps.

Read test files first, before production code. If you can infer the feature's requirements and edge cases from the tests alone, that's a sign the tests are well-written. If you need to read the implementation to understand what the tests are doing, that's a finding worth reporting.

## What Makes a Test Valuable

Weigh each test against four qualities:

**Regression protection** — Does this test actually catch bugs? A test that exercises trivial code or skips complex branches protects against nothing. Check: does the test touch business-critical logic, or only verify the happy path of a simple getter?

**Refactoring resilience** — Will this test break when someone restructures code without changing behavior? Tests coupled to internal method names, call sequences, or private state punish every cleanup with false failures, eroding trust in the suite.

**Fast feedback** — Unit tests should run in milliseconds. If a test hits the filesystem, network, or database unnecessarily, that's a design issue. But don't confuse speed with value — an integration test verifying a real database query is better than a fast unit test that mocks everything and verifies nothing.

**Maintainability** — Can someone unfamiliar with this code read the test and understand what it verifies and why? Tests with sprawling setup, cryptic names, or deeply nested mocking fail this check.

## Review Areas

### 1. Assertion Completeness

The most common weakness in generated tests: asserting only the obvious output and missing the full "blast radius" of a state change.

When a test triggers an action, ask what *else* changed. If a test adds an item to a cart, does it only check the item count? Or does it also verify the price calculation, subtotal update, and that other items are unaffected?

**Flag when:**
- A test asserts a return value but ignores side effects
- A test checks that an operation succeeded but not that it produced the right result
- A test verifies the happy path but skips boundary conditions (empty inputs, nulls, maximum values, off-by-one)
- Error-path tests only check that an error was thrown, not the error message, type, or cleanup behavior

### 2. Test Structure

Each test should have exactly one Arrange-Act-Assert cycle. If a test acts and asserts multiple times in sequence, it's testing multiple behaviors and should be split.

**Flag when:**
- A test has multiple act phases (testing a workflow, not a behavior)
- The arrange phase is so large the actual behavior being tested is buried
- Assertions appear inside setup helpers or utility functions (hides what's being verified)
- Test logic contains conditionals or loops — tests should be straight-line code

### 3. Fixture and State Management

How test data is created determines whether the suite is maintainable at scale. **Inline setup** (data created in the test body) is fine for simple tests but painful when constructor signatures change across many tests. **Implicit setup** (shared `beforeEach`/`setUp` blocks) eliminates duplication but obscures what each test actually depends on. **Delegated setup** (factory functions or builders called explicitly) keeps tests readable while centralizing construction logic.

**Flag when:**
- A shared setup block creates objects most tests don't use
- Tests depend on external files, database state, or globals defined elsewhere ("Mystery Guest" — everything a test needs should be visible in its body or one function call away)
- Tests assume resources exist without creating them (files, database records, environment variables)
- Tests mutate shared state without cleanup, causing order-dependent failures

### 4. Mocking Boundaries

Mocks are essential for isolation, but overuse turns tests into mirrors of the implementation.

**The key principle:** mock at architectural boundaries, not at every function call. Use stubs (canned data) for query-type dependencies and mocks (interaction verification) only for commands with side effects like sending emails or writing to external systems.

Respect the codebase's existing mocking convention. Flag inconsistency within the project, not deviation from a universal rule.

**Flag when:**
- A test mocks types it doesn't own (third-party libraries, framework internals) — when the library updates, the mock passes against outdated assumptions. Prefer: thin adapters, real implementations in integration tests, or official testing utilities (MemoryRouter, test databases, in-memory caches).
- Mock density is high — 4+ mock configurations suggests too many responsibilities in the production code
- A test verifies call counts or argument sequences on internal methods (couples the test to *how* the code works, not *what* it does)
- Stubs are being verified (checking a stub was called tests implementation, not behavior)

### 5. Test Smells

| Smell | What It Looks Like | Why It Matters |
|---|---|---|
| **Assertion Roulette** | Multiple assertions with no failure messages | Can't tell which assertion broke without debugging |
| **Eager Test** | One test exercises several unrelated methods | Failures are ambiguous — which behavior broke? |
| **Lazy Test** | Multiple tests call the same method with identical inputs | Redundant maintenance cost, no coverage gain |
| **Sleepy Test** | Hard-coded `sleep()`/`Sys.sleep()`/`setTimeout()` | Flaky in CI, slow everywhere. Use polling or explicit waits. |
| **Rotten Green** | Assertions inside `try`/`tryCatch` or conditional branches | Test always passes because the assertion is never reached |
| **Sensitive Equality** | Asserting against `toString()`/`print()` output | Breaks on formatting changes; assert structural properties instead |
| **Print Statement** | `print()`/`console.log()` instead of assertions | Debugging leftovers that verify nothing |
| **Snapshot Abuse** | Snapshots as a substitute for behavioral assertions | Any change triggers failure, developers blindly update. Good uses: one snapshot of an HTML component's structure (not every prop combination), error message text, CLI output. Bad: snapshotting entire objects or rendering every variant. |
| **Implementation Mirror** | Expected values computed using the same logic as production code | Test and production code will always agree — even when both are wrong. Hardcode expected values from a known-good source. |

### 6. Naming and Readability

Test names should describe behavior, not implementation. A well-named test suite reads like a feature specification.

**Flag when:**
- Test names reference internal method names (e.g., `test_processData_returns_true`) — break on rename
- Test names are generic (`test1`, `test_it_works`, `test_basic`)
- The name doesn't communicate the scenario or expected outcome

Prefer behavioral names: `test_expired_subscription_blocks_access`, `delivery_with_past_date_is_invalid`, `empty_cart_shows_zero_total`.

### 7. Coverage Gaps

Cross-reference production code changes against the test suite:

- Are there branches or conditions no test exercises?
- Are error paths tested? (Not just "does it throw" but "does it throw the right thing and clean up properly")
- Are edge cases covered? (Empty collections, null/NA/None/undefined, boundary values, concurrent access if applicable)
- If production code changed existing behavior, were existing tests updated?

Walk through the implementation and note every decision point — each `if`, `match`, `switch`, error handler, or early return. Check whether the test suite exercises both sides of that decision.

When reviewing R tests using `testthat`, check if the `testing-r-packages` skill is available and invoke it for R-specific conventions and patterns.

## Response Format

```
## Summary
[Overall assessment: How well do these tests protect the codebase?]

## Critical Issues (Blocking)
[Tests that provide false confidence or will cause real problems.]

## Required Changes
[Design problems that weaken the test suite.]

## Strong Suggestions
[Improvements to test quality and maintainability.]

## Noted
[Minor style or convention issues. Mention once, then move on.]

## Verdict
Request Changes | Needs Discussion | Approve

## Next Steps
[Options for proceeding]
```

Use `file:line` references for every finding. Quote the specific test code that demonstrates the issue and show what better code looks like.

## Next Steps

At the end of the review, offer the user these options:

**Discuss and address findings:** Use the AskUserQuestion tool to walk through the issues. Group by severity or topic, offer resolution options, and mark the recommended choice.

**Fix the issues:** Offer to apply fixes directly in priority order — blocking issues first, then required changes, then suggestions. Confirm before continuing after each group.

**Add to a pull request:** When reviewing in context of a PR, offer to post the review as a PR comment. Include attribution: "Review assisted by the [review-testing skill](https://github.com/posit-dev/skills/blob/main/posit-dev/review-testing/SKILL.md)."

If operating as a subagent, skip the next steps and output only the review findings.
