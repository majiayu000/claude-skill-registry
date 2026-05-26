---
name: api-envelope-pattern
description: Standard API envelope pattern for all responses (success/list/error). Wraps data in consistent structure with sys metadata, automatic payload compaction (30-40% reduction), timestamp injection. Triggers on "formatEntity", "formatEntityList", "formatErrorEntity", "API", "route handler", "dal".
---

# API Envelope Pattern

ALL API responses MUST use standard envelope pattern. NEVER return raw Convex docs or plain data. Consistent structure enables mobile clients, monitoring, caching.

## Standard Envelope Structure

Every response wrapped in `ApiResponse<T>`:

```typescript
// Success (single entity)
{
  status: "success",
  sys: {
    entity: "conversation",
    id: "j97...",
    timestamps?: {
      created: "2024-01-15T10:30:00.000Z",
      updated: "2024-01-15T12:45:00.000Z",
      retrieved: "2024-01-15T13:00:00.000Z"
    }
  },
  data: { ... }  // Compacted data (nulls/empty removed)
}

// List response
{
  status: "success",
  sys: { entity: "list" },
  data: [
    {
      sys: { entity: "conversation", id: "j97..." },
      data: { ... }
    }
  ]
}

// Error response
{
  status: "error",
  sys: { entity: "error" },
  error: "Resource not found"  // or { message, code, details }
}
```

## Entity Formatters

Use these helpers from `@/lib/utils/formatEntity`:

### formatEntity (Single Item)

```typescript
// From convex/api/dal/conversations.ts
return formatEntity(conversation, "conversation", conversation._id);

// Auto-injects timestamps from Convex _creationTime + updatedAt
// Compacts data (removes null/undefined/empty)
```

### formatEntityList (Arrays)

```typescript
// From convex/api/dal/conversations.ts
return conversations.map((conversation) =>
  formatEntity(conversation, "conversation", conversation._id)
);

// Each item wrapped with sys metadata
// Lists use sys.entity = "list" at top level
```

### formatErrorEntity (Errors)

```typescript
// String error
return NextResponse.json(formatErrorEntity("Verse not found"), {
  status: 404
});

// Structured error (from error middleware)
return NextResponse.json(
  formatErrorEntity({
    message: error.message,
    code: error.code,
  }),
  { status: error.statusCode }
);

// With details (e.g., Zod validation)
formatErrorEntity({
  message: "Validation failed",
  code: "VALIDATION_ERROR",
  details: zodError.issues,
})
```

## Compact Utility (30-40% Payload Reduction)

Automatically strips null/undefined/empty values:

```typescript
// From lib/utils/payload.ts
compact({
  a: 1,
  b: null,
  c: undefined,
  d: "",
  e: [],
  f: { nested: null }
})
// Returns: { a: 1 }

// Applied automatically in formatEntity/formatEntityList
// Recursive for nested objects and arrays
```

**What gets removed:**
- `null` and `undefined` values
- Empty strings (`""`)
- Empty arrays (`[]`)
- Empty objects after compaction (`{}`)

## Timestamp Injection

Automatic timestamp extraction from Convex:

```typescript
// formatEntity reads:
// - data._creationTime → sys.timestamps.created
// - data.updatedAt → sys.timestamps.updated
// - new Date() → sys.timestamps.retrieved

// Example output
{
  sys: {
    entity: "conversation",
    id: "j97...",
    timestamps: {
      created: "2024-01-15T10:30:00.000Z",
      updated: "2024-01-15T12:45:00.000Z",
      retrieved: "2024-01-15T13:00:00.000Z"
    }
  }
}
```

## DAL Layer Pattern

Data Access Layer (DAL) functions MUST return formatted entities:

```typescript
// From lib/api/dal/conversations.ts
export const conversationsDAL = {
  create: async (_userId: string, data: CreateData) => {
    const conversationId = await convex.mutation(api.conversations.create, data);
    const conversation = await convex.query(api.conversations.get, { conversationId });

    // ALWAYS format before returning
    return formatEntity(conversation, "conversation", conversation._id);
  },

  list: async (_userId: string, limit = 50, archived = false) => {
    const conversations = await convex.query(api.conversations.list, { limit, archived });

    // Map each item through formatEntity
    return conversations.map((c) =>
      formatEntity(c, "conversation", c._id)
    );
  },

  delete: async (userId: string, conversationId: string, sessionToken: string) => {
    await authConvex.mutation(api.conversations.deleteConversation, { conversationId });

    // Even for operations without response data
    return formatEntity(
      { deleted: true, conversationId },
      "conversation",
      conversationId
    );
  },
};
```

## Route Handler Pattern

API routes wrap DAL responses:

```typescript
// From app/api/v1/conversations/route.ts
async function postHandler(req: NextRequest, { userId }: { userId: string }) {
  const body = await parseBody(req, createSchema);
  const result = await conversationsDAL.create(userId, body);

  // DAL already formatted - return directly
  return NextResponse.json(result, { status: 201 });
}

async function getHandler(req: NextRequest, { userId }: { userId: string }) {
  const conversations = await conversationsDAL.list(userId, limit, archived);

  // Wrap list in top-level envelope
  return NextResponse.json(
    formatEntity(
      { items: conversations, total: conversations.length },
      "list",
    ),
    { headers: { "Cache-Control": cacheControl } }
  );
}

export const POST = withErrorHandling(withAuth(postHandler));
export const GET = withErrorHandling(withAuth(getHandler));
```

