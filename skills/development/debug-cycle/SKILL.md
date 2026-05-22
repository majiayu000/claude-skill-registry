---
name: debug-cycle
description: Universal PDCA debugging framework for systematic hypothesis verification. Use when debugging issues that require structured investigation, observing runtime behavior, or verifying fixes through iterative testing.
---

# Debug Cycle - PDCA Framework

## Overview

A systematic, platform-agnostic approach to debugging using the PDCA (Plan-Do-Check-Act) cycle. This methodology provides a structured workflow for forming hypotheses, adding instrumentation, analyzing behavior, and iterating until root cause identification.

## When to Use

- Debugging issues that require observation of runtime behavior
- Investigating problems that cannot be determined through static analysis alone
- Verifying that a fix actually resolves the issue
- Understanding data flow through complex systems
- Troubleshooting intermittent or timing-related bugs
- Any scenario where "guess and check" has failed

## The PDCA Cycle

### Phase 1: Plan (Hypothesis Formation)

**Objective**: Form a testable hypothesis about the root cause.

**Steps**:
1. **Document the symptom** - Describe the observed behavior precisely
2. **Form a hypothesis** - What specific condition might cause this?
3. **Identify data points** - What values/states would confirm or refute the hypothesis?
4. **Determine instrumentation points** - Where should debug output be added?

**Hypothesis Template**:
```
Symptom: [Precisely what is happening]
Expected: [What should happen instead]
Hypothesis: [Specific cause I believe is responsible]
Data needed: [Values/states to capture]
Instrumentation points: [Files, methods, lines to add logging]
```

**Good vs Bad Hypotheses**:

| Bad (Vague) | Good (Specific) |
|-------------|-----------------|
| "Something is wrong with the data" | "The user ID is null when passed to fetchProfile()" |
| "The UI isn't updating" | "setState is not being called after the API response" |
| "It's slow" | "The database query is executing N+1 times in the loop" |

### Phase 2: Do (Instrument & Build)

**Objective**: Add targeted instrumentation to capture the data needed.

**Steps**:
1. **Add debug logs** at identified points
2. **Include contextual information**:
   - Variable values at decision points
   - Method entry/exit with parameters and return values
   - Which conditional branch was taken
   - State before and after changes
3. **Build and deploy** the instrumented code
4. **Use hot reload/restart** when available for faster iteration

**Log Naming Convention**:
```
[ClassName] methodName: description key=value
```

**Essential Logging Points**:
- Method entry with parameters
- Conditional branch decisions
- Loop iterations (with index/count)
- Exception catch blocks
- State mutations
- Async operation start/complete

### Phase 3: Check (Observe & Analyze)

**Objective**: Collect and analyze data to evaluate the hypothesis.

**Steps**:
1. **Reproduce the scenario** that triggers the issue
2. **Capture all output** - logs, screenshots, error messages
3. **Analyze the data**:
   - Compare actual values vs expected values
   - Identify the exact point where behavior diverges
   - Note any unexpected states, ordering, or timing
4. **Document findings** with evidence

**Analysis Questions**:
- At what point does actual behavior diverge from expected?
- Are there any null/undefined values where data was expected?
- Is the execution order what was expected?
- Are there any race conditions or timing issues?

### Phase 4: Act (Decide Next Action)

**Objective**: Based on analysis, determine the appropriate next step.

**Decision Matrix**:

| Result | Evidence | Action |
|--------|----------|--------|
| Hypothesis CONFIRMED | Logs show exact predicted cause | Implement fix, then verify with new cycle |
| Hypothesis REFUTED | Logs show different behavior than predicted | Form new hypothesis based on actual findings |
| INCONCLUSIVE | Not enough data to determine | Add more granular logging, narrow scope |
| Root cause FOUND & FIXED | Fix applied, issue no longer reproduces | Remove debug logs, document solution |
| New issue DISCOVERED | Logs reveal separate problem | Create new hypothesis for new issue |

## Cycle Iteration Rules

1. **One hypothesis per cycle** - Test only one thing at a time
2. **Narrow, don't widen** - Each cycle should focus on a smaller scope
3. **Evidence-based pivots** - New hypotheses must be based on observed data
4. **Maximum 5 cycles** - If not solved, step back and reconsider approach
5. **Document everything** - Keep a log of all cycles for future reference

## Common Anti-patterns

| Anti-pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| "Shotgun debugging" | Changing multiple things at once | Change one thing, test, repeat |
| "Hypothesis-free" logging | Adding random logs hoping to find something | Form specific hypothesis first |
| "Premature fixing" | Implementing fix before confirming cause | Complete the Check phase first |
| "Ignoring inconclusive" | Assuming no news is good news | Add more instrumentation |
| "Forgetting cleanup" | Leaving debug code in production | Remove logs after resolution |

## Integration with Other Skills

- **debug-log-patterns**: Language-specific logging syntax and patterns
- **mobile-debug-tools**: MCP tools for mobile device interaction and log retrieval

## Quick Reference Card

```
PLAN:  Symptom -> Hypothesis -> Data needed -> Log points
DO:    Add logs -> Build -> Deploy
CHECK: Reproduce -> Capture -> Analyze -> Document
ACT:   Confirmed? -> Fix | Refuted? -> New hypothesis | Unclear? -> More logs
```
