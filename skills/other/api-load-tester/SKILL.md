---
name: api-load-tester
description: >-
  Generates and executes load test scripts for APIs using k6, wrk, or
  autocannon. Creates realistic test scenarios from OpenAPI specs, route
  files, or endpoint descriptions. Use when someone needs to load test,
  stress test, benchmark, or find the breaking point of their API.
  Trigger words: load test, stress test, benchmark, RPS, concurrent users,
  breaking point, performance test, k6, wrk.
license: Apache-2.0
compatibility: "Requires k6, wrk, or autocannon installed; Node.js for autocannon"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: devops
  tags: ["load-testing", "performance", "api", "k6", "benchmarking"]
---

# API Load Tester

## Overview

This skill generates realistic load test scripts from API definitions and executes them with proper ramp-up patterns, authentication flows, and assertions. It produces clear reports identifying breaking points, bottlenecks, and latency percentiles at each traffic level.

## Instructions

### Step 1: Choose Tool and Gather API Info

Prefer k6 for complex scenarios (multi-step flows, thresholds, custom metrics). Use wrk for quick single-endpoint benchmarks. Use autocannon if only Node.js is available.

Gather endpoint information from:
- OpenAPI/Swagger spec files
- Route definitions (Express, FastAPI, etc.)
- User-described endpoints

### Step 2: Generate Realistic Payloads

Read request/response types from the codebase (TypeScript interfaces, Python dataclasses, Go structs) and generate payloads with:
- Realistic field values (not "test123" or "foo")
- Proper data distributions (varied product IDs, realistic quantities)
- Edge cases mixed in (long strings, special characters at ~5% rate)

### Step 3: Design Test Scenarios

Create scenarios appropriate for the goal:

**Ramp-up test** (finding breaking point):
```
stages: [
  { duration: '2m', target: 50 },    // warm-up
  { duration: '5m', target: 200 },   // ramp
  { duration: '3m', target: 500 },   // push
  { duration: '2m', target: 500 },   // sustain
  { duration: '2m', target: 0 },     // cool-down
]
```

**Soak test** (finding memory leaks, connection exhaustion):
```
stages: [
  { duration: '5m', target: 100 },   // ramp
  { duration: '60m', target: 100 },  // sustain
  { duration: '5m', target: 0 },     // cool-down
]
```

**Spike test** (sudden traffic burst):
```
stages: [
  { duration: '2m', target: 50 },    // normal
  { duration: '30s', target: 500 },  // spike
  { duration: '5m', target: 500 },   // sustain spike
  { duration: '30s', target: 50 },   // drop back
]
```

### Step 4: Include Proper Assertions

Always add thresholds:
```javascript
thresholds: {
  http_req_duration: ['p(95)<800', 'p(99)<2000'],
  http_req_failed: ['rate<0.05'],
  // Custom per-endpoint if needed
}
```

### Step 5: Execute and Report

Run the test and parse output into a structured report showing:
- Latency percentiles (p50, p95, p99) per stage
- Error rate per stage
- Requests per second achieved
- Breaking point (where thresholds first violated)
- Bottleneck hypothesis based on error patterns

## Examples

### Example 1: Quick Endpoint Benchmark

**User prompt:**
```
Benchmark our /api/search endpoint handling 100 concurrent connections
```

**Agent output:**
```bash
# Quick benchmark with k6
k6 run --vus 100 --duration 60s - <<'EOF'
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const res = http.get('https://api.example.com/api/search?q=laptop&page=1');
  check(res, { 'status 200': (r) => r.status === 200 });
}
EOF
```

```
Results — /api/search @ 100 VUs for 60s
  Requests:    8,423 total (140.4 RPS)
  Latency:     p50=89ms  p95=340ms  p99=890ms
  Errors:      12 (0.14%)
  Data:        24.3 MB received

Verdict: Endpoint handles 140 RPS at 100 VUs. p99 approaching 1s suggests
database query optimization needed for sustained higher load.
```

### Example 2: Multi-Step Flow

**User prompt:**
```
Create a load test for our signup → login → create-project flow
```

**Agent generates a k6 script with:**
- Step 1: POST /api/auth/signup with randomized email/name
- Step 2: POST /api/auth/login to get JWT
- Step 3: POST /api/projects with auth header and realistic project data
- Custom metrics tracking each step's latency separately
- Sleep between steps to simulate real user behavior

## Guidelines

- **Never load test production without explicit confirmation** — always clarify the target environment
- **Start low, ramp gradually** — sudden jumps make it hard to identify the exact breaking point
- **Realistic think time** — add `sleep(1-3)` between requests to simulate real users; without it, you're testing throughput, not user concurrency
- **Authentication matters** — many bottlenecks only appear with real auth flows (token validation, session lookups)
- **Watch for connection reuse** — k6 reuses connections by default, which is realistic for browsers but not for serverless/mobile clients
- **Rate limit awareness** — if the API has rate limiting, note it in the report; it's not a performance bottleneck, it's intentional
- **Report infrastructure context** — always note the server specs, pod count, and database size alongside results
