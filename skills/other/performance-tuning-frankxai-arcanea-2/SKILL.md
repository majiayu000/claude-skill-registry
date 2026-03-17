---
name: arcanea-performance-tuning
description: Master the art of making systems fast. Profiling, optimization, caching, and the wisdom to know when performance matters and when it doesn't. Measure twice, optimize once.
version: 2.0.0
author: Arcanea
tags: [performance, optimization, profiling, speed, tuning, development]
triggers:
  - performance
  - optimization
  - slow
  - speed up
  - profiling
  - bottleneck
---

# The Performance Tuning Codex

> *"Premature optimization is the root of all evil. But mature optimization is the root of all delight."*

---

## The Performance Philosophy

### The Golden Rules

```
RULE 1: MEASURE FIRST
Don't guess where the bottleneck is.
Profile. Measure. Prove.

RULE 2: OPTIMIZE THE RIGHT THING
80% of time is spent in 20% of code.
Find that 20%.

RULE 3: SET TARGETS
"Faster" is not a goal.
"Under 200ms" is a goal.

RULE 4: REGRESSION PREVENTION
Performance is easy to lose.
Benchmark continuously.
```

### The Optimization Hierarchy

```
╔═══════════════════════════════════════════════════════════════════╗
║                    OPTIMIZATION HIERARCHY                          ║
║              (Optimize in this order)                              ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   1. ALGORITHM         │ O(n²) → O(n log n) = massive wins       ║
║   2. DATA STRUCTURE    │ Right structure for access pattern       ║
║   3. I/O               │ Network, disk, database calls            ║
║   4. MEMORY            │ Allocation, garbage collection           ║
║   5. CPU               │ Hot loops, cache efficiency              ║
║                                                                    ║
║   (Don't optimize #5 if #1-4 are the problem)                     ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## Profiling

### Types of Profiling

```
CPU PROFILING:
• What functions take the most time?
• Where are the hot paths?
• What's the call graph?

MEMORY PROFILING:
• Where is memory allocated?
• What's causing garbage collection?
• Are there memory leaks?

I/O PROFILING:
• What queries are slow?
• What network calls are made?
• What files are accessed?

TRACE PROFILING:
• What's the full request lifecycle?
• Where do requests spend time?
• What's the concurrency pattern?
```

### The Profiling Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE PROFILING CYCLE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. ESTABLISH BASELINE                                          │
│      Measure current performance                                 │
│      Record metrics: latency, throughput, resource usage         │
│                                                                  │
│   2. SET TARGET                                                   │
│      Define acceptable performance                               │
│      "P95 latency < 200ms"                                       │
│                                                                  │
│   3. PROFILE                                                      │
│      Identify bottlenecks                                        │
│      Focus on top 3 issues                                       │
│                                                                  │
│   4. HYPOTHESIZE                                                  │
│      Why is this slow?                                           │
│      What would make it faster?                                  │
│                                                                  │
│   5. OPTIMIZE                                                     │
│      Make ONE change                                             │
│      Keep it isolated                                            │
│                                                                  │
│   6. MEASURE                                                      │
│      Did it help?                                                │
│      Did it hurt anything else?                                  │
│                                                                  │
│   7. REPEAT                                                       │
│      Until target reached                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Common Performance Patterns

### The N+1 Query Problem

```
BAD: N+1 queries
┌──────────────────────────────────────────────────────────────┐
│ // Get all users (1 query)                                   │
│ users = db.query("SELECT * FROM users")                      │
│                                                              │
│ // For each user, get their orders (N queries)               │
│ for user in users:                                           │
│     orders = db.query("SELECT * FROM orders WHERE user_id=?")│
└──────────────────────────────────────────────────────────────┘

GOOD: Eager loading
┌──────────────────────────────────────────────────────────────┐
│ // Single query with JOIN                                    │
│ SELECT users.*, orders.*                                     │
│ FROM users                                                   │
│ LEFT JOIN orders ON orders.user_id = users.id                │
│                                                              │
│ // Or batch loading                                          │
│ SELECT * FROM orders WHERE user_id IN (1, 2, 3, 4, 5)       │
└──────────────────────────────────────────────────────────────┘
```

### Caching Strategies

```
╔═══════════════════════════════════════════════════════════════════╗
║                    CACHING STRATEGIES                              ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   CACHE-ASIDE (Lazy Loading)                                       ║
║   ┌─────────┐                                                      ║
║   │ Request │──┬──▶ Cache Hit ──▶ Return                          ║
║   └─────────┘  │                                                   ║
║                └──▶ Cache Miss ──▶ DB ──▶ Cache ──▶ Return        ║
║                                                                    ║
║   WRITE-THROUGH                                                    ║
║   ┌─────────┐                                                      ║
║   │  Write  │──▶ Cache ──▶ DB ──▶ Confirm                         ║
║   └─────────┘                                                      ║
║                                                                    ║
║   WRITE-BEHIND (Async)                                             ║
║   ┌─────────┐                                                      ║
║   │  Write  │──▶ Cache ──▶ Confirm                                ║
║   └─────────┘      │                                               ║
║                    └──▶ [Later] ──▶ DB                             ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝

CACHE INVALIDATION:
• TTL (Time To Live) - Simple but may serve stale data
• Event-based - Invalidate on writes
• Tag-based - Group related items
```

### Connection Pooling

```
WITHOUT POOLING:
┌──────────┐     ┌──────────┐
│ Request  │──▶──│ Connect  │──▶ 50-100ms overhead
└──────────┘     └──────────┘

WITH POOLING:
┌──────────┐     ┌──────────────┐     ┌──────────┐
│ Request  │──▶──│ Pool Manager │──▶──│ Reuse    │──▶ ~0ms
└──────────┘     └──────────────┘     └──────────┘

POOL CONFIGURATION:
• Min connections: Keep warm for base load
• Max connections: Limit to prevent exhaustion
• Idle timeout: Release unused connections
• Connection lifetime: Prevent stale connections
```

### Lazy Loading

```
EAGER (Load everything):
┌────────────────────────────────────────────────────────┐
│ class User:                                            │
│     def __init__(self, id):                            │
│         self.profile = load_profile(id)   # Always     │
│         self.orders = load_orders(id)     # Always     │
│         self.preferences = load_prefs(id) # Always     │
└────────────────────────────────────────────────────────┘

LAZY (Load on demand):
┌────────────────────────────────────────────────────────┐
│ class User:                                            │
│     def __init__(self, id):                            │
│         self._id = id                                  │
│         self._orders = None                            │
│                                                        │
│     @property                                          │
│     def orders(self):                                  │
│         if self._orders is None:                       │
│             self._orders = load_orders(self._id)       │
│         return self._orders                            │
└────────────────────────────────────────────────────────┘
```

---

## Database Optimization

### Index Optimization

```
WHEN TO INDEX:
✓ Columns in WHERE clauses
✓ Columns in JOIN conditions
✓ Columns in ORDER BY
✓ Columns with high selectivity

WHEN NOT TO INDEX:
✗ Small tables (full scan is faster)
✗ Columns with low selectivity (gender, boolean)
✗ Tables with heavy writes (index maintenance cost)
✗ Columns rarely queried

COMPOSITE INDEX ORDER:
• Equality conditions first
• Range conditions last
• Most selective first

INDEX (status, created_at)  -- status = 'active' AND created_at > ?
```

### Query Optimization

```
EXPLAIN ANALYZE:
Always explain before optimizing.

┌────────────────────────────────────────────────────────────────┐
│ EXPLAIN ANALYZE                                                 │
│ SELECT * FROM orders                                            │
│ WHERE user_id = 123 AND status = 'pending'                      │
│ ORDER BY created_at DESC                                        │
│ LIMIT 10;                                                       │
│                                                                 │
│ Look for:                                                       │
│ • Seq Scan (bad on large tables)                               │
│ • Index Scan (good)                                            │
│ • Sort (expensive if not indexed)                              │
│ • Rows vs estimated rows (accuracy of stats)                   │
└────────────────────────────────────────────────────────────────┘

COMMON FIXES:
• Add missing indexes
• Rewrite subqueries as JOINs
• Use LIMIT for pagination
• Avoid SELECT * in production
• Partition large tables
```

---

## Frontend Performance

### Critical Rendering Path

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  HTML   │──▶──│  CSS    │──▶──│   JS    │──▶──│ Render  │
│  Parse  │     │  Parse  │     │ Execute │     │  Paint  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │
     ▼               ▼               ▼
    DOM            CSSOM          Execute
   Build           Build         & Modify

OPTIMIZATION:
1. Minimize critical resources
2. Minimize critical bytes
3. Minimize critical path length
```

### Core Web Vitals

```
LCP (Largest Contentful Paint):
Target: < 2.5s
• Optimize images
• Preload critical resources
• Use CDN

FID (First Input Delay):
Target: < 100ms
• Break up long tasks
• Defer non-critical JS
• Use web workers

CLS (Cumulative Layout Shift):
Target: < 0.1
• Set image dimensions
• Reserve space for ads
• Avoid inserting content above fold
```

