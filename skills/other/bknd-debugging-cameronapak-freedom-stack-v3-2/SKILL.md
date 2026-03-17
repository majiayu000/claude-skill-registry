---
name: bknd-debugging
description: Use when troubleshooting Bknd issues, debugging errors, fixing common problems, or diagnosing why something isn't working. Covers CLI debug commands, error codes, logging, common issues and solutions.
---

# Debugging Common Issues

Diagnose and fix common Bknd problems using CLI tools, error analysis, and systematic troubleshooting.

## Prerequisites

- Bknd project set up locally
- Terminal/command line access
- Basic understanding of HTTP status codes

## When to Use UI Mode

- Inspecting data in admin panel (`/admin`)
- Verifying entity schema visually
- Testing CRUD operations manually
- Checking user/role configurations

## When to Use Code Mode

- Running debug CLI commands
- Analyzing API response errors
- Checking route registration
- Inspecting configuration paths
- Reviewing server logs

## CLI Debug Commands

### Show All Registered Routes

```bash
npx bknd debug routes
```

Output shows every HTTP endpoint:
- API routes (`/api/data/*`, `/api/auth/*`, `/api/media/*`)
- Admin routes (`/admin/*`)
- Custom Flow HTTP triggers
- Plugin routes

Use when: endpoint returns 404, verifying custom routes registered.

### Show Internal Paths

```bash
npx bknd debug paths
```

Output:
```
[PATHS] {
  rootpath: '/path/to/bknd',
  distPath: '/path/to/dist',
  relativeDistPath: './dist',
  cwd: '/your/project',
  dir: '/path/to/cli',
  resolvedPkg: '/path/to/package.json'
}
```

Use when: config file not loading, path resolution issues.

### CLI Help

```bash
npx bknd --help
npx bknd run --help
npx bknd types --help
```

## HTTP Error Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Invalid JSON, missing required fields, validation error |
| 401 | Unauthorized | Missing/invalid/expired token |
| 403 | Forbidden | Valid token but insufficient permissions |
| 404 | Not Found | Wrong endpoint, entity doesn't exist, record not found |
| 409 | Conflict | Duplicate unique field, user already exists |
| 413 | Payload Too Large | File upload exceeds `body_max_size` |
| 500 | Server Error | Unhandled exception, database error |

## Common Issues & Solutions

### Config File Not Loading

**Symptoms:** "Config file could not be resolved" error

**Diagnose:**
```bash
# Check config exists
ls bknd.config.*

# Check current directory
pwd

# Check what bknd sees
npx bknd debug paths
```

**Solutions:**
```bash
# Ensure correct extension
mv bknd.config.js bknd.config.ts

# Specify explicitly
npx bknd run -c ./bknd.config.ts

# Check supported extensions: .ts, .js, .mjs, .cjs, .json
```

### Database Not Persisting

**Symptoms:** Data disappears on server restart

**Diagnose:**
```bash
# Check if using memory mode
# Look for "Using in-memory" in startup output
npx bknd run

# Check for database file
ls *.db
```

**Solutions:**
```bash
# Use file-based database
npx bknd run --db-url "file:data.db"

# NOT memory mode
npx bknd run --memory  # Data will be lost!

# Verify in config:
# connection: { url: "file:data.db" }  ✓
# connection: { url: ":memory:" }      ✗
```

### Port Already in Use

**Symptoms:** `EADDRINUSE: address already in use`

**Diagnose:**
```bash
# Find process using port
lsof -i :3000

# Or on Windows
netstat -ano | findstr :3000
```

**Solutions:**
```bash
# Use different port
npx bknd run --port 3001

# Kill existing process
kill -9 <PID>

# Or on Windows
taskkill /PID <PID> /F
```

### Authentication Not Working

**Symptoms:** 401 errors, token not persisting, user always null

**Diagnose:**
```bash
# Test login endpoint
curl -X POST http://localhost:3000/api/auth/password/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Check auth configuration
# Look for "strategy" in response errors
```

**Solutions:**

1. **Auth not enabled:**
```typescript
export default {
  app: {
    auth: { enabled: true },  // Required!
  }
}
```

2. **Wrong strategy path:**
```bash
# Password auth endpoint:
POST /api/auth/password/login    # ✓
POST /api/auth/login             # ✗ 404
```

3. **JWT secret not set (production):**
```typescript
auth: {
  jwt: {
    secret: process.env.JWT_SECRET,  // Required for production
  }
}
```

4. **Cookie not set (CORS):**
```typescript
auth: {
  cookie: {
    secure: false,     // Set true only for HTTPS
    sameSite: "lax",   // Not "strict" for OAuth
  }
}
```

