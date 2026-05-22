---
name: MCP Testing (Incognito Mode)
description: Automated testing with Chrome DevTools MCP server ALWAYS in incognito mode to avoid cache issues
version: 1.0.0
allowed-tools: [Bash, mcp__chrome-devtools__*, Read, Write]
---

# MCP Testing Skill - Incognito Mode Enforced

## Overview

This skill ensures ALL MCP Chrome DevTools testing is done in **incognito mode** to avoid browser cache issues that caused debugging loops in previous sessions.

**Critical Rule:** NEVER test in regular browser mode. Always launch Chrome with `--incognito` flag.

---

## Why Incognito Mode is Mandatory

### Problem: Browser Cache Persistence

**What Happened (2025-10-20 Session):**
- Frontend had bug (TypeError in authStore.ts)
- Fixed bug, rebuilt 8 times
- Same error persisted for 9 hours
- Root cause: Browser cache with `max-age=31536000, immutable` (1 year!)
- Chrome refused to revalidate even with hard reload (Cmd+Shift+R)

**Lesson Learned:**
> Regular browser mode is UNRELIABLE for testing after deployments due to aggressive Next.js caching.

### Incognito Benefits

✅ **Zero cache:** Every session starts fresh
✅ **No localStorage:** Avoids persisted auth state
✅ **No cookies:** Clean authentication tests
✅ **No service workers:** Avoids outdated JS workers
✅ **Reliable:** What you see = what's actually deployed

---

## How to Launch Chrome in Incognito Mode

### Correct Command (ALWAYS USE THIS)

```bash
# Kill any existing Chrome debugging sessions
pkill -f "remote-debugging-port=9222"

# Wait for port to be free
sleep 2

# Launch Chrome in INCOGNITO mode with debugging
open -na "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --incognito \
  --new-window \
  "https://matrix.mutuapix.com/login"
```

### Verify Incognito Mode

After launching, verify the window shows:
- 🕵️ **Incognito icon** in top-right corner (sunglasses/hat)
- Dark theme (if user has incognito theme)
- "You've gone incognito" message

---

## MCP Chrome DevTools Integration

### Connection Status

```bash
# Check if Chrome DevTools is accessible
curl -s http://127.0.0.1:9222/json/version | jq .
```

**Expected Output:**
```json
{
  "Browser": "Chrome/130.x.x.x",
  "Protocol-Version": "1.3",
  "User-Agent": "Mozilla/5.0 ...",
  "V8-Version": "13.0.x.x",
  "WebKit-Version": "537.36",
  "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/browser/..."
}
```

### Available MCP Tools

**Navigation:**
- `mcp__chrome-devtools__navigate_page` - Go to URL
- `mcp__chrome-devtools__navigate_page_history` - Back/forward
- `mcp__chrome-devtools__new_page` - Open new tab

**Inspection:**
- `mcp__chrome-devtools__take_snapshot` - Get page elements with UIDs
- `mcp__chrome-devtools__take_screenshot` - Visual capture
- `mcp__chrome-devtools__list_console_messages` - JavaScript errors
- `mcp__chrome-devtools__list_network_requests` - API calls

**Interaction:**
- `mcp__chrome-devtools__click` - Click element by UID
- `mcp__chrome-devtools__fill` - Fill input field
- `mcp__chrome-devtools__fill_form` - Fill multiple fields at once
- `mcp__chrome-devtools__hover` - Hover over element

**Debugging:**
- `mcp__chrome-devtools__evaluate_script` - Run JavaScript
- `mcp__chrome-devtools__get_network_request` - Inspect specific request
- `mcp__chrome-devtools__wait_for` - Wait for text to appear

**Performance:**
- `mcp__chrome-devtools__performance_start_trace` - Start recording
- `mcp__chrome-devtools__performance_stop_trace` - Stop and analyze

---

## Testing Workflow (Mandatory Steps)

### Step 1: Launch Incognito Chrome

```bash
# ALWAYS run this first
pkill -f "remote-debugging-port=9222"
sleep 2
open -na "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --incognito \
  --new-window \
  "https://matrix.mutuapix.com/login"
```

**Wait 3 seconds** for Chrome to fully start before MCP commands.

---

### Step 2: Verify Connection

```javascript
// Check MCP connection
mcp__chrome-devtools__list_pages()
```

**Expected:** At least 1 page showing login URL

---

### Step 3: Take Snapshot (Get Element UIDs)

```javascript
mcp__chrome-devtools__take_snapshot()
```

**Returns:** HTML structure with UIDs like:
```
[1] input type="email" placeholder="Email"
[2] input type="password" placeholder="Senha"
[3] button "Entrar"
```

