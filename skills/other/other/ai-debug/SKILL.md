---
name: ai-debug
description: "Use when investigating unexpected behavior, test failures, runtime errors, or regressions. Systematic 4-phase diagnosis: symptom analysis, reproduction, root cause, solution."
effort: max
argument-hint: "[error description or file:line]"
---


# Debug

## Purpose

Systematic debugging skill. Four phases, always in order. NEVER fix symptoms -- always find and fix the root cause. After 2 failed fix attempts, escalate to the user.

## When to Use

- Test failures (expected vs actual mismatch)
- Runtime errors (exceptions, crashes, hangs)
- Regressions (worked before, broken now)
- Unexpected behavior (no error, but wrong result)

## Process

### Phase 1: Symptom Analysis (WHAT, WHEN, WHERE)

Gather facts before forming hypotheses:

1. **WHAT**: exact error message, stack trace, log output
2. **WHEN**: always? intermittent? after a specific change? under load?
3. **WHERE**: which file, function, line? which test? which environment?
4. **SINCE WHEN**: `git log --oneline -20` -- what changed recently?

Output: symptom report with all facts classified as KNOWN or SUSPECTED.

### Phase 2: Reproduction (MINIMAL REPRO)

Make the bug reproducible with the smallest possible case:

1. Run the failing test or reproduce the error
2. If not reproducible: document exact conditions and STOP (cannot debug what cannot be reproduced)
3. Strip to minimal repro: remove unrelated code, simplify inputs, isolate the component
4. Confirm: the minimal repro fails consistently

Output: exact command to reproduce the failure.

### Phase 3: Root Cause (WHY)

Apply the 5 Whys to move from symptom to cause:

1. **Why** does it fail? -> [immediate cause]
2. **Why** does that happen? -> [deeper cause]
3. **Why** does that happen? -> [root cause]
   (Continue until you reach a cause you can fix directly)

**Techniques** (use as appropriate):
- **Binary search**: comment out code, add assertions to narrow the location
- **Git bisect**: `git bisect start HEAD <known-good>` to find the breaking commit
- **Print tracing**: add targeted print/log statements at decision points
- **Diff analysis**: `git diff <known-good>..HEAD -- <file>` to see what changed
- **Assumption check**: list every assumption the code makes, verify each one

**Classification**: identify the root cause category:
- Logic error (wrong condition, off-by-one, missing case)
- State corruption (mutation, shared state, race condition)
- Contract violation (caller sends wrong type, missing field)
- Environment (missing dependency, wrong version, config)
- Data (unexpected input, encoding, edge case)

Output: root cause statement (1-2 sentences, specific and testable).

### Phase 4: Solution Design (FIX + REGRESSION TEST)

1. **Design the fix**: minimal change that addresses the root cause
   - Fix the ROOT CAUSE, not the symptom
   - One logical change only
   - If the fix is large, the root cause analysis may be wrong -- revisit Phase 3
2. **Write regression test**: a test that fails without the fix and passes with it
3. **Apply the fix**
4. **Verify**: regression test passes AND all existing tests pass
5. **Check for siblings**: does the same bug pattern exist elsewhere? (`grep` for similar code)

## Escalation Protocol

| Attempt | Action |
|---------|--------|
| 1st fix fails | Try a different approach (not the same thing again) |
| 2nd fix fails | STOP. Escalate to user with: symptom, repro, root cause analysis, 2 approaches tried |

Never retry the same approach. Never loop silently.

## 5 Whys Example

```
Symptom: test_parse_config_handles_empty fails with KeyError
Why 1: config["database"] raises KeyError
Why 2: parse_config returns empty dict when file is empty
Why 3: the YAML parser returns None for empty files, not empty dict
Root cause: missing None -> {} coercion after yaml.safe_load()
Fix: add `config = yaml.safe_load(f) or {}` instead of `config = yaml.safe_load(f)`
```

## Common Mistakes

- Fixing the symptom (add a try/except) instead of the root cause
- Not writing a regression test for the fix
- Guessing without reproducing first
- Changing multiple things at once (change one thing, verify, repeat)
- Retrying the same approach that already failed
- Not checking for sibling bugs (same pattern elsewhere)

## Integration

- **Called by**: `/ai-dispatch` (debug tasks), `ai-build agent` (when tests fail), user directly
- **Calls**: test runners (to reproduce), `/ai-test` (regression test)
- **Transitions to**: `ai-build` (fix implementation), `/ai-commit` (after verified fix)

$ARGUMENTS
