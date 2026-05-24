---
name: multi-agent-observability
description: Build observability interfaces for multi-agent systems. Use when monitoring multi-agent execution, tracking agent metrics, implementing logging for parallel agents, or debugging agent workflows.
allowed-tools: Read, Grep, Glob
---

# Multi-Agent Observability Skill

Build observability interfaces for monitoring and measuring multi-agent systems.

## Purpose

Guide the design and implementation of observability layers that provide real-time visibility into multi-agent execution.

## When to Use

- Designing monitoring for agent fleets
- Building metrics dashboards
- Implementing logging architecture
- Creating cost tracking systems

## Prerequisites

- Understanding of the Three Pillars (@three-pillars-orchestration.md)
- Familiarity with results-oriented patterns (@results-oriented-engineering.md)
- Access to Claude Agent SDK documentation

## SDK Requirement

> **Implementation Note**: Full observability requires Claude Agent SDK with custom MCP tools and UI components. This skill provides design patterns.

## The Critical Principle

> "If you can't measure it, you can't improve it. If you can't measure it, you can't scale it."

## What to Observe

### Per-Agent Metrics

| Metric | Purpose | How to Track |
| --- | --- | --- |
| Status | Know state | Agent state enum |
| Context usage | Token consumption | API response |
| Cost | Financial impact | API usage data |
| Tool calls | What it's doing | Hook logging |
| Results | Output verification | Result parsing |
| Duration | Execution time | Timestamps |

### Aggregate Metrics

| Metric | Purpose | Calculation |
| --- | --- | --- |
| Total agents | Scale | Count active |
| Total duration | End-to-end time | First to last |
| Total cost | Financial total | Sum per-agent |
| Success rate | Reliability | Success / total |
| Coverage | Scope | Files touched |

## Observability Components

### 1. Agent Cards

Real-time status for each agent:

```text
┌─────────────────────────────────────┐
│ scout_1                 [EXECUTING] │
├─────────────────────────────────────┤
│ Template: scout-fast                │
│ Model: haiku                        │
│ Context: 12,500 / 100,000 tokens    │
│ Cost: $0.05                         │
│ Duration: 45s                       │
│ Tool calls: 15                      │
└─────────────────────────────────────┘
```

**Required fields**:

- Agent ID and template
- Status (idle, executing, complete, error)
- Model being used
- Context usage (current / max)
- Running cost
- Execution duration
- Tool call count

### 2. Event Stream

Real-time log of all activities:

```text
[10:30:00] scout_1 created (template: scout-fast)
[10:30:01] scout_1 commanded: "Analyze auth module"
[10:30:05] scout_1 Read: src/auth/login.ts
[10:30:08] scout_1 Grep: "password" in src/auth/
[10:30:15] scout_1 completed (duration: 14s)
[10:30:16] scout_1 deleted
```

**Event types**:

- Agent lifecycle (create, delete)
- Commands sent
- Tool calls
- Status changes
- Errors

### 3. Cost Tracking

Track spend per agent and total:

```text
Cost Summary
────────────────────────────────────
scout_1 (haiku)      $0.05
scout_2 (haiku)      $0.04
builder_1 (sonnet)   $0.35
reviewer_1 (sonnet)  $0.12
────────────────────────────────────
Total                $0.56
Budget remaining     $4.44 (89%)
```

**Cost components**:

- Input tokens
- Output tokens
- Per-agent breakdown
- Running total
- Budget tracking

### 4. Result Inspector

View consumed and produced assets:

```text
Agent: builder_1

Consumed Assets:
├── Scout report (summary)
├── src/auth/middleware.ts
└── package.json

Produced Assets:
├── src/auth/rate-limit.ts (created)
├── src/auth/middleware.ts (modified)
└── tests/rate-limit.test.ts (created)

Summary: "Implemented rate limiting middleware"
Status: completed
```

### 5. Log Viewer

Filterable activity history:

