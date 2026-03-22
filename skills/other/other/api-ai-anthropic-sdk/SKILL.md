---
name: api-ai-anthropic-sdk
description: Official Anthropic SDK patterns for TypeScript/Node.js — client setup, Messages API, streaming, tool use, vision, extended thinking, structured outputs, prompt caching, batch API, and production best practices
---

# Anthropic SDK Patterns

> **Quick Guide:** Use the official `@anthropic-ai/sdk` package to interact with Claude models directly. Use `client.messages.create()` for single-turn and multi-turn conversations. Use `client.messages.stream()` for streaming with event-based consumption. `max_tokens` is always required. Content blocks are typed unions (`text`, `tool_use`, `thinking`). Use `client.messages.parse()` with `zodOutputFormat()` for structured outputs. Tool use requires a tool-result loop -- Claude returns `tool_use` blocks, you execute the tool and send back `tool_result` blocks. Extended thinking adds `thinking` content blocks before the response.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST always provide `max_tokens` in every `messages.create()` / `messages.stream()` call -- it is required and has no default)**

**(You MUST handle the `stop_reason` field to detect `end_turn`, `max_tokens`, `tool_use`, and `stop_sequence` -- ignoring it causes silent truncation or broken tool loops)**

**(You MUST iterate over `response.content` blocks (not assume a single text block) -- responses can contain `text`, `tool_use`, and `thinking` blocks mixed together)**

**(You MUST handle errors using `Anthropic.APIError` and its subclasses -- never use bare catch blocks without error type checking)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.ANTHROPIC_API_KEY`)**

</critical_requirements>

---

**Auto-detection:** Anthropic, @anthropic-ai/sdk, client.messages.create, client.messages.stream, client.messages.parse, client.messages.countTokens, client.messages.batches, ANTHROPIC_API_KEY, claude-sonnet, claude-opus, claude-haiku, ContentBlock, ToolUseBlock, tool_use, tool_result, thinking, budget_tokens, adaptive, cache_control, zodOutputFormat, betaZodTool, toolRunner

**When to use:**

- Building applications that call Claude models directly (Opus, Sonnet, Haiku families)
- Implementing streaming chat responses with event-based text accumulation
- Using tool use / function calling where Claude decides which tools to invoke
- Processing images, PDFs, or documents alongside text prompts
- Enabling extended thinking for complex reasoning tasks
- Extracting structured data from responses with Zod schema validation
- Caching large system prompts or conversation prefixes for cost savings
- Running batch jobs for high-volume, asynchronous processing
- Counting tokens before sending requests for cost estimation

**Key patterns covered:**

- Client initialization and configuration (retries, timeouts, API key)
- Messages API (`messages.create`, system prompts, multi-turn conversations)
- Streaming with `.stream()` helper and `stream: true` low-level SSE
- Tool use / function calling (tools array, `tool_use` / `tool_result` content blocks)
- Vision (base64 images, URL images, PDFs/documents)
- Extended thinking (`thinking` config, `budget_tokens`, thinking content blocks)
- Structured outputs (`zodOutputFormat`, `messages.parse`, `output_config`)
- Prompt caching (`cache_control: { type: "ephemeral" }`)
- Batch API (`messages.batches.create`)
- Token counting (`messages.countTokens`)
- Error handling, retries, and production best practices

**When NOT to use:**

- Multi-provider applications where you need to switch between multiple LLM providers -- use a unified provider SDK instead
- React-specific chat UI hooks (`useChat`, `useCompletion`) -- use a framework-integrated AI SDK
- When you need a higher-level agent framework -- consider the Claude Agent SDK (`@anthropic-ai/claude-agent-sdk`)

---

## Examples Index

- [Core: Setup & Configuration](examples/core.md) -- Client init, production config, error handling, token counting
- [Streaming](examples/streaming.md) -- `.stream()` helper, `stream: true` SSE, event types, abort
- [Tool Use / Function Calling](examples/tool-use.md) -- Tool definitions, tool loops, parallel tool calls, automated tool runner
- [Vision & Documents](examples/vision-documents.md) -- Base64 images, URL images, PDFs, multi-modal
- [Extended Thinking](examples/extended-thinking.md) -- Thinking config, streaming thinking, thinking with tool use
- [Quick API Reference](reference.md) -- Model IDs, method signatures, error types, streaming events, content block types

---

<philosophy>

## Philosophy

The official Anthropic SDK provides **direct, typed access** to the Claude API. It is auto-generated from Anthropic's API specification using Stainless, giving you the exact API surface that Anthropic documents with full TypeScript types.

**Core principles:**

1. **Content blocks, not strings** -- Responses are arrays of typed content blocks (`TextBlock`, `ToolUseBlock`, `ThinkingBlock`), not plain strings. Always iterate over `response.content` and switch on `block.type`.
2. **Explicit resource limits** -- `max_tokens` is always required. There is no default. The API will reject requests without it.
3. **Tool use is a conversation loop** -- When `stop_reason === "tool_use"`, Claude is requesting you execute a tool. You must send the result back as a `tool_result` content block to continue the conversation.
4. **Built-in resilience** -- The SDK retries 2 times by default on 429, 409, 408, 529, and 5xx errors with exponential backoff.
5. **Streaming as a first-class pattern** -- Use `.stream()` for an event-based API with `.on("text", ...)`, or `stream: true` for raw SSE iteration.

**When to use the Anthropic SDK directly:**

- You only use Claude models and want the simplest, most direct integration
- You need access to Anthropic-specific features (extended thinking, prompt caching, batch API)
- You want minimal dependencies and zero abstraction overhead
- You need the latest API features on day one

**When NOT to use:**

- You need to switch between multiple LLM providers -- use a unified provider SDK
- You want React-specific chat UI hooks -- use a framework-integrated AI SDK
- You want a higher-level agent framework -- consider the Claude Agent SDK

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize the Anthropic client. It auto-reads `ANTHROPIC_API_KEY` from the environment.

```typescript
// lib/anthropic.ts -- basic setup
import Anthropic from "@anthropic-ai/sdk";
const client = new Anthropic();
export { client };
```

```typescript
// lib/anthropic.ts -- production configuration
const TIMEOUT_MS = 30_000;
const MAX_RETRIES = 3;
const client = new Anthropic({ timeout: TIMEOUT_MS, maxRetries: MAX_RETRIES });
```

**Why good:** Minimal setup, env var auto-detected, named constants for production settings

```typescript
// BAD: Hardcoded API key
const client = new Anthropic({ apiKey: "sk-ant-api03-..." });
```

**Why bad:** Hardcoded keys get committed to version control, causing security breaches

**See:** [examples/core.md](examples/core.md) for per-request overrides, error handling patterns, token counting

---

### Pattern 2: Messages API

All interactions use `client.messages.create()`. `max_tokens` is always required.

```typescript
const MAX_TOKENS = 1024;

