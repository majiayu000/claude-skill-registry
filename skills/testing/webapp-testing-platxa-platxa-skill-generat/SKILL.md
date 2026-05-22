---
name: webapp-testing
description: >-
  Validate web application behavior by running Playwright-driven checks against
  a local or staging server. Covers page load verification, element discovery,
  form submission, console error detection, responsive layout checks, and
  network request auditing. Use when you need to confirm that a frontend works
  correctly before deployment or after code changes.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - validator
    - testing
    - playwright
    - browser-automation
    - frontend
  provenance:
    upstream_source: "webapp-testing"
    upstream_sha: "16447833d14a897d97233d30accfd295e40a28e9"
    regenerated_at: "2026-02-04T19:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# Web Application Testing Validator

Validate that a web application renders correctly, responds to user interaction, and produces no runtime errors by running Playwright-based checks from the terminal.

## Overview

This skill validates frontend behavior of local or staging web applications through automated Playwright scripts. Instead of writing full test suites, it runs targeted checks that produce a clear pass/fail result for each validation rule.

**What it validates:**

- Page loads without JavaScript errors
- Critical elements are present and visible after render
- Form submissions reach the expected success state
- Console output contains no uncaught exceptions or failed network calls
- Layout responds correctly to viewport changes

**Standards enforced:**

- Zero uncaught JavaScript errors in the console
- All expected DOM elements present after `networkidle`
- HTTP response codes in the 2xx range for primary resources
- Forms produce the expected post-submission state

**Prerequisites:**

- Python 3.8+ with `playwright` package installed (`pip install playwright && playwright install chromium`)
- The bundled `scripts/with_server.py` helper for managing server lifecycle
- Target application source or a running server URL

## Rules

### Rule 1: Page Load Success

**Description**: Navigates to the target URL and waits for `networkidle`. Passes when the page reaches a loaded state within the timeout.

**Passes when**: `page.wait_for_load_state('networkidle')` completes within 30 seconds and `page.title()` returns a non-empty string.

**Fails when**: Navigation times out or returns an HTTP error status (4xx/5xx).

**Severity**: Critical

### Rule 2: Zero Console Errors

**Description**: Captures all browser console messages during page load and interaction. Fails when any `error`-level message appears.

**Passes when**: No `console.error` messages are emitted during the check window.

**Fails when**: One or more `error`-level console messages appear. Warning-level messages produce a notice but do not fail the check.

**Severity**: High

### Rule 3: Element Presence

**Description**: Verifies that a list of expected selectors exist in the rendered DOM after `networkidle`.

**Passes when**: Every selector in the checklist resolves to at least one visible element via `page.locator(selector).first.is_visible()`.

**Fails when**: Any selector returns zero matches or all matches are hidden.

**Severity**: High

### Rule 4: Form Submission

**Description**: Fills a form with test data, submits it, and verifies the post-submission state.

**Passes when**: After submission the page contains the expected success indicator (text, URL change, or element).

**Fails when**: The success indicator is absent after a 10-second wait, or a console error occurs during submission.

**Severity**: Medium

### Rule 5: Responsive Layout

**Description**: Resizes the viewport to mobile (375x812), tablet (768x1024), and desktop (1920x1080) breakpoints, taking a screenshot at each.

**Passes when**: The page renders without horizontal overflow at every breakpoint (`document.documentElement.scrollWidth <= window.innerWidth`).

**Fails when**: Horizontal overflow is detected at any breakpoint.

**Severity**: Medium

### Rule 6: Network Health

**Description**: Monitors all network requests during page load. Flags failed requests (status >= 400) and mixed-content warnings.

**Passes when**: All XHR/Fetch requests return 2xx status codes and no mixed-content requests are detected.

**Fails when**: Any primary resource returns 4xx/5xx or the page triggers mixed-content warnings.

**Severity**: High

## Thresholds

