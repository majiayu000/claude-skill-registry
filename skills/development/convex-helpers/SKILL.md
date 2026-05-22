---
name: convex-helpers
description: Internal query helpers for TypeScript recursion workaround in 84+ module Convex backend. Helper pattern extracts thin queries to avoid "Type instantiation excessively deep" errors. Triggers on "internal.lib.helpers", "getCurrentUser", "getConversation", "runQuery", "helper".
---

# Convex Internal Query Helpers

84 Convex modules cause TypeScript recursion limits. Solution: extract thin `internalQuery` wrappers in `convex/lib/helpers.ts`, call from actions via `internal.lib.helpers.*`.

Complements existing `@ts-ignore` casting pattern (see convex-patterns skill).

## Why Helpers Exist

TypeScript fails resolving `internal.*` types with 94+ modules:
```
error TS2589: Type instantiation is excessively deep and possibly infinite
```

Official Convex recommendation: extract 90% logic to plain TS helpers, keep wrappers thin.

Pragmatic pattern: centralized internal queries for common operations.

## Helper Structure

Location: `packages/backend/convex/lib/helpers.ts`

All helpers are `internalQuery` (not public `query`):

```typescript
export const getConversation = internalQuery({
  args: { id: v.id("conversations") },
  handler: async (ctx, args): Promise<Doc<"conversations"> | null> => {
    return await ctx.db.get(args.id);
  },
});
```

Called from actions:

```typescript
// In generation.ts, hybrid.ts, etc.
const conversation = await ctx.runQuery(
  internal.lib.helpers.getConversation,
  { id: args.conversationId }
);
```

## When to Create Helpers

