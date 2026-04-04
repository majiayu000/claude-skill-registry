---
name: cloudflare-nextjs
description: Deploy Next.js to Cloudflare Workers via OpenNext adapter. Use for SSR, ISR, App/Pages Router, or encountering worker size limits, runtime compatibility, connection scoping errors.

  Keywords: Cloudflare Next.js, OpenNext Cloudflare, @opennextjs/cloudflare, Next.js Workers, Next.js App Router Cloudflare, Next.js Pages Router Cloudflare, Next.js SSR Cloudflare, Next.js ISR, server components cloudflare, server actions cloudflare, Next.js middleware workers, nextjs d1, nextjs r2, nextjs kv, Next.js deployment, opennextjs-cloudflare cli, nodejs_compat, worker size limit, next.js runtime compatibility, database connection scoping, Next.js migration cloudflare
license: MIT
metadata:
  version: 1.0.0
  last_verified: 2025-11-21
  package_versions:
    "@opennextjs/cloudflare": "^1.13.1"
    "next": "^14.2.0 || ^15.0.0 || ^16.0.0"
    "wrangler": "^4.50.0"
  compatibility_requirements:
    compatibility_date: "2025-05-05"
    compatibility_flags: ["nodejs_compat"]
  token_savings: "~59%"
  errors_prevented: 10
  official_docs: "https://opennext.js.org/cloudflare"
  cloudflare_guide: "https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/"
---

# Cloudflare Next.js Deployment Skill

Deploy Next.js applications to Cloudflare Workers using the OpenNext Cloudflare adapter for production-ready serverless Next.js hosting.

## When to Load References

Load additional reference files based on your specific task:

- **`references/error-catalog-extended.md`** - Load when encountering ANY error during setup, build, or deployment. Contains complete catalog of 11+ documented issues with root causes, solutions, and official sources.

- **`references/service-integration-patterns.md`** - Load when integrating Cloudflare services (D1, R2, KV, Workers AI) with Next.js. Contains complete patterns for database queries, file uploads, caching, and AI inference.

- **`references/troubleshooting.md`** - Load for general troubleshooting and debugging guidance beyond the error catalog.

- **`references/feature-support.md`** - Load when checking if a specific Next.js feature is supported on Cloudflare Workers (e.g., "Can I use Server Actions?", "Does ISR work?").

- **`references/database-client-example.ts`** - Load when integrating external database clients (Drizzle, Prisma, PostgreSQL, MySQL) with proper request-scoping patterns required by Workers.

- **`references/open-next.config.ts`** - Load when configuring caching behavior, image optimization, or custom OpenNext settings.

- **`references/package.json`** - Load when setting up a new project or migrating an existing Next.js application to Cloudflare Workers.

- **`references/wrangler.jsonc`** - Load when configuring Worker settings, compatibility flags, environment bindings (D1, R2, KV, AI), or deployment options.

## Use This Skill When

- Deploying Next.js applications (App Router or Pages Router) to Cloudflare Workers
- Need server-side rendering (SSR), static site generation (SSG), or incremental static regeneration (ISR) on Cloudflare
- Migrating existing Next.js apps from Vercel, AWS, or other platforms to Cloudflare
- Building full-stack Next.js applications with Cloudflare services (D1, R2, KV, Workers AI)
- Need React Server Components, Server Actions, or Next.js middleware on Workers
- Want global edge deployment with Cloudflare's network

## Key Differences from Standard Next.js

**OpenNext Adapter** transforms Next.js builds for Workers. **Critical requirements**:
- Node.js runtime (NOT Edge) via `nodejs_compat` flag
- Request-scoped database clients (global clients fail)
- Worker size limits: 3 MiB (free) / 10 MiB (paid)
- Dual testing: `next dev` for speed, `preview` for production-like validation

## Setup Patterns

### New Project Setup

Use Cloudflare's `create-cloudflare` (C3) CLI to scaffold a new Next.js project pre-configured for Workers:

```bash
npm create cloudflare@latest -- my-next-app --framework=next
```

**What this does**:
1. Runs Next.js official setup tool (`create-next-app`)
2. Installs `@opennextjs/cloudflare` adapter
3. Creates `wrangler.jsonc` with correct configuration
4. Creates `open-next.config.ts` for caching configuration
5. Adds deployment scripts to `package.json`
6. Optionally deploys immediately to Cloudflare

