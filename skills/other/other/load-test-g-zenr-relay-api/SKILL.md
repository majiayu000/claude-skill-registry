---
name: load-test
description: Write performance and load tests to validate throughput and thread safety (Priya Sharma's workflow)
disable-model-invocation: true
---

Write performance/load tests for: $ARGUMENTS

## Step 1 — Identify Performance Scenarios
- **Throughput**: How many requests/second can the API handle?
- **Concurrency**: Do concurrent requests cause race conditions or deadlocks?
- **Rate limiting**: Does the rate limiter correctly throttle under load?
- **Rapid state changes**: Can the system handle rapid state cycling without corruption?
- **Response time**: Do endpoints respond within acceptable latency (< 200ms)?

## Step 2 — Write Concurrency Tests
```
// Concurrency test — verify thread-safe access under load
TestConcurrency {
    test_concurrent_state_changes_no_race_condition(client) {
        // Submit 50 concurrent state-changing requests using a thread pool
        pool = new ThreadPool(max_workers: 10)
        futures = []
        for i in range(50) {
            futures.append(pool.submit(make_state_change_request, client, i))
        }
        results = [f.result() for f in futures]

        // All requests should succeed (no 500s from race conditions)
        for resp in results {
            assert resp.status == 200
        }
        // Final state should be consistent
    }
}
```

## Step 3 — Write Rapid State Change Tests
Verify the system handles rapid state changes without corruption.
After rapid cycling, final state should be deterministic and consistent.

## Step 4 — Write Latency Tests
```
// Latency test — verify endpoints respond within acceptable time
TestLatency {
    test_health_endpoint_under_200ms(client) {
        start = high_resolution_timer()     // see stack concepts
        resp = client.GET("<health endpoint path>")
        elapsed_ms = (high_resolution_timer() - start) * 1000
        assert resp.status == 200
        assert elapsed_ms < 200, "Health took {elapsed_ms}ms (limit: 200ms)"
    }
}
```

## Step 5 — Organize
Place load tests in the performance test file (see test file mapping in project config).

## Step 6 — Verify
Run the test command (see project config) — full suite still passes.

## Rules
- Performance tests MUST be deterministic — no flaky assertions based on timing
- Use a high-resolution timer (see stack concepts) for measurements
- Thread pool tests verify no 500 errors, not specific timing
- Rapid state change tests verify final state consistency