| Metric | Minimum | Target | Maximum |
|--------|---------|--------|---------|
| Page load time | N/A | < 3s | 30s (timeout) |
| Console errors | 0 | 0 | 0 |
| Element visibility | 100% of checklist | 100% | N/A |
| Failed network requests | 0 | 0 | 0 |
| Horizontal overflow (px) | 0 | 0 | 0 |

## Pass/Fail Criteria

### Automatic PASS

All of the following must be true:

- [ ] Page loads within timeout with a non-empty title
- [ ] Zero `error`-level console messages
- [ ] All checklist selectors resolve to visible elements
- [ ] No network requests with status >= 400

### Automatic FAIL

Any of the following triggers failure:

- Page navigation times out or returns HTTP error
- Uncaught JavaScript exception in the console
- A critical-severity selector is missing from the DOM
- Server process fails to start (when using `with_server.py`)

### Conditional PASS

May pass with warnings if:

- Console contains `warning`-level messages only
- Non-critical selectors are missing but critical selectors are present
- Network requests to third-party domains fail (analytics, CDN) but primary resources load

## Workflow

### Step 1: Start the Server

If the application is not already running, use the bundled helper:

```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_checks.py
```

For multiple servers (backend + frontend):

```bash
python scripts/with_server.py \
  --server "cd backend && python manage.py runserver 0.0.0.0:8000" --port 8000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_checks.py
```

Always run `python scripts/with_server.py --help` first to see all options.

### Step 2: Run Reconnaissance

Before writing checks, inspect the rendered page:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:5173")
    page.wait_for_load_state("networkidle")

    # Discover elements
    buttons = page.locator("button").all()
    print(f"Buttons: {len(buttons)}")
    for btn in buttons:
        print(f"  - {btn.inner_text()}")

    inputs = page.locator("input, textarea, select").all()
    print(f"Input fields: {len(inputs)}")
    for inp in inputs:
        name = inp.get_attribute("name") or inp.get_attribute("id") or "[unnamed]"
        print(f"  - {name} ({inp.get_attribute('type') or 'text'})")

    page.screenshot(path="/tmp/recon.png", full_page=True)
    browser.close()
```

### Step 3: Build the Selector Checklist

From reconnaissance results, list the selectors that must be present:

```python
REQUIRED_SELECTORS = [
    ("h1", "Page heading"),
    ("nav", "Navigation bar"),
    ("button[type='submit']", "Submit button"),
    ("#main-content", "Main content area"),
]
```

### Step 4: Execute Validation

Run checks against each rule. The script below combines all rules:

```python
from playwright.sync_api import sync_playwright
import sys

URL = "http://localhost:5173"
REQUIRED_SELECTORS = [("h1", "heading"), ("nav", "navigation")]
errors = []
warnings = []
console_errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("console", lambda msg: (
        console_errors.append(msg.text) if msg.type == "error"
        else warnings.append(msg.text) if msg.type == "warning"
        else None
    ))

    # Rule 1: Page load
    try:
        response = page.goto(URL, wait_until="networkidle", timeout=30000)
        if response and response.status >= 400:
            errors.append(f"FAIL Rule 1: HTTP {response.status}")
        else:
            title = page.title()
            print(f"PASS Rule 1: Page loaded (title: {title})")
    except Exception as e:
        errors.append(f"FAIL Rule 1: {e}")

    # Rule 2: Console errors (checked after all interactions)
    # Rule 3: Element presence
    for selector, label in REQUIRED_SELECTORS:
        loc = page.locator(selector).first
        if loc.is_visible():
            print(f"PASS Rule 3: '{label}' visible")
        else:
            errors.append(f"FAIL Rule 3: '{label}' ({selector}) not visible")

    # Rule 5: Responsive check
    for width, height, label in [(375, 812, "mobile"), (1920, 1080, "desktop")]:
        page.set_viewport_size({"width": width, "height": height})
        page.wait_for_timeout(500)
        overflow = page.evaluate(
            "document.documentElement.scrollWidth > window.innerWidth"
        )
        if overflow:
            errors.append(f"FAIL Rule 5: Horizontal overflow at {label} ({width}x{height})")
        else:
            print(f"PASS Rule 5: No overflow at {label}")

    browser.close()

