---
name: using-chrome-devtools
description: Automates headless Chrome via MCP for web scraping, screenshots, testing, and browser interactions. Handles multi-instance server selection to avoid lock conflicts between parallel agents. Triggers when browsing a website, taking a screenshot, scraping a page, testing a web app, automating browser interactions, or when chrome-devtools MCP tools are needed.
compatibility: Requires chrome-devtools MCP servers registered at user scope (chrome-devtools, chrome-devtools-2, chrome-devtools-3, chrome-devtools-visible)
allowed-tools: Bash, ToolSearch
metadata:
  author: Saturate
  version: "1.0"
---

You are helping the user interact with websites using Chrome via the chrome-devtools MCP servers.

There are 4 isolated server instances available. You must pick a free one before doing any browser work.

## Progress Checklist

Copy this checklist to track your progress through the workflow:

```
Chrome DevTools Progress:
- [ ] Step 1: Selected an available server instance
- [ ] Step 2: Loaded required MCP tools via ToolSearch
- [ ] Step 3: Performed the requested browser task
- [ ] Step 4: Cleaned up (closed pages)
```

## Step 1: Select an Available Server

There are 4 MCP server instances — 3 headless and 1 visible (opens a real browser window):

| Instance | Tool prefix | Mode |
|----------|-------------|------|
| 1 | `mcp__chrome-devtools__*` | Headless |
| 2 | `mcp__chrome-devtools-2__*` | Headless |
| 3 | `mcp__chrome-devtools-3__*` | Headless |
| visible | `mcp__chrome-devtools-visible__*` | Visible |

**When to use visible:** Use `chrome-devtools-visible` when the user asks to see the browser, needs to debug visually, or wants to watch automation in real-time. Default to headless instances for everything else.

**To find a free instance**, check each server's `list_pages` tool (e.g. `mcp__chrome-devtools__list_pages`). Load them via ToolSearch:

```
ToolSearch: "+chrome-devtools list_pages"
```

Then call `list_pages` on each instance. A server is **free** if it only has the default `about:blank` page (or returns no pages). A server is **busy** if it has pages with real URLs.

**Check headless servers in order** (1 → 2 → 3) and use the first free one. Only use visible if the user explicitly asks for it or all headless instances are busy.

If all 4 are busy, tell the user:
> "All chrome-devtools instances are currently in use. Wait for another task to finish or add more instances."

**CRITICAL:** Never run parallel Task agents on the same server instance. Each agent must claim its own instance.

## Step 2: Load MCP Tools

Once you've picked a server (e.g. instance 2), load the tools you need via ToolSearch using the correct prefix:

```
ToolSearch: "+chrome-devtools-2 navigate"
ToolSearch: "+chrome-devtools-2 screenshot"
```

Common tools available on each instance (shown for instance 1, substitute prefix for others):
- `mcp__chrome-devtools__navigate_page` — Navigate to a URL
- `mcp__chrome-devtools__take_screenshot` — Capture the current page
- `mcp__chrome-devtools__take_snapshot` — Get the DOM/accessibility snapshot (useful for scraping text content)
- `mcp__chrome-devtools__click` — Click an element
- `mcp__chrome-devtools__fill` — Fill a form field
- `mcp__chrome-devtools__fill_form` — Fill multiple form fields
- `mcp__chrome-devtools__evaluate_script` — Run JavaScript on the page
- `mcp__chrome-devtools__press_key` — Press a keyboard key
- `mcp__chrome-devtools__wait_for` — Wait for an element or condition
- `mcp__chrome-devtools__new_page` — Open a new page/tab
- `mcp__chrome-devtools__close_page` — Close a page/tab
- `mcp__chrome-devtools__list_pages` — List open pages
- `mcp__chrome-devtools__list_network_requests` — Monitor network traffic
- `mcp__chrome-devtools__list_console_messages` — Read console output

## Step 3: Perform the Browser Task

### Navigation

Always start by navigating to the target URL:
```
navigate_page(url: "https://example.com")
```

After navigation, take a screenshot or snapshot to verify the page loaded correctly.

### Taking Screenshots

Use `take_screenshot` to capture what the page looks like. This is useful for:
- Verifying a page loaded correctly
- Debugging layout issues
- Showing the user what you see

### Scraping Content

Use `take_snapshot` to get a structured text representation of the page. This gives you the accessibility tree which is more useful than raw HTML for extracting content.

For dynamic content, you may need to:
1. `wait_for` the content to appear
2. Then `take_snapshot`

### Form Interaction

1. Use `take_snapshot` to identify form fields
2. Use `fill` or `fill_form` to enter data
3. Use `click` to submit

### Running JavaScript

Use `evaluate_script` for operations that don't have dedicated tools:
```
evaluate_script(expression: "document.title")
```

## Step 4: Clean Up

**Always close pages when done.** There is no auto-timeout on these servers.

```
close_page(pageId: "<id>")
```

If you opened multiple pages, close all of them. Use `list_pages` to verify nothing is left behind.

## Troubleshooting

### Server won't respond / tools not loading
The MCP server may not be running. Try:
1. Check if the server is listed: `claude mcp list --scope user`
2. Restart Claude Code session to reinitialize MCP connections

### Stale pages from a previous session
If `list_pages` shows pages that aren't yours (leftover from a crashed session), close them before starting your work:
```
close_page(pageId: "<stale-page-id>")
```

### Navigation timeout
Some pages take a long time to load. Use `wait_for` with a selector to wait for specific content instead of relying on page load completion.

### Can't find an element
Use `take_snapshot` to see the accessibility tree structure, then target elements by their accessible name or role.

## Tips

- Prefer `take_snapshot` over `take_screenshot` when you need to extract text content — it's faster and gives structured data
- Use `take_screenshot` when you need to see visual layout or show the user what the page looks like
- For SPAs, wait for content to render after navigation before taking snapshots
- If a page requires authentication, let the user know — headless browsers start with no session/cookies
- Each server instance has its own isolated browser profile, so cookies and state are not shared between instances
- The `chrome-devtools-visible` instance opens a real browser window — useful for demos or debugging but slower to start
