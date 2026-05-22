---
name: tdd
description: Use when the user wants test-driven development, asks to write tests first, or mentions TDD.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[feature description]"
---

Implement **$ARGUMENTS** using strict TDD.

## Iron Laws

> **1. No production code exists without a failing test.**
> If you write code before a test, DELETE it. Not "keep as reference." Not "adapt it." DELETE it.
>
> **2. Write the MINIMUM code to pass the test.**
> If the test passes, STOP writing code. More code = more bugs = more maintenance.
>
> **3. Delete means delete.**
> If you wrote code before the test: don't keep it as reference, don't paste it somewhere, don't look at it. Delete it and write the test first. Your memory of the solution will make reimplementation fast.

## Cycle

### 1. RED — Write a Failing Test

- Find existing test files to match the naming pattern
- Write ONE test that describes ONE specific behavior
- Run it — confirm it **FAILS**
  ```
  [test command]
  ```
- If it passes without new code, your test is wrong — it's testing something that already exists

### 2. GREEN — Write Minimum Code

- Write the **simplest possible code** that makes the test pass
- No extra features, no "while I'm here" additions, no premature optimization
- Run the test — confirm it **PASSES**
  ```
  [test command]
  ```

### 3. REFACTOR — Clean Up

- Improve code quality **without changing behavior**
- Remove duplication, improve naming, simplify logic
- Run **ALL tests** — confirm nothing broke
  ```
  [test command]
  ```

### 4. REPEAT

If the feature needs more behavior:
- Go back to step 1 with the next test case
- Continue until all requirements from $ARGUMENTS are covered
- Each cycle should be small: one test, one behavior

## Anti-Rationalization

| Excuse | Rebuttal |
|--------|----------|
| "I already know the implementation, writing a test first is wasteful" | The test isn't just for verification — it's a specification. Write it. |
| "This is too simple to need TDD" | Simple code is the EASIEST to TDD. No excuse to skip it. |
| "I'll write the tests after" | Tests written after code are weaker — they test what you wrote, not what you should have written. |
| "The test framework isn't set up yet" | Set it up. That's step 0, not a reason to skip testing. |
| "I wrote code first but I can just add a test now" | Delete the code. Write the test. Watch it fail. THEN rewrite the code. This is the discipline. |
| "I need to see the implementation to know what to test" | You need to see the REQUIREMENTS to know what to test. Read the spec, not the code. |
| "Refactoring isn't needed for this small change" | Small changes accumulate. Refactor now while context is fresh. |

## Red Flags (you're doing it wrong if...)

- You wrote more than 10 lines of production code before running a test
- Your test passes on the first run without new code
- You're "refactoring" by adding new features
- You have untested edge cases and you're moving to the next feature
- You wrote multiple tests before writing any production code (write one at a time)

## Output

After completion, show:
- How many RED-GREEN-REFACTOR cycles completed
- All passing test names
- Files created/modified
- Any remaining edge cases not yet covered

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
