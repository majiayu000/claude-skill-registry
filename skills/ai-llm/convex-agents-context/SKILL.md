---
name: "Convex Agents Context"
description: "Customizes what information the LLM receives for each generation. Use this to control message history, implement RAG context injection, search across threads, and provide custom context."
---

## Purpose

By default, the Agent includes recent messages as context. This skill covers customizing that behavior for advanced patterns like cross-thread search, memory injection, summarization, and filtering.

## When to Use This Skill

- Limiting context window to prevent token overflow
- Searching across multiple threads for relevant context
- Injecting memories or user profiles into every prompt
- Summarizing long conversations before continuing
- Filtering out sensitive or irrelevant messages
- Adding few-shot examples to guide LLM

## Configure Default Context Options

```typescript
const myAgent = new Agent(components.agent, {
  name: "My Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  contextOptions: {
    recentMessages: 50,
    excludeToolMessages: true,
    searchOptions: {
      limit: 10,
      textSearch: true,
      vectorSearch: false,
    },
  },
});
```

## Override Context Per Call

```typescript
export const generateWithCustomContext = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const result = await myAgent.generateText(
      ctx,
      { threadId },
      { prompt },
      {
        contextOptions: {
          recentMessages: 20,
          searchOptions: {
            limit: 5,
            textSearch: true,
            vectorSearch: true,
          },
        },
      }
    );

    return result.text;
  },
});
```

## Search Across Threads

```typescript
export const generateWithCrossThreadContext = action({
  args: { threadId: v.string(), userId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, userId, prompt }) => {
    const result = await myAgent.generateText(
      ctx,
      { threadId, userId },
      { prompt },
      {
        contextOptions: {
          searchOtherThreads: true,
          searchOptions: {
            limit: 15,
            textSearch: true,
            vectorSearch: true,
          },
        },
      }
    );

    return result.text;
  },
});
```

## Custom Context Handler

Completely customize context:

```typescript
const myAgent = new Agent(components.agent, {
  name: "My Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  contextHandler: async (ctx, args) => {
    const userMemories = await getUserMemories(ctx, args.userId);
    const examples = getExamples();

    return [
      ...userMemories,
      ...examples,
      ...args.search,
      ...args.recent,
      ...args.inputMessages,
    ];
  },
});
```

## Fetch Context Manually

Get context without calling LLM:

```typescript
import { fetchContextWithPrompt } from "@convex-dev/agent";

export const getContextForPrompt = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { messages } = await fetchContextWithPrompt(ctx, components.agent, {
      threadId,
      prompt,
      contextOptions: {
        recentMessages: 20,
        searchOptions: { limit: 10, textSearch: true },
      },
    });

    return messages;
  },
});
```

## Key Principles

- **Default context is sufficient**: Most use cases work with defaults
- **Search improves relevance**: Enable for long conversations
- **userId required for cross-thread**: Provide when searching multiple threads
- **Context handlers are powerful**: Use for memories, examples, special formatting
- **Recent messages take precedence**: Used after search in context order

## Next Steps

- See **rag** for knowledge base context injection
- See **fundamentals** for agent setup
- See **rate-limiting** for token management
