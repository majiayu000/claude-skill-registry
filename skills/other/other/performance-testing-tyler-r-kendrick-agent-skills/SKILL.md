---
name: performance-testing
description: |
    Use for load, stress, and scalability testing of applications and APIs. Covers k6 (Grafana), JMeter, Gatling, Artillery, and Lighthouse for web performance audits. Includes test type definitions, key metrics, thresholds, CI integration patterns, and performance budgets.
    USE FOR: k6, JMeter, Gatling, Artillery, Lighthouse, load testing, stress testing, performance benchmarks, Core Web Vitals, throughput testing, spike testing, soak testing, capacity planning, performance budgets
    DO NOT USE FOR: functional API testing (use api-testing), browser E2E tests (use e2e-testing), visual regression (use visual-testing)
license: MIT
metadata:
  displayName: "Performance Testing"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "k6 Documentation (Grafana)"
    url: "https://grafana.com/docs/k6/latest/"
  - title: "Apache JMeter"
    url: "https://jmeter.apache.org"
  - title: "Gatling Documentation"
    url: "https://docs.gatling.io"
  - title: "Lighthouse Documentation (Chrome Developers)"
    url: "https://developer.chrome.com/docs/lighthouse/"
---

# Performance Testing

## Overview
Performance testing validates that your application meets speed, stability, and scalability requirements under expected and extreme conditions. It answers questions like "How many concurrent users can we handle?", "What's the 99th percentile response time?", and "Where does the system break?".

## Performance Test Types

| Type | Goal | Pattern | When to Use |
|------|------|---------|-------------|
| **Load** | Validate expected traffic | Ramp to target VUs, sustain, ramp down | Before release, capacity planning |
| **Stress** | Find the breaking point | Ramp beyond expected capacity | Pre-launch, architecture validation |
| **Spike** | Handle sudden traffic bursts | Jump to high VUs instantly | Flash sales, event-driven traffic |
| **Soak** | Detect memory leaks / degradation | Moderate load over hours | After major changes, long-running services |
| **Breakpoint** | Determine absolute maximum | Continuously increase until failure | Capacity planning, SLA definition |

## Key Metrics

| Metric | Description | Typical Thresholds |
|--------|-------------|-------------------|
| **Response Time (p50)** | Median latency | < 200ms for APIs, < 1s for pages |
| **Response Time (p95)** | 95th percentile latency | < 500ms for APIs, < 3s for pages |
| **Response Time (p99)** | 99th percentile latency | < 1s for APIs, < 5s for pages |
| **Throughput (RPS)** | Requests per second | Application-specific |
| **Error Rate** | % of failed requests | < 1% under normal load |
| **VU Concurrency** | Active virtual users | Application-specific |
| **TTFB** | Time to first byte | < 200ms |
| **Core Web Vitals (LCP)** | Largest Contentful Paint | < 2.5s |
| **Core Web Vitals (INP)** | Interaction to Next Paint | < 200ms |
| **Core Web Vitals (CLS)** | Cumulative Layout Shift | < 0.1 |

---

## Cross-Platform Tools

| Tool | Language | Strengths |
|------|----------|-----------|
| **k6 (Grafana)** | JavaScript | Developer-friendly, CLI-native, thresholds, scenarios, k6 cloud, k6 browser |
| **JMeter** | Java (GUI + CLI) | Mature, GUI test plan builder, extensive protocol support, plugins |
| **Gatling** | Scala / Java | High performance, code-based DSL, detailed HTML reports |
| **Artillery** | YAML + JS | Simple YAML config, plugin ecosystem, serverless mode |
| **Lighthouse** | CLI / Chrome | Web performance audits, Core Web Vitals, accessibility, SEO |

---

## k6 (Grafana)

### Load Test with Stages, Thresholds, and Checks

