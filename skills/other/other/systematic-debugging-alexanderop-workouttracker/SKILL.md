---
name: systematic-debugging
description: |
  Systematic debugging framework for any bug, test failure, or unexpected behavior.
  Use BEFORE proposing fixes. Triggers: "bug", "test failure", "flaky test", "debugging",
  "root cause", "investigate", "why is this failing", "unexpected behavior", "not working",
  "broken", "error", "fix this", "what's wrong".
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures (unit, integration, browser mode)
- Flaky tests (pass sometimes, fail under load)
- Vue reactivity issues
- Dexie/IndexedDB problems
- Build failures
- Type errors

**Use ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Full stack traces, not just the first line
   - Vitest output includes file paths and line numbers
   - TypeScript errors show the full type mismatch

2. **Reproduce Consistently**
   ```bash
   # Run specific test
   pnpm test src/features/workout/__tests__/specific.test.ts

   # Run with verbose output
   pnpm test --reporter=verbose
   ```

3. **Check Recent Changes**
   ```bash
   git diff HEAD~5 --stat
   git log --oneline -10
   ```

4. **Gather Evidence in Multi-Component Systems**

   For Vue/Dexie issues, trace through layers:
   ```
   Component → Composable → Repository → Dexie → IndexedDB
   ```

   Add console.error at each layer to find where it breaks.

5. **Trace Data Flow**

   See `references/root-cause-tracing.md` for the complete technique.

### Phase 2: Pattern Analysis

1. **Find Working Examples**
   - Similar working tests in the codebase
   - Same component patterns that work

2. **Compare Against References**
   - Check `testing-conventions` skill for test patterns
   - Check `vue-integration-testing` for browser mode patterns
   - Check `repository-pattern` for Dexie patterns

3. **Identify Differences**
   - What's different between working and broken?
   - Missing `await`? Missing `resetDatabase()`?
   - Wrong query priority (getByRole vs getByTestId)?

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis**
   - "I think X is the root cause because Y"
   - Write it down, be specific

2. **Test Minimally**
   - ONE change at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes -> Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

### Phase 4: Implementation

1. **Create Failing Test Case**
   - Use `vue-integration-testing` skill patterns
   - Query priority: getByRole > getByText > getByTestId

2. **Implement Single Fix**
   - ONE change addressing root cause
   - No "while I'm here" improvements

3. **Verify Fix**
   ```bash
   pnpm test           # All tests pass
   pnpm type-check     # No type errors
   pnpm lint           # No lint errors
   ```

4. **If Fix Doesn't Work**
   - STOP after 3 failed attempts
   - Question the architecture, not just the symptom
   - Discuss with user before attempting more fixes

## Common Issues in This Stack

### Flaky Tests

**Symptom:** Test passes sometimes, fails in CI or under load.

**Common causes:**
- Missing `await` on async operations
- Using arbitrary timeouts instead of `expect.poll()`
- Test isolation issues (missing `resetDatabase()`)
- Race conditions in Vue reactivity

**See:** `references/condition-based-waiting.md`

### Database Isolation Failures

**Symptom:** Test passes alone, fails when run with others.

**Root cause:** Data from other tests polluting state.

**Fix pattern:**
```ts
beforeEach(async () => {
  await resetDatabase()  // ALWAYS first
})
```

**See:** `references/defense-in-depth.md`

### Vue Reactivity Issues

**Symptom:** State updates but UI doesn't reflect changes.

**Debug pattern:**
```ts
import { nextTick } from 'vue'

// After state change
await nextTick()
// Now check DOM
```

## Red Flags - STOP and Follow Process

If you think:
- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "Add multiple changes, run tests"
- "I don't fully understand but this might work"

**STOP. Return to Phase 1.**

## Related Skills

- `testing-conventions` - Query priority, expect.poll(), gotchas
- `vue-integration-testing` - Page objects, browser mode patterns
- `vitest-mocking` - Test doubles and mocking patterns
- `repository-pattern` - Dexie/database patterns

## Supporting Techniques

In `references/` directory:
- `root-cause-tracing.md` - Trace bugs backward through call stack
- `defense-in-depth.md` - Validate at multiple layers
- `condition-based-waiting.md` - Replace timeouts with expect.poll()

In `scripts/` directory:
- `find-polluter.sh` - Find which test creates pollution

## Quick Reference

| Phase | Activities | Success Criteria |
|-------|------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |
