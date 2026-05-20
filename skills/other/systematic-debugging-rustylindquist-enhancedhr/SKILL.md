---
name: systematic-debugging
description: Methodical problem-solving workflow for debugging issues. Use when facing bugs, errors, or unexpected behavior that isn't immediately obvious.
---

# Systematic Debugging

A structured approach to debugging that prevents premature solutions and ensures root cause identification.

## Purpose

Replace ad-hoc debugging with a systematic process that:
1. Gathers evidence before making changes
2. Identifies root cause, not just symptoms
3. Prevents introducing new bugs while fixing
4. Documents findings for future reference

## When to Use

- Bug reports with unclear cause
- Errors that don't make immediate sense
- Issues that have "already been fixed" before
- Problems spanning multiple components
- Performance issues

## The DEBUG Protocol

### D - Define the Problem

Before touching code, clearly define:

```markdown
## Problem Definition

**Observed Behavior**: [What is actually happening]
**Expected Behavior**: [What should happen]
**Reproduction Steps**:
1. [Step 1]
2. [Step 2]
3. [Result]

**Environment**: [Browser, user role, data state]
**Frequency**: [Always / Sometimes / Rare]
**Recent Changes**: [What changed recently that might relate]
```

### E - Explore the Evidence

Gather information systematically:

1. **Console/Logs**: Check browser console, server logs
2. **Network**: Inspect API requests/responses
3. **Database**: Query relevant data state
4. **Code Path**: Trace the execution path
5. **User Context**: Check user role, permissions, session

```
/browser-use: Check the browser console for errors
@research-agent: Trace the code path for [action]
```

### B - Build Hypotheses

Generate multiple possible causes:

```markdown
## Hypotheses (ranked by likelihood)

1. **[Most likely]**: [Description]
   - Evidence for: [...]
   - Evidence against: [...]
   - Test: [How to confirm/refute]

2. **[Second likely]**: [Description]
   - Evidence for: [...]
   - Evidence against: [...]
   - Test: [How to confirm/refute]

3. **[Less likely]**: [Description]
   - Evidence for: [...]
   - Evidence against: [...]
   - Test: [How to confirm/refute]
```

### U - Uncover Root Cause

Test hypotheses systematically:

1. Start with most likely hypothesis
2. Design a test that will confirm OR refute
3. Execute test, record results
4. If refuted, move to next hypothesis
5. Continue until root cause confirmed

**The Five Whys**:
- Why did this happen? → [Answer 1]
- Why did [Answer 1] happen? → [Answer 2]
- Why did [Answer 2] happen? → [Answer 3]
- Why did [Answer 3] happen? → [Answer 4]
- Why did [Answer 4] happen? → [Root Cause]

### G - Generate Fix

Only after root cause is confirmed:

```markdown
## Fix Plan

**Root Cause**: [Confirmed cause]
**Fix Approach**: [How to fix]
**Files to Change**:
- [file1]: [change]
- [file2]: [change]

**Risk Assessment**:
- Blast radius: [What else might be affected]
- Rollback plan: [How to undo if needed]

**Verification**:
- [ ] Original issue resolved
- [ ] No new issues introduced
- [ ] Related functionality still works
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| **Shotgun debugging** | Random changes, new bugs | Systematic hypothesis testing |
| **Assuming the cause** | Fix wrong thing | Gather evidence first |
| **Only fixing symptom** | Bug returns | Find root cause |
| **No verification** | Incomplete fix | Test thoroughly |
| **No documentation** | Future confusion | Document findings |

## Quick Reference

```
1. DEFINE: What's happening vs what should happen?
2. EXPLORE: Console, network, database, code path
3. BUILD: 2-3 hypotheses ranked by likelihood
4. UNCOVER: Test hypotheses, use Five Whys
5. GENERATE: Fix only after root cause confirmed
```

## Output Format

```markdown
## Debug Report: [Issue Title]

### Problem
- **Observed**: [symptom]
- **Expected**: [correct behavior]
- **Repro**: [steps]

### Investigation
- **Console**: [findings]
- **Network**: [findings]
- **Code Path**: [findings]

### Root Cause
[Confirmed root cause with evidence]

### Fix
- **Approach**: [how fixed]
- **Files Changed**: [list]
- **Verification**: [how verified]

### Prevention
[How to prevent this class of bug in future]
```

## Integration

For complex debugging, coordinate with:
- **Research Agent**: Trace code paths
- **Test Agent**: Verify fix doesn't break other things
- **Doc Agent**: Check if documented behavior differs
