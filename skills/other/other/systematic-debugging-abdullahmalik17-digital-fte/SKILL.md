---
name: systematic-debugging
description: |
  Systematic methodology for debugging bugs, test failures, and unexpected behavior.
  Use when encountering any technical issue before proposing fixes. Covers root cause
  investigation, pattern analysis, hypothesis testing, and fix implementation.
  Use ESPECIALLY when under time pressure, "just one quick fix" seems obvious, or
  you've already tried multiple fixes. NOT for exploratory code reading.
---

# Systematic Debugging

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

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
   - If not reproducible, gather more data - don't guess

3. **Check Recent Changes**
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   When system has multiple components (CI -> build -> signing, API -> service -> database):

   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Verify environment/config propagation

   Run once to gather evidence showing WHERE it breaks
   THEN analyze to identify failing component
   ```

5. **Trace Data Flow**

   See [references/root-cause-tracing.md](references/root-cause-tracing.md) for backward tracing technique.

   Quick version: Where does bad value originate? Keep tracing up until you find the source. Fix at source, not symptom.

### Phase 2: Pattern Analysis

1. **Find Working Examples** - Locate similar working code in same codebase
2. **Compare Against References** - Read reference implementations COMPLETELY, don't skim
3. **Identify Differences** - List every difference between working and broken
4. **Understand Dependencies** - What settings, config, environment assumptions?

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** - "I think X is the root cause because Y"
2. **Test Minimally** - SMALLEST possible change, one variable at a time
3. **Verify Before Continuing** - Worked? Phase 4. Didn't? NEW hypothesis, don't stack fixes

### Phase 4: Implementation

1. **Create Failing Test Case** - Simplest reproduction, automated if possible
2. **Implement Single Fix** - ONE change, no "while I'm here" improvements
3. **Verify Fix** - Test passes? No regressions?

4. **If Fix Doesn't Work:**
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze
   - **If >= 3: STOP and question the architecture**

5. **If 3+ Fixes Failed: Question Architecture**

   Pattern indicating architectural problem:
   - Each fix reveals new shared state/coupling
   - Fixes require "massive refactoring"
   - Each fix creates new symptoms elsewhere

   **STOP. Discuss with user before attempting more fixes.**

---

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "Add multiple changes, run tests"
- "I'm confident it's X, let me fix that"
- "One more fix attempt" (when already tried 2+)
- Proposing solutions before tracing data flow

**ALL of these mean: STOP. Return to Phase 1.**

---

## Supporting Techniques

### Defense-in-Depth

When you fix a bug, validate at EVERY layer:

| Layer | Purpose | Example |
|-------|---------|---------|
| Entry Point | Reject invalid input at API boundary | `if (!dir) throw new Error('dir required')` |
| Business Logic | Ensure data makes sense for operation | Validate before processing |
| Environment Guards | Prevent dangerous ops in specific contexts | Refuse git init outside tmpdir in tests |
| Debug Instrumentation | Capture context for forensics | Log with stack trace before dangerous ops |

Single validation feels sufficient, but different code paths bypass it. Make bugs structurally impossible.

### Condition-Based Waiting

Flaky tests guess at timing. Wait for actual conditions instead:

```python
# BAD: Guessing at timing
await asyncio.sleep(0.05)
result = get_result()

# GOOD: Wait for condition
await wait_for(lambda: get_result() is not None)
result = get_result()
```

Pattern:
```python
async def wait_for(condition, timeout_ms=5000):
    start = time.time()
    while True:
        if condition():
            return
        if (time.time() - start) * 1000 > timeout_ms:
            raise TimeoutError("Condition not met")
        await asyncio.sleep(0.01)  # Poll every 10ms
```

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I see the problem, let me fix it" | Seeing symptoms != understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

---

## Verification

Run: `python scripts/verify.py`

## References

- [references/root-cause-tracing.md](references/root-cause-tracing.md) - Trace bugs backward through call stack
