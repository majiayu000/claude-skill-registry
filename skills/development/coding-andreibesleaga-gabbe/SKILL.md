---
name: debug
description: Systematic root-cause debugging — reproduce, isolate, hypothesize, fix with TDD
triggers: [bug, error, fix, broken, crash, exception, not working, unexpected behavior, regression]
context_cost: medium
---

# Debug Skill

## Goal
Find the root cause of a bug through systematic investigation, not trial-and-error. Fix it using TDD (write the failing test that reproduces the bug first, then fix the code).

## Steps

1. **Fill the bug report** (or read existing one)
   - Use templates/core/BUG_REPORT_TEMPLATE.md if not already filled
   - Gather: exact error message, stack trace, reproduction steps, environment

2. **Reproduce the bug reliably**
   - Create a minimal reproduction case
   - If you can't reproduce it: ask for more information (environment, data, user actions)
   - Note: if the bug is intermittent, identify the conditions that trigger it

3. **Write the failing test FIRST** (TDD for bugs)
   ```typescript
   // tests/bug/issue-42-null-user.test.ts
   test('should not crash when user is null in payment processor', () => {
     // This test should reproduce the exact bug scenario
     expect(() => processPayment(null, { amount: 100 })).not.toThrow();
     // OR: expect the correct error handling behavior
   });
   ```
   - Run the test — it MUST FAIL (reproducing the bug)
   - This is your regression test that ensures the bug never returns

4. **Isolate the fault**
   - Read the stack trace from bottom up (the bottom frames are your code, top is the error)
   - Add logging at the entry point of the failing function
   - Binary search: narrow down which function/line causes the issue
   - Check: what data enters the function vs what data should enter

5. **Classify the bug type**
   - **Null/undefined:** Missing validation, unexpected null input
   - **Logic error:** Wrong condition, off-by-one, incorrect algorithm
   - **Race condition:** Async operations in wrong order, missing await
   - **Data shape mismatch:** API response changed, schema migration issue
   - **State mutation:** Shared mutable state, missing deep clone
   - **Environment difference:** Works in dev, fails in prod (env vars, DB state)
   - **Dependency change:** Library upgrade changed behavior

6. **Hypothesize the root cause**
   - State your hypothesis explicitly: "I believe the bug is caused by [X] because [evidence]"
   - Test the hypothesis: add a breakpoint/log to verify
   - If hypothesis is wrong: revise and re-hypothesize

7. **Implement the fix**
   - Fix the root cause, not the symptom
   - Minimal change — don't refactor while fixing a bug
   - Common fix patterns:
     - Add null/undefined guards at entry points
     - Add missing await
     - Fix wrong conditional logic
     - Add missing error handling

8. **Verify the fix**
   - Run the regression test from Step 3 → must now PASS
   - Run the full test suite → must still pass (no new regressions)
   - Verify in the environment where the bug was reported (if possible)

9. **Add documentation / prevent recurrence**
   - Add code comment explaining WHY the fix is needed (not what it does)
   - If the bug was caused by a missing test: add the test to the permanent test suite
   - If the bug was caused by a common mistake: add to agents/memory/CONTINUITY.md

10. **Log to AUDIT_LOG.md**
    - Entry: what the bug was, what the root cause was, what the fix was

## Constraints
- NEVER fix a bug without a failing test that reproduces it first
- NEVER change more code than necessary to fix the bug
- If the bug requires an architectural change to fix properly: escalate to human
- If you cannot reproduce the bug after 3 attempts: escalate to human with detailed report

## Output Format
Fixed code + regression test. Report: "Bug fixed. Root cause: [X]. Regression test added at [path]. All [N] tests passing."
