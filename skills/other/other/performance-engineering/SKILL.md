---
name: performance-engineering
description: When validating system performance under load, identifying bottlenecks through profiling, or optimizing application responsiveness. Covers load testing (k6, Locust), profiling (CPU, memory, I/O), and optimization strategies (caching, query optimization, Core Web Vitals). Use for capacity planning, regression detection, and establishing performance SLOs.
---

# Performance Engineering

## Purpose

Performance engineering encompasses load testing, profiling, and optimization to deliver reliable, scalable systems. This skill provides frameworks for choosing the right performance testing approach (load, stress, soak, spike), profiling techniques to identify bottlenecks (CPU, memory, I/O), and optimization strategies for backend APIs, databases, and frontend applications.

Use this skill to validate system capacity before launch, detect performance regressions in CI/CD pipelines, identify and resolve bottlenecks through profiling, and optimize application responsiveness across the stack.

## When to Use This Skill

**Common Triggers:**
- "Validate API can handle expected traffic"
- "Find maximum capacity and breaking points"
- "Identify why the application is slow"
- "Detect memory leaks or resource exhaustion"
- "Optimize Core Web Vitals for SEO"
- "Set up performance testing in CI/CD"
- "Reduce cloud infrastructure costs"

**Use Cases:**
- Pre-launch capacity planning and load validation
- Post-refactor performance regression testing
- Investigating slow response times or high latency
- Detecting memory leaks in long-running services
- Optimizing database query performance
- Validating auto-scaling configuration
- Establishing performance SLOs and budgets

## Performance Testing Types

### Load Testing
Validate system behavior under expected traffic levels.

**When to use:** Pre-launch capacity planning, regression testing after refactors, validating auto-scaling.

### Stress Testing
Find system capacity limits and failure modes.

**When to use:** Capacity planning, understanding failure behavior, infrastructure sizing decisions.

### Soak Testing
Identify memory leaks, resource exhaustion, and degradation over time.

**When to use:** Detecting memory leaks, validating connection pool cleanup, testing long-running batch jobs.

### Spike Testing
Validate system response to sudden traffic spikes.

**When to use:** Validating auto-scaling, testing event-driven systems (product launches), ensuring rate limiting works.

## Quick Decision Framework

**Which test type to use?**

```
What am I trying to learn?
├─ Can my system handle expected traffic? → LOAD TEST
├─ What's the maximum capacity? → STRESS TEST
├─ Will it stay stable over time? → SOAK TEST
└─ Can it handle traffic spikes? → SPIKE TEST
```

For detailed testing patterns, load scenarios, and interpreting results, see `references/testing-types.md`.

## Load Testing Quick Starts

### k6 (JavaScript)

**Installation:**
```bash
brew install k6  # macOS
sudo apt-get install k6  # Linux
```

**Basic Load Test:**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 20 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
```

**Run:** `k6 run script.js`

For stress, soak, and spike testing examples, see `examples/k6/`.

### Locust (Python)

**Installation:**
```bash
pip install locust
```

**Basic Load Test:**
```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.example.com"

    @task(3)
    def view_products(self):
        self.client.get("/products")

    @task(1)
    def view_product_detail(self):
        self.client.get("/products/123")
```

**Run:** `locust -f locustfile.py --headless -u 100 -r 10 --run-time 10m`

For REST API testing and data-driven testing, see `examples/locust/`.

## Profiling Quick Starts

### When to Profile

| Symptom | Profiling Type | Tool |
|---------|----------------|------|
| High CPU (>70%) | CPU Profiling | py-spy, pprof, DevTools |
| Memory growing | Memory Profiling | memory_profiler, pprof heap |
| Slow response, low CPU | I/O Profiling | Query logs, pprof block |

### Python Profiling

**py-spy (Production-Safe):**
```bash
pip install py-spy

# Profile running process
py-spy record -o profile.svg --pid <PID> --duration 30

# Top-like view
py-spy top --pid <PID>
```

**Memory Profiling:**
```python
from memory_profiler import profile

@profile
def my_function():
    a = [1] * (10 ** 6)
    return a

# Run: python -m memory_profiler script.py
```

### Go Profiling

**pprof (Built-in):**
```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
    startApp()
}
```

**Capture profile:**
```bash
# CPU profile (30 seconds)
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Interactive analysis
(pprof) top
(pprof) web
```

### TypeScript/JavaScript Profiling

**Chrome DevTools (Browser/Node.js):**

Node.js:
```bash
node --inspect app.js
# Open chrome://inspect
# Performance tab → Record
```

**clinic.js (Node.js):**
```bash
npm install -g clinic
clinic doctor -- node app.js
```

For detailed profiling workflows and analysis, see `references/profiling-guide.md` and `examples/profiling/`.

## Optimization Strategies

### Caching

**When to cache:**
- Data queried frequently (>100 req/min)
- Data freshness tolerance (>1 minute acceptable staleness)

**Redis example:**
```python
import redis
r = redis.Redis()

def get_cached_data(key, fn, ttl=300):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    data = fn()
    r.setex(key, ttl, json.dumps(data))
    return data
```

### Database Query Optimization

**N+1 prevention:**
```python
# Bad: N+1 queries
users = User.query.all()
for user in users:
    print(user.orders)  # Separate query per user

