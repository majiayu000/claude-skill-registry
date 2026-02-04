---
name: performance-testing
description: Design and execute performance tests to measure response times, throughput, and resource utilization. Use for performance test, load test, JMeter, k6, benchmark, latency testing, and scalability analysis.
---

# Performance Testing

## Overview

Performance testing measures how systems behave under various load conditions, including response times, throughput, resource utilization, and scalability. It helps identify bottlenecks, validate performance requirements, and ensure systems can handle expected loads.

## When to Use

- Validating response time requirements
- Measuring API throughput and latency
- Testing database query performance
- Identifying performance bottlenecks
- Comparing algorithm efficiency
- Benchmarking before/after optimizations
- Validating caching effectiveness
- Testing concurrent user capacity

## Types of Performance Tests

- **Load Testing**: Normal expected load
- **Stress Testing**: Beyond normal capacity (see stress-testing skill)
- **Spike Testing**: Sudden load increases
- **Endurance Testing**: Sustained load over time
- **Scalability Testing**: Performance at different scales
- **Benchmark Testing**: Component-level performance

## Instructions

### 1. **k6 for API Load Testing**

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const orderDuration = new Trend('order_duration');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 10 },   // Ramp up to 10 users
    { duration: '5m', target: 10 },   // Stay at 10 users
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },   // Stay at 50 users
    { duration: '2m', target: 0 },    // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests under 500ms
    http_req_failed: ['rate<0.01'],    // Error rate under 1%
    errors: ['rate<0.1'],              // Custom error rate under 10%
  },
};

// Test data
const BASE_URL = 'https://api.example.com';
let authToken;

export function setup() {
  // Login once and get auth token
  const loginRes = http.post(`${BASE_URL}/auth/login`, {
    email: 'test@example.com',
    password: 'password123',
  });

  return { token: loginRes.json('token') };
}

