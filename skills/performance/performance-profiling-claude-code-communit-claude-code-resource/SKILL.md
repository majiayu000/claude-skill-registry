---
name: performance-profiling
description: Performance analysis methodology — identifying bottlenecks, profiling techniques, benchmarking, and common optimization patterns. Use when investigating or improving performance.
---

# Performance Profiling

## Core Principle: Measure First

Never optimize without data. Gut-feeling optimization leads to wasted effort on non-bottlenecks. Always follow this sequence:

1. Define a measurable performance goal (e.g., "page load under 2 seconds on 3G").
2. Measure current performance with appropriate tooling.
3. Identify the actual bottleneck from profiling data.
4. Apply a targeted fix.
5. Re-measure to confirm improvement.
6. Repeat until the goal is met.

## Bottleneck Categories

Before diving into tools, classify the bottleneck you are investigating:

| Category | Symptoms | Key Metrics | Common Causes |
|----------|----------|-------------|---------------|
| CPU | High CPU usage, slow computation | CPU time, flame graph hot paths | Tight loops, unoptimized algorithms, excessive parsing |
| Memory | Growing memory footprint, OOM errors | Heap size, allocation rate, GC pauses | Memory leaks, large object graphs, unbounded caches |
| I/O (Disk) | Slow reads/writes, high iowait | IOPS, throughput, latency | Synchronous file ops, missing buffering, excessive logging |
| Network | High latency, timeouts | RTT, TTFB, bandwidth utilization | Chatty APIs, missing compression, no connection reuse |
| Database | Slow queries, connection exhaustion | Query time, lock contention, pool usage | Missing indexes, N+1 queries, full table scans |

## Browser Performance Profiling

### Chrome DevTools Performance Tab

Use the Performance tab to capture a runtime profile:

1. Open DevTools (`Cmd+Option+I` / `Ctrl+Shift+I`).
2. Go to the **Performance** tab.
3. Click **Record**, perform the user action, then **Stop**.
4. Analyze the flame chart for long tasks (anything over 50ms blocks the main thread).
5. Check the **Summary** pane for a breakdown of Scripting, Rendering, Painting, and Idle time.

Key things to look for:

- Long Tasks (red corners in the timeline) blocking user interaction.
- Layout thrashing — repeated forced reflows from interleaved reads and writes.
- Excessive paint regions — use the **Rendering** drawer to enable Paint Flashing.

### Core Web Vitals

| Metric | What It Measures | Good | Needs Improvement | Poor |
|--------|-----------------|------|-------------------|------|
| LCP (Largest Contentful Paint) | Loading performance | <= 2.5s | <= 4.0s | > 4.0s |
| FID (First Input Delay) | Interactivity | <= 100ms | <= 300ms | > 300ms |
| INP (Interaction to Next Paint) | Responsiveness | <= 200ms | <= 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | Visual stability | <= 0.1 | <= 0.25 | > 0.25 |

Common fixes by metric:

- **LCP**: Optimize the critical rendering path, preload hero images, use `fetchpriority="high"` on LCP elements, server-side render above-the-fold content.
- **FID / INP**: Break up long tasks with `requestIdleCallback` or `scheduler.yield()`, defer non-critical JavaScript, use web workers for heavy computation.
- **CLS**: Set explicit `width` and `height` on images and embeds, avoid injecting content above existing content, use `transform` animations instead of layout-triggering properties.

### Lighthouse

Run Lighthouse audits from DevTools, CLI, or CI:

```bash
# CLI usage
npx lighthouse https://example.com --output=json --output-path=./report.json

# CI-friendly with budget assertions
npx lighthouse https://example.com --budget-path=./budget.json
```

Example performance budget file (`budget.json`):

```json
[
  {
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "image", "budget": 200 },
      { "resourceType": "total", "budget": 800 }
    ],
    "resourceCounts": [
      { "resourceType": "third-party", "budget": 5 }
    ]
  }
]
```

## Backend Profiling

### Flame Graphs

Flame graphs visualize call stacks with width proportional to time spent. Generate them for your runtime:

