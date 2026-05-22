---
name: load-testing
description: Auto-activates when user mentions load test, performance test, stress test, k6, Artillery, benchmark, or scalability testing. Expert in designing and executing performance tests.
category: testing
---

# Load Testing & Performance Testing

Creates comprehensive load tests using k6, Artillery, and other tools to validate application performance under stress.

## When This Activates

- User says: "load test this", "performance test", "stress test", "benchmark"
- User mentions: "k6", "Artillery", "JMeter", "Gatling", "scalability"
- Performance validation needed
- Pre-production testing
- Capacity planning questions

## Load Testing Tools Comparison

### k6 (Recommended)
- **Best for:** Modern apps, APIs, microservices
- **Language:** JavaScript/TypeScript
- **Pros:** Cloud-native, great metrics, scriptable
- **Use when:** Testing REST APIs, GraphQL, WebSocket

### Artillery
- **Best for:** Quick tests, CI/CD integration
- **Language:** YAML + JavaScript
- **Pros:** Simple config, plugins, HTTP/WS/Socket.io
- **Use when:** Simple scenarios, rapid testing

### Apache JMeter
- **Best for:** Enterprise apps, complex scenarios
- **Language:** GUI-based + Java
- **Pros:** Mature, extensive protocols, GUI
- **Use when:** Legacy systems, complex workflows

## k6 Load Testing

### Basic Load Test

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const checkDuration = new Trend('check_duration');
const requests = new Counter('requests');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 10 },   // Ramp up to 10 users
    { duration: '5m', target: 10 },   // Stay at 10 users
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'], // 95% < 500ms, 99% < 1s
    http_req_failed: ['rate<0.01'],                  // Error rate < 1%
    errors: ['rate<0.1'],                            // Custom error rate < 10%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';
const API_TOKEN = __ENV.API_TOKEN || '';

export default function () {
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${API_TOKEN}`,
    },
    tags: { name: 'GetUsers' },
  };

  // GET request
  let response = http.get(`${BASE_URL}/api/users`, params);
  
  const checkResult = check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'has users': (r) => JSON.parse(r.body).data.length > 0,
  });

  errorRate.add(!checkResult);
  checkDuration.add(response.timings.duration);
  requests.add(1);

  // POST request
  const payload = JSON.stringify({
    name: 'Test User',
    email: `test-${Date.now()}@example.com`,
  });

  response = http.post(`${BASE_URL}/api/users`, payload, params);
  
  check(response, {
    'user created': (r) => r.status === 201,
  });

  sleep(1); // Think time between requests
}

export function handleSummary(data) {
  return {
    'summary.json': JSON.stringify(data),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}
```

### Advanced Scenarios

```javascript
// advanced-test.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import papaparse from 'https://jslib.k6.io/papaparse/5.1.1/index.js';

// Load test data
const users = new SharedArray('users', function () {
  return papaparse.parse(open('./users.csv'), { header: true }).data;
});

export const options = {
  scenarios: {
    // Scenario 1: Constant load
    constant_load: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
    },
    // Scenario 2: Ramping load
    ramping_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 100 },
        { duration: '10m', target: 100 },
        { duration: '5m', target: 0 },
      ],
      gracefulRampDown: '30s',
    },
    // Scenario 3: Stress test
    stress_test: {
      executor: 'ramping-arrival-rate',
      startRate: 50,
      timeUnit: '1s',
      preAllocatedVUs: 500,
      maxVUs: 1000,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 200 },
        { duration: '2m', target: 500 },
        { duration: '5m', target: 500 },
        { duration: '2m', target: 0 },
      ],
    },
  },
};

export default function () {
  const user = users[Math.floor(Math.random() * users.length)];

  group('User Flow', function () {
    // 1. Login
    group('Login', function () {
      const loginRes = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify({
        email: user.email,
        password: user.password,
      }), {
        headers: { 'Content-Type': 'application/json' },
      });

      check(loginRes, {
        'login successful': (r) => r.status === 200,
      });

      const token = loginRes.json('token');
      
      // 2. Get profile
      group('Get Profile', function () {
        const profileRes = http.get(`${BASE_URL}/api/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        check(profileRes, {
          'profile loaded': (r) => r.status === 200,
        });
      });

      // 3. Create post
      group('Create Post', function () {
        const postRes = http.post(`${BASE_URL}/api/posts`, JSON.stringify({
          title: 'Load Test Post',
          content: 'This is a test post from k6',
        }), {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
        });

        check(postRes, {
          'post created': (r) => r.status === 201,
        });
      });
    });
  });

  sleep(Math.random() * 3 + 2); // Random think time 2-5s
}
```

### GraphQL Load Test

```javascript
// graphql-test.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50,
  duration: '5m',
  thresholds: {
    http_req_duration: ['p(95)<1000'],
  },
};

const GRAPHQL_ENDPOINT = `${__ENV.BASE_URL}/graphql`;

