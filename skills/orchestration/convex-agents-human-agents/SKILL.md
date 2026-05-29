---
name: "Convex Agents Human Agents"
description: "Integrates human agents into automated workflows for human-in-the-loop interactions. Use this when humans need to respond alongside AI agents, handle escalations, or provide context that AI cannot determine."
---

## Purpose

Human agents allow humans to participate in agent threads, creating hybrid workflows where humans and AI collaborate. Perfect for support, approval workflows, and escalations.

## When to Use This Skill

- Customer support with escalation to humans
- Approval workflows where humans verify AI decisions
- Human-AI collaboration (e.g., brainstorming)
- Workflows needing human context or judgment
- Handling exceptions AI can't resolve
- Collecting human feedback for continuous improvement

## How to Use It

### 1. Save a User Message

Store a message from the end user:

```typescript
// convex/humanAgents.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";
import { saveMessage } from "@convex-dev/agent";
import { components } from "./_generated/api";

export const saveUserMessage = mutation({
  args: { threadId: v.string(), message: v.string() },
  handler: async (ctx, { threadId, message }) => {
    const { messageId } = await saveMessage(ctx, components.agent, {
      threadId,
      prompt: message, // User message without agent generation
    });

    return { messageId };
  },
});
```

### 2. Save Human Agent Response

Store a message from a human (e.g., support agent):

```typescript
// convex/humanAgents.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";
import { saveMessage } from "./_generated/api";
import { components } from "./_generated/api";

export const saveHumanResponse = mutation({
  args: {
    threadId: v.string(),
    humanName: v.string(),
    response: v.string(),
  },
  handler: async (ctx, { threadId, humanName, response }) => {
    const { messageId } = await saveMessage(ctx, components.agent, {
      threadId,
      agentName: humanName, // Human's name as the "agent"
      message: {
        role: "assistant",
        content: response,
      },
      metadata: {
        provider: "human",
        providerMetadata: {
          human: { name: humanName },
        },
      },
    });

    return { messageId };
  },
});
```

### 3. Decide Who Responds Next

Route to AI or human:

```typescript
// convex/humanAgents.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { myAgent } from "./agents/myAgent";

export const routeResponse = action({
  args: { threadId: v.string(), userId: v.string(), question: v.string() },
  handler: async (ctx, { threadId, userId, question }) => {
    // Strategy 1: Check database for assigned responder
    const assignment = await ctx.db
      .query("threadAssignments")
      .filter((a) => a.threadId === threadId)
      .first();

    if (assignment?.assignedTo === "human") {
      return { responder: "human", requiresApproval: true };
    }

    // Strategy 2: Use fast LLM to classify
    const classification = await myAgent.generateText(
      ctx,
      { threadId },
      {
        prompt: `Should a human or AI respond? Question: ${question}`,
      }
    );

    if (classification.text.includes("human")) {
      return { responder: "human", reason: classification.text };
    }

    // Strategy 3: Use AI to respond
    return { responder: "ai" };
  },
});
```

### 4. Tool-Based Human Routing

Let AI call a tool to request human intervention:

```typescript
// convex/humanAgents.ts
import { tool } from "ai";
import { z } from "zod";
import { action } from "./_generated/server";
import { v } from "convex/values";
import { myAgent } from "./agents/myAgent";

const askHumanTool = tool({
  description: "Ask a human agent for help",
  parameters: z.object({
    question: z.string().describe("Question for the human"),
  }),
});

export const generateWithHumanTool = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const result = await myAgent.generateText(
      ctx,
      { threadId },
      {
        prompt,
        tools: { askHuman: askHumanTool },
        maxSteps: 5,
      }
    );

    // Check if AI asked for human help
    const humanRequests = result.toolCalls.filter(
      (tc) => tc.toolName === "askHuman"
    );

    if (humanRequests.length > 0) {
      // Notify human team
      await ctx.runMutation(internal.humanAgents.notifyHumanTeam, {
        threadId,
        requests: humanRequests,
      });
    }

    return result;
  },
});
```

### 5. Human Response to Tool Call

AI requested human help via tool; human now responds:

```typescript
// convex/humanAgents.ts
import { internalAction } from "./_generated/server";
import { v } from "convex/values";
import { saveMessage } from "@convex-dev/agent";
import { components } from "./_generated/api";
import { myAgent } from "./agents/myAgent";

export const humanRespondToToolCall = internalAction({
  args: {
    threadId: v.string(),
    messageId: v.string(),
    toolCallId: v.string(),
    humanName: v.string(),
    response: v.string(),
  },
  handler: async (
    ctx,
    { threadId, messageId, toolCallId, humanName, response }
  ) => {
    // Save human response as tool result
    await saveMessage(ctx, components.agent, {
      threadId,
      message: {
        role: "tool",
        content: [
          {
            type: "tool-result",
            toolName: "askHuman",
            toolCallId,
            result: response,
          },
        ],
      },
      metadata: {
        provider: "human",
        providerMetadata: { human: { name: humanName } },
      },
    });

    // Continue AI generation with human's response
    const { thread } = await myAgent.continueThread(ctx, { threadId });
    await thread.generateText({ promptMessageId: messageId });
  },
});
```

### 6. Track Assignment

Store who should respond to a thread:

```typescript
// convex/humanAgents.ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const assignThread = mutation({
  args: {
    threadId: v.string(),
    assignedTo: v.union(v.literal("ai"), v.literal("human")),
    assignedUser: v.optional(v.string()),
  },
  handler: async (ctx, { threadId, assignedTo, assignedUser }) => {
    await ctx.db.insert("threadAssignments", {
      threadId,
      assignedTo,
      assignedUser,
      assignedAt: Date.now(),
    });
  },
});
```

