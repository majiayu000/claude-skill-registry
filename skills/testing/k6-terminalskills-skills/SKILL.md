---
name: k6
description: When the user wants to perform load testing, stress testing, or performance testing of APIs and websites using k6. Also use when the user mentions "k6," "load test," "performance test," "stress test," "spike test," "soak test," "thresholds," "virtual users," or "VUs." For browser-based testing, see selenium.
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags:
    - load-testing
    - performance
    - stress-testing
    - benchmarking
---

# k6

## Overview

You are an expert in k6, the open-source load testing tool built for developer happiness. You help users write k6 test scripts in JavaScript, configure virtual users and durations, set thresholds for pass/fail criteria, and analyze results. You understand k6's execution model, lifecycle hooks, and how to integrate k6 into CI/CD pipelines.

## Instructions

### Initial Assessment

Before writing a load test, understand:

1. **Target** — What endpoint(s) or service are you testing?
2. **Goal** — What kind of test? (load, stress, spike, soak, smoke)
3. **Expectations** — What response time and error rate are acceptable?
4. **Scale** — How many concurrent users should the test simulate?

### Writing k6 Scripts

Always structure scripts with clear stages and thresholds:

```javascript
// load-test.js — k6 load test with ramping VUs and thresholds.
// Tests the /api/users endpoint under increasing load.
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '3m', target: 50 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
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

### Test Types

Guide users to the right test type:

- **Smoke test** — Minimal load (1-2 VUs) to verify the script works
- **Load test** — Expected normal and peak load
- **Stress test** — Beyond normal capacity to find breaking points
- **Spike test** — Sudden surge of traffic
- **Soak test** — Extended duration to find memory leaks and degradation

### Thresholds

Always recommend thresholds so tests have clear pass/fail criteria:

```javascript
// thresholds.js — Common threshold patterns for k6.
// Combine multiple metrics for comprehensive pass/fail.
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    http_reqs: ['rate>100'],
    checks: ['rate>0.99'],
    'http_req_duration{name:login}': ['p(95)<800'],
  },
};
```

### Custom Metrics

```javascript
// custom-metrics.js — Track business-specific metrics in k6.
// Useful for measuring things beyond HTTP response times.
import { Trend, Counter, Rate } from 'k6/metrics';

const loginDuration = new Trend('login_duration');
const successfulLogins = new Counter('successful_logins');
const loginSuccessRate = new Rate('login_success_rate');

export default function () {
  const start = Date.now();
  const res = http.post('https://api.example.com/login', JSON.stringify({
    username: 'testuser',
    password: 'testpass',
  }), { headers: { 'Content-Type': 'application/json' } });

  loginDuration.add(Date.now() - start);
  const success = res.status === 200;
  successfulLogins.add(success ? 1 : 0);
  loginSuccessRate.add(success);
}
```

### CI Integration

```yaml
# .github/workflows/load-test.yml — Run k6 load tests in GitHub Actions.
# Fails the pipeline if thresholds are breached.
name: Load Test
on:
  push:
    branches: [main]
jobs:
  k6:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/load-test.js
```

### Running k6

```bash
# run-k6.sh — Common k6 commands for different scenarios.
# Install and run with various output options.

# Install
brew install k6

# Basic run
k6 run load-test.js

# With environment variables
k6 run -e BASE_URL=https://staging.example.com load-test.js

# Override VUs and duration
k6 run --vus 100 --duration 5m load-test.js

# Output to JSON for analysis
k6 run --out json=results.json load-test.js
```

### Scenarios (Advanced)

```javascript
// scenarios.js — Multiple scenarios running different patterns simultaneously.
// Simulates realistic mixed traffic patterns.
export const options = {
  scenarios: {
    browse: {
      executor: 'constant-vus',
      vus: 20,
      duration: '5m',
      exec: 'browsePage',
    },
    checkout: {
      executor: 'ramping-arrival-rate',
      startRate: 1,
      timeUnit: '1s',
      preAllocatedVUs: 50,
      stages: [
        { duration: '2m', target: 10 },
        { duration: '2m', target: 0 },
      ],
      exec: 'checkout',
    },
  },
};

export function browsePage() {
  http.get('https://api.example.com/products');
  sleep(2);
}

export function checkout() {
  http.post('https://api.example.com/checkout', JSON.stringify({ item: 'widget' }));
}
```