```bash
# Node.js — built-in profiler
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# Node.js — 0x for flame graphs
npx 0x app.js

# Python — py-spy (no code changes needed)
py-spy record -o profile.svg -- python app.py

# Go — built-in pprof
import _ "net/http/pprof"
# then visit http://localhost:6060/debug/pprof/profile?seconds=30
go tool pprof -http=:8080 profile.pb.gz
```

### Database Query Analysis

Always use `EXPLAIN` (or `EXPLAIN ANALYZE`) before optimizing queries:

```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.name;
```

What to look for in the output:

| Plan Node | Concern | Action |
|-----------|---------|--------|
| Seq Scan on large table | Missing index | Add an index on the filter/join column |
| Nested Loop with high row count | N+1 pattern or missing index | Add index or restructure query |
| Sort with high cost | Sorting without index support | Add a covering index with sort column |
| Hash Join with large build side | Large intermediate result | Filter earlier, check join conditions |

### Connection Pooling

Exhausting database connections is a common backend bottleneck. Use a connection pool and configure it properly:

```javascript
// Node.js with pg-pool
const pool = new Pool({
  max: 20,              // Maximum connections (tune to DB limit / app instances)
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

// Always release connections — use pool.query for auto-release
const result = await pool.query('SELECT * FROM users WHERE id = $1', [userId]);
```

## Memory Leak Detection

### Heap Snapshots (Browser / Node.js)

1. Take a heap snapshot before the suspected action.
2. Perform the action (e.g., navigate to a page and back, or process N requests).
3. Take a second snapshot.
4. Compare snapshots — look for objects that grew unexpectedly.

```javascript
// Node.js — trigger heap snapshot programmatically
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot(filename) {
  const snapshotStream = v8.writeHeapSnapshot(filename);
  console.log(`Heap snapshot written to ${snapshotStream}`);
}
```

### Common Memory Leak Patterns

| Pattern | Description | Fix |
|---------|-------------|-----|
| Forgotten event listeners | Listeners added but never removed | Remove listeners in cleanup / `AbortController` |
| Closures over large scopes | Callback retains reference to large object | Null out references, narrow closure scope |
| Unbounded caches / maps | Map grows indefinitely | Use LRU cache with max size, or `WeakRef` / `WeakMap` |
| Detached DOM nodes | DOM removed but referenced in JS | Clear references after removal |
| Timers not cleared | `setInterval` without `clearInterval` | Store and clear timer IDs on cleanup |

### WeakRef for Cache-Friendly References

```javascript
class WeakCache {
  #cache = new Map();

  get(key) {
    const ref = this.#cache.get(key);
    if (!ref) return undefined;
    const value = ref.deref();
    if (!value) this.#cache.delete(key);
    return value;
  }

  set(key, value) {
    this.#cache.set(key, new WeakRef(value));
  }
}
```

## N+1 Query Detection and Resolution

### Identifying N+1 Queries

An N+1 query occurs when code fetches a list (1 query) then fetches related data for each item individually (N queries).

```javascript
// BAD: N+1 — 1 query for posts + N queries for authors
const posts = await db.query('SELECT * FROM posts LIMIT 50');
for (const post of posts) {
  post.author = await db.query('SELECT * FROM users WHERE id = $1', [post.author_id]);
}

// GOOD: Single join query
const posts = await db.query(`
  SELECT p.*, u.name AS author_name
  FROM posts p
  JOIN users u ON u.id = p.author_id
  LIMIT 50
`);

// GOOD: Batch loading with IN clause
const posts = await db.query('SELECT * FROM posts LIMIT 50');
const authorIds = [...new Set(posts.map(p => p.author_id))];
const authors = await db.query('SELECT * FROM users WHERE id = ANY($1)', [authorIds]);
const authorMap = new Map(authors.map(a => [a.id, a]));
posts.forEach(p => p.author = authorMap.get(p.author_id));
```

### Detection Tools

- **ORM query logging**: Enable SQL logging and watch for repeated patterns.
- **DataLoader pattern**: Batch and deduplicate requests within a single tick.
- **APM tools**: New Relic, Datadog APM — highlight repeated queries per request.

