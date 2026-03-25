---
name: refactor
description: Refactor code while preserving behavior — reads tests first, refactors, verifies tests pass
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[what to refactor]"
---

Refactor: **$ARGUMENTS**

## Rules

- NEVER change behavior — only improve structure
- ALWAYS run tests before AND after
- Make small, incremental changes
- Each change should be independently verifiable

## Steps

1. **Run tests first** — establish baseline
   ```
   [test command]
   ```
   If tests fail BEFORE refactoring, STOP and tell the user.

2. **Read the code** to refactor and understand it fully

3. **Read the tests** for this code — understand what behavior is expected

4. **Identify refactoring opportunities:**
   - Extract method (function too long)
   - Extract variable (complex expression)
   - Rename for clarity
   - Remove duplication (DRY)
   - Simplify conditionals
   - Replace magic numbers with constants
   - Reduce nesting depth
   - Split large files
   - Improve type safety

5. **Apply changes incrementally**
   - One refactoring at a time
   - Run tests after each change
   - If tests fail, revert immediately

6. **Run full test suite**
   ```
   [test command]
   ```

7. **Report**
   ```
   ## Refactoring Summary

   ### Changes
   - [what was refactored and why]

   ### Before → After
   - [specific improvements]

   ### Tests
   - All [X] tests passing
   - No behavior changes
   ```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
