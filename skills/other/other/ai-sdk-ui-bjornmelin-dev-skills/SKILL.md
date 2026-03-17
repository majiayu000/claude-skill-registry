---
name: ai-sdk-ui
description: |
  Expert guidance for building chat UIs with AI SDK React hooks.
  Use when: (1) Building chatbots with useChat hook,
  (2) Implementing tool UIs with server/client execution,
  (3) Handling message persistence and stream resumption,
  (4) Creating generative UI with React components,
  (5) Integrating with Next.js/Node/Fastify/Nest backends,
  (6) Using useObject for streaming structured data.
  Triggers: useChat, useObject, useCompletion, chat UI, chatbot, generative UI, message persistence, @ai-sdk/react, UIMessage, tool parts, streaming UI, toUIMessageStreamResponse.
---

# AI SDK UI - Chat & Generative UI Framework

AI SDK UI provides framework-agnostic hooks for building interactive chat, completion, and assistant applications with real-time streaming and state management.

## Quick Start: Basic Chat

### Client (React)

```tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { useState } from 'react';

export default function Chat() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  });
  const [input, setInput] = useState('');

  return (
    <>
      {messages.map(message => (
        <div key={message.id}>
          {message.role === 'user' ? 'User: ' : 'AI: '}
          {message.parts.map((part, index) =>
            part.type === 'text' ? <span key={index}>{part.text}</span> : null
          )}
        </div>
      ))}

      <form onSubmit={e => {
        e.preventDefault();
        if (input.trim()) {
          sendMessage({ text: input });
          setInput('');
        }
      }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={status !== 'ready'}
        />
        <button type="submit" disabled={status !== 'ready'}>
          Submit
        </button>
      </form>
    </>
  );
}
```

### Server (Next.js App Router)

```ts
import { convertToModelMessages, streamText, UIMessage } from 'ai';
import { openai } from '@ai-sdk/openai';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: openai('gpt-4o'),
    system: 'You are a helpful assistant.',
    messages: await convertToModelMessages(messages), // v6: now async
  });

  return result.toUIMessageStreamResponse();
}
```

## Hook Selection Guide

| Hook | Use Case | Stream Type | Best For |
|------|----------|-------------|----------|
| `useChat` | Multi-turn conversations | Messages with parts (text, tools, files) | Chatbots, assistants, tool-calling UIs |
| `useObject` | Structured data streaming | Typed objects with Zod schema | Forms, dashboards, real-time data |
| `useCompletion` | Single-turn text generation | Plain text | Autocomplete, simple generation |

**Decision tree:**
- Need conversation history + tools? → `useChat`
- Need typed/structured streaming data? → `useObject`
- Need simple text completion? → `useCompletion`

## Core Patterns

### 1. Status Management

```tsx
const { status, stop } = useChat();

// status values: 'submitted' | 'streaming' | 'ready' | 'error'

{(status === 'submitted' || status === 'streaming') && (
  <div>
    {status === 'submitted' && <Spinner />}
    <button onClick={() => stop()}>Stop</button>
  </div>
)}
```

### 2. Error Handling

```tsx
const { error, reload } = useChat();

{error && (
  <>
    <div>An error occurred.</div>
    <button onClick={() => reload()}>Retry</button>
  </>
)}
```

**Server-side error messages:**

```ts
return result.toUIMessageStreamResponse({
  onError: error => {
    if (error instanceof Error) return error.message;
    return 'Unknown error';
  },
});
```

### 3. Message Modification

```tsx
const { messages, setMessages } = useChat();

const handleDelete = (id: string) => {
  setMessages(messages.filter(m => m.id !== id));
};

const handleEdit = (id: string, newText: string) => {
  setMessages(messages.map(m =>
    m.id === id
      ? { ...m, parts: [{ type: 'text', text: newText }] }
      : m
  ));
};
```

### 4. File Attachments

```tsx
const [files, setFiles] = useState<FileList | undefined>();

<form onSubmit={e => {
  e.preventDefault();
  sendMessage({ text: input, files });
  setFiles(undefined);
}}>
  <input
    type="file"
    onChange={e => setFiles(e.target.files ?? undefined)}
    multiple
  />
</form>
```

### 5. Custom Request Options

```tsx
// Per-request customization (recommended)
sendMessage(
  { text: input },
  {
    headers: { Authorization: 'Bearer token' },
    body: { temperature: 0.7, user_id: '123' },
    metadata: { sessionId: 'abc' },
  }
);

// Hook-level configuration
const { sendMessage } = useChat({
  transport: new DefaultChatTransport({
    api: '/api/chat',
    headers: () => ({ Authorization: `Bearer ${getToken()}` }),
    body: { systemContext: 'expert' },
  }),
});
```

### 6. Message Metadata

```ts
// Server: Attach metadata
return result.toUIMessageStreamResponse({
  messageMetadata: ({ part }) => {
    if (part.type === 'start') {
      return { createdAt: Date.now(), model: 'gpt-4o' };
    }
    if (part.type === 'finish') {
      return { totalTokens: part.totalUsage.totalTokens };
    }
  },
});
```

```tsx
// Client: Access metadata
{messages.map(m => (
  <div key={m.id}>
    {m.metadata?.createdAt && new Date(m.metadata.createdAt).toLocaleString()}
    {m.parts.map(part => part.type === 'text' ? part.text : null)}
    {m.metadata?.totalTokens && <span>{m.metadata.totalTokens} tokens</span>}
  </div>
))}
```

### 7. Regenerate & Stop

