---
name: when-using-advanced-swarm-use-swarm-advanced
description: Advanced swarm patterns with dynamic topology switching and self-organizing behaviors for complex multi-agent coordination
version: 1.0.0
tags:
  - swarm
  - advanced
  - coordination
  - topology
  - self-organizing
category: workflow
agents:
  - hierarchical-coordinator
  - mesh-coordinator
  - adaptive-coordinator
complexity: advanced
estimated_duration: 45-90 minutes
prerequisites:
  - Claude Flow installed and configured
  - Understanding of swarm topologies
  - Multi-agent coordination experience
outputs:
  - Advanced swarm infrastructure
  - Dynamic topology configuration
  - Performance metrics
  - Optimization reports
---

# Advanced Swarm Coordination SOP

## Overview

This skill implements advanced swarm patterns with dynamic topology switching, self-organizing behaviors, and intelligent coordination for complex multi-agent systems. It enables sophisticated swarm orchestration with adaptive topology selection and performance optimization.

## Agents & Responsibilities

### hierarchical-coordinator
**Role:** Tree-based coordination with leader-follower patterns
**Responsibilities:**
- Manage hierarchical swarm structures
- Coordinate parent-child agent relationships
- Handle task delegation cascades
- Monitor hierarchy performance

### mesh-coordinator
**Role:** Peer-to-peer coordination with full connectivity
**Responsibilities:**
- Enable direct agent-to-agent communication
- Manage mesh network topology
- Coordinate distributed consensus
- Handle fault tolerance

### adaptive-coordinator
**Role:** Dynamic topology switching based on workload
**Responsibilities:**
- Analyze task complexity and requirements
- Switch topologies dynamically
- Optimize resource allocation
- Monitor and adapt to performance

## Phase 1: Initialize Swarm Infrastructure

### Objective
Establish foundation for advanced swarm coordination with proper topology and agent configuration.

### Evidence-Based Validation
- [ ] Swarm initialized with confirmed topology
- [ ] All agents spawned successfully
- [ ] Memory coordination active
- [ ] Health checks passing

### Scripts

```bash
# Initialize hierarchical swarm
npx claude-flow@alpha swarm init --topology hierarchical --max-agents 10

# Initialize mesh swarm
npx claude-flow@alpha swarm init --topology mesh --max-agents 8

# Initialize adaptive swarm
npx claude-flow@alpha swarm init --topology adaptive --max-agents 12 --strategy balanced

# Verify initialization
npx claude-flow@alpha swarm status --verbose

# Setup memory coordination
npx claude-flow@alpha memory store --key "swarm/topology" --value "hierarchical"
npx claude-flow@alpha memory store --key "swarm/max-agents" --value "10"
```

### MCP Integration

```javascript
// Initialize swarm with MCP
mcp__claude-flow__swarm_init({
  topology: "hierarchical",
  maxAgents: 10,
  strategy: "balanced"
})

// Alternative: Mesh topology
mcp__claude-flow__swarm_init({
  topology: "mesh",
  maxAgents: 8,
  strategy: "specialized"
})

// Alternative: Adaptive topology
mcp__claude-flow__swarm_init({
  topology: "adaptive",
  maxAgents: 12,
  strategy: "adaptive"
})
```

### Memory Patterns

```bash
# Store swarm configuration
npx claude-flow@alpha memory store \
  --key "swarm/config" \
  --value '{"topology":"hierarchical","maxAgents":10,"strategy":"balanced"}'

# Store agent assignments
npx claude-flow@alpha memory store \
  --key "swarm/agents/coordinator-1" \
  --value '{"type":"hierarchical-coordinator","status":"active","level":0}'
```

### Validation Criteria
1. Swarm ID generated and confirmed
2. Topology matches requested configuration
3. Agent count within specified limits
4. Memory coordination operational
5. Health endpoint responding

## Phase 2: Configure Topology

### Objective
Select and configure optimal topology pattern based on task requirements and complexity.

### Evidence-Based Validation
- [ ] Topology selected based on analysis
- [ ] Coordinator agents spawned
- [ ] Agent connections established
- [ ] Topology metrics baseline recorded

### Scripts

```bash
# Spawn hierarchical coordinator
npx claude-flow@alpha agent spawn \
  --type coordinator \
  --role "hierarchical-coordinator" \
  --capabilities "task-delegation,hierarchy-management"

# Spawn mesh coordinator
npx claude-flow@alpha agent spawn \
  --type coordinator \
  --role "mesh-coordinator" \
  --capabilities "peer-coordination,consensus"

# Spawn adaptive coordinator
npx claude-flow@alpha agent spawn \
  --type coordinator \
  --role "adaptive-coordinator" \
  --capabilities "topology-switching,optimization"

# Configure topology
npx claude-flow@alpha swarm configure \
  --topology hierarchical \
  --levels 3 \
  --branching-factor 3

# Verify topology
npx claude-flow@alpha swarm status --show-topology
```

