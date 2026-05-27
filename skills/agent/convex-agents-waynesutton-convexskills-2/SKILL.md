---
name: convex-agents
displayName: Convex Agents
description: Building AI agents with the Convex Agent component including thread management, tool integration, streaming responses, RAG patterns, and workflow orchestration
version: 1.0.0
author: Convex
tags: [convex, agents, ai, llm, tools, rag, workflows]
---

# Convex Agents

Build persistent, stateful AI agents with Convex including thread management, tool integration, streaming responses, RAG patterns, and workflow orchestration.

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: https://docs.convex.dev/ai
- Convex Agent Component: https://www.npmjs.com/package/@convex-dev/agent
- For broader context: https://docs.convex.dev/llms.txt

## Instructions

### Why Convex for AI Agents

- **Persistent State** - Conversation history survives restarts
- **Real-time Updates** - Stream responses to clients automatically
- **Tool Execution** - Run Convex functions as agent tools
- **Durable Workflows** - Long-running agent tasks with reliability
- **Built-in RAG** - Vector search for knowledge retrieval

### Setting Up Convex Agent

```bash
npm install @convex-dev/agent ai openai
```

```typescript
// convex/agent.ts
import { Agent } from "@convex-dev/agent";
import { components } from "./_generated/api";
import { OpenAI } from "openai";

const openai = new OpenAI();

export const agent = new Agent(components.agent, {
  chat: openai.chat,
  textEmbedding: openai.embeddings,
});
```

### Thread Management

```typescript
// convex/threads.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { agent } from "./agent";

// Create a new conversation thread
export const createThread = mutation({
  args: {
    userId: v.id("users"),
    title: v.optional(v.string()),
  },
  returns: v.id("threads"),
  handler: async (ctx, args) => {
    const threadId = await agent.createThread(ctx, {
      userId: args.userId,
      metadata: {
        title: args.title ?? "New Conversation",
        createdAt: Date.now(),
      },
    });
    return threadId;
  },
});

// List user's threads
export const listThreads = query({
  args: { userId: v.id("users") },
  returns: v.array(v.object({
    _id: v.id("threads"),
    title: v.string(),
    lastMessageAt: v.optional(v.number()),
  })),
  handler: async (ctx, args) => {
    return await agent.listThreads(ctx, {
      userId: args.userId,
    });
  },
});

// Get thread messages
export const getMessages = query({
  args: { threadId: v.id("threads") },
  returns: v.array(v.object({
    role: v.string(),
    content: v.string(),
    createdAt: v.number(),
  })),
  handler: async (ctx, args) => {
    return await agent.getMessages(ctx, {
      threadId: args.threadId,
    });
  },
});
```

### Sending Messages and Streaming Responses

```typescript
// convex/chat.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { agent } from "./agent";
import { internal } from "./_generated/api";

export const sendMessage = action({
  args: {
    threadId: v.id("threads"),
    message: v.string(),
  },
  returns: v.null(),
  handler: async (ctx, args) => {
    // Add user message to thread
    await ctx.runMutation(internal.chat.addUserMessage, {
      threadId: args.threadId,
      content: args.message,
    });

    // Generate AI response with streaming
    const response = await agent.chat(ctx, {
      threadId: args.threadId,
      messages: [{ role: "user", content: args.message }],
      stream: true,
      onToken: async (token) => {
        // Stream tokens to client via mutation
        await ctx.runMutation(internal.chat.appendToken, {
          threadId: args.threadId,
          token,
        });
      },
    });

    // Save complete response
    await ctx.runMutation(internal.chat.saveResponse, {
      threadId: args.threadId,
      content: response.content,
    });

    return null;
  },
});
```

### Tool Integration

Define tools that agents can use:

