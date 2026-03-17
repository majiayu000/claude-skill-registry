---
name: bknd-troubleshoot
description: Use when encountering Bknd errors, getting error messages, something not working, or needing quick fixes. Covers error code reference, quick solutions, and common mistake patterns.
---

# Troubleshoot Common Errors

Quick-reference guide for resolving Bknd errors by error code, symptom, or common mistake pattern.

## Prerequisites

- Bknd project running (or attempting to run)
- Error message or symptom to diagnose

## Error Code Quick Reference

### 400 Bad Request

**Cause:** Invalid request body or parameters

**Quick fixes:**
```bash
# Check JSON validity
echo '{"title":"Test"}' | jq .

# Verify Content-Type header
curl -X POST http://localhost:3000/api/data/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test"}'
```

**Common causes:**
- Missing `Content-Type: application/json` header
- Malformed JSON body
- Missing required field
- Invalid field type (string instead of number)
- Invalid enum value

### 401 Unauthorized

**Cause:** Missing or invalid authentication

**Quick fixes:**
```typescript
// Check token exists
console.log(localStorage.getItem("bknd_token"));

// Verify token with /me endpoint
const me = await api.auth.me();
console.log(me.ok ? "Valid" : "Invalid/expired");
```

**Common causes:**
- Token not stored (missing `storage: localStorage` in Api config)
- Token expired (check JWT `expires` config)
- Wrong auth header format (must be `Bearer <token>`)
- Cookie not sent (missing `credentials: "include"`)

**Fix pattern:**
```typescript
const api = new Api({
  host: "http://localhost:3000",
  storage: localStorage,  // Required for token persistence
});
```

### 403 Forbidden

**Cause:** Authenticated but insufficient permissions

**Quick fixes:**
```bash
# Check user's role
curl http://localhost:3000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

**Common causes:**
- Guard not enabled in config
- Role missing required permission
- Entity-specific permission needed
- Row-level policy blocking access

**Fix pattern:**
```typescript
auth: {
  guard: {
    enabled: true,
    roles: {
      user: {
        permissions: [
          "data.entity.read",
          "data.entity.create",  // Add missing permission
        ]
      }
    }
  }
}
```

### 404 Not Found

**Cause:** Endpoint or record doesn't exist

**Quick fixes:**
```bash
# List available routes
npx bknd debug routes

# List entities
curl http://localhost:3000/api/data

# Check entity name case (must match exactly)
curl http://localhost:3000/api/data/posts    # lowercase
```

**Common causes:**
- Entity name case mismatch (`Posts` vs `posts`)
- Schema not synced (restart server)
- Wrong endpoint path (`/api/auth/login` vs `/api/auth/password/login`)
- Record ID doesn't exist

### 409 Conflict

**Cause:** Duplicate value or constraint violation

**Quick fixes:**
```typescript
// Check for existing record before create
const exists = await api.data.readOneBy("users", { email });
if (!exists.ok) {
  await api.data.createOne("users", { email, ... });
}
```

**Common causes:**
- Duplicate unique field value
- User email already registered
- Unique constraint on field

### 413 Payload Too Large

**Cause:** File upload exceeds size limit

**Fix:**
```typescript
media: {
  body_max_size: 50 * 1024 * 1024,  // 50MB
}
```

### 500 Internal Server Error

**Cause:** Unhandled server exception

**Quick fixes:**
```bash
# Check server logs for stack trace
# Look for error details in response body
curl http://localhost:3000/api/data/posts 2>&1 | jq .error
```

**Common causes:**
- Database connection failed
- Invalid schema configuration
- Unhandled exception in seed/plugin
- Missing environment variable

## Common Mistake Patterns

### Using em() as EntityManager

**Wrong:**
```typescript
const schema = em({
  posts: entity("posts", { title: text() }),
});
schema.repo("posts").find();  // Error!
```

**Correct:**
```typescript
// em() is for schema definition only
const schema = em({
  posts: entity("posts", { title: text() }),
});

// Use SDK for queries
const api = new Api({ host: "http://localhost:3000" });
await api.data.readMany("posts");
```

### Wrong Auth Endpoint Path

**Wrong:**
```bash
POST /api/auth/login        # 404
POST /api/auth/register     # 404
```

**Correct:**
```bash
POST /api/auth/password/login      # For password strategy
POST /api/auth/password/register
POST /api/auth/google/login        # For Google OAuth
```

### Missing Storage in Api Config

**Symptom:** Token not persisting, logged out after refresh

**Wrong:**
```typescript
const api = new Api({
  host: "http://localhost:3000",
});
```

**Correct:**
```typescript
const api = new Api({
  host: "http://localhost:3000",
  storage: localStorage,  // Or sessionStorage
});
```

### Using enum() Instead of enumm()

**Wrong:**
```typescript
import { enum } from "bknd";  // Syntax error - reserved word
```

**Correct:**
```typescript
import { enumm } from "bknd";

