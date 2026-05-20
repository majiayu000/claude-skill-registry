---
name: Agentic Feature Design
description: Designing features for the "Action Era" that are AI-accessible by default
---

# Agentic Feature Design

Features in LivestockAI must now be designed for **dual consumption**: Humans (UI) and Agents (MCP/API).

## 1. The "Headless First" Rule

Every feature must be fully functional via Server Functions _before_ any UI is built.

**Test:** Can an agent complete the entire user story using only `bun run check-feature-x.ts` (a script calling server functions)?
If yes -> **Agent Ready.**
If no (logic lives in React components) -> **Refactor immediately.**

## 2. Agent-Ready Server Functions

Server functions are the tools we give to agents. Document them accordingly.

```typescript
export const createBatchFn = createServerFn({ method: 'POST' })
  .inputValidator(batchSchema)
  .handler(async ({ data }) => {
    /* ... */
  })

/**
 * @description Creates a new livestock batch.
 * @workflow
 * 1. Check `getFarmFacilities` for space.
 * 2. `createBatchFn`
 * 3. Log initial `feed_record` if applicable.
 */
```

## 3. The "Intention" Pattern

Agents operate on _Intent_, not just data.
Instead of generic CRUD (`updateBatch`), expose semantic actions (`graduateBatch`, `quarantineBatch`).

```typescript
// ❌ Generic
updateBatch(id, { status: 'sold' })

// ✅ Semantic (Agent Friendly)
markBatchAsSold(id, { date, price, customer })
```

Semantic actions allow agents to:

1. Understand the _consequences_ of the action.
2. Perform specialized validation (e.g. "Can't sell a quarantined batch").

## 4. Approval Loops (Human-in-the-Loop)

Agents need a standard way to ask for permission for high-stakes actions (e.g., ordering feed, selling stock).

**The `ApprovalRequest` Entity:**

- `agentId`: Who is asking?
- `action`: JSON payload of the server function to call.
- `summary`: Human-readable explanation ("I want to order 50 bags of Starter Feed").
- `status`: PENDING | APPROVED | REJECTED

## 5. Metadata for Context

All major entities (`Batches`, `Sales`) should have an `ai_metadata` JSONB column.
Agents use this to store reasoning ("Predicted harvest date change due to low feed intake").
_Do not show this raw JSON to users, but use it to power UI "Insights"._

## Related Skills

- `three-layer-architecture` - Where the logic lives
- `feature-structure` - How to organize the files
