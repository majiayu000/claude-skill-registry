---
name: dev-test-electron
description: This skill should be used when the user asks to "test Electron app", "automate Electron desktop app", "debug Electron renderer", "test VS Code extension", "E2E test Electron", or needs Chrome DevTools Protocol automation for Electron applications. Use for renderer process debugging, main process control, native menu automation, and file dialog testing.
user-invocable: false
disable-model-invocation: true
---

**Announce:** "I'm using dev-test-electron for Electron app automation via Chrome DevTools Protocol."

<EXTREMELY-IMPORTANT>
## REAL Test Requirements for Electron Apps

**A REAL Electron test must replicate what the user does. FAKE tests test something else.**

Before writing ANY test, verify from SPEC.md/PLAN.md:

| REAL Test Criteria | Your Test Must |
|-------------------|----------------|
| **User workflow** | Replicate exact steps (click → type → see result) |
| **Protocol** | Use SAME protocol as production (WebSocket, IPC, etc.) |
| **UI interaction** | Interact with ACTUAL UI elements user sees |
| **Verification** | Check what USER sees, not internal state |

### The Electron-Specific Fake Test Trap

**Electron apps often use WebSocket/IPC internally. Testing HTTP is a FAKE test.**

| FAKE Electron Test | Why It's Fake | REAL Test |
|--------------------|---------------|-----------|
| HTTP endpoint test | App uses WebSocket | Test WebSocket connection |
| Direct function call | User clicks button | CDP `Input.dispatchMouseEvent` or `Runtime.evaluate` click |
| Check internal state | User sees panel/status | CDP screenshot or DOM query |
| Mock IPC layer | Production uses real IPC | Test actual IPC messages |
| Skip main process | Main process has logic | Test BOTH renderer AND main |

### Before You Write a Test, Ask:

1. What protocol does this feature use? (WebSocket? IPC? HTTP?)
2. What does the user actually click/type?
3. What does the user actually SEE?
4. Am I testing the SAME code path as production?

**If any answer is "I don't know" → Go back to SPEC.md. Don't guess.**

### Rationalization Prevention (Electron-Specific)

| Thought | Reality |
|---------|---------|
| "HTTP is easier to test" | But app uses WebSocket. Test WebSocket. |
| "I can call the function directly" | User clicks a button. Use CDP Input events. |
| "CDP is complex, let me mock" | Mocking hides bugs. Use real CDP. |
| "Main process is hard to test" | Main process crashes break app. Test it. |
| "Panel state is internal" | User SEES the panel. Test what user sees. |
| "IPC is just plumbing" | IPC bugs cause silent failures. Test it. |
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## Gate Reminder

Before taking screenshots or running E2E tests, you MUST complete all 6 gates from dev-tdd:

```
GATE 1: BUILD
GATE 2: LAUNCH (with file-based logging)
GATE 3: WAIT
GATE 4: CHECK PROCESS
GATE 5: READ LOGS ← MANDATORY, CANNOT SKIP
GATE 6: VERIFY LOGS
THEN: E2E tests/screenshots
```

**You loaded dev-tdd earlier. Follow the gates now.**
</EXTREMELY-IMPORTANT>

## Contents

