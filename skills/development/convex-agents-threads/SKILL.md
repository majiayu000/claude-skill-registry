---
name: "Convex Agents Threads"
description: "Manages conversation threads to group messages into linear histories. Use this when organizing multi-turn conversations, managing per-user history, and handling thread metadata."
---

## Purpose

Threads group related messages into organized, linear conversation histories. Every message in the Agent component belongs to a thread.

## When to Use This Skill

- Creating new conversations for users
- Managing conversation history and metadata
- Continuing existing conversations
- Querying message history within a thread
- Organizing conversations by user or context
- Cleaning up old or completed conversations

## Create a Thread

```typescript
import { createThread } from "@convex-dev/agent";

export const startNewThread = mutation({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    const threadId = await createThread(ctx, components.agent, {
      userId,
      title: "New Conversation",
      summary: "Conversation summary",
    });
    return { threadId };
  },
});
```

## Continue a Thread (Actions Only)

In actions, get a thread object:

```typescript
export const continueConversation = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { thread } = await myAgent.continueThread(ctx, { threadId });

    const metadata = thread.getMetadata();
    const response = await thread.generateText({ prompt });

    return response.text;
  },
});
```

## List Threads for a User

```typescript
export const getUserThreads = query({
  args: { userId: v.string(), paginationOpts: paginationOptsValidator },
  handler: async (ctx, { userId, paginationOpts }) => {
    return await ctx.runQuery(
      components.agent.threads.listThreadsByUserId,
      { userId, paginationOpts }
    );
  },
});
```

## Delete Threads

```typescript
// Async deletion (non-blocking)
await myAgent.deleteThreadAsync(ctx, { threadId });

// Sync deletion (atomic)
await myAgent.deleteThreadSync(ctx, { threadId });

// Delete all for user
await ctx.runMutation(components.agent.users.deleteAllForUserId, { userId });
```

## Key Principles

- **User association**: Threads associated with userId
- **Metadata**: Use title and summary for organization
- **Message ordering**: Messages within thread maintain order
- **Async vs sync**: Use async for non-blocking, sync for atomic ops

## Next Steps

- See **messages** for saving and retrieving messages
- See **fundamentals** for basic agent setup
