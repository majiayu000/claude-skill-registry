---
name: arcanea-systematic-debug
description: Systematic debugging methodology - scientific approach to finding and fixing bugs using hypothesis testing, isolation, and root cause analysis. Based on the Arcanean principle that understanding precedes execution.
version: 2.0.0
author: Arcanea
tags: [debugging, troubleshooting, development, problem-solving]
triggers:
  - bug
  - error
  - not working
  - debug
  - broken
  - failing
  - unexpected behavior
---

# Systematic Debugging: The Arcanean Method

> *"Sophron teaches: Understanding precedes execution. Do not guess at the bug. Understand the system, and the bug reveals itself."*

---

## The Debugging Mindset

### What Debugging Is NOT
```
❌ Random changes hoping something works
❌ Blaming the framework/library/language
❌ Assuming you know the cause without evidence
❌ Deleting and rewriting until it works
```

### What Debugging IS
```
✓ Scientific investigation
✓ Hypothesis formation and testing
✓ Systematic isolation
✓ Understanding before fixing
```

---

## The Scientific Method for Bugs

```
╭─────────────────────────────────────────────────────────╮
│                    THE DEBUG CYCLE                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   1. OBSERVE    →  What exactly is happening?           │
│        ↓                                                 │
│   2. REPRODUCE  →  Can I make it happen reliably?       │
│        ↓                                                 │
│   3. HYPOTHESIZE→  What could cause this?               │
│        ↓                                                 │
│   4. TEST       →  Is my hypothesis correct?            │
│        ↓                                                 │
│   5. FIX        →  Address the root cause               │
│        ↓                                                 │
│   6. VERIFY     →  Is it actually fixed?                │
│        ↓                                                 │
│   7. PREVENT    →  How do we stop it happening again?   │
│                                                          │
╰─────────────────────────────────────────────────────────╯
```

---

## Step 1: Observe

### Gather the Facts
```
WHAT is happening?
- Exact error message (copy it!)
- Actual behavior vs. expected behavior
- What does "not working" mean specifically?

WHEN does it happen?
- Always, or intermittently?
- After a specific action?
- At a specific time?

WHERE does it happen?
- Which environment? (dev, staging, prod)
- Which browser/device/OS?
- Which user/account?

WHO does it affect?
- All users or specific users?
- New users or existing?
- Any pattern in affected users?
```

### The Bug Report Template
```markdown
## Bug: [Clear, specific title]

### Observed Behavior
[What actually happens]

### Expected Behavior
[What should happen]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Environment
- Browser/Client:
- OS:
- Environment:
- User role:

### Error Messages
[Exact error text or screenshot]

### Frequency
[Always / Sometimes / Once]

### Impact
[Who is affected and how severely]
```

---

## Step 2: Reproduce

### The Reproduction Requirement
```
IF YOU CAN'T REPRODUCE IT, YOU CAN'T FIX IT
(Or at least, you can't verify the fix)
```

### Creating a Minimal Reproduction
```
1. Start with the full scenario
2. Remove one element at a time
3. Does the bug still occur?
4. Continue until you have the smallest case

The minimal reproduction reveals the cause.
```

### When You Can't Reproduce
```
Consider:
- Environment differences
- Timing/race conditions
- State dependencies
- User-specific data
- Cached vs. fresh state
- Network conditions
```

---

## Step 3: Hypothesize

### Generate Hypotheses
```
List possible causes without judgment:

"The bug could be caused by:"
1. [Hypothesis A]
2. [Hypothesis B]
3. [Hypothesis C]

Rank by:
- Likelihood (most to least likely)
- Testability (easiest to hardest to test)
```

### Common Bug Categories
```
STATE BUGS
- Wrong initial state
- State not updated
- State updated incorrectly
- Stale state (caching)

LOGIC BUGS
- Wrong condition
- Off-by-one
- Wrong operator
- Missing case

DATA BUGS
- Wrong type
- Null/undefined
- Malformed data
- Encoding issues

TIMING BUGS
- Race condition
- Wrong order
- Timeout too short/long
- Async not awaited

INTEGRATION BUGS
- API contract mismatch
- Environment difference
- Missing dependency
- Version mismatch

EDGE CASES
- Empty input
- Maximum input
- Invalid input
- Concurrent access
```

---

## Step 4: Test Hypotheses

### Isolation Techniques

#### Binary Search Debugging
```
If you don't know where the bug is:

1. Find the midpoint of the suspicious code
2. Add a log/breakpoint there
3. Is the state correct at that point?
4. If yes: bug is after that point
5. If no: bug is before that point
6. Repeat until found

This finds any bug in O(log n) checks.
```