```javascript
// tests/performance/load-test.k6.js
import http from "k6/http";
import { check, sleep, group } from "k6";

export const options = {
    stages: [
        { duration: "2m", target: 50 },   // Ramp up to 50 VUs
        { duration: "5m", target: 50 },   // Sustain 50 VUs
        { duration: "2m", target: 100 },  // Ramp up to 100 VUs
        { duration: "5m", target: 100 },  // Sustain 100 VUs
        { duration: "2m", target: 0 },    // Ramp down
    ],
    thresholds: {
        http_req_duration: [
            "p(50)<200",     // 50th percentile under 200ms
            "p(95)<500",     // 95th percentile under 500ms
            "p(99)<1000",    // 99th percentile under 1s
        ],
        http_req_failed: ["rate<0.01"],   // Less than 1% errors
        checks: ["rate>0.99"],            // 99%+ checks pass
    },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:3000";

export default function () {
    group("Homepage flow", () => {
        const homeRes = http.get(`${BASE_URL}/`);
        check(homeRes, {
            "homepage returns 200": (r) => r.status === 200,
            "homepage loads under 500ms": (r) => r.timings.duration < 500,
        });

        const apiRes = http.get(`${BASE_URL}/api/products?limit=20`);
        check(apiRes, {
            "products API returns 200": (r) => r.status === 200,
            "products returns array": (r) => Array.isArray(r.json()),
        });
    });

    sleep(1); // Think time between iterations
}
```

### k6 Scenarios (Advanced)

```javascript
// tests/performance/scenarios.k6.js
import http from "k6/http";
import { check } from "k6";

export const options = {
    scenarios: {
        // Constant arrival rate — fixed RPS regardless of response time
        constant_load: {
            executor: "constant-arrival-rate",
            rate: 100,             // 100 RPS
            timeUnit: "1s",
            duration: "5m",
            preAllocatedVUs: 50,
            maxVUs: 200,
        },
        // Ramping VUs — gradual increase
        ramping_users: {
            executor: "ramping-vus",
            startVUs: 0,
            stages: [
                { duration: "2m", target: 50 },
                { duration: "3m", target: 50 },
                { duration: "1m", target: 0 },
            ],
        },
        // Spike test — sudden burst
        spike: {
            executor: "ramping-arrival-rate",
            startRate: 10,
            timeUnit: "1s",
            stages: [
                { duration: "10s", target: 10 },
                { duration: "1m", target: 500 },  // Spike
                { duration: "10s", target: 10 },   // Recover
            ],
            preAllocatedVUs: 200,
            maxVUs: 500,
        },
    },
    thresholds: {
        http_req_duration: ["p(95)<500"],
        http_req_failed: ["rate<0.01"],
    },
};

export default function () {
    const res = http.get(`${__ENV.BASE_URL}/api/health`);
    check(res, { "status 200": (r) => r.status === 200 });
}
```

### Running k6

```bash
# Basic run
k6 run tests/performance/load-test.k6.js

# With environment variables
k6 run tests/performance/load-test.k6.js --env BASE_URL=https://staging.example.com

# Output to multiple destinations
k6 run tests/performance/load-test.k6.js \
    --out json=results.json \
    --out influxdb=http://localhost:8086/k6

# k6 cloud (Grafana Cloud k6)
k6 cloud tests/performance/load-test.k6.js
```

---

## Artillery

### YAML Configuration Example

```yaml
# tests/performance/artillery-config.yml
config:
  target: "https://staging-api.example.com"
  phases:
    - name: "Warm up"
      duration: 60       # seconds
      arrivalRate: 5      # new virtual users per second
    - name: "Ramp up"
      duration: 120
      arrivalRate: 5
      rampTo: 50
    - name: "Sustained load"
      duration: 300
      arrivalRate: 50
  defaults:
    headers:
      Authorization: "Bearer {{ $processEnvironment.AUTH_TOKEN }}"
      Content-Type: "application/json"
  ensure:
    thresholds:
      - http.response_time.p95: 500
      - http.response_time.p99: 1000
      - http.codes.200: 95        # 95% of responses must be 200
  plugins:
    expect: {}

scenarios:
  - name: "Browse and purchase flow"
    flow:
      - get:
          url: "/api/products"
          expect:
            - statusCode: 200
            - hasProperty: "body.length"
          capture:
            - json: "$[0].id"
              as: "productId"
      - think: 2
      - get:
          url: "/api/products/{{ productId }}"
          expect:
            - statusCode: 200
      - think: 1
      - post:
          url: "/api/cart"
          json:
            productId: "{{ productId }}"
            quantity: 1
          expect:
            - statusCode: 201
```

