---
name: debug
description: >
  Systematic debugging workflow for tracking down and fixing issues.
  Use when encountering bugs, errors, or unexpected behavior.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.
Follow the four phases to find root cause before attempting any fix.

**Core principle:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

**Announce at start:** "I'm using the debug skill to investigate this issue."

## The Iron Law

```
If you haven't completed Phase 1, you cannot propose fixes.
```

## When to Use

Use for ANY technical issue:
- Test failures
- Runtime errors
- Unexpected behavior
- Performance problems
- Build failures

**Use ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- Previous fix didn't work
- You've tried multiple fixes already

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
   - If not reproducible - gather more data, don't guess

3. **Check Recent Changes**
   ```bash
   git diff HEAD~5           # Recent changes
   git log --oneline -10     # Recent commits
   ```

4. **Check Existing Knowledge**
   ```bash
   kodo query "similar bug"       # Was this fixed before?
   kodo query "error handling"    # Known patterns
   ```

5. **Trace Data Flow**
   - Where does the bad value originate?
   - Trace backward through call stack
   - Find the SOURCE, not the symptom

### Phase 2: Pattern Analysis

1. **Find Working Examples**
   - Locate similar working code in codebase
   - What works that's similar to what's broken?

2. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify**
   - Did it work? Yes -> Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

### Phase 4: Implementation

1. **Create Failing Test First**
   - Write test that reproduces the bug
   - Verify test fails before fixing
   - Use `kodo:plan` patterns for test structure

2. **Implement Single Fix**
   - Address the root cause identified
   - ONE change at a time
   - No "while I'm here" improvements

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - Count: How many fixes have you tried?
   - **If 3+ fixes failed: STOP**
   - Question the architecture, not the symptoms
   - Discuss with user before attempting more

5. **Capture Learning**
   ```bash
   kodo reflect --signal "Bug root cause was X, fixed by Y"
   ```

## Red Flags - STOP and Return to Phase 1

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "I don't fully understand but this might work"
- "Let me try multiple changes at once"
- **"One more fix attempt" (when already tried 2+)**

**ALL of these mean: STOP. Return to Phase 1.**

## Integration with Kodo

**Before debugging:**
```bash
kodo query "similar error"    # Check if this was solved before
kodo query "this module"      # Understand expected behavior
```

**After fixing:**
```bash
kodo reflect --signal "Root cause: X. Fixed by: Y"
kodo reflect --signal "Pattern to avoid: Z"
```

## Key Principles

- **Root cause first** - Symptom fixes are failure
- **One hypothesis at a time** - Scientific method works
- **Test before fix** - Prove the bug exists
- **3 strikes rule** - After 3 failed fixes, question architecture
- **Learn from bugs** - Capture patterns with `kodo reflect`

## Quick Reference

| Phase | Goal | Success Criteria |
|-------|------|------------------|
| 1. Root Cause | Understand WHAT and WHY | Can explain the bug |
| 2. Pattern | Find working reference | Know what should work |
| 3. Hypothesis | Form testable theory | Single clear hypothesis |
| 4. Implementation | Fix and verify | Bug gone, tests pass |
