---
name: test
description: |
  Use this skill to run tests, identify failures, and fix them. Triggered by
  "run tests", "fix failing tests", "make tests pass", or "/test".
argument-hint: "[file or pattern]"
allowed-tools: "Bash, Read, Edit, Grep, Glob"
---

# Test Runner & Fixer

Run the test suite and automatically fix any failures.

## Current Test Status

!`npm test -- --passWithNoTests 2>&1 | tail -30`

## Instructions

1. Run the tests (filtered to `$ARGUMENTS` if provided):
   ```bash
   npm test $ARGUMENTS
   # or: pytest $ARGUMENTS
   # or: go test ./...
   # or: cargo test
   ```

2. For each failing test:
   a. Read the test file to understand what's being tested
   b. Read the source file being tested
   c. Identify the root cause (test wrong? source wrong? missing mock?)
   d. Fix the root cause — **prefer fixing source bugs over changing tests**
   e. Only update a test if it's clearly wrong or testing the wrong thing

3. Re-run tests to confirm they pass

4. If tests still fail after 2 attempts at fixing, report:
   - The exact error message
   - What you tried
   - Your hypothesis for the root cause
   - Ask the user how to proceed

## Rules

- Never delete tests to make them "pass"
- Never change assertions to match wrong behavior
- Do NOT mock the database in integration tests
- Run the full suite at the end to check for regressions
- If adding new tests, follow the existing test file structure

$ARGUMENTS