export default function (data) {
  // Test 1: Get products (read-heavy)
  const productsRes = http.get(`${BASE_URL}/products`, {
    headers: { Authorization: `Bearer ${data.token}` },
  });

  check(productsRes, {
    'products status is 200': (r) => r.status === 200,
    'products response time < 200ms': (r) => r.timings.duration < 200,
    'has products array': (r) => Array.isArray(r.json('products')),
  }) || errorRate.add(1);

  sleep(1);

  // Test 2: Create order (write-heavy)
  const orderPayload = JSON.stringify({
    userId: 'user-123',
    items: [
      { productId: 'prod-1', quantity: 2 },
      { productId: 'prod-2', quantity: 1 },
    ],
  });

  const orderRes = http.post(`${BASE_URL}/orders`, orderPayload, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${data.token}`,
    },
  });

  const orderSuccess = check(orderRes, {
    'order status is 201': (r) => r.status === 201,
    'order has id': (r) => r.json('id') !== undefined,
  });

  if (!orderSuccess) {
    errorRate.add(1);
  }

  orderDuration.add(orderRes.timings.duration);

  sleep(2);

  // Test 3: Get order details
  if (orderSuccess) {
    const orderId = orderRes.json('id');
    const orderDetailRes = http.get(`${BASE_URL}/orders/${orderId}`, {
      headers: { Authorization: `Bearer ${data.token}` },
    });

    check(orderDetailRes, {
      'order detail status is 200': (r) => r.status === 200,
    }) || errorRate.add(1);
  }

  sleep(1);
}

export function teardown(data) {
  // Cleanup if needed
}
```

```bash
# Run k6 test
k6 run load-test.js

# Run with different scenarios
k6 run --vus 100 --duration 30s load-test.js

# Output to InfluxDB for visualization
k6 run --out influxdb=http://localhost:8086/k6 load-test.js
```

### 2. **Apache JMeter**

```xml
<!-- test-plan.jmx (simplified representation) -->
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2">
  <hashTree>
    <TestPlan testname="API Performance Test">
      <ThreadGroup testname="Users">
        <elementProp name="ThreadGroup.main_controller">
          <stringProp name="ThreadGroup.num_threads">50</stringProp>
          <stringProp name="ThreadGroup.ramp_time">60</stringProp>
          <stringProp name="ThreadGroup.duration">300</stringProp>
        </elementProp>

        <!-- HTTP Request: Get Products -->
        <HTTPSamplerProxy testname="GET /products">
          <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
          <stringProp name="HTTPSampler.path">/products</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
        </HTTPSamplerProxy>

        <!-- Assertions -->
        <ResponseAssertion testname="Response Code 200">
          <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
          <stringProp name="Assertion.test_type">8</stringProp>
          <stringProp name="Assertion.test_string">200</stringProp>
        </ResponseAssertion>

        <DurationAssertion testname="Response Time < 500ms">
          <stringProp name="DurationAssertion.duration">500</stringProp>
        </DurationAssertion>

        <!-- Timers -->
        <ConstantTimer testname="Think Time">
          <stringProp name="ConstantTimer.delay">2000</stringProp>
        </ConstantTimer>
      </ThreadGroup>
    </TestPlan>
  </hashTree>
</jmeterTestPlan>
```

```bash
# Run JMeter test
jmeter -n -t test-plan.jmx -l results.jtl -e -o report/

# Generate report from results
jmeter -g results.jtl -o report/
```

### 3. **pytest-benchmark for Python**

```python
# test_performance.py
import pytest
from app.services import DataProcessor, SearchEngine
from app.models import User, Product

class TestDataProcessorPerformance:
    @pytest.fixture
    def large_dataset(self):
        """Create large dataset for testing."""
        return [{'id': i, 'value': i * 2} for i in range(10000)]

    def test_process_data_performance(self, benchmark, large_dataset):
        """Benchmark data processing."""
        processor = DataProcessor()

        result = benchmark(processor.process, large_dataset)

        assert len(result) == len(large_dataset)
        # Benchmark will report execution time

    def test_filter_data_performance(self, benchmark, large_dataset):
        """Test filtering performance with different conditions."""
        processor = DataProcessor()

        def filter_operation():
            return processor.filter(large_dataset, lambda x: x['value'] > 5000)

        result = benchmark(filter_operation)
        assert all(item['value'] > 5000 for item in result)

    @pytest.mark.parametrize('dataset_size', [100, 1000, 10000])
    def test_scalability(self, benchmark, dataset_size):
        """Test performance at different scales."""
        processor = DataProcessor()
        data = [{'id': i, 'value': i} for i in range(dataset_size)]

        benchmark(processor.process, data)

class TestSearchPerformance:
    @pytest.fixture
    def search_engine(self):
        """Setup search engine with indexed data."""
        engine = SearchEngine()
        # Index 10,000 products
        for i in range(10000):
            engine.index(Product(id=i, name=f"Product {i}"))
        return engine

    def test_search_performance(self, benchmark, search_engine):
        """Benchmark search query."""
        result = benchmark(search_engine.search, "Product 5000")
        assert len(result) > 0

    def test_search_with_filters(self, benchmark, search_engine):
        """Benchmark search with filters."""
        def search_with_filters():
            return search_engine.search(
                "Product",
                filters={'price_min': 10, 'price_max': 100}
            )

        result = benchmark(search_with_filters)

# Run benchmarks
# pytest test_performance.py --benchmark-only
# pytest test_performance.py --benchmark-compare
```

### 4. **JMH for Java Benchmarking**

```java
// PerformanceBenchmark.java
import org.openjdk.jmh.annotations.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
@Fork(value = 1, warmups = 1)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 5, time = 1)
public class CollectionPerformanceBenchmark {

    @Param({"100", "1000", "10000"})
    private int size;

    private List<Integer> arrayList;
    private List<Integer> linkedList;
    private Set<Integer> hashSet;

    @Setup
    public void setup() {
        arrayList = new ArrayList<>();
        linkedList = new LinkedList<>();
        hashSet = new HashSet<>();

        for (int i = 0; i < size; i++) {
            arrayList.add(i);
            linkedList.add(i);
            hashSet.add(i);
        }
    }

    @Benchmark
    public void arrayListIteration() {
        int sum = 0;
        for (Integer num : arrayList) {
            sum += num;
        }
    }

    @Benchmark
    public void linkedListIteration() {
        int sum = 0;
        for (Integer num : linkedList) {
            sum += num;
        }
    }

    @Benchmark
    public void arrayListRandomAccess() {
        for (int i = 0; i < size; i++) {
            arrayList.get(i);
        }
    }

    @Benchmark
    public void linkedListRandomAccess() {
        for (int i = 0; i < size; i++) {
            linkedList.get(i);
        }
    }

    @Benchmark
    public boolean hashSetContains() {
        return hashSet.contains(size / 2);
    }

    public static void main(String[] args) throws Exception {
        org.openjdk.jmh.Main.main(args);
    }
}

// Run: mvn clean install
//      java -jar target/benchmarks.jar
```

### 5. **Database Query Performance**

```python
# test_database_performance.py
import pytest
import time
from sqlalchemy import create_engine
from app.models import User, Order

class TestDatabasePerformance:
    @pytest.fixture
    def db_session(self):
        """Create test database session."""
        engine = create_engine('postgresql://localhost/testdb')
        Session = sessionmaker(bind=engine)
        return Session()

    def test_query_without_index(self, db_session, benchmark):
        """Measure query performance without index."""
        def query():
            return db_session.query(User).filter(
                User.email == 'test@example.com'
            ).first()

        result = benchmark(query)

    def test_query_with_index(self, db_session, benchmark):
        """Measure query performance with index."""
        # Assume email column is indexed
        def query():
            return db_session.query(User).filter(
                User.email == 'test@example.com'
            ).first()

        result = benchmark(query)

    def test_n_plus_one_query(self, db_session):
        """Identify N+1 query problem."""
        start = time.time()

        # ❌ N+1 queries
        users = db_session.query(User).all()
        for user in users:
            orders = user.orders  # Triggers separate query for each user

        n_plus_one_time = time.time() - start

        # ✅ Eager loading
        start = time.time()
        users = db_session.query(User).options(
            joinedload(User.orders)
        ).all()

        eager_time = time.time() - start

        assert eager_time < n_plus_one_time, "Eager loading should be faster"
        print(f"N+1: {n_plus_one_time:.3f}s, Eager: {eager_time:.3f}s")

    def test_pagination_performance(self, db_session, benchmark):
        """Test pagination efficiency."""
        def paginate():
            return db_session.query(Product)\
                .order_by(Product.id)\
                .limit(50)\
                .offset(1000)\
                .all()

        results = benchmark(paginate)
        assert len(results) == 50
```

### 6. **Real-Time Monitoring**

```javascript
// performance-monitor.js
class PerformanceMonitor {
  constructor() {
    this.metrics = [];
  }

  async measureEndpoint(name, fn) {
    const start = performance.now();
    const startMemory = process.memoryUsage();

    try {
      const result = await fn();
      const duration = performance.now() - start;
      const endMemory = process.memoryUsage();

      this.metrics.push({
        name,
        duration,
        memoryDelta: {
          heapUsed: endMemory.heapUsed - startMemory.heapUsed,
          external: endMemory.external - startMemory.external,
        },
        timestamp: new Date(),
      });

      return result;
    } catch (error) {
      throw error;
    }
  }

  getStats(name) {
    const measurements = this.metrics.filter(m => m.name === name);
    const durations = measurements.map(m => m.duration);

    return {
      count: measurements.length,
      mean: durations.reduce((a, b) => a + b, 0) / durations.length,
      min: Math.min(...durations),
      max: Math.max(...durations),
      p50: this.percentile(durations, 50),
      p95: this.percentile(durations, 95),
      p99: this.percentile(durations, 99),
    };
  }

  percentile(values, p) {
    const sorted = values.sort((a, b) => a - b);
    const index = Math.ceil((p / 100) * sorted.length) - 1;
    return sorted[index];
  }
}

// Usage in tests
const monitor = new PerformanceMonitor();

test('API endpoint performance', async () => {
  for (let i = 0; i < 100; i++) {
    await monitor.measureEndpoint('getUsers', async () => {
      return await fetch('/api/users').then(r => r.json());
    });
  }

  const stats = monitor.getStats('getUsers');

  expect(stats.p95).toBeLessThan(500); // 95th percentile under 500ms
  expect(stats.mean).toBeLessThan(200); // Average under 200ms
});
```

## Performance Metrics

### Response Time
- **Average**: Mean response time
- **Median (P50)**: 50th percentile
- **P95**: 95th percentile (SLA target)
- **P99**: 99th percentile (worst case)
- **Max**: Slowest response

### Throughput
- **Requests/second**: Number of requests processed
- **Transactions/second**: Completed transactions
- **Data transferred**: MB/s or GB/s

### Resource Utilization
- **CPU**: Percentage usage
- **Memory**: Heap, RSS, external
- **Network**: Bandwidth usage
- **Disk I/O**: Read/write operations

## Best Practices

### ✅ DO
- Define clear performance requirements (SLAs)
- Test with realistic data volumes
- Monitor resource utilization
- Test caching effectiveness
- Use percentiles (P95, P99) over averages
- Warm up before measuring
- Run tests in production-like environment
- Identify and fix N+1 query problems

### ❌ DON'T
- Test only with small datasets
- Ignore memory leaks
- Test in unrealistic environments
- Focus only on average response times
- Skip database indexing analysis
- Test only happy paths
- Ignore network latency
- Compare without statistical significance

## Tools

- **Load Testing**: k6, JMeter, Gatling, Locust, Artillery
- **Benchmarking**: JMH (Java), pytest-benchmark (Python), Benchmark.js (Node.js)
- **Profiling**: Chrome DevTools, py-spy, VisualVM
- **Monitoring**: Prometheus, Grafana, New Relic, Datadog
- **Database**: EXPLAIN ANALYZE, pg_stat_statements

## Examples

See also: stress-testing, continuous-testing, code-metrics-analysis for comprehensive performance analysis.