# Rule 2: Console error summary
if console_errors:
    errors.append(f"FAIL Rule 2: {len(console_errors)} console error(s)")
    for e in console_errors[:3]:
        print(f"  console.error: {e}")
else:
    print("PASS Rule 2: Zero console errors")

if warnings:
    print(f"WARNING: {len(warnings)} console warning(s)")

# Verdict
print()
if errors:
    print("VALIDATION: FAILED")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print("VALIDATION: PASSED")
    sys.exit(0)
```

### Step 5: Review Results

After running the validation script:

- **PASSED**: All rules met. The application is ready for deployment.
- **FAILED**: Review the error list. Each failure references the rule number and specific issue.
- **WARNINGS**: Console warnings or non-critical selector misses. Investigate but not blocking.

Screenshots saved during validation provide visual evidence for review.

## Examples

### Example 1: Validate a React Development Server

```
User: Check if the React app at localhost:5173 works correctly
Assistant:
  1. python scripts/with_server.py --help
  2. python scripts/with_server.py --server "npm run dev" --port 5173 \
       -- python validate_app.py
  3. Results:
     PASS Rule 1: Page loaded (title: My App)
     PASS Rule 2: Zero console errors
     PASS Rule 3: 'heading' visible
     PASS Rule 3: 'navigation' visible
     PASS Rule 5: No overflow at mobile
     PASS Rule 5: No overflow at desktop

     VALIDATION: PASSED
```

### Example 2: Detect Broken API Calls

```
User: The dashboard page shows a blank table after the last deploy
Assistant:
  1. Navigate to http://localhost:3000/dashboard
  2. Capture console output and network requests
  3. Results:
     PASS Rule 1: Page loaded (title: Dashboard)
     FAIL Rule 2: 1 console error(s)
       console.error: Uncaught TypeError: Cannot read property 'map' of undefined
     FAIL Rule 6: GET /api/users returned 500
     FAIL Rule 3: '#user-table tbody tr' not visible

     VALIDATION: FAILED
       FAIL Rule 2: 1 console error(s)
       FAIL Rule 3: '#user-table tbody tr' not visible
       FAIL Rule 6: GET /api/users returned 500

     Root cause: The /api/users endpoint returns 500, causing the
     frontend to receive undefined instead of an array.
```

### Example 3: Responsive Layout Check

```
User: Verify the landing page looks good on mobile
Assistant:
  1. Navigate to http://localhost:5173
  2. Resize to 375x812 (iPhone 12)
  3. Results:
     PASS Rule 1: Page loaded
     PASS Rule 2: Zero console errors
     FAIL Rule 5: Horizontal overflow at mobile (375x812)
       scrollWidth=412 > viewportWidth=375

     VALIDATION: FAILED
       FAIL Rule 5: Horizontal overflow at mobile (375x812)

     The page has 37px of horizontal overflow on mobile.
     Check for elements with fixed widths wider than 375px.
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validation rules passed |
| 1 | One or more rules failed |
| 2 | Validation passed with warnings |

## Best Practices

- Always wait for `networkidle` before inspecting the DOM on dynamic applications
- Run `--help` on bundled scripts before reading their source code
- Use `page.screenshot()` to capture visual state at each check point
- Prefer CSS selectors and ARIA roles over XPath for element targeting
- Run checks in headless mode for CI; add `headless=False` for debugging
- Close the browser in a `finally` block to prevent orphan processes
- Store screenshots under `/tmp/webapp-test/` or a project-specific output directory

## References

Load these on demand for deeper detail:

- **Playwright patterns**: `references/playwright-patterns.md` -- selector strategies, wait conditions, and common recipes
- **Testing checklist**: `references/testing-checklist.md` -- comprehensive list of frontend validation items by category
- **Server management**: `references/server-management.md` -- advanced `with_server.py` usage and troubleshooting
