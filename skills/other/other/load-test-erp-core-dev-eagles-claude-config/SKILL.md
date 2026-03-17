---
name: load-test
description: Generate and run load tests with K6
argument-hint: "<target-url> [--vus=50] [--duration=30s]"
tags: [testing, load, k6, performance]
user-invocable: true
---

# Load Testing with K6

Generate and run load tests to validate performance under stress.

## What To Do

1. **Install**: `choco install k6` or `brew install k6`

2. **Generate test script** (tests/load/api-load.js):
   ```javascript
   import http from 'k6/http';
   import { check, sleep } from 'k6';
   export const options = {
     stages: [
       { duration: '30s', target: 20 },
       { duration: '1m', target: 50 },
       { duration: '30s', target: 0 },
     ],
     thresholds: {
       http_req_duration: ['p(95)<200'],
       http_req_failed: ['rate<0.01'],
     },
   };
   export default function () {
     const res = http.get('http://localhost:5000/api/candidates');
     check(res, { 'status 200': (r) => r.status === 200 });
     sleep(1);
   }
   ```

3. **Run**: `k6 run tests/load/api-load.js`

## Arguments
- `<target-url>`: Base URL to test
- `--vus=<n>`: Virtual users (default: 50)
- `--duration=<time>`: Test duration (default: 30s)