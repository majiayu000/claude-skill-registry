---
name: walkeros-understanding-mapping
description: Use when transforming walkerOS events in the flow (source→collector or collector→destination), configuring data/map/loop/set/condition/policy, or using $code: syntax in JSON configs.
---

# Understanding walkerOS Mapping

## Overview

Mapping transforms data at multiple points in the walkerOS flow:

1. **Source → Collector**: Transform raw input (HTTP requests, dataLayer pushes)
   into walkerOS events
2. **Collector → Destination**: Transform walkerOS events into vendor-specific
   formats

**Core principle:** Mapping is the universal transformation layer. Same
strategies work everywhere in the flow.

## Core Functions

See [packages/core/src/mapping.ts](../../packages/core/src/mapping.ts) for
implementation.

| Function                                        | Purpose                                     |
| ----------------------------------------------- | ------------------------------------------- |
| `getMappingEvent(event, rules)`                 | Find mapping rule for an event              |
| `getMappingValue(value, data, options)`         | Transform a value using mapping config      |
| `processEventMapping(event, config, collector)` | Unified processing for sources/destinations |

### processEventMapping Flow

```text
1. Apply config.policy (modifies event)
2. Find matching rule via getMappingEvent()
3. Apply rule.policy (modifies event)
4. Transform config.data (global)
5. Check rule.ignore
6. Override event.name if rule.name
7. Transform rule.data (event-specific)
```

---

## Configuration Hierarchy

### Mapping.Config (Top Level)

```typescript
interface Config {
  consent?: Consent; // Required consent for ALL events
  data?: Value; // Global data transformation
  policy?: Policy; // Pre-processing for ALL events
  mapping?: Rules; // Event-specific rules
}
```

### Mapping.Rule (Per Event)

```typescript
interface Rule {
  name?: string; // Override event name
  data?: Value; // Event-specific data transformation
  ignore?: boolean; // Skip this event entirely
  policy?: Policy; // Event-specific pre-processing
  condition?: Function; // Match condition (for arrays)
  consent?: Consent; // Required consent for this rule
  settings?: unknown; // Custom event configuration
  batch?: number; // Batch size for grouping
}
```

### Mapping.ValueConfig (Value Extraction)

```typescript
interface ValueConfig {
  key?: string; // Extract from path
  value?: Primitive; // Static fallback value
  fn?: Function; // Custom transformation
  map?: Record; // Object transformation
  loop?: [path, config]; // Array transformation
  set?: Value[]; // Create array from values
  condition?: Function; // Conditional extraction
  consent?: Consent; // Consent-gated extraction
  validate?: Function; // Value validation
}
```

---

## Event Matching

Match events to transformation rules by entity and action.

```typescript
const mapping = {
  // Exact match: "product view" → view_item
  product: {
    view: { name: 'view_item' },
    add: { name: 'add_to_cart' },
  },

  // Wildcard action: "foo *" → foo_interaction
  foo: {
    '*': { name: 'foo_interaction' },
  },

  // Wildcard entity: "* click" → generic_click
  '*': {
    click: { name: 'generic_click' },
  },
};
```

### Conditional Mapping (Array)

Array of rules - first matching condition wins:

```typescript
order: {
  complete: [
    {
      condition: (event) => event.data?.value > 100,
      name: 'high_value_purchase',
    },
    { name: 'purchase' }, // Fallback (no condition)
  ],
}
```

**JSON with $code:**

```json
{
  "order": {
    "complete": [
      {
        "condition": "$code:(event) => event.data?.value > 100",
        "name": "high_value_purchase"
      },
      { "name": "purchase" }
    ]
  }
}
```

---

## Value Mapping Strategies

Common patterns shown below. For detailed examples of all 12 strategies, see
[value-strategies.md](value-strategies.md).

### Essential Patterns

```typescript
// Key extraction (string shorthand)
'data.price'                              // → event.data.price

// Key with fallback
{ key: 'data.currency', value: 'USD' }    // Use USD if missing

// Static value
{ value: 'USD' }

// Function transform
{ fn: (event) => event.data.price * 100 } // Convert to cents

// Object map
{ map: { item_id: 'data.id', item_name: 'data.name' } }

// Array loop
{ loop: ['nested', { map: { item_id: 'data.id' } }] }

// Loop with "this" (single item as array)
{ loop: ['this', { map: { item_id: 'data.id' } }] }

// Set (create array)
{ set: ['data.id'] }                      // → ["SKU-123"]

// Fallback array (first success wins)
[{ key: 'data.sku' }, { key: 'data.id' }, { value: 'unknown' }]

// Consent-gated
{ key: 'user.email', consent: { marketing: true } }

// Validate
{ key: 'data.email', validate: (v) => v.includes('@') }
```

---

## Policy (Pre-Processing)

Policy modifies the event BEFORE mapping rules are applied. Use for:

- Adding computed fields
- Normalizing data structure
- Consent-gated field injection

### Config-Level Policy

Applied to ALL events:

```typescript
config: {
  policy: {
    'user_data.external_id': 'user.id',
    'custom_data.server_processed': { value: true },
  },
  mapping: { /* ... */ }
}
```

