---
name: cloud-workflow
description: Event-driven workflow automation in Flow Nexus cloud. Use for creating, executing, and managing complex automated workflows with message queue processing and intelligent agent coordination.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - workflow_creation
  - workflow_execution
  - agent_assignment
  - queue_management
  - audit_tracking
  - event_triggers
tools:
  - mcp__flow-nexus__workflow_create
  - mcp__flow-nexus__workflow_execute
  - mcp__flow-nexus__workflow_status
  - mcp__flow-nexus__workflow_list
  - mcp__flow-nexus__workflow_agent_assign
  - mcp__flow-nexus__workflow_queue_status
  - mcp__flow-nexus__workflow_audit_trail
related_skills:
  - cloud-swarm
  - cloud-sandbox
  - cloud-neural
---

# Cloud Workflow

> Design and orchestrate event-driven automation workflows with intelligent agent coordination and message queue processing.

## Quick Start

```javascript
// Create a CI/CD workflow
const workflow = await mcp__flow-nexus__workflow_create({
  name: "CI/CD Pipeline",
  description: "Automated testing and deployment",
  steps: [
    { id: "test", action: "run_tests", agent: "tester" },
    { id: "build", action: "build_app", agent: "builder" },
    { id: "deploy", action: "deploy_prod", agent: "deployer" }
  ],
  triggers: ["push_to_main", "manual_trigger"]
});

// Execute the workflow
await mcp__flow-nexus__workflow_execute({
  workflow_id: workflow.workflow_id,
  input_data: { branch: "main" },
  async: true
});
```

## When to Use

- Automating CI/CD pipelines with multiple stages
- Orchestrating data processing and ETL workflows
- Creating event-driven automation for business processes
- Managing multi-stage review and approval workflows
- Scheduling recurring automated tasks
- Coordinating complex multi-agent collaboration

## Prerequisites

- Flow Nexus account with active session
- MCP server `flow-nexus` configured
- Sufficient rUv credits for workflow execution

## Core Concepts

### Workflow Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **CI/CD Pipeline** | Test, build, deploy sequence | Software deployment |
| **Data Processing** | ETL with validation steps | Data engineering |
| **Multi-Stage Review** | Automated analysis + approval | Code review |
| **Event-Driven** | Reactive to external events | Webhooks, notifications |
| **Scheduled** | Time-based execution | Recurring tasks |
| **Conditional** | Branching logic and decisions | Complex business rules |

### Execution Strategies

- **Sequential**: Steps run one after another
- **Parallel**: Independent steps run simultaneously
- **Conditional**: Steps execute based on conditions

### Agent Assignment

Workflows can automatically assign optimal agents to tasks using:
- **Explicit Assignment**: Specify agent type per step
- **Vector Similarity**: AI-powered matching based on task requirements

## MCP Tools Reference

### Workflow Creation

```javascript
mcp__flow-nexus__workflow_create({
  name: "Workflow Name",
  description: "Workflow description",
  steps: [
    {
      id: "step1",
      action: "action_name",
      agent: "agent_type",     // Optional: auto-assigned if not specified
      config: {}               // Step-specific configuration
    },
    {
      id: "step2",
      action: "action_name",
      depends: ["step1"]       // Dependencies on other steps
    }
  ],
  triggers: ["trigger1", "trigger2"],  // Event triggers
  priority: 5,                 // Priority 0-10
  metadata: {}                 // Additional metadata
})
// Returns: { workflow_id, name, status, created_at }
```

### Workflow Execution

```javascript
mcp__flow-nexus__workflow_execute({
  workflow_id: "workflow_id",
  input_data: {                // Input data for execution
    key: "value"
  },
  async: true                  // Execute asynchronously via queue
})
// Returns: { execution_id, status, started_at }
```

### Status and Monitoring

```javascript
// Get workflow status
mcp__flow-nexus__workflow_status({
  workflow_id: "workflow_id",
  execution_id: "execution_id",  // Optional: specific execution
  include_metrics: true
})
// Returns: { status, progress, metrics, step_results }

// List all workflows
mcp__flow-nexus__workflow_list({
  status: "active",            // Filter by status
  limit: 10,
  offset: 0
})

// Check message queue status
mcp__flow-nexus__workflow_queue_status({
  queue_name: "queue_name",    // Optional: specific queue
  include_messages: true
})
```

