---
name: api-ai-llamaindex
description: LlamaIndex.TS data framework for RAG, indexing, retrieval, query engines, chat engines, and agentic workflows in TypeScript
---

# LlamaIndex.TS Patterns

> **Quick Guide:** LlamaIndex.TS is a data framework for building context-aware LLM applications in TypeScript. Use `Settings` singleton to configure LLM and embedding models globally. Load documents with `SimpleDirectoryReader`, chunk with `SentenceSplitter`, index with `VectorStoreIndex.fromDocuments()`, and query with `index.asQueryEngine()`. For agents, use `agent()` from `@llamaindex/workflow` with `tool()` definitions using Zod schemas. All core operations are async -- every function returns a Promise. The `llamaindex` package re-exports most things, but LLM providers require separate packages like `@llamaindex/openai` or `@llamaindex/ollama`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST configure `Settings.llm` and `Settings.embedModel` before any indexing or querying -- the Settings singleton is lazily initialized and defaults to OpenAI, which will fail without an API key)**

**(You MUST await all LlamaIndex operations -- `fromDocuments()`, `asQueryEngine()`, `query()`, `chat()`, `loadData()` are ALL async)**

**(You MUST install provider packages separately -- `@llamaindex/openai`, `@llamaindex/ollama`, `@llamaindex/anthropic` are NOT included in the base `llamaindex` package)**

**(You MUST use `storageContextFromDefaults({ persistDir })` to persist indexes -- without persistence, indexes are rebuilt from scratch on every restart)**

**(You MUST never hardcode API keys -- use environment variables and `dotenv/config`)**

</critical_requirements>

---

**Auto-detection:** LlamaIndex, llamaindex, VectorStoreIndex, SimpleDirectoryReader, Settings.llm, Settings.embedModel, asQueryEngine, asChatEngine, ContextChatEngine, SentenceSplitter, storageContextFromDefaults, @llamaindex/openai, @llamaindex/ollama, @llamaindex/workflow, FunctionTool, QueryEngineTool, agentStreamEvent

**When to use:**

- Building RAG (Retrieval-Augmented Generation) applications with custom documents
- Loading, chunking, and indexing documents for LLM consumption
- Creating query engines that answer questions from indexed data
- Building chat interfaces with conversation memory over your data
- Implementing agentic RAG with tool-calling agents that query indexes
- Working with multiple data sources (files, PDFs, markdown, code)
- Persisting vector indexes to avoid re-indexing on every restart

**Key patterns covered:**

- Settings singleton for LLM and embedding model configuration
- Document loading with SimpleDirectoryReader and custom readers
- VectorStoreIndex creation, persistence, and querying
- Query engines and chat engines
- Agent creation with `agent()` and `tool()` using Zod schemas
- Text splitting and chunking strategies
- Streaming responses from query and chat engines
- Storage context and index persistence

**When NOT to use:**

- Simple one-shot LLM calls without document context -- use the LLM provider SDK directly
- Applications that only need embeddings without indexing -- use the embedding API directly
- Client-side / browser applications -- LlamaIndex.TS is server-side focused (Node.js >= 20)

---

## Examples Index

- [Core: Setup, Indexing & Querying](examples/core.md) -- Settings config, document loading, VectorStoreIndex, query engines, persistence
- [Agents & Tools](examples/agents.md) -- FunctionTool, agent(), multi-agent workflows, QueryEngineTool
- [Chat & Streaming](examples/chat-streaming.md) -- Chat engines, ContextChatEngine, streaming responses
- [Ingestion & Splitting](examples/ingestion.md) -- Text splitters, node parsers, ingestion pipeline, custom readers
- [Quick API Reference](reference.md) -- Package map, method signatures, response modes, model providers

---

<philosophy>

## Philosophy

LlamaIndex.TS is a **data framework** -- its core value proposition is connecting your data to LLMs through indexing, retrieval, and synthesis. It sits between raw LLM APIs and full application frameworks.

**Core principles:**

1. **Context engineering** -- Inject the right data into the LLM prompt at the right time. This drives RAG, agent memory, extraction, and summarization.
2. **Modular provider system** -- LLM providers, embedding models, vector stores, and readers are separate packages you compose. The base `llamaindex` package provides the framework; providers are installed separately.
3. **Settings singleton** -- Global configuration for LLM, embedding model, node parser, and other shared resources. Set once, used everywhere. Override locally when needed.
4. **Async-first design** -- Every I/O operation is async. Document loading, indexing, querying, and chat all return Promises.
5. **Index as the core abstraction** -- Documents are loaded, split into nodes, embedded, and stored in an index. Queries retrieve relevant nodes and synthesize responses.

