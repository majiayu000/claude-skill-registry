---
name: using-logging
description: Use structured logging with Pino throughout your application. Covers log levels, context, and workflow-safe logging patterns.
---

# Working with Logging

Use structured logging with Pino throughout your application. Covers log levels, context, and workflow-safe logging patterns.

## Implement Working with Logging

Use structured logging with Pino throughout your application. Covers log levels, context, and workflow-safe logging patterns.

**See:**

- Resource: `using-logging` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/using-logging

---

### Basic Logging

Import the logger and use it throughout your application:

```typescript
import { logger } from "@/lib/logging/logger";

// Info level for normal operations
logger.info("Server started", { port: 3000 });

// Warn level for recoverable issues
logger.warn("Rate limit reached", { endpoint: "/api/chat" });

// Error level with Error objects
logger.error(err, "Failed to process request");

// Debug level for development troubleshooting
logger.debug("Cache miss", { key: "user:123" });
```

### Structured Logging

Always include context as the first argument for structured logs:

```typescript
// Context object first, message second
logger.info({ userId: "123", action: "login" }, "User logged in");

// For errors, pass the error first
logger.error({ err, userId: "123", endpoint: "/api/chat" }, "Request failed");
```

### Log Levels

Use appropriate levels for different scenarios:

| Level | When to Use |
| `trace` | Detailed debugging (rarely used) |
| `debug` | Development troubleshooting |
| `info` | Normal operations, business events |
| `warn` | Recoverable issues, deprecation warnings |
| `error` | Failures that need attention |
| `fatal` | Critical failures, app cannot continue |

### Configuring Log Level

Set the `LOG_LEVEL` environment variable:

```env
# Show all logs including debug
LOG_LEVEL="debug"

# Production: only warnings and errors
LOG_LEVEL="warn"
```

Default is `info` if not set. Valid values: `trace`, `debug`, `info`, `warn`, `error`, `fatal`.

### Logging in API Routes

```typescript
import { logger } from "@/lib/logging/logger";

export async function POST(request: Request) {
  const start = Date.now();

  try {
    const result = await processRequest(request);

    logger.info(
      { duration: Date.now() - start, status: 200 },
      "Request completed",
    );

    return Response.json(result);
  } catch (err) {
    logger.error({ err, duration: Date.now() - start }, "Request failed");

    return Response.json({ error: "Internal error" }, { status: 500 });
  }
}
```

### Logging in Workflows

Workflow functions run in a restricted environment. Use the logger step wrapper:

```typescript
// src/workflows/chat/steps/logger.ts
import { logger } from "@/lib/logging/logger";

export async function log(
  level: "info" | "warn" | "error" | "debug",
  message: string,
  data?: Record<string, unknown>,
): Promise<void> {
  "use step";

  if (data) {
    logger[level](data, message);
  } else {
    logger[level](message);
  }
}
```

Then use it in workflows:

```typescript
import { log } from "./steps/logger";

export async function chatWorkflow({ chatId }) {
  "use workflow";

  await log("info", "Workflow started", { chatId });
}
```

---

## References

- [Pino Documentation](https://getpino.io/)
- [Pino Log Levels](https://getpino.io/#/docs/api?id=levels)
