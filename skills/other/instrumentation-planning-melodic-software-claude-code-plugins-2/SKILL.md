---
name: instrumentation-planning
description: Plan instrumentation strategy before implementation, covering what to instrument, naming conventions, cardinality management, and instrumentation budget
allowed-tools: Read, Glob, Grep
---

# Instrumentation Planning

Strategic planning for application instrumentation before implementation.

## When to Use This Skill

- Planning instrumentation for new services
- Reviewing instrumentation strategy
- Establishing naming conventions
- Managing telemetry cardinality
- Setting instrumentation budgets

## Instrumentation Strategy Framework

### What to Instrument

```text
Instrumentation Layers:

┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Automatic/Library Instrumentation                     │
│  - HTTP clients/servers (auto-captured)                         │
│  - Database clients (auto-captured)                             │
│  - Message queue clients (auto-captured)                        │
│  - Framework-provided metrics                                   │
│  Effort: Low | Coverage: Broad | Customization: Limited        │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Business Transaction Instrumentation                  │
│  - Key user journeys                                            │
│  - Business operations (checkout, signup, etc.)                │
│  - Revenue-generating flows                                     │
│  - SLA-bound operations                                         │
│  Effort: Medium | Coverage: Targeted | Value: High             │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: Debug/Diagnostic Instrumentation                      │
│  - Algorithmic hot paths                                        │
│  - Cache behavior                                               │
│  - Circuit breaker states                                       │
│  - Retry/fallback paths                                         │
│  Effort: Medium | Coverage: Deep | Use: Troubleshooting        │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: Business Metrics                                      │
│  - Domain-specific counters                                     │
│  - Conversion rates                                             │
│  - Feature usage                                                │
│  - Customer behavior                                            │
│  Effort: High | Coverage: Custom | Value: Business Insights    │
└─────────────────────────────────────────────────────────────────┘
```

### Instrumentation Decision Matrix

```yaml
instrumentation_decisions:
  always_instrument:
    - "Inbound HTTP/gRPC requests"
    - "Outbound HTTP/gRPC calls"
    - "Database queries"
    - "Message publish/consume"
    - "Authentication/authorization"
    - "External API calls"
    - "Cache operations"

  consider_instrumenting:
    - "Complex business logic"
    - "Feature flags evaluation"
    - "Background jobs"
    - "Scheduled tasks"
    - "File I/O operations"
    - "CPU-intensive operations"

  avoid_instrumenting:
    - "Every method call (too noisy)"
    - "Tight loops (performance impact)"
    - "Data transformation (low value)"
    - "Validation helpers"
    - "Utility functions"

  decision_criteria:
    business_value:
      weight: 0.3
      question: "Does this help understand business outcomes?"

    debugging_value:
      weight: 0.25
      question: "Does this help diagnose production issues?"

    slo_relevance:
      weight: 0.25
      question: "Does this contribute to SLI measurement?"

    cost_impact:
      weight: 0.2
      question: "Is the cardinality/volume acceptable?"
```

## Naming Conventions

### Metric Naming

```yaml
metric_naming:
  format: "[namespace]_[subsystem]_[name]_[unit]"

  rules:
    case: "snake_case"
    unit_suffix: "Always include (_seconds, _bytes, _total)"
    base_units: "Use base units (seconds not milliseconds)"
    counter_suffix: "_total for counters"

  examples:
    good:
      - "http_server_requests_total"
      - "http_server_request_duration_seconds"
      - "http_server_response_size_bytes"
      - "db_connections_current"
      - "order_processing_duration_seconds"
      - "payment_transactions_total"

    bad:
      - "requests (no unit, no namespace)"
      - "HttpRequestDuration (wrong case)"
      - "order_latency_ms (use base units)"
      - "totalOrders (camelCase, no unit)"

  label_naming:
    case: "snake_case"
    avoid:
      - "Embedded values in name (path=/users)"
      - "High cardinality labels"
    good_labels:
      - "method, status_code, path"
      - "service, version, environment"
    bad_labels:
      - "user_id (high cardinality)"
      - "request_id (high cardinality)"
      - "timestamp (not a dimension)"
```

