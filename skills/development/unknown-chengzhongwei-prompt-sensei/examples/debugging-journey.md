# Example: A Debugging Journey

This example follows one developer improving the same prompt across four iterations over two days. Each iteration applies one habit from the previous session's feedback.

The scenario: a Jest test is failing after adding refresh-token support. The developer is using an AI coding agent to debug it.

---

## Day 1, Attempt 1 — Exploration

**Prompt:**
> fix this test

**Stage:** Exploration
**Score:** 70/100 — Good for Exploration

| Dimension | Score | Note |
|---|---|---|
| Goal Clarity | 2/5 | Implies debugging help but no goal stated |
| Privacy/Safety | 5/5 | No sensitive data |

**Feedback:**
This is a normal starting point when you first notice something is wrong. The problem is that "this test" could be any of the hundreds of tests in the project, and "fix" does not describe whether you want a diagnosis, a patch, or an explanation.

**One habit to practice next:**
Name the specific failing test and describe what you expected vs. what actually happened.

---

## Day 1, Attempt 2 — Diagnosis

After getting a partial response, the developer now has the error output. They try again.

**Prompt:**
> A Jest test is failing. Expected /login, actual /dashboard.

**Stage:** Diagnosis
**Score:** 67/100 — Developing

| Dimension | Score | Note |
|---|---|---|
| Goal Clarity | 3/5 | Symptom is clear; goal (debug? fix? explain?) is not |
| Context Completeness | 2/5 | No file, no test name, no recent change context |
| Privacy/Safety | 5/5 | Clean |

**Feedback:**
Meaningful progress. You added expected vs. actual behavior — that's the most valuable single addition for any debugging prompt. Claude can now at least understand the failure.

What's still missing: which file? Which test? What changed recently that might have caused this?

**One habit to practice next:**
Add the file path and the recent change that might be related.

---

## Day 2, Attempt 3 — Execution

The developer now knows the relevant file and suspects a recent change.

**Prompt:**
> Please debug this failing Jest test. Expected redirect to /login, actual /dashboard.
> Related file: src/__tests__/auth.test.ts
> Recent change: added refresh-token support.
> Do not refactor the whole auth flow.

**Stage:** Execution
**Score:** 60/100 — Developing

| Dimension | Score | Note |
|---|---|---|
| Goal Clarity | 4/5 | Clear outcome |
| Context Completeness | 3/5 | Recent change mentioned; error text still missing |
| Input Boundaries | 3/5 | Test file named; specific test case not named |
| Constraints | 3/5 | One constraint ("don't refactor") |
| Output Format | 2/5 | No structure specified |
| Verification | 1/5 | Not mentioned |
| Privacy/Safety | 5/5 | Clean |

**Feedback:**
This is a solid debugging prompt. Claude can work with this and may get to the root cause. The most useful next habit is verification: name the exact test command or failing assertion that proves the fix worked. Output format can help, but verification matters more here because the prompt already has context, a file, and a scope constraint.

**One habit to practice next:**
Add `Verification: run [test command]` or paste the exact failing assertion.

---

## Day 2, Attempt 4 — Execution (polished)

**Prompt:**
> Please debug this failing Jest test.
>
> Goal:
>   Find why unauthenticated users are redirected to /dashboard instead of /login.
>
> Context:
>   - Stack: TypeScript, React, Jest
>   - Recent change: added refresh-token support
>   - Related files:
>     - src/middleware/auth.ts
>     - src/routes/ProtectedRoute.tsx
>     - src/__tests__/auth.test.ts
>
> Expected:
>   If the user has no access token and no refresh token, redirect to /login.
>
> Actual:
>   The test receives /dashboard.
>
> Constraints:
>   - Do not refactor the whole auth flow
>   - Prefer the smallest safe fix
>   - If the test expectation is wrong, explain why before changing it
>
> Verification:
>   Run npm test src/__tests__/auth.test.ts.
>
> Return:
>   1. Root cause
>   2. Proposed fix
>   3. Patch summary
>   4. Test command
>   5. Edge cases to verify

**Stage:** Execution
**Score:** 94/100 — Excellent

| Dimension | Score | Note |
|---|---|---|
| Goal Clarity | 5/5 | Outcome is specific and verifiable |
| Context Completeness | 5/5 | Stack, change, files, expected, actual |
| Input Boundaries | 4/5 | Three files named (could specify which functions) |
| Constraints | 5/5 | Three constraints, all clear |
| Output Format | 5/5 | Numbered return structure |
| Verification | 5/5 | Exact test command + edge cases requested |
| Privacy/Safety | 5/5 | No sensitive data |

**Feedback:**
Excellent. This is execution-ready. Claude can go directly to the fix with no follow-up questions. The structured return format makes the response easy to review and act on.

---

## What changed

| Attempt | Stage | Key addition | Effect |
|---|---|---|
| 1 → 2 | Exploration → Diagnosis | Expected vs. actual behavior | The problem became diagnosable |
| 2 → 3 | Diagnosis → Execution | File name + constraint | Claude had enough scope to start work |
| 3 → 4 | Execution → Execution | Verification command + output structure | The request became execution-ready |

The score is stage-aware, so it is not always a straight line upward. When the prompt moves from Exploration to Execution, Prompt Sensei applies more dimensions and the bar gets higher. That is intentional: a short exploratory prompt can be reasonable early, while an implementation request needs clearer context, boundaries, and verification.

The three biggest gains came from:
1. Adding expected vs. actual (most impactful single addition for any debugging prompt)
2. Naming the specific file
3. Adding a verification command

Each of those took under 30 seconds to add. Together, they reduce the chance of follow-up clarification and make the result easier to verify. They do not guarantee a one-shot fix, but they give the agent a much cleaner first attempt.

---

## The pattern

Execution-ready debugging prompts tend to include:

```
Goal:        What behavior is wrong?
Context:     Stack, recent change, related files
Expected:    What should happen?
Actual:      What actually happens?
Constraints: What should Claude not touch?
Verification: Test command and edge cases
Return:      Root cause · Fix · Test command · Edge cases
```

Start where you are. Add one element at a time. That is how this prompt moved from a reasonable first signal to an execution-ready request.
