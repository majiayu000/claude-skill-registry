---
name: performance-capacity
description: Plan, diagnose, and verify performance budgets, latency targets, load tests, capacity estimates, bottleneck analysis, caching strategy, query efficiency, queue throughput, and regression gates. Use when a feature may be slow, a system must scale, a performance regression is suspected, or release readiness depends on throughput, cost, memory, CPU, or response time.
---

# Performance Capacity

## Purpose

Use this skill to make performance measurable before optimizing. It turns vague "make it faster" work into budgets, probes, bottleneck hypotheses, and regression gates.

## Baseline First

Before changing code, capture:

1. User-facing operation or background job under test.
2. Current p50/p95/p99 latency or throughput.
3. Data size and concurrency assumptions.
4. Resource limits: CPU, memory, IO, network, database, queue.
5. Existing cache behavior and invalidation rules.
6. Cost or quota constraints.

If no baseline can be gathered, state the nearest measurable proxy and its limitations.

## Budget Design

Define budgets by surface:

| Surface | Examples |
|---|---|
| UI | TTI, interaction latency, bundle size, render count |
| API | p95 latency, error rate, DB query count, payload size |
| Jobs | throughput, max lag, retry cost, idempotency |
| Data | query plan, index coverage, backfill duration |
| Infra | CPU/RSS, concurrency, autoscaling, cost per request |

## Optimization Rules

- Optimize the measured bottleneck, not the most familiar code.
- Prefer algorithmic, query, batching, and cache correctness fixes before capacity-only fixes.
- Define cache invalidation and stale-data tolerance.
- Add a regression test, benchmark, or dashboard check for risky paths.
- Do not trade correctness, authorization, or tenant isolation for speed.

## Output Shape

```text
operation:
baseline:
target_budget:
bottleneck_hypothesis:
measurement_plan:
optimization_options:
capacity_estimate:
regression_gate:
verification_commands:
```
