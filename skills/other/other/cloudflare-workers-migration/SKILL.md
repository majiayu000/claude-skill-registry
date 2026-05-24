---
name: cloudflare-workers-migration
description: Migrate to Cloudflare Workers from AWS Lambda, Vercel, Express, and Node.js. Use when porting existing applications to the edge, adapting serverless functions, or resolving Node.js API compatibility issues.
metadata:
  version: "1.0.0"
license: MIT
---

# Workers Migration Guide

Migrate existing applications to Cloudflare Workers from various platforms.

## Migration Decision Tree

```
What are you migrating from?
├── AWS Lambda
│   └── Node.js handler? → Lambda adapter pattern
│   └── Python? → Consider Python Workers
│   └── Container/custom runtime? → May need rewrite
├── Vercel/Next.js
│   └── API routes? → Minimal changes with adapter
│   └── Full Next.js app? → Use OpenNext adapter
│   └── Middleware? → Direct Workers equivalent
├── Express/Node.js
│   └── Simple API? → Hono (similar API)
│   └── Complex middleware? → Gradual migration
│   └── Heavy node: usage? → Compatibility layer
└── Other Edge (Deno Deploy, Fastly)
    └── Standard Web APIs? → Minimal changes
    └── Platform-specific? → Targeted rewrites
```

## Platform Comparison

| Feature | Workers | Lambda | Vercel | Express |
|---------|---------|--------|--------|---------|
| **Cold Start** | ~0ms | 100-500ms | 10-100ms | N/A |
| **CPU Limit** | 50ms/10ms | 15 min | 10s | None |
| **Memory** | 128MB | 10GB | 1GB | System |
| **Max Response** | 6MB (stream unlimited) | 6MB | 4.5MB | None |
| **Global Edge** | 300+ PoPs | Regional | ~20 PoPs | Manual |
| **Node.js APIs** | Partial | Full | Full | Full |

## Top 10 Migration Errors

| Error | From | Cause | Solution |
|-------|------|-------|----------|
| `fs is not defined` | Lambda/Express | File system access | Use KV/R2 for storage |
| `Buffer is not defined` | Node.js | Node.js globals | Import from `node:buffer` |
| `process.env undefined` | All | Env access pattern | Use `env` parameter |
| `setTimeout not returning` | Lambda | Async patterns | Use `ctx.waitUntil()` |
| `require() not found` | Express | CommonJS | Convert to ESM imports |
| `Exceeded CPU time` | All | Long computation | Chunk or use DO |
| `body already consumed` | Express | Request body | Clone before read |
| `Headers not iterable` | Lambda | Headers API | Use Headers constructor |
| `crypto.randomBytes` | Node.js | Node crypto | Use `crypto.getRandomValues` |
| `Cannot find module` | All | Missing polyfill | Check Workers compatibility |

## Quick Migration Patterns

### AWS Lambda Handler

```typescript
// Before: AWS Lambda
export const handler = async (event, context) => {
  const body = JSON.parse(event.body);
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello' }),
  };
};

// After: Cloudflare Workers
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const body = await request.json();
    return Response.json({ message: 'Hello' });
  },
};
```

### Express Middleware

```typescript
// Before: Express
app.use((req, res, next) => {
  if (!req.headers.authorization) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
});

// After: Hono Middleware
app.use('*', async (c, next) => {
  if (!c.req.header('Authorization')) {
    return c.json({ error: 'Unauthorized' }, 401);
  }
  await next();
});
```

### Environment Variables

```typescript
// Before: Node.js
const apiKey = process.env.API_KEY;

// After: Workers
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const apiKey = env.API_KEY;
    // ...
  },
};
```

## Node.js Compatibility

Workers support many Node.js APIs via compatibility flags:

```jsonc
// wrangler.jsonc
{
  "compatibility_flags": ["nodejs_compat_v2"],
  "compatibility_date": "2024-12-01"
}
```

**Supported with nodejs_compat_v2:**
- `crypto` (most methods)
- `buffer` (Buffer class)
- `util` (promisify, types)
- `stream` (Readable, Writable)
- `events` (EventEmitter)
- `path` (all methods)
- `string_decoder`
- `assert`

**Not Supported (need alternatives):**
- `fs` → Use R2/KV
- `child_process` → Not possible
- `cluster` → Not applicable
- `dgram` → Not supported
- `net` → Use fetch/WebSocket
- `tls` → Handled by platform

## When to Load References

| Reference | Load When |
|-----------|-----------|
| `references/lambda-migration.md` | Migrating AWS Lambda functions |
| `references/vercel-migration.md` | Migrating from Vercel/Next.js |
| `references/express-migration.md` | Migrating Express/Node.js apps |
| `references/node-compatibility.md` | Node.js API compatibility issues |

## Migration Checklist

1. **Analyze Dependencies**: Check for unsupported Node.js APIs
2. **Convert to ESM**: Replace require() with import
3. **Update Env Access**: Use env parameter instead of process.env
4. **Replace File System**: Use R2/KV for storage
5. **Handle Async**: Use ctx.waitUntil() for background tasks
6. **Test Locally**: Verify with wrangler dev
7. **Performance Test**: Ensure CPU limits aren't exceeded

## See Also

- `workers-runtime-apis` - Available APIs in Workers
- `workers-performance` - Optimization techniques
- `cloudflare-worker-base` - Basic Workers setup
