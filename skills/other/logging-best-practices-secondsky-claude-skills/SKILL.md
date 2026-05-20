---
name: logging-best-practices
description: Structured logging with proper levels, context, PII handling, centralized aggregation. Use for application logging, log management integration, distributed tracing, or encountering log bloat, PII exposure, missing context errors.
---

# Logging Best Practices

Implement secure, structured logging with proper levels and context.

## Log Levels

| Level | Use For | Production |
|-------|---------|------------|
| DEBUG | Detailed debugging | Off |
| INFO | Normal operations | On |
| WARN | Potential issues | On |
| ERROR | Errors with recovery | On |
| FATAL | Critical failures | On |

## Structured Logging (Winston)

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  defaultMeta: { service: 'api-service' },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'error.log', level: 'error' })
  ]
});

// Usage
logger.info('User logged in', { userId: '123', ip: '192.168.1.1' });
logger.error('Payment failed', { error: err.message, orderId: '456' });
```

## Request Context

```javascript
const { AsyncLocalStorage } = require('async_hooks');
const storage = new AsyncLocalStorage();

app.use((req, res, next) => {
  const context = {
    requestId: req.headers['x-request-id'] || uuid(),
    userId: req.user?.id
  };
  storage.run(context, next);
});

function log(level, message, meta = {}) {
  const context = storage.getStore() || {};
  logger.log(level, message, { ...context, ...meta });
}
```

## PII Sanitization

```javascript
const sensitiveFields = ['password', 'ssn', 'creditCard', 'token'];

function sanitize(obj) {
  const sanitized = { ...obj };
  for (const field of sensitiveFields) {
    if (sanitized[field]) sanitized[field] = '[REDACTED]';
  }
  if (sanitized.email) {
    sanitized.email = sanitized.email.replace(/(.{2}).*@/, '$1***@');
  }
  return sanitized;
}
```

## Best Practices

- Use structured JSON format
- Include correlation IDs across services
- Sanitize all PII before logging
- Use async logging for performance
- Implement log rotation
- Never log at DEBUG in production

## Additional Implementations

See [references/advanced-logging.md](references/advanced-logging.md) for:
- Python structlog setup
- Go zap high-performance logging
- ELK Stack integration
- AWS CloudWatch configuration
- OpenTelemetry tracing

## Never Do

- Log passwords or tokens
- Use console.log in production
- Log inside tight loops
- Include stack traces for client errors
