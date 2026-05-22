---
name: api-ai-openai-sdk
description: Official OpenAI SDK patterns for TypeScript/Node.js — client setup, Chat Completions, Responses API, streaming, structured outputs, function calling, embeddings, vision, audio, and production best practices
---

# OpenAI SDK Patterns

> **Quick Guide:** Use the official `openai` npm package (v6+) to interact with OpenAI's API directly. Use `client.responses.create()` (Responses API) for new projects with built-in tools and server-side state, or `client.chat.completions.create()` (Chat Completions) for stateless chat flows. Use `zodResponseFormat` and `client.chat.completions.parse()` for structured outputs. Use `.stream()` or `stream: true` for streaming. Supports GPT-5.x family, GPT-4o, o4-mini, embeddings, vision, audio, and batch processing.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the Responses API (`client.responses.create()`) for new projects -- it provides better performance, built-in tools, and server-side conversation state)**

**(You MUST use `zodResponseFormat()` from `openai/helpers/zod` for structured outputs -- do NOT manually construct JSON schemas)**

**(You MUST handle errors using `OpenAI.APIError` and its subclasses -- never use bare catch blocks without error type checking)**

**(You MUST configure appropriate retries and timeouts for production use -- the SDK retries 2 times by default on 429/5xx errors)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.OPENAI_API_KEY`)**

</critical_requirements>

---

**Auto-detection:** OpenAI, openai, client.chat.completions, client.responses.create, client.embeddings, client.audio, zodResponseFormat, zodTextFormat, zodFunction, runTools, GPT-5, GPT-4o, o4-mini, gpt-5-mini, text-embedding-3, whisper, tts, OPENAI_API_KEY, toFile

**When to use:**

- Building applications that call OpenAI models directly (GPT-5.x, GPT-4o, o4-mini, etc.)
- Implementing chat completions with streaming responses
- Using the Responses API for agentic workflows with built-in tools (web search, file search, code interpreter)
- Extracting structured data from LLM responses with Zod schema validation
- Implementing function calling / tool use with the Chat Completions or Responses API
- Creating embeddings for RAG pipelines or semantic search
- Processing images with vision models or audio with Whisper/TTS
- Running batch jobs for high-volume, cost-efficient processing

**Key patterns covered:**

- Client initialization and configuration (retries, timeouts, proxies)
- Chat Completions API (messages, streaming, function calling)
- Responses API (input, instructions, built-in tools, server-side state)
- Structured outputs with `zodResponseFormat` and `client.chat.completions.parse()`
- Streaming with `for await...of`, `.stream()` helper, and event handling
- Embeddings API (`text-embedding-3-small`, `text-embedding-3-large`)
- Vision (image URLs, base64), Audio (Whisper transcription, TTS), Batch API
- Error handling, retries, timeouts, and production best practices

**When NOT to use:**

- Multi-provider applications where you need to switch between OpenAI, Anthropic, Google, etc. -- use a unified provider SDK instead
- React-specific chat UI hooks (`useChat`, `useCompletion`) -- use a framework-integrated AI SDK
- When you need a higher-level abstraction over multiple LLM providers

---

## Examples Index

- [Core: Setup & Configuration](examples/core.md) -- Client init, production config, Azure, error handling, request overrides
- [Chat Completions](examples/chat.md) -- Basic chat, multi-turn, token tracking, output length control
- [Streaming](examples/streaming.md) -- `stream: true`, `.stream()` helper, Responses API streaming, abort
- [Tool/Function Calling](examples/tools.md) -- Manual tools, `zodFunction`, `runTools` automation, Responses API tools
- [Structured Output](examples/structured-output.md) -- `zodResponseFormat`, `zodTextFormat`, refusal handling
- [Embeddings, Vision & Audio](examples/embeddings-vision-audio.md) -- Semantic search, image analysis, transcription, TTS, batch processing
- [Quick API Reference](reference.md) -- Model IDs, method signatures, error types, streaming events

---

<philosophy>

## Philosophy

The official OpenAI SDK provides **direct, low-level access** to OpenAI's full API surface. It is the thinnest possible wrapper over the REST API, auto-generated from OpenAI's OpenAPI specification using Stainless.

**Core principles:**

1. **Direct API access** -- No abstractions or provider layers. You get the exact API that OpenAI documents, with full TypeScript types. Every API feature is available immediately when OpenAI releases it.
2. **Two API paradigms** -- The **Responses API** (`client.responses.create()`) is the newer, recommended API with built-in tools and server-side state. The **Chat Completions API** (`client.chat.completions.create()`) remains fully supported for stateless chat flows.
3. **Built-in resilience** -- The SDK handles retries (2 by default on 429/5xx), timeouts (10 min default), and auto-pagination out of the box.
4. **Streaming as a first-class pattern** -- Use `stream: true` for SSE-based streaming, `.stream()` helper for event-based consumption, or `for await...of` for simple iteration.
5. **Type-safe structured outputs** -- `zodResponseFormat()` and `client.chat.completions.parse()` convert Zod schemas to JSON Schema and parse responses, giving you validated, typed objects.

**When to use the OpenAI SDK directly:**

- You only use OpenAI models and want the simplest, most direct integration
- You need access to OpenAI-specific features (Responses API, Batch, Realtime)
- You want minimal dependencies and zero abstraction overhead
- You need the latest API features on day one

**When NOT to use:**

- You need to switch between providers (OpenAI, Anthropic, Google) -- use a unified provider SDK
- You want React-specific chat UI hooks -- use a framework-integrated AI SDK
- You want a higher-level agent framework -- consider OpenAI Agents SDK (`@openai/agents`)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize the OpenAI client. It auto-reads `OPENAI_API_KEY` from the environment.

```typescript
// lib/openai.ts -- basic setup
import OpenAI from "openai";
const client = new OpenAI();
export { client };
```

```typescript
// lib/openai.ts -- production configuration
const TIMEOUT_MS = 30_000;
const MAX_RETRIES = 3;
const client = new OpenAI({ timeout: TIMEOUT_MS, maxRetries: MAX_RETRIES });
```

**Why good:** Minimal setup, env var auto-detected, named constants for production settings

**See:** [examples/core.md](examples/core.md) for Azure OpenAI, per-request overrides, error handling patterns

---

### Pattern 2: Chat Completions API

Stateless text generation. You manage conversation history.

```typescript
const completion = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "developer", content: "You are a helpful coding assistant." },
    { role: "user", content: "Explain TypeScript generics." },
  ],
});
console.log(completion.choices[0].message.content);
```

**Why good:** Clear message roles, `developer` message for system instructions, direct content access

```typescript
// BAD: No developer message, no error handling
const res = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "do something" }],
});
```

**Why bad:** No system instruction means unpredictable behavior, vague prompt

**See:** [examples/chat.md](examples/chat.md) for multi-turn, token tracking, output length control

---

### Pattern 3: Responses API (Recommended for New Projects)

Newer API with built-in tools, server-side state, and better performance with reasoning models.

```typescript
const response = await client.responses.create({
  model: "gpt-4o",
  instructions: "You are a coding assistant.",
  input: "What are TypeScript generics?",
});
console.log(response.output_text);
```

**Why good:** Clean separation of instructions and input, `output_text` helper, simpler than messages array

```typescript
// BAD: Using Chat Completions parameters with Responses API
const response = await client.responses.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello" }], // WRONG: use 'input'
});
```

**Why bad:** Responses API uses `input` and `instructions`, not `messages`

#### Built-in Tools

Web search (`{ type: "web_search_preview" }`), file search (`{ type: "file_search" }`), code interpreter (`{ type: "code_interpreter" }`). Chain conversations with `previous_response_id` and `store: true`.

**See:** [examples/tools.md](examples/tools.md) for Responses API function calling with tool outputs

---

### Pattern 4: Streaming

Use streaming for user-facing responses.

```typescript
// Chat Completions -- stream: true with for-await
const stream = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Explain async/await." }],
  stream: true,
});
for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content;
  if (content) process.stdout.write(content);
}
```

```typescript
// Event-based with .stream() helper
const stream = client.chat.completions.stream({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Tell me a story." }],
});
stream.on("content", (delta) => process.stdout.write(delta));
const finalContent = await stream.finalContent();
```

**Why good:** Progressive output for better UX, event-based API for granular control

```typescript
// BAD: Not consuming the stream
const stream = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello" }],
  stream: true,
});
// Stream never consumed -- tokens are lost
```

**Why bad:** Stream must be consumed via iteration or event handlers, otherwise tokens are lost

**See:** [examples/streaming.md](examples/streaming.md) for Responses API streaming, abort, stream methods

---

### Pattern 5: Structured Outputs with Zod

Use `zodResponseFormat()` and `.parse()` for type-safe structured responses.

```typescript
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod";

