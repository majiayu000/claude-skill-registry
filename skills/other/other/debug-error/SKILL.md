---
name: debug-error
description: Analyze an error message or stack trace, find root cause, and implement fix
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "[error message or description]"
---

Debug and fix: **$ARGUMENTS**

## Steps

1. **Parse the error**
   - Identify error type (runtime, compile, type, network, etc.)
   - Extract file paths and line numbers from stack trace
   - Identify the error message

2. **Find the source**
   - Read the file(s) mentioned in the stack trace
   - If no stack trace, Grep for the error message in codebase
   - Read surrounding code to understand context

3. **Trace the root cause**
   - Follow the call chain backwards
   - Check recent git changes that might have caused it:
     ```
     git log --oneline -10
     git diff HEAD~3
     ```
   - Look for common causes: null/undefined, wrong types, missing imports, race conditions

4. **Implement the fix**
   - Fix the root cause, not just the symptom
   - Handle edge cases that led to the error

5. **Verify**
   - Run the failing scenario
   - Run related tests
   - Check for similar patterns elsewhere:
     ```
     grep -r "similar_pattern" src/
     ```

6. **Report**
   ```
   ## Bug Fix Report

   ### Error
   [original error]

   ### Root Cause
   [why it happened]

   ### Fix
   [what was changed and why]

   ### Files Modified
   - [file] — [change]

   ### Verified
   - [how it was tested]
   ```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
