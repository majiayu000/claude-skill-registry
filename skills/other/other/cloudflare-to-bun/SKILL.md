---
name: cloudflare-to-bun
description: Migrate Cloudflare Workers to Bun with runtime compatibility analysis. Use when converting Workers to Bun, migrating from Cloudflare bindings, or moving from edge to server deployment.
compatibility: Requires Bun 1.0+
allowed-tools: ["Bash", "Read", "Grep", "Write"]
metadata:
  author: daleseo
  category: bun-runtime
  tags: [bun, migration, cloudflare, workers, edge, bindings]
---

# Cloudflare Workers to Bun Migration

You are assisting with migrating Cloudflare Workers applications to Bun. This involves converting edge runtime APIs, replacing Cloudflare bindings, and adapting from edge to server deployment.

## Quick Reference

For detailed patterns, see:
- **Runtime APIs**: [runtime-apis.md](references/runtime-apis.md) - Cloudflare to Bun API mapping
- **Bindings Migration**: [bindings.md](references/bindings.md) - KV, R2, D1, Durable Objects replacements
- **Deployment**: [deployment.md](references/deployment.md) - Edge to server deployment strategies

## Migration Workflow

### 1. Pre-Migration Analysis

**Check current setup:**
```bash
# Check Cloudflare CLI
wrangler --version

# Check Bun installation
bun --version

# Analyze wrangler.toml
cat wrangler.toml
```

**Review worker configuration:**
```bash
# Check compatibility flags
grep compatibility_flags wrangler.toml

# Check bindings
grep -E "kv_namespaces|r2_buckets|d1_databases|durable_objects" wrangler.toml
```

### 2. Worker Types Analysis

Determine what type of Worker you're migrating:

- **Service Worker**: Traditional `addEventListener('fetch')` format
- **Module Worker**: Modern `export default { fetch() }` format
- **Scheduled Worker**: Cron triggers
- **Durable Objects**: Stateful objects
- **Pages Functions**: Next.js-like file-based routing

### 3. Runtime API Conversion

#### Basic Fetch Handler

**Cloudflare Worker (Module format):**
```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return new Response('Hello World');
  },
};
```

**Bun Server:**
```typescript
Bun.serve({
  port: 3000,
  fetch(request: Request): Response | Promise<Response> {
    return new Response('Hello World');
  },
});

console.log('Server running on http://localhost:3000');
```

#### Request/Response Handling

**Cloudflare Worker:**
```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/api/data') {
      return Response.json({ data: 'value' });
    }

    return new Response('Not found', { status: 404 });
  },
};
```

**Bun (with Hono for routing):**
```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/api/data', (c) => {
  return c.json({ data: 'value' });
});

app.notFound((c) => {
  return c.text('Not found', 404);
});

export default {
  port: 3000,
  fetch: app.fetch,
};
```

For complete API mapping, see [runtime-apis.md](references/runtime-apis.md).

### 4. Bindings Migration

Cloudflare Workers use bindings for KV, R2, D1, etc. These need to be replaced:

#### KV Namespace → Database/Cache

**Cloudflare Worker:**
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const value = await env.MY_KV.get('key');
    await env.MY_KV.put('key', 'value', { expirationTtl: 3600 });

    return Response.json({ value });
  },
};
```

**Bun (using Redis or SQLite):**
```typescript
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

Bun.serve({
  async fetch(request: Request) {
    const value = await redis.get('key');
    await redis.setex('key', 3600, 'value');

    return Response.json({ value });
  },
});
```

#### R2 Bucket → S3 or File System

**Cloudflare Worker:**
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const object = await env.MY_BUCKET.get('file.txt');
    const text = await object?.text();

    return new Response(text);
  },
};
```

**Bun (using S3-compatible storage):**
```typescript
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';

const s3 = new S3Client({ region: 'us-east-1' });

Bun.serve({
  async fetch(request: Request) {
    const command = new GetObjectCommand({
      Bucket: 'my-bucket',
      Key: 'file.txt',
    });

    const response = await s3.send(command);
    const text = await response.Body?.transformToString();

    return new Response(text);
  },
});
```

For all bindings replacements, see [bindings.md](references/bindings.md).

### 5. Environment Variables

**Cloudflare Worker (wrangler.toml):**
```toml
[vars]
API_KEY = "dev-key"

[[env.production.vars]]
API_KEY = "prod-key"
```

**Bun (.env files):**
```bash
# .env.development
API_KEY=dev-key

# .env.production
API_KEY=prod-key
```

Access in code:
```typescript
// Both use the same API
const apiKey = process.env.API_KEY;
```

### 6. Configuration Migration

**wrangler.toml:**
```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[vars]
ENVIRONMENT = "production"

kv_namespaces = [
  { binding = "MY_KV", id = "..." }
]

r2_buckets = [
  { binding = "MY_BUCKET", bucket_name = "my-bucket" }
]
```

**package.json (Bun):**
```json
{
  "name": "my-bun-app",
  "type": "module",
  "scripts": {
    "dev": "bun run --hot src/index.ts",
    "start": "bun run src/index.ts",
    "build": "bun build src/index.ts --outdir=dist"
  },
  "dependencies": {
    "hono": "^3.0.0",
    "ioredis": "^5.0.0"
  }
}
```

### 7. Routing Patterns

