---
name: api-ai-together-ai
description: Together AI SDK patterns for TypeScript — client setup, chat completions, streaming, structured output, function calling, embeddings, image generation, fine-tuning, and OpenAI-compatible endpoints
---

# Together AI SDK Patterns

> **Quick Guide:** Use the `together-ai` npm package to access 200+ open-source models (Llama, Qwen, Mistral, DeepSeek) via Together AI's fast inference API. The SDK mirrors the OpenAI API shape -- `client.chat.completions.create()` for chat, `client.images.generate()` for images, `client.embeddings.create()` for embeddings. Use `response_format: { type: "json_schema" }` with Zod-generated schemas for structured output. Function calling uses the same `tools` parameter shape as OpenAI. You can also use the OpenAI SDK directly by pointing `baseURL` to `https://api.together.xyz/v1`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `together-ai` package (`import Together from "together-ai"`) -- NOT the OpenAI SDK -- unless explicitly building an OpenAI-compatible integration)**

**(You MUST include the JSON schema in BOTH the `response_format` parameter AND the system prompt when using structured output -- the model needs both)**

**(You MUST handle errors using `Together.APIError` and its subclasses -- never use bare catch blocks without error type checking)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.TOGETHER_API_KEY`)**

</critical_requirements>

---

**Auto-detection:** Together AI, together-ai, together.ai, TOGETHER_API_KEY, client.chat.completions (together), client.images.generate, client.embeddings.create (together), Llama-3, Qwen3, Mistral, DeepSeek, FLUX, together.images, together.chat, together.embeddings, together.fineTuning, api.together.xyz

**When to use:**

- Running open-source LLMs (Llama, Qwen, Mistral, DeepSeek) via serverless inference
- Generating images with FLUX or Stable Diffusion models
- Creating embeddings for RAG pipelines with open-source embedding models
- Using function calling / tool use with open-source models
- Extracting structured JSON output from LLM responses
- Fine-tuning open-source models on custom data
- Migrating from OpenAI to open-source models with minimal code changes

**Key patterns covered:**

- Client initialization and configuration (retries, timeouts, logging)
- Chat completions with open-source models (Llama, Qwen, Mistral, DeepSeek)
- Streaming with `stream: true` and `for await...of`
- Structured output with `response_format: { type: "json_schema" }` and Zod
- Function calling / tool use with `tools` parameter
- Image generation with FLUX and Stable Diffusion models
- Embeddings API with open-source embedding models
- Fine-tuning API (file upload, job creation, monitoring)
- OpenAI SDK compatibility (base URL swap)
- Error handling, retries, timeouts

**When NOT to use:**

- You need OpenAI-specific features (Responses API, Batch API, Realtime API) -- use the OpenAI SDK directly
- You want React-specific chat UI hooks -- use a framework-integrated AI SDK
- You only use OpenAI models and never plan to use open-source models

---

## Examples Index

- [Core: Setup & Configuration](examples/core.md) -- Client init, production config, error handling, OpenAI compatibility
- [Chat Completions](examples/chat.md) -- Basic chat, multi-turn, model selection, vision
- [Streaming](examples/streaming.md) -- Async iteration, stream cancellation
- [Tool/Function Calling](examples/tools.md) -- Tool definitions, multi-step tool loops
- [Structured Output](examples/structured-output.md) -- JSON mode, Zod schemas, regex mode
- [Images & Embeddings](examples/images.md) -- FLUX image generation, embedding models, semantic search
- [Quick API Reference](reference.md) -- Model IDs, method signatures, error types

---

<philosophy>

## Philosophy

Together AI provides **fast serverless inference for open-source models**. The TypeScript SDK (`together-ai`) is auto-generated with Stainless and mirrors the OpenAI API shape, making migration straightforward.

**Core principles:**

1. **OpenAI-compatible API shape** -- Same `client.chat.completions.create()` pattern, same `messages` array, same `tools` parameter. Switching from OpenAI is often just changing the import and model name.
2. **Open-source model access** -- Run Llama, Qwen, Mistral, DeepSeek, and 200+ other models without managing infrastructure. Models are identified by their Hugging Face-style IDs (e.g., `meta-llama/Llama-3.3-70B-Instruct-Turbo`).
3. **Multi-modal support** -- Chat completions, image generation (FLUX, Stable Diffusion), embeddings, audio, and video -- all through one SDK.
4. **Structured output via JSON Schema** -- Pass a JSON schema in `response_format` and include it in the system prompt. Use Zod's `z.toJSONSchema()` to generate schemas from TypeScript types.
5. **Fine-tuning open-source models** -- Upload JSONL data, create LoRA or full fine-tuning jobs, and deploy custom models -- all via the API.

**When to use Together AI:**

- You want to use open-source models with fast serverless inference
- You need cost-effective inference (often cheaper than proprietary APIs)
- You want to fine-tune open-source models on your data
- You need image generation with FLUX models
- You want OpenAI API compatibility for easy migration

**When NOT to use:**

- You need OpenAI-specific features (Responses API, Batch API, Realtime) -- use the OpenAI SDK
- You need Anthropic or Google-specific features -- use their respective SDKs
- You want a provider-agnostic SDK -- use a unified provider framework

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize the Together client. It reads `TOGETHER_API_KEY` from the environment.

```typescript
// lib/together.ts -- basic setup
import Together from "together-ai";
const client = new Together();
export { client };
```

```typescript
// lib/together.ts -- production configuration
const TIMEOUT_MS = 30_000;
const MAX_RETRIES = 3;