### Event-Level Policy

Applied after config policy, only for specific event:

```typescript
mapping: {
  order: {
    complete: {
      policy: {
        'enriched.total_cents': {
          fn: (event) => Math.round(event.data.total * 100)
        }
      },
      name: 'purchase',
      data: { /* ... */ }
    }
  }
}
```

### Policy with Consent

```json
{
  "policy": {
    "user_data.em": {
      "key": "user.email",
      "consent": { "marketing": true }
    }
  }
}
```

---

## Rule Features

### Ignore Events

```typescript
mapping: {
  test: { '*': { ignore: true } },  // Ignore all test events
}
```

### Batch Processing

```typescript
mapping: {
  '*': {
    '*': {
      batch: 5,  // Send after 5 events
    }
  }
}
```

### Custom Settings

```typescript
mapping: {
  order: {
    complete: {
      name: 'purchase',
      settings: { priority: 'high', retryCount: 3 }
    }
  }
}
```

---

## $code: Prefix (JSON Configs)

The `$code:` prefix enables JavaScript functions in JSON configurations:

```json
{
  "fn": "$code:(event) => event.data.price * 100",
  "condition": "$code:(event) => event.data?.value > 100",
  "validate": "$code:(value) => value > 0"
}
```

**Important:** The `$code:` prefix is processed by the CLI bundler. It converts
JSON strings to actual JavaScript functions during build.

### Function Signatures

| Context             | Signature                                |
| ------------------- | ---------------------------------------- |
| `fn`                | `(value, mapping, options) => result`    |
| `condition` (value) | `(value, mapping, collector) => boolean` |
| `condition` (rule)  | `(event) => boolean`                     |
| `validate`          | `(value) => boolean`                     |
| `loop` condition    | `(item) => boolean`                      |

---

## Quick Reference

### Value Extraction Cheatsheet

| Pattern                       | Result                         |
| ----------------------------- | ------------------------------ |
| `"data.id"`                   | Extract `event.data.id`        |
| `{ value: "USD" }`            | Static `"USD"`                 |
| `{ key: "x", value: "y" }`    | Extract `x`, fallback to `"y"` |
| `{ fn: (e) => ... }`          | Custom function                |
| `{ map: {...} }`              | Object transformation          |
| `{ loop: ["nested", {...}] }` | Array transformation           |
| `{ loop: ["this", {...}] }`   | Single-item as array           |
| `{ set: ["a", "b"] }`         | Create array `[valA, valB]`    |
| `[m1, m2, m3]`                | Fallback chain                 |
| `{ consent: {...} }`          | Consent-gated                  |
| `{ condition: fn }`           | Conditional                    |
| `{ validate: fn }`            | Validated                      |

### Rule Features Cheatsheet

| Feature     | Purpose                  |
| ----------- | ------------------------ |
| `name`      | Override event name      |
| `data`      | Transform event data     |
| `ignore`    | Skip event entirely      |
| `policy`    | Pre-process event        |
| `condition` | Match condition (arrays) |
| `consent`   | Required consent         |
| `settings`  | Custom configuration     |
| `batch`     | Batch size               |

### Config Features Cheatsheet

| Feature   | Purpose                       |
| --------- | ----------------------------- |
| `consent` | Required consent (all events) |
| `data`    | Global data transformation    |
| `policy`  | Global pre-processing         |
| `mapping` | Event-specific rules          |

---

## Complete Examples

For full destination configuration examples (TypeScript + JSON), see
[complete-examples.md](complete-examples.md).

---

## Where Mapping Lives

| Location                                   | Purpose                                   |
| ------------------------------------------ | ----------------------------------------- |
| Source config                              | Transform raw input → walkerOS events     |
| Destination config                         | Transform walkerOS events → vendor format |
| `packages/core/src/mapping.ts`             | Core mapping functions                    |
| `packages/core/src/types/mapping.ts`       | Type definitions                          |
| `packages/cli/examples/flow-complete.json` | Comprehensive example (53 features)       |

---

## Related Skills

- [walkeros-understanding-events](../walkeros-understanding-events/SKILL.md) -
  Event structure
- [walkeros-understanding-destinations](../walkeros-understanding-destinations/SKILL.md) -
  Destination-side mapping
- [walkeros-mapping-configuration](../walkeros-mapping-configuration/SKILL.md) -
  Recipes and patterns

**Source Files:**

- [packages/core/src/mapping.ts](../../packages/core/src/mapping.ts) -
  Implementation
- [packages/core/src/types/mapping.ts](../../packages/core/src/types/mapping.ts) -
  Types

**Detailed References:**

- [value-strategies.md](value-strategies.md) - All 12 value extraction
  strategies with examples
- [complete-examples.md](complete-examples.md) - Full destination config
  examples

**Examples:**

- [packages/cli/examples/flow-complete.json](../../packages/cli/examples/flow-complete.json) -
  Comprehensive example
- [packages/cli/examples/flow-complete.md](../../packages/cli/examples/flow-complete.md) -
  Feature inventory
