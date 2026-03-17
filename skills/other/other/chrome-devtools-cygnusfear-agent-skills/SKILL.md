---
name: chrome-devtools
description: Control Chrome browser programmatically using chrome-devtools-mcp. Use when user asks to automate Chrome, debug web pages, take screenshots, evaluate JavaScript, inspect network requests, or interact with browser DevTools. Also use when asked about browser automation, web scraping, or testing websites.
allowed-tools: Bash, Read, Write
---

# Chrome DevTools MCP Skill

Control Chrome browser programmatically via chrome-devtools-mcp.

**⚡ Performance Tip:** Always use the patterns in "Quick Start" section below. They include cleanup and run everything in ONE command to avoid browser lock issues.

**Speed Comparison:**
- ❌ **OLD WAY:** Multiple attempts, manual cleanup, 5-10 commands → ~60-90 seconds
- ✅ **NEW WAY:** One optimized command → ~5-10 seconds

**📚 See also:** MCP CLI patterns and best practices (see create-mcp-skill skill for reference)

## Setup

```bash
# macOS
brew tap f/mcptools
brew install mcp

# Windows/Linux
go install github.com/f/mcptools/cmd/mcptools@latest
```

## Quick Start (FASTEST)

### Check Console Errors on localhost

**Single command (copy-paste ready):**
```bash
pkill -9 -f "chrome-devtools-mcp" 2>/dev/null; sleep 1; echo -e 'navigate_page {"url":"http://localhost:3000"}\nlist_console_messages {"pageIdx":0}\nexit' | timeout 30 mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

### Full Debug: Console + Network + Page Content

```bash
pkill -9 -f "chrome-devtools-mcp" 2>/dev/null; sleep 1; echo -e 'navigate_page {"url":"http://localhost:3000"}\nlist_console_messages {"pageIdx":0}\nlist_network_requests {"pageIdx":0}\ntake_snapshot {"verbose":true}\nexit' | timeout 30 mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

### Screenshot a Page

```bash
pkill -9 -f "chrome-devtools-mcp" 2>/dev/null; sleep 1; echo -e 'navigate_page {"url":"https://example.com"}\ntake_screenshot {"fullPage":true,"format":"png"}\nexit' | timeout 30 mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

### Execute JavaScript on Page

```bash
pkill -9 -f "chrome-devtools-mcp" 2>/dev/null; sleep 1; echo -e 'navigate_page {"url":"http://localhost:3000"}\nevaluate_script {"function":"() => document.querySelectorAll(\"div\").length"}\nexit' | timeout 30 mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

**⚡ Pattern:** `cleanup; sleep; echo commands | timeout shell`

This avoids:
- ❌ Browser profile locks (cleanup first)
- ❌ Multiple shell sessions (one pipeline)
- ❌ Hanging commands (timeout wrapper)

## Usage

**List available tools:**
```bash
mcp tools bunx -y chrome-devtools-mcp@latest
```

**Call tools (individual commands):**
```bash
# Navigate to a page (includes page list in response)
mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"url":"https://example.com"}'

# Take screenshot
mcp call take_screenshot bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"fullPage":true,"format":"png"}'

# Take snapshot (page content as text)
mcp call take_snapshot bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"verbose":false}'

# List console messages
mcp call list_console_messages bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"pageIdx":0}'

# Execute JavaScript
mcp call evaluate_script bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"function":"() => document.title"}'
```

**Interactive shell mode (RECOMMENDED - maintains single browser instance):**
```bash
mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated

# Then run commands:
navigate_page {"url":"https://example.com"}
take_snapshot {"verbose":false}
list_console_messages {"pageIdx":0}
new_page {"url":"https://httpbin.org"}
exit
```

**With Chrome launch options:**
```bash
# Headless mode
mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --headless --isolated --params '{"url":"https://example.com"}'

# Custom viewport
mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --viewport "1920x1080" --isolated --params '{"url":"https://example.com"}'

# Connect to existing Chrome instance (no --isolated needed)
mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --browserUrl http://127.0.0.1:9222 --params '{"url":"https://example.com"}'
```

## Common Workflows

