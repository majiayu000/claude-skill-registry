---
name: observability
description: Use when implementing metrics, tracing, SLOs, alerting, or dashboards. Covers Prometheus/Grafana/OTel stack design, SLI/SLO frameworks, error budgets, burn-rate alerting, and distributed tracing strategy.
---

# Observability

## Decision Framework: What to Instrument

**Golden Signals** (prefer for services): Latency, Traffic, Errors, Saturation
- RED (request-scoped): Rate, Errors, Duration
- USE (resource-scoped): Utilization, Saturation, Errors

Pick RED for microservices, USE for infrastructure. Don't mix.

## Metric Design Opinions

- Always use histograms over summaries for latency -- histograms are aggregatable, summaries are not
- Bucket defaults `[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2, 5]` cover most HTTP services
- Exclude `/health` and `/metrics` endpoints from SLI calculations
- Use recording rules for any query used in alerts or dashboards -- never put raw PromQL in alerts
- Label cardinality kills Prometheus: never use user IDs, request IDs, or unbounded values as labels

## Service Tier Classification

| Tier | Availability | Latency P99 | Examples |
|------|-------------|-------------|----------|
| Critical | 99.95% | 100ms | Payment, auth |
| Essential | 99.9% | 500ms | Search, catalog |
| Standard | 99.5% | 1s | Recommendations |
| Best Effort | 99.0% | 2s | Batch, reporting |

Assign tiers before writing SLOs. Tier drives alert routing and error budget policy.

## SLO Framework

### Error Budget Policy (non-negotiable escalation)

| Budget Remaining | Action |
|-----------------|--------|
| >50% | Normal velocity |
| 10-50% | Postpone risky changes |
| 1-10% | Freeze non-critical changes |
| 0% | Feature freeze, reliability only |

### Release Decision Matrix

| Budget Status | Low Risk | Medium Risk | High Risk |
|--------------|----------|-------------|-----------|
| Healthy | Approve | Approve | Review |
| Warning | Review | Defer | Block |
| Critical | Defer | Block | Block |
| Exhausted | Block | Block | Block |

### Burn Rate Alert Thresholds

| Alert | Burn Rate | Short Window | Action |
|-------|-----------|-------------|--------|
| Fast burn | 14.4x | 1h + 5m | Page on-call |
| Slow burn | 3x | 6h + 30m | Create ticket |

Multi-window burn rate is the only correct SLO alerting pattern. Single-window alerts produce false positives or miss slow degradation.

### Progressive SLO Rollout

Start at 99.0% for 1 month baseline, then tighten: 99.5% (2 months) -> 99.9% (3 months) -> 99.95% (ongoing). Never set SLO tighter than current measured reliability.

### SLO Templates

**API service**: availability (99.9% over 30d) + latency (95% of requests < 500ms over 30d)
**Data pipeline**: freshness (99% batches within 30 min over 7d) + completeness (99.95% records processed over 7d)

## Distributed Tracing Strategy

### Sampling Decisions
- **Dev/staging**: 100% sampling
- **Production low-traffic** (<1k rps): 10-50% probabilistic
- **Production high-traffic** (>10k rps): 1% probabilistic or rate-limit to ~100 traces/sec
- Always use `ParentBased` sampler so child spans follow parent's decision
- Force-sample all errors and high-latency requests regardless of probabilistic rate

### Context Propagation
- Use W3C `traceparent` header (not B3 or Jaeger-native) for new systems
- Always inject trace_id into structured logs for correlation
- Propagate context through async boundaries (queues, event buses) explicitly

### Backend Choice
- **Tempo** (Grafana stack): prefer when already using Grafana; object-storage backed, cheap at scale
- **Jaeger**: prefer when you need standalone deployment or Elasticsearch integration
- Both support OTLP -- always send via OpenTelemetry Collector, never direct from app to backend

## Alerting Opinions

- **Alert on symptoms, not causes** -- alert on error rate, not "pod restarted"
- Severity levels: `critical` (pages), `warning` (tickets), `info` (dashboard only)
- Every alert must have a runbook link in annotations
- `for:` duration: critical >= 2m, warning >= 5m, info >= 15m -- prevents flapping
- Route critical to PagerDuty, warning to Slack channel, info to dashboard only

## Stack Preferences

| Concern | Preferred Tool | Rationale |
|---------|---------------|-----------|
| Metrics | Prometheus + Thanos/Mimir | De facto standard, PromQL ecosystem |
| Visualization | Grafana | Dashboard-as-code, multi-datasource |
| Tracing | Tempo or Jaeger via OTel | OTLP-native, cost-effective |
| Logs | Loki or OpenSearch | Loki for Grafana stack, OpenSearch for complex queries |
| Collector | OpenTelemetry Collector | Vendor-neutral pipeline, single agent |
| Alerting | Alertmanager | Native Prometheus integration |

## Gotchas

- Prometheus `rate()` requires at least 2 data points in the window -- use `[5m]` minimum with 15s scrape interval
- `histogram_quantile` is an estimate; accuracy degrades with poor bucket choices
- OTel Collector `batch` processor default timeout is 200ms -- increase to 5-10s for production to reduce export overhead
- Grafana dashboards without variables become unmaintainable past 3 services
- Never scrape intervals faster than 10s in production -- it causes storage and CPU issues
- Alertmanager grouping: group by `alertname, namespace, service` -- too broad silences everything, too narrow floods on-call
