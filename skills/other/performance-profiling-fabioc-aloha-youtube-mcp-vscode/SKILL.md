---
name: "Performance Profiling"
description: "CPU, memory, network bottleneck analysis — systematic performance investigation"
applyTo: "**/*profile*,**/*performance*,**/*benchmark*,**/*bottleneck*,**/*optimize*"
---

# Performance Profiling Skill

> Find the bottleneck before optimizing. Measure twice, optimize once.

---

## The Golden Rule

> **"Premature optimization is the root of all evil"** — Donald Knuth

But also:

> **"Measure, don't guess"** — Everyone who's optimized the wrong thing

---

## Performance Investigation Flow

```
┌──────────────────────────────────────────────────────────┐
│  1. OBSERVE                                              │
│     User reports slowness → Reproduce → Measure baseline │
├──────────────────────────────────────────────────────────┤
│  2. IDENTIFY                                             │
│     Profile → Find hotspots → Determine bottleneck type  │
├──────────────────────────────────────────────────────────┤
│  3. HYPOTHESIZE                                          │
│     Why is this slow? → Form theory → Plan fix           │
├──────────────────────────────────────────────────────────┤
│  4. OPTIMIZE                                             │
│     Implement fix → Measure improvement → Verify         │
├──────────────────────────────────────────────────────────┤
│  5. MONITOR                                              │
│     Add metrics → Set alerts → Prevent regression        │
└──────────────────────────────────────────────────────────┘
```

---

## Bottleneck Types

| Type | Symptoms | Investigation |
|------|----------|---------------|
| **CPU-bound** | High CPU, reasonable memory | Profile CPU, look for hot functions |
| **Memory-bound** | High memory, GC pauses | Heap profile, allocation tracking |
| **I/O-bound** | Low CPU, waiting on disk/network | Trace I/O operations, latency |
| **Concurrency** | Low utilization, contention | Thread dumps, lock analysis |
| **Network** | High latency to external services | Trace calls, measure RTT |
| **Database** | Slow queries, connection wait | Query plans, pool stats |

---

## CPU Profiling

### Node.js

```bash
# Built-in profiler
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# Chrome DevTools
node --inspect app.js
# Open chrome://inspect

# clinic.js (recommended)
npm install -g clinic
clinic doctor -- node app.js
clinic flame -- node app.js
```

### Reading Flame Graphs

```
┌─────────────────────────────────────────────────────────┐
│                        main()                            │
│  ┌─────────────────────────┐  ┌────────────────────────┐│
│  │      processData()      │  │     renderUI()         ││
│  │  ┌──────────┐  ┌──────┐ │  │  ┌──────┐  ┌────────┐  ││
│  │  │ parseJSON││ │sort()│ │  │  │layout││ │ paint()│  ││
│  │  └──────────┘  └──────┘ │  │  └──────┘  └────────┘  ││
│  └─────────────────────────┘  └────────────────────────┘│
└─────────────────────────────────────────────────────────┘
             Width = Time spent
```

- **Wide bars** = slow functions (targets for optimization)
- **Deep stacks** = look for unnecessary recursion
- **Flat tops** = time spent in that function, not children

### .NET

```bash
# dotnet-trace
dotnet trace collect --process-id <PID> --format speedscope

# dotnet-counters (quick overview)
dotnet counters monitor --process-id <PID>

# Visual Studio Profiler
# Debug → Performance Profiler → CPU Usage
```

---

## Memory Profiling

### Node.js Heap Analysis

```javascript
// Take heap snapshot programmatically
const v8 = require('v8');
const fs = require('fs');

const snapshotPath = `heap-${Date.now()}.heapsnapshot`;
const snapshot = v8.writeHeapSnapshot(snapshotPath);
console.log(`Heap snapshot written to ${snapshot}`);

// Memory usage check
console.log(process.memoryUsage());
// { rss, heapTotal, heapUsed, external, arrayBuffers }
```

### Common Memory Leaks

| Pattern | Cause | Fix |
|---------|-------|-----|
| **Uncleared intervals** | `setInterval` without cleanup | Store and clear in teardown |
| **Event listener accumulation** | Adding listeners without removing | Remove in cleanup |
| **Closure capture** | Large objects in closures | Null out references |
| **Growing collections** | Maps/Sets that never shrink | Implement eviction |
| **Global state** | Module-level caches | Add size limits, TTL |

### .NET Memory

```bash
# Heap dump
dotnet-dump collect -p <PID>
dotnet-dump analyze <dump-file>

# GC stats
dotnet-counters monitor --counters System.Runtime
```

---

## Network Profiling

### Browser DevTools

1. Network tab → Record
2. Look for:
   - **Waterfall** — Blocked/waiting time
   - **Size** — Large payloads
   - **Time** — Slow responses

### API Latency Breakdown

```
Total Request Time: 500ms
├── DNS Lookup: 20ms
├── TCP Connection: 30ms
├── TLS Handshake: 50ms (HTTPS)
├── Time to First Byte: 350ms  ← Server processing
└── Content Download: 50ms
```

### Common Network Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| **No keep-alive** | TCP handshake per request | Enable connection reuse |
| **Large payloads** | Slow transfer | Compress, paginate |
| **No caching** | Repeat downloads | Cache headers |
| **Waterfall blocking** | Sequential requests | Parallelize, HTTP/2 |
| **DNS latency** | First request slow | DNS prefetch |

---

## Database Profiling

### Query Analysis

```sql
-- PostgreSQL: Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 100;  -- Log queries > 100ms

-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.1;

-- SQL Server
-- Query Store or Extended Events
```