---

### Step 4: Fill Login Form

```javascript
mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "1", value: "teste@mutuapix.com" },
    { uid: "2", value: "teste123" }
  ]
})
```

---

### Step 5: Click Login Button

```javascript
mcp__chrome-devtools__click({ uid: "3" })
```

---

### Step 6: Check for Errors

```javascript
// Wait for navigation
mcp__chrome-devtools__wait_for({ text: "Dashboard", timeout: 5000 })

// Check console errors
mcp__chrome-devtools__list_console_messages()
```

**Look for:**
- ❌ `TypeError: v is not a function`
- ❌ `ReferenceError: environment is not defined`
- ❌ Any errors with `authStore.ts` in stack trace

---

### Step 7: Check Network Requests

```javascript
mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["xhr", "fetch"]
})
```

**Verify:**
- ✅ `/api/v1/login` → 200 status
- ✅ `/api/v1/user` → 200 status (if dashboard loads)
- ❌ 401 errors (authentication failed)
- ❌ 500 errors (server error)

---

### Step 8: Take Screenshot (Evidence)

```javascript
mcp__chrome-devtools__take_screenshot({
  format: "png",
  fullPage: true
})
```

Save screenshot as evidence in `docs/testing/screenshots/`.

---

## Common Test Scenarios

### Scenario 1: Login Flow Test

**Goal:** Verify login works and dashboard loads

```javascript
// 1. Launch incognito
// (bash command above)

// 2. Navigate to login (already done in launch)
// 3. Take snapshot
const snapshot = mcp__chrome-devtools__take_snapshot()

// 4. Find email/password/button UIDs from snapshot
// 5. Fill form
mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "email-input-uid", value: "admin@mutuapix.com" },
    { uid: "password-input-uid", value: "Admin@123" }
  ]
})

// 6. Click login
mcp__chrome-devtools__click({ uid: "login-button-uid" })

// 7. Wait for dashboard
mcp__chrome-devtools__wait_for({ text: "Bem-vindo", timeout: 5000 })

// 8. Check errors
const errors = mcp__chrome-devtools__list_console_messages()
// Should be empty or only warnings

// 9. Screenshot success
mcp__chrome-devtools__take_screenshot({ filePath: "docs/testing/screenshots/login-success.png" })
```

---

### Scenario 2: Cache Validation

**Goal:** Verify new code is deployed (not cached)

```javascript
// 1. Launch incognito
// 2. Navigate to any page
mcp__chrome-devtools__navigate_page({ url: "https://matrix.mutuapix.com" })

// 3. Check for specific code pattern that was just deployed
const result = mcp__chrome-devtools__evaluate_script({
  function: `() => {
    // Look for new function/variable that didn't exist before
    return typeof window.someNewFeature !== 'undefined'
  }`
})

// 4. Check network for new bundle hash
const requests = mcp__chrome-devtools__list_network_requests({
  resourceTypes: ["script"]
})

// Verify bundle filename changed (new hash = new code)
// Example: page-8e52c12b50f60245.js (old) vs page-0757a9532994887c.js (new)
```

---

### Scenario 3: Console Error Detection

**Goal:** Find JavaScript errors that might cause bugs

```javascript
// 1. Navigate to page
mcp__chrome-devtools__navigate_page({ url: "https://matrix.mutuapix.com/user/dashboard" })

// 2. Wait for page load
await sleep(3000)

// 3. Get all console messages
const messages = mcp__chrome-devtools__list_console_messages()

// 4. Filter errors
const errors = messages.filter(m => m.level === 'error')

// 5. Report findings
if (errors.length > 0) {
  console.log(`❌ Found ${errors.length} errors:`)
  errors.forEach(e => console.log(`  - ${e.text} (${e.url}:${e.line})`))
} else {
  console.log(`✅ No console errors`)
}
```

---

## Integration with Deployment

### Post-Deploy Test (Automated)

After every deployment, run this test suite:

```bash
# 1. Deploy code
ssh root@138.199.162.115 'cd /var/www/mutuapix-frontend-production && rm -rf .next && npm run build && pm2 restart mutuapix-frontend'

# 2. Wait for PM2 restart
sleep 5

# 3. Launch incognito Chrome for testing
pkill -f "remote-debugging-port=9222"
sleep 2
open -na "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --incognito \
  --new-window \
  "https://matrix.mutuapix.com/login"

# 4. Wait for Chrome
sleep 3

# 5. Run MCP test suite (see scenarios above)
```

---

## Troubleshooting

### Issue: "Failed to fetch browser webSocket URL"