### MCP Integration

```javascript
// Spawn coordinator agents
mcp__claude-flow__agent_spawn({
  type: "coordinator",
  name: "hierarchical-coordinator",
  capabilities: ["task-delegation", "hierarchy-management"]
})

mcp__claude-flow__agent_spawn({
  type: "coordinator",
  name: "mesh-coordinator",
  capabilities: ["peer-coordination", "consensus"]
})

mcp__claude-flow__agent_spawn({
  type: "coordinator",
  name: "adaptive-coordinator",
  capabilities: ["topology-switching", "optimization"]
})
```

### Topology Selection Guide

**Hierarchical:**
- Best for: Clear task hierarchies, delegation workflows
- Pros: Efficient delegation, clear authority
- Cons: Single point of failure at root
- Use when: Tasks have natural parent-child relationships

**Mesh:**
- Best for: Peer collaboration, distributed consensus
- Pros: High fault tolerance, no bottlenecks
- Cons: Higher communication overhead
- Use when: Agents need direct communication

**Star:**
- Best for: Centralized coordination, simple workflows
- Pros: Simple control, low complexity
- Cons: Central coordinator bottleneck
- Use when: Single coordinator can handle all traffic

**Ring:**
- Best for: Sequential processing, pipeline workflows
- Pros: Predictable flow, ordered execution
- Cons: Latency accumulation
- Use when: Tasks must be processed in sequence

**Adaptive:**
- Best for: Dynamic workloads, variable complexity
- Pros: Automatic optimization, flexible
- Cons: Overhead from topology switching
- Use when: Workload patterns vary significantly

### Memory Patterns

```bash
# Store topology configuration
npx claude-flow@alpha memory store \
  --key "swarm/topology/config" \
  --value '{"type":"hierarchical","levels":3,"branchingFactor":3}'

# Store baseline metrics
npx claude-flow@alpha memory store \
  --key "swarm/metrics/baseline" \
  --value '{"latency":45,"throughput":120,"agentUtilization":0.75}'
```

### Validation Criteria
1. Coordinator agents active and responsive
2. Topology structure matches configuration
3. Agent connections verified
4. Baseline metrics recorded
5. No configuration errors

## Phase 3: Deploy Agents

### Objective
Spawn specialized agents based on topology and assign roles with proper coordination.

### Evidence-Based Validation
- [ ] All required agents spawned
- [ ] Agent roles assigned correctly
- [ ] Coordination protocols active
- [ ] Agent health checks passing

### Scripts

```bash
# Spawn specialized agents for hierarchical topology
npx claude-flow@alpha agent spawn --type researcher --capabilities "analysis,patterns"
npx claude-flow@alpha agent spawn --type coder --capabilities "implementation,testing"
npx claude-flow@alpha agent spawn --type reviewer --capabilities "quality,security"

# Assign agents to hierarchy levels
npx claude-flow@alpha swarm assign \
  --agent-id "agent-001" \
  --level 1 \
  --parent "coordinator-1"

# Spawn agents for mesh topology
npx claude-flow@alpha agent spawn --type analyst --peer-mode enabled
npx claude-flow@alpha agent spawn --type optimizer --peer-mode enabled

# Configure peer connections
npx claude-flow@alpha swarm connect-peers --all

# List all agents
npx claude-flow@alpha agent list --show-roles --show-connections
```

### MCP Integration

```javascript
// Spawn specialized agents
mcp__claude-flow__agent_spawn({
  type: "researcher",
  capabilities: ["analysis", "patterns", "research"]
})

mcp__claude-flow__agent_spawn({
  type: "coder",
  capabilities: ["implementation", "testing", "debugging"]
})

mcp__claude-flow__agent_spawn({
  type: "analyst",
  capabilities: ["optimization", "performance", "metrics"]
})

// Check agent status
mcp__claude-flow__agent_list({
  filter: "active"
})

mcp__claude-flow__agent_metrics({
  metric: "all"
})
```

### Agent Assignment Patterns

**Hierarchical Assignment:**
```bash
# Level 0: Root coordinator
# Level 1: Department coordinators
# Level 2: Task executors
# Level 3: Specialized workers

npx claude-flow@alpha memory store \
  --key "swarm/hierarchy/level-0" \
  --value '{"agent":"coordinator-1","role":"root"}'

npx claude-flow@alpha memory store \
  --key "swarm/hierarchy/level-1" \
  --value '["agent-001","agent-002","agent-003"]'
```