const client = new Together({
  apiKey: process.env.TOGETHER_API_KEY,
  timeout: TIMEOUT_MS,
  maxRetries: MAX_RETRIES,
});
export { client };
```

**Why good:** Minimal setup, env var auto-detected, named constants for production settings

```typescript
// BAD: Hardcoded API key
const client = new Together({
  apiKey: "sk-abc123...",
});
```

**Why bad:** Hardcoded keys get leaked in version control, security breach risk

**See:** [examples/core.md](examples/core.md) for error handling, OpenAI compatibility, per-request overrides

---

### Pattern 2: Chat Completions

Stateless text generation with open-source models.

```typescript
const completion = await client.chat.completions.create({
  model: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
  messages: [
    { role: "system", content: "You are a helpful coding assistant." },
    { role: "user", content: "Explain TypeScript generics." },
  ],
});
console.log(completion.choices[0].message.content);
```

**Why good:** Clear message roles, system message for behavior control, direct content access

```typescript
// BAD: No system message, no model specified
const res = await client.chat.completions.create({
  messages: [{ role: "user", content: "do something" }],
});
```

**Why bad:** Missing `model` field will error, no system instruction means unpredictable behavior

**See:** [examples/chat.md](examples/chat.md) for multi-turn, vision models, model selection guide

---

### Pattern 3: Streaming

Use streaming for user-facing responses.

```typescript
const stream = await client.chat.completions.create({
  model: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
  messages: [{ role: "user", content: "Explain async/await." }],
  stream: true,
});
for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content;
  if (content) process.stdout.write(content);
}
```

**Why good:** Progressive output for better UX, standard async iterator pattern

```typescript
// BAD: Not consuming the stream
const stream = await client.chat.completions.create({
  model: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
  messages: [{ role: "user", content: "Hello" }],
  stream: true,
});
// Stream never consumed -- tokens are lost
```

**Why bad:** Stream must be consumed via iteration, otherwise tokens are silently lost

**See:** [examples/streaming.md](examples/streaming.md) for stream cancellation, controller access

---

### Pattern 4: Structured Output with JSON Schema

Use `response_format: { type: "json_schema" }` with Zod-generated schemas.

```typescript
import Together from "together-ai";
import { z } from "zod";

const client = new Together();

const EventSchema = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const jsonSchema = z.toJSONSchema(EventSchema);

const completion = await client.chat.completions.create({
  model: "Qwen/Qwen3.5-9B",
  messages: [
    {
      role: "system",
      content: `Extract event details. Only answer in JSON. Follow this schema: ${JSON.stringify(jsonSchema)}`,
    },
    { role: "user", content: "Alice and Bob meet next Tuesday for lunch." },
  ],
  response_format: {
    type: "json_schema",
    json_schema: { name: "calendar_event", schema: jsonSchema },
  },
});

const event = JSON.parse(completion.choices[0].message.content ?? "{}");
```

**Why good:** Zod generates schema, schema included in both system prompt and `response_format`, named schema object

```typescript
// BAD: Schema only in response_format, not in system prompt
const completion = await client.chat.completions.create({
  model: "Qwen/Qwen3.5-9B",
  messages: [{ role: "user", content: "Extract event details." }],
  response_format: {
    type: "json_schema",
    json_schema: { name: "event", schema: jsonSchema },
  },
});
```

**Why bad:** Model needs the schema in the system prompt AND `response_format` for reliable structured output -- omitting the prompt instruction degrades output quality

**See:** [examples/structured-output.md](examples/structured-output.md) for regex mode, vision with JSON, complex schemas

---

### Pattern 5: Function Calling / Tool Use

Define functions the model can call. Same `tools` parameter shape as OpenAI.

```typescript
const completion = await client.chat.completions.create({
  model: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
  messages: [{ role: "user", content: "Weather in Paris?" }],
  tools: [
    {
      type: "function",
      function: {
        name: "get_weather",
        description: "Get current weather for a location",
        parameters: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" },
          },
          required: ["location"],
          additionalProperties: false,
        },
        strict: true,
      },
    },
  ],
});

