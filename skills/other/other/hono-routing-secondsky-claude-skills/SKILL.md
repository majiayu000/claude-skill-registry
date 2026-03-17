---
name: hono-routing
description: Type-safe Hono APIs with routing, middleware, RPC. Use for request validation, Zod/Valibot validators, or encountering middleware type inference, validation hook, RPC errors.

  Keywords: hono, hono routing, hono middleware, hono rpc, hono validator, zod validator, valibot validator, type-safe api, hono context, hono error handling, HTTPException, c.req.valid, middleware composition, hono hooks, typed routes, hono client, middleware response not typed, hono validation failed, hono rpc type inference

license: MIT
metadata:
  version: "2.0.0"
  package_version: "4.10.6"
  last_verified: "2025-11-21"
  errors_prevented: 12
  templates_included: 9
  references_included: 6
---

# Hono Routing & Middleware

**Status**: Production Ready ✅
**Last Updated**: 2025-11-21
**Dependencies**: None (framework-agnostic)
**Latest Versions**: hono@4.10.6, zod@4.1.12, valibot@1.1.0

---

## Quick Start (5 Minutes)

### Install

```bash
bun add hono@4.10.6  # preferred
# or: bun add hono@4.10.6
```

**Why Hono:**
- **Fast**: Built on Web Standards, runs on any JavaScript runtime
- **Lightweight**: ~10KB, no dependencies
- **Type-safe**: Full TypeScript support with type inference
- **Flexible**: Works on Cloudflare Workers, Deno, Bun, Node.js, Vercel

### Basic App

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => {
  return c.json({ message: 'Hello Hono!' })
})

export default app
```

**CRITICAL:**
- Use `c.json()`, `c.text()`, `c.html()` for responses
- Return the response (don't use `res.send()` like Express)
- Export app for runtime

### Add Validation

```bash
bun add zod@4.1.12 @hono/zod-validator@0.7.4
```

```typescript
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const schema = z.object({
  name: z.string(),
  age: z.number(),
})

app.post('/user', zValidator('json', schema), (c) => {
  const data = c.req.valid('json')
  return c.json({ success: true, data })
})
```

---

## Critical Rules

### Always Do

✅ **Return responses** from handlers (c.json, c.text, c.html, etc.)

✅ **Use c.req.valid('source')** after validation middleware to get typed data

✅ **Export app** for deployment (Cloudflare Workers, Bun, Deno, Node.js)

✅ **Use validation middleware** (zValidator, vValidator) for type-safe request data

✅ **Call await next()** in middleware to pass control to next handler

✅ **Use HTTPException** for expected errors (returns proper HTTP status)

✅ **Use template tag validators** (zValidator, vValidator) not hooks

✅ **Define context types** for custom variables (`Hono<{ Variables: { ... } }>`)

✅ **Use sub-apps** (app.route()) for organizing large APIs

✅ **Type your RPC routes** (`export type AppType = typeof routes`) for client

### Never Do

❌ **Never forget to return** response from handlers

❌ **Never use req.json() directly** without validation - use c.req.valid()

❌ **Never mix validation hooks** with middleware - use middleware only

❌ **Never forget await next()** in middleware - breaks middleware chain

❌ **Never use res.send()** - not available (use c.json(), c.text(), etc.)

❌ **Never skip error handling** - use app.onError() for global handler

❌ **Never access unvalidated data** after validation middleware

❌ **Never use blocking operations** in middleware - breaks async chain

❌ **Never hardcode origins** in CORS - use environment variables

❌ **Never skip type exports** for RPC - client won't have types

---

## Top 5 Errors (See references/top-errors.md for all 12)

### Error #1: Middleware Response Not Typed
**Problem**: Middleware returns response but route handler still executes
**Solution**: Don't return from middleware if you want chain to continue - only set variables
```typescript
// ❌ Wrong - breaks chain
app.use('*', (c) => {
  return c.json({ error: 'Unauthorized' }, 401)
})

// ✅ Correct - throw HTTPException instead
app.use('*', (c, next) => {
  if (!isAuthorized) {
    throw new HTTPException(401, { message: 'Unauthorized' })
  }
  await next()
})
```

### Error #2: Validation Hook vs Middleware Confusion
**Problem**: Using validation hooks instead of middleware
**Solution**: Always use middleware validators (zValidator, vValidator)
```typescript
// ❌ Wrong - hooks deprecated
app.post('/user', (c) => {
  const data = c.req.json<User>() // No runtime validation!
})

