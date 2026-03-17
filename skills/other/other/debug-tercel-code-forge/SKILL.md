---
name: debug
description: >
  Use when encountering any bug, test failure, or unexpected behavior — enforces
  root cause investigation before fixes. Prevents symptom-fixing, masking bugs, and
  "just try this" approaches. For code-forge features, use code-forge:fixbug instead.
---

# Code Forge — Debug

Systematic root cause debugging for any technical issue.

## When to Use

- Any test failure, bug report, or unexpected behavior
- Performance degradation, build failures, integration issues
- ESPECIALLY when under time pressure or when "one quick fix" seems obvious

**For code-forge features:** Use `/code-forge:fixbug` instead — it adds upstream document tracing and state tracking on top of this methodology.

## Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

No "let me just try this." No "obvious fix." No guessing. Investigate first.

## Workflow

```
Root Cause Investigation → Pattern Analysis → Hypothesis Testing → Implementation (TDD fix)
```

## Four Phases

Complete each phase before moving to the next.

### Phase 1: Root Cause Investigation

1. **Read error messages carefully** — complete messages, not skimmed
2. **Reproduce consistently** — can you trigger it reliably?
3. **Check recent changes** — `git diff`, `git log` for what changed
4. **Gather evidence** — add diagnostic instrumentation at each boundary in multi-component systems
5. **Trace data flow backward** — from the error, walk back through the call chain

### Phase 2: Pattern Analysis

1. **Find working examples** — is there a similar feature that works?
2. **Compare against references** — read reference code COMPLETELY, not skimmed
3. **Identify differences** — list EVERY difference between working and broken
4. **Understand dependencies** — what does this code depend on? What depends on it?

### Phase 3: Hypothesis and Testing

1. **Form a single hypothesis** — state it clearly, write it down, be specific
2. **Test minimally** — smallest possible change that tests the hypothesis
3. **One variable at a time** — never change multiple things simultaneously
4. **Verify before continuing** — did the test confirm or refute the hypothesis?

If you don't know: **say so.** Don't pretend. "I don't understand why X happens" is valuable information.

### Phase 4: Implementation

1. **Create a failing test case first** — use TDD (see code-forge:tdd)
2. **Implement a single fix** — ONE change, not "while I'm here" improvements
3. **Verify the fix worked** — run the test, confirm it passes
4. **Run the full test suite** — ensure no regressions

### When Fixes Fail

Count your fix attempts:
- **< 3 attempts:** Return to Phase 1, gather more evidence
- **>= 3 attempts:** **STOP.** This is NOT a hypothesis failure — it's likely a **wrong architecture** or **wrong mental model.** Discuss with the user before proceeding.

## Example

```
Bug: "UserService.getProfile() returns null for valid user IDs"

Phase 1 — Investigate:
  $ grep -r "getProfile" src/  →  found in UserService.ts:42, UserController.ts:15
  $ git log --oneline -5 src/services/UserService.ts  →  recent refactor changed query

Phase 2 — Compare:
  Working: getById() uses parameterized query with $1
  Broken:  getProfile() concatenates id into string (bug introduced in refactor)

Phase 3 — Hypothesis:
  "getProfile builds wrong SQL — id is treated as string, not integer"
  Test: hardcode known id=1 → returns null. Confirmed.

Phase 4 — Fix:
  Write test: expect(getProfile(1)).resolves.toMatchObject({id: 1})
  Fix: use parameterized query ($1) instead of string interpolation
  Verify: test passes, full suite 42/42 green
```

## Decision Rules

Apply these checks before acting:

| If you're about to... | Instead... | Why |
|----------------------|-----------|-----|
| Skip Phase 1 because the cause seems obvious | Run Phase 1 anyway — it will be fast if you're right | Obvious causes are often symptoms of deeper issues |
| Apply a fix without reproducing first | Reproduce the bug with a reliable trigger | A fix you can't verify is not a fix |
| Revert to a working state without understanding | Investigate WHY it broke, then fix | Blind reverts leave the root cause active |
| Trust the error message at face value | Trace backward from the error through the call chain | Error messages point to symptoms, not causes |
| Add logging everywhere | Add targeted logging at component boundaries only | Shotgun logging creates noise and obscures signal |
| Try the same approach again | STOP after 3 failed attempts — reassess your mental model | Repeated failure means wrong diagnosis, not wrong execution |

## Hard Stops

Halt and reassess if:
- You've attempted the same fix approach 3+ times
- You're adding workarounds instead of addressing the root issue
- You're suppressing or swallowing errors to make tests pass
- You're making changes without a specific hypothesis to test
- The fix is growing larger than the feature it supports