**Mesh Assignment:**
```bash
# All agents are peers with direct connections
npx claude-flow@alpha memory store \
  --key "swarm/mesh/peers" \
  --value '["agent-001","agent-002","agent-003","agent-004"]'
```

### Memory Patterns

```bash
# Store agent roster
npx claude-flow@alpha memory store \
  --key "swarm/agents/roster" \
  --value '{"total":8,"active":8,"idle":0,"roles":{"researcher":2,"coder":3,"reviewer":2,"optimizer":1}}'

# Store agent capabilities
npx claude-flow@alpha memory store \
  --key "swarm/agents/agent-001/capabilities" \
  --value '["analysis","patterns","research","documentation"]'
```

### Validation Criteria
1. Agent count matches requirements
2. All agents responding to health checks
3. Role assignments verified
4. Coordination protocols established
5. Memory state synchronized

## Phase 4: Monitor Performance

### Objective
Track swarm performance metrics, identify bottlenecks, and gather optimization data.

### Evidence-Based Validation
- [ ] Metrics collected continuously
- [ ] Performance baseline established
- [ ] Bottlenecks identified
- [ ] Optimization opportunities logged

### Scripts

```bash
# Monitor swarm status
npx claude-flow@alpha swarm monitor --interval 5 --duration 60

# Get agent metrics
npx claude-flow@alpha agent metrics --all --format json

# Check task performance
npx claude-flow@alpha task status --show-timing

# Analyze bottlenecks
npx claude-flow@alpha performance analyze --detect-bottlenecks

# Export metrics
npx claude-flow@alpha metrics export --output ./swarm-metrics.json

# Generate performance report
npx claude-flow@alpha performance report \
  --include-agents \
  --include-topology \
  --output ./performance-report.md
```

### MCP Integration

```javascript
// Monitor swarm in real-time
mcp__claude-flow__swarm_monitor({
  duration: 60,
  interval: 5
})

// Get comprehensive metrics
mcp__claude-flow__agent_metrics({
  metric: "all"
})

// Check task status
mcp__claude-flow__task_status({
  detailed: true
})

// Run performance benchmarks
mcp__claude-flow__benchmark_run({
  type: "swarm",
  iterations: 10
})
```

### Key Metrics to Track

**Swarm-Level Metrics:**
- Total throughput (tasks/minute)
- Average latency per task
- Agent utilization rate
- Coordination overhead
- Memory usage
- Network latency

**Agent-Level Metrics:**
- Task completion rate
- Response time
- Error rate
- Resource consumption
- Idle time percentage

**Topology-Level Metrics:**
- Connection count
- Message passing efficiency
- Fault tolerance score
- Scalability index

### Memory Patterns

```bash
# Store performance snapshot
npx claude-flow@alpha memory store \
  --key "swarm/metrics/snapshot-$(date +%s)" \
  --value '{"throughput":145,"latency":38,"utilization":0.82,"errors":2}'

# Store bottleneck analysis
npx claude-flow@alpha memory store \
  --key "swarm/analysis/bottlenecks" \
  --value '{"coordinator-1":{"type":"high-load","severity":"medium","recommendation":"add-peer"}}'
```

### Validation Criteria
1. Metrics collected every 5 seconds
2. No data loss or gaps
3. Bottlenecks identified and documented
4. Performance trends visible
5. Alerts triggered for anomalies

## Phase 5: Optimize Dynamically

### Objective
Apply dynamic optimizations including topology switching, agent rebalancing, and resource allocation.

### Evidence-Based Validation
- [ ] Optimization strategies applied
- [ ] Performance improvements measured
- [ ] Topology switches successful
- [ ] Resource allocation optimized
- [ ] Final metrics show improvement

### Scripts

```bash
# Analyze optimization opportunities
npx claude-flow@alpha performance analyze --recommend-optimizations

# Switch topology dynamically
npx claude-flow@alpha swarm reconfigure --topology mesh

# Rebalance agents
npx claude-flow@alpha swarm rebalance --strategy adaptive

# Scale swarm
npx claude-flow@alpha swarm scale --target-agents 12

# Apply neural optimizations
npx claude-flow@alpha neural train --pattern convergent

# Validate improvements
npx claude-flow@alpha performance compare \
  --baseline ./baseline-metrics.json \
  --current ./current-metrics.json

# Generate optimization report
npx claude-flow@alpha performance report \
  --show-improvements \
  --output ./optimization-report.md
```

### MCP Integration

