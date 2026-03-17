---
name: observability-patterns
description: Use when implementing observability strategy, correlating signals, or designing monitoring systems. Covers the three pillars (logs, metrics, traces) and their integration.
allowed-tools: Read, Glob, Grep
---

# Observability Patterns

Patterns for implementing comprehensive observability including logs, metrics, traces, and their correlation.

## When to Use This Skill

- Designing observability strategy
- Implementing the three pillars
- Correlating signals across systems
- Choosing observability tools
- Building monitoring dashboards

## What is Observability?

```text
Observability = Ability to understand internal state
                from external outputs

Not just monitoring (known-unknowns)
But understanding (unknown-unknowns)

Traditional monitoring: "Is CPU > 80%?"
Observability: "Why are users experiencing latency?"
```

## The Three Pillars

### Overview

```text
┌─────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                         │
│                                                          │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │   LOGS   │    │ METRICS  │    │  TRACES  │         │
│   │          │    │          │    │          │         │
│   │ Events   │    │ Counters │    │ Requests │         │
│   │ Details  │    │ Gauges   │    │ Spans    │         │
│   │ Context  │    │ Trends   │    │ Flow     │         │
│   └──────────┘    └──────────┘    └──────────┘         │
│        │               │               │                │
│        └───────────────┼───────────────┘                │
│                        │                                │
│               ┌────────┴────────┐                       │
│               │   CORRELATION   │                       │
│               │  (trace_id)     │                       │
│               └─────────────────┘                       │
└─────────────────────────────────────────────────────────┘

Each pillar answers different questions:
- Logs: What happened? (events)
- Metrics: How much/many? (aggregates)
- Traces: Where? (request flow)
```

### Logs

```text
Purpose: Discrete events with context

Structure:
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "ERROR",
  "service": "order-service",
  "message": "Payment failed",
  "trace_id": "abc123",
  "span_id": "def456",
  "user_id": "12345",
  "order_id": "ORD-789",
  "error": {
    "code": "CARD_DECLINED",
    "message": "Insufficient funds"
  }
}

Best for:
- Debugging specific issues
- Audit trails
- Error details
- Business events

Challenges:
- High volume → storage costs
- Unstructured → hard to query
- No aggregation → not for trends
```

### Metrics

```text
Purpose: Numeric measurements over time

Types:
┌─────────────────────────────────────────────────────────┐
│ Counter: Cumulative, only increases                     │
│ - http_requests_total                                   │
│ - errors_total                                          │
│ - bytes_transferred                                     │
├─────────────────────────────────────────────────────────┤
│ Gauge: Point-in-time value, can go up/down             │
│ - current_connections                                   │
│ - queue_depth                                           │
│ - temperature                                           │
├─────────────────────────────────────────────────────────┤
│ Histogram: Distribution of values                       │
│ - request_duration_seconds                              │
│ - response_size_bytes                                   │
│ Provides: count, sum, buckets                           │
├─────────────────────────────────────────────────────────┤
│ Summary: Similar to histogram, calculates quantiles     │
│ - request_latency_seconds (p50, p90, p99)              │
└─────────────────────────────────────────────────────────┘

Best for:
- Trends and patterns
- Alerting on thresholds
- Dashboards
- Capacity planning

Challenges:
- No event details
- Cardinality limits
- Not request-level
```

### Traces

```text
Purpose: Request flow across services

Structure:
Trace (end-to-end request)
├── Span (API Gateway) - 200ms
│   ├── Span (Auth) - 20ms
│   └── Span (OrderService) - 150ms
│       ├── Span (Database) - 50ms
│       └── Span (PaymentService) - 80ms
│           └── Span (External API) - 60ms

Best for:
- Understanding request flow
- Finding bottlenecks
- Debugging distributed issues
- Service dependencies

Challenges:
- Storage intensive
- Requires sampling
- Complex to implement
```

## Signal Correlation

### Why Correlate?

```text
Without correlation:
- Metrics: "Error rate is high"
- Logs: "Error logs from somewhere"
- Traces: "Some traces show errors"
→ Hard to connect the dots

With correlation:
- Metrics: "Error rate spike at 10:30"
  └── Click to see: Exemplar trace
      └── Click to see: Related logs
→ Full picture in seconds
```

### Correlation Methods

```text
1. Trace ID injection:
   All signals include trace_id

   Log: {"trace_id": "abc123", "message": "..."}
   Metric: http_requests{trace_id="abc123"}
   Trace: TraceID = abc123

2. Exemplars:
   Metrics point to sample traces

   request_latency = 2.5s
   └── exemplar: trace_id=abc123
   → "Show me a slow request"

3. Time correlation:
   Align signals by timestamp

   Metric spike at 10:30
   → Query logs around 10:30
   → Query traces around 10:30
```

### Unified Query Example

```text
Investigation flow:

1. Dashboard shows latency spike
   http_request_duration_p99 = 3s

2. Click on spike → exemplar trace
   trace_id: abc123

3. View trace → slow database span
   db.query: SELECT * FROM orders... (2.5s)

4. Query logs with trace_id
   {"trace_id":"abc123","query":"SELECT...","rows":50000}

5. Root cause identified
   Missing index causing full table scan
```

## OpenTelemetry Unified Approach

