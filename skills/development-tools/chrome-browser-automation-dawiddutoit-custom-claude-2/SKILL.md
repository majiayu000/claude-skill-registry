---
name: chrome-browser-automation
description: |
  Automates Chrome browser workflows for testing web apps, debugging with console/network logs,
  extracting data, filling forms, and interacting with authenticated web applications (Google Docs,
  Gmail, Notion). Use when testing local web apps, debugging frontend issues, automating data entry,
  scraping web content, or working with authenticated services. Triggers on "test my web app",
  "check the console", "fill this form", "extract data from [URL]", "automate [browser task]",
  "open [authenticated app]", or debugging web application issues. Works with Chrome via Claude in
  Chrome extension (MCP tools: navigate, click, form_input, read_console_messages, read_network_requests,
  tabs_context_mcp, gif_creator).

---

# Chrome Browser Automation

## Quick Start

Test a local web application with console monitoring:

```
User: "Open localhost:3000 and check for console errors when I submit the login form"

1. Get tab context: tabs_context_mcp(createIfEmpty=true)
2. Navigate to app: navigate(url="http://localhost:3000", tabId=<id>)
3. Monitor console: read_console_messages(tabId=<id>, onlyErrors=true)
4. Fill form: form_input(ref="email", value="test@example.com", tabId=<id>)
5. Submit: computer(action="left_click", ref="submit-btn", tabId=<id>)
6. Check errors: read_console_messages(tabId=<id>, onlyErrors=true)
7. Check network: read_network_requests(tabId=<id>, urlPattern="/api/")
8. Report findings with specific error messages and failed requests
```

**Key advantage:** Chain browser actions with terminal commands in a single workflow.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Setup and Prerequisites
4. Core Workflow Patterns
   - 4.1 Testing Web Applications
   - 4.2 Debugging with Console and Network
   - 4.3 Data Extraction
   - 4.4 Form Automation
   - 4.5 Authenticated Web Apps
   - 4.6 Multi-Site Workflows
5. MCP Tool Reference
6. Best Practices
7. Troubleshooting
8. Integration with Other Skills

## When to Use This Skill

**Explicit Triggers:**
- "Test my web app" / "Check the console"
- "Fill this form" / "Extract data from [URL]"
- "Automate [browser task]" / "Open [authenticated app]"
- "Debug [frontend issue]" / "Verify [UI behavior]"

**Implicit Triggers:**
- Frontend bug investigation requiring console logs
- Repetitive data entry or form filling
- Web scraping or data extraction from live sites
- Testing form validation or user flows
- Interacting with authenticated services (Gmail, Docs, Notion)
- Visual regression testing or design verification

**Debugging Triggers:**
- "Why is this breaking in the browser?"
- "What console errors appear when I..."
- "What network requests are failing?"

## What This Skill Does

Chrome integration enables six core capabilities:

1. **Live Debugging** - Read console errors and DOM state, identify root cause, fix code
2. **Web App Testing** - Verify form validation, check user flows, test local development servers
3. **Data Extraction** - Scrape structured data from web pages and save locally
4. **Form Automation** - Automate repetitive data entry, form filling, multi-site workflows
5. **Authenticated Apps** - Interact with Google Docs, Gmail, Notion, or any logged-in service
6. **Session Recording** - Capture browser interactions as annotated GIFs for documentation

## Setup and Prerequisites

**Required:**
- Google Chrome browser
- Claude in Chrome extension v1.0.36+ (from Chrome Web Store)
- Claude Code CLI v2.0.73+ (`claude --version`)
- Paid Claude plan (Pro, Team, or Enterprise)

**Enable Chrome integration:**

```bash
# Start with Chrome enabled
claude --chrome

# Or enable from within session
/chrome
```

**Verify connection:**

```bash
# Check status and manage settings
/chrome

# List available MCP tools
/mcp
# Click into 'claude-in-chrome' to see all tools
```