### Agent Assignment

```javascript
mcp__flow-nexus__workflow_agent_assign({
  task_id: "task_id",
  agent_type: "coder",         // Preferred agent type
  use_vector_similarity: true  // Use AI matching
})
// Returns: { agent_id, type, match_score }
```

### Audit Trail

```javascript
mcp__flow-nexus__workflow_audit_trail({
  workflow_id: "workflow_id",
  start_time: "2026-01-01T00:00:00Z",
  limit: 50
})
// Returns: { events: [{ timestamp, action, user, details }] }
```

## Usage Examples

### Example 1: CI/CD Pipeline

```javascript
// Create comprehensive CI/CD workflow
const cicdWorkflow = await mcp__flow-nexus__workflow_create({
  name: "Full CI/CD Pipeline",
  description: "Complete testing, building, and deployment workflow",
  steps: [
    {
      id: "lint",
      action: "run_linter",
      agent: "code-analyzer",
      config: { strict: true }
    },
    {
      id: "test",
      action: "run_tests",
      agent: "tester",
      config: { coverage_threshold: 80 },
      depends: ["lint"]
    },
    {
      id: "security_scan",
      action: "security_check",
      agent: "security-analyzer",
      depends: ["lint"]
    },
    {
      id: "build",
      action: "build_app",
      agent: "builder",
      depends: ["test", "security_scan"]
    },
    {
      id: "deploy_staging",
      action: "deploy",
      agent: "deployer",
      config: { environment: "staging" },
      depends: ["build"]
    },
    {
      id: "integration_tests",
      action: "run_integration_tests",
      agent: "tester",
      depends: ["deploy_staging"]
    },
    {
      id: "deploy_prod",
      action: "deploy",
      agent: "deployer",
      config: { environment: "production" },
      depends: ["integration_tests"]
    }
  ],
  triggers: ["push_to_main", "release_tag"],
  priority: 8
});

// Execute on push
await mcp__flow-nexus__workflow_execute({
  workflow_id: cicdWorkflow.workflow_id,
  input_data: {
    branch: "main",
    commit: "abc123",
    author: "developer@example.com"
  },
  async: true
});

// Monitor progress
const status = await mcp__flow-nexus__workflow_status({
  workflow_id: cicdWorkflow.workflow_id,
  include_metrics: true
});

console.log(`Progress: ${status.progress}%, Current step: ${status.current_step}`);
```

### Example 2: Data Processing Pipeline

```javascript
// ETL workflow with validation
const etlWorkflow = await mcp__flow-nexus__workflow_create({
  name: "Data ETL Pipeline",
  description: "Extract, transform, and load data with validation",
  steps: [
    {
      id: "extract",
      action: "extract_data",
      agent: "data-extractor",
      config: { source: "s3://bucket/raw-data" }
    },
    {
      id: "validate",
      action: "validate_schema",
      agent: "data-validator",
      depends: ["extract"]
    },
    {
      id: "transform",
      action: "transform_data",
      agent: "data-transformer",
      config: { rules: ["normalize", "dedupe", "enrich"] },
      depends: ["validate"]
    },
    {
      id: "quality_check",
      action: "run_quality_checks",
      agent: "data-analyst",
      depends: ["transform"]
    },
    {
      id: "load",
      action: "load_to_warehouse",
      agent: "data-loader",
      config: { target: "postgres://warehouse" },
      depends: ["quality_check"]
    }
  ],
  triggers: ["schedule:0 2 * * *", "manual_trigger"]  // Daily at 2 AM
});

// Manual execution
await mcp__flow-nexus__workflow_execute({
  workflow_id: etlWorkflow.workflow_id,
  input_data: { date: "2026-01-02" }
});
```

### Example 3: Multi-Stage Code Review

