---
name: test
context: fork
description: "Run test suites and report pass/fail results. Use when the user asks to execute tests, check whether tests pass, or verify code changes didn't break anything. Triggers: 'run tests', 'check if tests pass', 'verify nothing broke', 'run e2e tests', 'test the endpoints', 'run tests/unit/test_foo.py', 'let me know the results'. This skill executes test commands and reports output — it does NOT write tests, fix tests, explain test code, plan tests, or research testing practices. If the request is about learning, writing, or researching testing rather than executing and reporting, do not use this skill."
argument-hint: what-to-test-and-outcome
---

Think harder.

## Process

### 1. Understand Test Goal

Determine **what to verify** — not just what to run, but what the expected outcome is.
- e.g., "verify the submit button is green" → look for UI/style assertions on that button
- e.g., "auth flow works" → verify login/logout/token behavior end-to-end
- e.g., "run all unit tests" → verify the full suite passes

If argument is provided, use it to understand the goal.
If no argument, auto-determine from recent changes (`git diff`, `git status`) and infer what needs verification.

### 2. Detect Framework & Test Commands

Detect test framework from project config and look for existing test scripts (`Makefile`, `justfile`, `package.json` scripts, `scripts/` directory, `CLAUDE.md`, etc.). Use project-defined commands when available.

### 3. Run Tests
- Execute appropriate test command
- Capture stdout/stderr and timing
- Collect coverage if available

### 5. Report

```
## Test Results

**Target**: {what was tested}
**Status**: {PASS | FAIL}
**Total**: X tests
**Passed**: X | **Failed**: X | **Skipped**: X
**Duration**: Xs

### Failures (if any)
- `test_name`: error message

### Coverage (if available)
- Lines: X%
- Branches: X%
```

## Gotchas

- **Wrong test scope**: Match what the user asked to verify. "Run tests for the auth module" doesn't mean "run all tests."
- **Missing env setup**: Some test suites need env vars, database connections, or build steps first. Check project setup.
- **Treating flaky tests as passes**: If a test passes once after failing, it may be flaky. Note this in the report.
- **Not using project test commands**: Check package.json scripts, Makefile, justfile before running raw test framework commands.

## Constraints

- Run tests only — NO fixes
- Report results accurately, don't minimize failures
- If tests fail, suggest `/fix`
- For browser/UI visual verification, combine with browser skill as well

## Test Target

<target>$ARGUMENTS</target>
