---
name: langchain-js
description: Builds LLM-powered applications with LangChain.js for chat, agents, and RAG. Use when creating AI applications with chains, memory, tools, and retrieval-augmented generation in JavaScript.
---

# LangChain.js

Framework for building LLM-powered applications. Provides abstractions for chat models, chains, agents, RAG, and memory with support for multiple providers.

## Quick Start

```bash
npm install langchain @langchain/openai @langchain/core
```

### Basic Chat

```typescript
import { ChatOpenAI } from '@langchain/openai';

const model = new ChatOpenAI({
  modelName: 'gpt-4o',
  temperature: 0.7,
});

const response = await model.invoke('What is the capital of France?');
console.log(response.content);
```

## Chat Models

### OpenAI

```typescript
import { ChatOpenAI } from '@langchain/openai';

const model = new ChatOpenAI({
  modelName: 'gpt-4o',
  temperature: 0,
  maxTokens: 1000,
});

const response = await model.invoke([
  { role: 'system', content: 'You are a helpful assistant.' },
  { role: 'user', content: 'Hello!' },
]);
```

### Anthropic

```bash
npm install @langchain/anthropic
```

```typescript
import { ChatAnthropic } from '@langchain/anthropic';

const model = new ChatAnthropic({
  modelName: 'claude-sonnet-4-20250514',
  temperature: 0,
});

const response = await model.invoke('Explain quantum computing');
```

### Google (Gemini)

```bash
npm install @langchain/google-genai
```

```typescript
import { ChatGoogleGenerativeAI } from '@langchain/google-genai';

const model = new ChatGoogleGenerativeAI({
  modelName: 'gemini-pro',
  temperature: 0,
});
```

## Streaming

```typescript
import { ChatOpenAI } from '@langchain/openai';

const model = new ChatOpenAI({
  modelName: 'gpt-4o',
  streaming: true,
});

const stream = await model.stream('Tell me a story');

for await (const chunk of stream) {
  process.stdout.write(chunk.content as string);
}
```

## Prompt Templates

```typescript
import { ChatPromptTemplate } from '@langchain/core/prompts';

const prompt = ChatPromptTemplate.fromMessages([
  ['system', 'You are a {role} assistant.'],
  ['user', '{input}'],
]);

const formattedPrompt = await prompt.format({
  role: 'helpful',
  input: 'What is TypeScript?',
});
```

### With Model Chain

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';

const model = new ChatOpenAI();
const prompt = ChatPromptTemplate.fromMessages([
  ['system', 'Translate the following to {language}'],
  ['user', '{text}'],
]);

const chain = prompt.pipe(model);

const response = await chain.invoke({
  language: 'French',
  text: 'Hello, how are you?',
});
```

## Output Parsers

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { StringOutputParser, JsonOutputParser } from '@langchain/core/output_parsers';

// String output
const stringChain = prompt.pipe(model).pipe(new StringOutputParser());
const text = await stringChain.invoke({ input: 'Hello' });

// JSON output
const jsonChain = prompt.pipe(model).pipe(new JsonOutputParser());
const data = await jsonChain.invoke({ input: 'List 3 colors as JSON' });
```

### Structured Output

```typescript
import { z } from 'zod';
import { ChatOpenAI } from '@langchain/openai';

const model = new ChatOpenAI({ modelName: 'gpt-4o' });

const schema = z.object({
  name: z.string().describe('The person name'),
  age: z.number().describe('The person age'),
  occupation: z.string().describe('The person occupation'),
});

const structuredModel = model.withStructuredOutput(schema);

const result = await structuredModel.invoke(
  'Extract info: John is 30 years old and works as a developer.'
);
// { name: 'John', age: 30, occupation: 'developer' }
```

## Memory (Conversation History)

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate, MessagesPlaceholder } from '@langchain/core/prompts';
import { RunnableWithMessageHistory } from '@langchain/core/runnables';
import { ChatMessageHistory } from 'langchain/memory';

const model = new ChatOpenAI();

const prompt = ChatPromptTemplate.fromMessages([
  ['system', 'You are a helpful assistant.'],
  new MessagesPlaceholder('history'),
  ['user', '{input}'],
]);

const chain = prompt.pipe(model);

// In-memory store
const messageHistories: Record<string, ChatMessageHistory> = {};

const chainWithHistory = new RunnableWithMessageHistory({
  runnable: chain,
  getMessageHistory: async (sessionId) => {
    if (!messageHistories[sessionId]) {
      messageHistories[sessionId] = new ChatMessageHistory();
    }
    return messageHistories[sessionId];
  },
  inputMessagesKey: 'input',
  historyMessagesKey: 'history',
});

// Use with session
const response = await chainWithHistory.invoke(
  { input: 'My name is Alice' },
  { configurable: { sessionId: 'user-123' } }
);

const response2 = await chainWithHistory.invoke(
  { input: 'What is my name?' },
  { configurable: { sessionId: 'user-123' } }
);
// Response includes "Alice"
```

## RAG (Retrieval-Augmented Generation)

```bash
npm install @langchain/openai langchain
```

### Document Loading

```typescript
import { TextLoader } from 'langchain/document_loaders/fs/text';
import { PDFLoader } from 'langchain/document_loaders/fs/pdf';
import { WebLoader } from 'langchain/document_loaders/web/cheerio';

