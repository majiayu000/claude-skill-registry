---
name: cloudflare-workers
description: >
  Cloudflare Workers essentials - Hono routing, middleware, request handling, bindings.
  Trigger: When working with Cloudflare Workers, Hono framework, serverless APIs, edge computing.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Critical Patterns

### Basic Hono App

```typescript
import { Hono } from "hono"

type Env = {
  DB: D1Database
  MY_BUCKET: R2Bucket
  API_KEY: string
}

const app = new Hono<{ Bindings: Env }>()

app.get("/", (c) => c.text("Hello!"))

app.get("/api/users", async (c) => {
  const users = await c.env.DB.prepare("SELECT * FROM users").all()
  return c.json(users.results)
})

export default app
```

### Routes

```typescript
// GET, POST, PUT, DELETE
app.get("/users", (c) => c.json({ users: [] }))
app.post("/users", async (c) => {
  const body = await c.req.json()
  return c.json({ created: true }, 201)
})

// Dynamic params
app.get("/users/:id", (c) => {
  const id = c.req.param("id")
  return c.json({ id })
})

// Multiple params
app.get("/posts/:postId/comments/:commentId", (c) => {
  const postId = c.req.param("postId")
  const commentId = c.req.param("commentId")
  return c.json({ postId, commentId })
})

// Query params
app.get("/search", (c) => {
  const query = c.req.query("q")
  const page = c.req.query("page") || "1"
  return c.json({ query, page })
})
```

### Request Handling

```typescript
app.post("/api/data", async (c) => {
  // JSON body
  const body = await c.req.json()
  
  // Form data
  const formData = await c.req.formData()
  const file = formData.get("file")
  
  // Headers
  const auth = c.req.header("Authorization")
  
  // Cookies
  const sessionId = c.req.cookie("session_id")
  
  return c.json({ success: true })
})
```

### Response Types

```typescript
// JSON
app.get("/json", (c) => c.json({ message: "Hello" }, 200))

// Text
app.get("/text", (c) => c.text("Plain text"))

// HTML
app.get("/html", (c) => c.html("<h1>Hello</h1>"))

// Redirect
app.get("/redirect", (c) => c.redirect("/new-location", 301))

// Custom
app.get("/custom", (c) => {
  return new Response("Custom", {
    status: 200,
    headers: { "X-Custom": "value" }
  })
})
```

### Middleware

```typescript
// Global logging
app.use('*', async (c, next) => {
  console.log(`[${c.req.method}] ${c.req.url}`)
  await next()
})

// Auth middleware
const authMiddleware = async (c, next) => {
  const token = c.req.header("Authorization")
  
  if (!token || !token.startsWith("Bearer ")) {
    return c.json({ error: "Unauthorized" }, 401)
  }
  
  const user = await verifyToken(token.substring(7))
  c.set("user", user) // Store in context
  await next()
}

// Apply to routes
app.use('/api/*', authMiddleware)

// Access in route
app.get('/api/profile', (c) => {
  const user = c.get("user")
  return c.json({ user })
})

// CORS
import { cors } from "hono/cors"

app.use('*', cors({
  origin: ["https://yourapp.com"],
  allowMethods: ["GET", "POST", "PUT", "DELETE"],
  credentials: true
}))

// Error handler
app.onError((err, c) => {
  console.error(err)
  return c.json({ error: "Internal Error" }, 500)
})

// 404 handler
app.notFound((c) => c.json({ error: "Not Found" }, 404))
```

### Grouped Routes

```typescript
const api = new Hono()

api.get("/users", (c) => c.json({ users: [] }))
api.post("/users", (c) => c.json({ created: true }))
api.get("/users/:id", (c) => c.json({ id: c.req.param("id") }))

// Mount group
app.route("/api", api)

// Routes: /api/users, /api/users/:id
```

### Background Tasks

```typescript
app.post("/analytics", async (c) => {
  const event = await c.req.json()
  
  // Run in background (non-blocking)
  c.executionCtx.waitUntil(
    fetch("https://analytics.example.com/track", {
      method: "POST",
      body: JSON.stringify(event)
    })
  )
  
  return c.json({ success: true })
})
```

### Fetch API (Proxy)

```typescript
app.get("/proxy", async (c) => {
  const response = await fetch("https://api.example.com", {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${c.env.API_KEY}`,
      "Content-Type": "application/json"
    }
  })
  
  if (!response.ok) {
    return c.json({ error: "Failed" }, response.status)
  }
  
  const data = await response.json()
  return c.json(data)
})
```

## Complete REST API Example

```typescript
import { Hono } from "hono"
import { cors } from "hono/cors"

const app = new Hono<{ Bindings: Env }>()

// Middleware
app.use('*', cors())

// Health check
app.get("/health", (c) => c.json({ status: "ok" }))

// API routes
const api = new Hono()

api.get("/users", async (c) => {
  const users = await c.env.DB.prepare("SELECT * FROM users").all()
  return c.json(users.results)
})

api.post("/users", async (c) => {
  const { name, email } = await c.req.json()
  
  const result = await c.env.DB.prepare(
    "INSERT INTO users (name, email) VALUES (?, ?)"
  ).bind(name, email).run()
  
  return c.json({ id: result.meta.last_row_id }, 201)
})

api.get("/users/:id", async (c) => {
  const id = c.req.param("id")
  const user = await c.env.DB.prepare(
    "SELECT * FROM users WHERE id = ?"
  ).bind(id).first()
  
  if (!user) {
    return c.json({ error: "Not found" }, 404)
  }
  
  return c.json(user)
})

api.delete("/users/:id", async (c) => {
  const id = c.req.param("id")
  await c.env.DB.prepare("DELETE FROM users WHERE id = ?").bind(id).run()
  return c.json({ success: true })
})

app.route("/api", api)

// Handlers
app.notFound((c) => c.json({ error: "Not Found" }, 404))
app.onError((err, c) => {
  console.error(err)
  return c.json({ error: "Internal Error" }, 500)
})

export default app
```

## Performance Tips

```typescript
// ✅ Use waitUntil for non-blocking tasks
c.executionCtx.waitUntil(logAnalytics(event))
return c.json({ success: true })

// ❌ Don't await non-critical tasks
await logAnalytics(event) // Blocks response
return c.json({ success: true })

// ✅ Cache responses
app.get("/static-data", (c) => {
  return c.json(data, 200, {
    "Cache-Control": "public, max-age=3600"
  })
})

// ✅ Stream large responses
app.get("/large-file", async (c) => {
  const object = await c.env.BUCKET.get("large.json")
  return new Response(object.body)
})
```

## Commands

```bash
# Init worker
wrangler init my-worker

# Dev server
wrangler dev

# Deploy
wrangler deploy

# Tail logs
wrangler tail
```

## Resources

- **Docs**: [developers.cloudflare.com/workers](https://developers.cloudflare.com/workers)
- **Hono**: [hono.dev](https://hono.dev)
