---
name: workers-frameworks
description: Framework integration for Cloudflare Workers. Use when building with Hono, Remix, Next.js, Astro, SvelteKit, Qwik, or Nuxt on Workers. Covers routing, SSR, static assets, and edge deployment.
version: 1.0.0
---

# Workers Frameworks Integration

Build full-stack applications on Cloudflare Workers using modern frameworks.

## Quick Start: Choose Your Framework

| Framework | Best For | SSR | Static | Workers Native |
|-----------|----------|-----|--------|----------------|
| **Hono** | APIs, lightweight apps | ✅ | ✅ | ✅ Native |
| **Remix** | Full-stack apps | ✅ | ✅ | ✅ Adapter |
| **Next.js** | React apps | ✅ | ✅ | ⚠️ OpenNext |
| **Astro** | Content sites | ✅ | ✅ | ✅ Adapter |
| **SvelteKit** | Svelte apps | ✅ | ✅ | ✅ Adapter |
| **Qwik** | Resumable apps | ✅ | ✅ | ✅ Adapter |
| **Nuxt** | Vue apps | ✅ | ✅ | ✅ Nitro |

## Framework Decision Tree

```
Need an API only?
  └─ Yes → Hono (fastest, smallest)
  └─ No → Building a full app?
           └─ React → Next.js (OpenNext) or Remix
           └─ Vue → Nuxt
           └─ Svelte → SvelteKit
           └─ Content-heavy → Astro
           └─ Max performance → Qwik
```

## Top 10 Framework Errors

| Error | Framework | Cause | Solution |
|-------|-----------|-------|----------|
| `No matching export "default"` | All | Wrong export format | Use `export default app` not `module.exports` |
| `Worker exceeded CPU limit` | Next.js | Heavy SSR | Use ISR, reduce bundle size |
| `Cannot read properties of undefined (reading 'env')` | Remix | Missing context | Pass `context` to loader/action |
| `globalThis is not defined` | All | Node.js globals | Use `nodejs_compat` flag |
| `Dynamic require not supported` | All | CJS in ESM | Convert to ESM imports |
| `Response body is locked` | All | Body already read | Clone response before reading |
| `Bindings not available` | All | Missing wrangler config | Add bindings to wrangler.jsonc |
| `404 on static assets` | All | Wrong assets config | Configure `assets` in wrangler.jsonc |
| `Hydration mismatch` | React/Vue | Server/client differ | Ensure consistent rendering |
| `Maximum call stack exceeded` | All | Circular imports | Refactor module structure |

## Hono Quick Start (Recommended)

```typescript
// src/index.ts
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

interface Env {
  DB: D1Database;
  KV: KVNamespace;
}

const app = new Hono<{ Bindings: Env }>();

// Middleware
app.use('*', logger());
app.use('/api/*', cors());

// Routes
app.get('/', (c) => c.text('Hello Workers!'));

app.get('/api/users', async (c) => {
  const { results } = await c.env.DB.prepare('SELECT * FROM users').all();
  return c.json(results);
});

app.post('/api/users', async (c) => {
  const { name, email } = await c.req.json();
  await c.env.DB.prepare('INSERT INTO users (name, email) VALUES (?, ?)')
    .bind(name, email)
    .run();
  return c.json({ success: true }, 201);
});

export default app;
```

```jsonc
// wrangler.jsonc
{
  "name": "my-app",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "compatibility_flags": ["nodejs_compat"],
  "d1_databases": [
    { "binding": "DB", "database_name": "my-db", "database_id": "xxx" }
  ]
}
```

## Static Assets Configuration

```jsonc
// wrangler.jsonc - Serving static files
{
  "name": "my-app",
  "main": "src/index.ts",
  "assets": {
    "directory": "./public",
    "binding": "ASSETS"
  }
}
```

```typescript
// Serve static with fallback to app
import { Hono } from 'hono';

const app = new Hono<{ Bindings: { ASSETS: Fetcher } }>();

// API routes
app.get('/api/*', apiHandler);

// Static assets fallback
app.get('*', async (c) => {
  return c.env.ASSETS.fetch(c.req.raw);
});

export default app;
```

## When to Load References

Load the specific framework reference when user:

| Reference | Load When |
|-----------|-----------|
| `references/hono.md` | Building APIs, microservices, or lightweight apps |
| `references/remix.md` | Full-stack React with loaders/actions |
| `references/nextjs.md` | Next.js App Router on Workers via OpenNext |
| `references/astro.md` | Content sites, blogs, docs, marketing pages |
| `references/sveltekit.md` | Svelte applications on Workers |
| `references/qwik.md` | Resumable apps, instant loading |
| `references/nuxt.md` | Vue 3 applications with Nitro |

## Common Patterns Across Frameworks

### Environment Bindings Access

```typescript
// Hono
app.get('/', (c) => c.env.DB.prepare('...'));

// Remix
export async function loader({ context }) {
  return context.cloudflare.env.DB.prepare('...');
}

// Astro
const db = Astro.locals.runtime.env.DB;

// SvelteKit
export async function load({ platform }) {
  return platform.env.DB.prepare('...');
}

// Nuxt
const { cloudflare } = useRuntimeConfig();
// Or via nitro: event.context.cloudflare.env.DB
```

### Error Handling Pattern

```typescript
// Universal error boundary pattern
app.onError((err, c) => {
  console.error(`[${c.req.path}] ${err.message}`);

  if (err instanceof HTTPException) {
    return err.getResponse();
  }

  return c.json(
    { error: 'Internal Server Error' },
    500
  );
});
```

## Performance Tips

1. **Bundle Size**: Keep under 1MB compressed
2. **Cold Starts**: Minimize top-level code
3. **Streaming**: Use streaming SSR when available
4. **Caching**: Leverage Cache API and CDN
5. **Code Splitting**: Dynamic imports for routes

## See Also

- `workers-performance` - Optimization techniques
- `workers-runtime-apis` - Workers APIs reference
- `cloudflare-worker-base` - Basic Workers setup