// Load text file
const textLoader = new TextLoader('./document.txt');
const textDocs = await textLoader.load();

// Load PDF
const pdfLoader = new PDFLoader('./document.pdf');
const pdfDocs = await pdfLoader.load();

// Load webpage
const webLoader = new WebLoader('https://example.com');
const webDocs = await webLoader.load();
```

### Text Splitting

```typescript
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';

const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
});

const chunks = await splitter.splitDocuments(docs);
```

### Vector Store

```typescript
import { MemoryVectorStore } from 'langchain/vectorstores/memory';
import { OpenAIEmbeddings } from '@langchain/openai';

const embeddings = new OpenAIEmbeddings();

const vectorStore = await MemoryVectorStore.fromDocuments(
  chunks,
  embeddings
);

// Search
const results = await vectorStore.similaritySearch('query', 4);
```

### Full RAG Chain

```typescript
import { ChatOpenAI, OpenAIEmbeddings } from '@langchain/openai';
import { MemoryVectorStore } from 'langchain/vectorstores/memory';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { createRetrievalChain } from 'langchain/chains/retrieval';
import { createStuffDocumentsChain } from 'langchain/chains/combine_documents';

// Setup
const model = new ChatOpenAI({ modelName: 'gpt-4o' });
const embeddings = new OpenAIEmbeddings();
const vectorStore = await MemoryVectorStore.fromDocuments(chunks, embeddings);
const retriever = vectorStore.asRetriever();

// Prompt
const prompt = ChatPromptTemplate.fromTemplate(`
Answer the question based only on the following context:
{context}

Question: {input}
`);

// Chain
const documentChain = await createStuffDocumentsChain({ llm: model, prompt });
const retrievalChain = await createRetrievalChain({
  combineDocsChain: documentChain,
  retriever,
});

// Query
const response = await retrievalChain.invoke({
  input: 'What is the main topic?',
});

console.log(response.answer);
```

## Agents & Tools

```typescript
import { ChatOpenAI } from '@langchain/openai';
import { TavilySearchResults } from '@langchain/community/tools/tavily_search';
import { Calculator } from '@langchain/community/tools/calculator';
import { createReactAgent } from '@langchain/langgraph/prebuilt';

const model = new ChatOpenAI({ modelName: 'gpt-4o' });

const tools = [
  new TavilySearchResults({ maxResults: 3 }),
  new Calculator(),
];

const agent = createReactAgent({
  llm: model,
  tools,
});

const result = await agent.invoke({
  messages: [{ role: 'user', content: 'What is the weather in Tokyo?' }],
});
```

### Custom Tools

```typescript
import { tool } from '@langchain/core/tools';
import { z } from 'zod';

const weatherTool = tool(
  async ({ location }) => {
    // Call weather API
    return `The weather in ${location} is sunny, 72°F`;
  },
  {
    name: 'get_weather',
    description: 'Get the current weather for a location',
    schema: z.object({
      location: z.string().describe('The city name'),
    }),
  }
);

const tools = [weatherTool];
```

## LangGraph (Advanced Agents)

```bash
npm install @langchain/langgraph
```

```typescript
import { StateGraph, Annotation } from '@langchain/langgraph';

const StateAnnotation = Annotation.Root({
  messages: Annotation<BaseMessage[]>({
    reducer: (x, y) => x.concat(y),
  }),
});

const workflow = new StateGraph(StateAnnotation)
  .addNode('agent', agentNode)
  .addNode('tools', toolNode)
  .addEdge('__start__', 'agent')
  .addConditionalEdges('agent', shouldContinue)
  .addEdge('tools', 'agent');

const app = workflow.compile();

const result = await app.invoke({
  messages: [{ role: 'user', content: 'Search for AI news' }],
});
```

## Next.js API Route

```typescript
// app/api/chat/route.ts
import { ChatOpenAI } from '@langchain/openai';
import { ChatPromptTemplate } from '@langchain/core/prompts';
import { StringOutputParser } from '@langchain/core/output_parsers';
import { StreamingTextResponse, LangChainAdapter } from 'ai';

const model = new ChatOpenAI({ streaming: true });
const prompt = ChatPromptTemplate.fromMessages([
  ['system', 'You are a helpful assistant.'],
  ['user', '{input}'],
]);

const chain = prompt.pipe(model).pipe(new StringOutputParser());

export async function POST(request: Request) {
  const { message } = await request.json();

  const stream = await chain.stream({ input: message });

  return new StreamingTextResponse(LangChainAdapter.toAIStream(stream));
}
```

## Environment Variables

```bash
OPENAI_API_KEY=sk-xxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
GOOGLE_API_KEY=xxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxx
```

## Best Practices

1. **Use structured output** - For reliable data extraction
2. **Stream responses** - Better UX for chat applications
3. **Chunk documents** - Optimize for context windows
4. **Use vector stores** - For efficient similarity search
5. **Add memory** - For conversational context
6. **Use LangGraph** - For complex agent workflows
7. **Type with Zod** - For input/output validation
