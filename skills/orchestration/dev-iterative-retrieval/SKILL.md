---
version: 1.0.0
name: dev-iterative-retrieval
description: >
  Pattern for progressively refining context retrieval in multi-agent workflows.
  Solves the sub-agent context problem where agents don't know what context they
  need until they start working. Dispatches broad queries, evaluates relevance,
  refines, and loops (max 3 cycles). Use when spawning sub-agents that need
  codebase context, or when a single search isn't finding what you need.
disable-model-invocation: true
user-invocable: false
---

# Iterative Retrieval — Progressive Context Refinement

Solve the "context problem" in multi-agent workflows where sub-agents don't know what context they need until they start working.


## The Problem

Sub-agents are spawned with limited context. Standard approaches fail:
- **Send everything**: Exceeds context limits
- **Send nothing**: Agent lacks critical information
- **Guess what's needed**: Often wrong

## The Solution: 4-Phase Loop

```
┌──────────┐      ┌──────────┐
│ DISPATCH │─────▶│ EVALUATE │
└──────────┘      └──────────┘
     ▲                  │
     │                  ▼
┌──────────┐      ┌──────────┐
│   LOOP   │◀─────│  REFINE  │
└──────────┘      └──────────┘

    Max 3 cycles, then proceed
```

### Phase 1: DISPATCH

Start with a broad query based on the task description:

```
Search for: keywords from task description
Patterns: src/**/*.cs, src/**/*.ts (relevant to task)
Exclude: *.spec.ts, *Tests.cs, bin/, obj/, node_modules/
```

### Phase 2: EVALUATE

Score each result for relevance:

| Score | Meaning | Action |
|-------|---------|--------|
| 0.8-1.0 | Directly implements target functionality | Keep |
| 0.5-0.7 | Contains related patterns or types | Keep if needed |
| 0.2-0.4 | Tangentially related | Discard |
| 0-0.2 | Not relevant | Exclude from future searches |

For each file, also identify: **what context is still missing?**

### Phase 3: REFINE

Update search criteria based on what you learned:
- Add terminology the codebase actually uses (not what you assumed)
- Add patterns discovered in high-relevance files (e.g., `IOrderRepository` → search for all `IRepository` implementations)
- Exclude confirmed irrelevant paths
- Target specific gaps identified in evaluation

### Phase 4: LOOP

Repeat with refined criteria. Stop when:
- 3+ high-relevance files found AND no critical gaps remain
- Max 3 cycles reached (proceed with best available context)

## Practical Examples

### Example: Bug Fix

```
Task: "Fix the order total calculation rounding issue"

Cycle 1:
  DISPATCH: Search for "order", "total", "calculation" in src/**/*.cs
  EVALUATE: Found OrderService.cs (0.9), Order.cs (0.8), CartController.cs (0.3)
  REFINE: Spotted "Money" value object in Order.cs → search for Money type

Cycle 2:
  DISPATCH: Search "Money", "decimal", "rounding"
  EVALUATE: Found Money.cs (0.95), MoneyExtensions.cs (0.85)
  RESULT: Sufficient — 4 high-relevance files found

Context: OrderService.cs, Order.cs, Money.cs, MoneyExtensions.cs
```

### Example: Feature Implementation

```
Task: "Add email notifications when order status changes"

Cycle 1:
  DISPATCH: Search "notification", "email" in src/**
  EVALUATE: No matches — codebase uses "alert" and "message" instead
  REFINE: Add "alert", "message", "INotification" keywords

Cycle 2:
  DISPATCH: Search refined terms
  EVALUATE: Found AlertService.cs (0.9), IMessageSender.cs (0.7)
  REFINE: Need order status change events

Cycle 3:
  DISPATCH: Search "OrderStatus", "event", "handler"
  EVALUATE: Found OrderStatusChangedEvent.cs (0.95), EventHandlers/ (0.8)
  RESULT: Sufficient

Context: AlertService.cs, IMessageSender.cs, OrderStatusChangedEvent.cs, EventHandlers/
```

## How to Apply in Agent Prompts

When dispatching a sub-agent, include both the query AND the objective:

```
Task: {specific query}
Objective: {broader context — WHY this information is needed}

When retrieving context:
1. Start with broad keyword search
2. Evaluate each file's relevance (0-1 scale)
3. Identify what context is still missing
4. Refine search criteria and repeat (max 3 cycles)
5. Return files with relevance >= 0.7
```

## Best Practices

1. **Start broad, narrow progressively** — don't over-specify initial queries
2. **Learn codebase terminology** — first cycle often reveals naming conventions
3. **Track what's missing** — explicit gap identification drives refinement
4. **Stop at "good enough"** — 3 high-relevance files beats 10 mediocre ones
5. **Pass objective context** — sub-agents with the "why" make better decisions about what to include
