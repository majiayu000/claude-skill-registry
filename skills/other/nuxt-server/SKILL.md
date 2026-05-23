---
name: nuxt-server
description: Nuxt 5 server-side development with Nitro v3, h3 v2, API routes, middleware, and database integration. Use when creating server routes, integrating D1/Drizzle, or migrating from Nitro v2.
license: MIT
metadata:
  version: 5.0.0
  author: Claude Skills Maintainers
  category: Framework
  framework: Nuxt
  framework-version: 5.x
  last-verified: 2026-03-30
---

# Nuxt 5 Server Development

Server routes, API patterns, and backend development with Nitro v3.

**Use when**: creating server API routes, implementing server middleware, integrating databases (D1, PostgreSQL, Drizzle), handling file uploads, migrating from Nitro v2/h3 v1 to Nitro v3/h3 v2, or building backend logic.

## Quick Reference

### Nuxt 5 Server API Changes (from Nuxt 4)

| Area | Nuxt 4 (Nitro v2) | Nuxt 5 (Nitro v3) |
|------|-------------------|-------------------|
| Package | `nitropack` | `nitro` |
| h3 imports | `import { ... } from 'h3'` | `import { ... } from 'nitro/h3'` |
| Error creation | `createError({statusCode})` | `new HTTPError({status})` |
| Event path | `event.path` | `event.url.pathname` |
| Event method | `event.method` | `event.req.method` |
| Status code | `event.node.res.statusCode` | `event.res.status` |
| Response headers | `setResponseHeader(event, ...)` | `event.res.headers.set(...)` |
| Runtime config | `useRuntimeConfig(event)` | `useRuntimeConfig()` |
| Route rules redirect | `statusCode` | `status` |

### File-Based Server Routes

```
server/
├── api/                      # API endpoints (/api/*)
│   ├── users/
│   │   ├── index.get.ts      → GET  /api/users
│   │   ├── index.post.ts     → POST /api/users
│   │   ├── [id].get.ts       → GET  /api/users/:id
│   │   ├── [id].put.ts       → PUT  /api/users/:id
│   │   └── [id].delete.ts    → DELETE /api/users/:id
│   └── health.get.ts         → GET  /api/health
├── routes/                   # Non-API routes
│   └── sitemap.xml.get.ts    → GET  /sitemap.xml
├── middleware/               # Server middleware
├── plugins/                  # Nitro plugins
└── utils/                    # Server utilities
```

### HTTP Method Suffixes

| Suffix | HTTP Method |
|--------|-------------|
| `.get.ts` | GET |
| `.post.ts` | POST |
| `.put.ts` | PUT |
| `.patch.ts` | PATCH |
| `.delete.ts` | DELETE |
| `.ts` | All methods |

## When to Load References

**Load `references/server.md` when:**
- Implementing complex API routes
- Handling authentication and sessions
- Working with cookies and headers
- Building file upload endpoints
- Migrating from h3 v1 to h3 v2 API

## Basic Event Handler

```typescript
// server/api/users/index.get.ts
export default defineEventHandler(async (event) => {
  return {
    users: [
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' }
    ]
  }
})
```

## Web Standard Event API (v5)

### Request Properties

```typescript
// Nuxt 5 uses Web Standard APIs
export default defineEventHandler((event) => {
  // Path
  const path = event.url.pathname    // was: event.path
  const search = event.url.search    // URLSearchParams

  // Method
  const method = event.req.method    // was: event.method

  // Headers (Web Headers API)
  const auth = event.req.headers.get('authorization')  // was: getHeader(event, 'authorization')
  const allHeaders = event.req.headers

  return { path, search, method, auth }
})
```

### Response Properties

```typescript
export default defineEventHandler((event) => {
  // Set status
  event.res.status = 201                    // was: setResponseStatus(event, 201)

  // Set headers (Web Headers API)
  event.res.headers.set('X-Custom', 'value')     // was: setHeader(event, 'X-Custom', 'value')
  event.res.headers.append('Set-Cookie', 'val')   // was: appendResponseHeader(event, ...)

  return { message: 'Created' }
})
```

