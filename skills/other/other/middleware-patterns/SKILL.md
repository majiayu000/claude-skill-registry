---
name: middleware-patterns
description: >
  Express middleware chain patterns including auth middleware, error middleware, rate limiting,
  CORS configuration, and request validation. Use when the user is building Express.js APIs,
  configuring middleware, implementing authentication guards, adding rate limiting, or setting
  up CORS. Trigger on any mention of Express middleware, request pipeline, auth guards, rate
  limiting, or Express CORS.
---

# Express Middleware Patterns

Patterns for building robust Express.js middleware chains.

## When to Use
- User is setting up an Express.js application middleware stack
- User needs authentication or authorization middleware
- User asks about rate limiting, CORS, or request validation
- User is debugging middleware execution order
- User needs to write custom middleware

## Core Patterns

### Middleware Execution Order

Middleware executes in the order it is registered. Order matters: authentication must run before authorization, and error handlers must be last.

```typescript
import express from 'express'

const app = express()

// 1. Built-in middleware
app.use(express.json({ limit: '10kb' }))
app.use(express.urlencoded({ extended: true }))

// 2. Security / CORS
app.use(corsMiddleware)

// 3. Rate limiting
app.use(rateLimiter)

// 4. Request logging
app.use(requestLogger)

// 5. Routes (with route-specific middleware)
app.use('/api/v1/auth', authRoutes)
app.use('/api/v1/users', authenticate, userRoutes)
app.use('/api/v1/admin', authenticate, authorize('admin'), adminRoutes)

// 6. 404 handler
app.use(notFoundHandler)

// 7. Error handler (must be last, must have 4 parameters)
app.use(errorHandler)
```

### Authentication Middleware

Verify tokens and attach user context to the request object.

```typescript
import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

interface AuthRequest extends Request {
  user?: { id: string; role: string }
}

function authenticate(req: AuthRequest, res: Response, next: NextFunction): void {
  const header = req.headers.authorization
  if (!header?.startsWith('Bearer ')) {
    res.status(401).json({ error: 'Missing authorization header' })
    return
  }

  const token = header.slice(7)
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as { id: string; role: string }
    req.user = { id: payload.id, role: payload.role }
    next()
  } catch {
    res.status(401).json({ error: 'Invalid or expired token' })
  }
}

function authorize(...roles: string[]) {
  return (req: AuthRequest, res: Response, next: NextFunction): void => {
    if (!req.user || !roles.includes(req.user.role)) {
      res.status(403).json({ error: 'Insufficient permissions' })
      return
    }
    next()
  }
}
```

### Rate Limiting

Protect endpoints from abuse. Use different limits for different routes.

```typescript
import rateLimit from 'express-rate-limit'

const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, try again later' },
})

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,                     // Strict limit for auth endpoints
  message: { error: 'Too many login attempts' },
})

app.use(globalLimiter)
app.use('/api/v1/auth/login', authLimiter)
```

### CORS Configuration

Configure Cross-Origin Resource Sharing for frontend clients.

```typescript
import cors from 'cors'

const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || []

const corsMiddleware = cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
})
```

### Request Validation Middleware

Validate request body, query, and params using Zod. Create a reusable factory.

```typescript
import { z, ZodSchema } from 'zod'
import { Request, Response, NextFunction } from 'express'

function validate(schema: {
  body?: ZodSchema
  query?: ZodSchema
  params?: ZodSchema
}) {
  return (req: Request, res: Response, next: NextFunction): void => {
    const errors: Record<string, unknown> = {}

    if (schema.body) {
      const result = schema.body.safeParse(req.body)
      if (!result.success) errors.body = result.error.flatten()
    }
    if (schema.query) {
      const result = schema.query.safeParse(req.query)
      if (!result.success) errors.query = result.error.flatten()
    }
    if (schema.params) {
      const result = schema.params.safeParse(req.params)
      if (!result.success) errors.params = result.error.flatten()
    }

    if (Object.keys(errors).length > 0) {
      res.status(400).json({ error: 'Validation failed', details: errors })
      return
    }
    next()
  }
}

// Usage
const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
})

router.post('/users', validate({ body: CreateUserSchema }), createUser)
```

## Anti-Patterns

- **Forgetting to call `next()`** -- Every middleware must call `next()` or send a response. Forgetting causes the request to hang indefinitely.
- **Error handler with 3 parameters** -- Express only recognizes error middleware if it has exactly 4 parameters: `(err, req, res, next)`. Three parameters means it is treated as regular middleware.
- **Registering error handlers before routes** -- Error handlers must come after all routes and other middleware. Express routes to the first matching handler.
- **Blocking the event loop in middleware** -- Synchronous CPU-heavy operations (bcrypt with high rounds, large JSON parsing) block all requests. Use async alternatives or worker threads.
- **Applying auth middleware globally when some routes are public** -- Apply auth selectively to protected route groups, not to the entire app.

## Quick Reference

```
Middleware signature:  (req, res, next) => void
Error middleware:      (err, req, res, next) => void

Order: parsing -> security -> rate-limit -> logging -> routes -> 404 -> errors

Route-specific:  router.get('/path', middleware1, middleware2, handler)
Router-level:    router.use(middleware)
App-level:       app.use(middleware)
```
