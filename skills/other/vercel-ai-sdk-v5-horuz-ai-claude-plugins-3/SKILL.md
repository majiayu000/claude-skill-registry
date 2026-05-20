---
name: vercel-ai-sdk-v5
description: "Expert-level Vercel AI SDK v5 patterns for production chatbots. Use for: (1) Chat persistence with Drizzle/PostgreSQL, (2) Generative UI with typed tool parts, (3) Human-in-the-loop tool confirmations, (4) Custom data streaming with reconciliation, (5) Anthropic provider with extended thinking/reasoning, (6) Type-safe message metadata with token tracking. Covers advanced patterns only - assumes basic AI SDK knowledge. NOT for AI SDK v6."
---

# Vercel AI SDK v5

Production patterns for AI chatbots with persistence, generative UI, and streaming.

## Quick Reference

| Need | Reference |
|------|-----------|
| Database schema & persistence | `references/persistence.md` |
| Tools & generative UI | `references/tools-and-generative-ui.md` |
| Custom data streaming | `references/streaming.md` |
| Type definitions | `references/types.md` |
| Anthropic + reasoning | `references/anthropic-config.md` |
| Working examples | `cookbook/` directory |

## Core Architecture

### Message Flow
```
Client (useChat) → API Route (streamText) → DB (Drizzle)
     ↑                    ↓
     └── UIMessageStream ←┘
```

### Key Imports
```typescript
// Core
import { streamText, convertToModelMessages, UIMessage } from 'ai'
import { createUIMessageStream, createUIMessageStreamResponse } from 'ai'

// Client
import { useChat } from '@ai-sdk/react'
import { DefaultChatTransport } from 'ai'

// Provider
import { anthropic } from '@ai-sdk/anthropic'
```

## Decision Tree

### Streaming Response Type
- Simple text streaming → `streamText().toUIMessageStreamResponse()`
- Need custom data parts → `createUIMessageStream()` + `writer.write()`
- Need both → `createUIMessageStream()` + `writer.merge(result.toUIMessageStream())`

### Tool Execution Location
- Has server-side data/secrets → Server tool with `execute`
- Needs client confirmation → Client tool (no execute) + `addToolOutput`
- Auto-runs on client → Client tool + `onToolCall` handler

### Data Attachment
- Message-level info (tokens, model, timestamps) → `messageMetadata`
- Dynamic content in message → Data parts with `writer.write()`
- Temporary status (not persisted) → Transient data parts

## Naming Convention

This skill uses `agents` instead of `chats` for all database tables, routes, and methods:
- Table: `agents` (not `chats`)
- Foreign keys: `agentId` (not `chatId`)
- Actions: `createAgent()`, `loadAgent()`, `deleteAgent()`

## File Organization

Follow feature-based architecture:
```
features/
└── agents/
    ├── data/
    │   └── get-agent.ts
    ├── actions/
    │   └── create-agent.ts
    ├── types/
    │   └── message.ts
    └── components/
        ├── server/
        │   └── agent-messages.tsx
        └── client/
            └── chat-input.tsx

db/
├── schema.ts      # Table definitions
├── relations.ts   # Drizzle relations
└── actions.ts     # DB operations (upsert, load, delete)
```

## Essential Patterns

### 1. Send Only Last Message
```typescript
// Client
transport: new DefaultChatTransport({
  api: '/api/agent',
  prepareSendMessagesRequest: ({ messages, id }) => ({
    body: { message: messages.at(-1), agentId: id }
  })
})

// Server: Load history, append new message
const previous = await loadAgent(agentId)
const messages = [...previous, message]
```

### 2. Persist on Finish
```typescript
return result.toUIMessageStreamResponse({
  originalMessages: messages,
  onFinish: async ({ messages }) => {
    await upsertMessages({ agentId, messages })
  }
})
```

### 3. Handle Disconnects
```typescript
const result = streamText({ ... })
result.consumeStream() // No await - ensures completion even on disconnect
return result.toUIMessageStreamResponse({ ... })
```

### 4. Type-Safe Tools
```typescript
const tools = { myTool: tool({ ... }) } satisfies ToolSet
type MyTools = InferUITools<typeof tools>
type MyUIMessage = UIMessage<MyMetadata, MyDataParts, MyTools>
```

## Common Gotchas

1. **Tool part types are `tool-${toolName}`** not generic `tool-call`
2. **Data parts need `id` for reconciliation** - same ID updates existing part
3. **Transient parts only in `onData`** - never in `message.parts`
4. **`sendStart: false` when using custom start** - avoid duplicate start events
5. **`result.consumeStream()`** - call without await for disconnect handling
