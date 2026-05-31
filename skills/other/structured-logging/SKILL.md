---
name: structured-logging
description: Comprehensive logging system design guide. Use when designing log architecture, establishing logging standards, adding observability, or debugging production issues. Covers centralized configuration, field standards, and distributed tracing.
---
# Structured Logging System Design

## Core Principles

- **Logs are data** — Treat every log as a queryable, structured data point
- **Single source of truth** — One logging configuration, used everywhere
- **Context is king** — Every log must be traceable to its source and request
- **Human + Machine readable** — Structured for parsing, clear for debugging
- **Progressive enhancement** — Start simple, add fields as needed
- **No secrets** — Never log passwords, tokens, or PII without masking

---

## System Architecture

### The Golden Rule

> **Configure once, use everywhere. Never instantiate loggers directly in business code.**

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Service A│  │ Service B│  │ Service C│  │ Handler D│        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │             │             │               │
│       └─────────────┴──────┬──────┴─────────────┘               │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              LOGGING INFRASTRUCTURE                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │   │
│  │  │ Logger      │  │ Context     │  │ Formatters &    │  │   │
│  │  │ Factory     │  │ Provider    │  │ Transformers    │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────┘  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT TARGETS                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Console  │  │   File   │  │ Log Agg. │  │  Metrics │        │
│  │ (Dev)    │  │ (Local)  │  │ (Prod)   │  │ (Alerts) │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
src/
├── lib/
│   └── logging/                    # Centralized logging infrastructure
│       ├── index.ts                # Public API exports
│       ├── logger.ts               # Core logger implementation
│       ├── context.ts              # Request context management
│       ├── formatters.ts           # Output formatters (JSON, pretty)
│       ├── transports.ts           # Output destinations
│       ├── middleware.ts           # Framework integrations
│       ├── decorators.ts           # Method decorators (optional)
│       └── types.ts                # Type definitions
├── modules/
│   ├── users/
│   │   └── user.service.ts         # Uses: import { logger } from '@/lib/logging'
│   └── orders/
│       └── order.service.ts        # Uses: import { logger } from '@/lib/logging'
└── main.ts                         # Initialize logging once at startup
```

### Anti-Patterns to Avoid

```typescript
// ❌ BAD: Creating loggers everywhere
class UserService {
  private logger = new Logger({ service: 'user' });  // Don't do this
}

class OrderService {
  private logger = new Logger({ service: 'order' }); // Duplicated config
}

// ❌ BAD: Inconsistent configuration
const logger1 = winston.createLogger({ format: json() });
const logger2 = winston.createLogger({ format: simple() }); // Different format!

// ❌ BAD: Direct console usage in production code
console.log('User created:', userId);  // No structure, no context

// ❌ BAD: Passing logger instances around
function processOrder(order: Order, logger: Logger) { } // Don't pass loggers
```

### Correct Patterns

```typescript
// ✅ GOOD: Single configuration, exported singleton
// lib/logging/index.ts
export const logger = createLogger(config);
export { getContextLogger } from './context';

// ✅ GOOD: Import from central location
// modules/users/user.service.ts
import { logger, getContextLogger } from '@/lib/logging';

class UserService {
  async createUser(data: CreateUserInput) {
    const log = getContextLogger();  // Gets context automatically
    log.info('Creating user', { email: data.email });
    // ...
  }
}

// ✅ GOOD: Configure once at application startup
// main.ts
import { initializeLogging } from '@/lib/logging';

