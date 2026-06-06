---
name: systematic-debugging
description: Four-phase debugging framework for any technical issue. Use when encountering bugs, errors, or unexpected behavior. Prevents random fix attempts.
---
# Systematic Debugging

> From [obra/superpowers](https://github.com/obra/superpowers)

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Random fixes create new bugs. Understanding must precede solutions.

## The Four Phases

### Phase 1: Root Cause Investigation

Before ANY fix attempt:

1. **Read error messages carefully**
   - Full stack traces
   - Error codes and descriptions
   - Timestamps and context

2. **Reproduce consistently**
   - Document exact steps
   - Identify triggers
   - Note environmental factors

3. **Check recent changes**
   - Recent commits
   - Dependency updates
   - Configuration changes

4. **Gather diagnostic evidence**
   - Add logging at component boundaries
   - Check input/output at each step
   - Trace data flow backward to source

### Phase 2: Pattern Analysis

1. **Find similar working code**
   - Search codebase for related functionality
   - Look for existing patterns

2. **Read reference implementations completely**
   - Don't skim
   - Understand the full context

3. **Compare working vs broken**
   - What's different?
   - What assumptions changed?

4. **Understand dependencies**
   - What does this code rely on?
   - What relies on this code?

### Phase 3: Hypothesis and Testing

1. **Form a SINGLE, SPECIFIC hypothesis**
   - "The error occurs because X"
   - Not "maybe it's A or B or C"

2. **Test with minimal changes**
   - One variable at a time
   - Don't combine fixes

3. **Accept results**
   - If hypothesis is wrong, form new one
   - Don't force-fit evidence

4. **Ask for help when stuck**
   - After genuine investigation
   - With evidence gathered

### Phase 4: Implementation

1. **Create a failing test case FIRST**
   - Reproduces the bug
   - Will pass when fixed

2. **Implement SINGLE fix**
   - Address root cause only
   - Don't fix "nearby" issues

3. **Verify the fix**
   - Test case passes
   - No regressions
   - Issue is resolved

## The 3-Fix Rule

**If ≥3 fixes fail: STOP and question the architecture**

Three consecutive failed fixes signal:
- Architectural problem, not implementation bug
- Wrong mental model of the system
- Need to step back and reassess

Do NOT attempt more fixes. Reassess the approach.

## Critical Red Flags

STOP and restart investigation if you:

- Propose fixes before understanding the problem
- Add multiple changes simultaneously
- Skip investigation for "quick fixes"
- Make 3+ failed fix attempts
- Say "let's just try this"

## Debugging Checklist

```markdown
## Investigation
- [ ] Read full error message/stack trace
- [ ] Reproduced issue consistently
- [ ] Checked recent changes
- [ ] Added diagnostic logging
- [ ] Traced data flow

## Analysis
- [ ] Found similar working code
- [ ] Compared working vs broken
- [ ] Understood all dependencies

## Hypothesis
- [ ] Formed single specific hypothesis
- [ ] Tested with minimal change
- [ ] Accepted results honestly

## Fix
- [ ] Created failing test case
- [ ] Implemented single fix
- [ ] Verified fix works
- [ ] No regressions
```

## Example Workflow

```
Issue: User login fails silently

Phase 1 - Investigation:
- Error: "null reference at AuthService.validate()"
- Reproduced: happens with specific user emails
- Recent change: added email normalization

Phase 2 - Analysis:
- Working logins use lowercase emails
- Failing logins have mixed case
- Normalization strips @ symbol incorrectly

Phase 3 - Hypothesis:
- "Email normalization regex is wrong"
- Test: log email before/after normalization
- Result: "Test@Example.com" → "testexample.com"
- Confirmed!

Phase 4 - Fix:
- Write test: normalize("Test@Example.com") == "test@example.com"
- Fix regex to preserve @
- Verify: test passes, logins work
```
