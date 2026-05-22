---
name: Observability & Monitoring
description: Use when adding logging, metrics, tracing, or alerting to applications. Covers structured logging, Prometheus metrics, OpenTelemetry tracing, and alerting strategies.
context: fork
agent: metrics-architect
version: 1.0.0
category: Operations & Reliability
agents: [backend-system-architect, code-quality-reviewer, ai-ml-engineer]
keywords: [observability, monitoring, logging, metrics, tracing, alerts, Prometheus, OpenTelemetry]
author: SkillForge
user-invocable: false
---

# Observability & Monitoring Skill

Comprehensive frameworks for implementing observability including structured logging, metrics, distributed tracing, and alerting.

## When to Use

- Setting up application monitoring
- Implementing structured logging
- Adding metrics and dashboards
- Configuring distributed tracing
- Creating alerting rules
- Debugging production issues

## Three Pillars of Observability

```
+-----------------+-----------------+-----------------+
|     LOGS        |     METRICS     |     TRACES      |
+-----------------+-----------------+-----------------+
| What happened   | How is system   | How do requests |
| at specific     | performing      | flow through    |
| point in time   | over time       | services        |
+-----------------+-----------------+-----------------+
```

## References

### Logging Patterns
**See: `references/logging-patterns.md`**

Key topics covered:
- Correlation IDs for cross-service request tracking
- Log sampling strategies for high-traffic systems
- LogQL queries for Loki log aggregation
- SkillForge structlog configuration example

### Metrics Collection
**See: `references/metrics-collection.md`**

Key topics covered:
- Counter, Gauge, Histogram, Summary metric types
- Cardinality management and limits
- Custom business metrics (LLM tokens, cache hit rates)
- LLM cost tracking with Prometheus

### Distributed Tracing
**See: `references/distributed-tracing.md`**

Key topics covered:
- OpenTelemetry setup and auto-instrumentation
- Span relationships (parent/child, parallel)
- Head-based and tail-based sampling strategies
- Trace context propagation across services

### Alerting and Dashboards
**See: `references/alerting-dashboards.md`**

Key topics covered:
- Alert severity levels and response times
- Alert grouping and inhibition rules
- Escalation policies and runbook links
- Golden Signals dashboard design
- SLO/SLI definitions and error budgets

## Quick Reference

### Log Levels

| Level | Use Case |
|-------|----------|
| **ERROR** | Unhandled exceptions, failed operations |
| **WARN** | Deprecated API, retry attempts |
| **INFO** | Business events, successful operations |
| **DEBUG** | Development troubleshooting |

### RED Method (Rate, Errors, Duration)

Essential metrics for any service:
- **Rate** - Requests per second
- **Errors** - Failed requests per second
- **Duration** - Request latency distribution

### Prometheus Buckets

```typescript
// HTTP request latency
buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]

// Database query latency
buckets: [0.001, 0.01, 0.05, 0.1, 0.5, 1]
```

### Key Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| ServiceDown | `up == 0` for 1m | Critical |
| HighErrorRate | 5xx > 5% for 5m | Critical |
| HighLatency | p95 > 2s for 5m | High |
| LowCacheHitRate | < 70% for 10m | Medium |

### Health Checks (Kubernetes)

| Probe | Purpose | Endpoint |
|-------|---------|----------|
| **Liveness** | Is app running? | `/health` |
| **Readiness** | Ready for traffic? | `/ready` |
| **Startup** | Finished starting? | `/startup` |

## Observability Checklist

### Implementation
- [ ] JSON structured logging
- [ ] Request correlation IDs
- [ ] RED metrics (Rate, Errors, Duration)
- [ ] Business metrics
- [ ] Distributed tracing
- [ ] Health check endpoints

### Alerting
- [ ] Service outage alerts
- [ ] Error rate thresholds
- [ ] Latency thresholds
- [ ] Resource utilization alerts

### Dashboards
- [ ] Service overview
- [ ] Error analysis
- [ ] Performance metrics

## Templates Reference

| Template | Purpose |
|----------|---------|
| `structured-logging.ts` | Winston logger with request middleware |
| `prometheus-metrics.ts` | HTTP, DB, cache metrics with middleware |
| `opentelemetry-tracing.ts` | Distributed tracing setup |
| `alerting-rules.yml` | Prometheus alerting rules |
| `health-checks.ts` | Liveness, readiness, startup probes |

