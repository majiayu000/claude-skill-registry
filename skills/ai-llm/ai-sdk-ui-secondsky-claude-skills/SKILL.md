---
name: ai-sdk-ui
description: "Vercel AI SDK v5 React hooks (useChat, useCompletion, useObject) for AI chat interfaces. Use for React/Next.js AI apps or encountering parse stream errors, no response, streaming issues."

metadata:
  keywords:
    - ai sdk ui
    - useChat hook
    - useCompletion hook
    - useObject hook
    - react ai chat
    - ai chat interface
    - streaming ai ui
    - nextjs ai chat
    - vercel ai ui
    - react streaming
    - ai sdk react
    - chat message state
    - ai file attachments
    - message persistence
    - useChat error
    - streaming failed ui
    - parse stream error
    - useChat no response
    - react ai hooks
    - nextjs app router ai
    - nextjs pages router ai

license: MIT
---
# AI SDK UI - Frontend React Hooks

Frontend React hooks for AI-powered user interfaces with Vercel AI SDK v5.

**Version**: AI SDK v5.0.116 (Stable)
**Framework**: React 18+, Next.js 15+
**Last Updated**: 2025-12-22

## Table of Contents
1. [Quick Start](#quick-start-5-minutes)
2. [When to Load References](#when-to-load-references)
3. [useChat Hook](#usechat-hook---complete-reference)
4. [useCompletion Hook](#usecompletion-hook---complete-reference)
5. [useObject Hook](#useobject-hook---complete-reference)
6. [Next.js Integration](#nextjs-integration)
7. [Top UI Errors & Solutions](#top-ui-errors--solutions)
8. [Streaming Best Practices](#streaming-best-practices)
9. [When to Use This Skill](#when-to-use-this-skill)
10. [Package Versions](#package-versions)

---

## Quick Start (5 Minutes)

### Installation

```bash
bun add ai @ai-sdk/openai  # preferred
# or: bun add ai @ai-sdk/openai
```

### Basic Chat Component (v5)

```tsx
// app/chat/page.tsx
'use client';
import { useChat } from 'ai/react';
import { useState, FormEvent } from 'react';

export default function Chat() {
  const { messages, sendMessage, isLoading } = useChat({
    api: '/api/chat',
  });
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    sendMessage({ content: input });
    setInput('');
  };

  return (
    <div>
      <div>
        {messages.map(m => (
          <div key={m.id}>
            <strong>{m.role}:</strong> {m.content}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={isLoading}
        />
      </form>
    </div>
  );
}
```

### API Route (Next.js App Router)

```typescript
// app/api/chat/route.ts
import { streamText } from 'ai';
import { openai } from '@ai-sdk/openai';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: openai('gpt-4-turbo'),
    messages,
  });

  return result.toDataStreamResponse();
}
```

**Result**: A functional chat interface with streaming AI responses in ~10 lines of frontend code.

---

## When to Load References

For detailed implementation guides, API references, and advanced patterns, load the following reference files:

| Reference File | Load When... |
|----------------|--------------|
| `references/use-chat-migration.md` | Migrating from v4 to v5, understanding breaking changes |
| `references/streaming-patterns.md` | UI streaming best practices, performance optimization |
| `references/top-ui-errors.md` | Debugging common UI errors, error prevention |
| `references/nextjs-integration.md` | Next.js setup patterns, App vs Pages Router differences |
| `references/links-to-official-docs.md` | Finding official Vercel AI SDK documentation |
| `references/tool-calling-ui.md` | Implementing tool/function calling in chat UI |
| `references/file-attachments-guide.md` | Adding file upload/attachment support to chat |
| `references/message-persistence.md` | Persisting chat history with localStorage |
| `references/use-completion-full-reference.md` | Complete useCompletion API and examples |
| `references/use-object-full-reference.md` | Complete useObject API with Zod schemas |
| `references/nextjs-app-router-full.md` | Full Next.js App Router implementation |
| `references/nextjs-pages-router-full.md` | Full Next.js Pages Router implementation |

---

## useChat Hook - Complete Reference

### Basic Usage (v5 Pattern)

```tsx
'use client';
import { useChat } from 'ai/react';
import { useState, FormEvent } from 'react';

export default function ChatComponent() {
  const { messages, sendMessage, isLoading, error } = useChat({
    api: '/api/chat',
  });
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    sendMessage({ content: input });
    setInput('');
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map(message => (
          <div
            key={message.id}
            className={message.role === 'user' ? 'text-right' : 'text-left'}
          >
            <div className="inline-block p-2 rounded bg-gray-100">
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && <div className="text-gray-500">AI is thinking...</div>}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={isLoading}
          className="w-full p-2 border rounded"
        />
      </form>

      {/* Error */}
      {error && <div className="text-red-500 p-4">{error.message}</div>}
    </div>
  );
}
```

### Full API Reference

```typescript
const {
  // Messages
  messages,           // Message[] - Chat history
  setMessages,        // (messages: Message[]) => void - Update messages

  // Actions
  sendMessage,        // (message: { content: string }) => void - Send message (v5)
  reload,             // () => void - Reload last response
  stop,               // () => void - Stop current generation

  // State
  isLoading,          // boolean - Is AI responding?
  error,              // Error | undefined - Error if any

  // Data
  data,               // any[] - Custom data from stream
  metadata,           // object - Response metadata
} = useChat({
  // Required
  api: '/api/chat',   // API endpoint

  // Optional
  id: 'chat-1',       // Chat ID for persistence
  initialMessages: [], // Initial messages (controlled mode)

  // Callbacks
  onFinish: (message, options) => {},  // Called when response completes
  onError: (error) => {},              // Called on error

  // Configuration
  headers: {},        // Custom headers
  body: {},           // Additional body data
  credentials: 'same-origin', // Fetch credentials

  // Streaming
  streamProtocol: 'data', // 'data' | 'text' (default: 'data')
});
```

### v4 → v5 Breaking Changes

**CRITICAL: useChat no longer manages input state in v5!**

**v4 (OLD - DON'T USE):**
```tsx
const { messages, input, handleInputChange, handleSubmit, append } = useChat();

<form onSubmit={handleSubmit}>
  <input value={input} onChange={handleInputChange} />
</form>
```

**v5 (NEW - CORRECT):**
```tsx
const { messages, sendMessage } = useChat();
const [input, setInput] = useState('');

<form onSubmit={(e) => {
  e.preventDefault();
  sendMessage({ content: input });
  setInput('');
}}>
  <input value={input} onChange={(e) => setInput(e.target.value)} />
</form>
```

**Summary of v5 Changes:**
1. **Input management removed**: `input`, `handleInputChange`, `handleSubmit` no longer exist
2. **`append()` → `sendMessage()`**: New method for sending messages
3. **`onResponse` removed**: Use `onFinish` instead
4. **`initialMessages` → controlled mode**: Use `messages` prop for full control
5. **`maxSteps` removed**: Handle on server-side only

See `references/use-chat-migration.md` for complete migration guide.

**Advanced Features:** useChat supports tool calling (display `message.toolInvocations`), file attachments (`experimental_attachments`), and message persistence (localStorage with `id` + `initialMessages`). See [official docs](https://sdk.vercel.ai/docs/ai-sdk-ui/chatbot) for implementation examples.

---

## useCompletion & useObject Hooks

**useCompletion**: For single-prompt completions (not multi-turn chat). Returns `{ completion, complete, isLoading }`. Call `complete(prompt)` to generate. API route uses `streamText()`.

**useObject**: Stream structured JSON with live updates using Zod schemas. Returns `{ object, submit, isLoading }` where `object` is `Partial<T>` that updates progressively. API route uses `streamObject()`.

See [official docs](https://sdk.vercel.ai/docs/ai-sdk-ui/overview) for complete API references and examples.

---

## Next.js Integration

Complete working examples for both App Router and Pages Router with full chat UI components, API routes, and proper streaming setup.

**📖 Load `references/nextjs-integration.md`** for complete implementation code including:
- **App Router**: Full chat page with auto-scroll, loading states, error handling, and API route
- **Pages Router**: Complete chat implementation with proper streaming setup
- **Key Differences**: `toDataStreamResponse()` vs `pipeDataStreamToResponse()`

---

## Top UI Errors & Solutions

See `references/top-ui-errors.md` for complete documentation. Quick reference:

### 1. useChat Failed to Parse Stream

**Error**: `SyntaxError: Unexpected token in JSON at position X`

**Cause**: API route not returning proper stream format.

**Solution**:
```typescript
// ✅ CORRECT
return result.toDataStreamResponse();

// ❌ WRONG
return new Response(result.textStream);
```

### 2. useChat No Response

**Cause**: API route not streaming correctly.

**Solution**:
```typescript
// App Router - use toDataStreamResponse()
export async function POST(req: Request) {
  const result = streamText({ /* ... */ });
  return result.toDataStreamResponse(); // ✅
}

// Pages Router - use pipeDataStreamToResponse()
export default async function handler(req, res) {
  const result = streamText({ /* ... */ });
  return result.pipeDataStreamToResponse(res); // ✅
}
```

### 3. Streaming Not Working When Deployed

**Cause**: Deployment platform buffering responses.

**Solution**: Vercel auto-detects streaming. Other platforms may need configuration.

### 4. Stale Body Values with useChat

**Cause**: `body` option captured at first render only.

**Solution**:
```typescript
// ❌ WRONG - body captured once
const { userId } = useUser();
const { messages } = useChat({
  body: { userId },  // Stale!
});

// ✅ CORRECT - use controlled mode
const { userId } = useUser();
const { messages, sendMessage } = useChat();

sendMessage({
  content: input,
  data: { userId },  // Fresh on each send
});
```

### 5. React Maximum Update Depth

**Cause**: Infinite loop in useEffect.

**Solution**:
```typescript
// ❌ WRONG
useEffect(() => {
  saveMessages(messages);
}, [messages, saveMessages]); // saveMessages triggers re-render!

// ✅ CORRECT
useEffect(() => {
  saveMessages(messages);
}, [messages]); // Only depend on messages
```

See `references/top-ui-errors.md` for 7 more common errors.

---

## Streaming Best Practices

### Performance

**Always use streaming for better UX:**
```tsx
// ✅ GOOD - Streaming (shows tokens as they arrive)
const { messages } = useChat({ api: '/api/chat' });

// ❌ BAD - Non-streaming (user waits for full response)
const response = await fetch('/api/chat', { method: 'POST' });
```

### UX Patterns

**Show loading states:**
```tsx
{isLoading && <div>AI is typing...</div>}
```

**Provide stop button:**
```tsx
{isLoading && <button onClick={stop}>Stop</button>}
```

**Auto-scroll to latest message:**
```tsx
useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [messages]);
```

**Disable input while loading:**
```tsx
<input disabled={isLoading} />
```

See `references/streaming-patterns.md` for comprehensive best practices.

---

## When to Use This Skill

### Use ai-sdk-ui When:
- Building React chat interfaces
- Implementing AI completions in UI
- Streaming AI responses to frontend
- Building Next.js AI applications
- Handling chat message state
- Displaying tool calls in UI
- Managing file attachments with AI
- Migrating from v4 to v5 (UI hooks)
- Encountering useChat/useCompletion errors

### Don't Use When:
- Need backend AI functionality → Use **ai-sdk-core** instead
- Building non-React frontends (Svelte, Vue) → Check official docs
- Need Generative UI / RSC → See https://ai-sdk.dev/docs/ai-sdk-rsc
- Building native apps → Different SDK required

### Related Skills:
- **ai-sdk-core** - Backend text generation, structured output, tools, agents
- Compose both for full-stack AI applications

---

## Package Versions

**Required:**
```json
{
  "dependencies": {
    "ai": "^5.0.116",
    "@ai-sdk/openai": "^2.0.88",
    "react": "^18.2.0",
    "zod": "^3.23.8",
    "isomorphic-dompurify": "^2.16.0"
  }
}
```

**Next.js:**
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

**Version Notes:**
- AI SDK v5.0.116+ (stable)
- React 18+ (React 19 supported)
- Next.js 14+ recommended (13.4+ works)
- Zod 3.23.8+ for schema validation

---

## Links to Official Documentation

**Core UI Hooks:**
- AI SDK UI Overview: https://ai-sdk.dev/docs/ai-sdk-ui/overview
- useChat: https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
- useCompletion: https://ai-sdk.dev/docs/ai-sdk-ui/completion
- useObject: https://ai-sdk.dev/docs/ai-sdk-ui/object-generation

**Advanced Topics (Link Only):**
- Generative UI (RSC): https://ai-sdk.dev/docs/ai-sdk-rsc/overview
- Stream Protocols: https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocols
- Message Metadata: https://ai-sdk.dev/docs/ai-sdk-ui/message-metadata

**Next.js Integration:**
- Next.js App Router: https://ai-sdk.dev/docs/getting-started/nextjs-app-router
- Next.js Pages Router: https://ai-sdk.dev/docs/getting-started/nextjs-pages-router

**Migration & Troubleshooting:**
- v4→v5 Migration: https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0
- Troubleshooting: https://ai-sdk.dev/docs/troubleshooting
- Common Issues: https://ai-sdk.dev/docs/troubleshooting/common-issues

**Vercel Deployment:**
- Vercel Functions: https://vercel.com/docs/functions
- Streaming on Vercel: https://vercel.com/docs/functions/streaming

---

## Templates

This skill includes the following templates in `templates/`:

1. **use-chat-basic.tsx** - Basic chat with manual input (v5 pattern)
2. **use-chat-tools.tsx** - Chat with tool calling UI rendering
3. **use-chat-attachments.tsx** - File attachments support
4. **use-completion-basic.tsx** - Basic text completion
5. **use-object-streaming.tsx** - Streaming structured data
6. **nextjs-chat-app-router.tsx** - Next.js App Router complete example
7. **nextjs-chat-pages-router.tsx** - Next.js Pages Router complete example
8. **nextjs-api-route.ts** - API route for both App and Pages Router
9. **message-persistence.tsx** - Save/load chat history
10. **custom-message-renderer.tsx** - Custom message components with markdown
11. **package.json** - Dependencies template

## Reference Documents

See `references/` for:

- **use-chat-migration.md** - Complete v4→v5 migration guide
- **streaming-patterns.md** - UI streaming best practices
- **top-ui-errors.md** - 12 common UI errors with solutions
- **nextjs-integration.md** - Next.js setup patterns
- **links-to-official-docs.md** - Organized links to official docs

---

**Production Tested**: WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)
**Last Updated**: 2025-10-22
