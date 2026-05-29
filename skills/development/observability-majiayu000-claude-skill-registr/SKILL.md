---
name: Observability
description: This skill should be used when the user asks about "Effect logging", "Effect.log", "Effect metrics", "Effect tracing", "spans", "telemetry", "Metric.counter", "Metric.gauge", "Metric.histogram", "OpenTelemetry", "structured logging", "log levels", "Effect.logDebug", "Effect.logInfo", "Effect.logWarning", "Effect.logError", or needs to understand how Effect handles logging, metrics, and distributed tracing.
version: 1.0.0
---

# Observability in Effect

## Overview

Effect provides built-in observability:

- **Logging** - Structured, leveled logging
- **Metrics** - Counters, gauges, histograms
- **Tracing** - Distributed tracing with spans

All three integrate seamlessly with Effect's execution model.

## Logging

### Basic Logging

```typescript
import { Effect } from "effect"

const program = Effect.gen(function* () {
  yield* Effect.log("Starting process")
  yield* Effect.logDebug("Debug information")
  yield* Effect.logInfo("Processing item")
  yield* Effect.logWarning("Resource running low")
  yield* Effect.logError("Failed to connect")
  yield* Effect.logFatal("Critical system failure")
})
```

### Log Levels

```typescript
import { LogLevel, Logger } from "effect"

// Set minimum log level
const filtered = program.pipe(
  Logger.withMinimumLogLevel(LogLevel.Info)
)

// Available levels (lowest to highest):
// Trace, Debug, Info, Warning, Error, Fatal, None
```

### Structured Logging

```typescript
// Log with structured data
yield* Effect.log("User action").pipe(
  Effect.annotateLogs({
    userId: "123",
    action: "login",
    ip: "192.168.1.1"
  })
)

// Annotations apply to all logs in scope
const program = Effect.gen(function* () {
  yield* Effect.log("First log")   // Has userId annotation
  yield* Effect.log("Second log")  // Has userId annotation
}).pipe(
  Effect.annotateLogs({ userId: "123" })
)
```

### Log Spans

```typescript
// Add timing/context spans
const program = Effect.gen(function* () {
  yield* Effect.log("Processing")
  yield* processItems()
  yield* Effect.log("Complete")
}).pipe(
  Effect.withLogSpan("request-handler")
)
// Logs include: [request-handler 45ms] Processing
```

### Custom Logger

```typescript
import { Logger } from "effect"

const JsonLogger = Logger.make(({ logLevel, message, annotations, date }) => {
  console.log(JSON.stringify({
    level: logLevel.label,
    message: String(message),
    timestamp: date.toISOString(),
    ...annotations
  }))
})

const program = Effect.gen(function* () {
  yield* Effect.log("Hello")
}).pipe(
  Effect.provide(Logger.replace(Logger.defaultLogger, JsonLogger))
)
```

## Metrics

### Counter - Track Occurrences

```typescript
import { Metric } from "effect"

const requestCount = Metric.counter("http_requests_total", {
  description: "Total HTTP requests"
})

const program = Effect.gen(function* () {
  yield* Metric.increment(requestCount)
  yield* Metric.incrementBy(requestCount, 5)
})

const tracked = handleRequest.pipe(
  Metric.trackAll(requestCount)
)
```

### Gauge - Track Current Value

```typescript
const activeConnections = Metric.gauge("active_connections", {
  description: "Current active connections"
})

const program = Effect.gen(function* () {
  yield* Metric.set(activeConnections, 10)
  yield* Metric.incrementBy(activeConnections, 1)
  yield* Metric.decrementBy(activeConnections, 1)
})
```

### Histogram - Track Distributions

```typescript
const requestDuration = Metric.histogram("http_request_duration_ms", {
  description: "Request duration in milliseconds",
  boundaries: [10, 50, 100, 250, 500, 1000]
})

yield* Metric.observe(requestDuration, 125)

const tracked = handleRequest.pipe(
  Metric.trackDuration(requestDuration)
)
```

### Summary - Statistical Summary

```typescript
const responseSizes = Metric.summary("response_size_bytes", {
  description: "Response payload sizes",
  maxAge: "1 minute",
  maxSize: 100,
  quantiles: [0.5, 0.9, 0.99]
})

yield* Metric.observe(responseSizes, 1024)
```

### Frequency - Count by Tag

