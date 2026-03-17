---
name: api-observability-axiom-pino-sentry
description: Pino logging, Sentry error tracking, Axiom - structured logging with correlation IDs, error boundaries, performance monitoring, alerting
---

# Observability Patterns (Logging, Tracing, Error Handling)

> **Quick Guide:** Structured logging with Pino (debug/info/warn/error). Correlation IDs for request tracing. Sentry error boundaries in React. Attach user context after auth. Filter expected errors (404s). Create Axiom monitors for alerts.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST include correlation ID in ALL log statements for request tracing)**

**(You MUST use structured logging with required fields: level, message, correlationId, timestamp)**

**(You MUST filter expected errors (404, validation) from Sentry to avoid quota waste)**

**(You MUST attach user context to Sentry AFTER authentication completes)**

**(You MUST use child loggers with context instead of repeating fields in every log call)**

</critical_requirements>

---

**Auto-detection:** log, logger, pino, Sentry, error boundary, correlation ID, trace, span, observability, monitoring, alerting

**When to use:**

- Adding logging to new feature code
- Implementing error handling patterns
- Setting up request tracing with correlation IDs
- Creating custom traces and spans for performance debugging
- Configuring Sentry error boundaries in React components
- Creating Axiom monitors and alerts

**When NOT to use:**

- Initial project setup (use `setup/observability.md` instead)
- Installing dependencies (use `setup/observability.md` instead)
- Configuring `next.config.js` (use `setup/observability.md` instead)

**Key patterns covered:**

- Log levels decision tree (when to use debug/info/warn/error)
- Structured logging with required fields
- Correlation IDs: generating, propagating, attaching to logs
- Custom traces/spans with OpenTelemetry
- Sentry error boundaries in React (App Router compatible)
- Attaching user context to Sentry after auth
- Creating Axiom monitors and alerts
- Filtering noise (expected errors like 404s)
- Performance monitoring patterns
- Debugging guide: tracing a request through the system

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md) (essential patterns always loaded)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Extended Examples:**

- [examples/correlation-ids.md](examples/correlation-ids.md) - Middleware for request tracing
- [examples/tracing.md](examples/tracing.md) - OpenTelemetry spans and custom instrumentation
- [examples/error-boundaries.md](examples/error-boundaries.md) - React error boundaries with Sentry
- [examples/sentry-config.md](examples/sentry-config.md) - User context and error filtering
- [examples/axiom.md](examples/axiom.md) - Monitors, alerts, and debugging queries
- [examples/performance.md](examples/performance.md) - Query and API call tracking

---

<philosophy>

## Philosophy

**Good observability answers three questions:**

1. **What happened?** (Structured logs with context)
2. **Why did it happen?** (Error tracking with stack traces)
3. **How do I find it?** (Correlation IDs linking related events)

Logging should be **intentional, not defensive**. Every log statement should answer a specific question you might ask when debugging. Avoid logging "just in case" - it creates noise that makes real issues harder to find.

**This skill covers ongoing usage patterns. For initial setup (dependencies, configuration), see `setup/observability.md`.**

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Log Levels Decision Tree

Choose the appropriate log level based on the situation.

```
What are you logging?
├─ Development-only debugging info?
│   └─ debug (filtered in production)
├─ Normal operation events?
│   ├─ Request started/completed → info
│   ├─ User action completed → info
│   └─ Background job finished → info
├─ Something unexpected but recoverable?
│   ├─ Retry attempt → warn
│   ├─ Fallback used → warn
│   └─ Deprecation notice → warn
└─ Something that needs attention?
    ├─ Unhandled exception → error
    ├─ External service failure → error
    └─ Data integrity issue → error
```

**Level Guidelines:**

| Level   | Production      | When to Use                                        |
| ------- | --------------- | -------------------------------------------------- |
| `debug` | Filtered        | Development debugging, verbose tracing             |
| `info`  | Visible         | Normal operations, request lifecycle, user actions |
| `warn`  | Visible         | Recoverable issues, retries, fallbacks             |
| `error` | Visible + Alert | Unrecoverable issues, failures, exceptions         |