const CalendarEvent = z.object({
  name: z.string(),
  date: z.string(),
  participants: z.array(z.string()),
});

const completion = await client.chat.completions.parse({
  model: "gpt-4o",
  messages: [
    { role: "developer", content: "Extract event details." },
    { role: "user", content: "Alice and Bob meet next Tuesday for lunch." },
  ],
  response_format: zodResponseFormat(CalendarEvent, "calendar_event"),
});

const event = completion.choices[0].message.parsed; // Fully typed
```

**Why good:** Auto-converts schema, validates output, fully typed result, handles refusals

**See:** [examples/structured-output.md](examples/structured-output.md) for Responses API (`zodTextFormat`), refusal handling, complex schemas

---

### Pattern 6: Function Calling / Tool Use

Define functions the model can call. Use `zodFunction()` for type-safe definitions.

```typescript
import { zodFunction } from "openai/helpers/zod";
import { z } from "zod";

const GetWeatherParams = z.object({
  location: z.string().describe("City name"),
  unit: z.enum(["celsius", "fahrenheit"]).default("celsius"),
});

const completion = await client.chat.completions.parse({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Weather in Paris?" }],
  tools: [zodFunction({ name: "get_weather", parameters: GetWeatherParams })],
});

const toolCall = completion.choices[0].message.tool_calls?.[0];
if (toolCall?.type === "function") {
  console.log(toolCall.function.parsed_arguments); // Typed from Zod
}
```

**Why good:** `zodFunction` provides type-safe argument parsing, `.describe()` guides the model

Use `runTools()` for automated tool execution loops that handle the call-respond cycle automatically.

**See:** [examples/tools.md](examples/tools.md) for `runTools`, manual tool definitions, Responses API function calling

---

### Pattern 7: Embeddings, Vision & Audio

- **Embeddings:** `client.embeddings.create({ model: "text-embedding-3-small", input: [...] })` -- batch multiple inputs in one call
- **Vision:** Multi-part content array with `{ type: "image_url", image_url: { url } }` for URL or base64 images
- **Audio:** `client.audio.transcriptions.create()` for speech-to-text, `client.audio.speech.create()` for TTS
- **Files:** `client.files.create()` with `ReadStream`, `Buffer` (via `toFile`), or `fetch()` Response
- **Batch API:** Upload JSONL, create batch with `client.batches.create()`, poll for completion at 50% cost

**See:** [examples/embeddings-vision-audio.md](examples/embeddings-vision-audio.md) for full examples with cosine similarity, base64 images, timestamps, TTS voice instructions, batch processing

---

### Pattern 8: Error Handling

Always catch `OpenAI.APIError` and its subclasses. Re-throw unexpected errors.

```typescript
try {
  const completion = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Hello" }],
  });
} catch (error) {
  if (error instanceof OpenAI.APIError) {
    console.error(
      `API Error [${error.status}]: ${error.message} (${error.request_id})`,
    );
    // Check subclasses: RateLimitError, AuthenticationError, BadRequestError, etc.
  } else {
    throw error; // Re-throw non-API errors
  }
}
```

**Why good:** Specific error types with status codes, request ID for debugging, re-throws unexpected errors

**See:** [examples/core.md](examples/core.md) for full production error handling, stream errors, error type hierarchy

</patterns>

---

<performance>

## Performance Optimization

### Model Selection for Cost/Speed

```
General purpose             -> gpt-5.4 (most capable) or gpt-4o (proven, lower cost)
Cost-sensitive / high-vol   -> gpt-5-mini or gpt-5-nano (cheapest)
Complex reasoning           -> gpt-5.4 or o4-mini
Structured output           -> gpt-5.4 or gpt-4o (best schema adherence)
Embeddings                  -> text-embedding-3-small (cheapest) or text-embedding-3-large (highest quality)
Transcription               -> whisper-1 or gpt-4o-transcribe (higher accuracy)
TTS                         -> tts-1 (fast) or tts-1-hd (quality) or gpt-4o-mini-tts (voice control)
Batch processing            -> gpt-5-mini at 50% batch discount
```

### Key Optimization Patterns

- **Track token usage** via `completion.usage` for cost visibility
- **Check `finish_reason === "length"`** to detect truncated output
- **Use `temperature: 0`** for deterministic output (enables caching)
- **Use `AbortController`** to cancel long-running requests
- **Use Batch API** for high-volume jobs at 50% cost reduction

</performance>

---

<decision_framework>

## Decision Framework

### Which API to Use

```
Building a new application?
+-- YES -> Need built-in tools (web search, file search, code interpreter)?
|   +-- YES -> Use Responses API (client.responses.create())
|   +-- NO -> Need server-side conversation state?
|       +-- YES -> Use Responses API with store: true
|       +-- NO -> Either API works, prefer Responses for new code
+-- Existing Chat Completions code?
    +-- Working fine? -> Keep using Chat Completions (fully supported)
    +-- Need new features? -> Consider migrating to Responses API
