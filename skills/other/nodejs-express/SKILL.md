---
name: nodejs-express
description: Node.js + Express backend patterns. Use when building REST APIs, middleware, authentication, or backend services with Node.js/Express/TypeScript.
---

# Node.js + Express Patterns

## Project Structure
```
src/
  app.ts           # Express app, middleware setup
  server.ts        # HTTP server, port binding
  routes/          # Route definitions (auth.ts, users.ts)
  controllers/     # Request handlers
  services/        # Business logic
  models/          # Prisma/Mongoose models
  middleware/      # auth, error, validation
  types/           # TypeScript interfaces
  utils/           # Helpers
```

## App Setup
```typescript
// app.ts
import express from 'express'
import helmet from 'helmet'
import cors from 'cors'
import { errorHandler } from './middleware/error'

const app = express()

app.use(helmet())
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(','), credentials: true }))
app.use(express.json({ limit: '1mb' }))
app.use(express.urlencoded({ extended: true }))

app.use('/api/auth', authRouter)
app.use('/api/users', authenticate, usersRouter)

app.get('/health', (req, res) => res.json({ status: 'ok' }))

app.use(errorHandler)  // Must be last
export default app
```

## Controller Pattern (async error handling)
```typescript
// Wrap async handlers to catch errors automatically
const asyncHandler = (fn: RequestHandler): RequestHandler =>
  (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next)

export const getUser = asyncHandler(async (req, res) => {
  const user = await userService.findById(Number(req.params.id))
  if (!user) return res.status(404).json({ error: 'User not found' })
  res.json(user)
})
```

## Auth Middleware
```typescript
import jwt from 'jsonwebtoken'

export const authenticate: RequestHandler = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1]
  if (!token) return res.status(401).json({ error: 'No token' })
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload
    req.user = payload
    next()
  } catch {
    res.status(401).json({ error: 'Invalid token' })
  }
}
```

## Validation Middleware (Zod)
```typescript
import { z } from 'zod'

const validate = (schema: z.ZodSchema) => (req: Request, res: Response, next: NextFunction) => {
  const result = schema.safeParse(req.body)
  if (!result.success) return res.status(400).json({ errors: result.error.flatten() })
  req.body = result.data
  next()
}

const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().max(100)
})

router.post('/users', validate(CreateUserSchema), createUser)
```

## Error Handler
```typescript
export const errorHandler: ErrorRequestHandler = (err, req, res, next) => {
  console.error(err)
  const status = err.status || 500
  const message = status < 500 ? err.message : 'Internal server error'
  res.status(status).json({ error: message })
}
```

## Rules
- Use `helmet()` for security headers
- Use `express-rate-limit` on auth endpoints
- Validate ALL input with Zod (never trust req.body directly)
- Wrap all async handlers in asyncHandler (never unhandled promise rejections)
- Keep controllers thin — business logic in services
- Use `process.env` for config, validate at startup (crash fast if missing)
- Return 404 for missing resources, 400 for bad input, 401/403 for auth, 500 for server errors
