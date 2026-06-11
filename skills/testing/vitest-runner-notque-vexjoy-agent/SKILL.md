---
name: vitest-runner
description: "Run Vitest tests and parse results into actionable output."
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - "run vitest"
    - "JavaScript tests"
    - "TypeScript tests"
    - "vite tests"
    - "vitest output"
  category: testing
  pairs_with:
    - test-driven-development
    - typescript-check
    - e2e-testing
---

# Vitest Test Runner Skill

## Overview

This skill runs Vitest tests and parses results into actionable reports. It executes tests in non-interactive mode, extracts failure details (test name, assertion error, stack trace), and organizes results by test file with timing information. Use this skill when tests need to run and results need structured, complete reporting—not when tests need installation, creation, modification, or auto-fixing.

---

## Instructions

### Step 1: Verify Vitest Project

Before running tests, confirm Vitest is installed and configured. Why: Running tests in a non-Vitest project wastes time and produces misleading results. This skill is designed only for Vitest—not Jest, Mocha, or Playwright.

Verify vitest is available:

```bash
# Check for vitest configuration
ls vitest.config.* vite.config.* 2>/dev/null
grep -q "vitest" package.json && echo "vitest found in package.json"
```

If no vitest configuration found, stop and inform the user. Do not attempt to install dependencies or configure Vitest—that is outside this skill's scope.

### Step 2: Run Tests in Non-Interactive Mode

Execute Vitest using the `run` subcommand (not bare `npx vitest`, which starts interactive watch mode and will never complete in a non-interactive shell). Why: Watch mode is interactive and incompatible with automation. The `run` mode executes all tests once and exits with a status code reflecting pass/fail.

Default execution:

```bash
npx vitest run --reporter=verbose 2>&1
```

For specific files or patterns (optional behavior):

```bash
npx vitest run path/to/test.ts 2>&1
npx vitest run --grep "pattern" 2>&1
```

For coverage reporting (when user requests coverage):

```bash
npx vitest run --coverage 2>&1
```

### Step 3: Respect Exit Codes and Parse Complete Output

Capture the full exit code and output. Why: The exit code is the source of truth for pass/fail—code 0 = pass, nonzero = fail. Never assume tests passed based on partial output. Show all failures completely, including test names, assertion errors, and stack traces. Hiding failures prevents users from fixing them.

Extract for each test:
- **Test file**: Path to the test file
- **Test name**: Full test path (describe > it)
- **Status**: PASS / FAIL / SKIP
- **Duration**: Time taken
- **Error detail**: Complete assertion error and stack trace for failures (do not abbreviate)

### Step 4: Format Results as Structured Report

Present output in a format that groups failures by test file and includes complete error details. Why: Users need to see which tests failed, why they failed, and where in the code the assertions failed—this prevents wasted debugging time.

Example format:

```
=== Vitest Test Results ===

Status: PASS / FAIL (X passed, Y failed, Z skipped)

Failures:
---------
FAIL src/utils/__tests__/helpers.test.ts > parseData > handles null input
  AssertionError: expected null to equal { data: [] }
  - Expected: { data: [] }
  + Received: null
  at src/utils/__tests__/helpers.test.ts:25:10

Summary:
--------
Test Files: 12 passed, 2 failed (14 total)
Tests:      45 passed, 3 failed, 2 skipped (50 total)
Duration:   4.23s
```

---

## Error Handling

### Error: "Cannot find vitest"
Cause: Vitest not installed or node_modules missing
Constraint: This skill does not install dependencies; it assumes a fully configured Vitest project.
Solution: Advise user to check `grep vitest package.json` for presence, then run `npm install` or `npm install -D vitest`. After installation, re-run this skill.

### Error: "No test files found"
Cause: Test file patterns don't match vitest.config include/exclude globs
Constraint: Test discovery is driven by Vitest's configuration; this skill does not modify vitest.config.ts.
Solution: Verify test files exist with correct naming (*.test.ts, *.spec.ts, *.test.js, etc.) and match the patterns in vitest.config include/exclude. Show user the vitest.config.ts to help them debug the mismatch.

### Error: "Test environment not found"
Cause: Missing jsdom or happy-dom dependency for DOM tests
Constraint: This skill does not install dependencies or modify configurations.
Solution: Check vitest.config.ts environment setting (likely `environment: 'jsdom'` or `'happy-dom'`). Advise user to install the required devDependency: `npm install -D jsdom` or `npm install -D happy-dom`, or `@testing-library/jest-dom` for additional matchers.

### Error: "Out of memory" (large test suites)
Cause: Too many tests running in shared thread pool
Constraint: This skill runs all tests in the suite; it does not pre-filter by complexity.
Solution: When memory errors occur, advise user to split test execution: run tests in batches by directory (e.g., `npx vitest run src/unit/`), use `--pool=forks` for memory isolation, or use `--shard=1/N` to split the suite across N shards. The user controls which tests to run; this skill respects that choice.

---

## References

- [Verification Checklist](../shared-patterns/verification-checklist.md) - Pre-completion checks
- [Anti-Rationalization](../shared-patterns/anti-rationalization-core.md) - Prevents shortcut rationalizations

### Key Constraints (Inline with Workflow)

**Constraint: Do not auto-fix tests.** This skill's role is to report test failures completely, not to fix them. The test may be correct and the implementation wrong—only the user knows. Changing test assertions to make them pass would hide real bugs and violate the skill's scope.

**Constraint: Always use `npx vitest run`, not bare `npx vitest`.** Watch mode is interactive and incompatible with non-interactive execution. The skill must use `run` mode to ensure tests execute once and exit with a status code.

**Constraint: Show all failures completely.** Reporting "3 tests failed" without showing which tests or why wastes user time. Stack traces, assertion details, and test names are essential for debugging. Never abbreviate failure output.

**Constraint: Respect exit codes as source of truth.** The process exit code (0 = pass, nonzero = fail) is the definitive signal. Do not rely on partial output or assumptions about test results.
