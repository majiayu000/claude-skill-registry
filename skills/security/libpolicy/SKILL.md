---
name: libpolicy
description: >
  libpolicy - Policy engine for access control. PolicyIndex stores and evaluates
  authorization policies. createPolicyIndex factory loads policies from storage.
  Planned OPA-WASM integration for complex policy evaluation. Use for access
  control, authorization decisions, and resource permissions.
---

# libpolicy Skill

## When to Use

- Implementing access control for resources
- Evaluating authorization policies
- Managing permissions in multi-tenant systems
- Building role-based access control (RBAC)

## Key Concepts

**PolicyIndex**: Stores policies and evaluates access requests against them.

**Policy evaluation**: Determines if an actor can perform an action on a
resource based on defined policies.

## Usage Patterns

### Pattern 1: Evaluate access

```javascript
import { createPolicyIndex } from "@copilot-ld/libpolicy";

const index = await createPolicyIndex(storage);
const allowed = await index.evaluate({
  actor: "user:123",
  resource: "document:456",
  action: "read",
});
```

### Pattern 2: Load policies

```javascript
const index = await createPolicyIndex(storage);
await index.load("policies/"); // Load from directory
```

## Integration

Used by ResourceIndex for access control. Policies stored in data/policies/.
