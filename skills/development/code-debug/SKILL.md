---
name: code-debug
description: Systematic debugging with root cause tracing. Use when encountering bugs, test failures, or unexpected behavior - find root cause before attempting fixes, trace backward through call chain.
---

# Systematic Debugging

Random fixes waste time and create new bugs.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

---

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

---

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures

**Use ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- You don't fully understand the issue

---

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - If not reproducible, gather more data

3. **Check Recent Changes**
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Trace Data Flow Backward**
   - Where does the bad value originate?
   - What called this with the bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

5. **Multi-Component Systems**
   Add diagnostic instrumentation at each boundary:
   - Log what enters/exits each component
   - Verify environment/config propagation
   - Run once to gather evidence WHERE it breaks

### Phase 2: Pattern Analysis

1. **Find Working Examples** - Similar working code in same codebase
2. **Compare Against References** - Read reference implementations completely
3. **Identify Differences** - List every difference, however small
4. **Understand Dependencies** - Settings, config, environment, assumptions

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** - "I think X is the root cause because Y"
2. **Test Minimally** - Smallest possible change, one variable at a time
3. **Verify Before Continuing** - Worked? Phase 4. Didn't work? New hypothesis.
4. **When You Don't Know** - Say so. Ask for help. Research more.

### Phase 4: Implementation

1. **Create Failing Test Case** - Simplest possible reproduction
2. **Implement Single Fix** - ONE change at a time, no bundled improvements
3. **Verify Fix** - Test passes? No regressions?

**If fix doesn't work:**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1 with new information
- If >= 3: STOP and question the architecture

### When 3+ Fixes Fail

Pattern indicating architectural problem:
- Each fix reveals new shared state/coupling
- Fixes require "massive refactoring"
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Should we refactor architecture vs. continue fixing symptoms?
- Discuss with user before attempting more fixes

---

## Root Cause Tracing

When bugs manifest deep in the call stack:

1. **Observe the Symptom** - What error occurred?
2. **Find Immediate Cause** - What code directly causes this?
3. **Ask: What Called This?** - Trace up the call chain
4. **Keep Tracing Up** - What value was passed? Where did it come from?
5. **Find Original Trigger** - The source, not the symptom

**Adding Stack Traces:**
```
stack = capture_stack_trace()
log("DEBUG operation:", {
  input_value,
  current_directory,
  environment,
  stack
})
```

**NEVER fix just where the error appears.** Trace back to find the original trigger.

---

## Red Flags - STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)

**ALL of these mean:** STOP. Return to Phase 1.

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too. |
| "Emergency, no time" | Systematic is FASTER than thrashing. |
| "Just try this first" | First fix sets the pattern. Do it right. |
| "I see the problem" | Seeing symptoms != understanding root cause. |
| "One more fix attempt" | 3+ failures = architectural problem. |

---

## Integration

**Use with:**
- `code-test` - Write failing test to reproduce bug before fixing
- `completion-verify` - Verify fix actually worked before claiming done

---

## Reference

- [defense-in-depth.md](reference/defense-in-depth.md) - Multi-layer validation patterns
- [root-cause-tracing.md](reference/root-cause-tracing.md) - Detailed tracing techniques
