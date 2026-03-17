---
description: Performance testing expert for load testing (k6, Artillery), web performance (Lighthouse CI, Core Web Vitals), database performance, and memory/resource profiling. Use for performance tests, load tests, stress tests, lighthouse audits, k6 scripts, web vitals monitoring, or performance budgets.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# Performance Testing Expert

## When to Use

Invoke this skill when the task involves:
- **Load testing**: "performance test", "load test", "stress test", "soak test", "spike test"
- **Web performance**: "lighthouse", "performance budget", "bundle size", "core web vitals"
- **Specific tools**: "k6", "artillery", "lighthouse ci", "webpagetest"
- **Metrics**: "web vitals", "LCP", "FID", "INP", "CLS", "TTFB", "p95 latency"
- **Database performance**: "slow query", "n+1 query", "connection pool"
- **Resource profiling**: "memory leak", "cpu profile", "network throttle"

## Core Expertise

- **Load testing** with k6 (primary) and Artillery
- **Web performance** with Lighthouse CI and performance budgets
- **Core Web Vitals** monitoring and optimization
- **Database performance** testing and query analysis
- **Memory and resource** leak detection and profiling

---

## 1. Load Testing with k6

k6 is the primary tool for HTTP load testing. It uses JavaScript ES6 modules, runs in Go for high performance, and integrates with CI/CD pipelines.

### Installation

```bash
# macOS
brew install k6

# Docker
docker run --rm -i grafana/k6 run - <script.js

# npm (for CI)
npm install -g k6
```

### Basic k6 Script

```javascript
// load-tests/api-load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 20 },   // ramp up to 20 VUs
    { duration: '3m', target: 20 },   // hold at 20 VUs
    { duration: '1m', target: 0 },    // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // error rate below 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'body has users': (r) => JSON.parse(r.body).length > 0,
  });

  sleep(1);
}
```

### k6 Scenario Patterns

#### Stress Test (Find Breaking Point)

```javascript
export const options = {
  scenarios: {
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 200 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 300 },
        { duration: '5m', target: 300 },
        { duration: '5m', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(99)<1500'],
    http_req_failed: ['rate<0.05'],
  },
};
```

#### Spike Test (Sudden Burst)

```javascript
export const options = {
  scenarios: {
    spike: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 10 },   // warm up
        { duration: '10s', target: 500 },  // spike
        { duration: '1m', target: 500 },   // hold spike
        { duration: '10s', target: 10 },   // drop
        { duration: '2m', target: 10 },    // recovery
        { duration: '30s', target: 0 },    // ramp down
      ],
    },
  },
};
```

#### Soak Test (Extended Duration)

