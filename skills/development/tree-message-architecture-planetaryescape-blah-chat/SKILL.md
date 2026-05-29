---
name: tree-message-architecture
description: Message tree architecture with DAG structure, branching, and active path tracking. Covers parent/child/sibling queries, BFS traversal, cycle detection, active leaf tracking, and legacy field migration. Use when working with messages, conversation branching, tree navigation, parent/child relationships, siblings, activeLeaf, or any branching-related features.
---

# Tree Message Architecture

Messages form a DAG (Directed Acyclic Graph) allowing branches, siblings, and path tracking. Core pattern: dual parent fields (legacy + array), active path via `activeLeafMessageId`, BFS traversal for descendants.

## Parent Relationship (Dual Fields)

Messages support BOTH legacy and new parent tracking:

```typescript
// Schema (convex/schema.ts:200-207)
parentMessageId: v.optional(v.id("messages")), // DEPRECATED: Use parentMessageIds
parentMessageIds: v.optional(v.array(v.id("messages"))), // Multiple parents for merges
siblingIndex: v.optional(v.number()), // Position among siblings (0, 1, 2...)
isActiveBranch: v.optional(v.boolean()), // Part of currently displayed path
```

**Migration pattern**: Prefer array, fallback to legacy:

```typescript
// From tree.ts:90, 118, 148
const parentId = message.parentMessageIds?.[0] ?? message.parentMessageId;
```

**Why both**: Gradual migration without breaking existing messages. New code writes `parentMessageIds`, reads both.

## Children Queries (Handles Both Formats)

Get all children of a message (messages with this as parent):

```typescript
// From tree.ts:31-69
export async function getChildren(
  ctx: QueryCtx | MutationCtx,
  messageId: Id<"messages">,
): Promise<Message[]> {
  // Query by legacy parentMessageId first (indexed)
  const legacyChildren = await ctx.db
    .query("messages")
    .withIndex("by_parent", (q) => q.eq("parentMessageId", messageId))
    .collect();

  // For parentMessageIds array, scope to conversation to avoid full table scan
  const parentMessage = await ctx.db.get(messageId);
  let arrayChildren: Message[] = [];

  if (parentMessage) {
    const conversationMessages = await ctx.db
      .query("messages")
      .withIndex("by_conversation", (q) =>
        q.eq("conversationId", parentMessage.conversationId),
      )
      .collect();

    arrayChildren = conversationMessages.filter(
      (m) => m.parentMessageIds?.includes(messageId) && !m.parentMessageId,
    );
  }

  // Combine and dedupe
  const childMap = new Map<string, Message>();
  for (const child of [...legacyChildren, ...arrayChildren]) {
    childMap.set(child._id, child);
  }

  return Array.from(childMap.values()).sort(
    (a, b) => (a.siblingIndex ?? 0) - (b.siblingIndex ?? 0),
  );
}
```

**Key**: Legacy uses indexed query, array requires conversation-scoped scan (no array-contains index in Convex). Always dedupe and sort by `siblingIndex`.

## Sibling Navigation

Get siblings (messages with same parent):

```typescript
// From tree.ts:110-123
export async function getSiblings(
  ctx: QueryCtx | MutationCtx,
  messageId: Id<"messages">,
): Promise<Message[]> {
  const message = await ctx.db.get(messageId);
  if (!message) return [];

  const parentId = message.parentMessageIds?.[0] ?? message.parentMessageId;
  if (!parentId) return [message]; // Root message has no siblings

  const children = await getChildren(ctx, parentId);
  return children;
}
```

Siblings = children of parent. Root messages return `[self]`.

## Active Path Management

Conversation tracks current "head" via `activeLeafMessageId`:

```typescript
// From schema.ts:89
activeLeafMessageId: v.optional(v.id("messages")), // Current "head" position in tree
```

Get active path (root → activeLeaf):

```typescript
// From tree.ts:158-175
export async function getActivePath(
  ctx: QueryCtx | MutationCtx,
  conversationId: Id<"conversations">,
): Promise<Message[]> {
  const conversation = await ctx.db.get(conversationId);
  if (!conversation?.activeLeafMessageId) {
    // Fallback: get all messages and return in order
    const messages = await ctx.db
      .query("messages")
      .withIndex("by_conversation_created", (q) =>
        q.eq("conversationId", conversationId),
      )
      .collect();
    return messages.sort((a, b) => a.createdAt - b.createdAt);
  }

  return getPathToRoot(ctx, conversation.activeLeafMessageId);
}
```

Walk from leaf to root:

```typescript
// From tree.ts:128-153
export async function getPathToRoot(
  ctx: QueryCtx | MutationCtx,
  messageId: Id<"messages">,
): Promise<Message[]> {
  const path: Message[] = [];
  let currentId: Id<"messages"> | undefined = messageId;
  const visited = new Set<string>();

  while (currentId) {
    if (visited.has(currentId)) {
      // Cycle detection (shouldn't happen, but safety)
      break;
    }
    visited.add(currentId);

    const message: Message | null = await ctx.db.get(currentId);
    if (!message) break;

    path.push(message);

    currentId = message.parentMessageIds?.[0] ?? message.parentMessageId;
  }

  return path.reverse(); // Root first
}
```

**Cycle detection**: Use `visited` Set to prevent infinite loops if DAG has accidental cycles.

## Marking Active Branch

Update `isActiveBranch` field for entire path:

```typescript
// From tree.ts:260-289
export async function markPathAsActive(
  ctx: MutationCtx,
  targetMessageId: Id<"messages">,
): Promise<void> {
  const message = await ctx.db.get(targetMessageId);
  if (!message) return;

  // Get the active path to this message
  const activePath = await getPathToRoot(ctx, targetMessageId);
  const activeIds = new Set(activePath.map((m) => m._id));

  // Get all messages in this conversation
  const allMessages = await ctx.db
    .query("messages")
    .withIndex("by_conversation", (q) =>
      q.eq("conversationId", message.conversationId),
    )
    .collect();

  // Update isActiveBranch for all messages
  for (const msg of allMessages) {
    const shouldBeActive = activeIds.has(msg._id);
    if (msg.isActiveBranch !== shouldBeActive) {
      await ctx.db.patch(msg._id, {
        isActiveBranch: shouldBeActive,
        updatedAt: Date.now(),
      });
    }
  }
}
```

**Pattern**: Build Set of active IDs, iterate ALL messages, patch if status differs. Expensive but thorough.

## Deactivate Subtree (BFS Traversal)

Mark all descendants inactive (for deletion prep):

```typescript
// From tree.ts:296-337
export async function deactivateSubtree(
  ctx: MutationCtx,
  rootMessageId: Id<"messages">,
): Promise<number> {
  const root = await ctx.db.get(rootMessageId);
  if (!root) return 0;

  // Collect all descendants using BFS (handles DAG with multi-parent nodes)
  const descendants: Id<"messages">[] = [];
  const queue: Id<"messages">[] = [rootMessageId];
  const visited = new Set<string>([rootMessageId]); // Mark root as visited immediately

  while (queue.length > 0) {
    const currentId = queue.shift()!;
    descendants.push(currentId);

    const children = await getChildren(ctx, currentId);
    for (const child of children) {
      if (!visited.has(child._id)) {
        visited.add(child._id); // Mark visited when enqueueing to prevent duplicates
        queue.push(child._id);
      }
    }
  }

  // Mark all as inactive
  let deactivatedCount = 0;
  const now = Date.now();

  for (const id of descendants) {
    const msg = await ctx.db.get(id);
    if (msg && msg.isActiveBranch !== false) {
      await ctx.db.patch(id, {
        isActiveBranch: false,
        updatedAt: now,
      });
      deactivatedCount++;
    }
  }

  return deactivatedCount;
}
```

**BFS pattern**: Use queue + visited Set. Mark visited when enqueueing (not when processing) to prevent duplicates. Includes root in descendants.

## Get Descendants (Excluding Root)

Return all children, grandchildren, etc. WITHOUT root:

```typescript
// From tree.ts:343-365
export async function getDescendants(
  ctx: QueryCtx | MutationCtx,
  rootMessageId: Id<"messages">,
): Promise<Id<"messages">[]> {
  const descendants: Id<"messages">[] = [];
  const queue: Id<"messages">[] = [rootMessageId];
  const visited = new Set<string>([rootMessageId]);

  while (queue.length > 0) {
    const currentId = queue.shift()!;

    const children = await getChildren(ctx, currentId);
    for (const child of children) {
      if (!visited.has(child._id)) {
        visited.add(child._id);
        descendants.push(child._id); // Add AFTER deduping
        queue.push(child._id);
      }
    }
  }

  return descendants;
}
```

**Difference from deactivateSubtree**: `descendants.push()` inside child loop, NOT at queue processing. Root excluded.

## Message Context (One Query)

Get message with parent + children + sibling count:

```typescript
// From tree.ts:74-105
export interface MessageWithContext {
  message: Message;
  parent: Message | null;
  children: Message[];
  hasBranches: boolean;
  siblingCount: number;
  siblingIndex: number;
}

export async function getWithContext(
  ctx: QueryCtx | MutationCtx,
  messageId: Id<"messages">,
): Promise<MessageWithContext | null> {
  const message = await ctx.db.get(messageId);
  if (!message) return null;

  const parentId = message.parentMessageIds?.[0] ?? message.parentMessageId;
  const [parent, children, siblings] = await Promise.all([
    parentId ? ctx.db.get(parentId) : Promise.resolve(null),
    getChildren(ctx, messageId),
    parentId ? getChildren(ctx, parentId) : Promise.resolve([message]),
  ]);

  return {
    message,
    parent,
    children,
    hasBranches: children.length > 1,
    siblingCount: siblings.length,
    siblingIndex: message.siblingIndex ?? 0,
  };
}
```

**Optimization**: Parallel fetches with `Promise.all`. Siblings = parent's children.

## Next Sibling Index

Get next index for new child:

```typescript
// From tree.ts:246-255
export async function getNextSiblingIndex(
  ctx: QueryCtx | MutationCtx,
  parentMessageId: Id<"messages">,
): Promise<number> {
  const children = await getChildren(ctx, parentMessageId);
  if (children.length === 0) return 0;

  const maxIndex = Math.max(...children.map((c) => c.siblingIndex ?? 0));
  return maxIndex + 1;
}
```

Pattern: Find max existing index, increment. Starts at 0.

## Key Files

- `convex/lib/tree.ts` - All traversal/query utilities
- `convex/conversations/branching.ts` - Access checks, child branch queries
- `convex/schema.ts` - Message and conversation schema (lines 169-338, 55-140)
- `convex/messages.ts` - Message mutations (use tree utilities)
- `convex/chat.ts` - Send message logic (updates activeLeafMessageId)

## Avoid

- **Don't query `parentMessageIds` directly** - Use `getChildren()` (handles both formats + dedup)
- **Don't forget cycle detection** - Always use `visited` Set when traversing
- **Don't mix legacy/new** - Write to `parentMessageIds`, read from both via fallback pattern
- **Don't scan all messages** - Scope to conversation when querying array fields
- **Don't assume linear** - Messages can have multiple children (branches) and multiple parents (merges)
