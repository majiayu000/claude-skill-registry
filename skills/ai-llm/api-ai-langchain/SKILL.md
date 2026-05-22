---
name: api-ai-langchain
description: LangChain.js patterns for building LLM applications — chat models, LCEL chains, prompt templates, structured output, agents, tools, RAG, streaming, and LangSmith tracing
---

# LangChain.js Patterns

> **Quick Guide:** Use LangChain.js (v1.x) to build composable LLM applications. Use LCEL (`prompt.pipe(model).pipe(parser)`) for all chain composition -- never use legacy `LLMChain`. Use `withStructuredOutput(zodSchema)` for typed responses. Use `createAgent()` (LangGraph-backed) for agentic workflows -- `AgentExecutor` is legacy. All `@langchain/*` packages must share the same `@langchain/core` version or you get cryptic type errors at runtime.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use LCEL pipe composition (`prompt.pipe(model).pipe(parser)`) for all chains -- never use legacy `LLMChain`, `ConversationChain`, or `SequentialChain`)**

**(You MUST ensure all `@langchain/*` packages depend on the same version of `@langchain/core` -- version mismatches cause cryptic runtime errors)**

**(You MUST use `withStructuredOutput(zodSchema)` for structured LLM responses -- never manually parse JSON from completion text)**

**(You MUST use `createAgent()` from `langchain` for new agent code -- `AgentExecutor` and `createToolCallingAgent` are legacy patterns)**

**(You MUST never hardcode API keys -- use environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.))**

</critical_requirements>

---

**Auto-detection:** LangChain, langchain, @langchain/core, @langchain/openai, @langchain/anthropic, @langchain/google-genai, ChatOpenAI, ChatAnthropic, ChatPromptTemplate, StringOutputParser, RunnableSequence, pipe, withStructuredOutput, createAgent, createToolCallingAgent, AgentExecutor, tool, DynamicStructuredTool, RecursiveCharacterTextSplitter, MemoryVectorStore, OpenAIEmbeddings, LCEL, LangSmith, LANGCHAIN_TRACING_V2

**When to use:**

- Building LLM applications that compose prompts, models, and output parsers into chains
- Creating agentic workflows where models decide which tools to call
- Implementing RAG pipelines with document loading, splitting, embedding, and retrieval
- Needing structured output from LLMs with type-safe Zod schema validation
- Streaming LLM responses token-by-token to users
- Switching between LLM providers (OpenAI, Anthropic, Google) with a unified interface
- Tracing and debugging LLM applications with LangSmith

**Key patterns covered:**

- Chat model initialization and provider switching (ChatOpenAI, ChatAnthropic, ChatGoogleGenerativeAI)
- LCEL chain composition with `.pipe()` and `RunnableSequence`
- Prompt templates (`ChatPromptTemplate`, `MessagesPlaceholder`)
- Structured output with `withStructuredOutput()` and Zod schemas
- Tool definition with `tool()` function and Zod schemas
- Agent creation with `createAgent()` (LangGraph-backed)
- RAG pipelines: document loaders, text splitters, vector stores, retrievers
- Streaming from chains, models, and agents
- LangSmith tracing setup

**When NOT to use:**

- You only call one LLM provider and want the thinnest wrapper -- use the provider's SDK directly
- You need React-specific chat UI hooks (`useChat`, `useCompletion`) -- use a framework-integrated AI SDK
- You want a simple single-call completion with no chaining -- a direct SDK call is simpler
- You need real-time bidirectional communication -- LangChain does not cover WebSocket/Realtime APIs

---

## Examples Index

- [Core: Setup, LCEL & Chat Models](examples/core.md) -- Package installation, chat model init, LCEL chains, prompt templates, output parsers
- [Structured Output & Tools](examples/structured-output-tools.md) -- `withStructuredOutput`, tool definition, binding tools to models
- [Agents](examples/agents.md) -- `createAgent`, tool-calling agents, chat history, streaming agents
- [RAG Pipelines](examples/rag.md) -- Document loaders, text splitters, vector stores, retrieval chains
- [Streaming](examples/streaming.md) -- Model streaming, chain streaming, agent streaming
- [Quick API Reference](reference.md) -- Package map, import paths, environment variables, model IDs

---

<philosophy>

## Philosophy

LangChain.js provides a **composable framework** for building LLM-powered applications. Its core abstraction is the **Runnable** -- any component that takes an input and produces an output. Runnables compose via LCEL (`.pipe()`) to form chains, and every Runnable supports `.invoke()`, `.stream()`, `.batch()` uniformly.

**Core principles:**

1. **Composability via LCEL** -- Chains are built by piping Runnables: `prompt.pipe(model).pipe(parser)`. Each step is independently testable and replaceable. Legacy chain classes (`LLMChain`, `ConversationChain`) are deprecated.
2. **Provider-agnostic models** -- Chat models (`ChatOpenAI`, `ChatAnthropic`, `ChatGoogleGenerativeAI`) share a common interface. Swap providers by changing one import and model name. Use `initChatModel()` for runtime provider selection.
3. **Type-safe structured output** -- `model.withStructuredOutput(zodSchema)` constrains LLM responses to your schema. No manual JSON parsing.
4. **Split package architecture** -- `@langchain/core` holds abstractions, provider packages (`@langchain/openai`, `@langchain/anthropic`) hold implementations, `langchain` holds higher-level composables. All must share the same `@langchain/core` version.
5. **Observability built in** -- Set `LANGCHAIN_TRACING_V2=true` and every chain/agent/tool call is traced to LangSmith automatically.

**When to use LangChain:**

- You need to compose multi-step LLM workflows (prompt -> model -> parser -> next step)
- You want to swap LLM providers without rewriting business logic
- You need agent-style tool calling with automatic routing
- You need RAG with document loading, chunking, embedding, and retrieval
- You want built-in tracing and evaluation via LangSmith

**When NOT to use:**

- Single-provider, single-call use cases -- the provider SDK is simpler and has less overhead
- You want full control over HTTP requests -- LangChain abstracts the transport layer
- Extremely latency-sensitive applications where the abstraction overhead matters

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Chat Model Initialization

Initialize chat models from any provider. They all share the same interface.

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  model: "gpt-4o",
  temperature: 0,
});

const response = await model.invoke("Explain TypeScript generics.");
console.log(response.text);
```

**Why good:** Explicit model name, temperature set for determinism, `.text` accessor for content

```typescript
// BAD: Hardcoded API key, no model specified
import { ChatOpenAI } from "@langchain/openai";
const model = new ChatOpenAI({ apiKey: "sk-1234..." });
```

**Why bad:** Hardcoded API key is a security risk, missing model name uses unpredictable defaults

#### Provider Switching

```typescript
import { ChatAnthropic } from "@langchain/anthropic";
const model = new ChatAnthropic({ model: "claude-sonnet-4-20250514" });

// Or use initChatModel for runtime provider selection
import { initChatModel } from "langchain";
const model = await initChatModel("openai:gpt-4o", { temperature: 0 });
```

**See:** [examples/core.md](examples/core.md) for full provider examples and configuration options

---

### Pattern 2: LCEL Chain Composition

Compose chains using `.pipe()`. Every component is a Runnable.

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

const prompt = ChatPromptTemplate.fromTemplate(
  "Summarize this in one sentence: {text}",
);
const model = new ChatOpenAI({ model: "gpt-4o" });
const parser = new StringOutputParser();

const chain = prompt.pipe(model).pipe(parser);
const result = await chain.invoke({ text: "LangChain is a framework..." });
// result is a plain string
```

**Why good:** Each step is independently testable, streaming propagates through the entire chain, swapping model is one line change