const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  system: "You are a helpful coding assistant.",
  messages: [{ role: "user", content: "Explain TypeScript generics." }],
});

// Response is an array of content blocks -- iterate, don't assume
for (const block of message.content) {
  if (block.type === "text") {
    console.log(block.text);
  }
}
```

**Why good:** Named constant for max_tokens, system prompt separated from messages, content blocks iterated

```typescript
// BAD: Assuming content is a single text string
const text = message.content[0].text; // Crashes if block is tool_use or thinking
```

**Why bad:** Content can contain multiple blocks of different types -- direct index access without type checking crashes at runtime

**See:** [examples/core.md](examples/core.md) for multi-turn conversations, system prompts, token tracking

---

### Pattern 3: Streaming

Use `.stream()` for event-based streaming with text accumulation helpers.

```typescript
const MAX_TOKENS = 1024;

const stream = client.messages.stream({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  messages: [{ role: "user", content: "Explain async/await." }],
});

stream.on("text", (text) => {
  process.stdout.write(text);
});

const finalMessage = await stream.finalMessage();
```

**Why good:** Event-based API handles accumulation, `finalMessage()` gives the complete response object

```typescript
// BAD: Using stream: true without consuming events
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  messages: [{ role: "user", content: "Hello" }],
  stream: true,
});
// Response is an async iterable, not a Message -- must iterate
```

**Why bad:** `stream: true` returns an async iterable of raw SSE events, not a Message. Treating it as a Message silently breaks.

**See:** [examples/streaming.md](examples/streaming.md) for raw SSE iteration, abort, stream events, streaming with thinking

---

### Pattern 4: Tool Use / Function Calling

Define tools Claude can invoke. Handle the `tool_use` -> `tool_result` conversation loop.

```typescript
const tools: Anthropic.Messages.Tool[] = [
  {
    name: "get_weather",
    description: "Get current weather for a location",
    input_schema: {
      type: "object" as const,
      properties: {
        location: { type: "string", description: "City name" },
      },
      required: ["location"],
    },
  },
];

