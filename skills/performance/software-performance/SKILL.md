---
name: software-performance
description: "Systematic profiling, load testing, performance budgets, and regression prevention. Use when diagnosing slow services, benchmarking systems, or preventing regressions."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Performance Engineering

Use this skill for systematic performance work across APIs, web apps, services, and release gates. It owns profiling, load and stress testing, performance budgets, and regression detection. It does not replace SQL tuning, observability setup, or system-architecture design.

## Quick Reference

| Task | Use |
|------|-----|
| Profiling hot paths | flamegraph-first profiling with the right language toolchain |
| Load and stress testing | k6 by default; alternate tools only when the team has a clear reason |
| Frontend or backend budgets | CI thresholds plus representative benchmarks |
| Database-related slowdown | query and pool investigation first, then broader system review |
| Continuous regression detection | benchmark suites plus statistical comparison |
| CWV thresholds, k6 patterns, Lighthouse CI budget JSON, profiling tools | [references/perf-budgets-and-cwv.md](references/perf-budgets-and-cwv.md) | LCP/INP/CLS, pprof, dotnet-counters, Instruments |
| assert CWV budgets from Lighthouse JSON | [scripts/check_perf_budget.py](scripts/check_perf_budget.py) | exits non-zero on breach |

## When to Use

- Diagnose slow API responses, page loads, or jobs.
- Design and run load, stress, soak, or spike tests.
- Set and enforce performance budgets.
- Find CPU, memory, or I/O bottlenecks.
- Plan capacity or benchmark architectural changes.
- Catch regressions before they reach production.

## Route Elsewhere

- SQL query tuning and indexing: use [data-sql-optimization](../data-sql-optimization/SKILL.md).
- System architecture and scaling design: use [software-architecture-design](../software-architecture-design/SKILL.md).
- Frontend build-tool setup: use [software-frontend](../software-frontend/SKILL.md).
- Observability and telemetry setup: use [qa-observability](../qa-observability/SKILL.md).
- Resilience patterns such as retries and breakers: use [qa-resilience](../qa-resilience/SKILL.md).
- Mobile-specific performance: use [software-mobile](../software-mobile/SKILL.md).

## Defaults

- Measure before you optimize.
- Flamegraphs first for CPU questions.
- Benchmark before and after every claimed fix.
- Prefer realistic load patterns over synthetic vanity numbers.
- Gate regressions in CI where practical.
- Treat tool comparisons and best-tool claims as time-sensitive.

### When NOT to Optimize

- The path is not on a measured critical path for users or cost (e.g., a report run 3x/week is not worth a profiling sprint that a checkout endpoint would be).
- The gain is real but below the noise floor of your measurement (see benchmark-variance guidance below) — you cannot prove it shipped.
- The fix trades a rare but catastrophic failure mode (e.g., removing a safety timeout) for average-case speed.
- The team cannot commit to re-measuring after the change — an unverified "optimization" is a liability, not a win.
- Business impact of the current latency is unclear — ship the instrumentation to find out before shipping the fix.

### Common Misdiagnoses

