---
name: claude-chrome-debugging
description: Diagnoses and fixes Claude in Chrome extension issues including zombie MCP processes, action failures, and extension conflicts
---

# Claude Chrome Debugging

Troubleshoot Claude in Chrome browser automation issues.

## Symptoms & Causes

| Symptom                                                                                                                     | Likely Cause                                                     |
| --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `navigate`/`form_input` work but `click`/`screenshot`/`javascript_exec` fail with "Cannot access a chrome-extension:// URL" | CDP debugger conflict (other extensions) or zombie MCP processes |
| Extension completely unresponsive                                                                                           | MCP server not running or Chrome extension disabled              |
| Actions work intermittently                                                                                                 | Multiple MCP processes competing                                 |

## Diagnostic Steps

### 1. Check for Zombie MCP Processes

```bash
ps aux | grep -i "claude-in-chrome-mcp" | grep -v grep
```

**Expected:** 1-2 processes (one per active Claude Code session)

**Problem:** Multiple processes, especially with old timestamps (days ago)

### 2. Check Active Claude Code Sessions

Count your actual terminal sessions running Claude Code. Compare to MCP process count.

### 3. Verify Chrome Extension Status

In Chrome: `chrome://extensions/` → Find "Claude in Chrome" → Ensure enabled

### 4. Check for Conflicting Extensions

Chrome only allows **one extension** to attach the CDP debugger per tab ([root cause analysis](https://github.com/anthropics/claude-code/issues/16239#issuecomment-2593972182)). Extensions that conflict:

| Extension Type | Examples                                                                                                       |
| -------------- | -------------------------------------------------------------------------------------------------------------- |
| DevTools       | React DevTools, Vue DevTools, Redux DevTools                                                                   |
| Automation     | Selenium IDE, Puppeteer Recorder                                                                               |
| Page tools     | Screenshot tools, page inspectors                                                                              |
| Security       | Some password managers ([ref](https://github.com/anthropics/claude-code/issues/16239#issuecomment-2591621552)) |

**Any extension using `chrome.debugger` API will conflict.**

## Fixes

### Fix CDP Conflicts (Most Common)

**Disable conflicting extensions** ([confirmed by multiple users](https://github.com/anthropics/claude-code/issues/16239)):

1. Go to `chrome://extensions/`
2. Disable DevTools extensions (React, Vue, Redux)
3. Disable any automation/screenshot extensions
4. Refresh the tab and retry

**macOS: Enable JavaScript from Apple Events** ([mixed results](https://github.com/anthropics/claude-code/issues/16239#issuecomment-2591660693)):

1. Chrome → View → Developer → Allow JavaScript from Apple Events
2. Refresh/re-navigate tabs (old tabs don't pick up the change)

**Close other Chromium browsers** ([ref](https://github.com/anthropics/claude-code/issues/16239#issuecomment-2591766590)):

Other Chromium-based browsers (Arc, Brave, Dia) can interfere. Close them when using Claude in Chrome.

### Quick Fix: /chrome Command

Run `/chrome` in your Claude Code session. Options include:

- **Reconnect extension** - Re-establish connection without killing processes
- **Enabled by default** - Check/change whether Chrome starts with every session

If "Enabled by default" is Yes and you run multiple CC sessions, disable it. Use `--chrome` flag only when needed.

### Kill Zombie MCP Processes

```bash
# View processes first
ps aux | grep "claude-in-chrome-mcp" | grep -v grep

# Kill all MCP processes (will auto-restart for active sessions)
pkill -f "claude-in-chrome-mcp"
```

After killing, wait a few seconds. Active Claude Code sessions will reconnect automatically.

### Full Reset (if above doesn't work)

1. Kill all MCP processes: `pkill -f "claude-in-chrome-mcp"`
2. Quit Chrome completely
3. Restart Chrome
4. Restart Claude Code session

### Extension Reinstall (last resort)

1. `chrome://extensions/` → Remove "Claude in Chrome"
2. Reinstall from Chrome Web Store
3. Restart Claude Code

## Prevention

### Multi-Session Conflicts

Each Claude Code session spawns its own `claude-in-chrome-mcp` process. Multiple sessions = multiple processes competing for the single Chrome extension connection.

**Best practice:** Only enable Chrome in sessions that need browser automation.

**Session flags:**

```bash
# Start with Chrome (for browser QA sessions)
claude --chrome

# Resume existing session with Chrome
claude --resume <session-id> --chrome
```

**Check your default:** Run `/chrome` → if "Enabled by default" is Yes, set to No. Then use `--chrome` flag only when needed.

### Zombie Processes

Zombie processes occur when Claude Code sessions exit uncleanly (force quit, terminal crash, system sleep). Diagnose and fix when symptoms appear using steps above.

## Notes

- The "chrome-extension:// URL of different extension" error is misleading - you're on localhost, but stale MCP processes confuse the extension about which server to use
- `form_input` uses different code path than `click`/`screenshot` which is why some actions work while others fail

## References

- [GitHub Issue #16239](https://github.com/anthropics/claude-code/issues/16239) - Comprehensive discussion of CDP conflicts and workarounds
