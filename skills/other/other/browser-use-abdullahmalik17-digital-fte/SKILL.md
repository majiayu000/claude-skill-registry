---
name: browser-use
description: Browser automation using Playwright MCP. Navigate websites, fill forms, click elements, take screenshots, and extract data. Use when tasks require web browsing, form submission, web scraping, UI testing, or any browser interaction.
---

# Browser Automation

Automate browser interactions via Playwright MCP server.

## Server Lifecycle

### Start Server
```bash
# Using helper script (recommended)
bash scripts/start-server.sh

# Or manually
npx @playwright/mcp@latest --port 8808 --shared-browser-context &
```

### Stop Server
```bash
# Using helper script (closes browser first)
bash scripts/stop-server.sh

# Or manually
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_close -p '{}'
pkill -f "@playwright/mcp"
```

### When to Stop
- **End of task**: Stop when browser work is complete
- **Long sessions**: Keep running if doing multiple browser tasks
- **Errors**: Stop and restart if browser becomes unresponsive

**Important:** The `--shared-browser-context` flag is required to maintain browser state across multiple mcp-client.py calls. Without it, each call gets a fresh browser context.

## Quick Reference

### Navigation

```bash
# Go to URL
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_navigate \
  -p '{"url": "https://example.com"}'

# Go back
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_navigate_back -p '{}'
```

### Get Page State

```bash
# Accessibility snapshot (returns element refs for clicking/typing)
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_snapshot -p '{}'

# Screenshot
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_take_screenshot \
  -p '{"type": "png", "fullPage": true}'
```

### Interact with Elements

Use `ref` from snapshot output to target elements:

```bash
# Click element
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_click \
  -p '{"element": "Submit button", "ref": "e42"}'

# Type text
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_type \
  -p '{"element": "Search input", "ref": "e15", "text": "hello world", "submit": true}'

# Fill form (multiple fields)
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_fill_form \
  -p '{"fields": [{"ref": "e10", "value": "john@example.com"}, {"ref": "e12", "value": "password123"}]}'

# Select dropdown
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_select_option \
  -p '{"element": "Country dropdown", "ref": "e20", "values": ["US"]}'
```

### Wait for Conditions

```bash
# Wait for text to appear
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_wait_for \
  -p '{"text": "Success"}'

# Wait for time (ms)
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_wait_for \
  -p '{"time": 2000}'
```

### Execute JavaScript

```bash
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_evaluate \
  -p '{"function": "return document.title"}'
```

### Multi-Step Playwright Code

For complex workflows, use `browser_run_code` to run multiple actions in one call:

```bash
python3 scripts/mcp-client.py call -u http://localhost:8808 -t browser_run_code \
  -p '{"code": "async (page) => { await page.goto(\"https://example.com\"); await page.click(\"text=Learn more\"); return await page.title(); }"}'
```

**Tip:** Use `browser_run_code` for complex multi-step operations that should be atomic (all-or-nothing).

## Workflow: Form Submission

1. Navigate to page
2. Get snapshot to find element refs
3. Fill form fields using refs
4. Click submit
5. Wait for confirmation
6. Screenshot result

## Workflow: Data Extraction

1. Navigate to page
2. Get snapshot (contains text content)
3. Use browser_evaluate for complex extraction
4. Process results

## Tool Reference

See [references/playwright-tools.md](references/playwright-tools.md) for complete tool documentation.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Element not found | Run browser_snapshot first to get current refs |
| Click fails | Try browser_hover first, then click |
| Form not submitting | Use `"submit": true` with browser_type |
| Page not loading | Increase wait time or use browser_wait_for |
