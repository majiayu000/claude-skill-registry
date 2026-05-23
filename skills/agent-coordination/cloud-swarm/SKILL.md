---
name: cloud-swarm
description: AI swarm orchestration and management in Flow Nexus cloud. Use for deploying, coordinating, and scaling multi-agent swarms for complex task execution.
version: 1.0.0
category: cloud
type: skill
capabilities:
  - swarm_initialization
  - agent_deployment
  - task_orchestration
  - swarm_scaling
  - performance_monitoring
  - lifecycle_management
tools:
  - mcp__flow-nexus__swarm_init
  - mcp__flow-nexus__agent_spawn
  - mcp__flow-nexus__task_orchestrate
  - mcp__flow-nexus__swarm_status
  - mcp__flow-nexus__swarm_scale
  - mcp__flow-nexus__swarm_destroy
  - mcp__flow-nexus__swarm_list
  - mcp__flow-nexus__swarm_templates_list
  - mcp__flow-nexus__swarm_create_from_template
related_skills:
  - cloud-workflow
  - cloud-neural
  - cloud-sandbox
---

# Cloud Swarm Orchestration

> Deploy, coordinate, and scale multi-agent swarms in Flow Nexus cloud for complex task execution.

## Quick Start

```javascript
// Initialize a swarm with mesh topology
mcp__flow-nexus__swarm_init({
  topology: "mesh",
  maxAgents: 8,
  strategy: "balanced"
})

// Deploy specialized agents
mcp__flow-nexus__agent_spawn({ type: "researcher", name: "Lead Researcher" })
mcp__flow-nexus__agent_spawn({ type: "coder", name: "Implementation Expert" })

// Orchestrate a complex task
mcp__flow-nexus__task_orchestrate({
  task: "Build authentication API with JWT tokens",
  strategy: "parallel",
  priority: "high"
})
```

## When to Use

- Deploying multi-agent systems for complex problem-solving
- Orchestrating parallel task execution across specialized agents
- Scaling AI workloads dynamically based on requirements
- Coordinating distributed workflows with agent collaboration
- Setting up hierarchical or mesh-based agent coordination

## Prerequisites

- Flow Nexus account with active session
- MCP server `flow-nexus` configured: `claude mcp add flow-nexus npx flow-nexus@latest mcp start`
- Sufficient rUv credits for agent deployment

## Core Concepts

### Swarm Topologies

| Topology | Description | Best For |
|----------|-------------|----------|
| **Hierarchical** | Queen-led coordination with central control | Complex projects requiring oversight |
| **Mesh** | Peer-to-peer distributed network | Collaborative problem-solving |
| **Ring** | Circular coordination pattern | Sequential processing workflows |
| **Star** | Centralized hub-and-spoke | Single-objective focused tasks |

### Agent Types

| Type | Specialization |
|------|----------------|
| `researcher` | Information gathering and analysis |
| `coder` | Implementation and development |
| `analyst` | Data processing and pattern recognition |
| `optimizer` | Performance tuning and efficiency |
| `coordinator` | Workflow management and orchestration |

### Distribution Strategies

- **balanced**: Even distribution across agent capabilities
- **specialized**: Focus on specific agent types for task needs
- **adaptive**: Dynamic adjustment based on workload

## MCP Tools Reference

### Swarm Initialization

```javascript
mcp__flow-nexus__swarm_init({
  topology: "hierarchical",  // mesh, ring, star, hierarchical
  maxAgents: 8,              // Maximum agents in swarm (1-100)
  strategy: "balanced"       // balanced, specialized, adaptive
})
// Returns: { swarm_id, topology, status, agents: [] }
```

### Agent Deployment

```javascript
mcp__flow-nexus__agent_spawn({
  type: "researcher",        // researcher, coder, analyst, optimizer, coordinator
  name: "Agent Name",        // Custom identifier
  capabilities: ["web_search", "analysis", "summarization"]
})
// Returns: { agent_id, type, name, status, capabilities }
```

### Task Orchestration

```javascript
mcp__flow-nexus__task_orchestrate({
  task: "Task description",  // What to accomplish
  strategy: "parallel",      // parallel, sequential, adaptive
  maxAgents: 5,              // Agents to assign (1-10)
  priority: "high"           // low, medium, high, critical
})
// Returns: { task_id, status, assigned_agents, strategy }
```

### Swarm Management

```javascript
// Check swarm status
mcp__flow-nexus__swarm_status({ swarm_id: "optional" })

// List all swarms
mcp__flow-nexus__swarm_list({ status: "active" })  // active, destroyed, all

// Scale swarm
mcp__flow-nexus__swarm_scale({ target_agents: 10 })

// Destroy swarm
mcp__flow-nexus__swarm_destroy({ swarm_id: "id" })
```

### Template-Based Creation

```javascript
// List available templates
mcp__flow-nexus__swarm_templates_list({
  category: "quickstart",    // quickstart, specialized, enterprise, custom, all
  includeStore: true
})

// Create from template
mcp__flow-nexus__swarm_create_from_template({
  template_id: "template_id",
  overrides: { maxAgents: 10, strategy: "adaptive" }
})
```

## Usage Examples

