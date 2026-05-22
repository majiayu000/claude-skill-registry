---
name: ops-browser-uat
description: Browser-based user acceptance testing via Playwright MCP tools. Logs into the application, navigates through features, and captures visual proof with screenshots.
allowed-tools:
  - Bash
  - Read
---

# Ops: Browser UAT

Perform browser-based user acceptance testing using Playwright MCP tools.

**Argument**: `$ARGUMENTS` — scenario and environment (e.g., `smoke-test dev`, `login staging`, `player-detail dev`, `custom production /path`)

## Prerequisites

1. **Load Playwright MCP tools** — use `ToolSearch` to search for `playwright browser` and load all browser tools.
2. **Verify target environment is up** — curl check the frontend URL before launching the browser.
3. **For localhost** — ensure the frontend is running on port 8081.

## Discovery

Before running any scenario, read these project files to discover configuration:

1. **`e2e/constants.ts`** — environment URLs, test credentials (phone, OTP), timeouts, viewports
2. **`e2e/selectors.ts`** — all `data-testid` values organized by feature area
3. **`e2e/fixtures/auth.fixture.ts`** — exact login/logout flow to replicate via MCP tools
4. **`playwright.config.ts`** — video/trace recording config, test directory

## Authentication Procedure

Replicate the login flow from `e2e/fixtures/auth.fixture.ts` using Playwright MCP tools. Read the file to get the exact steps, which typically follow this pattern:

### Login

1. `browser_navigate` to `{BASE_URL}/signin`
2. `browser_snapshot` to discover page elements
3. `browser_fill_form` — fill the phone input (discover placeholder text from auth fixture)
4. Wait for form validation debounce (typically 500ms)
5. `browser_click` — click the "Next" button
6. `browser_wait_for` — wait for URL to contain `confirm-code` (timeout from constants)
7. `browser_snapshot` to discover OTP input
8. `browser_fill_form` — fill the OTP input (discover testid from selectors, value from constants)
9. `browser_wait_for` — wait for URL to NOT contain `confirm-code`
10. `browser_take_screenshot` — capture login proof

### Dismiss Error Overlay

Expo's development error overlay may appear. Dismiss it:

1. `browser_evaluate` with script:
   ```javascript
   document.getElementById('error-overlay')?.remove();
   document.querySelectorAll('[id*="error"]').forEach(el => el.remove());
   ```
2. `browser_press_key` — press "Escape" as backup

### Check if Logged In

```javascript
// browser_evaluate
localStorage.getItem("@authData") !== null
```

### Logout

Discover the menu button and sign-out flow from `e2e/selectors.ts` and `e2e/fixtures/auth.fixture.ts`:

1. `browser_click` — menu button element (discover testid from selectors)
2. `browser_click` — element with text "Sign Out"
3. `browser_wait_for` — URL contains `signin`

## Selector Reference

Read `e2e/selectors.ts` to get the complete `data-testid` reference for the project. The selectors object is organized by feature area (auth, nav, home sections, player detail, etc.).

Use `[data-testid="{TESTID}"]` to target elements in Playwright MCP tools.

## Built-in UAT Scenarios

### 1. smoke-test

Full app walkthrough. Read `e2e/selectors.ts` to identify which sections and elements to verify:

1. **Login** (auth procedure above)
2. **Home screen** — verify key sections exist using selectors from the project
3. **Feature pages** — navigate to 2-3 key routes and verify content loads
4. **Logout** → verify redirect to signin
5. Screenshot at each step

### 2. login

Just the login flow with screenshot proof.

### 3. home-screen

Login → verify all home screen sections have data. Screenshot each section.

### 4. custom

Login → navigate to user-specified URL → interact as instructed → screenshot.

## Proof Recording

At each verification point:

1. `browser_take_screenshot` — visual proof of current state
2. `browser_console_messages` — check for JavaScript errors
3. `browser_network_requests` — monitor for failed API calls (4xx, 5xx)

## Output Format

Report UAT results as a table:

| Step | Action | Status | Notes |
|------|--------|--------|-------|
| 1 | Navigate to /signin | PASS | Page loaded in 1.2s |
| 2 | Enter phone number | PASS | Input accepted |
| 3 | Click Next | PASS | Navigated to /confirm-code |
| 4 | Enter OTP | PASS | OTP accepted |
| 5 | Verify home screen | PASS | All sections present |
| 6 | Logout | PASS | Redirected to /signin |

Include total PASS/FAIL count and any JS errors or failed network requests observed.
