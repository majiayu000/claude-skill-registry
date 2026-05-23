---
name: "Convex Agents Streaming"
description: "Streams agent responses in real-time to clients without blocking. Use this for responsive UIs, long-running generations, and asynchronous streaming to multiple clients."
---

## Purpose

Streaming allows responses to appear character-by-character in real-time, improving UX and perceived performance. Supports async streaming and multiple clients.

## When to Use This Skill

- Building real-time chat interfaces with live updates
- Generating long responses that benefit from progressive display
- Streaming to multiple clients from single generation
- Using asynchronous streaming in background actions
- Implementing smooth text animation

## Basic Async Streaming

Stream and save deltas to database:

```typescript
export const streamResponse = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { thread } = await myAgent.continueThread(ctx, { threadId });

    await thread.streamText(
      { prompt },
      { saveStreamDeltas: true }
    );

    return { success: true };
  },
});
```

## Configure Stream Chunking

```typescript
await thread.streamText(
  { prompt },
  {
    saveStreamDeltas: {
      chunking: "line", // "word" | "line" | regex | function
      throttleMs: 500, // Save deltas every 500ms
    },
  }
);
```

## Retrieve Stream Deltas

```typescript
import { vStreamArgs, syncStreams } from "@convex-dev/agent";

export const listMessagesWithStreams = query({
  args: {
    threadId: v.string(),
    paginationOpts: paginationOptsValidator,
    streamArgs: vStreamArgs,
  },
  handler: async (ctx, { threadId, paginationOpts, streamArgs }) => {
    const messages = await listUIMessages(ctx, components.agent, {
      threadId,
      paginationOpts,
    });

    const streams = await syncStreams(ctx, components.agent, {
      threadId,
      streamArgs,
    });

    return { ...messages, streams };
  },
});
```

## Display Streaming in React

```typescript
import { useUIMessages, useSmoothText } from "@convex-dev/agent/react";

function ChatStreaming({ threadId }: { threadId: string }) {
  const { results } = useUIMessages(
    api.streaming.listMessages,
    { threadId },
    { initialNumItems: 20, stream: true }
  );

  return (
    <div>
      {results?.map((message) => (
        <StreamingMessage key={message.key} message={message} />
      ))}
    </div>
  );
}

function StreamingMessage({ message }: { message: UIMessage }) {
  const [visibleText] = useSmoothText(message.text, {
    startStreaming: message.status === "streaming",
  });

  return <div>{visibleText}</div>;
}
```

## Key Principles

- **Asynchronous streaming**: Best for background generations
- **Delta throttling**: Balances responsiveness with write volume
- **Stream status**: Check `message.status === "streaming"`
- **Smooth animation**: Use `useSmoothText` for text updates
- **Persistence**: Deltas survive page reloads

## Next Steps

- See **messages** for message management
- See **fundamentals** for agent setup
- See **context** for streaming-aware context
