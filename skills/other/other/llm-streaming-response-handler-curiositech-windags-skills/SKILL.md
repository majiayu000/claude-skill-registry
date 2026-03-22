---
name: llm-streaming-response-handler
description: Build production LLM streaming UIs with Server-Sent Events, real-time token display, cancellation, error recovery. Handles OpenAI/Anthropic/Claude streaming APIs. Use for chatbots, AI assistants, real-time text generation. Activate on "LLM streaming", "SSE", "token stream", "chat UI", "real-time AI". NOT for batch processing, non-streaming APIs, or WebSocket bidirectional chat.
allowed-tools: Read,Write,Edit,Bash(npm:*)
---

# LLM Streaming Response Handler

Expert in building production-grade streaming interfaces for LLM responses that feel instant and responsive.

## When to Use

✅ **Use for**:
- Chat interfaces with typing animation
- Real-time AI assistants
- Code generation with live preview
- Document summarization with progressive display
- Any UI where users expect immediate feedback from LLMs

❌ **NOT for**:
- Batch document processing (no user watching)
- APIs that don't support streaming
- WebSocket-based bidirectional chat (use Socket.IO)
- Simple request/response (fetch is fine)

## Quick Decision Tree

```
Does your LLM interaction:
├── Need immediate visual feedback? → Streaming
├── Display long-form content (&gt;100 words)? → Streaming
├── User expects typewriter effect? → Streaming
├── Short response (&lt;50 words)? → Regular fetch
└── Background processing? → Regular fetch
```

---

## Technology Selection

### Server-Sent Events (SSE) - Recommended

**Why SSE over WebSockets for LLM streaming**:
- **Simplicity**: HTTP-based, works with existing infrastructure
- **Auto-reconnect**: Built-in reconnection logic
- **Firewall-friendly**: Easier than WebSockets through proxies
- **One-way perfect**: LLMs only stream server → client

**Timeline**:
- 2015-2020: WebSockets for everything
- 2020: SSE adoption for streaming APIs
- 2023+: SSE standard for LLM streaming (OpenAI, Anthropic)
- 2024: Vercel AI SDK popularizes SSE patterns

### Streaming APIs

| Provider | Streaming Method | Response Format |
|----------|------------------|-----------------|
| OpenAI | SSE | `data: {"choices":[{"delta":{"content":"token"}}]}` |
| Anthropic | SSE | `data: {"type":"content_block_delta","delta":{"text":"token"}}` |
| Claude (API) | SSE | `data: {"delta":{"text":"token"}}` |
| Vercel AI SDK | SSE | Normalized across providers |

---

## Common Anti-Patterns

### Anti-Pattern 1: Buffering Before Display

**Novice thinking**: "Collect all tokens, then show complete response"

**Problem**: Defeats the entire purpose of streaming.

**Wrong approach**:
```typescript
// ❌ Waits for entire response before showing anything
const response = await fetch('/api/chat', { method: 'POST', body: prompt });
const fullText = await response.text();
setMessage(fullText); // User sees nothing until done
```

**Correct approach**:
```typescript
// ✅ Display tokens as they arrive
const response = await fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ prompt })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  const chunk = decoder.decode(value);
  const lines = chunk.split('\n').filter(line => line.trim());

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      setMessage(prev => prev + data.content); // Update immediately
    }
  }
}
```

**Timeline**:
- Pre-2023: Many apps buffered entire response
- 2023+: Token-by-token display expected

---

### Anti-Pattern 2: No Stream Cancellation

**Problem**: User can't stop generation, wasting tokens and money.

**Symptom**: "Stop" button doesn't work or doesn't exist.

**Correct approach**:
```typescript
// ✅ AbortController for cancellation
const [abortController, setAbortController] = useState<AbortController | null>(null);

const streamResponse = async () => {
  const controller = new AbortController();
  setAbortController(controller);

  try {
    const response = await fetch('/api/chat', {
      signal: controller.signal,
      method: 'POST',
      body: JSON.stringify({ prompt })
    });

    // Stream handling...
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Stream cancelled by user');
    }
  } finally {
    setAbortController(null);
  }
};

const cancelStream = () => {
  abortController?.abort();
};

return (
  <button onClick={cancelStream} disabled={!abortController}>
    Stop Generating
  </button>
);
```

---

### Anti-Pattern 3: No Error Recovery

**Problem**: Stream fails mid-response, user sees partial text with no indication of failure.

**Correct approach**:
```typescript
// ✅ Error states and recovery
const [streamState, setStreamState] = useState<'idle' | 'streaming' | 'error' | 'complete'>('idle');
const [errorMessage, setErrorMessage] = useState<string | null>(null);

try {
  setStreamState('streaming');

  // Streaming logic...

  setStreamState('complete');
} catch (error) {
  setStreamState('error');

  if (error.name === 'AbortError') {
    setErrorMessage('Generation stopped');
  } else if (error.message.includes('429')) {
    setErrorMessage('Rate limit exceeded. Try again in a moment.');
  } else {
    setErrorMessage('Something went wrong. Please retry.');
  }
}

// UI feedback
{streamState === 'error' && (
  <div className="error-banner">
    {errorMessage}
    <button onClick={retryStream}>Retry</button>
  </div>
)}
```

---

### Anti-Pattern 4: Memory Leaks from Unclosed Streams

**Problem**: Streams not cleaned up, causing memory leaks.

**Symptom**: Browser slows down after multiple requests.

