---
name: streaming-api-patterns
description: Real-time data streaming with SSE, WebSockets, and ReadableStream. Use when implementing streaming responses, real-time data updates, Server-Sent Events, WebSocket setup, live notifications, push updates, or chat server backends.
context: fork
agent: frontend-ui-developer
version: 1.0.0
author: AI Agent Hub
tags: [streaming, sse, websocket, real-time, api, 2025]
user-invocable: false
---

# Streaming API Patterns

## Overview

**When to use this skill:**
- Streaming LLM responses (ChatGPT-style interfaces)
- Real-time notifications and updates
- Live data feeds (stock prices, analytics)
- Chat applications
- Progress updates for long-running tasks
- Collaborative editing features

## Core Technologies

### 1. Server-Sent Events (SSE)

**Best for**: Server-to-client streaming (LLM responses, notifications)

```typescript
// Next.js Route Handler
export async function GET(req: Request) {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      // Send data
      controller.enqueue(encoder.encode('data: Hello\n\n'))

      // Keep connection alive
      const interval = setInterval(() => {
        controller.enqueue(encoder.encode(': keepalive\n\n'))
      }, 30000)

      // Cleanup
      req.signal.addEventListener('abort', () => {
        clearInterval(interval)
        controller.close()
      })
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    }
  })
}

// Client
const eventSource = new EventSource('/api/stream')
eventSource.onmessage = (event) => {
  console.log(event.data)
}
```

### 2. WebSockets

**Best for**: Bidirectional real-time communication (chat, collaboration)

```typescript
// WebSocket Server (Next.js with ws)
import { WebSocketServer } from 'ws'

const wss = new WebSocketServer({ port: 8080 })

wss.on('connection', (ws) => {
  ws.on('message', (data) => {
    // Broadcast to all clients
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(data)
      }
    })
  })
})

// Client
const ws = new WebSocket('ws://localhost:8080')
ws.onmessage = (event) => console.log(event.data)
ws.send(JSON.stringify({ type: 'message', text: 'Hello' }))
```

### 3. ReadableStream API

**Best for**: Processing large data streams with backpressure

```typescript
async function* generateData() {
  for (let i = 0; i < 1000; i++) {
    await new Promise(resolve => setTimeout(resolve, 100))
    yield "data-" + i
  }
}

const stream = new ReadableStream({
  async start(controller) {
    for await (const chunk of generateData()) {
      controller.enqueue(new TextEncoder().encode(chunk + '\n'))
    }
    controller.close()
  }
})
```

## LLM Streaming Pattern

```typescript
// Server
import OpenAI from 'openai'

const openai = new OpenAI()

export async function POST(req: Request) {
  const { messages } = await req.json()

  const stream = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages,
    stream: true
  })

  const encoder = new TextEncoder()

  return new Response(
    new ReadableStream({
      async start(controller) {
        for await (const chunk of stream) {
          const content = chunk.choices[0]?.delta?.content
          if (content) {
            controller.enqueue(encoder.encode("data: " + JSON.stringify({ content }) + "\n\n"))
          }
        }
        controller.enqueue(encoder.encode('data: [DONE]\n\n'))
        controller.close()
      }
    }),
    {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache'
      }
    }
  )
}

// Client
async function streamChat(messages) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages })
  })

  const reader = response.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value)
    const lines = chunk.split('\n')

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        if (data === '[DONE]') return

        const json = JSON.parse(data)
        console.log(json.content) // Stream token
      }
    }
  }
}
```

## Reconnection Strategy

```typescript
class ReconnectingEventSource {
  private eventSource: EventSource | null = null
  private reconnectDelay = 1000
  private maxReconnectDelay = 30000

  constructor(private url: string, private onMessage: (data: string) => void) {
    this.connect()
  }

  private connect() {
    this.eventSource = new EventSource(this.url)

    this.eventSource.onmessage = (event) => {
      this.reconnectDelay = 1000 // Reset on success
      this.onMessage(event.data)
    }

    this.eventSource.onerror = () => {
      this.eventSource?.close()

      // Exponential backoff
      setTimeout(() => this.connect(), this.reconnectDelay)
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay)
    }
  }

  close() {
    this.eventSource?.close()
  }
}
```

