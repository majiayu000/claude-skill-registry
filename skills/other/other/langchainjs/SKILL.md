---
name: langchainjs
version: "1.0.0"
description: LangChain.js - TypeScript framework for building LLM-powered applications with agents, chains, RAG, tools, memory, and integrations for OpenAI, Anthropic, Google, and hundreds of other providers
---

# LangChain.js

LangChain.js is a comprehensive TypeScript framework for building applications powered by large language models. It provides standardized interfaces for connecting LLMs with diverse data sources, tools, and external systems through a modular architecture.

## When to Use

- Building AI agents with tool-calling capabilities
- Creating chatbots with conversation memory
- Implementing Retrieval Augmented Generation (RAG) systems
- Connecting LLMs to external data sources and APIs
- Building chains of LLM operations
- Switching between AI providers without code changes
- Streaming LLM responses in real-time
- Implementing structured output from LLMs
- Creating document Q&A systems
- Building semantic search applications

## Core Concepts

### Agents
Autonomous entities that use LLMs to decide which actions to take. Agents can call tools, access memory, and orchestrate complex workflows.

### Chains
Sequences of operations that process inputs through multiple steps. Chains can combine prompts, LLM calls, and post-processing.

### Tools
Functions that agents can call to interact with external systems (APIs, databases, web search, etc.).

### Memory
Short-term and long-term context management for maintaining conversation state and persistent information.

### Retrieval
Integration with vector stores and retrievers for finding relevant documents and context.

### Messages
Structured communication format for chat-based interactions (system, human, AI, tool messages).

### Structured Output
Constraining LLM responses to specific formats and schemas using Zod or JSON Schema.

---

## Installation

### Core Packages

```bash
# Install core packages
npm install langchain @langchain/core

# Or with other package managers
pnpm install langchain @langchain/core
yarn add langchain @langchain/core
bun add langchain @langchain/core
```

**Requirement**: Node.js 20+

### Provider Packages

Install provider-specific packages as needed:

```bash
# OpenAI
npm install @langchain/openai

# Anthropic
npm install @langchain/anthropic

# Google
npm install @langchain/google-genai

# AWS Bedrock
npm install @langchain/aws

# Azure OpenAI
npm install @langchain/azure-openai

# Mistral
npm install @langchain/mistralai

# Cohere
npm install @langchain/cohere

# Ollama (local models)
npm install @langchain/ollama
```

---

## Package Structure

LangChain.js is organized as a monorepo with specialized packages:

| Package | Purpose |
|---------|---------|
| `langchain` | Main entry point, high-level abstractions |
| `@langchain/core` | Base interfaces and foundational abstractions |
| `@langchain/community` | Community-contributed integrations |
| `@langchain/textsplitters` | Text chunking utilities |
| `@langchain/openai` | OpenAI integration |
| `@langchain/anthropic` | Anthropic Claude integration |
| `@langchain/google-genai` | Google AI integration |
| `@langchain/mcp-adapters` | Model Context Protocol adapters |

---

## Supported Environments

- Node.js (ESM/CommonJS) - versions 20.x, 22.x, 24.x
- Cloudflare Workers
- Vercel/Next.js (all execution contexts)
- Supabase Edge Functions
- Modern browsers
- Deno
- Bun

---

## Basic Usage

### Chat Models

```typescript
import { ChatOpenAI } from "@langchain/openai";

// Initialize chat model
const model = new ChatOpenAI({
  modelName: "gpt-4",
  temperature: 0.7,
});

// Simple invocation
const response = await model.invoke("What is the capital of France?");
console.log(response.content);

// With message array
import { HumanMessage, SystemMessage } from "@langchain/core/messages";

const messages = [
  new SystemMessage("You are a helpful assistant."),
  new HumanMessage("What is the capital of France?"),
];

const result = await model.invoke(messages);
```

### Using Anthropic

```typescript
import { ChatAnthropic } from "@langchain/anthropic";

const model = new ChatAnthropic({
  modelName: "claude-sonnet-4-20250514",
  temperature: 0,
});

const response = await model.invoke("Explain quantum computing in simple terms.");
```

### Streaming Responses

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  modelName: "gpt-4",
  streaming: true,
});

// Stream tokens
const stream = await model.stream("Write a poem about coding.");

for await (const chunk of stream) {
  process.stdout.write(chunk.content);
}
```

---

## Prompt Templates

```typescript
import { ChatPromptTemplate } from "@langchain/core/prompts";

// Create template
const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a {role} expert."],
  ["human", "{question}"],
]);

