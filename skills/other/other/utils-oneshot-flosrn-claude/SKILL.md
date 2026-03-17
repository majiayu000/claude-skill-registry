---
name: oneshot
description: Ultra-fast feature implementation using Explore → Code → Test workflow. Use when implementing focused features, single tasks, or when speed over completeness is priority.
argument-hint: <feature-description>
---

# OneShot

Implement `$ARGUMENTS` at maximum speed. Ship fast, iterate later.

## Workflow

### 1. EXPLORE (minimal)

Gather minimum viable context:
- Use `Glob` to find 2-3 key files by pattern
- Use `Grep` to search for specific patterns
- Quick `WebSearch` only if library-specific API knowledge needed
- NO exploration tours - find examples/edit targets and move on

### 2. CODE (main phase)

Execute changes immediately:
- Follow existing codebase patterns exactly
- Clear variable/method names over comments
- Stay STRICTLY in scope - change only what's needed
- NO comments unless genuinely complex
- NO refactoring beyond requirements
- Run formatters if available (`npm run format`)

### 3. TEST (validate)

Check quality:
- Run: `npm run lint && npm run typecheck` (or equivalent)
- If fails: fix only what you broke, re-run
- NO full test suite unless explicitly requested

## Output

When complete, return:

```
## Done

**Task:** {what was implemented}
**Files changed:** {list}
**Validation:** ✓ lint ✓ typecheck
```

## Constraints

- ONE task only - no tangential improvements
- NO documentation files unless requested
- NO refactoring outside immediate scope
- NO "while I'm here" additions
- If stuck >2 attempts: report blocker and stop
