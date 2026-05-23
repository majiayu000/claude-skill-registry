---
name: Cloudflare Workers
description: Edge deployment patterns and Cloudflare-specific considerations for LivestockAI
---

# Cloudflare Workers

LivestockAI is deployed on Cloudflare Workers for global edge performance. This skill covers Workers-specific patterns and constraints.

## Key Constraints

### No `process.env`

Cloudflare Workers does NOT support `process.env`. Environment variables come from:

- **Local dev**: `.dev.vars` file
- **Production**: Wrangler secrets

```bash
# .dev.vars (local)
DATABASE_URL=postgres://...
BETTER_AUTH_SECRET=...

# Production secrets
wrangler secret put DATABASE_URL
wrangler secret put BETTER_AUTH_SECRET
```

### Dynamic Imports Required

Database and auth modules must use dynamic imports in server functions:

```typescript
// ✅ Correct - works on Workers
export const fn = createServerFn().handler(async () => {
  const { getDb } = await import('~/lib/db')
  const db = await getDb()
  // ...
})

// ❌ Wrong - fails on Workers
import { db } from '~/lib/db'
```

### Memory Limits

Workers have a 128MB memory limit. For large operations:

- Stream responses instead of buffering
- Paginate database queries
- Avoid loading large datasets into memory

## Configuration

The `wrangler.jsonc` file configures the Worker:

```jsonc
{
  "name": "livestockai",
  "compatibility_date": "2024-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "main": "./dist/server/index.mjs",
}
```

## Deployment

```bash
# Deploy to production
bun run deploy
# or
wrangler deploy

# Preview deployment
wrangler deploy --env preview

# View logs
wrangler tail
```

## MCP Servers for Cloudflare

The `devops-engineer` agent has access to Cloudflare MCP servers:

| Server                     | Purpose                    |
| -------------------------- | -------------------------- |
| `cloudflare-bindings`      | Manage Workers, KV, R2, D1 |
| `cloudflare-builds`        | Deployment status and logs |
| `cloudflare-observability` | Worker logs and debugging  |
| `cloudflare-docs`          | Documentation search       |

Other agents should delegate Cloudflare tasks to `devops-engineer`.

## Common Issues

### "Cannot find module" errors

Use dynamic imports for database connections:

```typescript
const { getDb } = await import('~/lib/db')
const db = await getDb()
```

### Cold start latency

Minimize bundle size and avoid heavy initialization code.

### Environment variable access

```typescript
// ✅ Works - uses getDb() which handles env detection
const { getDb } = await import('~/lib/db')
const db = await getDb()

// ❌ Fails - process.env not available
const url = process.env.DATABASE_URL
```

## Request Flow

```
Browser → Cloudflare CDN → Worker → TanStack Start → Server Functions → Neon PostgreSQL
```

## Static Assets

Static assets are served from Cloudflare's CDN automatically. The `public/` directory contents are deployed alongside the Worker.

## Related Skills

- `neon-database` - Database connection patterns
- `dynamic-imports` - Why dynamic imports are required
- `tanstack-start` - Server function patterns