## Caching Strategies

| Strategy | Scope | TTL | Best For | Invalidation |
|----------|-------|-----|----------|--------------|
| Memoization | In-process, single call | Request lifetime | Pure function results, expensive computation | Automatic (GC) |
| In-memory cache (LRU) | In-process, across requests | Seconds to minutes | Hot config data, session data | TTL expiry, manual purge |
| HTTP cache (`Cache-Control`) | Browser / CDN | Minutes to days | Static assets, API responses | Versioned URLs, `ETag` |
| CDN cache | Edge network | Minutes to hours | Static assets, public pages | Purge API, versioned filenames |
| Application cache (Redis) | Shared across instances | Configurable | Session store, computed results, rate limits | TTL, explicit delete, pub/sub |
| Database cache (materialized views) | Database | Manual refresh | Complex aggregations, reporting | `REFRESH MATERIALIZED VIEW` |

## Bundle Size Analysis

### Webpack Bundle Analyzer

```bash
# Install
npm install --save-dev webpack-bundle-analyzer

# Generate stats and visualize
npx webpack --profile --json > stats.json
npx webpack-bundle-analyzer stats.json
```

### Source Map Explorer

```bash
npx source-map-explorer dist/main.js
```

### Common Optimization Targets

| Issue | Detection | Fix |
|-------|-----------|-----|
| Entire lodash imported | Large `lodash` chunk | Use `lodash-es` with tree shaking or `lodash/get` imports |
| Moment.js locales | ~300KB of unused locales | Switch to `dayjs` or `date-fns`; use `IgnorePlugin` for moment |
| Duplicate dependencies | Multiple versions of same lib | `npm dedupe`, check `resolutions` / `overrides` |
| Uncompressed assets | Large transfer size | Enable gzip/brotli compression on server |
| No code splitting | Single massive bundle | Use dynamic `import()` for routes and heavy components |

## Database Indexing and Query Optimization

### Indexing Checklist

- [ ] Add indexes on all foreign key columns.
- [ ] Add indexes on columns used in `WHERE` clauses.
- [ ] Add composite indexes for multi-column queries (column order matters: most selective first).
- [ ] Consider partial indexes for queries filtering on a constant value.
- [ ] Avoid over-indexing — each index slows writes.
- [ ] Use `EXPLAIN ANALYZE` to verify index usage.
- [ ] Monitor unused indexes periodically and drop them.

```sql
-- Composite index for common query pattern
CREATE INDEX idx_orders_user_status ON orders (user_id, status);

-- Partial index for active records only
CREATE INDEX idx_users_active_email ON users (email) WHERE active = true;

-- Covering index to avoid table lookup
CREATE INDEX idx_posts_author_title ON posts (author_id) INCLUDE (title, created_at);
```

## Load Testing

### k6 Example

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up to 50 users
    { duration: '3m', target: 50 },   // Sustain 50 users
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // Less than 1% errors
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

```bash
k6 run load-test.js
```

### Artillery Example

```yaml
# artillery-config.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 180
      arrivalRate: 50
      name: "Sustained load"
scenarios:
  - name: "Browse and search"
    flow:
      - get:
          url: "/api/products"
      - think: 1
      - get:
          url: "/api/products/search?q=widget"
```

## Performance Review Checklist

Before shipping performance-sensitive changes, verify:

- [ ] Measured baseline performance before changes.
- [ ] Identified bottleneck category from profiling data.
- [ ] Applied targeted optimization based on data (not guessing).
- [ ] Re-measured to confirm improvement and quantify gain.
- [ ] No regressions in other areas (run full benchmark suite).
- [ ] Bundle size impact checked (if frontend).
- [ ] Database queries reviewed with `EXPLAIN ANALYZE` (if backend).
- [ ] Memory profile stable under sustained load (no leaks).
- [ ] Load test passes with acceptable p95 latency.
- [ ] Performance budget (if defined) still met.
- [ ] Changes documented with before/after metrics.
