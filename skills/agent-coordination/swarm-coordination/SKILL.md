---
name: swarm-coordination
description: Multi-agent swarm coordination patterns. Orchestrates parallel agent execution, manages agent communication, handles task distribution, and coordinates results aggregation.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Spawn independent agents in parallel
  - Use structured handoff formats
  - Aggregate results systematically
  - Handle partial failures gracefully
error_handling: graceful
streaming: supported
---

# Swarm Coordination Skill

<identity>
Swarm Coordination Skill - Orchestrates parallel agent execution, manages inter-agent communication, handles task distribution, and coordinates results aggregation for complex multi-agent workflows.
</identity>

<capabilities>
- Parallel agent spawning
- Task distribution strategies
- Results aggregation
- Inter-agent communication
- Failure handling and recovery
</capabilities>

<instructions>
<execution_process>

### Step 1: Analyze Task for Parallelization

Identify parallelizable work:

| Pattern           | Example                        | Strategy               |
| ----------------- | ------------------------------ | ---------------------- |
| Independent tasks | Review multiple files          | Spawn in parallel      |
| Dependent tasks   | Design → Implement             | Sequential spawn       |
| Fan-out/Fan-in    | Multiple reviews → Consolidate | Parallel + Aggregation |
| Pipeline          | Parse → Transform → Validate   | Sequential handoff     |

### Step 2: Spawn Agents in Parallel

Use the Task tool to spawn multiple agents in a single message:

```javascript
// Spawn multiple agents in ONE message for parallel execution
Task({
  subagent_type: 'general-purpose',
  description: 'Architect reviewing design',
  prompt: 'Review architecture...',
});

Task({
  subagent_type: 'general-purpose',
  description: 'Security reviewing design',
  prompt: 'Review security...',
});
```

**Key**: Both Task calls must be in the SAME message for true parallelism.

### Step 3: Define Handoff Format

Use structured formats for agent communication:

```markdown
## Agent Handoff: [Source] → [Target]

### Context

- Task: [What was done]
- Files: [Files touched]

### Findings

- [Key finding 1]
- [Key finding 2]

### Recommendations

- [Action item 1]
- [Action item 2]

### Artifacts

- [Path to artifact 1]
- [Path to artifact 2]
```

### Step 4: Aggregate Results

Combine outputs from parallel agents:

```markdown
## Swarm Results Aggregation

### Participating Agents

- Architect: Completed ✅
- Security: Completed ✅
- DevOps: Completed ✅

### Consensus Points

- [Point all agents agree on]

### Conflicts

- [Point agents disagree on]
- Resolution: [How to resolve]

### Combined Recommendations

1. [Prioritized recommendation]
2. [Prioritized recommendation]
```

### Step 5: Handle Failures

Strategies for partial failures:

| Scenario                | Strategy                        |
| ----------------------- | ------------------------------- |
| Agent timeout           | Retry with simpler prompt       |
| Agent error             | Continue with available results |
| Conflicting results     | Use consensus-voting skill      |
| Missing critical result | Block and retry                 |

</execution_process>

<best_practices>

1. **Parallelize Aggressively**: Independent work should run in parallel
2. **Structured Handoffs**: Use consistent formats for communication
3. **Graceful Degradation**: Continue with partial results when safe
4. **Clear Aggregation**: Combine results systematically
5. **Track Provenance**: Know which agent produced each result

</best_practices>
</instructions>

<examples>
<usage_example>
**Parallel Review Request**:

```
Get architecture, security, and performance reviews for the new API design
```

**Swarm Coordination**:

```javascript
// Spawn 3 reviewers in parallel (single message)
Task({ description: 'Architect reviewing API', prompt: '...' });
Task({ description: 'Security reviewing API', prompt: '...' });
Task({ description: 'Performance reviewing API', prompt: '...' });
```

**Aggregated Results**:

```markdown
## API Design Review (3 agents)

### Consensus

- RESTful design is appropriate
- Need authentication on all endpoints

### Recommendations by Priority

1. [HIGH] Add rate limiting (Security)
2. [HIGH] Use connection pooling (Performance)
3. [MED] Add versioning to URLs (Architect)
```

</usage_example>
</examples>

## Rules

- Always spawn independent agents in parallel
- Use structured handoff formats
- Handle partial failures gracefully

## Related Workflow

This skill has a corresponding workflow for complex multi-agent scenarios:

- **Workflow**: `.claude/workflows/enterprise/swarm-coordination-skill-workflow.md`
- **When to use workflow**: For massively parallel task execution with Queen/Worker topology, fault tolerance, and distributed coordination (large-scale refactoring, parallel code review, multi-file implementation)
- **When to use skill directly**: For simple parallel agent spawning or when integrating swarm patterns into other workflows

## Workflow Integration

This skill powers multi-agent orchestration patterns across the framework:

**Router Decision:** `.claude/workflows/core/router-decision.md`

- Router uses swarm patterns for parallel agent spawning
- Planning Orchestration Matrix defines when to use swarm coordination

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

- Swarm patterns apply to artifact creation at scale
- Parallel validation of multiple artifacts

**Related Workflows:**

- `consensus-voting` skill for resolving conflicting agent outputs
- `context-compressor` skill for aggregating parallel results
- Enterprise workflows in `.claude/workflows/enterprise/` use swarm patterns

---

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
