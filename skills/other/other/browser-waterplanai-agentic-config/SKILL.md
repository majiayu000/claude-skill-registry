---
name: browser
description: "Opens browser at URL for E2E testing via playwright-cli. Provides CLI commands for navigation, screenshots, and interaction. Triggers on keywords: browser, open browser, playwright browser, e2e browser"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
---

# Browser Command

Open browser for E2E testing using playwright-cli.

**Target URL:** $ARGUMENTS

If no URL provided, default to: `http://localhost:${DEFAULT_PORT:-5173}/`

## Pre-Flight Checks

1. **Verify playwright-cli Installed**
   - Run: `playwright-cli --help`
   - If not available: STOP with error "playwright-cli not installed. Run: npm install -g @playwright/cli@latest && playwright-cli install-browser"

## Execution

1. **Navigate to URL**
   ```bash
   playwright-cli open "${URL:-http://localhost:${DEFAULT_PORT:-5173}/}"
   ```

2. **Verify Page Load**
   ```bash
   playwright-cli snapshot
   ```
   Report page title and URL from snapshot output.

3. **Report Status**
   - Confirm browser is open and ready
   - Display current page title
   - Display current URL

## Available CLI Commands

After opening browser, these commands are available via Bash:
- `playwright-cli goto <url>` - Navigate to URL
- `playwright-cli snapshot` - Capture accessibility snapshot
- `playwright-cli click "<selector>"` - Click element
- `playwright-cli fill "<selector>" "<text>"` - Fill input field
- `playwright-cli type "<text>"` - Type text
- `playwright-cli screenshot` - Take PNG screenshot
- `playwright-cli close` - Close browser session
- `playwright-cli video-start` / `video-stop` - Record video

## Notes
- Video recording is explicit: use `playwright-cli video-start` before the flow and `video-stop` after
- Configure output via `playwright-cli.json` in project root
- Use `--headed` flag for visible browser window: `playwright-cli --headed open <url>`
- Port can be configured via DEFAULT_PORT environment variable
- Sessions persist across commands: use `playwright-cli -s=<name>` for named sessions
