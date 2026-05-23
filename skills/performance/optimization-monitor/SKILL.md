---
name: optimization-monitor
description: Real-time performance metrics collection, bottleneck detection, SLA monitoring, anomaly detection, and resource tracking. Use for continuous system monitoring, performance dashboards, and proactive issue detection.
---

# Performance Monitor Skill

## Overview

This skill provides comprehensive real-time performance monitoring capabilities including metrics collection, bottleneck detection, SLA compliance tracking, anomaly detection, and resource utilization monitoring for swarm-based systems.

## When to Use

- Continuous monitoring of swarm performance
- Detecting performance bottlenecks before they impact operations
- Tracking SLA compliance and generating alerts
- Anomaly detection in system metrics
- Resource utilization tracking and forecasting
- Building real-time performance dashboards

## Quick Start

```bash
# Start comprehensive monitoring
npx claude-flow performance-report --format detailed --timeframe 24h

# Real-time bottleneck analysis
npx claude-flow bottleneck-analyze --component swarm-coordination

# Health check all components
npx claude-flow health-check --components ["swarm", "agents", "coordination"]

# Collect specific metrics
npx claude-flow metrics-collect --components ["cpu", "memory", "network"]
```

## Architecture

```
+-----------------------------------------------------------+
|                  Performance Monitor                       |
+-----------------------------------------------------------+
|  Metrics Collector  |  Bottleneck Analyzer  |  SLA Monitor |
+---------------------+-----------------------+--------------+
         |                     |                      |
         v                     v                      v
+-------------------+  +------------------+  +---------------+
| System Metrics    |  | Pattern Detection|  | Threshold     |
| - CPU/Memory      |  | - CPU Bottleneck |  | Checking      |
| - I/O/Network     |  | - Memory Leak    |  | - Availability|
| - Process Stats   |  | - I/O Saturation |  | - Response    |
+-------------------+  | - Network Issues |  | - Throughput  |
                       +------------------+  +---------------+
         |                     |                      |
         v                     v                      v
+-----------------------------------------------------------+
|              Dashboard Provider (Real-time)                |
+-----------------------------------------------------------+
```

## Core Capabilities

### 1. Multi-Dimensional Metrics Collection

```javascript
// Real-time metrics collection
const metrics = await mcp.metrics_collect({
  components: ['cpu', 'memory', 'network', 'agents']
});

// System metrics include:
// - CPU: usage, load average, core utilization
// - Memory: usage, available, pressure
// - I/O: disk usage, disk I/O, network I/O
// - Processes: count, threads, handles
```

### 2. Bottleneck Detection

Detects and categorizes bottlenecks:
- **CPU Bottlenecks**: High CPU usage, core saturation
- **Memory Bottlenecks**: Memory pressure, leak detection
- **I/O Bottlenecks**: Disk saturation, network congestion
- **Coordination Bottlenecks**: Agent communication delays
- **Task Queue Bottlenecks**: Queue backup, processing delays

```bash
# Analyze specific component
npx claude-flow bottleneck-analyze --component task-queue

# Full system analysis
npx claude-flow bottleneck-analyze
```

### 3. SLA Monitoring

Configure and monitor SLA metrics:

| Metric | Description | Typical Threshold |
|--------|-------------|-------------------|
| Availability | System uptime percentage | 99.9% |
| Response Time | Request latency | < 1000ms |
| Throughput | Requests per second | > 100 RPS |
| Error Rate | Failed requests percentage | < 0.1% |
| Recovery Time | Time to recover from failure | < 300s |

### 4. Anomaly Detection

Multi-model anomaly detection:
- **Statistical**: 3-sigma rule deviation detection
- **Machine Learning**: Trained anomaly detection models
- **Time Series**: LSTM-based temporal anomaly detection
- **Behavioral**: Agent behavior pattern analysis

## Key Metrics

### KPIs Monitored

| Category | Metrics |
|----------|---------|
| Availability | Uptime, MTBF, MTTR |
| Performance | Response time (p50/p90/p95/p99), throughput |
| Efficiency | Resource utilization, cost per transaction |
| Reliability | Error rate, success rate, fault tolerance |

### Resource Tracking

- CPU: Current, peak, average utilization with percentiles
- Memory: Usage trends, leak detection, pressure indicators
- Network: Bandwidth utilization, latency, packet loss
- Agents: Per-agent efficiency, responsiveness, reliability

## MCP Integration

```javascript
// Comprehensive monitoring setup
const monitoring = {
  // Start all monitors
  async startMonitoring() {
    const [health, performance, bottlenecks] = await Promise.all([
      mcp.health_check({ components: ['swarm', 'coordination'] }),
      mcp.performance_report({ format: 'detailed', timeframe: '24h' }),
      mcp.bottleneck_analyze({})
    ]);

    return { health, performance, bottlenecks };
  },

  // Agent performance tracking
  async monitorAgents(swarmId) {
    const agents = await mcp.agent_list({ swarmId });
    const metrics = new Map();

    for (const agent of agents) {
      metrics.set(agent.id, await mcp.agent_metrics({ agentId: agent.id }));
    }

    return metrics;
  }
};
```

## Alert Configuration

```bash
# Configure performance alerts
npx claude-flow alert-config --metric cpu_usage --threshold 80 --severity warning

# Set up anomaly detection
npx claude-flow anomaly-setup --models ["statistical", "ml", "time_series"]

# Configure notification channels
npx claude-flow notification-config --channels ["slack", "email", "webhook"]
```

## Integration Points

| Integration | Purpose |
|-------------|---------|
| Load Balancer | Provides performance data for load balancing decisions |
| Topology Optimizer | Supplies network and coordination metrics |
| Resource Allocator | Shares resource utilization and forecasting data |
| Task Orchestrator | Monitors task execution performance |

## Best Practices

1. **Baseline Establishment**: Collect baseline metrics before monitoring for anomalies
2. **Alert Tuning**: Start with conservative thresholds, tune based on false positive rate
3. **Multi-Layer Monitoring**: Monitor at system, agent, and task levels
4. **Historical Analysis**: Retain metrics for trend analysis and capacity planning
5. **Proactive Detection**: Use predictive analytics to detect issues before impact

## Example: Dashboard Data Provider

```javascript
// Real-time dashboard data
const dashboardData = {
  overview: {
    swarmHealth: 'healthy',
    activeAgents: 12,
    totalTasks: 1547,
    averageResponseTime: 45  // ms
  },
  performance: {
    throughput: 250,  // tasks/sec
    latency: { p50: 40, p90: 85, p99: 120 },  // ms
    errorRate: 0.02,  // percentage
    utilization: 0.72  // percentage
  },
  alerts: [],
  timestamp: Date.now()
};
```

## Related Skills

- `optimization-benchmark` - Comprehensive performance benchmarking
- `optimization-load-balancer` - Dynamic load distribution
- `optimization-resources` - Resource allocation and scaling
- `optimization-topology` - Network topology optimization

---

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from performance-monitor agent with metrics collection, bottleneck detection, SLA monitoring, anomaly detection, and dashboard integration
