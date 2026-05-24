---
name: agent-lifecycle-management
description: Manage agent fleet through CRUD operations and lifecycle patterns. Use when creating, commanding, monitoring, or deleting agents in multi-agent systems, or implementing proper resource cleanup.
allowed-tools: Read, Grep, Glob
---

# Agent Lifecycle Management Skill

Manage agent fleets through Create, Command, Monitor, and Delete operations.

## Purpose

Guide the implementation of CRUD operations for agent fleets, ensuring proper lifecycle management and resource cleanup.

## When to Use

- Setting up agent lifecycle patterns
- Implementing agent management tools
- Designing cleanup and resource management
- Building agent state tracking

## Prerequisites

- Understanding of orchestrator architecture (@single-interface-pattern.md)
- Familiarity with the Three Pillars (@three-pillars-orchestration.md)
- Access to Claude Agent SDK documentation

## SDK Requirement

> **Implementation Note**: Full lifecycle management requires Claude Agent SDK with custom MCP tools. This skill provides design patterns for SDK implementation.

## Lifecycle Pattern

```text
Create --> Command --> Monitor --> Aggregate --> Delete
|  |  |  |  |
   v          v           v            v           v
Template   Prompt      Status      Results     Cleanup
```

## CRUD Operations

### Create Operation

Spin up a new specialized agent.

**Parameters**:

- `template`: Pre-defined configuration to use
- `name`: Unique identifier for this agent
- `system_prompt`: Custom prompt (alternative to template)
- `model`: haiku, sonnet, or opus
- `allowed_tools`: Tools this agent can use

**Example**:

```python
create_agent(
    name="scout_1",
    template="scout-fast",
    # OR
    system_prompt="...",
    model="haiku",
    allowed_tools=["Read", "Glob", "Grep"]
)
```

**Best Practices**:

- Use templates for consistency
- Give descriptive names
- Select appropriate model
- Minimize tool access

### Command Operation

Send prompts to an agent.

**Parameters**:

- `agent_id`: Which agent to command
- `prompt`: The detailed instruction

**Example**:

```python
command_agent(
    agent_id="scout_1",
    prompt="""
    Analyze the authentication module in src/auth/.
    Focus on:
    1. Current implementation patterns
    2. Security considerations
    3. Potential improvements

    Report findings in structured format.
    """
)
```

**Best Practices**:

- Detailed, specific prompts
- Clear expected output format
- Include all relevant context
- One task per command

### Monitor Operation (Read)

Check agent status and progress.

**Operations**:

```python
# Check status
check_agent_status(
    agent_id="scout_1",
    verbose_logs=True
)

# List all agents
list_agents()

# Read agent logs
read_agent_logs(
    agent_id="scout_1",
    offset=0,
    limit=50
)
```

**Status Values**:

| Status | Meaning |
| --- | --- |
| `idle` | Ready for commands |
| `executing` | Processing prompt |
| `waiting` | Waiting for input |
| `blocked` | Permission needed |
| `complete` | Finished |

### Delete Operation

Clean up agents when work is complete.

**Example**:

```python
delete_agent(agent_id="scout_1")
```

**Key Principle**:
> "Treat agents as deletable temporary resources that serve a single purpose."

## Lifecycle Patterns

### Scout-Build Pattern

```text
1. Create scout agent
2. Command: Analyze codebase
3. Monitor until complete
4. Aggregate scout findings
5. Delete scout

6. Create builder agent
7. Command: Implement based on findings
8. Monitor until complete
9. Aggregate build results
10. Delete builder
```

### Scout-Build-Review Pattern

```text
Phase 1: Scout
- Create scouts (parallel)
- Command each with specific area
- Aggregate findings

Phase 2: Build
- Create builder
- Command with scout reports
- Monitor implementation

Phase 3: Review
- Create reviewer
- Command to verify implementation
- Generate final report

Cleanup: Delete all agents
```

### Parallel Execution

```text
Create: scout_1, scout_2, scout_3 (parallel)
Command each with different area
Monitor all until complete
Aggregate all findings
Delete all scouts

Create: builder_1, builder_2 (parallel)
Command each with different files
Monitor all until complete
Aggregate all changes
Delete all builders
```

## Agent Templates

### Fast Scout Template

```yaml
---
name: scout-fast
description: Quick codebase reconnaissance
tools: [Read, Glob, Grep]
model: haiku
---

# Scout Agent

Analyze codebase efficiently. Focus on:
- File structure
- Key patterns
- Relevant code sections

Report findings concisely.
```

### Builder Template

```yaml
---
name: builder
description: Code implementation specialist
tools: [Read, Write, Edit, Bash]
model: sonnet
---

# Builder Agent

Implement changes based on specifications.
Follow existing patterns.
Test your changes.
Report what was modified.
```

### Reviewer Template

```yaml
---
name: reviewer
description: Code review and verification
tools: [Read, Grep, Glob, Bash]
model: sonnet
---

# Reviewer Agent

Verify implementation against requirements.
Check for issues and risks.
Report findings by severity.
```

## State Tracking

Track agent state for observability:

```json
{
  "agent_id": "scout_1",
  "template": "scout-fast",
  "status": "executing",
  "created_at": "2024-01-15T10:30:00Z",
  "last_activity": "2024-01-15T10:32:15Z",
  "context_tokens": 12500,
  "cost": 0.05,
  "tool_calls": 15
}
```

## Resource Cleanup

### Cleanup Triggers

| Trigger | Action |
| --- | --- |
| Work complete | Delete immediately |
| Error state | Delete and report |
| Timeout | Delete and warn |
| User abort | Delete all |

### Cleanup Checklist

- [ ] All agents have termination logic
- [ ] Dead agents are detected
- [ ] Resources are released
- [ ] Final results are captured
- [ ] Cleanup is logged

## Output Format

When implementing lifecycle management, provide:

```markdown
## Lifecycle Implementation

### Agent Templates

[List of templates with configurations]

### CRUD Tools

| Tool | Implementation | Parameters |
| --- | --- | --- |
| create_agent | ... | ... |
| command_agent | ... | ... |
| check_agent_status | ... | ... |
| list_agents | ... | ... |
| delete_agent | ... | ... |

### State Schema

[JSON schema for agent state]

### Cleanup Logic

[When and how agents are deleted]
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Keeping dead agents | Resource waste | Delete when done |
| Long-lived agents | Context accumulation | Fresh agents per task |
| Generic agents | Unfocused work | Specialized templates |
| Missing cleanup | Dead agents accumulate | Always delete |
| Reusing agents | Context contamination | Create fresh |

## Key Quotes

> "The rate at which you create and command your agents becomes the constraint of your engineering output."
>
> "One agent, one prompt, one purpose - then delete."

## Cross-References

- @agent-lifecycle-crud.md - Lifecycle patterns
- @three-pillars-orchestration.md - CRUD pillar
- @single-interface-pattern.md - Orchestrator architecture
- @orchestrator-design skill - System design

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
