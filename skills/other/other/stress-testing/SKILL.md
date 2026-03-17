---
name: stress-testing
description: Test system behavior under extreme load conditions to identify breaking points, capacity limits, and failure modes. Use for stress test, capacity testing, breaking point analysis, spike test, and system limits validation.
---

# Stress Testing

## Overview

Stress testing pushes systems beyond normal operating capacity to identify breaking points, failure modes, and recovery behavior. It validates system stability under extreme conditions and helps determine maximum capacity before degradation or failure.

## When to Use

- Finding system capacity limits
- Identifying breaking points
- Testing auto-scaling behavior
- Validating error handling under load
- Testing recovery after failures
- Planning capacity requirements
- Verifying graceful degradation
- Testing spike traffic handling

## Test Types

- **Stress Test**: Gradually increase load until failure
- **Spike Test**: Sudden large increase in load
- **Soak Test**: Sustained high load over extended period
- **Capacity Test**: Find maximum sustainable load
- **Volume Test**: Large data volumes
- **Scalability Test**: Performance at different scales

## Instructions

### 1. **k6 Stress Testing**

```javascript
// stress-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    // Stress testing: Progressive load increase
    { duration: '2m', target: 100 },    // Normal load
    { duration: '5m', target: 100 },    // Sustain normal
    { duration: '2m', target: 200 },    // Above normal
    { duration: '5m', target: 200 },    // Sustain above normal
    { duration: '2m', target: 300 },    // Breaking point approaching
    { duration: '5m', target: 300 },    // Sustain high load
    { duration: '2m', target: 400 },    // Beyond capacity
    { duration: '5m', target: 400 },    // System under stress
    { duration: '5m', target: 0 },      // Gradual recovery
  ],
  thresholds: {
    http_req_duration: ['p(99)<1000'],  // 99% under 1s during stress
    http_req_failed: ['rate<0.05'],     // Allow 5% error rate under stress
    errors: ['rate<0.1'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export function setup() {
  // Prepare test data
  const res = http.post(`${BASE_URL}/api/auth/login`, {
    email: 'stress-test@example.com',
    password: 'test123',
  });

  return { token: res.json('token') };
}

export default function (data) {
  const headers = {
    Authorization: `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };

  // Heavy database query
  const productsRes = http.get(
    `${BASE_URL}/api/products?page=1&limit=100`,
    { headers }
  );

  const productsCheck = check(productsRes, {
    'products loaded': (r) => r.status === 200,
    'has products': (r) => r.json('products').length > 0,
  });

  if (!productsCheck) {
    errorRate.add(1);
    console.error(`Products failed: ${productsRes.status} ${productsRes.body}`);
  }

  sleep(1);

  // Write operation - stress database
  const orderPayload = JSON.stringify({
    items: [
      { productId: Math.floor(Math.random() * 100), quantity: 2 },
    ],
  });

  const orderRes = http.post(`${BASE_URL}/api/orders`, orderPayload, {
    headers,
  });

  const orderCheck = check(orderRes, {
    'order created': (r) => r.status === 201 || r.status === 503,
    'response within 5s': (r) => r.timings.duration < 5000,
  });

  if (!orderCheck) {
    errorRate.add(1);
  }

  // Monitor degradation
  if (orderRes.status === 503) {
    console.log('Service unavailable - system at capacity');
  }

  sleep(1);
}

export function teardown(data) {
  // Log final metrics
  console.log('Stress test completed');
}
```

### 2. **Spike Testing**

```javascript
// spike-test.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },     // Normal baseline
    { duration: '1m', target: 10 },      // Stable baseline
    { duration: '10s', target: 1000 },   // SPIKE! 100x increase
    { duration: '3m', target: 1000 },    // Maintain spike
    { duration: '10s', target: 10 },     // Drop back
    { duration: '3m', target: 10 },      // Recovery period
  ],
  thresholds: {
    http_req_duration: ['p(95)<5000'],   // Allow degradation during spike
    http_req_failed: ['rate<0.1'],       // Allow 10% errors during spike
  },
};

export default function () {
  const res = http.get('http://api.example.com/health');

  check(res, {
    'system responsive': (r) => r.status === 200 || r.status === 429,
    'response received': (r) => r.body.length > 0,
  });
}
```

### 3. **Soak/Endurance Testing**

```python
# soak_test.py
import asyncio
import aiohttp
import time
from datetime import datetime, timedelta
import psutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SoakTest:
    """Run sustained load test to detect memory leaks and degradation."""

    def __init__(self, url, duration_hours=4, requests_per_second=50):
        self.url = url
        self.duration = timedelta(hours=duration_hours)
        self.rps = requests_per_second
        self.metrics = {
            'requests': 0,
            'errors': 0,
            'response_times': [],
            'memory_usage': [],
        }

    async def make_request(self, session):
        """Make single request and record metrics."""
        start = time.time()
        try:
            async with session.get(self.url) as response:
                await response.read()
                duration = time.time() - start

                self.metrics['requests'] += 1
                self.metrics['response_times'].append(duration)

                if response.status >= 400:
                    self.metrics['errors'] += 1
                    logger.warning(f"Error: {response.status}")

        except Exception as e:
            self.metrics['errors'] += 1
            logger.error(f"Request failed: {e}")

    async def worker(self, session):
        """Worker that makes requests at target rate."""
        while self.running:
            await self.make_request(session)
            await asyncio.sleep(1 / self.rps)

    def monitor_resources(self):
        """Monitor system resources."""
        process = psutil.Process()
        return {
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'cpu_percent': process.cpu_percent(),
            'timestamp': datetime.now(),
        }

    async def run(self):
        """Execute soak test."""
        start_time = datetime.now()
        end_time = start_time + self.duration
        self.running = True

        logger.info(f"Starting soak test for {self.duration}")
        logger.info(f"Target: {self.rps} req/s to {self.url}")

        async with aiohttp.ClientSession() as session:
            # Start workers
            workers = [
                asyncio.create_task(self.worker(session))
                for _ in range(10)  # 10 concurrent workers
            ]

            # Monitor resources periodically
            while datetime.now() < end_time:
                await asyncio.sleep(60)  # Check every minute

                resources = self.monitor_resources()
                self.metrics['memory_usage'].append(resources)

                # Log progress
                elapsed = (datetime.now() - start_time).total_seconds()
                error_rate = self.metrics['errors'] / max(self.metrics['requests'], 1)
                avg_response = sum(self.metrics['response_times'][-1000:]) / 1000

                logger.info(
                    f"Elapsed: {elapsed:.0f}s | "
                    f"Requests: {self.metrics['requests']} | "
                    f"Error Rate: {error_rate:.2%} | "
                    f"Avg Response: {avg_response:.3f}s | "
                    f"Memory: {resources['memory_mb']:.1f}MB"
                )

                # Check for memory leak
                if len(self.metrics['memory_usage']) > 10:
                    initial_mem = self.metrics['memory_usage'][0]['memory_mb']
                    current_mem = resources['memory_mb']
                    growth = current_mem - initial_mem

                    if growth > 500:  # 500MB growth
                        logger.warning(f"Possible memory leak: +{growth:.1f}MB")

            # Stop workers
            self.running = False
            await asyncio.gather(*workers, return_exceptions=True)

        self.report()

    def report(self):
        """Generate test report."""
        total_requests = self.metrics['requests']
        error_rate = self.metrics['errors'] / total_requests if total_requests > 0 else 0
        response_times = self.metrics['response_times']

        print("\n" + "="*60)
        print("SOAK TEST RESULTS")
        print("="*60)
        print(f"Total Requests: {total_requests:,}")
        print(f"Total Errors: {self.metrics['errors']:,}")
        print(f"Error Rate: {error_rate:.2%}")
        print(f"\nResponse Times:")
        print(f"  Min: {min(response_times):.3f}s")
        print(f"  Max: {max(response_times):.3f}s")
        print(f"  Mean: {sum(response_times)/len(response_times):.3f}s")
        print(f"  P95: {sorted(response_times)[int(len(response_times)*0.95)]:.3f}s")

        # Memory analysis
        if self.metrics['memory_usage']:
            initial_mem = self.metrics['memory_usage'][0]['memory_mb']
            final_mem = self.metrics['memory_usage'][-1]['memory_mb']
            growth = final_mem - initial_mem

            print(f"\nMemory Usage:")
            print(f"  Initial: {initial_mem:.1f}MB")
            print(f"  Final: {final_mem:.1f}MB")
            print(f"  Growth: {growth:.1f}MB ({growth/initial_mem*100:.1f}%)")

            if growth > 200:
                print("  ⚠️  Possible memory leak detected!")

        print("="*60)

