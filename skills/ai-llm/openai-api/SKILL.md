---
name: openai-api
description: Integrates OpenAI APIs for chat completions, embeddings, and image generation. Use when building AI-powered features with GPT models, DALL-E, or Whisper in Node.js applications.
---

# OpenAI API

Official Node.js/TypeScript SDK for OpenAI. Access GPT models for chat, embeddings, image generation, and audio transcription.

## Quick Start

```bash
npm install openai
```

### Setup

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});
```

## Chat Completions

### Basic Chat

```typescript
const completion = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello, how are you?' },
  ],
});

console.log(completion.choices[0].message.content);
```

### With Parameters

```typescript
const completion = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: 'Write a haiku about programming' },
  ],
  temperature: 0.7,
  max_tokens: 100,
  top_p: 1,
  frequency_penalty: 0,
  presence_penalty: 0,
});
```

### Streaming

```typescript
const stream = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Tell me a story' }],
  stream: true,
});

for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content || '';
  process.stdout.write(content);
}
```

### Streaming with Helpers

```typescript
const stream = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Hello' }],
  stream: true,
});

// Get final message when done
const finalMessage = await stream.finalMessage();
console.log(finalMessage.choices[0].message);

// Or use event handlers
stream.on('message', (msg) => console.log(msg));
stream.on('content', (content) => console.log(content));
```

## Function Calling (Tools)

```typescript
const tools = [
  {
    type: 'function' as const,
    function: {
      name: 'get_weather',
      description: 'Get the current weather for a location',
      parameters: {
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
  },
];

const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'user', content: 'What is the weather in Tokyo?' },
  ],
  tools,
  tool_choice: 'auto',
});

const toolCall = response.choices[0].message.tool_calls?.[0];
if (toolCall) {
  const args = JSON.parse(toolCall.function.arguments);
  // Call your function with args
  const weatherData = await getWeather(args.location);

  // Send result back
  const finalResponse = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'user', content: 'What is the weather in Tokyo?' },
      response.choices[0].message,
      {
        role: 'tool',
        tool_call_id: toolCall.id,
        content: JSON.stringify(weatherData),
      },
    ],
  });
}
```

## Structured Output (JSON Mode)

```typescript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    {
      role: 'system',
      content: 'Extract the following info as JSON: name, age, occupation',
    },
    {
      role: 'user',
      content: 'John is a 30 year old software developer',
    },
  ],
  response_format: { type: 'json_object' },
});

const data = JSON.parse(response.choices[0].message.content!);
// { name: 'John', age: 30, occupation: 'software developer' }
```

### With JSON Schema

```typescript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'List 3 programming languages' }],
  response_format: {
    type: 'json_schema',
    json_schema: {
      name: 'languages',
      schema: {
        type: 'object',
        properties: {
          languages: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                name: { type: 'string' },
                paradigm: { type: 'string' },
              },
              required: ['name', 'paradigm'],
            },
          },
        },
        required: ['languages'],
      },
    },
  },
});
```

## Embeddings

```typescript
const response = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: 'The quick brown fox jumps over the lazy dog',
});

const embedding = response.data[0].embedding;
// [0.0123, -0.0456, ...] - 1536 dimensions
```

### Multiple Inputs

```typescript
const response = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: [
    'First document text',
    'Second document text',
    'Third document text',
  ],
});

const embeddings = response.data.map((d) => d.embedding);
```

## Image Generation (DALL-E)

```typescript
const response = await openai.images.generate({
  model: 'dall-e-3',
  prompt: 'A futuristic city skyline at sunset',
  n: 1,
  size: '1024x1024',
  quality: 'hd',
  style: 'vivid',
});

const imageUrl = response.data[0].url;
```

### Image Edit

```typescript
import fs from 'fs';

const response = await openai.images.edit({
  model: 'dall-e-2',
  image: fs.createReadStream('original.png'),
  mask: fs.createReadStream('mask.png'),
  prompt: 'Add a red hat to the person',
  n: 1,
  size: '1024x1024',
});
```

## Vision (Image Analysis)

```typescript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'What is in this image?' },
        {
          type: 'image_url',
          image_url: {
            url: 'https://example.com/image.jpg',
            detail: 'high',
          },
        },
      ],
    },
  ],
  max_tokens: 300,
});
```

### Base64 Image

```typescript
const base64Image = fs.readFileSync('image.jpg').toString('base64');

const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'Describe this image' },
        {
          type: 'image_url',
          image_url: {
            url: `data:image/jpeg;base64,${base64Image}`,
          },
        },
      ],
    },
  ],
});
```

## Audio (Whisper & TTS)

### Speech to Text

```typescript
import fs from 'fs';

const transcription = await openai.audio.transcriptions.create({
  file: fs.createReadStream('audio.mp3'),
  model: 'whisper-1',
  language: 'en',
  response_format: 'text',
});

console.log(transcription);
```

### Text to Speech

```typescript
const response = await openai.audio.speech.create({
  model: 'tts-1',
  voice: 'alloy',  // alloy, echo, fable, onyx, nova, shimmer
  input: 'Hello, this is a test of text to speech.',
});

const buffer = Buffer.from(await response.arrayBuffer());
fs.writeFileSync('output.mp3', buffer);
```

## Next.js API Route

```typescript
// app/api/chat/route.ts
import OpenAI from 'openai';
import { OpenAIStream, StreamingTextResponse } from 'ai';

const openai = new OpenAI();

export async function POST(request: Request) {
  const { messages } = await request.json();

  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages,
    stream: true,
  });

  const stream = OpenAIStream(response);
  return new StreamingTextResponse(stream);
}
```

### With Edge Runtime

```typescript
// app/api/chat/route.ts
export const runtime = 'edge';

import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(request: Request) {
  const { prompt } = await request.json();

  const stream = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: prompt }],
    stream: true,
  });

  return new Response(stream.toReadableStream(), {
    headers: { 'Content-Type': 'text/event-stream' },
  });
}
```

## Error Handling

```typescript
import OpenAI from 'openai';

try {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: 'Hello' }],
  });
} catch (error) {
  if (error instanceof OpenAI.APIError) {
    console.error('Status:', error.status);
    console.error('Message:', error.message);
    console.error('Code:', error.code);

    if (error.status === 429) {
      // Rate limited - implement retry logic
    } else if (error.status === 401) {
      // Invalid API key
    }
  }
}
```

## Responses API (Newer)

```typescript
const response = await openai.responses.create({
  model: 'gpt-4o',
  input: 'What is the capital of France?',
});

console.log(response.output_text);
```

### Streaming with Responses API

```typescript
const stream = await openai.responses.create({
  model: 'gpt-4o',
  input: 'Tell me a story',
  stream: true,
});

for await (const event of stream) {
  if (event.type === 'response.output_text.delta') {
    process.stdout.write(event.delta);
  }
}
```

## Environment Variables

```bash
OPENAI_API_KEY=sk-xxxxxxxx
```

## Best Practices

1. **Stream responses** - Better UX for long outputs
2. **Use function calling** - For structured tool usage
3. **Handle rate limits** - Implement exponential backoff
4. **Choose right model** - gpt-4o for complex, gpt-4o-mini for simple
5. **Use JSON mode** - For reliable structured output
6. **Set max_tokens** - Prevent runaway costs
7. **Add timeouts** - Handle slow responses
