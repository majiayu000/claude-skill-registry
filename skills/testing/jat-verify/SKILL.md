---
name: jat-verify
description: Escalatory browser verification - open the app in a real browser and test the feature you built. Use after showing "READY FOR REVIEW" when the user asks you to verify in a browser.
metadata:
  author: jat
  version: "1.0"
---

# /skill:jat-verify - Browser Verification

Test your work in a real browser using JAT's browser automation tools.

## Usage

```
/skill:jat-verify                           # Auto-detect what to test
/skill:jat-verify http://localhost:5173/tasks  # Test specific URL
/skill:jat-verify /tasks                     # Test specific path
```

## When to Use

- User asks to "verify in browser" or "actually test this"
- After showing "READY FOR REVIEW"
- NOT for static checks (tests, lint) - those are in `/skill:jat-complete`

## Browser Tools

JAT includes browser automation tools in `~/.local/bin/`:

| Tool | Purpose |
|------|---------|
| `browser-start.js` | Launch Chrome with DevTools port |
| `browser-nav.js` | Navigate to URL |
| `browser-screenshot.js` | Capture screenshot |
| `browser-eval.js` | Execute JavaScript in page |
| `browser-pick.js` | Click element by selector |
| `browser-cookies.js` | Get/set cookies |
| `browser-wait.js` | Wait for condition |

## Steps

### STEP 1: Determine What to Test

Based on your recent work, identify:
- **URL**: What page to open
- **Feature**: What to test
- **Success criteria**: How to know it works

If unclear, ask the user.

### STEP 2: Open Browser and Navigate

```bash
browser-start.js
browser-nav.js --url "http://localhost:5173/tasks"
browser-screenshot.js --output /tmp/verify-initial.png
```

Show the screenshot and describe what you see.

### STEP 3: Test the Feature

Interact with what you built:

```bash
# Click elements
browser-pick.js --selector "button.create-task"

# Fill form fields
browser-eval.js "document.querySelector('input[name=title]').value = 'Test'"

# Check for elements
browser-eval.js "!!document.querySelector('.success-message')"

# Wait for content
browser-wait.js --text "Task created"
```

Take screenshots after each significant action.

### STEP 4: Check Console for Errors

```bash
browser-eval.js "window.__errors = []; const orig = console.error; console.error = (...a) => { window.__errors.push(a.join(' ')); orig.apply(console, a); }"
# ... test the feature ...
browser-eval.js "window.__errors"
```

### STEP 5: Report Findings

```
BROWSER VERIFICATION: {TASK_ID}

URL: http://localhost:5173/tasks
Feature: Task creation drawer

  [pass] Page loaded successfully
  [pass] Button visible and clickable
  [pass] Form renders correctly
  [pass] No console errors

Screenshots:
  /tmp/verify-initial.png
  /tmp/verify-after-action.png
```

If issues found, fix them and re-verify.

## After Verification

- **Passed**: Return to "READY FOR REVIEW" state
- **Failed**: Fix issues, re-verify, then return to review state