### Legacy Helpers Still Work

The h3 v1 helper functions (auto-imported) still work for request reading:

```typescript
// These continue to work (auto-imported)
const id = getRouterParam(event, 'id')
const query = getQuery(event)
const body = await readBody(event)
const cookie = getCookie(event, 'name')
```

But for setting responses, prefer the Web Standard API:

```typescript
// Prefer v5 style
event.res.status = 201
event.res.headers.set('Cache-Control', 'max-age=3600')

// Still works but deprecated for setting
setResponseStatus(event, 201)
setHeader(event, 'Cache-Control', 'max-age=3600')
```

## Error Handling (v5 Change)

### Server-Side: HTTPError

In server routes, use `HTTPError` instead of `createError`:

```typescript
// Nuxt 5 server routes
import { HTTPError } from 'nitro/h3'

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw new HTTPError({ status: 400, statusText: 'User ID is required' })
  }

  const user = await findUser(id)

  if (!user) {
    throw new HTTPError({ status: 404, statusText: 'Not Found' })
  }

  return user
})
```

### App-Side: createError (Unchanged)

In the Vue part of your app (`app/` directory), `createError` continues to work:

```typescript
// app/ code - createError still works
throw createError({
  statusCode: 404,
  statusMessage: 'Page Not Found',
  fatal: true
})
```

### Validation Errors

```typescript
import { z } from 'zod'
import { HTTPError } from 'nitro/h3'

const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email()
})

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const result = createUserSchema.safeParse(body)

  if (!result.success) {
    throw new HTTPError({
      status: 400,
      statusText: 'Validation failed',
    })
  }

  return { success: true, data: result.data }
})
```

## Request Utilities

### URL Parameters

```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw new HTTPError({ status: 400, statusText: 'User ID is required' })
  }

  return { id }
})
```

### Query Parameters

```typescript
export default defineEventHandler(async (event) => {
  const query = getQuery(event)

  const page = Number(query.page) || 1
  const limit = Number(query.limit) || 10
  const search = query.search as string | undefined

  return { page, limit, search }
})
```

### Request Body

```typescript
export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  if (!body.name || !body.email) {
    throw new HTTPError({ status: 400, statusText: 'Name and email are required' })
  }

  return { success: true, user: { id: 1, ...body } }
})
```

## Cookies

```typescript
export default defineEventHandler(async (event) => {
  // Read cookie (helper still works)
  const sessionId = getCookie(event, 'session_id')

  // Set cookie
  setCookie(event, 'session_id', 'abc123', {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7
  })

  // Delete cookie
  deleteCookie(event, 'old_cookie')

  return { sessionId }
})
```

## Server Middleware

```typescript
// server/middleware/auth.ts
export default defineEventHandler(async (event) => {
  const publicRoutes = ['/api/auth/login', '/api/health']

  // v5: Use event.url.pathname instead of event.path
  if (publicRoutes.includes(event.url.pathname)) {
    return
  }

  const token = event.req.headers.get('authorization')?.replace('Bearer ', '')

  if (!token) {
    throw new HTTPError({ status: 401, statusText: 'Authentication required' })
  }

  const user = await verifyToken(token)
  event.context.user = user
})
```

## Runtime Config (v5 Change)

```typescript
// Nuxt 5: useRuntimeConfig() no longer accepts event
export default defineEventHandler(() => {
  const config = useRuntimeConfig()
  return { apiBase: config.public.apiBase }
})

// Nuxt 4 (deprecated in v5):
// const config = useRuntimeConfig(event)
```

## Database Integration

### Cloudflare D1 with Drizzle

```typescript
// server/utils/db.ts
import { drizzle } from 'drizzle-orm/d1'
import * as schema from '~/server/database/schema'

export function useDB(event: H3Event) {
  const { DB } = event.context.cloudflare.env
  return drizzle(DB, { schema })
}

// server/api/users/index.get.ts
export default defineEventHandler(async (event) => {
  const db = useDB(event)
  const users = await db.select().from(schema.users).limit(10)
  return { users }
})
```

### CRUD Operations