```typescript
const statusCodes = Metric.frequency("http_status_codes")

yield* Metric.observe(statusCodes, "200")
yield* Metric.observe(statusCodes, "404")
yield* Metric.observe(statusCodes, "500")
```

### Tagged Metrics

```typescript
const requestCount = Metric.counter("requests").pipe(
  Metric.tagged("service", "api"),
  Metric.tagged("version", "v1")
)

// Dynamic tags
const taggedCount = Metric.counter("requests").pipe(
  Metric.taggedWithLabels(["method", "endpoint"])
)

yield* Metric.increment(taggedCount).pipe(
  Metric.taggedWithLabels(["GET", "/users"])
)
```

### Reading Metrics

```typescript
const program = Effect.gen(function* () {
  yield* Metric.increment(requestCount)
  yield* Metric.increment(requestCount)

  const snapshot = yield* Metric.value(requestCount)
  // snapshot.count === 2
})
```

## Tracing

### Creating Spans

```typescript
import { Effect } from "effect"

const traced = handleRequest.pipe(
  Effect.withSpan("handle-request")
)

const traced = handleRequest.pipe(
  Effect.withSpan("handle-request", {
    attributes: {
      "http.method": "GET",
      "http.url": "/api/users"
    }
  })
)
```

### Nested Spans

```typescript
const program = Effect.gen(function* () {
  yield* fetchUser(id).pipe(Effect.withSpan("fetch-user"))
  yield* processData(data).pipe(Effect.withSpan("process-data"))
  yield* saveResult(result).pipe(Effect.withSpan("save-result"))
}).pipe(
  Effect.withSpan("main-operation")
)
// Creates: main-operation
//            ├── fetch-user
//            ├── process-data
//            └── save-result
```

### Adding Span Attributes

```typescript
import { Tracer } from "effect"

const program = Effect.gen(function* () {
  yield* Effect.annotateCurrentSpan("user.id", userId)

  yield* Effect.annotateCurrentSpan("event", "user_validated")

  const result = yield* processUser(userId)

  yield* Effect.annotateCurrentSpan("result.status", result.status)
})
```

### Span Status

```typescript
const program = Effect.gen(function* () {
  try {
    return yield* riskyOperation
  } catch (error) {
    yield* Effect.setSpanStatus({
      code: "error",
      message: error.message
    })
    return yield* Effect.fail(error)
  }
}).pipe(Effect.withSpan("risky-operation"))
```

### Custom Tracer

```typescript
import { Tracer } from "effect"

const ConsoleTracer = Tracer.make({
  span: (name, parent, context, links, startTime) => ({
    attribute: (key, value) => console.log(`[${name}] ${key}=${value}`),
    end: (endTime, exit) => console.log(`[${name}] ended`),
    event: (name, startTime, attributes) => console.log(`[${name}] event: ${name}`),
    status: (status) => console.log(`[${name}] status: ${status.code}`)
  })
})

const program = myEffect.pipe(
  Effect.provide(Tracer.layer(ConsoleTracer))
)
```

## OpenTelemetry Integration

```typescript
import { NodeSdk } from "@effect/opentelemetry"
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http"

const TracingLive = NodeSdk.layer(() => ({
  resource: { serviceName: "my-service" },
  spanProcessor: new BatchSpanProcessor(new OTLPTraceExporter())
}))

const program = myEffect.pipe(
  Effect.provide(TracingLive)
)
```

## Combining Observability

```typescript
const handleRequest = (req: Request) =>
  Effect.gen(function* () {
    yield* Effect.log("Request received").pipe(
      Effect.annotateLogs({ path: req.path, method: req.method })
    )

    yield* Metric.increment(requestCount)

    const result = yield* processRequest(req)

    yield* Effect.annotateCurrentSpan("response.status", result.status)
    yield* Metric.observe(requestDuration, result.duration)

    return result
  }).pipe(
    Effect.withSpan("handle-request", {
      attributes: {
        "http.method": req.method,
        "http.url": req.path
      }
    })
  )
```

## Best Practices

1. **Use structured logging** - Add context via annotations
2. **Name spans descriptively** - Use verb-noun format
3. **Add meaningful attributes** - Enable debugging/analysis
4. **Track key metrics** - Request count, latency, errors
5. **Use appropriate log levels** - Debug in dev, Info in prod

## Additional Resources

For comprehensive observability documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Built-in Logging" for logging APIs
- "Metrics" for metric types
- "Tracing" for distributed tracing