**When to use LlamaIndex.TS:**

- You have documents/data that need to be indexed for LLM consumption
- You want structured RAG pipelines with configurable retrieval and synthesis
- You need agentic RAG where agents query multiple indexes with tools
- You want persistence and incremental updates to your index

**When NOT to use:**

- Simple LLM calls without data context -- use the provider SDK directly
- Browser-only applications -- LlamaIndex.TS requires Node.js >= 20
- You only need embeddings -- use the embedding API directly

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Settings Configuration

The `Settings` singleton configures LLM, embedding model, and node parser globally. Set it once at application startup before any indexing or querying.

```typescript
import { Settings } from "llamaindex";
import { openai, OpenAIEmbedding } from "@llamaindex/openai";

// Configure at app startup -- before any index operations
Settings.llm = openai({ model: "gpt-4o" });
Settings.embedModel = new OpenAIEmbedding({ model: "text-embedding-3-small" });
```

**Why good:** Single configuration point, provider packages are explicit imports, model names are visible

```typescript
// BAD: No Settings configuration, relying on implicit defaults
import { VectorStoreIndex, SimpleDirectoryReader } from "llamaindex";

// This will silently try to use OpenAI with OPENAI_API_KEY from env
// Fails with cryptic error if key is missing
const documents = await new SimpleDirectoryReader().loadData({
  directoryPath: "./data",
});
const index = await VectorStoreIndex.fromDocuments(documents);
```

**Why bad:** Implicit defaults make failures confusing, no explicit provider, no model selection

**See:** [examples/core.md](examples/core.md) for local LLM setup with Ollama, Anthropic configuration, and embedding model options

---

### Pattern 2: Document Loading and Indexing

Load documents, create a vector index, and query it. This is the canonical RAG pipeline.

```typescript
import { SimpleDirectoryReader, VectorStoreIndex, Settings } from "llamaindex";
import { openai, OpenAIEmbedding } from "@llamaindex/openai";

Settings.llm = openai({ model: "gpt-4o" });
Settings.embedModel = new OpenAIEmbedding({ model: "text-embedding-3-small" });

// Load all supported files from a directory
const documents = await new SimpleDirectoryReader().loadData({
  directoryPath: "./data",
});

// Create vector index -- embeds and stores all document chunks
const index = await VectorStoreIndex.fromDocuments(documents);

// Query the index
const queryEngine = index.asQueryEngine();
const response = await queryEngine.query({ query: "What is the main topic?" });
console.log(response.message.content);
```

**Why good:** Complete pipeline in minimal code, explicit Settings, clear data flow

**See:** [examples/core.md](examples/core.md) for persistence, custom readers, and advanced indexing options

---

### Pattern 3: Index Persistence

Persist indexes to disk to avoid re-indexing on every restart.

```typescript
import {
  VectorStoreIndex,
  storageContextFromDefaults,
  SimpleDirectoryReader,
} from "llamaindex";

const PERSIST_DIR = "./storage";

// First run: create and persist
const storageContext = await storageContextFromDefaults({
  persistDir: PERSIST_DIR,
});
const documents = await new SimpleDirectoryReader().loadData({
  directoryPath: "./data",
});
const index = await VectorStoreIndex.fromDocuments(documents, {
  storageContext,
});

// Subsequent runs: load from storage
const loadedStorageContext = await storageContextFromDefaults({
  persistDir: PERSIST_DIR,
});
const loadedIndex = await VectorStoreIndex.init({
  storageContext: loadedStorageContext,
});
```

**Why good:** Named constant for path, separate create vs load paths, storage context reuse

```typescript
// BAD: Rebuilding index on every request
async function handleQuery(question: string) {
  const docs = await new SimpleDirectoryReader().loadData({
    directoryPath: "./data",
  });
  const index = await VectorStoreIndex.fromDocuments(docs); // Expensive!
  const engine = index.asQueryEngine();
  return engine.query({ query: question });
}
```

**Why bad:** Re-indexes all documents on every call, wastes time and API credits on re-embedding

**See:** [examples/core.md](examples/core.md) for load-or-create pattern

---

### Pattern 4: Agents with Tool Definitions

Create agents that use tools defined with Zod schemas. Use `agent()` from `@llamaindex/workflow`.