# Run soak test
if __name__ == '__main__':
    test = SoakTest(
        url='http://api.example.com/products',
        duration_hours=4,
        requests_per_second=50
    )
    asyncio.run(test.run())
```

### 4. **JMeter Stress Test**

```xml
<!-- stress-test.jmx -->
<jmeterTestPlan>
  <ThreadGroup testname="Stress Test Thread Group">
    <!-- Ultimate Thread Group for advanced load patterns -->
    <elementProp name="ThreadGroup.main_controller">
      <!-- Stage 1: Ramp up to 100 users -->
      <collectionProp name="ultimatethreadgroupdata">
        <stringProp>100</stringProp>  <!-- Users -->
        <stringProp>60</stringProp>   <!-- Ramp-up (sec) -->
        <stringProp>300</stringProp>  <!-- Duration (sec) -->
      </collectionProp>

      <!-- Stage 2: Ramp up to 500 users -->
      <collectionProp name="ultimatethreadgroupdata">
        <stringProp>500</stringProp>
        <stringProp>120</stringProp>
        <stringProp>600</stringProp>
      </collectionProp>

      <!-- Stage 3: Ramp up to 1000 users (stress) -->
      <collectionProp name="ultimatethreadgroupdata">
        <stringProp>1000</stringProp>
        <stringProp>180</stringProp>
        <stringProp>600</stringProp>
      </collectionProp>
    </elementProp>

    <HTTPSamplerProxy testname="Heavy Query">
      <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
      <stringProp name="HTTPSampler.path">/api/search?q=stress</stringProp>
      <stringProp name="HTTPSampler.method">GET</stringProp>
    </HTTPSamplerProxy>

    <!-- Monitor for errors and degradation -->
    <ResponseAssertion testname="Allow 503 During Stress">
      <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
      <stringProp name="Assertion.test_type">8</stringProp>
      <stringProp>200|503</stringProp>
    </ResponseAssertion>
  </ThreadGroup>
</jmeterTestPlan>
```

### 5. **Auto-Scaling Validation**

```typescript
// test-autoscaling.ts
import { test, expect } from '@playwright/test';
import axios from 'axios';

test.describe('Auto-scaling Stress Test', () => {
  test('system should scale up under load', async () => {
    const baseUrl = 'http://api.example.com';
    const cloudwatch = new AWS.CloudWatch();

    // Initial instance count
    const initialInstances = await getInstanceCount();
    console.log(`Initial instances: ${initialInstances}`);

    // Generate high load
    const requests = [];
    for (let i = 0; i < 1000; i++) {
      requests.push(
        axios.get(`${baseUrl}/api/heavy-operation`)
          .catch(err => ({ error: err.message }))
      );
    }

    // Wait for auto-scaling trigger
    await Promise.all(requests);
    await new Promise(resolve => setTimeout(resolve, 120000)); // 2 min

    // Check if scaled up
    const scaledInstances = await getInstanceCount();
    console.log(`Scaled instances: ${scaledInstances}`);

    expect(scaledInstances).toBeGreaterThan(initialInstances);

    // Verify metrics
    const cpuMetrics = await cloudwatch.getMetricStatistics({
      Namespace: 'AWS/EC2',
      MetricName: 'CPUUtilization',
      // ... metric params
    }).promise();

    expect(cpuMetrics.Datapoints.some(d => d.Average > 70)).toBe(true);
  });
});
```

### 6. **Breaking Point Analysis**

```python
# find_breaking_point.py
import requests
import threading
import time
from collections import defaultdict

