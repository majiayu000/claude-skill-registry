---
name: llm-streaming
description: LLM streaming response patterns. Use when implementing real-time token streaming, Server-Sent Events for AI responses, or streaming with tool calls.
context: fork
agent: llm-integrator
version: 1.0.0
author: SkillForge
user-invocable: false
---

# LLM Streaming

Deliver LLM responses in real-time for better UX.

## Basic Streaming (OpenAI)

```python
from openai import OpenAI

client = OpenAI()

async def stream_response(prompt: str):
    """Stream tokens as they're generated."""
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

## Streaming with Async

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def async_stream(prompt: str):
    """Async streaming for better concurrency."""
    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

## FastAPI SSE Endpoint

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

@app.get("/chat/stream")
async def stream_chat(prompt: str):
    """Server-Sent Events endpoint for streaming."""
    async def generate():
        async for token in async_stream(prompt):
            yield {
                "event": "token",
                "data": token
            }
        yield {"event": "done", "data": ""}

    return EventSourceResponse(generate())
```

## Frontend SSE Consumer

```typescript
async function streamChat(prompt: string, onToken: (t: string) => void) {
  const response = await fetch("/chat/stream?prompt=" + encodeURIComponent(prompt));
  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;

    const text = decoder.decode(value);
    const lines = text.split('\n');

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data !== '[DONE]') {
          onToken(data);
        }
      }
    }
  }
}

// Usage
let fullResponse = '';
await streamChat('Hello', (token) => {
  fullResponse += token;
  setDisplayText(fullResponse);  // Update UI incrementally
});
```

## Streaming with Tool Calls

```python
async def stream_with_tools(messages: list, tools: list):
    """Handle streaming responses that include tool calls."""
    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        stream=True
    )

    collected_content = ""
    collected_tool_calls = []

    async for chunk in stream:
        delta = chunk.choices[0].delta

        # Collect content tokens
        if delta.content:
            collected_content += delta.content
            yield {"type": "content", "data": delta.content}

        # Collect tool call chunks
        if delta.tool_calls:
            for tc in delta.tool_calls:
                # Tool calls come in chunks, accumulate them
                if tc.index >= len(collected_tool_calls):
                    collected_tool_calls.append({
                        "id": tc.id,
                        "function": {"name": "", "arguments": ""}
                    })

                if tc.function.name:
                    collected_tool_calls[tc.index]["function"]["name"] += tc.function.name
                if tc.function.arguments:
                    collected_tool_calls[tc.index]["function"]["arguments"] += tc.function.arguments

    # If tool calls, execute them
    if collected_tool_calls:
        yield {"type": "tool_calls", "data": collected_tool_calls}
```

## Backpressure Handling

```python
import asyncio

async def stream_with_backpressure(prompt: str, max_buffer: int = 100):
    """Handle slow consumers with backpressure."""
    buffer = asyncio.Queue(maxsize=max_buffer)

    async def producer():
        async for token in async_stream(prompt):
            await buffer.put(token)  # Blocks if buffer full
        await buffer.put(None)  # Signal completion

    async def consumer():
        while True:
            token = await buffer.get()
            if token is None:
                break
            yield token
            await asyncio.sleep(0)  # Yield control

    # Start producer in background
    asyncio.create_task(producer())

    # Return consumer generator
    async for token in consumer():
        yield token
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Protocol | SSE for web, WebSocket for bidirectional |
| Buffer size | 50-200 tokens |
| Timeout | 30-60s for long responses |
| Retry | Reconnect on disconnect |

## Common Mistakes

- No timeout (hangs on network issues)
- Missing error handling in stream
- Not closing connections properly
- Buffering entire response (defeats purpose)

## Related Skills

- `streaming-api-patterns` - SSE/WebSocket deep dive
- `function-calling` - Tool calls in streams
- `react-streaming-ui` - React streaming components

## Capability Details

### token-streaming
**Keywords:** streaming, token, stream response, real-time, incremental
**Solves:**
- Stream tokens as they're generated
- Display real-time LLM output
- Reduce time to first byte

### sse-responses
**Keywords:** SSE, Server-Sent Events, event stream, text/event-stream
**Solves:**
- Implement SSE for streaming
- Handle SSE reconnection
- Parse SSE event data

### streaming-with-tools
**Keywords:** stream tools, tool streaming, function call stream
**Solves:**
- Stream responses with tool calls
- Handle partial tool call data
- Coordinate streaming and tool execution

### partial-json-parsing
**Keywords:** partial JSON, incremental parse, streaming JSON
**Solves:**
- Parse JSON as it streams
- Handle incomplete JSON safely
- Display partial structured data

### stream-cancellation
**Keywords:** cancel, abort, stop stream, AbortController
**Solves:**
- Cancel ongoing streams
- Handle user interrupts
- Clean up stream resources