// Format with variables
const formattedPrompt = await prompt.format({
  role: "Python",
  question: "How do I read a file?",
});

// Or chain with model
const chain = prompt.pipe(model);
const response = await chain.invoke({
  role: "Python",
  question: "How do I read a file?",
});
```

### Template Variables

```typescript
import { PromptTemplate } from "@langchain/core/prompts";

const template = PromptTemplate.fromTemplate(
  "Translate the following to {language}: {text}"
);

const result = await template.format({
  language: "Spanish",
  text: "Hello, world!",
});
```

---

## Structured Output

### With Zod Schema

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

const model = new ChatOpenAI({
  modelName: "gpt-4",
});

// Define schema
const Person = z.object({
  name: z.string().describe("The person's name"),
  age: z.number().describe("The person's age"),
  occupation: z.string().describe("The person's job"),
});

// Use withStructuredOutput
const structuredModel = model.withStructuredOutput(Person);

const result = await structuredModel.invoke(
  "Extract info: John is a 30 year old software engineer."
);

console.log(result);
// { name: "John", age: 30, occupation: "software engineer" }
```

### JSON Mode

```typescript
const model = new ChatOpenAI({
  modelName: "gpt-4-turbo",
  modelKwargs: { response_format: { type: "json_object" } },
});
```

---

## Tools and Function Calling

### Defining Tools

```typescript
import { tool } from "@langchain/core/tools";
import { z } from "zod";

// Define a tool with Zod schema
const weatherTool = tool(
  async ({ location }) => {
    // Actual API call would go here
    return `The weather in ${location} is sunny, 72°F`;
  },
  {
    name: "get_weather",
    description: "Get the current weather for a location",
    schema: z.object({
      location: z.string().describe("The city and state, e.g. San Francisco, CA"),
    }),
  }
);

// Bind tools to model
const modelWithTools = model.bindTools([weatherTool]);
```

### Using Tools with Agents

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

const model = new ChatOpenAI({ modelName: "gpt-4" });

const tools = [weatherTool, searchTool, calculatorTool];

// Create ReAct agent
const agent = createReactAgent({
  llm: model,
  tools: tools,
});

// Run agent
const result = await agent.invoke({
  messages: [{ role: "user", content: "What's the weather in NYC?" }],
});
```

---

## Building Agents

### Simple Agent (Under 10 Lines)

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { TavilySearchResults } from "@langchain/community/tools/tavily_search";

const model = new ChatOpenAI({ modelName: "gpt-4" });
const tools = [new TavilySearchResults()];

const agent = createReactAgent({ llm: model, tools });

const response = await agent.invoke({
  messages: [{ role: "user", content: "Search for LangChain news" }],
});
```

### Agent with Memory

```typescript
import { MemorySaver } from "@langchain/langgraph";

const memory = new MemorySaver();

const agent = createReactAgent({
  llm: model,
  tools: tools,
  checkpointSaver: memory,
});

// First conversation
const config = { configurable: { thread_id: "conversation-1" } };

await agent.invoke(
  { messages: [{ role: "user", content: "My name is Alice" }] },
  config
);

// Agent remembers context
await agent.invoke(
  { messages: [{ role: "user", content: "What's my name?" }] },
  config
);
// Response: "Your name is Alice"
```

---

## Chains

### Simple Chain

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

const model = new ChatOpenAI();
const prompt = ChatPromptTemplate.fromTemplate("Tell me a joke about {topic}");
const outputParser = new StringOutputParser();

// Create chain using pipe
const chain = prompt.pipe(model).pipe(outputParser);

const result = await chain.invoke({ topic: "programming" });
```

### Runnable Sequence

```typescript
import { RunnableSequence } from "@langchain/core/runnables";

const chain = RunnableSequence.from([
  {
    topic: (input) => input.topic,
    language: (input) => input.language,
  },
  prompt,
  model,
  outputParser,
]);

const result = await chain.invoke({
  topic: "cats",
  language: "French",
});
```

### Parallel Execution

```typescript
import { RunnableParallel } from "@langchain/core/runnables";

const parallel = RunnableParallel.from({
  joke: jokeChain,
  poem: poemChain,
  fact: factChain,
});

const results = await parallel.invoke({ topic: "space" });
// { joke: "...", poem: "...", fact: "..." }
```

---

## RAG (Retrieval Augmented Generation)

### Document Loading

```typescript
import { TextLoader } from "langchain/document_loaders/fs/text";
import { PDFLoader } from "@langchain/community/document_loaders/fs/pdf";
import { WebLoader } from "langchain/document_loaders/web/cheerio";