#### Diff Debugging
```
If the code used to work:

1. Find last known working version (git bisect)
2. Compare with current version
3. What changed?
4. The bug is in the diff

git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
git bisect run npm test
```

#### Rubber Duck Debugging
```
Explain the code line by line to:
- A rubber duck
- A colleague
- Yourself out loud

The act of explaining often reveals the bug.
```

### Diagnostic Tools
```
LOGGING
- Add strategic console.log/print statements
- Log inputs, outputs, intermediate state
- Remove logs after debugging

BREAKPOINTS
- Pause execution at specific lines
- Inspect variable state
- Step through execution

ASSERTIONS
- Add runtime checks for assumptions
- assert(value !== null, 'value should exist')
- Fail fast when assumptions break

PROFILERS
- For performance bugs
- Identify slow functions
- Find memory leaks
```

---

## Step 5: Fix

### The Fix Principles
```
FIX THE ROOT CAUSE, NOT THE SYMPTOM

Symptom: "Users get 500 error on profile page"
Surface fix: Catch the error, show generic message
Root cause fix: Prevent the null pointer in user data

Surface fixes hide bugs. Root cause fixes eliminate them.
```

### Before Fixing
```
□ I understand WHY the bug occurs
□ I can explain the fix to someone else
□ The fix addresses root cause, not symptom
□ The fix won't introduce new bugs
□ The fix is the simplest solution
```

### The Minimal Fix
```
Change as little as possible.
One bug = one fix.
Don't refactor while fixing bugs.
Don't add features while fixing bugs.
```

---

## Step 6: Verify

### Verification Checklist
```
□ Original bug is fixed
□ Bug cannot be reproduced anymore
□ All existing tests still pass
□ New test written for this bug
□ Related functionality still works
□ Fix works in all affected environments
```

### The Regression Test
```
Write a test that:
1. Failed before the fix
2. Passes after the fix
3. Prevents this bug from returning

This is the most important test you can write.
```

---

## Step 7: Prevent

### Post-Mortem Questions
```
1. Why did this bug exist?
   - Missing test?
   - Unclear requirement?
   - Complex code?
   - Communication failure?

2. Why wasn't it caught earlier?
   - Code review missed it?
   - Tests didn't cover it?
   - QA didn't test this flow?

3. How can we prevent similar bugs?
   - Add tests?
   - Improve code review?
   - Simplify code?
   - Better tooling?
```

### Prevention Strategies
```
ADD TESTS
- Unit test for this specific bug
- Integration test for this flow
- Edge case tests

IMPROVE CODE
- Simplify complex logic
- Add defensive checks
- Improve error messages

IMPROVE PROCESS
- Update code review checklist
- Add to QA test cases
- Document the gotcha
```

---

## Debugging Specific Bug Types

### Null Pointer / Undefined
```
1. Find the null value
2. Trace backward: where should it have been set?
3. Why wasn't it set?
   - Never initialized
   - Initialization failed
   - Set then cleared
   - Wrong variable
```

### Race Condition
```
1. Identify the shared resource
2. What operations are racing?
3. What's the problematic order?
4. Add proper synchronization:
   - Locks/mutexes
   - Atomic operations
   - Message queues
```

### Performance Bug
```
1. Profile: where is time spent?
2. Is it algorithmic? (O(n²) vs O(n))
3. Is it I/O? (database, network)
4. Is it memory? (garbage collection)
5. Fix the biggest bottleneck first
```

### Memory Leak
```
1. Take memory snapshots over time
2. What objects are growing?
3. Why aren't they being collected?
   - Event listeners not removed
   - Closures holding references
   - Global references
   - Caching without limits
```

---

## Quick Reference

### The Debug Checklist
```
□ Exact error message captured
□ Steps to reproduce documented
□ Minimal reproduction created
□ Hypotheses listed
□ Most likely hypothesis tested first
□ Root cause identified
□ Minimal fix applied
□ Fix verified
□ Regression test written
□ Prevention documented
```

### Debug Commands
```javascript
// Quick state logging
console.log('State:', JSON.stringify(state, null, 2));

// Trace function calls
console.trace('Called from:');

// Measure timing
console.time('operation');
// ... operation ...
console.timeEnd('operation');

// Assert assumptions
console.assert(condition, 'This should be true');

// Group related logs
console.group('Processing user');
console.log('id:', user.id);
console.log('status:', user.status);
console.groupEnd();
```

### When You're Stuck
```
1. Take a break (fresh eyes find bugs)
2. Explain it to someone else
3. Question your assumptions
4. Look at what changed recently
5. Search for similar issues online
6. Add more logging
7. Reduce to minimal case
8. Sleep on it (seriously)
```

---

*"The bug exists in the gap between what you think the code does and what it actually does. Close that gap with understanding."*
