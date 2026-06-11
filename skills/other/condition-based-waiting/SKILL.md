---
name: condition-based-waiting
description: "Polling, retry, and backoff patterns."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - "exponential backoff"
    - "health check polling"
    - "retry pattern"
    - "wait for"
    - "keep trying until"
    - "poll until ready"
    - "retry until success"
  category: process
  pairs_with:
    - shell-process-patterns
    - service-health-check
---

# Condition-Based Waiting

Implement condition-based polling and retry patterns with bounded timeouts, jitter, and error classification. Select the right pattern for the scenario, implement it with safety bounds, and verify both success and failure paths.

| Pattern | Use When | Key Safety Bound |
|---------|----------|-----------------|
| Simple Poll | Wait for condition to become true | Timeout + min poll interval |
| Exponential Backoff | Retry with increasing delays | Max retries + jitter + delay cap |
| Rate Limit Recovery | API returns 429 | Retry-After header + default fallback |
| Health Check | Wait for service(s) to be ready | All-pass requirement + per-check status |
| Circuit Breaker | Prevent cascade failures | Failure threshold + recovery timeout |

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| reviewing wait/retry code for polling, retry, and backoff mistakes | `preferred-patterns.md` | Loads detailed guidance from `preferred-patterns.md`. |
| writing wait code: polling, exponential backoff, rate-limit recovery, health checks, circuit breaker | `implementation-patterns.md` | Loads detailed guidance from `implementation-patterns.md`. |
| tests, implementation patterns | `testing-patterns.md` | Loads detailed guidance from `testing-patterns.md`. |

## Instructions

Before implementing any pattern, read the repository CLAUDE.md and search the codebase for existing wait/retry patterns to maintain consistency with what already exists.

### Step 1: Select the Pattern

Walk this decision tree to pick the right pattern. Only implement the pattern directly needed -- do not add circuit breakers when simple retries suffice, and do not add health checks when a single poll works.

```
1. Waiting for a condition to become true?
   YES -> Simple Polling (Step 2)
   NO  -> Continue

2. Retrying a failing operation?
   YES -> Rate-limited (429)?
         YES -> Rate Limit Recovery (Step 5)
         NO  -> Exponential Backoff (Step 4)
   NO  -> Continue

3. Waiting for a service to start?
   YES -> Health Check Waiting (Step 6)
   NO  -> Continue

4. Service frequently failing, need fast-fail?
   YES -> Circuit Breaker (Step 7)
   NO  -> Simple Poll or Backoff
```

### Step 2: Implement Simple Polling

Wait for a condition to become true with bounded timeout.

1. Define the condition function (returns truthy when ready).
2. Set timeout and poll interval based on target type. Use `time.monotonic()` for elapsed time measurement -- never `time.time()`, which drifts with clock adjustments.

| Target Type | Min Interval | Typical Interval | Example |
|-------------|-------------|-----------------|---------|
| In-process state | 10ms | 50-100ms | Flag, queue, state machine |
| Local file/socket | 100ms | 500ms | File exists, port open |
| Local service | 500ms | 1-2s | Database, cache |
| Remote API | 1s | 5-10s | HTTP endpoint, cloud service |

Never busy-wait (tight loop with no sleep). The minimum poll interval is 10ms for local operations, 100ms for external services. Tighter loops burn CPU, cause thermal throttling, and starve other processes.

3. Implement with a mandatory timeout. Every wait loop must have a maximum timeout to prevent infinite hangs. The timeout error message must include what was waited for and the last observed state so the caller can diagnose failures.

```python
# Core pattern (full implementation in references/implementation-patterns.md)
start = time.monotonic()
deadline = start + timeout_seconds
while time.monotonic() < deadline:
    result = condition()
    if result:
        return result
    time.sleep(poll_interval)
raise TimeoutError(f"Timeout waiting for: {description}")
```

4. Report wait progress with timeout values and retry counts during the wait. Cancel pending operations when the timeout expires.
5. Test with both success and timeout scenarios. Force the condition to never become true and confirm TimeoutError fires with a descriptive message.

### Step 3: Verify Before Proceeding

After implementing any pattern from Steps 2-7, verify:
- Success path works as expected
- Failure/timeout path produces a descriptive error
- Logging captures each attempt with failure reason and attempt number
- No arbitrary sleep values remain (replace `sleep(N)` with condition-based polling)

### Step 4: Implement Exponential Backoff

Retry failing operations with increasing delays and jitter.

1. Classify errors before implementing retries. Separate transient from permanent errors -- retrying permanent errors wastes time and quota.
   - **Retryable**: 408, 429, 500, 502, 503, 504, network timeouts, connection refused
   - **Non-retryable**: 400, 401, 403, 404, validation errors, auth failures

2. Configure backoff parameters. Every retry loop must have a maximum retry count.
   - `max_retries`: 3-5 for APIs, 5-10 for infrastructure
   - `initial_delay`: 0.5-2s
   - `max_delay`: 30-60s
   - `jitter_range`: 0.5 (adds +/-50% randomness)

3. Implement with jitter. Jitter is mandatory on all exponential backoff -- without it, all clients retry at the same instant after an outage (thundering herd), amplifying the load spike that caused the failure.

