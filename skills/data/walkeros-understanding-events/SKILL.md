---
name: walkeros-understanding-events
description:
  Use when creating walkerOS events, understanding event structure, or working
  with event properties. Covers entity-action naming, event properties,
  statelessness, and vendor-agnostic design.
---

# Understanding walkerOS Events

## Overview

walkerOS events are self-describing, stateless, vendor-agnostic data structures.
They capture user interactions in a standardized format that can be transformed
for any destination.

**Core principle:** Events describe WHAT happened, not WHERE it goes. Stateless.
Self-describing. Industry-agnostic.

## Entity-Action Naming (Critical)

**STRICT REQUIREMENT:** All events use "entity action" format with space
separation.

```typescript
// Correct
'page view';
'product add';
'order complete';
'button click';

// Wrong
'page_view'; // underscore
'pageview'; // no separator
'purchase'; // no entity
'add_to_cart'; // wrong format
```

**Parsing:** `const [entity, action] = event.split(' ')`

- **Entity:** Noun (page, product, user, order, button)
- **Action:** Verb (view, add, complete, click, login)

## Event Properties

See
[packages/core/src/types/walkeros.ts](../../packages/core/src/types/walkeros.ts)
for canonical types (Event interface, plus event helpers in `event.ts`).

| Property    | Type   | Purpose                    | Example                               |
| ----------- | ------ | -------------------------- | ------------------------------------- |
| `name`      | string | "entity action" format     | `"product view"`                      |
| `data`      | object | Entity-specific properties | `{ id: "P123", price: 99 }`           |
| `context`   | object | State/environment info     | `{ stage: ["checkout", 1] }`          |
| `globals`   | object | Global properties          | `{ language: "en" }`                  |
| `user`      | object | User identification        | `{ id: "user123" }`                   |
| `nested`    | array  | Related entities           | `[{ type: "category", data: {...} }]` |
| `consent`   | object | Consent states             | `{ marketing: true }`                 |
| `id`        | string | Auto-generated unique ID   | `"1647261462000-01b5e2-2"`            |
| `timestamp` | number | Auto-generated Unix ms     | `1647261462000`                       |
| `entity`    | string | Parsed from name           | `"product"`                           |
| `action`    | string | Parsed from name           | `"view"`                              |

### data Property

Entity-specific properties. Schema-free but consistent within entity type.

```typescript
// product entity
data: { id: "P123", name: "Laptop", price: 999, currency: "USD" }

// page entity
data: { title: "Home", path: "/", referrer: "https://..." }
```

### context Property

Hierarchical state information. Format: `{ name: [value, order] }`

```typescript
context: {
  stage: ["checkout", 1],    // checkout stage, first step
  test: ["variant-A", 0],    // A/B test variant
  group: ["premium", 2]      // user segment
}
```

### globals Property

Properties that apply to ALL events in the session.

```typescript
globals: {
  language: "en",
  currency: "USD",
  environment: "production"
}
```

### nested Property

Related entities captured together.

```typescript
// Order with line items
nested: [
  { type: 'product', data: { id: 'P1', quantity: 2 } },
  { type: 'product', data: { id: 'P2', quantity: 1 } },
];
```

### user Property

User identification across sessions.

```typescript
user: {
  id: "user123",        // Your user ID
  device: "device456",  // Device fingerprint
  session: "sess789"    // Session ID
}
```

## Design Principles

### Statelessness

Events are immutable snapshots. They don't reference previous events or maintain
state.

### Self-Describing

Events contain all context needed to understand them. No external lookups
required.

### Vendor-Agnostic

Events use generic concepts (product, order) not vendor-specific (GA4 item, FB
content).

Transformation to vendor formats happens in **mapping**, not in event creation.

## Creating Events

```typescript
import { elb } from '@walkeros/collector';

// Basic event
await elb('page view', { title: 'Home', path: '/' });

// With all properties
await elb(
  'product add',
  { id: 'P123', price: 99 }, // data
  { stage: ['cart', 1] }, // context (optional)
  { currency: 'USD' }, // globals (optional)
);
```

## Related Skills

- [walkeros-understanding-mapping](../walkeros-understanding-mapping/SKILL.md) -
  Transform events for destinations
- [walkeros-understanding-flow](../walkeros-understanding-flow/SKILL.md) - Data
  flow architecture

**Source Files:**

- [packages/core/src/types/walkeros.ts](../../packages/core/src/types/walkeros.ts) -
  Event types
- [packages/core/src/schemas/](../../packages/core/src/schemas/) - Event schemas

**Documentation:**

- [Website: Event Model](../../website/docs/getting-started/event-model.mdx) -
  User-facing docs
- [walkeros.io/docs](https://www.walkeros.io/docs/) - Public documentation