```

### Which Model to Choose

```
What is your task?
+-- General text generation -> gpt-5.4 (most capable) or gpt-4o (lower cost)
+-- Fast + cheap simple tasks -> gpt-5-mini or gpt-5-nano
+-- Complex reasoning / math -> gpt-5.4 or o4-mini
+-- Structured output -> gpt-5.4 or gpt-4o (best schema adherence)
+-- Vision (images) -> gpt-5.4 or gpt-4o
+-- Embeddings -> text-embedding-3-small (default) or text-embedding-3-large
+-- Transcription -> whisper-1 or gpt-4o-transcribe
+-- Text-to-speech -> tts-1 (fast) or gpt-4o-mini-tts (voice instructions)
+-- Batch processing -> gpt-5-mini (cheapest at 50% batch discount)
```

### Streaming vs Non-Streaming

```
Is the response user-facing?
+-- YES -> Use streaming (stream: true or .stream())
|   +-- Need event-level control? -> .stream() with event handlers
|   +-- Simple text output? -> stream: true with for await
+-- NO -> Use non-streaming
    +-- Background processing -> client.chat.completions.create()
    +-- Structured output -> client.chat.completions.parse()
    +-- High volume -> Batch API
```

### When to Use This SDK vs a Provider-Agnostic SDK

```
Do you need multiple LLM providers (OpenAI + others)?
+-- YES -> Not this skill's scope -- use a unified provider SDK
+-- NO -> Do you need OpenAI-specific features?
    +-- YES -> Use OpenAI SDK directly
    |   Examples: Responses API, Batch API,
    |   Realtime API, built-in web search/file search
    +-- NO -> OpenAI SDK is simplest for OpenAI-only use
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Hardcoding API keys instead of using environment variables (security breach risk)
- Using bare `catch` blocks without checking `OpenAI.APIError` (hides API errors)
- Not consuming streams returned by `stream: true` (tokens are silently lost)
- Using `JSON.parse()` on completion content without `zodResponseFormat` (fragile, no validation)
- Sending full conversation history every request when Responses API's `previous_response_id` could manage state