```python
# Core pattern (full implementation in references/implementation-patterns.md)
for attempt in range(max_retries + 1):
    try:
        return operation()
    except retryable_exceptions as e:
        if attempt >= max_retries:
            raise
        jitter = 1.0 + random.uniform(-0.5, 0.5)
        actual_delay = min(delay * jitter, max_delay)
        time.sleep(actual_delay)
        delay = min(delay * backoff_factor, max_delay)
```

4. Log each retry attempt with the failure reason and attempt number. Verify retry behavior with forced failures.

### Step 5: Implement Rate Limit Recovery

Handle HTTP 429 responses using Retry-After headers.

1. Detect 429 status code in response.
2. Parse `Retry-After` header (seconds or HTTP-date format).
3. Wait the specified duration, then retry.
4. Fall back to default wait (60s) if header missing.

See `references/implementation-patterns.md` for full `RateLimitedClient` class.

### Step 6: Implement Health Check Waiting

Wait for services to become healthy before proceeding.

1. Define health checks by type:

| Type | Check | Example |
|------|-------|---------|
| TCP | Port accepting connections | `localhost:5432` |
| HTTP | Endpoint returns 2xx | `http://localhost:8080/health` |
| Command | Exit code 0 | `pgrep -f 'celery worker'` |

2. Set appropriate timeouts (services often need 30-120s to start). Use poll intervals from the target type table in Step 2.
3. Poll all checks, succeed only when ALL pass. Report status of each check during waiting so the caller can see which service is lagging.

See `references/implementation-patterns.md` for full `wait_for_healthy()` implementation.

### Step 7: Implement Circuit Breaker

Prevent cascade failures by failing fast after repeated errors.

1. Configure thresholds:
   - `failure_threshold`: Number of failures before opening (typically 5)
   - `recovery_timeout`: Time before testing recovery (typically 30s)
   - `half_open_max_calls`: Successful calls needed to close (typically 3)

2. Implement state machine:
   - CLOSED: Normal operation, count failures
   - OPEN: Reject immediately, wait for recovery timeout
   - HALF_OPEN: Allow test calls, close on success streak

3. Add fallback behavior for OPEN state.
4. Test all state transitions:

```
CLOSED --(failure_threshold reached)--> OPEN
OPEN   --(recovery_timeout elapsed)---> HALF_OPEN
HALF_OPEN --(success streak)----------> CLOSED
HALF_OPEN --(any failure)-------------> OPEN
```

See `references/implementation-patterns.md` for full `CircuitBreaker` class.

### Examples

**Flaky test with sleep()**: User says "This test uses sleep(5) and sometimes fails in CI." Identify as Simple Polling (Step 2). Define what the test is actually waiting for, replace `sleep(5)` with `wait_for(condition, description, timeout=30)`, run test 3 times to verify reliability, then force the condition to never be true and confirm TimeoutError.

**API integration with rate limits**: User says "Our batch job hits 429 errors from the API." Classify errors: 429 is retryable, 400/401/404 are not (Step 4). Add Retry-After header parsing with 60s default fallback (Step 5). Add exponential backoff with jitter for non-429 transient errors (Step 4). Test: normal flow, 429 handling, exhausted retries, non-retryable errors.

**Service startup in Docker Compose**: User says "App crashes because it starts before the database is ready." Define checks: TCP on postgres:5432, HTTP on api:8080/health (Step 6). Set 120s timeout with 2s poll interval. Implement wait_for_healthy() with all-pass requirement. Verify: services start within timeout, timeout fires when service is down.

## Error Handling

### Error: "Timeout expired before condition met"
Cause: Condition never became true within timeout window.
Solution:
1. Verify condition function logic is correct
2. Increase timeout if operation legitimately needs more time
3. Add logging inside condition to observe state changes
4. Check for deadlocks or blocked resources

### Error: "All retries exhausted"
Cause: Operation failed on every attempt including retries.
Solution:
1. Distinguish transient from permanent errors in retryable_exceptions
2. Verify external service is actually reachable
3. Check if authentication/configuration is correct
4. Increase max_retries only if error is genuinely transient

### Error: "Circuit breaker open"
Cause: Failure threshold exceeded, circuit rejecting calls.
Solution:
1. Investigate why underlying service is failing
2. Implement fallback behavior for CircuitOpenError
3. Wait for recovery_timeout to elapse before testing
4. Consider adjusting failure_threshold for known-flaky services

## References

### Loading Table

| Task Type | Signal Keywords | Load |
|-----------|----------------|------|
| Implementing any pattern | "implement", "add retry", "write polling", "create backoff" | `implementation-patterns.md` |
| Reviewing existing code | "review", "check for", "find issues", "audit", "detect" | `preferred-patterns.md` |
| Replacing `sleep()` in tests | "sleep", "flaky test", "CI hang", "test timeout" | `preferred-patterns.md` |
| Writing tests for retry/wait code | "test", "pytest", "mock", "verify retry", "unit test" | `testing-patterns.md` |

### Reference Files
- `${CLAUDE_SKILL_DIR}/references/implementation-patterns.md`: Complete Python/Bash implementations for all patterns
- `${CLAUDE_SKILL_DIR}/references/preferred-patterns.md`: Detection commands and fixes for common wait/retry mistakes
- `${CLAUDE_SKILL_DIR}/references/testing-patterns.md`: pytest patterns for testing polling, backoff, and circuit breaker code
