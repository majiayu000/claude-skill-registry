---
name: optimization-resources
description: Adaptive resource allocation, predictive scaling with ML, capacity planning, circuit breakers, and performance profiling. Use for intelligent resource management, auto-scaling, and fault tolerance.
---

# Resource Allocator Skill

## Overview

This skill provides comprehensive adaptive resource allocation capabilities including ML-powered predictive scaling, capacity planning, fault tolerance patterns, and performance profiling for efficient swarm resource management.

## When to Use

- Dynamically allocating resources based on workload
- Predictive scaling before demand spikes
- Capacity planning for future growth
- Implementing fault tolerance (circuit breakers, bulkheads)
- Performance profiling and optimization
- Cost-efficient resource management

## Quick Start

```bash
# Analyze resource usage
npx claude-flow metrics-collect --components ["cpu", "memory", "network"]

# Optimize resource allocation
npx claude-flow daa-resource-alloc --resources <resource-config>

# Predictive scaling
npx claude-flow swarm-scale --swarm-id <id> --target-size <size>

# Performance profiling
npx claude-flow performance-report --format detailed --timeframe 24h
```

## Architecture

```
+-----------------------------------------------------------+
|                   Resource Allocator                       |
+-----------------------------------------------------------+
|  Adaptive Allocator  |  Predictive Scaler  |  Profiler    |
+----------------------+---------------------+--------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +---------------+
| Multi-Objective  |  | ML Models        |  | CPU Profiler  |
| Optimization     |  | - LSTM TimeSeries|  | Memory Profiler|
| - Genetic Algo   |  | - Random Forest  |  | I/O Profiler  |
| - Constraint     |  | - Deep Q-Network |  | Network Prof  |
+------------------+  +------------------+  +---------------+
          |                    |                    |
          v                    v                    v
+-----------------------------------------------------------+
|           Circuit Breaker / Fault Tolerance                |
+-----------------------------------------------------------+
```

## Core Capabilities

### 1. Adaptive Resource Allocation

Dynamic allocation based on workload patterns:

```javascript
// Workload pattern analysis
const patterns = {
  temporal: {
    hourly: analyzeHourlyPatterns(),    // Peak hours
    daily: analyzeDailyPatterns(),       // Weekday vs weekend
    weekly: analyzeWeeklyPatterns(),     // Week cycles
    seasonal: analyzeSeasonalPatterns()  // Monthly/quarterly
  },
  load: {
    baseline: calculateBaselineLoad(),   // Normal load
    peaks: identifyPeakPatterns(),       // Peak times
    valleys: identifyValleyPatterns(),   // Low usage
    spikes: detectAnomalousSpikes()      // Unusual bursts
  },
  correlations: {
    cpu_memory: analyzeCPUMemoryCorrelation(),
    network_load: analyzeNetworkLoadCorrelation(),
    agent_resource: analyzeAgentResourceCorrelation()
  }
};
```

### 2. ML-Powered Predictive Scaling

| Model | Use Case | Accuracy |
|-------|----------|----------|
| LSTM Time Series | Temporal patterns | 85-95% |
| Random Forest | Multi-feature regression | 80-90% |
| Isolation Forest | Anomaly detection | 90%+ |
| Deep Q-Network | Scaling decisions | Adaptive |

```javascript
// Predictive scaling workflow
const prediction = await scaler.predictScaling(swarmId, {
  timeHorizon: 3600,    // 1 hour ahead
  confidence: 0.95,      // 95% confidence
  models: ['lstm', 'ensemble']
});

// Returns:
// - predictions: Resource needs forecast
// - scalingPlan: Recommended scaling actions
// - confidence: Prediction confidence
```

### 3. Multi-Objective Optimization

Genetic algorithm for resource optimization:

```javascript
// Optimization objectives
const objectives = [
  { name: 'minimizeLatency', weight: 0.3 },
  { name: 'maximizeUtilization', weight: 0.25 },
  { name: 'balanceLoad', weight: 0.25 },
  { name: 'minimizeCost', weight: 0.2 }
];

// Genetic algorithm configuration
const geneticConfig = {
  populationSize: 100,
  generations: 200,
  mutationRate: 0.1,
  crossoverRate: 0.8
};

// Returns Pareto-optimal solutions
```

### 4. Fault Tolerance Patterns

#### Circuit Breaker

```javascript
const circuitBreaker = {
  failureThreshold: 5,     // Open after 5 failures
  recoveryTimeout: 60000,  // 60s before half-open
  successThreshold: 3,     // Close after 3 successes

  // Adaptive threshold adjustment
  adaptiveConfig: {
    enabled: true,
    windowSize: 1000,      // Analyze last 1000 requests
    adjustmentRate: 0.1    // 10% threshold adjustment
  }
};
```

#### Bulkhead Pattern

```javascript
// Resource isolation pools
const bulkheads = [
  { name: 'critical', capacity: 10, queue: 50 },
  { name: 'standard', capacity: 20, queue: 100 },
  { name: 'background', capacity: 5, queue: 200 }
];
```

## Performance Profiling

### CPU Profiling

- High-frequency sampling (10ms intervals)
- Flame graph generation
- Hotspot identification
- Function-level statistics

### Memory Profiling