**Enable by default (optional):**

Run `/chrome` and select "Enabled by default" to avoid `--chrome` flag each time.

**Note:** Chrome integration requires a visible browser window. You'll see Chrome open and navigate in real time - there's no headless mode.

## Core Workflow Patterns

### 4.1 Testing Web Applications

**Pattern: Test local development server**

```
Workflow:
1. tabs_context_mcp(createIfEmpty=true) → Get tabId
2. navigate(url="http://localhost:3000", tabId=<id>)
3. computer(action="screenshot", tabId=<id>) → Visual verification
4. form_input(ref="username", value="testuser", tabId=<id>)
5. computer(action="left_click", ref="submit", tabId=<id>)
6. read_console_messages(tabId=<id>, onlyErrors=true)
7. read_network_requests(tabId=<id>, urlPattern="/api/auth")
8. Report: Success/failure with specific errors or network issues
```

**Common testing scenarios:**
- Form validation (submit invalid data, verify error messages)
- User flows (signup → login → dashboard → action)
- Visual regressions (screenshot before/after changes)
- API integration (verify network requests match expectations)

**Example request:**
```
"I just updated the signup form. Can you test it on localhost:3000?
Try submitting with invalid email, then valid data, and check if
the success message appears."
```

### 4.2 Debugging with Console and Network

**Pattern: Investigate frontend errors**

```
Workflow:
1. tabs_context_mcp() → Get current tab
2. read_console_messages(
     tabId=<id>,
     pattern="error|exception|failed",
     onlyErrors=true
   )
3. read_network_requests(
     tabId=<id>,
     urlPattern="/api/",
     filterStatus=[400, 401, 403, 404, 500, 502, 503]
   )
4. Analyze errors:
   - Console: TypeError, ReferenceError, network failures
   - Network: Failed requests, 401 unauthorized, 500 server errors
5. Identify root cause (missing API endpoint, CORS issue, auth token expired)
6. Suggest fix in codebase (update API call, add error handling, fix endpoint)
```

**Example request:**
```
"The dashboard page is throwing errors. Can you check what's failing?"
```

**Common debugging patterns:**
- CORS issues (network request blocked, check headers)
- API authentication (401/403, check token in request headers)
- Missing dependencies (module not found, check imports)
- Runtime errors (undefined variables, null references)

See `references/debugging-patterns.md` for comprehensive error analysis workflows.

### 4.3 Data Extraction

**Pattern: Scrape structured data from web pages**

```
Workflow:
1. tabs_context_mcp(createIfEmpty=true)
2. navigate(url="https://example.com/products", tabId=<id>)
3. get_page_text(tabId=<id>) → Full page text
4. Parse structured data:
   - Product names
   - Prices
   - Availability
   - URLs
5. Save to CSV/JSON:
   Write(file_path="products.csv", content=<data>)
6. Report: "Extracted 47 products to products.csv"
```

**Example request:**
```
"Go to the product listings page and extract the name, price, and
availability for each item. Save as CSV."
```

**Advanced extraction:**
- Multi-page pagination (loop through pages)
- Dynamic content (wait for AJAX to load)
- Authenticated data (use logged-in session)

See `examples/data-extraction-examples.md` for complex scraping workflows.

### 4.4 Form Automation

**Pattern: Automate repetitive data entry**

```
Workflow:
1. Read local data: Read(file_path="contacts.csv")
2. Parse CSV rows
3. For each row:
   a. tabs_context_mcp()
   b. navigate(url="https://crm.example.com/add-contact", tabId=<id>)
   c. form_input(ref="name", value=row.name, tabId=<id>)
   d. form_input(ref="email", value=row.email, tabId=<id>)
   e. form_input(ref="phone", value=row.phone, tabId=<id>)
   f. computer(action="left_click", ref="submit", tabId=<id>)
   g. Wait for confirmation
4. Report: "Processed 15 contacts successfully"
```