## Python Async Generator Cleanup (2025 Best Practice)

**CRITICAL**: Async generators can leak resources if not properly cleaned up. Python 3.10+ provides `aclosing()` from `contextlib` to guarantee cleanup.

### The Problem

```python
# ❌ DANGEROUS: Generator not closed if exception occurs mid-iteration
async def stream_analysis():
    async for chunk in external_api_stream():  # What if exception here?
        yield process(chunk)  # Generator may be garbage collected without cleanup

# ❌ ALSO DANGEROUS: Using .aclose() manually is error-prone
gen = stream_analysis()
try:
    async for chunk in gen:
        process(chunk)
finally:
    await gen.aclose()  # Easy to forget, verbose
```

### The Solution: `aclosing()`

```python
from contextlib import aclosing

# ✅ CORRECT: aclosing() guarantees cleanup
async def stream_analysis():
    async with aclosing(external_api_stream()) as stream:
        async for chunk in stream:
            yield process(chunk)

# ✅ CORRECT: Using aclosing() at consumption site
async def consume_stream():
    async with aclosing(stream_analysis()) as gen:
        async for chunk in gen:
            handle(chunk)
```

### Real-World Pattern: LLM Streaming

```python
from contextlib import aclosing
from langchain_core.runnables import RunnableConfig

async def stream_llm_response(prompt: str, config: RunnableConfig | None = None):
    """Stream LLM tokens with guaranteed cleanup."""
    async with aclosing(llm.astream(prompt, config=config)) as stream:
        async for chunk in stream:
            yield chunk.content

# Consumption with proper cleanup
async def generate_response(user_input: str):
    result_chunks = []
    async with aclosing(stream_llm_response(user_input)) as response:
        async for token in response:
            result_chunks.append(token)
            yield token  # Stream to client

    # Post-processing after stream completes
    full_response = "".join(result_chunks)
    await log_response(full_response)
```

### Database Connection Pattern

```python
from contextlib import aclosing
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

async def stream_large_query(
    session: AsyncSession,
    batch_size: int = 1000
) -> AsyncIterator[Row]:
    """Stream large query results with automatic connection cleanup."""
    result = await session.execute(
        select(Model).execution_options(stream_results=True)
    )

    async with aclosing(result.scalars()) as stream:
        async for row in stream:
            yield row
```

### When to Use `aclosing()`

| Scenario | Use `aclosing()` |
|----------|------------------|
| External API streaming (LLM, HTTP) | ✅ **Always** |
| Database streaming results | ✅ **Always** |
| File streaming | ✅ **Always** |
| Simple in-memory generators | ⚠️ Optional (no cleanup needed) |
| Generator with `try/finally` cleanup | ✅ **Always** |

### Anti-Patterns to Avoid

```python
# ❌ NEVER: Consuming without aclosing
async for chunk in stream_analysis():
    process(chunk)

# ❌ NEVER: Manual try/finally (verbose, error-prone)
gen = stream_analysis()
try:
    async for chunk in gen:
        process(chunk)
finally:
    await gen.aclose()

# ❌ NEVER: Assuming GC will handle cleanup
gen = stream_analysis()
# ... later gen goes out of scope without close
```

### Testing Async Generators

```python
import pytest
from contextlib import aclosing

@pytest.mark.asyncio
async def test_stream_cleanup_on_error():
    """Test that cleanup happens even when exception raised."""
    cleanup_called = False

    async def stream_with_cleanup():
        nonlocal cleanup_called
        try:
            yield "data"
            yield "more"
        finally:
            cleanup_called = True

    with pytest.raises(ValueError):
        async with aclosing(stream_with_cleanup()) as gen:
            async for chunk in gen:
                raise ValueError("simulated error")

    assert cleanup_called, "Cleanup must run even on exception"
```