// Load text file
const textLoader = new TextLoader("./document.txt");
const textDocs = await textLoader.load();

// Load PDF
const pdfLoader = new PDFLoader("./document.pdf");
const pdfDocs = await pdfLoader.load();

// Load web page
const webLoader = new WebLoader("https://example.com/article");
const webDocs = await webLoader.load();
```

### Text Splitting

```typescript
import { RecursiveCharacterTextSplitter } from "@langchain/textsplitters";

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
});

const chunks = await splitter.splitDocuments(docs);
```

### Vector Store

```typescript
import { OpenAIEmbeddings } from "@langchain/openai";
import { MemoryVectorStore } from "langchain/vectorstores/memory";

const embeddings = new OpenAIEmbeddings();

// Create vector store
const vectorStore = await MemoryVectorStore.fromDocuments(
  chunks,
  embeddings
);

// Search for similar documents
const results = await vectorStore.similaritySearch(
  "What is the main topic?",
  3  // Return top 3 results
);
```

### RAG Chain

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { createStuffDocumentsChain } from "langchain/chains/combine_documents";
import { createRetrievalChain } from "langchain/chains/retrieval";

const model = new ChatOpenAI();

// Create retriever from vector store
const retriever = vectorStore.asRetriever();

// Create RAG prompt
const ragPrompt = ChatPromptTemplate.fromTemplate(`
Answer the question based on the following context:

Context: {context}

Question: {input}
`);

// Build RAG chain
const combineDocsChain = await createStuffDocumentsChain({
  llm: model,
  prompt: ragPrompt,
});

const ragChain = await createRetrievalChain({
  retriever,
  combineDocsChain,
});

// Query
const response = await ragChain.invoke({
  input: "What is discussed in the document?",
});

console.log(response.answer);
```

---

## Memory

### Conversation Buffer Memory

```typescript
import { BufferMemory } from "langchain/memory";
import { ConversationChain } from "langchain/chains";

const memory = new BufferMemory();

const chain = new ConversationChain({
  llm: model,
  memory: memory,
});

await chain.call({ input: "Hi, I'm Bob" });
await chain.call({ input: "What's my name?" });
// Remembers: "Your name is Bob"
```

### Message History

```typescript
import { ChatMessageHistory } from "@langchain/community/stores/message/in_memory";

const messageHistory = new ChatMessageHistory();

await messageHistory.addUserMessage("Hello!");
await messageHistory.addAIMessage("Hi there! How can I help?");

const messages = await messageHistory.getMessages();
```

---

## Callbacks and Streaming

### Custom Callbacks

```typescript
import { BaseCallbackHandler } from "@langchain/core/callbacks/base";

class MyHandler extends BaseCallbackHandler {
  name = "MyHandler";

  async handleLLMStart(llm, prompts) {
    console.log("LLM starting with prompts:", prompts);
  }

  async handleLLMEnd(output) {
    console.log("LLM finished:", output);
  }

  async handleLLMError(error) {
    console.error("LLM error:", error);
  }
}

const model = new ChatOpenAI({
  callbacks: [new MyHandler()],
});
```

### Streaming with Callbacks

```typescript
const model = new ChatOpenAI({
  streaming: true,
  callbacks: [
    {
      handleLLMNewToken(token) {
        process.stdout.write(token);
      },
    },
  ],
});

await model.invoke("Write a story about a robot.");
```

---

## Output Parsers

### String Parser

```typescript
import { StringOutputParser } from "@langchain/core/output_parsers";

const parser = new StringOutputParser();
const chain = prompt.pipe(model).pipe(parser);
```

### JSON Parser

```typescript
import { JsonOutputParser } from "@langchain/core/output_parsers";

const parser = new JsonOutputParser();
```

### List Parser

```typescript
import { CommaSeparatedListOutputParser } from "@langchain/core/output_parsers";

const parser = new CommaSeparatedListOutputParser();
const chain = prompt.pipe(model).pipe(parser);

const result = await chain.invoke({ topic: "colors" });
// ["red", "blue", "green", ...]
```

---

## LangGraph Integration

LangChain agents are built on top of LangGraph for advanced orchestration:

```typescript
import { StateGraph, END } from "@langchain/langgraph";

// Define state
interface AgentState {
  messages: BaseMessage[];
  next: string;
}

// Create graph
const graph = new StateGraph<AgentState>({
  channels: {
    messages: { value: (a, b) => [...a, ...b] },
    next: { value: (_, b) => b },
  },
});

// Add nodes
graph.addNode("agent", agentNode);
graph.addNode("tools", toolsNode);

// Add edges
graph.addEdge("agent", "tools");
graph.addConditionalEdges("tools", shouldContinue);

// Compile
const app = graph.compile();
```

