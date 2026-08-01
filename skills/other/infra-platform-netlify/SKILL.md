---
name: infra-platform-netlify
description: Netlify deployment platform — serverless functions, edge functions, redirects, forms, Blobs, build plugins
---

# Netlify Platform Patterns

> **Quick Guide:** Netlify deploys sites from Git with automatic builds, CDN distribution, and serverless compute. Use `netlify.toml` for all configuration (redirects, headers, build settings, function schedules, plugins). Serverless functions live in `netlify/functions/` and use the standard `(req: Request, context: Context) => Response` signature. Edge functions run on Deno at the network edge for geo-personalization and request transformation. Use `Netlify.env.get()` for environment variables in functions — never `process.env`. Use Netlify Blobs for key-value storage accessible from functions and edge functions.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `Netlify.env.get()` to access environment variables in functions — NOT `process.env` which is unavailable in the modern functions runtime)**

**(You MUST use the `.mts` file extension for serverless functions to get ES module support — `.ts` defaults to CommonJS unless `"type": "module"` is in package.json)**

**(You MUST use `context.waitUntil()` for post-response background work — work not passed to waitUntil may be cancelled when the response is sent)**

**(You MUST keep redirects and headers in `netlify.toml` — they are global and NOT scoped to deploy contexts)**

</critical_requirements>

---

## Examples

- [Core Setup & Functions](examples/core.md) — netlify.toml, serverless functions, scheduled functions, background functions, response streaming
- [Edge Functions & Blobs](examples/edge-functions.md) — edge function patterns, geo-personalization, middleware, Netlify Blobs storage
- [Quick Reference](reference.md) — CLI commands, limits tables, redirects/headers syntax, build plugin structure

---

**Auto-detection:** Netlify, netlify.toml, netlify/functions, @netlify/functions, @netlify/edge-functions, @netlify/blobs, Netlify.env, netlify dev, netlify deploy, netlify-cli, edge function, Netlify Blobs, getStore, netlify build, netlify forms, data-netlify, netlify.app, deploy-preview, branch-deploy, Netlify Identity

**When to use:**

- Deploying sites and applications to Netlify's CDN and serverless platform
- Writing serverless functions (API endpoints, webhooks, scheduled tasks)
- Writing edge functions (geo-personalization, A/B testing, auth, request transformation)
- Configuring redirects, rewrites, proxy rules, and custom headers
- Storing data with Netlify Blobs (key-value, file uploads, metadata)
- Setting up build plugins for custom build pipeline logic
- Managing environment variables across deploy contexts (production, deploy-preview, branch-deploy)
- Configuring Netlify Forms for static site form handling

**When NOT to use:**

- Long-running compute exceeding 60 seconds (serverless) or 50ms CPU (edge) — use traditional servers
- Workloads needing persistent database connections — Netlify functions are stateless per invocation
- Applications requiring WebSocket connections (Netlify does not support persistent WebSockets)

**Key patterns covered:**

- `netlify.toml` configuration (build, redirects, headers, deploy contexts, plugins)
- Serverless functions with typed `Context` (geo, cookies, params, waitUntil)
- Scheduled functions with cron expressions
- Background functions for long-running tasks (up to 15 minutes)
- Response streaming for real-time output
- Edge functions on Deno runtime with geo and request transformation
- Netlify Blobs key-value storage (site-level and deploy-scoped)
- Environment variables with scopes and deploy context overrides
- Netlify Forms with honeypot spam filtering
- Build plugins with lifecycle hooks

---

<philosophy>

## Philosophy

Netlify is a Git-centric platform: push to a branch, Netlify builds and deploys automatically. Configuration lives in `netlify.toml` alongside your code. The platform provides three compute primitives:

1. **Serverless Functions** — Node.js-based, up to 60 seconds execution, 1 GB memory. For API endpoints, webhooks, form handlers, and scheduled tasks.
2. **Edge Functions** — Deno-based, 50ms CPU limit, run at the nearest edge node. For request/response transformation, geo-personalization, A/B testing, and authentication.
3. **Background Functions** — Same as serverless but async (client gets 202 immediately), up to 15 minutes. For long-running tasks like data processing and batch operations.

**Key architectural decisions:**

