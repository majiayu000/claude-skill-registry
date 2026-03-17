---
name: root-cause-tracing
description: Trace bugs backward to their origin, not just symptoms
version: 1.0.0
author: Ariff
when_to_use: When fixing bugs - trace to source before patching
---

# Root Cause Tracing

## Core Principle

```
TRACE BACKWARD TO THE BUG'S ORIGIN
Don't patch symptoms - fix the disease
```

## The Backward Trace Method

```
SYMPTOM
   ↓ Where does this value come from?
IMMEDIATE CAUSE
   ↓ What set that to wrong value?
DEEPER CAUSE
   ↓ Why did that happen?
ROOT CAUSE ← Fix HERE
```

## Practical Steps

### 1. Start at Symptom
```
Q: What exactly went wrong?
→ Document the exact symptom
→ Note file, line, error message
```

### 2. First Backward Step
```
Q: Where does this value/state come from?
→ Find the direct source
→ Check: is THIS the bug or just a carrier?
```

### 3. Keep Tracing
```
Q: What set THAT to the wrong value?
→ Follow the data flow backward
→ Each step: is this the origin or just passing it along?
```

### 4. Identify Root
```
SIGNS YOU'VE FOUND ROOT:
- Logic error in requirements interpretation
- Initial state incorrectly set
- Wrong assumption in algorithm
- Missing validation at entry point
- Broken invariant at creation
```

## Stop Conditions

**You've found root cause when:**
- There's no earlier source to trace
- The error was introduced HERE (not inherited)
- Fixing HERE prevents the bug entirely
- The "why" answer is: "wrong logic/design"

**You're still at symptoms if:**
- The wrong value came from somewhere else
- Another function passed bad data
- It's a consequence, not origin
- Fixing here = adding a workaround

## Common Patterns

| Bug Pattern | Root Usually At |
|-------------|-----------------|
| Wrong value displayed | Data calculation, not display code |
| Null pointer | Where object should've been created |
| Off-by-one | Loop bounds definition, not body |
| Race condition | Shared state design, not specific access |
| Invalid state | State transition logic, not current handler |

## Anti-Patterns (Don't Do This)

❌ **Symptom Patching**
```
// Bad: Fix where error happens
if (value === undefined) value = defaultValue
// Good: Find why value is undefined
```

❌ **Guard Stacking**
```
// Bad: Add guards everywhere
if (x) if (y) if (z) doThing()
// Good: Ensure x, y, z correct at source
```

❌ **Quick Fix Pressure**
```
"Just make it work" → Technical debt
Better: "5 more minutes tracing saves 5 hours debugging later"
```

## Verification

After identifying root cause:

1. **Explain the chain** - Symptom ← caused by ← caused by ← ROOT
2. **Confirm origin** - "This is where wrong value first appears"
3. **Fix at root** - Change the origin, not the symptoms
4. **Verify fix** - Original symptom gone + no new bugs

## Integration with Checkers

Use with:
- `assumption-checker` → Was root cause an assumption?
- `dependency-validator` → Was root cause a broken dependency?
- `pre-action-verifier` → Verify root cause fix before applying
