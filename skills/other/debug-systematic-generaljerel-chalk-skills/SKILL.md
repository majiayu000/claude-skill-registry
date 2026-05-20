---
name: debug-systematic
description: Apply a systematic four-phase debugging workflow when the user asks to debug an issue, investigate a bug, troubleshoot a problem, or find the root cause of unexpected behavior
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[bug description, error message, or issue number]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: debugging, troubleshooting, code
---

# Systematic Debugging

## Overview

Apply a structured four-phase debugging workflow -- Reproduce, Isolate, Root-cause, Verify -- to systematically find and fix bugs. This approach prevents shotgun debugging (randomly changing things) and ensures the fix addresses the root cause, not just the symptoms.

## Workflow

### Phase 1: Reproduce

Before fixing anything, confirm the bug exists and capture the exact conditions.

1. **Understand the report** -- From `$ARGUMENTS` and conversation context, extract:
   - What is the expected behavior?
   - What is the actual behavior?
   - What are the steps to reproduce?
   - In what environment does it occur (browser, OS, Node version, etc.)?
   - How consistently does it reproduce (always, intermittently, only under load)?

2. **Read project context** -- Check `.chalk/docs/engineering/` for:
   - Architecture docs to understand the affected subsystem
   - Known issues or debugging guides
   - Test infrastructure to understand how to reproduce in a test

3. **Reproduce the bug** -- Try to trigger the bug:
   - If there are existing tests, check if any test covers this case -- if so, does it pass or fail?
   - If no tests cover it, write a failing test that demonstrates the bug (this becomes the regression test)
   - If the bug is environment-specific, note the exact environment conditions
   - If the bug is intermittent, identify what makes it intermittent (timing, data, concurrency)

4. **Document the reproduction** -- Record:
   - Exact steps to reproduce
   - Exact error message or incorrect output
   - Expected correct behavior
   - Whether a failing test was written

**Phase 1 exit criteria**: You can trigger the bug reliably, or you have documented the intermittent conditions. You have a failing test or a manual reproduction procedure.

### Phase 2: Isolate

Narrow the problem space to the smallest possible area of code.

5. **Identify the subsystem** -- Based on the error or behavior:
   - Read the stack trace (if available) to identify the failing function and call chain
   - If no stack trace, trace the data flow from input to the point where incorrect output appears
   - Use Grep to find the relevant code paths

6. **Binary search for the boundary** -- Systematically narrow:
   - **By time**: Use `git log` and `git bisect` to find the commit that introduced the bug. Run: `git log --oneline --since="2 weeks ago" -- <path>` to find recent changes in the affected area.
   - **By code path**: Add logging or assertions at midpoints to determine where correct behavior becomes incorrect
   - **By data**: If the bug only occurs with certain inputs, identify the smallest input that triggers it
   - **By component**: If the system has layers (API -> Service -> DB), check each boundary to find where the bug lives

7. **Narrow to the specific function** -- Once the subsystem is identified:
   - Read the function(s) in full, including all callers and callees
   - Read the tests for these functions
   - Check recent changes to these functions: `git log --oneline -10 -- <file>`
   - Check if the function has any known edge cases documented in comments

**Phase 2 exit criteria**: You know the specific function(s) where the bug occurs. You can point to the exact lines of code involved.

### Phase 3: Root-Cause

Distinguish the symptom from the actual cause. Apply the 5 Whys.

8. **Apply the 5 Whys** -- Start with the symptom and ask "Why?" repeatedly:
   ```
   Symptom: Users get a 500 error when uploading large files
   Why? The upload handler throws an OutOfMemoryError
   Why? The entire file is loaded into memory before processing
   Why? The streaming parser was not used for multipart uploads
   Why? The original implementation used a simple body parser that buffers
   Why? The feature was built as a prototype and never updated for production use
   Root cause: Missing streaming implementation for file uploads
   ```

   Usually 3-5 iterations reaches the root cause. Stop when you reach something you can fix.

9. **Verify it is the root cause, not a symptom** -- Ask yourself:
   - If I fix this, will the bug be gone permanently, or will it resurface under different conditions?
   - Is this the *only* place this pattern exists, or is the same mistake elsewhere?
   - Did the code ever work correctly? If so, what changed?

10. **Check for the same pattern elsewhere** -- Use Grep to search for:
    - The same coding pattern that caused the bug
    - Similar functions that might have the same issue
    - Other callers of the same underlying function
    - Document any additional instances found

**Phase 3 exit criteria**: You can explain the root cause clearly (not just "this line is wrong" but *why* it is wrong). You have checked for the same pattern elsewhere.

### Phase 4: Verify

Fix the bug and confirm the fix is correct and complete.

11. **Implement the fix** -- Fix the root cause, not the symptom:
    - If the root cause is in function A but the symptom appears in function B, fix function A
    - If the same pattern exists elsewhere, fix all instances (or create a shared abstraction that prevents the pattern)
    - Keep the fix minimal -- do not refactor unrelated code in the same change

