---
name: cloudflare-debug
description: Debugging patterns for Cloudflare Workers. Activates when troubleshooting errors, checking logs, or investigating production issues.
triggers:
  - debug
  - error
  - logs
  - tail
  - console
  - 500
  - 404
  - exception
  - troubleshoot
  - fix
  - broken
  - not working
---

# Cloudflare Workers Debugging

## Real-Time Log Commands

```bash
# All logs with pretty formatting
npx wrangler tail pitchey-api-prod --format pretty

# Errors only (most useful)
npx wrangler tail pitchey-api-prod --status error

# Filter by endpoint path
npx wrangler tail pitchey-api-prod --search "/api/browse"
npx wrangler tail pitchey-api-prod --search "/api/ndas"
npx wrangler tail pitchey-api-prod --search "/api/auth"
npx wrangler tail pitchey-api-prod --search "/api/pitches"

# Filter by HTTP method
npx wrangler tail pitchey-api-prod --method POST
npx wrangler tail pitchey-api-prod --method GET

# Combined filters
npx wrangler tail pitchey-api-prod --status error --search "/api/auth"
npx wrangler tail pitchey-api-prod --method POST --search "/api/ndas"
```

## Local Debugging with Breakpoints

```bash
# Start dev server with remote bindings (connects to real DB/R2/KV)
npx wrangler dev --remote

# Press 'd' to open Chrome DevTools
# - Set breakpoints in Sources tab
# - Inspect variables in Scope panel
# - Profile memory usage
# - Check network requests
```

## Test Endpoints Directly

```bash
# Health check
curl https://pitchey-api-prod.ndlovucavelle.workers.dev/health

# GET with auth (copy session cookie from browser DevTools)
curl -X GET "https://pitchey-api-prod.ndlovucavelle.workers.dev/api/user" \
  -H "Cookie: better-auth.session_token=YOUR_TOKEN"

# POST with JSON body
curl -X POST "https://pitchey-api-prod.ndlovucavelle.workers.dev/api/pitches" \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_TOKEN" \
  -d '{"title": "Test Pitch", "description": "Testing"}'

# Test browse endpoints
curl "https://pitchey-api-prod.ndlovucavelle.workers.dev/api/browse?tab=trending&limit=4"
curl "https://pitchey-api-prod.ndlovucavelle.workers.dev/api/browse?tab=new&limit=4"
```

## Common Error Patterns

### ReferenceError: X is not defined
- Check imports at top of file
- Verify variable is in scope where used
- Check if variable was renamed but not updated everywhere
- Look for typos in variable names

### TypeError: Cannot read property 'X' of undefined
- Add null checks before accessing properties
- Verify API response shape matches expectations
- Check if async data loaded before access

### 500 Internal Server Error
```bash
npx wrangler tail pitchey-api-prod --status error --format pretty
# Look for stack trace - shows exact file and line number
```

### 401 Unauthorized
- Better Auth uses cookies, NOT JWT headers
- Ensure `credentials: 'include'` in frontend fetch
- Check session hasn't expired
- Verify cookie domain matches

### 404 Not Found
- Check route is registered in Worker
- Verify HTTP method matches (GET vs POST)
- Check for typos in endpoint path

### CORS Errors
- Frontend must use `credentials: 'include'`
- Worker must return `Access-Control-Allow-Credentials: true`
- Origin must match exactly (including https://)

### Database Connection Errors
- Always use: `postgres(env.HYPERDRIVE.connectionString)`
- Never use direct Neon URL or pooler URL with Hyperdrive
- Check Neon dashboard for connection limit issues

### Session/Auth Errors (Better Auth)
- Uses cookies, NOT Authorization header
- Session cookie name: `better-auth.session_token`
- Must include credentials in fetch calls
- Check cookie SameSite and Secure attributes

## Quick Diagnostic Sequence

```bash
# 1. Check if Worker is responding
curl -I https://pitchey-api-prod.ndlovucavelle.workers.dev/health

# 2. Stream errors
npx wrangler tail pitchey-api-prod --status error --format pretty

# 3. Test specific endpoint
curl "https://pitchey-api-prod.ndlovucavelle.workers.dev/api/[endpoint]"

# 4. Check with auth if needed
# Get cookie from browser, test with curl

# 5. If still stuck, enable local debugging
npx wrangler dev --remote
# Press 'd' for DevTools
```