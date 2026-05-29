---
name: live-debug
description: Debug the live solution at home.st44.no using Chrome browser tools
user-invocable: true
allowed-tools: mcp__claude-in-chrome__*
tags:
  - debugging
  - production
  - browser
  - chrome
version: 1.0.0
---

# Live Debug Skill

Debug the production application at **home.st44.no** using Chrome browser automation tools (Claude in Chrome MCP).

## When to Use This Skill

Use this skill when:

- **Bug Investigation**: See exact visual state of reported issues on production
- **Understanding PO Wishes**: Observe current app behavior to understand requirements
- **Deployment Verification**: Confirm features work after shipping to production
- **Visual Comparison**: Compare design specs or mockups with actual implementation
- **Requirements Clarification**: Get visual reference for ambiguous requirements
- **User Flow Analysis**: Walk through user journeys on the live site

## Usage

```
/live-debug [description of what to investigate]
```

**Examples:**

```
/live-debug Check if the login page has the white border bug
/live-debug Investigate how task completion flow works
/live-debug Verify the new dashboard deployed correctly
/live-debug Understand the current household management UI
```

## Production URL

**Live Site**: https://home.st44.no

## Capabilities

- Navigate to production site and specific pages
- Take screenshots of current state
- Read page accessibility tree for element structure
- Execute JavaScript to inspect component state
- Find elements by description
- Monitor network requests (API calls)
- View console messages (errors, logs)
- Record GIFs demonstrating bugs or user flows
- Interact with page (clicks, form input, scrolling)

## Available Tools

| Tool                    | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| `tabs_context_mcp`      | Get/create browser tabs                       |
| `tabs_create_mcp`       | Create new tab in MCP group                   |
| `navigate`              | Go to URL or back/forward                     |
| `computer`              | Screenshots, clicks, typing, scrolling        |
| `read_page`             | Get accessibility tree                        |
| `find`                  | Find elements by natural language description |
| `form_input`            | Set form field values                         |
| `javascript_tool`       | Execute JS in page context                    |
| `read_console_messages` | View console output                           |
| `read_network_requests` | Monitor API calls                             |
| `gif_creator`           | Record/export GIFs                            |
| `get_page_text`         | Extract page text content                     |

## Standard Workflow

### 1. Initialize Browser Session

```
tabs_context_mcp(createIfEmpty: true)
```

This returns available tabs and creates an MCP tab group if none exists.

### 2. Navigate to Production

```
navigate(url: "https://home.st44.no", tabId: <id>)
```

The site will redirect to login if not authenticated.

### 3. Capture Current State

```
computer(action: "screenshot", tabId: <id>)
```

Always screenshot before and after actions for reference.

### 4. Investigate Structure

```
read_page(tabId: <id>)                    # Full accessibility tree
read_page(tabId: <id>, filter: "interactive")  # Only interactive elements
find(query: "login button", tabId: <id>)  # Natural language search
```

### 5. Inspect State with JavaScript

```
javascript_tool(
  text: "window.localStorage.getItem('auth_token')",
  tabId: <id>
)

javascript_tool(
  text: "document.querySelector('[data-testid=\"task-list\"]')?.innerHTML",
  tabId: <id>
)
```

### 6. Monitor Network/Console

```
read_network_requests(tabId: <id>, urlPattern: "/api/")
read_console_messages(tabId: <id>, pattern: "error")
```

## Recording Bug Reproductions

For complex bugs, record a GIF showing reproduction steps:

### Start Recording

```
gif_creator(action: "start_recording", tabId: <id>)
computer(action: "screenshot", tabId: <id>)  # Capture initial frame
```

### Perform Reproduction Steps

```
computer(action: "left_click", coordinate: [x, y], tabId: <id>)
computer(action: "type", text: "test@example.com", tabId: <id>)
# ... more steps
```

### Stop and Export

```
computer(action: "screenshot", tabId: <id>)  # Capture final frame
gif_creator(action: "stop_recording", tabId: <id>)
gif_creator(action: "export", download: true, filename: "bug-reproduction.gif", tabId: <id>)
```

## Common Investigation Patterns

### Investigate Visual Bug

```
1. tabs_context_mcp(createIfEmpty: true)
2. navigate(url: "https://home.st44.no/...", tabId: <id>)
3. computer(action: "screenshot", tabId: <id>)
4. read_page(tabId: <id>)
5. javascript_tool(text: "getComputedStyle(document.querySelector('...'))", tabId: <id>)
```

### Check API Responses

```
1. tabs_context_mcp(createIfEmpty: true)
2. navigate(url: "https://home.st44.no", tabId: <id>)
3. # Trigger action that makes API call
4. read_network_requests(tabId: <id>, urlPattern: "/api/tasks")
```

### Verify Feature Deployment

```
1. tabs_context_mcp(createIfEmpty: true)
2. navigate(url: "https://home.st44.no", tabId: <id>)
3. computer(action: "screenshot", tabId: <id>)  # Before
4. # Navigate to feature area
5. computer(action: "screenshot", tabId: <id>)  # After
6. find(query: "new feature element", tabId: <id>)
```

### Walk Through User Flow

```
1. tabs_context_mcp(createIfEmpty: true)
2. gif_creator(action: "start_recording", tabId: <id>)
3. navigate(url: "https://home.st44.no", tabId: <id>)
4. computer(action: "screenshot", tabId: <id>)
5. # Complete user flow steps
6. gif_creator(action: "stop_recording", tabId: <id>)
7. gif_creator(action: "export", download: true, tabId: <id>)
```

## Authentication Notes

- The live site requires authentication
- After navigating, you may be redirected to `/login`
- Browser may have saved credentials from previous sessions
- For authenticated actions, ensure login is completed first

## Tips

- **Always screenshot** before and after actions for context
- **Use `find`** for natural language element queries
- **Use `read_page` with filter** to reduce output size
- **Check console** for JavaScript errors: `read_console_messages(pattern: "error")`
- **Monitor API calls** to understand data flow
- **Record GIFs** for bug reports - they're more valuable than screenshots

## Related Resources

- **Report Bug Skill**: `/report-bug` - Create GitHub issues with live screenshots
- **E2E Skill**: `/e2e` - Compare e2e tests with live behavior
- **Frontend Agent**: `.claude/agents/agent-frontend.md` - UI debugging patterns

## Troubleshooting

### Tab Not Found

If you get "tab not found" errors, call `tabs_context_mcp` again to get fresh tab IDs.

### Page Not Loading

Check if the site is up by navigating directly. If login required, ensure authentication.

### GIF Not Recording

Make sure to take screenshots after starting and before stopping recording to capture frames.

### JavaScript Errors

If `javascript_tool` returns errors, check that the selector exists using `read_page` or `find` first.