# Good: Eager loading
users = User.query.options(joinedload(User.orders)).all()
```

**Indexing:**
```sql
CREATE INDEX idx_users_email ON users(email);
```

### API Performance

**Cursor-based pagination:**
```typescript
app.get('/api/products', async (req, res) => {
  const { cursor, limit = 20 } = req.query;

  const products = await db.query(
    'SELECT * FROM products WHERE id > ? ORDER BY id LIMIT ?',
    [cursor || 0, limit]
  );

  res.json({
    data: products,
    next_cursor: products[products.length - 1]?.id,
  });
});
```

### Frontend Performance (Core Web Vitals)

**Key metrics:**
- **LCP (Largest Contentful Paint):** < 2.5s
- **INP (Interaction to Next Paint):** < 200ms
- **CLS (Cumulative Layout Shift):** < 0.1

**Optimization techniques:**
- Code splitting (lazy loading)
- Image optimization (WebP, responsive, lazy loading)
- Preload critical resources
- Minimize render-blocking resources

For detailed optimization strategies, see `references/optimization-strategies.md` and `references/frontend-performance.md`.

## Performance SLOs

### Recommended SLOs by Service Type

| Service Type | p95 Latency | p99 Latency | Availability |
|--------------|-------------|-------------|--------------|
| User-Facing API | < 200ms | < 500ms | 99.9% |
| Internal API | < 100ms | < 300ms | 99.5% |
| Database Query | < 50ms | < 100ms | 99.99% |
| Background Job | < 5s | < 10s | 99% |
| Real-time API | < 50ms | < 100ms | 99.95% |

### SLO Selection Process

1. Measure baseline performance
2. Identify user expectations
3. Set achievable targets (10-20% better than baseline)
4. Iterate as system matures

For detailed SLO framework and performance budgets, see `references/slo-framework.md`.

## CI/CD Integration

### Performance Testing in Pipelines

**GitHub Actions example:**
```yaml
name: Performance Tests

on:
  pull_request:
    branches: [main]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install k6
        run: |
          curl https://github.com/grafana/k6/releases/download/v0.48.0/k6-v0.48.0-linux-amd64.tar.gz -L | tar xvz
          sudo mv k6-v0.48.0-linux-amd64/k6 /usr/local/bin/

      - name: Run load test
        run: k6 run tests/load/api-test.js
```

**Performance budgets:**
```javascript
// k6 test with thresholds (fail build if violated)
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

## Profiling Workflow

**Standard process:**
1. Observe symptoms (high CPU, memory growth, slow response)
2. Hypothesize bottleneck (CPU? Memory? I/O?)
3. Choose profiling type based on hypothesis
4. Run profiler under realistic load
5. Analyze profile (flamegraph, call tree)
6. Identify hot spots (top 20% functions using 80% resources)
7. Optimize bottlenecks
8. Re-profile to validate improvement

**Best practices:**
- Profile under realistic load (not idle systems)
- Use sampling profilers (py-spy, pprof) in production (low overhead)
- Focus on hot paths (optimize biggest bottlenecks first)
- Validate optimizations with before/after comparisons

## Tool Recommendations

### Load Testing

**Primary: k6** (JavaScript-based, Grafana-backed)
- Modern architecture, cloud-native
- JavaScript DSL (ES6+)
- Grafana/Prometheus integration
- Multi-protocol (HTTP/1.1, HTTP/2, WebSocket, gRPC)

**When to use:** Modern APIs, microservices, CI/CD integration.

**Alternative: Locust** (Python-based)
- Python-native (write tests in Python)
- Web UI for real-time monitoring
- Flexible for complex user scenarios

**When to use:** Python-heavy teams, complex user flows.

### Profiling

**Python:**
- py-spy (sampling, production-safe)
- cProfile (deterministic, detailed)
- memory_profiler (memory leak detection)

**Go:**
- pprof (built-in, CPU/heap/goroutine/block profiling)

**TypeScript/JavaScript:**
- Chrome DevTools (browser/Node.js)
- clinic.js (Node.js performance suite)

For detailed tool comparisons, see `references/testing-types.md` and `references/profiling-guide.md`.

## Reference Documentation

**Detailed Guides:**
- `references/testing-types.md` - Load, stress, soak, spike testing patterns
- `references/profiling-guide.md` - CPU, memory, I/O profiling across languages
- `references/optimization-strategies.md` - Caching, database, API optimization
- `references/frontend-performance.md` - Core Web Vitals, bundle optimization
- `references/slo-framework.md` - Setting SLOs, performance budgets
- `references/benchmarking.md` - Benchmarking best practices

**Examples:**
- `examples/k6/` - Load, stress, soak, spike tests
- `examples/locust/` - Python-based load testing
- `examples/profiling/` - Profiling examples (Python, Go, TypeScript)
- `examples/optimization/` - Caching, query, API optimization

## Related Skills

For comprehensive testing strategies, see the `testing-strategies` skill.

For CI/CD integration patterns, see the `building-ci-pipelines` skill.

For infrastructure sizing based on load tests, see the `infrastructure-as-code` skill.

For Kubernetes performance testing, see the `kubernetes-operations` skill.
