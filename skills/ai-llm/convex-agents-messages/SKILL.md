---
name: "Convex Agents Messages"
description: "Sends, saves, retrieves, and manages messages within agent conversations. Use this when handling user messages, displaying conversation history, and working with UIMessages for rich rendering."
---

## Purpose

Messages represent individual exchanges in a conversation thread. This skill covers saving, retrieving, displaying, and managing messages.

## When to Use This Skill

- Displaying conversation history to users
- Saving user messages before generating responses
- Implementing optimistic message updates in UI
- Working with UIMessages for rich formatting
- Filtering tool messages from displayed history

## Retrieve Messages

```typescript
import { listUIMessages } from "@convex-dev/agent";

export const listThreadMessages = query({
  args: { threadId: v.string(), paginationOpts: paginationOptsValidator },
  handler: async (ctx, { threadId, paginationOpts }) => {
    return await listUIMessages(ctx, components.agent, {
      threadId,
      paginationOpts,
    });
  },
});
```

## Display in React

```typescript
import { useUIMessages } from "@convex-dev/agent/react";

function ChatComponent({ threadId }: { threadId: string }) {
  const { results } = useUIMessages(
    api.messages.listThreadMessages,
    { threadId },
    { initialNumItems: 20 }
  );

  return (
    <div>
      {results?.map((message) => (
        <div key={message.key}>{message.text}</div>
      ))}
    </div>
  );
}
```

## Save a Message Manually

```typescript
import { saveMessage } from "@convex-dev/agent";

export const saveUserMessage = mutation({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { messageId } = await saveMessage(ctx, components.agent, {
      threadId,
      prompt,
      skipEmbeddings: true,
    });
    return { messageId };
  },
});
```

## Optimistic Updates

Show messages immediately before they're saved:

```typescript
const sendMessage = useMutation(api.chat.generateResponse).withOptimisticUpdate(
  optimisticallySendMessage(api.messages.listThreadMessages)
);
```

## Delete Messages

```typescript
await myAgent.deleteMessage(ctx, { messageId });
await myAgent.deleteMessages(ctx, { messageIds });
await myAgent.deleteMessageRange(ctx, { threadId, startOrder, endOrder });
```

## UIMessage Type

Extended message with agent-specific fields:

```typescript
interface UIMessage {
  key: string;
  role: "user" | "assistant" | "system";
  text: string;
  status: "saved" | "streaming" | "finished" | "aborted";
  agentName?: string;
  _creationTime?: Date;
  parts?: MessagePart[];
}
```

## Key Principles

- **UIMessages vs MessageDocs**: Use UIMessages for UI, MessageDocs for backend
- **Message ordering**: Maintained automatically by order and stepOrder
- **Optimistic updates**: Better UX showing messages before save
- **Skip embeddings in mutations**: Use when saving in mutations

## Next Steps

- See **streaming** for real-time message updates
- See **files** for attaching media to messages
- See **threads** for managing message containers