**Medium Priority Issues:**

- Not setting `maxRetries` / `timeout` for production deployments (10 min default timeout may be too long)
- Missing `developer` role message (no system instruction = unpredictable output style)
- Using deprecated `system` role instead of `developer` role in Chat Completions
- Not checking `finish_reason` for `'length'` truncation
- Ignoring `usage` data (no cost visibility)

**Common Mistakes:**

- Confusing Responses API (`client.responses.create()`) with Chat Completions (`client.chat.completions.create()`) parameters -- they use different shapes
- Using `messages` parameter with Responses API (it uses `input` and `instructions`)
- Using `response_format` with models that don't support structured outputs (need gpt-4o or later)
- Using `max_tokens` with reasoning models (o4-mini, gpt-5.x) -- use `max_completion_tokens` instead
- Not handling the case where `completion.choices[0].message.tool_calls` is undefined
- Forgetting that `runTools()` defaults to max 10 completions -- set `maxChatCompletions` explicitly

**Gotchas & Edge Cases:**

- The SDK auto-retries on 429 (rate limit) and 5xx errors -- 2 retries by default. Disable with `maxRetries: 0` if you handle retries yourself.
- `stream: true` returns raw SSE chunks. Use `.stream()` helper for a nicer event-based API.
- `client.chat.completions.parse()` throws `LengthFinishReasonError` if `finish_reason` is `'length'` and `ContentFilterFinishReasonError` if `'content_filter'`.
- Embedding responses return `Float64Array` typed arrays -- convert to regular arrays with `Array.from()` if needed.
- File uploads support `ReadStream`, `File`, `fetch()` Response, and `toFile()` helper -- use whichever matches your data source.
- The Responses API's `store: true` enables server-side state but also means OpenAI stores your conversations. Set `store: false` for sensitive data.
- `developer` role replaces `system` role in newer models (gpt-4o and later).
- Batch API has a 24h completion window and 50,000 request limit per batch.
- Audio transcription has a 25 MB file size limit.
- Zod schemas with `zodResponseFormat` must use `additionalProperties: false` -- the SDK handles this automatically.
- `zodTextFormat` and `zodResponseFormat` are NOT compatible with Zod v4 -- use Zod v3.x until the SDK adds v4 support.
- The Assistants API is deprecated (sunset August 2026) -- use the Responses API for new code.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the Responses API (`client.responses.create()`) for new projects -- it provides better performance, built-in tools, and server-side conversation state)**

**(You MUST use `zodResponseFormat()` from `openai/helpers/zod` for structured outputs -- do NOT manually construct JSON schemas)**

**(You MUST handle errors using `OpenAI.APIError` and its subclasses -- never use bare catch blocks without error type checking)**

**(You MUST configure appropriate retries and timeouts for production use -- the SDK retries 2 times by default on 429/5xx errors)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.OPENAI_API_KEY`)**

**Failure to follow these rules will produce insecure, unreliable, or poorly-typed AI integrations.**

</critical_reminders>
