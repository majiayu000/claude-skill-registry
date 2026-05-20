---
name: logging-observability
description: Implement structured logging, tracing, and metrics for debugging
category: DevOps Operations
---

# Skill: logging-observability

## What I do

I provide expertise in implementing structured logging, tracing, and metrics to ensure system observability. I focus on creating a clear, actionable data trail that allows for rapid debugging and performance analysis in production environments.

## When to use me

- When designing a new service's logging strategy
- When instrumenting code with distributed tracing spans
- When adding metrics to track business-critical KPIs or system health
- When debugging complex, distributed issues that span multiple services

## Core principles

1. **Structure over prose**: Use structured formats like JSON to make logs easily searchable and machine-readable.
2. **Actionability**: Every log message and metric should have a clear purpose. Avoid noise that obscures real issues.
3. **Context is king**: Include correlation IDs, request IDs, and relevant metadata (e.g., user ID, tenant ID) in every log entry.
4. **The three pillars**: Combine logs (discrete events), traces (request flow), and metrics (aggregates) for a complete view of system health.

## Patterns & examples

**Structured logging (JSON):**
```json
{
  "level": "info",
  "ts": "2026-02-22T21:00:00Z",
  "msg": "processed order",
  "order_id": "ORD-123",
  "user_id": "USR-456",
  "duration_ms": 150,
  "correlation_id": "CORR-789"
}
```

**Log levels guide:**
- **DEBUG**: Verbose information for development and troubleshooting.
- **INFO**: General operational events (e.g., service started, request completed).
- **WARN**: Unexpected but non-critical events that might require attention.
- **ERROR**: Critical failures that require immediate investigation.

**Distributed tracing:**
Use OpenTelemetry to start spans at the beginning of a request and inject the context into downstream calls. This allows you to visualize the entire lifecycle of a request across multiple services.

**Metrics types:**
- **Counters**: For events that only increase (e.g., total requests, error count).
- **Gauges**: For values that go up and down (e.g., current memory usage, active connections).
- **Histograms**: For distributions of values (e.g., request latency, payload size).

## Anti-patterns to avoid

- ❌ **Log noise**: Logging every trivial operation at the INFO level. This increases storage costs and makes finding real issues harder.
- ❌ **Sensitive data in logs**: Never log passwords, PII, or secrets. Always scrub or mask sensitive fields.
- ❌ **Missing correlation IDs**: Logs without a way to link them across services are nearly useless in distributed systems.
- ❌ **Ignoring metrics**: Relying solely on logs for health monitoring. Use metrics for real-time alerting and dashboards.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/Logging Observability.md`

## Related skills

- `devops`: For infrastructure and deployment considerations
- `automation`: For setting up alerting based on metrics and logs
- `security`: For ensuring logging practices meet compliance and data privacy standards
- `performance`: For using traces and metrics to identify and fix bottlenecks
