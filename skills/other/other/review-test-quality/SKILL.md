---
name: review-test-quality
description: Audit AHK test suite for drifted copies, dead tests, and design issues
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit the AHK test suite for quality issues. Use maximum parallelism — spawn explore agents for independent test files.

**Scope**: AHK tests only — unit tests, GUI tests, live tests, lifecycle tests in `tests/`. NOT static analysis checks, NOT query tools, NOT test coverage (this is about quality of existing tests, not finding gaps).

## Priority Issue — Production Code Copies

This is the highest-priority defect. Past reviews have found tests that copy-paste production logic into the test file instead of `#Include`-ing the production file. These tests always pass because they test the copy, not production. When production changes, the copy doesn't update — the test is useless.

**Detection pattern**: A test file that defines a function with the same name as a production function, but does NOT `#Include` the production file containing it. The test's "function" is a frozen copy.

For each test file, check:
1. What production files does it `#Include`?
2. Does it define any functions that shadow production functions? (Compare against `query_function_visibility.ps1` to find the real definition)
3. Is the test calling real production code, or its own copy?

A test that defines **mocks** (GUI rendering, IPC sends, DWM calls) is fine — that's intentional shadowing per `testing.md`. The problem is when **business logic** is copied instead of included.

## Other Quality Issues

### Dead tests
Tests that can never fail regardless of production behavior:
- Assertions that test hardcoded values against themselves
- Tests that set up state and assert on the setup, not on production function output
- Tests where the "expected" value is computed by the same logic being tested

### Duplicative tests
Multiple tests verifying the exact same behavior:
- Same function called with same inputs and same assertions, in different test files
- A unit test and a live test that test identical logic (the unit test is sufficient for pure logic; the live test should test integration aspects the unit test can't)

### Broken assertions
Tests that appear to assert but don't actually fail on wrong values:
- Missing `TestErrors++` after a failed comparison
- Conditions that log `FAIL` but don't increment the error counter
- Assertions comparing wrong variables (e.g., comparing input to input instead of input to output)

### Stale tests
Tests for features or code paths that no longer exist:
- Tests for removed functions (function deleted from production, test still "passes" because it tests its own copy or mock)
- Tests for old behavior that was intentionally changed

## Constraints

The test suite is designed for **automated agentic execution** — no user interaction. Any suggested modifications must follow existing patterns from `test_utils.ahk` and respect the parallel, timing-critical design. See `testing.md` for the full pattern guide.

## Validation

After explore agents report back, **validate every finding yourself**. Test quality issues are subtle — what looks like a copy may actually be an intentional mock, and what looks dead may test an edge case.

For each candidate:

1. **Cite evidence**: "I verified by reading `test_file.ahk` lines X–Y and `production_file.ahk` lines A–B" — show both sides.
2. **Trace the test path**: Does the test call the real production function, or a local copy? Use `query_function_visibility.ps1` to confirm where the function is defined.
3. **Counter-argument**: "What would make this test valuable despite appearances?" — Is it testing a subtle edge case? Is the "copy" actually an intentional mock? Would removing it lose coverage of an important path?
4. **Observed vs inferred**: Did you confirm the test calls a copy (by reading both files), or infer it from the absence of an `#Include`?

## Plan Format

**Section 1 — Production code copies** (highest priority):

| Test File | Lines | Function Copied | Production Source | Fix |
|-----------|-------|----------------|------------------|-----|
| `test_foo.ahk` | 10–25 | `CalculateScore()` | `src/shared/scoring.ahk:42` | Replace copy with `#Include`, add mock for GUI dependency |

**Section 2 — Dead/broken tests**:

| Test File | Lines | Issue | Evidence | Fix |
|-----------|-------|-------|----------|-----|
| `test_bar.ahk` | 88–95 | Asserts setup value, not production output | Expected value is hardcoded `3`, same as setup | Rewrite to call production function and assert result |

**Section 3 — Duplicative tests**:

| Test A | Test B | Overlap | Recommendation |
|--------|--------|---------|---------------|
| `test_unit_x.ahk:30` | `test_live_y.ahk:55` | Both test `ParseConfig()` with same inputs | Keep unit test, refocus live test on integration behavior |

**Section 4 — Stale tests** (testing removed features):

| Test File | Lines | What It Tests | Status | Fix |
|-----------|-------|--------------|--------|-----|
| `test_old.ahk` | 1–50 | `LegacyFormat()` — removed in v0.7 | Always passes (tests own copy) | Delete |

Order by impact: production copies first (actively hiding bugs), then dead tests, then duplicative, then stale.

Ignore any existing plans — create a fresh one.
