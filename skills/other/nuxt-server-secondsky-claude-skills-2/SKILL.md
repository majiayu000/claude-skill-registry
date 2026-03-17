---
name: nuxt-server
description: |
  Nuxt 4 server-side development with Nitro: API routes, server middleware,
  database integration, and backend patterns.

  Use when: creating server API routes, implementing server middleware,
  integrating databases (D1, PostgreSQL, Drizzle), handling file uploads,
  implementing WebSockets, or building backend logic with Nitro.

  Keywords: server routes, API routes, Nitro, defineEventHandler,
  getRouterParam, getQuery, readBody, setCookie, createError,
  server middleware, D1, Drizzle, PostgreSQL, WebSocket, file upload
license: MIT
metadata:
  version: 4.0.0
  author: Claude Skills Maintainers
  category: Framework
  framework: Nuxt
  framework-version: 4.x
  last-verified: 2025-12-28
---

# Nuxt 4 Server Development

Server routes, API patterns, and backend development with Nitro.

## Quick Reference

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
│   └── auth.ts               # Runs on every request
├── plugins/                  # Nitro plugins
│   └── database.ts           # Initialize database
└── utils/                    # Server utilities
    └── db.ts                 # Database helpers
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
- Understanding Nitro internals

**Load `references/database-patterns.md` when:**
- Integrating Cloudflare D1 with Drizzle
- Setting up PostgreSQL connections
- Implementing database migrations
- Building query patterns

**Load `references/websocket-patterns.md` when:**
- Implementing real-time features
- Building WebSocket endpoints
- Using Durable Objects for state

## Basic Event Handler

```typescript
// server/api/users/index.get.ts
export default defineEventHandler(async (event) => {
  // Return data (automatically serialized to JSON)
  return {
    users: [
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' }
    ]
  }
})
```

## Request Utilities

### URL Parameters

```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw createError({
      statusCode: 400,
      message: 'User ID is required'
    })
  }

  return { id }
})
```

### Query Parameters

```typescript
// GET /api/users?page=1&limit=10&search=john
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
// server/api/users/index.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  // Validate body
  if (!body.name || !body.email) {
    throw createError({
      statusCode: 400,
      message: 'Name and email are required'
    })
  }

  // Create user...
  return { success: true, user: { id: 1, ...body } }
})
```

### Headers

```typescript
export default defineEventHandler(async (event) => {
  // Read headers
  const authHeader = getHeader(event, 'authorization')
  const contentType = getHeader(event, 'content-type')

  // Set response headers
  setHeader(event, 'X-Custom-Header', 'value')
  setHeader(event, 'Cache-Control', 'max-age=3600')

  return { authHeader, contentType }
})
```

## Response Utilities

### Setting Status Code

```typescript
export default defineEventHandler(async (event) => {
  // Set status code
  setResponseStatus(event, 201)  // Created

  return { message: 'Resource created' }
})
```

### Redirects

```typescript
export default defineEventHandler(async (event) => {
  // Redirect
  return sendRedirect(event, '/new-location', 302)
})
```

### Error Handling

```typescript
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  const user = await findUser(id)

  if (!user) {
    throw createError({
      statusCode: 404,
      statusMessage: 'Not Found',
      message: `User with ID ${id} not found`
    })
  }

  return user
})
```

## Cookies

```typescript
export default defineEventHandler(async (event) => {
  // Read cookie
  const sessionId = getCookie(event, 'session_id')

  // Set cookie
  setCookie(event, 'session_id', 'abc123', {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7  // 1 week
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
  // Skip for public routes
  const publicRoutes = ['/api/auth/login', '/api/health']
  if (publicRoutes.includes(event.path)) {
    return  // Continue to next handler
  }

  // Check authentication
  const token = getHeader(event, 'authorization')?.replace('Bearer ', '')

  if (!token) {
    throw createError({
      statusCode: 401,
      message: 'Authentication required'
    })
  }

  // Verify token and attach user to context
  const user = await verifyToken(token)
  event.context.user = user
})
```

### Accessing Context in Routes

```typescript
// server/api/profile.get.ts
export default defineEventHandler(async (event) => {
  // User attached by middleware
  const user = event.context.user

  if (!user) {
    throw createError({ statusCode: 401, message: 'Not authenticated' })
  }

  return { user }
})
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

### Schema Definition

```typescript
// server/database/schema.ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: integer('created_at', { mode: 'timestamp' })
    .notNull()
    .$defaultFn(() => new Date())
})

export const posts = sqliteTable('posts', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  userId: integer('user_id').notNull().references(() => users.id),
  title: text('title').notNull(),
  content: text('content'),
  createdAt: integer('created_at', { mode: 'timestamp' })
    .notNull()
    .$defaultFn(() => new Date())
})
```

### CRUD Operations

```typescript
// server/api/users/index.post.ts
import { users } from '~/server/database/schema'
import { eq } from 'drizzle-orm'

