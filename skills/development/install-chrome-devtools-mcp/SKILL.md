---
name: install-chrome-devtools-mcp
description: Install Chrome DevTools MCP server for debugging and network inspection in Claude Code
argument-hint: "[--scope <scope>] [--headless] [--auto-connect]"
---

# Install Chrome DevTools MCP Server

Install the Chrome DevTools MCP server to enable debugging and network inspection capabilities.

## What This Does

The Chrome DevTools MCP server provides:
- **Console inspection** - View errors, warnings, and log messages
- **Network analysis** - Inspect HTTP requests and responses
- **JavaScript evaluation** - Run code in page context
- **Performance tracing** - Analyze page performance
- **Screenshots** - Capture page state

## Installation Command

Run this command to install:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

## Scope Options

- `--scope local` (default): Available only in current project
- `--scope project`: Shared with team via `.mcp.json`
- `--scope user`: Available across all your projects

```bash
# Install for user (all projects)
claude mcp add chrome-devtools --scope user -- npx -y chrome-devtools-mcp@latest

# Install for project (team shared)
claude mcp add chrome-devtools --scope project -- npx -y chrome-devtools-mcp@latest
```

## Common Configurations

### Headless Mode

For headless operation (no visible browser):

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --headless
```

### Auto-Connect to Running Chrome

Connect to an already-running Chrome instance (Chrome 145+):

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --autoConnect
```

### Connect to Specific Browser URL

For sandboxed environments or remote debugging:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --browserUrl http://127.0.0.1:9222
```

### Custom Viewport

Set initial window size:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --viewport 1920x1080
```

### Isolated Sessions (No Persistence)

Use temporary profile that cleans up automatically:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --isolated
```

## Verify Installation

After installation:
1. Restart Claude Code
2. Run `/mcp` to see the chrome-devtools server
3. Test with: "Navigate to google.com and list console messages"

## Available Tools After Installation

### Debugging Tools
- `evaluate_script` - Run JavaScript in page context
- `get_console_message` - Get specific console message
- `list_console_messages` - List all console messages
- `take_screenshot` - Capture page screenshots
- `take_snapshot` - Capture accessibility snapshot

### Network Tools
- `get_network_request` - Get specific network request details
- `list_network_requests` - List all network requests

### Navigation & Input
- `navigate_page` - Navigate to URL
- `click` - Click elements
- `fill` - Fill input fields
- `fill_form` - Fill multiple form fields
- `wait_for` - Wait for conditions

### Performance Tools
- `performance_start_trace` - Start performance trace
- `performance_stop_trace` - Stop and analyze trace
- `performance_analyze_insight` - Get performance insights

### Page Management
- `new_page` - Open new tab
- `close_page` - Close current page
- `list_pages` - List all open pages
- `select_page` - Switch to specific page

## Coexistence with Playwright

Chrome DevTools MCP works alongside Playwright MCP:

| Use Case | Recommended Tool |
|----------|-----------------|
| QA Testing / Automation | Playwright |
| Debugging / Network inspection | Chrome DevTools |
| Form filling / Navigation | Either |
| Console inspection | Chrome DevTools |
| Accessibility snapshots | Either |
| Performance analysis | Chrome DevTools |

Both can be installed simultaneously - they use different tool namespaces:
- Playwright: `mcp__playwright__*`
- Chrome DevTools: `mcp__chrome-devtools__*`

## Browser Connection Modes

### Mode 1: Managed (Default) - No Browser Setup

The MCP server launches and controls its own Chrome instance. No browser-side setup needed:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

**Best for**: Simple debugging, isolated sessions, no existing login state needed.

### Mode 2: Auto-Connect (Chrome 145+)

Connect to your regular Chrome browser to debug with your logged-in sessions.

**Browser setup**: Launch Chrome with remote debugging enabled:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222

# Windows
chrome.exe --remote-debugging-port=9222
```

**Install command**:
```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --autoConnect
```

**Best for**: Debugging pages that require your authentication/cookies.

### Mode 3: Browser URL

For sandboxed environments or when auto-connect doesn't work.

**Browser setup**: Same as auto-connect - launch Chrome with `--remote-debugging-port=9222`

**Install command**:
```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --browserUrl http://127.0.0.1:9222
```

**Best for**: Sandboxed environments, remote debugging, CI/CD pipelines.

## Creating a Chrome Shortcut with Remote Debugging

### macOS

Create an Automator app or alias:
```bash
alias chrome-debug='/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222'
```

### Linux

Create a desktop shortcut with the `--remote-debugging-port=9222` flag.

### Windows

1. Copy Chrome shortcut
2. Right-click > Properties
3. Add ` --remote-debugging-port=9222` to Target field

## Troubleshooting

### Browser Won't Launch (Managed Mode)

On macOS with sandboxing restrictions:
```bash
# Use auto-connect mode instead
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --autoConnect
```

### Connection Refused (Auto-Connect/Browser URL)

1. Verify Chrome is running with remote debugging:
   - Visit `http://127.0.0.1:9222/json` in another browser
   - Should show JSON with open tabs
2. Check no other process is using port 9222
3. Ensure Chrome was started with `--remote-debugging-port=9222`

### Port Already in Use

```bash
# Use a different port
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9333

# Then connect with:
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --browserUrl http://127.0.0.1:9333
```

## Execution Instructions

When the user runs this command:

1. **Determine scope** from arguments or default to `local`

2. **Check for options**:
   - `--headless` -> add `--headless` flag
   - `--auto-connect` -> add `--autoConnect` flag

3. **Run installation**:
   ```bash
   claude mcp add chrome-devtools [--scope <scope>] -- npx -y chrome-devtools-mcp@latest [options]
   ```

4. **Verify success** by checking output

5. **Inform user** to restart Claude Code to use the new MCP server
