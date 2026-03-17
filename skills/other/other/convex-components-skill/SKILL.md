---
name: convex-components
description: 'Universal patterns for Convex components including installation, configuration, and usage. Use when working with Rate Limiter, Aggregate, Workpool, Workflow, or any Convex component from the ecosystem.'
---

# Convex Components

Components are sandboxed packages with their own database tables, functions, and isolated execution.

## Universal Installation Pattern

All components follow the same installation pattern:

```bash
npm install @convex-dev/<component-name>
```

```typescript
// convex/convex.config.ts
import { defineApp } from 'convex/server';
import componentName from '@convex-dev/<component-name>/convex.config';

const app = defineApp();
app.use(componentName);

// Multiple instances with different names
app.use(componentName, { name: 'instance2' });

export default app;
```

Run `npx convex dev` to generate code.

## Accessing Components

```typescript
import { components } from './_generated/api';

// Default instance
const instance = new ComponentClass(components.componentName, {
  /* config */
});

// Named instance
const instance2 = new ComponentClass(components.instance2, {
  /* config */
});
```

## Transaction Semantics

Component mutations participate in the parent transaction:

```typescript
export const doWork = mutation({
  handler: async (ctx) => {
    await ctx.db.insert('myTable', { data: 'value' });
    await component.doSomething(ctx); // Same transaction

    // If mutation throws, BOTH writes roll back
  }
});
```

Component exceptions can be caught:

```typescript
try {
  await rateLimiter.limit(ctx, 'myLimit', { throws: true });
} catch (e) {
  // Only component's writes roll back
  // Parent mutation can continue
}
```

## Available Components

### Durable Functions

- **[Workflow](references/WORKFLOW.md)** - Long-running, durable code flows with retries
- **[Workpool](references/WORKPOOL.md)** - Queue actions with parallelism limits
- **[Action Retrier](references/ACTION-RETRIER.md)** - Retry failed actions with backoff

### Backend Utilities

- **[Rate Limiter](references/RATE-LIMITER.md)** - Application-layer rate limiting
- **[Aggregate](references/AGGREGATE.md)** - Efficient COUNT, SUM, MAX operations
- **[Sharded Counter](references/SHARDED-COUNTER.md)** - High-throughput counting
- **[Presence](references/PRESENCE.md)** - Real-time user presence tracking
- **[Action Cache](references/ACTION-CACHE.md)** - Cache expensive action results
- **[Migrations](references/MIGRATIONS.md)** - Stateful online data migrations

### Payments

- **[Stripe](references/STRIPE.md)** - Payments, subscriptions, and billing

### Integrations

- **[ProseMirror Sync](references/PROSEMIRROR-SYNC.md)** - Collaborative text editing (Tiptap/BlockNote)
- **[Resend](references/RESEND.md)** - Transactional email with queuing and webhooks

### AI Components

- **[Agent](../convex-agent-skill/SKILL.md)** - AI agents with persistent threads (separate skill)

## Quick Reference

| Component        | Package                        | Primary Use                |
| ---------------- | ------------------------------ | -------------------------- |
| Rate Limiter     | `@convex-dev/rate-limiter`     | Control action frequency   |
| Aggregate        | `@convex-dev/aggregate`        | Fast count/sum queries     |
| Sharded Counter  | `@convex-dev/sharded-counter`  | High-throughput counting   |
| Presence         | `@convex-dev/presence`         | Real-time user tracking    |
| Action Cache     | `@convex-dev/action-cache`     | Cache expensive results    |
| Migrations       | `@convex-dev/migrations`       | Online data migrations     |
| Workpool         | `@convex-dev/workpool`         | Queue work with limits     |
| Workflow         | `@convex-dev/workflow`         | Durable multi-step flows   |
| Action Retrier   | `@convex-dev/action-retrier`   | Retry failed actions       |
| ProseMirror Sync | `@convex-dev/prosemirror-sync` | Collaborative text editing |
| Resend           | `@convex-dev/resend`           | Transactional email        |
| Stripe           | `@convex-dev/stripe`           | Payments & subscriptions   |
| Agent            | `@convex-dev/agent`            | AI chat with history       |

## Common Patterns

### Component + Triggers

Auto-sync components with table changes using `convex-helpers` triggers:

```typescript
import { Triggers } from 'convex-helpers/server/triggers';
import {
  customCtx,
  customMutation
} from 'convex-helpers/server/customFunctions';

const triggers = new Triggers<DataModel>();

// Register component trigger
triggers.register('myTable', aggregate.trigger());

// Wrap mutation to use triggers
const mutation = customMutation(mutationRaw, customCtx(triggers.wrapDB));
```

### Testing Components

```typescript
import componentTest from '@convex-dev/<component>/test';
import { convexTest } from 'convex-test';

function initTest() {
  const t = convexTest();
  componentTest.register(t);
  return t;
}

test('component test', async () => {
  const t = initTest();
  await t.run(async (ctx) => {
    // Test with component
  });
});
```

### Dashboard Access

View component data in dashboard via component dropdown. Each component has isolated tables.

## Best Practices

1. **Name instances descriptively** - `emailWorkpool`, `scrapeWorkpool` vs generic `workpool1`
2. **Configure once** - Set options when creating instance, not per-call
3. **Use triggers for sync** - Keep aggregates in sync automatically
4. **Handle component errors** - Catch and handle gracefully when appropriate
5. **Check limits** - Respect parallelism limits on free tier (20 concurrent functions)
