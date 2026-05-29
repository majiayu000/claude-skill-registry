---
name: libtelemetry
description: >
  libtelemetry - OpenTelemetry-based logging and tracing. createLogger and
  Logger provide RFC 5424 structured logging. Tracer creates distributed trace
  spans. TraceVisualizer renders trace diagrams. TraceIndex stores trace data.
  observe function wraps operations with timing. Use for logging, distributed
  tracing, and performance monitoring.
---

# libtelemetry Skill

## When to Use

- Adding structured logging to services
- Implementing distributed tracing across microservices
- Visualizing trace data for debugging
- Monitoring operation timing and performance

## Key Concepts

**Logger**: RFC 5424 compliant structured logging with severity levels.

**Tracer**: Creates spans for distributed tracing across service boundaries.

**TraceVisualizer**: Renders trace spans as visual diagrams.

## Usage Patterns

### Pattern 1: Structured logging

```javascript
import { createLogger } from "@copilot-ld/libtelemetry";

const logger = createLogger("my-service");
logger.info("Request received", { requestId: "123" });
logger.error("Operation failed", { error: err.message });
```

### Pattern 2: Distributed tracing

```javascript
import { Tracer } from "@copilot-ld/libtelemetry/tracer.js";

const tracer = new Tracer(storage);
const span = tracer.startSpan("processRequest");
// ... do work ...
span.end();
```

## Integration

Used by all services and extensions. Traces stored via Trace service.