```typescript
// BAD: Legacy LLMChain (deprecated)
import { LLMChain } from "langchain/chains";
const chain = new LLMChain({ llm: model, prompt });
```

**Why bad:** `LLMChain` is deprecated, does not support streaming propagation, harder to compose

**See:** [examples/core.md](examples/core.md) for `RunnableSequence.from()`, `RunnablePassthrough`, `RunnableParallel`

---

### Pattern 3: Structured Output with Zod

Use `withStructuredOutput()` for type-safe LLM responses.

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

const MovieSchema = z.object({
  title: z.string().describe("The movie title"),
  year: z.number().describe("Release year"),
  genres: z.array(z.string()).describe("List of genres"),
});

const structuredModel = new ChatOpenAI({
  model: "gpt-4o",
}).withStructuredOutput(MovieSchema);
const movie = await structuredModel.invoke("Tell me about Inception.");
// movie is typed: { title: string; year: number; genres: string[] }
```

**Why good:** Output is validated against schema, fully typed, no manual JSON parsing

```typescript
// BAD: Manual JSON parsing from completion text
const response = await model.invoke("Return JSON with title and year...");
const data = JSON.parse(response.text); // Fragile, untyped, can throw
```

**Why bad:** No schema validation, untyped result, model may return malformed JSON

**See:** [examples/structured-output-tools.md](examples/structured-output-tools.md) for complex schemas and edge cases

---

### Pattern 4: Tool Definition

Define tools with the `tool()` function and Zod schemas. Use `snake_case` for tool names.

```typescript
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const getWeather = tool(
  async ({ location }) => {
    // Call real weather API here
    return `Weather in ${location}: 22C, sunny`;
  },
  {
    name: "get_weather",
    description: "Get current weather for a city",
    schema: z.object({
      location: z.string().describe("City name, e.g. 'San Francisco'"),
    }),
  },
);
```

**Why good:** Zod schema validates input, `.describe()` guides model's argument generation, `snake_case` name avoids provider compatibility issues

```typescript
// BAD: Using DynamicStructuredTool (verbose, legacy pattern)
import { DynamicStructuredTool } from "@langchain/core/tools";
const tool = new DynamicStructuredTool({
  name: "getWeather",        // camelCase breaks some providers
  description: "...",
  schema: z.object({ ... }),
  func: async (input) => { ... },
});
```

**Why bad:** `DynamicStructuredTool` is verbose compared to `tool()`, camelCase name causes issues with some providers

**See:** [examples/structured-output-tools.md](examples/structured-output-tools.md) for binding tools to models and handling tool calls

---

### Pattern 5: Agents with `createAgent()`

Use `createAgent()` for agentic workflows. It is backed by LangGraph and handles tool calling loops automatically.

```typescript
import { createAgent } from "langchain";
import { tool } from "@langchain/core/tools";
import { z } from "zod";

const search = tool(async ({ query }) => `Results for: ${query}`, {
  name: "search",
  description: "Search for information",
  schema: z.object({ query: z.string() }),
});

const agent = createAgent({
  model: "openai:gpt-4o",
  tools: [search],
  systemPrompt: "You are a helpful research assistant.",
});

const stream = await agent.stream({
  messages: [{ role: "user", content: "Find info about LangChain" }],
});
for await (const step of stream) {
  console.log(step.messages.at(-1));
}
```

**Why good:** `createAgent` handles the tool-call loop, supports streaming, manages state via LangGraph

```typescript
// BAD: Legacy AgentExecutor pattern
import { AgentExecutor, createToolCallingAgent } from "langchain/agents";
const agent = createToolCallingAgent({ llm, tools, prompt });
const executor = new AgentExecutor({ agent, tools });
```

**Why bad:** `AgentExecutor` is legacy, does not integrate with LangGraph state management, less composable

**See:** [examples/agents.md](examples/agents.md) for chat history, custom state, and middleware patterns

---

### Pattern 6: RAG Pipeline

Load documents, split into chunks, embed, store in a vector store, and retrieve.

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";
import { OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "@langchain/classic/vectorstores/memory";

const CHUNK_SIZE = 1000;
const CHUNK_OVERLAP = 200;

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: CHUNK_SIZE,
  chunkOverlap: CHUNK_OVERLAP,
});
const chunks = await splitter.splitDocuments(docs);

const embeddings = new OpenAIEmbeddings({ model: "text-embedding-3-small" });
const vectorStore = new MemoryVectorStore(embeddings);
await vectorStore.addDocuments(chunks);

// Retrieve
const results = await vectorStore.similaritySearch("query", 3);
```

