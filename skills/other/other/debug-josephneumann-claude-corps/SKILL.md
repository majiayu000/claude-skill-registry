---
name: debug
description: "Use when facing a bug, test failure, or unexpected behavior that isn't immediately obvious"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
---

# Systematic Debugging

**Iron Law**: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

## Phase 1: Reproduce & Isolate

- Reproduce the failure reliably before anything else
- Isolate the smallest failing case
- If you can't reproduce it, you can't fix it
- Record the exact command, input, and output that demonstrates the failure

## Phase 2: Root Cause Trace

- Read the actual code path. Don't guess from memory.
- Form hypotheses about the cause
- Trace data flow from input to failure point
- Check recent changes in the area: `git log --oneline -10 -- <file>`

## Phase 3: Hypothesis Testing

- Test one variable at a time
- Predict the outcome BEFORE running each test
- If your prediction is wrong, update your mental model — don't just try the next thing
- Write down: "I expect X because Y." Run it. Was X correct?

## Phase 4: Minimal Fix

- Fix the root cause, not the symptom
- Verify the fix addresses the actual cause (not just suppressing the error)
- Run the original failing test to confirm
- Run the full test suite to check for regressions

## Three-Strikes Rule

If 3+ attempted fixes have failed, STOP. You are likely wrong about the root cause. Go back to Phase 2 and re-read the code path from scratch. Question your assumptions about the architecture.

## Red Flags

If you catch yourself thinking any of these, STOP:

- "Let me just try..." — You're guessing, not tracing.
- "Maybe if I..." — Form a hypothesis and predict the outcome first.
- "This might work..." — Why would it work? What's your evidence?

## Anti-Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Let me try a quick fix first" | Quick fixes without root cause analysis create new bugs. |
| "I know what the problem is" | Then state your hypothesis and predict the test outcome. |
| "It works now after my change" | Correlation is not causation. Verify your fix addresses the root cause. |

## Post-Debug

After resolution, if the root cause was non-obvious, save debugging insights to auto-memory.

*Adapted from obra/superpowers systematic-debugging skill. Source: https://github.com/obra/superpowers*