```typescript
import { tool, Settings } from "llamaindex";
import { agent, agentStreamEvent } from "@llamaindex/workflow";
import { openai } from "@llamaindex/openai";
import { z } from "zod";

Settings.llm = openai({ model: "gpt-4o" });

const weatherTool = tool({
  name: "getWeather",
  description: "Get current weather for a city",
  parameters: z.object({
    city: z.string({ description: "City name" }),
  }),
  execute: async ({ city }) => {
    // Your weather API call here
    return { temperature: 22, condition: "sunny" };
  },
});

const myAgent = agent({ tools: [weatherTool] });
const result = await myAgent.run("What's the weather in Paris?");
console.log(result.data);
```

**Why good:** Zod schema for type-safe parameters, description guides the LLM, async execute function

**See:** [examples/agents.md](examples/agents.md) for multi-agent workflows, QueryEngineTool, streaming agents

---

### Pattern 5: Chat Engine

Build conversational interfaces over your indexed data with conversation memory.

```typescript
import {
  VectorStoreIndex,
  ContextChatEngine,
  SimpleDirectoryReader,
} from "llamaindex";

const documents = await new SimpleDirectoryReader().loadData({
  directoryPath: "./data",
});
const index = await VectorStoreIndex.fromDocuments(documents);
const retriever = index.asRetriever({ similarityTopK: 3 });

const chatEngine = new ContextChatEngine({ retriever });

// Multi-turn conversation -- chat engine maintains history
const response1 = await chatEngine.chat({ message: "What is LlamaIndex?" });
console.log(response1.message.content);

const response2 = await chatEngine.chat({
  message: "How does it handle streaming?",
});
console.log(response2.message.content);
```

**Why good:** Retriever-based context injection, automatic conversation history, multi-turn support

**See:** [examples/chat-streaming.md](examples/chat-streaming.md) for streaming chat, system prompts, chat history management

---

### Pattern 6: Streaming Responses

Stream responses for user-facing applications.

```typescript
import { agentStreamEvent } from "@llamaindex/workflow";

// Agent streaming
const events = myAgent.runStream("Tell me about TypeScript");
for await (const event of events) {
  if (agentStreamEvent.include(event)) {
    process.stdout.write(event.data.delta);
  }
}

// Query engine streaming
const response = await queryEngine.query({
  query: "Summarize the document",
  stream: true,
});
for await (const chunk of response) {
  process.stdout.write(chunk.message.content);
}
```

**Why good:** Event-based agent streaming with typed filters, query engine streaming with for-await

**See:** [examples/chat-streaming.md](examples/chat-streaming.md) for response synthesizer streaming, chat engine streaming

---

### Pattern 7: Text Splitting and Node Parsing

Configure how documents are chunked before indexing.

```typescript
import { SentenceSplitter, Settings } from "llamaindex";

const CHUNK_SIZE = 512;
const CHUNK_OVERLAP = 50;

// Set globally via Settings
Settings.nodeParser = new SentenceSplitter({
  chunkSize: CHUNK_SIZE,
  chunkOverlap: CHUNK_OVERLAP,
});

// Or use standalone
const splitter = new SentenceSplitter({ chunkSize: CHUNK_SIZE });
const texts = splitter.splitText("Your long document text here...");
```

**Why good:** Named constants for chunk parameters, global vs standalone usage shown, sentence-aware splitting

```typescript
// BAD: Using default chunk size without considering document characteristics
const index = await VectorStoreIndex.fromDocuments(documents);
// Default chunk size may be too large for short Q&A or too small for long narratives
```

**Why bad:** Default chunk size (1024 tokens) may not suit your data, causes poor retrieval quality

**See:** [examples/ingestion.md](examples/ingestion.md) for MarkdownNodeParser, CodeSplitter, custom chunk strategies

</patterns>

---

<decision_framework>

## Decision Framework

### Which Index Type to Use

```
What is your use case?
+-- Semantic search over documents -> VectorStoreIndex (most common)
+-- Summarization of all documents -> SummaryIndex
+-- Both search AND summarization -> Create both, use as separate tools in an agent
+-- Hierarchical document structure -> Use MarkdownNodeParser + VectorStoreIndex
```

### Query Engine vs Chat Engine vs Agent

```
How should users interact with your data?
+-- Single question, single answer -> Query Engine (index.asQueryEngine())
+-- Multi-turn conversation -> Chat Engine (ContextChatEngine)
+-- Multiple tools/indexes + reasoning -> Agent (agent() from @llamaindex/workflow)
+-- Complex multi-step workflow -> Multi-agent with handoffs
```

