---
name: optimization-topology
description: Dynamic swarm topology reconfiguration, network latency optimization, agent placement, and communication pattern optimization. Use for optimizing swarm structure, reducing communication overhead, and adaptive network design.
---

# Topology Optimizer Skill

## Overview

This skill provides sophisticated swarm topology optimization capabilities including dynamic reconfiguration, network latency optimization, agent placement strategies, and communication pattern optimization for optimal swarm coordination.

## When to Use

- Optimizing swarm communication patterns
- Reducing network latency and overhead
- Dynamic topology reconfiguration based on workload
- Agent placement for minimal communication distance
- Scaling swarms while maintaining performance
- AI-powered topology prediction and optimization

## Quick Start

```bash
# Analyze current topology
npx claude-flow topology-analyze --swarm-id <id> --metrics performance

# Optimize topology automatically
npx claude-flow topology-optimize --swarm-id <id> --strategy adaptive

# Compare topology configurations
npx claude-flow topology-compare --topologies ["hierarchical", "mesh", "hybrid"]

# Generate topology recommendations
npx claude-flow topology-recommend --workload-profile <file> --constraints <file>
```

## Architecture

```
+-----------------------------------------------------------+
|                   Topology Optimizer                       |
+-----------------------------------------------------------+
|  Topology Engine  |  Network Optimizer  |  Placement Algo |
+-------------------+---------------------+-----------------+
         |                   |                    |
         v                   v                    v
+----------------+  +------------------+  +------------------+
| Topologies     |  | Latency Optimize |  | Placement Algos  |
| - Hierarchical |  | - Physical       |  | - Genetic        |
| - Mesh         |  | - Routing        |  | - Sim Annealing  |
| - Ring         |  | - Protocol       |  | - Particle Swarm |
| - Star         |  | - Caching        |  | - Graph Partition|
| - Hybrid       |  | - Compression    |  | - ML-Based       |
+----------------+  +------------------+  +------------------+
         |                   |                    |
         v                   v                    v
+-----------------------------------------------------------+
|           Communication Pattern Optimizer                  |
+-----------------------------------------------------------+
```

## Topology Types

| Topology | Best For | Latency | Scalability | Fault Tolerance |
|----------|----------|---------|-------------|-----------------|
| Hierarchical | Large teams, clear hierarchy | Medium | High | Medium |
| Mesh | Small teams, high collaboration | Low | Low | High |
| Ring | Sequential processing | Medium | Medium | Low |
| Star | Central coordination | Low | Medium | Low |
| Hybrid | Complex workloads | Variable | High | High |
| Adaptive | Dynamic workloads | Optimized | High | High |

## Core Capabilities

### 1. Dynamic Topology Reconfiguration

```javascript
// Topology optimization workflow
const optimization = await topologyOptimizer.optimize(swarm, workloadProfile, {
  minImprovement: 0.1,    // Only change if 10%+ improvement
  migrationCost: 0.05,    // Factor in migration overhead
  constraints: {
    maxAgentsPerNode: 10,
    minConnectivity: 2,
    maxLatency: 100        // ms
  }
});

// Returns:
// - recommended: Optimal topology
// - improvement: Expected improvement %
// - migrationPlan: Steps to migrate
// - benefits: Detailed improvements
```

### 2. Network Latency Optimization

Multi-layer optimization:

| Layer | Optimization | Impact |
|-------|--------------|--------|
| Physical | Agent placement, bandwidth | 20-40% |
| Routing | Path optimization, load balancing | 10-30% |
| Protocol | TCP/UDP/gRPC selection | 5-15% |
| Caching | Reduce redundant communication | 30-50% |
| Compression | Reduce payload size | 10-25% |

### 3. Agent Placement Algorithms

Multi-algorithm optimization:

```javascript
// Agent placement strategies
const placementAlgorithms = {
  genetic: {
    populationSize: 100,
    mutationRate: 0.1,
    maxGenerations: 500
  },
  simulated_annealing: {
    initialTemperature: 1000,
    coolingRate: 0.95,
    minTemperature: 1
  },
  particle_swarm: {
    swarmSize: 50,
    inertia: 0.7,
    cognitive: 1.5,
    social: 1.5
  },
  graph_partitioning: {
    objective: 'minimize_cut',
    balanceConstraint: 0.05
  }
};
```

### 4. Communication Pattern Optimization

```javascript
// Message batching strategies
const batchingStrategies = [
  { type: 'time', interval: 100, minBatch: 5 },
  { type: 'size', maxSize: 1024, timeout: 50 },
  { type: 'adaptive', targetLatency: 20 },
  { type: 'priority', highPriorityImmediate: true }
];

// Protocol selection per agent pair
const protocolSelection = {
  tcp: { reliability: 0.99, latency: 'medium' },
  udp: { reliability: 0.95, latency: 'low' },
  websocket: { reliability: 0.98, latency: 'medium' },
  grpc: { reliability: 0.99, latency: 'low' },
  mqtt: { reliability: 0.97, latency: 'low' }
};
```

## Optimization Algorithms

### Genetic Algorithm

```javascript
// Evolve optimal topology
const result = await geneticOptimizer.evolve(
  initialTopologies,
  fitnessFunction,
  {
    populationSize: 50,
    mutationRate: 0.1,
    crossoverRate: 0.8,
    maxGenerations: 100,
    eliteSize: 5
  }
);

// Operations:
// - Selection: Tournament selection
// - Crossover: Topology structure combination
// - Mutation: Connection add/remove/modify
```

### Simulated Annealing

