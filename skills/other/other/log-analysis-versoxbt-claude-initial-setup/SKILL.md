---
name: log-analysis
description: >
  Implement structured logging and analyze logs to diagnose issues.
  Use when the user sets up logging, asks about log levels, needs to trace
  requests through distributed systems, or is analyzing log output to debug
  a problem. Apply when adding logging to any application.
---

# Log Analysis

Implement structured, queryable logging with proper levels and correlation IDs to enable fast diagnosis of production issues.

## When to Use

- Adding logging to an application or service
- Choosing appropriate log levels
- Debugging production issues via log output
- Setting up log aggregation (ELK, Datadog, CloudWatch)
- Tracing requests across multiple services

## Core Patterns

### Structured Logging (JSON)

Always log structured data, not interpolated strings:

```typescript
// BAD: Unstructured string logs
console.log(`User ${userId} failed to login from ${ip} with error: ${err.message}`);
// Hard to parse, search, and aggregate

// GOOD: Structured JSON logging
import pino from "pino";

const logger = pino({ level: "info" });

logger.error({
  event: "login_failed",
  userId,
  ip,
  error: err.message,
  errorCode: err.code,
}, "User login failed");
```

```python
# Python structured logging
import structlog

logger = structlog.get_logger()

logger.error(
    "login_failed",
    user_id=user_id,
    ip=ip,
    error=str(err),
    error_code=getattr(err, "code", None),
)
```

```go
// Go structured logging with slog
import "log/slog"

slog.Error("login failed",
    "event", "login_failed",
    "userId", userId,
    "ip", ip,
    "error", err.Error(),
)
```

### Log Levels

Use levels consistently across the entire application:

```
LEVEL    WHEN TO USE                              EXAMPLE
-----    -----------                              -------
error    Something failed, needs attention         Database connection lost
         Action: alert on-call, investigate        Payment processing failed

warn     Unexpected but handled, may need review   Rate limit approaching
         Action: review in daily triage            Deprecated API called

info     Normal but significant operations         User registered
         Action: none, useful for auditing         Order completed

debug    Detailed flow for development             Cache hit/miss
         Action: none, disabled in production      SQL query executed
```

```typescript
const logger = pino({ level: process.env.LOG_LEVEL || "info" });

// ERROR: Operation failed, requires investigation
logger.error({ orderId, error: err.message }, "Payment charge failed");

// WARN: Handled but notable
logger.warn({ userId, attempts: 4, max: 5 }, "Login attempt threshold approaching");

// INFO: Normal business events
logger.info({ orderId, total, itemCount }, "Order placed successfully");

// DEBUG: Development-time detail (disabled in production)
logger.debug({ query, params, durationMs: 12 }, "Database query executed");
```

### Correlation IDs for Request Tracing

Assign a unique ID to each request and propagate it through all logs and service calls:

```typescript
import { randomUUID } from "crypto";
import { AsyncLocalStorage } from "async_hooks";

const requestContext = new AsyncLocalStorage<{ correlationId: string }>();

// Middleware: assign correlation ID
function correlationMiddleware(req: Request, res: Response, next: NextFunction) {
  const correlationId = req.headers["x-correlation-id"] as string || randomUUID();
  res.setHeader("x-correlation-id", correlationId);

  requestContext.run({ correlationId }, () => next());
}

// Logger: include correlation ID automatically
function getLogger() {
  const ctx = requestContext.getStore();
  return logger.child({ correlationId: ctx?.correlationId });
}

// Usage in any handler or service
function processOrder(order: Order) {
  const log = getLogger();
  log.info({ orderId: order.id }, "Processing order");
  // All logs from this request share the same correlationId
}
```

Output enables tracing a single request across services:

```json
{"level":"info","correlationId":"abc-123","service":"api","msg":"Order received","orderId":"ord-1"}
{"level":"info","correlationId":"abc-123","service":"inventory","msg":"Stock reserved","orderId":"ord-1"}
{"level":"info","correlationId":"abc-123","service":"payment","msg":"Payment charged","orderId":"ord-1"}
{"level":"error","correlationId":"abc-123","service":"email","msg":"Notification failed","error":"SMTP timeout"}
```

### Log Context Enrichment

Add persistent context to every log entry from a scope:

```typescript
// Child loggers for adding scope context
const serviceLogger = logger.child({ service: "order-service", version: "2.1.0" });
const requestLogger = serviceLogger.child({ correlationId, userId });

// All logs from this request include service, version, correlationId, userId
requestLogger.info({ orderId }, "Order created");
```

```python
# Python: bind context to logger
logger = structlog.get_logger()
log = logger.bind(service="order-service", correlation_id=correlation_id, user_id=user_id)

log.info("order_created", order_id=order_id)
# Output includes all bound context automatically
```

### Analyzing Logs

```bash
# Search JSON logs with jq
# Find all errors for a specific correlation ID
cat app.log | jq 'select(.correlationId == "abc-123" and .level == "error")'

# Count errors by type in the last hour
cat app.log | jq 'select(.level == "error") | .event' | sort | uniq -c | sort -rn

# Find slow requests (> 1000ms)
cat app.log | jq 'select(.durationMs > 1000) | {path: .path, duration: .durationMs}'

# Trace a request across services
cat *.log | jq 'select(.correlationId == "abc-123")' | jq -s 'sort_by(.timestamp)'
```

## Anti-Patterns

### What NOT to Do

- **Logging sensitive data**: Never log passwords, tokens, credit card numbers, SSNs, or PII without masking.
- **String interpolation in log messages**: `logger.info(\`User ${id}\`)` defeats structured search. Use fields.
- **Logging inside tight loops**: Thousands of log entries per second saturate I/O and storage.
- **Inconsistent levels**: Using `error` for non-errors or `info` for debug-level detail makes filtering useless.
- **Missing context**: `logger.error("Failed")` — failed what? Add the operation, entity ID, and error.

```typescript
// BAD: Sensitive data in logs
logger.info({ password: user.password }, "User login");

// BAD: No context
logger.error("Something went wrong");

// BAD: Wrong level
logger.error("Cache miss for key: user:123");  // This is debug, not error

// GOOD: Masked sensitive data, full context, correct level
logger.info({ userId: user.id, email: maskEmail(user.email) }, "User login successful");
logger.error({ orderId, error: err.message, stack: err.stack }, "Payment processing failed");
logger.debug({ key: "user:123", hit: false }, "Cache lookup");
```

## Quick Reference

```
Log Levels:
  error   Operation failed, needs attention
  warn    Unexpected but handled
  info    Normal significant events
  debug   Development detail

Structured Logging Checklist:
  - JSON format, not string interpolation
  - Consistent field names across services
  - Correlation ID on every request
  - Timestamps in ISO 8601 (UTC)
  - Service name and version in every entry
  - Error entries include message + stack
  - No sensitive data (mask PII, tokens)

Libraries:
  Node.js:  pino, winston
  Python:   structlog, python-json-logger
  Go:       slog (stdlib), zap, zerolog
  Java:     SLF4J + Logback, Log4j2

Analysis:
  jq        Query JSON logs from the command line
  grep -c   Count occurrences
  tail -f   Follow log output in real time
```