For code examples, see [examples/core.md](examples/core.md#pattern-1-log-levels).

---

### Pattern 2: Structured Logging with Required Fields

Every log statement should include structured context for searchability.

**Required Fields:**

| Field           | Type    | Purpose                                               |
| --------------- | ------- | ----------------------------------------------------- |
| `correlationId` | string  | Links all logs from same request                      |
| `service`       | string  | Identifies the service (api, web, worker)             |
| `operation`     | string  | What action is being performed                        |
| `userId`        | string? | User performing the action (if authenticated)         |
| `duration`      | number? | Time taken in milliseconds (for completed operations) |

For code examples, see [examples/core.md](examples/core.md#pattern-2-structured-logging).

---

### Pattern 3: Correlation IDs for Request Tracing

Generate and propagate correlation IDs to trace requests across services.

**Key Components:**

1. **Correlation ID Middleware** - Generates/extracts correlation ID from headers
2. **Request Logger Middleware** - Creates request-scoped logger with correlation context
3. **Route Handler Usage** - Child loggers inherit correlation ID automatically

**Modern Alternative: AsyncLocalStorage + Mixin**

For larger applications, use AsyncLocalStorage with Pino's `mixin` option for automatic context injection without manual child logger creation in every handler.

For implementation examples of both approaches, see [examples/correlation-ids.md](examples/correlation-ids.md).

---

### Pattern 4: Custom Traces and Spans with OpenTelemetry

Add custom instrumentation for performance debugging.

**Key Utilities:**

- `withSpan()` - Wrap async operations in traced spans
- `createSpan()` - Create simple spans for synchronous operations

For code examples, see [examples/tracing.md](examples/tracing.md).

---

### Pattern 5: Sentry Error Boundaries in React (App Router)

Catch and report React component errors with recovery capability.

**Key Components:**

1. **ErrorBoundary** - Class component for catching render errors
2. **global-error.tsx** - App Router global error handler
3. **Feature-level boundaries** - Wrap feature sections with custom fallbacks

For implementation examples, see [examples/error-boundaries.md](examples/error-boundaries.md).

---

### Pattern 6: Attaching User Context to Sentry

Add user information to Sentry after authentication for better debugging.

**Key Functions:**

- `setSentryUser()` - Call after successful authentication
- `clearSentryUser()` - Call on logout
- `setSentryContext()` - Add additional context per-feature

For code examples, see [examples/sentry-config.md](examples/sentry-config.md#pattern-setting-user-context).

---

### Pattern 7: Filtering Expected Errors

Prevent expected errors from polluting Sentry quota and alerts.

**Filtering Strategies:**

1. **beforeSend hook** - Filter by error message patterns
2. **HTTP status filtering** - Skip 404, 401, 403
3. **beforeBreadcrumb hook** - Remove noisy console.log breadcrumbs

For configuration examples, see [examples/sentry-config.md](examples/sentry-config.md#pattern-error-filtering-configuration).

---

### Pattern 8: Creating Axiom Monitors and Alerts

Set up proactive monitoring for production issues.

**Monitor Types:**

1. **Error Rate Monitor** - Alert when error rate > 1%
2. **Latency Monitor** - Alert when P95 > 2 seconds
3. **Specific Error Monitor** - Alert on database connection errors

For APL query examples, see [examples/axiom.md](examples/axiom.md#pattern-axiom-monitors).

---

### Pattern 9: Performance Monitoring Patterns

Track and optimize slow operations.

**Tracking Utilities:**

- `trackedQuery()` - Wrap database queries with performance tracking
- `trackedApiCall()` - Wrap external API calls with performance tracking

For implementation examples, see [examples/performance.md](examples/performance.md).

---

### Pattern 10: Debugging Guide - Tracing a Request

How to trace a request through the system when debugging.

**Steps:**

1. Get correlation ID from response headers, Sentry, or user report
2. Search Axiom for all logs with that correlation ID
3. Analyze request flow with timeline view
4. Find related errors and stack traces
5. Check Sentry for additional context

For detailed APL queries and checklist, see [examples/axiom.md](examples/axiom.md#pattern-debugging-guide---tracing-a-request).

</patterns>

---

<integration>

## Integration Guide

**Works with:**

- **setup/observability.md**: Initial configuration this skill builds upon
- **backend/api.md**: Hono middleware for logging and correlation IDs
- **backend/database.md**: Drizzle query logging patterns
- **frontend/react.md**: Error boundary patterns

**Related Patterns:**

- Use correlation ID middleware from Pattern 3 in all Hono routes
- Use error boundaries from Pattern 5 around feature sections
- Use performance wrappers from Pattern 9 for external calls

</integration>

---

<red_flags>

## RED FLAGS

For comprehensive anti-patterns and red flags, see [reference.md](reference.md#red-flags).

**Quick Reference - High Priority Issues:**

- Missing correlation ID in logs - Impossible to trace requests
- Using `console.log` instead of structured logger - Not searchable, no levels
- Logging sensitive data - Security vulnerability
- Not filtering expected errors in Sentry - Wastes quota, buries real issues
- Error logs without stack traces - Can't debug without knowing where error occurred

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST include correlation ID in ALL log statements for request tracing)**

**(You MUST use structured logging with required fields: level, message, correlationId, timestamp)**

**(You MUST filter expected errors (404, validation) from Sentry to avoid quota waste)**

**(You MUST attach user context to Sentry AFTER authentication completes)**

**(You MUST use child loggers with context instead of repeating fields in every log call)**

**Failure to follow these rules will result in untraceable requests, wasted Sentry quota, and impossible debugging.**

</critical_reminders>
