---
name: systematic-debugging
description: "Four-phase debugging: root cause → patterns → hypothesis → implement. For complex bugs, test failures, multi-component issues. NOT for obvious syntax errors."
context: fork
inputs:
  - { from: any, field: error_message, required: false }
  - { from: any, field: reproduction_steps, required: false }
outputs:
  - { field: root_cause, type: string }
  - { field: fix_applied, type: boolean }
next_skills: [pop-test-driven-development, pop-root-cause-tracing]
workflow:
  id: systematic-debugging
  version: 1
  steps:
    [
      { id: initial_triage },
      { id: issue_type_decision },
      { id: phase1_investigate },
      { id: phase2_patterns },
      { id: root_cause_decision },
      { id: phase3_hypothesis },
      { id: phase4_implement },
    ]
---

# Systematic Debugging

Random fixes waste time. Quick patches mask issues.

**Core principle:** ALWAYS find root cause before fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION
```

## When to Use

ANY technical issue: test failures, bugs, unexpected behavior, performance, builds, integration.

**ESPECIALLY when:**

- Under time pressure
- "Just one quick fix" seems obvious
- Already tried multiple fixes
- Previous fix didn't work
- Don't fully understand issue

**Don't skip when:**

- Seems simple (simple bugs have root causes)
- You're hurrying (systematic is faster than thrashing)
- Manager wants NOW (systematic prevents rework)

## Four Phases

### Phase 1: Root Cause Investigation

**For test failures, check flakiness FIRST:**

```
Test fails → Run 5x
├─ Passes 5/5: Not flaky, investigate as bug
├─ Fails 5/5: Consistent, investigate as bug
└─ Mixed (3/5): FLAKY TEST - fix test first
```

**Flaky test checklist:**

| Check                 | How                      | Fix                     |
| --------------------- | ------------------------ | ----------------------- |
| Isolated/connected?   | Run single vs suite      | State pollution         |
| Timing-dependent?     | Look for timeouts/sleeps | Condition-based waiting |
| Environment-specific? | CI vs local              | Mock env vars           |
| Order-dependent?      | Different order          | Setup/teardown          |
| Race condition?       | Async without waits      | Proper async/await      |

**Then continue:**

1. **Read Errors Carefully** - Stack traces, line numbers, error codes
2. **Reproduce Consistently** - Exact steps, happens every time?
3. **Check Recent Changes** - Git diff, dependencies, config
4. **Multi-Component Systems** - Add diagnostic instrumentation at boundaries BEFORE proposing fixes
5. **Trace Data Flow** - Where does bad value originate? (See pop-root-cause-tracing)

### Phase 2: Pattern Analysis

1. **Find Working Examples** - Similar code that works
2. **Compare References** - Read reference implementations COMPLETELY
3. **Identify Differences** - List ALL differences
4. **Understand Dependencies** - Config, environment, assumptions

### Phase 3: Hypothesis & Testing

1. **Form Single Hypothesis** - "I think X causes Y because Z"
2. **Test Minimally** - Smallest change, one variable
3. **Verify** - Worked? → Phase 4. Didn't? → New hypothesis
4. **When Unknown** - Say "I don't understand X", ask for help

### Phase 4: Implementation

1. **Create Failing Test** - Use test-driven-development skill
2. **Implement Single Fix** - Address root cause, ONE change
3. **Verify Fix** - Test passes, no other tests broken
4. **If Fix Doesn't Work**
   - STOP. Count fixes tried.
   - If < 3: Return to Phase 1 with new info
   - **If >= 3: STOP. Question architecture** (see below)
5. **If 3+ Fixes Failed: Question Architecture**
   - Each fix reveals new problems elsewhere
   - Fixes require "massive refactoring"
   - Pattern fundamentally unsound?
   - Discuss with user before more fixes

## Red Flags

STOP if thinking:

- "Quick fix for now"
- "Just try X and see"
- "Add multiple changes"
- "Skip test, manually verify"
- "It's probably X"
- "Don't fully understand but..."
- "One more fix" (after 2+)

**ALL → Return to Phase 1**

**3+ failures → Question architecture**

## Quick Reference

| Phase         | Key Activities                          | Success               |
| ------------- | --------------------------------------- | --------------------- |
| 1. Root Cause | Read errors, reproduce, gather evidence | Understand WHAT & WHY |
| 2. Pattern    | Find working examples, compare          | Identify differences  |
| 3. Hypothesis | Form theory, test minimally             | Confirmed or new      |
| 4. Implement  | Test, fix, verify                       | Resolved, tests pass  |

## Real-World Impact

- Systematic: 15-30min to fix, 95% first-time success, near-zero new bugs
- Random: 2-3h thrashing, 40% success, common new bugs

## Cross-References

- **Flaky tests:** pop-test-driven-development (Condition-Based Waiting)
- **Root cause tracing:** pop-root-cause-tracing (backward tracing)
- **Defense:** pop-defense-in-depth (multi-layer validation)

## Examples

See `examples/` for:

- `flaky-test-patterns.md` - Common flaky test causes & fixes
- `debugging-flowchart.pdf` - Visual decision tree
- `multi-component-diagnostic.md` - Instrumentation strategy
