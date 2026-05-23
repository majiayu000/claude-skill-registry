---
name: orchestration-coordination-framework
description: Production-scale multi-agent coordination, task orchestration, and workflow automation. Use for distributed system orchestration, agent communication protocols, DAG workflows, state machines, error handling, resource allocation, load balancing, and observability. Covers Apache Airflow, Temporal, Prefect, Celery, Step Functions, and orchestration patterns.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
---

# Orchestration Coordination Framework

## Purpose

Production-scale AI development requires sophisticated orchestration and coordination. This Skill provides comprehensive orchestration capabilities for:

1. **Multi-Agent Coordination** - Coordinate multiple AI agents working on complex tasks
2. **Task Decomposition** - Break down complex objectives into manageable subtasks
3. **Workflow Orchestration** - DAGs, state machines, event-driven patterns
4. **Communication Protocols** - Agent-to-agent messaging, pub/sub, queues
5. **Error Handling** - Retry logic, circuit breakers, fallback strategies
6. **Resource Management** - Load balancing, rate limiting, concurrency control
7. **Observability** - Monitoring, logging, tracing, metrics for distributed systems
8. **Framework Integration** - Apache Airflow, Temporal, Prefect, Celery, Step Functions

## When to Use This Skill

Use orchestration coordination for:
- Orchestrating multiple agents or services working together
- Complex multi-step workflows requiring coordination
- Distributed task execution with dependencies
- Event-driven architectures and reactive systems
- Building CI/CD pipelines with complex dependencies
- Microservices coordination and saga patterns
- Data pipeline orchestration (ETL/ELT)
- Long-running workflows with state management
- Fault-tolerant distributed systems
- Resource allocation across multiple workers
- Implementing retries and error recovery strategies
- Monitoring and observability for distributed systems

## Quick Start

### Basic Multi-Agent Orchestration

Here's a minimal example:

```python
import asyncio
from typing import List, Dict, Any

class SimpleOrchestrator:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent_id: str, agent_type: str):
        self.agents[agent_id] = {"type": agent_type, "busy": False}

    async def execute_task(self, agent_id: str, task: Dict[str, Any]) -> Any:
        print(f"Agent {agent_id} executing: {task['name']}")
        await asyncio.sleep(1)
        return {"status": "completed", "result": f"Result of {task['name']}"}

    async def orchestrate(self, tasks: List[Dict[str, Any]]) -> List[Any]:
        results = await asyncio.gather(*[
            self.execute_task(f"agent_{i}", task)
            for i, task in enumerate(tasks)
        ])
        return results

# Usage
async def main():
    orchestrator = SimpleOrchestrator()
    orchestrator.register_agent("agent_0", "analyzer")
    orchestrator.register_agent("agent_1", "security")

    tasks = [
        {"name": "analyze_code", "type": "analysis"},
        {"name": "scan_security", "type": "security"}
    ]

    results = await orchestrator.orchestrate(tasks)
    print(f"Results: {results}")

asyncio.run(main())
```

## Core Orchestration Concepts

### 1. DAG (Directed Acyclic Graph) Pattern

Tasks execute based on dependencies, enabling parallel execution where possible.

```
Start
  │
  ├──► Task A ──┐
  │            │
  └──► Task B ──┼──► Task D ──► Task F ──► End
       │        │
       └──► Task C ──► Task E ───┘
```

**Use when:** You have tasks with clear dependencies and want parallel execution.

### 2. State Machine Pattern

Workflows transition through defined states with explicit transitions.

```
     ┌─────────┐
     │  IDLE   │
     └────┬────┘
          │ start()
     ┌────▼────┐
     │ RUNNING │◄──────┐
     └────┬────┘       │
          │            │ retry()
    ┌─────┴─────┐      │
    │           │      │
┌───▼───┐   ┌───▼───┐  │
│SUCCESS│   │FAILURE├──┘
└───────┘   └───┬───┘
                │ max_retries
            ┌───▼───┐
            │ ERROR │
            └───────┘
```

**Use when:** You need explicit state tracking and complex transition logic.

### 3. Event-Driven Pattern

Agents communicate via events and messages (pub/sub, message queues).

