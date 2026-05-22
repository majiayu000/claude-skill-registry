---
name: genkit
description: Build production-ready AI workflows using Firebase Genkit. Use when creating flows, tool-calling agents, RAG pipelines, multi-agent systems, or deploying AI to Firebase/Cloud Run. Supports TypeScript, Go, and Python with Gemini, OpenAI, Anthropic, Ollama, and Vertex AI plugins.
metadata:
  tags: genkit, firebase, ai, llm, flows, agents, rag, gemini, typescript, google-cloud
  platforms: Claude, ChatGPT, Gemini, Codex
  version: 1.0.0
---


# Firebase Genkit

## When to use this skill

- **AI workflow orchestration**: Building multi-step AI pipelines with type-safe inputs/outputs
- **Flow-based APIs**: Wrapping LLM calls into deployable HTTP endpoints
- **Tool calling / agents**: Equipping models with custom tools and implementing agentic loops
- **RAG pipelines**: Retrieval-augmented generation with vector databases (Pinecone, pgvector, Firestore, Chroma, etc.)
- **Multi-agent systems**: Coordinating multiple specialized AI agents
- **Streaming responses**: Real-time token-by-token output for chat or long-form content
- **Firebase/Cloud Run deployment**: Deploying AI functions to Google Cloud
- **Prompt management**: Managing prompts as versioned `.prompt` files with Dotprompt

---

## Installation & Setup

### Step 1: Install the Genkit CLI

```bash
# npm (recommended for JavaScript/TypeScript)
npm install -g genkit-cli

# macOS/Linux binary
curl -sL cli.genkit.dev | bash
```

### Step 2: Create a TypeScript project

```bash
mkdir my-genkit-app && cd my-genkit-app
npm init -y
npm pkg set type=module
npm install -D typescript tsx
npx tsc --init
mkdir src && touch src/index.ts
```

### Step 3: Install Genkit core and a model plugin

```bash
# Core + Google AI (Gemini) — free tier, no credit card required
npm install genkit @genkit-ai/google-genai

# Or: Vertex AI (requires GCP project)
npm install genkit @genkit-ai/vertexai

# Or: OpenAI
npm install genkit genkitx-openai

# Or: Anthropic (Claude)
npm install genkit genkitx-anthropic

# Or: Ollama (local models)
npm install genkit genkitx-ollama
```

### Step 4: Configure API Key

```bash
# Google AI (Gemini)
export GEMINI_API_KEY=your_key_here

# OpenAI
export OPENAI_API_KEY=your_key_here

# Anthropic
export ANTHROPIC_API_KEY=your_key_here
```

---

## Core Concepts

### Initializing Genkit

```typescript
import { googleAI } from '@genkit-ai/google-genai';
import { genkit } from 'genkit';

const ai = genkit({
  plugins: [googleAI()],
  model: googleAI.model('gemini-2.5-flash'), // default model
});
```

### Defining Flows

Flows are the core primitive: type-safe, observable, deployable AI functions.

```typescript
import { genkit, z } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';

const ai = genkit({ plugins: [googleAI()] });

// Input/output schemas with Zod
const SummaryInputSchema = z.object({
  text: z.string().describe('Text to summarize'),
  maxWords: z.number().optional().default(100),
});

const SummaryOutputSchema = z.object({
  summary: z.string(),
  keyPoints: z.array(z.string()),
});

export const summarizeFlow = ai.defineFlow(
  {
    name: 'summarizeFlow',
    inputSchema: SummaryInputSchema,
    outputSchema: SummaryOutputSchema,
  },
  async ({ text, maxWords }) => {
    const { output } = await ai.generate({
      model: googleAI.model('gemini-2.5-flash'),
      prompt: `Summarize the following text in at most ${maxWords} words and extract key points:\n\n${text}`,
      output: { schema: SummaryOutputSchema },
    });

    if (!output) throw new Error('No output generated');
    return output;
  }
);

// Call the flow
const result = await summarizeFlow({
  text: 'Long article content here...',
  maxWords: 50,
});
console.log(result.summary);
```

### Generating Content

```typescript
// Simple text generation
const { text } = await ai.generate({
  model: googleAI.model('gemini-2.5-flash'),
  prompt: 'Explain quantum computing in one sentence.',
});

// Structured output
const { output } = await ai.generate({
  prompt: 'List 3 programming languages with their use cases',
  output: {
    schema: z.object({
      languages: z.array(z.object({
        name: z.string(),
        useCase: z.string(),
      })),
    }),
  },
});

// With system prompt
const { text: response } = await ai.generate({
  system: 'You are a senior TypeScript engineer. Be concise.',
  prompt: 'What is the difference between interface and type in TypeScript?',
});

// Multimodal (image + text)
const { text: description } = await ai.generate({
  prompt: [
    { text: 'What is in this image?' },
    { media: { url: 'https://example.com/image.jpg', contentType: 'image/jpeg' } },
  ],
});
```

