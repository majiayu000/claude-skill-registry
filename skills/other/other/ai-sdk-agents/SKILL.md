---
name: ai-sdk-agents
description: |
  Expert guidance for building AI agents with ToolLoopAgent (AI SDK v6+). Use when creating agents, configuring stopWhen/prepareStep, callOptionsSchema/prepareCall, dynamic tool selection, tool loops, or agent workflows (sequential, routing, evaluator-optimizer, orchestrator-worker). Triggers: ToolLoopAgent, agent loop, stopWhen, stepCountIs, prepareStep, callOptionsSchema, prepareCall, hasToolCall, InferAgentUIMessage, agent workflows.
---

# AI SDK Agents

Build autonomous agents with ToolLoopAgent: reusable model + tools + loop control.

## Quick Start

Assume Zod v4.3.5 for schema typing.

```ts
import { ToolLoopAgent, tool } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

const weatherAgent = new ToolLoopAgent({
  model: anthropic('claude-sonnet-4-20250514'),
  tools: {
    weather: tool({
      description: 'Get the weather in a location (F)',
      inputSchema: z.object({ location: z.string() }),
      execute: async ({ location }) => ({ location, temperature: 72 }),
    }),
  },
});

const result = await weatherAgent.generate({
  prompt: 'What is the weather in San Francisco?',
});
```

## When to Use ToolLoopAgent vs Core Functions

- Use **ToolLoopAgent** for dynamic, multi-step tasks where the model decides which tools to call.
- Use **generateText/streamText** for deterministic flows or strict ordering.

## Essential Patterns

### Structured Output

```ts
import { ToolLoopAgent, Output } from 'ai';
import { z } from 'zod';

const analysisAgent = new ToolLoopAgent({
  model: 'openai/gpt-4o',
  output: Output.object({
    schema: z.object({
      sentiment: z.enum(['positive', 'neutral', 'negative']),
      summary: z.string(),
    }),
  }),
});
```

### Streaming Agent

```ts
const stream = myAgent.stream({ prompt: 'Summarize this report' });
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}
```

### API Route

```ts
import { createAgentUIStreamResponse } from 'ai';

export async function POST(request: Request) {
  const { messages } = await request.json();
  return createAgentUIStreamResponse({ agent: myAgent, messages });
}
```

### Type-Safe Client Integration

```ts
import { ToolLoopAgent, InferAgentUIMessage } from 'ai';

const myAgent = new ToolLoopAgent({ model, tools });
export type MyAgentUIMessage = InferAgentUIMessage<typeof myAgent>;
```

## Loop Control Checklist

- Set `stopWhen` (default: `stepCountIs(20)`) for safety.
- Use `hasToolCall('finalAnswer')` to stop on terminal actions.
- Use `prepareStep` to swap models, compress messages, or limit tools per step.

## Runtime Configuration

- Use `callOptionsSchema` to define type-safe runtime options.
- Use `prepareCall` to select model/tools or inject RAG context once per call.
- Use `prepareStep` for per-step decisions (budget limits, dynamic tools).

## Reference Files

| Reference | When to Use |
|-----------|-------------|
| `references/fundamentals.md` | ToolLoopAgent basics, Output types, streaming |
| `references/loop-control.md` | stopWhen, hasToolCall, prepareStep patterns |
| `references/configuration.md` | callOptionsSchema, prepareCall vs prepareStep |
| `references/workflow-patterns.md` | multi-agent workflows and routing |
| `references/real-world.md` | RAG, multimodal, file processing |
| `references/production.md` | monitoring, safety, cost control |
| `references/migration.md` | v6 migration notes |