**Example request:**
```
"I have customer contacts in contacts.csv. For each row, go to
our CRM and fill in the contact form."
```

**Form filling tips:**
- Use `form_input` for text fields (faster than typing)
- Use `computer(action="left_click")` for buttons
- Use `computer(action="type")` for rich text editors
- Wait between submissions to avoid rate limits

### 4.5 Authenticated Web Apps

**Pattern: Interact with Google Docs, Gmail, Notion**

```
Workflow:
1. tabs_context_mcp() → Access existing logged-in session
2. navigate(url="https://docs.google.com/document/d/abc123", tabId=<id>)
3. computer(action="left_click", coordinate=[400, 300], tabId=<id>) → Click into editor
4. computer(action="type", text="Meeting notes:\n- Discussed Q1 roadmap", tabId=<id>)
5. Verify: get_page_text(tabId=<id>) → Check content saved
6. Report: "Added meeting notes to Google Doc"
```

**Example request:**
```
"Draft a project update based on recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123"
```

**Supported authenticated apps:**
- Google Workspace (Docs, Sheets, Gmail, Calendar)
- Notion (databases, pages)
- Slack (channels, DMs)
- GitHub (issues, PRs)
- Any service you're logged into in Chrome

**Authentication handling:**
- Uses your existing browser login state (no credential entry needed)
- If you hit a login page, Claude pauses and asks you to log in manually
- Claude never handles passwords or 2FA (you complete authentication)

### 4.6 Multi-Site Workflows

**Pattern: Coordinate tasks across multiple websites**

```
Workflow:
1. Check calendar for meetings tomorrow
   - navigate(url="https://calendar.google.com", tabId=<id>)
   - get_page_text(tabId=<id>)
   - Extract meeting attendees
2. For each external attendee:
   - tabs_create_mcp() → New tab
   - navigate(url="https://linkedin.com/in/{name}", tabId=<new-id>)
   - get_page_text(tabId=<new-id>)
   - Extract company info
3. Return to calendar tab
   - navigate(url="https://calendar.google.com/event/{id}", tabId=<id>)
   - Add note about attendee's company
4. Report: "Added context notes for 3 external meetings"
```

**Example request:**
```
"Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company on LinkedIn and add a
note about what they do."
```

**Tab management:**
- `tabs_context_mcp()` - Get current tab info
- `tabs_create_mcp()` - Create new tab
- Switch between tabs by using different tabId values

## MCP Tool Reference

**Core Navigation:**
- `navigate(url, tabId)` - Navigate to URL
- `computer(action="left_click", coordinate/ref, tabId)` - Click element
- `computer(action="type", text, tabId)` - Type text
- `form_input(ref, value, tabId)` - Fill form field (faster than typing)

**Data Retrieval:**
- `get_page_text(tabId)` - Get full page text
- `read_page(tabId)` - Get page content with structure
- `find(selector, tabId)` - Find elements matching selector

**Debugging:**
- `read_console_messages(tabId, pattern, onlyErrors)` - Get console logs
- `read_network_requests(tabId, urlPattern, filterStatus)` - Get network requests

**Tab Management:**
- `tabs_context_mcp(createIfEmpty)` - Get current tab info (always call first)
- `tabs_create_mcp()` - Create new tab
- `browser_close(tabId)` - Close tab

**Recording:**
- `gif_creator(action="start_recording", tabId)` - Start GIF recording
- `gif_creator(action="stop_recording", tabId)` - Stop recording
- `gif_creator(action="export", tabId, filename, options)` - Export GIF

**Visual:**
- `computer(action="screenshot", tabId)` - Take screenshot
- `browser_resize(width, height, tabId)` - Resize browser window

For detailed parameter schemas, run:
```bash
mcp-cli info claude-in-chrome/<tool-name>
```

See `references/mcp-tool-reference.md` for comprehensive parameter documentation.