initializeLogging({
  service: 'my-app',
  environment: process.env.NODE_ENV,
  level: process.env.LOG_LEVEL || 'info',
});
```

## Log Record Schema

### Tier 1: Essential Fields (Always Required)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `timestamp` | ISO 8601 | When the event occurred | `2025-12-16T10:30:00.123Z` |
| `level` | string | Log severity | `INFO`, `WARN`, `ERROR` |
| `message` | string | Human-readable description | `User login successful` |
| `service` | string | Service/application name | `user-auth` |

```json
{
  "timestamp": "2025-12-16T10:30:00.123Z",
  "level": "INFO",
  "message": "Payment processed successfully",
  "service": "payment-service"
}
```

### Tier 2: Tracing Fields (Distributed Systems)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `trace_id` | string | Request chain identifier (32 hex) | `7b2e4f1a9c3d8e5b6a1f2c3d4e5f6a7b` |
| `span_id` | string | Current operation ID (16 hex) | `1a2b3c4d5e6f7890` |
| `parent_span_id` | string | Parent operation ID | `0987654321fedcba` |
| `request_id` | string | HTTP request identifier | `req_abc123` |

```json
{
  "timestamp": "2025-12-16T10:30:00.123Z",
  "level": "INFO",
  "message": "Order created",
  "service": "order-service",
  "trace_id": "7b2e4f1a9c3d8e5b6a1f2c3d4e5f6a7b",
  "span_id": "1a2b3c4d5e6f7890",
  "request_id": "req_abc123"
}
```

### Tier 3: Context Fields (Debugging & Analysis)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `user_id` | string | User identifier (hashed if needed) | `usr_xyz789` |
| `method` | string | Function/method name | `OrderService.create` |
| `duration_ms` | number | Operation duration | `245` |
| `error_code` | string | Application error code | `ERR_PAYMENT_FAILED` |
| `error_message` | string | Error description | `Card declined` |
| `stack_trace` | string | Exception stack (ERROR only) | `...` |

### Tier 4: Environment Fields (Operations)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `env` | string | Deployment environment | `production` |
| `version` | string | Service version | `2.1.0` |
| `host` | string | Server hostname | `web-01` |
| `region` | string | Cloud region | `us-east-1` |
| `instance_id` | string | Container/instance ID | `i-0abc123` |

## Log Levels

### When to Use Each Level

| Level | When to Use | Production Visibility | Alert |
|-------|-------------|----------------------|-------|
| `TRACE` | Ultra-fine debugging | ❌ Off | No |
| `DEBUG` | Development diagnostics | ❌ Off | No |
| `INFO` | Normal business operations | ✅ On | No |
| `WARN` | Unexpected but recoverable | ✅ On | Optional |
| `ERROR` | Failures requiring attention | ✅ On | Yes |
| `FATAL` | Application cannot continue | ✅ On | Immediate |

### Level Selection Guide

```
DEBUG: Variable states, method entry/exit, detailed flow
       → "Processing item 5 of 10"
       → "Cache miss for key: user:123"

INFO:  Business milestones, successful operations
       → "User registered successfully"
       → "Order #123 shipped"
       → "Scheduled job completed: 50 records processed"

WARN:  Degraded service, retries, approaching limits
       → "Database connection slow (>2s), retrying"
       → "Rate limit at 80%, throttling soon"
       → "Deprecated API called, migrate to v2"

ERROR: Operation failures, exceptions, data issues
       → "Payment failed: card declined"
       → "Database query timeout after 3 retries"
       → "Invalid data format in message queue"

FATAL: Unrecoverable state, shutdown imminent
       → "Database connection lost, shutting down"
       → "Out of memory, cannot allocate"
       → "Critical configuration missing"
```

## Implementation Patterns

### Pattern 1: Basic Logger Setup

```typescript
// logger.ts
interface LogEntry {
  timestamp: string;
  level: string;
  message: string;
  service: string;
  trace_id?: string;
  span_id?: string;
  [key: string]: unknown;
}

class Logger {
  constructor(
    private service: string,
    private context: Record<string, unknown> = {}
  ) {}

  private log(level: string, message: string, data?: Record<string, unknown>) {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      service: this.service,
      ...this.context,
      ...data
    };
    console.log(JSON.stringify(entry));
  }

  debug(message: string, data?: Record<string, unknown>) {
    this.log('DEBUG', message, data);
  }

  info(message: string, data?: Record<string, unknown>) {
    this.log('INFO', message, data);
  }

  warn(message: string, data?: Record<string, unknown>) {
    this.log('WARN', message, data);
  }

  error(message: string, data?: Record<string, unknown>) {
    this.log('ERROR', message, data);
  }

  child(context: Record<string, unknown>): Logger {
    return new Logger(this.service, { ...this.context, ...context });
  }
}

export const logger = new Logger('my-service');
```

### Pattern 2: Request Context Propagation

```typescript
// middleware/logging.ts
import { AsyncLocalStorage } from 'async_hooks';
import { v4 as uuid } from 'uuid';

interface RequestContext {
  trace_id: string;
  span_id: string;
  request_id: string;
  user_id?: string;
}

export const requestContext = new AsyncLocalStorage<RequestContext>();

