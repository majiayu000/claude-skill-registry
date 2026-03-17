---
name: orchestration-template
description: Reference template for multi-agent orchestrated skills. Use as a pattern when creating complex skills that need parallel execution.
model: sonnet
context: orchestrate
user-invocable: false
---

# Sub-Agent Orchestration Template

This is a **reference template** for creating skills that use parallel sub-agents. It is NOT directly invocable - use it as a pattern when building new orchestrated skills.

## When to Use This Pattern

Use sub-agent orchestration when:

- Task has 3+ independent research phases
- Each phase can run in parallel without dependencies
- Results need synthesis into a unified output
- Context isolation improves quality (prevents contamination)

Do NOT use when:

- Task is simple and linear
- Phases depend on each other sequentially
- Interactive dialogue is needed throughout

## Orchestration Structure

### Phase 1: Planning

```markdown
1. TaskCreate for overall work item
2. Identify independent workstreams
3. Create sub-tasks for each workstream
4. Set dependencies with TaskUpdate (addBlockedBy)
```

### Phase 2: Parallel Execution

Launch N agents in parallel using Task tool:

```markdown
Task tool calls (in single message for parallelism):

Agent 1: subagent_type: "Explore", model: "haiku"

- Purpose: [specific research goal]
- Tools: Read, Glob, Grep (read-only)

Agent 2: subagent_type: "Explore", model: "haiku"

- Purpose: [different research goal]
- Tools: Read, Glob, Grep (read-only)

Agent 3: subagent_type: "general-purpose"

- Purpose: [complex analysis requiring writes]
- Tools: All available
```

### Phase 3: Synthesis

```markdown
1. Collect results from all agents
2. Identify conflicts or gaps
3. Generate unified output
4. Update tasks to completed
```

## Model Selection for Sub-Agents

| Sub-Agent Purpose            | Model  | Rationale                     |
| ---------------------------- | ------ | ----------------------------- |
| Read-only search/exploration | Haiku  | Fast, cheap, isolated context |
| Analysis with context        | Sonnet | Good reasoning                |
| Complex synthesis            | Sonnet | Balanced cost/quality         |
| Deep architecture reasoning  | Opus   | Extended thinking needed      |

## Example: Parallel Research Pattern

```markdown
## Phase 1: Create Tasks

TaskCreate: "Research API patterns"
TaskCreate: "Research database patterns"
TaskCreate: "Research auth patterns"
TaskCreate: "Synthesise findings" (blockedBy: above three)

## Phase 2: Launch Parallel Agents

[Single message with 3 Task tool calls]

Task 1: Explore agent for API patterns
Task 2: Explore agent for database patterns
Task 3: Explore agent for auth patterns

## Phase 3: Synthesise

Read agent outputs
Combine into unified report
Mark all tasks completed
```

## Best Practices

1. **Limit to 3-5 parallel agents** - More causes coordination overhead
2. **Use Haiku for exploration** - Cheaper and faster for read-only
3. **Clear agent prompts** - Each agent needs complete context (no shared state)
4. **Aggregate carefully** - Agents may have conflicting findings
5. **Track with Tasks** - Use TaskCreate/TaskUpdate for visibility
6. **Handle failures** - If one agent fails, others continue

## Anti-Patterns

❌ **Don't** spawn agents for sequential work
❌ **Don't** use background agents when MCP tools needed
❌ **Don't** pass partial context expecting shared state
❌ **Don't** spawn 10+ agents (diminishing returns)

## Skills Using This Pattern

Reference these for working examples:

- `/vault-maintenance` - Parallel health checks
- `/quality-report` - Parallel analysis dimensions
- `/project-status` - Parallel data gathering agents

## Template Variables

When creating a new orchestrated skill, replace:

```
{{SKILL_NAME}} - Name of the skill
{{PHASE_COUNT}} - Number of parallel phases
{{AGENT_PURPOSE_N}} - Purpose of each agent
{{SYNTHESIS_OUTPUT}} - What the final output looks like
```
