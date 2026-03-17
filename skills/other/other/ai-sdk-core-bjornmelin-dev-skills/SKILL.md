---
name: ai-sdk-core
description: |
  Expert guidance for AI SDK Core: text generation, structured data, tool calling (tool/dynamicTool), MCP integration (createMCPClient, Experimental_StdioMCPTransport), embeddings/reranking, provider setup, middleware, telemetry, and error handling. Use when building with generateText/streamText, generateObject/streamObject, tools (needsApproval, strict, inputExamples, activeTools, toolChoice, experimental_context), embeddings (embed/embedMany/rerank), or MCP tools/resources/prompts/elicitation.
---

# AI SDK Core

Use AI SDK Core to generate text/structured output, call tools, and connect to MCP servers with consistent APIs across providers.

## Quick Start

```bash
pnpm add ai @ai-sdk/openai zod@^4.3.5
```

```ts
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'openai/gpt-4o',
  prompt: 'Explain quantum computing in one paragraph.',
});
```

## Function Selection

| Need | Function | Streaming |
|------|----------|-----------|
| Text response | `generateText` | No |
| Streaming text | `streamText` | Yes |
| Structured JSON | `generateObject` | No |
| Streaming JSON | `streamObject` | Yes |
| Embeddings | `embed` / `embedMany` | No |
| Rerank | `rerank` | No |

## Core Patterns

### Generate Text

```ts
import { generateText } from 'ai';

const { text, usage } = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  system: 'You are a helpful assistant.',
  prompt: 'What is the capital of France?',
});
```

### Stream Text

```ts
import { streamText } from 'ai';

const result = streamText({
  model: 'openai/gpt-4o',
  prompt: 'Write a short story.',
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

### Generate Structured Data

```ts
import { generateObject } from 'ai';
import { z } from 'zod';

const { object } = await generateObject({
  model: 'openai/gpt-4o',
  schema: z.object({
    recipe: z.object({
      name: z.string(),
      ingredients: z.array(z.object({ name: z.string(), amount: z.string() })),
      steps: z.array(z.string()),
    }),
  }),
  prompt: 'Generate a recipe for chocolate chip cookies.',
});
```

### Tool Calling (Typed)

```ts
import { generateText, tool } from 'ai';
import { z } from 'zod';

const { text, toolCalls } = await generateText({
  model: 'openai/gpt-4o',
  tools: {
    weather: tool({
      description: 'Get weather for a location',
      inputSchema: z.object({ location: z.string() }),
      execute: async ({ location }) => ({ temperature: 72, condition: 'sunny' }),
    }),
  },
  prompt: 'What is the weather in San Francisco?',
});
```

### Dynamic Tools (Runtime Schemas)

```ts
import { dynamicTool } from 'ai';
import { z } from 'zod';

const customTool = dynamicTool({
  description: 'Execute a custom function',
  inputSchema: z.object({}),
  execute: async input => ({ ok: true, input }),
});
```

### Multi-Step Tool Execution

```ts
import { generateText, stepCountIs } from 'ai';

const { steps } = await generateText({
  model: 'openai/gpt-4o',
  tools: { search, analyze, summarize },
  stopWhen: stepCountIs(5),
  prompt: 'Research and summarize AI developments.',
});
```

## Tooling Checklist

- Use `tool()` for typed inputs and `dynamicTool()` for unknown schemas.
- Use `needsApproval` for sensitive actions (tool-approval-request/response flow).
- Use `stopWhen` with `stepCountIs`/`hasToolCall` for multi-step loops.
- Use `prepareStep` for per-step controls (model swap, toolChoice, activeTools, prompt compression).
- Use `experimental_context` when tools need app-specific context.
- Use `inputExamples` and `strict` to improve tool call reliability.

## MCP Integration (Model Context Protocol)

- Use `createMCPClient()` to load MCP tools, resources, and prompts.
- Prefer HTTP transport for production; use `Experimental_StdioMCPTransport` only for local Node.js servers.
- Close MCP clients after use (try/finally or `onFinish`).

See `references/mcp-integration.md` for transports, schema definition, outputSchema typing, and elicitation.

## Reference Files

| Reference | When to Use |
|-----------|-------------|
| `references/text-generation.md` | generateText/streamText callbacks, streaming, response handling |
| `references/structured-data.md` | generateObject/streamObject, Output API, Zod patterns |
| `references/tool-calling.md` | tool/dynamicTool, approval flow, repair, activeTools, hooks |
| `references/dynamic-tools.md` | dynamicTool patterns, MCP + dynamic tools, large tool sets |
| `references/embeddings-rag.md` | embed/embedMany, rerank, chunking |
| `references/providers.md` | OpenAI/Anthropic/Google setup, registry, AI Gateway |
| `references/middleware.md` | wrapLanguageModel, built-in/custom middleware |
| `references/mcp-integration.md` | MCP client, transports, tools/resources/prompts/elicitation |
| `references/production.md` | Telemetry, error handling, testing, cost control |
| `references/migration.md` | v6 upgrade notes |

## Error Handling

```ts
import { generateText, AI_APICallError } from 'ai';

try {
  await generateText({ model: 'openai/gpt-4o', prompt: 'Hello' });
} catch (error) {
  if (error instanceof AI_APICallError) {
    console.error('API Error:', error.message);
  }
}
```

## Provider Setup

```ts
import { openai } from '@ai-sdk/openai';

const { text } = await generateText({
  model: openai('gpt-4o'),
  prompt: 'Hello!',
});
```

## Version Guidance

- Use AI SDK v6+ with matching provider packages.
- Pin major versions in `package.json` to avoid breaking changes.