```typescript
// server/api/users/index.post.ts
import { users } from '~/server/database/schema'

export default defineEventHandler(async (event) => {
  const db = useDB(event)
  const body = await readBody(event)

  const [user] = await db.insert(users)
    .values({ name: body.name, email: body.email })
    .returning()

  return { user }
})

// server/api/users/[id].delete.ts
import { eq } from 'drizzle-orm'
import { users } from '~/server/database/schema'
import { HTTPError } from 'nitro/h3'

export default defineEventHandler(async (event) => {
  const db = useDB(event)
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw new HTTPError({ status: 400, statusText: 'ID is required' })
  }

  await db.delete(users).where(eq(users.id, Number(id)))
  return { success: true }
})
```

## File Uploads

```typescript
// server/api/upload.post.ts
import { HTTPError } from 'nitro/h3'

export default defineEventHandler(async (event) => {
  const formData = await readMultipartFormData(event)

  if (!formData) {
    throw new HTTPError({ status: 400, statusText: 'No file uploaded' })
  }

  const file = formData.find(f => f.name === 'file')

  if (!file) {
    throw new HTTPError({ status: 400, statusText: 'File field is required' })
  }

  const { R2 } = event.context.cloudflare.env
  const key = `uploads/${Date.now()}-${file.filename}`
  await R2.put(key, file.data)

  return { key, filename: file.filename, type: file.type }
})
```

## Server Utilities

```typescript
// server/utils/auth.ts
import { HTTPError } from 'nitro/h3'

export function requireAuth(event: H3Event) {
  const user = event.context.user

  if (!user) {
    throw new HTTPError({ status: 401, statusText: 'Authentication required' })
  }

  return user
}

export function requireRole(event: H3Event, role: string) {
  const user = requireAuth(event)

  if (user.role !== role) {
    throw new HTTPError({ status: 403, statusText: 'Insufficient permissions' })
  }

  return user
}
```

## Route Rules (v5 Change)

```typescript
// nuxt.config.ts - redirect status property renamed
export default defineNuxtConfig({
  routeRules: {
    '/old-page': {
      redirect: { to: '/new-page', status: 302 }  // was: statusCode
    },
    '/api/**': { cors: true },
    '/blog/**': { swr: 3600 }
  }
})
```

## Common Anti-Patterns

### Using createError in Server Routes

```typescript
// WRONG in v5 server routes - use HTTPError
import { createError } from 'h3'
throw createError({ statusCode: 404, statusMessage: 'Not found' })

// CORRECT in v5 server routes
import { HTTPError } from 'nitro/h3'
throw new HTTPError({ status: 404, statusText: 'Not found' })
```

### Using event.path

```typescript
// WRONG - deprecated in v5
const path = event.path

// CORRECT
const path = event.url.pathname
```

### Using useRuntimeConfig(event)

```typescript
// WRONG - no longer accepts event in v5
const config = useRuntimeConfig(event)

// CORRECT
const config = useRuntimeConfig()
```

### Not Throwing Errors

```typescript
// WRONG - Returns error as data with 200 status
if (!user) {
  return { error: 'Not found' }
}

// CORRECT - Throw error
if (!user) {
  throw new HTTPError({ status: 404, statusText: 'Not found' })
}
```

## Troubleshooting

**Import errors from 'h3':**
- Change `import { ... } from 'h3'` to `import { ... } from 'nitro/h3'`
- Auto-imports (`defineEventHandler`, `getQuery`, `readBody`) continue to work

**404 on API Routes:**
- Ensure file is in `server/api/`
- Check method suffix matches request (`.get.ts` for GET)

**Body is Empty:**
- Ensure `await readBody(event)` not `readBody(event)`

**D1 Binding Not Found:**
- Check wrangler.toml has `[[d1_databases]]` configured
- Access via `event.context.cloudflare.env.DB`

## Related Skills

- **nuxt-core**: Project setup, routing, configuration
- **nuxt-data**: Composables, data fetching, state
- **nuxt-production**: Performance, testing, deployment
- **cloudflare-d1**: D1 database patterns

---

**Version**: 5.0.0 | **Last Updated**: 2026-03-30 | **License**: MIT
