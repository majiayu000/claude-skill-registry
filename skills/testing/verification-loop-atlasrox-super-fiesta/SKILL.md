---
name: verification-loop
description: Rigorous protocol for verifying code correctness before considering a task complete.
---

# ✅ Verification Loop Protocol

**Goal**: Ensure zero regressions and 100% functional correctness for every change.

## 📝 The Instruction
**When to run**: After writing code, but **BEFORE** asking the user for review.

**Protocol Steps**:

1.  **Define Success State**:
    *   What exactly should happen if this works? (e.g., "The API returns 200 OK with JSON X").
    *   What should *not* happen? (e.g., "The server should not crash on null input").

2.  **Reproduction / Test Creation**:
    *   **Case A (Bug Fix)**: Create a minimal reproduction script that fails *before* your fix and passes *after*.
    *   **Case B (New Feature)**: Write a unit/integration test covering the happy path AND one edge case.

3.  **Execute & Observe**:
    *   Run the test using `run_command`.
    *   **CRITICAL**: Do not assume it passed. Read the output closely.
    *   If it failed, analyze the error, fix the code, and GOTO Step 2.

4.  **Regression Check**:
    *   Run related existing tests (e.g., `npm test tests/related-file.js`).
    *   If you broke something, FIX IT.

5.  **Self-Correction**:
    *   "Did I leave any `console.log`?"
    *   "Did I leave any TODOs?"
    *   "Is the code style consistent?" (Check `rules/coding-style.md`).

6.  **Final Output**:
    *   Only when all checks pass, report to the user:
    *   "Verification Passed: [Test Name]✅"

## 🔍 Troubleshooting
*   **"Tests are flaky"**: Investigate concurrency or shared state. Fix the test, don't ignore it.
*   **"I can't run tests"**: Create a small standalone script (e.g., `verify-fix.js`) and run that with `node`.

***
*Trust, but verify.*