```typescript
// convex/tools.ts
import { tool } from "@convex-dev/agent";
import { v } from "convex/values";
import { api } from "./_generated/api";

// Tool to search knowledge base
export const searchKnowledge = tool({
  name: "search_knowledge",
  description: "Search the knowledge base for relevant information",
  parameters: v.object({
    query: v.string(),
    limit: v.optional(v.number()),
  }),
  handler: async (ctx, args) => {
    const results = await ctx.runQuery(api.knowledge.search, {
      query: args.query,
      limit: args.limit ?? 5,
    });
    return results;
  },
});

// Tool to create a task
export const createTask = tool({
  name: "create_task",
  description: "Create a new task for the user",
  parameters: v.object({
    title: v.string(),
    description: v.optional(v.string()),
    dueDate: v.optional(v.string()),
  }),
  handler: async (ctx, args) => {
    const taskId = await ctx.runMutation(api.tasks.create, {
      title: args.title,
      description: args.description,
      dueDate: args.dueDate ? new Date(args.dueDate).getTime() : undefined,
    });
    return { success: true, taskId };
  },
});

// Tool to get weather
export const getWeather = tool({
  name: "get_weather",
  description: "Get current weather for a location",
  parameters: v.object({
    location: v.string(),
  }),
  handler: async (ctx, args) => {
    const response = await fetch(
      `https://api.weather.com/current?location=${encodeURIComponent(args.location)}`
    );
    return await response.json();
  },
});
```

### Agent with Tools

```typescript
// convex/assistant.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { agent } from "./agent";
import { searchKnowledge, createTask, getWeather } from "./tools";

export const chat = action({
  args: {
    threadId: v.id("threads"),
    message: v.string(),
  },
  returns: v.string(),
  handler: async (ctx, args) => {
    const response = await agent.chat(ctx, {
      threadId: args.threadId,
      messages: [{ role: "user", content: args.message }],
      tools: [searchKnowledge, createTask, getWeather],
      systemPrompt: `You are a helpful assistant. You have access to tools to:
        - Search the knowledge base for information
        - Create tasks for the user
        - Get weather information
        Use these tools when appropriate to help the user.`,
    });

    return response.content;
  },
});
```

### RAG (Retrieval Augmented Generation)

```typescript
// convex/knowledge.ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { agent } from "./agent";

// Add document to knowledge base
export const addDocument = mutation({
  args: {
    title: v.string(),
    content: v.string(),
    metadata: v.optional(v.object({
      source: v.optional(v.string()),
      category: v.optional(v.string()),
    })),
  },
  returns: v.id("documents"),
  handler: async (ctx, args) => {
    // Generate embedding
    const embedding = await agent.embed(ctx, args.content);

    return await ctx.db.insert("documents", {
      title: args.title,
      content: args.content,
      embedding,
      metadata: args.metadata ?? {},
      createdAt: Date.now(),
    });
  },
});

// Search knowledge base
export const search = query({
  args: {
    query: v.string(),
    limit: v.optional(v.number()),
  },
  returns: v.array(v.object({
    _id: v.id("documents"),
    title: v.string(),
    content: v.string(),
    score: v.number(),
  })),
  handler: async (ctx, args) => {
    const results = await agent.search(ctx, {
      query: args.query,
      table: "documents",
      limit: args.limit ?? 5,
    });

    return results.map((r) => ({
      _id: r._id,
      title: r.title,
      content: r.content,
      score: r._score,
    }));
  },
});
```

### Workflow Orchestration

```typescript
// convex/workflows.ts
import { action, internalMutation } from "./_generated/server";
import { v } from "convex/values";
import { agent } from "./agent";
import { internal } from "./_generated/api";

