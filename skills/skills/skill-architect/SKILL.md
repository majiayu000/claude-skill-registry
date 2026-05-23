---
name: skill-architect
description: Design subagents for new skills. Triggers on requests to architect skills, design agents for skills, plan skill agents, figure out what agents a skill needs, or optimize skill with agents.
allowed-tools: Read, Edit, Write, Task, Glob
---

# Skill Architect

Analyze skill requirements and design subagents that make skills efficient and repeatable.

## When to Use Subagents

Subagents excel at:
- **Parallel exploration** - Multiple searches/reads at once
- **Isolated analysis** - Focused work without context accumulation
- **Repeatable operations** - Same task structure, different inputs
- **Research gathering** - Collect info, return only findings

## Analysis Process

### 1. Gather Skill Requirements

Identify the skill's:
- Primary workflow steps
- Input variations
- Output requirements
- External dependencies (APIs, files, tools)

### 2. Map Work Patterns

For each workflow step, classify:

| Pattern | Agent Fit | Example |
|---------|-----------|---------|
| Search multiple sources | High | Research best practices across domains |
| Process items in parallel | High | Validate multiple files simultaneously |
| Explore then decide | High | Find options, return summary for decision |
| Sequential dependencies | Low | Step B needs Step A's exact output |
| Interactive refinement | Low | Requires back-and-forth with user |

### 3. Define Agents

For each identified agent, specify:

```markdown
### Agent: <name>

**Purpose:** Single sentence describing what it accomplishes

**Inputs:**
- <input 1>
- <input 2>

**Returns:**
- <structured output description>

**Subagent type:** Explore | general-purpose | Bash | Plan

**Parallelizable:** Yes/No - can multiple instances run concurrently?
```

### 4. Design Agent Coordination

Map how agents interact:

```
Main skill flow:
1. Spawn research agents (parallel)
2. Collect results
3. Spawn processing agents (parallel)
4. Synthesize outputs
5. Present to user
```

## Output Format

Produce an agent design document:

```markdown
# Agent Design: <skill-name>

## Identified Agents

### 1. <agent-name>
[agent spec from step 3]

### 2. <agent-name>
[agent spec from step 3]

## Coordination Flow
[flow from step 4]

## Implementation Notes
- <any special considerations>
```

## Creating the Skill

Once agent design is approved, invoke skill-creator:

> "Create a skill called <name> with the agents defined above"

The skill-creator will incorporate the agent definitions into the new skill's SKILL.md.

See `references/agent-patterns.md` for common agent patterns and anti-patterns.
