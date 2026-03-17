---
name: libresource
description: >
  libresource - Typed resource management with access control. ResourceIndex
  stores and retrieves resources with policy-based authorization. toInstance
  converts objects to typed instances. toResourceId parses URI strings.
  createResourceIndex factory. Use for persisting structured data, managing
  entities, and enforcing access control.
---

# libresource Skill

## When to Use

- Storing and retrieving typed resources
- Managing entities with access control
- Converting between resource formats
- Building resource-based APIs

## Key Concepts

**ResourceIndex**: Storage-backed index with policy enforcement for resource
access.

**Resource identifiers**: URIs that identify resource type and instance (e.g.,
`conversation:abc123`).

**toInstance**: Converts plain objects to properly typed resource instances.

## Usage Patterns

### Pattern 1: Get resource

```javascript
import { createResourceIndex } from "@copilot-ld/libresource";

const index = await createResourceIndex(storage, policyIndex);
const resource = await index.get("conversation:abc123", actor);
```

### Pattern 2: Parse resource ID

```javascript
import { toResourceId } from "@copilot-ld/libresource";

const id = toResourceId("conversation:abc123");
// { type: "conversation", id: "abc123" }
```

## Integration

Used by Memory and Agent services. Works with libpolicy for access control.
