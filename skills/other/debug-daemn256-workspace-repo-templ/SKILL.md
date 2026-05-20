---
name: debug
description: Debug errors, find root causes, and fix failing code.
---

# Debug

The Implementer drives this workflow with Test support. Systematically investigate issues using hypothesis-driven debugging, identify root cause, and implement fixes.

**Prerequisites:** Error description, reproduction steps, or failing test output.

---

## Phase 1: Characterize the Problem

Gather evidence and identify the error.

### Steps

1. Reproduce the error or review the error output
2. Identify the error type, message, and stack trace
3. Note the affected file(s) and line(s)
4. Determine when the issue started (recent change? new environment?)

---

## Phase 2: Hypothesize and Test

Form and test hypotheses about root cause.

### Steps

1. List 2-3 likely root causes based on evidence
2. Rank by likelihood
3. For each hypothesis (most likely first):
   - State the hypothesis clearly
   - Describe the diagnostic step
   - Execute the diagnostic
   - Record the result — confirm or eliminate

### Common Root Cause Patterns

| Pattern              | Diagnostic                               |
| -------------------- | ---------------------------------------- |
| Null/undefined       | Trace data flow to find missing value    |
| Race condition       | Check async ordering, add logging        |
| Configuration error  | Compare expected vs actual config values |
| Dependency mismatch  | Check version compatibility              |
| State mutation       | Track state changes through flow         |
| Missing error handle | Check for uncaught exceptions            |

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** Hypothesize

## Hypotheses

| #   | Hypothesis   | Likelihood   | Evidence For | Evidence Against |
| --- | ------------ | ------------ | ------------ | ---------------- |
| 1   | <hypothesis> | High/Med/Low | <evidence>   | <evidence>       |

## Root Cause

**Confirmed hypothesis:** <which one>
**Explanation:** <why this is the cause>

## Next Step

Propose and implement fix.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not implement a fix until root cause is confirmed and approved.

---

## Phase 3: Fix and Verify

Implement the minimal fix and verify.

### Steps

1. Make the minimal change that addresses the root cause
2. Add or update tests to cover the failure case
3. Confirm the original error no longer occurs
4. Run related tests to check for regressions

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>

## Fix Applied

<description of the change>

## Verification

- [ ] Original error resolved
- [ ] Tests pass
- [ ] No regressions introduced

## Next Step

<commit the fix / create PR>

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human approves:

- Fix is correct and minimal
- Verification confirms the issue is resolved
- No regressions introduced

---

## Error Handling

| Situation                   | Recovery                                           |
| --------------------------- | -------------------------------------------------- |
| Cannot reproduce            | Gather more context, check environment differences |
| Multiple root causes        | Address each separately, prioritize by impact      |
| Fix introduces new failures | Revert, re-analyze with new information            |
| Root cause is external      | Document workaround, file upstream issue           |