### Streaming Flows

```typescript
export const streamingFlow = ai.defineFlow(
  {
    name: 'streamingFlow',
    inputSchema: z.object({ topic: z.string() }),
    streamSchema: z.string(),        // type of each chunk
    outputSchema: z.object({ full: z.string() }),
  },
  async ({ topic }, { sendChunk }) => {
    const { stream, response } = ai.generateStream({
      prompt: `Write a detailed essay about ${topic}.`,
    });

    for await (const chunk of stream) {
      sendChunk(chunk.text);         // stream each token to client
    }

    const { text } = await response;
    return { full: text };
  }
);

// Client-side consumption
const stream = streamingFlow.stream({ topic: 'AI ethics' });
for await (const chunk of stream.stream) {
  process.stdout.write(chunk);
}
const finalOutput = await stream.output;
```

### Tool Calling (Agents)

```typescript
import { z } from 'genkit';

// Define tools
const getWeatherTool = ai.defineTool(
  {
    name: 'getWeather',
    description: 'Get current weather for a city',
    inputSchema: z.object({ city: z.string() }),
    outputSchema: z.object({ temp: z.number(), condition: z.string() }),
  },
  async ({ city }) => {
    // Call real weather API
    return { temp: 22, condition: 'sunny' };
  }
);

const searchWebTool = ai.defineTool(
  {
    name: 'searchWeb',
    description: 'Search the web for information',
    inputSchema: z.object({ query: z.string() }),
    outputSchema: z.string(),
  },
  async ({ query }) => {
    // Call search API
    return `Search results for: ${query}`;
  }
);

// Agent flow with tools
export const agentFlow = ai.defineFlow(
  {
    name: 'agentFlow',
    inputSchema: z.object({ question: z.string() }),
    outputSchema: z.string(),
  },
  async ({ question }) => {
    const { text } = await ai.generate({
      prompt: question,
      tools: [getWeatherTool, searchWebTool],
      returnToolRequests: false, // auto-execute tools
    });
    return text;
  }
);
```

### Prompts with Dotprompt

Manage prompts as versioned `.prompt` files:

```
# src/prompts/summarize.prompt
---
model: googleai/gemini-2.5-flash
input:
  schema:
    text: string
    style?: string
output:
  schema:
    summary: string
    sentiment: string
---
Summarize the following text in a {{style, default: "professional"}} tone:

{{text}}

Return JSON with summary and sentiment (positive/negative/neutral).
```

```typescript
// Load and use dotprompt
const summarizePrompt = ai.prompt('summarize');
const { output } = await summarizePrompt({
  text: 'Article content here...',
  style: 'casual',
});
```

### RAG — Retrieval-Augmented Generation

```typescript
import { devLocalVectorstore } from '@genkit-ai/dev-local-vectorstore';
import { textEmbedding004 } from '@genkit-ai/google-genai';

const ai = genkit({
  plugins: [
    googleAI(),
    devLocalVectorstore([{
      indexName: 'documents',
      embedder: textEmbedding004,
    }]),
  ],
});

// Index documents
await ai.index({
  indexer: devLocalVectorstoreIndexer('documents'),
  docs: [
    { content: [{ text: 'Document 1 content...' }], metadata: { source: 'doc1' } },
    { content: [{ text: 'Document 2 content...' }], metadata: { source: 'doc2' } },
  ],
});

// RAG flow
export const ragFlow = ai.defineFlow(
  {
    name: 'ragFlow',
    inputSchema: z.object({ question: z.string() }),
    outputSchema: z.string(),
  },
  async ({ question }) => {
    // Retrieve relevant documents
    const docs = await ai.retrieve({
      retriever: devLocalVectorstoreRetriever('documents'),
      query: question,
      options: { k: 3 },
    });

    // Generate answer grounded in retrieved docs
    const { text } = await ai.generate({
      system: 'Answer questions using only the provided context.',
      prompt: question,
      docs,
    });

    return text;
  }
);
```

### Chat Sessions

```typescript
export const chatFlow = ai.defineFlow(
  {
    name: 'chatFlow',
    inputSchema: z.object({ message: z.string(), sessionId: z.string() }),
    outputSchema: z.string(),
  },
  async ({ message, sessionId }) => {
    const session = ai.loadSession(sessionId) ?? ai.createSession({ sessionId });
    const chat = session.chat({
      system: 'You are a helpful assistant.',
    });

    const { text } = await chat.send(message);
    return text;
  }
);
```

