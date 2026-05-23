---
name: optimizing-performance
description: Guides performance optimization, profiling techniques, and bottleneck identification. Use when improving application speed, reducing resource usage, or diagnosing performance issues.
license: MIT
compatibility: opencode
metadata:
  category: quality
  audience: developers
---

# Optimizing Performance

Strategies for identifying, analyzing, and resolving performance bottlenecks.

## When to Use This Skill

- Application is running slowly
- High resource consumption (CPU, memory)
- Database queries are slow
- API response times are high
- Need to scale for more users
- Preparing for load testing

---

## Performance Optimization Philosophy

### The Golden Rules

1. **Measure first** - Never optimize without data
2. **Optimize the right thing** - Find the actual bottleneck
3. **Keep it simple** - Complexity often hurts performance
4. **Test after** - Verify the optimization worked
5. **Document trade-offs** - Performance often costs readability

### The 80/20 Rule

```
80% of performance problems come from 20% of the code.

Focus on:
├── Hot paths (frequently executed code)
├── I/O operations (database, network, disk)
├── Memory allocation patterns
└── Algorithm complexity
```

---

## Profiling Techniques

### Types of Profiling

| Type | What It Measures | Tools |
|------|------------------|-------|
| CPU Profiling | Time spent in functions | pprof, py-spy, Chrome DevTools |
| Memory Profiling | Allocation patterns, leaks | Valgrind, memory_profiler, Chrome |
| I/O Profiling | Disk/network operations | strace, perf, Wireshark |
| Database Profiling | Query performance | EXPLAIN, slow query log, APM |

### Profiling Workflow

```
1. Establish baseline
   └─ Measure current performance with realistic load

2. Identify hotspots
   └─ Profile to find where time/resources are spent

3. Form hypothesis
   └─ Why is this slow? What would make it faster?

4. Implement fix
   └─ Make ONE change at a time

5. Measure again
   └─ Did it help? By how much?

6. Repeat
   └─ Until performance goals are met
```

### Common Profiling Commands

```bash
# Node.js
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Python
python -m cProfile -s cumtime app.py
py-spy record -o profile.svg -- python app.py

# Go
go test -cpuprofile cpu.prof -memprofile mem.prof -bench .
go tool pprof cpu.prof

# Database (PostgreSQL)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

---

## Common Bottleneck Patterns

### N+1 Query Problem

```
BAD (N+1 queries):
  SELECT * FROM posts;             -- 1 query
  SELECT * FROM users WHERE id=1;  -- N queries
  SELECT * FROM users WHERE id=2;
  ...

GOOD (2 queries):
  SELECT * FROM posts;
  SELECT * FROM users WHERE id IN (1, 2, 3, ...);
```

**Detection**: High query count relative to data returned
**Fix**: Eager loading, batch fetching, JOINs

### Unbounded Operations

```
BAD:
  SELECT * FROM logs;  -- Returns millions of rows

GOOD:
  SELECT * FROM logs
  WHERE created_at > NOW() - INTERVAL '1 day'
  LIMIT 100;
```

**Detection**: Memory spikes, timeouts
**Fix**: Pagination, limits, streaming

### Synchronous Blocking

```
BAD (blocking):
  result1 = fetch_api_1()  -- Wait 200ms
  result2 = fetch_api_2()  -- Wait 200ms
  return combine(result1, result2)  -- Total: 400ms

GOOD (parallel):
  [result1, result2] = await Promise.all([
    fetch_api_1(),
    fetch_api_2()
  ])  -- Total: ~200ms
```

**Detection**: Sequential I/O in traces
**Fix**: Parallel execution, async/await

### Excessive Allocation

```
BAD (allocates in loop):
  for item in large_list:
      result = []  # Allocates each iteration
      result.append(transform(item))

GOOD (pre-allocate):
  result = []
  for item in large_list:
      result.append(transform(item))

BEST (generator):
  def transform_all(items):
      for item in items:
          yield transform(item)
```

**Detection**: GC pressure, memory profiling
**Fix**: Object pooling, pre-allocation, generators

---

## Optimization Techniques

### Database Optimization

| Technique | When to Use | Impact |
|-----------|-------------|--------|
| **Indexing** | Slow WHERE/JOIN queries | High |
| **Query optimization** | Complex queries | High |
| **Connection pooling** | Many short connections | Medium |
| **Read replicas** | Read-heavy workloads | High |
| **Caching** | Repeated queries | Very High |
| **Denormalization** | Complex JOINs | Medium |

### Index Guidelines

```sql
-- Create index for frequently queried columns
CREATE INDEX idx_users_email ON users(email);

-- Composite index for multiple column queries
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Check if index is used
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### Caching Strategies

