---
name: debug
description: Fix bugs systematically instead of guessing. Use when features break, users report errors, or tests fail. Covers reproducing bugs, gathering diagnostic info, and working with AI tools to fix issues efficiently for non-technical founders.
---

# Debug

## Debugging Workflow

```
Debug Process:
- [ ] Reproduce bug consistently
- [ ] Capture what's happening (screenshots, errors)
- [ ] Check what changed recently
- [ ] Gather diagnostic info
- [ ] Give info to AI to diagnose
- [ ] AI proposes fix
- [ ] Test fix works
- [ ] Verify didn't break anything else
```

See [DEBUG-CHECKLIST.md](DEBUG-CHECKLIST.md) for detailed steps.

---

## The Golden Rule

**NO GUESSING. GATHER INFO FIRST.**

Bad approach:
1. Something broke
2. Try random fix
3. Doesn't work
4. Try another fix
5. Still broken after 5 attempts

Good approach:
1. Something broke
2. Reproduce it consistently
3. Gather diagnostic info
4. Give to AI to diagnose
5. AI fixes it (usually first try)

**Diagnosis before fixes.**

---

## Reproducing Bugs

**Before asking AI to fix, reproduce it:**

```
Can you reproduce it?
- [ ] Exact steps to trigger bug
- [ ] Happens every time
- [ ] Happens on specific browser/device
- [ ] Happens with specific data

If can't reproduce:
- Ask user for exact steps
- Try different browser/device
- Try with different data
- Check if intermittent (timing issue)
```

**Tell AI:**
```
Bug: [description]

Steps to reproduce:
1. [Step]
2. [Step]
3. [Bug happens]

Happens: [Always / Sometimes / Once]
Browser: [Chrome 120 on Mac]
Screenshot: [attach]
```

---

## Capturing Error Info

### Browser Console Errors

**Open console:**
1. Right-click page → Inspect
2. Click "Console" tab
3. Look for red errors

**Screenshot errors and give to AI:**
```
I see this error in console:
[paste error message]

When it happens:
[what you were doing]

Please:
1. Explain what this means
2. Identify the cause
3. Fix the issue
```

### Network Errors

**Check network tab:**
1. Open DevTools → Network
2. Reproduce bug
3. Look for failed requests (red)
4. Click failed request
5. Check response

**Tell AI:**
```
API call failing:
URL: /api/endpoint
Status: 500 Internal Server Error
Response: [paste error response]

This happens when: [action]
```

### Visual Bugs

**Screenshot everything:**
- What you expected to see
- What actually shows
- Full page context
- Error messages

**Tell AI:**
```
Visual bug: [description]
Expected: [screenshot or description]
Actual: [screenshot]
Device: [iPhone 14, Chrome on Mac, etc]
```

---

## What Changed?

**Ask yourself:**
- Did this work yesterday?
- What did AI change today?
- Did you deploy recently?
- Did you change any settings?

**Tell AI:**
```
This worked yesterday, broke today.
Changes made today:
- [Change 1]
- [Change 2]

Which could cause: [the bug]?
```

---

## Common Bug Types

### "Nothing happens when I click"

**Check:**
- Console errors?
- Network request failing?
- Button actually clickable?

**Tell AI:**
```
Button does nothing when clicked.
Button: [which button]
Expected: [what should happen]
Console errors: [paste any errors]
```

### "Page won't load"

**Check:**
- Network errors?
- JavaScript errors?
- Infinite redirect?

**Tell AI:**
```
Page won't load: /page/url
Browser shows: [blank / error / loading forever]
Console errors: [paste]
Network errors: [paste]
```

### "Wrong data showing"

**Check:**
- API returning wrong data?
- Caching issue?
- State management bug?

**Tell AI:**
```
Showing wrong data.
Expected: [User A's profile]
Showing: [User B's profile]
API response: [paste from Network tab]
```

### "Form doesn't submit"

**Check:**
- Validation errors?
- Console errors?
- Network request happening?

**Tell AI:**
```
Form won't submit.
Form: [which form]
Filled: [what data entered]
Validation errors: [any visible]
Console errors: [paste]
```

---

## Working with AI to Debug

### Step 1: Gather Info

```
Before asking AI to fix, provide:
- Exact steps to reproduce
- Expected vs actual behavior
- Screenshots/error messages
- Browser and device
- What changed recently (if known)
```

### Step 2: AI Diagnoses

```
[Paste all info above]

Before proposing fixes:
1. What do you think is wrong?
2. Why is it happening?
3. What needs to change?

Explain in plain English first.
```

