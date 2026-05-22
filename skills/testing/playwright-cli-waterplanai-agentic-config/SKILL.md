---
name: playwright-cli
description: "Browser automation via playwright-cli. Token-efficient alternative to Playwright MCP - uses CLI commands through Bash instead of MCP tool schemas. Supports navigation, interaction, screenshots, video recording, and session management. Triggers on keywords: browser, e2e, playwright, screenshot, navigate, click, type, test browser, visual test"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
---

# Playwright CLI Browser Automation

Browser automation using `playwright-cli` - a token-efficient CLI alternative to Playwright MCP.

## Prerequisites

- Node.js >= 18
- Global install: `npm install -g @playwright/cli@latest`
- Browser: `playwright-cli install-browser`

## Quick Reference

### Navigation

```bash
playwright-cli open https://example.com          # Open URL (creates default session)
playwright-cli -s=mytest open https://example.com # Named session
playwright-cli goto https://example.com/page      # Navigate within session
playwright-cli go-back                             # Browser back
playwright-cli go-forward                          # Browser forward
playwright-cli reload                              # Reload page
playwright-cli close                               # Close session
```

### Page Inspection

```bash
playwright-cli snapshot                  # Accessibility snapshot (like browser_snapshot)
playwright-cli screenshot                # Take PNG screenshot
playwright-cli screenshot --output ./out.png  # Save to specific path
playwright-cli pdf --output ./page.pdf   # Save page as PDF
```

### Interaction

```bash
playwright-cli click "Button Text"       # Click by text
playwright-cli click "#submit-btn"       # Click by selector
playwright-cli fill "#email" "user@example.com"  # Fill input field
playwright-cli type "Hello world"        # Type text into focused element
playwright-cli select "#dropdown" "option1"      # Select dropdown option
playwright-cli hover "#menu-item"        # Hover over element
playwright-cli check "#checkbox"         # Check a checkbox
playwright-cli uncheck "#checkbox"       # Uncheck a checkbox
playwright-cli dblclick "#element"       # Double-click
playwright-cli upload "#file-input" ./file.txt   # Upload file
```

### Keyboard & Mouse

```bash
playwright-cli press Enter               # Press key
playwright-cli press Control+a           # Key combination
playwright-cli keydown Shift             # Hold key
playwright-cli keyup Shift               # Release key
```

### Tabs

```bash
playwright-cli tab-list                  # List open tabs
playwright-cli tab-new https://example.com  # Open new tab
playwright-cli tab-select 1              # Switch to tab by index
playwright-cli tab-close                 # Close current tab
```

### Session Management

```bash
playwright-cli -s=session1 open https://example.com  # Create named session
playwright-cli -s=session1 snapshot      # Use existing session
playwright-cli list                      # List active sessions
playwright-cli close-all                 # Close all sessions
PLAYWRIGHT_CLI_SESSION=session1 playwright-cli snapshot  # Env var session
```

### Video Recording

```bash
playwright-cli video-start               # Start recording
playwright-cli video-stop                # Stop recording (saves file)
```

### Developer Tools

```bash
playwright-cli console                   # Get console messages
playwright-cli network                   # Get network requests
playwright-cli run-code "document.title" # Execute JavaScript in page
```

### Tracing

```bash
playwright-cli tracing-start             # Start trace capture
playwright-cli tracing-stop --output trace.zip  # Stop and save trace
```

### Network Mocking

```bash
playwright-cli route "**\/api\/*" --status 200 --body '{"ok":true}'
playwright-cli route-list                # List active routes
playwright-cli unroute "**\/api\/*"      # Remove route
```

### Storage State

```bash
playwright-cli state-save --output state.json    # Save cookies + storage
playwright-cli state-load --input state.json     # Restore state
```

### Window

```bash
playwright-cli resize 1920 1080          # Set viewport size
```

### Dialog Handling

```bash
playwright-cli dialog-accept             # Accept alert/confirm/prompt
playwright-cli dialog-dismiss            # Dismiss dialog
```

## Configuration

Optional `playwright-cli.json` in project root:

```json
{
  "browserName": "chromium",
  "isolated": true,
  "launchOptions": {
    "headless": false
  },
  "contextOptions": {
    "viewport": { "width": 1920, "height": 1080 }
  },
  "saveVideo": {
    "width": 1920,
    "height": 1080
  },
  "outputDir": "./outputs/e2e"
}
```

## Headed Mode

```bash
playwright-cli --headed open https://example.com  # Visible browser window
```

## Key Differences from Playwright MCP

| Aspect | MCP | CLI |
|--------|-----|-----|
| Token usage | Heavy (page snapshots + tool schemas) | Light (shell commands) |
| Integration | MCP config per AI tool | Single global npm install |
| State | MCP server process | Persistent named sessions |
| Video | Automatic via `--save-video` | Explicit `video-start`/`video-stop` |
| Screenshots | `browser_take_screenshot` tool | `playwright-cli screenshot` |
| Snapshots | `browser_snapshot` tool | `playwright-cli snapshot` |

## Reference Documentation

- [Session Management](resources/session-management.md)
- [Video Recording](resources/video-recording.md)
- [Test Generation](resources/test-generation.md)
- [Request Mocking](resources/request-mocking.md)
- [Storage State](resources/storage-state.md)
- [Tracing](resources/tracing.md)
- [Running Code](resources/running-code.md)
