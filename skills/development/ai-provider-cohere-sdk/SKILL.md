---
name: ai-provider-cohere-sdk
description: Official Cohere TypeScript SDK patterns -- CohereClientV2, chat, embeddings, rerank, RAG with citations, tool use, streaming, and model selection
---

# Cohere SDK Patterns

> **Quick Guide:** Use the `cohere-ai` npm package with `CohereClientV2` for all new Cohere integrations. V2 API requires `model` on every call. Use `chatStream` for streaming with `content-delta` events. Embeddings require `inputType` matching your use case (`search_document` for indexing, `search_query` for querying). Rerank scores documents by relevance. RAG works by passing `documents` to `chat()` -- the model returns inline citations automatically. Tool use follows a 4-step loop: user message, model returns `tool_calls`, you execute and return results, model generates cited response.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `CohereClientV2` (not `CohereClient`) for all new code -- V2 is the current API with required `model` parameter)**

**(You MUST specify `inputType` on every embed call -- `search_document` for indexing, `search_query` for querying -- mismatched types produce garbage similarity scores)**

**(You MUST handle the tool use loop correctly: append the full assistant message (with `tool_calls`) to messages, then append `tool` role results with matching `tool_call_id`)**

**(You MUST check `finish_reason` in responses -- `MAX_TOKENS` means the output was truncated)**

**(You MUST never hardcode API keys -- pass via `token` constructor parameter sourced from environment variables)**

</critical_requirements>

---

**Auto-detection:** Cohere, cohere-ai, CohereClientV2, CohereClient, command-a, command-r, command-r-plus, embed-v4, rerank-v4, chatStream, content-delta, inputType, search_document, search_query, embeddingTypes, topN, CO_API_KEY, COHERE_API_KEY

**When to use:**

- Building applications with Cohere Command models (chat, generation, summarization)
- Creating semantic search pipelines with Cohere embeddings
- Adding relevance scoring to search results with Cohere Rerank
- Implementing RAG with inline document grounding and automatic citations
- Building agentic workflows with Cohere tool use / function calling
- Streaming chat responses for real-time user interfaces

**Key patterns covered:**

- Client setup with `CohereClientV2` (token, timeout, platform configs)
- Chat and streaming (`chat`, `chatStream`, event types)
- Embeddings with `inputType` for search/classification/clustering
- Rerank for relevance scoring and search result ordering
- RAG with documents and automatic citation handling
- Tool use / function calling with multi-step loops
- Model selection (Command-A, Command-R, Embed v4, Rerank v4)

**When NOT to use:**

- Multi-provider applications needing OpenAI/Anthropic/Google switching -- use a unified provider SDK
- React-specific chat UI hooks -- use a framework-integrated AI SDK
- Simple text completion without Cohere-specific features (rerank, citations)

---

## Examples Index

- [Core: Setup, Chat & Error Handling](examples/core.md) -- CohereClientV2 init, basic chat, streaming, error handling
- [Embeddings & Rerank](examples/embeddings-rerank.md) -- Semantic search, input types, rerank scoring, RAG pipeline
- [Tool Use & RAG](examples/tools-rag.md) -- Function calling, document grounding, citation handling
- [Quick API Reference](reference.md) -- Model IDs, method signatures, event types, error classes

---

<philosophy>

## Philosophy

The Cohere TypeScript SDK (`cohere-ai`) provides **direct access to Cohere's API surface** -- chat, embeddings, rerank, and RAG with citations. The SDK is auto-generated from Cohere's API spec using Fern.

**Core principles:**

1. **V2 API is current** -- `CohereClientV2` provides the modern API. `model` is required on every call. V1 methods on `CohereClient` are legacy.
2. **Embeddings are typed** -- The `inputType` parameter (`search_document`, `search_query`, `classification`, `clustering`) is mandatory for v3+ models. Mismatching input types between indexing and querying silently degrades results.
3. **RAG is first-class** -- Pass `documents` directly to `chat()` and the model returns grounded answers with inline citations. No external retrieval framework required for the grounding step.
4. **Rerank is a standalone primitive** -- Score and reorder search results without building a full RAG pipeline. Feed any list of documents and a query, get relevance scores back.
5. **Citations are automatic** -- When documents are provided (via RAG or tool results), the model generates fine-grained citations with start/end positions and source references.

**When to use the Cohere SDK directly:**

- You want Cohere-specific features: rerank, citation grounding, multilingual embeddings
- You need semantic search with embed + rerank pipeline
- You want RAG with automatic inline citations
- You are building on Cohere's platform (or Bedrock/Azure/OCI with Cohere models)

**When NOT to use:**

- You need to switch between multiple LLM providers -- use a unified provider SDK
- You want React-specific chat UI hooks -- use a framework-integrated AI SDK
- You only need basic chat completion without Cohere differentiators

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize `CohereClientV2`. The `token` parameter is required (pass from environment).

