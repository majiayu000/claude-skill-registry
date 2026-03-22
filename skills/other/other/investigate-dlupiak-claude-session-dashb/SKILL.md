---
name: investigate
description: Investigate a URL or page using Playwright browser
user-invocable: true
argument-hint: "<url>"
---

# Browser Investigation

You are investigating **$ARGUMENTS.url** using Playwright.

## Steps

### 1. Resolve URL
- If the URL starts with `/`, prepend `http://localhost:3000`
- If the URL starts with `http`, use as-is
- Check if the dev server is running on :3000; if not, suggest `npm run dev`

### 2. Navigate
- Use `mcp__playwright__browser_navigate` to open the URL
- Take a screenshot with `mcp__playwright__browser_take_screenshot`

### 3. Inspect
- Use `mcp__playwright__browser_snapshot` to get the accessibility tree
- Check `mcp__playwright__browser_console_messages` for errors
- Check `mcp__playwright__browser_network_requests` for failed requests

### 4. Report
- Summarize what you see: layout, content, errors
- If there are console errors or network failures, list them
- Suggest fixes if issues are found

## Notes
- Use Playwright MCP tools, not Bash-based browser commands
- Take screenshots at each significant step
- Close the browser when done: `mcp__playwright__browser_close`