// ✅ Correct - middleware with runtime validation
app.post('/user', zValidator('json', schema), (c) => {
  const data = c.req.valid('json') // Validated & typed!
})
```

### Error #3: Missing await next() in Middleware
**Problem**: Middleware doesn't call next(), breaking chain
**Solution**: Always call await next() unless returning early
```typescript
// ❌ Wrong - chain broken
app.use('*', (c) => {
  console.log('Log')
  // Missing await next()!
})

// ✅ Correct
app.use('*', async (c, next) => {
  console.log('Log')
  await next()
})
```

### Error #4: Context Variable Type Inference
**Problem**: c.get() and c.set() not typed
**Solution**: Define Variables type in Hono constructor
```typescript
// ❌ Wrong - no types
const app = new Hono()
c.set('user', { id: '123' }) // Not typed
const user = c.get('user') // any

// ✅ Correct - typed
type Variables = {
  user: { id: string; name: string }
}
const app = new Hono<{ Variables: Variables }>()
c.set('user', { id: '123', name: 'Alice' })
const user = c.get('user') // Fully typed!
```

### Error #5: RPC Type Inference Not Working
**Problem**: Client doesn't have types from server routes
**Solution**: Export AppType and use hc<AppType>
```typescript
// Server
const routes = app.get('/users', (c) => c.json([]))
export type AppType = typeof routes // Export this!

// Client
import { hc } from 'hono/client'
import type { AppType } from './server'

const client = hc<AppType>('http://localhost:8787') // Fully typed!
```

**Load `references/top-errors.md` for all 12 errors with detailed solutions.**

---

## Common Use Cases

### Use Case 1: Basic REST API
**When**: Simple CRUD operations
**Quick Pattern**:
```typescript
app.get('/users', (c) => c.json({ users: [] }))
app.post('/users', (c) => c.json({ created: true }))
app.get('/users/:id', (c) => c.json({ user: {} }))
app.put('/users/:id', (c) => c.json({ updated: true }))
app.delete('/users/:id', (c) => c.json({ deleted: true }))
```
**Load**: `references/setup-guide.md` → Complete Example

### Use Case 2: Request Validation (Zod)
**When**: Need type-safe request validation
**Quick Pattern**:
```typescript
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

app.post('/user',
  zValidator('json', z.object({
    name: z.string(),
    email: z.string().email(),
  })),
  (c) => {
    const data = c.req.valid('json') // Typed!
    return c.json(data)
  }
)
```
**Load**: `references/validation-libraries.md`

### Use Case 3: Type-Safe RPC
**When**: Full-stack TypeScript with shared types
**Load**: `references/rpc-guide.md` + `templates/rpc-pattern.ts`

### Use Case 4: Middleware Composition
**When**: Authentication, logging, rate limiting
**Load**: `references/middleware-catalog.md` + `templates/middleware-composition.ts`

### Use Case 5: Custom Context Variables
**When**: Share data between middleware and routes
**Load**: `templates/context-extension.ts`

---

## When to Load References

**Load `references/setup-guide.md` when**:
- User needs complete setup walkthrough
- User asks about deployment to different runtimes
- User needs CRUD API example
- User wants to try alternative validators (Valibot, ArkType, Typia)

**Load `references/top-errors.md` when**:
- Encountering any of the 12 documented errors
- User has middleware type issues
- User confused about validation hooks vs middleware
- User needs troubleshooting or debugging

**Load `references/common-patterns.md` when**:
- User asks for code examples or best practices
- User needs route grouping, error handling, file upload patterns
- User wants streaming, WebSocket, or pagination examples

**Load `references/middleware-catalog.md` when**:
- User needs built-in middleware (cors, logger, jwt, cache, compress, etag)
- User wants to create custom middleware
- User asks about authentication or authorization

**Load `references/rpc-guide.md` when**:
- User building full-stack TypeScript app
- User wants type-safe client/server communication
- User asks about hono/client or RPC patterns

**Load `references/validation-libraries.md` when**:
- User comparing Zod vs Valibot vs ArkType vs Typia
- User needs validation examples for each library
- User asks about performance or bundle size

---

## Configuration Reference

### Minimal Configuration

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/', (c) => c.json({ message: 'Hello' }))

export default app
```

### Production Configuration

```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import { HTTPException } from 'hono/http-exception'

type Variables = {
  user: { id: string; name: string }
  requestId: string
}

const app = new Hono<{ Variables: Variables }>()

// Global middleware
app.use('*', logger())
app.use('*', async (c, next) => {
  c.set('requestId', crypto.randomUUID())
  await next()
})

app.use('*', cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
  credentials: true,
}))

// Routes
app.route('/api', apiRoutes)

// Global error handler
app.onError((err, c) => {
  if (err instanceof HTTPException) {
    return c.json(
      { error: err.message },
      err.status
    )
  }

  console.error(err)
  return c.json(
    { error: 'Internal Server Error' },
    500
  )
})

// 404 handler
app.notFound((c) => {
  return c.json({ error: 'Not Found' }, 404)
})

export default app
```