**Development workflow**:
```bash
npm run dev      # Next.js dev server (fast reloads)
npm run preview  # Test in workerd runtime (production-like)
npm run deploy   # Build and deploy to Cloudflare
```

### Existing Project Migration

To add the OpenNext adapter to an existing Next.js application:

#### 1. Install the adapter

```bash
bun add -d @opennextjs/cloudflare
```

#### 2. Create wrangler.jsonc

```jsonc
{
  "name": "my-next-app",
  "compatibility_date": "2025-05-05",
  "compatibility_flags": ["nodejs_compat"]
}
```

**Critical configuration**:
- `compatibility_date`: **Minimum `2025-05-05`** (for FinalizationRegistry support)
- `compatibility_flags`: **Must include `nodejs_compat`** (for Node.js runtime)

#### 3. Create open-next.config.ts

```typescript
import { defineCloudflareConfig } from "@opennextjs/cloudflare";

export default defineCloudflareConfig({
  // Caching configuration (optional)
  // See: https://opennext.js.org/cloudflare/caching
});
```

#### 4. Update package.json scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "preview": "opennextjs-cloudflare build && opennextjs-cloudflare preview",
    "deploy": "opennextjs-cloudflare build && opennextjs-cloudflare deploy",
    "cf-typegen": "wrangler types --env-interface CloudflareEnv cloudflare-env.d.ts"
  }
}
```

**Script purposes**:
- `dev`: Next.js development server (fast iteration)
- `preview`: Build + run in workerd runtime (test before deploy)
- `deploy`: Build + deploy to Cloudflare
- `cf-typegen`: Generate TypeScript types for Cloudflare bindings

#### 5. Ensure Node.js runtime (not Edge)

Remove Edge runtime exports from your app:

```typescript
// ❌ REMOVE THIS (Edge runtime not supported)
export const runtime = "edge";