class BreakingPointTest:
    """Find system breaking point by gradually increasing load."""

    def __init__(self, url):
        self.url = url
        self.results = defaultdict(lambda: {'success': 0, 'errors': 0, 'times': []})
        self.running = True

    def worker(self, vusers):
        """Worker thread that makes requests."""
        while self.running:
            start = time.time()
            try:
                response = requests.get(self.url, timeout=10)
                duration = time.time() - start

                if response.status_code == 200:
                    self.results[vusers]['success'] += 1
                    self.results[vusers]['times'].append(duration)
                else:
                    self.results[vusers]['errors'] += 1

            except Exception as e:
                self.results[vusers]['errors'] += 1

            time.sleep(0.1)

    def test_load_level(self, vusers, duration=60):
        """Test system with specific number of virtual users."""
        print(f"\nTesting with {vusers} concurrent users...")

        threads = []
        for _ in range(vusers):
            t = threading.Thread(target=self.worker, args=(vusers,))
            t.start()
            threads.append(t)

        time.sleep(duration)

        self.running = False
        for t in threads:
            t.join()

        self.running = True

        # Analyze results
        stats = self.results[vusers]
        total = stats['success'] + stats['errors']
        error_rate = stats['errors'] / total if total > 0 else 0
        avg_time = sum(stats['times']) / len(stats['times']) if stats['times'] else 0

        print(f"  Requests: {total}")
        print(f"  Success: {stats['success']}")
        print(f"  Errors: {stats['errors']}")
        print(f"  Error Rate: {error_rate:.1%}")
        print(f"  Avg Response: {avg_time:.3f}s")

        # System is breaking if error rate > 5% or avg response > 5s
        is_breaking = error_rate > 0.05 or avg_time > 5.0

        return not is_breaking

    def find_breaking_point(self):
        """Binary search to find breaking point."""
        min_users = 10
        max_users = 1000
        breaking_point = None

        while min_users < max_users:
            mid = (min_users + max_users) // 2

            if self.test_load_level(mid):
                # System handles this load, try higher
                min_users = mid + 10
            else:
                # System breaking, found upper limit
                breaking_point = mid
                max_users = mid - 10

        print(f"\n{'='*60}")
        print(f"Breaking point: ~{breaking_point} concurrent users")
        print(f"{'='*60}")

        return breaking_point

# Run
test = BreakingPointTest('http://api.example.com/products')
test.find_breaking_point()
```

## Metrics to Monitor

### Application Metrics
- Response times (P50, P95, P99, Max)
- Error rates and types
- Throughput (req/s)
- Queue depths
- Circuit breaker trips

### System Metrics
- CPU utilization
- Memory usage and leaks
- Disk I/O
- Network bandwidth
- Thread/connection pools

### Database Metrics
- Query execution times
- Connection pool usage
- Lock contention
- Cache hit rates
- Replication lag

## Best Practices

### ✅ DO
- Test in production-like environment
- Monitor all system resources
- Gradually increase load to find limits
- Test recovery after stress
- Document breaking points
- Test auto-scaling behavior
- Plan for graceful degradation
- Monitor for memory leaks

### ❌ DON'T
- Test in production without safeguards
- Skip recovery testing
- Ignore warning signs (CPU, memory)
- Test only success scenarios
- Assume linear scalability
- Forget database capacity
- Skip monitoring third-party dependencies
- Test without proper cleanup

## Tools

- **Load Generation**: k6, JMeter, Gatling, Locust, Artillery
- **Monitoring**: Prometheus, Grafana, DataDog, New Relic
- **Cloud Metrics**: CloudWatch, Azure Monitor, GCP Monitoring
- **Profiling**: py-spy, async-profiler, clinic.js

## Examples

See also: performance-testing, continuous-testing, api-versioning-strategy for comprehensive system testing.
