---
name: chrome-devtools-mcp
description: Testing UI and automating browsers via Chrome DevTools MCP. Use when taking screenshots, checking console errors, testing UI interactions, or verifying visual changes.
license: MIT
compatibility: Requires Chrome DevTools MCP server configured via 'claude mcp add chrome-devtools'
allowed-tools: mcp__chrome-devtools__*
---

# Chrome DevTools MCP - UI Testing Skill

## Auto-activation Triggers

### English
- "test UI", "test the UI", "UI test"
- "open browser", "launch browser"
- "take screenshot", "capture screenshot"
- "check console errors", "any console errors"
- "test in browser", "verify in browser"

### 中文
- "測試 UI"、"UI 測試"、"測試畫面"
- "開瀏覽器"、"啟動瀏覽器"
- "截圖"、"擷取畫面"
- "檢查錯誤"、"有沒有錯誤"、"console 錯誤"
- "瀏覽器測試"、"在瀏覽器驗證"

### Auto-trigger Scenarios
- User completed a feature and needs visual verification
- User asks to verify a UI change
- User wants to debug a visual issue

## Prerequisites

Ensure Chrome DevTools MCP is configured in Claude Code:

```bash
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

Or with options:
```bash
# Headless mode (no UI)
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --headless

# Isolated session (clean browser state)
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest --isolated
```

## Available MCP Tools (26 total)

### Navigation & Pages
| Tool | Description |
|------|-------------|
| `mcp__chrome-devtools__new_page` | Open new page with URL |
| `mcp__chrome-devtools__navigate_page` | Navigate to URL, back, forward, reload |
| `mcp__chrome-devtools__list_pages` | List all open pages |
| `mcp__chrome-devtools__select_page` | Select page by index |
| `mcp__chrome-devtools__close_page` | Close page by index |
| `mcp__chrome-devtools__wait_for` | Wait for text to appear |

### Input & Interaction
| Tool | Description |
|------|-------------|
| `mcp__chrome-devtools__click` | Click element by uid |
| `mcp__chrome-devtools__fill` | Fill input/textarea/select |
| `mcp__chrome-devtools__fill_form` | Fill multiple form elements |
| `mcp__chrome-devtools__hover` | Hover over element |
| `mcp__chrome-devtools__drag` | Drag element to another |
| `mcp__chrome-devtools__press_key` | Press key or combination |
| `mcp__chrome-devtools__handle_dialog` | Accept/dismiss browser dialogs |
| `mcp__chrome-devtools__upload_file` | Upload file through input |

### Debugging & Inspection
| Tool | Description |
|------|-------------|
| `mcp__chrome-devtools__take_snapshot` | Get page A11y tree with UIDs |
| `mcp__chrome-devtools__take_screenshot` | Capture page/element screenshot |
| `mcp__chrome-devtools__evaluate_script` | Run JavaScript in page |
| `mcp__chrome-devtools__list_console_messages` | List console messages |
| `mcp__chrome-devtools__get_console_message` | Get specific console message |

### Network
| Tool | Description |
|------|-------------|
| `mcp__chrome-devtools__list_network_requests` | List network requests |
| `mcp__chrome-devtools__get_network_request` | Get request details |

### Performance
| Tool | Description |
|------|-------------|
| `mcp__chrome-devtools__performance_start_trace` | Start performance trace |
| `mcp__chrome-devtools__performance_stop_trace` | Stop trace recording |
| `mcp__chrome-devtools__performance_analyze_insight` | Analyze performance insights |

### Emulation
| Tool | Description |
|------|-------------|
| `mcp__chrome-devtools__emulate` | Emulate network/CPU throttling |
| `mcp__chrome-devtools__resize_page` | Resize viewport |

## Common UI Testing Patterns

### 1. Basic Page Verification

```
1. take_snapshot → Get page structure with element UIDs
2. take_screenshot → Visual verification
3. list_console_messages → Check for errors
```

### 2. Form Testing Flow

```
1. new_page → Open target URL
2. take_snapshot → Get form element UIDs
3. fill_form → Fill all form fields
4. click → Submit button
5. wait_for → Wait for success message
6. take_screenshot → Capture result
```

### 3. Interactive Component Testing

```
1. take_snapshot → Get element UIDs
2. click → Trigger component action
3. take_snapshot → Verify state change
4. list_console_messages → Check for errors
```

### 4. Responsive Design Testing

```
1. resize_page → Set mobile viewport (375x667)
2. take_screenshot → Mobile view
3. resize_page → Set tablet viewport (768x1024)
4. take_screenshot → Tablet view
5. resize_page → Set desktop viewport (1920x1080)
6. take_screenshot → Desktop view
```

### 5. Performance Audit

```
1. performance_start_trace → Begin recording
2. navigate_page → Load page
3. performance_stop_trace → End recording
4. performance_analyze_insight → Get CWV scores
```

### 6. Network Request Verification

```
1. navigate_page → Load page
2. list_network_requests → See all requests
3. get_network_request → Check specific API response
```

## Workflow: Post-Feature UI Verification

When you complete a feature that requires UI testing:

### Step 1: Start Browser
```
Use: mcp__chrome-devtools__new_page
URL: http://localhost:{PORT}/path-to-feature