- **`netlify.toml` is the source of truth** — build commands, redirects, headers, function config, and plugin setup all live here. Settings in `netlify.toml` override the Netlify UI.
- **Functions use web standard APIs** — `Request`, `Response`, `ReadableStream`, `URL`. No proprietary request/response objects.
- **Edge functions are middleware** — they intercept requests, can modify them, and call `context.next()` to continue the chain. Return `undefined` to skip.
- **Blobs for storage** — Netlify Blobs provides key-value storage accessible from serverless functions, edge functions, and build plugins without external database setup.

**When to use Netlify:**

- Static sites, JAMstack apps, and full-stack applications with serverless backends
- Sites needing CDN distribution with automatic HTTPS
- Projects benefiting from deploy previews on every pull request
- Applications needing geo-based personalization at the edge

**When NOT to use Netlify:**

- CPU-intensive compute exceeding function time limits
- Applications needing persistent server processes or WebSockets
- Workloads requiring more than 1 GB memory per function invocation
- Data-heavy applications needing a collocated database (functions run in a single AWS region)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: netlify.toml Configuration

All Netlify configuration lives in `netlify.toml` at the repository root. It controls builds, redirects, headers, function settings, deploy contexts, and plugins.

```toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[functions]
  node_bundler = "esbuild"

[context.production.environment]
  API_URL = "https://api.example.com"

[context.deploy-preview.environment]
  API_URL = "https://staging-api.example.com"
```

**Key rule:** Redirects (`[[redirects]]`) and headers (`[[headers]]`) are global — they cannot be scoped to deploy contexts. Everything else (`[build]`, `[functions]`, `[[plugins]]`) supports context-specific overrides.

See [examples/core.md](examples/core.md) for full netlify.toml with redirects, headers, and deploy contexts.

---

### Pattern 2: Serverless Functions

Functions live in `netlify/functions/` and use the standard Web API signature. Use `.mts` for ES module support.

```typescript
// netlify/functions/hello.mts
import type { Config, Context } from "@netlify/functions";

export default async (req: Request, context: Context) => {
  const name = new URL(req.url).searchParams.get("name") ?? "World";
  return new Response(`Hello, ${name}!`, {
    headers: { "content-type": "text/plain" },
  });
};

export const config: Config = {
  path: "/api/hello",
};
```

**Why good:** Uses standard `Request`/`Response` APIs, typed `Context` provides geo/cookies/params, `config.path` maps custom routes instead of the default `/.netlify/functions/hello` path.

See [examples/core.md](examples/core.md) for full function patterns with route params, POST handling, and error responses.

---

### Pattern 3: Scheduled Functions

Scheduled functions run on a cron schedule. They receive a JSON body with `next_run` timestamp. They only run on published (production) deploys.

```typescript
// netlify/functions/daily-report.mts
import type { Config } from "@netlify/functions";

export default async (req: Request) => {
  const { next_run } = await req.json();
  console.log("Running daily report. Next run:", next_run);
  // Perform scheduled work...
};

export const config: Config = {
  schedule: "@daily",
};
```

**Limitation:** 60-second execution limit. Cannot be invoked via URL. For longer tasks, use background functions triggered by a scheduled function.

See [examples/core.md](examples/core.md) for cron expressions and netlify.toml schedule config.

---

### Pattern 4: Background Functions

Background functions return a 202 to the client immediately and continue processing for up to 15 minutes. Name the file with a `-background` suffix.

```typescript
// netlify/functions/process-background.mts
import type { Context } from "@netlify/functions";

export default async (req: Request, context: Context) => {
  const data = await req.json();
  // Long-running work — client already received 202
  await processLargeDataset(data);
  console.log("Background processing complete");
};
```

**Key rule:** The return value is ignored. The client gets `202 Accepted` immediately. Use for data processing, batch operations, email sending, and webhook fanout.

---

### Pattern 5: Edge Functions (Deno Runtime)

Edge functions run on Deno at the nearest edge node. They intercept requests and can modify, redirect, rewrite, or pass through to the origin.

```typescript
// netlify/edge-functions/geo-redirect.ts
import type { Config, Context } from "@netlify/edge-functions";

export default async (req: Request, context: Context) => {
  const { country } = context.geo;
  if (country?.code === "DE") {
    return new URL("/de", req.url); // Rewrite to German page
  }
  // Return undefined to continue the chain
};

export const config: Config = {
  path: "/",
};
```