12. **Verify with the reproduction test** -- The failing test from Phase 1 must now pass:
    - Run the specific test that reproduces the bug
    - If the test still fails, the fix is incomplete -- go back to Phase 3
    - If the test passes, run the full test suite to check for regressions

13. **Write a regression test** -- If you did not write a test in Phase 1, write one now:
    - The test must fail without the fix and pass with it
    - The test should test the root cause, not just the symptom
    - Include edge cases discovered during debugging

14. **Check for collateral damage** -- Verify the fix does not break other things:
    - Run the full test suite
    - If the fix changes a shared function, check all callers
    - If the fix changes data handling, verify with different data shapes

15. **Document** -- Summarize the debugging session:
    - What was the bug (symptom)?
    - What was the root cause?
    - What was the fix?
    - What other instances of the same pattern were found and fixed?
    - What regression test was added?

## Debugging Strategy Decision Tree

```
Do you have an error message or stack trace?
├── Yes
│   ├── Read the stack trace bottom-up
│   ├── Identify the first frame in YOUR code (not library code)
│   ├── Read that function and its inputs
│   └── Is the error in your code or in how you call a library?
│       ├── Your code → Read the function, check inputs
│       └── Library call → Check docs for correct usage, version changes
└── No (silent incorrect behavior)
    ├── Can you add logging to trace the data flow?
    │   ├── Yes → Add logging at key boundaries, reproduce, read logs
    │   └── No → Use a debugger with breakpoints
    ├── Did this ever work correctly?
    │   ├── Yes → Use git bisect to find the breaking commit
    │   └── No → This is a design issue, not a regression
    └── Is it intermittent?
        ├── Yes → Likely a concurrency, timing, or data-dependent issue
        │   ├── Check for race conditions (shared mutable state)
        │   ├── Check for timing assumptions (timeouts, ordering)
        │   └── Check for data assumptions (null, empty, unicode, large)
        └── No → Follow the deterministic debugging path above
```

## Common Root Cause Categories

| Category | Symptoms | Investigation Approach |
|----------|----------|----------------------|
| **Off-by-one** | Wrong number of items, missing first/last element | Check loop bounds, array indexing, pagination |
| **Null/undefined access** | TypeError, NullPointerException | Trace where the value should be set, check all code paths |
| **Race condition** | Intermittent failures, works in debugger but not in production | Look for shared mutable state, missing locks, async ordering assumptions |
| **Type coercion** | Wrong comparisons, unexpected truthiness | Check `==` vs `===`, string-to-number conversions, falsy values |
| **Stale state** | Correct on first run, wrong after update | Check caching, memoization, state mutation, closure captures |
| **Missing error handling** | Silent failures, incomplete operations | Check for missing try/catch, unhandled promise rejections, ignored return values |
| **Environment difference** | Works locally, fails in CI/production | Check env vars, file paths, timezone, locale, dependency versions |
| **Data assumption** | Works with test data, fails with real data | Check for unicode, special chars, empty strings, very large values, null |

## Git Bisect Quick Reference

When you know the bug was introduced recently:

```bash
# Start bisect
git bisect start

# Mark current (broken) commit as bad
git bisect bad

# Mark a known good commit (e.g., last release tag)
git bisect good v1.2.0

# Git checks out a middle commit. Test it.
# If the bug exists at this commit:
git bisect bad

# If the bug does not exist at this commit:
git bisect good

# Repeat until git identifies the first bad commit
# When done:
git bisect reset
```

For automated bisect with a test script:

```bash
git bisect start HEAD v1.2.0
git bisect run npm test -- --filter="test-that-reproduces-bug"
```

## Anti-patterns

- **Fixing symptoms, not causes** -- If users get a 500 error because of a null pointer, adding a null check is fixing the symptom. The root cause is why the value was null in the first place. Null checks are appropriate only when null is a legitimate state. Ask: "Why was this null?" and fix *that*.
- **Not writing a regression test** -- Every bug fix must include a test that would have caught the bug. If the bug recurs in 6 months because there is no test, the debugging time was wasted. The test is part of the fix, not optional.
- **Not checking for the same pattern elsewhere** -- If a null pointer bug was caused by not checking the return value of `findUser()`, grep for all other callers of `findUser()`. The same mistake likely exists elsewhere. Fix all instances, not just the one that was reported.
- **Shotgun debugging** -- Changing things randomly until the bug seems to go away is not debugging. It produces fragile fixes that mask the real issue and often introduce new bugs. Follow the four phases systematically.
- **Debugging in production** -- Unless the bug only reproduces in production (and cannot be reproduced locally even with production data and config), debug locally. Production debugging is slow, risky, and noisy. Reproduce locally first.
- **Skipping Phase 1 (Reproduce)** -- "I think I know what the problem is" leads to fixing the wrong thing. Always reproduce first. If you cannot reproduce it, you cannot verify the fix.
- **Refactoring during a bugfix** -- The bugfix commit should contain only the fix and its regression test. Refactoring muddies the commit history and makes it harder to revert if the fix causes issues. Refactor in a separate commit.
- **Assuming a single cause** -- Complex bugs sometimes have multiple contributing causes. If the fix seems too simple for the symptoms, question whether you have found all the causes.
