---
name: fan-out
description: |
  Orchestration pattern for parallelizable tasks. When facing work that can be
  split into independent subtasks (research multiple topics, analyze multiple
  files, test multiple scenarios), spawn parallel agents and aggregate results.
  Use when subtasks have no dependencies on each other.
allowed-tools: |
  bash: ls, cat, grep
  file: read
  mcp: task
---

# Fan-Out

<purpose>
Some tasks are embarrassingly parallel - researching 5 APIs, analyzing 10 files,
testing 3 approaches. Running them sequentially wastes time. This elixir
orchestrates parallel execution: decompose work, fan out to agents, collect
and synthesize results.
</purpose>

## When To Activate

Trigger when:

- Task involves analyzing multiple independent items
- Research spans several unrelated topics
- Need to explore multiple approaches simultaneously
- Batch processing with no inter-item dependencies
- User says "check all of these" or "investigate each"

Do NOT trigger for:

- Sequential tasks where B depends on A
- Single-item deep analysis
- Tasks requiring context accumulation across items
- When parallel execution would overwhelm system resources

## The Pattern

```
                    ┌──→ [Agent 1] ──→ Result 1 ──┐
                    │                              │
[Task] → Decompose ─┼──→ [Agent 2] ──→ Result 2 ──┼──→ Aggregate → [Final]
                    │                              │
                    └──→ [Agent 3] ──→ Result 3 ──┘
```

## Instructions

### Step 1: Validate Parallelizability

Confirm the task is fan-out appropriate:

```
Subtask independence check:
- Can subtask B complete without subtask A's result? [YES/NO]
- Do subtasks share mutable state? [YES/NO - should be NO]
- Is order of completion irrelevant? [YES/NO - should be YES]

If any check fails → Use 'pipeline' pattern instead
```

### Step 2: Decompose the Task

Break work into discrete, independent units:

```
Original task: [Description]

Subtasks:
1. [Subtask 1] - Agent type: [explore/research/analyze]
2. [Subtask 2] - Agent type: [explore/research/analyze]
3. [Subtask 3] - Agent type: [explore/research/analyze]
...

Expected outputs:
- Subtask 1 → [What result looks like]
- Subtask 2 → [What result looks like]
```

### Step 3: Spawn Parallel Agents

Launch agents simultaneously:

```
Spawning [N] parallel agents:

Agent 1: [Subtask description]
Agent 2: [Subtask description]
Agent 3: [Subtask description]

[Wait for all to complete]
```

Use Task tool with appropriate subagent_type for each.

### Step 4: Collect Results

Gather outputs from all agents:

```
Results received:
- Agent 1: [Summary]
- Agent 2: [Summary]
- Agent 3: [Summary]
```

### Step 5: Synthesize

Aggregate results into coherent output:

```
Synthesis:
- [Combined insight 1]
- [Combined insight 2]
- [Patterns across results]
- [Conflicts or contradictions]
```

### Step 6: Report

Present unified findings:

```
## Fan-Out Results: [Task]

### Summary
[High-level findings]

### Details by Subtask
1. [Subtask 1 findings]
2. [Subtask 2 findings]
...

### Cross-Cutting Insights
[Patterns that emerged across subtasks]

### Recommendations
[Actionable next steps]
```

## Resource Management

<resources>
**Agent limits:**
- Recommended max: 5 parallel agents
- Hard limit: Based on system capacity

**When to limit parallelism:**
- Complex subtasks → fewer agents (3 max)
- Simple lookups → more agents (5+)
- Resource-intensive work → sequential fallback

**Failure handling:**
- If agent fails: Log error, continue with others
- If >50% fail: Abort and report
- Partial results: Clearly mark incomplete
</resources>

## NEVER

- Fan out dependent tasks (use pipeline instead)
- Spawn more agents than subtasks warrant
- Ignore failed agents - always report what succeeded/failed
- Assume all results are equally valid without synthesis
- Fan out trivial tasks (overhead not worth it)

## ALWAYS

- Verify independence before fanning out
- Define clear, specific prompts for each agent
- Set expectations for what each agent should return
- Synthesize results, don't just concatenate
- Report which subtasks succeeded/failed

## Examples

### Example 1: Multi-File Analysis

User: "Check all our API endpoints for authentication issues"

```
Subtask independence check:
- Can each file be analyzed independently? YES
- Shared state? NO
- Order irrelevant? YES

→ Fan-out appropriate

Decomposing:
1. Analyze src/api/users.ts for auth issues
2. Analyze src/api/orders.ts for auth issues
3. Analyze src/api/products.ts for auth issues
4. Analyze src/api/admin.ts for auth issues

[Spawns 4 parallel explore agents]

Results:
- users.ts: Missing rate limiting on login endpoint
- orders.ts: No auth check on order history
- products.ts: Clean
- admin.ts: Using deprecated auth method

Synthesis:
3 of 4 files have auth issues. Most critical: orders.ts
exposes user data without authentication.
```

### Example 2: Research Multiple Technologies

User: "Compare Redis, Memcached, and DynamoDB for our caching layer"

```
Subtask independence check:
- Independent research? YES
- Shared state? NO
- Order irrelevant? YES

→ Fan-out appropriate

Decomposing:
1. Research Redis: features, performance, pricing
2. Research Memcached: features, performance, pricing
3. Research DynamoDB: features, performance, pricing

[Spawns 3 parallel research agents]

Results synthesized into comparison table with
cross-cutting analysis of trade-offs.
```

### Example 3: Not Appropriate for Fan-Out

User: "Build a feature: first design it, then implement, then test"

```
Subtask independence check:
- Can implementation happen without design? NO
- Can tests run without implementation? NO

→ NOT fan-out appropriate
→ Use 'pipeline' pattern instead
```

<failed-attempts>
What DOESN'T work:
- Fanning out dependent tasks: Results are incoherent, agents make conflicting assumptions
- Too many agents: System overwhelmed, diminishing returns
- Vague agent prompts: Results are too varied to synthesize
- No synthesis step: User gets disconnected bullet points, not insight
</failed-attempts>

## Why This Elixir Exists

Sequential processing of independent tasks wastes time. A human would delegate
parallel work to multiple people. This elixir gives Claude the same capability:
decompose, distribute, synthesize.

The key insight: parallelism only helps when tasks are truly independent.
Otherwise, you get chaos, not speed.
