---
name: performance-testing-patterns
description: "Performance testing methodology: load/stress/endurance testing, Core Web Vitals targets, system-level performance budgets, and statistical analysis. Use when writing performance tests, assessing performance test coverage, or designing systems with performance SLOs. Do NOT use for code-level performance review (algorithmic complexity, memory leaks) -- that is performance-reviewer's domain. Do NOT use for API endpoint-level thresholds -- that is api-testing-patterns' domain."
durability: encoded-preference
---

# Performance Testing Patterns

## Scope

This skill covers performance TESTING methodology -- how to measure, validate, and gate performance at the system level. For code-level performance issues (algorithmic complexity, memory leaks, rendering, bundle size), see `performance-reviewer`. For API endpoint-level thresholds (p95 response time, error rate per endpoint), see `api-testing-patterns`.

## When to Use Each Test Type

- **Load test** every release that has performance SLAs
- **Stress test** before capacity planning decisions -- find the breaking point
- **Endurance (soak) test** before major releases and after architecture changes -- detect memory leaks and degradation
- **Spike test** systems with unpredictable traffic patterns -- validate burst handling
- **Scalability test** before auto-scaling configuration -- measure performance delta as resources scale

## Core Web Vitals

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| INP (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |

Measure at the 75th percentile of page loads, segmented by device type.

## System-Level Performance Budgets

Define as CI/CD quality gates:

- **Bundle size budget**: maximum JS/CSS payload per route
- **Load capacity budget**: minimum traffic multiplier the system must handle (starting point: 3x normal peak)
- **Page load budget**: maximum time to interactive (starting point: LCP target above)

Budgets are project-specific. The values above are starting points for discussion, not mandates. For API endpoint-level thresholds (p95 latency, error rate), see `api-testing-patterns`.

## Statistical Rigor

- Establish baseline performance BEFORE optimization
- Use percentiles (p50, p95, p99), not averages
- Require confidence intervals for performance claims (minimum 95% CI)
- Always compare before/after with the same test conditions
- Run tests long enough for statistical significance (minimum 5 minutes sustained load)
- Account for warm-up effects -- exclude initial ramp-up from measurements

## RUM vs Synthetic Testing

Use both: synthetic for gatekeeping, RUM for truth.

- **Synthetic** (lab): CI/CD gates, regression detection, SLA validation
- **RUM** (field): Real-world performance, device/network variance

## Performance Test Coverage Assessment

When reviewing test coverage, check:

- Are critical user journeys covered by load tests?
- Do performance tests run in CI/CD (not just manually)?
- Are thresholds defined and enforced (not just measured)?
- Is there endurance testing for long-running services?
- Are performance baselines documented and tracked over time?