- [Tool Availability Gate](#tool-availability-gate)
- [When to Use Electron CDP](#when-to-use-electron-cdp)
- [Connecting to Electron](#connecting-to-electron)
- [CDP Domains](#cdp-domains)
- [Renderer Process Automation](#renderer-process-automation)
- [Main Process Control](#main-process-control)
- [Verification](#verification)
- [Complete E2E Examples](#complete-e2e-examples)

# Electron E2E Testing via Chrome DevTools Protocol

<EXTREMELY-IMPORTANT>
## Tool Availability Gate

**Verify CDP tooling is available before proceeding.**

Check for these tools:
```bash
# Check for curl (CDP communication)
which curl || echo "MISSING: curl"

# Check for jq (JSON parsing)
which jq || echo "MISSING: jq"

# Check for websocat or wscat (WebSocket CLI)
which websocat || which wscat || echo "MISSING: WebSocket CLI"
```

**If missing tools:**
```
STOP: Cannot proceed with Electron CDP automation.

Missing tools needed for CDP:
- curl (for HTTP requests)
- jq (for JSON parsing)
- websocat or wscat (for WebSocket communication)

Install with:
  # macOS: Install via nix-darwin (see ~/nix/). Do NOT use brew.
  # Linux: sudo apt install curl jq websocat

Reply when installed and I'll continue testing.
```

**This gate is non-negotiable. Missing tools = full stop.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## When to Use Electron CDP

**USE Electron CDP when you need:**
- Test Electron desktop applications (VS Code, Slack, etc.)
- Debug Electron renderer process (console, DOM, network)
- Automate Electron main process (native menus, dialogs, IPC)
- Multi-window Electron testing
- Electron-specific features (webContents, BrowserWindow)
- File system operations from Electron app

**DO NOT use Electron CDP when:**
- Testing web applications only (use Chrome MCP or Playwright)
- Testing non-Electron desktop apps (use Hammerspoon for macOS, dev-test-linux for Linux)
- Need headless CI/CD for web apps (use Playwright MCP)

**For web apps or native desktop apps, discover and read the relevant skill:**
Related skills:
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-test-chrome/SKILL.md` and follow its instructions.
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-test-playwright/SKILL.md` and follow its instructions.
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-test-hammerspoon/SKILL.md` and follow its instructions.
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-test-linux/SKILL.md` and follow its instructions.
- Chrome MCP skill - web debugging
- Playwright skill - headless CI/CD
- Hammerspoon skill - macOS native
- Linux skill - Linux native

### Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "Chrome MCP works for Electron" | NO. Electron has main process + renderer. Need Electron-specific CDP. |
| "Playwright can test Electron apps" | NO. Playwright is for web browsers, not Electron main process. |
| "I'll just test the renderer" | Main process matters. File dialogs, native menus need testing too. |
| "CDP is too complex" | It's the ONLY way to properly test Electron apps. Learn it. |
| "I can skip the main process" | NO. Main process crashes break the app. Test both. |

### Capability Comparison

| Capability | Electron CDP | Chrome MCP | Playwright MCP | Hammerspoon |
|------------|--------------|------------|----------------|-------------|
| Electron renderer | ✅ | ❌ | ❌ | ❌ |
| Electron main process | ✅ | ❌ | ❌ | ❌ |
| Native menus/dialogs | ✅ | ❌ | ❌ | ✅ (macOS only) |
| Multi-window Electron | ✅ | ❌ | ❌ | ✅ (macOS only) |
| Console/network debugging | ✅ | ✅ (web only) | ❌ | ❌ |
| Headless mode | ✅ | ❌ | ✅ (web only) | ❌ |
| WebSocket IPC | ✅ | ❌ | ❌ | ❌ |
</EXTREMELY-IMPORTANT>

## Connecting to Electron

<EXTREMELY-IMPORTANT>
### The Iron Law of Connection

**EVERY Electron E2E test MUST establish CDP connection BEFORE any automation.**

You CANNOT automate without:
1. Launching Electron with CDP enabled
2. Discovering the CDP WebSocket URL
3. Connecting to the WebSocket
4. Verifying the connection works

| Action | Why It Fails Without Connection |
|--------|----------------------------------|
| Send CDP command | No connection = command never sent |
| Read console logs | Can't receive events without WebSocket |
| Navigate to page | CDP Page.navigate requires connection |
| Take screenshot | CDP Page.captureScreenshot requires connection |

**"App is running" ≠ "CDP is connected". Verify connection first.**
</EXTREMELY-IMPORTANT>

### Enable Remote Debugging

Launch Electron with remote debugging port:

```bash
# Option 1: Fixed port
/path/to/electron-app --remote-debugging-port=9222

# Option 2: Random port (app outputs port number)
/path/to/electron-app --remote-debugging-port=0

# Option 3: With logging
/path/to/electron-app --remote-debugging-port=9222 --enable-logging --log-file=/tmp/electron.log 2>&1 &
```

**CRITICAL:** For GATE 2 (LAUNCH), always use `--log-file` flag for file-based logging.

### Discover CDP WebSocket URL

```bash
# Get list of inspectable targets
curl -s http://localhost:9222/json/list | jq '.'

# Extract WebSocket URL for main target
WS_URL=$(curl -s http://localhost:9222/json/list | jq -r '.[0].webSocketDebuggerUrl')
echo "WebSocket URL: $WS_URL"
```

Example response:
```json
[
  {
    "description": "",
    "devtoolsFrontendUrl": "/devtools/inspector.html?ws=localhost:9222/devtools/page/...",
    "id": "page-id",
    "title": "My Electron App",
    "type": "page",
    "url": "file:///app/index.html",
    "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/..."
  }
]
```

### Connect via WebSocket

```bash
# Interactive WebSocket session
websocat "$WS_URL"

# Send CDP commands (one per line, JSON format)
{"id":1,"method":"Runtime.enable"}
{"id":2,"method":"Page.enable"}
{"id":3,"method":"Runtime.evaluate","params":{"expression":"document.title"}}
```

**Helper script:** See `scripts/connect-electron-cdp.sh` for automated connection.

## CDP Domains

### Essential Domains for Electron

| Domain | Purpose | Example |
|--------|---------|---------|
| **Runtime** | Execute JavaScript, console logs | `Runtime.evaluate`, `Runtime.consoleAPICalled` |
| **Page** | Navigation, screenshots, DOM events | `Page.navigate`, `Page.captureScreenshot` |
| **DOM** | Query and manipulate DOM | `DOM.getDocument`, `DOM.querySelector` |
| **Debugger** | Breakpoints, step debugging | `Debugger.setBreakpoint` |
| **Network** | Network requests/responses | `Network.enable`, `Network.responseReceived` |
| **Input** | Keyboard/mouse events | `Input.dispatchKeyEvent`, `Input.dispatchMouseEvent` |

**Enable domains before use:**
```json
{"id":1,"method":"Runtime.enable"}
{"id":2,"method":"Page.enable"}
{"id":3,"method":"DOM.enable"}
{"id":4,"method":"Network.enable"}
```

## Renderer Process Automation

### Execute JavaScript

```bash
# Evaluate JavaScript expression
echo '{"id":1,"method":"Runtime.evaluate","params":{"expression":"document.title"}}' | websocat "$WS_URL"

# Execute with return value
echo '{"id":2,"method":"Runtime.evaluate","params":{"expression":"2 + 2","returnByValue":true}}' | websocat "$WS_URL"

# Execute complex script
SCRIPT='document.querySelector("#username").value = "testuser"'
echo "{\"id\":3,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$SCRIPT\"}}" | websocat "$WS_URL"
```

### Navigate to URL

```bash
# Navigate to URL (file:// or http://)
echo '{"id":10,"method":"Page.navigate","params":{"url":"file:///app/index.html"}}' | websocat "$WS_URL"

# Wait for load event
echo '{"id":11,"method":"Page.enable"}' | websocat "$WS_URL"
# Listen for Page.loadEventFired event
```

### Read Console Messages

```bash
# Enable Runtime domain to receive console events
echo '{"id":20,"method":"Runtime.enable"}' | websocat "$WS_URL"

# Console events arrive as:
# {"method":"Runtime.consoleAPICalled","params":{"type":"log","args":[...]}}
```

**For complete console reading, see `references/cdp-api.md`**

### Take Screenshots

```bash
# Capture viewport screenshot (PNG base64)
echo '{"id":30,"method":"Page.captureScreenshot"}' | websocat "$WS_URL" > response.json

# Extract base64 and decode
jq -r '.result.data' response.json | base64 -d > screenshot.png
```

### Query DOM

```bash
# Get document root
echo '{"id":40,"method":"DOM.getDocument"}' | websocat "$WS_URL"

# Query selector
ROOT_ID=$(jq -r '.result.root.nodeId' response.json)
echo "{\"id\":41,\"method\":\"DOM.querySelector\",\"params\":{\"nodeId\":$ROOT_ID,\"selector\":\"#submit-btn\"}}" | websocat "$WS_URL"
```

## Main Process Control

<EXTREMELY-IMPORTANT>
### Electron Main Process vs Renderer Process

**Electron has TWO processes:**

| Process | What It Does | How to Test |
|---------|--------------|-------------|
| **Main** | Node.js runtime, native APIs, file system, menus, dialogs | CDP `Runtime.evaluate` in main context OR IPC |
| **Renderer** | Browser/Chromium runtime, web content, DOM | CDP commands (Page, DOM, Runtime) |

**Both processes MUST be tested. Renderer-only testing is incomplete.**
</EXTREMELY-IMPORTANT>

### Access Main Process via CDP

Some Electron apps expose main process debugging:

```bash
# Check for main process target
curl -s http://localhost:9222/json/list | jq '.[] | select(.type == "node")'
```

If main process is available:
```bash
# Get main process WebSocket URL
MAIN_WS=$(curl -s http://localhost:9222/json/list | jq -r '.[] | select(.type == "node") | .webSocketDebuggerUrl')

# Execute Node.js code in main process
echo '{"id":1,"method":"Runtime.evaluate","params":{"expression":"process.version"}}' | websocat "$MAIN_WS"
```

### Trigger Native Dialogs (via IPC)

```bash
# From renderer, send IPC to main process
SCRIPT='require("electron").ipcRenderer.send("open-file-dialog")'
echo "{\"id\":50,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$SCRIPT\"}}" | websocat "$WS_URL"
```

**For advanced main process patterns, see `references/electron-specific.md`**

## Verification

<EXTREMELY-IMPORTANT>
### The Iron Law of Verification

**EVERY CDP command must be VERIFIED. Sending the command is not enough.**

After sending a CDP command, you MUST:
1. Read the response
2. Check for errors (`error` field in response)
3. Verify the result matches expectations
4. Document the verification

| Command | Verification |
|---------|--------------|
| `Runtime.evaluate` | Check `result.value` or `result.exceptionDetails` |
| `Page.navigate` | Wait for `Page.loadEventFired` event |
| `Page.captureScreenshot` | Verify `result.data` exists and decode base64 |
| `DOM.querySelector` | Check `result.nodeId` exists (not 0) |

**"I sent the command" is not verification. Read the response and verify success.**
</EXTREMELY-IMPORTANT>

### Response Verification Pattern

```bash
# Send command and capture response
RESPONSE=$(echo '{"id":100,"method":"Runtime.evaluate","params":{"expression":"2 + 2"}}' | websocat --one-message "$WS_URL")

# Check for error
if echo "$RESPONSE" | jq -e '.error' > /dev/null; then
    echo "ERROR: CDP command failed"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

# Verify result
RESULT=$(echo "$RESPONSE" | jq -r '.result.result.value')
if [ "$RESULT" != "4" ]; then
    echo "ERROR: Expected 4, got $RESULT"
    exit 1
fi

echo "✓ VERIFIED: 2 + 2 = $RESULT"
```

### Event-Based Verification

```bash
# Enable Page domain
echo '{"id":1,"method":"Page.enable"}' | websocat "$WS_URL" &

# Navigate and wait for load event
echo '{"id":2,"method":"Page.navigate","params":{"url":"file:///app/index.html"}}' | websocat "$WS_URL"

# Wait for Page.loadEventFired event (listen to WebSocket)
# Event format: {"method":"Page.loadEventFired","params":{...}}
```

## Complete E2E Examples

### Basic Electron App Test (All 6 Gates)

```bash
#!/bin/bash
set -e

# ============ GATE 1: BUILD ============
echo "GATE 1: Building Electron app..."
cd /path/to/electron-app
npm run build
echo "✓ GATE 1 PASSED"

# ============ GATE 2: LAUNCH ============
echo "GATE 2: Launching with CDP and logging..."
npm start -- --remote-debugging-port=9222 --enable-logging --log-file=/tmp/electron.log 2>&1 &
APP_PID=$!
echo "✓ GATE 2 PASSED (PID: $APP_PID)"

# ============ GATE 3: WAIT ============
echo "GATE 3: Waiting for Electron initialization..."
sleep 3
echo "✓ GATE 3 PASSED"

# ============ GATE 4: CHECK PROCESS ============
echo "GATE 4: Checking Electron process..."
if ! ps -p $APP_PID > /dev/null; then
    echo "✗ GATE 4 FAILED: Electron process crashed"
    echo "Reading logs from GATE 5..."
    cat /tmp/electron.log
    exit 1
fi

# Verify CDP port is open
if ! curl -s http://localhost:9222/json/list > /dev/null; then
    echo "✗ GATE 4 FAILED: CDP port not accessible"
    cat /tmp/electron.log
    exit 1
fi
echo "✓ GATE 4 PASSED"

# ============ GATE 5: READ LOGS ============
echo "GATE 5: Reading full runtime logs..."
echo "=== ELECTRON RUNTIME LOGS ==="
cat /tmp/electron.log
echo "=== END LOGS ==="
echo "✓ GATE 5 PASSED (logs read)"

# ============ GATE 6: VERIFY LOGS ============
echo "GATE 6: Verifying no errors in logs..."
if grep -qE "(ERROR|FATAL|CRITICAL|Segmentation|core dumped|Uncaught Exception)" /tmp/electron.log; then
    echo "✗ GATE 6 FAILED: Errors found in logs"
    exit 1
fi
echo "✓ GATE 6 PASSED"

# ============ NOW: E2E TESTING ============
echo "All gates passed. Proceeding to E2E tests..."

# Get WebSocket URL
WS_URL=$(curl -s http://localhost:9222/json/list | jq -r '.[0].webSocketDebuggerUrl')
echo "CDP WebSocket: $WS_URL"

# Enable Runtime domain
echo '{"id":1,"method":"Runtime.enable"}' | websocat --one-message "$WS_URL"

# Execute test: Get document title
RESPONSE=$(echo '{"id":2,"method":"Runtime.evaluate","params":{"expression":"document.title","returnByValue":true}}' | websocat --one-message "$WS_URL")

# Verify response
if echo "$RESPONSE" | jq -e '.error' > /dev/null; then
    echo "✗ E2E FAILED: CDP command error"
    echo "$RESPONSE" | jq '.error'
    exit 1
fi

TITLE=$(echo "$RESPONSE" | jq -r '.result.result.value')
echo "✓ E2E VERIFIED: Document title = '$TITLE'"

# Take screenshot
SCREENSHOT_RESPONSE=$(echo '{"id":3,"method":"Page.captureScreenshot"}' | websocat --one-message "$WS_URL")
echo "$SCREENSHOT_RESPONSE" | jq -r '.result.data' | base64 -d > /tmp/electron_screenshot.png
echo "✓ Screenshot saved: /tmp/electron_screenshot.png"

# Cleanup
kill $APP_PID
echo "✓ E2E TEST PASSED"
```

**Tool description:** Execute all 6 gates, then run Electron E2E test with CDP

### Form Automation Example

```bash
#!/bin/bash
# Assumes gates 1-6 already passed and WS_URL is set

# Enable domains
echo '{"id":1,"method":"Runtime.enable"}' | websocat --one-message "$WS_URL"
echo '{"id":2,"method":"Page.enable"}' | websocat --one-message "$WS_URL"

# Fill form field
FILL_USERNAME='document.querySelector("#username").value = "testuser"'
RESPONSE=$(echo "{\"id\":10,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$FILL_USERNAME\"}}" | websocat --one-message "$WS_URL")

if echo "$RESPONSE" | jq -e '.error' > /dev/null; then
    echo "✗ FAILED: Could not fill username"
    exit 1
fi

FILL_PASSWORD='document.querySelector("#password").value = "testpass"'
echo "{\"id\":11,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$FILL_PASSWORD\"}}" | websocat --one-message "$WS_URL"

# Click submit button
CLICK_SUBMIT='document.querySelector("#submit-btn").click()'
echo "{\"id\":12,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$CLICK_SUBMIT\"}}" | websocat --one-message "$WS_URL"

# Wait for navigation
sleep 1

# Verify success message appears
CHECK_SUCCESS='document.querySelector(".success-message") !== null'
VERIFY_RESPONSE=$(echo "{\"id\":13,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$CHECK_SUCCESS\",\"returnByValue\":true}}" | websocat --one-message "$WS_URL")

SUCCESS=$(echo "$VERIFY_RESPONSE" | jq -r '.result.result.value')
if [ "$SUCCESS" != "true" ]; then
    echo "✗ VERIFICATION FAILED: Success message not found"
    exit 1
fi

echo "✓ VERIFIED: Form submission successful"

# Screenshot for evidence
echo '{"id":14,"method":"Page.captureScreenshot"}' | websocat --one-message "$WS_URL" | jq -r '.result.data' | base64 -d > /tmp/form_success.png
echo "✓ Screenshot: /tmp/form_success.png"
```

### Multi-Window Testing

```bash
# Get all inspectable targets
curl -s http://localhost:9222/json/list | jq '.[] | {title: .title, url: .url, wsUrl: .webSocketDebuggerUrl}'

# Connect to specific window by title
WINDOW_WS=$(curl -s http://localhost:9222/json/list | jq -r '.[] | select(.title == "Settings Window") | .webSocketDebuggerUrl')

# Automate the settings window
echo '{"id":1,"method":"Runtime.evaluate","params":{"expression":"document.querySelector(\"#theme\").value = \"dark\""}}' | websocat --one-message "$WINDOW_WS"
```

**For more advanced patterns, see `references/advanced-patterns.md`**

## Error Handling

### Common CDP Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Electron not started with `--remote-debugging-port` | Restart with flag |
| WebSocket timeout | App crashed or port blocked | Check GATE 4 (process) and GATE 5 (logs) |
| `"error":{"code":-32601}` | Method not found | Enable domain first (e.g., `Runtime.enable`) |
| `exceptionDetails` in result | JavaScript error in evaluated code | Check expression syntax |
| Empty response | WebSocket closed | Reconnect to WebSocket |

### Retry Pattern

```bash
# Retry CDP command up to 3 times
for i in {1..3}; do
    RESPONSE=$(echo "$CDP_COMMAND" | websocat --one-message "$WS_URL")

    if echo "$RESPONSE" | jq -e '.result' > /dev/null; then
        echo "✓ Command succeeded on attempt $i"
        break
    fi

    if [ $i -eq 3 ]; then
        echo "✗ Command failed after 3 attempts"
        echo "$RESPONSE"
        exit 1
    fi

    echo "Retry $i failed, waiting 1s..."
    sleep 1
done
```

## Limitations

<EXTREMELY-IMPORTANT>
### What Electron CDP Cannot Do

| Need | Why Electron CDP Fails | Use Instead |
|------|------------------------|-------------|
| Native macOS window management | CDP doesn't control OS | Hammerspoon (macOS) |
| Cross-platform native automation | CDP is Chromium-only | Platform-specific tools |
| Test non-Electron apps | CDP requires Electron/Chromium | Hammerspoon, dev-test-linux |
| Headless CI/CD for web apps | Electron is for desktop apps | Playwright MCP |

**For web apps, use Playwright or Chrome MCP. For native desktop, use platform tools.**
</EXTREMELY-IMPORTANT>

## Additional Resources

### Reference Files

For detailed CDP API documentation and Electron-specific features:
- **`references/cdp-api.md`** - Complete CDP domains reference (Runtime, Page, DOM, Network, Input, Debugger)
- **`references/electron-specific.md`** - Electron main process, IPC, native APIs, file dialogs
- **`references/advanced-patterns.md`** - Multi-window, devtools, event listeners, WebSocket streaming

### Example Files

Working examples in `examples/`:
- **`basic-test.sh`** - Complete E2E test with all 6 gates
- **`cdp-commands.json`** - Common CDP command reference

### Scripts

Utility scripts in `scripts/`:
- **`connect-electron-cdp.sh`** - Automated CDP connection discovery
- **`launch-electron-with-logging.sh`** - Launch template with proper logging
- **`verify-electron-process.sh`** - Health check for main + renderer

## VS Code Extension Testing (Common Case)

<EXTREMELY-IMPORTANT>
**VS Code extensions are a common Electron test case. Here's how to test them REAL.**

### What Makes VS Code Extension Tests REAL

| User Action | FAKE Test | REAL Test |
|-------------|-----------|-----------|
| Highlight text in editor | `editor.setSelection()` programmatically | CDP simulate actual text selection |
| Click Claude panel | Call panel function directly | CDP click on actual panel element |
| See status in panel | Check internal state variable | CDP query panel DOM for displayed text |
| Extension uses WebSocket | Test HTTP endpoint | Test WebSocket connection |

### VS Code Extension Protocol Discovery

Before testing, discover what protocol the extension uses:

```bash
# Search for WebSocket usage
rg "WebSocket|ws://" --type ts

# Search for HTTP usage
rg "fetch|axios|http" --type ts

# Search for IPC usage
rg "ipcRenderer|ipcMain" --type ts
```

**If extension uses WebSocket → Your test MUST use WebSocket, not HTTP.**

### Example: Testing Selection → Panel Status

**FAKE test (DON'T DO THIS):**
```javascript
// FAKE: Calls function directly, checks internal state
const selection = await vscode.window.activeTextEditor.selection;
await extensionApi.updateSelection(selection);  // Direct call!
expect(internalState.selectionCount).toBe(5);   // Internal state!
```

**REAL test (DO THIS):**
```bash
# REAL: Simulates user, checks what user sees

# 1. Use CDP to simulate text selection in editor
SCRIPT='
  const editor = document.querySelector(".monaco-editor");
  // Simulate actual selection via CDP Input events
'
echo "{\"id\":1,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$SCRIPT\"}}" | websocat "$WS_URL"

# 2. Use CDP to query Claude panel for displayed status
VERIFY='document.querySelector(".claude-panel .status-text").textContent'
RESULT=$(echo "{\"id\":2,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"$VERIFY\",\"returnByValue\":true}}" | websocat --one-message "$WS_URL")

# 3. Verify user-visible output
STATUS=$(echo "$RESULT" | jq -r '.result.result.value')
if [[ "$STATUS" != *"5 lines selected"* ]]; then
    echo "✗ FAKE TEST: Panel doesn't show expected status"
    exit 1
fi
echo "✓ REAL TEST: Panel shows '$STATUS'"
```

### VS Code Extension Test Checklist

Before writing VS Code extension test, verify:

```
[ ] Protocol discovered (WebSocket/HTTP/IPC)
[ ] User workflow documented (what user clicks/sees)
[ ] Test uses SAME protocol as extension
[ ] Test simulates ACTUAL user actions (not API calls)
[ ] Test verifies PANEL DISPLAY (not internal state)
[ ] Test covers BOTH main and renderer processes
```

**If any box is unchecked → Your test is probably FAKE.**
</EXTREMELY-IMPORTANT>

## Integration

This skill is referenced by `dev-test` for Electron desktop application testing.

Related skills:
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-test-chrome/SKILL.md` and follow its instructions.
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-test-playwright/SKILL.md` and follow its instructions.
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-test-hammerspoon/SKILL.md` and follow its instructions.
- Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-tdd/SKILL.md` and follow its instructions.
- Chrome MCP skill - web debugging
- Playwright skill - headless web CI/CD
- Hammerspoon skill - macOS native apps
- TDD skill - TDD protocol and gate enforcement
