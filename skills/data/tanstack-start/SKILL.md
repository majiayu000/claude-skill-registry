---
name: tanstack-start
description: |
  Build full-stack React apps with TanStack Start on Cloudflare Workers. Type-safe routing, server functions, SSR/streaming, D1/KV/R2 integration.

  Use when building full-stack React apps with SSR, migrating from Next.js, or from Vinxi to Vite (v1.121.0+). Prevents 9 documented errors including middleware bugs, file upload limitations, and deployment config issues.
user-invocable: true
allowed-tools: [Bash, Read, Write, Edit]
metadata:
  package: "@tanstack/react-start"
  version: "1.154.0"
  last_verified: "2026-01-21"
  repository: "https://github.com/TanStack/router"
  documentation: "https://tanstack.com/start/latest"
  error_count: 9
---

# TanStack Start Skill

⚠️ **Status: Production Ready (RC v1.154.0)**

TanStack Start is a full-stack React framework built on TanStack Router. It provides type-safe routing, server functions, SSR/streaming, and first-class Cloudflare Workers support.

**Current Package:** `@tanstack/react-start@1.154.0` (Jan 21, 2026)

**Production Readiness:**
- ✅ RC v1.154.0 stable (v1.0 expected soon)
- ✅ Memory leak issue (#5734) resolved Jan 5, 2026
- ✅ Migrated to Vite from Vinxi (v1.121.0, June 2025)
- ✅ Production deployments on Cloudflare Workers validated

This skill prevents **9 documented errors** and provides comprehensive guidance for Cloudflare Workers deployment, migrations, and server function patterns.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Migration from Vinxi to Vite](#migration-from-vinxi-to-vite-v1210)
- [Cloudflare Workers Deployment](#cloudflare-workers-deployment)
- [Server Functions](#server-functions)
- [Authentication Patterns](#authentication-patterns)
- [Database Integration](#database-integration)
- [Known Issues Prevention](#known-issues-prevention)
- [Performance Optimization](#performance-optimization)

---

## Quick Start

### Installation

```bash
# Create new project (uses Vite)
npm create cloudflare@latest my-app -- --framework=tanstack-start
cd my-app

# Install dependencies
npm install

# Development
npm run dev

# Build and deploy
npm run build
wrangler deploy
```

### Dependencies

```json
{
  "dependencies": {
    "@tanstack/react-start": "^1.154.0",
    "@tanstack/react-router": "latest",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "vite": "latest",
    "@cloudflare/vite-plugin": "latest",
    "wrangler": "latest"
  }
}
```

---

## Migration from Vinxi to Vite (v1.121.0+)

**Timeline**: TanStack Start migrated from Vinxi to Vite in v1.121.0 (released June 10, 2025).

### Breaking Changes

| Change | Old (Vinxi) | New (Vite) |
|--------|-------------|------------|
| Package name | `@tanstack/start` | `@tanstack/react-start` |
| Config file | `app.config.ts` | `vite.config.ts` |
| API routes | `createAPIFileRoute()` | `createServerFileRoute().methods()` |
| Entry files | `ssr.tsx`, `client.tsx` | `server.tsx` (optional) |
| Source folder | `app/` | `src/` |
| Dev command | `vinxi dev` | `vite dev` |

### Migration Steps

```bash
# 1. Remove Vinxi
npm uninstall vinxi @tanstack/start

# 2. Install Vite and framework-specific adapter
npm install vite @tanstack/react-start @cloudflare/vite-plugin

# 3. Delete old config
rm app.config.ts

# 4. Delete default entry files (unless customized)
rm app/ssr.tsx app/client.tsx

# 5. Rename customized entries
mv app/ssr.tsx app/server.tsx  # If you customized SSR entry

# 6. Move source files (optional, for consistency)
mv app/ src/
```

### Create vite.config.ts

```typescript
import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import { cloudflare } from '@cloudflare/vite-plugin'

export default defineConfig({
  plugins: [
    tanstackStart(),
    cloudflare({
      viteEnvironment: { name: 'ssr' } // Required for Workers
    })
  ]
})
```

### Update package.json Scripts

```json
{
  "scripts": {
    "dev": "vite dev --port 3000",
    "build": "vite build",
    "start": "node .output/server/index.mjs"
  }
}
```

### Update API Routes

```typescript
// Old (Vinxi)
import { createAPIFileRoute } from '@tanstack/start/api'

export const Route = createAPIFileRoute('/api/users')({
  GET: async () => {
    return { users: [] }
  }
})

// New (Vite)
import { createServerFileRoute } from '@tanstack/react-start/api'

export const Route = createServerFileRoute('/api/users').methods({
  GET: async () => {
    return { users: [] }
  }
})
```

### Common Migration Errors

**Error**: "invariant failed: could not find the nearest match"
**Cause**: Old Vinxi route definitions mixed with Vite config
**Fix**: Update all `createAPIFileRoute()` → `createServerFileRoute().methods()`

**Error**: "SyntaxError: The requested module '@tanstack/router-generator' does not provide an export named 'CONSTANTS'"
**Cause**: Conflicting Vinxi/Vite dependencies
**Fix**: Delete `node_modules/`, `package-lock.json`, reinstall

**Issue**: Auto-generated `app.config.timestamp_*` files duplicating
**Cause**: Old Vinxi config interfering
**Fix**: Delete all `app.config.*` files, restart dev server

**Reference**: [Official Migration Guide](https://github.com/TanStack/router/discussions/2863#discussioncomment-13104960) | [LogRocket Migration Article](https://blog.logrocket.com/migrating-tanstack-start-vinxi-vite/)

---

## Cloudflare Workers Deployment

### Required Configuration

#### wrangler.toml (or wrangler.jsonc)

```toml
name = "my-app"
compatibility_date = "2026-01-21"
compatibility_flags = ["nodejs_compat"] # REQUIRED

# REQUIRED: Point to TanStack Start's server entry
main = "@tanstack/react-start/server-entry"

[observability]
enabled = true # Optional: Enable monitoring
```

#### vite.config.ts

```typescript
import { defineConfig } from 'vite'
import { tanstackStart } from '@tanstack/react-start/plugin/vite'
import { cloudflare } from '@cloudflare/vite-plugin'

export default defineConfig({
  plugins: [
    tanstackStart(),
    cloudflare({
      viteEnvironment: { name: 'ssr' } // REQUIRED
    })
  ]
})
```

### Bindings (D1, KV, R2)

```toml
# D1 Database
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"

# KV Namespace
[[kv_namespaces]]
binding = "KV"
id = "your-kv-id"

# R2 Bucket
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"
```

Access bindings in server functions:

```typescript
import { createServerFn } from '@tanstack/react-start/server'

export const getUser = createServerFn()
  .handler(async ({ request }) => {
    const env = request.context.cloudflare.env

    // D1
    const result = await env.DB.prepare('SELECT * FROM users').all()

    // KV
    const value = await env.KV.get('key')

    // R2
    const object = await env.BUCKET.get('file.txt')

    return result.results
  })
```

### Prerendering Gotchas

**Critical**: Prerendering runs during build step using LOCAL environment variables, not Cloudflare bindings.

**Problem**: If routes use `loaders` that query D1/KV/R2, prerendering will fail because bindings aren't available at build time.

**Solutions**:

1. **Disable prerendering for routes with bindings**:

```typescript
export const Route = createFileRoute('/users')({
  loader: async () => {
    // This route queries D1
  },
  // Disable prerendering
  prerender: false
})
```

2. **Use remote bindings during builds** (requires `wrangler dev` running):

```bash
# In CI environment
export CLOUDFLARE_INCLUDE_PROCESS_ENV=true

# Use .env file (NOT .env.local) for CI
# .env.local is gitignored and won't be in CI
```

3. **Conditional logic in loaders**:

```typescript
loader: async ({ context }) => {
  // Skip DB queries during prerender
  if (typeof context.cloudflare === 'undefined') {
    return { users: [] }
  }

  const result = await context.cloudflare.env.DB.prepare('SELECT * FROM users').all()
  return { users: result.results }
}
```

**Version Requirements**:
- Static prerendering requires `@tanstack/react-start@1.138.0+`

**Reference**: [Cloudflare Workers Guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/)

---

## Server Functions

Server functions run on the server and can access Cloudflare bindings, databases, and secrets.

### Basic Server Function

```typescript
import { createServerFn } from '@tanstack/react-start/server'

export const getUsers = createServerFn()
  .handler(async ({ request }) => {
    const env = request.context.cloudflare.env
    const result = await env.DB.prepare('SELECT * FROM users').all()
    return result.results
  })
```

### Use in Components

```typescript
import { getUsers } from './server-functions'

function UserList() {
  const users = await getUsers()

  return (
    <ul>
      {users.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  )
}
```

### File Upload Limitation

⚠️ **Known Issue**: TanStack Start automatically calls `await request.formData()` for multipart/form-data requests, loading entire files into memory BEFORE the handler runs.

**Impact**:
- Cannot enforce upload size limits before loading
- Cannot implement streaming uploads
- Large file uploads consume excessive memory

**Example of the Problem**:

```typescript
export const uploadFile = createServerFn()
  .handler(async ({ request }) => {
    // By the time this runs, the entire file is already in memory
    const formData = await request.formData()
    const file = formData.get('file') as File

    // Too late to check size - file already loaded!
    if (file.size > 10_000_000) {
      throw new Error("File too large")
    }
  })
```

**Workarounds**:

1. **Client-side validation** (not foolproof, can be bypassed):

```typescript
function FileUpload() {
  const handleSubmit = async (e: FormEvent) => {
    const file = e.currentTarget.querySelector('input[type="file"]').files[0]

    if (file.size > 10_000_000) {
      alert("File too large")
      return
    }

    await uploadFile({ file })
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

2. **Use Cloudflare R2 multipart upload API directly** for large files (bypasses Start's form handling).

**Status**: [Open issue #5704](https://github.com/TanStack/router/issues/5704), no fix planned yet.

### Server Function Redirects Return Undefined

When a server function performs a redirect, the promise resolves to `undefined` instead of the declared return type.

```typescript
const login = createServerFn<{ username: string, password: string }, User>()
  .handler(async ({ data, request }) => {
    const user = await authenticateUser(data)

    if (!user) {
      // Redirect returns void, but type says it returns User
      throw redirect({ to: '/login', status: 401 })
    }

    return user
  })

// In component
const result = await login({ username, password })
// result is undefined if redirected, User object otherwise
// Check before using!
if (result) {
  console.log(result.name)
}
```

**Prevention**: Always check return value before use if server function can redirect.

**Status**: [Open PR #6295](https://github.com/TanStack/router/pull/6295) to fix return type.

---

## Authentication Patterns

### Stateful Backend Integration (Laravel Sanctum, etc.)

**Problem**: When using stateful backends, server functions lose auth context because requests originate from the Start server, not the browser. Cookies, CSRF tokens, and origin headers are missing.

```typescript
// This FAILS - cookies not forwarded
const getData = createServerFn()
  .handler(async () => {
    const response = await fetch('https://api.example.com/user')
    // 401 Unauthorized - no cookies!
  })
```

**Solution 1: Use createIsomorphicFn** (runs on client when possible)

```typescript
import { createIsomorphicFn } from '@tanstack/react-start/server'

const getData = createIsomorphicFn()
  .handler(async () => {
    // Runs on client when possible, preserving cookies
    const response = await fetch('https://api.example.com/user')
    return response.json()
  })
```

**Solution 2: Manual Header Forwarding**

```typescript
import { createServerFn } from '@tanstack/react-start/server'
import { getRequestHeaders } from '@tanstack/react-start/server'

const getData = createServerFn()
  .handler(async () => {
    const headers = getRequestHeaders() // Get browser's original headers

    const response = await fetch('https://api.example.com/user', {
      headers: {
        'Cookie': headers.get('cookie') || '',
        'X-XSRF-TOKEN': headers.get('x-xsrf-token') || '',
        'Origin': headers.get('origin') || '',
      }
    })

    return response.json()
  })
```

**When to Use Each**:
- `createIsomorphicFn`: Best for read operations, maintains full browser context
- Manual forwarding: Required for operations that must run server-side (secrets, DB access)

**Reference**: [GitHub Discussion #6289](https://github.com/TanStack/router/discussions/6289)

### Better Auth Integration

**Issue**: Better Auth cookie caching has edge cases with TanStack Start:
1. Session cookie not re-set after expiry
2. Session token cookie issues with certain plugins (`multiSession`, `lastLoginMethod`, `oneTap`)
3. Hard reload/direct URL doesn't read cookies (works with client navigation only)

**Solution**: Use Better Auth's official TanStack Start plugin

```typescript
import { betterAuth } from 'better-auth'
import { reactStartCookies } from 'better-auth/plugins'

export const auth = betterAuth({
  plugins: [
    reactStartCookies(), // Handles cookie setting for TanStack Start
  ],
  // ... other config
})
```

**Known Limitations**:
- Some edge cases remain with hard reloads
- Session cookie re-setting after expiry may not work consistently

**References**: [Issue #4389](https://github.com/better-auth/better-auth/issues/4389), [Issue #5639](https://github.com/better-auth/better-auth/issues/5639)

---

## Database Integration

### Prisma with Cloudflare Workers

**Issue**: Deploying with Prisma Edge fails with "No such module 'assets/.prisma/client/edge'" error.

**Solution**: Configure Prisma for Cloudflare runtime

```prisma
// prisma/schema.prisma
generator client {
  provider   = "prisma-client"
  output     = "../src/generated/prisma"
  engineType = "library"
  runtime    = "cloudflare" // or "workerd"
}
```

**Alternative Configuration**:

```prisma
generator client {
  provider = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

**Then use with Cloudflare Hyperdrive**:

```typescript
import { PrismaClient } from '@prisma/client'
import { PrismaPg } from '@prisma/adapter-pg'
import { Pool } from 'pg'

export const getUser = createServerFn()
  .handler(async ({ request }) => {
    const env = request.context.cloudflare.env

    const pool = new Pool({ connectionString: env.HYPERDRIVE.connectionString })
    const adapter = new PrismaPg(pool)
    const prisma = new PrismaClient({ adapter })

    return prisma.user.findMany()
  })
```

**Reference**: [Cloudflare Workers SDK Issue #10969](https://github.com/cloudflare/workers-sdk/issues/10969)

### D1 Database

```typescript
export const getUsers = createServerFn()
  .handler(async ({ request }) => {
    const env = request.context.cloudflare.env
    const result = await env.DB.prepare('SELECT * FROM users').all()
    return result.results
  })
```

Use with `drizzle-orm-d1` skill for type-safe ORM.

---

## Known Issues Prevention

This skill prevents **9** documented issues:

### Issue #1: Middleware Does Not Catch Server Function Errors

**Error**: Errors thrown by server functions bypass middleware try-catch blocks
**Source**: [GitHub Issue #6381](https://github.com/TanStack/router/issues/6381)
**Status**: Fixed in v1.155+ (expected release)

**Why It Happens**: Server function errors are returned as error objects in the response, not thrown directly.

**Prevention** (workaround for v1.154 and earlier):

```typescript
import { createMiddleware } from '@tanstack/react-start/server'

const middleware = createMiddleware().server(async (ctx) => {
  try {
    const r = await ctx.next()

    // Check for error in response object
    if ('error' in r && r.error) {
      throw r.error
    }

    return r
  } catch (error: any) {
    console.error("Middleware caught an error:", error)
    return new Response("An error occurred", { status: 500 })
  }
})
```

### Issue #2: File Upload Streaming Not Supported

**Error**: Large file uploads consume excessive memory
**Source**: [GitHub Issue #5704](https://github.com/TanStack/router/issues/5704)
**Status**: Open, no fix planned

**Why It Happens**: Framework automatically calls `await request.formData()` before handler runs, loading entire file into memory.

**Prevention**:
1. Implement client-side file size validation
2. Use Cloudflare R2 multipart upload API directly for large files
3. Set reasonable file size limits in upload UI

See [File Upload Limitation](#file-upload-limitation) section for details.

### Issue #3: Server Function Redirects Return Undefined

**Error**: Type errors when using server function result after redirect
**Source**: [GitHub PR #6295](https://github.com/TanStack/router/pull/6295)
**Status**: Open PR

**Why It Happens**: Redirects return void, but return type doesn't reflect this.

**Prevention**: Always check server function return value before use

```typescript
const result = await login({ username, password })

if (result) {
  // Safe to use result
  console.log(result.name)
}
```

### Issue #4: Stateful Auth Cookies Not Forwarded

**Error**: 401 Unauthorized when calling stateful backend APIs from server functions
**Source**: [GitHub Discussion #6289](https://github.com/TanStack/router/discussions/6289)

**Why It Happens**: Server functions originate from Start server, not browser, so cookies aren't forwarded.

**Prevention**: Use `createIsomorphicFn` or manual header forwarding

See [Stateful Backend Integration](#stateful-backend-integration-laravel-sanctum-etc) section.

### Issue #5: Prisma Edge Module Not Found

**Error**: "No such module 'assets/.prisma/client/edge'"
**Source**: [Cloudflare Workers SDK Issue #10969](https://github.com/cloudflare/workers-sdk/issues/10969)
**Status**: Resolved with runtime config

**Why It Happens**: Prisma Edge client not properly bundled for Workers environment.

**Prevention**: Configure Prisma with `runtime = "cloudflare"` in schema.prisma

See [Prisma with Cloudflare Workers](#prisma-with-cloudflare-workers) section.

### Issue #6: Better Auth Cookie Caching Issues

**Error**: Session cookies not set/refreshed properly
**Source**: [Better Auth Issues #4389, #5639](https://github.com/better-auth/better-auth/issues/4389)

**Why It Happens**: Better Auth's default cookie handling doesn't account for Start's execution model.

**Prevention**: Use `reactStartCookies()` plugin

See [Better Auth Integration](#better-auth-integration) section.

### Issue #7: Missing nodejs_compat Flag

**Error**: Runtime errors when using Node.js APIs on Cloudflare Workers
**Source**: [Cloudflare Workers Guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/)

**Why It Happens**: TanStack Start uses Node.js APIs that require compatibility flag.

**Prevention**: Add `compatibility_flags = ["nodejs_compat"]` to wrangler.toml

### Issue #8: Prerendering Fails with Cloudflare Bindings

**Error**: Build fails when routes with loaders use D1/KV/R2
**Source**: [Cloudflare Workers Guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/)

**Why It Happens**: Prerendering runs at build time without access to Cloudflare bindings.

**Prevention**: Disable prerendering for routes with bindings, or use conditional logic

See [Prerendering Gotchas](#prerendering-gotchas) section.

### Issue #9: Vinxi Migration Errors

**Error**: "invariant failed: could not find the nearest match" after upgrading to v1.121.0+
**Source**: [Release v1.121.0](https://github.com/TanStack/router/releases/tag/v1.121.0)

**Why It Happens**: v1.121.0 migrated from Vinxi to Vite with breaking changes.

**Prevention**: Follow complete migration guide

See [Migration from Vinxi to Vite](#migration-from-vinxi-to-vite-v1210) section.

---

## Performance Optimization

### Static Process.env Replacement

**Feature**: Build-time replacement of `process.env.NODE_ENV` for better optimization (v1.154.0+)

```typescript
// This condition is statically evaluated and dead code eliminated
if (process.env.NODE_ENV === 'production') {
  // Production-only code
} else {
  // Development-only code (removed in prod build)
}
```

**Automatic**: No configuration needed, works out of the box.

### Development Performance with Many Routes

**Issue**: Apps with 100+ routes generate 700+ HTTP requests in Vite dev mode.

**Why**: `routeTree.gen.ts` statically imports every route for type generation, even though `autoCodeSplitting` is enabled by default.

**Impact**: Slow dev server, hits proxy rate limits (ngrok 360 req/min)

**Status**: Expected behavior until Router v2. Not a bug, architectural limitation.

**Workarounds**:
- Use production builds for testing with many routes
- Reduce route count during development
- Use local tunneling without rate limits (Cloudflare Tunnel instead of ngrok)

**Reference**: [GitHub Discussion #6353](https://github.com/TanStack/router/discussions/6353)

---

## Additional Resources

**Official Documentation**:
- [TanStack Start Docs](https://tanstack.com/start/latest)
- [Cloudflare Workers Guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/)
- [TanStack Router Docs](https://tanstack.com/router/latest)

**Migration Guides**:
- [Official Vinxi→Vite Migration](https://github.com/TanStack/router/discussions/2863#discussioncomment-13104960)
- [LogRocket Migration Article](https://blog.logrocket.com/migrating-tanstack-start-vinxi-vite/)

**Related Skills**:
- `cloudflare-worker-base` - Cloudflare Workers deployment patterns
- `drizzle-orm-d1` - Type-safe D1 database access
- `ai-sdk-core` - AI integration with server functions
- `react-hook-form-zod` - Form handling with validation

---

**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Expanded from draft with 9 documented issues, migration guide, Cloudflare deployment, auth patterns, and database integration
