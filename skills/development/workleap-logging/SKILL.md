---
name: workleap-logging
description: |
  Guide for Workleap's logging library (@workleap/logging) that provides structured, composable logging for frontend TypeScript applications.

  Use this skill when:
  (1) Setting up logging in a Workleap frontend application
  (2) Creating or configuring loggers (BrowserConsoleLogger, CompositeLogger)
  (3) Understanding log levels (debug, information, warning, error, critical)
  (4) Building complex log entries with chained segments (withText, withObject, withError)
  (5) Using logging scopes to group related log entries
  (6) Styling log output in browser console
  (7) Composing multiple loggers to send logs to different destinations
  (8) Filtering logs by severity level
  (9) Integrating logging with LogRocket or other telemetry tools
  (10) Reviewing logging-related changes in pull requests
  (11) Questions about logging best practices specific to wl-logging
---

# Workleap Logging (@workleap/logging)

A structured logging library for Workleap frontend applications. Provides composable, styled console logging with support for scopes, multiple log levels, and integration with telemetry tools.

## Installation

```bash
pnpm add @workleap/logging
```

## Core Concepts

### Loggers
- **BrowserConsoleLogger**: Outputs to browser console with styling support
- **CompositeLogger**: Forwards logs to multiple underlying loggers

### Log Levels (lowest to highest severity)
1. `debug` - Detailed diagnostic info for development
2. `information` - General application flow events
3. `warning` - Non-critical issues needing attention
4. `error` - Failures preventing functionality
5. `critical` - Severe errors risking data integrity

### Scopes
Group related log entries under a label. Useful for tracing operations or correlating events.

**IMPORTANT:** Only a `RootLogger` instance can start a scope. If the logger is typed as a `Logger` (e.g., when using `useLogger()` from Squide), you must cast it to `RootLogger` before starting a scope:

```ts
// Squide example:
import { useLogger } from "@squide/firefly";
import type { RootLogger } from "@workleap/logging";

const logger = useLogger();
(logger as RootLogger).startScope("User signup");
```

## API Reference

### BrowserConsoleLogger

```ts
import { BrowserConsoleLogger, LogLevel } from "@workleap/logging";

// Basic usage
const logger = new BrowserConsoleLogger();

// With minimum log level
const logger = new BrowserConsoleLogger({ logLevel: LogLevel.information });
```

### CompositeLogger

```ts
import { BrowserConsoleLogger, CompositeLogger } from "@workleap/logging";
import { LogRocketLogger } from "@workleap/telemetry"; // or from "@workleap/logrocket"

const logger = new CompositeLogger([
    new BrowserConsoleLogger(),
    new LogRocketLogger()
]);
```

### Logger Methods

**Simple logging:**
```ts
logger.debug("message");
logger.information("message");
logger.warning("message"); // or logger.warn("message")
logger.error("message");
logger.critical("message");
```

**Chained segments (complete chain with log method):**
```ts
logger
    .withText("Processing order")
    .withObject({ orderId: 123 })
    .withError(new Error("Failed"))
    .error();
```

**Styled text:**
```ts
logger.withText("Success", {
    style: { color: "green", fontWeight: "bold" }
}).information();
```

**Line breaks:**
```ts
logger
    .withText("Line 1")
    .withLineChange()
    .withText("Line 2")
    .debug();
```

### Scopes

```ts
const scope = logger.startScope("User signup");

scope.information("Form loaded");
scope.debug("Validating...");
scope.withText("Failed").withError(err).error();

// Output all scope entries
scope.end();

// Or dismiss without output
scope.end({ dismiss: true });
```

**Styled scope labels:**
```ts
// At creation
const scope = logger.startScope("Label", {
    labelStyle: { backgroundColor: "purple", color: "white" }
});

// At end (useful for status-based styling)
scope.end({
    labelStyle: { backgroundColor: "green", color: "white" }
});
```

### createCompositeLogger

Factory function to create a `CompositeLogger` instance from Workleap libraries standard logging API.

