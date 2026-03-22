---
name: test-browsy-flow
description: Test a URL with the browsy CLI and report page detection accuracy
---

# Test Browsy Flow

Test browsy's page detection and interaction capabilities against a specific URL. Useful for validating that browsy correctly parses a site before deploying agents against it.

## Usage

```
/test-browsy-flow https://example.com/login
```

## What it does

Runs the browsy CLI against a target URL and reports on detection quality:

- **Page parsing** — fetches the URL and converts it to browsy's Spatial DOM, reporting element counts and types
- **Page classification** — checks whether browsy correctly identifies the page type (Login, Search, Content, Form, Consent, Verification, Error)
- **Suggested actions** — validates that browsy suggests the right actions (e.g., Login for a sign-in page, Search for a search engine)
- **Element inventory** — counts interactive elements (links, buttons, inputs, selects, checkboxes) and checks for missing or misidentified elements
- **Hidden content** — verifies that dropdown menus, modals, accordion panels, and tab content are exposed with `hidden: true`
- **Interaction testing** — optionally tests clicking, typing, and form submission to verify browsy handles the page's interaction patterns

## Workflow

1. Run `browsy browse <url>` to fetch and parse the page
2. Run `browsy page-info` to get detection results
3. Analyze the Spatial DOM output:
   - Count elements by type (links, buttons, inputs, text)
   - Check for landmark markers (nav, header, footer, main, form)
   - Verify hidden elements are exposed
4. Optionally test interactions:
   - Click a link or button
   - Fill a form field
   - Submit a search query
5. Report findings with pass/fail assessment

## Example output

```
=== Browsy Flow Test: https://example.com/login ===

Page title: Sign In - Example App
Page type: Login [CORRECT]
Suggested actions: Login [CORRECT]

Elements detected: 12
  Links: 3 (Home, Forgot password, Sign up)
  Buttons: 1 (Sign in)
  Inputs: 2 (email [text], password [password])
  Text: 4 (heading, labels, helper text)
  Hidden: 2 (error alert, password tooltip)

Landmarks:
  [PASS] <form> detected as form landmark
  [PASS] <nav> detected as navigation landmark
  [PASS] <main> detected as main landmark

Interaction test:
  [PASS] browsy_type_text on email field — value persisted
  [PASS] browsy_type_text on password field — value persisted
  [PASS] browsy_login compound action — form submitted

Result: 9/9 checks passed. Page fully compatible with browsy.
```

## Example with issues

```
=== Browsy Flow Test: https://spa-heavy.example.com ===

Page title: App
Page type: Content [EXPECTED: Dashboard]
Suggested actions: (none) [EXPECTED: Login or Navigation]

Elements detected: 3
  Links: 1 (logo link)
  Text: 2 (loading spinner text, noscript message)

WARNING: Only 3 elements detected. This page likely requires
JavaScript rendering. Consider using Playwright for this site.

Result: 1/5 checks passed. Page NOT compatible with browsy.
Recommendation: Keep Playwright for this JS-heavy SPA.
```

## Requirements

- browsy CLI must be installed (`browsy` in PATH or set `BROWSY_BIN` env var)