const toolCall = completion.choices[0].message.tool_calls?.[0];
if (toolCall) {
  const args = JSON.parse(toolCall.function.arguments);
  console.log(`Call ${toolCall.function.name} with:`, args);
}
```

**Why good:** Standard OpenAI-compatible tool format, strict mode for reliable arguments, `additionalProperties: false` prevents hallucinated fields

**See:** [examples/tools.md](examples/tools.md) for multi-step tool loops, `tool_choice`, parallel calls, supported models

---

### Pattern 6: Image Generation

Generate images with FLUX and Stable Diffusion models.

```typescript
const response = await client.images.generate({
  model: "black-forest-labs/FLUX.1-schnell",
  prompt: "A serene mountain landscape at sunset with a lake reflection",
  steps: 4,
});
console.log(response.data[0].url);
```

**Why good:** Simple API, model-specific parameters, URL response by default

**See:** [examples/images.md](examples/images.md) for FLUX variants, base64, reference images, multiple variations

---

### Pattern 7: Embeddings

Create embeddings for semantic search and RAG pipelines.

```typescript
const EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5";

const response = await client.embeddings.create({
  model: EMBEDDING_MODEL,
  input: "TypeScript provides static type checking.",
});
console.log(response.data[0].embedding);
```

**Why good:** Named model constant, simple single-input embedding, array response

**See:** [examples/images.md](examples/images.md) for batch embeddings, semantic search with cosine similarity

---

### Pattern 8: Error Handling

Always catch `Together.APIError` and its subclasses.

```typescript
try {
  const completion = await client.chat.completions.create({
    model: "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages: [{ role: "user", content: "Hello" }],
  });
} catch (error) {
  if (error instanceof Together.APIError) {
    console.error(`API Error [${error.status}]: ${error.message}`);
    if (error instanceof Together.RateLimitError) {
      console.error("Rate limited -- SDK will auto-retry.");
    }
    if (error instanceof Together.AuthenticationError) {
      throw new Error("Invalid API key. Check TOGETHER_API_KEY.");
    }
  } else {
    throw error; // Re-throw non-API errors
  }
}
```

**Why good:** Specific error types, re-throws unexpected errors, actionable error messages

**See:** [examples/core.md](examples/core.md) for full production error handling, error type hierarchy

</patterns>

---

<performance>

## Performance Optimization

### Model Selection for Cost/Speed

```
Fast + cheap              -> Llama 3.3 70B Turbo, Qwen3.5 9B
Most capable              -> DeepSeek V3.1, Qwen3.5 397B
Complex reasoning         -> DeepSeek R1
Function calling          -> Llama 3.3 70B, Qwen3.5 9B, DeepSeek V3
Structured output (JSON)  -> Qwen3.5 9B, Llama 3.3 70B
Embeddings                -> BAAI/bge-large-en-v1.5 (quality), UAE-Large-V1
Image generation (fast)   -> FLUX.1 schnell (4 steps)
Image generation (quality)-> FLUX.2 pro, FLUX.1.1 pro
Vision / multimodal       -> Qwen3-VL-8B-Instruct, Llama 3.2 Vision
```

### Key Optimization Patterns

- **Use Turbo variants** for chat models -- they are optimized for Together's infrastructure
- **Set `temperature: 0`** for deterministic output when possible
- **Batch embedding inputs** -- pass an array of strings to `client.embeddings.create()` instead of one at a time
- **Use `steps: 4`** for FLUX.1 schnell images (higher steps have diminishing returns)
- **Use streaming** for user-facing responses to reduce perceived latency

</performance>

---

<decision_framework>

## Decision Framework

### Which Model to Choose

```
What is your task?
+-- General chat / instruction following -> Llama 3.3 70B Turbo (fast, cheap)
+-- Most capable reasoning -> DeepSeek V3.1, Qwen3.5 397B
+-- Complex math / chain-of-thought -> DeepSeek R1
+-- Function calling / tool use -> Llama 3.3 70B, Qwen3.5 9B
+-- Structured JSON output -> Qwen3.5 9B (best JSON mode support)
+-- Vision / image understanding -> Qwen3-VL-8B-Instruct
+-- Code generation -> DeepSeek V3, Qwen Coder
+-- Embeddings -> BAAI/bge-large-en-v1.5 (default)
+-- Image generation (fast) -> FLUX.1 schnell
+-- Image generation (quality) -> FLUX.2 pro, FLUX.1.1 pro
```

### Together AI SDK vs OpenAI SDK

```
Do you ONLY use Together AI models?
+-- YES -> Use together-ai package (purpose-built, full API coverage)
+-- NO -> Do you also use OpenAI models?
    +-- YES -> Two options:
    |   +-- Separate SDKs: together-ai for Together, openai for OpenAI
    |   +-- OpenAI SDK only: Point baseURL to api.together.xyz/v1
    +-- NO -> Use a provider-agnostic SDK