### Span Naming

```yaml
span_naming:
  format: "[operation] [resource]"

  rules:
    - "Use verb + noun pattern"
    - "Keep names low cardinality"
    - "Include operation type, not specific values"
    - "Be consistent across services"

  examples:
    http:
      pattern: "HTTP {METHOD} {route_template}"
      good: "HTTP GET /users/{id}"
      bad: "HTTP GET /users/12345"

    database:
      pattern: "{operation} {table}"
      good: "SELECT orders"
      bad: "SELECT * FROM orders WHERE id=123"

    messaging:
      pattern: "{operation} {queue/topic}"
      good: "PUBLISH order-events"
      bad: "publish message to order-events queue"

    rpc:
      pattern: "{service}/{method}"
      good: "OrderService/CreateOrder"
      bad: "grpc call to order service"

  attributes:
    required:
      - "service.name"
      - "service.version"
      - "deployment.environment"

    recommended:
      http:
        - "http.method"
        - "http.route"
        - "http.status_code"
        - "http.target"

      database:
        - "db.system"
        - "db.name"
        - "db.operation"
        - "db.statement (sanitized)"

      messaging:
        - "messaging.system"
        - "messaging.destination"
        - "messaging.operation"
```

### Log Field Naming

```yaml
log_naming:
  format: "snake_case for all fields"

  standard_fields:
    timestamp: "ISO 8601 format"
    level: "INFO, WARN, ERROR, etc."
    message: "Human-readable description"
    service: "Service name"
    trace_id: "Correlation ID"
    span_id: "Current span"

  domain_fields:
    pattern: "{domain}_{field}"
    examples:
      - "order_id"
      - "customer_id"
      - "payment_amount"
      - "product_sku"

  avoid:
    - "Nested objects (flatten for indexing)"
    - "Arrays of unknown length"
    - "Large text blobs"
    - "Sensitive data (PII, secrets)"
```

## Cardinality Management

### Understanding Cardinality

```text
Cardinality = Number of unique time series

Example:
http_requests_total{method="GET", path="/api/users", status="200"}

Cardinality = methods × paths × statuses
            = 5 × 100 × 10
            = 5,000 time series

With user_id (1M users):
            = 5 × 100 × 10 × 1,000,000
            = 5,000,000,000 time series ← EXPLOSION!
```

### Cardinality Budget

```yaml
cardinality_budget:
  planning:
    total_budget: 100000  # Target max time series per service
    allocation:
      automatic_instrumentation: 30%  # 30,000
      business_transactions: 40%      # 40,000
      custom_metrics: 20%             # 20,000
      buffer: 10%                     # 10,000

  per_metric_limits:
    low_cardinality:
      max_series: 100
      example: "status codes, methods"

    medium_cardinality:
      max_series: 1000
      example: "endpoints, operations"

    high_cardinality:
      max_series: 10000
      example: "aggregated by hour"
      requires: "Justification and approval"

  monitoring:
    - "Alert on cardinality growth > 10% per day"
    - "Weekly cardinality reviews"
    - "Automatic label value limiting"
```

### Cardinality Reduction Techniques

```yaml
cardinality_reduction:
  bucketing:
    before: "path=/users/12345"
    after: "path=/users/{id}"
    technique: "Path template extraction"

  sampling:
    description: "Sample high-volume, low-value traces"
    strategies:
      head_sampling: "Decide at trace start"
      tail_sampling: "Decide after seeing full trace"
      adaptive: "Adjust rate based on volume"

  aggregation:
    description: "Pre-aggregate before export"
    example: "Count by status, not per request"

  value_limiting:
    description: "Cap unique values per label"
    example: "Max 100 unique paths, then 'other'"

  dropping:
    description: "Drop low-value dimensions"
    candidates:
      - "Instance ID (use service name)"
      - "Request ID (not for metrics)"
      - "Full URLs (use route templates)"
```

## Instrumentation Budget

### Performance Impact