```javascript
export const options = {
  scenarios: {
    soak: {
      executor: 'constant-vus',
      vus: 50,
      duration: '4h',
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<800', 'p(99)<1500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

#### Constant Request Rate

```javascript
export const options = {
  scenarios: {
    constant_rate: {
      executor: 'constant-arrival-rate',
      rate: 100,             // 100 requests per timeUnit
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
};
```

### k6 Custom Metrics

```javascript
import { Counter, Trend, Rate, Gauge } from 'k6/metrics';

const orderDuration = new Trend('order_duration');
const orderErrors = new Rate('order_errors');
const ordersCreated = new Counter('orders_created');

export default function () {
  const start = Date.now();
  const res = http.post('https://api.example.com/orders', JSON.stringify({
    product: 'widget', quantity: 1,
  }), { headers: { 'Content-Type': 'application/json' } });

  orderDuration.add(Date.now() - start);
  orderErrors.add(res.status !== 201);
  if (res.status === 201) ordersCreated.add(1);
}
```

### k6 Authentication and Headers

```javascript
import http from 'k6/http';
import { check } from 'k6';

export function setup() {
  const loginRes = http.post('https://api.example.com/auth/login', JSON.stringify({
    username: 'loadtest',
    password: __ENV.LOAD_TEST_PASSWORD,
  }), { headers: { 'Content-Type': 'application/json' } });

  return { token: JSON.parse(loginRes.body).token };
}

export default function (data) {
  const params = {
    headers: {
      Authorization: `Bearer ${data.token}`,
      'Content-Type': 'application/json',
    },
  };
  const res = http.get('https://api.example.com/protected', params);
  check(res, { 'authenticated request OK': (r) => r.status === 200 });
}
```

### k6 Multi-Scenario (Mixed Workload)

```javascript
export const options = {
  scenarios: {
    browse: {
      executor: 'constant-vus', vus: 30, duration: '10m',
      exec: 'browseProducts',
    },
    checkout: {
      executor: 'ramping-arrival-rate', startRate: 5, timeUnit: '1s',
      stages: [{ duration: '5m', target: 20 }, { duration: '5m', target: 20 }],
      preAllocatedVUs: 50, exec: 'checkout',
    },
  },
  thresholds: {
    'http_req_duration{scenario:browse}': ['p(95)<300'],
    'http_req_duration{scenario:checkout}': ['p(95)<1000'],
  },
};

export function browseProducts() {
  http.get('https://api.example.com/products');
  sleep(Math.random() * 3 + 1);
}

export function checkout() {
  http.post('https://api.example.com/checkout', JSON.stringify({
    items: [{ id: 1, qty: 1 }],
  }), { headers: { 'Content-Type': 'application/json' } });
}
```

### Running k6

```bash
k6 run load-tests/api-load.js                                    # Basic run
k6 run -e BASE_URL=https://staging.example.com load-tests/api-load.js  # Env vars
k6 run --vus 100 --duration 5m load-tests/api-load.js            # Override options
k6 run --out json=results.json load-tests/api-load.js             # JSON output
k6 run --out influxdb=http://localhost:8086/k6 load-tests/api-load.js  # Grafana
```

---

## 2. Load Testing with Artillery

Artillery uses YAML configuration and is well-suited for quick HTTP and WebSocket load tests.

### Artillery Configuration

```yaml
# load-tests/artillery.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 5
      name: "Warm up"
    - duration: 120
      arrivalRate: 20
      rampTo: 50
      name: "Ramp up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
  defaults:
    headers:
      Content-Type: "application/json"
  ensure:
    p95: 500
    maxErrorRate: 1

scenarios:
  - name: "Browse and Purchase"
    weight: 70
    flow:
      - get:
          url: "/products"
          capture:
            - json: "$[0].id"
              as: "productId"
      - think: 2
      - get:
          url: "/products/{{ productId }}"
      - post:
          url: "/cart"
          json:
            productId: "{{ productId }}"
            quantity: 1

  - name: "Search"
    weight: 30
    flow:
      - get:
          url: "/search?q=widget"
      - think: 3
```

### Running Artillery

```bash
npx artillery run load-tests/artillery.yml                        # Run test
npx artillery run --output report.json load-tests/artillery.yml   # Save results
npx artillery report report.json                                  # HTML report
npx artillery quick --count 50 --num 10 https://api.example.com/health  # Quick test
```

---

## 3. Web Performance with Lighthouse CI

### Lighthouse CI Configuration

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/products',
        'http://localhost:3000/checkout',
      ],
      startServerCommand: 'npm run start',
      startServerReadyPattern: 'Server started',
      numberOfRuns: 3,
      settings: { preset: 'desktop' },
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['warn', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.9 }],

        // Core Web Vitals
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }],

        // Bundle and resource budgets
        'resource-summary:script:size': ['error', { maxNumericValue: 300000 }],
        'resource-summary:total:size': ['error', { maxNumericValue: 800000 }],
        'resource-summary:third-party:count': ['warn', { maxNumericValue: 10 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

### Performance Budgets

```json
[
  {
    "path": "/*",
    "timings": [
      { "metric": "interactive", "budget": 3000 },
      { "metric": "first-contentful-paint", "budget": 1500 },
      { "metric": "largest-contentful-paint", "budget": 2500 },
      { "metric": "cumulative-layout-shift", "budget": 0.1 },
      { "metric": "total-blocking-time", "budget": 300 }
    ],
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "stylesheet", "budget": 100 },
      { "resourceType": "image", "budget": 500 },
      { "resourceType": "total", "budget": 1000 }
    ],
    "resourceCounts": [
      { "resourceType": "script", "budget": 15 },
      { "resourceType": "third-party", "budget": 10 },
      { "resourceType": "total", "budget": 50 }
    ]
  }
]
```

### Lighthouse CI in GitHub Actions

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci && npm run build
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
      - name: Upload Lighthouse Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: lighthouse-report
          path: .lighthouseci/
```

