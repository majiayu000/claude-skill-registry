---
name: optimization-load-balancer
description: Dynamic task distribution, work-stealing algorithms, queue management, and adaptive load balancing. Use for optimizing task execution across agents, preventing overload, and maximizing throughput.
---

# Load Balancing Coordinator Skill

## Overview

This skill provides comprehensive load balancing capabilities including work-stealing algorithms, dynamic task distribution, queue management, and adaptive resource allocation for optimal swarm coordination.

## When to Use

- Distributing tasks across multiple agents efficiently
- Preventing agent overload while maximizing utilization
- Implementing fair scheduling across different task priorities
- Optimizing throughput in distributed systems
- Handling variable workloads with adaptive balancing
- Migrating tasks from overloaded to underloaded agents

## Quick Start

```bash
# Initialize load balancer
npx claude-flow agent spawn load-balancer --type coordinator

# Start load balancing
npx claude-flow load-balance --swarm-id <id> --strategy adaptive

# Monitor load distribution
npx claude-flow agent-metrics --type load-balancer

# Adjust balancing parameters
npx claude-flow config-manage --action update --config '{"stealThreshold": 5, "agingBoost": 10}'
```

## Architecture

```
+-----------------------------------------------------------+
|                Load Balancing Coordinator                  |
+-----------------------------------------------------------+
|  Work Stealer  |  Load Balancer  |  Queue Manager         |
+----------------+-----------------+-------------------------+
        |                |                    |
        v                v                    v
+---------------+  +-----------------+  +------------------+
| Victim Select |  | Agent Capacity  |  | Priority Queues  |
| - Heaviest    |  | - Load Tracking |  | - Critical       |
| - Threshold   |  | - Performance   |  | - High/Normal    |
| - Locality    |  | - Migration     |  | - Low/Background |
+---------------+  +-----------------+  +------------------+
        |                |                    |
        v                v                    v
+-----------------------------------------------------------+
|              Resource Optimization Engine                  |
+-----------------------------------------------------------+
```

## Core Capabilities

### 1. Work-Stealing Algorithm

Efficiently redistributes work from overloaded agents:

```javascript
// Work-stealing configuration
const workStealing = {
  stealThreshold: 5,       // Steal when queue > 5 tasks
  stealPercentage: 0.5,    // Take 50% of victim's queue
  victimSelection: 'heaviest',  // Steal from busiest agent
  localityAware: true      // Prefer nearby agents
};

// Victim selection strategies:
// - heaviest: Steal from agent with most tasks
// - random: Random selection for fairness
// - locality: Prefer agents in same topology region
```

### 2. Dynamic Load Balancing

Real-time load distribution:

| Strategy | Description | Best For |
|----------|-------------|----------|
| Round Robin | Sequential distribution | Uniform tasks |
| Weighted | Based on agent capacity | Heterogeneous agents |
| Least Connections | To least loaded agent | Variable task duration |
| Adaptive | ML-based optimization | Complex workloads |

### 3. Queue Management

Multi-level feedback queue scheduling:

| Priority Level | Weight | Use Case |
|----------------|--------|----------|
| Critical | 40% | System-critical tasks |
| High | 30% | User-facing operations |
| Normal | 20% | Standard processing |
| Low | 10% | Background tasks |

### 4. Resource Allocation

Multi-objective optimization:
- Minimize latency
- Maximize utilization
- Balance load
- Minimize cost

## Scheduling Algorithms

### Earliest Deadline First (EDF)

```javascript
// EDF for real-time task scheduling
const edfScheduler = {
  schedule(tasks) {
    return tasks.sort((a, b) => a.deadline - b.deadline);
  },

  // Liu & Layland utilization bound
  admissionControl(newTask, existingTasks) {
    const utilization = [...existingTasks, newTask]
      .reduce((sum, t) => sum + (t.executionTime / t.period), 0);
    return utilization <= 1.0;
  }
};
```

### Completely Fair Scheduler (CFS)

```javascript
// CFS for fair task distribution
const cfsScheduler = {
  virtualRuntime: new Map(),
  weights: new Map(),

  schedule() {
    // Select task with minimum virtual runtime
    return this.getMinVirtualRuntimeTask();
  },

  updateVirtualRuntime(task, elapsedTime) {
    const weight = this.weights.get(task.id) || 1;
    const vruntime = this.virtualRuntime.get(task.id) || 0;
    this.virtualRuntime.set(task.id, vruntime + (elapsedTime / weight));
  }
};
```

### Weighted Fair Queuing (WFQ)

Proportional bandwidth allocation based on agent weights.

## MCP Integration