```javascript
// Automated code review workflow
const reviewWorkflow = await mcp__flow-nexus__workflow_create({
  name: "Automated Code Review",
  description: "Multi-stage code analysis and review",
  steps: [
    {
      id: "static_analysis",
      action: "run_static_analysis",
      agent: "code-analyzer"
    },
    {
      id: "security_review",
      action: "security_scan",
      agent: "security-reviewer",
      depends: ["static_analysis"]
    },
    {
      id: "performance_review",
      action: "analyze_performance",
      agent: "perf-analyzer",
      depends: ["static_analysis"]
    },
    {
      id: "ai_review",
      action: "ai_code_review",
      agent: "ai-reviewer",
      depends: ["static_analysis"]
    },
    {
      id: "compile_report",
      action: "generate_report",
      agent: "report-generator",
      depends: ["security_review", "performance_review", "ai_review"]
    }
  ],
  triggers: ["pull_request_opened", "pull_request_updated"]
});

// Assign optimal agent dynamically
await mcp__flow-nexus__workflow_agent_assign({
  task_id: "security_review_123",
  use_vector_similarity: true
});
```

### Example 4: Queue Management

```javascript
// Check queue status
const queueStatus = await mcp__flow-nexus__workflow_queue_status({
  include_messages: true
});

console.log(`Pending messages: ${queueStatus.pending}`);
console.log(`Processing: ${queueStatus.processing}`);

// Review audit trail
const audit = await mcp__flow-nexus__workflow_audit_trail({
  workflow_id: "workflow_id",
  limit: 100
});

for (const event of audit.events) {
  console.log(`${event.timestamp}: ${event.action} by ${event.user}`);
}
```

## Execution Checklist

- [ ] Define workflow steps and dependencies
- [ ] Assign or auto-assign agents to steps
- [ ] Configure triggers (events, schedules)
- [ ] Set workflow priority
- [ ] Create the workflow
- [ ] Execute with appropriate input data
- [ ] Monitor progress and step status
- [ ] Review audit trail for compliance
- [ ] Clean up or archive completed workflows

## Best Practices

1. **Step Granularity**: Break complex tasks into atomic steps for better monitoring
2. **Dependency Chains**: Carefully plan dependencies to maximize parallelism
3. **Error Handling**: Include retry logic and fallback steps
4. **Async Execution**: Use async mode for long-running workflows
5. **Agent Matching**: Leverage vector similarity for optimal agent assignment
6. **Audit Compliance**: Regularly review audit trails for security

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `workflow_create_failed` | Invalid step configuration | Verify step IDs and dependencies |
| `execution_failed` | Step error or timeout | Check step logs, increase timeout |
| `agent_assignment_failed` | No suitable agent available | Specify alternative agent type |
| `queue_overflow` | Too many pending messages | Scale workers or reduce rate |
| `circular_dependency` | Steps reference each other | Review dependency graph |

## Metrics & Success Criteria

- **Workflow Completion Rate**: Target >95%
- **Average Execution Time**: Track per workflow type
- **Queue Latency**: <10 seconds for async jobs
- **Agent Utilization**: >80% during active workflows
- **Error Rate**: <5% per workflow type

## Integration Points

### With Swarms

```javascript
// Swarm-powered workflow
const swarm = await mcp__flow-nexus__swarm_init({ topology: "mesh" });

await mcp__flow-nexus__workflow_create({
  name: "Swarm Workflow",
  steps: [
    { id: "task", action: "swarm_execute", config: { swarm_id: swarm.swarm_id } }
  ]
});
```

### With Sandboxes

```javascript
// Sandbox execution in workflow
await mcp__flow-nexus__workflow_create({
  name: "Sandbox Pipeline",
  steps: [
    { id: "create", action: "sandbox_create", config: { template: "node" } },
    { id: "test", action: "sandbox_execute", depends: ["create"] },
    { id: "cleanup", action: "sandbox_delete", depends: ["test"] }
  ]
});
```

### Related Skills

- [cloud-swarm](../cloud-swarm/SKILL.md) - Multi-agent orchestration
- [cloud-sandbox](../cloud-sandbox/SKILL.md) - Isolated execution environments
- [cloud-neural](../cloud-neural/SKILL.md) - Neural network operations

## References

- [Flow Nexus Workflow Documentation](https://flow-nexus.ruv.io)
- [Event-Driven Architecture Patterns](https://github.com/ruvnet/claude-flow)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-workflow agent