### Lighthouse Programmatic API

```typescript
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

async function runLighthouse(url: string) {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
  const result = await lighthouse(url, {
    port: chrome.port, output: 'json', onlyCategories: ['performance'],
  });

  const { categories, audits } = result.lhr;
  console.log('Performance Score:', categories.performance.score * 100);
  console.log('LCP:', audits['largest-contentful-paint'].displayValue);
  console.log('TBT:', audits['total-blocking-time'].displayValue);
  console.log('CLS:', audits['cumulative-layout-shift'].displayValue);

  if (categories.performance.score < 0.9) {
    console.error('Performance score below 90!');
    process.exit(1);
  }
  await chrome.kill();
}
```

---

## 4. Core Web Vitals Monitoring

### Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | <= 2.5s | <= 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | <= 200ms | <= 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | <= 0.1 | <= 0.25 | > 0.25 |
| **FCP** (First Contentful Paint) | <= 1.8s | <= 3.0s | > 3.0s |
| **TTFB** (Time to First Byte) | <= 800ms | <= 1800ms | > 1800ms |

### PerformanceObserver API

```typescript
// LCP Observer
function observeLCP(callback: (value: number) => void) {
  const observer = new PerformanceObserver((list) => {
    const entries = list.getEntries();
    callback(entries[entries.length - 1].startTime);
  });
  observer.observe({ type: 'largest-contentful-paint', buffered: true });
}

// INP Observer (replaces FID)
function observeINP(callback: (value: number) => void) {
  let maxDuration = 0;
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      const inp = (entry as PerformanceEventTiming).duration;
      if (inp > maxDuration) { maxDuration = inp; callback(inp); }
    }
  });
  observer.observe({ type: 'event', buffered: true });
}

// CLS Observer
function observeCLS(callback: (value: number) => void) {
  let clsValue = 0, sessionValue = 0;
  let sessionEntries: PerformanceEntry[] = [];
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries() as any[]) {
      if (!entry.hadRecentInput) {
        const first = sessionEntries[0], last = sessionEntries[sessionEntries.length - 1];
        if (sessionValue && entry.startTime - last?.startTime < 1000
            && entry.startTime - first?.startTime < 5000) {
          sessionValue += entry.value;
          sessionEntries.push(entry);
        } else {
          sessionValue = entry.value;
          sessionEntries = [entry];
        }
        if (sessionValue > clsValue) { clsValue = sessionValue; callback(clsValue); }
      }
    }
  });
  observer.observe({ type: 'layout-shift', buffered: true });
}
```

### Using the web-vitals Library

```typescript
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric: { name: string; value: number; rating: string; id: string }) {
  fetch('/api/vitals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: metric.name, value: metric.value, rating: metric.rating,
      url: window.location.href, timestamp: Date.now(),
    }),
    keepalive: true,
  });
}

export function initVitalsReporting() {
  onLCP(sendToAnalytics);
  onINP(sendToAnalytics);
  onCLS(sendToAnalytics);
  onFCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
}
```

### Real User Monitoring (RUM) Setup

