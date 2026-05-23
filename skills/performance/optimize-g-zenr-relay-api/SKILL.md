---
name: optimize
description: Profile and optimize code for performance — identify bottlenecks and fix them
disable-model-invocation: true
---

Optimize: $ARGUMENTS

## Step 1 — Baseline Measurement
Before optimizing, run the test command (see project config) to ensure tests pass.

Identify what to measure:
- **Endpoint latency**: Time from request to response
- **Throughput**: Requests per second under load
- **Memory**: Per-request memory allocation
- **Lock contention**: Time spent waiting on locks

## Step 2 — Profile
Read the code and identify potential bottlenecks:

### Common bottlenecks:
- **Lock contention** in the service class — are locks held too long?
- **External resource communication** — is it blocking other requests?
- **Middleware overhead** — rate limiter checking on every request
- **Schema serialization** — model validation on large response lists
- **Logging** — synchronous logging in hot paths

### Static analysis checklist:
- [ ] Lock scope is minimal (acquire late, release early)
- [ ] No I/O operations inside lock
- [ ] No unnecessary object creation in hot paths
- [ ] Middleware short-circuits early for exempt paths
- [ ] List comprehensions instead of loops where applicable

## Step 3 — Optimize (targeted fixes only)
For each bottleneck identified:
1. Write a benchmark test that demonstrates the issue
2. Implement the fix
3. Re-run the benchmark to verify improvement
4. Run full test suite to verify no regressions

### Optimization principles:
- Measure before and after — no blind optimization
- Optimize the bottleneck, not everything
- Prefer algorithmic improvements over micro-optimizations
- Never sacrifice readability for negligible performance gains
- Never sacrifice thread safety for performance

## Step 4 — Verify
Run the test and type-check commands (see project config).
All tests MUST still pass. No type errors. No regressions.

## Step 5 — Document
- Comment any non-obvious optimization with rationale
- Update performance-sensitive code with complexity notes if applicable