**Why good:** Named constants for chunk parameters, explicit embedding model, `MemoryVectorStore` for prototyping

**See:** [examples/rag.md](examples/rag.md) for full RAG chains, agent-based RAG, and production vector stores

---

### Pattern 7: Streaming

All Runnables support `.stream()`. Streaming propagates through LCEL chains.

```typescript
const chain = prompt.pipe(model).pipe(parser);

const stream = await chain.stream({ text: "Explain quantum computing." });
for await (const chunk of stream) {
  process.stdout.write(chunk);
}
```

**Why good:** Streaming propagates through the entire chain, progressive output for better UX

```typescript
// BAD: Collecting all output then displaying
const result = await chain.invoke({ text: "..." });
console.log(result); // User waits for full response
```

**Why bad:** User waits for full generation before seeing anything, bad UX for long responses

**See:** [examples/streaming.md](examples/streaming.md) for model streaming, stream events, agent streaming

---

### Pattern 8: LangSmith Tracing

Enable tracing by setting environment variables. No code changes needed.

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_PROJECT=my-project
# Recommended for non-serverless environments:
LANGCHAIN_CALLBACKS_BACKGROUND=true
```

**Why good:** Zero-code setup, traces every chain/model/tool invocation, `LANGCHAIN_CALLBACKS_BACKGROUND=true` reduces latency in long-running processes

**See:** [reference.md](reference.md) for all environment variables

</patterns>

---

<decision_framework>

## Decision Framework

### When to Use LangChain vs Direct SDK

```
Do you need multi-step LLM workflows (prompt -> model -> parser -> ...)?
+-- YES -> Use LangChain (LCEL chains)
+-- NO -> Do you need to swap between LLM providers?
    +-- YES -> Use LangChain (unified chat model interface)
    +-- NO -> Do you need RAG or agent tool calling?
        +-- YES -> Use LangChain
        +-- NO -> Use the provider SDK directly (simpler, fewer deps)
```

### Which Chat Model Class

```
Which provider?
+-- OpenAI -> ChatOpenAI from @langchain/openai
+-- Anthropic -> ChatAnthropic from @langchain/anthropic
+-- Google -> ChatGoogleGenerativeAI from @langchain/google-genai
+-- Runtime selection -> initChatModel("provider:model") from langchain
+-- Other -> Check @langchain/community
```

### LCEL vs createAgent

```
Does the model need to autonomously decide when to call tools?
+-- YES -> createAgent() (handles tool-call loops, state management)
+-- NO -> Is it a fixed sequence of steps?
    +-- YES -> LCEL chain (prompt.pipe(model).pipe(parser))
    +-- NO -> RunnableSequence.from() with branching
```

### Legacy Chain vs LCEL

```
Are you writing new code?
+-- YES -> ALWAYS use LCEL (.pipe()) -- never legacy chains
+-- NO -> Is the existing code using LLMChain/ConversationChain?
    +-- YES -> Migrate to LCEL when touching the code
    +-- NO -> Keep as-is if it works
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using legacy chains (`LLMChain`, `ConversationChain`, `SequentialChain`) instead of LCEL -- these are deprecated
- Mismatched `@langchain/core` versions across packages -- causes `instanceof` checks to fail silently, methods to be undefined, and type errors
- Hardcoding API keys instead of using environment variables
- Manually parsing JSON from LLM text output instead of using `withStructuredOutput()`
- Using `AgentExecutor` for new code instead of `createAgent()`

