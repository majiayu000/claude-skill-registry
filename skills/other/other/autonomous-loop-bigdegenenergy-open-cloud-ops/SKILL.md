---
name: autonomous-loop
description: Autonomous development loop patterns for iterative self-improvement. Auto-triggers when implementing features autonomously, fixing bugs in a loop, or running until completion. Based on frankbria/ralph-claude-code.
---

# Autonomous Development Loop

Based on [@ghuntley's Ralph technique](https://github.com/frankbria/ralph-claude-code) for Claude Code.

> **For full autonomous mode, use `/ralph`.** This skill provides the underlying patterns.

## Core Principle: Dual-Condition Exit Gate

**Never exit prematurely.** Exit requires BOTH conditions:

1. **Completion Indicators ≥ 2** - Heuristic detection from your work
2. **Explicit EXIT_SIGNAL: true** - Your conscious declaration

**If only ONE is true → KEEP GOING**

This innovation (introduced in ralph-claude-code v0.9.9) prevents false exits when completion language appears during productive work.

## Completion Indicators

Count how many apply each loop:

| Indicator         | Pattern                                    |
| ----------------- | ------------------------------------------ |
| Tests passing     | 100% pass rate                             |
| Fix plan complete | All `- [ ]` → `- [x]`                      |
| "Done" language   | "done", "complete", "finished"             |
| "Nothing to do"   | "no changes needed", "already implemented" |
| "Ready" language  | "ready for review", "ready to merge"       |
| No errors         | Zero execution errors                      |

**Need ≥2 indicators + explicit EXIT_SIGNAL: true to exit**

## Circuit Breaker Pattern

Track your own progress and halt when stuck:

| State         | Condition                | Action             |
| ------------- | ------------------------ | ------------------ |
| **CLOSED**    | Normal operation         | Continue executing |
| **HALF_OPEN** | 2 loops without progress | Increase scrutiny  |
| **OPEN**      | Threshold exceeded       | HALT immediately   |

### Halt Thresholds

| Trigger           | Threshold     | Meaning             |
| ----------------- | ------------- | ------------------- |
| No progress loops | 3 consecutive | Spinning wheels     |
| Identical errors  | 5 consecutive | Stuck on same issue |
| Test-only loops   | 3 consecutive | Not implementing    |
| Output decline    | >70% drop     | Something's wrong   |

## Progress Detection

Track mentally each loop:

- **Files modified** (0 = no progress)
- **Tests changed** (pass/fail delta)
- **Tasks completed** (fix plan updates)
- **Errors encountered** (same vs different)

## Structured Status Reporting

**Every response MUST end with:**

```
## Status Report

STATUS: IN_PROGRESS | COMPLETE | BLOCKED
LOOP: [N]
CIRCUIT: CLOSED | HALF_OPEN | OPEN
EXIT_SIGNAL: false | true

TASKS_COMPLETED: [what you finished]
FILES_MODIFIED: [count and list]
TESTS: [X/Y passing]
ERRORS: [count or "none"]

PROGRESS_INDICATORS:
- [x] Files changed this loop
- [ ] Tests improved
- [ ] Tasks marked complete
- [ ] No repeated errors

NEXT: [next action or "done"]
```

## Exit Signal Checklist

Before setting `EXIT_SIGNAL: true`, verify ALL:

```
□ All fix_plan.md items complete (or task done if no plan)
□ All tests passing (or code works if no tests)
□ No execution errors
□ All requirements implemented
□ No meaningful work remaining
```

**If ANY unchecked → EXIT_SIGNAL: false**

## Work Focus Hierarchy

| Activity             | Effort | Priority        |
| -------------------- | ------ | --------------- |
| **Implementation**   | 60-70% | PRIMARY         |
| **Testing**          | 15-20% | Secondary       |
| **Fix Plan Updates** | 5-10%  | Tracking        |
| **Documentation**    | 0-5%   | Only if needed  |
| **Cleanup**          | 0-10%  | After core work |

## Anti-Patterns to Avoid

- **Premature exit**: Tests pass but tasks remain
- **Infinite loops**: Not detecting repeated failures
- **Busy work**: Testing without implementing
- **Silent failures**: Not reporting errors clearly
- **Scope creep**: Adding unplanned work
- **Analysis paralysis**: Over-researching instead of implementing

## Fix Plan Integration

Maintain `fix_plan.md`:

```markdown
## High Priority

- [ ] Critical task

## Medium Priority

- [ ] Supporting task

## Completed

- [x] Done item
```

**Empty fix plan + passing tests = consider exit**

## Example: Why Dual-Gate Matters

```
Loop 5:
  Output: "Auth complete! Moving to sessions."
  Indicators: 3 (tests pass, "complete", no errors)
  EXIT_SIGNAL: false (Claude continuing)
  Result: CONTINUE ✅ (respects intent)

Loop 8:
  Output: "All done, tests green, ready for review."
  Indicators: 4 (all signals present)
  EXIT_SIGNAL: true (Claude done)
  Result: EXIT ✅ (both conditions met)
```

## Recovery Protocols

### If BLOCKED

1. State: "I am blocked because [reason]"
2. List what you tried (min 2 approaches)
3. Suggest alternatives
4. Set STATUS: BLOCKED, EXIT_SIGNAL: false
5. Wait for input

### If Circuit Breaker OPENS

1. State: "Circuit breaker OPEN - halting"
2. Summarize accomplishments
3. Describe stagnation pattern
4. Set CIRCUIT: OPEN, EXIT_SIGNAL: false
5. Recommend next steps

**Never infinite loop on a blocker.**