**Correct approach**:
```typescript
// ✅ Cleanup with useEffect
useEffect(() => {
  let reader: ReadableStreamDefaultReader | null = null;

  const streamResponse = async () => {
    const response = await fetch('/api/chat', { ... });
    reader = response.body.getReader();

    // Streaming...
  };

  streamResponse();

  // Cleanup on unmount
  return () => {
    reader?.cancel();
  };
}, [prompt]);
```

---

### Anti-Pattern 5: No Typing Indicator Between Tokens

**Problem**: UI feels frozen between slow tokens.

**Correct approach**:
```typescript
// ✅ Animated cursor during generation
<div className="message">
  {content}
  {isStreaming && <span className="typing-cursor">▊</span>}
</div>
```

```css
.typing-cursor {
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  50% { opacity: 0; }
}
```

---

## Implementation Patterns

### Pattern 1: Basic SSE Stream Handler

```typescript
async function* streamCompletion(prompt: string) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt })
  });

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));

        if (data.content) {
          yield data.content;
        }

        if (data.done) {
          return;
        }
      }
    }
  }
}

// Usage
for await (const token of streamCompletion('Hello')) {
  console.log(token);
}
```

### Pattern 2: React Hook for Streaming

```typescript
import { useState, useCallback } from 'react';

interface UseStreamingOptions {
  onToken?: (token: string) => void;
  onComplete?: (fullText: string) => void;
  onError?: (error: Error) => void;
}

export function useStreaming(options: UseStreamingOptions = {}) {
  const [content, setContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [abortController, setAbortController] = useState<AbortController | null>(null);

  const stream = useCallback(async (prompt: string) => {
    const controller = new AbortController();
    setAbortController(controller);
    setIsStreaming(true);
    setError(null);
    setContent('');

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        signal: controller.signal,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      });

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();

      let accumulated = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n').filter(line => line.trim());

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));

            if (data.content) {
              accumulated += data.content;
              setContent(accumulated);
              options.onToken?.(data.content);
            }
          }
        }
      }

      options.onComplete?.(accumulated);
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err as Error);
        options.onError?.(err as Error);
      }
    } finally {
      setIsStreaming(false);
      setAbortController(null);
    }
  }, [options]);

  const cancel = useCallback(() => {
    abortController?.abort();
  }, [abortController]);

  return { content, isStreaming, error, stream, cancel };
}

// Usage in component
function ChatInterface() {
  const { content, isStreaming, stream, cancel } = useStreaming({
    onToken: (token) => console.log('New token:', token),
    onComplete: (text) => console.log('Done:', text)
  });

  return (
    <div>
      <div className="message">
        {content}
        {isStreaming && <span className="cursor">▊</span>}
      </div>

      <button onClick={() => stream('Tell me a story')} disabled={isStreaming}>
        Generate
      </button>

      {isStreaming && <button onClick={cancel}>Stop</button>}
    </div>
  );
}
```

### Pattern 3: Server-Side Streaming (Next.js)

```typescript
// app/api/chat/route.ts
import { OpenAI } from 'openai';

export const runtime = 'edge'; // Required for streaming

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
  });

  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    stream: true
  });

  // Convert OpenAI stream to SSE format
  const encoder = new TextEncoder();

  const readable = new ReadableStream({
    async start(controller) {
      try {
        for await (const chunk of stream) {
          const content = chunk.choices[0]?.delta?.content;

          if (content) {
            const sseMessage = `data: ${JSON.stringify({ content })}\n\n`;
            controller.enqueue(encoder.encode(sseMessage));
          }
        }

        // Send completion signal
        controller.enqueue(encoder.encode('data: {"done":true}\n\n'));
        controller.close();
      } catch (error) {
        controller.error(error);
      }
    }
  });

  return new Response(readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    }
  });
}
```

---

## Production Checklist

```
□ AbortController for cancellation
□ Error states with retry capability
□ Typing indicator during generation
□ Cleanup on component unmount
□ Rate limiting on API route
□ Token usage tracking
□ Streaming fallback (if API fails)
□ Accessibility (screen reader announces updates)
□ Mobile-friendly (touch targets for stop button)
□ Network error recovery (auto-retry on disconnect)
□ Max response length enforcement
□ Cost estimation before generation
```

---

## When to Use vs Avoid

| Scenario | Use Streaming? |
|----------|----------------|
| Chat interface | ✅ Yes |
| Long-form content generation | ✅ Yes |
| Code generation with preview | ✅ Yes |
| Short completions (&lt;50 words) | ❌ No - regular fetch |
| Background jobs | ❌ No - use job queue |
| Bidirectional chat | ⚠️ Use WebSockets instead |

---

## Technology Comparison

| Feature | SSE | WebSockets | Long Polling |
|---------|-----|-----------|--------------|
| Complexity | Low | Medium | High |
| Auto-reconnect | ✅ | ❌ | ❌ |
| Bidirectional | ❌ | ✅ | ❌ |
| Firewall-friendly | ✅ | ⚠️ | ✅ |
| Browser support | ✅ All modern | ✅ All modern | ✅ Universal |
| LLM API support | ✅ Standard | ❌ Rare | ❌ Not used |

---

## References

- `/references/sse-protocol.md` - Server-Sent Events specification details
- `/references/vercel-ai-sdk.md` - Vercel AI SDK integration patterns
- `/references/error-recovery.md` - Stream error handling strategies

## Scripts

- `scripts/stream_tester.ts` - Test SSE endpoints locally
- `scripts/token_counter.ts` - Estimate costs before generation

---

**This skill guides**: LLM streaming implementation | SSE protocol | Real-time UI updates | Cancellation | Error recovery | Token-by-token display