entity("posts", {
  status: enumm(["draft", "published"]),
});
```

### Using primary() Function

**Wrong:**
```typescript
import { primary } from "bknd";  // Not exported in v0.20.0
```

**Correct:**
```typescript
// Primary keys are auto-generated
// To customize format:
entity("posts", { title: text() }, { primary_format: "uuid" });
```

### Wrong Policy Variable Prefix

**Wrong:**
```typescript
permissions: [{
  permission: "data.entity.read",
  filter: { user_id: { $eq: "@user.id" } },  // Wrong prefix
}]
```

**Correct:**
```typescript
permissions: [{
  permission: "data.entity.read",
  filter: { user_id: { $eq: "@auth.user.id" } },  // Correct prefix
}]
```

### Memory Database for Persistent Data

**Symptom:** Data disappears on restart

**Wrong:**
```bash
npx bknd run --memory
# Or config: { url: ":memory:" }
```

**Correct:**
```bash
npx bknd run --db-url "file:data.db"
# Or config: { url: "file:data.db" }
```

### Missing Guard Enable

**Symptom:** Permissions not working, everyone has access

**Wrong:**
```typescript
auth: {
  guard: {
    roles: { ... }  // Guard not enabled!
  }
}
```

**Correct:**
```typescript
auth: {
  guard: {
    enabled: true,  // Required!
    roles: { ... }
  }
}
```

### CORS Cookie Issues

**Symptom:** Auth works in Postman but not browser

**Fix:**
```typescript
// Server config
server: {
  cors: {
    origin: ["http://localhost:5173"],
    credentials: true,
  }
}

auth: {
  cookie: {
    secure: false,     // false for HTTP dev
    sameSite: "lax",   // Not "strict" for OAuth
  }
}

// Client fetch
fetch(url, { credentials: "include" });
```

### Filter vs Allow/Deny Effect

**Symptom:** RLS filter returns all records instead of filtering

**Wrong:**
```typescript
permissions: [{
  permission: "data.entity.read",
  effect: "allow",  // Won't filter!
  condition: { user_id: { $eq: "@auth.user.id" } },
}]
```

**Correct:**
```typescript
permissions: [{
  permission: "data.entity.read",
  effect: "filter",  // Filters results
  filter: { user_id: { $eq: "@auth.user.id" } },
}]
```

## Quick Diagnostic Commands

### Check Server Health

```bash
curl http://localhost:3000/api/data
```

### List All Routes

```bash
npx bknd debug routes
```

### Check Config Paths

```bash
npx bknd debug paths
```

### Test Auth

```bash
# Login
curl -X POST http://localhost:3000/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Check token
curl http://localhost:3000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

### Test Entity Access

```bash
# Unauthenticated
curl http://localhost:3000/api/data/posts

# Authenticated
curl http://localhost:3000/api/data/posts \
  -H "Authorization: Bearer <token>"
```

### Check Schema

```bash
curl http://localhost:3000/api/system/schema
```

## Environment-Specific Issues

### Development

| Issue | Solution |
|-------|----------|
| Config not loading | Check file name: `bknd.config.ts` |
| Port in use | `npx bknd run --port 3001` |
| Types outdated | `npx bknd types` |
| Hot reload not working | Restart server |

### Production

| Issue | Solution |
|-------|----------|
| JWT errors | Set `JWT_SECRET` env var (32+ chars) |
| Cookie not set | `secure: true` for HTTPS |
| 500 errors | Check logs, set `NODE_ENV=production` |
| D1 not found | Check wrangler.json bindings |

### Serverless

| Issue | Solution |
|-------|----------|
| Cold start slow | Use edge-compatible DB (D1, Turso) |
| File upload fails | Use S3/R2, not local storage |
| SQLite native error | Use LibSQL or PostgreSQL |

## Symptom-Based Troubleshooting

### "Config file could not be resolved"

```bash
# Check file exists
ls bknd.config.*

# Specify explicitly
npx bknd run -c ./bknd.config.ts
```

### "EADDRINUSE: address already in use"

```bash
# Find process
lsof -i :3000

# Use different port
npx bknd run --port 3001
```

### "spawn xdg-open ENOENT"

```bash
# Headless server - disable browser open
npx bknd run --no-open
```

### "Data disappears after restart"

```bash
# Check for memory mode in output
# Use file database
npx bknd run --db-url "file:data.db"
```

### "ERR_UNSUPPORTED_ESM_URL_SCHEME" (Windows)

1. Use Node.js 18+
2. Add `"type": "module"` to package.json
3. Use `.mjs` extension for config

### "TypeError: X is not a function"

Check import paths:
```typescript
// SDK client
import { Api } from "bknd/client";

// Schema builders
import { em, entity, text } from "bknd";

// Adapters
import { serve } from "bknd/adapter/node";      // Node
import { serve } from "bknd/adapter/cloudflare"; // CF Workers
```

## DOs and DON'Ts

**DO:**
- Check server logs first
- Verify entity names are lowercase
- Test with curl before debugging frontend
- Restart server after schema changes
- Use `npx bknd debug routes` for 404s

**DON'T:**
- Use `em()` for runtime queries
- Use `:memory:` for persistent data
- Forget `storage: localStorage` in Api
- Skip `enabled: true` for guard
- Use `@user.id` (use `@auth.user.id`)

## Related Skills

- **bknd-debugging** - Comprehensive debugging guide
- **bknd-local-setup** - Initial project setup
- **bknd-setup-auth** - Authentication configuration
- **bknd-assign-permissions** - Permission configuration
- **bknd-api-discovery** - Explore available endpoints
