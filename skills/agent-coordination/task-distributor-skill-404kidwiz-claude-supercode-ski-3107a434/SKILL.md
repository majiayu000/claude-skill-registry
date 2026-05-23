---
name: task-distributor
description: Expert in load balancing and dynamic task allocation for multi-agent systems. Specializes in optimal routing based on agent capability, availability, and cost (Token Economics).
---

# Task Distributor

## Purpose
Provides expertise in distributing tasks across multi-agent systems efficiently. Specializes in load balancing algorithms, capability-based routing, cost optimization, and ensuring optimal resource utilization across distributed agent pools.

## When to Use
- Designing task distribution strategies for multi-agent systems
- Implementing load balancing across worker pools
- Optimizing for cost (token economics) vs speed trade-offs
- Building routing logic based on agent capabilities
- Managing task queues with priorities and deadlines
- Implementing retry and failover strategies
- Scaling agent pools dynamically based on demand
- Monitoring and optimizing task throughput

## Quick Start
**Invoke this skill when:**
- Designing task distribution strategies for multi-agent systems
- Implementing load balancing across worker pools
- Optimizing for cost (token economics) vs speed trade-offs
- Building routing logic based on agent capabilities
- Managing task queues with priorities and deadlines

**Do NOT invoke when:**
- Designing overall agent architecture → use agent-organizer
- Implementing individual agent logic → use appropriate domain skill
- Handling agent errors and recovery → use error-coordinator
- Building workflow orchestration → use workflow-orchestrator

## Decision Framework
```
Distribution Strategy?
├── Uniform Workloads → Round-robin or random distribution
├── Variable Task Complexity → Weighted distribution by capability
├── Cost Sensitive → Route to cheapest capable agent
├── Latency Sensitive → Route to fastest/nearest agent
├── Specialized Tasks → Capability-based routing
└── Burst Traffic → Dynamic scaling + queue management
```

## Core Workflows

### 1. Capability-Based Routing
1. Define capability taxonomy for agents
2. Tag tasks with required capabilities
3. Implement capability matching algorithm
4. Score agents by capability fit and availability
5. Route to best-matched agent
6. Track capability utilization for optimization
7. Adjust routing weights based on performance

### 2. Cost-Optimized Distribution
1. Define cost model per agent type (tokens, time, money)
2. Estimate task cost based on complexity signals
3. Set budget constraints and optimization targets
4. Route to minimize cost while meeting SLAs
5. Implement fallback to higher-cost agents when needed
6. Track actual vs estimated costs
7. Refine cost models from historical data

### 3. Queue Management with Priorities
1. Define priority levels and SLA requirements
2. Implement priority queue with deadline awareness
3. Set up work stealing for idle agents
4. Handle starvation of low-priority tasks
5. Implement backpressure when queue depth exceeds threshold
6. Monitor queue latency and throughput
7. Scale agent pool based on queue metrics

## Best Practices
- Implement health checks and remove unhealthy agents from pool
- Use exponential backoff with jitter for retries
- Track per-agent metrics for informed routing decisions
- Implement circuit breakers for failing agent types
- Design for graceful degradation under load
- Make routing decisions observable for debugging

## Anti-Patterns
- **Static assignment** → Use dynamic routing based on current state
- **Ignoring agent health** → Remove unhealthy agents from rotation
- **FIFO only** → Implement priority awareness for SLA compliance
- **Tight coupling** → Decouple task producers from agent pool
- **No backpressure** → Implement admission control under overload
