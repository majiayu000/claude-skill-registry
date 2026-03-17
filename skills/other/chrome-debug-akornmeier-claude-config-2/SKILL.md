---
name: chrome-debug
description: How to use Chrome DevTools MCP for browser debugging. Use when you need to inspect pages, take screenshots, debug UI issues, or verify visual changes.
---

# Chrome DevTools Debugging

This skill explains how to use the Chrome DevTools MCP for browser debugging and UI verification.

## Setup

Before using Chrome DevTools MCP, you must launch Chrome in headless mode with remote debugging enabled:

```bash
npm run chrome &
```

This runs Chrome with the required flags for Docker/containerized environments:

- `--remote-debugging-port=9222` - Enables MCP connection
- `--no-sandbox` - Required for Docker
- `--headless` - Runs without display
- `--disable-gpu` - Avoids GPU issues in containers

Wait a few seconds for Chrome to start before using MCP tools.

## Screenshots

**IMPORTANT:** Always save screenshots to the `.screenshots` directory using the `filePath` parameter:

```
mcp__chrome-devtools__take_screenshot with filePath: ".screenshots/descriptive-name.png"
```

Use descriptive filenames like:

- `.screenshots/homepage-initial.png`
- `.screenshots/login-form-error.png`
- `.screenshots/after-click-submit.png`

This allows debugging and visual comparison later.

## Workflow Example

1. **Start Chrome:**

   ```bash
   npm run chrome &
   ```

   Wait 2-3 seconds for startup.

2. **Navigate to the dev server:**

   ```
   mcp__chrome-devtools__navigate_page url="http://localhost:5173"
   ```

3. **Take a snapshot to see page structure:**

   ```
   mcp__chrome-devtools__take_snapshot
   ```

   The snapshot shows element UIDs you can use for interactions.

4. **Take a screenshot for visual verification:**

   ```
   mcp__chrome-devtools__take_screenshot filePath=".screenshots/page-state.png"
   ```

5. **Interact with elements using UIDs from snapshot:**
   ```
   mcp__chrome-devtools__click uid="1_4"
   mcp__chrome-devtools__fill uid="1_5" value="test@example.com"
   ```

## Tips

- **Prefer snapshots over screenshots** - Snapshots are faster and provide element UIDs for interaction
- **Always save screenshots locally** - Use `.screenshots/` directory with descriptive names
- **Check if Chrome is running** - If tools fail to connect, run `npm run chrome &` again
- **Wait after navigation** - Use `wait_for` to ensure page content loads before interacting