```javascript
// Find optimal through local search
const result = await annealingOptimizer.optimize(
  initialTopology,
  objectiveFunction,
  {
    initialTemperature: 1000,
    coolingRate: 0.95,
    minTemperature: 1,
    maxIterations: 10000
  }
);

// Neighbor generation:
// - Add connection
// - Remove connection
// - Modify connection weight
// - Relocate agent
```

## MCP Integration

```javascript
// Topology management integration
const topologyIntegration = {
  // Real-time topology optimization
  async optimizeSwarmTopology(swarmId, config = {}) {
    const [status, performance, bottlenecks] = await Promise.all([
      mcp.swarm_status({ swarmId }),
      mcp.performance_report({ format: 'detailed' }),
      mcp.bottleneck_analyze({ component: 'topology' })
    ]);

    const recommendations = this.generateRecommendations(
      status, performance, bottlenecks, config
    );

    if (recommendations.beneficial) {
      const result = await mcp.topology_optimize({ swarmId });
      return { applied: true, recommendations, result };
    }

    return { applied: false, recommendations };
  },

  // Scale with topology optimization
  async scaleWithTopology(swarmId, targetSize, workloadProfile) {
    await mcp.swarm_scale({ swarmId, targetSize });
    await mcp.topology_optimize({ swarmId });
  }
};
```

### Neural Network Integration

```javascript
// AI-powered topology prediction
const neuralOptimizer = {
  async predictOptimalTopology(swarmState, workloadProfile) {
    const model = await mcp.model_load({
      modelPath: '/models/topology_optimizer.model'
    });

    const features = this.extractFeatures(swarmState, workloadProfile);

    const prediction = await mcp.neural_predict({
      modelId: model.id,
      input: JSON.stringify(features)
    });

    return {
      predictedTopology: prediction.topology,
      confidence: prediction.confidence,
      expectedImprovement: prediction.improvement
    };
  }
};
```

## Commands Reference

```bash
# Analyze current topology
npx claude-flow topology-analyze --swarm-id <id> --metrics performance

# Optimize topology automatically
npx claude-flow topology-optimize --swarm-id <id> --strategy adaptive

# Compare topology configurations
npx claude-flow topology-compare --topologies ["hierarchical", "mesh", "hybrid"]

# Generate topology recommendations
npx claude-flow topology-recommend --workload-profile <file>

# Monitor topology performance
npx claude-flow topology-monitor --swarm-id <id> --interval 60

# Optimize agent placement
npx claude-flow placement-optimize --algorithm genetic --agents <list>

# Analyze placement efficiency
npx claude-flow placement-analyze --current-placement <config>
```

## Key Metrics

### Topology Performance Indicators

| Category | Metric | Description |
|----------|--------|-------------|
| Communication | Latency | Average message latency |
| Communication | Throughput | Messages per second |
| Communication | Bandwidth Util | Network usage |
| Network | Diameter | Max hops between nodes |
| Network | Clustering Coeff | Local connectivity |
| Network | Betweenness | Critical path nodes |
| Fault Tolerance | Connectivity | Min cuts to disconnect |
| Fault Tolerance | Redundancy | Backup paths |
| Scalability | Growth Capacity | Max agents supported |
| Scalability | Efficiency | Performance at scale |

### Benchmark Results

```javascript
const topologyBenchmarks = {
  hierarchical: { latency: 45, throughput: 1200, scalability: 0.95 },
  mesh: { latency: 25, throughput: 2500, scalability: 0.70 },
  ring: { latency: 80, throughput: 800, scalability: 0.85 },
  star: { latency: 30, throughput: 1500, scalability: 0.75 },
  hybrid: { latency: 35, throughput: 2000, scalability: 0.90 }
};
```

## Integration Points

| Integration | Purpose |
|-------------|---------|
| Load Balancer | Coordinate topology with load distribution |
| Performance Monitor | Topology performance metrics |
| Resource Allocator | Resource constraints for topology |
| Task Orchestrator | Task distribution patterns |

## Best Practices

1. **Workload Analysis**: Understand communication patterns before optimization
2. **Gradual Migration**: Migrate topology incrementally
3. **Monitoring**: Continuously monitor topology metrics
4. **Hybrid Approach**: Combine topologies for different workload types
5. **AI-Assisted**: Use ML models for complex optimization
6. **Cost-Benefit**: Consider migration cost vs. performance gain

## Example: Workload-Aware Topology

```javascript
// Select topology based on workload
const topologySelector = {
  selectTopology(workloadProfile) {
    const { coordination, parallelism, locality, faultTolerance } = workloadProfile;

    if (coordination > 0.8 && locality > 0.7) {
      return 'hierarchical';  // High coordination, local processing
    } else if (parallelism > 0.8 && faultTolerance > 0.7) {
      return 'mesh';          // High parallelism, fault tolerant
    } else if (locality > 0.9) {
      return 'ring';          // Sequential, local processing
    } else if (coordination > 0.9) {
      return 'star';          // Central coordination
    }

    return 'hybrid';          // Mixed workload
  },

  async optimizeForWorkload(swarmId, workloadProfile) {
    const recommended = this.selectTopology(workloadProfile);
    const current = await this.getCurrentTopology(swarmId);

    if (recommended !== current) {
      await this.migrateTopology(swarmId, recommended);
    }
  }
};
```

## Related Skills

- `optimization-monitor` - Real-time performance monitoring
- `optimization-load-balancer` - Load distribution optimization
- `optimization-resources` - Resource allocation
- `optimization-benchmark` - Topology performance testing

---

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from topology-optimizer agent with dynamic reconfiguration, latency optimization, agent placement algorithms, genetic/simulated annealing optimization, and neural network integration