## Error Handling Middleware

`withErrorHandling` automatically wraps errors:

```typescript
// From lib/api/middleware/errors.ts
export function withErrorHandling(handler) {
  return async (req, context) => {
    try {
      return await handler(req, context);
    } catch (error) {
      // ApiError - custom errors
      if (error instanceof ApiError) {
        return NextResponse.json(
          formatErrorEntity({ message: error.message, code: error.code }),
          { status: error.statusCode }
        );
      }

      // Zod validation errors
      if (error instanceof z.ZodError) {
        return NextResponse.json(
          formatErrorEntity({
            message: "Validation failed",
            code: "VALIDATION_ERROR",
            details: error.issues,
          }),
          { status: 400 }
        );
      }

      // Pattern matching Convex errors
      if (error.message.includes("not found")) {
        return NextResponse.json(formatErrorEntity("Resource not found"), {
          status: 404,
        });
      }

      // Fallback
      return NextResponse.json(formatErrorEntity("Internal server error"), {
        status: 500,
      });
    }
  };
}
```

## Frontend Unwrapping

Clients MUST unwrap `.data` property:

```typescript
// From lib/api/client.ts
async function fetchWithAuth<T>(url, options, getToken) {
  const response = await fetch(url, options);
  const data: ApiResponse<T> = await response.json();

  if (!response.ok || data.status === "error") {
    const msg = typeof data.error === "string" ? data.error : data.error?.message;
    const code = typeof data.error === "object" ? data.error?.code : undefined;
    throw new ApiClientError(response.status, code, msg);
  }

  // CRITICAL: Unwrap envelope before returning
  return data.data as T;
}

// Usage in components
const client = useApiClient();
const conversation = await client.get<Conversation>("/api/v1/conversations/123");
// conversation is unwrapped - direct access to fields
```

## Type Definitions

```typescript
// From lib/api/types.ts
export type ApiResponse<T> = {
  status: "success" | "error";
  sys: {
    entity: string;
    id?: string;
    timestamps?: {
      created?: string;
      updated?: string;
      retrieved?: string;
    };
    async?: boolean;
  };
  data?: T;
  error?: string | { message: string; code?: string; details?: unknown };
};

export type EntityListItem<T> = {
  sys: {
    entity: string;
    id?: string;
  };
  data: T;
};
```

## Key Files

- `apps/web/src/lib/utils/formatEntity.ts` - Core formatters
- `apps/web/src/lib/utils/payload.ts` - compact() utility
- `apps/web/src/lib/api/types.ts` - TypeScript types
- `apps/web/src/lib/api/middleware/errors.ts` - Auto-wrapping errors
- `apps/web/src/lib/api/client.ts` - Frontend unwrapping
- `apps/web/src/lib/api/dal/*.ts` - DAL examples
- `apps/web/src/app/api/v1/*/route.ts` - Route handler examples

## Common Mistakes

❌ **Returning raw Convex documents:**
```typescript
// WRONG
return NextResponse.json(conversation);
```

✅ **Always use formatEntity:**
```typescript
// CORRECT
return NextResponse.json(formatEntity(conversation, "conversation", conversation._id));
```

❌ **Forgetting to unwrap on frontend:**
```typescript
// WRONG - accessing envelope directly
const title = response.data.title; // undefined!
```

✅ **Use client helper that unwraps:**
```typescript
// CORRECT
const conversation = await client.get<Conversation>("/api/v1/conversations/123");
const title = conversation.title; // works!
```

❌ **Manually creating envelope structure:**
```typescript
// WRONG - bypasses compaction and timestamp logic
return { status: "success", sys: { entity: "user" }, data: user };
```

✅ **Always use formatter functions:**
```typescript
// CORRECT
return formatEntity(user, "user", user._id);
```

❌ **Not using error formatter:**
```typescript
// WRONG
return NextResponse.json({ error: "Not found" }, { status: 404 });
```

✅ **Use formatErrorEntity:**
```typescript
// CORRECT
return NextResponse.json(formatErrorEntity("Not found"), { status: 404 });
```

## Benefits

1. **Consistency**: All endpoints same structure
2. **Mobile-friendly**: REST clients expect envelopes
3. **Monitoring**: sys metadata enables tracking
4. **Caching**: Timestamps enable ETags/Last-Modified
5. **Performance**: 30-40% smaller payloads via compact()
6. **Type safety**: Single ApiResponse<T> type
7. **Error handling**: Structured error format
8. **Debugging**: entity/id in every response

## Mobile API Integration

Mobile clients (React Native) use REST endpoints, not Convex SDK. Envelope pattern critical for:
- SSE streaming (parseable chunks)
- React Query caching (needs metadata)
- Offline queue (structured errors)
- Request deduplication (sys.id)

See `docs/api/mobile-integration.md` for full mobile patterns.