```yaml
performance_budget:
  cpu_overhead:
    target: "< 1% CPU increase"
    measurement: "Profile with/without instrumentation"

  memory_overhead:
    target: "< 50MB additional heap"
    components:
      - "Metric registries"
      - "Span buffers"
      - "Log buffers"

  latency_overhead:
    target: "< 1ms per request"
    hot_paths: "< 100μs"

  data_volume:
    metrics:
      target: "< 1GB/day per service"
      calculation: "series × scrape_interval × 8 bytes"

    traces:
      target: "< 10GB/day per service (with sampling)"
      sampling_rate: "1-10% for high-volume services"

    logs:
      target: "< 5GB/day per service"
      strategies: "Sampling, level gating"
```

### Cost Planning

```yaml
cost_planning:
  estimation_formula:
    metrics:
      monthly_cost: "time_series × $0.003 (typical cloud pricing)"
      example: "10,000 series × $0.003 = $30/month"

    traces:
      monthly_cost: "spans_per_month × $0.000005"
      example: "100M spans × $0.000005 = $500/month"

    logs:
      monthly_cost: "GB_per_month × $0.50"
      example: "500GB × $0.50 = $250/month"

  optimization_strategies:
    - "Increase scrape interval (15s → 60s)"
    - "Reduce trace sampling rate"
    - "Log level gating in production"
    - "Shorter retention for debug data"
    - "Downsample old metrics"
```

## Instrumentation Plan Template

```yaml
instrumentation_plan:
  service: "{Service Name}"
  version: "1.0"
  date: "{Date}"
  owner: "{Team}"

  objectives:
    - "Track SLIs for order processing"
    - "Enable distributed tracing for debugging"
    - "Monitor payment success rates"

  automatic_instrumentation:
    framework: "OpenTelemetry .NET"
    enabled:
      - "ASP.NET Core (HTTP server)"
      - "HttpClient (HTTP client)"
      - "Entity Framework Core (database)"
      - "Azure.Messaging.ServiceBus"
    configuration:
      sampling_rate: 0.1  # 10% of traces
      batch_export_interval: 5000  # ms

  custom_spans:
    - name: "ProcessOrder"
      purpose: "Track order processing duration"
      attributes:
        - "order.id"
        - "order.item_count"
        - "order.total_amount"
      events:
        - "inventory.reserved"
        - "payment.processed"

    - name: "ValidatePayment"
      purpose: "Track payment validation steps"
      attributes:
        - "payment.method"
        - "payment.provider"
      sensitive: false

  custom_metrics:
    counters:
      - name: "orders_total"
        labels: ["status", "payment_method"]
        purpose: "Count orders by outcome"
        cardinality_estimate: 20

      - name: "payment_failures_total"
        labels: ["reason", "provider"]
        purpose: "Track payment failure reasons"
        cardinality_estimate: 50

    histograms:
      - name: "order_processing_duration_seconds"
        labels: ["order_type"]
        purpose: "Track order processing latency"
        buckets: [0.1, 0.5, 1, 2, 5, 10]
        cardinality_estimate: 10

    gauges:
      - name: "pending_orders_current"
        labels: []
        purpose: "Current pending order count"
        cardinality_estimate: 1

  cardinality_summary:
    estimated_total: 81
    budget: 1000
    status: "Within budget"

  log_strategy:
    production_level: "INFO"
    structured_fields:
      standard:
        - "trace_id"
        - "span_id"
        - "service"
        - "environment"
      domain:
        - "order_id"
        - "customer_id (hashed)"
    sampling:
      debug_logs: "1% in production"

  cost_estimate:
    monthly:
      metrics: "$30"
      traces: "$200"
      logs: "$150"
      total: "$380"

  review_schedule:
    frequency: "Quarterly"
    metrics_to_review:
      - "Cardinality growth"
      - "Data volume"
      - "Cost vs budget"
```

## Related Skills

- `observability-patterns` - Three pillars overview
- `distributed-tracing` - Trace implementation details
- `slo-sli-error-budget` - What to measure for SLOs

---

**Last Updated:** 2025-12-26
