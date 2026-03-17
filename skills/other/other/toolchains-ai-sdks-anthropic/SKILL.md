# Anthropic SDK - Official Claude AI Integration

---
progressive_disclosure:
  entry_point:
    summary: "Official Anthropic SDK for Claude AI - chat, streaming, function calling, vision"
    when_to_use:
      - "When integrating Claude AI into applications"
      - "When building AI-powered features with Claude models"
      - "When using function calling/tool use patterns"
      - "When processing images with vision models"
      - "When implementing streaming chat interfaces"
    quick_start:
      - "pip install anthropic (Python) or npm install @anthropic-ai/sdk (TypeScript)"
      - "Set ANTHROPIC_API_KEY environment variable"
      - "Create client and send messages with Messages API"
      - "Use streaming for real-time responses"
    installation:
      python: "pip install anthropic"
      typescript: "npm install @anthropic-ai/sdk"
    config:
      - "ANTHROPIC_API_KEY: Your API key from console.anthropic.com"
      - "Model: claude-3-5-sonnet-20241022 (recommended)"
      - "Max tokens: 1024-8192 for responses"
  token_estimate:
    entry: 85
    full: 5000
---

## Installation & Setup

### Python
```bash
pip install anthropic
```

### TypeScript
```bash
npm install @anthropic-ai/sdk
```

### API Key Configuration
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

Get your API key from: https://console.anthropic.com/settings/keys

---

## Messages API - Basic Usage

### Python - Simple Message
```python
import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ]
)

print(message.content[0].text)
```

### TypeScript - Simple Message
```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Explain quantum computing in simple terms' }
  ],
});

console.log(message.content[0].text);
```

### System Prompts
```python
# Python - System prompt for context
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful coding assistant specializing in Python and TypeScript.",
    messages=[
        {"role": "user", "content": "How do I handle errors in async functions?"}
    ]
)
```

```typescript
// TypeScript - System prompt
const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  system: 'You are a helpful coding assistant specializing in Python and TypeScript.',
  messages: [
    { role: 'user', content: 'How do I handle errors in async functions?' }
  ],
});
```

---

## Streaming Responses

### Python - Streaming
```python
# Real-time streaming responses
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a short poem about coding"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Python - Async Streaming
```python
import asyncio

async def stream_response():
    async with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Explain recursion"}
        ]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

asyncio.run(stream_response())
```

### TypeScript - Streaming
```typescript
// Streaming with event handlers
const stream = await client.messages.stream({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Write a short poem about coding' }
  ],
});

for await (const chunk of stream) {
  if (chunk.type === 'content_block_delta' &&
      chunk.delta.type === 'text_delta') {
    process.stdout.write(chunk.delta.text);
  }
}
```

---

## Function Calling / Tool Use

### Python - Function Calling
```python
# Define tools (functions)
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g., San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]

# Initial request
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in San Francisco?"}
    ]
)

# Check for tool use
if message.stop_reason == "tool_use":
    tool_use = next(block for block in message.content if block.type == "tool_use")
    tool_name = tool_use.name
    tool_input = tool_use.input

    # Execute function (mock example)
    if tool_name == "get_weather":
        weather_result = {
            "temperature": 72,
            "unit": "fahrenheit",
            "conditions": "sunny"
        }

    # Send result back to Claude
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in San Francisco?"},
            {"role": "assistant", "content": message.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(weather_result)
                    }
                ]
            }
        ]
    )
    print(response.content[0].text)
```

### TypeScript - Function Calling
```typescript
// Define tools
const tools: Anthropic.Tool[] = [
  {
    name: 'get_weather',
    description: 'Get the current weather for a location',
    input_schema: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'City name, e.g., San Francisco, CA',
        },
        unit: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
          description: 'Temperature unit',
        },
      },
      required: ['location'],
    },
  },
];

// Initial request
const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  tools,
  messages: [
    { role: 'user', content: "What's the weather in San Francisco?" },
  ],
});

// Check for tool use
if (message.stop_reason === 'tool_use') {
  const toolUse = message.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === 'tool_use'
  );

  if (toolUse && toolUse.name === 'get_weather') {
    // Execute function
    const weatherResult = {
      temperature: 72,
      unit: 'fahrenheit',
      conditions: 'sunny',
    };

    // Send result back
    const response = await client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      tools,
      messages: [
        { role: 'user', content: "What's the weather in San Francisco?" },
        { role: 'assistant', content: message.content },
        {
          role: 'user',
          content: [
            {
              type: 'tool_result',
              tool_use_id: toolUse.id,
              content: JSON.stringify(weatherResult),
            },
          ],
        },
      ],
    });

    console.log(response.content[0].text);
  }
}
```

---

## Vision Models - Image Input

### Python - Image Analysis
```python
import base64

# Load image
with open("image.jpg", "rb") as image_file:
    image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

# Send image to Claude
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image in detail"
                }
            ],
        }
    ],
)

print(message.content[0].text)
```

### TypeScript - Image Analysis
```typescript
import * as fs from 'fs';

// Load image
const imageData = fs.readFileSync('image.jpg').toString('base64');

