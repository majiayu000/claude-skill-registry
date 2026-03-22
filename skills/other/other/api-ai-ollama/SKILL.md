---
name: api-ai-ollama
description: Local LLM inference with the Ollama JavaScript client -- chat, streaming, tool calling, vision, embeddings, structured output, model management, and OpenAI-compatible endpoint
---

# Ollama Patterns

> **Quick Guide:** Use the `ollama` npm package to run LLMs locally. Use `ollama.chat()` for conversations and `ollama.generate()` for single prompts. Enable streaming with `stream: true` and iterate with `for await`. Use `format` with a JSON schema (via `zodToJsonSchema`) for structured outputs. Use `tools` array for function calling. Use `ollama.embed()` for embeddings. Models run on your machine -- no API keys required for local use, but be aware of model loading time and memory usage.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `ollama.chat()` for conversations and `ollama.generate()` for single-prompt completions -- they have different parameter shapes)**

**(You MUST handle model loading delays -- the first request after a model is loaded takes significantly longer due to model initialization)**

**(You MUST use `zodToJsonSchema()` from `zod-to-json-schema` for structured outputs -- do NOT manually construct JSON schemas)**

**(You MUST accumulate streamed `thinking`, `content`, and `tool_calls` fields to maintain conversation history in multi-turn interactions)**

**(You MUST never assume a model is already pulled -- check with `ollama.list()` or handle errors from missing models gracefully)**

</critical_requirements>

---

**Auto-detection:** Ollama, ollama, ollama.chat, ollama.generate, ollama.embed, ollama.pull, ollama.list, ollama.show, ollama.delete, ollama.ps, ollama.abort, ollama.create, keep_alive, zodToJsonSchema, OLLAMA_HOST, llama3, mistral, qwen, gemma, phi, deepseek, local LLM

**When to use:**

- Running LLMs locally for development, testing, or privacy-sensitive workloads
- Building chat applications with local models (Llama, Mistral, Qwen, Gemma, etc.)
- Extracting structured data from text or images using local models with JSON schemas
- Implementing tool calling / function calling with locally-hosted models
- Generating embeddings for RAG or semantic search without cloud API costs
- Managing local model lifecycle (pull, list, show, delete, copy)
- Prototyping AI features before committing to a cloud provider

**Key patterns covered:**

- Client setup (default and custom instances)
- Chat completions (`ollama.chat`) and text generation (`ollama.generate`)
- Streaming with `for await` and accumulated state
- Structured output with `format` + `zodToJsonSchema`
- Tool calling with `tools` array and multi-turn tool loops
- Vision / multimodal inputs with `images` parameter
- Embeddings with `ollama.embed()`
- Model management (pull, list, show, delete, copy, ps)
- OpenAI-compatible endpoint for drop-in migration

**When NOT to use:**

- Production workloads requiring guaranteed uptime and SLAs -- use a cloud LLM provider
- Multi-provider applications where you need to switch between OpenAI, Anthropic, Google -- use a unified provider SDK
- Applications requiring the latest proprietary models (GPT-5, Claude) -- those are cloud-only

---

## Examples Index

- [Core: Setup, Chat & Generate](examples/core.md) -- Client init, chat, generate, streaming, error handling
- [Tool Calling](examples/tools.md) -- Tool definitions, single/parallel calls, multi-turn agent loops
- [Structured Output](examples/structured-output.md) -- JSON schema via Zod, vision extraction
- [Embeddings & Vision](examples/embeddings-vision.md) -- Embeddings, image analysis, multimodal
- [Model Management](examples/model-management.md) -- Pull, list, show, delete, copy, ps
- [Quick API Reference](reference.md) -- Method signatures, options, response types, model names

---

<philosophy>

## Philosophy

The Ollama JavaScript library is a **thin client over Ollama's local REST API** (default `http://127.0.0.1:11434`). It provides direct access to locally-running open-source LLMs with zero cloud dependencies.

**Core principles:**

1. **Local-first** -- Models run on your hardware. No API keys required for local use, complete data privacy, no per-token costs. Trade-off: you need sufficient GPU/CPU memory.
2. **Simple API** -- `ollama.chat()` and `ollama.generate()` are the two primary methods. The default import is a pre-configured singleton client; create custom instances with `new Ollama()` for non-default hosts.
3. **Streaming by default in REST, opt-in in SDK** -- The REST API streams by default. The SDK returns full responses by default; set `stream: true` to get an `AsyncGenerator`.
4. **Model-agnostic** -- The same API works with any Ollama-supported model (Llama, Mistral, Qwen, Gemma, Phi, DeepSeek, etc.). Model capabilities (vision, tool calling, structured output) depend on the model.
5. **OpenAI-compatible** -- Ollama exposes `/v1/chat/completions` and `/v1/embeddings` endpoints, allowing the OpenAI SDK to connect with `baseURL: 'http://localhost:11434/v1'`.

