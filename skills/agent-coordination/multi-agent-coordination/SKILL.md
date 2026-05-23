---
name: Multi-Agent Coordination
description: This skill should be used when the user asks about "multi-agent coordination", "agent spawning", "parallel agents", "agent communication", "team coordination", "sub-agent management", "agent limits", "agent layers", or needs guidance on coordinating multiple agents for complex tasks.
version: 1.0.0
---

# Multi-Agent Coordination

Establish effective coordination between multiple agents working on complex tasks, ensuring proper communication, resource sharing, and conflict resolution.

## Agent Spawning Guidelines

### Mandatory Limits (ENFORCED)

| Constraint | Value | Enforcement |
|------------|-------|-------------|
| **Minimum Agents** | 3 per complex task | Hook-enforced |
| **Maximum Agents** | 13 per task | Hard limit |
| **Recommended** | 5-7 agents | Optimal performance |

### When to Spawn Agents

**Always spawn agents for:**
- Tasks requiring more than 3 steps
- Work spanning multiple files/components
- Tasks requiring diverse expertise
- Parallel workstreams

**Single agent sufficient for:**
- Simple file edits
- Quick lookups
- Straightforward questions

## Agent Layer Architecture

Organize agents into functional layers for clear responsibility separation:

### Strategic Layer
- **Role**: High-level planning and decision-making
- **Agents**: master-strategist, architect-supreme, risk-assessor
- **Output**: Plans, architectural decisions, risk assessments

### Tactical Layer
- **Role**: Coordination and resource management
- **Agents**: plan-decomposer, resource-allocator, conflict-resolver
- **Output**: Task breakdowns, schedules, conflict resolutions

### Operational Layer
- **Role**: Direct implementation work
- **Agents**: coder, tester, reviewer, debugger
- **Output**: Code, tests, reviews, fixes

### Quality Layer
- **Role**: Validation and documentation
- **Agents**: test-strategist, security-specialist, documentation-expert
- **Output**: Test plans, security audits, documentation

## Parallel Execution Strategy

### Level-Based Parallelization

```
Level 0: [Agent A] [Agent B] [Agent C]  ← Execute in parallel
         ↓         ↓         ↓
Level 1: [Agent D] [Agent E]            ← Wait for L0, then parallel
         ↓         ↓
Level 2: [Agent F]                       ← Wait for L1
```

### Dependency Rules
1. Agents at same level execute concurrently
2. Level N+1 waits for all Level N completion
3. Independent agents always run in parallel
4. Shared resources require coordination

## Communication Patterns

### Message Types

| Type | Purpose | Priority |
|------|---------|----------|
| **TASK** | Assign work to agent | High |
| **STATUS** | Progress updates | Medium |
| **RESULT** | Completed work output | High |
| **HANDOFF** | Transfer context to next agent | Critical |
| **ERROR** | Failure notification | Critical |

### Handoff Protocol

When transferring work between agents:

1. **Context Package**
   - Task description and objectives
   - Files modified/created
   - Decisions made and rationale
   - Known issues or blockers

2. **State Transfer**
   - Current phase and progress
   - Pending tasks
   - Dependencies resolved/pending

3. **Verification**
   - Receiving agent confirms context
   - Missing information requested
   - Handoff logged for audit

## Conflict Resolution

### Resource Conflicts

When multiple agents need the same resource:

1. **Priority-Based**: Higher-layer agents get priority
2. **Time-Based**: First requester wins
3. **Merge-Based**: Combine compatible changes
4. **Escalation**: Strategic layer decides

### Decision Conflicts

When agents disagree on approach:

1. Document both positions
2. Escalate to strategic layer
3. Strategic agent decides with rationale
4. Decision logged for learning

## Agent Lifecycle

### Spawning
1. Define clear scope and objectives
2. Assign layer and role
3. Provide initial context
4. Set success criteria

### Monitoring
- Track progress against objectives
- Monitor resource usage
- Detect stuck/blocked states
- Log all significant actions

### Completion
1. Verify deliverables against objectives
2. Package outputs for next phase
3. Document lessons learned
4. Clean up resources

## Best Practices

### DO:
- Spawn minimum 3 agents for complex tasks
- Use parallel execution for independent work
- Include quality layer agents in every task
- Document all handoffs
- Set clear success criteria

### DON'T:
- Exceed 13 agents per task
- Skip testing agents
- Allow single agent for complex work
- Ignore conflicts between agents
- Lose context during handoffs

## Additional Resources

### Reference Files
- **`references/agent-layer-details.md`** - Detailed layer specifications
- **`references/communication-protocols.md`** - Message format specifications

### Examples
- **`examples/parallel-execution.json`** - Sample parallel execution plan
- **`examples/handoff-package.json`** - Sample context handoff structure
