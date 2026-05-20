---
name: api-ai-vercel-ai-sdk
description: Vercel AI SDK patterns - providers, text generation, streaming, structured output, tool calling, chat UI hooks, embeddings, and RAG
---

# Vercel AI SDK Patterns

> **Quick Guide:** Use Vercel AI SDK (v6) to build AI-powered applications with a unified provider API. Use `generateText`/`streamText` for text generation and streaming, `Output.object()`/`Output.array()` for structured data with Zod, `tool()` for function calling, and `useChat`/`useCompletion` hooks for React chat UIs. Supports OpenAI, Anthropic, Google, and 20+ providers through a single API.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `ai` package (v6) with `Output.object()` / `Output.array()` for structured output -- NOT the deprecated `generateObject` / `streamObject` functions)**

**(You MUST define tool input schemas with `z.object()` and use `.describe()` on each property to help the model understand expected inputs)**

**(You MUST use `streamText` for user-facing responses to enable progressive rendering -- use `generateText` only for background/non-interactive tasks)**

**(You MUST handle streaming errors via `onError` callback -- streamText errors become part of the stream and are NOT thrown)**

**(You MUST use `inputSchema` (not `parameters`) when defining tools -- `parameters` was renamed in SDK v5+)**

</critical_requirements>

---

**Auto-detection:** AI SDK, Vercel AI, generateText, streamText, generateObject, streamObject, Output.object, Output.array, useChat, useCompletion, @ai-sdk/openai, @ai-sdk/anthropic, @ai-sdk/google, tool(), toolChoice, embedMany, embed, cosineSimilarity, ToolLoopAgent, smoothStream

**When to use:**

- Building AI chat interfaces with streaming responses
- Generating structured data (JSON objects, arrays) from LLMs with Zod schema validation
- Implementing tool calling / function calling with LLMs
- Creating multi-provider AI applications (OpenAI, Anthropic, Google, etc.)
- Building RAG pipelines with embeddings and vector similarity
- Adding AI text completion or generation to any Node.js/React/Next.js app

**Key patterns covered:**

- Provider setup and model configuration (OpenAI, Anthropic, Google, custom)
- Text generation (`generateText`) and streaming (`streamText`)
- Structured output with Zod schemas (`Output.object`, `Output.array`, `Output.choice`)
- Tool calling with `tool()`, multi-step execution, and approval flows
- React hooks: `useChat` for chat UIs, `useCompletion` for text completion
- Embeddings (`embed`, `embedMany`) and RAG patterns with `cosineSimilarity`

**When NOT to use:**

- Simple static content that doesn't need AI generation
- Server-side-only batch jobs where a direct provider SDK (e.g., `openai` npm package) is simpler
- Image generation only (AI SDK supports it, but dedicated image SDKs may be more feature-rich)

**Detailed Resources:**

- For provider setup, text generation, and error handling, see [examples/core.md](examples/core.md)
- For chat UI patterns with useChat, see [examples/chat.md](examples/chat.md)
- For tool definitions and multi-step calling, see [examples/tools.md](examples/tools.md)
- For Zod-based structured output, see [examples/structured-output.md](examples/structured-output.md)
- For embeddings and RAG, see [examples/rag.md](examples/rag.md)
- For quick reference tables, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

The Vercel AI SDK provides a **unified TypeScript API** for building AI-powered applications across providers. Instead of learning each provider's unique SDK, you write one set of code that works with OpenAI, Anthropic, Google, and 20+ other providers.

**Core principles:**

1. **Provider agnostic** -- Switch models by changing a string, not rewriting code. The provider abstraction means `generateText({ model: 'openai/gpt-4o' })` and `generateText({ model: 'anthropic/claude-sonnet-4.5' })` use the same API.
2. **Streaming first** -- `streamText` starts delivering tokens immediately. Use it for all user-facing responses. `generateText` blocks until completion and is better for background tasks and agent loops.
3. **Type-safe structured output** -- Define Zod schemas and get validated, typed objects back from the model. Use `.describe()` on schema properties to guide the model.
4. **Tools as first-class citizens** -- Define tools with Zod input schemas and execute functions. The SDK handles the tool call loop, including multi-step execution and human approval.
5. **Framework-agnostic UI hooks** -- `useChat` and `useCompletion` work with React, Svelte, Vue, and Angular. They manage streaming state, message history, and input handling.

