---
name: debug-systematic
description: Systematic 4-phase debugging methodology for complex, intermittent, or mysterious issues. Use when investigating bugs, race conditions, or unexplained failures.
---

# Systematic Debugging Protocol

A disciplined, evidence-based approach to debugging that prevents guessing and ensures root cause discovery.

## The 4-Phase Protocol

### Phase 1: REPRODUCE (Establish Ground Truth)

**Goal**: Create reliable reproduction steps before ANY investigation.

**Actions**:

1. Document exact steps to trigger the bug
2. Record environment specifics (OS, versions, config, memory, network)
3. Determine frequency: Always? Sometimes? Specific conditions?
4. Capture exact error messages, stack traces, screenshots
5. Test on different environments to isolate variables

**Key Questions**:

- When did it last work correctly?
- What changed since then? (code, deps, config, infrastructure)
- Is it environment-specific?
- Is it data-specific?
- Is it timing-specific?

**Output**: Clear reproduction steps that reliably trigger the issue.

---

### Phase 2: ISOLATE (Narrow the Scope)

**Goal**: Reduce the search space from "entire codebase" to "specific component."

**Techniques**:

**Binary Search**:

1. Identify two points: working state and broken state
2. Test the midpoint
3. Recurse into the broken half
4. Continue until the change is identified

**Git Bisect** (for regressions):

```bash
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Git will checkout commits for testing
# After each test:
git bisect good  # or git bisect bad
# Continue until culprit found
```

**Code Elimination**:

- Comment out sections to isolate the problem
- Create minimal reproduction case
- Strip away everything non-essential

**Environment Isolation**:

- Test in isolation (unit test the failing path)
- Compare working vs broken environments
- Use fresh installs to eliminate pollution

**Output**: "The bug is in [specific component/function/line range]"

---

### Phase 3: DIAGNOSE (Understand Root Cause)

**Goal**: Know exactly WHY the bug occurs, not just WHERE.

**Scientific Method**:

1. **Observe**: What exactly is happening?
2. **Hypothesize**: Why might this be happening?
3. **Predict**: If hypothesis is correct, what else would be true?
4. **Test**: Verify predictions with evidence
5. **Iterate**: Refine hypothesis based on results

**Logging Strategy**:

```javascript
// Add strategic logging at boundaries
console.log("[DEBUG] Function entry:", { input, state });
console.log("[DEBUG] After processing:", { result, sideEffects });
console.log("[DEBUG] Function exit:", { returnValue });
```

**Common Root Causes**:

| Symptom                    | Likely Causes                                      |
| -------------------------- | -------------------------------------------------- |
| Works locally, fails in CI | Environment differences, timing, resources         |
| Intermittent failure       | Race condition, flaky network, resource contention |
| Works then stops working   | State mutation, memory leak, cache poisoning       |
| Wrong data                 | Type coercion, encoding, timezone, precision       |
| Silent failure             | Swallowed exception, async error, missing await    |

**Output**: Clear explanation of the root cause with evidence.

---

### Phase 4: FIX & VERIFY (Resolve and Prevent)

**Goal**: Fix the issue and prevent regression.

**Fix Process**:

1. **Write a failing test** that captures the bug
2. **Implement minimal fix** - change as little as possible
3. **Verify test passes** - confirms fix works
4. **Check for similar patterns** - same bug elsewhere?
5. **Review fix for side effects** - does it break anything?
6. **Document the fix** - why it happened, how to prevent

**Verification Checklist**:

- [ ] Test passes that specifically catches this bug
- [ ] Existing tests still pass
- [ ] Manual verification confirms fix
- [ ] Fix works in all affected environments
- [ ] No new warnings or errors introduced

**Prevention**:

- Add guards/validation at boundaries
- Improve error messages for easier future debugging
- Document gotchas for other developers
- Consider if architectural change prevents similar bugs

---

## Debugging Anti-Patterns

**DO NOT**:

- Guess and hope (change things randomly)
- Assume you know the problem without evidence
- Trust comments/docs over actual code behavior
- Debug production with print statements you'll forget to remove
- Fix the symptom instead of the root cause
- Make multiple changes at once

**DO**:

- Verify assumptions with evidence
- Change one thing at a time
- Log actual values, not what you expect
- Trust the code over documentation
- Take breaks when stuck (fresh eyes help)

---

## Quick Reference

```
1. REPRODUCE → Can I reliably trigger this?
2. ISOLATE   → Where exactly is it failing?
3. DIAGNOSE  → Why is it failing?
4. FIX       → How do I fix it permanently?
```

---

## Output Template

```markdown
## Bug Investigation: [Title]

### Reproduction

- Steps to reproduce
- Environment details
- Frequency

### Isolation

- Search method used
- Scope narrowed to

### Root Cause

- What's actually wrong
- Why it happens
- Evidence

### Fix

- Code changes made
- Test added

### Prevention

- How to prevent similar bugs
- Documentation updates
```
