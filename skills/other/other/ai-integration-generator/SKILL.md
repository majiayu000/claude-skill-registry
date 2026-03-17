---
name: ai-integration-generator
description: Generate AI-powered features using Vercel AI SDK — streaming chat routes, useChat/useCompletion hooks, structured output with Zod, and RAG patterns. Use when asked to add AI, chatbot, LLM integration, streaming responses, or AI-powered features.
---

# AI Integration Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Generation Process

1. Determine AI feature type (chat, completion, structured output, tool calling, RAG)
2. Generate API route with streaming
3. Generate UI component with appropriate hook
4. Add error handling and loading states
5. Verify streaming works end-to-end

## Streaming Chat Route

Create `app/api/chat/route.ts`:

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    system: 'You are a helpful assistant.',
    messages,
  });

  return result.toDataStreamResponse();
}
```

### With Anthropic

```typescript
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic('claude-sonnet-4-5-20250929'),
    system: 'You are a helpful assistant.',
    messages,
  });

  return result.toDataStreamResponse();
}
```

## Chat UI Component

```typescript
'use client';

import { useChat } from '@ai-sdk/react';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, error } =
    useChat();

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={message.role === 'user' ? 'text-right' : 'text-left'}
          >
            <div
              className={`inline-block rounded-lg px-4 py-2 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-900'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </div>

      {error && (
        <div role="alert" className="p-2 text-red-600 text-sm">
          Something went wrong. Please try again.
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex gap-2 p-4 border-t">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type a message..."
          className="flex-1 rounded-lg border px-4 py-2"
          disabled={isLoading}
          aria-label="Chat message input"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          aria-busy={isLoading}
          className="rounded-lg bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
```

## Completion Route

Create `app/api/completion/route.ts` for single-prompt completion:

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    prompt,
  });

  return result.toDataStreamResponse();
}
```

## Completion UI

```typescript
'use client';

import { useCompletion } from '@ai-sdk/react';

export function CompletionForm() {
  const { completion, input, handleInputChange, handleSubmit, isLoading } =
    useCompletion();

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Enter a prompt..."
          className="flex-1 rounded-lg border px-4 py-2"
          disabled={isLoading}
          aria-label="Completion prompt input"
        />
        <button
          type="submit"
          disabled={isLoading}
          aria-busy={isLoading}
          className="rounded-lg bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
        >
          Generate
        </button>
      </form>

      {completion && (
        <div className="rounded-lg border p-4 whitespace-pre-wrap">
          {completion}
        </div>
      )}
    </div>
  );
}
```

## Structured Output

Use `generateObject()` for typed, non-streaming output with Zod validation:

```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const recipeSchema = z.object({
  name: z.string(),
  ingredients: z.array(
    z.object({
      name: z.string(),
      amount: z.string(),
    })
  ),
  steps: z.array(z.string()),
});

export type Recipe = z.infer<typeof recipeSchema>;

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const { object } = await generateObject({
    model: openai('gpt-4o'),
    schema: recipeSchema,
    prompt,
  });

  return Response.json(object);
}
```

## Tool Calling

Define tools that the model can invoke:

```typescript
import { streamText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    messages,
    tools: {
      getWeather: tool({
        description: 'Get the current weather for a location',
        parameters: z.object({
          location: z.string().describe('City name'),
        }),
        execute: async ({ location }) => {
          // TODO: Call weather API
          return { temperature: 22, condition: 'sunny', location };
        },
      }),
      searchProducts: tool({
        description: 'Search for products in the catalog',
        parameters: z.object({
          query: z.string(),
          maxResults: z.number().default(5),
        }),
        execute: async ({ query, maxResults }) => {
          // TODO: Query database
          return { results: [], query, maxResults };
        },
      }),
    },
    maxSteps: 5,
  });

  return result.toDataStreamResponse();
}
```

### Rendering Tool Results in the Frontend

```typescript
'use client';

import { useChat } from '@ai-sdk/react';

export function ChatWithTools() {
  const { messages, input, handleInputChange, handleSubmit } = useChat();

  return (
    <div>
      {messages.map((message) => (
        <div key={message.id}>
          {message.content}

          {message.toolInvocations?.map((toolInvocation) => {
            if (toolInvocation.state === 'result') {
              return (
                <div key={toolInvocation.toolCallId} className="text-sm text-gray-500">
                  Tool: {toolInvocation.toolName} — Result:{' '}
                  {JSON.stringify(toolInvocation.result)}
                </div>
              );
            }
            return (
              <div key={toolInvocation.toolCallId} className="text-sm text-gray-400">
                Calling {toolInvocation.toolName}...
              </div>
            );
          })}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} aria-label="Message input" />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## RAG Pattern

### Embedding Generation

```typescript
import { embed } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function generateEmbedding(text: string) {
  const { embedding } = await embed({
    model: openai.embedding('text-embedding-3-small'),
    value: text,
  });

  return embedding;
}
```

### Vector Search + Context Injection

```typescript
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { messages } = await req.json();
  const lastMessage = messages[messages.length - 1].content;

  // 1. Generate embedding for the query
  const queryEmbedding = await generateEmbedding(lastMessage);

  // 2. Search vector store for relevant documents
  const relevantDocs = await prisma.$queryRaw`
    SELECT content, 1 - (embedding <=> ${queryEmbedding}::vector) as similarity
    FROM documents
    ORDER BY similarity DESC
    LIMIT 5
  `;

  // 3. Inject context into system prompt
  const context = relevantDocs.map((doc: any) => doc.content).join('\n\n');

  const result = streamText({
    model: openai('gpt-4o'),
    system: `Answer based on the following context:\n\n${context}`,
    messages,
  });

  return result.toDataStreamResponse();
}
```

## Error Handling

### Route-Level Error Handling

```typescript
import { streamText, APICallError } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const result = streamText({
      model: openai('gpt-4o'),
      messages,
    });

    return result.toDataStreamResponse();
  } catch (error) {
    if (APICallError.isInstance(error)) {
      return Response.json(
        { error: 'AI service unavailable' },
        { status: error.statusCode ?? 503 }
      );
    }
    return Response.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```

### Client-Side Error Handling

```typescript
const { messages, error, reload } = useChat({
  onError(error) {
    console.error('Chat error:', error);
  },
});

// In JSX:
{error && (
  <div role="alert">
    <p>Something went wrong.</p>
    <button onClick={() => reload()}>Retry</button>
  </div>
)}
```

## Environment Variables

Add to `.env.local`:

```bash
OPENAI_API_KEY=         # OpenAI API key
ANTHROPIC_API_KEY=      # Anthropic API key (if using Claude)
```

## Completeness Check

After generating an AI integration, verify that: the route exports a POST handler with `streamText` or `generateObject`, the UI component uses the correct hook (`useChat` for chat, `useCompletion` for completion), error and loading states are handled in both the route and the UI, streaming responses return `result.toDataStreamResponse()`, and the required API key environment variable is documented. If using tools, verify each tool has a Zod parameters schema and an `execute` function.

## Asset

See `assets/chat-route/route.ts` for a minimal streaming chat route template.