export default function () {
  const query = `
    query GetPosts($first: Int!) {
      posts(first: $first) {
        edges {
          node {
            id
            title
            author {
              name
            }
          }
        }
      }
    }
  `;

  const variables = { first: 20 };

  const response = http.post(
    GRAPHQL_ENDPOINT,
    JSON.stringify({ query, variables }),
    {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${__ENV.API_TOKEN}`,
      },
    }
  );

  check(response, {
    'no errors': (r) => !r.json('errors'),
    'has data': (r) => r.json('data.posts.edges.length') > 0,
  });
}
```

## Artillery Load Testing

### Basic Configuration

```yaml
# artillery.yml
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60
      arrivalRate: 10     # 10 users per second
      name: "Warm up"
    - duration: 300
      arrivalRate: 50     # 50 users per second
      name: "Sustained load"
    - duration: 120
      arrivalRate: 100    # 100 users per second
      name: "Spike"
  
  processor: "./helpers.js"
  
  variables:
    apiToken: "{{ $processEnvironment.API_TOKEN }}"
  
  plugins:
    expect: {}
    metrics-by-endpoint: {}

scenarios:
  - name: "User Registration and Login"
    flow:
      - post:
          url: "/api/auth/register"
          json:
            email: "user-{{ $randomString() }}@example.com"
            name: "Test User"
            password: "password123"
          capture:
            - json: "$.token"
              as: "authToken"
          expect:
            - statusCode: 201
            - contentType: json
            - hasProperty: token

      - get:
          url: "/api/profile"
          headers:
            Authorization: "Bearer {{ authToken }}"
          expect:
            - statusCode: 200

      - post:
          url: "/api/posts"
          headers:
            Authorization: "Bearer {{ authToken }}"
          json:
            title: "Test Post"
            content: "This is a test"
          expect:
            - statusCode: 201

  - name: "Browse Posts"
    weight: 3
    flow:
      - get:
          url: "/api/posts?page=1&limit=20"
          expect:
            - statusCode: 200
            - hasProperty: data

      - think: 2  # Wait 2 seconds

      - get:
          url: "/api/posts/{{ $randomNumber(1, 100) }}"
          expect:
            - statusCode: [200, 404]
```

```javascript
// helpers.js
module.exports = {
  generateRandomEmail,
  logResponse,
};

function generateRandomEmail(context, events, done) {
  context.vars.email = `user-${Date.now()}@example.com`;
  return done();
}

function logResponse(requestParams, response, context, ee, next) {
  if (response.statusCode >= 400) {
    console.error(`Error ${response.statusCode}: ${response.body}`);
  }
  return next();
}
```

## Running Tests

```bash
# k6
k6 run load-test.js
k6 run --vus 100 --duration 5m load-test.js
k6 run --env BASE_URL=https://api.example.com load-test.js

# k6 Cloud
k6 cloud load-test.js

# Artillery
artillery run artillery.yml
artillery run --target https://api.example.com artillery.yml

# Artillery with environment
API_TOKEN=xxx artillery run artillery.yml

# Generate HTML report
artillery run --output report.json artillery.yml
artillery report report.json
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/load-test.yml
name: Load Test

on:
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run k6 load test
        uses: grafana/k6-action@v0.3.0
        with:
          filename: tests/load-test.js
          cloud: true
          token: ${{ secrets.K6_CLOUD_TOKEN }}
        env:
          BASE_URL: ${{ secrets.STAGING_URL }}
          API_TOKEN: ${{ secrets.API_TOKEN }}
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: load-test-results
          path: summary.json
```

## Performance Benchmarking

```javascript
// benchmark.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    baseline: {
      executor: 'constant-vus',
      vus: 1,
      duration: '1m',
      tags: { test_type: 'baseline' },
    },
  },
};

export default function () {
  const endpoints = [
    '/api/users',
    '/api/posts',
    '/api/comments',
  ];

  endpoints.forEach(endpoint => {
    const response = http.get(`${BASE_URL}${endpoint}`);
    
    check(response, {
      [`${endpoint} status 200`]: (r) => r.status === 200,
    });
  });
}

export function handleSummary(data) {
  const baseline = {
    endpoints: {},
    timestamp: new Date().toISOString(),
  };

  for (const [name, metric] of Object.entries(data.metrics)) {
    if (name.includes('http_req_duration')) {
      baseline.endpoints[name] = {
        avg: metric.values.avg,
        p95: metric.values['p(95)'],
        p99: metric.values['p(99)'],
      };
    }
  }

  return {
    'baseline.json': JSON.stringify(baseline, null, 2),
  };
}
```

## Analyzing Results

### Key Metrics to Monitor

1. **Response Time**
   - Average, p95, p99
   - Target: p95 < 500ms, p99 < 1s

2. **Error Rate**
   - HTTP 4xx, 5xx errors
   - Target: < 1%

3. **Throughput**
   - Requests per second
   - Target: Based on requirements

4. **Concurrent Users**
   - Maximum sustainable load
   - Target: Based on traffic projections

### Identifying Bottlenecks

```javascript
// Find slow endpoints
const slowRequests = data.metrics.http_req_duration.values;
console.log(`Average: ${slowRequests.avg}ms`);
console.log(`p95: ${slowRequests['p(95)']}ms`);
console.log(`p99: ${slowRequests['p(99)']}ms`);

// Check error patterns
const failedRequests = data.metrics.http_req_failed.values.rate;
if (failedRequests > 0.01) {
  console.error(`Error rate: ${failedRequests * 100}%`);
}
```

## Best Practices

### Test Types

1. **Smoke Test:** 1-2 VUs, 1-2 minutes
   - Verify system works under minimal load

2. **Load Test:** Expected normal/peak load, 5-15 minutes
   - Validate performance under typical conditions

3. **Stress Test:** Beyond peak load, gradually increase
   - Find breaking point

4. **Spike Test:** Sudden large increase, then drop
   - Test auto-scaling, recovery

5. **Soak Test:** Moderate load, 1+ hours
   - Find memory leaks, degradation

### Checklist

- [ ] Define performance requirements (SLAs)
- [ ] Identify critical user flows
- [ ] Prepare test data (users, content)
- [ ] Set up realistic scenarios
- [ ] Configure appropriate thresholds
- [ ] Test in staging environment first
- [ ] Monitor system resources during tests
- [ ] Analyze results against baselines
- [ ] Document bottlenecks and fixes
- [ ] Run tests regularly (CI/CD)
- [ ] Compare results over time

**Design load tests, execute tests, analyze results, provide optimization recommendations.**
