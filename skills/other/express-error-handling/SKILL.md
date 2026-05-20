---
name: express-error-handling
description: >
  Express.js error handling patterns including async error catching, custom error classes,
  centralized error middleware, and the distinction between operational and programmer errors.
  Use when the user is handling errors in Express, writing async route handlers, creating
  custom error types, or debugging unhandled rejections. Trigger on mentions of Express error
  handling, async errors, error middleware, AppError, or unhandled exceptions in Node.js.
---

# Express Error Handling

Patterns for comprehensive, centralized error handling in Express.js applications.

## When to Use
- User is writing Express route handlers with async operations
- User needs custom error classes for different HTTP status codes
- User asks about centralized error handling
- User has unhandled promise rejections or uncaught exceptions
- User needs to distinguish between operational and programmer errors

## Core Patterns

### Custom Error Classes

Create a hierarchy of application errors that carry HTTP status codes and operational flags.

```typescript
export class AppError extends Error {
  readonly statusCode: number
  readonly isOperational: boolean

  constructor(message: string, statusCode: number, isOperational = true) {
    super(message)
    this.statusCode = statusCode
    this.isOperational = isOperational
    Object.setPrototypeOf(this, new.target.prototype)
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404)
  }
}

export class ValidationError extends AppError {
  readonly details: Record<string, string[]>

  constructor(details: Record<string, string[]>) {
    super('Validation failed', 400)
    this.details = details
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 401)
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(message, 403)
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 409)
  }
}
```

### Async Error Wrapper

Express does not catch errors from async route handlers automatically. Wrap them to forward errors to the error middleware.

```typescript
import { Request, Response, NextFunction, RequestHandler } from 'express'

function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<void>
): RequestHandler {
  return (req, res, next) => {
    fn(req, res, next).catch(next)
  }
}

// Usage -- errors are automatically forwarded to error middleware
router.get(
  '/users/:id',
  asyncHandler(async (req, res) => {
    const user = await db.user.findUnique({ where: { id: req.params.id } })
    if (!user) throw new NotFoundError('User')
    res.json({ data: user })
  })
)
```

### Centralized Error Middleware

A single error handler that formats all errors consistently. Must have exactly 4 parameters.

```typescript
import { Request, Response, NextFunction } from 'express'
import { AppError, ValidationError } from './errors'

interface ErrorResponse {
  error: string
  details?: Record<string, string[]>
  stack?: string
}

function errorHandler(err: Error, req: Request, res: Response, _next: NextFunction): void {
  if (err instanceof ValidationError) {
    const body: ErrorResponse = { error: err.message, details: err.details }
    res.status(err.statusCode).json(body)
    return
  }

  if (err instanceof AppError) {
    const body: ErrorResponse = { error: err.message }
    res.status(err.statusCode).json(body)
    return
  }

  // Programmer error -- do not leak internals
  console.error('Unexpected error:', err)
  const body: ErrorResponse = { error: 'Internal server error' }
  if (process.env.NODE_ENV === 'development') {
    body.stack = err.stack
  }
  res.status(500).json(body)
}

export { errorHandler }
```

### Operational vs Programmer Errors

Operational errors are expected (invalid input, resource not found, network timeout). Programmer errors are bugs (TypeError, undefined access). Handle them differently.

```typescript
// Operational -- expected, recoverable
throw new NotFoundError('User')
throw new ValidationError({ email: ['Invalid email format'] })

// Programmer -- unexpected, indicates a bug
// These should crash the process in production (after cleanup)
const user = undefined
user.name  // TypeError -- programmer error

// In production, catch unhandled errors and restart gracefully
process.on('uncaughtException', (err) => {
  console.error('UNCAUGHT EXCEPTION -- shutting down:', err)
  server.close(() => process.exit(1))
})

process.on('unhandledRejection', (reason) => {
  console.error('UNHANDLED REJECTION -- shutting down:', reason)
  server.close(() => process.exit(1))
})
```

### 404 Handler

Catch requests that do not match any route. Register after all routes but before the error handler.

```typescript
function notFoundHandler(req: Request, res: Response, _next: NextFunction): void {
  res.status(404).json({
    error: `Cannot ${req.method} ${req.path}`,
  })
}

// Registration order
app.use('/api', apiRoutes)
app.use(notFoundHandler)  // After routes
app.use(errorHandler)     // After 404
```

## Anti-Patterns

- **try/catch in every single route handler** -- Use the asyncHandler wrapper instead. Centralize error formatting in the error middleware, not in each handler.
- **Sending error response AND calling next(err)** -- This causes "headers already sent" errors. Do one or the other, never both.
- **Swallowing errors silently** -- `catch () {}` hides bugs. Always log unexpected errors and forward them to the error handler.
- **Leaking stack traces in production** -- Never send `err.stack` or internal details in production responses. Attackers use these to find vulnerabilities.
- **Treating all errors the same** -- A validation error (400) and a database connection failure (500) need different handling. Use the AppError hierarchy to distinguish them.

## Quick Reference

```
Error hierarchy:
  AppError (base)
    NotFoundError (404)
    ValidationError (400)
    UnauthorizedError (401)
    ForbiddenError (403)
    ConflictError (409)

Middleware registration order:
  1. Routes
  2. 404 handler (3 params)
  3. Error handler (4 params)

Async pattern:
  router.get('/path', asyncHandler(async (req, res) => { ... }))

Process-level:
  process.on('uncaughtException', ...)
  process.on('unhandledRejection', ...)
```
