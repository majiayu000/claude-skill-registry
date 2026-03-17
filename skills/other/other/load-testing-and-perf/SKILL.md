---
name: load-testing-and-perf
description: Run load tests and profile applications with Locust, py-spy, and database query analysis
---

# Load Testing and Performance Profiling

## Decision Table

| Scenario | Tool | Why |
|----------|------|-----|
| HTTP API load testing | Locust | Python-native, programmable scenarios, distributed mode |
| Protocol-level perf (gRPC, WS) | k6 | Built-in protocol support, JS scripting |
| Production CPU profiling | py-spy | No code changes, low overhead, flame graphs |
| Function-level hotspots | line_profiler | Per-line timing, surgical precision |
| Memory profiling | memray | Native + Python allocations, flame graphs |
| DB query performance | EXPLAIN ANALYZE | Actual execution plan with timing |
| Microbenchmarks | pytest-benchmark | Statistical rigor, comparison across runs |

## Locust Load Testing

### Basic HttpUser with Custom Shape

```python
# locustfile.py
from locust import HttpUser, task, between, tag, LoadTestShape

class APIUser(HttpUser):
    wait_time = between(1, 3)  # seconds between tasks
    host = "http://localhost:8000"

    def on_start(self):
        resp = self.client.post("/auth/login", json={
            "username": "loadtest", "password": "secret"
        })
        self.token = resp.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @tag("read")
    @task(10)  # weight: 10x more likely than weight-1 tasks
    def list_items(self):
        with self.client.get("/api/items", headers=self.headers,
                             catch_response=True) as resp:
            if resp.status_code == 200 and len(resp.json()) > 0:
                resp.success()
            else:
                resp.failure(f"Unexpected: {resp.status_code}")

    @tag("write")
    @task(1)
    def create_item(self):
        self.client.post("/api/items", headers=self.headers,
                         json={"name": "load-test-item", "value": 42})

class StepLoadShape(LoadTestShape):
    """Ramp up in steps: 10 users every 30s up to 100, hold, ramp down."""
    stages = [
        {"duration": 30,  "users": 10,  "spawn_rate": 10},
        {"duration": 60,  "users": 50,  "spawn_rate": 10},
        {"duration": 120, "users": 100, "spawn_rate": 10},
        {"duration": 240, "users": 100, "spawn_rate": 10},  # hold
        {"duration": 270, "users": 0,   "spawn_rate": 10},  # ramp down
    ]
    def tick(self):
        run_time = self.get_run_time()
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        return None
```

### Distributed Mode

```bash
# master
locust --master --expect-workers=4 -f locustfile.py
# workers (separate machines)
locust --worker --master-host=10.0.0.1 -f locustfile.py
```

## k6 Script Patterns

```javascript
// load_test.js
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

const errorRate = new Rate("errors");

export const options = {
  stages: [
    { duration: "30s", target: 20 },  // ramp up
    { duration: "1m",  target: 20 },  // hold
    { duration: "10s", target: 0 },   // ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<500", "p(99)<1000"],
    errors: ["rate<0.01"],
  },
};

export default function () {
  const res = http.get("http://localhost:8000/api/items");
  check(res, {
    "status is 200": (r) => r.status === 200,
    "body has items": (r) => JSON.parse(r.body).length > 0,
  }) || errorRate.add(1);
  sleep(1);
}
```

## Python Profiling

### py-spy and cProfile

```bash
# profile a running process (no code changes needed)
py-spy record -o profile.svg --pid 12345
# profile a script directly
py-spy record -o profile.svg -- python app.py
# top-like live view
py-spy top --pid 12345
```

```python
# profile_runner.py
import cProfile, pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile a function and return sorted stats."""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(20)
    print(stream.getvalue())
    return result

# save for snakeviz: cProfile.run("main()", "output.prof")
# then: snakeviz output.prof
```

### line_profiler for Hot Functions

```python
# pip install line_profiler
from line_profiler import profile

@profile
def process_batch(items):
    results = []
    for item in items:            # line-by-line timing shown
        parsed = parse(item)       # identify which lines are slow
        validated = validate(parsed)
        results.append(validated)
    return results
# run: kernprof -l -v script.py
```

## Benchmarking Methodology

```python
# test_perf.py -- pytest-benchmark
import json, pytest

def test_serialization_perf(benchmark):
    data = {"users": [{"id": i, "name": f"user_{i}"} for i in range(1000)]}
    result = benchmark(json.dumps, data)  # warmup + stats automatic
    assert result is not None

def test_db_query_perf(benchmark, db_session):
    benchmark.pedantic(
        target=lambda: db_session.execute("SELECT count(*) FROM users"),
        rounds=50, warmup_rounds=5, iterations=1,
    )
# run: pytest test_perf.py --benchmark-only --benchmark-histogram
```

### Percentile Analysis

```python
# perf_stats.py
import numpy as np, time

def measure_latencies(func, n=1000, warmup=50):
    """Run func n times, return percentile breakdown."""
    for _ in range(warmup):
        func()  # let JIT/caches stabilize
    latencies = []
    for _ in range(n):
        start = time.perf_counter_ns()
        func()
        latencies.append(time.perf_counter_ns() - start)
    arr = np.array(latencies) / 1e6  # convert to ms
    return {f"p{p}": np.percentile(arr, p) for p in [50, 90, 95, 99]} | {
        "mean": np.mean(arr), "std": np.std(arr),
    }
```

## Database Query Profiling

```sql
-- full execution plan with buffers and timing
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT u.id, u.email, count(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > now() - interval '30 days'
GROUP BY u.id;
```

```python
# analyze_slow_queries.py
import psycopg2

def find_slow_queries(conn, min_mean_ms=100, limit=20):
    """Pull worst queries from pg_stat_statements."""
    cur = conn.cursor()
    cur.execute("""
        SELECT query, calls, mean_exec_time, total_exec_time, rows
        FROM pg_stat_statements
        WHERE mean_exec_time > %s
        ORDER BY total_exec_time DESC LIMIT %s
    """, (min_mean_ms, limit))
    for query, calls, mean_ms, total_ms, rows in cur.fetchall():
        print(f"Mean: {mean_ms:.1f}ms | Calls: {calls} | "
              f"Total: {total_ms/1000:.1f}s\n  {query[:120]}\n")
```

## Gotchas

- **Locust counts RPS per worker** -- aggregate in master UI, not per-worker logs
- **py-spy needs root on Linux** -- use `--nonblocking` or run as root; macOS needs SIP consideration
- **cProfile overhead is ~2x** -- do not use in production; use py-spy for live systems
- **k6 thresholds are assertions** -- test exits non-zero if thresholds fail; wire into CI
- **Warmup matters** -- first N requests hit cold caches, JIT compilation; always discard
- **Coordinated omission** -- if load tool waits for response before sending next, you undercount tail latency
- **EXPLAIN vs EXPLAIN ANALYZE** -- plain EXPLAIN shows estimated plan; ANALYZE executes the query
- **pg_stat_statements requires extension** -- `CREATE EXTENSION pg_stat_statements` and restart
- **line_profiler slows code 10-50x** -- profile only targeted functions, never full application
- **Distributed Locust workers share nothing** -- each loads its own locustfile; ensure identical code