```typescript
// lib/cohere.ts -- basic setup
import { CohereClientV2 } from "cohere-ai";

const client = new CohereClientV2({
  token: process.env.CO_API_KEY,
});

export { client };
```

```typescript
// lib/cohere.ts -- production configuration
const TIMEOUT_MS = 30_000;

const client = new CohereClientV2({
  token: process.env.CO_API_KEY,
  timeout: TIMEOUT_MS,
});
```

**Why good:** Explicit token from env var, named timeout constant, named export

```typescript
// BAD: Hardcoded key, default CohereClient (V1)
import { CohereClient } from "cohere-ai";
const client = new CohereClient({ token: "sk-abc123" });
```

**Why bad:** Hardcoded API key is a security breach risk, `CohereClient` is the legacy V1 client

**See:** [examples/core.md](examples/core.md) for error handling, platform configs (Bedrock, Azure)

---

### Pattern 2: Chat Completion

V2 chat uses `messages` array with `system`, `user`, `assistant`, and `tool` roles.

```typescript
const response = await client.chat({
  model: "command-a-03-2025",
  messages: [
    { role: "system", content: "You are a helpful coding assistant." },
    { role: "user", content: "Explain TypeScript generics." },
  ],
});

console.log(response.message.content[0].text);
```

**Why good:** System message for instruction, `model` explicitly specified, correct V2 content access path

```typescript
// BAD: Missing model (required in V2), wrong response access
const response = await client.chat({
  messages: [{ role: "user", content: "Hello" }],
});
console.log(response.text); // WRONG: V2 uses response.message.content[0].text
```

**Why bad:** V2 requires `model`, response shape is `response.message.content[0].text` not `response.text`

**See:** [examples/core.md](examples/core.md) for multi-turn, token tracking, temperature control

---

### Pattern 3: Streaming

Use `chatStream` with `for await` and check event `type` for `content-delta`.

```typescript
const stream = await client.chatStream({
  model: "command-a-03-2025",
  messages: [{ role: "user", content: "Explain async/await." }],
});

for await (const event of stream) {
  if (event.type === "content-delta") {
    process.stdout.write(event.delta?.message?.content?.text ?? "");
  }
}
```

**Why good:** Checks event type before accessing delta, handles nullable content safely

```typescript
// BAD: Not checking event type
for await (const event of stream) {
  console.log(event.delta?.message); // Many events don't have message delta
}
```

**Why bad:** Only `content-delta` events have text content -- other events (`message-start`, `citation-start`, `tool-plan-delta`) have different shapes

**See:** [examples/core.md](examples/core.md) for full streaming with all event types

---

### Pattern 4: Embeddings

`inputType` is required for v3+ models. Mismatching types between indexing and querying silently degrades results.

```typescript
const EMBEDDING_MODEL = "embed-v4.0";

// Index documents with search_document
const docEmbeddings = await client.embed({
  model: EMBEDDING_MODEL,
  inputType: "search_document",
  texts: ["TypeScript is a typed superset of JavaScript."],
  embeddingTypes: ["float"],
});

// Query with search_query
const queryEmbedding = await client.embed({
  model: EMBEDDING_MODEL,
  inputType: "search_query",
  texts: ["What is TypeScript?"],
  embeddingTypes: ["float"],
});
```

**Why good:** Correct `inputType` pairing, `embeddingTypes` explicitly specified, named model constant

```typescript
// BAD: Same inputType for both indexing and querying
const docs = await client.embed({
  model: "embed-v4.0",
  inputType: "search_query", // WRONG for documents
  texts: documents,
  embeddingTypes: ["float"],
});
```

**Why bad:** Using `search_query` for document indexing silently produces worse similarity scores -- documents must use `search_document`

**See:** [examples/embeddings-rerank.md](examples/embeddings-rerank.md) for cosine similarity, dimension control, batch embedding

---

### Pattern 5: Rerank

Score documents by relevance to a query. Returns ordered results with relevance scores.

```typescript
const RERANK_MODEL = "rerank-v4.0-pro";
const TOP_N = 3;

const result = await client.rerank({
  model: RERANK_MODEL,
  query: "What is TypeScript?",
  documents: [
    "TypeScript is a typed superset of JavaScript.",
    "Python is a general-purpose language.",
    "TypeScript compiles to JavaScript.",
  ],
  topN: TOP_N,
});

for (const item of result.results) {
  console.log(`Doc ${item.index}: score ${item.relevanceScore}`);
}
```

**Why good:** Named constants, `topN` limits results, accesses `index` and `relevanceScore`

**See:** [examples/embeddings-rerank.md](examples/embeddings-rerank.md) for embed + rerank pipeline, rank fields

---