```text
Filters: [agent: all] [level: all] [tool: all]

10:30:00 INFO  scout_1   Created from template
10:30:01 INFO  scout_1   Received command
10:30:05 DEBUG scout_1   Read: src/auth/login.ts (1,200 tokens)
10:30:08 DEBUG scout_1   Grep: found 5 matches
10:30:12 WARN  scout_1   Context at 80% capacity
10:30:15 INFO  scout_1   Completed successfully
```

## Implementation Patterns

### Logging Architecture

```python
# Event types
class AgentEvent:
    timestamp: datetime
    agent_id: str
    event_type: str  # create, command, tool, status, error
    details: dict

# Log collector
def log_event(event: AgentEvent):
    # Store to database
    db.events.insert(event)
    # Emit to WebSocket
    ws.broadcast(event)
    # Update metrics
    metrics.update(event)
```

### Real-Time Updates

```python
# WebSocket for live updates
async def agent_status_stream(agent_id):
    while agent_active(agent_id):
        status = get_agent_status(agent_id)
        yield status
        await asyncio.sleep(1)
```

### Cost Calculation

```python
def calculate_cost(usage):
    input_cost = usage.input_tokens * MODEL_INPUT_PRICE
    output_cost = usage.output_tokens * MODEL_OUTPUT_PRICE
    return input_cost + output_cost
```

## UI Components

### Minimal CLI View

```text
Orchestration: Add rate limiting
────────────────────────────────────
Agents: 3 active | 2 complete | 0 error
Cost: $0.56 / $5.00 budget
Progress: ████████░░ 80%

[scout_1] ✓ complete (14s)
[scout_2] ✓ complete (12s)
[builder] ⚡ executing (45s)
```

### Rich Dashboard View

```text
┌─────────────────────────────────────────────────────────────┐
│                    Orchestration Dashboard                    │
├─────────────────────────────────────────────────────────────┤
│ Task: Add rate limiting to authentication                    │
│ Started: 10:30:00 | Duration: 2m 15s | Cost: $0.56          │
├─────────────────────────────────────────────────────────────┤
│ Agent Fleet                          │ Event Stream          │
│ ┌─────────────────────────────────┐  │ [10:32:15] builder   │
│ │ scout_1        [✓ complete]    │  │   Write: rate-limit  │
│ │ scout_2        [✓ complete]    │  │ [10:32:10] builder   │
│ │ builder        [⚡ executing]   │  │   Read: middleware   │
│ │ reviewer       [○ pending]     │  │ [10:30:15] scout_2   │
│ └─────────────────────────────────┘  │   completed          │
├─────────────────────────────────────────────────────────────┤
│ Cost Breakdown     │ Results Summary                         │
│ haiku:  $0.09     │ Files read: 8                           │
│ sonnet: $0.47     │ Files written: 3                        │
│ Total:  $0.56     │ Tests: 5/5 passing                      │
└─────────────────────────────────────────────────────────────┘
```

## Design Checklist

- [ ] Per-agent metrics defined
- [ ] Aggregate metrics calculated
- [ ] Event logging implemented
- [ ] Real-time updates via WebSocket
- [ ] Cost tracking per agent
- [ ] Result inspection available
- [ ] Log filtering supported
- [ ] UI components designed

## Output Format

When designing observability, provide:

```markdown
## Observability Design

### Metrics

**Per-Agent:**
[List with tracking method]

**Aggregate:**
[List with calculation]

### Components

**Agent Cards:** [fields and update frequency]
**Event Stream:** [event types and storage]
**Cost Tracking:** [breakdown and budgets]
**Result Inspector:** [consumed/produced format]
**Log Viewer:** [filters and retention]

### Implementation

**Logging:** [architecture]
**Real-Time:** [WebSocket design]
**Storage:** [database schema]
**UI:** [component specifications]
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| No metrics | Flying blind | Track everything |
| Delayed updates | Stale status | Real-time WebSocket |
| No cost tracking | Budget overruns | Per-agent costs |
| Missing logs | Can't debug | Log all events |
| No aggregation | Can't summarize | Calculate totals |

## Cross-References

- @three-pillars-orchestration.md - Observability pillar
- @results-oriented-engineering.md - Result patterns
- @agent-lifecycle-crud.md - Agent state tracking
- @orchestrator-design skill - System architecture

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