// Express middleware
export function loggingMiddleware(req, res, next) {
  const context: RequestContext = {
    trace_id: req.headers['x-trace-id'] || uuid().replace(/-/g, ''),
    span_id: uuid().substring(0, 16),
    request_id: req.headers['x-request-id'] || `req_${uuid().substring(0, 8)}`,
    user_id: req.user?.id
  };

  // Propagate to downstream services
  res.setHeader('x-trace-id', context.trace_id);
  res.setHeader('x-request-id', context.request_id);

  requestContext.run(context, () => next());
}

// Context-aware logger
export function getLogger() {
  const ctx = requestContext.getStore();
  return logger.child(ctx || {});
}
```

### Pattern 3: Operation Logging with Duration

```typescript
// utils/operation-logger.ts
export async function logOperation<T>(
  name: string,
  operation: () => Promise<T>,
  metadata?: Record<string, unknown>
): Promise<T> {
  const log = getLogger();
  const startTime = performance.now();

  log.info(`${name} started`, { operation: name, ...metadata });

  try {
    const result = await operation();
    const duration_ms = Math.round(performance.now() - startTime);

    log.info(`${name} completed`, {
      operation: name,
      duration_ms,
      status: 'success',
      ...metadata
    });

    return result;
  } catch (error) {
    const duration_ms = Math.round(performance.now() - startTime);

    log.error(`${name} failed`, {
      operation: name,
      duration_ms,
      status: 'failure',
      error_code: error.code || 'UNKNOWN',
      error_message: error.message,
      stack_trace: error.stack,
      ...metadata
    });

    throw error;
  }
}

// Usage
await logOperation('create_order', async () => {
  return orderService.create(orderData);
}, { order_id: orderData.id, user_id: userId });
```

### Pattern 4: Structured Error Logging

```typescript
// errors/logging.ts
interface ErrorContext {
  error_code: string;
  error_message: string;
  error_type: string;
  stack_trace?: string;
  original_error?: unknown;
}

export function logError(error: unknown, context?: Record<string, unknown>) {
  const log = getLogger();
  const errorContext: ErrorContext = normalizeError(error);

  log.error(errorContext.error_message, {
    ...errorContext,
    ...context
  });
}

function normalizeError(error: unknown): ErrorContext {
  if (error instanceof AppError) {
    return {
      error_code: error.code,
      error_message: error.message,
      error_type: error.constructor.name,
      stack_trace: error.stack
    };
  }

  if (error instanceof Error) {
    return {
      error_code: 'INTERNAL_ERROR',
      error_message: error.message,
      error_type: error.constructor.name,
      stack_trace: error.stack
    };
  }

  return {
    error_code: 'UNKNOWN_ERROR',
    error_message: String(error),
    error_type: 'Unknown',
    original_error: error
  };
}
```

## Best Practices

### DO ✅

```typescript
// Structured, queryable data
log.info('Order created', {
  order_id: 'ord_123',
  user_id: 'usr_456',
  total_amount: 99.99,
  currency: 'USD',
  items_count: 3
});

// Consistent field naming across services
// user_id (not userId, user-id, or uid)
// duration_ms (not duration, time_ms, or elapsed)

// Include correlation IDs in all logs
log.info('Processing payment', { trace_id, span_id, order_id });

// Use appropriate log levels
log.warn('Rate limit approaching', { current: 80, limit: 100 });
log.error('Payment failed', { error_code: 'CARD_DECLINED' });

// Log at boundaries (entry/exit points)
log.info('API request received', { method: 'POST', path: '/orders' });
log.info('API response sent', { status: 201, duration_ms: 145 });
```

### DON'T ❌

```typescript
// String concatenation (not queryable)
log.info(`User ${userId} created order ${orderId}`);

// Logging sensitive data
log.info('Login', { password: '...', credit_card: '...' });

// Inconsistent field names
log.info('Order', { orderId: '...' });  // another file uses order_id
log.info('Order', { order_id: '...' }); // inconsistent!

// Wrong log levels
log.error('Cache miss');  // Should be DEBUG
log.debug('Payment failed'); // Should be ERROR

// Missing context
log.error('Something went wrong'); // What? Where? Why?

// Logging entire objects (may contain secrets)
log.info('User data', { user }); // Might log password hash
```


## Extended Reference

Detailed material starting at `## Sensitive Data Handling` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