**Cause:** Chrome not running or port 9222 blocked

**Fix:**
```bash
# Kill existing sessions
pkill -f "remote-debugging-port=9222"

# Check if port is free
lsof -i :9222

# If port is in use by something else, kill it
kill -9 $(lsof -t -i:9222)

# Restart Chrome
open -na "Google Chrome" --args --remote-debugging-port=9222 --incognito
```

---

### Issue: MCP finds element but can't click it

**Cause:** Element might be covered by overlay or still loading

**Fix:**
```javascript
// Wait for element to be visible
mcp__chrome-devtools__wait_for({ text: "Button Text", timeout: 5000 })

// Then click
mcp__chrome-devtools__click({ uid: "button-uid" })
```

---

### Issue: Network requests show 401 errors

**Cause:** Authentication failed or token expired

**Debug:**
```javascript
// Check if login request succeeded
const loginRequest = mcp__chrome-devtools__get_network_request({
  url: "https://api.mutuapix.com/api/v1/login"
})

// Check response
console.log(loginRequest.response.body)

// Verify token was set in localStorage
const tokenCheck = mcp__chrome-devtools__evaluate_script({
  function: `() => {
    return localStorage.getItem('auth-storage')
  }`
})
```

---

## Best Practices

### ✅ DO

- **Always** launch Chrome with `--incognito` flag
- **Always** wait 3 seconds after launching Chrome before MCP commands
- **Always** check console messages after each test
- **Always** verify network requests succeeded (200 status)
- **Always** take screenshots as evidence
- **Always** close Chrome after tests to avoid port conflicts

### ❌ DON'T

- **Never** test in regular browser mode (cache issues!)
- **Never** assume element UIDs are stable (re-take snapshot each test)
- **Never** skip incognito mode "to save time" (will waste hours debugging cache)
- **Never** run multiple Chrome instances on port 9222 (conflict)
- **Never** trust hard reload (Cmd+Shift+R) - use incognito instead

---

## Checklist: Before Every MCP Test

- [ ] 1. Kill existing Chrome sessions: `pkill -f "remote-debugging-port=9222"`
- [ ] 2. Wait for port to be free: `sleep 2`
- [ ] 3. Launch Chrome with `--incognito` flag
- [ ] 4. Wait for Chrome to start: `sleep 3`
- [ ] 5. Verify connection: `mcp__chrome-devtools__list_pages()`
- [ ] 6. Take snapshot to get element UIDs
- [ ] 7. Run test scenario
- [ ] 8. Check console messages for errors
- [ ] 9. Verify network requests
- [ ] 10. Take screenshot as evidence

---

## Example: Complete Login Test

```bash
#!/bin/bash
# test-login-incognito.sh

echo "🧪 Testing Login in Incognito Mode"

# Step 1: Clean slate
echo "1. Killing existing Chrome sessions..."
pkill -f "remote-debugging-port=9222"
sleep 2

# Step 2: Launch incognito Chrome
echo "2. Launching Chrome in incognito mode..."
open -na "Google Chrome" --args \
  --remote-debugging-port=9222 \
  --incognito \
  --new-window \
  "https://matrix.mutuapix.com/login"

# Step 3: Wait for Chrome
echo "3. Waiting for Chrome to start..."
sleep 3

# Step 4: Verify connection
echo "4. Verifying MCP connection..."
curl -s http://127.0.0.1:9222/json/version > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ Chrome DevTools connected"
else
  echo "❌ Chrome DevTools not accessible"
  exit 1
fi

# Step 5: Run MCP tests (via Claude Code)
echo "5. Running MCP test suite..."
# (Claude Code MCP commands here)

echo "✅ Test complete!"
```

---

## Integration with CLAUDE.md

Add this to [CLAUDE.md](CLAUDE.md):

```markdown
## MCP Testing

**CRITICAL:** Always use incognito mode for MCP Chrome DevTools testing.

See: @.claude/skills/mcp-testing-incognito/SKILL.md

Quick launch:
```bash
pkill -f "remote-debugging-port=9222" && sleep 2 && \
open -na "Google Chrome" --args --remote-debugging-port=9222 \
  --incognito --new-window "https://matrix.mutuapix.com/login"
```
```

---

## Version History

**v1.0.0 (2025-10-20):**
- Initial creation after 9-hour debugging session
- Enforces incognito mode for all MCP testing
- Prevents browser cache issues that caused debugging loops
- Includes complete test scenarios and troubleshooting guide

---

**Status:** ✅ Active
**Last Updated:** 2025-10-20
**Related Issues:** Browser cache persistence (2025-10-20 session)