```javascript
// MCP load balancing integration
const loadBalancingIntegration = {
  // Real-time metrics collection
  async collectMetrics() {
    const [performance, bottlenecks, tokenUsage] = await Promise.all([
      mcp.performance_report({ format: 'json' }),
      mcp.bottleneck_analyze({}),
      mcp.token_usage({})
    ]);

    return { performance, bottlenecks, tokenUsage, timestamp: Date.now() };
  },

  // Execute load balancing
  async coordinateLoadBalancing(swarmId) {
    const agents = await mcp.agent_list({ swarmId });
    const metrics = await mcp.agent_metrics({});

    const rebalancing = this.calculateRebalancing(agents, metrics);

    if (rebalancing.required) {
      await mcp.load_balance({
        swarmId,
        tasks: rebalancing.taskMigrations
      });
    }

    return rebalancing;
  }
};
```

## Circuit Breaker Pattern

Protect against cascade failures:

```javascript
const circuitBreaker = {
  state: 'CLOSED',           // CLOSED, OPEN, HALF_OPEN
  failureThreshold: 5,       // Open after 5 failures
  successThreshold: 3,       // Close after 3 successes
  timeout: 60000,            // Recovery timeout (ms)

  async execute(operation, fallback) {
    if (this.state === 'OPEN' && !this.shouldAttemptReset()) {
      return fallback ? await fallback() : null;
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      if (fallback) return fallback();
      throw error;
    }
  }
};
```

## Key Metrics

### Performance Indicators

| Metric | Description | Target |
|--------|-------------|--------|
| Load Distribution Variance | Balance across agents | < 0.1 |
| Task Migration Rate | Work-stealing frequency | < 5% |
| Queue Latency | Time in queue | < 100ms |
| Utilization Efficiency | Resource usage | > 80% |
| Fairness Index | Jain's fairness | > 0.9 |

### Benchmarking

```javascript
// Load balancer benchmarks
const benchmarks = {
  async throughputTest(taskCount, agentCount) {
    const startTime = performance.now();
    await this.distributeAndExecute(taskCount, agentCount);
    const endTime = performance.now();

    return {
      throughput: taskCount / ((endTime - startTime) / 1000),
      averageLatency: (endTime - startTime) / taskCount
    };
  },

  async loadBalanceEfficiency(tasks, agents) {
    const distribution = await this.distributeLoad(tasks, agents);
    const idealLoad = tasks.length / agents.length;

    const variance = distribution.reduce((sum, load) =>
      sum + Math.pow(load - idealLoad, 2), 0) / agents.length;

    return {
      efficiency: 1 / (1 + variance),
      loadVariance: variance
    };
  }
};
```

## Commands Reference

```bash
# Real-time load monitoring
npx claude-flow performance-report --format detailed

# Bottleneck analysis
npx claude-flow bottleneck-analyze --component swarm-coordination

# Resource utilization tracking
npx claude-flow metrics-collect --components ["load-balancer", "task-queue"]

# Configure load balancing strategy
npx claude-flow config-manage --action update \
  --config '{"strategy": "adaptive", "threshold": 0.8}'
```

## Integration Points

| Integration | Purpose |
|-------------|---------|
| Performance Monitor | Real-time metrics for load decisions |
| Topology Optimizer | Coordinate topology changes with load |
| Resource Allocator | Optimize resource distribution |
| Task Orchestrator | Receive load-balanced assignments |

## Best Practices

1. **Gradual Migration**: Move tasks incrementally to avoid oscillation
2. **Locality Awareness**: Prefer local task execution to minimize latency
3. **Priority Preservation**: Maintain task priorities during migration
4. **Monitoring**: Track load balance metrics continuously
5. **Adaptive Thresholds**: Adjust thresholds based on workload patterns
6. **Circuit Breakers**: Protect against cascade failures

## Example: Adaptive Load Balancing

```javascript
// Adaptive load balancing strategy
const adaptiveBalancer = {
  config: {
    checkInterval: 5000,     // Check every 5 seconds
    migrationThreshold: 0.3, // Migrate if imbalance > 30%
    cooldownPeriod: 30000,   // Wait 30s between migrations
    maxMigrations: 5         // Max 5 migrations per cycle
  },

  async balance(swarm) {
    const loads = await this.getAgentLoads(swarm);
    const average = loads.reduce((a, b) => a + b) / loads.length;

    const overloaded = loads.filter(l => l > average * 1.3);
    const underloaded = loads.filter(l => l < average * 0.7);

    if (overloaded.length > 0 && underloaded.length > 0) {
      await this.migrateTasks(overloaded, underloaded);
    }
  }
};
```

## Related Skills

- `optimization-monitor` - Real-time performance monitoring
- `optimization-resources` - Resource allocation and scaling
- `optimization-topology` - Network topology optimization
- `optimization-benchmark` - Performance validation

---

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from load-balancer agent with work-stealing, queue management, scheduling algorithms, circuit breaker pattern, and adaptive balancing