```typescript
class RealUserMonitoring {
  constructor(private config: { endpoint: string; sampleRate: number; appVersion: string }) {}

  init() {
    if (Math.random() > this.config.sampleRate) return;
    this.observeNavigation();
    this.observeResources();
    this.observeLongTasks();
  }

  private observeNavigation() {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const nav = entry as PerformanceNavigationTiming;
        this.report('navigation', {
          ttfb: nav.responseStart - nav.requestStart,
          domComplete: nav.domComplete - nav.domInteractive,
          totalTime: nav.loadEventEnd - nav.startTime,
        });
      }
    }).observe({ type: 'navigation', buffered: true });
  }

  private observeResources() {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const res = entry as PerformanceResourceTiming;
        if (res.duration > 1000) {
          this.report('slow-resource', {
            name: res.name, duration: res.duration, size: res.transferSize,
          });
        }
      }
    }).observe({ type: 'resource', buffered: true });
  }

  private observeLongTasks() {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        this.report('long-task', { duration: entry.duration, startTime: entry.startTime });
      }
    }).observe({ type: 'longtask', buffered: true });
  }

  private report(type: string, data: Record<string, unknown>) {
    fetch(this.config.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        type, data, appVersion: this.config.appVersion,
        url: window.location.href, timestamp: Date.now(),
      }),
      keepalive: true,
    }).catch(() => { /* RUM should never break the app */ });
  }
}

// Usage: sample 10% of users
const rum = new RealUserMonitoring({ endpoint: '/api/rum', sampleRate: 0.1, appVersion: '1.2.3' });
rum.init();
```

---

## 5. Database Performance Testing

### Slow Query Detection

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { Pool } from 'pg';

describe('Database Query Performance', () => {
  let pool: Pool;

  beforeAll(async () => { pool = new Pool({ connectionString: process.env.DATABASE_URL }); });
  afterAll(async () => { await pool.end(); });

  it('should fetch user by ID within 50ms', async () => {
    const start = performance.now();
    await pool.query('SELECT * FROM users WHERE id = $1', [1]);
    expect(performance.now() - start).toBeLessThan(50);
  });

  it('should detect missing indexes via EXPLAIN ANALYZE', async () => {
    const result = await pool.query(
      "EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_email = 'test@example.com'"
    );
    const plan = result.rows.map((r) => r['QUERY PLAN']).join('\n');
    // Should use index scan, not sequential scan on large tables
    expect(plan).not.toMatch(/Seq Scan.*orders/);
  });
});
```

### Connection Pool Testing

```typescript
describe('Connection Pool Behavior', () => {
  it('should handle concurrent connections within pool limits', async () => {
    const pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 10, idleTimeoutMillis: 5000, connectionTimeoutMillis: 3000,
    });

    const concurrentQueries = 20;
    const start = performance.now();
    const results = await Promise.allSettled(
      Array.from({ length: concurrentQueries }, () => pool.query('SELECT pg_sleep(0.1)'))
    );
    const duration = performance.now() - start;

    expect(results.filter((r) => r.status === 'fulfilled').length).toBe(concurrentQueries);
    // 10 pool connections, 20 queries at 100ms: ~200ms (2 batches), not 2000ms
    expect(duration).toBeLessThan(1000);
    await pool.end();
  });

  it('should timeout when pool is exhausted', async () => {
    const pool = new Pool({
      connectionString: process.env.DATABASE_URL, max: 2, connectionTimeoutMillis: 500,
    });
    const held = await Promise.all([pool.connect(), pool.connect()]);
    await expect(pool.connect()).rejects.toThrow(/timeout/);
    for (const client of held) client.release();
    await pool.end();
  });
});
```

### N+1 Query Detection

```typescript
class QueryCounter {
  queries: string[] = [];
  private originalQuery: Function;

  constructor(private pool: any) { this.originalQuery = pool.query.bind(pool); }

  start() {
    this.queries = [];
    this.pool.query = (...args: any[]) => { this.queries.push(args[0]); return this.originalQuery(...args); };
  }

  stop() { this.pool.query = this.originalQuery; }
  get count() { return this.queries.length; }
}

