---
name: test
description: Test features before users find bugs. Use when feature is built, before deploying, or when bugs reported. Covers manual testing, edge cases, cross-browser testing, and testing checklists for non-technical founders.
---

# Test

## Testing Checklist

```
Feature Testing:
- [ ] Happy path works (main user flow)
- [ ] Edge cases handled (empty, long, invalid data)
- [ ] Error messages clear and helpful
- [ ] Works on mobile (iOS and Android)
- [ ] Works in Safari, Chrome, Firefox
- [ ] Loading states show during waits
- [ ] Forms validate input
- [ ] Can't break it with weird input
- [ ] Back button works correctly
- [ ] Page refresh doesn't lose data
```

See [TEST-SCENARIOS.md](TEST-SCENARIOS.md) for detailed scenarios.

---

## When to Test

**Test when:**
- Feature just built by AI
- Before deploying to production
- After fixing a bug (verify fix works)
- Users report issues (reproduce first)

**Don't test:**
- While AI is still building
- Before feature is complete
- Every tiny change (batch test features)

**Rule:** Build → Test → Fix → Test again → Deploy

---

## Manual Testing Workflow

```
1. Test happy path
   - Does the main flow work?
   - Can user complete the task?

2. Test edge cases
   - What if field is empty?
   - What if text is very long?
   - What if user clicks twice?

3. Test on mobile
   - Open on real phone
   - Test main actions
   - Check layout doesn't break

4. Test in different browsers
   - Chrome (most users)
   - Safari (iOS users)
   - Firefox (some users)

5. Document issues
   - Screenshot the problem
   - Write exact steps to reproduce
   - Give to AI to fix
```

---

## Testing Edge Cases

**Always test these:**

**Empty data:**
- What shows when no items in list?
- What happens with empty form field?
- Is placeholder/empty state clear?

**Long data:**
- Very long name (200 characters)
- Very long text (10,000 characters)
- Does layout break?