## Best Practices

**Always start with tab context:**
```
tabs_context_mcp(createIfEmpty=true) → Get tabId
```
Without this, you won't have a valid tabId for subsequent operations.

**Handle authentication gracefully:**
- Never ask for passwords or API keys
- If you hit a login page, pause and ask user to log in manually
- Resume workflow after user confirms "I'm logged in"

**Monitor console and network during testing:**
```
read_console_messages(tabId=<id>, onlyErrors=true)
read_network_requests(tabId=<id>, urlPattern="/api/")
```
Report specific errors, not generic "something failed".

**Use appropriate input methods:**
- `form_input` - Text fields (fast, reliable)
- `computer(action="type")` - Rich text editors, contenteditable
- `computer(action="left_click")` - Buttons, links, dropdowns

**Wait for page loads:**
```
navigate(url="...", tabId=<id>)
computer(action="wait", duration=2, tabId=<id>) → Let page load
```
Dynamic content (AJAX, React) needs time to render.

**Filter console output:**
```
read_console_messages(
  tabId=<id>,
  pattern="error|exception|failed",
  onlyErrors=true
)
```
Console logs can be verbose - focus on errors.

**Dismiss modal dialogs manually:**
JavaScript alerts/confirms block browser events. If a dialog appears, ask user to dismiss it and tell Claude to continue.

**Fresh tabs for unresponsive sessions:**
If a tab becomes unresponsive, create a new tab:
```
tabs_create_mcp() → New tabId
```

## Troubleshooting

**Extension not detected:**
1. Verify Claude in Chrome extension v1.0.36+ installed
2. Verify Claude Code CLI v2.0.73+ (`claude --version`)
3. Check Chrome is running
4. Run `/chrome` → "Reconnect extension"
5. Restart both Claude Code and Chrome if needed

**Browser not responding:**
1. Check for modal dialog (alert, confirm, prompt) blocking page
2. Ask Claude to create new tab and retry
3. Restart Chrome extension (disable and re-enable)

**First-time setup issues:**
First use installs native messaging host. If permission errors occur, restart Chrome.

**Console/network requests not appearing:**
1. Verify page is fully loaded (wait 2-3 seconds after navigate)
2. Check URL pattern matches actual requests
3. Try without filters first (get all logs, then refine)

**Form input not working:**
1. Verify element reference is correct (use `find` to locate)
2. Try `computer(action="type")` instead of `form_input`
3. Click into field first: `computer(action="left_click", ref=<field>)`

See `references/troubleshooting.md` for detailed diagnostic workflows.

## Integration with Other Skills

**With chrome-gif-recorder:**
Record visual tutorials of web workflows with annotations.

**With quality-code-review:**
Test changes in browser before committing (verify UI works correctly).

**With observability-analyze-logs:**
Combine application logs with browser console for full-stack debugging.

**With create-adr-spike:**
Research libraries by navigating documentation sites and extracting examples.

**Example integrated workflow:**
```
1. Make code changes (terminal)
2. Test in browser with console monitoring (chrome-browser-automation)
3. Record successful demo as GIF (chrome-gif-recorder)
4. Run quality gates (quality-run-quality-gates)
5. Commit with proof-of-work GIF (git commit)
```

## Supporting Files