5. **Token not persisting (frontend):**
```typescript
const api = new Api({
  host: "http://localhost:3000",
  storage: localStorage,  // Required for token persistence
});
```

### Permission Denied (403)

**Symptoms:** Valid token but 403 Forbidden

**Diagnose:**
```bash
# Check user's role
curl http://localhost:3000/api/auth/me \
  -H "Authorization: Bearer <token>"

# Check role permissions in config
```

**Solutions:**

1. **Guard not enabled:**
```typescript
export default {
  app: {
    auth: {
      guard: { enabled: true },  // Required for permissions
    }
  }
}
```

2. **No default role (anonymous access):**
```typescript
auth: {
  guard: {
    roles: {
      anonymous: {
        is_default: true,  // Allow unauthenticated access
        permissions: ["data.entity.read"],
      }
    }
  }
}
```

3. **Role missing permission:**
```typescript
roles: {
  user: {
    permissions: [
      "data.entity.read",
      "data.entity.create",  // Add if needed
    ]
  }
}
```

4. **Entity-specific permission needed:**
```typescript
permissions: [
  { permission: "data.entity.read", entity: "posts" },
]
```

### Entity/Record Not Found (404)

**Symptoms:** 404 on data endpoints

**Diagnose:**
```bash
# List all entities
curl http://localhost:3000/api/data

# Check entity name (case-sensitive)
curl http://localhost:3000/api/data/Posts    # ✗
curl http://localhost:3000/api/data/posts    # ✓

# Verify routes
npx bknd debug routes | grep data
```

**Solutions:**

1. **Schema not synced:**
```bash
# Restart server to sync schema
npx bknd run
```

2. **Entity name case mismatch:**
```typescript
// Schema defines lowercase
entity("posts", { ... })

// API call must match exactly
api.data.readMany("posts");     // ✓
api.data.readMany("Posts");     // ✗ 404
```

3. **Record doesn't exist:**
```typescript
const result = await api.data.readOne("posts", 999);
if (!result.ok) {
  console.log("Not found:", result.status);  // 404
}
```

### Type Errors with em()

**Symptoms:** TypeScript errors using schema object

**Problem:** `em()` returns schema definition, NOT queryable EntityManager.

```typescript
// WRONG - this will fail
const schema = em({
  posts: entity("posts", { title: text() }),
});
schema.repo("posts").find();  // ✗ Error!

// CORRECT - use SDK for queries
const api = new Api({ url: "http://localhost:3000" });
await api.data.readMany("posts");  // ✓
```

For direct database access (server-side only):
```typescript
const app = new App(config);
await app.build();
const posts = await app.em.repo("posts").findMany();  // ✓
```

### Schema Sync Issues

**Symptoms:** Entity exists in code but not in database, or vice versa

**Diagnose:**
```bash
# Check admin panel -> Schema view
# Or query directly
curl http://localhost:3000/api/system/schema
```

**Solutions:**

1. **Restart server** - schema syncs on startup:
```bash
npx bknd run
```

2. **Force sync** (may drop data):
```typescript
options: {
  sync: {
    force: true,  // Dangerous! Can drop tables
  }
}
```

3. **Check mode** - Database Mode ignores code schema:
```typescript
// Code Mode (default) - schema from code
mode: "code"

// Hybrid Mode - merges code + database
mode: "hybrid"
```

### File Upload Failing

**Symptoms:** 413 error, upload silently fails

**Diagnose:**
```bash
# Check file size
ls -la myfile.jpg

# Test upload
curl -X POST http://localhost:3000/api/media/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@myfile.jpg"
```

**Solutions:**

1. **File too large:**
```typescript
media: {
  body_max_size: 10 * 1024 * 1024,  // 10MB
}
```

2. **Storage not configured:**
```typescript
media: {
  adapter: {
    type: "s3",
    // ... S3 config
  }
}
```

3. **Local storage (dev only):**
```typescript
import { registerLocalMediaAdapter } from "bknd/adapter/node";
const local = registerLocalMediaAdapter();

export default {
  app: {
    media: { adapter: local }
  }
}
```

### CORS Errors

**Symptoms:** "Access-Control-Allow-Origin" errors in browser console

**Diagnose:**
```bash
# Check CORS headers
curl -I http://localhost:3000/api/data/posts \
  -H "Origin: http://localhost:5173"
```

**Solutions:**
```typescript
export default {
  app: {
    server: {
      cors: {
        origin: ["http://localhost:5173", "https://myapp.com"],
        credentials: true,  // For cookies
      }
    }
  }
}
```

For development (allow all):
```typescript
server: {
  cors: {
    origin: "*",
  }
}
```

### Headless Environment Crash

**Symptoms:** `spawn xdg-open ENOENT` on server without display

**Solution:**
```bash
npx bknd run --no-open
```

### Windows ESM Errors