**Key differences from serverless functions:** Deno runtime (not Node.js), 50ms CPU limit, runs at edge (not a single region), return `undefined` to skip, return `URL` for same-site rewrite. Use `context.next()` to call the next function in the chain or the origin.

See [examples/edge-functions.md](examples/edge-functions.md) for middleware patterns, geo-personalization, and response transformation.

---

### Pattern 6: Netlify Blobs Storage

Blobs provide key-value storage accessible from functions and edge functions. No external database setup needed.

```typescript
import { getStore } from "@netlify/blobs";
import type { Context } from "@netlify/functions";

export default async (req: Request, context: Context) => {
  const store = getStore("user-preferences");
  const userId = context.params.id;

  if (req.method === "GET") {
    const prefs = await store.get(userId, { type: "json" });
    if (!prefs) return new Response("Not found", { status: 404 });
    return Response.json(prefs);
  }

  if (req.method === "PUT") {
    const data = await req.json();
    await store.setJSON(userId, data);
    return new Response("Saved", { status: 200 });
  }
};
```

**Consistency:** Eventually consistent by default (~60s propagation). Use `{ consistency: "strong" }` when immediate reads after writes are required.

See [examples/edge-functions.md](examples/edge-functions.md) for Blobs patterns with metadata, listing, and deploy-scoped stores.

---

### Pattern 7: Redirects and Rewrites

Redirects and rewrites are defined in `netlify.toml` with `[[redirects]]` tables. Status 200 creates a rewrite (URL stays the same). Status 301/302 creates a redirect.

```toml
# SPA fallback
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# API proxy (avoids CORS)
[[redirects]]
  from = "/api/*"
  to = "https://api.example.com/:splat"
  status = 200
  force = true

# Old URL redirect
[[redirects]]
  from = "/old-blog/*"
  to = "/blog/:splat"
  status = 301
```

**Key rules:** Redirects are processed in order — first match wins. Use `force = true` to override existing files. Use `:splat` for wildcard captures and `:paramName` for named captures.

See [reference.md](reference.md) for full redirect syntax, conditional redirects, and signed proxy patterns.

---

### Pattern 8: Environment Variables

Environment variables are set in the Netlify UI (for secrets) or `netlify.toml` (for non-sensitive values). They support scopes (Builds, Functions) and deploy context overrides.

```toml
# netlify.toml — non-sensitive values only
[build.environment]
  NODE_VERSION = "20"

[context.production.environment]
  API_URL = "https://api.example.com"

[context.deploy-preview.environment]
  API_URL = "https://staging-api.example.com"
```

```typescript
// In functions — always use Netlify.env, not process.env
const apiUrl = Netlify.env.get("API_URL");
const hasKey = Netlify.env.has("SECRET_KEY");
```

**Key rule:** Never put secrets in `netlify.toml` — it is version controlled. Use the Netlify UI or CLI (`netlify env:set KEY value`) for sensitive values.

</patterns>

---

<performance>

## Performance Optimization

### Function Limits

| Type                  | Execution Time | Memory | Payload Size            |
| --------------------- | -------------- | ------ | ----------------------- |
| Serverless (sync)     | 60 seconds     | 1 GB   | 6 MB (request/response) |
| Serverless (streamed) | 60 seconds     | 1 GB   | 20 MB (response)        |
| Background            | 15 minutes     | 1 GB   | 256 KB                  |
| Scheduled             | 60 seconds     | 1 GB   | N/A                     |
| Edge                  | 50ms CPU       | 512 MB | N/A                     |

### Optimization Techniques

| Technique                              | Impact                                                          |
| -------------------------------------- | --------------------------------------------------------------- |
| Response streaming                     | Faster TTFB, up to 20 MB response (vs 6 MB buffered)            |
| `context.waitUntil()`                  | Returns response immediately, processes analytics/logging after |
| Edge functions with caching            | Responses cached at edge, invocations don't count toward limits |
| `esbuild` bundler for functions        | Faster builds than default `zisi` bundler                       |
| `preferStatic: true` on edge functions | Serves static files when available, skips edge function         |

### Deploy Context Priority

Settings cascade from most general to most specific:

```
[build] (default for all contexts)
  └── [context.production] (production deploys)
  └── [context.deploy-preview] (PR/MR deploys)
  └── [context.branch-deploy] (non-production branches)
  └── [context."feature-branch"] (specific branch — highest priority)
```

</performance>

---

<decision_framework>