### Pattern 6: RAG with Documents

Pass `documents` to `chat()` and the model returns grounded answers with inline citations.

```typescript
const response = await client.chat({
  model: "command-a-03-2025",
  messages: [{ role: "user", content: "What is TypeScript?" }],
  documents: [
    {
      data: {
        text: "TypeScript is a typed superset of JavaScript.",
        title: "TS Docs",
      },
    },
    {
      data: {
        text: "TypeScript was developed by Microsoft.",
        title: "History",
      },
    },
  ],
});

console.log(response.message.content[0].text);

// Citations reference which documents support each claim
if (response.message.citations) {
  for (const citation of response.message.citations) {
    console.log(`"${citation.text}" from doc ${citation.sources}`);
  }
}
```

**Why good:** Documents passed inline with metadata, citations accessed from response, no external retrieval framework needed

**See:** [examples/tools-rag.md](examples/tools-rag.md) for full RAG pipeline with embed + rerank + chat

---

### Pattern 7: Tool Use / Function Calling

4-step loop: user message -> model returns `tool_calls` -> execute tools -> return results with `tool_call_id`.

```typescript
const tools = [
  {
    type: "function" as const,
    function: {
      name: "get_weather",
      description: "Get weather for a city",
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

const response = await client.chat({
  model: "command-a-03-2025",
  messages: [{ role: "user", content: "Weather in Paris?" }],
  tools,
});

// Check if model wants to call tools
if (response.message.toolCalls) {
  // See examples/tools-rag.md for the complete tool execution loop
}
```

**Why good:** Standard JSON Schema tool definition, checks for toolCalls before executing

**See:** [examples/tools-rag.md](examples/tools-rag.md) for complete multi-step tool loop with tool result submission

---

### Pattern 8: Error Handling

Catch `CohereError` for API errors, `CohereTimeoutError` for timeouts.

```typescript
import { CohereError, CohereTimeoutError } from "cohere-ai";

try {
  const response = await client.chat({
    model: "command-a-03-2025",
    messages: [{ role: "user", content: "Hello" }],
  });
} catch (error) {
  if (error instanceof CohereTimeoutError) {
    console.error("Request timed out");
  } else if (error instanceof CohereError) {
    console.error(`API Error [${error.statusCode}]: ${error.message}`);
    console.error("Body:", error.body);
  } else {
    throw error; // Re-throw unknown errors
  }
}
```

**Why good:** Specific error types with status codes, re-throws unexpected errors, timeout handled separately

**See:** [examples/core.md](examples/core.md) for production error handling patterns

</patterns>

---

<performance>

## Performance Optimization

### Model Selection for Cost/Speed

```
General purpose (best)      -> command-a-03-2025 (256K context, strongest)
Reasoning tasks             -> command-a-reasoning-08-2025 (multi-step reasoning)
Vision/document analysis    -> command-a-vision-07-2025 (images, charts, OCR)
Translation                 -> command-a-translate-08-2025 (23 languages)
Lightweight / edge          -> command-r7b-12-2024 (7B, fast, 128K context)
Legacy (still supported)    -> command-r-08-2024, command-r-plus-08-2024
Embeddings (best)           -> embed-v4.0 (multimodal, 128K context, flexible dims)
Embeddings (English)        -> embed-english-v3.0 (1024 dims)
Embeddings (multilingual)   -> embed-multilingual-v3.0 (23 languages)
Rerank (quality)            -> rerank-v4.0-pro (32K context, multilingual)
Rerank (speed)              -> rerank-v4.0-fast (32K context, latency-optimized)
```

### Key Optimization Patterns

- **Batch embeddings** -- pass up to 96 texts per `embed()` call instead of calling per-document
- **Use `topN` in rerank** -- limit results to reduce response size and cost
- **Use `outputDimension` with embed-v4** -- reduce dimensions (256/512/1024) for faster similarity search at minimal quality loss
- **Check `finish_reason === "MAX_TOKENS"`** -- detect truncated output
- **Use `temperature: 0`** for deterministic output (enables caching)
- **Use embed-v4 `int8`/`binary` types** for compressed storage with minimal quality loss
- **Use `strictTools: true`** to force tool calls to follow the schema exactly (structured outputs)
- **Use `thinking: { type: "enabled" }`** with reasoning models for complex multi-step tasks
- **Use `toolChoice: "REQUIRED"`** when you always want the model to call a tool (command-r7b+ only)

</performance>

---

<decision_framework>

## Decision Framework

### Which Client Class to Use

```
New project?
+-- YES -> CohereClientV2 (always)
+-- Existing V1 code?
    +-- Working fine? -> Keep CohereClient but plan migration
    +-- Need V2 features? -> Migrate to CohereClientV2
```

### Which Model to Choose