### Step 3: AI Fixes

```
Okay, now please fix it.

After fixing:
- Explain what you changed
- How to test the fix
- What to watch out for
```

### Step 4: Verify Fix

```
Test the fix:
- [ ] Original bug is gone
- [ ] Tested same steps, works now
- [ ] Related features still work
- [ ] No new console errors
```

See [DEBUG-PROMPTS.md](DEBUG-PROMPTS.md) for more patterns.

---

## When You're Stuck

**After 2 failed fix attempts:**

Stop. Don't try a 3rd fix.

**Ask AI:**
```
Tried 2 fixes, both didn't work.

Original bug: [description]
Fix 1: [what we tried] - didn't work
Fix 2: [what we tried] - still broken

Questions:
- Are we fixing the wrong thing?
- Is there a better approach?
- Should we start over?
```

**If 3+ fixes failed:** Probably need to rethink approach, not try more fixes.

---

## Intermittent Bugs

**"It works sometimes, breaks sometimes"**

**Likely causes:**
- Race condition (timing)
- Caching issue
- Network timing
- External API flakiness

**Tell AI:**
```
Bug is intermittent.
Works: [X] out of 10 times
Fails: [Y] out of 10 times

Pattern noticed:
- Fails more often when [condition]
- Never fails when [condition]

Please add logging to capture when it fails.
```

---

## Bugs in Production

**Users reporting bugs in live app:**

**Priority 1: Can users work around it?**
- Yes → Fix in next deployment
- No → Emergency fix needed

**For emergency fixes:**
```
Production bug blocking users.
Bug: [description]
Impact: [how many users affected]

Need quick fix:
- Simplest solution that works
- Don't optimize, just unblock users
- Can improve later
```

**For non-urgent:**
```
Production bug reported by user.
Bug: [description]
Impact: [minor / major]
Can work around: [yes / no]

Reproduce in development:
[steps]

Then fix and test before deploying.
```

---

## Reading Error Messages

**Common error patterns:**

**"Cannot read property of undefined"**
- Trying to access something that doesn't exist
- Check: Is data loaded before accessing it?

**"Maximum call stack exceeded"**
- Infinite loop or recursion
- Check: Function calling itself forever?

**"Network request failed"**
- API call not working
- Check: Network tab for status code

**"Unauthorized" or "401"**
- Authentication issue
- Check: Are you logged in? Token valid?

**"Internal Server Error" or "500"**
- Backend problem
- Check: Server logs for details

See [ERROR-MESSAGES.md](ERROR-MESSAGES.md) for more.

---

## Debugging Tools

**Built into browser:**
- Console: See errors and logs
- Network: See API calls and responses
- Elements: Inspect HTML/CSS
- Sources: Set breakpoints (advanced)

**How to use:**
1. Open DevTools (F12 or right-click → Inspect)
2. Click relevant tab
3. Reproduce bug
4. Look for errors/failed requests

**Screenshot and give to AI** - AI can interpret errors.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trying fixes without info | Gather diagnostic info first |
| "It doesn't work" | Be specific: what doesn't work? |
| Not reproducing first | Find consistent steps to trigger bug |
| Random fixes | Diagnose root cause first |
| Ignoring console errors | Always check console |
| Not testing after fix | Verify fix works, didn't break other things |

---

## When to Get Help

**Consider hiring developer when:**
- Stuck after following this process
- Critical bug can't figure out
- Same bug keeps coming back
- Bug in complex integration
- Need production fixed urgently

**For most bugs:** Following this process with AI is sufficient.

---

## Prevention

**After fixing, ask AI:**
```
Bug is fixed. 

How could we have prevented this?
- Better validation?
- Better error handling?
- Testing we should add?
```

**Build prevention into next features.**

---

## Quick Debug Checklist

**When something breaks:**

```
Quick Debug:
- [ ] Can I reproduce it?
- [ ] Any console errors?
- [ ] Any network errors?
- [ ] What changed recently?
- [ ] Screenshot the issue
- [ ] Gather all info
- [ ] Give to AI with context
- [ ] Test AI's fix
```

**5 minutes of diagnosis > 2 hours of guessing**

---

## Success Looks Like

✅ Bugs fixed on first or second try  
✅ Can explain what was wrong  
✅ Know how to reproduce bugs  
✅ Gather complete info before asking for fixes  
✅ Verify fixes work and don't break other things  
✅ Bugs getting rarer over time (learning patterns)