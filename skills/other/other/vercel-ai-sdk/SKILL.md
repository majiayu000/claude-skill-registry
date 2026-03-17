---
name: vercel-ai-sdk
description: Vercel AI SDK for building chat interfaces with streaming. Use when implementing useChat hook, handling tool calls, streaming responses, or building chat UI. Triggers on useChat, @ai-sdk/react, UIMessage, ChatStatus, streamText, toUIMessageStreamResponse, addToolOutput, onToolCall, sendMessage.
---

# Vercel AI SDK

The Vercel AI SDK provides React hooks and server utilities for building streaming chat interfaces with support for tool calls, file attachments, and multi-step reasoning.

## Quick Reference

### Basic useChat Setup

```typescript
import { useChat } from '@ai-sdk/react';

const { messages, status, sendMessage, stop, regenerate } = useChat({
  id: 'chat-id',
  messages: initialMessages,
  onFinish: ({ message, messages, isAbort, isError }) => {
    console.log('Chat finished');
  },
  onError: (error) => {
    console.error('Chat error:', error);
  }
});

// Send a message
sendMessage({ text: 'Hello', metadata: { createdAt: Date.now() } });

// Send with files
sendMessage({
  text: 'Analyze this',
  files: fileList // FileList or FileUIPart[]
});
```

### ChatStatus States

The `status` field indicates the current state of the chat:

- **`ready`**: Chat is idle and ready to accept new messages
- **`submitted`**: Message sent to API, awaiting response stream start
- **`streaming`**: Response actively streaming from the API
- **`error`**: An error occurred during the request

### Message Structure

Messages use the `UIMessage` type with a parts-based structure:

```typescript
interface UIMessage {
  id: string;
  role: 'system' | 'user' | 'assistant';
  metadata?: unknown;
  parts: Array<UIMessagePart>; // text, file, tool-*, reasoning, etc.
}
```

Part types include:
- `text`: Text content with optional streaming state
- `file`: File attachments (images, documents)
- `tool-{toolName}`: Tool invocations with state machine
- `reasoning`: AI reasoning traces
- `data-{typeName}`: Custom data parts

### Server-Side Streaming

```typescript
import { streamText } from 'ai';
import { convertToModelMessages } from 'ai';

const result = streamText({
  model: openai('gpt-4'),
  messages: convertToModelMessages(uiMessages),
  tools: {
    getWeather: tool({
      description: 'Get weather',
      inputSchema: z.object({ city: z.string() }),
      execute: async ({ city }) => {
        return { temperature: 72, weather: 'sunny' };
      }
    })
  }
});

return result.toUIMessageStreamResponse({
  originalMessages: uiMessages,
  onFinish: ({ messages }) => {
    // Save to database
  }
});
```

### Tool Handling Patterns

**Client-Side Tool Execution:**
```typescript
const { addToolOutput } = useChat({
  onToolCall: async ({ toolCall }) => {
    if (toolCall.toolName === 'getLocation') {
      addToolOutput({
        tool: 'getLocation',
        toolCallId: toolCall.toolCallId,
        output: 'San Francisco'
      });
    }
  }
});
```

**Rendering Tool States:**
```typescript
{message.parts.map(part => {
  if (part.type === 'tool-getWeather') {
    switch (part.state) {
      case 'input-streaming':
        return <pre>{JSON.stringify(part.input, null, 2)}</pre>;
      case 'input-available':
        return <div>Getting weather for {part.input.city}...</div>;
      case 'output-available':
        return <div>Weather: {part.output.weather}</div>;
      case 'output-error':
        return <div>Error: {part.errorText}</div>;
    }
  }
})}
```

## Reference Files

Detailed documentation on specific aspects:

- **[use-chat.md](references/use-chat.md)**: Complete useChat API reference
- **[messages.md](references/messages.md)**: UIMessage structure and part types
- **[streaming.md](references/streaming.md)**: Server-side streaming implementation
- **[tools.md](references/tools.md)**: Tool definition and execution patterns

## Common Patterns

### Error Handling

```typescript
const { error, clearError } = useChat({
  onError: (error) => {
    toast.error(error.message);
  }
});

// Clear error and reset to ready state
if (error) {
  clearError();
}
```

### Message Regeneration

```typescript
const { regenerate } = useChat();

// Regenerate last assistant message
await regenerate();

// Regenerate specific message
await regenerate({ messageId: 'msg-123' });
```

### Custom Transport

```typescript
import { DefaultChatTransport } from 'ai';

const { messages } = useChat({
  transport: new DefaultChatTransport({
    api: '/api/chat',
    prepareSendMessagesRequest: ({ id, messages, trigger, messageId }) => ({
      body: {
        chatId: id,
        lastMessage: messages[messages.length - 1],
        trigger,
        messageId
      }
    })
  })
});
```

### Performance Optimization

```typescript
// Throttle UI updates to reduce re-renders
const chat = useChat({
  experimental_throttle: 100 // Update max once per 100ms
});
```

### Automatic Message Sending

```typescript
import { lastAssistantMessageIsCompleteWithToolCalls } from 'ai';

const chat = useChat({
  sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls
  // Automatically resend when all tool calls have outputs
});
```

## Type Safety

The SDK provides full type inference for tools and messages:

```typescript
import { InferUITools, UIMessage } from 'ai';

const tools = {
  getWeather: tool({
    inputSchema: z.object({ city: z.string() }),
    execute: async ({ city }) => ({ weather: 'sunny' })
  })
};

type MyMessage = UIMessage<
  { createdAt: number }, // Metadata type
  UIDataTypes,
  InferUITools<typeof tools> // Tool types
>;

const { messages } = useChat<MyMessage>();
```

## Key Concepts

### Parts-Based Architecture

Messages use a parts array instead of a single content field. This allows:
- Streaming text while maintaining other parts
- Tool calls with independent state machines
- File attachments and custom data mixed with text

### Tool State Machine

Tool parts progress through states:
1. `input-streaming`: Tool input streaming (optional)
2. `input-available`: Tool input complete
3. `approval-requested`: Waiting for user approval (optional)
4. `approval-responded`: User approved/denied (optional)
5. `output-available`: Tool execution complete
6. `output-error`: Tool execution failed
7. `output-denied`: User denied approval

### Streaming Protocol

The SDK uses Server-Sent Events (SSE) with UIMessageChunk types:
- `text-start`, `text-delta`, `text-end`
- `tool-input-available`, `tool-output-available`
- `reasoning-start`, `reasoning-delta`, `reasoning-end`
- `start`, `finish`, `abort`

### Client vs Server Tools

**Server-side tools** have an `execute` function and run on the API route.

**Client-side tools** omit `execute` and are handled via `onToolCall` and `addToolOutput`.

## Best Practices

1. Always handle the `error` state and provide user feedback
2. Use `experimental_throttle` for high-frequency updates
3. Implement proper loading states based on `status`
4. Type your messages with custom metadata and tools
5. Use `sendAutomaticallyWhen` for multi-turn tool workflows
6. Handle all tool states in the UI for better UX
7. Use `stop()` to allow users to cancel long-running requests
8. Validate messages with `validateUIMessages` on the server