### Bundle Optimization

```
CODE SPLITTING:
// Instead of one large bundle
import { everything } from 'huge-library';

// Load on demand
const HeavyComponent = lazy(() => import('./HeavyComponent'));

TREE SHAKING:
// Bad: imports everything
import _ from 'lodash';

// Good: imports only what's used
import { debounce } from 'lodash-es';

COMPRESSION:
• Gzip: 70-90% reduction
• Brotli: 15-20% better than Gzip
• Enable on server and CDN
```

---

## Concurrency & Parallelism

### Async Patterns

```
SEQUENTIAL (Slow):
┌────────────────────────────────────────────────────────────────┐
│ result1 = await fetchUser()      // 100ms                      │
│ result2 = await fetchOrders()    // 150ms                      │
│ result3 = await fetchProducts()  // 120ms                      │
│ // Total: 370ms                                                │
└────────────────────────────────────────────────────────────────┘

PARALLEL (Fast):
┌────────────────────────────────────────────────────────────────┐
│ [user, orders, products] = await Promise.all([                 │
│     fetchUser(),                                               │
│     fetchOrders(),                                             │
│     fetchProducts()                                            │
│ ])                                                             │
│ // Total: 150ms (slowest call)                                │
└────────────────────────────────────────────────────────────────┘
```

### Rate Limiting & Backpressure

```
RATE LIMITING:
┌────────────────────────────────────────────────────────────────┐
│ Token Bucket Algorithm:                                         │
│                                                                 │
│ • Bucket has capacity (e.g., 100 tokens)                       │
│ • Tokens added at fixed rate (e.g., 10/second)                 │
│ • Each request consumes a token                                │
│ • No tokens = request rejected                                 │
└────────────────────────────────────────────────────────────────┘

BACKPRESSURE:
┌────────────────────────────────────────────────────────────────┐
│ When producer is faster than consumer:                          │
│                                                                 │
│ Options:                                                        │
│ • Drop: Discard excess (lossy)                                 │
│ • Buffer: Queue until processed (memory risk)                  │
│ • Sample: Process every Nth item                               │
│ • Slow down: Signal producer to wait                           │
└────────────────────────────────────────────────────────────────┘
```

---

## Monitoring & Metrics

### Key Metrics

```
THE FOUR GOLDEN SIGNALS:
┌─────────────────────────────────────────────────────────────┐
│ 1. LATENCY    │ Time to serve a request                    │
│ 2. TRAFFIC    │ Requests per second                        │
│ 3. ERRORS     │ Rate of failed requests                    │
│ 4. SATURATION │ How "full" the service is                  │
└─────────────────────────────────────────────────────────────┘

PERCENTILES:
• P50 (median): Typical experience
• P95: Most users' worst experience
• P99: Tail latency (important!)
• Max: Absolute worst case

Note: Average is misleading.
      A few slow requests hide in the average.
```

### Benchmarking

```
MICRO-BENCHMARKS:
• Test specific functions
• Isolate from I/O
• Run many iterations
• Beware of JIT warmup

LOAD TESTING:
• Simulate realistic traffic
• Measure at various loads
• Find the breaking point
• Test failure scenarios

TOOLS:
• k6, Artillery, Locust (load testing)
• wrk, hey (HTTP benchmarking)
• hyperfine (CLI benchmarking)
```

---

## Quick Reference

### Performance Checklist

```
□ Profiled to find actual bottlenecks
□ Set measurable performance targets
□ Optimized hot paths first
□ Added appropriate caching
□ Minimized I/O operations
□ Used connection pooling
□ Indexed frequently queried columns
□ Implemented lazy loading where appropriate
□ Set up performance monitoring
□ Established performance regression tests
```

### Common Performance Wins

```
| Problem              | Solution                    |
|----------------------|-----------------------------|
| N+1 queries          | Eager loading, batch        |
| Slow queries         | Add indexes, optimize SQL   |
| Large payloads       | Pagination, compression     |
| Repeated computation | Caching, memoization        |
| Synchronous waits    | Async, parallel execution   |
| Cold starts          | Warmup, connection pools    |
| Large bundles        | Code splitting, tree shake  |
| Slow images          | Lazy load, WebP, CDN        |
```

### The Performance Mantras

```
"Measure first, optimize second"
"The fastest code is code that doesn't run"
"Cache invalidation is hard; TTL is your friend"
"Profile in production, not just development"
"Optimize for the common case"
```

---

*"Performance is not about making things fast. It's about removing what makes things slow."*
