---
name: jaeger-tracing-specialist
description: Jaeger/OpenTelemetry patterns plus Skriptoteket tracing conventions (async context propagation, correlation, debugging).
---

# Jaeger Distributed Tracing Specialist

**Responsibility**: Jaeger/OpenTelemetry novel patterns + HuleEdu tracing conventions

**Prerequisites**: Assumes knowledge of basic distributed tracing concepts. For complete OpenTelemetry API documentation, use Context7 `/open-telemetry/opentelemetry-python`.

---

## When to Use This Skill

Use this skill when:
- ✅ Instrumenting async operations with context preservation
- ✅ Debugging trace context propagation across service boundaries
- ✅ Implementing queue/event-based tracing patterns
- ✅ Understanding span lifecycle in async contexts
- ✅ Troubleshooting missing/broken spans in Jaeger UI
- ✅ Integrating traces with metrics and logs (correlation)
- ✅ Implementing HuleEdu tracing conventions

Do NOT use for:
- ❌ Basic "what is distributed tracing" questions (Claude knows this)
- ❌ Simple span creation syntax (use Context7)
- ❌ Generic tracing theory (not implementation-specific)

---

## Core Capabilities

### Novel OpenTelemetry Patterns
- Async context propagation edge cases (threading vs asyncio)
- Token management lifecycle (attach/detach ordering)
- Baggage vs tags vs events (when to use each)
- Sampling strategy internals and edge cases
- Context pollution symptoms and debugging

### HuleEdu-Specific Patterns
- Service initialization (tracer setup, middleware)
- Naming conventions (spans, attributes)
- Trace context propagation (Kafka, Redis, HTTP)
- TraceContextManagerImpl queue pattern
- Correlation ID integration
- LLM provider instrumentation

---

## Quick Decision Tree

```
Need help with Jaeger tracing?
├─ Instrumenting new service?
│  └─ See: huleedu-patterns.md (initialization + middleware)
│
├─ Traces breaking across async boundaries?
│  ├─ Queue processing? → examples/async-propagation.md (TraceContextManagerImpl)
│  ├─ Kafka events? → examples/async-propagation.md (event chaining)
│  └─ Threading? → fundamentals.md (manual scope activation)
│
├─ Missing spans in Jaeger UI?
│  └─ See: examples/troubleshooting.md (common causes + fixes)
│
├─ Custom instrumentation pattern?
│  ├─ LLM calls? → examples/advanced-instrumentation.md (custom attributes)
│  ├─ Debugging markers? → fundamentals.md (span events vs attributes)
│  └─ Multi-span operations? → examples/advanced-instrumentation.md
│
├─ Novel OpenTelemetry API question?
│  └─ Use Context7: /open-telemetry/opentelemetry-python
│
└─ Understanding async context propagation?
   └─ See: fundamentals.md (asyncio vs threading gotchas)
```

---

## File Reference

| File | Content | Use When |
|------|---------|----------|
| **fundamentals.md** | Context7 novel patterns, OpenTelemetry gotchas | Learning non-obvious tracing behaviors |
| **huleedu-patterns.md** | HuleEdu naming, initialization, conventions | Implementing tracing in new service |
| **async-propagation.md** | Queue, Kafka, background task patterns | Fixing broken trace chains |
| **advanced-instrumentation.md** | Custom attributes, span events, LLM patterns | Adding domain-specific instrumentation |
| **troubleshooting.md** | Jaeger UI queries, debugging missing spans | Diagnosing tracing issues |

---

## Related Documentation

- **Context7**: `/open-telemetry/opentelemetry-python` - Complete OpenTelemetry API docs
- **HuleEdu Observability**: `.claude/rules/071.1-service-observability-core-patterns.md`
- **Prometheus Metrics**: `.claude/skills/prometheus-metrics/` - Metrics correlation patterns
- **Structlog Logging**: `.claude/skills/structlog-logging/` - Log correlation patterns

---

**LoC**: 80