**When to use Vercel AI SDK:**

- Multi-provider applications where you want to switch models easily
- Streaming chat interfaces with React/Next.js
- Structured data extraction from natural language
- Agent-style applications with tool calling loops
- RAG systems with embedding and retrieval

**When NOT to use:**

- Single-provider scripts where the native SDK is simpler and has fewer dependencies
- Extremely high-throughput batch processing (direct API calls avoid SDK overhead)
- Non-TypeScript environments (the SDK is TypeScript-first)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Provider Setup

Configure providers via direct imports (auto-reads env vars), custom instances, or AI Gateway. See [examples/core.md](examples/core.md) for full examples.

```typescript
import { gateway } from "ai";
import { openai } from "@ai-sdk/openai";

// Gateway: provider/model string routing
const model = gateway("anthropic/claude-sonnet-4.5");

// Direct: auto-reads OPENAI_API_KEY from env
const openaiModel = openai("gpt-4o");
```

Use `customProvider` for semantic model aliases (`models('fast')`, `models('smart')`). Never hardcode API keys.

---

### Pattern 2: Text Generation with generateText

Use `generateText` for non-interactive tasks. Returns a promise that resolves when complete. See [examples/core.md](examples/core.md).

```typescript
import { generateText } from "ai";

const { text, usage } = await generateText({
  model: "openai/gpt-4o",
  system: "You are a professional technical writer.",
  prompt: `Summarize: ${article}`,
});
```

Use `ModelMessage[]` for multi-turn conversations. Append `response.messages` for continued dialogue. Do NOT use `generateText` for user-facing responses -- use `streamText` instead.

---

### Pattern 3: Streaming with streamText

Use `streamText` for all user-facing responses. Errors are part of the stream (not thrown) -- use `onError`. See [examples/core.md](examples/core.md).

```typescript
import { streamText, smoothStream } from "ai";

const result = streamText({
  model: "anthropic/claude-sonnet-4.5",
  prompt: "Explain TypeScript.",
  experimental_transform: smoothStream(),
  onError({ error }) {
    console.error("Stream error:", error);
  },
});

for await (const part of result.textStream) {
  process.stdout.write(part);
}
```

Use `result.toTextStreamResponse()` in route handlers. Use `result.fullStream` for granular event types (`text-delta`, `tool-call`, `error`, `finish`).

---

### Pattern 4: Structured Output with Zod

Use `Output.object()` with `generateText`/`streamText` for type-safe structured data. See [examples/structured-output.md](examples/structured-output.md).

```typescript
import { generateText, Output } from "ai";
import { z } from "zod";

const schema = z.object({
  name: z.string().describe("Recipe name"),
  steps: z.array(z.string()).describe("Cooking instructions"),
});

const { output } = await generateText({
  model: "openai/gpt-4o",
  output: Output.object({ schema }),
  prompt: "Generate a vegetarian lasagna recipe.",
});
```

**Key variants:** `Output.array({ element })` with `elementStream` for streaming arrays, `Output.choice()` for classification, `partialOutputStream` for streaming partial objects. Do NOT use deprecated `generateObject`/`streamObject`.

---

### Pattern 5: Tool Calling

Define tools with `tool()`, Zod `inputSchema`, and `execute`. The SDK handles multi-step loops. See [examples/tools.md](examples/tools.md).