## Best Practices

### SSE
- ✅ Use for one-way server-to-client streaming
- ✅ Implement automatic reconnection
- ✅ Send keepalive messages every 30s
- ✅ Handle browser connection limits (6 per domain)
- ✅ Use HTTP/2 for better performance

### WebSockets
- ✅ Use for bidirectional real-time communication
- ✅ Implement heartbeat/ping-pong
- ✅ Handle reconnection with exponential backoff
- ✅ Validate and sanitize messages
- ✅ Implement message queuing for offline periods

### Backpressure
- ✅ Use ReadableStream with proper flow control
- ✅ Monitor buffer sizes
- ✅ Pause production when consumer is slow
- ✅ Implement timeouts for slow consumers

### Performance
- ✅ Compress data (gzip/brotli)
- ✅ Batch small messages
- ✅ Use binary formats (MessagePack, Protobuf) for large data
- ✅ Implement client-side buffering
- ✅ Monitor connection count and resource usage

## Resources

- [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)
- [Vercel AI SDK](https://sdk.vercel.ai/docs)

## Related Skills

- `llm-streaming` - LLM-specific streaming patterns for token-by-token responses
- `api-design-framework` - REST API design patterns for streaming endpoints
- `caching-strategies` - Cache invalidation patterns for real-time data updates
- `edge-computing-patterns` - Edge function streaming for low-latency delivery

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Server-to-Client Streaming | SSE | Simple protocol, auto-reconnect, HTTP/2 compatible |
| Bidirectional Communication | WebSockets | Full-duplex, low latency, binary support |
| LLM Token Streaming | ReadableStream + SSE | Backpressure control, standard format |
| Reconnection Strategy | Exponential Backoff | Prevents thundering herd, graceful recovery |
| Async Generator Cleanup | `aclosing()` | Guaranteed resource cleanup on exceptions |

## Capability Details

### sse
**Keywords:** sse, server-sent events, event stream, one-way stream
**Solves:**
- How do I implement SSE?
- Stream data from server to client
- Real-time notifications

### sse-protocol
**Keywords:** sse protocol, event format, event types, sse headers
**Solves:**
- SSE protocol fundamentals
- Event format and types
- SSE HTTP headers

### sse-buffering
**Keywords:** event buffering, sse race condition, late subscriber, buffer events
**Solves:**
- How do I buffer SSE events?
- Fix SSE race condition
- Handle late-joining subscribers

### sse-reconnection
**Keywords:** sse reconnection, reconnect, last-event-id, retry, exponential backoff
**Solves:**
- How do I handle SSE reconnection?
- Implement automatic reconnection
- Resume from Last-Event-ID

### skillforge-sse
**Keywords:** skillforge sse, event broadcaster, workflow events, analysis progress
**Solves:**
- How does SkillForge SSE work?
- EventBroadcaster implementation
- Real-world SSE example

### websocket
**Keywords:** websocket, ws, bidirectional, real-time chat, socket
**Solves:**
- How do I set up WebSocket server?
- Build a chat application
- Bidirectional real-time communication

### llm-streaming
**Keywords:** llm stream, chatgpt stream, ai stream, token stream, openai stream
**Solves:**
- How do I stream LLM responses?
- ChatGPT-style streaming interface
- Stream tokens as they arrive

### backpressure
**Keywords:** backpressure, flow control, buffer, readable stream, transform stream
**Solves:**
- Handle slow consumers
- Implement backpressure
- Stream large files efficiently

### reconnection
**Keywords:** reconnect, connection lost, retry, resilient, heartbeat
**Solves:**
- Handle connection drops
- Implement automatic reconnection
- Keep-alive and heartbeat