**Create helper when:**
- Action needs DB access (actions can't query directly)
- Operation reused across multiple actions
- Simple, focused query (single responsibility)
- Standard CRUD (get by ID, list by index)

**Don't create helper when:**
- Complex business logic (extract to plain TS function instead)
- Only used once (inline with casting pattern)
- Mutation (use `internalMutation` in respective module)
- Auth not needed (direct `ctx.db` in query context)

## Naming Conventions

Pattern: `get{Entity}`, `list{Entity}`, `get{Entity}By{Field}s`

```typescript
getCurrentUser      // Get current authenticated user
getConversation     // Get single by ID
getConversationMessages  // List related entities
getMemoriesByIds    // Batch operation (plural field + "s")
listAllMemories     // List all for user
```

Avoid generic names like `fetch`, `load`, `retrieve`.

## Return Type Patterns

**Single entity**: `Doc<T> | null`

```typescript
export const getProject = internalQuery({
  args: { id: v.id("projects") },
  handler: async (ctx, args): Promise<Doc<"projects"> | null> => {
    return await ctx.db.get(args.id);
  },
});
```

**Collection**: `Doc<T>[]`

```typescript
export const getConversationMessages = internalQuery({
  args: { conversationId: v.id("conversations") },
  handler: async (ctx, args): Promise<Doc<"messages">[]> => {
    return await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", args.conversationId)
      )
      .order("asc")
      .collect();
  },
});
```

**Custom shape**: Explicit type annotation

```typescript
export const getApiKeyAvailability = internalQuery({
  args: {},
  handler: async (ctx) => {
    return {
      stt: {
        groq: !!process.env.GROQ_API_KEY,
        openai: !!process.env.OPENAI_API_KEY,
      },
      isProduction: process.env.NODE_ENV === "production",
    };
  },
});
```

## Auth Checks in Helpers

**getCurrentUser** - standard pattern for auth:

```typescript
export const getCurrentUser = internalQuery({
  args: {},
  handler: async (ctx): Promise<Doc<"users"> | null> => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) return null;

    return await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
      .first();
  },
});
```

Used in every action:

```typescript
// generation.ts, hybrid.ts, etc.
const user = await ctx.runQuery(internal.lib.helpers.getCurrentUser, {});
if (!user) return [];
```

**No auth required** for ID-based gets (caller owns auth):

```typescript
// No ctx.auth check - action passes valid conversationId
export const getConversation = internalQuery({
  args: { id: v.id("conversations") },
  handler: async (ctx, args): Promise<Doc<"conversations"> | null> => {
    return await ctx.db.get(args.id);
  },
});
```

## Batch Operations

**Pattern**: Accept `v.array(v.id(T))`, filter nulls

```typescript
export const getMemoriesByIds = internalQuery({
  args: { ids: v.array(v.id("memories")) },
  handler: async (ctx, args): Promise<Doc<"memories">[]> => {
    const results = await Promise.all(args.ids.map((id) => ctx.db.get(id)));
    return results.filter((m): m is Doc<"memories"> => m !== null);
  },
});
```

**For related entities**: Fetch all matching, return flat array

```typescript
export const getAttachmentsByMessageIds = internalQuery({
  args: { messageIds: v.array(v.id("messages")) },
  handler: async (ctx, args): Promise<Doc<"attachments">[]> => {
    const results = await Promise.all(
      args.messageIds.map((messageId) =>
        ctx.db
          .query("attachments")
          .withIndex("by_message", (q) => q.eq("messageId", messageId))
          .collect()
      )
    );
    return results.flat();
  },
});
```

Caller groups by key:

```typescript
// In generation.ts
const allAttachments = await ctx.runQuery(
  internal.lib.helpers.getAttachmentsByMessageIds,
  { messageIds: filteredMessages.map((m) => m._id) }
);

const attachmentsByMessage = new Map<string, Doc<"attachments">[]>();
for (const attachment of allAttachments) {
  const msgId = attachment.messageId as string;
  if (!attachmentsByMessage.has(msgId)) {
    attachmentsByMessage.set(msgId, []);
  }
  attachmentsByMessage.get(msgId)!.push(attachment);
}
```

## Usage in Actions

Standard calling pattern:

```typescript
import { internal } from "../_generated/api";

// Single entity
const user = await ctx.runQuery(internal.lib.helpers.getCurrentUser, {});

// With args
const conversation = await ctx.runQuery(
  internal.lib.helpers.getConversation,
  { id: args.conversationId }
);

// Batch
const messages = await ctx.runQuery(
  internal.lib.helpers.getConversationMessages,
  { conversationId: args.conversationId }
);
```

No `@ts-ignore` needed for helpers (clean type signatures).

## Real-World Examples

**generation.ts** - uses 7 helpers:

```typescript
// Auth check
const user = await ctx.runQuery(internal.lib.helpers.getCurrentUser, {});

// Get conversation for title check
const conversation = await ctx.runQuery(
  internal.lib.helpers.getConversation,
  { id: args.conversationId }
);

// Batch fetch attachments (O(1) query instead of O(n))
const allAttachments = await ctx.runQuery(
  internal.lib.helpers.getAttachmentsByMessageIds,
  { messageIds: filteredMessages.map((m) => m._id) }
);
```

**hybrid.ts** - auth + native API:

```typescript
const user = await (ctx.runQuery as any)(
  // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
  internal.lib.helpers.getCurrentUser,
  {}
) as Doc<"users"> | null;
if (!user) return [];
```

Note: Still needs casting when mixing with other complex calls.

## Key Files

- `packages/backend/convex/lib/helpers.ts` - All helpers (332 lines, 25 helpers)
- `packages/backend/convex/generation.ts` - Heavy user (uses 5 helpers)
- `packages/backend/convex/search/hybrid.ts` - Auth pattern example

## Anti-Patterns

**Don't inline complex logic**:

```typescript
// ❌ BAD - business logic in helper
export const getUserWithStats = internalQuery({
  handler: async (ctx) => {
    const user = await getCurrentUser(ctx);
    const stats = await calculateStats(user);
    const recommendations = await buildRecommendations(stats);
    return { user, stats, recommendations };
  },
});

// ✅ GOOD - extract to plain TS function
// helpers.ts
export const getCurrentUser = internalQuery({ ... });

// stats.ts (plain TS file)
export function buildUserStats(user: Doc<"users">, messages: Doc<"messages">[]) {
  // Complex logic here
}

// action.ts
const user = await ctx.runQuery(internal.lib.helpers.getCurrentUser, {});
const messages = await ctx.runQuery(internal.lib.helpers.getUserMessages, { userId: user._id });
const stats = buildUserStats(user, messages);
```

**Don't duplicate existing queries**:

```typescript
// ❌ BAD - Already exists as helper
export const fetchProject = internalQuery({
  args: { id: v.id("projects") },
  handler: async (ctx, args) => ctx.db.get(args.id),
});

// ✅ GOOD - Use existing getProject helper
```

**Don't add auth to entity gets**:

```typescript
// ❌ BAD - Unnecessary auth check (action owns validation)
export const getMessage = internalQuery({
  args: { id: v.id("messages") },
  handler: async (ctx, args) => {
    const user = await getCurrentUser(ctx);
    const message = await ctx.db.get(args.id);
    if (message.userId !== user._id) throw new Error("Unauthorized");
    return message;
  },
});

// ✅ GOOD - Trust caller (action already validated)
export const getMessage = internalQuery({
  args: { id: v.id("messages") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.id);
  },
});
```
