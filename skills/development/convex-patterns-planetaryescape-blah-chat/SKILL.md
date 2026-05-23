---
name: convex-patterns
description: Convex backend patterns for this project. Query/mutation/action structure, TypeScript recursion workarounds, auth patterns, resilient generation (10min actions), normalized schema design. Triggers on "convex", "mutation", "query", "action", "internalQuery", "internalMutation", "internalAction".
---

# Convex Backend Patterns

94+ Convex modules power the backend. Real-time queries, mutations for writes, actions for LLM calls (10min limit). Normalized schema design (no nested documents).

## Query/Mutation/Action Structure

Three function types:

```typescript
// QUERY: Read-only, reactive, client-subscribable
export const getUser = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    return await ctx.db.get(args.userId);
  },
});

// MUTATION: Write operations, trigger re-renders
export const updateUser = mutation({
  args: { userId: v.id("users"), name: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.userId, { name: args.name });
  },
});

// ACTION: External APIs, LLM calls, long-running (up to 10min)
export const generateResponse = action({
  args: { conversationId: v.id("conversations"), modelId: v.string() },
  handler: async (ctx, args) => {
    // Call external API (Vercel AI Gateway)
    const result = await streamText({ model, messages });
    // Update DB via mutation
    await ctx.runMutation(internal.messages.create, { ... });
  },
});
```

**When to use**:
- Query: Real-time data fetch (conversations, messages, users)
- Mutation: DB writes (create message, update status)
- Action: LLM streaming, embeddings, external HTTP calls

## TypeScript Recursion Workaround

With 94+ modules, TypeScript hits depth limits on `internal.*` and `api.*` types. Use `@ts-ignore` + cast pattern:

```typescript
// From convex/generation.ts line 100-110
const costBias = await (ctx.runQuery as any)(
  // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
  api.users.getUserPreferenceByUserId,
  { userId: args.userId, key: "autoRouterCostBias" },
) as Promise<number | null>;

// From convex/chat.ts line 166-174
const conversationId = await ctx.runMutation(
  // @ts-ignore - TypeScript recursion limit with 85+ Convex modules
  internal.conversations.createInternal,
  {
    userId: user._id,
    model: modelsToUse[0],
    title: "New Chat",
  },
);
```

**Pattern**: `(ctx.runX as any)` + `@ts-ignore` on reference + `as ReturnType`. Bypasses parameter inference, keeps return type safety.

## Auth Pattern (Defense-in-Depth)

Every query/mutation verifies user via internal helper:

```typescript
// From convex/lib/userSync.ts (pattern)
export async function getCurrentUserOrCreate(ctx: MutationCtx) {
  const identity = await ctx.auth.getUserIdentity();
  if (!identity) throw new Error("Not authenticated");

  const user = await ctx.db
    .query("users")
    .withIndex("by_clerk_id", (q) => q.eq("clerkId", identity.subject))
    .first();

  if (!user) throw new Error("User not found");
  return user;
}

// Usage in mutations (from convex/chat.ts line 91)
const user = await getCurrentUserOrCreate(ctx);
```

**Actions use internal queries**:

```typescript
// From convex/lib/helpers.ts line 30-41
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

// Called from actions
const user = await ctx.runQuery(internal.lib.helpers.getCurrentUser, {});
```

## Normalized Schema Design

NO nested documents. Use junction tables for M:N relationships.

**Bad** (nested):
```typescript
// ❌ DON'T DO THIS
defineTable("messages", {
  attachments: v.optional(v.array(v.object({
    name: v.string(),
    storageId: v.string(),
    size: v.number(),
  }))),
})
```

**Good** (normalized):
```typescript
// ✅ From convex/schema.ts line 304-337
attachments: defineTable({
  messageId: v.id("messages"),
  conversationId: v.id("conversations"), // Denormalized for filtering
  userId: v.id("users"),
  type: v.union(v.literal("image"), v.literal("file"), v.literal("audio")),
  name: v.string(),
  storageId: v.id("_storage"),
  mimeType: v.string(),
  size: v.number(),
  createdAt: v.number(),
})
  .index("by_message", ["messageId"])
  .index("by_conversation", ["conversationId"])
  .index("by_user", ["userId"])
```

**Junction tables for M:N**:

```typescript
// From convex/schema.ts line 552-560
projectConversations: defineTable({
  projectId: v.id("projects"),
  conversationId: v.id("conversations"),
  addedAt: v.number(),
  addedBy: v.id("users"),
})
  .index("by_project", ["projectId"])
  .index("by_conversation", ["conversationId"])
  .index("by_project_conversation", ["projectId", "conversationId"])
```

**Benefits**: 40% smaller docs, 10x faster cascade deletes, queryable relationships, no data drift.

## Resilient Generation Pattern

LLM calls MUST survive page refresh. Use 10min actions + DB persistence.

**Flow** (from convex/chat.ts + generation.ts):