```typescript
import { generateText, tool, stepCountIs } from "ai";
import { z } from "zod";

const weatherTool = tool({
  description: "Get weather in a location",
  inputSchema: z.object({
    location: z.string().describe("City name"),
  }),
  execute: async ({ location }) => fetchWeather(location),
});

const MAX_STEPS = 5;
const { text } = await generateText({
  model: "openai/gpt-4o",
  tools: { weather: weatherTool },
  stopWhen: stepCountIs(MAX_STEPS),
  prompt: "Weather in SF and Tokyo?",
});
```

**Key features:** `needsApproval` for human-in-the-loop, `ToolLoopAgent` for reusable agents (use `instructions` not `system`), `toolChoice` to force/prevent tool usage, `activeTools`/`prepareStep` for per-step control. Always use `stepCountIs()` to prevent infinite loops.

---

### Pattern 6: useChat Hook (React)

`useChat` manages streaming chat state. v6 uses transport-based architecture and external input state. See [examples/chat.md](examples/chat.md).

```tsx
import { useChat } from "@ai-sdk/react";
import { useState } from "react";

export function Chat() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status, stop, error } = useChat();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage({ text: input }); // NOT { role, content }
    setInput("");
  }
  // ... render messages.parts, status-based UI
}
```

**v6 breaking changes:** `sendMessage({ text })` replaces `handleSubmit`/`append({ role, content })`. External `useState` for input (hook no longer manages it). `status` replaces `isLoading`. Import from `@ai-sdk/react` not `ai/react`.

---

### Pattern 7: useCompletion Hook (React)

`useCompletion` handles single-turn text completions. Unlike `useChat`, it still manages input state internally. See [examples/core.md](examples/core.md).

```tsx
import { useCompletion } from "@ai-sdk/react";

const { completion, input, handleInputChange, handleSubmit, isLoading } =
  useCompletion({
    api: "/api/completion",
  });
```

Good for autocomplete, summarization, and one-shot generation where multi-turn chat is not needed.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Function to Use

```
Do you need AI-generated content?
├─ YES -> Is it user-facing (needs progressive display)?
│   ├─ YES -> Is it a multi-turn conversation?
│   │   ├─ YES -> useChat hook (React) or streamText (server)
│   │   └─ NO -> Is it a single completion/generation?
│   │       ├─ YES -> useCompletion hook (React) or streamText (server)
│   │       └─ NO -> streamText with custom UI
│   └─ NO -> Is it a background task (agent, batch)?
│       ├─ YES -> generateText (blocks until complete)
│       └─ NO -> generateText for simple one-shots
├─ Do you need structured data (JSON/objects)?
│   ├─ YES -> Output.object() with Zod schema
│   │   ├─ Need streaming partial object? -> streamText + partialOutputStream
│   │   ├─ Need array of items? -> Output.array() + elementStream
│   │   └─ Need one of N options? -> Output.choice()
│   └─ NO -> Plain text generation
├─ Do you need the model to call functions?
│   ├─ YES -> Define tools with tool() + Zod inputSchema
│   │   ├─ Multi-step reasoning? -> stopWhen: stepCountIs(N)
│   │   ├─ Need human approval? -> needsApproval on tool
│   │   └─ Single tool call? -> Default (stops after first response)
│   └─ NO -> No tools needed
└─ Do you need vector embeddings?
    ├─ Single text -> embed()
    ├─ Batch of texts -> embedMany()
    └─ Similarity search -> cosineSimilarity()
```

### Which Provider to Choose

```
What is your primary concern?
├─ Best reasoning / complex tasks -> anthropic/claude-sonnet-4.5 or openai/o3
├─ Fast + cheap for simple tasks -> openai/gpt-4o-mini or anthropic/claude-haiku-4.5
├─ Structured output reliability -> openai/gpt-4o (best schema adherence)
├─ Multi-modal (images + text) -> openai/gpt-4o or anthropic/claude-sonnet-4.5
├─ Google ecosystem / grounding -> google/gemini-2.5-flash
└─ Provider agnostic -> Use AI Gateway with model aliases
```

</decision_framework>

---

<integration>

## Integration Guide

**Framework support:**