- Snapshot-based analysis (5s intervals)
- Allocation/deallocation tracking
- Memory leak detection
- Growth pattern analysis

### I/O Profiling

- Disk I/O statistics
- Network I/O metrics
- Latency analysis
- Bottleneck identification

## MCP Integration

```javascript
// Resource management integration
const resourceIntegration = {
  // Dynamic allocation
  async allocateResources(swarmId, requirements) {
    const [usage, performance, bottlenecks] = await Promise.all([
      mcp.metrics_collect({ components: ['cpu', 'memory', 'network', 'agents'] }),
      mcp.performance_report({ format: 'detailed' }),
      mcp.bottleneck_analyze({})
    ]);

    const allocation = this.calculateOptimalAllocation(
      usage, performance, bottlenecks, requirements
    );

    return await mcp.daa_resource_alloc({
      resources: allocation.resources,
      agents: allocation.agents
    });
  },

  // Predictive scaling
  async predictiveScale(swarmId, predictions) {
    const status = await mcp.swarm_status({ swarmId });
    const plan = this.calculateScalingPlan(status, predictions);

    if (plan.scaleRequired) {
      await mcp.swarm_scale({ swarmId, targetSize: plan.targetSize });
      await mcp.topology_optimize({ swarmId });
    }

    return plan;
  }
};
```

## Commands Reference

```bash
# Run performance optimization
npx claude-flow optimize-performance --swarm-id <id> --strategy adaptive

# Generate resource forecasts
npx claude-flow forecast-resources --time-horizon 3600 --confidence 0.95

# Profile system performance
npx claude-flow profile-performance --duration 60000 --components all

# Analyze bottlenecks
npx claude-flow bottleneck-analyze --component swarm-coordination

# Circuit breaker configuration
npx claude-flow fault-tolerance --strategy circuit-breaker --config <config>
```

## Key Metrics

### Resource Allocation KPIs

| Category | Metric | Target |
|----------|--------|--------|
| Efficiency | Utilization rate | > 70% |
| Efficiency | Waste percentage | < 10% |
| Efficiency | Allocation accuracy | > 90% |
| Performance | Allocation latency | < 100ms |
| Performance | Scaling response time | < 30s |
| Reliability | Availability | > 99.9% |
| Reliability | Recovery time | < 30s |

### Profiling Output

```javascript
// Profiling results structure
const profilingResults = {
  cpu: {
    samples: [],           // CPU samples
    hotspots: [],          // Top CPU consumers
    flamegraph: {}         // Visualization data
  },
  memory: {
    snapshots: [],         // Memory snapshots
    leaks: [],             // Potential leaks
    growth: []             // Growth patterns
  },
  recommendations: [
    { type: 'optimization', target: 'cpu', suggestion: '...' }
  ]
};
```

## Reinforcement Learning for Scaling

```javascript
// Deep Q-Network agent for scaling decisions
const scalingAgent = {
  stateSize: 10,           // Resource metrics
  actionSize: 5,           // Scale up/down/none
  learningRate: 0.001,
  epsilon: 1.0,            // Exploration rate
  epsilonDecay: 0.995,
  memorySize: 10000,

  // Training loop learns optimal scaling policies
  async train(environment, episodes = 1000) {
    // Agent learns from experience
    // Maximizes resource efficiency while minimizing cost
  }
};
```

## Integration Points

| Integration | Purpose |
|-------------|---------|
| Load Balancer | Resource data for load decisions |
| Performance Monitor | Performance metrics and bottlenecks |
| Topology Optimizer | Coordinate with topology changes |
| Task Orchestrator | Resource allocation for tasks |

## Best Practices

1. **Predictive vs Reactive**: Use prediction for expected patterns, reactive for anomalies
2. **Gradual Scaling**: Scale incrementally to avoid oscillation
3. **Resource Limits**: Set hard limits to prevent runaway allocation
4. **Cost Awareness**: Include cost in optimization objectives
5. **Monitoring**: Continuously monitor allocation effectiveness
6. **Fallback Strategies**: Always have fallback for prediction failures

## Example: Adaptive Scaling

```javascript
// Adaptive scaling configuration
const adaptiveScaler = {
  config: {
    minAgents: 2,
    maxAgents: 50,
    scaleUpThreshold: 0.8,    // 80% utilization
    scaleDownThreshold: 0.3,  // 30% utilization
    cooldownPeriod: 300000,   // 5 minutes
    predictionWeight: 0.7,    // 70% prediction, 30% reactive
  },

  async evaluate(swarmId) {
    const current = await this.getCurrentUtilization(swarmId);
    const predicted = await this.predictFutureLoad(swarmId);

    const combined = current * 0.3 + predicted * 0.7;

    if (combined > this.config.scaleUpThreshold) {
      return { action: 'scale_up', reason: 'high_utilization' };
    } else if (combined < this.config.scaleDownThreshold) {
      return { action: 'scale_down', reason: 'low_utilization' };
    }

    return { action: 'none' };
  }
};
```

## Related Skills

- `optimization-monitor` - Real-time performance monitoring
- `optimization-load-balancer` - Dynamic load distribution
- `optimization-topology` - Network topology optimization
- `optimization-benchmark` - Performance validation

---

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from resource-allocator agent with adaptive allocation, ML-powered scaling, fault tolerance patterns, and performance profiling