```text
OpenTelemetry provides unified API for all signals:

Application Code
      │
      ▼
┌─────────────────────────────────────────────────────┐
│              OpenTelemetry SDK                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │ Tracer  │  │  Meter  │  │ Logger  │             │
│  │Provider │  │Provider │  │Provider │             │
│  └────┬────┘  └────┬────┘  └────┬────┘             │
│       │            │            │                   │
│       └────────────┼────────────┘                   │
│                    │                                │
│            ┌───────┴───────┐                        │
│            │  Exporters    │                        │
│            └───────────────┘                        │
└─────────────────────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     ▼               ▼               ▼
┌─────────┐   ┌─────────┐    ┌─────────┐
│  Tempo  │   │Prometheus│   │  Loki   │
│(Traces) │   │(Metrics) │   │ (Logs)  │
└─────────┘   └─────────┘    └─────────┘
```

## Logging Patterns

### Structured Logging

```text
Unstructured (bad):
"User 12345 failed to login: invalid password"

Structured (good):
{
  "event": "login_failed",
  "user_id": "12345",
  "reason": "invalid_password",
  "timestamp": "2024-01-15T10:30:00Z",
  "trace_id": "abc123"
}

Benefits:
- Queryable: user_id:12345 AND event:login_failed
- Parseable: Automated analysis
- Correlatable: trace_id links to traces
```

### Log Levels

```text
Level     | When to use
----------|------------------------------------------
TRACE     | Very detailed, development only
DEBUG     | Development, verbose
INFO      | Normal operations, audit events
WARN      | Degraded, recoverable issues
ERROR     | Failures requiring attention
FATAL     | Application cannot continue

Production typically: INFO and above
Debug mode: DEBUG and above
```

### Log Aggregation Architecture

```text
┌─────────────────────────────────────────────────────────┐
│  Application Pods                                        │
│  ┌──────┐ ┌──────┐ ┌──────┐                            │
│  │ App  │ │ App  │ │ App  │ → stdout/stderr             │
│  └──────┘ └──────┘ └──────┘                            │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Log Collector (Fluentd/Vector/Fluent Bit)             │
│  - Parse logs                                           │
│  - Add metadata (pod, namespace, etc.)                 │
│  - Transform/filter                                     │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Storage (Elasticsearch/Loki/CloudWatch)               │
│  - Index for search                                     │
│  - Retention policies                                   │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│  Query Interface (Kibana/Grafana)                      │
│  - Search and filter                                    │
│  - Dashboards                                           │
└─────────────────────────────────────────────────────────┘
```

## Metrics Patterns

### Naming Conventions

```text
Format: [namespace]_[subsystem]_[name]_[unit]

Examples:
http_requests_total
http_request_duration_seconds
http_response_size_bytes
process_cpu_seconds_total
db_connections_current

Guidelines:
- Use snake_case
- Include unit suffix (_seconds, _bytes, _total)
- Use base units (seconds not milliseconds)
- Be consistent across services
```

### Labels/Dimensions

```text
Metrics with labels:

http_requests_total{
  method="GET",
  path="/api/users",
  status="200"
}

Cardinality warning:
http_requests_total{user_id="..."}  // BAD: High cardinality

Keep labels low cardinality:
- status: ~5 values (200, 4xx, 5xx...)
- method: ~10 values
- service: ~100 values
- user_id: millions → TOO MANY
```

### RED Method

```text
For request-based services:

R - Rate: Requests per second
    http_requests_total

E - Errors: Failed requests per second
    http_requests_total{status=~"5.."}

D - Duration: Latency distribution
    http_request_duration_seconds
```

### USE Method

```text
For resources (CPU, memory, disk):

U - Utilization: % of resource used
    cpu_usage_percent

S - Saturation: Queued work
    thread_pool_queued_tasks

E - Errors: Error count
    disk_errors_total
```

## Dashboards and Alerts

### Dashboard Design

```text
Dashboard hierarchy:

1. Overview (executive level)
   - Key SLOs
   - Error rates
   - Traffic trends

2. Service dashboards
   - RED metrics
   - Dependencies
   - Resource usage

3. Debug dashboards
   - Detailed metrics
   - Component breakdown
   - Query performance
```

### Alert Design

```text
Good alerts:
- Actionable: Someone can do something
- Meaningful: Reflects user impact
- Urgent: Needs attention now

Bad alerts:
- CPU > 80% (maybe fine)
- Disk > 90% (too late?)
- Any single error (noise)

Better approach: SLO-based alerting
- "Error budget burning too fast"
- Directly tied to user impact
```

## Tool Selection

### Open Source Stack

```text
Metrics: Prometheus + Grafana
Logs: Loki + Grafana
Traces: Jaeger/Tempo + Grafana

Alternative:
Metrics: VictoriaMetrics + Grafana
Logs: Elasticsearch + Kibana
Traces: Zipkin
```

### Cloud Native

```text
AWS:
- CloudWatch (metrics, logs)
- X-Ray (traces)

GCP:
- Cloud Monitoring (metrics)
- Cloud Logging (logs)
- Cloud Trace (traces)

Azure:
- Azure Monitor (metrics, logs)
- Application Insights (traces)
```

### Commercial Platforms

```text
Full stack:
- Datadog
- New Relic
- Dynatrace
- Splunk

Benefits: Unified, managed, features
Costs: Price, vendor lock-in
```

## Best Practices

```text
1. Structured logging from day one
   Don't retrofit later

2. Consistent trace context
   Propagate trace_id everywhere

3. Metric cardinality awareness
   Monitor and limit label values

4. Correlation by default
   trace_id in logs, exemplars in metrics

5. Alert on symptoms, not causes
   "Users affected" not "CPU high"

6. Regular observability review
   Are we seeing what we need?
```

## Related Skills

- `distributed-tracing` - Deep dive on traces
- `slo-sli-error-budget` - SLO-based observability
- `incident-response` - Using observability in incidents
