---
name: sentry
description: Sentry error monitoring and performance tracing patterns for Next.js applications.
---

# Sentry Integration

Guidelines for using Sentry for error monitoring and performance tracing.

## Exception Catching

Use `Sentry.captureException(error)` in try/catch blocks:

```javascript
try {
  await riskyOperation();
} catch (error) {
  Sentry.captureException(error);
  throw error;
}
```

## Performance Tracing

Create spans for meaningful actions like button clicks, API calls, and function calls.

### UI Actions

```javascript
function handleClick() {
  Sentry.startSpan(
    { op: "ui.click", name: "Submit Form" },
    (span) => {
      span.setAttribute("formId", formId);
      submitForm();
    }
  );
}
```

### API Calls

```javascript
async function fetchData(id) {
  return Sentry.startSpan(
    { op: "http.client", name: `GET /api/items/${id}` },
    async () => {
      const response = await fetch(`/api/items/${id}`);
      return response.json();
    }
  );
}
```

## Configuration (Next.js)

Sentry initialization files:
- `sentry.client.config.ts` - Client-side
- `sentry.server.config.ts` - Server-side
- `sentry.edge.config.ts` - Edge runtime

Import with `import * as Sentry from "@sentry/nextjs"` - no need to initialize in other files.

### Basic Setup

```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enableLogs: true,
});
```

### With Console Logging

```javascript
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  integrations: [
    Sentry.consoleLoggingIntegration({ levels: ["log", "warn", "error"] }),
  ],
});
```

## Structured Logging

Use `logger.fmt` for template literals with variables:

```javascript
const { logger } = Sentry;

logger.trace("Starting connection", { database: "users" });
logger.debug(logger.fmt`Cache miss for: ${userId}`);
logger.info("Updated profile", { profileId: 345 });
logger.warn("Rate limit reached", { endpoint: "/api/data" });
logger.error("Payment failed", { orderId: "order_123" });
logger.fatal("Connection pool exhausted", { activeConnections: 100 });
```