**Symptoms:** `ERR_UNSUPPORTED_ESM_URL_SCHEME` on Windows

**Solutions:**
1. Use Node.js 18+
2. Ensure `"type": "module"` in package.json
3. Use `.mjs` extension for config

### TypeScript Types Not Updating

**Symptoms:** IDE shows old types, autocomplete wrong

**Solutions:**
```bash
# Regenerate types
npx bknd types

# Restart TypeScript server (VS Code)
# Cmd/Ctrl + Shift + P -> "TypeScript: Restart TS Server"

# Clear cache
rm -rf node_modules/.cache
```

## Debug Script Pattern

Create a debug helper for systematic troubleshooting:

```typescript
// debug.ts
import { Api } from "bknd/client";

async function debug() {
  const api = new Api({ host: "http://localhost:3000" });

  // 1. Check server health
  console.log("=== Health Check ===");
  const entities = await fetch("http://localhost:3000/api/data");
  console.log("Status:", entities.status);
  console.log("Entities:", await entities.json());

  // 2. Check auth
  console.log("\n=== Auth Check ===");
  const me = await api.auth.me();
  console.log("Auth status:", me.ok ? "authenticated" : "not authenticated");
  if (me.data) console.log("User:", me.data);

  // 3. Check schema
  console.log("\n=== Schema Check ===");
  const schema = await fetch("http://localhost:3000/api/system/schema");
  console.log("Schema:", await schema.json());

  // 4. Test entity access
  console.log("\n=== Entity Access ===");
  const posts = await api.data.readMany("posts", { limit: 1 });
  console.log("Posts access:", posts.ok ? "success" : `failed (${posts.status})`);
}

debug().catch(console.error);
```

Run with:
```bash
npx tsx debug.ts
```

## Logging Patterns

### Server-Side Logging

```typescript
// In seed function or plugin
options: {
  seed: async (ctx) => {
    console.log("[SEED] Starting...");
    console.log("[SEED] Entities:", Object.keys(ctx.em.entities));

    try {
      await ctx.em.mutator("posts").insertOne({ title: "Test" });
      console.log("[SEED] Created post");
    } catch (e) {
      console.error("[SEED] Error:", e);
    }
  }
}
```

### API Response Logging

```typescript
const api = new Api({
  host: "http://localhost:3000",
  verbose: true,  // Logs all requests/responses
});

// Or manual logging
const result = await api.data.readMany("posts");
console.log("Request result:", {
  ok: result.ok,
  status: result.status,
  data: result.data,
  error: result.error,
});
```

### Custom Fetcher with Logging

```typescript
const api = new Api({
  host: "http://localhost:3000",
  fetcher: async (url, options) => {
    console.log("→", options?.method || "GET", url);
    const start = Date.now();
    const response = await fetch(url, options);
    console.log("←", response.status, `(${Date.now() - start}ms)`);
    return response;
  },
});
```

## Flow/Task Debugging

### HTTP Trigger Errors

Sync mode returns errors in response:
```json
{
  "success": false,
  "errors": [
    {
      "task": "fetchUser",
      "error": "Failed to fetch user: 404 Not Found",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Task Error Handling

```typescript
import { Task, Condition } from "bknd/flows";

const flow = new Flow("myFlow", [
  mainTask,
  errorTask.connect(mainTask, Condition.error()),  // Handle errors
]);
```

## Verification Checklist

When debugging, check these in order:

1. **Server running?**
   ```bash
   curl http://localhost:3000/api/data
   ```

2. **Config loaded?**
   - Check startup logs for "Using config from"

3. **Schema synced?**
   - Check admin panel or `/api/system/schema`

4. **Auth enabled?** (if needed)
   - Check `auth: { enabled: true }` in config

5. **Permissions set?** (if 403)
   - Check `guard: { enabled: true }` and roles

6. **CORS configured?** (if browser errors)
   - Check `server: { cors: {...} }`

## DOs and DON'Ts

**DO:**
- Check server logs first
- Use `npx bknd debug routes` for 404s
- Verify entity names match exactly (case-sensitive)
- Test with curl before debugging frontend
- Use `verbose: true` in Api for request logging
- Restart server after schema changes

**DON'T:**
- Assume `em()` returns a queryable EntityManager
- Forget `--no-open` on headless servers
- Use `:memory:` database for persistent data
- Skip checking HTTP status codes in responses
- Ignore CORS when debugging frontend issues
- Use `sync: { force: true }` in production

## Related Skills

- **bknd-local-setup** - Initial project setup
- **bknd-env-config** - Environment variables
- **bknd-setup-auth** - Authentication configuration
- **bknd-assign-permissions** - Permission troubleshooting
- **bknd-api-discovery** - Explore available endpoints