describe('N+1 Query Detection', () => {
  it('should fetch orders with items in constant queries (not N+1)', async () => {
    const counter = new QueryCounter(pool);
    counter.start();
    const orders = await orderService.getOrdersWithItems({ limit: 50 });
    counter.stop();

    // Expect at most 2-3 queries (orders + items batch), not 51 (1 + N)
    expect(counter.count).toBeLessThanOrEqual(3);
    expect(orders.length).toBeGreaterThan(0);
  });
});
```

---

## 6. Memory and Resource Testing

### Memory Leak Detection in Node.js

```typescript
describe('Memory Leak Detection', () => {
  it('should not leak memory during repeated operations', async () => {
    if (global.gc) global.gc();  // Run with --expose-gc
    const baselineMemory = process.memoryUsage().heapUsed;
    const iterations = 1000;

    for (let i = 0; i < iterations; i++) {
      await processRequest({ id: i, data: 'test' });
    }

    if (global.gc) global.gc();
    const growthPerIteration = (process.memoryUsage().heapUsed - baselineMemory) / iterations;
    expect(growthPerIteration).toBeLessThan(1024); // < 1KB per iteration
  });

  it('should properly clean up event listeners', () => {
    const emitter = new EventEmitter();
    const initialListeners = emitter.listenerCount('data');

    for (let i = 0; i < 100; i++) {
      const service = new DataService(emitter);
      service.start();
      service.stop(); // Must remove listeners
    }
    expect(emitter.listenerCount('data')).toBe(initialListeners);
  });
});
```

### Browser Memory Profiling (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('should not leak memory on repeated modal open/close', async ({ page }) => {
  await page.goto('/dashboard');
  const getMemory = () => page.evaluate(() => (performance as any).memory?.usedJSHeapSize || 0);
  const initialMemory = await getMemory();

  for (let i = 0; i < 20; i++) {
    await page.click('[data-testid="open-modal"]');
    await page.waitForSelector('[data-testid="modal"]');
    await page.click('[data-testid="close-modal"]');
    await page.waitForSelector('[data-testid="modal"]', { state: 'hidden' });
  }

  await page.evaluate(() => { if ((window as any).gc) (window as any).gc(); });
  expect(await getMemory() - initialMemory).toBeLessThan(5 * 1024 * 1024); // < 5MB growth
});
```

### CPU Profiling

```typescript
import { Session } from 'inspector';
import { writeFileSync } from 'fs';

async function profileOperation(operation: () => Promise<void>) {
  const session = new Session();
  session.connect();
  session.post('Profiler.enable');
  session.post('Profiler.start');

  await operation();

  return new Promise<void>((resolve) => {
    session.post('Profiler.stop', (err, { profile }) => {
      if (!err) writeFileSync('cpu-profile.cpuprofile', JSON.stringify(profile));
      session.disconnect();
      resolve();
    });
  });
}
```

### Network Throttling Test Strategies

```typescript
import { test, expect } from '@playwright/test';

const networkConditions = {
  'slow-3g': { downloadThroughput: 50_000, uploadThroughput: 25_000, latency: 400 },
  'fast-3g': { downloadThroughput: 187_500, uploadThroughput: 75_000, latency: 150 },
  'regular-4g': { downloadThroughput: 500_000, uploadThroughput: 250_000, latency: 50 },
};

const budgets: Record<string, number> = { 'slow-3g': 3000, 'fast-3g': 1500, 'regular-4g': 800 };

for (const [name, conditions] of Object.entries(networkConditions)) {
  test(`page loads within budget on ${name}`, async ({ page }) => {
    const cdp = await page.context().newCDPSession(page);
    await cdp.send('Network.emulateNetworkConditions', { offline: false, ...conditions });

    const start = Date.now();
    await page.goto('/', { waitUntil: 'domcontentloaded' });
    expect(Date.now() - start).toBeLessThan(budgets[name]);
  });
}
```

### Bundle Size Budget Tests

```typescript
import { describe, it, expect } from 'vitest';
import { statSync, readdirSync } from 'fs';
import { join } from 'path';

describe('Bundle Size Budget', () => {
  const distDir = join(process.cwd(), 'dist');

  function totalSize(dir: string, ext: string): number {
    const files = readdirSync(dir, { recursive: true }) as string[];
    return files
      .filter((f) => f.endsWith(ext))
      .reduce((sum, f) => sum + statSync(join(dir, f)).size, 0);
  }

  it('total JS bundle should be under 300KB', () => {
    expect(totalSize(distDir, '.js')).toBeLessThan(300 * 1024);
  });

  it('total CSS should be under 100KB', () => {
    expect(totalSize(distDir, '.css')).toBeLessThan(100 * 1024);
  });
});
```

---

## 7. CI/CD Performance Regression Detection

### Performance Gate in GitHub Actions

