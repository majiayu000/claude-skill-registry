---
name: optimization-analyzer
description: Performance bottleneck analysis, workflow inefficiency detection, pattern recognition, and optimization recommendations. Use for identifying performance issues, root cause analysis, and generating actionable improvement plans.
---

# Performance Analyzer Skill

## Overview

This skill specializes in identifying and resolving performance bottlenecks in development workflows, agent coordination, and system operations. It provides comprehensive analysis, pattern recognition, and actionable recommendations.

## When to Use

- Analyzing slow execution times in workflows
- Identifying resource constraints (CPU, memory, I/O)
- Detecting coordination overhead in agent systems
- Finding parallelization opportunities
- Root cause analysis for performance issues
- Generating optimization recommendations

## Quick Start

```bash
# Run bottleneck analysis
npx claude-flow bottleneck-analyze --component swarm-coordination

# Generate performance report
npx claude-flow performance-report --format detailed --timeframe 24h

# Collect metrics for analysis
npx claude-flow metrics-collect --components ["cpu", "memory", "network"]

# Trend analysis
npx claude-flow trend-analysis --metric performance --period 7d
```

## Architecture

```
+-----------------------------------------------------------+
|                  Performance Analyzer                      |
+-----------------------------------------------------------+
|  Data Collector  |  Pattern Analyzer  |  Recommender      |
+------------------+--------------------+-------------------+
         |                  |                    |
         v                  v                    v
+----------------+  +------------------+  +------------------+
| Metrics        |  | Bottleneck Types |  | Strategies       |
| - Execution    |  | - Execution Time |  | - Parallelization|
| - Resources    |  | - Resources      |  | - Reallocation   |
| - Dependencies |  | - Coordination   |  | - Algorithm      |
| - Communication|  | - Sequential     |  | - Caching        |
+----------------+  | - Data Transfer  |  | - Topology       |
                    +------------------+  +------------------+
         |                  |                    |
         v                  v                    v
+-----------------------------------------------------------+
|              Report Generator & Action Plan                |
+-----------------------------------------------------------+
```

## Bottleneck Types

| Type | Symptoms | Detection Method |
|------|----------|------------------|
| Execution Time | Tasks taking longer than expected | Timing analysis |
| Resource Constraints | CPU/memory/I/O at limits | Resource monitoring |
| Coordination Overhead | Inefficient agent communication | Message analysis |
| Sequential Blockers | Unnecessary serial execution | Dependency mapping |
| Data Transfer | Large payload movements | Network analysis |

## Analysis Workflow

### 1. Data Collection Phase

```javascript
// Comprehensive data collection
const dataCollection = {
  async collect(swarmId, duration = 60000) {
    const metrics = await Promise.all([
      this.gatherExecutionMetrics(swarmId),
      this.profileResourceUsage(swarmId),
      this.mapTaskDependencies(swarmId),
      this.traceCommunicationPatterns(swarmId),
      this.identifyHotspots(swarmId)
    ]);

    return {
      execution: metrics[0],
      resources: metrics[1],
      dependencies: metrics[2],
      communication: metrics[3],
      hotspots: metrics[4],
      timestamp: Date.now()
    };
  }
};
```

### 2. Analysis Phase

```javascript
// Multi-dimensional analysis
const analysis = {
  async analyze(data, baselines) {
    return {
      // Compare against baselines
      comparison: this.compareAgainstBaselines(data, baselines),

      // Identify anomalies
      anomalies: this.identifyAnomalies(data),

      // Correlate metrics
      correlations: this.correlateMetrics(data),

      // Determine root causes
      rootCauses: await this.determineRootCauses(data),

      // Prioritize issues
      prioritizedIssues: this.prioritizeIssues(data)
    };
  }
};
```

### 3. Recommendation Phase

```javascript
// Generate actionable recommendations
const recommendations = {
  async generate(analysis) {
    return {
      optimizations: this.generateOptimizationOptions(analysis),
      improvements: this.estimateImprovementPotential(analysis),
      effort: this.assessImplementationEffort(analysis),
      actionPlan: this.createActionPlan(analysis),
      successMetrics: this.defineSuccessMetrics(analysis)
    };
  }
};
```

## Common Bottleneck Patterns

### 1. Single Agent Overload

**Symptoms**: One agent handling complex tasks alone
**Detection**: Agent utilization > 90%, queue depth growing
**Solution**: Spawn specialized agents for parallel work
**Expected Improvement**: 40-60%

### 2. Sequential Task Chain

**Symptoms**: Tasks waiting unnecessarily
**Detection**: Low parallelization ratio, high wait times
**Solution**: Identify parallelization opportunities
**Expected Improvement**: 30-50%

### 3. Resource Starvation

**Symptoms**: Agents waiting for resources
**Detection**: Resource contention, lock waits
**Solution**: Increase limits or optimize usage
**Expected Improvement**: 20-40%

### 4. Communication Overhead

**Symptoms**: Excessive inter-agent messages
**Detection**: High message count, latency spikes
**Solution**: Batch operations or change topology
**Expected Improvement**: 25-45%