**Check localhost console logs:**
```bash
# Shell mode (RECOMMENDED):
mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
# Then: navigate_page {"url":"http://localhost:3000"}
# Then: list_console_messages {"pageIdx":0}

# Or as individual commands:
mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"url":"http://localhost:3000"}'
mcp call list_console_messages bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"pageIdx":0}'
```

**Automate form filling:**
```bash
mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
# Then in shell:
# navigate_page {"url":"https://example.com/login"}
# take_snapshot {"verbose":false}   # Get UIDs for elements
# fill {"uid":"#username","value":"user"}
# fill {"uid":"#password","value":"pass"}
# click {"uid":"#submit"}
```

**Network debugging:**
```bash
# Shell mode (RECOMMENDED):
mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
# Then: navigate_page {"url":"https://example.com"}
# Then: list_network_requests {"pageIdx":0}

# Or as individual commands:
mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"url":"https://example.com"}'
mcp call list_network_requests bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"pageIdx":0}'
```

## Key Tools

- **navigate_page** - Go to URL (returns page list)
- **new_page** - Open new tab (returns page list)
- **select_page** - Switch to different page by index
- **close_page** - Close page by index
- **click** - Click element
- **fill** - Fill input/textarea
- **evaluate_script** - Run JavaScript
- **take_screenshot** - Capture page as image
- **take_snapshot** - Get page content as text with UIDs
- **list_console_messages** - View console logs (use `{"pageIdx":0}`)
- **list_network_requests** - View network activity (use `{"pageIdx":0}`)
- **wait_for** - Wait for text/condition

## Important Notes

- Always use `bunx` (not `npx`) for chrome-devtools-mcp
- **Correct syntax:** `mcp call TOOL_NAME bunx -y chrome-devtools-mcp@latest -- --isolated --params '{...}'`
  - Server command comes AFTER tool name, BEFORE --params
  - Parameters are passed directly (no "arguments" wrapper)
  - Use `-- --isolated` to create temporary profile (prevents browser lock conflicts)
- Server exposes full browser content - avoid sensitive data

## Working with Multiple Commands

**Problem:** Each `mcp call` starts a new server & browser instance, causing conflicts.

**Solutions:**

1. **Shell mode (RECOMMENDED):** Maintains single browser instance
   ```bash
   mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
   ```

2. **Individual calls:** Use `-- --isolated` for one-off commands
   ```bash
   mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --isolated --params '{"url":"..."}'
   ```

3. **Connect to running Chrome:** Start Chrome with debugging enabled
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   mcp call navigate_page bunx -y chrome-devtools-mcp@latest -- --browserUrl http://127.0.0.1:9222 --params '{"url":"..."}'
   ```

## Known Issues (mcp CLI v0.7.1)

⚠️ **Bug:** Tools with empty parameter schemas fail with "Invalid arguments" error.

**Workaround:** Provide at least one optional parameter:
- ✅ `list_console_messages {"pageIdx":0}` - Works
- ✅ `list_network_requests {"pageIdx":0}` - Works
- ✅ `take_snapshot {"verbose":false}` - Works
- ❌ `list_pages` - Broken, use `navigate_page` or `new_page` instead (they return page list)

## Troubleshooting

**Problem: "The browser is already running" error**

This happens when a previous Chrome instance is still holding the profile lock.

**Quick fix (ALWAYS DO THIS FIRST):**
```bash
pkill -9 -f "chrome-devtools-mcp" 2>/dev/null; sleep 1
```

**Then run your command:**
```bash
echo -e 'navigate_page {"url":"YOUR_URL"}\nlist_console_messages {"pageIdx":0}\nexit' | mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

**Problem: Multiple failed attempts**

Don't create multiple shell sessions - keep ONE session open and run multiple commands:

❌ **BAD (slow - 2 separate sessions):**
```bash
echo 'navigate_page {"url":"..."}' | mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
echo 'list_console_messages {"pageIdx":0}' | mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

✅ **GOOD (fast - 1 session, multiple commands):**
```bash
echo -e 'navigate_page {"url":"..."}\nlist_console_messages {"pageIdx":0}\nexit' | mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```

**Problem: Commands hanging/timing out**

Use `timeout` to prevent hanging:
```bash
timeout 30 mcp shell bunx -y chrome-devtools-mcp@latest -- --isolated
```