```yaml
# .github/workflows/perf-check.yml
name: Performance Check
on: [pull_request]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci && npm run build
      - name: Start server
        run: npm start &
        env:
          NODE_ENV: production
      - run: npx wait-on http://localhost:3000 --timeout 30000
      - name: Run k6 load test
        uses: grafana/k6-action@v0.3.1
        with:
          filename: load-tests/api-load.js
          flags: --out json=k6-results.json
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: k6-results.json
```

### Performance Comparison Script

```typescript
interface PerfMetrics { p50: number; p95: number; p99: number; errorRate: number; throughput: number; }

function compareMetrics(base: PerfMetrics, current: PerfMetrics) {
  const regressions: string[] = [];
  const threshold = 0.10; // 10% regression threshold

  if (current.p95 > base.p95 * (1 + threshold))
    regressions.push(`p95 regressed: ${base.p95.toFixed(0)}ms -> ${current.p95.toFixed(0)}ms`);
  if (current.errorRate > base.errorRate * (1 + threshold) && current.errorRate > 0.01)
    regressions.push(`Error rate regressed: ${(base.errorRate*100).toFixed(2)}% -> ${(current.errorRate*100).toFixed(2)}%`);
  if (current.throughput < base.throughput * (1 - threshold))
    regressions.push(`Throughput regressed: ${base.throughput.toFixed(0)} -> ${current.throughput.toFixed(0)} rps`);

  return { passed: regressions.length === 0, regressions };
}
```

---

## 8. Quick Reference

### CLI Commands

```bash
# k6
k6 run script.js                    # Run load test
k6 run --vus 50 --duration 2m       # Override options
k6 run -e API_KEY=xxx script.js     # Pass env vars
k6 run --out json=out.json          # JSON output
k6 inspect script.js                # Validate script

# Lighthouse CI
lhci autorun                        # Full CI pipeline
lhci collect --url=http://...       # Collect only
lhci assert                         # Assert against config
lhci upload                         # Upload results
```

### Performance Testing Decision Matrix

| Scenario | Tool | Configuration |
|----------|------|---------------|
| API load testing | k6 | ramping-vus, thresholds |
| Stress/breaking point | k6 | ramping-vus with high targets |
| Soak testing | k6 | constant-vus, long duration |
| Spike testing | k6 | ramping-vus, sudden jumps |
| Web performance audit | Lighthouse CI | assert with budgets |
| Bundle size regression | Vitest | statSync + budget checks |
| Core Web Vitals (lab) | Lighthouse CI | performance category |
| Core Web Vitals (field) | web-vitals lib | RUM endpoint |
| Database queries | Vitest + pg | EXPLAIN ANALYZE |
| Memory leaks | Node inspector | heap snapshots |
| Network conditions | Playwright CDP | emulateNetworkConditions |

### Threshold Guidelines

| Metric | Target | Maximum |
|--------|--------|---------|
| API p95 latency | < 200ms | < 500ms |
| API p99 latency | < 500ms | < 1500ms |
| Error rate | < 0.1% | < 1% |
| LCP | < 2.5s | < 4.0s |
| INP | < 200ms | < 500ms |
| CLS | < 0.1 | < 0.25 |
| JS bundle (total) | < 200KB | < 300KB |
| CSS (total) | < 50KB | < 100KB |
| DB query | < 50ms | < 200ms |

## Best Practices

1. **Test in production-like environments** -- staging with similar data volumes and infra
2. **Establish baselines** before optimizing -- measure first, then improve
3. **Set realistic thresholds** -- based on SLAs and user expectations, not arbitrary numbers
4. **Automate in CI/CD** -- performance regressions should block merges
5. **Monitor real users (RUM)** -- lab data is a proxy; field data is truth
6. **Test at scale** -- seed databases with production-like data volumes
7. **Profile before optimizing** -- find the bottleneck, do not guess
8. **Budget for third parties** -- third-party scripts are the top performance killer
9. **Test degraded conditions** -- slow networks, cold caches, high concurrency
10. **Track trends over time** -- individual runs have variance; trends reveal regressions

## Related Skills

- `qa-engineer` - Overall test strategy and quality gates
- `e2e-testing` - Browser automation and E2E tests
- `unit-testing` - Unit tests and TDD workflow
