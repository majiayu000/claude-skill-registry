---
name: BrowserBridge
description: Real-time browser debugging and interaction via WebSocket bridge server on localhost:3141
---

# BrowserBridge - Browser Debugging Integration

BrowserBridge enables Claude Code to interact with web browsers in real-time through a C# bridge server and Chrome/Edge extension for debugging, DOM inspection, and JavaScript execution.

## Quick Start for Claude

**Prerequisites Check:**

```bash
curl http://localhost:3141/api/browser/health
```

If successful, you can execute browser commands. If connection refused, bridge server is not running.

**Common Commands:**

```bash
# Execute JavaScript
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.title"}'

# Inspect element
curl -X POST http://localhost:3141/api/browser/inspect -H "Content-Type: application/json" -d '{"selector": "#myElement"}'

# List connections
curl http://localhost:3141/api/browser/connections
```

## Setup Requirements

1. **Bridge Server Running:** User must have started the bridge server
   ```bash
   cd bridge-server/ClaudeBrowserBridge
   dotnet run
   ```

2. **Extension Connected:** User must have:
   - Loaded the extension in Chrome/Edge (`chrome://extensions/`)
   - Clicked "Connect to Claude" in the extension popup
   - Status shows "Connected" (green dot)

3. **Active Webpage:** User must be viewing a webpage in the browser

## Available API Endpoints

### 1. Health Check
```bash
curl http://localhost:3141/api/browser/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-21T10:30:00Z",
  "connections": 1
}
```

Use this to verify bridge server is running and count connected browsers.

### 2. List Connections
```bash
curl http://localhost:3141/api/browser/connections
```

Response shows all connected browser tabs with connection IDs and last activity.

### 3. Execute JavaScript
```bash
curl -X POST http://localhost:3141/api/browser/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "YOUR_JAVASCRIPT_HERE"}'
```

**Common Scripts:**

Get page title:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.title"}'
```

Check if element exists:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#myId\") !== null"}'
```

Get element innerHTML:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#myId\")?.innerHTML"}'
```

Get element count:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelectorAll(\".className\").length"}'
```

Check if function exists:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "typeof window.myFunction"}'
```

Get computed style:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "window.getComputedStyle(document.querySelector(\"#myId\")).display"}'
```

Test DOM change live:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#test\").style.border = \"2px solid red\""}'
```

**Note:** Results are sent via WebSocket. The bridge server writes script results to a file for easy access:

```bash
# Read the last script result
cat "C:/RI Services/BrowserBridge/claude_browser_last_result.json"
```

Example result:
```json
{"type":"script_result","success":true,"result":"2408","timestamp":1764632896201}
```

For debugging, all messages are logged to:
```bash
powershell -Command "Get-Content 'C:\RI Services\BrowserBridge\all_messages.log' -Tail 20"
```

### 4. Inspect Element
```bash
curl -X POST http://localhost:3141/api/browser/inspect \
  -H "Content-Type: application/json" \
  -d '{"selector": "#myElement"}'
```

Inspection results appear in bridge server console with:
- Full HTML (`outerHTML` and `innerHTML`)
- Computed styles (display, position, width, height, colors, fonts)
- Bounding box (x, y, width, height, position on screen)
- Element properties (tagName, className, id)

**Common Selectors:**
- By ID: `#pagination`
- By class: `.button-class`
- By attribute: `[data-id="123"]`
- Complex: `#parent .child:first-of-type`

### 5. Take Screenshot
```bash
curl -X POST http://localhost:3141/api/browser/screenshot \
  -H "Content-Type: application/json" \
  -d '{"fullPage": false}'
```

Screenshot sent as base64 PNG via WebSocket to bridge server logs.

### 6. Get Connection Details
```bash
curl http://localhost:3141/api/browser/connections/{connectionId}
```

Get detailed info about a specific connection.

### 7. Get Message History
```bash
curl "http://localhost:3141/api/browser/connections/{connectionId}/history?limit=50"
```

Get recent messages from a connection (console logs, errors, etc).

## Automatic Monitoring

The extension automatically captures and sends to bridge server:

1. **Console Logs:** All `console.log`, `console.warn`, `console.error`, `console.info`
2. **JavaScript Errors:** Uncaught exceptions with stack traces
3. **Promise Rejections:** Unhandled promise rejections
4. **Page Events:** Page loads, tab switches, navigation

Check the bridge server console to see these events in real-time.

## Usage Patterns

### Debugging "Element Not Visible" Issues

1. Check if element exists:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#myElement\") !== null"}'
```

2. If true, inspect it:
```bash
curl -X POST http://localhost:3141/api/browser/inspect -H "Content-Type: application/json" -d '{"selector": "#myElement"}'
```

3. Check bridge server logs for:
   - Is it hidden? (`display: none` or `visibility: hidden`)
   - Is it empty? (no innerHTML)
   - Is it off-screen? (negative position values)

### Verifying JavaScript Functions

Check if function exists:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "typeof window.updatePaginationControls"}'
```

