---
name: performance-benchmark
description: |
  Comprehensive performance testing framework for load testing, stress testing, and benchmarking.
  Measures throughput, latency percentiles (p50, p95, p99), and resource utilization. Identifies
  bottlenecks and detects performance regressions across releases.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
compatibility:
  claude-code: ">=1.0.0"
metadata:
  version: "1.0.0"
  author: "QuantQuiver AI R&D"
  category: "testing"
  tags:
    - performance
    - load-testing
    - stress-testing
    - benchmarking
    - latency
---

# Performance Benchmark Suite

## Purpose

Comprehensive performance testing framework for load testing, stress testing, and benchmarking. Measures throughput, latency percentiles, and resource utilization. Identifies bottlenecks and detects performance regressions.

## Triggers

Use this skill when:

- "load test"
- "benchmark"
- "performance test"
- "stress test"
- "profile this code"
- "find performance bottlenecks"
- "measure latency"
- "check for performance regression"

## When to Use

- Pre-production performance validation
- Capacity planning
- SLA verification
- Release comparison
- Cost optimization
- Latency-sensitive applications

## When NOT to Use

- Functional testing (use unit-test-generator)
- Security testing (use security-test-suite)
- Data quality validation (use data-validation)

---

## Core Instructions

### Performance Test Types

| Type | Purpose | Duration | Load Pattern |
| ---- | ------- | -------- | ------------ |
| **Baseline** | Reference metrics | Minutes | Constant |
| **Load Test** | Normal capacity | Minutes | Constant |
| **Stress Test** | Breaking point | Minutes | Ramp-up |
| **Spike Test** | Burst handling | Minutes | Sudden bursts |
| **Soak Test** | Memory leaks | Hours | Constant |

### Metrics Collected

| Metric | Description | Target |
| ------ | ----------- | ------ |
| **Throughput** | Requests per second | Maximize |
| **Latency (p50)** | Median response time | Minimize |
| **Latency (p95)** | 95th percentile | < SLA |
| **Latency (p99)** | 99th percentile | < SLA |
| **Error Rate** | Failed requests | < 0.1% |
| **CPU Usage** | Processor utilization | < 80% |
| **Memory** | RAM consumption | Stable |

### Test Scenarios

```yaml
scenarios:
  baseline:
    rps: 100
    duration: 300s

  load_test:
    stages:
      - duration: 60s
        target_rps: 100
      - duration: 300s
        target_rps: 500
      - duration: 60s
        target_rps: 100

  stress_test:
    start_rps: 100
    step_rps: 50
    step_duration: 60s
    stop_on_error_rate: 5.0
```

---

## Templates

### Performance Report

```markdown
# Performance Benchmark Report

**Target:** {target_url}
**Generated:** {timestamp}

## Executive Summary

| Metric | Value |
| ------ | ----- |
| Total Requests | {total_requests} |
| Best Throughput | {best_rps} RPS |
| Worst p99 Latency | {worst_p99}ms |

## {test_name}

**Duration:** {duration}s
**Throughput:** {rps} RPS
**Error Rate:** {error_rate}%

### Latency Distribution

| Percentile | Latency (ms) |
| ---------- | ------------ |
| p50 | {p50} |
| p95 | {p95} |
| p99 | {p99} |
| Max | {max} |

### Threshold Violations

- {violation_description}

## Recommendations

- {recommendation}
```

---

## Example

**Input**: Load test REST API endpoint

**Output**:

```markdown
## Executive Summary

**Overall Status:** PASSED

| Metric | Value |
| ------ | ----- |
| Total Requests | 45,230 |
| Best Throughput | 523.4 RPS |
| Worst p99 Latency | 187.3ms |

## Baseline Test

**Throughput:** 100.0 RPS
**Error Rate:** 0.03%

### Latency Distribution

| Percentile | Latency (ms) |
| ---------- | ------------ |
| p50 | 23.4 |
| p95 | 67.8 |
| p99 | 98.2 |
```

---

## Validation Checklist

- [ ] System under test is isolated
- [ ] Warmup period completed before measurement
- [ ] Sufficient test duration for statistical significance
- [ ] Resource monitoring data collected
- [ ] Baseline comparison performed (if available)
- [ ] All threshold violations documented
- [ ] Recommendations actionable and specific

---

## Related Skills

- `unit-test-generator` - For function-level testing
- `api-contract-validator` - For API correctness
- `test-health-monitor` - For tracking performance trends
