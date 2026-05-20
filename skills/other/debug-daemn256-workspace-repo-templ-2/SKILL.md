---
name: debug
description: Debug errors, find root causes, and fix failing code
---

# Debug

Uses **Implementer** (primary) with **Test** support. Systematically investigate issues using hypothesis-driven debugging, identify root cause, and implement fixes.

**Prerequisites:** Error description, reproduction steps, or failing test output

---

## Phase 1: Characterize the Problem

### Gather Evidence

1. Reproduce the error or review the error output
2. Identify the error type, message, and stack trace
3. Note the affected file(s) and line(s)
4. Determine when the issue started (recent change? new environment?)

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title> (if applicable)
- **Phase:** 1 — Characterize

## Problem Summary

**Error:** <error message>
**Location:** <file:line>
**Reproduction:** <how to trigger>

## Initial Observations

- <observation 1>
- <observation 2>

## Next Step

Form hypotheses about root cause.

**Approval Required:** No
```

---

## Phase 2: Hypothesize and Test

### Form Hypotheses

1. List 2-3 likely root causes based on evidence
2. Rank by likelihood
3. For each hypothesis, identify what evidence would confirm or refute it

### Test Hypotheses

For each hypothesis (most likely first):

1. State the hypothesis clearly
2. Describe the diagnostic step
3. Execute the diagnostic (read code, add logging, run test)
4. Record the result
5. Confirm or eliminate the hypothesis

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
- **Phase:** 2 — Hypothesize

## Hypotheses

| #   | Hypothesis   | Likelihood   | Evidence For | Evidence Against |
| --- | ------------ | ------------ | ------------ | ---------------- |
| 1   | <hypothesis> | High/Med/Low | <evidence>   | <evidence>       |
| 2   | <hypothesis> | High/Med/Low | <evidence>   | <evidence>       |

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

### Implement Fix

1. Make the minimal change that addresses the root cause
2. Avoid changing unrelated code
3. Add or update tests to cover the failure case

### Verify

1. Confirm the original error no longer occurs
2. Run related tests to check for regressions
3. Review the fix for side effects

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 3 — Fix

## Root Cause

<confirmed root cause>

## Fix Applied

<description of the change>

## Verification

- [ ] Original error resolved
- [ ] Tests pass
- [ ] No regressions introduced

## Next Step

<commit the fix / create PR / further investigation>

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