If returns "function", get its source:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "window.updatePaginationControls.toString()"}'
```

### Accessing Module-Scoped Variables

ES6 modules encapsulate their variables, making them inaccessible from the global scope. Instead of repeatedly exposing individual variables, add a generic `getValue` helper:

**Add this pattern to the module:**
```javascript
// Debug helper - access module values by dot-notation path
window.getValue = (path) => {
    const moduleVars = { state, filterOptions, myFunction, loadData }; // Add all you need
    const parts = path.split('.');
    let val = moduleVars[parts[0]];
    for (let i = 1; i < parts.length && val !== undefined; i++) {
        val = val[parts[i]];
    }
    return val;
};
```

**Usage from Browser Bridge:**
```bash
# Get nested state value
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "getValue(\"state.filters.lang\")"}'

# Get array length
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "getValue(\"filterOptions.refs\")?.length"}'

# Get complex state as JSON
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "JSON.stringify({filters: getValue(\"state.filters\"), count: getValue(\"state.data.totalCount\")})"}'
```

**Alternative: Expose state to window directly:**
```javascript
// At module start
const state = window.__state = { /* ... */ };
```

Then access via `window.__state.filters.lang` without needing `getValue`.

### Testing DOM Changes Live

Before suggesting code changes, test them:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelectorAll(\"button\").forEach(b => b.style.border = \"2px solid red\")"}'
```

User sees changes immediately. If it works, provide the permanent CSS/JS fix.

### Checking for Null/Undefined

Always use optional chaining to avoid errors:
```bash
# Good
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#myId\")?.innerHTML || \"Element not found\""}'

# Bad (will throw if element doesn't exist)
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#myId\").innerHTML"}'
```

### Common Bug: Missing Optional Chaining on Method Calls

When calling functions programmatically that normally run from UI events, `event` may be undefined:

```javascript
// BAD - throws "Cannot read properties of undefined (reading 'add')"
event?.target?.classList.add('active');  // classList is undefined when event is undefined

// GOOD - chain all the way through
event?.target?.classList?.add('active');
```

This applies to any pattern where you use `?.` but then call a method on the result.

## Error Handling

### Connection Refused
```
curl: (7) Failed to connect to localhost port 3141
```

**Cause:** Bridge server not running

**Tell User:**
```
The bridge server isn't running. Please start it:

cd bridge-server/ClaudeBrowserBridge
dotnet run
```

### No Connections
```json
{"connections": 0}
```

**Cause:** Extension not connected

**Tell User:**
```
The extension isn't connected. Please:
1. Click the extension icon in your browser
2. Click "Connect to Claude"
3. Verify status shows "Connected" (green dot)
```

### Script Execution Errors

Results appear in bridge server console. Check logs for:
- Element doesn't exist → Use optional chaining or check existence first
- Function undefined → Verify script loaded, check console for errors
- Permission denied → Site has strict CSP, some operations blocked

## Best Practices

1. **Always check health first:** Verify server is running before attempting commands
2. **Use specific selectors:** Prefer IDs over classes, classes over tags
3. **Check for null:** Use optional chaining (`?.`) or null checks
4. **Watch server logs:** Execution results appear in bridge server console
5. **Test before fixing:** Execute test commands live before suggesting code changes
6. **Escape quotes:** Use `\"` for quotes inside JSON strings

## JSON Escaping

When constructing curl commands with nested quotes:

```bash
# Escape double quotes inside JSON
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#myId\")"}'

# Or use single quotes in JavaScript
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d "{\"script\": \"document.querySelector('#myId')\"}"
```

## Troubleshooting

### Extension Not Working

Tell user to:
1. Refresh the webpage after connecting extension
2. Check browser console (F12) for "Claude Browser Bridge content script loaded"
3. Verify `window.__claudeBridge` exists in console

### Server Not Receiving Messages

1. Verify WebSocket connection in extension popup (should show "Connected")
2. Check bridge server console for connection messages
3. Try disconnect/reconnect in extension popup

### Results Not Appearing

Results are sent via WebSocket to bridge server console. User must check the terminal running `dotnet run` to see:
- Script execution results
- Inspection data
- Console logs from browser
- Error messages

## Security Notes

- Bridge server only accepts localhost connections (127.0.0.1)
- No authentication (development tool only)
- Can execute arbitrary JavaScript (by design)
- Not for production use
- Some sites with strict CSP may block functionality

## Example Workflow

**User says:** "The pagination controls aren't showing up"

**Claude:**

1. Check connection:
```bash
curl http://localhost:3141/api/browser/health
```

2. Check if element exists:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "document.querySelector(\"#pagination\") !== null"}'
```

3. If true, inspect it:
```bash
curl -X POST http://localhost:3141/api/browser/inspect -H "Content-Type: application/json" -d '{"selector": "#pagination"}'
```

4. Check bridge server logs → See it has `display: none` or empty innerHTML

5. Find why:
```bash
curl -X POST http://localhost:3141/api/browser/execute -H "Content-Type: application/json" -d '{"script": "typeof updatePaginationControls"}'
```

6. Diagnose issue and provide fix to user

## Quick Reference

| Action | Endpoint | Method |
|--------|----------|--------|
| Health check | `/api/browser/health` | GET |
| List connections | `/api/browser/connections` | GET |
| Execute JavaScript | `/api/browser/execute` | POST |
| Inspect element | `/api/browser/inspect` | POST |
| Screenshot | `/api/browser/screenshot` | POST |
| Connection details | `/api/browser/connections/{id}` | GET |
| Message history | `/api/browser/connections/{id}/history` | GET |

## Related Project Files

- Bridge Server: `bridge-server/ClaudeBrowserBridge/`
- Extension: `extension/`
- Setup Guide: `SETUP.md`
