---
name: ms-playwright-mcp
description: Apply when automating browser interactions, web scraping, or UI testing with AI agents
---

# Playwright MCP Guide

Rules and usage for Microsoft Playwright MCP server.

## Table of Contents

**Core**
- [MUST-NOT-FORGET](#must-not-forget)
- [Configuration](#configuration)
- [Available Tools](#available-tools)

**Workflows**
- [Common Workflows](#common-workflows)
- [Advanced Workflows](PLAYWRIGHT_ADVANCED_WORKFLOWS.md) - Cookie popups, scrolling, expanding items, full page screenshots

**Reference**
- [Element Selection](#element-selection)
- [Authentication](PLAYWRIGHT_AUTHENTICATION.md) - Persistent profiles, storage state, extension mode
- [Troubleshooting](PLAYWRIGHT_TROUBLESHOOTING.md) - Common issues, flaky tests
- [Setup](SETUP.md) - Installation

## Intent Lookup

**User wants to...**
- **Research a topic / read articles** → Navigate, dismiss cookie popup, scroll for lazy content, screenshot
- **Find a product / compare prices** → Navigate, search, extract data with `browser_evaluate`
- **Fill out a form / submit application** → Use `browser_fill` for fields, `browser_click` for submit
- **Download file / attachment** → First find links with [Section 5](PLAYWRIGHT_ADVANCED_WORKFLOWS.md#5-find-and-extract-links), then click to download
- **Log into a site** → Fill credentials, submit; use [PLAYWRIGHT_AUTHENTICATION.md](PLAYWRIGHT_AUTHENTICATION.md) to stay logged in
- **Do a bank transfer / pay bills** → Requires persistent profile for auth; use `browser_snapshot` before each action
- **Check email / download attachments** → Navigate to webmail, expand messages, click attachment links
- **Archive a webpage** → See [PLAYWRIGHT_ADVANCED_WORKFLOWS.md](PLAYWRIGHT_ADVANCED_WORKFLOWS.md) for full page screenshot workflow
- **Interact with dynamic content** → Scroll to load lazy content, expand collapsed sections, then proceed

**UI testing...**
- **Verify page loads correctly** → Navigate, `browser_snapshot`, check expected elements present
- **Test form validation** → Submit empty/invalid data, check error messages appear
- **Test navigation flow** → Click through menus, verify correct pages load
- **Test responsive layout** → Resize browser, screenshot at different widths
- **Test button states** → Hover, click, verify visual/functional changes
- **Test modal dialogs** → Trigger modal, interact, close, verify dismissed
- **Test error states** → Force errors (bad URL, timeout), verify error handling
- **Test accessibility** → Use `browser_snapshot` (accessibility tree), check refs have labels
- **Compare before/after** → Screenshot before change, screenshot after, compare
- **Test login/logout** → Full auth flow, verify session state

**Technical tasks...**
- **Handle cookie popup** → [PLAYWRIGHT_ADVANCED_WORKFLOWS.md#1-close-cookie-popups](PLAYWRIGHT_ADVANCED_WORKFLOWS.md#1-close-cookie-popups)
- **Run custom JavaScript** → `browser_evaluate(expression: "...")`
- **Debug failures** → [PLAYWRIGHT_TROUBLESHOOTING.md](PLAYWRIGHT_TROUBLESHOOTING.md)

## MUST-NOT-FORGET

- Use accessibility tree (not screenshots) for element selection
- Reference elements via `ref=e5` format from `browser_snapshot`
- Always call `browser_snapshot` before clicking to get current refs
- Use `browser_close` when done to free resources
- For logged-in sessions: Use persistent user profile or storage state

## Configuration

**Repository**: https://github.com/microsoft/playwright-mcp
**Package**: `@playwright/mcp`

**Basic (isolated session):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Persistent profile (remembers logins):**
```json
{
  "args": ["@playwright/mcp@latest", "--user-data-dir", "[USER_PROFILE_PATH]/.ms-playwright-mcp-profile"]
}
```

**Headless:** Add `"--headless"` to args.

**Timeouts:** Add `"--timeout-action", "10000", "--timeout-navigation", "120000"` for slow pages.

## Available Tools

### Navigation
- **browser_navigate** - `browser_navigate(url: "https://example.com")`

### Element Interaction
- **browser_snapshot** - Get accessibility tree with element refs
- **browser_click** - `browser_click(element: "Button", ref: "e12")`
- **browser_type** - `browser_type(element: "Input", ref: "e8", text: "query")`
- **browser_fill** - `browser_fill(element: "Email", ref: "e3", value: "user@example.com")`
- **browser_select** - `browser_select(element: "Country", ref: "e15", values: ["USA"])`
- **browser_hover** - `browser_hover(element: "Menu", ref: "e5")`
- **browser_drag** - Drag and drop between elements
- **browser_press_key** - `browser_press_key(key: "Enter")` or `browser_press_key(key: "Control+A")`

### Inspection
- **browser_screenshot** - `browser_screenshot()` or `browser_screenshot(fullPage: true)`
- **browser_console_messages** - Get console logs
- **browser_evaluate** - `browser_evaluate(expression: "document.title")`

### Timing
- **browser_wait_for** - `browser_wait_for(time: 2)` wait seconds, or `browser_wait_for(text: "Loading")` wait for text

### Session
- **browser_close** - Close browser and free resources

## Common Workflows

### Navigate and Click
```
1. browser_navigate(url: "https://example.com")
2. browser_snapshot()
3. browser_click(element: "Login button", ref: "e12")
```

### Fill Form
```
1. browser_snapshot()
2. browser_fill(element: "Username", ref: "e3", value: "user@example.com")
3. browser_fill(element: "Password", ref: "e5", value: "password123")
4. browser_click(element: "Submit", ref: "e8")
```

### Wait for Content
After navigation or click, call `browser_snapshot()` to verify page loaded and get updated refs.

### Full Page Screenshot
```
browser_screenshot(fullPage: true)
```

For cookie popups, lazy-load scrolling, and expanding collapsed items, see [PLAYWRIGHT_ADVANCED_WORKFLOWS.md](PLAYWRIGHT_ADVANCED_WORKFLOWS.md).

## Element Selection

### Using Refs from Snapshot

1. Call `browser_snapshot()` to get current page structure
2. Find element in returned accessibility tree
3. Use the `ref` value in subsequent commands

**Example snapshot output:**
```
- banner [ref=e3]:
    - link "Home" [ref=e5] [cursor=pointer]
    - navigation [ref=e12]:
        - link "Docs" [ref=e13]
```

### Selector Priority

When refs unavailable, use stable selectors:
1. `[data-testid="submit"]` - Best
2. `getByRole('button', { name: 'Save' })` - Semantic
3. `getByText('Sign in')` - User-facing
4. `input[name="email"]` - HTML attributes
5. Avoid: `.btn-primary`, `#submit` - Classes/IDs change

## Requirements

- Node.js 18+ with npx in PATH
- Chrome/Chromium for headed mode

See [SETUP.md](SETUP.md) for installation details.
