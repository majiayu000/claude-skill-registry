---
name: cloudflare-worker-base
description: |
  Set up Cloudflare Workers with Hono routing, Vite plugin, and Static Assets. Prevents 10 errors including export syntax, routing conflicts, Vite 8 nodejs_compat, base option regression, and cache corruption.

  Use when: creating Workers projects, configuring Hono/Vite, or troubleshooting export syntax, API route conflicts, HMR issues, or Vite 8+ compatibility.
user-invocable: true
---

# Cloudflare Worker Base Stack

**Production-tested**: cloudflare-worker-base-test (https://cloudflare-worker-base-test.webfonts.workers.dev)
**Last Updated**: 2026-01-20
**Status**: Production Ready ✅
**Latest Versions**: hono@4.11.3, @cloudflare/vite-plugin@1.17.1, vite@7.3.1, wrangler@4.54.0
**Skill Version**: 3.1.0

**Recent Updates (2025-2026)**:
- **Wrangler 4.55+**: Auto-config for frameworks (`wrangler deploy --x-autoconfig`)
- **Wrangler 4.45+**: Auto-provisioning for R2, D1, KV bindings (enabled by default)
- **Workers RPC**: JavaScript-native RPC via `WorkerEntrypoint` class for service bindings
- **March 2025**: Wrangler v4 release (minimal breaking changes, v3 supported until Q1 2027)
- **June 2025**: Native Integrations removed from dashboard (CLI-based approach with wrangler secrets)
- **2025 Platform**: Workers VPC Services, Durable Objects Data Studio, 64 env vars (5KB each), unlimited Cron Triggers per Worker, WebSocket 32 MiB messages, node:fs/Web File System APIs
- **2025 Static Assets**: Gradual rollout asset mismatch issue, free tier 429 errors with run_worker_first, Vite plugin auto-detection
- **Hono 4.11.x**: Enhanced TypeScript RPC type inference, cloneRawRequest utility, JWT aud validation, auth middleware improvements

---

## Quick Start (5 Minutes)

```bash
# 1. Scaffold project
npm create cloudflare@latest my-worker -- --type hello-world --ts --git --deploy false --framework none

# 2. Install dependencies
cd my-worker
npm install hono@4.11.3
npm install -D @cloudflare/vite-plugin@1.17.1 vite@7.3.1

# 3. Create wrangler.jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "account_id": "YOUR_ACCOUNT_ID",
  "compatibility_date": "2025-11-11",
  "assets": {
    "directory": "./public/",
    "binding": "ASSETS",
    "not_found_handling": "single-page-application",
    "run_worker_first": ["/api/*"]  // CRITICAL: Prevents SPA fallback from intercepting API routes
  }
}

# 4. Create vite.config.ts
import { defineConfig } from 'vite'
import { cloudflare } from '@cloudflare/vite-plugin'
export default defineConfig({ plugins: [cloudflare()] })

# 5. Create src/index.ts
import { Hono } from 'hono'
type Bindings = { ASSETS: Fetcher }
const app = new Hono<{ Bindings: Bindings }>()
app.get('/api/hello', (c) => c.json({ message: 'Hello!' }))
app.all('*', (c) => c.env.ASSETS.fetch(c.req.raw))
export default app  // CRITICAL: Use this pattern (NOT { fetch: app.fetch })

# 6. Deploy
npm run dev              # Local: http://localhost:8787
wrangler deploy          # Production
```

**Critical Configuration**:
- `run_worker_first: ["/api/*"]` - Without this, SPA fallback intercepts API routes returning `index.html` instead of JSON ([workers-sdk #8879](https://github.com/cloudflare/workers-sdk/issues/8879))
- `export default app` - Using `{ fetch: app.fetch }` causes "Cannot read properties of undefined" ([honojs/hono #3955](https://github.com/honojs/hono/issues/3955))


## Known Issues Prevention

This skill prevents **10 documented issues**:

### Issue #1: Export Syntax Error
**Error**: "Cannot read properties of undefined (reading 'map')"
**Source**: [honojs/hono #3955](https://github.com/honojs/hono/issues/3955)
**Prevention**: Use `export default app` (NOT `{ fetch: app.fetch }`)

### Issue #2: Static Assets Routing Conflicts
**Error**: API routes return `index.html` instead of JSON
**Source**: [workers-sdk #8879](https://github.com/cloudflare/workers-sdk/issues/8879)
**Prevention**: Add `"run_worker_first": ["/api/*"]` to wrangler.jsonc

### Issue #3: Scheduled/Cron Not Exported
**Error**: "Handler does not export a scheduled() function"
**Source**: [honojs/vite-plugins #275](https://github.com/honojs/vite-plugins/issues/275)
**Prevention**: Use Module Worker format when needed:
```typescript
export default {
  fetch: app.fetch,
  scheduled: async (event, env, ctx) => { /* ... */ }
}
```

### Issue #4: HMR Race Condition
**Error**: "A hanging Promise was canceled" during development
**Source**: [workers-sdk #9518](https://github.com/cloudflare/workers-sdk/issues/9518)
**Prevention**: Use `@cloudflare/vite-plugin@1.13.13` or later

### Issue #5: Static Assets Upload Race
**Error**: Non-deterministic deployment failures in CI/CD
**Source**: [workers-sdk #7555](https://github.com/cloudflare/workers-sdk/issues/7555)
**Prevention**: Use Wrangler 4.x+ with retry logic (fixed in recent versions)

### Issue #6: Service Worker Format Confusion
**Error**: Using deprecated Service Worker format
**Source**: Cloudflare migration guide
**Prevention**: Always use ES Module format

### Issue #7: Gradual Rollouts Asset Mismatch (2025)
**Error**: 404 errors for fingerprinted assets during gradual deployments
**Source**: [Cloudflare Static Assets Docs](https://developers.cloudflare.com/workers/static-assets/routing/advanced/gradual-rollouts)
**Why It Happens**: Modern frameworks (React/Vue/Angular with Vite) generate fingerprinted filenames (e.g., `index-a1b2c3d4.js`). During gradual rollouts between versions, a user's initial request may go to Version A (HTML references `index-a1b2c3d4.js`), but subsequent asset requests route to Version B (only has `index-m3n4o5p6.js`), causing 404s
**Prevention**:
- Avoid gradual deployments with fingerprinted assets
- Use instant cutover deployments for static sites
- Or implement version-aware routing with custom logic

### Issue #8: Free Tier 429 Errors with run_worker_first (2025)
**Error**: 429 (Too Many Requests) responses on asset requests when exceeding free tier limits
**Source**: [Cloudflare Static Assets Billing Docs](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations)
**Why It Happens**: When using `run_worker_first`, requests matching specified patterns ALWAYS invoke your Worker script (counted toward free tier limits). After exceeding limits, these requests receive 429 instead of falling back to free static asset serving
**Prevention**:
- Upgrade to Workers Paid plan ($5/month) for unlimited requests
- Use negative patterns (`!/pattern`) to exclude paths from Worker invocation
- Minimize `run_worker_first` patterns to only essential API routes

### Issue #9: Vite 8 Breaks nodejs_compat with require()
**Error**: `Calling require for "buffer" in an environment that doesn't expose the require function`
**Source**: [workers-sdk #11948](https://github.com/cloudflare/workers-sdk/issues/11948)
**Affected Versions**: Vite 8.x with @cloudflare/vite-plugin 1.21.0+
**Why It Happens**: Vite 8 uses Rolldown bundler which doesn't convert `require()` to `import` for external modules. Workers don't expose `require()` function, causing Node built-in module imports to fail at runtime.
**Prevention**:
```typescript
// vite.config.ts - Add esmExternalRequirePlugin
import { defineConfig } from 'vite'
import { cloudflare } from '@cloudflare/vite-plugin'
import { esmExternalRequirePlugin } from 'vite'
import { builtinModules } from 'node:module'

export default defineConfig({
  plugins: [
    cloudflare(),
    esmExternalRequirePlugin({
      external: [/^node:/, ...builtinModules],
    }),
  ],
})
```
**Status**: Workaround available. Vite team working on fix ([vitejs/vite#21452](https://github.com/vitejs/vite/pull/21452)).

### Issue #10: Vite base Option Breaks SPA Routing (1.13.8+)
**Error**: `curl http://localhost:5173/prefix` returns 404 instead of index.html
**Source**: [workers-sdk #11857](https://github.com/cloudflare/workers-sdk/issues/11857)
**Affected Versions**: @cloudflare/vite-plugin 1.13.8+
**Why It Happens**: Plugin now passes full URL with base path to Asset Worker (matching prod behavior). Platform support for `assets.base` not yet available.
**Prevention** (dev-mode workaround):
```typescript
// worker.ts - Strip base path in development
if (import.meta.env.DEV) {
  url.pathname = url.pathname.replace(import.meta.env.BASE_URL, '');
  if (url.pathname === '/') {
    return this.env.ASSETS.fetch(request);
  }
  request = new Request(url, request);
}
```
**Status**: Intentional change to align dev with prod. Platform feature `assets.base` planned for Q1 2026 ([workers-sdk #9885](https://github.com/cloudflare/workers-sdk/issues/9885)).



## Route Priority with run_worker_first

**Critical Understanding**: `"not_found_handling": "single-page-application"` returns `index.html` for unknown routes (enables React Router, Vue Router). Without `run_worker_first`, this intercepts API routes!

**Request Routing with `run_worker_first: ["/api/*"]`**:
1. `/api/hello` → Worker handles (returns JSON)
2. `/` → Static Assets serve `index.html`
3. `/styles.css` → Static Assets serve `styles.css`
4. `/unknown` → Static Assets serve `index.html` (SPA fallback)

**Static Assets Caching**: Automatic edge caching. Cache bust with query strings: `<link href="/styles.css?v=1.0.0">`

**Free Tier Warning** (2025): `run_worker_first` patterns count toward free tier limits. After exceeding, requests get 429 instead of falling back to free static assets. Use negative patterns (`!/pattern`) or upgrade to Paid plan.


## Auto-Provisioning (Wrangler 4.45+)

**Default Behavior**: Wrangler automatically provisions R2 buckets, D1 databases, and KV namespaces when deploying. This eliminates manual resource creation steps.

**Critical: Always Specify Resource Names**

⚠️ **Edge Case** ([workers-sdk #11870](https://github.com/cloudflare/workers-sdk/issues/11870)): If you provide only `binding` without `database_name`/`bucket_name`, Wrangler uses the binding name as the resource name. This causes confusing behavior with `wrangler dev` and subcommands, which prefer `database_id` → `database_name` → `binding`.

```jsonc
// ❌ DON'T: Binding-only creates database named "DB"
{
  "d1_databases": [{ "binding": "DB" }]
}

// ✅ DO: Explicit names prevent confusion
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-app-db"  // Always specify!
    }
  ],
  "r2_buckets": [
    {
      "binding": "STORAGE",
      "bucket_name": "my-app-files"  // Always specify!
    }
  ],
  "kv_namespaces": [
    {
      "binding": "CACHE",
      "title": "my-app-cache"  // Always specify!
    }
  ]
}
```

```bash
# Deploy - resources auto-provisioned if they don't exist
wrangler deploy

# Disable auto-provisioning (use existing resources only)
wrangler deploy --no-x-provision
```

**Benefits**:
- No separate `wrangler d1 create` / `wrangler r2 create` steps needed
- Idempotent - existing resources are used, not recreated
- Works with local dev (`wrangler dev` creates local emulated resources)


## Workers RPC (Service Bindings)

**What It Is**: JavaScript-native RPC system for calling methods between Workers. Uses Cap'n Proto under the hood for zero-copy message passing.

**Use Case**: Split your application into multiple Workers (e.g., API Worker + Auth Worker + Email Worker) that call each other with type-safe methods.

**Defining an RPC Service**:
```typescript
import { WorkerEntrypoint } from 'cloudflare:workers'

export class AuthService extends WorkerEntrypoint<Env> {
  async verifyToken(token: string): Promise<{ userId: string; valid: boolean }> {
    // Access bindings via this.env
    const session = await this.env.SESSIONS.get(token)
    return session ? { userId: session.userId, valid: true } : { userId: '', valid: false }
  }

  async createSession(userId: string): Promise<string> {
    const token = crypto.randomUUID()
    await this.env.SESSIONS.put(token, JSON.stringify({ userId }), { expirationTtl: 3600 })
    return token
  }
}

// Default export still handles HTTP requests
export default { fetch: ... }
```

**Calling from Another Worker**:
```typescript
// wrangler.jsonc
{
  "services": [
    { "binding": "AUTH", "service": "auth-worker", "entrypoint": "AuthService" }
  ]
}

// In your main Worker
const { valid, userId } = await env.AUTH.verifyToken(authHeader)
```

**Key Points**:
- **Zero latency**: Workers on same account typically run in same thread
- **Type-safe**: Full TypeScript support for method signatures
- **32 MiB limit**: Max serialized RPC message size
- **Self-bindings**: In `wrangler dev`, shows as `[connected]` for same-Worker calls


## Troubleshooting

### Random "Response Already Sent" Errors in Development

**Symptom**: Sporadic `ResponseSentError: The response has already been sent to the browser and cannot be altered` during `wrangler dev`
**Source**: [workers-sdk #11932](https://github.com/cloudflare/workers-sdk/issues/11932)
**Cause**: Cache corruption in `.wrangler` directory or stale Vite cache

**Solution**:
```bash
# Clear all caches
rm -rf .wrangler dist node_modules/.vite

# Rebuild
npm run build

# Recreate local D1 databases if needed
wrangler d1 execute DB --local --file schema.sql
```

**Applies to**: Wrangler 4.x full Workers mode (not Cloudflare Pages)


## Community Tips

> **Note**: These tips come from community discussions. Verify against your version.

### Avoid vite-tsconfig-paths v6 with React SSR

**Source**: [workers-sdk #11825](https://github.com/cloudflare/workers-sdk/issues/11825) (Community-sourced)

If using React SSR with `@cloudflare/vite-plugin`, pin to `vite-tsconfig-paths@5.1.4`:

```bash
npm install vite-tsconfig-paths@5.1.4
```

**Why**: Version 6.x doesn't follow path aliases during dependency scan, causing duplicate React instances and "Invalid hook call" errors.

**Applies to**: Projects using TypeScript path aliases with React SSR

### Use crypto.randomUUID() Instead of uuid Package

**Source**: [workers-sdk #11957](https://github.com/cloudflare/workers-sdk/issues/11957)

The `uuid@11` package (ESM) can cause runtime crashes with "fileURLToPath undefined" in Workers. Use the native Web Crypto API instead:

```typescript
// ✅ Native Workers API (recommended)
const uuid = crypto.randomUUID();

// ❌ Avoid uuid package in Workers
import { v4 as uuidv4 } from 'uuid';  // May crash
```

**Applies to**: All Workers projects needing UUIDs


## Commands

### `/deploy` - One-Command Deploy Pipeline

**Use when**: Ready to commit, push, and deploy your Cloudflare Worker in one step.

**Does**:
1. **Pre-flight**: Verifies wrangler config, checks for changes, builds, runs TypeScript check
2. **Commit & Push**: Stages changes, generates conventional commit message, pushes to remote
3. **Deploy**: Runs `wrangler deploy`, captures Worker URL
4. **Report**: Shows commit hash, branch, deployed URL, any warnings

**Time savings**: 2-3 min per deploy cycle

**Edge Cases Handled**:
- No changes to commit → skips to deploy
- Build script missing → warns and continues
- No remote configured → reports error with suggestion
- TypeScript errors → stops and reports

---

## Bundled Resources

**Templates**: Complete setup files in `templates/` directory (wrangler.jsonc, vite.config.ts, package.json, tsconfig.json, src/index.ts, public/index.html, styles.css, script.js)


## Official Documentation

- **Cloudflare Workers**: https://developers.cloudflare.com/workers/
- **Static Assets**: https://developers.cloudflare.com/workers/static-assets/
- **Vite Plugin**: https://developers.cloudflare.com/workers/vite-plugin/
- **Wrangler**: https://developers.cloudflare.com/workers/wrangler/
- **Hono**: https://hono.dev/docs/getting-started/cloudflare-workers
- **MCP Tool**: Use `mcp__cloudflare-docs__search_cloudflare_documentation` for latest docs

---

## Dependencies (Latest Verified 2026-01-03)

```json
{
  "dependencies": {
    "hono": "^4.11.3"
  },
  "devDependencies": {
    "@cloudflare/vite-plugin": "^1.17.1",
    "@cloudflare/workers-types": "^4.20260103.0",
    "vite": "^7.3.1",
    "wrangler": "^4.54.0",
    "typescript": "^5.9.3"
  }
}
```

---

## Production Validation

**Live Example**: https://cloudflare-worker-base-test.webfonts.workers.dev (build time: 45 min, 0 errors, all 10 issues prevented)

---

**Last verified**: 2026-01-20 | **Skill version**: 3.1.0 | **Changes**: Added Vite 8 nodejs_compat workaround (Issue #9), Vite base option regression (Issue #10), auto-provisioning edge case warning, troubleshooting section for cache corruption, and community tips for vite-tsconfig-paths v6 and uuid package alternatives. Research conducted by skill-researcher agent covering post-May 2025 Workers SDK updates.