```tsx
const { regenerate, stop, status } = useChat();

<>
  <button onClick={stop} disabled={status !== 'streaming'}>
    Stop
  </button>
  <button onClick={regenerate} disabled={!(status === 'ready' || status === 'error')}>
    Regenerate
  </button>
</>
```

## Message Parts Type Reference

Messages use a `parts` array instead of `content` for flexible multi-modal rendering:

```ts
type MessagePart =
  | { type: 'text'; text: string }
  | { type: 'file'; filename: string; mediaType: string; url: string }
  | { type: 'tool-invocation'; toolName: string; input: unknown; result?: unknown }
  | { type: 'tool-result'; toolName: string; result: unknown }
  | { type: 'reasoning'; text: string }  // DeepSeek R1, Claude 3.7 Sonnet
  | { type: 'source-url'; id: string; url: string; title?: string }  // Perplexity, Google
  | { type: 'source-document'; id: string; title?: string };

// Render pattern
{message.parts.map((part, index) => {
  switch (part.type) {
    case 'text':
      return <span key={index}>{part.text}</span>;
    case 'file':
      return part.mediaType.startsWith('image/')
        ? <img key={index} src={part.url} alt={part.filename} />
        : null;
    case 'reasoning':
      return <pre key={index}>{part.text}</pre>;
    case 'source-url':
      return <a key={index} href={part.url}>{part.title ?? 'Source'}</a>;
    case 'tool-invocation':
      return <ToolUI key={index} tool={part} />;
    default:
      return null;
  }
})}
```

## Framework Support

| Framework | Package | Hooks |
|-----------|---------|-------|
| React | `@ai-sdk/react` | `useChat`, `useCompletion`, `useObject` |
| Vue.js | `@ai-sdk/vue` | `useChat`, `useCompletion`, `useObject` |
| Svelte | `@ai-sdk/svelte` | `Chat`, `Completion`, `StructuredObject` |
| Angular | `@ai-sdk/angular` | `Chat`, `Completion`, `StructuredObject` |
| SolidJS | `ai-sdk-solid` (community) | `useChat`, `useCompletion`, `useObject` |

## AI Elements (shadcn/ui Components)

Pre-built UI components for chat interfaces: https://ai-sdk.dev/elements

Includes: Message bubbles, input fields, tool UIs, and more.

## Reference Navigation

| Reference | Topics |
|-----------|--------|
| **[usechat-fundamentals.md](./usechat-fundamentals.md)** | Hook API, transport config, status lifecycle, message state |
| **[tool-integration.md](./tool-integration.md)** | Tool calling, client/server execution, tool approval, type inference |
| **[generative-ui.md](./generative-ui.md)** | React components in streams, dynamic UIs, RSC integration |
| **[persistence.md](./persistence.md)** | Message storage, resume streams, optimistic updates, sync patterns |
| **[hooks-reference.md](./hooks-reference.md)** | Complete API for useChat/useObject/useCompletion, options reference |
| **[backend.md](./backend.md)** | Next.js/Node/Fastify/Nest routes, convertToModelMessages, toUIMessageStreamResponse |
| **[production.md](./production.md)** | Error boundaries, retry strategies, throttling, security best practices |
| **[migration.md](./migration.md)** | v6 migration guide, breaking changes, codemod usage |

## Event Callbacks

```tsx
const { messages } = useChat({
  onFinish: ({ message, messages, isAbort, isDisconnect, isError }) => {
    // Log completion, update analytics, trigger side effects
    if (!isError) logMessage(message);
  },
  onError: error => {
    // Custom error handling, fallback UI
    Sentry.captureException(error);
  },
  onData: data => {
    // Process data parts, validate responses
    // Throw error to abort processing
  },
});
```

## Advanced: Custom Transport

```tsx
const { sendMessage } = useChat({
  transport: new DefaultChatTransport({
    prepareSendMessagesRequest: ({ id, messages, trigger, messageId }) => {
      if (trigger === 'submit-user-message') {
        return {
          body: {
            id,
            message: messages[messages.length - 1],
            messageId,
          },
        };
      }
      // Handle regenerate, custom triggers
    },
  }),
});
```

## Type Inference for Tools

```tsx
import { InferUITools, InferAgentUIMessage, ToolSet, UIMessage } from 'ai';

const tools = {
  weather: {
    description: 'Get weather',
    inputSchema: z.object({ location: z.string() }),
    execute: async ({ location }) => `Sunny in ${location}`,
  },
} satisfies ToolSet;

type MyUITools = InferUITools<typeof tools>;
type MyUIMessage = UIMessage<never, never, MyUITools>;
// Or for agent messages:
// type MyAgentUIMessage = InferAgentUIMessage<typeof myAgent>;

const { messages } = useChat<MyUIMessage>();
```

## Reasoning & Sources

```ts
// Enable reasoning (DeepSeek R1, Claude 3.7 Sonnet)
return result.toUIMessageStreamResponse({ sendReasoning: true });

// Enable sources (Perplexity, Google)
return result.toUIMessageStreamResponse({ sendSources: true });
```

```tsx
// Render reasoning and sources
{message.parts.map(part => {
  if (part.type === 'reasoning') return <pre>{part.text}</pre>;
  if (part.type === 'source-url') return <a href={part.url}>{part.title}</a>;
})}
```

## Performance: Throttle Updates

```tsx
const { messages } = useChat({
  experimental_throttle: 50, // React only: throttle to 50ms
});
```

## Plain Text Streams

```tsx
import { TextStreamChatTransport } from 'ai';

const { messages } = useChat({
  transport: new TextStreamChatTransport({ api: '/api/chat' }),
});
```

**Note:** Tools, usage, and finish reasons unavailable with `TextStreamChatTransport`.
