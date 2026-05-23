---
name: "Convex Agents Tools"
description: "Enables agents to call external functions, APIs, and database operations through tool definitions. Use this when agents need to fetch data, perform actions, or integrate with external services while maintaining clean separation."
---

## Purpose

Equips agents with the ability to take actions beyond text generation. Tools allow agents to call Convex functions, external APIs, and complex operations.

## When to Use This Skill

- Agents need to query or modify database data
- Integrating with external APIs
- Creating human-in-the-loop workflows
- Agents autonomously deciding what actions to take
- Chaining tool calls for multi-step operations

## Define Tools

Create Convex-aware tools:

```typescript
import { createTool } from "@convex-dev/agent";
import { z } from "zod";

export const getUserDataTool = createTool({
  description: "Fetch user information by email",
  args: z.object({
    email: z.string().email().describe("The user's email address"),
  }),
  handler: async (ctx, { email }): Promise<string> => {
    const user = await ctx.runQuery(api.users.getUserByEmail, { email });
    return user ? JSON.stringify(user) : "User not found";
  },
});
```

## Configure Agent with Tools

```typescript
const agentWithTools = new Agent(components.agent, {
  name: "Database Agent",
  languageModel: openai.chat("gpt-4o-mini"),
  tools: {
    getUserData: getUserDataTool,
  },
  maxSteps: 5, // Allow tool calls
});
```

## Enable Automatic Tool Calling

```typescript
export const autonomousAgent = action({
  args: { threadId: v.string(), request: v.string() },
  handler: async (ctx, { threadId, request }) => {
    const { thread } = await agentWithTools.continueThread(ctx, { threadId });

    const result = await thread.generateText(
      { prompt: request },
      { maxSteps: 10 } // Allow up to 10 tool calls
    );

    return result.text;
  },
});
```

## Key Principles

- **Use Zod for validation**: `.describe()` on fields helps LLMs understand parameters
- **Explicit return types**: Always annotate handler return types
- **Automatic history**: Tool calls and results saved automatically in thread
- **Context binding**: Create tools inside actions where you have access to userId, etc.

## Next Steps

- See **fundamentals** for agent setup
- See **workflows** for orchestrating multi-step operations
- See **context** for tool-aware context management