**When to use Ollama:**

- Local development and testing without cloud costs
- Privacy-sensitive workloads where data cannot leave your infrastructure
- Prototyping AI features before choosing a cloud provider
- Running open-source models (Llama, Mistral, etc.) on your own hardware
- Offline or air-gapped environments

**When NOT to use:**

- Production workloads requiring high availability and SLAs
- Applications needing proprietary models (GPT-5, Claude)
- When you need a multi-provider abstraction layer

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

The default import is a pre-configured singleton pointing to `http://127.0.0.1:11434`.

```typescript
// lib/ollama.ts -- default client (most common)
import ollama from "ollama";

// Use directly -- connects to localhost:11434
const response = await ollama.chat({
  model: "llama3.1",
  messages: [{ role: "user", content: "Hello" }],
});
```

```typescript
// lib/ollama.ts -- custom client for non-default host
import { Ollama } from "ollama";

const ollama = new Ollama({
  host: "http://192.168.1.100:11434",
});

export { ollama };
```

**Why good:** Minimal setup, default client requires zero configuration, custom client for remote servers

```typescript
// BAD: Hardcoding host inline everywhere
import { Ollama } from "ollama";
const response = await new Ollama({ host: "http://192.168.1.100:11434" }).chat({
  model: "llama3.1",
  messages: [{ role: "user", content: "Hello" }],
});
```

**Why bad:** Creates a new client instance per request, no reuse, host scattered across codebase

**See:** [examples/core.md](examples/core.md) for cloud API setup, custom headers, browser usage

---

### Pattern 2: Chat Completions

Multi-turn conversations with message history. You manage the messages array.

```typescript
import ollama from "ollama";

const response = await ollama.chat({
  model: "llama3.1",
  messages: [
    { role: "system", content: "You are a helpful coding assistant." },
    { role: "user", content: "Explain TypeScript generics." },
  ],
});

console.log(response.message.content);
```

**Why good:** Clear message roles, system message for behavior control, direct content access

```typescript
// BAD: Not checking response, no system message
const res = await ollama.chat({
  model: "llama3.1",
  messages: [{ role: "user", content: "do something" }],
});
```

**Why bad:** No system instruction means unpredictable behavior, vague prompt

**See:** [examples/core.md](examples/core.md) for multi-turn conversations, model options

---

### Pattern 3: Text Generation

Single-prompt completions without message history. Simpler than chat for one-shot tasks.

```typescript
import ollama from "ollama";

const response = await ollama.generate({
  model: "llama3.1",
  prompt: "Write a haiku about TypeScript.",
  system: "You are a creative writer.",
});

console.log(response.response);
```

**Why good:** Simpler API for one-shot tasks, `system` parameter instead of message array

**See:** [examples/core.md](examples/core.md) for generate with images, suffix, raw mode

---

### Pattern 4: Streaming

Set `stream: true` to get an `AsyncGenerator`. Iterate with `for await`.

```typescript
import ollama from "ollama";

const stream = await ollama.chat({
  model: "llama3.1",
  messages: [{ role: "user", content: "Explain async/await." }],
  stream: true,
});

for await (const chunk of stream) {
  process.stdout.write(chunk.message.content);
}
console.log(); // newline
```

**Why good:** Progressive output for better UX, memory-efficient for long responses

```typescript
// BAD: Not consuming the stream
const stream = await ollama.chat({
  model: "llama3.1",
  messages: [{ role: "user", content: "Hello" }],
  stream: true,
});
// Stream never consumed -- response is lost
```

**Why bad:** Stream must be consumed via iteration, otherwise the response is silently lost

**See:** [examples/core.md](examples/core.md) for generate streaming, abort, thinking mode streaming

---

### Pattern 5: Structured Output with Zod

Use `format` with a JSON schema to constrain model output. Use `zodToJsonSchema()` from `zod-to-json-schema` to convert Zod schemas.

```typescript
import ollama from "ollama";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const Country = z.object({
  name: z.string(),
  capital: z.string(),
  languages: z.array(z.string()),
});

type Country = z.infer<typeof Country>;

const response = await ollama.chat({
  model: "llama3.1",
  messages: [
    {
      role: "user",
      content: "Tell me about France. Respond in JSON.",
    },
  ],
  format: zodToJsonSchema(Country),
});

const country: Country = Country.parse(JSON.parse(response.message.content));
console.log(country.capital); // "Paris"
```

**Why good:** Type-safe output via Zod, JSON schema constrains model output, parse validates response