const MAX_TOKENS = 1024;

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  tools,
  messages: [{ role: "user", content: "Weather in Paris?" }],
});

// Check stop_reason to know if Claude wants to call a tool
if (response.stop_reason === "tool_use") {
  const toolBlock = response.content.find(
    (block): block is Anthropic.Messages.ToolUseBlock =>
      block.type === "tool_use",
  );
  if (toolBlock) {
    console.log(`Call ${toolBlock.name} with:`, toolBlock.input);
  }
}
```

**Why good:** Typed tool definitions, `stop_reason` checked, type guard for `ToolUseBlock`

```typescript
// BAD: Not checking stop_reason, not sending tool_result back
const response = await client.messages.create({
  /* ... with tools */
});
console.log(response.content[0]); // May be a tool_use block, not text!
```

**Why bad:** When Claude wants to call a tool, there is no text content -- only `tool_use` blocks. You must execute the tool and send back a `tool_result` to get the final answer.

**See:** [examples/tool-use.md](examples/tool-use.md) for complete tool loops, parallel tool calls, automated tool runner

---

### Pattern 5: Vision & Documents

Pass images and PDFs as content blocks alongside text.

```typescript
import { readFileSync } from "node:fs";

const MAX_TOKENS = 1024;
const imageData = readFileSync("photo.jpg").toString("base64");

const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "image",
          source: { type: "base64", media_type: "image/jpeg", data: imageData },
        },
        { type: "text", text: "What's in this image?" },
      ],
    },
  ],
});
```

**Why good:** Multi-part content array, explicit media type, text and image combined in one message

**See:** [examples/vision-documents.md](examples/vision-documents.md) for URL images, PDFs, multiple images

---

### Pattern 6: Extended Thinking

Enable extended thinking for complex reasoning. Responses include `thinking` content blocks. Use **adaptive thinking** on Opus 4.6 and Sonnet 4.6 (recommended). Use manual `budget_tokens` on older models.

```typescript
const MAX_TOKENS = 16_000;

// Adaptive thinking (recommended for 4.6 models)
const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  thinking: { type: "adaptive" },
  messages: [
    { role: "user", content: "Prove there are infinitely many primes." },
  ],
} as unknown as Anthropic.MessageCreateParamsNonStreaming);

for (const block of response.content) {
  if (block.type === "thinking") {
    console.log("Thinking:", block.thinking);
  } else if (block.type === "text") {
    console.log("Answer:", block.text);
  }
}
```

**Why good:** Adaptive thinking lets Claude decide how much to reason, iterates content blocks, handles both thinking and text blocks

```typescript
// Manual thinking (deprecated on 4.6 models, required on older models)
const THINKING_BUDGET = 10_000;

const response = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: MAX_TOKENS,
  thinking: { type: "enabled", budget_tokens: THINKING_BUDGET },
  messages: [
    { role: "user", content: "Prove there are infinitely many primes." },
  ],
});
```

**Note:** The TypeScript SDK does not yet have `"adaptive"` in its type definitions. The `as unknown as Anthropic.MessageCreateParamsNonStreaming` assertion is required until the SDK types are updated.

**See:** [examples/extended-thinking.md](examples/extended-thinking.md) for streaming thinking, thinking with tools, display options

---

### Pattern 7: Structured Outputs

Use `zodOutputFormat()` and `messages.parse()` for type-safe structured responses.

```typescript
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import { z } from "zod";

const ContactInfo = z.object({
  name: z.string(),
  email: z.string(),
  topics: z.array(z.string()),
});

const MAX_TOKENS = 1024;

const response = await client.messages.parse({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  messages: [
    {
      role: "user",
      content:
        "Extract info: John (john@example.com) asked about billing and API limits.",
    },
  ],
  output_config: { format: zodOutputFormat(ContactInfo) },
});

