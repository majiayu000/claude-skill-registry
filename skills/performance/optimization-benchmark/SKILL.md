---
name: optimization-benchmark
description: Comprehensive performance benchmarking, regression detection, automated testing, and performance validation. Use for CI/CD quality gates, baseline comparisons, and systematic performance testing.
---

# Benchmark Suite Skill

## Overview

This skill provides comprehensive automated performance testing capabilities including benchmark execution, regression detection, performance validation, and quality assessment for ensuring optimal system performance.

## When to Use

- Running performance benchmark suites before deployment
- Detecting performance regressions between versions
- Validating SLA compliance through automated testing
- Load, stress, and endurance testing
- CI/CD pipeline performance quality gates
- Comparing performance across configurations

## Quick Start

```bash
# Run comprehensive benchmark suite
npx claude-flow benchmark-run --suite comprehensive --duration 300

# Execute specific benchmark
npx claude-flow benchmark-run --suite throughput --iterations 10

# Compare with baseline
npx claude-flow benchmark-compare --current <results> --baseline <baseline>

# Quality assessment
npx claude-flow quality-assess --target swarm-performance --criteria throughput,latency

# Performance validation
npx claude-flow validate-performance --results <file> --criteria <file>
```

## Architecture

```
+-----------------------------------------------------------+
|                   Benchmark Suite                          |
+-----------------------------------------------------------+
|  Benchmark Runner  |  Regression Detector  |  Validator   |
+--------------------+-----------------------+--------------+
         |                     |                    |
         v                     v                    v
+------------------+  +-------------------+  +--------------+
| Benchmark Types  |  | Detection Methods |  | Validation   |
| - Throughput     |  | - Statistical     |  | - SLA        |
| - Latency        |  | - ML-based        |  | - Regression |
| - Scalability    |  | - Threshold       |  | - Scalability|
| - Coordination   |  | - Trend Analysis  |  | - Reliability|
+------------------+  +-------------------+  +--------------+
         |                     |                    |
         v                     v                    v
+-----------------------------------------------------------+
|              Reporter & Comparator                         |
+-----------------------------------------------------------+
```

## Benchmark Types

### Standard Benchmarks

| Benchmark | Metrics | Duration | Targets |
|-----------|---------|----------|---------|
| Throughput | requests/sec, tasks/sec, messages/sec | 5 min | min: 1000, optimal: 5000 |
| Latency | p50, p90, p95, p99, max | 5 min | p50<100ms, p99<1s |
| Scalability | linear coefficient, efficiency retention | variable | coefficient>0.8 |
| Coordination | message latency, sync time | 5 min | <50ms |
| Fault Tolerance | recovery time, failover success | 10 min | <30s recovery |

### Test Campaign Types

1. **Load Testing**: Gradual ramp-up to sustained load
2. **Stress Testing**: Find breaking points
3. **Volume Testing**: Large data set handling
4. **Endurance Testing**: Long-duration stability
5. **Spike Testing**: Sudden load changes
6. **Configuration Testing**: Different settings comparison

## Core Capabilities

### 1. Comprehensive Benchmarking

```javascript
// Run benchmark suite
const results = await benchmarkSuite.run({
  duration: 300000,      // 5 minutes
  iterations: 10,        // 10 iterations
  warmupTime: 30000,     // 30 seconds warmup
  cooldownTime: 10000,   // 10 seconds cooldown
  parallel: false,       // Sequential execution
  baseline: previousRun  // Compare with baseline
});

// Results include:
// - summary: Overall scores and status
// - detailed: Per-benchmark results
// - baseline_comparison: Delta from baseline
// - recommendations: Optimization suggestions
```

### 2. Regression Detection

Multi-algorithm detection:

| Method | Description | Use Case |
|--------|-------------|----------|
| Statistical | CUSUM change point detection | Detect gradual degradation |
| Machine Learning | Anomaly detection models | Identify unusual patterns |
| Threshold | Fixed limit comparisons | Hard performance limits |
| Trend | Time series regression | Long-term degradation |

```bash
# Detect performance regressions
npx claude-flow detect-regression --current <results> --historical <data>

# Set up automated regression monitoring
npx claude-flow regression-monitor --enable --sensitivity 0.95
```

### 3. Automated Performance Testing

```javascript
// Execute test campaign
const campaign = await tester.runTestCampaign({
  tests: [
    { type: 'load', config: loadTestConfig },
    { type: 'stress', config: stressTestConfig },
    { type: 'endurance', config: enduranceConfig }
  ],
  constraints: {
    maxDuration: 3600000,  // 1 hour max
    failFast: true         // Stop on first failure
  }
});
```

### 4. Performance Validation

Validation framework with multi-criteria assessment:

| Validation Type | Criteria |
|-----------------|----------|
| SLA Validation | Availability, response time, throughput, error rate |
| Regression Validation | Comparison with historical data |
| Scalability Validation | Linear scaling, efficiency retention |
| Reliability Validation | Error handling, recovery, consistency |

## MCP Integration

```javascript
// Comprehensive benchmark integration
const benchmarkIntegration = {
  // Execute performance benchmarks
  async runBenchmarks(config = {}) {
    const [benchmark, metrics, trends, cost] = await Promise.all([
      mcp.benchmark_run({ suite: config.suite || 'comprehensive' }),
      mcp.metrics_collect({ components: ['system', 'agents', 'coordination'] }),
      mcp.trend_analysis({ metric: 'performance', period: '24h' }),
      mcp.cost_analysis({ timeframe: '24h' })
    ]);

    return { benchmark, metrics, trends, cost, timestamp: Date.now() };
  },

  // Quality assessment
  async assessQuality(criteria) {
    return await mcp.quality_assess({
      target: 'swarm-performance',
      criteria: criteria || ['throughput', 'latency', 'reliability', 'scalability']
    });
  }
};
```

## Key Metrics

### Benchmark Targets

```javascript
const benchmarkTargets = {
  throughput: {
    requests_per_second: { min: 1000, optimal: 5000 },
    tasks_per_second: { min: 100, optimal: 500 },
    messages_per_second: { min: 10000, optimal: 50000 }
  },
  latency: {
    p50: { max: 100 },   // 100ms
    p90: { max: 200 },   // 200ms
    p95: { max: 500 },   // 500ms
    p99: { max: 1000 },  // 1s
    max: { max: 5000 }   // 5s
  },
  scalability: {
    linear_coefficient: { min: 0.8 },
    efficiency_retention: { min: 0.7 }
  }
};
```

### CI/CD Quality Gates

| Gate | Criteria | Action on Failure |
|------|----------|-------------------|
| Performance | < 10% degradation | Block deployment |
| Latency | p99 < 1s | Warning |
| Error Rate | < 0.5% | Block deployment |
| Scalability | > 80% linear | Warning |

## Load Testing Example

```javascript
// Load test with gradual ramp-up
const loadTest = {
  type: 'load',
  phases: [
    { phase: 'ramp-up', duration: 60000, startLoad: 10, endLoad: 100 },
    { phase: 'sustained', duration: 300000, load: 100 },
    { phase: 'ramp-down', duration: 30000, startLoad: 100, endLoad: 0 }
  ],
  successCriteria: {
    p99_latency: { max: 1000 },
    error_rate: { max: 0.01 },
    throughput: { min: 80 }  // % of expected
  }
};
```

## Stress Testing Example

```javascript
// Stress test to find breaking point
const stressTest = {
  type: 'stress',
  startLoad: 100,
  maxLoad: 10000,
  loadIncrement: 100,
  duration: 60000,  // Per load level
  breakingCriteria: {
    error_rate: { max: 0.05 },    // 5% errors
    latency_p99: { max: 5000 },   // 5s latency
    timeout_rate: { max: 0.10 }   // 10% timeouts
  }
};
```

## Integration Points

| Integration | Purpose |
|-------------|---------|
| Performance Monitor | Continuous monitoring data for benchmarking |
| Load Balancer | Validates load balancing effectiveness |
| Topology Optimizer | Tests topology configurations |
| CI/CD Pipeline | Automated quality gates |

## Best Practices

1. **Consistent Environment**: Run benchmarks in consistent, isolated environments
2. **Warmup Period**: Always include warmup to eliminate cold-start effects
3. **Multiple Iterations**: Run multiple iterations for statistical significance
4. **Baseline Maintenance**: Keep baseline updated with expected performance
5. **Historical Tracking**: Store all benchmark results for trend analysis
6. **Realistic Workloads**: Use production-like workload patterns

## Example: CI/CD Integration

```bash
#!/bin/bash
# ci-performance-gate.sh

# Run benchmark suite
RESULTS=$(npx claude-flow benchmark-run --suite quick --output json)

# Compare with baseline
COMPARISON=$(npx claude-flow benchmark-compare \
  --current "$RESULTS" \
  --baseline ./baseline.json)

# Check for regressions
if echo "$COMPARISON" | jq -e '.regression_detected == true' > /dev/null; then
  echo "Performance regression detected!"
  echo "$COMPARISON" | jq '.regressions'
  exit 1
fi

echo "Performance validation passed"
exit 0
```

## Related Skills

- `optimization-monitor` - Real-time performance monitoring
- `optimization-analyzer` - Bottleneck analysis and reporting
- `optimization-load-balancer` - Load distribution optimization
- `optimization-topology` - Topology performance testing

---

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from benchmark-suite agent with comprehensive benchmarking, regression detection, automated testing, and performance validation