Common ports:
- Next.js: 3000 or custom (this project: 1408)
- Vite: 5173
- Angular: 4200
```

### Step 2: Take Snapshot (ALWAYS do this first)
```
Use: mcp__chrome-devtools__take_snapshot
This returns element UIDs needed for interactions
```

### Step 3: Interact with Elements
```
Use element UIDs from snapshot to:
- click buttons
- fill forms
- hover for tooltips
```

### Step 4: Verify Results
```
- take_screenshot for visual verification
- list_console_messages for error checking
- take_snapshot for DOM state verification
```

## Error Handling

### Navigation Timeout
If `navigate_page` times out:
1. Check if dev server is running
2. Use `new_page` instead of `navigate_page`
3. Increase timeout: `timeout: 30000`

### Element Not Found
If click/fill fails:
1. Re-run `take_snapshot` to get latest UIDs
2. Verify element is within viewport
3. Use `wait_for` to wait for element to appear

### Page Not Loading
If page fails to load:
1. Verify URL is correct
2. Check dev server logs
3. Try `navigate_page` with `type: "reload"`

## Tips

1. **Always take_snapshot first** - You need element UIDs before interacting
2. **Prefer snapshot over screenshot** - Faster and provides actionable data
3. **Check console after interactions** - Catch runtime errors early
4. **Use wait_for after navigation** - Ensure page is loaded before interacting
5. **Filter network requests** - Use resourceTypes to focus on API calls
6. **Re-snapshot after interactions** - UIDs may change after DOM updates

## Quick Reference

```
# Open dev server and test
mcp__chrome-devtools__new_page → http://localhost:{PORT}

# Get page structure
mcp__chrome-devtools__take_snapshot

# Interact (use UID from snapshot)
mcp__chrome-devtools__click → uid: "abc123"
mcp__chrome-devtools__fill → uid: "input1", value: "test"

# Verify
mcp__chrome-devtools__take_screenshot
mcp__chrome-devtools__list_console_messages → types: ["error", "warn"]
```

## Complete Example: Testing a Login Form

Complete login form testing workflow:

```
Step 1: Open login page
────────────────────
mcp__chrome-devtools__new_page
  url: "http://localhost:3000/login"

Step 2: Get page structure
────────────────────
mcp__chrome-devtools__take_snapshot

Output:
  uid=1_10 textbox "Email"
  uid=1_15 textbox "Password"
  uid=1_20 button "Sign In"

Step 3: Fill form
────────────────────
mcp__chrome-devtools__fill_form
  elements: [
    { uid: "1_10", value: "test@example.com" },
    { uid: "1_15", value: "password123" }
  ]

Step 4: Click login
────────────────────
mcp__chrome-devtools__click
  uid: "1_20"

Step 5: Wait for result
────────────────────
mcp__chrome-devtools__wait_for
  text: "Welcome"
  timeout: 5000

Step 6: Verify
────────────────────
mcp__chrome-devtools__take_screenshot  → Verify UI is correct
mcp__chrome-devtools__list_console_messages → Check for errors
  types: ["error", "warn"]

Step 7: Check API requests (optional)
────────────────────
mcp__chrome-devtools__list_network_requests
  resourceTypes: ["fetch", "xhr"]
```

## Responsive Testing Example

Test responsive design across breakpoints:

```
# Mobile (iPhone SE)
mcp__chrome-devtools__resize_page → width: 375, height: 667
mcp__chrome-devtools__take_screenshot

# Tablet (iPad)
mcp__chrome-devtools__resize_page → width: 768, height: 1024
mcp__chrome-devtools__take_screenshot

# Desktop
mcp__chrome-devtools__resize_page → width: 1920, height: 1080
mcp__chrome-devtools__take_screenshot
```
