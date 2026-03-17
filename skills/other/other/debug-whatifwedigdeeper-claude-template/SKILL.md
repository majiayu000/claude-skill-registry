---
skill: debug
description: Investigate and fix a bug systematically
arguments: bug description or error message
---

# Debug: $ARGUMENTS

Systematically investigate and fix the reported bug.

## Process

### 1. Reproduce the Issue

- Understand the expected vs actual behavior
- Identify steps to reproduce
- Run the app or tests to confirm the bug exists

### 2. Gather Information

```bash
# Check recent changes
git log --oneline -10

# Check for related errors
npm run build 2>&1
npm test 2>&1 | head -50
```

### 3. Locate the Problem

**Search strategies:**
- Grep for error messages or related keywords
- Trace the code path from UI to data
- Check recent git changes to affected files

**Narrow down:**
1. Which file(s) are involved?
2. Which function(s)?
3. Which line(s)?

### 4. Understand Root Cause

Read the code and understand:
- What is the code supposed to do?
- What is it actually doing?
- Why is there a difference?

Common causes:
- Off-by-one errors
- Null/undefined not handled
- Async timing issues
- State not updated correctly
- Wrong variable referenced

### 5. Develop Fix

- Fix the root cause, not just symptoms
- Consider edge cases
- Keep the fix minimal and focused

### 6. Add Regression Test

Create a test that:
- Would have caught this bug
- Verifies the fix works
- Prevents future regression

```typescript
test('should handle [specific case that was broken]', () => {
  // Test the exact scenario that was failing
});
```

### 7. Validate

```bash
npm run build
npm run lint
npm test
```

### 8. Document

Summarize:
- What was the bug
- Root cause
- How it was fixed
- Test added

## Debugging Tools

**Console debugging:**
```typescript
console.log('variable:', variable);
console.trace('call stack');
```

**React DevTools:** Check component state and props

**Network tab:** Check API requests/responses

**Node debugging:**
```bash
node --inspect script.js
```