```typescript
// BAD: Using format: 'json' without a schema
const response = await ollama.chat({
  model: "llama3.1",
  messages: [{ role: "user", content: "Tell me about France as JSON" }],
  format: "json",
});
// No schema enforcement -- model can return any JSON shape
```

**Why bad:** `format: 'json'` only ensures valid JSON syntax, not structure -- use a JSON schema for reliable extraction

**See:** [examples/structured-output.md](examples/structured-output.md) for vision extraction, complex schemas

---

### Pattern 6: Tool Calling

Define tools the model can request. Handle `tool_calls` in responses and feed results back.

```typescript
import ollama from "ollama";

const tools = [
  {
    type: "function" as const,
    function: {
      name: "get_weather",
      description: "Get the current weather for a city",
      parameters: {
        type: "object",
        required: ["city"],
        properties: {
          city: { type: "string", description: "City name" },
        },
      },
    },
  },
];

const response = await ollama.chat({
  model: "llama3.1",
  messages: [{ role: "user", content: "What is the weather in Tokyo?" }],
  tools,
});

if (response.message.tool_calls?.length) {
  for (const toolCall of response.message.tool_calls) {
    console.log(`Call: ${toolCall.function.name}`);
    console.log(`Args:`, toolCall.function.arguments);
  }
}
```

**Why good:** Standard tool schema format, checks for tool_calls before processing, arguments already parsed (not stringified JSON)

**See:** [examples/tools.md](examples/tools.md) for multi-turn tool loops, streaming tool calls, parallel tools

---

### Pattern 7: Embeddings

Use `ollama.embed()` for text embeddings. Supports single or batch inputs.

```typescript
import ollama from "ollama";

const EMBEDDING_MODEL = "nomic-embed-text";

const response = await ollama.embed({
  model: EMBEDDING_MODEL,
  input: [
    "TypeScript is a typed superset of JavaScript.",
    "Rust is a systems programming language.",
  ],
});

console.log(`Vectors: ${response.embeddings.length}`);
console.log(`Dimensions: ${response.embeddings[0].length}`);
```

**Why good:** Batch multiple inputs in one call, named constant for model, returns array of number arrays

**See:** [examples/embeddings-vision.md](examples/embeddings-vision.md) for semantic search, cosine similarity

---

### Pattern 8: Model Management

Pull, list, show, and delete models programmatically.

```typescript
import ollama from "ollama";

// List available models
const models = await ollama.list();
for (const model of models.models) {
  console.log(`${model.name} (${model.size} bytes)`);
}

// Pull a model with progress streaming
const stream = await ollama.pull({ model: "llama3.1", stream: true });
for await (const progress of stream) {
  console.log(
    `${progress.status}: ${progress.completed ?? 0}/${progress.total ?? 0}`,
  );
}

// Show model details
const info = await ollama.show({ model: "llama3.1" });
console.log(`Parameters: ${info.details.parameter_size}`);
console.log(`Quantization: ${info.details.quantization_level}`);

// Delete a model
await ollama.delete({ model: "old-model" });
```

**Why good:** Streaming progress for large downloads, programmatic model lifecycle, detailed model metadata

**See:** [examples/model-management.md](examples/model-management.md) for copy, create, running models (ps)

---

### Pattern 9: OpenAI-Compatible Endpoint

Ollama exposes `/v1/chat/completions` and `/v1/embeddings` that work with the OpenAI SDK.

```typescript
import OpenAI from "openai";

const OLLAMA_BASE_URL = "http://localhost:11434/v1";

const client = new OpenAI({
  baseURL: OLLAMA_BASE_URL,
  apiKey: "ollama", // Required by SDK but unused by Ollama
});

const completion = await client.chat.completions.create({
  model: "llama3.1",
  messages: [{ role: "user", content: "Why is the sky blue?" }],
});

console.log(completion.choices[0].message.content);
```

**Why good:** Drop-in replacement for OpenAI SDK code, named constant for URL, easy to switch between local and cloud

**When to use:** When migrating existing OpenAI SDK code to local models, or when you want to use OpenAI SDK tooling (structured outputs, streaming helpers) with local models

**When not to use:** For new Ollama-native code, prefer the `ollama` package directly -- it exposes Ollama-specific features (model management, `keep_alive`, thinking mode) that the OpenAI compat layer does not

**See:** [reference.md](reference.md) for supported and unsupported OpenAI features

</patterns>

---

<decision_framework>

## Decision Framework

### `ollama.chat()` vs `ollama.generate()`

```
Need multi-turn conversation history?
+-- YES -> ollama.chat() (messages array with roles)
+-- NO -> Is it a single prompt completion?
    +-- YES -> ollama.generate() (simpler API)
    +-- NO -> ollama.chat() (default choice for most use cases)
```

### Native Ollama SDK vs OpenAI-Compatible Endpoint