export default defineEventHandler(async (event) => {
  const db = useDB(event)
  const body = await readBody(event)

  // Create
  const [user] = await db.insert(users)
    .values({ name: body.name, email: body.email })
    .returning()

  return { user }
})

// server/api/users/[id].put.ts
export default defineEventHandler(async (event) => {
  const db = useDB(event)
  const id = getRouterParam(event, 'id')
  const body = await readBody(event)

  // Update
  const [user] = await db.update(users)
    .set({ name: body.name })
    .where(eq(users.id, Number(id)))
    .returning()

  if (!user) {
    throw createError({ statusCode: 404, message: 'User not found' })
  }

  return { user }
})

// server/api/users/[id].delete.ts
export default defineEventHandler(async (event) => {
  const db = useDB(event)
  const id = getRouterParam(event, 'id')

  // Delete
  await db.delete(users).where(eq(users.id, Number(id)))

  return { success: true }
})
```

## Validation with Zod

```typescript
// server/api/users/index.post.ts
import { z } from 'zod'

const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional()
})

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  // Validate
  const result = createUserSchema.safeParse(body)

  if (!result.success) {
    throw createError({
      statusCode: 400,
      message: 'Validation failed',
      data: result.error.flatten()
    })
  }

  // Use validated data
  const { name, email, age } = result.data

  // Create user...
  return { success: true }
})
```

## File Uploads

```typescript
// server/api/upload.post.ts
export default defineEventHandler(async (event) => {
  const formData = await readMultipartFormData(event)

  if (!formData) {
    throw createError({ statusCode: 400, message: 'No file uploaded' })
  }

  const file = formData.find(f => f.name === 'file')

  if (!file) {
    throw createError({ statusCode: 400, message: 'File field is required' })
  }

  // file.filename - Original filename
  // file.type - MIME type
  // file.data - Buffer with file contents

  // Upload to R2 (Cloudflare)
  const { R2 } = event.context.cloudflare.env
  const key = `uploads/${Date.now()}-${file.filename}`
  await R2.put(key, file.data)

  return { key, filename: file.filename, type: file.type }
})
```

## Server Utilities

```typescript
// server/utils/auth.ts
import { H3Event } from 'h3'

export function requireAuth(event: H3Event) {
  const user = event.context.user

  if (!user) {
    throw createError({
      statusCode: 401,
      message: 'Authentication required'
    })
  }

  return user
}

export function requireRole(event: H3Event, role: string) {
  const user = requireAuth(event)

  if (user.role !== role) {
    throw createError({
      statusCode: 403,
      message: 'Insufficient permissions'
    })
  }

  return user
}

// Usage in routes
export default defineEventHandler(async (event) => {
  const user = requireAuth(event)
  // or
  const admin = requireRole(event, 'admin')
})
```

## Common Anti-Patterns

### Missing Method Suffix

```typescript
// WRONG - Handles all methods
// server/api/users.ts

// CORRECT - Explicit method
// server/api/users.get.ts   → GET
// server/api/users.post.ts  → POST
```

### Not Throwing Errors

```typescript
// WRONG - Returns error as data
export default defineEventHandler(async (event) => {
  const user = await findUser(id)
  if (!user) {
    return { error: 'Not found' }  // 200 status!
  }
})

// CORRECT - Throw error
export default defineEventHandler(async (event) => {
  const user = await findUser(id)
  if (!user) {
    throw createError({ statusCode: 404, message: 'Not found' })
  }
})
```

### Forgetting Async/Await

```typescript
// WRONG - Body not awaited
export default defineEventHandler((event) => {
  const body = readBody(event)  // Returns Promise!
})

// CORRECT
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
})
```

## Troubleshooting

**404 on API Routes:**
- Ensure file is in `server/api/` (not `app/api/`)
- Check method suffix matches request (`.get.ts` for GET)
- Verify file extension is `.ts`

**Body is Empty:**
- Ensure `await readBody(event)` not `readBody(event)`
- Check Content-Type header is set correctly
- For multipart, use `readMultipartFormData`

**Middleware Not Running:**
- Check file is in `server/middleware/`
- Middleware runs for ALL requests unless filtered

**D1 Binding Not Found:**
- Check wrangler.toml has `[[d1_databases]]` configured
- Access via `event.context.cloudflare.env.DB`

## Related Skills

- **nuxt-core**: Project setup, routing, configuration
- **nuxt-data**: Composables, data fetching, state
- **nuxt-production**: Performance, testing, deployment
- **cloudflare-d1**: D1 database patterns

---

**Version**: 4.0.0 | **Last Updated**: 2025-12-28 | **License**: MIT
