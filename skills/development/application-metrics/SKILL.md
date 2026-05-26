---
name: application-metrics
description: Guide for instrumenting applications with metrics. Use when adding
  observability, monitoring, metrics, counters, gauges, or instrumentation to code.
  Covers API endpoints, databases, queues, caching, and locks.
allowed-tools: Read, Grep, Edit, Write
---

# Application Metrics Instrumentation

Practical patterns for adding observability to applications.

## Five Metric Types

| Type | Purpose | Example |
|------|---------|---------|
| **Operational Counters** | Track discrete events (success/failure) | `api.requests.success_total` |
| **Resource Utilization** | Current capacity usage (gauges) | `db.connections.active` |
| **Performance/Latency** | Speed with explicit units | `api.request.duration_ms` |
| **Data Volume** | Information flow rates | `queue.messages.bytes_total` |
| **Business Logic** | Domain-specific value | `orders.completed_total` |

## Naming Convention

```
<system>.<component>.<operation>.<metric_type>
```

Examples:
- `myapp.api.users.requests_total`
- `myapp.db.queries.duration_ms`
- `myapp.cache.items.hit_total`

## Component Checklists

### API Endpoints
- Request count by endpoint and method
- Response time (p50, p95, p99)
- Error rate by status code
- Authentication failures
- Request/response payload sizes

### Database
- Connection pool (active, idle, waiting)
- Query duration by operation type
- Slow query count (threshold-based)
- Error count by type (timeout, constraint, connection)
- Transaction commit/rollback rates

### Message Queues
- Messages produced/consumed per topic
- Queue depth (current backlog)
- Processing latency (end-to-end)
- Consumer lag
- Dead letter queue size

### Caching
- Hit/miss ratio
- Eviction count and reason
- Cache size (entries and bytes)
- TTL expiration rate
- Connection pool status

### Locks/Synchronization
- Acquisition time
- Contention count (failed acquisitions)
- Hold duration
- Timeout count
- Deadlock occurrences

## Anti-patterns to Avoid

1. **Unbounded label cardinality** - Never use user IDs, session tokens, or request IDs as labels
2. **Missing failure paths** - Always instrument errors alongside successes
3. **No heartbeat metric** - Add a constant gauge (e.g., `app.up = 1`) to verify instrumentation works
4. **Inconsistent naming** - Stick to one convention across the codebase

## Full Reference

For detailed examples, patterns, and rationale, fetch the complete guide:
https://pierrezemb.fr/posts/practical-guide-to-application-metrics/
