---
name: cross-platform-structured-logging
version: "1.0"
description: >
  Unified JSON logging across Next.js, Python, and Firebase Functions using Pino and structlog.
  PROACTIVELY activate for: (1) Setting up structured logging, (2) Configuring Pino for Node.js,
  (3) Configuring structlog for Python, (4) Implementing PII redaction, (5) Log correlation with trace IDs.
  Triggers: "logging", "pino", "winston", "structlog", "logger", "console.log", "firebase functions logger", "setup-logging", "json logging"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Cross-Platform Structured Logging

Establish unified, machine-readable JSON logging across all platforms for centralized aggregation, powerful querying, and correlation with distributed traces.

## Why Structured Logging

**Problem with traditional logging**:
```typescript
console.log('User ' + userId + ' logged in from ' + ip)
```

- Not machine-readable
- Hard to query
- No type safety
- Can't aggregate metrics

**Structured logging solution**:
```typescript
logger.info('User logged in', {
  user_id: userId,
  ip_address: ip,
  auth_method: 'oauth'
})
```

**Output (JSON)**:
```json
{
  "level": "info",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "message": "User logged in",
  "user_id": "user_123",
  "ip_address": "192.168.1.1",
  "auth_method": "oauth",
  "trace_id": "abc123...",
  "service": "api"
}
```

**Benefits**:
- Query: `user_id:user_123 AND level:error`
- Aggregate: Count logins by auth_method
- Correlate: Find all logs for trace_id

## Unified Log Schema

Use consistent field names across all platforms:

### Standard Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| level | string/number | Log severity | "info", 30 |
| timestamp | ISO 8601 | When event occurred | "2024-01-15T10:30:00.000Z" |
| message | string | Human-readable message | "User logged in" |
| service.name | string | Service identifier | "api", "web", "worker" |
| service.version | string | Deployment version | "1.2.3" |
| environment | string | Runtime environment | "production", "staging" |
| trace_id | string | OpenTelemetry trace ID | "abc123..." |
| span_id | string | OpenTelemetry span ID | "def456..." |
| user_id | string | User identifier | "user_789" |
| request_id | string | Request identifier | "req_xyz" |

### Context Fields (as needed)

```json
{
  "http": {
    "method": "POST",
    "url": "/api/users",
    "status_code": 201,
    "user_agent": "Mozilla/5.0..."
  },
  "error": {
    "type": "ValidationError",
    "message": "Invalid email",
    "stack": "Error: Invalid email\n  at..."
  }
}
```

## Node.js: Pino

Pino is the fastest JSON logger for Node.js.

### Basic Setup

```typescript
// lib/logger.ts
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',

  // Pretty print in development
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,

  // Base fields included in every log
  base: {
    service: {
      name: process.env.SERVICE_NAME || 'api',
      version: process.env.SERVICE_VERSION || '1.0.0'
    },
    environment: process.env.NODE_ENV || 'development'
  },

  // Redact sensitive fields
  redact: {
    paths: ['password', 'api_key', 'credit_card', '*.password', '*.token'],
    censor: '[REDACTED]'
  }
})

export default logger
```

### Usage

```typescript
import logger from '@/lib/logger'

// Simple message
logger.info('Server started')

// With context
logger.info({ user_id: '123', action: 'login' }, 'User logged in')

// Child logger (adds context to all subsequent logs)
const requestLogger = logger.child({ request_id: req.id })
requestLogger.info('Processing request')
requestLogger.error({ err }, 'Request failed')
```

### Middleware Integration (Next.js API Routes)

```typescript
// lib/logger-middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import logger from '@/lib/logger'

export function withLogging(
  handler: (req: NextRequest) => Promise<NextResponse>
) {
  return async (req: NextRequest) => {
    const requestLogger = logger.child({
      request_id: crypto.randomUUID(),
      http: {
        method: req.method,
        url: req.url
      }
    })

    requestLogger.info('Request started')

    try {
      const response = await handler(req)
      requestLogger.info({ status: response.status }, 'Request completed')
      return response
    } catch (error) {
      requestLogger.error({ err: error }, 'Request failed')
      throw error
    }
  }
}

// Usage in API route
export const GET = withLogging(async (req) => {
  // Your handler logic
})
```

### Production Configuration (Async Transport)

```typescript
// lib/logger.ts (production)
import pino from 'pino'

const logger = pino({
  level: 'info',

  // Don't use pino-pretty in production (performance)
  transport: process.env.NODE_ENV === 'production'
    ? {
        target: 'pino/file',
        options: { destination: 1 } // stdout
      }
    : { target: 'pino-pretty' },

  // Async logging (don't block event loop)
  destination: pino.destination({
    sync: false // Async mode
  })
})

export default logger
```

## Python: structlog

structlog integrates with Python's standard logging library.

### Basic Setup

```python
# logging_config.py
import structlog
import logging
import sys

def configure_logging():
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Configure structlog
    structlog.configure(
        processors=[
            # Add log level
            structlog.stdlib.add_log_level,

            # Add timestamp
            structlog.processors.TimeStamper(fmt="iso"),

            # Add calling location (file:line)
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ]
            ),

            # Format exceptions
            structlog.processors.format_exc_info,

            # Render as JSON
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Call at app startup
configure_logging()
```

### Usage