// Multi-step research workflow
export const researchTopic = action({
  args: {
    topic: v.string(),
    userId: v.id("users"),
  },
  returns: v.id("research"),
  handler: async (ctx, args) => {
    // Create research record
    const researchId = await ctx.runMutation(internal.workflows.createResearch, {
      topic: args.topic,
      userId: args.userId,
      status: "searching",
    });

    // Step 1: Search for relevant documents
    const searchResults = await agent.search(ctx, {
      query: args.topic,
      table: "documents",
      limit: 10,
    });

    await ctx.runMutation(internal.workflows.updateStatus, {
      researchId,
      status: "analyzing",
    });

    // Step 2: Analyze and synthesize
    const analysis = await agent.chat(ctx, {
      messages: [{
        role: "user",
        content: `Analyze these sources about "${args.topic}" and provide a comprehensive summary:\n\n${
          searchResults.map((r) => r.content).join("\n\n---\n\n")
        }`,
      }],
      systemPrompt: "You are a research assistant. Provide thorough, well-cited analysis.",
    });

    // Step 3: Generate key insights
    await ctx.runMutation(internal.workflows.updateStatus, {
      researchId,
      status: "summarizing",
    });

    const insights = await agent.chat(ctx, {
      messages: [{
        role: "user",
        content: `Based on this analysis, list 5 key insights:\n\n${analysis.content}`,
      }],
    });

    // Save final results
    await ctx.runMutation(internal.workflows.completeResearch, {
      researchId,
      analysis: analysis.content,
      insights: insights.content,
      sources: searchResults.map((r) => r._id),
    });

    return researchId;
  },
});
```

## Examples

### Complete Chat Application Schema

```typescript
// convex/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  threads: defineTable({
    userId: v.id("users"),
    title: v.string(),
    lastMessageAt: v.optional(v.number()),
    metadata: v.optional(v.any()),
  }).index("by_user", ["userId"]),

  messages: defineTable({
    threadId: v.id("threads"),
    role: v.union(v.literal("user"), v.literal("assistant"), v.literal("system")),
    content: v.string(),
    toolCalls: v.optional(v.array(v.object({
      name: v.string(),
      arguments: v.any(),
      result: v.optional(v.any()),
    }))),
    createdAt: v.number(),
  }).index("by_thread", ["threadId"]),

  documents: defineTable({
    title: v.string(),
    content: v.string(),
    embedding: v.array(v.float64()),
    metadata: v.object({
      source: v.optional(v.string()),
      category: v.optional(v.string()),
    }),
    createdAt: v.number(),
  }).vectorIndex("by_embedding", {
    vectorField: "embedding",
    dimensions: 1536,
  }),
});
```

### React Chat Component

```typescript
import { useQuery, useMutation, useAction } from "convex/react";
import { api } from "../convex/_generated/api";
import { useState, useRef, useEffect } from "react";

function ChatInterface({ threadId }: { threadId: Id<"threads"> }) {
  const messages = useQuery(api.threads.getMessages, { threadId });
  const sendMessage = useAction(api.chat.sendMessage);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || sending) return;

    const message = input.trim();
    setInput("");
    setSending(true);

    try {
      await sendMessage({ threadId, message });
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages?.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            <strong>{msg.role === "user" ? "You" : "Assistant"}:</strong>
            <p>{msg.content}</p>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="input-form">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={sending}
        />
        <button type="submit" disabled={sending || !input.trim()}>
          {sending ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
}
```

## Best Practices

- Never run `npx convex deploy` unless explicitly instructed
- Never run any git commands unless explicitly instructed
- Store conversation history in Convex for persistence
- Use streaming for better user experience with long responses
- Implement proper error handling for tool failures
- Use vector indexes for efficient RAG retrieval
- Rate limit agent interactions to control costs
- Log tool usage for debugging and analytics

## Common Pitfalls

1. **Not persisting threads** - Conversations lost on refresh
2. **Blocking on long responses** - Use streaming instead
3. **Tool errors crashing agents** - Add proper error handling
4. **Large context windows** - Summarize old messages
5. **Missing embeddings for RAG** - Generate embeddings on insert

## References

- Convex Documentation: https://docs.convex.dev/
- Convex LLMs.txt: https://docs.convex.dev/llms.txt
- Convex AI: https://docs.convex.dev/ai
- Agent Component: https://www.npmjs.com/package/@convex-dev/agent