```javascript
// Get optimization recommendations
mcp__claude-flow__benchmark_run({
  type: "swarm",
  iterations: 5
})

// Train neural patterns
mcp__claude-flow__neural_train({
  agentId: "adaptive-coordinator",
  iterations: 10
})

// Check neural patterns
mcp__claude-flow__neural_patterns({
  pattern: "all"
})
```

### Optimization Strategies

**Topology Switching:**
```bash
# Switch from hierarchical to mesh if bottleneck detected
if [ "$COORDINATOR_LOAD" -gt 80 ]; then
  npx claude-flow@alpha swarm reconfigure --topology mesh
fi

# Switch to ring for sequential processing
if [ "$TASK_TYPE" == "pipeline" ]; then
  npx claude-flow@alpha swarm reconfigure --topology ring
fi
```

**Agent Rebalancing:**
```bash
# Identify underutilized agents
npx claude-flow@alpha agent metrics --filter "utilization<0.3"

# Reassign tasks from overloaded agents
npx claude-flow@alpha swarm rebalance --threshold 0.8

# Add agents if all are highly utilized
if [ "$AVG_UTILIZATION" -gt 0.9 ]; then
  npx claude-flow@alpha agent spawn --type optimizer --auto-assign
fi
```

**Resource Allocation:**
```bash
# Allocate more memory to high-priority agents
npx claude-flow@alpha agent configure \
  --agent-id "agent-001" \
  --memory-limit 2048MB

# Adjust coordination intervals
npx claude-flow@alpha swarm configure --sync-interval 3s
```

### Memory Patterns

```bash
# Store optimization actions
npx claude-flow@alpha memory store \
  --key "swarm/optimization/actions" \
  --value '{"timestamp":"2025-10-30T10:30:00Z","action":"topology-switch","from":"hierarchical","to":"mesh","reason":"coordinator-bottleneck"}'

# Store improvement metrics
npx claude-flow@alpha memory store \
  --key "swarm/optimization/improvements" \
  --value '{"throughput":{"before":120,"after":175,"improvement":45.8},"latency":{"before":45,"after":32,"improvement":28.9}}'
```

### Validation Criteria
1. Performance metrics improved by ≥15%
2. Bottlenecks eliminated or reduced
3. Agent utilization balanced (±10%)
4. No errors introduced by optimizations
5. Topology switches completed successfully

## Success Criteria

### Overall Validation
- [ ] Swarm infrastructure stable and operational
- [ ] Optimal topology selected and configured
- [ ] All agents deployed and coordinated
- [ ] Performance monitored and optimized
- [ ] Improvements measured and validated

### Performance Targets
- Throughput increase: ≥20%
- Latency reduction: ≥15%
- Agent utilization: 70-90%
- Error rate: <2%
- Coordination overhead: <10%

## Common Issues & Solutions

### Issue: Coordinator Bottleneck
**Symptoms:** High latency, coordinator CPU >90%
**Solution:** Switch to mesh topology or add peer coordinators

### Issue: Agent Underutilization
**Symptoms:** Many agents idle, unbalanced load
**Solution:** Rebalance task assignment, reduce agent count

### Issue: Topology Switch Failures
**Symptoms:** Errors during reconfiguration, lost connections
**Solution:** Drain tasks before switching, validate agent states

### Issue: Memory Synchronization Lag
**Symptoms:** Agents have inconsistent state
**Solution:** Increase sync frequency, use distributed consensus

## Best Practices

1. **Start Simple:** Begin with hierarchical or star topology
2. **Monitor First:** Collect baseline metrics before optimizing
3. **Gradual Scaling:** Add agents incrementally
4. **Test Topology Switches:** Validate in non-production first
5. **Document Patterns:** Record successful configurations
6. **Use Neural Training:** Improve pattern recognition
7. **Enable Auto-Healing:** Configure self-recovery mechanisms
8. **Regular Health Checks:** Monitor agent health continuously

## Integration Points

### With Other Skills
- **swarm-orchestration:** For complex task coordination
- **performance-analysis:** For deep performance insights
- **hive-mind:** For collective intelligence patterns
- **cascade-orchestrator:** For workflow chaining

### With External Systems
- GitHub Actions for CI/CD integration
- Prometheus for metrics collection
- Grafana for visualization
- Slack/Discord for alerts

## Next Steps

After completing this skill:
1. Explore specific topology patterns in depth
2. Implement custom coordination protocols
3. Integrate with monitoring systems
4. Create domain-specific swarm templates
5. Experiment with hybrid topologies

## References

- Claude Flow Documentation: https://github.com/ruvnet/claude-flow
- Swarm Intelligence Patterns
- Multi-Agent Coordination Theory
- Dynamic Topology Selection Algorithms