```
What is your task?
+-- General chat/generation -> command-a-03-2025 (most capable)
+-- Reasoning / multi-step -> command-a-reasoning-08-2025
+-- Image/document analysis -> command-a-vision-07-2025
+-- Translation -> command-a-translate-08-2025
+-- Lightweight / low latency -> command-r7b-12-2024
+-- Embeddings -> embed-v4.0 (or embed-english-v3.0 for English-only)
+-- Rerank quality -> rerank-v4.0-pro
+-- Rerank speed -> rerank-v4.0-fast
```

### Embed `inputType` Selection

```
What are you embedding?
+-- Documents for a search index -> "search_document"
+-- Search queries against an index -> "search_query"
+-- Text for a classifier -> "classification"
+-- Text for clustering -> "clustering"
+-- Images -> "image" (embed-v4+ only)
```

### When to Use Rerank

```
Do you have search results to re-order?
+-- YES -> Use rerank as a second-stage ranker
|   +-- Quality matters most? -> rerank-v4.0-pro
|   +-- Latency matters most? -> rerank-v4.0-fast
+-- NO -> Not applicable (rerank needs existing results to score)
```

### RAG Approach

```
Do you need grounded answers with citations?
+-- YES -> Pass documents to chat()
|   +-- Have pre-retrieved documents? -> Pass directly via documents param
|   +-- Need retrieval first? -> Use embed + vector search + rerank pipeline, then pass top results to chat()
+-- NO -> Use plain chat without documents
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `CohereClient` instead of `CohereClientV2` for new code (V1 is legacy)
- Missing `model` parameter in V2 API calls (required on every call, unlike V1)
- Using wrong `inputType` for embeddings (`search_query` for documents or vice versa -- silently degrades results)
- Hardcoding API keys instead of using environment variables
- Not appending the full assistant message (with `tool_calls`) before appending tool results in the tool use loop

**Medium Priority Issues:**

- Not specifying `embeddingTypes` (defaults may not match your storage format)
- Ignoring `finish_reason: "MAX_TOKENS"` (output was silently truncated)
- Not handling `CohereTimeoutError` separately from `CohereError`
- Processing all stream events without checking `type` (only `content-delta` has text)
- Using V1 parameter names (`preamble`, `connectors`, `conversation_id`) with V2 client

**Common Mistakes:**

- Accessing `response.text` instead of `response.message.content[0].text` (V2 response shape changed)
- Forgetting that `embeddingTypes` is required in V2 Embed API
- Not matching `tool_call_id` when submitting tool results (model cannot correlate results)
- Using `documents` with string values instead of `{ data: { text: "..." } }` objects in V2
- Expecting `response.message.citations` to exist when no documents were provided (citations only appear with grounded responses)

**Gotchas & Edge Cases:**

- The SDK is in beta -- pin your `cohere-ai` version in package.json to avoid breaking changes
- V2 API is NOT yet supported for cloud deployments (Bedrock, SageMaker, Azure, OCI) -- use V1 client for cloud platforms
- `inputType` is camelCase in TypeScript SDK (`inputType`) but snake_case in the REST API (`input_type`)
- Embed API accepts max 96 texts per call -- batch larger sets yourself
- `embed-v4.0` supports `outputDimension` for flexible sizing (256, 512, 1024, 1536) but v3 models have fixed dimensions
- Rerank `relevanceScore` is normalized 0-1 but not calibrated across queries -- compare scores within a single query only
- Stream events include `tool-plan-delta` before `tool-call-start` -- the model's reasoning about which tool to call
- V2 uses `system` role for instructions (V1 used `preamble` parameter)
- Citation `sources` in tool use responses reference `tool_call_id` values, not document indices
- The `clientName` constructor parameter is for logging/analytics, not authentication
- `responseFormat: { type: "json_object" }` is NOT supported in RAG mode (with `documents`, `tools`, or `toolResults`)
- `toolChoice` is only supported on `command-r7b-12-2024` and newer models
- First requests with `strictTools: true` and a new tool set take longer (schema compilation)
- `thinking` (reasoning mode) is only available on reasoning-capable models like `command-a-reasoning-08-2025`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `CohereClientV2` (not `CohereClient`) for all new code -- V2 is the current API with required `model` parameter)**

**(You MUST specify `inputType` on every embed call -- `search_document` for indexing, `search_query` for querying -- mismatched types produce garbage similarity scores)**

**(You MUST handle the tool use loop correctly: append the full assistant message (with `tool_calls`) to messages, then append `tool` role results with matching `tool_call_id`)**

**(You MUST check `finish_reason` in responses -- `MAX_TOKENS` means the output was truncated)**

**(You MUST never hardcode API keys -- pass via `token` constructor parameter sourced from environment variables)**

**Failure to follow these rules will produce broken embeddings, missing citations, or insecure AI integrations.**

</critical_reminders>
