---
name: spring-boot-observability
description: Spring Boot 4 observability with Actuator, Micrometer, and OpenTelemetry. Use when configuring health indicators, custom metrics, distributed tracing, production endpoint exposure, or Kubernetes/Cloud Run probes. Covers Actuator security, Micrometer Timer/Counter/Gauge patterns, and OpenTelemetry span customization.
---

# Spring Boot Observability

Production observability with Actuator endpoints, Micrometer metrics, and OpenTelemetry tracing.

## Core Components

| Component | Purpose |
|-----------|---------|
| **Actuator** | Health checks, info, metrics exposure, operational endpoints |
| **Micrometer** | Metrics abstraction (Timer, Counter, Gauge, DistributionSummary) |
| **OpenTelemetry** | Distributed tracing (default in Spring Boot 4) |

## Core Workflow

1. **Add starters** → `actuator`, `micrometer-registry-*`, `opentelemetry`
2. **Configure endpoint exposure** → Secure sensitive endpoints
3. **Define health groups** → Separate liveness from readiness
4. **Add custom metrics** → Business-specific measurements
5. **Configure tracing** → Sampling, propagation, export

## Quick Patterns

See [EXAMPLES.md](EXAMPLES.md) for complete working examples including:
- **Production Actuator Configuration** with health groups and Kubernetes probes
- **Custom Health Indicator** with latency monitoring (Java + Kotlin)
- **Custom Micrometer Metrics** with Counter, Timer, and Gauge patterns
- **OpenTelemetry Span Customization** with Observation API
- **OpenTelemetry Configuration** for OTLP export
- **Actuator Endpoint Access Control** (Boot 4)

## Spring Boot 4 Specifics

- **OpenTelemetry** is the default tracer (replaces Brave)
- **Health Indicator** imports from `org.springframework.boot.health.contributor.*`
- **Endpoint Access Control** with `access: none/unrestricted/read-only`

## Detailed References

- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for complete working code examples
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and Boot 4 migration
- **Actuator Endpoints**: See [references/ACTUATOR.md](references/ACTUATOR.md) for endpoint configuration, security, custom endpoints
- **Micrometer Metrics**: See [references/METRICS.md](references/METRICS.md) for Timer, Counter, Gauge, DistributionSummary patterns
- **Distributed Tracing**: See [references/TRACING.md](references/TRACING.md) for OpenTelemetry, span customization, context propagation

## Anti-Pattern Checklist

| Anti-Pattern | Fix |
|--------------|-----|
| DB checks in liveness probe | Move to readiness group only |
| 100% trace sampling in production | Use 10% or less |
| Exposing all endpoints publicly | Separate management port + auth |
| High-cardinality metric tags | Use low-cardinality tags only |
| Missing graceful shutdown | Add `server.shutdown=graceful` |
| No health probe groups | Separate liveness and readiness |

## Related Skills

- `spring-boot-verify` — For dependency and configuration validation
- `spring-boot-security` — For securing Actuator endpoints with Spring Security

## Critical Reminders

1. **Separate liveness from readiness** — Liveness: "is process alive?", Readiness: "can handle traffic?"
2. **Low cardinality tags only** — User IDs, request IDs = bad; status codes, regions = good
3. **Secure Actuator endpoints** — Use separate port or authentication
4. **Sample traces in production** — 100% sampling overwhelms collectors
5. **Graceful shutdown** — Allow in-flight requests to complete