### Example 1: Research and Development Swarm

```javascript
// Step 1: Initialize hierarchical swarm for R&D
const swarm = await mcp__flow-nexus__swarm_init({
  topology: "hierarchical",
  maxAgents: 6,
  strategy: "specialized"
});

// Step 2: Deploy specialized agents
await mcp__flow-nexus__agent_spawn({
  type: "researcher",
  name: "Market Researcher",
  capabilities: ["web_search", "trend_analysis"]
});

await mcp__flow-nexus__agent_spawn({
  type: "analyst",
  name: "Data Analyst",
  capabilities: ["data_processing", "visualization"]
});

await mcp__flow-nexus__agent_spawn({
  type: "coder",
  name: "Prototype Developer",
  capabilities: ["rapid_prototyping", "api_development"]
});

// Step 3: Orchestrate research task
await mcp__flow-nexus__task_orchestrate({
  task: "Research competitor authentication solutions and prototype an improved version",
  strategy: "sequential",
  maxAgents: 3,
  priority: "high"
});

// Step 4: Monitor progress
const status = await mcp__flow-nexus__swarm_status();
console.log(`Active agents: ${status.agents.length}, Tasks: ${status.active_tasks}`);
```

### Example 2: Parallel Processing with Mesh Topology

```javascript
// Initialize mesh for collaborative processing
await mcp__flow-nexus__swarm_init({
  topology: "mesh",
  maxAgents: 8,
  strategy: "balanced"
});

// Deploy multiple coders for parallel work
for (const module of ["auth", "api", "database", "frontend"]) {
  await mcp__flow-nexus__agent_spawn({
    type: "coder",
    name: `${module}-developer`,
    capabilities: ["implementation", "testing"]
  });
}

// Orchestrate parallel development
await mcp__flow-nexus__task_orchestrate({
  task: "Build microservices architecture with 4 independent modules",
  strategy: "parallel",
  maxAgents: 4,
  priority: "critical"
});

// Scale up if needed
await mcp__flow-nexus__swarm_scale({ target_agents: 12 });
```

### Example 3: Using Templates

```javascript
// List available templates
const templates = await mcp__flow-nexus__swarm_templates_list({
  category: "enterprise",
  includeStore: true
});

// Deploy from template
await mcp__flow-nexus__swarm_create_from_template({
  template_name: "full-stack-development",
  overrides: {
    maxAgents: 10,
    strategy: "adaptive"
  }
});
```

## Execution Checklist

- [ ] Verify Flow Nexus authentication status
- [ ] Choose appropriate topology for task requirements
- [ ] Initialize swarm with correct parameters
- [ ] Deploy agents with relevant capabilities
- [ ] Orchestrate tasks with suitable strategy
- [ ] Monitor swarm performance and agent utilization
- [ ] Scale swarm based on workload
- [ ] Clean up: destroy swarm when complete

## Best Practices

1. **Topology Selection**: Choose hierarchical for complex projects, mesh for collaboration, ring for sequential workflows
2. **Agent Specialization**: Deploy agents with capabilities matching task requirements
3. **Resource Efficiency**: Start with fewer agents and scale up as needed
4. **Task Decomposition**: Break complex objectives into manageable sub-tasks
5. **Monitoring**: Regularly check swarm status and agent utilization
6. **Cleanup**: Always destroy swarms when work is complete to free resources

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `swarm_init_failed` | Invalid topology or max agents | Verify topology is valid, agents between 1-100 |
| `agent_spawn_failed` | Invalid type or swarm not active | Check agent type, ensure swarm is initialized |
| `insufficient_credits` | Low rUv balance | Add credits via payment tools |
| `swarm_not_found` | Invalid swarm_id | Use `swarm_list` to get valid IDs |

## Metrics & Success Criteria

- **Agent Utilization**: Target >80% utilization during active tasks
- **Task Completion**: All orchestrated tasks complete successfully
- **Response Time**: Swarm initialization <5 seconds
- **Scaling Efficiency**: Scale operations complete <10 seconds

## Integration Points

### With Workflows

```javascript
// Create workflow that uses swarm
await mcp__flow-nexus__workflow_create({
  name: "Swarm-Powered Pipeline",
  steps: [
    { id: "init", action: "swarm_init", config: { topology: "mesh" } },
    { id: "deploy", action: "agent_spawn", depends: ["init"] },
    { id: "execute", action: "task_orchestrate", depends: ["deploy"] }
  ]
});
```

### With Sandboxes

```javascript
// Deploy agents with sandbox execution capabilities
await mcp__flow-nexus__agent_spawn({
  type: "coder",
  name: "Sandbox Developer",
  capabilities: ["sandbox_execution", "code_testing"]
});
```

### Related Skills

- [cloud-workflow](../cloud-workflow/SKILL.md) - Event-driven workflow automation
- [cloud-neural](../cloud-neural/SKILL.md) - Neural network training and deployment
- [cloud-sandbox](../cloud-sandbox/SKILL.md) - Isolated execution environments

## References

- [Flow Nexus Documentation](https://flow-nexus.ruv.io)
- [Swarm Topology Guide](https://github.com/ruvnet/claude-flow)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from flow-nexus-swarm agent
