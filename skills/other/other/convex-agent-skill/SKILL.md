---
name: convex-agent
description: 'Build AI agents with persistent threads, tool calling, and streaming on Convex. Use when implementing chat interfaces, AI assistants, multi-agent workflows, RAG systems, or any LLM-powered features with message history.'
---

# Convex Agent Component

Build AI agents with persistent message history, tool calling, real-time streaming, and durable workflows.

## Installation

```bash
npm install @convex-dev/agent
```

```typescript
// convex/convex.config.ts
import { defineApp } from 'convex/server';
import agent from '@convex-dev/agent/convex.config';

const app = defineApp();
app.use(agent);
export default app;
```

Run `npx convex dev` to generate component code before defining agents.

## Core Concepts

### Agent Definition

```typescript
// convex/agents.ts
import { Agent } from '@convex-dev/agent';
import { openai } from '@ai-sdk/openai';
import { components } from './_generated/api';

const supportAgent = new Agent(components.agent, {
  name: 'Support Agent',
  languageModel: openai.chat('gpt-4o-mini'),
  textEmbeddingModel: openai.embedding('text-embedding-3-small'), // For vector search
  instructions: 'You are a helpful support assistant.',
  tools: { lookupAccount, createTicket },
  stopWhen: stepCountIs(10) // Or use maxSteps: 10
});
```

### Basic Usage (Two Approaches)

**Approach 1: Direct generation (simpler)**

```typescript
import { createThread } from '@convex-dev/agent';

export const chat = action({
  args: { prompt: v.string() },
  handler: async (ctx, { prompt }) => {
    const threadId = await createThread(ctx, components.agent);
    const result = await agent.generateText(ctx, { threadId }, { prompt });
    return result.text;
  }
});
```

**Approach 2: Thread object (more features)**

```typescript
export const chat = action({
  args: { prompt: v.string() },
  handler: async (ctx, { prompt }) => {
    const { threadId, thread } = await agent.createThread(ctx);
    const result = await thread.generateText({ prompt });
    return { threadId, text: result.text };
  }
});
```

### Continue Existing Thread

```typescript
export const continueChat = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    // Message history included automatically
    const result = await agent.generateText(ctx, { threadId }, { prompt });
    return result.text;
  }
});
```

### Asynchronous Pattern (Recommended)

Best practice: save message in mutation, generate response asynchronously.

```typescript
import { saveMessage } from '@convex-dev/agent';

// Step 1: Mutation saves message and schedules generation
export const sendMessage = mutation({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { messageId } = await saveMessage(ctx, components.agent, {
      threadId,
      prompt
    });
    await ctx.scheduler.runAfter(0, internal.chat.generateResponse, {
      threadId,
      promptMessageId: messageId
    });
    return messageId;
  }
});

// Step 2: Action generates response
export const generateResponse = internalAction({
  args: { threadId: v.string(), promptMessageId: v.string() },
  handler: async (ctx, { threadId, promptMessageId }) => {
    await agent.generateText(ctx, { threadId }, { promptMessageId });
  }
});

// Shorthand for Step 2:
export const generateResponse = agent.asTextAction();
```

## Generation Methods

```typescript
// Text generation
const result = await agent.generateText(ctx, { threadId }, { prompt });

// Structured output
const result = await agent.generateObject(
  ctx,
  { threadId },
  {
    prompt: 'Extract user info',
    schema: z.object({ name: z.string(), email: z.string() })
  }
);

// Stream text (see STREAMING.md)
const result = await agent.streamText(ctx, { threadId }, { prompt });

// Multiple messages
const result = await agent.generateText(
  ctx,
  { threadId },
  {
    messages: [
      { role: 'user', content: 'Context message' },
      { role: 'user', content: 'Actual question' }
    ]
  }
);
```

## Querying Messages

```typescript
import { listUIMessages, paginationOptsValidator } from '@convex-dev/agent';

export const listMessages = query({
  args: { threadId: v.string(), paginationOpts: paginationOptsValidator },
  handler: async (ctx, args) => {
    return await listUIMessages(ctx, components.agent, args);
  }
});
```

**React Hook:**

```typescript
import { useUIMessages } from '@convex-dev/agent/react';

const { results, status, loadMore } = useUIMessages(
  api.chat.listMessages,
  { threadId },
  { initialNumItems: 20 }
);
```

## Agent Configuration Options

```typescript
const agent = new Agent(components.agent, {
  name: 'Agent Name',
  languageModel: openai.chat('gpt-4o-mini'),
  textEmbeddingModel: openai.embedding('text-embedding-3-small'),
  instructions: 'System prompt...',
  tools: {
    /* tools */
  },
  stopWhen: stepCountIs(10), // Or maxSteps: 10

  // Context options (see CONTEXT.md)
  contextOptions: {
    recentMessages: 100,
    excludeToolMessages: true,
    searchOptions: { limit: 10, textSearch: false, vectorSearch: false }
  },

  // Storage options
  storageOptions: { saveMessages: 'promptAndOutput' }, // 'all' | 'none'

  // Handlers
  usageHandler: async (ctx, { usage, model, provider, agentName }) => {},
  contextHandler: async (ctx, { allMessages }) => allMessages,
  rawRequestResponseHandler: async (ctx, { request, response }) => {},

  // Call settings
  callSettings: { maxRetries: 3, temperature: 1.0 }
});
```

## Key References

- [Streaming](references/STREAMING.md) - Delta streaming, HTTP streaming, text smoothing
- [Tools](references/TOOLS.md) - Defining and using tools with Convex context
- [Context](references/CONTEXT.md) - Customizing LLM context and RAG
- [Threads](references/THREADS.md) - Thread management and deletion
- [Messages](references/MESSAGES.md) - Message storage, ordering, UIMessage type
- [Workflows](references/WORKFLOWS.md) - Durable multi-step workflows
- [Human Agents](references/HUMAN-AGENTS.md) - Mixing human and AI responses
- [Files](references/FILES.md) - Images and files in messages
- [RAG](references/RAG.md) - Retrieval-augmented generation patterns
- [Rate Limiting](references/RATE-LIMITING.md) - Controlling request rates
- [Usage Tracking](references/USAGE-TRACKING.md) - Token usage and billing
- [Debugging](references/DEBUGGING.md) - Troubleshooting and playground

## Best Practices

1. **Define agents at module level** - Reuse across functions
2. **Use `userId` on threads** - Enables cross-thread search and per-user data
3. **Set appropriate `stopWhen`/`maxSteps`** - Prevents runaway tool loops
4. **Use `promptMessageId` for async** - Enables safe retries without duplicates
5. **Save messages in mutations** - Use optimistic updates, schedule actions
6. **Use `textEmbeddingModel` for RAG** - Required for vector search
7. **Handle streaming via deltas** - Better UX than HTTP streaming alone