### Multi-Agent Systems

```typescript
// Specialist agents
const researchAgent = ai.defineFlow(
  { name: 'researchAgent', inputSchema: z.string(), outputSchema: z.string() },
  async (query) => {
    const { text } = await ai.generate({
      system: 'You are a research expert. Gather facts and cite sources.',
      prompt: query,
      tools: [searchWebTool],
    });
    return text;
  }
);

const writerAgent = ai.defineFlow(
  { name: 'writerAgent', inputSchema: z.string(), outputSchema: z.string() },
  async (brief) => {
    const { text } = await ai.generate({
      system: 'You are a professional writer. Write clear, engaging content.',
      prompt: brief,
    });
    return text;
  }
);

// Orchestrator delegates to specialists
export const contentPipelineFlow = ai.defineFlow(
  {
    name: 'contentPipelineFlow',
    inputSchema: z.object({ topic: z.string() }),
    outputSchema: z.string(),
  },
  async ({ topic }) => {
    const research = await researchAgent(`Research: ${topic}`);
    const article = await writerAgent(`Write an article based on: ${research}`);
    return article;
  }
);
```

---

## Developer Tools

### CLI Commands

```bash
# Start Developer UI + connect to your app
genkit start -- npx tsx --watch src/index.ts
genkit start -o -- npx tsx src/index.ts    # auto-open browser

# Run a specific flow from CLI
genkit flow:run summarizeFlow '{"text": "Hello world", "maxWords": 10}'

# Run with streaming output
genkit flow:run streamingFlow '{"topic": "AI"}' -s

# Evaluate a flow
genkit eval:flow ragFlow --input eval-inputs.json

# View all commands
genkit --help

# Disable analytics telemetry
genkit config set analyticsOptOut true
```

### Developer UI

The Developer UI runs at **http://localhost:4000** and provides:

- **Flow runner**: Execute flows with custom JSON inputs
- **Trace inspector**: Visualize each step (generate, embed, retrieve, tool calls)
- **Prompt playground**: Test prompts interactively
- **Model tester**: Compare outputs across different models
- **Evaluator**: Run evaluation datasets against flows

```bash
# Add npm script for convenience
# package.json
"scripts": {
  "genkit:dev": "genkit start -- npx tsx --watch src/index.ts"
}

npm run genkit:dev
```

---

## Deployment

### Firebase Cloud Functions

```typescript
import { onCallGenkit } from 'firebase-functions/https';
import { defineSecret } from 'firebase-functions/params';

const apiKey = defineSecret('GOOGLE_AI_API_KEY');

export const summarize = onCallGenkit(
  { secrets: [apiKey] },
  summarizeFlow
);
```

```bash
firebase deploy --only functions
```

### Express.js Server

```typescript
import express from 'express';
import { expressHandler } from 'genkit/express';

const app = express();
app.use(express.json());

app.post('/summarize', expressHandler(summarizeFlow));
app.post('/chat', expressHandler(chatFlow));

app.listen(3000, () => console.log('Server running on port 3000'));
```

### Cloud Run

```bash
# Build and deploy
gcloud run deploy genkit-app \
  --source . \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY
```

---

## Supported Plugins

### Model Providers

| Plugin | Package | Models |
|--------|---------|--------|
| Google AI | `@genkit-ai/google-genai` | Gemini 2.5 Flash/Pro |
| Vertex AI | `@genkit-ai/vertexai` | Gemini, Imagen, Claude |
| OpenAI | `genkitx-openai` | GPT-4o, o1, etc. |
| Anthropic | `genkitx-anthropic` | Claude 3.5/3 |
| AWS Bedrock | `genkitx-aws-bedrock` | Claude, Titan, etc. |
| Ollama | `genkitx-ollama` | Local models |
| DeepSeek | `genkitx-deepseek` | DeepSeek-R1 |
| xAI (Grok) | `genkitx-xai` | Grok models |

### Vector Databases

| Plugin | Package |
|--------|---------|
| Dev Local (testing) | `@genkit-ai/dev-local-vectorstore` |
| Pinecone | `genkitx-pinecone` |
| pgvector | `genkitx-pgvector` |
| Chroma | `genkitx-chroma` |
| Cloud Firestore | `@genkit-ai/firebase` |
| LanceDB | `genkitx-lancedb` |

---

## Best Practices