### 7. Implement Approval Workflow

AI generates response; human approves before sending:

```typescript
// convex/humanAgents.ts
import { action, mutation } from "./_generated/server";
import { v } from "convex/values";
import { saveMessage } from "@convex-dev/agent";
import { components } from "./_generated/api";
import { myAgent } from "./agents/myAgent";

// Step 1: Generate AI response (pending approval)
export const generateForApproval = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const { thread } = await myAgent.continueThread(ctx, { threadId });
    const result = await thread.generateText({ prompt });

    // Save as draft (not yet visible to user)
    const { messageId } = await saveMessage(ctx, components.agent, {
      threadId,
      message: { role: "assistant", content: result.text },
      metadata: { status: "pending_approval" },
    });

    // Notify human reviewer
    await ctx.runMutation(internal.humanAgents.notifyForApproval, {
      threadId,
      messageId,
      draftText: result.text,
    });

    return { messageId, draftText: result.text };
  },
});

// Step 2: Human approves or rejects
export const approveOrRejectResponse = mutation({
  args: {
    messageId: v.string(),
    approved: v.boolean(),
    review: v.optional(v.string()),
  },
  handler: async (ctx, { messageId, approved, review }) => {
    // Update message metadata
    const message = await ctx.db.get(messageId);
    if (message) {
      await ctx.db.patch(messageId, {
        metadata: {
          ...message.metadata,
          status: approved ? "approved" : "rejected",
          review,
        },
      });
    }
  },
});
```

### 8. Escalation System

Escalate to human when AI confidence is low:

```typescript
// convex/humanAgents.ts
import { action } from "./_generated/server";
import { v } from "convex/values";
import { z } from "zod";
import { myAgent } from "./agents/myAgent";

export const generateWithConfidence = action({
  args: { threadId: v.string(), prompt: v.string() },
  handler: async (ctx, { threadId, prompt }) => {
    const result = await myAgent.generateObject(
      ctx,
      { threadId },
      {
        prompt,
        schema: z.object({
          response: z.string(),
          confidence: z.number().min(0).max(1),
          requiresHuman: z.boolean(),
        }),
      }
    );

    const { response, confidence, requiresHuman } = result.object;

    if (requiresHuman || confidence < 0.7) {
      // Escalate to human
      await ctx.runMutation(internal.humanAgents.escalateToHuman, {
        threadId,
        reason: `AI confidence: ${confidence}`,
        aiSuggestion: response,
      });
      return { escalated: true };
    }

    return { response, confidence };
  },
});
```

## Key Principles

- **Hybrid workflows**: Combine AI efficiency with human judgment
- **Tool-based escalation**: AI can request human help via tools
- **Approval gates**: Route sensitive responses through humans
- **Metadata tracking**: Mark messages as human-provided
- **Assignment tracking**: Know who should respond next
- **Graceful fallback**: Fall back to human when AI is uncertain

## Example: Support Chat with Escalation

```typescript
// convex/support.ts
import { mutation, action, query } from "./_generated/server";
import { v } from "convex/values";
import { saveMessage } from "@convex-dev/agent";
import { components } from "./_generated/api";
import { supportAgent } from "./agents";
import { z } from "zod";
import { tool } from "ai";

const escalateTool = tool({
  description: "Escalate to human support",
  parameters: z.object({
    reason: z.string(),
  }),
});

// User sends message
export const sendSupportMessage = mutation({
  args: { threadId: v.string(), message: v.string() },
  handler: async (ctx, { threadId, message }) => {
    const { messageId } = await saveMessage(ctx, components.agent, {
      threadId,
      prompt: message,
    });
    return { messageId };
  },
});

// AI or human responds
export const respondToTicket = action({
  args: { threadId: v.string(), promptMessageId: v.string() },
  handler: async (ctx, { threadId, promptMessageId }) => {
    const result = await supportAgent.generateText(
      ctx,
      { threadId },
      {
        promptMessageId,
        tools: { escalate: escalateTool },
        maxSteps: 3,
      }
    );

    // Check if escalated
    if (result.toolCalls.some((tc) => tc.toolName === "escalate")) {
      await ctx.runMutation(internal.support.escalateTicket, { threadId });
    }
  },
});

// Human responds
export const humanReply = mutation({
  args: { threadId: v.string(), humanName: v.string(), reply: v.string() },
  handler: async (ctx, { threadId, humanName, reply }) => {
    await saveMessage(ctx, components.agent, {
      threadId,
      agentName: humanName,
      message: { role: "assistant", content: reply },
      metadata: { provider: "human" },
    });
  },
});
```

## Common Patterns

- **First-touch by AI**: Fast response for common issues
- **Escalation on uncertainty**: Human for complex cases
- **Approval gate**: Human reviews before sending
- **Hybrid reasoning**: AI analyzes, human decides
- **Feedback loop**: Humans improve AI over time

## Next Steps

- **Add streaming**: See **Convex Agents Streaming** for real-time human responses
- **Implement rate limiting**: See **Convex Agents Rate Limiting** for limiting escalations
- **Track usage**: See **Convex Agents Usage Tracking** for billing human labor

## Troubleshooting

- **Too many escalations**: Improve AI instructions or add more tools
- **Humans overwhelmed**: Implement better routing or queue management
- **Lost context**: Include thread history when notifying humans
- **Slow response times**: Monitor human response time SLAs
