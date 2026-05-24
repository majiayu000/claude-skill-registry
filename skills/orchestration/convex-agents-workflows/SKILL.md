---
name: "Convex Agents Workflows"
description: "Orchestrates multi-step agent operations with durable execution, automatic retries, and recovery from failures. Use this for complex workflows that need to survive server restarts or coordinate multiple agents."
---

## Purpose

Provides durable, reliable execution of complex agent workflows. Workflows ensure multi-step operations complete reliably, survive server failures, and maintain idempotency.

## When to Use This Skill

- Building multi-step agent operations (research → analysis → report)
- Coordinating multiple agents working together
- Long-running operations that need to survive server restarts
- Ensuring idempotency (no duplicate work even if retried)
- Complex applications requiring durable execution guarantees

## Setup

Configure Workflow component in `convex.config.ts`:

```typescript
import { defineApp } from "convex/server";
import agent from "@convex-dev/agent/convex.config";
import workflow from "@convex-dev/workflow/convex.config";

const app = defineApp();
app.use(agent);
app.use(workflow);

export default app;
```

## Define a Workflow

```typescript
import { WorkflowManager } from "@convex-dev/workflow";

const workflow = new WorkflowManager(components.workflow);

export const simpleAgentFlow = workflow.define({
  id: "simple-flow",
  args: { userId: v.string(), prompt: v.string() },
  handler: async (step, { userId, prompt }) => {
    // Step 1: Create thread
    const { threadId } = await step.runMutation(
      internal.agents.createThreadMutation,
      { userId }
    );

    // Step 2: Generate response
    const response = await step.runAction(
      internal.agents.generateTextAction,
      { threadId, prompt }
    );

    return response;
  },
});
```

## Multi-Agent Workflows

Orchestrate multiple agents:

```typescript
export const researchFlow = workflow.define({
  id: "research",
  args: { topic: v.string(), userId: v.string() },
  handler: async (step, { topic, userId }) => {
    const { threadId: researchId } = await step.runMutation(
      internal.agents.createThreadMutation,
      { userId, title: `Research: ${topic}` }
    );

    const research = await step.runAction(
      internal.agents.generateTextAction,
      { threadId: researchId, prompt: `Research: ${topic}` }
    );

    const { threadId: analysisId } = await step.runMutation(
      internal.agents.createThreadMutation,
      { userId, title: `Analysis: ${topic}` }
    );

    const analysis = await step.runAction(
      internal.agents.generateTextAction,
      { threadId: analysisId, prompt: `Analyze: ${research}` }
    );

    return { research, analysis };
  },
});
```

## Key Principles

- **Durability**: Workflows survive server restarts
- **Idempotency**: Same workflow can be safely retried
- **Atomicity**: Each step either completes fully or retries
- **Composability**: Steps can call other workflows or actions

## Next Steps

- See **fundamentals** for agent setup
- See **tools** for agents that call functions
- See **context** for workflow-aware context
