---
name: replicate
description: Runs open-source ML models via Replicate API for image generation, LLMs, and audio. Use when calling Stable Diffusion, Llama, Whisper, or other models without infrastructure management.
---

# Replicate

Run open-source ML models in the cloud. Access Stable Diffusion, Llama, Whisper, and thousands of other models via API.

## Quick Start

```bash
npm install replicate
```

### Setup

```typescript
import Replicate from 'replicate';

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});
```

## Run Models

### Basic Prediction

```typescript
const output = await replicate.run(
  'stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf',
  {
    input: {
      prompt: 'A futuristic city at sunset',
    },
  }
);

console.log(output);
// ['https://replicate.delivery/pbxt/...']
```

### With Options

```typescript
const output = await replicate.run(
  'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
  {
    input: {
      prompt: 'A majestic lion in the savanna',
      negative_prompt: 'blurry, low quality',
      width: 1024,
      height: 1024,
      num_outputs: 1,
      scheduler: 'K_EULER',
      num_inference_steps: 50,
      guidance_scale: 7.5,
    },
  }
);
```

## Streaming (Language Models)

```typescript
const output = await replicate.stream(
  'meta/llama-2-70b-chat',
  {
    input: {
      prompt: 'Tell me a story about a robot',
      max_new_tokens: 500,
    },
  }
);

for await (const event of output) {
  process.stdout.write(event.data);
}
```

### Stream Events

```typescript
for await (const event of output) {
  switch (event.event) {
    case 'output':
      process.stdout.write(event.data);
      break;
    case 'logs':
      console.log('Log:', event.data);
      break;
    case 'error':
      console.error('Error:', event.data);
      break;
    case 'done':
      console.log('Complete');
      break;
  }
}
```

## Predictions API

### Create Prediction

```typescript
const prediction = await replicate.predictions.create({
  version: 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf',
  input: {
    prompt: 'A painting of a cat',
  },
});

console.log(prediction.id);
// 'ufawqhfynnddngld...'
```

### Wait for Completion

```typescript
const prediction = await replicate.predictions.create({
  version: 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf',
  input: { prompt: 'A cat' },
});

// Poll for result
let result = await replicate.predictions.get(prediction.id);
while (result.status !== 'succeeded' && result.status !== 'failed') {
  await new Promise((r) => setTimeout(r, 1000));
  result = await replicate.predictions.get(prediction.id);
}

console.log(result.output);
```

### Using wait()

```typescript
const prediction = await replicate.predictions.create({
  version: 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf',
  input: { prompt: 'A cat' },
});

const result = await replicate.wait(prediction);
console.log(result.output);
```

## Webhooks

Receive results via webhook instead of polling.

```typescript
const prediction = await replicate.predictions.create({
  version: 'db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf',
  input: { prompt: 'A cat' },
  webhook: 'https://your-app.com/api/replicate-webhook',
  webhook_events_filter: ['completed'],
});
```

### Webhook Handler

```typescript
// app/api/replicate-webhook/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const prediction = await request.json();

  if (prediction.status === 'succeeded') {
    console.log('Output:', prediction.output);
    // Save to database, notify user, etc.
  } else if (prediction.status === 'failed') {
    console.error('Failed:', prediction.error);
  }

  return NextResponse.json({ received: true });
}
```

## Popular Models

### Image Generation (SDXL)

```typescript
const output = await replicate.run(
  'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
  {
    input: {
      prompt: 'An astronaut riding a horse on Mars',
      width: 1024,
      height: 1024,
    },
  }
);
```

### Llama 3

```typescript
const output = await replicate.run(
  'meta/meta-llama-3.1-405b-instruct',
  {
    input: {
      prompt: 'Explain quantum computing in simple terms',
      max_tokens: 500,
      temperature: 0.7,
    },
  }
);
```

### Whisper (Speech to Text)