### Running Artillery

```bash
# Install Artillery
npm install -g artillery

# Run test
artillery run tests/performance/artillery-config.yml

# Run with environment overrides
artillery run tests/performance/artillery-config.yml --target https://staging.example.com

# Generate HTML report
artillery run tests/performance/artillery-config.yml --output results.json
artillery report results.json --output report.html

# Quick one-liner smoke test
artillery quick --count 10 --num 5 https://staging-api.example.com/api/health
```

---

## JMeter

### Overview
Apache JMeter is a mature load testing tool with a GUI for building test plans and a CLI mode for CI execution.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Test Plan** | Root container for all test elements |
| **Thread Group** | Defines VUs (threads), ramp-up time, loop count |
| **Samplers** | HTTP Request, JDBC Request, FTP, etc. |
| **Assertions** | Response assertions (status, body, duration) |
| **Listeners** | Results viewers (Summary Report, Graph, JTL files) |
| **Config Elements** | CSV Data Set, HTTP Header Manager, User Variables |
| **Timers** | Think time between requests |

### CLI Mode for CI

```bash
# Run test plan in non-GUI mode
jmeter -n -t test-plan.jmx -l results.jtl -e -o report/

# With properties
jmeter -n -t test-plan.jmx \
    -Jthreads=100 \
    -Jrampup=60 \
    -Jduration=300 \
    -Jhost=staging-api.example.com \
    -l results.jtl

# Generate HTML report from results
jmeter -g results.jtl -o report/
```

### GitHub Actions Integration

```yaml
# .github/workflows/jmeter.yml
jobs:
  performance-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run JMeter Tests
        uses: rbhadti94/apache-jmeter-action@v0.5.0
        with:
          testFilePath: tests/performance/test-plan.jmx
          outputReportsFolder: reports/
          args: >
            -Jthreads=50 -Jrampup=30 -Jduration=120
            -Jhost=${{ secrets.STAGING_HOST }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: jmeter-report
          path: reports/
```

---

## Gatling

### Overview
Gatling uses a code-based DSL (Scala or Java) for defining simulations, producing detailed HTML reports automatically.

### Scala DSL Example

```scala
// src/test/scala/simulations/BasicSimulation.scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._
import scala.concurrent.duration._

class BasicSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("https://staging-api.example.com")
    .acceptHeader("application/json")
    .authorizationHeader("Bearer ${authToken}")

  val feeder = csv("test-data/users.csv").random

  val browseScenario = scenario("Browse Products")
    .feed(feeder)
    .exec(
      http("List Products")
        .get("/api/products")
        .check(status.is(200))
        .check(jsonPath("$[0].id").saveAs("productId"))
    )
    .pause(1, 3)
    .exec(
      http("Get Product Detail")
        .get("/api/products/${productId}")
        .check(status.is(200))
    )

  setUp(
    browseScenario.inject(
      rampUsers(50).during(2.minutes),
      constantUsersPerSec(10).during(5.minutes),
      rampUsers(0).during(1.minute)
    )
  ).protocols(httpProtocol)
    .assertions(
      global.responseTime.percentile(95).lt(500),
      global.successfulRequests.percent.gt(99.0)
    )
}
```

### Running Gatling

```bash
# Run with Maven
mvn gatling:test

# Run with Gradle
gradle gatlingRun

# Run specific simulation
mvn gatling:test -Dgatling.simulationClass=simulations.BasicSimulation
```

---

