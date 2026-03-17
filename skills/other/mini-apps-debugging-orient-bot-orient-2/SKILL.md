---
name: mini-apps-debugging
description: Debug and troubleshoot Mini-Apps when they fail to load, build, or run. Covers build checks, browser console inspection, bridge issues, and asset routing fixes.
---

# Mini-Apps Debugging Skill

Debug and troubleshoot Mini-Apps in the Orient. Use this skill when an app fails to load, has runtime errors, or behaves unexpectedly.

## Trigger Phrases

Use this skill when:

- "The mini-app is broken"
- "App won't load"
- "Console errors in the app"
- "Debug the meeting-scheduler app"
- "Why is the app failing?"
- "Fix the mini-app errors"

## Quick Debugging Checklist

### 1. Build Status Check

```bash
# Check if app is built
curl -s http://localhost/api/apps/<app-name> | jq '.app.isBuilt'

# Rebuild if needed
cd apps/<app-name> && npm run build
```

### 2. Common Build Errors

| Error                                 | Cause                           | Fix                                                 |
| ------------------------------------- | ------------------------------- | --------------------------------------------------- |
| `Cannot find module 'react'`          | Types not resolved for \_shared | Update tsconfig.json with `baseUrl` and `typeRoots` |
| `Property 'X' does not exist on type` | Props interface incomplete      | Extend `React.HTMLAttributes<Element>`              |
| `Missing parameter name` (Express 5)  | Old wildcard syntax `/*`        | Use `/{*splat}` instead                             |

### 3. Runtime Debugging with Browser MCP

Use the browser extension MCP tools:

```
1. browser_navigate - Go to the app URL
2. browser_console_messages - Check for JS errors
3. browser_snapshot - Get current page state
4. browser_take_screenshot - Visual verification
```

### 4. Bridge Connection Issues

If the app shows "Loading..." forever:

- App is waiting for bridge ping (30s timeout)
- In standalone mode, `useBridge()` should immediately set `isReady=true`

**Fix in `_shared/hooks/useBridge.ts`:**

```typescript
if (window.parent === window) {
  // Standalone mode - immediately ready
  setIsReady(true);
  return;
}
```

### 5. Asset Loading (404) Errors

If assets fail to load:

- Check `vite.config.ts` has correct `base` path

```typescript
// vite.config.ts
export default defineConfig({
  base: '/apps/<app-name>/', // Must match the serving path
  // ...
});
```

Rebuild after fixing:

```bash
cd apps/<app-name> && npm run build
```

### 6. Preview/Mock Mode

Apps running standalone (not in iframe) use mock responses.
The app should show a "Preview Mode" banner.

**Mock responses are returned for:**

- `calendar.createEvent` → Mock event with fake Meet link
- `scheduler.createJob` → Mock job ID
- `slack.sendDM/sendChannel` → No-op

## Debugging Workflow

### Step 1: Identify the Problem

```bash
# Get app status
curl -s http://localhost/api/apps/<app-name> | jq '.'

# Check build output
cd apps/<app-name> && npm run build 2>&1
```

### Step 2: Check Browser Console

Use browser MCP:

```
browser_navigate({ url: "http://localhost/apps/<app-name>/" })
browser_console_messages()
```

### Step 3: Common Error Categories

**Build Errors (TypeScript):**

- Props interface issues
- Missing React types
- Path resolution failures

**Runtime Errors (Browser):**

- Bridge timeout
- Asset 404s
- React rendering failures

**Server Errors (Nginx/Express):**

- 502 Bad Gateway → Server not running
- 404 → Route not configured
- SPA fallback catching app routes

### Step 4: Fix and Verify

1. Make the fix
2. Rebuild: `cd apps/<app-name> && npm run build`
3. Reload: `curl -X POST http://localhost/api/apps/reload`
4. Test: `browser_navigate` + `browser_snapshot`

## Server-Side Debugging

### Check Dashboard Server Logs

```bash
# In dev mode, check terminal output for:
grep -i "apps\|error" /tmp/dev.log | tail -20
```

### Check Apps Service Initialization

```bash
# Should see these logs on startup:
# [apps-service] Apps service created
# [apps-service] initializeApps: Apps initialized
# [dashboard-server] Apps services initialized
```

### Route Debugging

Check nginx routes `/apps/` in:

- `docker/nginx-local.conf` (dev)
- `docker/nginx.conf` (prod)

Should proxy to dashboard server:

```nginx
location /apps/ {
    proxy_pass http://dashboard_api_local/apps/;
}
```

## Testing Mini-Apps

### Manual Testing via Browser

1. Navigate to `http://localhost/apps/<app-name>/`
2. Check for "Preview Mode" banner (expected in standalone)
3. Fill out form and submit
4. Verify mock success response

### Automated Testing

```bash
# Use browser MCP for automated testing
browser_navigate({ url: "http://localhost/apps/<app-name>/" })
browser_type({ element: "Title input", ref: "e14", text: "Test" })
browser_click({ element: "Submit button", ref: "e29" })
browser_snapshot()  # Verify success state
```

## Adding Debug Logging to Apps

For deeper debugging, add console logs:

```typescript
// In App.tsx
const { bridge, isReady, isPreviewMode } = useBridge();
console.log('[App] Bridge state:', { isReady, isPreviewMode });

// In useBridge.ts
console.log('[Mock Bridge] Calling:', method, params);
```

## Related Skills

- `mini-apps` - Creating new apps
- `testing-strategy` - General testing patterns
- `production-debugging` - Server-side issues