**Invalid data:**
- Invalid email format
- Negative numbers where not allowed
- Special characters in text field
- SQL characters ('; DROP TABLE)

**Boundary cases:**
- Exactly at limit (100 char limit, enter 100)
- Just over limit (enter 101)
- Zero/empty values

**Tell AI:**
```
Test these edge cases:
- Empty username: show "Required"
- Username too long (>50 chars): show "Max 50 characters"
- Username with spaces: show "No spaces allowed"
- Special characters: show "Letters and numbers only"
```

See [EDGE-CASES.md](EDGE-CASES.md) for comprehensive list.

---

## Testing on Mobile

**Minimum mobile tests:**

```
Mobile Testing:
- [ ] Page loads and looks correct
- [ ] Can tap all buttons (44px minimum)
- [ ] Forms work (keyboard appears)
- [ ] No horizontal scroll
- [ ] Images load and fit screen
- [ ] Navigation works
- [ ] Can complete main user flow
```

**Test on:**
- iPhone (Safari) - Most common iOS
- Android phone (Chrome) - Most common Android

**Don't need to test:**
- Every phone model
- Tablets (unless primary use case)
- Landscape mode (unless important)

---

## Cross-Browser Testing

**Priority order:**

1. **Chrome** (65% of users) - Test thoroughly
2. **Safari** (20% of users) - Test main flows
3. **Firefox** (5% of users) - Quick check
4. **Edge** (5% of users) - Usually works if Chrome works

**Common browser issues:**
- Date pickers look different
- Flexbox behaves differently
- Scrolling momentum feels different
- Animations may not work on old Safari

**Quick test:**
```
Open in each browser:
1. Load homepage
2. Sign up / Log in
3. Complete 1-2 main actions
4. Check nothing is broken
```

---

## Testing Forms

**Form validation testing:**

```
Form Testing Checklist:
- [ ] Required fields show error if empty
- [ ] Email validation works (format check)
- [ ] Password requirements enforced
- [ ] Can't submit invalid form
- [ ] Error messages clear and specific
- [ ] Success message shows after submit
- [ ] Form disables during submit (no double-submit)
- [ ] Errors clear when user fixes them
```

**Tell AI:**
```
Test form validation:
- Required field left empty: "This field is required"
- Invalid email: "Enter a valid email address"
- Weak password: "Password must be 8+ characters with 1 number"
- All valid: Allow submit
- Show errors inline, not alert()
```

---

## Testing Authentication

**Auth flow testing:**

```
Auth Testing:
- [ ] Can sign up with valid info
- [ ] Can't sign up with existing email
- [ ] Can log in with correct password
- [ ] Can't log in with wrong password
- [ ] Can reset password via email
- [ ] Session expires after timeout
- [ ] Logout works (can't access protected pages)
- [ ] Can't access protected routes without login
- [ ] Redirect to login when session expires
```

---

## Testing Integrations

**Third-party services:**

**Payment (Stripe):**
```
- [ ] Test card (4242 4242 4242 4242) processes
- [ ] Declined card shows error
- [ ] Receipt email sent
- [ ] Subscription status updates
- [ ] Can cancel subscription
```

**Email (SendGrid):**
```
- [ ] Welcome email sends on signup
- [ ] Password reset email arrives
- [ ] Emails have correct content
- [ ] Links in email work
- [ ] Unsubscribe link works
```

**Tell AI:**
```
Add test mode checking:
Log when using test API keys.
Show banner: "TEST MODE - No real charges"
Use Stripe test cards only in development.
```

---

## Finding Bugs Yourself

**How to break your app:**

**1. Click fast and repeatedly**
- Double-click submit button
- Click back button quickly
- Refresh during loading

**2. Enter unexpected data**
- Copy/paste 10,000 characters
- Enter emojis 🎉 in text fields
- Try SQL: `'; DROP TABLE users;--`
- Enter HTML: `<script>alert('xss')</script>`

**3. Change state unexpectedly**
- Log out in another tab
- Let session expire, then try action
- Open same page in multiple tabs

**4. Use slow connection**
- Chrome DevTools → Network → Slow 3G
- Try all main actions
- Do loading states show?

See [BREAKING-THINGS.md](BREAKING-THINGS.md) for full list.

---

## Documenting Bugs

**Bug report template:**

```
Bug: [Short description]

Steps to reproduce:
1. [First action]
2. [Second action]
3. [What triggers the bug]

Expected: [What should happen]
Actual: [What actually happened]

Screenshot: [Attach if visual]
Browser: [Chrome 120 on Mac]
URL: [Where it happened]
Frequency: [Always / Sometimes / Once]
```

**Give to AI to fix:**
```
Bug found: [paste bug report]

Please:
1. Reproduce the bug
2. Identify root cause
3. Fix the issue
4. Verify fix works
5. Test that fix didn't break anything else
```

---

## Regression Testing

**After fixing a bug, test:**

```
Regression Checklist:
- [ ] Original bug is fixed
- [ ] Happy path still works
- [ ] Related features still work
- [ ] No new errors in console
- [ ] No new visual issues
```

**Common regression issues:**
- Fix breaks different browser
- Fix breaks mobile layout
- Fix breaks related feature
- Fix introduces new edge case bug

---

## Pre-Deployment Checklist

**Before pushing to production:**

```
Production Readiness:
- [ ] All features tested (happy path + edge cases)
- [ ] Works on mobile (iPhone + Android)
- [ ] Works in Safari and Chrome
- [ ] No console errors
- [ ] Forms validate correctly
- [ ] Authentication works
- [ ] No test data visible
- [ ] Error messages are user-friendly
- [ ] Loading states show
- [ ] Can't break it with weird input
```

---

## When to Get QA Help

**Consider hiring QA when:**
- > 10 features to test before launch
- Complex user flows (multi-step processes)
- Multiple integrations to verify
- Preparing for big launch (> 1000 users)

**For most MVPs:** Following this checklist is sufficient.

---

## Common Testing Mistakes

| Mistake | Fix |
|---------|-----|
| Only test happy path | Test edge cases too |
| Test only on Chrome desktop | Test mobile + Safari |
| Skip testing forms | Forms are where bugs hide |
| Test while AI still building | Wait until feature complete |
| Ignore console errors | Fix all errors before deploy |
| Test with perfect data | Test empty, long, invalid data |

---

## Quick Testing Shortcuts

**5-minute quick test:**
```
1. Load page in Chrome
2. Complete main user flow
3. Try one edge case (empty field)
4. Check mobile view (Chrome DevTools)
5. Look for console errors
```

**15-minute thorough test:**
```
1. Happy path in Chrome
2. 3-4 edge cases
3. Test on real phone
4. Check Safari
5. Try to break it (fast clicks, weird input)
6. Check all error messages
```

---

## Testing Tools

**Built into browser:**
- Chrome DevTools (Inspect)
- Network tab (check API calls)
- Console (check for errors)
- Device mode (test mobile sizes)
- Lighthouse (performance + best practices)

**Free external tools:**
- BrowserStack (free trial) - Test on real devices
- Can I Use (caniuse.com) - Check browser support
- Validator.nu - Check HTML validity

**Usually don't need:**
- Automated testing frameworks (too complex for non-technical)
- Paid testing services (manual testing sufficient for MVP)

---

## Success Looks Like

✅ Main user flow works perfectly  
✅ Edge cases handled gracefully  
✅ Works on mobile and desktop  
✅ Works in Chrome and Safari  
✅ Error messages clear and helpful  
✅ Can't break it with weird input  
✅ No bugs reported by users