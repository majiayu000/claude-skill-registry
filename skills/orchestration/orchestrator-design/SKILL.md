---
name: orchestrator-design
description: Design O-Agent systems for multi-agent fleet management. Use when building orchestrator agents, designing multi-agent architectures, or creating unified interfaces for agent fleet control.
allowed-tools: Read, Grep, Glob
---

# Orchestrator Design Skill

Design O-Agent (Orchestrator Agent) systems for managing fleets of specialized agents.

## Purpose

Guide the architectural design of orchestrator systems that create, command, monitor, and delete specialized agents through a single unified interface.

## When to Use

- Designing multi-agent systems
- Building fleet management architecture
- Creating scalable agent workflows
- Implementing the Single Interface Pattern

## Prerequisites

- Understanding of the Three Pillars (@three-pillars-orchestration.md)
- Familiarity with agent lifecycle patterns (@agent-lifecycle-crud.md)
- Access to Claude Agent SDK documentation

## SDK Requirement

> **Implementation Note**: Orchestrator patterns require Claude Agent SDK with custom MCP tools. Claude Code subagents cannot spawn other subagents.

## Design Process

### Step 1: Define Orchestration Scope

Answer these questions:

- What workflows will be orchestrated?
- What agent types are needed?
- What is the expected scale?
- What observability is required?

**Output**: Scope document (requirements and constraints)

### Step 2: Design Agent Templates

For each agent type needed:

| Template | Purpose | Model | Tools |
| --- | --- | --- | --- |
| scout-fast | Quick reconnaissance | Haiku | Read, Glob, Grep |
| builder | Code implementation | Sonnet | Read, Write, Edit, Bash |
| reviewer | Code review | Sonnet | Read, Grep, Glob, Bash |
| planner | Task planning | Sonnet | Read, Glob, Grep |

**Template Structure**:

```yaml
---
name: template-name
description: What this agent does
tools: [tool1, tool2]
model: sonnet|haiku
---

# System Prompt

[Agent-specific instructions]
```

### Step 3: Design Orchestrator System Prompt

The orchestrator needs a specific identity:

```markdown
# Orchestrator Agent

## Purpose
Manage and coordinate specialized agents to accomplish complex tasks.
You do NOT perform work directly - you orchestrate other agents.

## Capabilities
- Create specialized agents from templates
- Command agents with detailed prompts
- Monitor agent progress
- Aggregate and report results
- Delete agents when work is complete

## Workflow Pattern
1. Analyze task requirements
2. Create appropriate agents
3. Command agents with detailed instructions
4. Monitor progress
5. Aggregate results
6. Report to user
7. Delete agents

## Context Protection
- Keep your context focused on orchestration
- Delegate detailed work to specialized agents
- Do not read files directly
- Do not write code
```

### Step 4: Define Management Tools

Design the MCP tools for agent management:

| Tool | Purpose | Parameters |
| --- | --- | --- |
| `create_agent` | Spin up new agent | template, name |
| `command_agent` | Send prompt to agent | agent_id, prompt |
| `check_agent_status` | Get agent progress | agent_id |
| `list_agents` | View all active agents | - |
| `delete_agent` | Clean up agent | agent_id |
| `read_agent_logs` | View agent responses | agent_id |

### Step 5: Design Observability Layer

Essential metrics to track:

| Metric | Purpose |
| --- | --- |
| Agent status | Know what's running |
| Context usage | Monitor token consumption |
| Costs | Track spend per agent |
| Tool calls | See what agents are doing |
| Results | Verify outputs |
| Time | Measure execution duration |

**Observability Components**:

1. Agent Cards - Status, model, context, cost per agent
2. Event Stream - Real-time log of all activities
3. Cost Tracking - Per-agent and total costs
4. Result Inspector - consumed/produced assets
5. Log Viewer - Filterable activity history

### Step 6: Design Workflow Phases

Standard orchestration workflow:

```text
Phase 1: Scout
├── Create scouts (parallel)
├── Command each with specific area
├── Monitor until complete
└── Aggregate findings

Phase 2: Build
├── Create builder
├── Command with scout reports
├── Monitor implementation
└── Aggregate changes

Phase 3: Review
├── Create reviewer
├── Command to verify implementation
├── Monitor review
└── Generate final report

Cleanup: Delete all agents
```

### Step 7: Plan Deployment Architecture

Required components for SDK implementation:

| Component | Purpose |
| --- | --- |
| Claude Agent SDK | Core orchestration |
| MCP Servers | Agent management tools |
| Database | Agent state persistence |
| WebSocket | Real-time updates |
| UI/CLI | User interface |

## Output Format

When designing an orchestrator system, provide:

```markdown
## Orchestrator System Design

**Name:** [system-name]
**Purpose:** [1-2 sentences]
**Scale:** [expected agent count and concurrency]

### Agent Templates

| Template | Purpose | Model | Tools |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

### Orchestrator Configuration

**System Prompt:** [included or file reference]
**Management Tools:** [list of MCP tools]
**Observability:** [metrics and components]

### Workflow Design

[Phase diagram with agent creation/deletion points]

### Architecture

[Deployment diagram with components]

### Implementation Notes

[SDK considerations, constraints, scaling factors]
```

## Design Checklist

- [ ] Orchestration scope defined
- [ ] Agent templates designed
- [ ] Orchestrator system prompt written
- [ ] Management tools specified
- [ ] Observability layer planned
- [ ] Workflow phases designed
- [ ] Deployment architecture planned

## Anti-Patterns

| Avoid | Why | Instead |
| --- | --- | --- |
| Orchestrator doing work | Context pollution | Delegate everything |
| Missing observability | Flying blind | Track all metrics |
| Keeping dead agents | Resource waste | Delete when done |
| No lifecycle management | Can't scale | CRUD operations |
| Generic agents | Unfocused work | Specialized templates |

## Cross-References

- @three-pillars-orchestration.md - Framework foundation
- @single-interface-pattern.md - O-Agent architecture
- @agent-lifecycle-crud.md - Lifecycle management
- @multi-agent-context-protection.md - Context boundaries
- @results-oriented-engineering.md - Result patterns

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