## Lighthouse

### Overview
Lighthouse audits web performance, accessibility, best practices, and SEO. It measures Core Web Vitals and provides actionable improvement suggestions.

### CLI Usage

```bash
# Install Lighthouse CLI
npm install -g lighthouse

# Run performance audit
lighthouse https://example.com \
    --output json,html \
    --output-path ./results/lighthouse \
    --chrome-flags="--headless --no-sandbox"

# Performance-only audit
lighthouse https://example.com \
    --only-categories=performance \
    --output json \
    --output-path ./results/perf.json

# Run with budget
lighthouse https://example.com \
    --budget-path=budgets.json \
    --output html
```

### Performance Budget File

```json
// budgets.json
[
    {
        "path": "/*",
        "timings": [
            { "metric": "interactive", "budget": 3000 },
            { "metric": "first-contentful-paint", "budget": 1500 },
            { "metric": "largest-contentful-paint", "budget": 2500 }
        ],
        "resourceSizes": [
            { "resourceType": "script", "budget": 300 },
            { "resourceType": "total", "budget": 1000 }
        ]
    }
]
```

### CI Integration with Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install -g @lhci/cli
      - run: |
          lhci autorun \
            --collect.url=https://staging.example.com \
            --collect.numberOfRuns=3 \
            --assert.preset=lighthouse:recommended \
            --assert.assertions.largest-contentful-paint=warn:2500 \
            --assert.assertions.interactive=error:5000
```

---

## CI Integration Patterns

### When to Run Each Test Type

| Test Type | Trigger | Duration | Gate |
|-----------|---------|----------|------|
| **Smoke** (minimal load) | Every PR | 1-2 min | Fail PR if errors |
| **Load** (expected traffic) | Nightly or pre-release | 10-20 min | Alert on threshold breach |
| **Stress** (beyond capacity) | Pre-release | 20-30 min | Report, don't gate |
| **Soak** (extended duration) | Weekly or pre-release | 2-8 hours | Alert on degradation |
| **Lighthouse** | Every PR | 1-2 min | Warn on budget violation |

### k6 CI Pipeline Example

```yaml
# .github/workflows/performance.yml
name: Performance Tests
on:
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * *"   # Nightly at 2 AM

jobs:
  smoke-test:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/performance/smoke.k6.js
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}

  load-test:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/performance/load-test.k6.js
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: k6-results
          path: results/
```

---

## Best Practices

### Test Design
- Start with a smoke test (minimal load) to validate the test script works before scaling up.
- Use realistic think times (`sleep()` / `pause()`) to simulate actual user behavior.
- Use data-driven tests with CSV feeders or dynamic data generation to avoid caching skew.
- Test the same scenario at different load levels: smoke, load, stress, spike.

### Metrics and Thresholds
- Always define thresholds — tests without pass/fail criteria are just logs.
- Focus on percentiles (p95, p99), not averages — averages hide tail latency.
- Track error rate alongside response time — fast errors are still failures.
- Baseline before optimizing — run tests against a known-good build first.

### CI Integration
- Run smoke tests on every PR (fast, catches regressions early).
- Run full load tests nightly or pre-release (comprehensive, takes time).
- Store results as artifacts for trend analysis over time.
- Set thresholds as CI gates: fail the pipeline if p95 exceeds the budget.

### Infrastructure
- Run performance tests against a dedicated staging environment, not shared dev.
- Ensure the load generator has sufficient resources (CPU, network) to avoid bottlenecking the test tool itself.
- Use distributed load generation (k6 cloud, JMeter distributed mode) for large-scale tests.
- Monitor the system under test (CPU, memory, DB connections) alongside the k6/Artillery metrics.

### Reporting
- Generate HTML reports for human review (Gatling, JMeter, Artillery all support this).
- Export machine-readable results (JSON, JTL) for trend tracking and dashboards.
- Compare results against previous runs to catch performance regressions.
- Document performance baselines and SLAs in the repository alongside the test scripts.