```ts
import { createCompositeLogger, BrowserConsoleLogger } from "@workleap/logging";
import { LogRocketLogger } from "@workleap/telemetry"; // or from "@workleap/logrocket"

const logger = createCompositeLogger(false, [new BrowserConsoleLogger(), new LogRocketLogger()]);
```

**Parameters:**
- `verbose`: Whether debug information should be logged. If no loggers are provided, creates with a `BrowserConsoleLogger` by default.
- `loggers`: Array of loggers to create the `CompositeLogger` with.

## LogRocket Integration

By default, LogRocket session replays exclude console output. To send log entries to LogRocket, use `LogRocketLogger` from `@workleap/telemetry` or `@workleap/logrocket`:

```ts
import { LogRocketLogger } from "@workleap/telemetry"; // or from "@workleap/logrocket"

const logger = new LogRocketLogger();
logger.debug("Application started!");
```

Use `CompositeLogger` to send logs to both browser console and LogRocket:

```ts
import { BrowserConsoleLogger, CompositeLogger } from "@workleap/logging";
import { LogRocketLogger } from "@workleap/telemetry"; // or from "@workleap/logrocket"

const logger = new CompositeLogger([
    new BrowserConsoleLogger(),
    new LogRocketLogger()
]);

logger.debug("Application started!"); // Processed by both loggers
```

## Common Patterns

### Application logger setup

```ts
import { BrowserConsoleLogger, CompositeLogger, LogLevel } from "@workleap/logging";

const isDev = process.env.NODE_ENV === "development";

const logger = new BrowserConsoleLogger({
    logLevel: isDev ? LogLevel.debug : LogLevel.information
});
```

### Error logging

```ts
try {
    await processOrder(orderId);
} catch (error) {
    logger
        .withText("Failed to process order")
        .withObject({ orderId })
        .withError(error as Error)
        .error();
}
```

### Feature/operation scoping

```ts
async function registerModule(moduleName: string) {
    const scope = logger.startScope(`${moduleName} registration`);

    try {
        scope.debug("Registering routes...");
        await registerRoutes();
        scope.debug("Routes registered");

        scope.debug("Fetching data...");
        await fetchData();
        scope.debug("Data loaded");

        scope.end({ labelStyle: { color: "green" } });
    } catch (error) {
        scope.withText("Registration failed").withError(error as Error).error();
        scope.end({ labelStyle: { color: "red" } });
        throw error;
    }
}
```

### Multi-destination logging

```ts
import { BrowserConsoleLogger, CompositeLogger, LogLevel } from "@workleap/logging";
import { LogRocketLogger } from "@workleap/telemetry"; // or from "@workleap/logrocket"

const logger = new CompositeLogger([
    new BrowserConsoleLogger({
        logLevel: LogLevel.error
    }),
    new LogRocketLogger({
        logLevel: LogLevel.debug
    })
]);
```

## Log Level Guidelines

| Environment | Recommended Level |
|-------------|-------------------|
| Development | `debug` |
| Production  | `information` |

## PR Review Checklist

When reviewing logging changes:
- Verify appropriate log levels (debug for diagnostics, error for failures)
- Check that errors include context (withObject) and stack traces (withError)
- Ensure scopes are properly ended (end() or end({ dismiss: true }))
- Confirm no sensitive data in log messages
- Verify CompositeLogger filters are set per environment

## Common Mistakes

1. **Forgetting to call log method**: Chained segments require `.debug()`, `.error()`, etc. to output
2. **Not ending scopes**: Always call `scope.end()` or logs won't output
3. **Using wrong log level**: Use `error` for failures, not `warning`
4. **Logging sensitive data**: Never log passwords, tokens, or PII
5. **Missing error context**: Always include `withObject()` for relevant data and `withError()` for exceptions
6. **Calling startScope on a non-RootLogger**: Only `RootLogger` instances can start scopes. When using `useLogger()` from Squide, cast to `RootLogger` first: `(logger as RootLogger).startScope("Label")`
