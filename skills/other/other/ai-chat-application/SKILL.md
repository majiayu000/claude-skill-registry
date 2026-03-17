---
name: ai-chat-application
model: reasoning
description: Complete guide to building AI chat applications with Vercel AI SDK. Orchestrates streaming routes, useChat integration, tool architecture, message handling, and UX patterns. Use when building production AI chatbots or assistants. Triggers on build AI chat, create chatbot, AI assistant, Vercel AI SDK app, chat application.
---

# AI Chat Application (Meta-Skill)

Complete guide to building production AI chat applications with the Vercel AI SDK.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install ai-chat-application
```


---

## When to Use

- Building a new AI chatbot or assistant
- Adding AI chat features to an existing app
- Need end-to-end guidance on AI chat architecture

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (React)                            │
├─────────────────────────────────────────────────────────────┤
│  useChat Hook                    │  Data Stream Handler     │
│  - messages, input, submit       │  - Custom data events    │
│  - isLoading, error              │  - Message annotations   │
│  See: vercel-ai-chat-integration │  See: vercel-ai-data-streaming
├─────────────────────────────────────────────────────────────┤
│                    API Route (Next.js)                       │
│  - createDataStreamResponse, streamText, message persistence│
│  See: ai-streaming-routes                                    │
├─────────────────────────────────────────────────────────────┤
│                    Tool System                               │
│  - Toolkit composition, singleton factories, error handling │
│  See: ai-tool-composition, vercel-ai-tool-architecture      │
├─────────────────────────────────────────────────────────────┤
│                    Message Handling                          │
│  - DB ↔ UI conversion, sanitization, annotations           │
│  See: ai-message-handling                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Steps

### Step 1: API Route

Create the streaming chat endpoint.

**Read:** `ai/skills/ai-chat/ai-streaming-routes`

```typescript
// app/api/chat/route.ts
export async function POST(request: Request) {
  const { id, messages, modelId } = await request.json();
  
  // Auth, validation, save user message...
  
  return createDataStreamResponse({
    execute: (dataStream) => {
      const result = streamText({
        model: customModel(model),
        system: systemPrompt,
        messages: convertToCoreMessages(messages),
        tools: makeToolkitByName(model.toolkit, params),
        onFinish: async ({ response }) => {
          // Save assistant messages
        },
      });
      result.mergeIntoDataStream(dataStream);
    },
  });
}
```

### Step 2: Chat Component

Build the client-side chat interface.

**Read:** `ai/skills/ai-chat/vercel-ai-chat-integration`

```tsx
// components/chat.tsx
export function Chat({ id, initialMessages }: ChatProps) {
  const { messages, input, handleSubmit, isLoading } = useChat({
    id,
    initialMessages,
    experimental_throttle: 100,
    onError: (error) => toast.error(parseError(error)),
  });

  return (
    <div>
      <Messages messages={messages} isLoading={isLoading} />
      <ChatInput value={input} onSubmit={handleSubmit} />
    </div>
  );
}
```

### Step 3: UX Polish

Add auto-scroll and loading states.

```tsx
const [containerRef, endRef] = useScrollToBottom();

{isLoading && lastMessage?.role === 'user' && <ThinkingMessage />}
```

### Step 4: Tool System

Add function calling capabilities.

**Read:** `ai/skills/ai-chat/ai-tool-composition`

```typescript
// lib/tools/allTools.ts
export function allToolsToolkit(params: ToolkitParams) {
  return {
    ...makeWeb3Tools(params),
    ...makeSearchTools(params),
    getTime: tool({ /* inline tool */ }),
  };
}
```

### Step 5: Message Persistence

Handle message format conversion and persistence.

**Read:** `ai/skills/ai-chat/ai-message-handling`

```typescript
// Convert DB → UI on page load
const uiMessages = convertToUIMessages(dbMessages);

// Sanitize before save
const cleanMessages = sanitizeResponseMessages(response.messages);
```

---

## Component Skills Reference

| Skill | Purpose |
|-------|---------|
| `vercel-ai-chat-integration` | useChat hook patterns |
| `vercel-ai-data-streaming` | Custom data events |
| `vercel-ai-tool-architecture` | Tool system design |
| `ai-streaming-routes` | API route patterns |
| `ai-message-handling` | Format conversion |
| `ai-tool-composition` | Tool factories |
---

## NEVER Do

- **Never skip error handling in useChat** — AI APIs fail; always handle onError
- **Never forget to sanitize messages before persistence** — Incomplete tool calls corrupt DB
- **Never skip throttling for streaming** — Causes janky UI with fast token streams
- **Never expose raw API errors to users** — Parse and show user-friendly messages
- **Never block on tool calls without timeout** — Tools can hang; set maxSteps and timeouts
- **Never save user messages in onFinish** — Save immediately before streaming starts
- **Never forget maxDuration on API route** — Default timeout is too short for AI
- **Never skip message annotations** — Client needs server-generated IDs for persistence
- **Never mutate messages during streaming** — Wait for onFinish before state updates

---

## Quick Start Checklist

- [ ] Create API route with createDataStreamResponse
- [ ] Set up useChat hook in client component
- [ ] Add message persistence (save/load)
- [ ] Implement auto-scroll behavior
- [ ] Add thinking indicator
- [ ] Create tool system (if needed)
- [ ] Define AI persona via system prompt
- [ ] Handle errors gracefully
- [ ] Add throttling for smooth streaming