- **Blaming GC for lock contention.** Long "stop-the-world"-looking pauses under load are just as often mutex/monitor contention, thread-pool starvation, or connection-pool waits as they are garbage collection. Distinguish with a lock-aware profile (JFR lock events, Go's mutex/block profiler, or async-profiler's native lock detection added in v4.3) before tuning heap or GC flags.
- **Blaming the database for N+1s that are actually application-side serialization.** A flamegraph showing time "in the DB driver" can mean waiting on the network, not waiting on the query — check whether requests are sequential when they could be batched or parallelized.
- **Blaming cold cache for a regression that is actually a new synchronous call in the hot path.** Warm the cache and re-test before concluding the cache is the fix.
- **Blaming "the network" for tail latency that is actually queueing.** A rising p99 with a flat p50 under increasing load is frequently a queueing/concurrency-limit signal (see Little's Law below), not a network problem.

### Capacity and Concurrency Math (Little's Law)

Little's Law relates concurrency, throughput, and latency: `L = λ × W` (average number in the system = arrival rate × average time in the system). Use it to sanity-check load-test configuration and capacity plans before trusting a result.

Worked example: target throughput λ = 500 req/s, average request latency W = 300 ms = 0.3 s. Required steady-state concurrency: `L = 500 × 0.3 = 150` requests in flight. If a k6 script is configured with only 50 VUs and no sleep, the achievable throughput is capped at `L / W = 50 / 0.3 ≈ 166.7 req/s` — the test will report clean p95s and "pass," but it never exercised the 500 req/s target and the result is a false negative on capacity. Always check `VUs ≥ target_rps × expected_latency_s` before trusting a load test's headline throughput.

The same relation explains connection-pool exhaustion: if a pool has 20 connections and each query holds a connection for 50 ms, the pool saturates at `20 / 0.05 = 400 req/s` regardless of CPU headroom — no amount of caching or CPU optimization above the app layer will raise that ceiling.

### Diminishing Returns on Parallelism (Amdahl's Law)

Amdahl's Law bounds the speedup from adding parallelism: `speedup = 1 / (s + (1 − s) / N)`, where `s` is the serial (non-parallelizable) fraction and `N` is the number of workers/cores. Worked example: if profiling shows 20% of a job's time is inherently serial (`s = 0.2`), the maximum speedup as `N → ∞` is `1 / 0.2 = 5×` — no matter how many workers you add. Before recommending "add more workers/threads/pods," measure the serial fraction (locks, single-writer steps, shared queues); if it is already the bottleneck, the fix is architectural (remove the serial section), not more parallelism.

## Workflow

1. Define the symptom, target metric, traffic shape, and acceptance threshold.
2. Choose the investigation path: latency, page load, scale behavior, memory growth, or cost efficiency.
3. Measure a baseline with the smallest tool that exposes the bottleneck.
4. Make the smallest change that addresses the measured constraint.
5. Benchmark before and after, then decide whether the change is worth shipping.

## ASCII Flow

```text
Performance task
  -> Define user-visible symptom and success budget
  -> Reproduce with controlled load, trace, or profile
  -> Locate bottleneck in CPU, memory, I/O, network, DB, or rendering
  -> Apply the smallest proven fix
  -> Re-measure with the same method
  -> Add regression guardrail and report tradeoffs
```

## Core Decisions

### Profiling Sequence

- [ ] Reproduce the problem under a production-like build and dataset
- [ ] Capture a profile (flamegraph for CPU, heap snapshot for memory)
- [ ] Identify the hot path — do not guess from code reading alone
- [ ] Fix the specific bottleneck; resist adjacent cleanups in the same change
- [ ] Verify the metric moved by re-running the same profiling method

### Load Testing Scenarios

| Scenario | Use For | Pass/Fail Defined Before Run |
|----------|---------|------------------------------|
| Smoke | Correctness under low load | Yes — define before starting |
| Load | Expected production traffic | Yes |
| Stress | Breaking point | Yes |
| Soak | Long-duration degradation, memory leaks | Yes — time + heap trend |
| Spike | Sudden surge behavior | Yes |

### Budgets and Gates

| Surface | Metric | Gate |
|---------|--------|------|
| Frontend | LCP, INP, CLS, TBT, JS bundle size | Lighthouse CI assertions in PR pipeline |
| Backend | p95, p99 latency, error rate, startup time | k6 thresholds in CI smoke run |

Automated gates catch regressions before they reach production.

### Database and Pooling — Triage Order

1. Check slow-query logs and EXPLAIN plans first
2. Check indexes (missing or unused)
3. Check connection pool exhaustion (pool size vs concurrency)
4. Check N+1 patterns (query count per request under load)
5. Check lock contention

Add a cache only after ruling out the above. Caching an unindexed query shifts load; fixing the index eliminates it.

## Output Modes

Default to one of these:

- Performance diagnosis:
  suspected bottleneck, evidence, and next measurement step.
- Test plan:
  scenario, thresholds, tooling, and environment assumptions.
- Budget proposal:
  target metrics, CI gates, and exception policy.
- Regression review:
  before/after evidence, significance, and ship/no-ship recommendation.

## Known Traps

- Profiling a non-production-like build, dataset, or deployment shape and then optimizing for the wrong bottleneck.
- Reading one benchmark run as signal instead of checking variance, warmup effects, and environmental noise.
- Celebrating cache hit-rate gains while ignoring invalidation cost, stale data risk, or memory pressure.
- Running load tests against an environment that does not resemble production concurrency, latency, or dependency behavior.
- Improving the mean while p95 and p99 tails quietly worsen for the user path that actually matters.
- Reporting p95/p99 from a single service without accounting for fan-out amplification: if a request calls 10 downstream services each with a 1% chance of hitting their own p99, the caller's effective miss rate compounds toward `1 − (0.99)^10 ≈ 9.6%` — a healthy-looking per-service p99 does not imply a healthy end-to-end tail.
- Averaging or blending percentiles across nodes/instances (e.g., averaging each host's p99) instead of computing the percentile over the full merged sample — this systematically understates the true tail.

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|-------------|
| Premature optimization | Fixes the wrong bottleneck before measuring |
| Optimizing without before/after metrics | No way to confirm the change helped |
| Treating microbenchmarks as system proof | Ignores real load shape, concurrency, and infrastructure latency |
| Adding caches before understanding query behavior | Caching a missing index shifts load instead of eliminating it |
| Reading one benchmark run as meaningful | Single-run noise can be larger than the signal |
| Profiling debug builds | Debug builds have different hot paths and no compiler optimizations |

## Scenarios

### S1 — High LCP on a marketing page (field data alert)

CrUX reports LCP at 4.8s at the 75th percentile. Check TTFB first (if above 800ms, server-side fixes unblock everything else); then audit the LCP element for missing `fetchpriority="high"`, unoptimized image format, and missing explicit dimensions causing CLS. Add LHCI assertions on LCP and TBT before closing the ticket.

### S2 — API p95 regression after a release

Capture a CPU flamegraph under production-like load before bisecting code changes. Identify hot paths (JWT decode per request, N+1 queries, lock contention) and fix the smallest measured bottleneck first. Benchmark before and after each change with at least 5 runs; compare medians and p99s, not single-run results.

### S3 — Enforcing a performance budget on a React SPA

Define a `perf-budget.json` with LCP, INP, CLS, TBT, JS bytes, and Lighthouse score thresholds. Add Lighthouse CI to the PR pipeline with assertion blocks. Flag the JS bundle in the budget once it exceeds roughly 300kB gzipped initial load (300-350kB is a lenient ceiling; 150-250kB is the tighter target teams increasingly hold to on mobile); recommend route-based code splitting. Bundle-size guidance is hardware- and network-dependent and shifts over time — verify current community consensus before treating a specific kB figure as fixed. See [references/web-vitals-and-budgets.md](references/web-vitals-and-budgets.md) for budget templates.

### S4 — Load-testing a new service before launch

Write a k6 script with smoke, load, and stress stages. Define p95 and p99 latency thresholds and an error-rate threshold before running. Run the stress test against a staging environment that matches production concurrency, connection pool sizes, and downstream stub latency. Gate the CI pipeline on the smoke test; run load and stress as pre-launch gates only.

### S5 — Detecting a memory leak in a long-running Node.js service

Use a soak test (k6 or autocannon, 4-hour duration, steady load) and monitor heap growth over time. Capture heap snapshots at the start and after 2 hours; diff the allocation trees. Look for retained closures, growing caches without eviction, and event listeners not removed on request end. Confirm the fix by re-running the soak and showing flat heap growth.

## Navigation

- Related skills: [software-backend](../software-backend/SKILL.md), [software-frontend](../software-frontend/SKILL.md), [software-mobile](../software-mobile/SKILL.md), [data-sql-optimization](../data-sql-optimization/SKILL.md), [qa-observability](../qa-observability/SKILL.md), [ops-devops-platform](../ops-devops-platform/SKILL.md), [software-architecture-design](../software-architecture-design/SKILL.md)
- Source map: [data/sources.json](data/sources.json)
- Reference: [references/web-vitals-and-budgets.md](references/web-vitals-and-budgets.md)

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Tool rankings, profiler capabilities, APM comparisons, and current best-practice budget numbers are time-sensitive and should be verified against current primary sources before being presented as current fact.
- Use [data/sources.json](data/sources.json) as the source map for freshness checks.
- If live verification is unavailable, give stable methodology guidance and mark tooling claims as provisional.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