```typescript
// 1. Pre-create message with status: "pending"
const assistantMessageId = await ctx.runMutation(internal.messages.create, {
  conversationId,
  userId: user._id,
  role: "assistant",
  content: "",
  status: "pending", // Not "generating" yet
  model,
});

// 2. Schedule action (non-blocking)
await ctx.scheduler.runAfter(0, internal.generation.generateResponse, {
  conversationId,
  existingMessageId: assistantMessageId,
  modelId,
  userId: user._id,
});

// 3. Action updates status → "generating" → streams to partialContent → "complete"
await ctx.runMutation(internal.messages.updateStatus, {
  messageId: assistantMessageId,
  status: "generating",
  generationStartedAt: Date.now(),
});

// 4. Stream updates DB periodically (every 500ms)
for await (const chunk of stream) {
  accumulatedContent += chunk;
  await ctx.runMutation(internal.messages.updatePartialContent, {
    messageId: assistantMessageId,
    partialContent: accumulatedContent,
  });
}

// 5. Finalize on complete
await ctx.runMutation(internal.messages.updateStatus, {
  messageId: assistantMessageId,
  status: "complete",
  content: finalContent,
  partialContent: undefined,
  generationCompletedAt: Date.now(),
});
```

**Message states**: `pending` | `generating` | `complete` | `stopped` | `error`

**Client subscribes**:
```typescript
const message = useQuery(api.messages.get, { id: messageId });
// Auto-updates as partialContent changes
```

**On refresh**: Client sees `partialContent` from DB, streaming continues server-side.

## Index Requirements

Every foreign key needs index. Composite indexes for common queries.

```typescript
// From convex/schema.ts line 282-301
messages: defineTable({ ... })
  .index("by_conversation", ["conversationId"])
  .index("by_user", ["userId"])
  .index("by_conversation_status", ["conversationId", "status"]) // Find generating messages
  .index("by_conversation_created", ["conversationId", "createdAt"]) // Ordered messages
  .vectorIndex("by_embedding", {
    vectorField: "embedding",
    dimensions: 1536,
    filterFields: ["conversationId", "userId"],
  })
  .searchIndex("search_content", {
    searchField: "content",
    filterFields: ["conversationId", "userId", "role"],
  })
```

**Index types**:
- **Simple**: `["userId"]` - Foreign keys
- **Composite**: `["userId", "status"]` - Filtered queries
- **Vector**: Semantic search (1536d embeddings)
- **Search**: Full-text search (Convex native)

## Internal Helpers Pattern

Avoid type recursion by extracting helpers:

```typescript
// From convex/lib/helpers.ts line 58-69
export const getConversationMessages = internalQuery({
  args: { conversationId: v.id("conversations") },
  handler: async (ctx, args): Promise<Doc<"messages">[]> => {
    return await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", args.conversationId))
      .order("asc")
      .collect();
  },
});
```

**Usage in actions**:
```typescript
const messages = await ctx.runQuery(
  internal.lib.helpers.getConversationMessages,
  { conversationId }
);
```

**All helpers**: `getCurrentUser`, `getConversation`, `getConversationMessages`, `getMemoriesByIds`, `getMessage`, `getMessageAttachments`, etc.

## Testing Patterns

Use `convex-test` with factories:

```typescript
// From convex/__tests__/users.test.ts
import { convexTest } from "../../__tests__/testSetup";
import { createMockIdentity, createTestUserData } from "@/lib/test/factories";
import schema from "../schema";

it("returns user for authenticated identity", async () => {
  const t = convexTest(schema);
  const identity = createMockIdentity();

  await t.run(async (ctx) => {
    await ctx.db.insert("users", createTestUserData({
      clerkId: identity.subject,
      email: "test@example.com",
    }));
  });

  const asUser = t.withIdentity(identity);
  // @ts-ignore - Type instantiation too deep with 94+ Convex modules
  const result = await asUser.query(api.users.getCurrentUser, {});

  expect(result?.email).toBe("test@example.com");
});
```

**Factories** (`src/lib/test/factories.ts`):
- `createMockIdentity()` - Auth identity
- `createTestUserData()` - User record
- `createTestConversationData()` - Conversation
- `createTestMessageData()` - Message

**Pattern**: `t.run()` for DB setup, `t.withIdentity()` for auth context, `@ts-ignore` on type-deep queries.

## Key Files

- `convex/schema.ts` - Normalized schema (1546 lines)
- `convex/chat.ts` - Message sending, regeneration
- `convex/generation.ts` - LLM streaming action (resilient)
- `convex/lib/helpers.ts` - Internal query helpers (avoid recursion)
- `convex/__tests__/users.test.ts` - Testing patterns
- `convex/lib/userSync.ts` - Auth helpers (getCurrentUserOrCreate)
- `convex/messages.ts` - Message mutations (status, partialContent)

## Avoid

- Nested documents in schema (use junction tables)
- Client-only streaming (loses data on refresh)
- Direct `ctx.runQuery(api.*)` in actions without cast (type errors)
- Missing indexes on foreign keys (slow queries)
- Queries in actions without internal helper (type depth errors)
- Mutations for LLM calls (10s timeout, use actions)
