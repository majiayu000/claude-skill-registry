---
name: chrome-devtools-testing
description: Use when testing web applications with Chrome DevTools MCP. Covers GUI Chrome setup and dev server configuration. Required reading before any browser automation.
---

# Chrome DevTools Testing Skill

## Purpose

Automate testing of web applications using Chrome DevTools Protocol (CDP) with GUI Chrome browser.

## Standard Setup

### Step 1: Start Chrome (GUI Browser)

```bash
/usr/bin/google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-profile \
  --no-first-run \
  --no-default-browser-check \
  "about:blank" &

sleep 3
curl -s http://127.0.0.1:9222/json/version
```

**MANDATORY FLAGS:**

- `--user-data-dir=/tmp/chrome-debug-profile` - Remote debugging REQUIRES a non-default profile
- `--remote-debugging-port=9222` - Standard CDP port

**NOTE:** Headless mode (`--headless=new`) has known issues. Use GUI browser instead.

### Step 2: Start Dev Server

```bash
pnpm exec vite --host 0.0.0.0
```

### Step 3: Navigate and Test

```
navigate_page(url: "http://localhost:PORT", type: "url")
take_snapshot()
```

---

## Complete Workflow

### Clean Start

```bash
# Kill existing Chrome sessions
pkill -f "chrome.*remote-debugging" || true

# Kill process on dev port if needed
fuser -k 3000/tcp || true
```

### Start Services

```bash
# 1. Start Chrome (GUI)
/usr/bin/google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-profile \
  --no-first-run \
  --no-default-browser-check \
  "about:blank" &

sleep 3
curl -s http://127.0.0.1:9222/json/version

# 2. Start dev server
cd /path/to/app
pnpm exec vite --host 0.0.0.0 &

sleep 5
```

### MCP Connection

If chrome-devtools MCP shows "Not connected":

1. Ask user to run `/mcp` to reconnect
2. Wait for confirmation
3. Retry

---

## Troubleshooting

| Symptom                               | Fix                                             |
| ------------------------------------- | ----------------------------------------------- |
| "requires non-default data directory" | Add `--user-data-dir=/tmp/chrome-debug-profile` |
| "Not connected" from MCP              | User runs `/mcp` to reconnect                   |
| `ERR_CONNECTION_REFUSED`              | Start dev server with `--host 0.0.0.0`          |
| Chrome won't start                    | `pkill -f "chrome.*remote-debugging"`           |
| Stale UIDs                            | Take fresh snapshot                             |

---

## MCP Tools Quick Reference

### Navigation

| Tool            | Purpose           |
| --------------- | ----------------- |
| `list_pages`    | List open tabs    |
| `select_page`   | Switch active tab |
| `new_page`      | Open new tab      |
| `navigate_page` | Navigate URL      |
| `close_page`    | Close tab         |

### Inspection

| Tool                    | Purpose              |
| ----------------------- | -------------------- |
| `take_snapshot`         | Get DOM with UIDs    |
| `take_screenshot`       | Capture visual       |
| `list_console_messages` | Get console logs     |
| `list_network_requests` | Get network activity |

### Interaction

| Tool        | Purpose        |
| ----------- | -------------- |
| `click`     | Click element  |
| `fill`      | Enter text     |
| `hover`     | Hover element  |
| `press_key` | Keyboard input |

---

## Pre-Flight Checklist

- [ ] Chrome started with `--user-data-dir` flag
- [ ] `curl http://127.0.0.1:9222/json/version` returns JSON
- [ ] Dev server started with `--host 0.0.0.0`
- [ ] MCP chrome-devtools connected

---

## Common Mistakes

1. **Missing `--user-data-dir`** → Remote debugging fails
2. **Multiple Chrome instances** → Port conflicts
3. **Multiple dev servers** → Port conflicts
4. **Not waiting for services** → Connection fails
5. **Not checking MCP status** → Tools fail silently

---

## Known Failures (WSL Environment)

### Problem: Chrome Starts But MCP Tools Fail

**Symptoms:**

- `curl http://127.0.0.1:9222/json/version` returns valid JSON
- MCP chrome-devtools tools return "Not connected"
- Chrome window never appears visually for user
- Multiple background processes accumulate

**Root Cause:** In WSL2 environments, Chrome may technically start with debugging enabled but fail to establish proper GUI display or MCP connection. The CDP endpoint responds to curl but the MCP integration cannot connect.

**What To Do:**

1. **Acknowledge the failure immediately:**

   ```
   Chrome DevTools automation failed. You can restart manually.
   ```

2. **Do NOT:**
   - Keep retrying indefinitely
   - Spawn more background processes
   - Pretend it might work next time

3. **Tell user to verify manually:**
   - Open Chrome on Windows side
   - Navigate to `http://localhost:PORT`
   - Check browser console for errors

### When This Happens

If MCP tools fail after Chrome appears to start:

```
Chrome DevTools automation failed.
HTTP verification shows servers are responding.
Please verify manually in your browser:
- http://localhost:3000 (main app)
- http://localhost:5173 (dev server)
```

Then stop attempting browser automation.