const parsed = response.parsed_output; // Fully typed: { name, email, topics }
```

**Why good:** Auto-converts Zod schema, validates output, fully typed result

**See:** [examples/core.md](examples/core.md) for raw JSON schema, combined with tool use

---

### Pattern 8: Prompt Caching

Cache large system prompts and conversation prefixes for cost savings.

```typescript
const MAX_TOKENS = 1024;

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: MAX_TOKENS,
  system: [
    {
      type: "text",
      text: "You are a legal document analyst.",
    },
    {
      type: "text",
      text: largeDocumentText, // 50+ pages of legal text
      cache_control: { type: "ephemeral" },
    },
  ],
  messages: [{ role: "user", content: "What are the key terms?" }],
});

// Check cache performance
console.log("Cache read tokens:", response.usage.cache_read_input_tokens);
console.log("Cache write tokens:", response.usage.cache_creation_input_tokens);
```

**Why good:** Cache breakpoint on the large static content, cache metrics tracked

**See:** [reference.md](reference.md) for cache pricing, TTL options, automatic caching

---

### Pattern 9: Error Handling

Always catch `Anthropic.APIError` and its subclasses. Re-throw unexpected errors.

```typescript
try {
  const message = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }],
  });
} catch (error) {
  if (error instanceof Anthropic.APIError) {
    console.error(`API Error [${error.status}]: ${error.message}`);

    if (error instanceof Anthropic.RateLimitError) {
      console.error("Rate limited -- SDK will auto-retry 2 times");
    }
    if (error instanceof Anthropic.AuthenticationError) {
      throw new Error("Invalid API key. Check ANTHROPIC_API_KEY.");
    }
  } else {
    throw error; // Re-throw non-API errors
  }
}
```

**Why good:** Specific error types, status code access, re-throws unexpected errors

**See:** [examples/core.md](examples/core.md) for full error hierarchy, stream error handling

</patterns>

---

<performance>

## Performance Optimization

### Model Selection for Cost/Speed

```
Most capable, complex reasoning -> claude-opus-4-6  (1M context, 128K output)
General purpose, best value      -> claude-sonnet-4-6 (1M context, 64K output)
Fast + cheap, simple tasks       -> claude-haiku-4-5  (200K context, 64K output)
Extended thinking                -> claude-sonnet-4-6 or claude-opus-4-6 (use adaptive thinking)
Vision / multimodal              -> claude-sonnet-4-6 or claude-opus-4-6
Batch processing                 -> Any model at 50% batch discount
```

### Key Optimization Patterns

- **Track token usage** via `message.usage` for cost visibility (`input_tokens`, `output_tokens`)
- **Check `stop_reason === "max_tokens"`** to detect truncated output
- **Use prompt caching** for large system prompts -- cache reads cost 0.1x base input price
- **Use `messages.countTokens()`** before sending to estimate costs
- **Use Batch API** for high-volume async jobs at 50% cost reduction
- **Use `AbortController`** to cancel long-running requests
- **Set `temperature: 0`** for deterministic output when caching matters

</performance>

---

<decision_framework>

## Decision Framework

### Which Model to Choose

```
What is your task?
+-- Complex reasoning / analysis    -> claude-opus-4-6
+-- General purpose (best balance)  -> claude-sonnet-4-6
+-- Fast + cheap, high throughput   -> claude-haiku-4-5
+-- Extended thinking needed        -> claude-sonnet-4-6 (or opus-4-6 with adaptive thinking)
+-- Vision / image analysis         -> claude-sonnet-4-6 or claude-opus-4-6
+-- Batch processing                -> Any model (50% discount)
```

### Streaming vs Non-Streaming

```
Is the response user-facing?
+-- YES -> Use streaming (client.messages.stream())
|   +-- Need event-level control? -> .on("text", ...) + .on("contentBlock", ...)
|   +-- Just want final message?  -> stream.finalMessage() (avoids HTTP timeouts on large responses)
+-- NO -> Use non-streaming (client.messages.create())
    +-- Background processing  -> messages.create()
    +-- Structured output      -> messages.parse()
    +-- High volume            -> Batch API
```

### When to Use Extended Thinking

```
Does the task require multi-step reasoning?
+-- YES -> Which model?
|   +-- Opus 4.6 or Sonnet 4.6? -> Use adaptive: thinking: { type: "adaptive" }
|   |   +-- Control depth?       -> Add output_config: { effort: "high" | "medium" | "low" }
|   |   +-- Opus only max depth? -> effort: "max"
|   +-- Older models?            -> Manual: thinking: { type: "enabled", budget_tokens: N }
+-- NO -> Standard messages.create() is sufficient (omit thinking param or type: "disabled")
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Not providing `max_tokens` (request will be rejected -- it has no default)
- Hardcoding API keys instead of using environment variables (security breach risk)
- Treating `response.content` as a string instead of iterating content blocks (crashes on `tool_use` or `thinking` blocks)
- Not checking `stop_reason` for `"tool_use"` (breaks function calling flows -- Claude is waiting for tool results)
- Using bare `catch` blocks without checking `Anthropic.APIError` (hides API-specific error information)

