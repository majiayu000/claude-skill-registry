---
name: dev-test-chrome
description: "Chrome MCP browser testing. Console/network debugging, JS execution, GIF recording."
---

**Announce:** "I'm using dev-test-chrome for Chrome browser automation with debugging."

<EXTREMELY-IMPORTANT>
## Gate Reminder

Before taking screenshots or running E2E tests, you MUST complete all 6 gates from dev-tdd:

```
GATE 1: BUILD
GATE 2: LAUNCH (with file-based logging)
GATE 3: WAIT
GATE 4: CHECK PROCESS
GATE 5: READ LOGS ← MANDATORY, CANNOT SKIP
GATE 6: VERIFY LOGS
THEN: E2E tests/screenshots
```

**You loaded dev-tdd earlier. Follow the gates now.**
</EXTREMELY-IMPORTANT>

## Contents

- [Tool Availability Gate](#tool-availability-gate)
- [When to Use Chrome MCP](#when-to-use-chrome-mcp)
- [MCP Tools Overview](#mcp-tools-overview)
- [Console Debugging](#console-debugging)
- [Network Request Inspection](#network-request-inspection)
- [JavaScript Execution](#javascript-execution)
- [Navigation & Interaction](#navigation--interaction)
- [GIF Recording](#gif-recording)
- [Complete E2E Examples](#complete-e2e-examples)

# Chrome MCP Browser Automation

<EXTREMELY-IMPORTANT>
## Tool Availability Gate

**Verify Chrome MCP tools are available before proceeding.**

Check for these MCP functions:
- `mcp__claude-in-chrome__read_page`
- `mcp__claude-in-chrome__navigate`
- `mcp__claude-in-chrome__read_console_messages`
- `mcp__claude-in-chrome__read_network_requests`

**If MCP tools are not available:**
```
STOP: Cannot proceed with Chrome MCP automation.

Missing: Chrome MCP server (claude-in-chrome extension)

The Chrome MCP requires:
1. Chrome browser with claude-in-chrome extension installed
2. Extension connected to Claude Code
3. Browser window visible (not headless)

Check your Claude Code MCP configuration.

Reply when configured and I'll continue testing.
```

**This gate is non-negotiable. Missing tools = full stop.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## When to Use Chrome MCP

**USE Chrome MCP when you need:**
- Console message debugging (`console.log`, `console.error`)
- Network request inspection (API calls, XHR, Fetch)
- JavaScript execution in page context
- GIF recording of interactions
- Interactive debugging with real browser
- Natural language element finding

**DO NOT use Chrome MCP when:**
- Running in CI/CD (requires visible browser)
- Cross-browser testing needed (Chrome only)
- Headless automation required

**For CI/CD and headless, use:** `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-test-playwright/SKILL.md")`

### Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "I'll check the console manually" | NO. Use `read_console_messages` |
| "I can infer what the API returns" | NO. Use `read_network_requests` |
| "I'll just look at DevTools" | AUTOMATE IT. Chrome MCP captures the same data |
| "Chrome MCP works for CI" | NO. It requires visible browser. Use Playwright. |
| "Recording a GIF is overkill" | GIFs prove interactions worked. Record them. |
</EXTREMELY-IMPORTANT>

## MCP Tools Overview

| Tool | Purpose |
|------|---------|
| `navigate` | Navigate to URL |
| `read_page` | Get accessibility tree (page state) |
| `find` | Natural language element search |
| `computer` | Mouse/keyboard (click, type, scroll, screenshot) |
| `form_input` | Set form values |
| `javascript_tool` | Execute JS in page context |
| `read_console_messages` | Read browser console |
| `read_network_requests` | Read HTTP requests |
| `get_page_text` | Extract page text content |
| `gif_creator` | Record interactions as GIF |
| `tabs_context_mcp` | Get tab context |
| `tabs_create_mcp` | Create new tab |

## Console Debugging

<EXTREMELY-IMPORTANT>
### The Iron Law of Console Debugging

**DO NOT manually check console. Use `read_console_messages`.**

If JavaScript errors exist, you MUST capture them automatically.
</EXTREMELY-IMPORTANT>

### Reading Console Messages

```
mcp__claude-in-chrome__read_console_messages(
    tabId=TAB_ID,
    pattern="error|warning"  # Filter by regex pattern
)
```

### Pattern Filtering (Required)

**Always provide a pattern** to avoid verbose output:

| Pattern | Captures |
|---------|----------|
| `"error"` | All error messages |
| `"error\|warning"` | Errors and warnings |
| `"MyApp"` | Application-specific logs |
| `"API"` | API-related messages |
| `"fetch\|xhr"` | Network-related logs |

### Example: Debug JavaScript Error

```
# 1. Navigate to page
mcp__claude-in-chrome__navigate(tabId=TAB_ID, url="https://app.example.com")

# 2. Trigger the action
mcp__claude-in-chrome__computer(action="left_click", tabId=TAB_ID, coordinate=[500, 300])

# 3. Check for errors
mcp__claude-in-chrome__read_console_messages(
    tabId=TAB_ID,
    pattern="error|Error|ERROR",
    onlyErrors=true
)
```

### Clearing Console Between Tests

```
mcp__claude-in-chrome__read_console_messages(
    tabId=TAB_ID,
    pattern=".*",
    clear=true  # Clear after reading
)
```

## Network Request Inspection

<EXTREMELY-IMPORTANT>
### The Iron Law of API Debugging

**DO NOT guess API responses. Use `read_network_requests`.**

If debugging API calls, you MUST capture actual requests and responses.
</EXTREMELY-IMPORTANT>

### Reading Network Requests

```
mcp__claude-in-chrome__read_network_requests(
    tabId=TAB_ID,
    urlPattern="/api/"  # Filter by URL pattern
)
```

### URL Pattern Filtering

| Pattern | Captures |
|---------|----------|
| `"/api/"` | All API calls |
| `"graphql"` | GraphQL requests |
| `"auth"` | Authentication requests |
| `"example.com"` | Requests to specific domain |

### Example: Debug API Call

```
# 1. Navigate and trigger action
mcp__claude-in-chrome__navigate(tabId=TAB_ID, url="https://app.example.com")
mcp__claude-in-chrome__computer(action="left_click", tabId=TAB_ID, ref="submit-button")

# 2. Wait for network activity
mcp__claude-in-chrome__computer(action="wait", tabId=TAB_ID, duration=2)

# 3. Inspect API calls
mcp__claude-in-chrome__read_network_requests(
    tabId=TAB_ID,
    urlPattern="/api/submit"
)
```

### Clearing Network Log Between Tests

```
mcp__claude-in-chrome__read_network_requests(
    tabId=TAB_ID,
    clear=true
)
```

## JavaScript Execution

<EXTREMELY-IMPORTANT>
### The Iron Law of JS Execution

**DO NOT assume page state. Execute JS to verify.**

If you need to check page variables, DOM state, or run custom logic, use `javascript_tool`.
</EXTREMELY-IMPORTANT>

### Executing JavaScript

```
mcp__claude-in-chrome__javascript_tool(
    action="javascript_exec",
    tabId=TAB_ID,
    text="document.querySelector('#my-element').innerText"
)
```

### Common Use Cases

**Get element text:**
```
text="document.querySelector('.status').innerText"
```

**Check if element exists:**
```
text="document.querySelector('#login-button') !== null"
```

**Get form values:**
```
text="document.querySelector('input[name=email]').value"
```

**Check localStorage:**
```
text="localStorage.getItem('authToken')"
```

**Get page data:**
```
text="window.__APP_STATE__"
```

**Trigger event:**
```
text="document.querySelector('#btn').dispatchEvent(new Event('click'))"
```

### Important Notes

- Do NOT use `return` statements - just write the expression
- Result of the last expression is returned automatically
- Code runs in page context with access to DOM, window, etc.

## Navigation & Interaction

### Get Tab Context First

```
# Always start by getting available tabs
mcp__claude-in-chrome__tabs_context_mcp(createIfEmpty=true)
```

### Navigation

```
mcp__claude-in-chrome__navigate(tabId=TAB_ID, url="https://example.com")
```

### Reading Page Structure

```
# Get accessibility tree
mcp__claude-in-chrome__read_page(tabId=TAB_ID)

# Get interactive elements only
mcp__claude-in-chrome__read_page(tabId=TAB_ID, filter="interactive")

# Get specific element by ref
mcp__claude-in-chrome__read_page(tabId=TAB_ID, ref_id="ref_123")
```

### Finding Elements (Natural Language)

```
mcp__claude-in-chrome__find(
    tabId=TAB_ID,
    query="login button"
)
```

### Clicking Elements

```
# By coordinates
mcp__claude-in-chrome__computer(
    action="left_click",
    tabId=TAB_ID,
    coordinate=[500, 300]
)

# By element ref (from read_page or find)
mcp__claude-in-chrome__computer(
    action="left_click",
    tabId=TAB_ID,
    ref="ref_1"
)
```

### Typing Text

```
mcp__claude-in-chrome__computer(
    action="type",
    tabId=TAB_ID,
    text="hello@example.com"
)
```

### Form Input

```
mcp__claude-in-chrome__form_input(
    tabId=TAB_ID,
    ref="ref_1",
    value="user@example.com"
)
```

### Screenshots

```
mcp__claude-in-chrome__computer(
    action="screenshot",
    tabId=TAB_ID
)
```

### Waiting

```
mcp__claude-in-chrome__computer(
    action="wait",
    tabId=TAB_ID,
    duration=2  # seconds
)
```

## GIF Recording

<EXTREMELY-IMPORTANT>
### When to Record GIFs

**Record GIFs for multi-step interactions that need visual verification.**

GIFs prove interactions worked. Screenshots only show end state.
</EXTREMELY-IMPORTANT>

### Recording Workflow

```
# 1. Start recording
mcp__claude-in-chrome__gif_creator(action="start_recording", tabId=TAB_ID)

# 2. Take initial screenshot (first frame)
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)

# 3. Perform interactions
mcp__claude-in-chrome__computer(action="left_click", tabId=TAB_ID, coordinate=[500, 300])
mcp__claude-in-chrome__computer(action="wait", tabId=TAB_ID, duration=1)
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)

# ... more interactions with screenshots between ...

# 4. Take final screenshot (last frame)
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)

# 5. Stop recording
mcp__claude-in-chrome__gif_creator(action="stop_recording", tabId=TAB_ID)

# 6. Export GIF
mcp__claude-in-chrome__gif_creator(
    action="export",
    tabId=TAB_ID,
    download=true,
    filename="login_flow.gif"
)
```

### GIF Best Practices

1. **Name meaningfully** - Use descriptive filenames like `checkout_flow.gif`
2. **Capture extra frames** - Take screenshots before and after actions
3. **Include wait time** - Allow animations to complete between screenshots

## Complete E2E Examples

### Login Flow with Console/Network Debugging

```
# 1. Get tab context
mcp__claude-in-chrome__tabs_context_mcp(createIfEmpty=true)

# 2. Create new tab
mcp__claude-in-chrome__tabs_create_mcp()
# Returns tabId

# 3. Navigate to login
mcp__claude-in-chrome__navigate(tabId=TAB_ID, url="https://app.example.com/login")
mcp__claude-in-chrome__computer(action="wait", tabId=TAB_ID, duration=2)

# 4. Clear console and network for clean test
mcp__claude-in-chrome__read_console_messages(tabId=TAB_ID, pattern=".*", clear=true)
mcp__claude-in-chrome__read_network_requests(tabId=TAB_ID, clear=true)

# 5. Get page structure
mcp__claude-in-chrome__read_page(tabId=TAB_ID, filter="interactive")

# 6. Fill login form
mcp__claude-in-chrome__find(tabId=TAB_ID, query="email input")
mcp__claude-in-chrome__form_input(tabId=TAB_ID, ref="ref_1", value="user@example.com")

mcp__claude-in-chrome__find(tabId=TAB_ID, query="password input")
mcp__claude-in-chrome__form_input(tabId=TAB_ID, ref="ref_2", value="password123")

# 7. Submit
mcp__claude-in-chrome__find(tabId=TAB_ID, query="sign in button")
mcp__claude-in-chrome__computer(action="left_click", tabId=TAB_ID, ref="ref_3")

# 8. Wait for response
mcp__claude-in-chrome__computer(action="wait", tabId=TAB_ID, duration=3)

# 9. Check for errors in console
mcp__claude-in-chrome__read_console_messages(
    tabId=TAB_ID,
    pattern="error|Error|failed",
    onlyErrors=true
)

# 10. Verify API call succeeded
mcp__claude-in-chrome__read_network_requests(
    tabId=TAB_ID,
    urlPattern="/api/login"
)

# 11. Verify logged in state via JS
mcp__claude-in-chrome__javascript_tool(
    action="javascript_exec",
    tabId=TAB_ID,
    text="localStorage.getItem('authToken') !== null"
)

# 12. Screenshot for evidence
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)
```

### API Debugging Workflow

```
# 1. Setup
mcp__claude-in-chrome__tabs_context_mcp(createIfEmpty=true)
mcp__claude-in-chrome__navigate(tabId=TAB_ID, url="https://api-dashboard.example.com")

# 2. Clear previous network data
mcp__claude-in-chrome__read_network_requests(tabId=TAB_ID, clear=true)

# 3. Trigger the problematic action
mcp__claude-in-chrome__find(tabId=TAB_ID, query="refresh data button")
mcp__claude-in-chrome__computer(action="left_click", tabId=TAB_ID, ref="ref_1")

# 4. Wait for network activity
mcp__claude-in-chrome__computer(action="wait", tabId=TAB_ID, duration=3)

# 5. Inspect all API calls
mcp__claude-in-chrome__read_network_requests(
    tabId=TAB_ID,
    urlPattern="/api/"
)

# 6. Check console for related errors
mcp__claude-in-chrome__read_console_messages(
    tabId=TAB_ID,
    pattern="API|fetch|error"
)

# 7. Verify page state after API call
mcp__claude-in-chrome__javascript_tool(
    action="javascript_exec",
    tabId=TAB_ID,
    text="document.querySelector('.data-table tbody tr').length"
)
```

### Form Submission with Validation

```
# 1. Navigate to form
mcp__claude-in-chrome__navigate(tabId=TAB_ID, url="https://app.example.com/contact")

# 2. Start GIF recording
mcp__claude-in-chrome__gif_creator(action="start_recording", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)

# 3. Fill form with invalid data to test validation
mcp__claude-in-chrome__form_input(tabId=TAB_ID, ref="email-input", value="invalid-email")
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)

# 4. Submit
mcp__claude-in-chrome__computer(action="left_click", tabId=TAB_ID, ref="submit-btn")
mcp__claude-in-chrome__computer(action="wait", tabId=TAB_ID, duration=1)
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)

# 5. Check for validation errors in console
mcp__claude-in-chrome__read_console_messages(tabId=TAB_ID, pattern="validation|error")

# 6. Verify error message appears
mcp__claude-in-chrome__javascript_tool(
    action="javascript_exec",
    tabId=TAB_ID,
    text="document.querySelector('.error-message').innerText"
)

# 7. Stop and export GIF
mcp__claude-in-chrome__gif_creator(action="stop_recording", tabId=TAB_ID)
mcp__claude-in-chrome__gif_creator(
    action="export",
    tabId=TAB_ID,
    download=true,
    filename="form_validation.gif"
)
```

## Integration

This skill is referenced by `dev-test` for Chrome MCP browser automation.

**For headless/CI testing, use:** `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-test-playwright/SKILL.md")`

For TDD protocol, see: `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-tdd/SKILL.md")`
