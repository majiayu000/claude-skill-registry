---
name: openai-sdk
description: >-
  Integrate OpenAI APIs into applications. Use when a user asks to add GPT or
  ChatGPT to an app, generate text with OpenAI, build a chatbot, use GPT-4 or
  o1 models, generate embeddings, use function calling, stream chat completions,
  build AI features, moderate content, generate images with DALL-E, transcribe
  audio with Whisper API, or integrate any OpenAI model. Covers Chat Completions,
  Assistants API, function calling, embeddings, streaming, vision, DALL-E,
  Whisper, and moderation.
license: Apache-2.0
compatibility: 'Node.js 18+, Python 3.8+'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - openai
    - gpt
    - chatgpt
    - llm
    - ai
    - embeddings
    - function-calling
---

# OpenAI SDK

## Overview

The OpenAI SDK provides access to GPT-4o, o1, DALL-E 3, Whisper, and embedding models. This skill covers the Chat Completions API (text generation, conversation, function calling), streaming responses, vision (image understanding), embeddings, the Assistants API (stateful agents), DALL-E image generation, Whisper transcription, and content moderation. Examples in both TypeScript/Node.js and Python.

## Instructions

### Step 1: Installation and Setup

```bash
# Node.js
npm install openai

# Python
pip install openai
```

```typescript
// lib/openai.ts — Client initialization
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,    // or set OPENAI_API_KEY env var
})
```

### Step 2: Chat Completions

```typescript
// chat.ts — Basic chat completion and conversation
import OpenAI from 'openai'

const openai = new OpenAI()

// Single message
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: 'You are a helpful coding assistant.' },
    { role: 'user', content: 'Write a Python function to merge two sorted lists.' },
  ],
  temperature: 0.7,       // 0 = deterministic, 2 = creative
  max_tokens: 1000,
})

console.log(response.choices[0].message.content)

// Multi-turn conversation (maintain message history)
const messages: OpenAI.ChatCompletionMessageParam[] = [
  { role: 'system', content: 'You are a data analysis assistant.' },
]

async function chat(userMessage: string) {
  messages.push({ role: 'user', content: userMessage })

  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages,
  })

  const assistantMessage = response.choices[0].message
  messages.push(assistantMessage)
  return assistantMessage.content
}
```

### Step 3: Streaming Responses

```typescript
// stream.ts — Stream chat completions for real-time UI
const stream = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Explain quantum computing in simple terms.' }],
  stream: true,
})

for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content || ''
  process.stdout.write(content)    // stream to terminal/UI
}
```

```typescript
// Next.js streaming API route
// app/api/chat/route.ts — Server-sent events for streaming to frontend
import { OpenAIStream, StreamingTextResponse } from 'ai'    // Vercel AI SDK helper

export async function POST(req: Request) {
  const { messages } = await req.json()

  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages,
    stream: true,
  })

  const stream = OpenAIStream(response)
  return new StreamingTextResponse(stream)
}
```

### Step 4: Function Calling (Tool Use)

```typescript
// function_calling.ts — Let GPT call your functions
const tools: OpenAI.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get current weather for a city',
      parameters: {
        type: 'object',
        properties: {
          city: { type: 'string', description: 'City name' },
          units: { type: 'string', enum: ['celsius', 'fahrenheit'] },
        },
        required: ['city'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'search_database',
      description: 'Search the product database',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string' },
          category: { type: 'string' },
          max_price: { type: 'number' },
        },
        required: ['query'],
      },
    },
  },
]

const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'What is the weather in Tokyo?' }],
  tools,
  tool_choice: 'auto',
})

// Handle function call
const toolCall = response.choices[0].message.tool_calls?.[0]
if (toolCall) {
  const args = JSON.parse(toolCall.function.arguments)
  // Execute the actual function
  const result = await getWeather(args.city, args.units)

  // Send result back to GPT
  const finalResponse = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'user', content: 'What is the weather in Tokyo?' },
      response.choices[0].message,
      { role: 'tool', tool_call_id: toolCall.id, content: JSON.stringify(result) },
    ],
    tools,
  })
}
```

### Step 5: Embeddings

```typescript
// embeddings.ts — Generate embeddings for semantic search
const response = await openai.embeddings.create({
  model: 'text-embedding-3-small',    // 1536 dimensions, cheapest
  input: 'How to deploy a Node.js app to production',
})

const embedding = response.data[0].embedding    // number[] of length 1536

// Batch embeddings
const batchResponse = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: [
    'First document text',
    'Second document text',
    'Third document text',
  ],
})
// batchResponse.data[0].embedding, batchResponse.data[1].embedding, etc.
```

### Step 6: Vision (Image Understanding)

```typescript
// vision.ts — Analyze images with GPT-4o
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'What is in this image? Describe in detail.' },
      { type: 'image_url', image_url: { url: 'https://example.com/photo.jpg' } },
    ],
  }],
})

// Base64 image (from file upload)
const base64Image = fs.readFileSync('photo.jpg').toString('base64')
const response2 = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Extract all text from this receipt.' },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${base64Image}` } },
    ],
  }],
})
```

### Step 7: Structured Outputs

```typescript
// structured.ts — Get JSON output matching a schema
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Extract info from: John Smith, 35, Software Engineer at Google, lives in SF' }],
  response_format: {
    type: 'json_schema',
    json_schema: {
      name: 'person_info',
      schema: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          age: { type: 'number' },
          job_title: { type: 'string' },
          company: { type: 'string' },
          city: { type: 'string' },
        },
        required: ['name', 'age', 'job_title', 'company', 'city'],
      },
    },
  },
})
// Guaranteed to match the schema
const person = JSON.parse(response.choices[0].message.content!)
```

## Examples

### Example 1: Build a customer support chatbot with function calling
**User prompt:** "Build a chatbot for our e-commerce site that can check order status, search products, and answer FAQs using our knowledge base."

The agent will:
1. Define tools for `check_order_status`, `search_products`, and `search_knowledge_base`.
2. Create a chat endpoint with streaming for real-time responses.
3. Implement the tool execution loop (GPT calls tool → execute → send result back).
4. Add conversation history management for multi-turn interactions.

### Example 2: Build a document analysis pipeline
**User prompt:** "Users upload contracts (PDF/images). Extract key terms, dates, and parties, then generate a structured summary."

The agent will:
1. Use vision API to extract text from document images.
2. Use structured outputs to extract entities into a typed JSON schema.
3. Generate a plain-language summary with a system prompt tuned for legal documents.

## Guidelines

- Use `gpt-4o` for most tasks — it's the best balance of quality, speed, and cost. Use `gpt-4o-mini` for simple tasks where cost matters.
- Always set a `system` message to define the assistant's behavior, constraints, and output format.
- Use structured outputs (`response_format: json_schema`) when you need reliable JSON — it guarantees schema compliance, unlike asking for JSON in the prompt.
- For function calling, define clear `description` fields — GPT uses these to decide when to call each function.
- Use streaming for any user-facing chat interface — the perceived latency drops dramatically when users see tokens appear in real-time.
- Set `temperature: 0` for deterministic tasks (classification, extraction, code generation) and `0.7-1.0` for creative tasks (writing, brainstorming).
- Track token usage via `response.usage` for cost monitoring. Embedding and completion costs differ significantly.
