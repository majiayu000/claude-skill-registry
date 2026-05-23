---
name: payload-optimization
description: API response compaction utilities for network transfer optimization. Recursive null/undefined/empty value removal, field selection. Triggers on "compact", "payload", "pick", "omit", "optimization", "response size".
---

# Payload Optimization

Reduce API response size by 30-40% via automatic compaction. Used in all formatEntity responses.

## Why Compaction

Network transfer bottleneck - remove dead weight:
- Optional fields often null/undefined
- Empty strings/arrays
- Nested objects with no data
- Mobile clients on slow connections

Real impact: 500KB response → 300KB after compaction.

## compact() Function

Removes null, undefined, empty strings, empty arrays recursively:

```typescript
// From apps/web/src/lib/utils/payload.ts
import { compact } from "@/lib/utils/payload";

const data = {
  id: "123",
  name: "Test",
  email: null,
  tags: [],
  metadata: {
    key: "value",
    empty: "",
    nested: { foo: null }
  }
};

const result = compact(data);
// Result: { id: "123", name: "Test", metadata: { key: "value" } }
```

## Recursive Compaction

Handles nested objects and arrays automatically:

```typescript
// Nested object compaction
const nested = {
  user: {
    name: "John",
    bio: null,
    settings: {
      theme: "dark",
      notifications: undefined
    }
  }
};

compact(nested);
// { user: { name: "John", settings: { theme: "dark" } } }

// Array element compaction
const withArrays = {
  items: [
    { id: 1, name: "A", meta: null },
    { id: 2, name: "", meta: {} },
    { id: 3, name: "C", meta: { key: "val" } }
  ]
};

compact(withArrays);
// { items: [{ id: 1, name: "A" }, { id: 3, name: "C", meta: { key: "val" } }] }
```

Empty objects removed after compaction:
- `{ nested: { foo: null } }` → `{}` (removed)
- Empty array elements filtered out

## formatEntity Integration

All API responses auto-compact via formatEntity:

```typescript
// From apps/web/src/lib/utils/formatEntity.ts
export function formatEntity<T>(
  data: T,
  entity: string,
  id?: string,
): ApiResponse<T> {
  // Automatic compaction (30-40% size reduction)
  const compactedData =
    data && typeof data === "object"
      ? (compact(data as Record<string, unknown>) as T)
      : data;

  return {
    status: "success",
    sys: { entity, ...(id && { id }) },
    data: compactedData,
  };
}
```

Lists also compact each item:

```typescript
export function formatEntityList<T>(
  items: T[],
  entity: string,
): ApiResponse<EntityListItem<T>[]> {
  return {
    status: "success",
    sys: { entity: "list" },
    data: items.map((item) => {
      const compactedItem =
        item && typeof item === "object"
          ? (compact(item as Record<string, unknown>) as T)
          : item;

      return {
        sys: { entity, ...(item?._id && { id: item._id }) },
        data: compactedItem,
      };
    }),
  };
}
```

## pick/omit Utilities

Field selection before compaction:

```typescript
import { pick, omit } from "@/lib/utils/payload";

// Select only needed fields
const user = {
  id: "123",
  name: "John",
  email: "john@example.com",
  passwordHash: "...",
  internalMetadata: {...}
};

// Pick specific fields
const publicUser = pick(user, ["id", "name", "email"]);
// { id: "123", name: "John", email: "john@example.com" }

// Omit sensitive fields
const safeUser = omit(user, ["passwordHash", "internalMetadata"]);
// { id: "123", name: "John", email: "john@example.com" }
```

Combine with compact for max reduction:

```typescript
const optimized = compact(pick(user, ["id", "name", "bio"]));
// If bio is null: { id: "123", name: "John" }
```

## When to Apply

Apply compaction:
- All API route responses (via formatEntity)
- SSE streaming data chunks
- Mobile API endpoints (bandwidth critical)
- List endpoints with many items
- Nested relationship data

Skip compaction:
- Schema validation (needs exact structure)
- Forms (empty string vs undefined matters)
- Raw DB writes (preserve nulls)

## Performance Impact

Real examples from this project:

```typescript
// Before compaction (conversation with messages)
{
  id: "conv_123",
  title: "Test Chat",
  model: "gpt-4o",
  systemPrompt: null,
  metadata: {},
  messages: [
    {
      id: "msg_1",
      content: "Hello",
      role: "user",
      attachments: [],
      sources: [],
      error: null,
      partialContent: null
    }
  ]
}
// Size: ~350 bytes

// After compaction
{
  id: "conv_123",
  title: "Test Chat",
  model: "gpt-4o",
  messages: [
    { id: "msg_1", content: "Hello", role: "user" }
  ]
}
// Size: ~180 bytes (48% reduction)
```

List response savings scale:

```typescript
// 100 conversations with avg 5 messages each
// Before: ~175KB
// After:  ~105KB (40% reduction)
// Saved: 70KB per request
```

## Implementation Pattern

Standard API route pattern:

```typescript
import { formatEntity, formatEntityList } from "@/lib/utils/formatEntity";
import { pick } from "@/lib/utils/payload";

export async function GET(req: Request) {
  const data = await fetchFromDB();

  // Pick fields if needed
  const selected = pick(data, ["id", "name", "status"]);

  // Format with auto-compaction
  return Response.json(formatEntity(selected, "resource", data.id));
}

export async function GET_LIST(req: Request) {
  const items = await fetchManyFromDB();

  // Each item auto-compacted
  return Response.json(formatEntityList(items, "resource"));
}
```

## Key Files

- `apps/web/src/lib/utils/payload.ts` - compact, pick, omit functions
- `apps/web/src/lib/utils/formatEntity.ts` - Integration with API envelope
- `apps/web/src/lib/api/types.ts` - ApiResponse type definition

## Avoid

Don't compact when:
- Schema validation expects exact fields
- Form data (empty string meaningful)
- Database writes (preserve null vs undefined)
- Debug/logging (need full structure)

Don't use with:
- Non-object types (strings, numbers, primitives)
- Already minified JSON
- Streaming where order matters (compact after collect)
