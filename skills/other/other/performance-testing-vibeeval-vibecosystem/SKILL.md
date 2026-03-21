---
name: performance-testing
description: Load testing with k6/Artillery, response time thresholds, memory leak detection, N+1 query detection, and CI integration.
---

# Performance Testing

## k6 Script Patterns

### Basic scenario with stages
```javascript
// k6 run load-test.js
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // ramp up
    { duration: '1m',  target: 50 },   // hold load
    { duration: '30s', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    http_req_failed:   ['rate<0.01'],   // < 1% error rate
  },
}

export default function () {
  const res = http.get('https://api.example.com/users')
  check(res, {
    'status is 200':       (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  })
  sleep(1)
}
```

### POST with auth
```javascript
export default function () {
  const payload = JSON.stringify({ email: 'test@example.com', password: 'secret' })
  const headers = { 'Content-Type': 'application/json' }
  const res = http.post(`${BASE_URL}/auth/login`, payload, { headers })
  const token = res.json('token')

  http.get(`${BASE_URL}/profile`, {
    headers: { Authorization: `Bearer ${token}` },
  })
}
```

## Load Test Types

| Type | Duration | Target VU | Purpose |
|------|----------|-----------|---------|
| Smoke | 1 min | 1-5 | Verify script works, no regressions |
| Load | 30 min | expected peak | Normal production conditions |
| Stress | 60 min | 2-3x peak | Find breaking point |
| Spike | 2 min | 10x peak → 0 | Sudden traffic burst behavior |
| Soak | 4-8 hours | 80% peak | Memory leaks, degradation over time |

## Threshold Definitions

```javascript
export const options = {
  thresholds: {
    // Response time
    http_req_duration: ['p(95)<200', 'p(99)<500', 'avg<100'],

    // Error rate
    http_req_failed: ['rate<0.01'],   // < 1%

    // Custom metric for specific endpoint
    'http_req_duration{name:login}': ['p(95)<300'],

    // Checks pass rate
    checks: ['rate>0.99'],
  },
}
```

## CI Integration (GitHub Actions + k6)

```yaml
# .github/workflows/perf.yml
name: Performance Tests
on:
  pull_request:
    branches: [main]

jobs:
  k6:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run k6 smoke test
        uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/perf/smoke.js
          flags: --out json=results.json
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json
```

## Memory Leak Detection (Node.js)

### Heap snapshot approach
```bash
# Start with --inspect
node --inspect --expose-gc server.js

# In Chrome DevTools → Memory → Take heap snapshot
# Run load, take another snapshot
# Compare: growing retained objects = leak
```

### Programmatic detection
```javascript
import v8 from 'v8'

function checkHeap(label) {
  const stats = v8.getHeapStatistics()
  console.log(`[${label}] Heap used: ${Math.round(stats.used_heap_size / 1024 / 1024)}MB`)
}

setInterval(() => checkHeap('monitor'), 30_000)
```

### Common leak patterns to watch
```javascript
// BAD: event listener never removed
emitter.on('data', handler)   // grows on every request

// GOOD: cleanup in teardown
emitter.on('data', handler)
return () => emitter.off('data', handler)

// BAD: unbounded cache
const cache = {}
cache[userId] = data   // never evicted

// GOOD: bounded cache
import LRU from 'lru-cache'
const cache = new LRU({ max: 1000, ttl: 1000 * 60 * 5 })
```

## N+1 Query Detection

### pg_stat_statements (PostgreSQL)
```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find repetitive queries during a load test window
SELECT
  query,
  calls,
  mean_exec_time,
  total_exec_time
FROM pg_stat_statements
WHERE calls > 100
ORDER BY calls DESC
LIMIT 20;
```

### Query logging (development)
```javascript
// Prisma: log all queries
const prisma = new PrismaClient({
  log: ['query'],
})

// Detect N+1: same query fired N times in a request
// Fix: use include/select or DataLoader
```

### DataLoader pattern (N+1 fix)
```javascript
import DataLoader from 'dataloader'

const userLoader = new DataLoader(async (ids) => {
  const users = await db.user.findMany({ where: { id: { in: ids } } })
  return ids.map(id => users.find(u => u.id === id))
})

// In resolver — batches automatically
const user = await userLoader.load(post.authorId)
```

## Web Vitals / Lighthouse CI

```yaml
# .github/workflows/lhci.yml
- name: Lighthouse CI
  run: |
    npm install -g @lhci/cli
    lhci autorun
  env:
    LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

```json
// lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.8 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    }
  }
}
```

## Trend Tracking

Store k6 results to Grafana/InfluxDB for trend visualization:

```bash
k6 run --out influxdb=http://localhost:8086/k6 load-test.js
```

Or export JSON and compare baselines:

```bash
k6 run --out json=results-$(git rev-parse --short HEAD).json load-test.js
```
