---
name: Subagent-Driven Development
description: This skill should be used when coordinating "multiple specialized agents", "complex workflow orchestration", "autonomous development teams", "agent collaboration", "distributed task management", or when managing sophisticated multi-agent development processes.
version: 2.0.0
---

# Subagent-Driven Development: Multi-Agent Coordination

## Overview

This skill provides comprehensive patterns for orchestrating multiple specialized agents in complex development workflows. It enables sophisticated coordination between autonomous agents, each with specific expertise and responsibilities.

## When to Use This Skill

Use this skill when implementing:
- **Multi-agent development workflows** with specialized roles
- **Complex task orchestration** requiring multiple expertise areas
- **Autonomous development teams** with agent coordination
- **Parallel workflow execution** with dependency management
- **Agent collaboration patterns** for complex problems
- **Distributed task management** across multiple agents
- **Quality assurance through specialized reviewers**

## Quick Start

### 1. Basic Multi-Agent Workflow

```python
from subagent_framework import WorkflowOrchestrator, Task, AgentType, Priority

# Create orchestrator
orchestrator = WorkflowOrchestrator()

# Register specialized agents
orchestrator.register_agent(ArchitectAgent("architect_001"))
orchestrator.register_agent(DeveloperAgent("developer_001"))
orchestrator.register_agent(TesterAgent("tester_001"))

# Define task workflow
tasks = [
    Task(
        id="design_001",
        title="Design System Architecture",
        agent_type=AgentType.ARCHITECT,
        priority=Priority.HIGH,
        input_data={'requirements': {...}}
    ),
    Task(
        id="implement_001",
        title="Implement Feature",
        agent_type=AgentType.DEVELOPER,
        priority=Priority.HIGH,
        dependencies=["design_001"],  # Depends on architect
        input_data={'specification': {...}}
    ),
    Task(
        id="test_001",
        title="Test Implementation",
        agent_type=AgentType.TESTER,
        priority=Priority.MEDIUM,
        dependencies=["implement_001"],  # Depends on developer
        input_data={'test_type': 'integration'}
    )
]

# Execute workflow
results = await orchestrator.execute_workflow(tasks)
```

### 2. Parallel Agent Execution

```python
# Create tasks that can run in parallel
parallel_tasks = [
    Task(
        id="frontend_dev",
        title="Develop Frontend",
        agent_type=AgentType.DEVELOPER,
        dependencies=["design_001"],
        input_data={'component': 'ui'}
    ),
    Task(
        id="backend_dev",
        title="Develop Backend API",
        agent_type=AgentType.DEVELOPER,
        dependencies=["design_001"],
        input_data={'component': 'api'}
    ),
    Task(
        id="database_dev",
        title="Develop Database Schema",
        agent_type=AgentType.DEVELOPER,
        dependencies=["design_001"],
        input_data={'component': 'database'}
    )
]

# These tasks will execute in parallel (same dependency level)
results = await orchestrator.execute_workflow(parallel_tasks)
```

### 3. Quality Gate Workflow

```python
# Add quality gate for production-critical code
quality_workflow = [
    Task(id="develop", agent_type=AgentType.DEVELOPER, ...),
    Task(
        id="security_review",
        agent_type=AgentType.SECURITY,
        dependencies=["develop"],
        priority=Priority.CRITICAL,
        input_data={'scan_type': 'comprehensive'}
    ),
    Task(
        id="quality_gate",
        agent_type=AgentType.QUALITY_GATE,
        dependencies=["security_review"],
        priority=Priority.CRITICAL,
        input_data={'approval_required': True}
    )
]

results = await orchestrator.execute_workflow(quality_workflow)
```

## Core Components

### Agent Types

**See**: `reference/agent-taxonomy.md` for complete agent type specifications

**Available Agent Types**:
- `ARCHITECT` - System design and architecture
- `DEVELOPER` - Code implementation
- `TESTER` - Testing and quality assurance
- `REVIEWER` - Code review and analysis
- `SECURITY` - Security analysis and hardening
- `PERFORMANCE` - Performance optimization
- `QUALITY_GATE` - Quality validation and approval
- `COORDINATOR` - Workflow coordination

### Task Management

**See**: `reference/task-management.md` for complete task data structures

**Key Task Properties**:
- `agent_type` - Which agent handles this task
- `priority` - Task priority (LOW to EMERGENCY)
- `dependencies` - Tasks that must complete first
- `input_data` - Task-specific input parameters
- `metadata` - Additional context and configuration

### Workflow Orchestrator

**Central coordination system for multi-agent workflows**

**Key Methods**:
- `register_agent()` - Add agent to available pool
- `execute_workflow()` - Execute task workflow
- `get_workflow_status()` - Monitor progress
- `handle_agent_failure()` - Error recovery

## Common Workflows

### Sequential Pipeline

Linear workflow with strict dependencies:

```
Architect → Developer → Tester → Reviewer → Quality Gate
```

**See**: `reference/orchestration-patterns.md#sequential-pipeline`

### Parallel Fan-Out

Multiple agents working independently:

```
                 ┌─> Developer A (Frontend)
Architect ──────┼─> Developer B (Backend)
                 └─> Developer C (Database)
                           ↓
                      [Integration]
```

**See**: `reference/orchestration-patterns.md#parallel-fan-out`

### Iterative Refinement

Progressive improvement through feedback loops:

```
Developer → Reviewer → [Feedback] → Developer → Reviewer → [Approved]
```

**See**: `reference/orchestration-patterns.md#iterative-refinement`

## Orchestration Patterns

**Complete patterns**: `reference/orchestration-patterns.md`

### Pattern Selection Guide