### 5. Inefficient Algorithms

**Symptoms**: High complexity operations
**Detection**: O(n^2) patterns, memory pressure
**Solution**: Algorithm optimization or caching
**Expected Improvement**: 50-80%

## Key Performance Indicators

| KPI | Description | Target |
|-----|-------------|--------|
| Task Execution Time | Average, P95, P99 | < baseline * 1.1 |
| Resource Utilization | CPU, Memory, I/O | 60-80% optimal |
| Parallelization Ratio | Parallel vs Sequential | > 0.7 |
| Agent Efficiency | Task throughput per agent | > baseline |
| Communication Latency | Message delays | < 50ms |

## MCP Integration

```javascript
// Performance analysis integration
const performanceIntegration = {
  // Comprehensive bottleneck analysis
  async analyzeBottlenecks(component = null) {
    const [bottlenecks, metrics, trends] = await Promise.all([
      mcp.bottleneck_analyze({ component }),
      mcp.metrics_collect({ components: ['system', 'agents', 'coordination'] }),
      mcp.trend_analysis({ metric: 'performance', period: '24h' })
    ]);

    return {
      bottlenecks,
      metrics,
      trends,
      analysis: this.synthesizeAnalysis(bottlenecks, metrics, trends)
    };
  },

  // Generate performance report
  async generateReport(format = 'detailed') {
    const [performance, usage, errors] = await Promise.all([
      mcp.performance_report({ format, timeframe: '24h' }),
      mcp.usage_stats({}),
      mcp.error_analysis({})
    ]);

    return { performance, usage, errors };
  }
};
```

## Report Format

```markdown
## Performance Analysis Report

### Executive Summary
- Overall performance score: 78/100
- Critical bottlenecks identified: 2
- Recommended actions: 5

### Detailed Findings

#### 1. Sequential Task Execution
- **Impact**: High (40% of execution time)
- **Root Cause**: Tasks A, B, C running sequentially without dependencies
- **Recommendation**: Parallelize tasks A, B, C
- **Expected Improvement**: 35%

#### 2. Memory Pressure
- **Impact**: Medium (25% of issues)
- **Root Cause**: Large file operations loading entire files
- **Recommendation**: Implement streaming processing
- **Expected Improvement**: 50% memory reduction

### Trend Analysis
- Performance over last 7 days: Declining 5%
- Improvement since last optimization: +12%
- Regression detection: None
```

## Optimization Examples

### Example 1: Slow Test Execution

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Duration | 10 min | 3 min | 70% |
| Parallelization | 10% | 80% | 8x |
| Agent Utilization | 25% | 85% | 3.4x |

**Solution**: Parallelize test suites across multiple agents

### Example 2: Agent Coordination Delay

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Latency | 150ms | 90ms | 40% |
| Messages | 500/s | 200/s | 60% reduction |
| Throughput | 100/s | 180/s | 80% |

**Solution**: Switch from hierarchical to mesh topology

### Example 3: Memory Pressure

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Peak Memory | 8GB | 800MB | 90% |
| GC Pauses | 500ms | 50ms | 90% |
| Processing Time | 5min | 3min | 40% |

**Solution**: Stream processing instead of loading entire files

## Advanced Features

### 1. Predictive Analysis

```javascript
// ML-based bottleneck prediction
const predictiveAnalysis = {
  async predictBottlenecks(historicalData) {
    // Train model on historical patterns
    // Predict future bottlenecks
    // Recommend preemptive actions
  }
};
```

### 2. Automated Optimization

```javascript
// Self-tuning optimization
const automatedOptimization = {
  async optimize(swarm, constraints) {
    // Self-tuning parameters
    // Dynamic resource allocation
    // Adaptive execution strategies
  }
};
```

### 3. A/B Testing

```javascript
// Compare optimization strategies
const abTesting = {
  async compare(strategies, workload) {
    // Run strategies in parallel
    // Measure real-world impact
    // Data-driven decision
  }
};
```

## Integration Points

| Integration | Purpose |
|-------------|---------|
| Orchestration Agents | Performance feedback, strategy suggestions |
| Monitoring Agents | Real-time metrics, health correlation |
| Optimization Agents | Handoff optimization tasks, validate results |
| CI/CD Pipeline | Performance gates, regression detection |

## Best Practices

### Continuous Monitoring
- Set up baseline metrics before analysis
- Monitor performance trends continuously
- Alert on regressions immediately
- Run regular optimization cycles

### Proactive Analysis
- Analyze before issues become critical
- Predict bottlenecks from patterns
- Plan capacity ahead of need
- Implement gradual optimizations

### Documentation
- Document all findings and actions
- Track improvement over time
- Share learnings across teams
- Maintain optimization history

## Related Skills

- `optimization-monitor` - Real-time performance monitoring
- `optimization-benchmark` - Performance testing and validation
- `optimization-load-balancer` - Load distribution optimization
- `optimization-resources` - Resource allocation
- `optimization-topology` - Network topology optimization

---

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from performance-analyzer agent with bottleneck detection, pattern recognition, root cause analysis, and optimization recommendations