- Server-side route handlers for `streamText` (any framework with standard `Request`/`Response`)
- Frontend hooks (`useChat`, `useCompletion`) from `@ai-sdk/react` with framework-specific variants for Svelte, Vue, and Angular
- Edge runtime compatible (Cloudflare Workers, Vercel Edge)

**Provider architecture:**

- Core `ai` package provides `generateText`, `streamText`, `embed`, `Output`, `tool`, `gateway`
- Provider packages (`@ai-sdk/openai`, `@ai-sdk/anthropic`, `@ai-sdk/google`) auto-read environment variables
- `@ai-sdk/openai-compatible` supports any OpenAI-compatible API (Ollama, Together AI, etc.)
- AI Gateway (`gateway`) routes to any provider with a `provider/model` string

**Schema integration:**

- Structured output (`Output.object()`) and tool input schemas use Zod for validation and type inference
- MCP (Model Context Protocol) integration for standardized tool access

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using deprecated `generateObject` / `streamObject` instead of `generateText` + `Output.object()` (removed in v6)
- Using `parameters` instead of `inputSchema` in tool definitions (renamed in v5+)
- Using `generateText` for user-facing chat responses (blocks until complete, no streaming)
- Hardcoding API keys in source code instead of using environment variables
- Using `import { useChat } from 'ai/react'` instead of `import { useChat } from '@ai-sdk/react'`
- Using `CoreMessage` type instead of `ModelMessage` (renamed in v6)
- Calling `sendMessage({ role: 'user', content: text })` instead of `sendMessage({ text })` (v6 API change)

**Medium Priority Issues:**

- Missing `.describe()` on Zod schema properties for structured output (model gets less guidance)
- Not setting `stopWhen` with `stepCountIs()` for multi-step tool calling (risks infinite loops)
- Not handling stream errors with `onError` callback (errors silently disappear)
- Using `system` instead of `instructions` in `ToolLoopAgent` (renamed in v6)

**Common Mistakes:**

- Forgetting that `streamText` does NOT throw errors -- they appear in the stream as error events
- Not consuming the stream from `streamText` -- the function returns immediately, you must iterate the stream
- Using `object` destructure from deprecated `generateObject` instead of `output` from `generateText` with `Output.object()`
- Passing raw strings to `model` parameter without a provider prefix (e.g., `'gpt-4o'` instead of `'openai/gpt-4o'`)

**Gotchas & Edge Cases:**

- `smoothStream()` transform adds slight delay but makes output feel more natural -- always use for chat UIs
- `Output.array()` with `elementStream` yields each element only when fully validated -- partial elements are not emitted
- `embed()` and `embedMany()` require embedding model strings (e.g., `'openai/text-embedding-3-small'`), not chat model strings
- Zod schema support varies by provider -- complex unions and transforms may not work with all models
- `useChat` v6 no longer manages input state -- you must use external `useState` for the input field and call `sendMessage({ text })` (not `{ role, content }`)
- `convertToModelMessages()` is async in v6 (was sync as `convertToCoreMessages()` in v5)
- `fullStream` gives you all event types including `tool-call`, `tool-result`, `source`, and `error` -- `textStream` only gives text deltas
- Token usage is available via `usage` property on results, including cache hit details in `usage.inputTokenDetails`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `ai` package (v6) with `Output.object()` / `Output.array()` for structured output -- NOT the deprecated `generateObject` / `streamObject` functions)**

**(You MUST define tool input schemas with `z.object()` and use `.describe()` on each property to help the model understand expected inputs)**

**(You MUST use `streamText` for user-facing responses to enable progressive rendering -- use `generateText` only for background/non-interactive tasks)**

**(You MUST handle streaming errors via `onError` callback -- streamText errors become part of the stream and are NOT thrown)**

**(You MUST use `inputSchema` (not `parameters`) when defining tools -- `parameters` was renamed in SDK v5+)**

**Failure to follow these rules will produce broken AI integrations, deprecated API usage, or poor user experiences with blocked responses.**

</critical_reminders>