---

## LangSmith Integration

Monitor and debug LLM applications:

```typescript
// Set environment variables
process.env.LANGCHAIN_TRACING_V2 = "true";
process.env.LANGCHAIN_API_KEY = "your-api-key";
process.env.LANGCHAIN_PROJECT = "my-project";

// All LangChain operations are now traced
const result = await chain.invoke({ input: "Hello" });
// View traces at smith.langchain.com
```

---

## Common Integrations

### Vector Stores

```typescript
// Pinecone
import { Pinecone } from "@pinecone-database/pinecone";
import { PineconeStore } from "@langchain/pinecone";

// Chroma
import { Chroma } from "@langchain/community/vectorstores/chroma";

// Supabase
import { SupabaseVectorStore } from "@langchain/community/vectorstores/supabase";

// Weaviate
import { WeaviateStore } from "@langchain/weaviate";

// Qdrant
import { QdrantVectorStore } from "@langchain/qdrant";
```

### Document Loaders

```typescript
// File loaders
import { TextLoader } from "langchain/document_loaders/fs/text";
import { JSONLoader } from "langchain/document_loaders/fs/json";
import { CSVLoader } from "@langchain/community/document_loaders/fs/csv";

// Web loaders
import { CheerioWebBaseLoader } from "@langchain/community/document_loaders/web/cheerio";
import { PlaywrightWebBaseLoader } from "@langchain/community/document_loaders/web/playwright";

// API loaders
import { NotionLoader } from "@langchain/community/document_loaders/web/notion";
import { GitHubLoader } from "@langchain/community/document_loaders/web/github";
```

### Tools

```typescript
// Search
import { TavilySearchResults } from "@langchain/community/tools/tavily_search";
import { SerpAPI } from "@langchain/community/tools/serpapi";

// Code execution
import { PythonREPL } from "@langchain/community/tools/python";

// APIs
import { WikipediaQueryRun } from "@langchain/community/tools/wikipedia";
import { Calculator } from "@langchain/community/tools/calculator";
```

---

## Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
GOOGLE_API_KEY=...

# LangSmith (tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=my-project

# Vector stores
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...
```

---

## Project Statistics

- **16.7k GitHub stars**
- **3k forks**
- **1,055 contributors**
- **7,264 commits**
- **548+ releases**
- **48.9k dependent projects**
- **95.6% TypeScript**

---

## Resources

- **Repository**: https://github.com/langchain-ai/langchainjs
- **Documentation**: https://docs.langchain.com/oss/javascript/langchain/overview
- **LangSmith**: https://smith.langchain.com
- **LangGraph**: https://langchain-ai.github.io/langgraphjs/
- **Discord**: https://discord.gg/langchain
- **License**: MIT

---

## Best Practices

### Model Selection
- Use `gpt-4` or `claude-sonnet-4-20250514` for complex reasoning
- Use `gpt-3.5-turbo` or `claude-haiku` for simple tasks (cost-effective)
- Use streaming for better UX in chat applications

### Memory Management
- Use `MemorySaver` for conversation persistence
- Clear memory when starting new topics
- Consider token limits when storing history

### RAG Optimization
- Chunk documents appropriately (1000-2000 chars)
- Use overlap (10-20% of chunk size)
- Rerank results for better relevance
- Consider hybrid search (semantic + keyword)

### Error Handling
```typescript
try {
  const result = await chain.invoke(input);
} catch (error) {
  if (error.message.includes("rate limit")) {
    // Implement retry with backoff
  } else if (error.message.includes("context length")) {
    // Reduce input size
  }
}
```

### Testing
```typescript
// Use LangSmith for evaluation
import { evaluate } from "langsmith/evaluation";

await evaluate(
  (input) => chain.invoke(input),
  {
    data: "my-dataset",
    evaluators: [accuracy, relevance],
  }
);
```

---

## Troubleshooting

### "API key not found"
```bash
export OPENAI_API_KEY=sk-...
# Or set in code
const model = new ChatOpenAI({ openAIApiKey: "sk-..." });
```

### "Context length exceeded"
- Reduce input size
- Use text splitter for long documents
- Implement summarization for conversation history

### "Rate limit exceeded"
- Implement exponential backoff
- Use caching for repeated queries
- Consider batch processing

### "Module not found"
```bash
# Install specific provider package
npm install @langchain/openai

# Or community package
npm install @langchain/community
```