**Medium Priority Issues:**

- Using camelCase tool names (`getWeather`) instead of snake_case (`get_weather`) -- some providers reject camelCase
- Not adding `.describe()` to Zod schema fields for tools -- model gets no guidance on argument format
- Using `BufferMemory` / `ConversationSummaryMemory` -- these are deprecated, use LangGraph checkpointing or `RunnableWithMessageHistory`
- Not setting `LANGCHAIN_CALLBACKS_BACKGROUND=true` in non-serverless environments -- adds latency to every LLM call when tracing is on
- Importing from `langchain/` (main package) when the import should come from `@langchain/core/` or a provider package

**Common Mistakes:**

- Installing `langchain` without `@langchain/core` -- `@langchain/core` is a required peer dependency
- Mixing `@langchain/core` v0.x with `langchain` v1.x -- all packages must be on compatible versions
- Using `RunnableLambda` in a chain and expecting `.stream()` to work -- lambda functions do not propagate streaming by default; subclass `Runnable` and implement `transform` instead
- Forgetting that `ChatPromptTemplate.fromTemplate()` creates a single user message -- use `ChatPromptTemplate.fromMessages()` for multi-message prompts with system/assistant/user roles
- Using `MemoryVectorStore` in production -- it is in-memory only, all data is lost on restart; use a persistent vector store

**Gotchas & Edge Cases:**

- `@langchain/core` is a peer dependency, not a transitive dependency. You must install it explicitly: `npm install @langchain/core`. If you see "cannot resolve @langchain/core" or `instanceof` checks failing, you likely have duplicate core versions -- run `npm ls @langchain/core` to check.
- `withStructuredOutput()` uses function calling under the hood, not JSON mode. Not all models support it -- check provider docs. If the model does not support function calling, use `JsonOutputParser` with a prompt instead.
- `ChatPromptTemplate.fromMessages()` uses tuple syntax `["system", "..."]` or `["human", "..."]` -- the role names are `system`, `human`, `ai`, not `developer`, `user`, `assistant`.
- `tool()` from `@langchain/core/tools` vs `tool()` from `langchain` -- both exist. The `langchain` re-export is a convenience wrapper. Use whichever matches your import pattern but be consistent.
- `initChatModel()` requires the provider package to be installed. If you call `initChatModel("anthropic:claude-sonnet-4-20250514")` without `@langchain/anthropic` installed, you get a confusing module resolution error, not a clear "package not installed" message.
- Zod v4 is NOT fully supported by `withStructuredOutput()` as of early 2026 -- stick with Zod v3.x for now.
- `RecursiveCharacterTextSplitter` now lives in `@langchain/textsplitters` (separate package), not `langchain/text_splitter`.
- When using streaming with `createAgent()`, use `streamMode: "values"` to get full state at each step, or omit for incremental updates.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use LCEL pipe composition (`prompt.pipe(model).pipe(parser)`) for all chains -- never use legacy `LLMChain`, `ConversationChain`, or `SequentialChain`)**

**(You MUST ensure all `@langchain/*` packages depend on the same version of `@langchain/core` -- version mismatches cause cryptic runtime errors)**

**(You MUST use `withStructuredOutput(zodSchema)` for structured LLM responses -- never manually parse JSON from completion text)**

**(You MUST use `createAgent()` from `langchain` for new agent code -- `AgentExecutor` and `createToolCallingAgent` are legacy patterns)**

**(You MUST never hardcode API keys -- use environment variables (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.))**

**Failure to follow these rules will produce fragile, hard-to-debug LLM applications with version conflicts and untyped outputs.**

</critical_reminders>