**Medium Priority Issues:**

- Not setting `maxRetries` / `timeout` for production deployments (default timeout is 10 minutes, which may be too long)
- Ignoring `stop_reason === "max_tokens"` (response was truncated but you are using it as complete)
- Ignoring `usage` data (no cost visibility or budget tracking)
- Not sending `thinking` blocks back in multi-turn conversations when using extended thinking (Claude loses reasoning context)
- Changing `thinking` parameters between turns in a tool use loop (invalidates message cache, causes errors)

**Common Mistakes:**

- Using `system` as a message role instead of the top-level `system` parameter (there is no `system` role in messages -- use the `system` parameter)
- Assuming `response.content` has exactly one block (it can have multiple `text`, `tool_use`, and `thinking` blocks)
- Not passing `tool_result` back after a `tool_use` response (Claude cannot continue without it)
- Using `max_completion_tokens` instead of `max_tokens` (the Anthropic API uses `max_tokens`, not `max_completion_tokens`)
- Using `response_format` instead of `output_config` for structured outputs (wrong parameter name)
- Forgetting that `budget_tokens` must be less than `max_tokens` (except with interleaved thinking)

**Gotchas & Edge Cases:**

- The SDK auto-retries on 429 (rate limit), 529 (overloaded), 408 (timeout), 409 (conflict), and 5xx errors -- 2 retries by default with exponential backoff. Disable with `maxRetries: 0`.
- `client.messages.stream()` returns a `MessageStream` with event helpers. `client.messages.create({ stream: true })` returns a raw async iterable of SSE events. They are different APIs.
- When using extended thinking with tool use, you must include the `thinking` blocks unmodified when sending conversation history back. Omitting or modifying them causes errors.
- `tool_choice: { type: "any" }` forces Claude to call a tool but cannot be used with extended thinking. Only `"auto"` and `"none"` work with thinking enabled.
- Prompt caching requires a minimum of 1024-4096 tokens (model-dependent) to be cacheable. Small prompts will not be cached.
- Cache breakpoints on messages are invalidated when `thinking` parameters change between requests. System prompt cache is preserved.
- `budget_tokens` is deprecated on both Claude Opus 4.6 and Sonnet 4.6 -- use `thinking: { type: "adaptive" }` instead. `budget_tokens` still works but will be removed in a future release.
- The `display` field on thinking config controls whether thinking text is returned: `"summarized"` (default) or `"omitted"` (only signature, faster streaming).
- Adaptive thinking automatically enables interleaved thinking (thinking between tool calls). Manual mode on Sonnet 4.6 requires the `interleaved-thinking-2025-05-14` beta header for interleaved thinking.
- The `effort` parameter (`output_config: { effort: "high" | "medium" | "low" | "max" }`) works with adaptive thinking to control thinking depth. `"max"` is Opus 4.6 only.
- The TypeScript SDK does not yet include `"adaptive"` in its type definitions -- use a type assertion when passing `thinking: { type: "adaptive" }`.
- Multi-turn conversations require you to include the full assistant response (all content blocks) in the conversation history, not just the text.
- Batch API requests have a 24-hour completion window. Use `messages.batches.results()` to retrieve completed results.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST always provide `max_tokens` in every `messages.create()` / `messages.stream()` call -- it is required and has no default)**

**(You MUST handle the `stop_reason` field to detect `end_turn`, `max_tokens`, `tool_use`, and `stop_sequence` -- ignoring it causes silent truncation or broken tool loops)**

**(You MUST iterate over `response.content` blocks (not assume a single text block) -- responses can contain `text`, `tool_use`, and `thinking` blocks mixed together)**

**(You MUST handle errors using `Anthropic.APIError` and its subclasses -- never use bare catch blocks without error type checking)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.ANTHROPIC_API_KEY`)**

**Failure to follow these rules will produce broken tool loops, silent truncation, security vulnerabilities, or untyped AI integrations.**

</critical_reminders>