```
┌──────────┐      ┌─────────────┐      ┌──────────┐
│ Agent A  │─────►│  Event Bus  │─────►│ Agent B  │
└──────────┘      └─────────────┘      └──────────┘
                        │
                        ▼
                  ┌──────────┐
                  │ Agent C  │
                  └──────────┘
```

**Use when:** Agents need loose coupling and async communication.

### 4. Orchestrator Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Orchestrator                       │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Task Queue  │  │ State Manager│  │ Scheduler │ │
│  └─────────────┘  └──────────────┘  └───────────┘ │
└──────────────┬──────────────────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
   ┌───▼───┐       ┌───▼───┐       ┌────────┐
   │Agent 1│       │Agent 2│       │Agent N │
   │       │       │       │       │        │
   │Task A │       │Task B │       │Task N  │
   └───┬───┘       └───┬───┘       └───┬────┘
       │               │               │
       └───────┬───────┴───────────────┘
               │
         ┌─────▼─────┐
         │  Results  │
         │Aggregator │
         └───────────┘
```

## Critical Gotchas

### 1. Retry Storms
**Problem:** Failed tasks retry simultaneously, overwhelming systems.
**Solution:** Use exponential backoff with jitter, circuit breakers, and max retry limits. See [GOTCHAS.md](./GOTCHAS.md#retry-storms) for details.

### 2. State Management Complexity
**Problem:** Losing track of workflow state across restarts.
**Solution:** Use durable execution platforms (Temporal), persist state externally, make tasks idempotent. See [GOTCHAS.md](./GOTCHAS.md#state-management) for details.

### 3. Serialization Issues
**Problem:** Large data passed between tasks causes memory issues.
**Solution:** Pass references (S3 URLs) not data, use streaming, implement chunking. See [GOTCHAS.md](./GOTCHAS.md#serialization) for details.

For all common gotchas and solutions, see [GOTCHAS.md](./GOTCHAS.md).

## Orchestration Patterns

This framework provides 7 production-ready patterns:

1. **Multi-Agent Task Decomposition** - Break complex objectives into subtasks
2. **Airflow DAG Coordination** - Orchestrate agents with Apache Airflow
3. **Temporal Durable Execution** - Long-running workflows with automatic retries
4. **Event-Driven Coordination** - Pub/Sub messaging for loose coupling
5. **Circuit Breaker Pattern** - Prevent cascading failures
6. **Resource Pool with Load Balancing** - Manage agent resources efficiently
7. **Distributed Tracing** - Monitor and debug distributed workflows

See [PATTERNS.md](./PATTERNS.md) for detailed pattern descriptions and when to use each.

## Working Examples

All patterns include complete, runnable code examples:

- **Multi-Agent Orchestrator** - Coordinate specialized agents with dependency resolution
- **Airflow DAG** - Production DAG for agent coordination with XCom
- **Temporal Workflow** - Durable workflow with activities and retry policies
- **Event-Driven System** - Redis-based pub/sub for agent communication
- **Circuit Breaker** - Fault-tolerant agent calls with state management
- **Resource Pool** - Load-balanced agent pool with multiple strategies
- **Distributed Tracing** - OpenTelemetry-style tracing for workflows

See [EXAMPLES.md](./EXAMPLES.md) for complete code examples you can copy and adapt.

## Framework Selection

Choose the right orchestration framework for your needs:

| Framework | Best For | Key Strength | Learn More |
|-----------|----------|--------------|------------|
| **Airflow** | Batch ETL, scheduled jobs | Rich UI, Python DAGs | [KNOWLEDGE.md](./KNOWLEDGE.md#airflow) |
| **Temporal** | Long-running workflows | Durable execution | [KNOWLEDGE.md](./KNOWLEDGE.md#temporal) |
| **Prefect** | Data science, dynamic flows | Pythonic API | [KNOWLEDGE.md](./KNOWLEDGE.md#prefect) |
| **Celery** | Distributed task queues | Real-time tasks | [KNOWLEDGE.md](./KNOWLEDGE.md#celery) |
| **Step Functions** | AWS serverless workflows | No infrastructure | [KNOWLEDGE.md](./KNOWLEDGE.md#step-functions) |

See [KNOWLEDGE.md](./KNOWLEDGE.md) for detailed framework comparisons, concepts, and learning resources.

## Best Practices

### DO's
1. **Design for Idempotency** - Tasks should be safely retryable without side effects
2. **Use Correlation IDs** - Track requests across distributed systems
3. **Implement Timeouts** - Every operation should have a timeout
4. **Monitor Everything** - Metrics, logs, traces for all components
5. **Implement Circuit Breakers** - Prevent cascading failures
6. **Use Exponential Backoff** - Space out retries to avoid thundering herd
7. **Validate DAGs** - Check for cycles before execution
8. **Version Workflows** - Track workflow changes over time

### DON'Ts
1. **Don't Pass Large Data** - Use references (S3 URLs, database IDs) instead
2. **Don't Ignore Partial Failures** - Handle them explicitly
3. **Don't Use Distributed Transactions** - Use saga pattern instead
4. **Don't Synchronous Chain** - Use async/parallel execution where possible
5. **Don't Skip Health Checks** - Monitor agent health continuously
6. **Don't Hardcode Timeouts** - Make them configurable per task type
7. **Don't Trust Clocks** - Use logical ordering, not wall clock time
8. **Don't Forget Cleanup** - Clean up zombie workflows and stale state

See [REFERENCE.md](./REFERENCE.md#best-practices) for extended best practices guide.

## Production Deployment

### Essential Checklist

Before deploying orchestrated workflows to production:

- [ ] Define clear task boundaries and responsibilities
- [ ] Implement comprehensive error handling and retries
- [ ] Set up distributed tracing (OpenTelemetry, Jaeger)
- [ ] Configure monitoring and alerting (Prometheus, Grafana)
- [ ] Implement circuit breakers for external dependencies
- [ ] Use message queues for async communication (RabbitMQ, Kafka)
- [ ] Set up health checks for all agents
- [ ] Implement graceful shutdown handling
- [ ] Configure resource limits and quotas
- [ ] Set up log aggregation (ELK, Loki)

See [REFERENCE.md](./REFERENCE.md#production-deployment) for complete deployment guide.

## Documentation Structure

This skill is organized for progressive disclosure:

- **SKILL.md** (this file) - Quick start, core concepts, overview
- **[KNOWLEDGE.md](./KNOWLEDGE.md)** - Frameworks, theory, distributed systems concepts
- **[PATTERNS.md](./PATTERNS.md)** - Implementation patterns and when to use them
- **[EXAMPLES.md](./EXAMPLES.md)** - Complete working code examples
- **[GOTCHAS.md](./GOTCHAS.md)** - Common pitfalls and troubleshooting
- **[REFERENCE.md](./REFERENCE.md)** - API docs, configuration, production deployment

## Related Skills

- `multi-agent-coordination-framework` - For advanced agent architectures
- `mcp-integration-toolkit` - For agent communication via MCP protocol
- `git-mastery-suite` - For orchestrating Git-based workflows
- `security-scanning-suite` - For security orchestration and SAST/DAST coordination

## Learning Path

1. **Start Here:** Read this SKILL.md for quick start and core concepts
2. **Choose Framework:** Review [KNOWLEDGE.md](./KNOWLEDGE.md) to select your orchestration framework
3. **Pick Pattern:** Browse [PATTERNS.md](./PATTERNS.md) to find the pattern matching your use case
4. **Copy Code:** Use [EXAMPLES.md](./EXAMPLES.md) to get working code
5. **Avoid Pitfalls:** Check [GOTCHAS.md](./GOTCHAS.md) for common mistakes
6. **Go to Production:** Follow [REFERENCE.md](./REFERENCE.md) deployment guide

## Quick Reference

### Common Operations

```python
# Register agents
orchestrator.register_agent(agent_id, agent_type, capacity)

# Submit task
result = await orchestrator.execute_task(task)

# Execute workflow
results = await orchestrator.execute_workflow(tasks)

# Check circuit breaker status
status = circuit_breaker.get_state()

# Monitor resource pool
status = resource_pool.get_pool_status()
```

### Key Metrics to Monitor

- Task queue depth
- Agent utilization (%)
- Task success rate (%)
- Average task duration
- Circuit breaker state
- Error rate by agent type

See [REFERENCE.md](./REFERENCE.md#monitoring) for complete monitoring guide.