```python
import structlog

logger = structlog.get_logger()

# Simple message
logger.info("server_started", port=8000)

# With context
logger.info(
    "user_logged_in",
    user_id="user_123",
    auth_method="oauth"
)

# Error logging
try:
    risky_operation()
except Exception as e:
    logger.error("operation_failed", exc_info=e)
```

### FastAPI Integration

```python
# main.py
import structlog
from fastapi import FastAPI, Request
from uuid import uuid4

app = FastAPI()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid4())

    # Bind context for this request
    logger = structlog.get_logger().bind(
        request_id=request_id,
        method=request.method,
        path=request.url.path
    )

    logger.info("request_started")

    try:
        response = await call_next(request)
        logger.info("request_completed", status_code=response.status_code)
        return response
    except Exception as e:
        logger.error("request_failed", exc_info=e)
        raise
```

### Adding Trace Context

```python
# Integrate with OpenTelemetry
from opentelemetry import trace

logger = structlog.get_logger()

# Get current span
span = trace.get_current_span()
context = span.get_span_context()

# Log with trace context
logger.info(
    "database_query",
    trace_id=format(context.trace_id, '032x'),
    span_id=format(context.span_id, '016x'),
    query="SELECT * FROM users"
)
```

## Firebase Functions: Native Logger

Firebase provides a built-in logger optimized for Cloud Logging.

### Setup

```typescript
// src/utils/logger.ts
import { logger } from 'firebase-functions'

export function log(message: string, data?: Record<string, any>) {
  logger.info(message, {
    ...data,
    service: 'firebase-functions',
    environment: process.env.GCLOUD_PROJECT
  })
}

export function logError(message: string, error: Error, data?: Record<string, any>) {
  logger.error(message, {
    ...data,
    error: {
      type: error.name,
      message: error.message,
      stack: error.stack
    }
  })
}
```

### Usage

```typescript
import * as functions from 'firebase-functions'
import { log, logError } from './utils/logger'

export const myFunction = functions.https.onCall(async (data, context) => {
  log('Function called', {
    user_id: context.auth?.uid,
    data
  })

  try {
    const result = await processData(data)
    log('Function completed', { result })
    return result
  } catch (error) {
    logError('Function failed', error as Error, { data })
    throw error
  }
})
```

### Automatic Execution ID (2nd Gen Functions)

Cloud Run-based 2nd gen functions automatically inject execution_id:

```typescript
import { onRequest } from 'firebase-functions/v2/https'
import { logger } from 'firebase-functions'

export const myHttpFunction = onRequest(async (req, res) => {
  // execution_id automatically added by Cloud Run
  logger.info('Processing request', {
    path: req.path,
    method: req.method
  })
  // Output includes: execution_id, trace, span_id
})
```

## Security: PII Redaction

Never log sensitive data:

### Pino Redaction

```typescript
const logger = pino({
  redact: {
    paths: [
      'password',
      'api_key',
      'credit_card',
      'ssn',
      '*.password',
      '*.token',
      'req.headers.authorization'
    ],
    censor: '[REDACTED]'
  }
})

logger.info({ password: 'secret123' }, 'User created')
// Output: { "password": "[REDACTED]", "message": "User created" }
```

### structlog Redaction

```python
def redact_sensitive_data(logger, method_name, event_dict):
    """Processor to redact sensitive fields"""
    sensitive_fields = ['password', 'api_key', 'credit_card', 'ssn']

    for field in sensitive_fields:
        if field in event_dict:
            event_dict[field] = '[REDACTED]'

    return event_dict

structlog.configure(
    processors=[
        redact_sensitive_data,  # Add as first processor
        # ... other processors
    ]
)
```

## Anti-Patterns

### String Interpolation

```typescript
// BAD
logger.info(`User ${userId} logged in from ${ip}`)

// GOOD
logger.info('User logged in', { user_id: userId, ip_address: ip })
```

### console.log in Production

```typescript
// BAD
console.log('User logged in', userId)

// GOOD
logger.info('User logged in', { user_id: userId })
```

### Logging Sensitive Data

```typescript
// BAD
logger.info('Login attempt', { password: req.body.password })

// GOOD
logger.info('Login attempt', { email: req.body.email })
```

### Synchronous Logging (Node.js Production)

```typescript
// BAD (blocks event loop)
const logger = pino({ sync: true })

// GOOD (async)
const logger = pino({ sync: false })
```

## Log Levels

Use appropriate levels:

| Level | When to Use | Example |
|-------|-------------|---------|
| debug | Verbose development info | Function entry/exit |
| info | Normal operations | Request completed |
| warn | Unexpected but handled | Deprecated API used |
| error | Errors requiring attention | Database connection failed |
| fatal | App cannot continue | Out of memory |

## Best Practices

1. **Use structured data, not string interpolation**
2. **Redact PII and secrets automatically**
3. **Include trace_id in every log for correlation**
4. **Use child loggers for request-scoped context**
5. **Set appropriate log levels per environment**
6. **Use async transports in production (Node.js)**
7. **Include service.name for multi-service aggregation**

## Verification

Test structured logging:

```bash
# Start service and make request
curl http://localhost:3000/api/test

# Check logs (should be JSON)
cat logs.json | jq '.'

# Verify fields present
cat logs.json | jq 'select(.trace_id != null)'
```

Query in Google Cloud Logging:

```
resource.type="cloud_run_revision"
jsonPayload.user_id="user_123"
jsonPayload.trace_id="abc123..."
```