// Send image to Claude
const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'image',
          source: {
            type: 'base64',
            media_type: 'image/jpeg',
            data: imageData,
          },
        },
        {
          type: 'text',
          text: 'Describe this image in detail',
        },
      ],
    },
  ],
});

console.log(message.content[0].text);
```

---

## Prompt Caching (Beta)

Reduce costs by caching repetitive prompt content.

### Python - Prompt Caching
```python
# Cache system prompt and long context
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert Python developer...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "How do I use async/await?"
        }
    ]
)

# Subsequent requests reuse cached system prompt
```

### TypeScript - Prompt Caching
```typescript
const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  system: [
    {
      type: 'text',
      text: 'You are an expert TypeScript developer...',
      cache_control: { type: 'ephemeral' },
    },
  ],
  messages: [
    { role: 'user', content: 'How do I use async/await?' },
  ],
});
```

**Caching Benefits:**
- Reduces latency for repeated content
- Lowers costs (cached tokens charged at reduced rate)
- Useful for long system prompts, documentation, examples

---

## FastAPI Integration (Python)

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import anthropic
import os

app = FastAPI()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    stream: bool = False

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if request.stream:
            # Streaming response
            async def generate():
                async with client.messages.stream(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": request.message}]
                ) as stream:
                    async for text in stream.text_stream:
                        yield text

            return StreamingResponse(generate(), media_type="text/plain")
        else:
            # Non-streaming response
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": request.message}]
            )
            return {"response": message.content[0].text}

    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/tools")
async def chat_with_tools(request: ChatRequest):
    tools = [
        {
            "name": "search_database",
            "description": "Search the knowledge database",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    ]

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[{"role": "user", "content": request.message}]
    )

    return {"response": message.content, "stop_reason": message.stop_reason}
```

---

## Express Integration (TypeScript)

```typescript
import express from 'express';
import Anthropic from '@anthropic-ai/sdk';

const app = express();
app.use(express.json());

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

interface ChatRequest {
  message: string;
  stream?: boolean;
}

app.post('/chat', async (req, res) => {
  const { message, stream }: ChatRequest = req.body;

  try {
    if (stream) {
      // Streaming response
      res.setHeader('Content-Type', 'text/plain');
      res.setHeader('Transfer-Encoding', 'chunked');

      const streamResponse = await client.messages.stream({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        messages: [{ role: 'user', content: message }],
      });

      for await (const chunk of streamResponse) {
        if (chunk.type === 'content_block_delta' &&
            chunk.delta.type === 'text_delta') {
          res.write(chunk.delta.text);
        }
      }
      res.end();
    } else {
      // Non-streaming response
      const response = await client.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        messages: [{ role: 'user', content: message }],
      });

      res.json({ response: response.content[0].text });
    }
  } catch (error) {
    if (error instanceof Anthropic.APIError) {
      res.status(500).json({ error: error.message });
    } else {
      res.status(500).json({ error: 'Internal server error' });
    }
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

## Error Handling & Retries

### Python - Error Handling
```python
from anthropic import (
    APIError,
    APIConnectionError,
    RateLimitError,
    APITimeoutError
)
import time