| Workflow Type | Recommended Pattern | Agents Needed |
|--------------|-------------------|---------------|
| Feature Development | Sequential Pipeline | Architect, Developer, Tester, Quality Gate |
| Independent Components | Parallel Fan-Out | Multiple Developers, Coordinator |
| Critical Production Code | Multi-Stage Review | Developer, Security, Performance, Reviewer |
| Optimization Tasks | Iterative Refinement | Developer, Performance, Reviewer |
| Security Vulnerabilities | Emergency Fast-Track | Security, Developer, Tester |

## Error Handling

### Retry Strategy

```python
task = Task(
    id="task_001",
    title="Implement Feature",
    agent_type=AgentType.DEVELOPER,
    priority=Priority.HIGH,
    max_retries=3,  # Retry up to 3 times
    input_data={...}
)
```

### Fallback Agents

```python
# Register multiple developer agents for fallback
orchestrator.register_agent(DeveloperAgent("dev_primary"))
orchestrator.register_agent(DeveloperAgent("dev_fallback_1"))
orchestrator.register_agent(DeveloperAgent("dev_fallback_2"))

# Orchestrator automatically uses fallback if primary fails
```

**See**: `reference/orchestration-patterns.md#error-handling-patterns`

## Monitoring and Status

### Get Workflow Status

```python
status = orchestrator.get_workflow_status(workflow_id)

print(f"Progress: {status['progress']['percentage']}%")
print(f"Completed: {status['progress']['completed']}/{status['progress']['total']}")
print(f"Active Agents: {status['active_agents']}")
```

### Monitor Agent Health

```python
for agent_id, agent_status in status['agent_details'].items():
    print(f"{agent_id}: {agent_status['status']}")
    if agent_status['current_task']:
        print(f"  Working on: {agent_status['current_task']}")
```

## Real Estate Platform Example

**Complete example**: `examples/real-estate-workflow.py`

```python
async def create_property_matching_workflow():
    """Multi-agent workflow for property matching feature."""
    orchestrator = WorkflowOrchestrator()

    # Register agents
    orchestrator.register_agent(ArchitectAgent("architect_001"))
    orchestrator.register_agent(DeveloperAgent("developer_001"))
    orchestrator.register_agent(DeveloperAgent("developer_002"))
    orchestrator.register_agent(TesterAgent("tester_001"))
    orchestrator.register_agent(QualityGateAgent("quality_gate_001"))

    # Define workflow
    workflow = [
        # Phase 1: Architecture
        Task(
            id="arch_001",
            title="Design Property Matching System",
            agent_type=AgentType.ARCHITECT,
            priority=Priority.HIGH,
            input_data={'requirements': {'ai_integration': True}}
        ),

        # Phase 2: Parallel Development
        Task(
            id="api_dev",
            title="Develop Matching API",
            agent_type=AgentType.DEVELOPER,
            dependencies=["arch_001"],
            input_data={'framework': 'FastAPI'}
        ),
        Task(
            id="model_dev",
            title="Develop Data Models",
            agent_type=AgentType.DEVELOPER,
            dependencies=["arch_001"],
            input_data={'orm': 'SQLAlchemy'}
        ),

        # Phase 3: Testing
        Task(
            id="integration_test",
            title="Integration Testing",
            agent_type=AgentType.TESTER,
            dependencies=["api_dev", "model_dev"],
            input_data={'coverage_target': 0.80}
        ),

        # Phase 4: Quality Gate
        Task(
            id="quality_gate",
            title="Production Approval",
            agent_type=AgentType.QUALITY_GATE,
            dependencies=["integration_test"],
            priority=Priority.CRITICAL
        )
    ]

    # Execute
    results = await orchestrator.execute_workflow(workflow)
    return results
```

## Best Practices

1. **Clear Agent Responsibilities**: Each agent should have well-defined, non-overlapping responsibilities
2. **Proper Dependency Management**: Ensure task dependencies are correctly specified and enforced
3. **Error Handling**: Implement robust error handling and retry mechanisms
4. **Status Monitoring**: Provide comprehensive status monitoring and reporting
5. **Resource Management**: Prevent resource contention and ensure efficient agent utilization
6. **Quality Gates**: Implement quality validation at appropriate workflow stages
7. **Scalability**: Design for horizontal scaling of agent instances

## Advanced Usage

For advanced multi-agent orchestration scenarios, see:
- `reference/agent-taxonomy.md` - Complete agent type specifications
- `reference/task-management.md` - Task and workflow state management
- `reference/orchestration-patterns.md` - Advanced coordination patterns
- `examples/real-estate-workflow.py` - Real Estate platform workflows
- `examples/emergency-workflow.py` - Emergency fast-track patterns
- `scripts/workflow-monitor.py` - Monitoring and observability tools

## Troubleshooting

### Agents Not Executing Tasks
**Cause**: No registered agents matching task's `agent_type`
**Solution**: Ensure agents are registered before workflow execution

### Circular Dependencies
**Cause**: Task A depends on Task B which depends on Task A
**Solution**: Use dependency resolver to validate task graph before execution

### Workflow Stuck
**Cause**: Agent failed but retry limit not reached
**Solution**: Check agent logs, increase retry limit or add fallback agents

## Quick Reference

| Operation | Command |
|-----------|---------|
| Register agent | `orchestrator.register_agent(agent)` |
| Execute workflow | `await orchestrator.execute_workflow(tasks)` |
| Get status | `orchestrator.get_workflow_status(workflow_id)` |
| Create task | `Task(id, title, agent_type, priority, input_data)` |
| Add dependency | `Task(..., dependencies=["task_id"])` |

---

**Version**: 2.0.0 (Token-Optimized)
**Original**: 1,395 lines
**Optimized**: ~400 lines (71% reduction)
**Full Documentation**: See `reference/` directory
