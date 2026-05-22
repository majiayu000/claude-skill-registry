---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
---

# Web Application Testing

Test local web applications using native Python Playwright scripts.

## Helper Scripts

- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run with `--help` first** to see usage.

## Decision Tree

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly for selectors
    │         → Write Playwright script
    │
    └─ No (dynamic webapp) → Is server running?
        ├─ No → Use with_server.py helper
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors
            4. Execute actions
```

## Using with_server.py

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers:**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

## Playwright Script Template

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL!

    # Reconnaissance
    page.screenshot(path='/tmp/inspect.png', full_page=True)

    # Actions
    page.locator('button:has-text("Submit")').click()

    browser.close()
```

## Common Pitfall

**Don't** inspect DOM before `networkidle` on dynamic apps.
**Do** wait for `page.wait_for_load_state('networkidle')` first.

## Best Practices

- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS, IDs
- Add appropriate waits: `wait_for_selector()`, `wait_for_timeout()`
