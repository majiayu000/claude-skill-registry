---
name: debugging
description: Use when something is broken — errors, bugs, crashes, exceptions, unexpected behavior, stack traces
user-invokable: false
tier: core
context: fork
agent: epost-debugger

metadata:
  agent-affinity:
    - epost-debugger
    - epost-implementer
  keywords:
    - debug
    - error
    - bug
    - troubleshoot
    - root-cause
    - stack-trace
    - logging
    - crash
    - exception
    - fix
  platforms:
    - all
  connections:
    enhances: [debug, fix, fix-deep, fix-ci, fix-ui]
  triggers:
    - /debug
    - error
    - bug
    - crash
    - exception
---

# Debugging Skill

## Purpose
Systematic debugging methodology.

## When Active
User uses /debug, reports errors.

## Expertise

### Systematic Debugging
1. **Understand**: What's the symptom?
2. **Reproduce**: Can you reproduce it?
3. **Isolate**: What's the minimal case?
4. **Analyze**: What's actually happening?
5. **Hypothesize**: What could cause this?
6. **Verify**: Does the fix work?

### Log Analysis
- Parse error messages
- Follow stack traces
- Identify log patterns
- Contextual logging

### Stack Trace Interpretation
- Read top-down
- Identify root cause frame
- Distinguish cause from symptom
- Async stack traces

### Reproduction Strategies
- Minimal reproduction
- Environment matching
- Data setup
- Step reproduction

### Root Cause Analysis

See `problem-solving` for root cause analysis techniques (5 Whys, bisection, inversion).

### Fix Validation
- Regression testing
- Edge case testing
- Performance impact
- Side effect analysis

## Patterns

### Debug Logging
```typescript
console.log('[Feature]', { variable, state });
console.debug('[Debug]', value);
console.error('[Error]', error);
```

### Error Boundaries
```typescript
class ErrorBoundary extends Component {
  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
  }
}
```

### Debug Mode
```typescript
const DEBUG = process.env.DEBUG === 'true';
if (DEBUG) console.debug('Debug info');
```

### Structured Logging
```typescript
logger.info('User action', {
  action: 'login',
  userId: user.id,
  timestamp: Date.now()
});
```

## Common Issues

### TypeScript
- Type mismatches
- Missing type imports
- Any type issues
- Generic constraints

### React
- Stale closures
- Missing dependencies
- Re-render loops
- State timing

### Async
- Race conditions
- Promise rejection
- Missing await
- Callback hell

## Defense-in-Depth Patterns

### Validation Layers
1. Input validation (reject invalid early)
2. Business logic validation (enforce invariants)
3. Output validation (verify results before return)

### Error Handling Strategy
- **Catch**: Only where you can handle meaningfully
- **Transform**: Convert to domain-specific errors
- **Log**: Include context (not just message)
- **Propagate**: Let upstream handle if you can't

### Assertion vs Exception
- Assertions: Programmer errors (should never happen)
- Exceptions: Runtime problems (can happen legitimately)

### State Diagram Tracing

When debugging **state-related bugs** (unexpected transitions, stuck states, race conditions):

1. **Draw the ACTUAL state machine** from code — read every `if/switch/state=` and extract what ACTUALLY happens
2. **Draw the EXPECTED state machine** from requirements or docs
3. **Overlay and diff** — mismatches reveal the bug:
   - Missing transitions (no path from state A to B)
   - Unguarded transitions (state changes without preconditions)
   - Dead states (reachable but no exit — component gets "stuck")
   - Race conditions (two transitions competing for same state)

```
ACTUAL:   [LOADING] ──(timeout)──▸ [LOADING]     ← stuck! no error path
EXPECTED: [LOADING] ──(timeout)──▸ [ERROR] ──(retry)──▸ [LOADING]
MISSING:  timeout → ERROR transition
```

Applies to: React `useState`/`useReducer`, iOS view lifecycle, Android Compose state, async/Promise chains, WebSocket connections.

See `planning/references/state-machine-guide.md` for notation and common patterns.

## Verification Checklist
- [ ] Symptom reproduced consistently
- [ ] Root cause identified and documented
- [ ] Fix applied and tested
- [ ] No new issues introduced
- [ ] Edge cases considered
- [ ] Similar issues checked elsewhere in codebase

## Tools
- Browser DevTools (breakpoints, profiling)
- Node debugger (--inspect)
- Console logging (structured)
- Source maps (correct line numbers)
- Test suite (regression testing)

## References
- `references/debugging-flow.dot` — Authoritative debugging process flowchart
- `references/condition-based-waiting.md` — Patterns for replacing `sleep()` with condition polling

Use `knowledge-capture` skill to persist learnings after this task.

## Debugging Discipline

> **IRON LAW: NO FIXES WITHOUT ROOT CAUSE FIRST.**
>
> Applying a fix before identifying root cause is not debugging — it is guessing. Guesses compound into technical debt.

See `verification-before-completion` skill for anti-rationalization table, red flags, and the full verification gate protocol.

## Sub-Skill Routing

When this skill is active and user intent matches a sub-skill, delegate:

| Intent | Sub-Skill | When |
|--------|-----------|------|
| Interactive debug | `debug` | `/debug`, "debug this", trace/inspect |
| Fix broken code | `fix` | `/fix`, "fix this", error/crash/failing |
| Fix deeply | `fix-deep` | `/fix-deep`, complex multi-file bugs |
| Fix CI pipeline | `fix-ci` | `/fix-ci`, CI/CD failures, build pipeline |
| Fix UI issues | `fix-ui` | `/fix-ui`, visual bugs, layout broken |

### Related Skills
- `knowledge-base` — Knowledge storage format and `docs/` directory
- `knowledge-capture` — Post-task capture workflow
- `problem-solving` — Root cause analysis techniques
- `error-recovery` — Error handling and recovery patterns
- `verification-before-completion` — Verify fixes before claiming done
- `auto-improvement` — Error metrics auto-captured by session-metrics hook on Stop