## Decision Framework

### Choosing a Compute Primitive

```
What does your function need to do?
  |
  +-- API endpoint / webhook handler
  |     +-- Needs geo data or request transformation? --> Edge Function
  |     +-- Standard request/response? --> Serverless Function
  |
  +-- Scheduled/cron job
  |     +-- Under 60 seconds? --> Scheduled Function
  |     +-- Longer processing? --> Scheduled Function triggers Background Function
  |
  +-- Long-running task (data processing, batch operations)
  |     +-- Up to 15 minutes? --> Background Function
  |     +-- Longer? --> External service / queue
  |
  +-- Request modification (auth, geo-redirect, A/B test, headers)
        +-- Edge Function (runs before origin, at the nearest edge node)
```

### Choosing Storage

```
What kind of data?
  |
  +-- Key-value pairs (preferences, config, cache)
  |     +-- Netlify Blobs (site-level store, eventual or strong consistency)
  |
  +-- Build artifacts / deploy-specific data
  |     +-- Netlify Blobs (deploy-scoped store)
  |
  +-- Relational data with queries
  |     +-- External database (PostgreSQL, MySQL, etc.)
  |
  +-- File uploads (images, documents)
        +-- Netlify Blobs (up to 5 GB per object)
        +-- External object storage for advanced needs
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `process.env` in modern Netlify functions — use `Netlify.env.get()` instead (process.env is unavailable in the modern runtime)
- Putting secrets in `netlify.toml` — this file is version controlled; use the Netlify UI or CLI for sensitive values
- Missing `await` on `context.waitUntil()` promises — work not passed to waitUntil may be silently cancelled after response
- Using `.ts` extension without `"type": "module"` in package.json — defaults to CommonJS, causing import issues; use `.mts` instead
- Scoping `[[redirects]]` or `[[headers]]` under `[context.*]` — they are always global and context scoping is silently ignored

**Medium Priority Issues:**

- Not setting `force = true` on proxy rewrites — without it, Netlify serves an existing file instead of proxying
- Using `node_bundler = "zisi"` (the default) instead of `"esbuild"` — esbuild is significantly faster
- Edge functions with `/*` path without `preferStatic: true` — shadows all static files, breaking CSS/JS/images
- Expecting edge functions to work with Split Testing — Split Testing relies on branch deploys which skip edge functions
- Not setting `NODE_VERSION` in build environment — defaults may not match your project's requirements

**Common Mistakes:**

- Trying to invoke scheduled functions via URL — they only run on their cron schedule (or manually via the Netlify UI)
- Expecting background functions to return data to the client — the client receives 202 immediately, return value is ignored
- Using `context.next()` in serverless functions — `next()` is an edge function concept for middleware chaining
- Forgetting that edge functions run on Deno, not Node.js — some Node.js APIs and npm packages may not be available
- Setting cookies across subdomains on `netlify.app` — `netlify.app` is on the Public Suffix List, cross-subdomain cookies require a custom domain

**Gotchas & Edge Cases:**

- Redirects are processed in order — first match wins; put specific rules before catch-all rules
- Edge function CPU time is 50ms, not wall-clock time — I/O waiting (fetch, Blobs) does not count
- Netlify Blobs is eventually consistent by default (~60s) — use `{ consistency: "strong" }` for immediate reads after writes
- Deploy preview URLs have unique subdomains — hardcoded absolute URLs will break in previews; use relative paths
- The `functions` directory defaults to `netlify/functions/` — custom paths need `[functions] directory = "path"` in netlify.toml
- Background functions have a 256 KB payload limit — much smaller than the 6 MB serverless limit
- Edge functions cannot rewrite to external URLs — use `fetch()` to retrieve external content and return it as a `Response`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `Netlify.env.get()` to access environment variables in functions — NOT `process.env` which is unavailable in the modern functions runtime)**

**(You MUST use the `.mts` file extension for serverless functions to get ES module support — `.ts` defaults to CommonJS unless `"type": "module"` is in package.json)**

**(You MUST use `context.waitUntil()` for post-response background work — work not passed to waitUntil may be cancelled when the response is sent)**

**(You MUST keep redirects and headers in `netlify.toml` — they are global and NOT scoped to deploy contexts)**

**Failure to follow these rules will cause broken environment variable access, module format errors, lost background work, and silently ignored configuration.**

</critical_reminders>