// ✅ Use Node.js runtime (default)
// No export needed - Node.js is default
```

## Development Workflow

**Dual Testing Required**:
- `npm run dev` - Fast iteration (Next.js dev server)
- `npm run preview` - Production-like testing (workerd runtime, **REQUIRED before deploy**)
- `npm run deploy` - Build and deploy

**Critical**: Always test `preview` before deploying to catch Workers-specific runtime issues

## Critical Configuration

**wrangler.jsonc** minimum requirements:
```jsonc
{
  "compatibility_date": "2025-05-05",  // Minimum for FinalizationRegistry
  "compatibility_flags": ["nodejs_compat"]  // Required for Node.js runtime
}
```

**Cloudflare Bindings**: Add D1, R2, KV, or AI bindings in `wrangler.jsonc`, access via `process.env` (see "Cloudflare Services Integration" section for complete patterns)

**Package Exports** (if needed): Create `.env` with `WRANGLER_BUILD_PLATFORM="node"` to prioritize Node.js exports

## Top 5 Critical Errors

These are the most common deployment-blocking errors. **For the complete catalog of 11+ errors, load `references/error-catalog-extended.md`**.

### 1. Worker Size Limit Exceeded

**Error**: `"Your Worker exceeded the size limit of 3 MiB"` (Free) or `"10 MiB"` (Paid)

**Quick Fix**: Upgrade plan, analyze bundle with `bunx opennextjs-cloudflare build` → check `.open-next/server-functions/default/handler.mjs.meta.json`, remove unused dependencies, or use dynamic imports.

**Source**: https://opennext.js.org/cloudflare/troubleshooting#worker-size-limits

---

### 2. Cannot Perform I/O on Behalf of Different Request

**Error**: `"Cannot perform I/O on behalf of a different request"`

**Cause**: Global database client reused across requests (Workers limitation)

**Quick Fix**: Create database clients INSIDE request handlers, never globally. Or use Cloudflare D1 which is designed for Workers.

```typescript
// ❌ WRONG: Global client
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// ✅ CORRECT: Request-scoped
export async function GET() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  // ... use pool
  await pool.end();
}
```

**Source**: https://opennext.js.org/cloudflare/troubleshooting#cannot-perform-io-on-behalf-of-a-different-request

---

### 3. NPM Package Import Failures

**Error**: `"Could not resolve '<package>'"`

**Quick Fix**: Enable `nodejs_compat` flag in wrangler.jsonc, and/or create `.env` with `WRANGLER_BUILD_PLATFORM="node"`.

**Source**: https://opennext.js.org/cloudflare/troubleshooting#npm-packages-fail-to-import

---

### 4. SSRF Vulnerability (CVE-2025-6087)

**Vulnerability**: Server-Side Request Forgery via `/_next/image` endpoint in versions < 1.3.0

**Quick Fix**: Upgrade immediately: `bun add -d @opennextjs/cloudflare@^1.3.0`

**Source**: https://github.com/advisories/GHSA-rvpw-p7vw-wj3m

---

### 5. Failed to Load Chunk (Turbopack)

**Error**: `"Failed to load chunk server/chunks/ssr/"`

**Quick Fix**: Remove `--turbo` flag from build command. Use `next build` (standard), NOT `next build --turbo`.

**Source**: https://opennext.js.org/cloudflare/troubleshooting#failed-to-load-chunk

---

**More Errors**: Load `references/error-catalog-extended.md` for 6 additional documented errors including FinalizationRegistry issues, Durable Objects warnings, Prisma conflicts, cross-fetch errors, and Windows development issues

## Feature Support Matrix

| Feature | Status | Notes |
|---------|--------|-------|
| **App Router** | ✅ Fully Supported | Latest App Router features work |
| **Pages Router** | ✅ Fully Supported | Legacy Pages Router supported |
| **Route Handlers** | ✅ Fully Supported | API routes work as expected |
| **React Server Components** | ✅ Fully Supported | RSC fully functional |
| **Server Actions** | ✅ Fully Supported | Server Actions work |
| **SSG** | ✅ Fully Supported | Static Site Generation |
| **SSR** | ✅ Fully Supported | Server-Side Rendering |
| **ISR** | ✅ Fully Supported | Incremental Static Regeneration |
| **Middleware** | ✅ Supported | Except Node.js middleware (15.2+) |
| **Image Optimization** | ✅ Supported | Via Cloudflare Images |
| **Partial Prerendering (PPR)** | ✅ Supported | Experimental in Next.js |
| **Composable Caching** | ✅ Supported | `'use cache'` directive |
| **Response Streaming** | ✅ Supported | Streaming responses work |
| **`next/after` API** | ✅ Supported | Post-response async work |
| **Node.js Middleware (15.2+)** | ❌ Not Supported | Future support planned |
| **Edge Runtime** | ❌ Not Supported | Use Node.js runtime |

**Source**: https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/#next-js-supported-features

## Cloudflare Services Integration

Access Cloudflare bindings via `process.env` in Next.js route handlers:

```typescript
import type { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const env = process.env as any;

  // D1 Database
  const users = await env.DB.prepare('SELECT * FROM users').all();

  // R2 Storage
  const file = await env.BUCKET.get('file.txt');

  // KV Storage
  const value = await env.KV.get('key');

  // Workers AI
  const ai = await env.AI.run('@cf/meta/llama-3-8b-instruct', { prompt: 'Hello' });

  return Response.json({ users, file, value, ai });
}
```

**Wrangler Bindings Configuration**:
```jsonc
{
  "d1_databases": [{ "binding": "DB", "database_id": "..." }],
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "..." }],
  "kv_namespaces": [{ "binding": "KV", "id": "..." }],
  "ai": { "binding": "AI" }
}
```

**Detailed Integration Patterns**: Load `references/service-integration-patterns.md` for complete patterns including:
- D1: Queries, inserts, transactions, batch operations
- R2: Upload, download, list, delete with streaming
- KV: Get, set with TTL, delete, list keys
- Workers AI: Text generation, embeddings, image classification
- Multi-service integration examples
- TypeScript types for bindings (`npm run cf-typegen`)

**Related Skills**: `cloudflare-d1`, `cloudflare-r2`, `cloudflare-kv`, `cloudflare-workers-ai` for service-specific deep dives

## Image Optimization & Caching

**Images**: Automatic optimization via Cloudflare Images (billed separately). Configure in `open-next.config.ts` with `imageOptimization: { loader: 'cloudflare' }`. Use standard Next.js `<Image />` component.

**Caching**: OpenNext provides sensible defaults. Override in `open-next.config.ts` if needed. See https://opennext.js.org/cloudflare/caching for advanced configuration

## Known Limitations

### Not Yet Supported

1. **Node.js Middleware (Next.js 15.2+)**
   - Introduced in Next.js 15.2
   - Support planned for future releases
   - Use standard middleware for now

2. **Edge Runtime**
   - Only Node.js runtime supported
   - Remove `export const runtime = "edge"` from your app

3. **Full Windows Support**
   - Development on Windows not fully guaranteed
   - Use WSL, VM, or Linux-based CI/CD

### Worker Size Constraints

- **Free plan**: 3 MiB limit (gzip-compressed)
- **Paid plan**: 10 MiB limit (gzip-compressed)
- Monitor bundle size during development
- Use dynamic imports for code splitting

### Database Connections

- External database clients (PostgreSQL, MySQL) must be request-scoped
- Cannot reuse connections across requests (Workers limitation)
- Prefer Cloudflare D1 for database needs (designed for Workers)

## Deployment

**Local**: `npm run deploy` (builds and deploys)

**CI/CD**: Use `npm run deploy` command in GitHub Actions, GitLab CI, or Cloudflare Workers Builds (auto-detected)

**Custom Domains**: Workers & Pages → Settings → Domains & Routes (domain must be on Cloudflare)

## TypeScript & Testing

**TypeScript Types**: Run `npm run cf-typegen` to generate `cloudflare-env.d.ts` with typed bindings (D1Database, R2Bucket, KVNamespace, Ai)

**Testing**: Always test in `preview` mode before deployment to catch Workers-specific runtime issues and verify bindings work correctly

## Migration from Other Platforms

### From Vercel

1. Copy existing Next.js project
2. Run existing project migration steps (above)
3. Update environment variables in Cloudflare dashboard
4. Replace Vercel-specific features:
   - Vercel Postgres → Cloudflare D1
   - Vercel Blob → Cloudflare R2
   - Vercel KV → Cloudflare KV
   - Vercel Edge Config → Cloudflare KV
5. Test thoroughly with `npm run preview`
6. Deploy with `npm run deploy`

### From AWS / Other Platforms

Same process as Vercel migration - the adapter handles Next.js standard features automatically.

## Resources

### Official Documentation
- **OpenNext Cloudflare**: https://opennext.js.org/cloudflare
- **Cloudflare Next.js Guide**: https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/
- **Next.js Docs**: https://nextjs.org/docs

### Troubleshooting
- **Troubleshooting Guide**: https://opennext.js.org/cloudflare/troubleshooting
- **Known Issues**: https://opennext.js.org/cloudflare/known-issues
- **GitHub Issues**: https://github.com/opennextjs/opennextjs-cloudflare/issues

### Related Skills
- `cloudflare-worker-base` - Base Worker setup with Hono + Vite + React
- `cloudflare-d1` - D1 database integration
- `cloudflare-r2` - R2 object storage
- `cloudflare-kv` - KV key-value storage
- `cloudflare-workers-ai` - Workers AI integration
- `cloudflare-vectorize` - Vector database for RAG

## Quick Reference

### Essential Commands

```bash
# New project
npm create cloudflare@latest -- my-next-app --framework=next

# Development
npm run dev      # Fast iteration (Next.js dev server)
npm run preview  # Test in workerd (production-like)

# Deployment
npm run deploy   # Build and deploy to Cloudflare

# TypeScript
npm run cf-typegen  # Generate binding types
```

### Critical Configuration

```jsonc
// wrangler.jsonc
{
  "compatibility_date": "2025-05-05",  // Minimum!
  "compatibility_flags": ["nodejs_compat"]  // Required!
}
```

### Common Pitfalls

1. ❌ Using Edge runtime → ✅ Use Node.js runtime
2. ❌ Global DB clients → ✅ Request-scoped clients
3. ❌ Old compatibility_date → ✅ Use 2025-05-05+
4. ❌ Missing nodejs_compat → ✅ Add to compatibility_flags
5. ❌ Only testing in `dev` → ✅ Always test `preview` before deploy
6. ❌ Using Turbopack → ✅ Use standard Next.js build

---

**Production Tested**: Official Cloudflare support and active community
**Token Savings**: ~59% vs manual setup
**Errors Prevented**: 11+ documented issues
**Last Verified**: 2025-12-04