## Langfuse Integration

For LLM observability, use Langfuse decorators:

```python
from langfuse.decorators import observe, langfuse_context

@observe(name="analyze_content")
async def analyze_content(url: str) -> AnalysisResult:
    langfuse_context.update_current_trace(
        name="content_analysis",
        user_id="system",
        metadata={"url": url}
    )
    # ... workflow implementation
```

See `examples/skillforge-monitoring-dashboard.md` for real-world examples.

## Extended Thinking Triggers

Use Opus 4.5 extended thinking for:
- **Incident investigation** - Correlating logs, metrics, traces
- **Alert tuning** - Reducing noise, catching real issues
- **Architecture decisions** - Choosing monitoring solutions
- **Performance debugging** - Cross-service latency analysis

---

## Related Skills

- `defense-in-depth` - Layer 8 observability as part of security architecture
- `devops-deployment` - Observability integration with CI/CD and Kubernetes
- `resilience-patterns` - Monitoring circuit breakers and failure scenarios
- `fastapi-advanced` - FastAPI-specific middleware for logging and metrics

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Log format | Structured JSON | Machine-parseable, supports log aggregation, enables queries |
| Metric types | RED method (Rate, Errors, Duration) | Industry standard, covers essential service health indicators |
| Tracing | OpenTelemetry | Vendor-neutral, auto-instrumentation, broad ecosystem support |
| Alerting severity | 4 levels (Critical, High, Medium, Low) | Clear escalation paths, appropriate response times |

---

## Capability Details

### structured-logging
**Keywords:** logging, structured log, json log, correlation id, log level, winston, pino, structlog
**Solves:**
- How do I set up structured logging?
- Implement correlation IDs across services
- JSON logging best practices

### correlation-tracking
**Keywords:** correlation id, request tracking, trace context, distributed logs
**Solves:**
- How do I track requests across services?
- Implement correlation IDs in middleware
- Find all logs for a single request

### log-sampling
**Keywords:** log sampling, high traffic logging, sampling rate, log volume
**Solves:**
- How do I reduce log volume in production?
- Sample INFO logs while keeping all errors

### prometheus-metrics
**Keywords:** metrics, prometheus, counter, histogram, gauge, summary, red method
**Solves:**
- How do I collect application metrics?
- Implement RED method (Rate, Errors, Duration)
- Choose between Counter, Gauge, Histogram

### metric-types
**Keywords:** counter, gauge, histogram, summary, bucket, quantile
**Solves:**
- When to use Counter vs Gauge?
- Histogram vs Summary for latency
- Configure histogram buckets

### cardinality-management
**Keywords:** cardinality, label explosion, time series, prometheus performance
**Solves:**
- How do I prevent label cardinality explosions?
- Fix unbounded labels (user IDs, request IDs)

### distributed-tracing
**Keywords:** tracing, distributed tracing, opentelemetry, span, trace id, waterfall
**Solves:**
- How do I implement distributed tracing?
- OpenTelemetry setup with auto-instrumentation
- Create manual spans for custom operations

### trace-sampling
**Keywords:** trace sampling, head-based sampling, tail-based sampling
**Solves:**
- How do I reduce trace volume?
- Sample 10% of traces but keep all errors

### alerting-strategy
**Keywords:** alert, alerting, notification, threshold, pagerduty, slack, severity
**Solves:**
- How do I set up effective alerts?
- Define alert severity levels (P1-P4)

### alert-fatigue-prevention
**Keywords:** alert fatigue, alert grouping, inhibition, escalation
**Solves:**
- How do I reduce alert noise?
- Group related alerts together

### dashboards
**Keywords:** dashboard, visualization, grafana, golden signals, red method
**Solves:**
- How do I create monitoring dashboards?
- Design Golden Signals dashboard layout
- Build SLO/SLI dashboards

### health-checks
**Keywords:** health check, liveness, readiness, startup probe, kubernetes
**Solves:**
- How do I implement health check endpoints?
- Difference between liveness and readiness

### langfuse-observability
**Keywords:** langfuse, llm observability, llm tracing, token usage, llm cost tracking
**Solves:**
- How do I monitor LLM calls with Langfuse?
- Track LLM token usage and cost

### llm-cost-tracking
**Keywords:** llm cost, token tracking, cost optimization, prometheus llm metrics
**Solves:**
- How do I track LLM costs with Prometheus?
- Measure token usage by model and operation