```

### Streaming vs Non-Streaming

```
Is the response user-facing?
+-- YES -> Use streaming (stream: true)
+-- NO -> Use non-streaming
    +-- Background processing -> client.chat.completions.create()
    +-- Structured output -> Non-streaming with response_format
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Hardcoding `TOGETHER_API_KEY` instead of using environment variables (security breach risk)
- Using bare `catch` blocks without checking `Together.APIError` (hides API errors)
- Not consuming streams returned by `stream: true` (tokens are silently lost)
- Using `JSON.parse()` on completion content without `response_format` (fragile, model may return non-JSON)
- Omitting the schema from the system prompt when using `response_format: { type: "json_schema" }` (degrades output quality)

**Medium Priority Issues:**

- Not setting `maxRetries` / `timeout` for production deployments (default timeout is 1 minute)
- Missing `system` role message (no system instruction means unpredictable behavior)
- Using a model that does not support function calling with `tools` parameter (will silently fail or error)
- Not checking if `tool_calls` is defined before accessing arguments
- Using `width`/`height` with FLUX schnell/Kontext models (use `aspect_ratio` instead)

**Common Mistakes:**

- Using OpenAI model names (e.g., `gpt-4o`) with the Together AI SDK -- Together uses Hugging Face-style IDs like `meta-llama/Llama-3.3-70B-Instruct-Turbo`
- Confusing `client.images.generate()` (Together) with `client.images.create()` (OpenAI) -- different method name
- Forgetting to use `z.toJSONSchema()` (Zod v4) or `zodToJsonSchema()` (Zod v3) to convert schemas before passing to `response_format`
- Using the `developer` role (OpenAI-specific) instead of `system` role with Together AI models
- Passing `max_completion_tokens` instead of `max_tokens` -- Together uses `max_tokens`

**Gotchas & Edge Cases:**

- The SDK auto-retries on 429 (rate limit), 408, 409, and 5xx errors -- 2 retries by default. Disable with `maxRetries: 0`.
- Model IDs are case-sensitive and follow the `org/model-name` format from Hugging Face.
- Not all models support function calling. See [examples/tools.md](examples/tools.md) for the current supported list, or check the [official docs](https://docs.together.ai/docs/function-calling).
- FLUX.1 schnell and Kontext models use `aspect_ratio` parameter; FLUX.1 Pro and FLUX.1.1 Pro use `width`/`height`.
- Image generation returns URLs by default. Use `response_format: "base64"` for inline data.
- The `response_format: { type: "json_schema" }` requires telling the model to "only answer in JSON" in the system prompt -- the schema alone is not sufficient.
- Structured output uses `z.toJSONSchema()` (Zod v4) -- if using Zod v3, use `zodToJsonSchema()` from the `zod-to-json-schema` package.
- Together AI's `client.images.generate()` is the method name, not `client.images.create()` like OpenAI.
- Fine-tuning supports LoRA and full fine-tuning. File format is JSONL with `messages` array per line.
- The OpenAI compatibility endpoint (`api.together.xyz/v1`) supports chat, embeddings, images, vision, function calling, and structured output -- but not fine-tuning or model management.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the `together-ai` package (`import Together from "together-ai"`) -- NOT the OpenAI SDK -- unless explicitly building an OpenAI-compatible integration)**

**(You MUST include the JSON schema in BOTH the `response_format` parameter AND the system prompt when using structured output -- the model needs both)**

**(You MUST handle errors using `Together.APIError` and its subclasses -- never use bare catch blocks without error type checking)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.TOGETHER_API_KEY`)**

**Failure to follow these rules will produce insecure, unreliable, or incorrectly structured AI integrations.**

</critical_reminders>
