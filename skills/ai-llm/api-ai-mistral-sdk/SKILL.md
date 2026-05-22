---
name: api-ai-mistral-sdk
description: Official Mistral AI TypeScript SDK patterns — client setup, chat completions, streaming, function calling, structured outputs, embeddings, vision, Codestral FIM, and production best practices
---

# Mistral SDK Patterns

> **Quick Guide:** Use `@mistralai/mistralai` (ESM-only) to interact with Mistral's API. Use `client.chat.complete()` for chat, `client.chat.stream()` for streaming (async iterable via `for await`), `client.chat.parse()` with a Zod schema for structured outputs, and `client.fim.complete()` for Codestral fill-in-middle code completion. The SDK uses `responseFormat` (camelCase) not `response_format`. Streaming events expose content via `event.data.choices[0]?.delta?.content`. Retries default to `strategy: "none"` -- you must configure them explicitly for production.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `responseFormat` (camelCase) in SDK calls -- NOT `response_format` (snake_case). The SDK uses camelCase property names throughout.)**

**(You MUST configure retries explicitly -- the SDK defaults to `strategy: "none"` (no retries), unlike OpenAI's SDK which retries automatically)**

**(You MUST consume streaming results with `for await (const event of result)` and access content via `event.data.choices[0]?.delta?.content` -- the event shape differs from OpenAI)**

**(You MUST never hardcode API keys -- use `process.env["MISTRAL_API_KEY"]` with the bracket notation the SDK documents)**

**(You MUST use `client.chat.parse()` with a Zod schema for structured outputs -- NOT manual `JSON.parse()` on completion content)**

</critical_requirements>

---

**Auto-detection:** Mistral, mistral, @mistralai/mistralai, client.chat.complete, client.chat.stream, client.chat.parse, client.fim.complete, client.embeddings.create, mistral-large, mistral-small, codestral, pixtral, ministral, magistral, devstral, MISTRAL_API_KEY, responseFormat, mistral-embed

**When to use:**

- Building applications that call Mistral models directly (Mistral Large, Small, Codestral, etc.)
- Implementing chat completions with SSE streaming
- Using Codestral for code generation and fill-in-middle (FIM) completion
- Extracting structured data with `client.chat.parse()` and Zod schemas
- Implementing function calling / tool use
- Creating embeddings for RAG pipelines or semantic search
- Processing images with Pixtral / vision-capable models
- Using Mistral Agents API for pre-configured agent completions

**Key patterns covered:**

- Client initialization and configuration (retries, timeouts, custom HTTP client)
- Chat completions (`chat.complete`) and streaming (`chat.stream`)
- Structured outputs with `chat.parse()` and Zod schemas
- Function calling / tool use with tool call loop
- Embeddings (`embeddings.create`) with `mistral-embed`
- Vision (image URL / base64 with Pixtral models)
- Codestral FIM (`fim.complete`) for code completion
- Error handling, retry configuration, and production patterns

**When NOT to use:**

- Multi-provider applications where you need to switch between Mistral, OpenAI, Anthropic, etc. -- use a unified provider SDK
- React-specific chat UI hooks (`useChat`) -- use a framework-integrated AI SDK
- When you need OpenAI-compatible endpoints -- use OpenAI SDK with Mistral's compatible endpoint instead

---

## Examples Index

- [Core: Setup & Configuration](examples/core.md) -- Client init, production config, error handling, retries, custom HTTP client
- [Chat & Streaming](examples/chat.md) -- Chat completions, streaming with async iteration, multi-turn
- [Structured Output](examples/structured-output.md) -- `chat.parse()` with Zod, JSON mode, typed responses
- [Function Calling](examples/function-calling.md) -- Tool definitions, tool call loop, streaming tools
- [Embeddings & Vision](examples/embeddings-vision.md) -- Semantic search, image analysis with Pixtral
- [Codestral FIM](examples/codestral.md) -- Fill-in-middle code completion, code generation
- [Quick API Reference](reference.md) -- Model IDs, method signatures, error types, configuration options

---

<philosophy>

## Philosophy

The `@mistralai/mistralai` SDK is **auto-generated from Mistral's OpenAPI spec using Speakeasy**, giving you a thin, type-safe wrapper over the REST API. It is ESM-only and uses camelCase property names (not snake_case like the REST API).

**Core principles:**

1. **ESM-only** -- The package is published as ESM only. CommonJS projects must use `await import()`. This is a hard constraint, not optional.
2. **camelCase API surface** -- SDK properties use camelCase (`responseFormat`, `maxTokens`, `toolChoice`) even though the REST API uses snake_case. This catches OpenAI SDK migrants who write `response_format`.
3. **No automatic retries** -- Unlike OpenAI's SDK (2 retries by default), Mistral defaults to `strategy: "none"`. You must configure retries explicitly for production.
4. **Streaming via async iterables** -- `chat.stream()` returns an `EventStream` consumed with `for await...of`. Events have a `data` wrapper: `event.data.choices[0]?.delta?.content`.
5. **Structured outputs via `chat.parse()`** -- Pass a Zod schema directly to `responseFormat` and access `message.parsed` for typed results. No manual JSON schema construction needed.
6. **Codestral FIM** -- Dedicated `fim.complete()` endpoint for fill-in-middle code completion, separate from chat.

**When to use the Mistral SDK directly:**

- You only use Mistral models and want the simplest, most direct integration
- You need Mistral-specific features (Codestral FIM, Mistral Agents, Voxtral audio)
- You want minimal dependencies and zero abstraction overhead
- You need the latest Mistral API features on day one

**When NOT to use:**

- You need to switch between providers (OpenAI, Anthropic, Mistral) -- use a unified provider SDK
- You want React-specific chat UI hooks -- use a framework-integrated AI SDK
- You want an OpenAI-compatible wrapper -- Mistral exposes an OpenAI-compatible endpoint, use the OpenAI SDK for that

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize the Mistral client. It reads `MISTRAL_API_KEY` from the environment.

```typescript
// lib/mistral.ts -- basic setup
import { Mistral } from "@mistralai/mistralai";

const client = new Mistral({
  apiKey: process.env["MISTRAL_API_KEY"] ?? "",
});

export { client };
```

```typescript
// lib/mistral.ts -- production configuration
import { Mistral } from "@mistralai/mistralai";

const TIMEOUT_MS = 30_000;

const client = new Mistral({
  apiKey: process.env["MISTRAL_API_KEY"] ?? "",
  timeoutMs: TIMEOUT_MS,
  retryConfig: {
    strategy: "backoff",
    backoff: {
      initialInterval: 1_000,
      maxInterval: 30_000,
      exponent: 1.5,
      maxElapsedTime: 120_000,
    },
    retryConnectionErrors: true,
  },
});

export { client };
```

**Why good:** Explicit retry config (SDK defaults to no retries), named constants, env var with bracket notation

**See:** [examples/core.md](examples/core.md) for custom HTTP client, async API key provider, error handling

---

### Pattern 2: Chat Completions

Basic chat using `chat.complete()`.

```typescript
const result = await client.chat.complete({
  model: "mistral-large-latest",
  messages: [
    { role: "system", content: "You are a helpful coding assistant." },
    { role: "user", content: "Explain TypeScript generics." },
  ],
});

const content = result?.choices?.[0]?.message?.content;
console.log(content);
```

**Why good:** Uses `system` role for instructions, safe optional chaining on nullable response

```typescript
// BAD: Using snake_case properties (REST API style, not SDK style)
const result = await client.chat.complete({
  model: "mistral-large-latest",
  messages: [{ role: "user", content: "hello" }],
  response_format: { type: "json_object" }, // WRONG: use responseFormat
  max_tokens: 100, // WRONG: use maxTokens
});
```

**Why bad:** SDK uses camelCase properties -- `response_format` and `max_tokens` will be silently ignored

**See:** [examples/chat.md](examples/chat.md) for multi-turn, token tracking, temperature control

---

### Pattern 3: Streaming

Use `chat.stream()` for streaming. Events are async iterables.

```typescript
const result = await client.chat.stream({
  model: "mistral-large-latest",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Explain async/await in TypeScript." },
  ],
});

for await (const event of result) {
  const content = event.data.choices[0]?.delta?.content;
  if (content) {
    process.stdout.write(content as string);
  }
}
console.log();
```

**Why good:** Proper `for await` iteration, accesses `event.data` (not `event` directly), handles nullable delta

```typescript
// BAD: Trying to access content directly on event (OpenAI pattern)
for await (const chunk of result) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? ""); // WRONG
}
```

**Why bad:** Mistral streaming events wrap data in `event.data` -- direct access on `chunk` will fail

**See:** [examples/chat.md](examples/chat.md) for complete streaming examples

---

### Pattern 4: Structured Outputs with Zod

Use `chat.parse()` with a Zod schema for type-safe structured responses.

```typescript
import { Mistral } from "@mistralai/mistralai";
import { z } from "zod";

const client = new Mistral({ apiKey: process.env["MISTRAL_API_KEY"] ?? "" });

const BookSchema = z.object({
  name: z.string(),
  authors: z.array(z.string()),
});

const MAX_TOKENS = 256;

const result = await client.chat.parse({
  model: "mistral-large-latest",
  messages: [
    { role: "system", content: "Extract the book information." },
    { role: "user", content: "I recently read 'Dune' by Frank Herbert." },
  ],
  responseFormat: BookSchema,
  maxTokens: MAX_TOKENS,
  temperature: 0,
});

const parsed = result.choices?.[0]?.message?.parsed;
// parsed is typed as { name: string; authors: string[] }
```

**Why good:** Schema passed directly to `responseFormat`, `message.parsed` is fully typed, named constants

**See:** [examples/structured-output.md](examples/structured-output.md) for JSON mode, complex schemas

---

### Pattern 5: Function Calling / Tool Use

Define tools and handle the tool call loop.

```typescript
const tools = [
  {
    type: "function" as const,
    function: {
      name: "get_weather",
      description: "Get current weather for a city",
      parameters: {
        type: "object",
        properties: {
          location: { type: "string", description: "City name" },
        },
        required: ["location"],
      },
    },
  },
];

const result = await client.chat.complete({
  model: "mistral-large-latest",
  messages: [{ role: "user", content: "Weather in Paris?" }],
  tools,
  toolChoice: "any",
});

const toolCall = result?.choices?.[0]?.message?.toolCalls?.[0];
if (toolCall) {
  const args = JSON.parse(toolCall.function.arguments);
  console.log(`Call ${toolCall.function.name} with:`, args);
}
```

**Why good:** Uses `toolChoice` (camelCase), `toolCalls` (camelCase), proper `as const` for type literal

**See:** [examples/function-calling.md](examples/function-calling.md) for complete tool loop, parallel calls

---

### Pattern 6: Embeddings

Create embeddings with `mistral-embed`. Note: uses `inputs` (plural), not `input`.

```typescript
const EMBEDDING_MODEL = "mistral-embed";

const result = await client.embeddings.create({
  model: EMBEDDING_MODEL,
  inputs: ["First document", "Second document", "Third document"],
});

const vectors = result.data?.map((item) => item.embedding) ?? [];
```

**Why good:** Uses `inputs` (Mistral-specific, plural), named model constant, safe optional chaining

```typescript
// BAD: Using singular 'input' (OpenAI pattern)
const result = await client.embeddings.create({
  model: "mistral-embed",
  input: ["First document"], // WRONG: Mistral uses 'inputs' (plural)
});
```

**Why bad:** Mistral SDK uses `inputs` (plural) -- `input` (singular) will error or be silently ignored

**See:** [examples/embeddings-vision.md](examples/embeddings-vision.md) for cosine similarity, semantic search

---

### Pattern 7: Vision (Pixtral)

Send images to vision-capable models using multi-part content arrays.

```typescript
const result = await client.chat.complete({
  model: "mistral-small-latest",
  messages: [
    {
      role: "user",
      content: [
        { type: "text", text: "What is in this image?" },
        {
          type: "image_url",
          imageUrl: "https://example.com/photo.jpg",
        },
      ],
    },
  ],
});
```

**Why good:** Uses `imageUrl` (camelCase string), not `image_url: { url }` (OpenAI's nested object pattern)

**See:** [examples/embeddings-vision.md](examples/embeddings-vision.md) for base64 images, multiple images

---

### Pattern 8: Codestral FIM

Fill-in-middle code completion using the dedicated FIM endpoint.

```typescript
const result = await client.fim.complete({
  model: "codestral-latest",
  prompt: "function fibonacci(n: number): number {\n  if (n <= 1) return n;\n",
  suffix: "}\n\nconsole.log(fibonacci(10));",
  temperature: 0,
});

const completion = result.choices?.[0]?.message?.content;
// completion fills the gap between prompt and suffix
```

**Why good:** Dedicated FIM endpoint, separate `prompt` + `suffix` (not messages), deterministic with `temperature: 0`

**See:** [examples/codestral.md](examples/codestral.md) for code generation patterns

---

### Pattern 9: Error Handling

The SDK provides specific error types. Configure retries since the default is no retries.

```typescript
import { Mistral } from "@mistralai/mistralai";
import {
  SDKError,
  SDKValidationError,
  HTTPValidationError,
} from "@mistralai/mistralai/models/errors";

try {
  const result = await client.chat.complete({
    model: "mistral-large-latest",
    messages: [{ role: "user", content: "Hello" }],
  });
} catch (error) {
  if (error instanceof HTTPValidationError) {
    console.error("Validation error:", error.message);
  } else if (error instanceof SDKValidationError) {
    console.error("Input validation error:", error.message);
  } else if (error instanceof SDKError) {
    console.error(`API error [${error.statusCode}]: ${error.message}`);
  } else {
    throw error;
  }
}
```

**Why good:** Specific error types checked in order of specificity, re-throws unexpected errors

**See:** [examples/core.md](examples/core.md) for full error handling, timeout handling, retry configuration

</patterns>

---

<performance>

## Performance Optimization

### Model Selection

```
General purpose (most capable)    -> mistral-large-latest (Mistral Large 3)
Balanced cost/quality             -> mistral-medium-latest (Mistral Medium 3.1)
Cost-sensitive / fast             -> mistral-small-latest (Mistral Small 4)
Edge / minimal                    -> ministral-3b-latest or ministral-8b-latest
Complex reasoning                 -> magistral-medium-latest
Code generation                   -> codestral-latest or devstral-latest
Code completion (FIM)             -> codestral-latest (dedicated FIM endpoint)
Vision / images                   -> mistral-small-latest or mistral-large-latest
Embeddings                        -> mistral-embed (1024 dimensions)
Code embeddings                   -> codestral-embed-latest
```

### Key Optimization Patterns

- **Configure retries** -- Default is no retries. Always set `retryConfig` for production.
- **Set timeouts** -- Default is no timeout (`-1`). Set `timeoutMs` to avoid hanging requests.
- **Use `temperature: 0`** for deterministic output (enables server-side caching).
- **Batch embedding inputs** -- Pass multiple strings to `inputs` array in one call.
- **Use FIM for code completion** -- `fim.complete()` is purpose-built and more efficient than chat for code completion tasks.

</performance>

---

<decision_framework>

## Decision Framework

### Which Method to Use

```
What do you need?
+-- Chat completion (text in, text out)?
|   +-- Need streaming? -> client.chat.stream()
|   +-- Need structured JSON? -> client.chat.parse() with Zod schema
|   +-- Basic completion? -> client.chat.complete()
+-- Code completion / fill-in-middle?
|   +-- YES -> client.fim.complete() with Codestral
+-- Embeddings for search/RAG?
|   +-- YES -> client.embeddings.create() with mistral-embed
+-- Pre-configured agent?
    +-- YES -> client.agents.complete() with agent ID
```

### Which Model to Choose

```
What is your task?
+-- Most capable general purpose -> mistral-large-latest
+-- Balanced cost/performance -> mistral-medium-latest
+-- Fast + cost-efficient -> mistral-small-latest
+-- Minimal / edge deployment -> ministral-3b-latest
+-- Complex reasoning / math -> magistral-medium-latest
+-- Code generation (chat) -> codestral-latest or devstral-latest
+-- Code completion (FIM) -> codestral-latest
+-- Vision / image analysis -> mistral-small-latest (or any vision-capable model)
+-- Embeddings -> mistral-embed
+-- Code embeddings -> codestral-embed-latest
```

### Streaming vs Non-Streaming

```
Is the response user-facing?
+-- YES -> Use client.chat.stream()
|   +-- Iterate with: for await (const event of result)
|   +-- Access content: event.data.choices[0]?.delta?.content
+-- NO -> Use client.chat.complete()
    +-- Background processing -> chat.complete()
    +-- Structured output -> chat.parse() with Zod
```

### When to Use This SDK vs a Provider-Agnostic SDK

```
Do you need multiple LLM providers (Mistral + others)?
+-- YES -> Not this skill's scope -- use a unified provider SDK
+-- NO -> Do you need Mistral-specific features?
    +-- YES -> Use Mistral SDK directly
    |   Examples: Codestral FIM, Mistral Agents,
    |   Voxtral audio, OCR, custom endpoints
    +-- NO -> Mistral SDK is simplest for Mistral-only use
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `response_format` (snake_case) instead of `responseFormat` (camelCase) -- silently ignored, no error thrown
- Using `input` (singular) for embeddings instead of `inputs` (plural) -- Mistral-specific naming
- Not configuring retries for production (SDK defaults to `strategy: "none"` -- zero retries)
- Hardcoding API keys instead of using environment variables
- Accessing `chunk.choices[0]?.delta?.content` directly on streaming events instead of `event.data.choices[0]?.delta?.content`

**Medium Priority Issues:**

- Not setting `timeoutMs` for production (default is `-1`, meaning no timeout -- requests can hang indefinitely)
- Using `max_tokens` instead of `maxTokens` (camelCase SDK convention)
- Missing `system` role message for behavior guidance
- Using `tool_choice` instead of `toolChoice`
- Using `tool_calls` instead of `toolCalls` when reading responses

**Common Mistakes:**

- Importing from `"mistralai"` instead of `"@mistralai/mistralai"` -- the correct package name has the org scope
- Using CommonJS `require()` -- the package is ESM-only, use `import` or `await import()`
- Confusing Mistral's `imageUrl: "url"` (flat string) with OpenAI's `image_url: { url: "..." }` (nested object)
- Using `client.chat.completions.create()` (OpenAI pattern) instead of `client.chat.complete()` (Mistral pattern)
- Assuming embedding dimensions match OpenAI's -- `mistral-embed` returns 1024-dimensional vectors, not 1536

**Gotchas & Edge Cases:**

- The SDK is ESM-only. In CommonJS projects, you must use `const { Mistral } = await import("@mistralai/mistralai")`.
- Streaming content may be `string | string[]` -- cast or check type when writing to stdout.
- `chat.parse()` requires a Zod schema passed to `responseFormat` -- it does not accept `{ type: "json_object" }`.
- The `apiKey` constructor option accepts a string OR an async function `() => Promise<string>` for dynamic key rotation.
- Model aliases like `mistral-large-latest` resolve to the latest version of that model tier. Pin to specific versions (e.g., `mistral-large-3-25-12`) for reproducibility.
- `toolChoice: "any"` forces the model to call a tool. `toolChoice: "auto"` lets the model decide. `toolChoice: "none"` prevents tool calls.
- `parallelToolCalls: false` forces sequential tool calling (default `true` allows parallel).
- FIM endpoint (`fim.complete()`) uses `prompt` + `suffix` parameters, NOT the `messages` array.
- `safePrompt: true` injects Mistral's safety system prompt before your messages.
- The SDK provides standalone functions (e.g., `chatComplete()` from `"@mistralai/mistralai/funcs/chatComplete.js"`) for tree-shaking in browser/edge runtimes.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `responseFormat` (camelCase) in SDK calls -- NOT `response_format` (snake_case). The SDK uses camelCase property names throughout.)**

**(You MUST configure retries explicitly -- the SDK defaults to `strategy: "none"` (no retries), unlike OpenAI's SDK which retries automatically)**

**(You MUST consume streaming results with `for await (const event of result)` and access content via `event.data.choices[0]?.delta?.content` -- the event shape differs from OpenAI)**

**(You MUST never hardcode API keys -- use `process.env["MISTRAL_API_KEY"]` with the bracket notation the SDK documents)**

**(You MUST use `client.chat.parse()` with a Zod schema for structured outputs -- NOT manual `JSON.parse()` on completion content)**

**Failure to follow these rules will produce broken API calls (snake_case properties silently ignored), unreliable production services (no retries), or incorrectly parsed streaming data.**

</critical_reminders>
