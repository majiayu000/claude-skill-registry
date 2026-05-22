---
name: "Convex Agents Fundamentals"
description: "Sets up and configures Convex agents for chat-based AI interactions. Use this when initializing agent instances, creating conversation threads, and generating basic text or structured responses from LLMs. Essential foundation for any Convex agent implementation."
---

## Purpose

Guides you through the core patterns for setting up Convex agents, managing conversation threads, and generating LLM responses. This is the foundation upon which all other agent capabilities build.

## When to Use This Skill

- Setting up your first Convex agent in a project
- Creating or continuing conversation threads with users
- Generating text responses or structured JSON objects from an LLM
- Configuring agent defaults (system prompt, chat model, embedding model)
- Building basic chat interfaces that need message history

## How to Use It

### 1. Install and Configure

Add the agent component to your `convex.config.ts`:

```typescript
// convex/convex.config.ts
import { defineApp } from "convex/server";
import agent from "@convex-dev/agent/convex.config";

const app = defineApp();
app.use(agent);

export default app;
```

Run `npx convex dev` to generate the required code.

### 2. Define Your Agent

Create an agent instance with a chat model:

```typescript
// convex/agents/myAgent.ts
import { components } from "../_generated/api";
import { Agent } from "@convex-dev/agent";
import { openai } from "@ai-sdk/openai";

export const myAgent = new Agent(components.agent, {
  name: "My Assistant",
  languageModel: openai.chat("gpt-4o-mini"),
  instructions: "You are a helpful assistant.", // Optional: default system prompt
});
```

### 3. Create Threads

Create a thread for a user to manage their conversation history:

```typescript
// convex/threads.ts
import { action } from "../_generated/server";
import { v } from "convex/values";
import { myAgent } from "./agents/myAgent";

export const createNewThread = action({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    const { thread } = await myAgent.createThread(ctx, {
      userId,
      title: "New Conversation",
    });
    return { threadId: thread.getMetadata().threadId };
  },
});
```

### 4. Generate Responses

Generate text or structured responses in a thread:

```typescript
// convex/generation.ts
export const generateReply = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { thread } = await myAgent.continueThread(ctx, { threadId });
    const result = await thread.generateText({ prompt });
    return result.text;
  },
});
```

## Key Principles

- **Thread isolation**: Each user/conversation gets its own thread for independent history
- **Automatic message storage**: Generated responses are automatically saved to the thread
- **Context by default**: Each generation includes recent message history automatically
- **Async-friendly**: Use actions for LLM calls; mutations for transactional writes
- **Type safety**: Always provide explicit return types to avoid circular reference errors

## Common Patterns

- **Per-user organization**: Always include `userId` when creating threads
- **Message history**: Automatically included in LLM context
- **Thread reuse**: Same thread can be used by multiple agents

## Next Steps

- **Manage threads**: See **threads** skill for conversation management
- **Work with messages**: See **messages** skill for saving and retrieving
- **Add tools**: See **tools** skill to let agents take actions
