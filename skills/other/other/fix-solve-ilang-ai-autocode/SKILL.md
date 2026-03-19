---
name: fix-solve
description: Three-step method step 3. Fix the problem and verify the fix works.
---

# Solve (三步法 Step 3)

After finding root cause:
1. Write a test that reproduces the bug (if possible)
2. Make the minimal fix — change as little as possible
3. Run the test — confirm it passes
4. Run all other tests — confirm nothing else broke
5. Verify the original symptom is gone

Rules:
- Minimal fix. Don't refactor while fixing.
- If the fix is a one-liner, that's ideal.
- If the fix requires restructuring, discuss with user first.
- After fixing, activate fix-explain to tell user what happened.