```typescript
const output = await replicate.run(
  'openai/whisper:4d50797290df275329f202e48c76360b3f22b08d28c196cbc54600319435f8d2',
  {
    input: {
      audio: 'https://example.com/audio.mp3',
      model: 'large-v3',
      language: 'en',
    },
  }
);

console.log(output.transcription);
```

### Image Upscaling

```typescript
const output = await replicate.run(
  'nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b',
  {
    input: {
      image: 'https://example.com/low-res-image.jpg',
      scale: 4,
    },
  }
);
```

### Background Removal

```typescript
const output = await replicate.run(
  'cjwbw/rembg:fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003',
  {
    input: {
      image: 'https://example.com/photo.jpg',
    },
  }
);
```

### Face Restoration

```typescript
const output = await replicate.run(
  'tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3',
  {
    input: {
      img: 'https://example.com/old-photo.jpg',
      version: 'v1.4',
      scale: 2,
    },
  }
);
```

## Input from Files

### URL Input

```typescript
const output = await replicate.run('model/version', {
  input: {
    image: 'https://example.com/image.jpg',
  },
});
```

### File Upload

```typescript
import fs from 'fs';

const output = await replicate.run('model/version', {
  input: {
    image: fs.createReadStream('./image.jpg'),
  },
});
```

### Base64

```typescript
const base64 = fs.readFileSync('./image.jpg').toString('base64');

const output = await replicate.run('model/version', {
  input: {
    image: `data:image/jpeg;base64,${base64}`,
  },
});
```

## Next.js Integration

```typescript
// app/api/generate/route.ts
import Replicate from 'replicate';
import { NextRequest, NextResponse } from 'next/server';

const replicate = new Replicate();

export async function POST(request: NextRequest) {
  const { prompt } = await request.json();

  const output = await replicate.run(
    'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
    {
      input: {
        prompt,
        width: 1024,
        height: 1024,
      },
    }
  );

  return NextResponse.json({ images: output });
}
```

### Streaming LLM

```typescript
// app/api/chat/route.ts
import Replicate from 'replicate';

const replicate = new Replicate();

export async function POST(request: Request) {
  const { prompt } = await request.json();

  const stream = await replicate.stream('meta/meta-llama-3.1-405b-instruct', {
    input: {
      prompt,
      max_tokens: 500,
    },
  });

  const encoder = new TextEncoder();
  const readable = new ReadableStream({
    async start(controller) {
      for await (const event of stream) {
        if (event.event === 'output') {
          controller.enqueue(encoder.encode(event.data));
        }
      }
      controller.close();
    },
  });

  return new Response(readable, {
    headers: { 'Content-Type': 'text/plain' },
  });
}
```

## List Models

```typescript
const models = await replicate.models.list();

for (const model of models.results) {
  console.log(`${model.owner}/${model.name}`);
}
```

## Get Model Versions

```typescript
const model = await replicate.models.get('stability-ai', 'sdxl');
console.log('Latest version:', model.latest_version?.id);

const versions = await replicate.models.versions.list('stability-ai', 'sdxl');
for (const version of versions.results) {
  console.log(version.id);
}
```

## Error Handling

```typescript
try {
  const output = await replicate.run('model/version', {
    input: { prompt: 'Hello' },
  });
} catch (error) {
  if (error.response?.status === 422) {
    console.error('Invalid input:', error.message);
  } else if (error.response?.status === 429) {
    console.error('Rate limited');
  } else {
    console.error('Error:', error.message);
  }
}
```

## Environment Variables

```bash
REPLICATE_API_TOKEN=r8_xxxxxxxx
```

## Best Practices

1. **Use webhooks** - For long-running predictions
2. **Stream LLMs** - Better UX for text generation
3. **Handle timeouts** - Some models take minutes
4. **Cache results** - Avoid duplicate predictions
5. **Use specific versions** - Pinned for reproducibility
6. **Compress images** - Reduce upload time
7. **Set reasonable limits** - Control costs with max_tokens