def chat_with_retry(message_content: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{"role": "user", "content": message_content}]
            )
            return message.content[0].text

        except RateLimitError as e:
            if attempt < max_retries - 1:
                # Exponential backoff
                wait_time = 2 ** attempt
                print(f"Rate limit hit, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

        except APIConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Connection error, retrying...")
                time.sleep(1)
            else:
                raise

        except APITimeoutError as e:
            if attempt < max_retries - 1:
                print(f"Timeout, retrying...")
                time.sleep(2)
            else:
                raise

        except APIError as e:
            # Don't retry on general API errors
            print(f"API error: {e}")
            raise
```

### TypeScript - Error Handling
```typescript
import Anthropic from '@anthropic-ai/sdk';

async function chatWithRetry(
  messageContent: string,
  maxRetries: number = 3
): Promise<string> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const message = await client.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        messages: [{ role: 'user', content: messageContent }],
      });

      return message.content[0].text;
    } catch (error) {
      if (error instanceof Anthropic.RateLimitError) {
        if (attempt < maxRetries - 1) {
          const waitTime = Math.pow(2, attempt) * 1000;
          console.log(`Rate limit hit, waiting ${waitTime}ms...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
        } else {
          throw error;
        }
      } else if (error instanceof Anthropic.APIConnectionError) {
        if (attempt < maxRetries - 1) {
          console.log('Connection error, retrying...');
          await new Promise(resolve => setTimeout(resolve, 1000));
        } else {
          throw error;
        }
      } else {
        // Don't retry on other errors
        throw error;
      }
    }
  }

  throw new Error('Max retries exceeded');
}
```

---

## Token Counting & Cost Management

### Python - Token Counting
```python
# Get token usage from response
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)

print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")

# Calculate cost (example rates)
INPUT_COST_PER_1K = 0.003  # $3 per million tokens
OUTPUT_COST_PER_1K = 0.015  # $15 per million tokens

input_cost = (message.usage.input_tokens / 1000) * INPUT_COST_PER_1K
output_cost = (message.usage.output_tokens / 1000) * OUTPUT_COST_PER_1K
total_cost = input_cost + output_cost

print(f"Total cost: ${total_cost:.6f}")
```

### TypeScript - Token Counting
```typescript
const message = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(`Input tokens: ${message.usage.input_tokens}`);
console.log(`Output tokens: ${message.usage.output_tokens}`);

// Calculate cost
const INPUT_COST_PER_1K = 0.003;
const OUTPUT_COST_PER_1K = 0.015;

const inputCost = (message.usage.input_tokens / 1000) * INPUT_COST_PER_1K;
const outputCost = (message.usage.output_tokens / 1000) * OUTPUT_COST_PER_1K;
const totalCost = inputCost + outputCost;

console.log(`Total cost: $${totalCost.toFixed(6)}`);
```

---

## Best Practices

### Temperature & Parameters
```python
# Low temperature (0.0-0.3) for factual, deterministic responses
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    temperature=0.1,  # More focused
    messages=[{"role": "user", "content": "What is 2+2?"}]
)

# Higher temperature (0.7-1.0) for creative responses
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    temperature=0.9,  # More creative
    messages=[{"role": "user", "content": "Write a creative story"}]
)

# Top-p (nucleus sampling)
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    top_p=0.9,  # Consider top 90% probability mass
    messages=[{"role": "user", "content": "Brainstorm ideas"}]
)
```

### Rate Limiting Strategies
```python
from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window  # seconds
        self.requests = deque()

    def can_proceed(self) -> bool:
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.time_window)

        # Remove old requests
        while self.requests and self.requests[0] < cutoff:
            self.requests.popleft()

        return len(self.requests) < self.max_requests

    def add_request(self):
        self.requests.append(datetime.now())

# Usage: 50 requests per minute
limiter = RateLimiter(max_requests=50, time_window=60)

if limiter.can_proceed():
    limiter.add_request()
    message = client.messages.create(...)
else:
    print("Rate limit reached, waiting...")
```

### Conversation Management
```python
# Multi-turn conversation
conversation = []

def chat(user_message: str):
    # Add user message
    conversation.append({"role": "user", "content": user_message})

    # Send to Claude
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=conversation
    )

    # Add assistant response
    conversation.append({
        "role": "assistant",
        "content": message.content
    })

    return message.content[0].text

# Multi-turn usage
response1 = chat("What is Python?")
response2 = chat("Can you show me an example?")
response3 = chat("Explain the example in detail")
```

---

## Production Patterns

### Connection Pooling & Timeouts
```python
# Configure client with custom timeout
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    timeout=60.0,  # 60 second timeout
    max_retries=2,
)

# For async operations
async_client = anthropic.AsyncAnthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    timeout=60.0,
)
```

### Logging & Monitoring
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitored_chat(user_message: str):
    start_time = time.time()

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_message}]
        )

        duration = time.time() - start_time

        logger.info(
            f"Chat completed - "
            f"Duration: {duration:.2f}s, "
            f"Input tokens: {message.usage.input_tokens}, "
            f"Output tokens: {message.usage.output_tokens}"
        )

        return message.content[0].text

    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise
```

### Environment-Based Configuration
```python
import os
from typing import Optional

class Config:
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1024"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TIMEOUT: float = float(os.getenv("API_TIMEOUT", "60.0"))

    @classmethod
    def validate(cls):
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set")

# Initialize client with config
Config.validate()
client = anthropic.Anthropic(
    api_key=Config.ANTHROPIC_API_KEY,
    timeout=Config.TIMEOUT,
)
```

---

## Available Models

| Model | Context Window | Best For |
|-------|----------------|----------|
| claude-3-5-sonnet-20241022 | 200K tokens | General purpose, reasoning, code |
| claude-3-5-haiku-20241022 | 200K tokens | Fast responses, cost-effective |
| claude-3-opus-20240229 | 200K tokens | Complex tasks, highest capability |

**Recommended:** `claude-3-5-sonnet-20241022` for best balance of speed, cost, and capability.

---

## Common Pitfalls

1. **Not handling tool use loops**: Always check `stop_reason` and handle tool use iteratively
2. **Exceeding max_tokens**: Set appropriate limits based on expected response length
3. **Missing error handling**: Always wrap API calls in try/catch with specific error types
4. **Ignoring rate limits**: Implement exponential backoff for production systems
5. **Hardcoding API keys**: Always use environment variables
6. **Not monitoring token usage**: Track costs and usage in production
7. **Blocking operations**: Use async clients for high-throughput applications

---

## Additional Resources

- **Official Docs**: https://docs.anthropic.com/
- **API Reference**: https://docs.anthropic.com/en/api/
- **Python SDK**: https://github.com/anthropics/anthropic-sdk-python
- **TypeScript SDK**: https://github.com/anthropics/anthropic-sdk-typescript
- **Prompt Engineering**: https://docs.anthropic.com/en/docs/prompt-engineering
- **Model Comparison**: https://docs.anthropic.com/en/docs/models-overview