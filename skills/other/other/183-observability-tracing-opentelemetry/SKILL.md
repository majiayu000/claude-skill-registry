---
name: 183-observability-tracing-opentelemetry
description: Use when you need to implement or improve distributed tracing with OpenTelemetry in Java — including trace/span modeling, context propagation, semantic conventions, span attributes/events/status, sampling strategy, baggage usage, privacy safeguards, and backend integration with OTLP collectors. This should trigger for requests such as Improve tracing; Apply OpenTelemetry tracing; Add distributed tracing; Refactor tracing instrumentation. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Distributed Tracing with OpenTelemetry

Implement robust distributed tracing in Java with OpenTelemetry by modeling meaningful spans, preserving context propagation, and instrumenting critical business and infrastructure paths with low-overhead, privacy-safe telemetry.

**What is covered in this Skill?**

- OpenTelemetry tracing fundamentals for Java services
- Span design: boundaries, parent/child relationships, and operation naming
- Context propagation across HTTP, messaging, async tasks, and thread boundaries
- Semantic conventions and stable attribute naming
- Error/status/event recording best practices
- Sampling strategy and performance/cost trade-offs
- Privacy and security controls for trace attributes
- Testing and verification of trace propagation and span correctness

**Scope:** Distributed tracing quality in application and integration layers, focused on diagnosability, consistency, and operational safety.

## Constraints

Tracing instrumentation must preserve context correctly and avoid leaking sensitive data. Over-instrumentation and high-cardinality attributes can harm cost and signal quality.

- **PROPAGATION FIRST**: Ensure context propagation across all sync/async boundaries before adding extra span detail
- **NO SENSITIVE DATA**: Never store secrets, credentials, tokens, raw payloads, or PII in span attributes/events
- **LOW CARDINALITY ATTRIBUTES**: Avoid unbounded values in attributes that are used for aggregation/search
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after applying tracing changes

## When to use this skill

- Improve tracing
- Apply OpenTelemetry tracing
- Add distributed tracing
- Refactor tracing instrumentation

## Workflow

1. **Define trace model and critical flows**

Identify high-value request and async flows, define operation boundaries, and choose span names/attributes aligned with semantic conventions.

2. **Instrument and propagate context**

Add OpenTelemetry spans to key boundaries and ensure trace context is propagated across HTTP clients/servers, messaging, and executor-based async work.

3. **Harden span data and sampling**

Record status/errors/events consistently, remove sensitive data, control attribute cardinality, and configure sampling/exporters according to environment needs.

4. **Validate traces end-to-end**

Verify parent-child relationships, propagation continuity, and backend visibility through tests and runtime checks.

## Reference

For detailed guidance, examples, and constraints, see [references/183-observability-tracing-opentelemetry.md](references/183-observability-tracing-opentelemetry.md).
