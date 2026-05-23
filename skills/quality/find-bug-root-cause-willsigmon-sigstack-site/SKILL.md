---
name: find-bug-root-cause
description: Deep investigation to find actual root cause (not just symptoms)
model: sonnet
---

# Root Cause Analysis Protocol

When a feature is broken, don't just add logging - find and fix the ACTUAL problem.

## Methodology

1. **Understand the Symptom:**
   - What does the user see/experience?
   - What SHOULD happen?
   - What ACTUALLY happens?

2. **Trace the Data Flow:**
   - Follow code execution from UI → ViewModel → Service → Backend
   - Check each layer for failures
   - Use breakpoint logic (mental trace)

3. **Check Dependencies:**
   - Is the service initialized? (`DIContainer.shared.service`)
   - Are databases/indexes ready?
   - Are async operations completing?
   - Are errors being swallowed?

4. **Find the Bug:**
   - Don't stop at "add try/catch" or "add logging"
   - Find the EXACT line where logic fails
   - Understand WHY it fails

5. **Fix It Properly:**
   - Fix root cause, not symptoms
   - Add defensive checks only AFTER fixing core issue
   - Test the fix logic

6. **Verify:**
   - Does the fix address the root cause?
   - Are there edge cases?
   - Will this prevent recurrence?

## Example: "Search returns no results"

❌ **Bad approach:**
```swift
// Just add logging
AppLog.info("Search started")
let results = await search(query)
AppLog.info("Search returned \(results.count) results")
```

✅ **Good approach:**
```swift
// Find WHY search returns nothing:
// 1. Is ScriptureDatabase initialized? → Check init
// 2. Are indexes built? → Check index creation
// 3. Is query being processed? → Check query transformation
// 4. FIX the actual issue (e.g., index not built on first launch)

// THEN add logging to prevent future issues
```

**Return the root cause and the actual fix that solves it.**