```
Do you have existing OpenAI SDK code to migrate?
+-- YES -> Use OpenAI SDK with baseURL: 'http://localhost:11434/v1'
+-- NO -> Do you need Ollama-specific features?
    +-- YES -> Use ollama package (model management, keep_alive, thinking, abort)
    +-- NO -> Either works, prefer ollama package for new code
```

### Structured Output vs Plain Text

```
Do you need structured data from the model?
+-- YES -> Use format parameter with zodToJsonSchema()
|   +-- Always include "respond in JSON" in the prompt
|   +-- Always parse and validate with Zod after receiving response
+-- NO -> Omit format parameter (plain text response)
```

### Model Selection Guidance

```
What is your task?
+-- General chat / coding -> llama3.1 (8B for speed, 70B for quality)
+-- Fast + small -> phi4-mini, gemma3 (smaller memory footprint)
+-- Code generation -> qwen2.5-coder, deepseek-coder-v2
+-- Vision/multimodal -> llama3.2-vision, gemma3
+-- Embeddings -> nomic-embed-text, all-minilm
+-- Tool calling -> llama3.1, qwen3, mistral
+-- Reasoning/thinking -> qwen3 (with think: true), deepseek-r1
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Not handling model loading time -- first request after model load can take 30+ seconds on CPU; show a loading indicator or set `keep_alive` to keep models warm
- Using `format: 'json'` instead of a JSON schema -- only ensures valid JSON syntax, not structure; always use `zodToJsonSchema()` for reliable extraction
- Not accumulating streamed fields in multi-turn conversations -- you must collect `thinking`, `content`, and `tool_calls` from all chunks to maintain history
- Assuming all models support all features -- tool calling, vision, and structured output depend on the model; check model capabilities first

**Medium Priority Issues:**

- Not setting `keep_alive` for latency-sensitive applications -- models unload after 5 minutes of inactivity by default; set `keep_alive: '30m'` or `keep_alive: -1` (indefinite) for persistent sessions
- Creating new `Ollama()` instances per request instead of reusing a singleton client
- Not handling `AbortError` when using `ollama.abort()` -- listening threads throw when streams are cancelled
- Ignoring model size vs available memory -- loading a 70B model on 8GB RAM will fail or swap heavily

**Common Mistakes:**

- Confusing `ollama.chat()` and `ollama.generate()` parameters -- `chat` uses `messages[]`, `generate` uses `prompt` and `system`
- Using `ollama.embeddings()` (deprecated) instead of `ollama.embed()` -- the newer `embed()` method supports batch inputs
- Passing image URLs to `images` parameter -- Ollama expects `Uint8Array` or base64-encoded strings, not URLs
- Using tool calling with models that do not support it -- not all models handle tools; use Llama 3.1+, Qwen 3, or Mistral for reliable tool calling
- Forgetting to `JSON.parse()` the response content when using structured output -- Ollama returns JSON as a string in `message.content`, not a parsed object

**Gotchas & Edge Cases:**

- Ollama returns tool call arguments as already-parsed objects (not JSON strings like OpenAI) -- `toolCall.function.arguments` is an object, not a string
- The `keep_alive` parameter accepts both duration strings (`'5m'`, `'1h'`) and numbers (seconds) -- `0` unloads immediately, `-1` keeps loaded indefinitely
- `ollama.abort()` cancels ALL active streams for that client instance, not individual requests
- Model names can include tags (`llama3.1:8b`, `llama3.1:70b`) -- omitting the tag uses the default (usually smallest)
- The `think` parameter enables extended reasoning but only works with models that support it (Qwen 3, DeepSeek R1) -- it adds a `thinking` field to the response alongside `content`
- Browser usage requires importing from `ollama/browser` instead of `ollama` -- the default import uses Node.js-specific APIs
- Cloud API access (ollama.com) requires an API key via `Authorization: Bearer` header and setting `host: 'https://ollama.com'`
- Response includes performance metrics: `total_duration`, `eval_count`, `eval_duration` (in nanoseconds) -- calculate tokens/second with `eval_count / eval_duration * 1e9`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `ollama.chat()` for conversations and `ollama.generate()` for single-prompt completions -- they have different parameter shapes)**

**(You MUST handle model loading delays -- the first request after a model is loaded takes significantly longer due to model initialization)**

**(You MUST use `zodToJsonSchema()` from `zod-to-json-schema` for structured outputs -- do NOT manually construct JSON schemas)**

**(You MUST accumulate streamed `thinking`, `content`, and `tool_calls` fields to maintain conversation history in multi-turn interactions)**

**(You MUST never assume a model is already pulled -- check with `ollama.list()` or handle errors from missing models gracefully)**

**Failure to follow these rules will produce unreliable, poorly-typed, or broken local LLM integrations.**

</critical_reminders>