**Cloudflare Worker (manual routing):**
```typescript
export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/') {
      return new Response('Home');
    }

    if (url.pathname.startsWith('/api/')) {
      return handleApi(request);
    }

    return new Response('Not found', { status: 404 });
  },
};
```

**Bun (with Hono framework):**
```typescript
import { Hono } from 'hono';

const app = new Hono();

app.get('/', (c) => c.text('Home'));

const api = new Hono();
api.get('/users', (c) => c.json({ users: [] }));
app.route('/api', api);

export default {
  port: 3000,
  fetch: app.fetch,
};
```

### 8. Scheduled Events (Cron)

**Cloudflare Worker:**
```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    await doCleanup();
  },
};

// wrangler.toml
[triggers]
crons = ["0 0 * * *"]  # Daily at midnight
```

**Bun (using node-cron):**
```typescript
import cron from 'node-cron';

// Run daily at midnight
cron.schedule('0 0 * * *', async () => {
  await doCleanup();
});

// Start server
Bun.serve({
  fetch(request: Request) {
    return new Response('Server running');
  },
});
```

### 9. Testing Migration

**Cloudflare Worker (Miniflare):**
```typescript
import { Miniflare } from 'miniflare';

const mf = new Miniflare({
  script: `
    export default {
      fetch() { return new Response('Hello'); }
    }
  `,
});

const response = await mf.dispatchFetch('http://localhost/');
```

**Bun Test:**
```typescript
import { describe, test, expect } from 'bun:test';

describe('Server', () => {
  test('should respond to requests', async () => {
    const response = await fetch('http://localhost:3000/');
    expect(response.status).toBe(200);
  });
});
```

### 10. Deployment Strategy

**Cloudflare Workers:**
- Edge deployment (globally distributed)
- No cold starts
- Limited runtime (CPU time limits)
- Specialized bindings (KV, R2, D1)

**Bun Server:**
- Traditional server deployment
- Self-hosted or cloud (AWS, GCP, Azure)
- No CPU time limits
- Standard databases and storage
- Use Docker for containerization (see bun-deploy skill)

For deployment strategies, see [deployment.md](references/deployment.md).

### 11. Update package.json

```json
{
  "name": "migrated-from-cloudflare",
  "type": "module",
  "scripts": {
    "dev": "bun run --hot src/index.ts",
    "start": "NODE_ENV=production bun run src/index.ts",
    "test": "bun test",
    "build": "bun build src/index.ts --outdir=dist --minify"
  },
  "dependencies": {
    "hono": "^3.11.0",
    "ioredis": "^5.3.0",
    "@aws-sdk/client-s3": "^3.478.0"
  },
  "devDependencies": {
    "@types/bun": "latest"
  }
}
```

### 12. File Structure Migration

**Cloudflare Worker:**
```
cloudflare-worker/
├── src/
│   └── index.ts
├── wrangler.toml
└── package.json
```

**Bun Server:**
```
bun-server/
├── src/
│   ├── index.ts
│   ├── routes/
│   └── services/
├── .env.development
├── .env.production
├── package.json
├── tsconfig.json
└── bunfig.toml
```

## Migration Checklist

- [ ] Bun installed and verified
- [ ] Worker type identified (service/module/durable)
- [ ] Bindings mapped to replacements (KV→Redis, R2→S3, etc.)
- [ ] Environment variables migrated
- [ ] Routing migrated (manual → framework)
- [ ] Scheduled tasks migrated (cron triggers)
- [ ] wrangler.toml converted to package.json
- [ ] TypeScript configuration created
- [ ] Dependencies installed with `bun install`
- [ ] Tests migrated and passing
- [ ] Local server running
- [ ] Deployment strategy planned

## Key Differences

| Feature | Cloudflare Workers | Bun Server |
|---------|-------------------|------------|
| **Runtime** | Edge (V8 isolates) | Server (JavaScriptCore) |
| **Deployment** | Global edge network | Traditional hosting |
| **Cold Start** | ~0ms | Minimal with Bun |
| **Execution Time** | Limited (CPU time) | Unlimited |
| **Storage** | KV, R2, D1, DO | Redis, S3, PostgreSQL, etc. |
| **Cost Model** | Per-request | Server/container costs |
| **Scaling** | Automatic | Manual/auto-scaling groups |
| **State** | Durable Objects | Traditional databases |

## Common Patterns

### CORS Handling

**Same in both:**
```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// Handle OPTIONS preflight
if (request.method === 'OPTIONS') {
  return new Response(null, { headers: corsHeaders });
}
```

### JSON Responses

**Same in both:**
```typescript
return Response.json({ data: 'value' }, {
  headers: { 'Cache-Control': 'max-age=3600' }
});
```

### Error Handling

**Same in both:**
```typescript
try {
  // Your code
} catch (error) {
  return new Response('Internal Server Error', { status: 500 });
}
```

## Completion

Once migration is complete, provide summary:
- ✅ Migration status (success/partial/issues)
- ✅ Bindings replaced (KV→Redis, R2→S3, etc.)
- ✅ Deployment strategy chosen
- ✅ Performance comparison
- ✅ Links to Bun documentation

## Next Steps

Suggest to the user:
1. Set up Redis/database for KV replacement
2. Configure S3-compatible storage for R2 replacement
3. Set up monitoring and logging
4. Plan deployment strategy (Docker, cloud hosting)
5. Use bun-deploy skill for containerization
6. Update CI/CD pipelines
7. Load test the migrated application
