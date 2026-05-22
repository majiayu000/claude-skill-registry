---
name: anthropic-api
description: Integrates Anthropic Claude API for chat, tool use, and vision capabilities. Use when building AI-powered features with Claude models including streaming, extended thinking, and multi-turn conversations.
---

# Anthropic Claude API

Official TypeScript SDK for Anthropic's Claude AI. Access Claude models for chat, tool use, vision, and extended thinking.

## Quick Start

```bash
npm install @anthropic-ai/sdk
```

### Setup

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

## Messages API

### Basic Message

```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' },
  ],
});

console.log(message.content[0].text);
```

### System Prompt

```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  system: 'You are a helpful coding assistant.',
  messages: [
    { role: 'user', content: 'Explain async/await in JavaScript' },
  ],
});
```

### Multi-turn Conversation

```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'What is TypeScript?' },
    { role: 'assistant', content: 'TypeScript is a typed superset of JavaScript...' },
    { role: 'user', content: 'How do I define an interface?' },
  ],
});
```

## Streaming

### Basic Streaming

```typescript
const stream = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Tell me a story' }],
  stream: true,
});

for await (const event of stream) {
  if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
    process.stdout.write(event.delta.text);
  }
}
```

### Using .stream() Helper

```typescript
const stream = anthropic.messages.stream({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello' }],
});

stream.on('text', (text) => {
  process.stdout.write(text);
});

const finalMessage = await stream.finalMessage();
```

### Stream Events

```typescript
const stream = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello' }],
  stream: true,
});

for await (const event of stream) {
  switch (event.type) {
    case 'message_start':
      console.log('Started:', event.message.id);
      break;
    case 'content_block_start':
      console.log('Block started:', event.content_block.type);
      break;
    case 'content_block_delta':
      if (event.delta.type === 'text_delta') {
        process.stdout.write(event.delta.text);
      }
      break;
    case 'content_block_stop':
      console.log('Block stopped');
      break;
    case 'message_stop':
      console.log('Message complete');
      break;
  }
}
```

## Tool Use (Function Calling)

```typescript
const tools = [
  {
    name: 'get_weather',
    description: 'Get the current weather for a location',
    input_schema: {
      type: 'object',
      properties: {
        location: {
          type: 'string',
          description: 'City name, e.g., San Francisco',
        },
        unit: {
          type: 'string',
          enum: ['celsius', 'fahrenheit'],
        },
      },
      required: ['location'],
    },
  },
];

const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  tools,
  messages: [
    { role: 'user', content: 'What is the weather in Tokyo?' },
  ],
});

// Check for tool use
const toolUse = message.content.find((block) => block.type === 'tool_use');
if (toolUse) {
  // Execute the tool
  const weatherData = await getWeather(toolUse.input.location);

  // Send result back
  const finalMessage = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    tools,
    messages: [
      { role: 'user', content: 'What is the weather in Tokyo?' },
      { role: 'assistant', content: message.content },
      {
        role: 'user',
        content: [
          {
            type: 'tool_result',
            tool_use_id: toolUse.id,
            content: JSON.stringify(weatherData),
          },
        ],
      },
    ],
  });
}
```

## Vision (Image Analysis)

### URL Image

```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'image',
          source: {
            type: 'url',
            url: 'https://example.com/image.jpg',
          },
        },
        {
          type: 'text',
          text: 'What is in this image?',
        },
      ],
    },
  ],
});
```

### Base64 Image

```typescript
import fs from 'fs';

const imageData = fs.readFileSync('image.jpg').toString('base64');

const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
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
```

## Extended Thinking

For complex reasoning tasks, enable extended thinking.

```typescript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 16000,
  thinking: {
    type: 'enabled',
    budget_tokens: 10000,
  },
  messages: [
    { role: 'user', content: 'Solve this complex math problem...' },
  ],
});

// Access thinking blocks
for (const block of message.content) {
  if (block.type === 'thinking') {
    console.log('Thinking:', block.thinking);
  } else if (block.type === 'text') {
    console.log('Response:', block.text);
  }
}
```

## PDF Support

```typescript
import fs from 'fs';

const pdfData = fs.readFileSync('document.pdf').toString('base64');

const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'document',
          source: {
            type: 'base64',
            media_type: 'application/pdf',
            data: pdfData,
          },
        },
        {
          type: 'text',
          text: 'Summarize this document',
        },
      ],
    },
  ],
});
```

## Next.js API Route

```typescript
// app/api/chat/route.ts
import Anthropic from '@anthropic-ai/sdk';
import { AnthropicStream, StreamingTextResponse } from 'ai';

const anthropic = new Anthropic();

export async function POST(request: Request) {
  const { messages } = await request.json();

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages,
    stream: true,
  });

  const stream = AnthropicStream(response);
  return new StreamingTextResponse(stream);
}
```

### Manual Streaming

```typescript
// app/api/chat/route.ts
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

export async function POST(request: Request) {
  const { prompt } = await request.json();

  const stream = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }],
    stream: true,
  });

  const encoder = new TextEncoder();
  const readable = new ReadableStream({
    async start(controller) {
      for await (const event of stream) {
        if (event.type === 'content_block_delta' && event.delta.type === 'text_delta') {
          controller.enqueue(encoder.encode(event.delta.text));
        }
      }
      controller.close();
    },
  });

  return new Response(readable, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}
```

## Error Handling

```typescript
import Anthropic from '@anthropic-ai/sdk';

try {
  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: 'Hello' }],
  });
} catch (error) {
  if (error instanceof Anthropic.APIError) {
    console.error('Status:', error.status);
    console.error('Message:', error.message);

    if (error.status === 429) {
      // Rate limited
    } else if (error.status === 401) {
      // Invalid API key
    } else if (error.status === 400) {
      // Bad request
    }
  }
}
```

## Counting Tokens

```typescript
const tokenCount = await anthropic.messages.countTokens({
  model: 'claude-sonnet-4-20250514',
  messages: [
    { role: 'user', content: 'Hello, how are you?' },
  ],
});

console.log('Input tokens:', tokenCount.input_tokens);
```

## Models

| Model | ID | Best For |
|-------|-----|----------|
| Claude Opus 4 | claude-opus-4-20250514 | Complex tasks, research |
| Claude Sonnet 4 | claude-sonnet-4-20250514 | Balanced performance |
| Claude Haiku 4 | claude-haiku-4-20250514 | Fast, simple tasks |

## Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
```

## Best Practices

1. **Stream for long responses** - Better UX and partial recovery
2. **Use system prompts** - Set behavior and context
3. **Handle tool use loops** - Multiple back-and-forth may be needed
4. **Enable extended thinking** - For complex reasoning tasks
5. **Set appropriate max_tokens** - Control response length
6. **Implement retries** - Handle rate limits gracefully
7. **Use message batching** - For batch processing workloads