### Which LLM Provider

```
Which LLM provider are you using?
+-- OpenAI -> npm install @llamaindex/openai
+-- Anthropic -> npm install @llamaindex/anthropic
+-- Local (Ollama) -> npm install @llamaindex/ollama
+-- Groq -> npm install @llamaindex/groq
+-- Google Gemini -> npm install @llamaindex/gemini
```

### Chunk Size Selection

```
What kind of documents are you indexing?
+-- Short Q&A pairs -> chunkSize: 256-512
+-- Technical documentation -> chunkSize: 512-1024
+-- Long narratives/reports -> chunkSize: 1024-2048
+-- Code files -> Use CodeSplitter (AST-aware)
+-- Markdown -> Use MarkdownNodeParser (structure-aware)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Not configuring `Settings.llm` before indexing/querying -- defaults to OpenAI, fails silently without API key
- Forgetting to `await` async operations -- `fromDocuments()`, `query()`, `chat()` all return Promises
- Rebuilding indexes on every request instead of persisting with `storageContextFromDefaults`
- Hardcoding API keys instead of using environment variables
- Installing only `llamaindex` without provider packages (`@llamaindex/openai`, etc.)

**Medium Priority Issues:**

- Using default chunk size (1024) without considering document characteristics -- causes poor retrieval
- Not setting `similarityTopK` on retrievers -- default may return too few or too many results
- Ignoring the response `sourceNodes` -- they contain the retrieved context for debugging and citations
- Creating a new `SimpleDirectoryReader` per request instead of caching the loaded documents
- Not handling the case where `response.message.content` might be empty on retrieval failure

**Common Mistakes:**

- Confusing `asQueryEngine()` (single question) with `ContextChatEngine` (multi-turn conversation)
- Using `VectorStoreIndex.fromDocuments()` when you should use `VectorStoreIndex.init()` to load from storage
- Importing `openai` from `llamaindex` instead of `@llamaindex/openai` -- the `llamaindex` package may re-export some things but provider-specific imports are more reliable
- Passing `messages` array to `query()` -- query engines take `{ query: string }`, not a messages array
- Using `index.asQueryEngine()` multiple times instead of storing the engine reference

**Gotchas & Edge Cases:**

- `Settings` is a global singleton -- setting it in one module affects all others. Override locally by passing `llm` directly to constructors when you need different models for different operations.
- `SimpleDirectoryReader` only works on Node.js -- it uses `fs` internally. For edge/serverless, load documents differently or use LlamaParse.
- `storageContextFromDefaults` creates four JSON files in the persist directory (`docstore.json`, `graph_store.json`, `index_store.json`, `vector_store.json`). If any are corrupted, delete the directory and re-index.
- Node.js >= 20 is required. Some modules use Web Stream API (`ReadableStream`, `WritableStream`), so add `"DOM.AsyncIterable"` to `tsconfig.json` `lib` if you get type errors.
- `tsconfig.json` must use `"moduleResolution": "bundler"` or `"nodenext"` -- the classic `"node"` resolution will fail to resolve LlamaIndex sub-packages.
- Default tokenizer is slow -- install `gpt-tokenizer` for 60x faster tokenization.
- `SentenceSplitter` chunk size is in tokens, not characters. A 512-token chunk is roughly 2000 characters.
- The `llamaindex` package is large (~2MB+). For production, consider importing specific sub-packages to reduce bundle size.
- `VectorStoreIndex.fromDocuments()` makes embedding API calls for every chunk. For large document sets, this can be expensive. Monitor costs.
- Chat engine conversation history grows unbounded -- implement history pruning for long-running sessions.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST configure `Settings.llm` and `Settings.embedModel` before any indexing or querying -- the Settings singleton is lazily initialized and defaults to OpenAI, which will fail without an API key)**

**(You MUST await all LlamaIndex operations -- `fromDocuments()`, `asQueryEngine()`, `query()`, `chat()`, `loadData()` are ALL async)**

**(You MUST install provider packages separately -- `@llamaindex/openai`, `@llamaindex/ollama`, `@llamaindex/anthropic` are NOT included in the base `llamaindex` package)**

**(You MUST use `storageContextFromDefaults({ persistDir })` to persist indexes -- without persistence, indexes are rebuilt from scratch on every restart)**

**(You MUST never hardcode API keys -- use environment variables and `dotenv/config`)**

**Failure to follow these rules will produce broken RAG pipelines, wasted embedding API credits, or cryptic runtime errors.**

</critical_reminders>