| Strategy | Use Case | Invalidation |
|----------|----------|--------------|
| **Cache-aside** | General purpose | Manual or TTL |
| **Write-through** | Strong consistency | On write |
| **Write-behind** | Write-heavy | Async batched |
| **Read-through** | Read-heavy | On miss |

```
Cache-aside pattern:
1. Check cache
2. If miss, query database
3. Store in cache
4. Return result
```

### Memory Optimization

| Technique | When to Use |
|-----------|-------------|
| Object pooling | Frequent allocation of same type |
| Lazy loading | Large objects not always needed |
| Streaming | Processing large datasets |
| Weak references | Cache that can be evicted |
| Data structure choice | Right structure for access pattern |

---

## Frontend Performance

### Core Web Vitals

| Metric | Target | What It Measures |
|--------|--------|------------------|
| LCP (Largest Contentful Paint) | < 2.5s | Load performance |
| INP (Interaction to Next Paint) | < 200ms | Interactivity |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability |

### Frontend Optimization Checklist

```
Loading Performance:
  ☐ Code splitting (lazy load routes/components)
  ☐ Tree shaking (remove unused code)
  ☐ Minification (JS, CSS)
  ☐ Compression (gzip, brotli)
  ☐ Image optimization (WebP, srcset, lazy loading)
  ☐ CDN for static assets

Runtime Performance:
  ☐ Virtualized lists for large data
  ☐ Debounce/throttle event handlers
  ☐ Memoization of expensive computations
  ☐ Avoid layout thrashing (batch DOM reads/writes)
  ☐ Use CSS transforms for animations
  ☐ Web Workers for heavy computation
```

### Bundle Optimization

```bash
# Analyze bundle size
npx webpack-bundle-analyzer stats.json
npx source-map-explorer bundle.js

# Identify large dependencies
npx depcheck
```

---

## API Performance

### Response Time Targets

| Percentile | Target | User Experience |
|------------|--------|-----------------|
| p50 | < 100ms | Fast |
| p95 | < 500ms | Acceptable |
| p99 | < 1s | Tolerable |

### API Optimization Techniques

| Technique | Benefit |
|-----------|---------|
| Response compression | Reduce transfer size |
| Pagination | Limit response size |
| Field selection | Return only needed data |
| ETags/Caching headers | Reduce redundant requests |
| Connection keep-alive | Reduce handshake overhead |
| HTTP/2 | Multiplexing, header compression |

### Batch Endpoints

```
BAD (multiple requests):
  GET /users/1
  GET /users/2
  GET /users/3

GOOD (batch):
  POST /users/batch
  { "ids": [1, 2, 3] }
```

---

## Monitoring and Alerting

### Key Metrics to Track

| Category | Metrics |
|----------|---------|
| Latency | p50, p95, p99 response times |
| Throughput | Requests per second |
| Errors | Error rate, error types |
| Saturation | CPU, memory, connections |

### Alerting Thresholds

```
Critical (page immediately):
  - Error rate > 5%
  - p99 latency > 5s
  - Service down

Warning (notify during hours):
  - Error rate > 1%
  - p95 latency > 2s
  - Resource utilization > 80%
```

### Logging for Performance

```python
# Log slow operations
import time
import logging

def timed_operation(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        if duration > 1.0:  # Log if > 1 second
            logging.warning(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper
```

---

## Performance Testing

### Load Testing Tools

| Tool | Use Case |
|------|----------|
| k6 | Modern, scriptable load testing |
| JMeter | Complex scenarios, GUI |
| Locust | Python-based, distributed |
| Artillery | YAML config, easy to start |
| wrk | Simple HTTP benchmarking |

### Load Test Example (k6)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

---

## Anti-Patterns to Avoid

1. **Premature optimization** - Optimize only proven bottlenecks
2. **Optimizing without measuring** - Guessing wastes time
3. **Over-caching** - Cache invalidation is hard
4. **Ignoring database** - Often the real bottleneck
5. **Complex micro-optimizations** - Usually not worth it
6. **Not testing under load** - Production behavior differs
7. **Ignoring cold starts** - First request matters too
8. **Over-engineering** - Simpler is often faster

---

## Quick Reference

```
PROFILING FLOW:
  Measure → Identify → Hypothesize → Fix → Measure → Repeat

COMMON BOTTLENECKS:
  N+1 queries → Eager loading
  Unbounded data → Pagination
  Blocking I/O → Parallelization
  Excessive allocation → Object pooling

DATABASE:
  Index frequently queried columns
  Use EXPLAIN ANALYZE
  Add caching layer

CACHING:
  Cache-aside for general use
  TTL for time-based invalidation
  Invalidate on write for consistency

TARGETS:
  p50 < 100ms
  p95 < 500ms
  p99 < 1s

TOOLS:
  CPU: pprof, py-spy
  Memory: valgrind, memory_profiler
  Load: k6, locust
  DB: EXPLAIN, slow query log
```