1. **Always define input/output schemas** — Use Zod objects for Dev UI labeled fields and API safety
2. **Use flows for all AI logic** — Even simple calls; flows give you tracing and deployment for free
3. **Store API keys in environment variables** — Never hardcode; use Firebase Secrets for production
4. **Use `ai.run()` to trace custom steps** — Wrap non-Genkit code in `ai.run()` for trace visibility
5. **Stream long-form content** — Use `defineFlow` with `streamSchema` + `sendChunk` for better UX
6. **Separate concerns with agents** — Specialized subflows > one monolithic flow
7. **Use Dotprompt for team prompts** — `.prompt` files enable versioning, review, and reuse

## Constraints

### Must Do
- Define schemas for all flow inputs and outputs
- Handle `null` output from `generate()` — throw meaningful errors
- Set `GENKIT_ENV=dev` when running flows separately from the dev server
- Use `onCallGenkit` (not raw Cloud Functions) when deploying to Firebase

### Must Not Do
- Never hardcode API keys in source code
- Do not use `generate()` outside a flow if you need tracing/observability
- Do not call `genkit start` without a command — always pass `-- <your-run-command>`
- Avoid blocking the event loop in tool handlers — use `async/await`

---

## References

- [Official Docs](https://genkit.dev/docs/overview/)
- [Get Started Guide](https://genkit.dev/docs/get-started/)
- [Developer Tools](https://genkit.dev/docs/devtools/)
- [Flows Reference](https://genkit.dev/docs/flows/)
- [Tool Calling](https://genkit.dev/docs/tool-calling/)
- [RAG Guide](https://genkit.dev/docs/rag/)
- [Multi-Agent Systems](https://genkit.dev/docs/multi-agent/)
- [Dotprompt](https://genkit.dev/docs/dotprompt/)
- [GitHub Repository](https://github.com/firebase/genkit)
- [API References](https://genkit.dev/docs/api-references/)

## Examples

### Example 1: Minimal Flow

```typescript
import { googleAI } from '@genkit-ai/google-genai';
import { genkit, z } from 'genkit';

const ai = genkit({ plugins: [googleAI()] });

export const helloFlow = ai.defineFlow(
  {
    name: 'helloFlow',
    inputSchema: z.object({ name: z.string() }),
    outputSchema: z.string(),
  },
  async ({ name }) => {
    const { text } = await ai.generate(`Say hello to ${name} in a creative way.`);
    return text;
  }
);

// Run it
const greeting = await helloFlow({ name: 'World' });
console.log(greeting);
```

### Example 2: Full RAG + Agent Pipeline

```typescript
import { googleAI, textEmbedding004 } from '@genkit-ai/google-genai';
import { devLocalVectorstore } from '@genkit-ai/dev-local-vectorstore';
import { genkit, z } from 'genkit';

const ai = genkit({
  plugins: [
    googleAI(),
    devLocalVectorstore([{ indexName: 'kb', embedder: textEmbedding004 }]),
  ],
});

// Index knowledge base documents
const indexKnowledgeBase = ai.defineFlow(
  { name: 'indexKB', inputSchema: z.array(z.string()) },
  async (texts) => {
    await ai.index({
      indexer: devLocalVectorstoreIndexer('kb'),
      docs: texts.map(text => ({ content: [{ text }] })),
    });
  }
);

// Answer questions using RAG
export const answerFlow = ai.defineFlow(
  {
    name: 'answerFlow',
    inputSchema: z.object({ question: z.string() }),
    outputSchema: z.object({ answer: z.string(), sources: z.number() }),
  },
  async ({ question }) => {
    const docs = await ai.retrieve({
      retriever: devLocalVectorstoreRetriever('kb'),
      query: question,
      options: { k: 5 },
    });

    const { text } = await ai.generate({
      system: 'Answer only from the provided context. If unsure, say so.',
      prompt: question,
      docs,
    });

    return { answer: text, sources: docs.length };
  }
);
```

### Example 3: Multi-Model Comparison

```typescript
import { googleAI } from '@genkit-ai/google-genai';
import { openAI } from 'genkitx-openai';
import { genkit, z } from 'genkit';

const ai = genkit({ plugins: [googleAI(), openAI()] });

export const compareModelsFlow = ai.defineFlow(
  {
    name: 'compareModelsFlow',
    inputSchema: z.object({ prompt: z.string() }),
    outputSchema: z.object({ gemini: z.string(), gpt4o: z.string() }),
  },
  async ({ prompt }) => {
    const [geminiResult, gptResult] = await Promise.all([
      ai.generate({ model: googleAI.model('gemini-2.5-flash'), prompt }),
      ai.generate({ model: 'openai/gpt-4o', prompt }),
    ]);

    return {
      gemini: geminiResult.text,
      gpt4o: gptResult.text,
    };
  }
);
```
