---
name: error-monitoring
description: Expert guide for error handling, logging, monitoring, and debugging. Use when implementing error boundaries, logging systems, or integrating monitoring tools like Sentry.
---

# Error Monitoring & Logging Skill

## Overview

This skill helps you implement robust error handling, logging, and monitoring in your Next.js application. From local development to production monitoring, this covers everything you need to catch and fix issues.

## Error Boundaries (React)

### Basic Error Boundary
```typescript
// app/error.tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log error to your monitoring service
    console.error('Error caught:', error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Try again
      </button>
    </div>
  )
}
```

### Global Error Boundary
```typescript
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <h2>Application Error</h2>
        <p>{error.message}</p>
        <button onClick={reset}>Try again</button>
      </body>
    </html>
  )
}
```

### Nested Error Boundaries
```typescript
// app/dashboard/error.tsx
'use client'

export default function DashboardError({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div className="p-4">
      <h2>Dashboard Error</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Reload Dashboard</button>
    </div>
  )
}

// app/dashboard/settings/error.tsx - More specific
'use client'

export default function SettingsError({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div className="p-4">
      <h2>Settings Error</h2>
      <p>Failed to load settings: {error.message}</p>
      <button onClick={reset}>Reload Settings</button>
    </div>
  )
}
```

## Custom Error Classes

```typescript
// lib/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message)
    this.name = this.constructor.name
    Error.captureStackTrace(this, this.constructor)
  }
}

export class ValidationError extends AppError {
  constructor(message: string, public field?: string) {
    super(message, 'VALIDATION_ERROR', 400)
  }
}

export class AuthenticationError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 'AUTHENTICATION_ERROR', 401)
  }
}

export class AuthorizationError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(message, 'AUTHORIZATION_ERROR', 403)
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404)
  }
}

export class DatabaseError extends AppError {
  constructor(message: string) {
    super(message, 'DATABASE_ERROR', 500, false)
  }
}

// Usage
throw new ValidationError('Invalid email format', 'email')
throw new NotFoundError('User')
throw new AuthenticationError()
```

## Error Logger

```typescript
// lib/logger.ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error'

interface LogEntry {
  level: LogLevel
  message: string
  timestamp: string
  context?: Record<string, any>
  error?: Error
}

class Logger {
  private logs: LogEntry[] = []

  private log(level: LogLevel, message: string, context?: Record<string, any>, error?: Error) {
    const entry: LogEntry = {
      level,
      message,
      timestamp: new Date().toISOString(),
      context,
      error
    }

    this.logs.push(entry)

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      const color = {
        debug: '\x1b[36m',
        info: '\x1b[32m',
        warn: '\x1b[33m',
        error: '\x1b[31m'
      }[level]

      console.log(
        `${color}[${level.toUpperCase()}]\x1b[0m ${message}`,
        context || '',
        error || ''
      )
    }

    // Send to monitoring service in production
    if (process.env.NODE_ENV === 'production' && level === 'error') {
      this.sendToMonitoring(entry)
    }
  }

  debug(message: string, context?: Record<string, any>) {
    this.log('debug', message, context)
  }

  info(message: string, context?: Record<string, any>) {
    this.log('info', message, context)
  }

  warn(message: string, context?: Record<string, any>) {
    this.log('warn', message, context)
  }

  error(message: string, error?: Error, context?: Record<string, any>) {
    this.log('error', message, context, error)
  }

  private async sendToMonitoring(entry: LogEntry) {
    // Send to Sentry, LogRocket, etc.
    try {
      await fetch('/api/logs', {
        method: 'POST',
        body: JSON.stringify(entry)
      })
    } catch (e) {
      // Fallback: log to console
      console.error('Failed to send log to monitoring:', e)
    }
  }
}

export const logger = new Logger()

// Usage
logger.info('User logged in', { userId: '123' })
logger.error('Payment failed', error, { orderId: '456' })
```

## API Error Handling

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { AppError } from '@/lib/errors'
import { logger } from '@/lib/logger'

export async function GET(request: NextRequest) {
  try {
    const users = await db.users.findMany()
    return NextResponse.json({ users })
  } catch (error) {
    return handleApiError(error)
  }
}

function handleApiError(error: unknown): NextResponse {
  // Log error
  logger.error('API Error', error as Error)

  // Handle known errors
  if (error instanceof AppError) {
    return NextResponse.json(
      {
        error: error.message,
        code: error.code
      },
      { status: error.statusCode }
    )
  }

  // Handle Zod validation errors
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      {
        error: 'Validation failed',
        code: 'VALIDATION_ERROR',
        issues: error.issues
      },
      { status: 400 }
    )
  }

  // Handle database errors
  if (error.code === 'P2002') {  // Prisma unique constraint
    return NextResponse.json(
      {
        error: 'Resource already exists',
        code: 'DUPLICATE_ERROR'
      },
      { status: 409 }
    )
  }

  // Handle unexpected errors
  return NextResponse.json(
    {
      error: 'Internal server error',
      code: 'INTERNAL_ERROR'
    },
    { status: 500 }
  )
}
```

## Sentry Integration

### Setup
```typescript
// instrumentation.ts
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    await import('./sentry.server.config')
  }

  if (process.env.NEXT_RUNTIME === 'edge') {
    await import('./sentry.edge.config')
  }
}

// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  debug: false,
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,

  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
})

// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  debug: false,
})
```

### Using Sentry
```typescript
import * as Sentry from '@sentry/nextjs'

// Capture exception
try {
  await riskyOperation()
} catch (error) {
  Sentry.captureException(error, {
    tags: {
      section: 'payment',
    },
    extra: {
      userId: user.id,
      orderId: order.id,
    },
  })
  throw error
}

// Capture message
Sentry.captureMessage('Something went wrong', {
  level: 'warning',
  tags: { feature: 'checkout' },
})

// Set user context
Sentry.setUser({
  id: user.id,
  email: user.email,
  username: user.name,
})

// Add breadcrumb
Sentry.addBreadcrumb({
  category: 'auth',
  message: 'User logged in',
  level: 'info',
})
```

## Client-Side Error Tracking

```typescript
// components/error-tracker.tsx
'use client'

import { useEffect } from 'react'
import * as Sentry from '@sentry/nextjs'

export function ErrorTracker() {
  useEffect(() => {
    // Catch unhandled errors
    window.addEventListener('error', (event) => {
      Sentry.captureException(event.error)
    })

    // Catch unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      Sentry.captureException(event.reason)
    })
  }, [])

  return null
}

// app/layout.tsx
import { ErrorTracker } from '@/components/error-tracker'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ErrorTracker />
        {children}
      </body>
    </html>
  )
}
```

## Performance Monitoring

```typescript
// lib/performance.ts
export class PerformanceMonitor {
  private marks: Map<string, number> = new Map()

  start(label: string) {
    this.marks.set(label, performance.now())
  }

  end(label: string) {
    const start = this.marks.get(label)
    if (!start) return

    const duration = performance.now() - start
    this.marks.delete(label)

    logger.info(`Performance: ${label}`, { duration: `${duration.toFixed(2)}ms` })

    // Send to monitoring if slow
    if (duration > 1000) {
      Sentry.captureMessage(`Slow operation: ${label}`, {
        level: 'warning',
        extra: { duration },
      })
    }

    return duration
  }
}

export const perfMonitor = new PerformanceMonitor()

// Usage
perfMonitor.start('fetchUsers')
const users = await db.users.findMany()
perfMonitor.end('fetchUsers')
```

## Structured Logging

```typescript
// lib/structured-logger.ts
type LogContext = {
  userId?: string
  requestId?: string
  ip?: string
  userAgent?: string
  [key: string]: any
}

class StructuredLogger {
  private context: LogContext = {}

  setContext(context: LogContext) {
    this.context = { ...this.context, ...context }
  }

  clearContext() {
    this.context = {}
  }

  log(level: string, message: string, data?: any) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      ...this.context,
      ...data,
    }

    // In production, send to log aggregation service
    if (process.env.NODE_ENV === 'production') {
      this.sendToLogService(logEntry)
    } else {
      console.log(JSON.stringify(logEntry, null, 2))
    }
  }

  private async sendToLogService(entry: any) {
    // Send to DataDog, Logtail, etc.
  }

  info(message: string, data?: any) {
    this.log('info', message, data)
  }

  error(message: string, error?: Error, data?: any) {
    this.log('error', message, {
      ...data,
      error: {
        message: error?.message,
        stack: error?.stack,
        name: error?.name,
      },
    })
  }
}

export const structuredLogger = new StructuredLogger()

// Usage in API route
export async function POST(request: NextRequest) {
  const requestId = crypto.randomUUID()

  structuredLogger.setContext({
    requestId,
    ip: request.ip,
    userAgent: request.headers.get('user-agent'),
  })

  structuredLogger.info('Processing payment', { amount: 100 })

  try {
    await processPayment()
    structuredLogger.info('Payment successful')
  } catch (error) {
    structuredLogger.error('Payment failed', error)
    throw error
  } finally {
    structuredLogger.clearContext()
  }
}
```

## Error Recovery Strategies

```typescript
// lib/retry.ts
export async function retry<T>(
  fn: () => Promise<T>,
  options = { maxAttempts: 3, delay: 1000 }
): Promise<T> {
  let lastError: Error

  for (let attempt = 1; attempt <= options.maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      logger.warn(`Attempt ${attempt} failed`, { error: lastError.message })

      if (attempt < options.maxAttempts) {
        await new Promise((resolve) =>
          setTimeout(resolve, options.delay * attempt)
        )
      }
    }
  }

  throw lastError!
}

// Usage
const data = await retry(
  () => fetch('/api/data').then((r) => r.json()),
  { maxAttempts: 3, delay: 1000 }
)
```

## Best Practices Checklist

- [ ] Implement error boundaries at key levels
- [ ] Use custom error classes for different types
- [ ] Log errors with context (user, request ID, etc.)
- [ ] Send errors to monitoring service (Sentry)
- [ ] Handle expected errors gracefully
- [ ] Show user-friendly error messages
- [ ] Include retry logic for transient failures
- [ ] Monitor performance bottlenecks
- [ ] Set up alerts for critical errors
- [ ] Track error rates and trends
- [ ] Include request IDs for debugging
- [ ] Sanitize sensitive data from logs
- [ ] Test error scenarios

## When to Use This Skill

Invoke this skill when:
- Setting up error boundaries
- Implementing error logging
- Integrating Sentry or monitoring tools
- Handling API errors
- Creating custom error classes
- Debugging production issues
- Setting up performance monitoring
- Implementing retry logic
- Tracking user sessions