**references/**
- `mcp-tool-reference.md` - Detailed MCP tool parameters and schemas
- `debugging-patterns.md` - Console/network error analysis workflows
- `troubleshooting.md` - Common issues and diagnostic procedures

**examples/**
- `testing-examples.md` - Web app testing patterns (form validation, user flows)
- `data-extraction-examples.md` - Scraping workflows (pagination, dynamic content)
- `authenticated-app-examples.md` - Google Docs, Gmail, Notion workflows
- `multi-site-examples.md` - Complex multi-tab coordination patterns

## Expected Outcomes

**Successful web app test:**
```
✅ Web App Tested Successfully

URL: http://localhost:3000/login
Test: Form validation with invalid/valid data
Console: 0 errors
Network: POST /api/auth → 200 OK (token received)
Result: Success message displayed correctly

All validations passed!
```

**Debugging with errors found:**
```
⚠️ Frontend Issues Detected

Console Errors:
1. TypeError: Cannot read property 'name' of undefined
   - File: dashboard.js:42
   - Cause: API response missing 'user' object

Network Failures:
1. GET /api/user/preferences → 401 Unauthorized
   - Cause: Auth token expired

Recommendations:
1. Add null check: user?.name || 'Unknown'
2. Refresh auth token before API call
```

**Data extraction success:**
```
✅ Data Extracted Successfully

Source: https://example.com/products
Extracted: 47 products
Fields: name, price, availability, url
Output: products.csv (8KB)

Sample data:
- Widget Pro, $49.99, In Stock, /products/widget-pro
- Gadget Plus, $79.99, Backordered, /products/gadget-plus
```

## Expected Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Frontend debugging time | 15-30 min | 3-5 min | 80% faster |
| Form automation (50 entries) | 60 min manual | 5 min automated | 90% faster |
| Multi-site data gathering | 30 min | 5 min | 83% faster |
| Test coverage (manual check) | Ad-hoc | Systematic | 100% reliability |

## Success Metrics

A successful browser automation workflow meets these criteria:

✅ Tab context retrieved before operations
✅ Navigation completed successfully
✅ Console/network monitoring included for testing
✅ Specific errors reported (not generic failures)
✅ Data extraction validated (row counts, field completeness)
✅ Form submissions confirmed (success messages visible)
✅ Authentication handled gracefully (no credential exposure)
✅ Results saved locally (CSV, JSON, screenshots)

## Requirements

**Browser:** Chrome with Claude in Chrome extension v1.0.36+, visible window required
**CLI:** Claude Code v2.0.73+, started with `--chrome` flag or `/chrome` enabled
**Permissions:** Chrome extension permissions for target sites (manage in extension settings)
**Network:** Internet access for web navigation, local server access for development testing

## Red Flags to Avoid

1. **Skipping tab context** - Always call `tabs_context_mcp()` first
2. **Handling passwords** - Never ask for credentials, let user log in manually
3. **Ignoring console errors** - Always check console during testing
4. **Generic error reports** - Report specific error messages and stack traces
5. **Not waiting for page loads** - Add waits after navigation for dynamic content
6. **Skipping network monitoring** - Check network requests for API failures
7. **Using wrong input method** - `form_input` for fields, `type` for rich text
8. **Continuing after modal dialogs** - Ask user to dismiss alerts/confirms
9. **Not verifying data extraction** - Validate row counts and field completeness
10. **Exposing sensitive data** - Never log passwords, tokens, or PII

## Notes

**Architecture:**
- Claude Code (CLI) ↔ Native Messaging API ↔ Claude in Chrome Extension ↔ Browser
- Extension has same permissions as your browser (site-level permissions inherited)
- No headless mode - browser window must be visible

**Privacy:**
- Uses existing browser login state (no credential storage)
- Browser automation shares your session (cookies, tokens)
- Screenshot/GIF recording captures visible content only

**Performance:**
- Console logs can be verbose (filter with pattern/onlyErrors)
- Network requests accumulate (use urlPattern to filter)
- Page loads vary (wait 2-3 seconds for dynamic content)

**Limitations:**
- Google Chrome only (Brave, Arc, other Chromium browsers not supported)
- WSL (Windows Subsystem for Linux) not supported
- Modal dialogs (alert/confirm/prompt) block automation
- CAPTCHAs and login pages require manual user intervention

**Context usage:**
- Enabling `--chrome` by default increases context usage (all tools loaded)
- Use flag only when needed if context consumption is a concern
- Run `/chrome` to check current settings
