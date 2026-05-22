---
name: "Convex Agents RAG"
description: "Implements Retrieval-Augmented Generation (RAG) patterns to enhance agents with custom knowledge bases. Use this when agents need to search through documents, retrieve context from a knowledge base, or ground responses in specific data."
---

## Purpose

Enables agents to search through custom content and knowledge bases to provide accurate, context-grounded responses. RAG combines LLM capabilities with semantic search.

## When to Use This Skill

- Agents need to reference a knowledge base or document collection
- Grounding answers in specific data (policies, product docs, etc.)
- Semantic search across custom content
- Building a search + generation system (FAQ, documentation, support)
- Reducing hallucinations by constraining responses to known information
- Managing user-specific or team-specific knowledge namespaces

## Setup

Install and configure RAG in your `convex.config.ts`:

```typescript
import { defineApp } from "convex/server";
import agent from "@convex-dev/agent/convex.config";
import rag from "@convex-dev/rag/convex.config";

const app = defineApp();
app.use(agent);
app.use(rag);

export default app;
```

## Add Content

Ingest documents into a namespace:

```typescript
import { rag } from "@convex-dev/rag";

export const addContent = action({
  args: { userId: v.string(), key: v.string(), text: v.string() },
  handler: async (ctx, { userId, key, text }) => {
    const namespace = `user:${userId}`;
    await rag.addContent(ctx, components.rag, {
      namespace,
      key,
      text,
      filters: { filterNames: [filename] },
    });
  },
});
```

## Search and Generate

Use RAG with agents:

```typescript
export const answerWithContext = action({
  args: { threadId: v.string(), userId: v.string(), question: v.string() },
  handler: async (ctx, { threadId, userId, question }) => {
    const { thread } = await myAgent.continueThread(ctx, { threadId });

    const context = await rag.search(ctx, components.rag, {
      namespace: `user:${userId}`,
      query: question,
      limit: 10,
    });

    const augmentedPrompt = `# Context:\n\n${context.text}\n\n# Question:\n\n${question}`;
    const result = await thread.generateText({ prompt: augmentedPrompt });

    return result.text;
  },
});
```

## Key Principles

- **Namespaces isolate data**: Use `user:userId` or `team:teamId` for multi-tenant safety
- **Hybrid search**: Combine text and vector search for better results
- **Filtering**: Use `filterNames` to target specific documents

## Next Steps

- See **fundamentals** for basic agent setup
- See **context** for advanced context customization
