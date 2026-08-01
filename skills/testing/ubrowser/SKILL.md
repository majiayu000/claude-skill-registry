---
name: ubrowser
description: Browser automation optimized for speed and cost efficiency
---

# μBrowser

Control a headless browser with 98% token reduction compared to Playwright MCP and Dev Browser. Uses batch execution, minimal responses, and efficient HTML formatting.

## Setup

Start the ubrowser server before using browser tools:

```bash
./skills/ubrowser/server.sh &
```

Wait for "μBrowser MCP server started" message. First run installs dependencies and downloads Playwright Chromium.

Use `--headless` flag for headless mode:
```bash
./skills/ubrowser/server.sh --headless &
```

## Key Optimization: Batch Execution

**Always prefer `browser_batch` for multi-step workflows.** This is the key to 98% cost savings.

Instead of:
```
browser_navigate → browser_type → browser_type → browser_click (4 calls, 4 snapshots)
```

Use:
```json
{
  "tool": "browser_batch",
  "steps": [
    {"tool": "navigate", "args": {"url": "/login"}},
    {"tool": "type", "args": {"selector": "#email", "text": "user@test.com"}},
    {"tool": "type", "args": {"selector": "#password", "text": "secret"}},
    {"tool": "click", "args": {"selector": "button[type=submit]"}}
  ],
  "snapshot": {"when": "final"}
}
```

**Result: 1 call, 1 snapshot = 80%+ token reduction**

## Available Tools

### browser_navigate
Navigate to a URL.
```json
{"url": "https://example.com"}
```

### browser_click
Click element by ref or selector.
```json
{"ref": "e1"}
{"selector": "button.submit"}
```

### browser_type
Type text into input.
```json
{"ref": "e2", "text": "hello@example.com", "clear": true, "pressEnter": true}
```

### browser_select
Select dropdown option.
```json
{"selector": "#country", "label": "United States"}
```

### browser_scroll
Scroll page or element.
```json
{"direction": "down", "amount": 500}
{"toBottom": true}
```

### browser_snapshot
Get interactive elements with refs (e1, e2, e3...).
```json
{"scope": "#main", "format": "full"}
```

### browser_batch (KEY)
Execute multiple actions, snapshot only at end.
```json
{
  "steps": [
    {"tool": "navigate", "args": {"url": "/search"}},
    {"tool": "type", "args": {"selector": "input[name=q]", "text": "query"}},
    {"tool": "click", "args": {"selector": "button[type=submit]"}}
  ],
  "snapshot": {"when": "final", "scope": ".results"}
}
```

### browser_pages
Manage multiple browser pages.
```json
{"action": "create", "name": "login"}
{"action": "switch", "name": "dashboard"}
{"action": "list"}
{"action": "close", "name": "login"}
```

### browser_inspect
Inspect specific element.
```json
{"selector": ".form", "includeText": true, "depth": 3}
```

## Element References

Snapshots return elements with short refs:
```
<input id="e1" type="email" placeholder="Email">
<input id="e2" type="password">
<button id="e3">Sign In</button>
```

Use refs in subsequent commands: `{"ref": "e1", "text": "user@test.com"}`

## Best Practices

1. **Always batch** - Use `browser_batch` for multi-step flows
2. **Request snapshots sparingly** - Default is no snapshot, add `snapshot: {include: true}` only when needed
3. **Scope snapshots** - Use `scope` parameter to limit to relevant DOM region
4. **Use refs** - Short IDs save tokens vs full selectors
5. **Use diff format** - After first snapshot, use `format: "diff"` for changes only

## Cost Comparison (Opus 4.5)

| Approach | Per Task | Monthly (3000) |
|----------|----------|----------------|
| Playwright MCP | $3.28 | $9,827 |
| μBrowser | $0.01 | $45 |
| **Savings** | **$3.26** | **$9,782** |
