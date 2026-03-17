---
name: prometheus-metrics-specialist
description: Instrument services with Prometheus metrics and write PromQL queries. Guides HuleEdu naming conventions, metrics middleware setup, and business vs operational metrics. Integrates with Context7 for latest Prometheus documentation.
---

# Prometheus Metrics Specialist

Compact skill for instrumenting HuleEdu services with Prometheus metrics and querying them with PromQL.

## When to Use

Activate when the user:
- Needs to add metrics instrumentation to a service
- Wants to write PromQL queries for dashboards or alerts
- Asks about metrics naming conventions
- Needs help with metrics middleware setup
- Wants to understand business vs operational metrics
- Mentions Prometheus, PromQL, metrics, instrumentation, or monitoring
- Needs to expose `/metrics` endpoint

## I Need To...

### Get Started (First Time)
1. **Learn Prometheus basics** → [fundamentals.md](fundamentals.md) - Counter, Histogram, Gauge concepts
2. **Set up HuleEdu service** → [huleedu-patterns.md](huleedu-patterns.md) - metrics.py module, /metrics endpoint
3. **Pick an example** → See "Add Metrics to Service" below

### Add Metrics to Service

| I need to instrument... | Read this file |
|------------------------|----------------|
| **HTTP endpoints** | [examples/http-and-kafka.md](examples/http-and-kafka.md#http-instrumentation) |
| **Kafka event processing** | [examples/http-and-kafka.md](examples/http-and-kafka.md#kafka-event-metrics) |
| **LLM API calls** | [examples/llm-and-batch.md](examples/llm-and-batch.md#llm-provider-metrics) |
| **Batch processing** | [examples/llm-and-batch.md](examples/llm-and-batch.md#batch-processing-metrics) |
| **Database queries** | [examples/database-and-business.md](examples/database-and-business.md#database-metrics) |
| **Business logic** | [examples/database-and-business.md](examples/database-and-business.md#business-logic-metrics) |

### Choose Naming Pattern
→ [huleedu-patterns.md § Naming Patterns](huleedu-patterns.md#naming-patterns)

### Write PromQL Queries

| I need to... | Read this section |
|--------------|-------------------|
| **Learn PromQL syntax** | [promql-guide.md § Basics](promql-guide.md#promql-basics) |
| **Calculate error rate** | [promql-guide.md § Error Rates](promql-guide.md#error-rate-patterns) |
| **Get P95 latency** | [promql-guide.md § Percentiles](promql-guide.md#percentile-queries) |
| **Troubleshoot issues** | [promql-guide.md § Troubleshooting](promql-guide.md#troubleshooting-patterns) |

### Reference

| What I need to know | Where to find it |
|---------------------|------------------|
| **Metric types (Counter/Histogram/Gauge)** | [fundamentals.md § Metric Types](fundamentals.md#metric-types) |
| **Label design principles** | [fundamentals.md § Labels](fundamentals.md#label-design) |
| **Histogram bucket design** | [fundamentals.md § Buckets](fundamentals.md#histogram-bucket-design) |
| **HuleEdu architecture** | [huleedu-patterns.md § Architecture](huleedu-patterns.md#architecture) |

## Quick Metric Type Cheatsheet

```python
# Counter: Events that only increase (resets to 0 on restart)
operations_total = Counter("spell_checker_operations_total", "desc", ["status"])
operations_total.labels(status="success").inc()

# Histogram: Distributions (latency, sizes, scores)
duration_seconds = Histogram("spell_checker_duration_seconds", "desc")
duration_seconds.observe(0.23)  # 230ms

# Gauge: Point-in-time values that go up/down
active_connections = Gauge("spell_checker_active_connections", "desc")
active_connections.set(15)
active_connections.inc()  # 16
```

## HuleEdu Naming Cheatsheet

```python
# Pattern 1: Service-Prefixed (most common, operational metrics)
spell_checker_operations_total
spell_checker_http_request_duration_seconds

# Pattern 2: Business Metrics (cross-service, business logic)
huleedu_llm_prompt_tokens_total
huleedu_spellcheck_corrections_made

# Pattern 3: Legacy (being phased out)
request_count
```

**Decision**: Service-specific metric? → Pattern 1. Cross-service business metric? → Pattern 2.

## Core Capabilities

- **Naming Conventions**: 3 patterns (service-prefixed, business, legacy)
- **Instrumentation**: Counter, Histogram, Gauge, Summary usage
- **Middleware Setup**: Standard HTTP metrics middleware
- **Service-Specific Metrics**: Business logic patterns
- **PromQL Queries**: Troubleshooting and dashboard queries
- **Scrape Configuration**: Prometheus targets and discovery
- **Best Practices**: Metric types, cardinality, aggregation
- **Context7 Integration**: Latest Prometheus/PromQL docs

## Documentation Structure

- **[fundamentals.md](fundamentals.md)**: Universal Prometheus concepts + prometheus_client API
- **[huleedu-patterns.md](huleedu-patterns.md)**: HuleEdu naming, architecture, setup patterns
- **[promql-guide.md](promql-guide.md)**: PromQL syntax + HuleEdu query patterns
- **[examples/](examples/)**: Real-world instrumentation examples