---

## Using Bundled Resources

### References (references/)

- **setup-guide.md** - Complete 6-step setup (install → deploy)
- **top-errors.md** - All 12 errors with solutions
- **common-patterns.md** - 7 production patterns (RPC, middleware, error handling, file upload)
- **middleware-catalog.md** - Built-in middleware reference (cors, logger, jwt, cache)
- **rpc-guide.md** - Type-safe RPC client/server guide
- **validation-libraries.md** - Comparison of Zod, Valibot, ArkType, Typia

### Templates (templates/)

- **routing-patterns.ts** - Route examples (params, query, wildcard, grouping)
- **validation-zod.ts** - Zod validation examples
- **validation-valibot.ts** - Valibot validation examples
- **middleware-composition.ts** - Auth, rate limiting, logging middleware
- **error-handling.ts** - HTTPException and global error handler
- **context-extension.ts** - Custom context variables
- **rpc-pattern.ts** - RPC server setup
- **rpc-client.ts** - RPC client usage
- **package.json** - Dependencies configuration

---

## Dependencies

**Required**:
- `hono@^4.10.2` - Core framework

**Choose ONE validator** (recommended):
- `zod@^4.1.12` + `@hono/zod-validator@^0.7.4` (most popular)
- `valibot@^1.1.0` + `@hono/valibot-validator@^0.5.3` (smaller bundle)
- `arktype@^2.0.0` + `@hono/arktype-validator@^0.1.0` (fastest runtime)
- `typia@^7.0.0` + `@hono/typia-validator@^0.1.0` (compile-time validation)

**Optional**:
- `@hono/node-server` - Node.js adapter
- `@cloudflare/workers-types` - TypeScript types for Workers

---

## Official Documentation

- **Hono**: https://hono.dev
- **GitHub**: https://github.com/honojs/hono (17.8k ⭐)
- **API Reference**: https://hono.dev/docs/api/hono
- **Routing**: https://hono.dev/docs/api/routing
- **Middleware**: https://hono.dev/docs/guides/middleware
- **Validation**: https://hono.dev/docs/guides/validation
- **RPC**: https://hono.dev/docs/guides/rpc
- **Examples**: https://github.com/honojs/hono/tree/main/examples

---

## Comparison: Hono vs Alternatives

| Feature          | Hono      | Express   | Fastify   |
| ---------------- | --------- | --------- | --------- |
| **Size**         | ~10KB     | ~200KB    | ~100KB    |
| **TypeScript**   | ✅ Native  | ⚠️ Types  | ✅ Native  |
| **Type Inference**| ✅ Full   | ❌ No     | ⚠️ Limited |
| **RPC**          | ✅ Built-in| ❌ No     | ❌ No     |
| **Edge Runtime** | ✅ Yes    | ❌ No     | ❌ No     |
| **Validation**   | ✅ Plugin  | ⚠️ Manual | ✅ Plugin  |
| **Speed**        | Very Fast | Fast      | Very Fast |

**Recommendation**:
- **Use Hono if**: TypeScript, edge runtime, full type inference, small bundle
- **Use Express if**: Legacy Node.js app, large ecosystem needed
- **Use Fastify if**: Node.js only, need fastest Node.js framework

---

## Production Examples

**Verified working projects**:

1. **Cloudflare Workers API**: https://github.com/honojs/examples/tree/main/cloudflare-workers
2. **Bun REST API**: https://github.com/honojs/examples/tree/main/bun
3. **Deno API**: https://github.com/honojs/examples/tree/main/deno
4. **Node.js API**: https://github.com/honojs/examples/tree/main/nodejs

---

## Complete Setup Checklist

- [ ] Installed Hono (`bun add hono`)
- [ ] Installed validator (Zod, Valibot, ArkType, or Typia)
- [ ] Created basic app with routes
- [ ] Added validation middleware to routes
- [ ] Configured CORS for cross-origin requests
- [ ] Added global error handler (app.onError)
- [ ] Added 404 handler (app.notFound)
- [ ] Configured context types for custom variables
- [ ] Tested routes locally
- [ ] Deployed to target runtime (Cloudflare, Bun, Deno, Node.js)

---

**Questions? Issues?**

1. Check `references/top-errors.md` for all 12 errors and solutions
2. Review `references/setup-guide.md` for complete setup walkthrough
3. See `references/common-patterns.md` for production patterns
4. Check `references/middleware-catalog.md` for built-in middleware
5. See `references/rpc-guide.md` for type-safe client/server
6. Check official docs: https://hono.dev
