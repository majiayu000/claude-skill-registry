---
name: error-handling-gate
description: |
  TRIGGERS: "error handling check", "what if this fails?", "ready to merge",
  error verification, failure handling, graceful degradation, user feedback review.
  USE WHEN: Code is ready to merge and needs error handling verification.
  PROVIDES: Empty catch detection, user message review, logging verification.
  GATE TYPE: WARNING - Recommends proper error handling before merge.
---

# Gate 3: Error Handling Review

> "Happy path code is easy. Error handling is where senior engineers shine."

## Purpose

This gate ensures the code handles failures gracefully, provides meaningful feedback to users, and doesn't silently swallow errors.

## Gate Status

- **PASS** — Error handling is appropriate
- **WARNING** — Issues found that should be addressed

---

## Gate Questions

### Question 1: Failure Scenario
> "What happens if [main operation] fails? Walk me through the user experience."

**Looking for:**
- Awareness of failure modes
- User-friendly error messages
- Recovery options (retry, fallback)
- No silent failures

**Example scenarios:**
- Network request fails
- Database is down
- Validation fails
- Third-party API errors

### Question 2: User Feedback
> "What does the user see when an error occurs? Would they understand what to do next?"

**Looking for:**
- Helpful, non-technical messages
- Actionable guidance ("Try again", "Check your connection")
- Appropriate error placement in UI

### Question 3: Error Visibility
> "How would you debug this in production if something went wrong?"

**Looking for:**
- Errors are logged
- Sufficient context in logs
- No sensitive data in logs
- Error tracking awareness (Sentry, etc.)

---

## Error Handling Checklist

### Async Operations
- [ ] All async calls wrapped in try/catch or .catch()
- [ ] No empty catch blocks
- [ ] Errors include context (what operation, what data)
- [ ] finally blocks for cleanup (loading states, etc.)

### User Experience
- [ ] User-friendly error messages (no technical jargon)
- [ ] Errors are actionable (what can user do?)
- [ ] Loading states cleared on error
- [ ] Retry options where appropriate

### Logging & Debugging
- [ ] Errors logged with context
- [ ] No sensitive data in error logs
- [ ] Error types/codes for categorization
- [ ] Stack traces available in development

### Edge Cases
- [ ] Empty states handled
- [ ] Timeout handling
- [ ] Partial failure handling (some items succeed, some fail)
- [ ] Concurrent request handling

---

## Response Templates

### If PASS

```
✅ ERROR HANDLING GATE: PASSED

Error handling looks solid:
- Async operations properly wrapped
- User-friendly error messages
- Errors logged for debugging

Moving to the next gate...
```

### If WARNING

```
⚠️ ERROR HANDLING GATE: WARNING

Found [X] error handling concerns:

**Issue 1: [Empty catch block / Missing error handling]**
Location: `file.ts:42`
Question: "What happens when this fails silently?"

**Issue 2: [Technical error shown to user]**
Location: `file.ts:88`
Question: "Will users understand 'TypeError: Cannot read property...'?"

**Issue 3: [No loading state cleanup]**
Location: `file.ts:100`
Question: "What happens to the loading spinner if this fails?"

These should be addressed to ensure a good user experience.
```

---

## Common Issues to Check

### 1. Empty Catch Blocks
```
❌ try {
     await submitForm();
   } catch (error) {
     // Silent failure - user has no idea
   }

✅ try {
     await submitForm();
   } catch (error) {
     console.error('Form submission failed:', error);
     setError('Could not submit. Please try again.');
   }
```

### 2. Missing Finally for Cleanup
```
❌ try {
     setLoading(true);
     await fetchData();
     setLoading(false);
   } catch (error) {
     handleError(error);
     // Loading stays true forever!
   }

✅ try {
     setLoading(true);
     await fetchData();
   } catch (error) {
     handleError(error);
   } finally {
     setLoading(false);
   }
```

### 3. Technical Errors Exposed
```
❌ catch (error) {
     setError(error.message);
     // User sees: "TypeError: Cannot read property 'map' of undefined"
   }

✅ catch (error) {
     console.error('Load failed:', error);
     setError('Something went wrong. Please try again.');
   }
```

### 4. No Error Differentiation
```
❌ catch (error) {
     setError('Error');
   }

✅ catch (error) {
     if (error.status === 401) {
       setError('Please log in to continue.');
       redirectToLogin();
     } else if (error.status === 404) {
       setError('Item not found.');
     } else if (error.name === 'NetworkError') {
       setError('Check your internet connection.');
     } else {
       setError('Something went wrong. Please try again.');
     }
   }
```

---

## Socratic Error Questions

Instead of pointing out the fix, ask:

1. "What happens if the network is down when the user clicks this?"
2. "If this catch block runs, what will the user see?"
3. "How will you know this failed in production?"
4. "What if only some of the items fail to save?"
5. "Is the loading spinner stuck if an error happens?"

---

## Error Message Quality Check

| Bad Message | Better Message |
|-------------|----------------|
| "Error" | "Could not save. Please try again." |
| "An error occurred" | "Unable to load your profile. Check your connection." |
| "TypeError: undefined" | "Something went wrong. Please refresh and try again." |
| "500 Internal Server Error" | "Our servers are having trouble. Please try again in a moment." |
| "Failed" | "Could not complete your request. Need help? Contact support." |

---

## Severity Guide

| Issue | Severity | Impact |
|-------|----------|--------|
| Empty catch block | HIGH | Silent failures, hard to debug |
| No loading state cleanup | MEDIUM | Stuck UI, poor UX |
| Technical error shown | MEDIUM | Confusing UX, potential info leak |
| No retry option | LOW | Minor UX friction |
| Generic error message | LOW | Less helpful but not broken |
