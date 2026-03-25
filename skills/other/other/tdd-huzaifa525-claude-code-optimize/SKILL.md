---
name: tdd
description: Test-Driven Development cycle — write failing test, implement, verify, refactor
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[feature description]"
---

Implement **$ARGUMENTS** using strict TDD.

## Cycle

### 1. RED — Write a Failing Test

- Find existing test files to match the pattern
- Write a test that describes the expected behavior
- Run it — confirm it FAILS
  ```
  [test command]
  ```

### 2. GREEN — Write Minimum Code

- Write the simplest code that makes the test pass
- No extra features, no premature optimization
- Run the test — confirm it PASSES
  ```
  [test command]
  ```

### 3. REFACTOR — Clean Up

- Improve code quality without changing behavior
- Remove duplication, improve naming
- Run ALL tests — confirm nothing broke
  ```
  [test command]
  ```

### 4. REPEAT

If the feature needs more behavior:
- Go back to step 1 with the next test case
- Continue until all requirements from $ARGUMENTS are covered

## Rules

- NEVER write production code without a failing test first
- NEVER write more code than needed to pass the current test
- ALWAYS run tests after every change
- Match existing test file patterns and naming conventions

## Output

After completion, show:
- How many tests were written
- All passing test names
- Files created/modified

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