### Query Plan Analysis

```sql
-- PostgreSQL
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders WHERE customer_id = 123;

-- Look for:
-- - Seq Scan on large tables (need index?)
-- - High "actual rows" vs "plan rows" (stats out of date?)
-- - Nested loops with high iterations (join order?)
```

### Connection Pool Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Waiting for connection | Pool exhausted | Increase pool size |
| Many idle connections | Pool too large | Decrease max connections |
| Connection timeout | Queries holding connections | Add query timeout |

---

## VS Code Extension Profiling

For Alex-like extensions:

### Activation Performance

```typescript
// Measure activation time
export async function activate(context: vscode.ExtensionContext) {
    const start = performance.now();
    
    // ... initialization ...
    
    console.log(`Extension activated in ${performance.now() - start}ms`);
    
    // Report to telemetry
    telemetry.logUsage('activation', { durationMs: performance.now() - start });
}
```

### Command Performance

```typescript
// Wrap commands with timing
function withTiming<T>(
    commandId: string,
    handler: () => Promise<T>
): () => Promise<T> {
    return async () => {
        const start = performance.now();
        try {
            return await handler();
        } finally {
            const duration = performance.now() - start;
            if (duration > 1000) {
                console.warn(`Slow command: ${commandId} took ${duration}ms`);
            }
        }
    };
}
```

### Extension Host Profiling

1. Developer: Show Running Extensions
2. Note CPU/memory per extension
3. Use `--prof` flag for detailed profiling

---

## Benchmarking Best Practices

### Benchmark Setup

```typescript
// Node.js with Benchmark.js
import Benchmark from 'benchmark';

const suite = new Benchmark.Suite();

suite
  .add('Method A', () => methodA(testData))
  .add('Method B', () => methodB(testData))
  .on('cycle', (event) => console.log(String(event.target)))
  .on('complete', function() {
    console.log('Fastest is ' + this.filter('fastest').map('name'));
  })
  .run({ async: true });
```

### Benchmarking Rules

1. **Warm up** — Run once before measuring
2. **Isolate** — One variable at a time
3. **Repeat** — Statistical significance (n > 30)
4. **Realistic data** — Use production-like inputs
5. **Disable optimizations** — Ensure code runs (avoid dead code elimination)
6. **Document baseline** — Record environment, date, conditions

---

## Performance Optimization Patterns

### Caching

| Level | Latency | Example |
|-------|---------|---------|
| L1 Cache | 1ns | CPU cache |
| L2 Cache | 4ns | CPU cache |
| RAM | 100ns | In-memory cache |
| SSD | 100μs | Local database |
| Network | 1-100ms | Remote API |

**Cache strategy:**
```typescript
async function getCached<T>(key: string, fetchFn: () => Promise<T>, ttlMs: number): Promise<T> {
    const cached = cache.get(key);
    if (cached && cached.expires > Date.now()) {
        return cached.value;
    }
    const value = await fetchFn();
    cache.set(key, { value, expires: Date.now() + ttlMs });
    return value;
}
```

### Lazy Evaluation

```typescript
// ❌ Eager - computes immediately
const allUsers = users.filter(u => u.active).map(u => u.name);
const firstTen = allUsers.slice(0, 10);

// ✅ Lazy - computes only what's needed (with generator)
function* activeUserNames(users) {
    for (const user of users) {
        if (user.active) yield user.name;
    }
}
const iterator = activeUserNames(users);
const firstTen = Array.from({ length: 10 }, () => iterator.next().value);
```

### Batching

```typescript
// ❌ N requests
for (const id of ids) {
    await fetchUser(id);  // N round trips
}

// ✅ 1 request
const users = await fetchUsers(ids);  // Batch endpoint
```

### Debouncing/Throttling

```typescript
// Debounce - wait for pause in calls
function debounce(fn: Function, delay: number) {
    let timeout: NodeJS.Timeout;
    return (...args: any[]) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}

// Throttle - max once per interval
function throttle(fn: Function, interval: number) {
    let lastCall = 0;
    return (...args: any[]) => {
        const now = Date.now();
        if (now - lastCall >= interval) {
            lastCall = now;
            fn(...args);
        }
    };
}
```

---

## Performance Budget

Define acceptable limits:

| Metric | Budget | Measurement |
|--------|--------|-------------|
| Page load (LCP) | < 2.5s | Lighthouse |
| API response (P95) | < 500ms | APM |
| Memory (steady state) | < 100MB | Heap snapshot |
| Bundle size | < 200KB gzip | Build output |
| Startup time | < 100ms | Activation timing |

---

## Implementation Checklist

### Investigation

- [ ] Reproduce the performance issue
- [ ] Establish baseline measurement
- [ ] Identify bottleneck type (CPU/memory/I/O/network)
- [ ] Profile with appropriate tool
- [ ] Find the hotspot

### Optimization

- [ ] Form hypothesis for fix
- [ ] Implement fix (smallest change first)
- [ ] Measure improvement
- [ ] Verify no regression elsewhere
- [ ] Document the change

### Prevention

- [ ] Add performance metric to monitoring
- [ ] Set alert threshold
- [ ] Add benchmark to CI
- [ ] Update performance budget

---

## Related Skills

- **observability-monitoring** — Ongoing performance visibility
- **database-design** — Query optimization at design level
- **debugging-patterns** — Systematic investigation approaches
- **code-review** — Catch performance issues in review

---

*The fastest code is code that doesn't run. The second fastest is code that runs once.*
