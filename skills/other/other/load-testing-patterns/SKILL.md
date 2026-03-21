---
name: load-testing-patterns
description: k6 script templates, load profiles, response time thresholds, SLO validation, and performance testing strategies.
---

# Load Testing Patterns

Performance validation with k6 for SLO-driven load testing.

## Basic k6 Script Template

```javascript
import http from 'k6/http'
import { check, sleep } from 'k6'
import { Rate, Trend } from 'k6/metrics'

// Custom metrics
const errorRate = new Rate('errors')
const loginDuration = new Trend('login_duration')

// Thresholds define pass/fail criteria
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],  // 95th < 500ms, 99th < 1s
    http_req_failed: ['rate<0.01'],                    // Error rate < 1%
    errors: ['rate<0.05'],                             // Custom error rate < 5%
  },
  scenarios: {
    smoke: {
      executor: 'constant-vus',
      vus: 5,
      duration: '1m',
    }
  }
}

export default function () {
  const res = http.get('https://api.example.com/health')

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body has status': (r) => JSON.parse(r.body).status === 'ok',
  }) || errorRate.add(1)

  sleep(1)
}
```

## Load Profiles

```javascript
export const options = {
  scenarios: {
    // 1. Smoke Test: verify system works under minimal load
    smoke: {
      executor: 'constant-vus',
      vus: 3,
      duration: '1m',
    },

    // 2. Load Test: normal expected traffic
    load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },   // Ramp up
        { duration: '5m', target: 50 },   // Steady state
        { duration: '2m', target: 0 },    // Ramp down
      ],
    },

    // 3. Stress Test: find breaking point
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 200 },  // Beyond normal
        { duration: '5m', target: 200 },
        { duration: '2m', target: 300 },  // Breaking point?
        { duration: '5m', target: 300 },
        { duration: '5m', target: 0 },
      ],
    },

    // 4. Spike Test: sudden traffic surge
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 10 },
        { duration: '10s', target: 500 },  // Instant spike
        { duration: '1m', target: 500 },
        { duration: '10s', target: 10 },   // Instant drop
        { duration: '1m', target: 10 },
      ],
    },

    // 5. Soak Test: sustained load over time (memory leaks, connection exhaustion)
    soak: {
      executor: 'constant-vus',
      vus: 50,
      duration: '2h',
    },
  }
}
```

## Realistic User Scenarios

```javascript
import http from 'k6/http'
import { check, group, sleep } from 'k6'

const BASE_URL = __ENV.BASE_URL || 'https://api.example.com'

export default function () {
  // Simulate real user journey, not isolated endpoints
  let token

  group('01_login', () => {
    const res = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
      email: `user${__VU}@test.com`,
      password: 'testpass123'
    }), { headers: { 'Content-Type': 'application/json' } })

    check(res, { 'login successful': (r) => r.status === 200 })
    token = JSON.parse(res.body).token
  })

  sleep(Math.random() * 3 + 1)  // Think time: 1-4 seconds

  group('02_browse_products', () => {
    const headers = { Authorization: `Bearer ${token}` }

    const listRes = http.get(`${BASE_URL}/products?page=1&limit=20`, { headers })
    check(listRes, { 'products loaded': (r) => r.status === 200 })

    const products = JSON.parse(listRes.body).data
    if (products.length > 0) {
      const product = products[Math.floor(Math.random() * products.length)]
      const detailRes = http.get(`${BASE_URL}/products/${product.id}`, { headers })
      check(detailRes, { 'product detail loaded': (r) => r.status === 200 })
    }
  })

  sleep(Math.random() * 2 + 1)

  group('03_add_to_cart', () => {
    const res = http.post(`${BASE_URL}/cart/items`, JSON.stringify({
      productId: 'prod_001',
      quantity: 1
    }), {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      }
    })
    check(res, { 'item added to cart': (r) => r.status === 201 })
  })
}
```

## SLO Validation

```javascript
export const options = {
  thresholds: {
    // SLO: Availability > 99.9%
    http_req_failed: ['rate<0.001'],

    // SLO: p50 < 100ms, p95 < 500ms, p99 < 1000ms
    http_req_duration: [
      'p(50)<100',
      'p(95)<500',
      'p(99)<1000',
    ],

    // SLO per endpoint using tags
    'http_req_duration{name:login}': ['p(95)<800'],
    'http_req_duration{name:get_products}': ['p(95)<200'],
    'http_req_duration{name:checkout}': ['p(95)<2000'],

    // SLO: Throughput > 1000 RPS
    http_reqs: ['rate>1000'],
  }
}

// Tag requests for per-endpoint SLOs
export default function () {
  http.get(`${BASE_URL}/products`, { tags: { name: 'get_products' } })
  http.post(`${BASE_URL}/auth/login`, payload, { tags: { name: 'login' } })
}
```

## CI Integration

```yaml
# .github/workflows/load-test.yml
name: Load Test
on:
  pull_request:
    branches: [main]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/load/smoke.js
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}

      # k6 exits non-zero if thresholds fail → PR check fails
```

## Checklist

- [ ] Run smoke test on every PR (fast, catches regressions)
- [ ] Load test weekly against staging with production-like data
- [ ] Stress test quarterly to find breaking points
- [ ] Soak test before major releases (2+ hours, detect memory leaks)
- [ ] Thresholds set per endpoint, not just global p95
- [ ] Realistic think times between requests (sleep 1-5s)
- [ ] Use multiple VU scenarios (not everyone does the same thing)
- [ ] Store results in Grafana/InfluxDB for trend analysis

## Anti-Patterns

- Testing only happy paths: include error scenarios (404, 429, 500)
- No think time: unrealistic request rate, not how users behave
- Testing against production without traffic control (use staging)
- Single endpoint tests: real users hit multiple endpoints per session
- Ignoring connection time: p95 duration hides DNS/TLS overhead
- Hardcoded test data: VUs sharing same user account causes contention
