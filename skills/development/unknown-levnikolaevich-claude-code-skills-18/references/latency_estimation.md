# Latency Estimation Heuristics

<!-- SCOPE: Known latency ranges for common operations. Used by profiler for time map estimation when runtime instrumentation is unavailable. -->
<!-- DO NOT add here: classification logic -> bottleneck_classification.md; profiling workflow -> ln-811 SKILL.md -->

Structural estimation heuristics for building time maps from static code analysis.

---

## Estimation Methods

| Method | When | Accuracy |
|--------|------|----------|
| Known latency patterns (this file) | Always — first pass | Low-Medium |
| Log/trace analysis | If APM, structured logs, or tracing exists | High |
| Existing benchmarks | If benchmarks exist in project | High |
| Code structure analysis | Count loop iterations, data sizes | Medium |

**Priority:** Use highest-accuracy method available. Fall back to heuristics below.

---

## Known Latency Ranges

### Network I/O

| Operation | Range | Typical | Notes |
|-----------|-------|---------|-------|
| HTTP (localhost/internal) | 1-50ms | 5-10ms | Service mesh, container-to-container |
| HTTP (same datacenter) | 5-100ms | 20-50ms | Cross-service within cluster |
| HTTP (external API) | 100-5000ms | 200-700ms | Third-party services, DNS lookup |
| HTTP (CDN cached) | 5-50ms | 10-20ms | Static assets, edge cache |
| gRPC (internal) | 0.5-20ms | 2-5ms | Binary protocol, connection reuse |
| WebSocket message | 0.1-5ms | 1ms | Already-open connection |
| DNS lookup | 1-100ms | 5-20ms | Cached vs uncached |
| TLS handshake | 20-100ms | 30-50ms | First connection only |

### Database

| Operation | Range | Typical | Notes |
|-----------|-------|---------|-------|
| Simple query (indexed) | 0.5-10ms | 1-3ms | Primary key, unique index |
| Query (composite index) | 1-20ms | 3-8ms | Multi-column index |
| Full table scan (small) | 5-50ms | 10-20ms | < 10K rows |
| Full table scan (large) | 50-5000ms | 200-1000ms | > 100K rows |
| Write (single row) | 1-20ms | 3-10ms | INSERT/UPDATE with index update |
| Batch write | 10-200ms | 20-50ms | Bulk INSERT (100-1000 rows) |
| Transaction commit | 1-10ms | 2-5ms | fsync, WAL write |
| Connection acquire | 0.1-5ms | 0.5-1ms | From pool; 50-200ms if new connection |
| Migration (ALTER TABLE) | 100ms-60s | Varies | Depends on table size |

### File System

| Operation | Range | Typical | Notes |
|-----------|-------|---------|-------|
| File read (< 1KB) | 0.1-5ms | 0.5-1ms | OS cache hit |
| File read (1KB-1MB) | 1-50ms | 5-10ms | SSD |
| File read (> 1MB) | 10-500ms | 50-100ms | Linear with size |
| File write (small) | 1-20ms | 2-5ms | Includes fsync |
| Directory listing | 1-50ms | 5-10ms | Depends on entry count |
| Temp file create+delete | 2-20ms | 5-10ms | OS overhead |

### CPU Operations

| Operation | Range | Typical | Notes |
|-----------|-------|---------|-------|
| JSON parse (1KB) | 0.01-0.1ms | 0.05ms | Language-dependent |
| JSON parse (1MB) | 1-20ms | 5-10ms | Linear with size |
| Regex match (simple) | 0.001-0.1ms | 0.01ms | Compiled regex |
| Regex match (complex) | 0.1-10ms | 0.5-2ms | Backtracking patterns |
| bcrypt hash (cost=10) | 50-200ms | 100ms | Intentionally slow |
| SHA-256 (1KB) | 0.001-0.01ms | 0.005ms | Hardware-accelerated |
| XML/HTML parse (small) | 0.1-5ms | 1ms | DOM parsing |
| Template rendering | 0.1-10ms | 1-3ms | Depends on complexity |
| Image resize | 50-2000ms | 200-500ms | Depends on dimensions |
| Sort (10K items) | 1-10ms | 2-5ms | O(n log n) |
| Sort (1M items) | 100-500ms | 200ms | O(n log n) |

### Cache

| Operation | Range | Typical | Notes |
|-----------|-------|---------|-------|
| In-memory cache hit | 0.001-0.01ms | 0.005ms | Dict/Map lookup |
| Redis GET | 0.1-2ms | 0.3-0.5ms | Network + deserialization |
| Redis SET | 0.1-2ms | 0.3-0.5ms | Network + serialization |
| Memcached GET | 0.1-1ms | 0.2-0.3ms | Slightly faster than Redis |
| Cache miss + compute | = cache_check + original_operation | Varies | Miss penalty |

### Message Queue

| Operation | Range | Typical | Notes |
|-----------|-------|---------|-------|
| Publish (async) | 1-20ms | 3-5ms | Non-blocking, fire-and-forget |
| Publish (sync/ack) | 5-100ms | 10-30ms | Wait for broker acknowledgment |
| Consume (poll) | 1-50ms | 5-10ms | If messages available |

---

## Loop Multiplier

When I/O operation is inside a loop:

```
total_time = single_operation_time x iteration_count
```

**Iteration count detection:**
- Explicit: `for i in range(N)` — use N
- Collection: `for item in items` — estimate collection size from context (API response, DB result)
- Unknown: estimate 10 iterations as default, note uncertainty

**Flag as Architecture bottleneck if:** `iteration_count x operation_time > 100ms`

---

## Estimation Confidence Levels

| Confidence | When | How to Communicate |
|------------|------|--------------------|
| HIGH | Based on logs/traces/benchmarks | "Measured: {value}ms" |
| MEDIUM | Based on heuristics + code structure | "Estimated: ~{value}ms (based on {N} {type} operations)" |
| LOW | Based on default heuristics only | "Rough estimate: ~{value}ms (no instrumentation data)" |

Always report confidence level alongside estimates.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-14
