---
name: openai-api
description: Complete guide for OpenAI APIs: Chat Completions (GPT-5.2, GPT-4o), Embeddings, Images (GPT-Image-1.5), Audio (Whisper + TTS + Transcribe), Moderation. Includes Node.js SDK and fetch approaches.
license: MIT
---

# OpenAI API

**Package**: openai@6.9.1 | **Last Updated**: 2025-11-21

## Quick Start

```bash
bun add openai
export OPENAI_API_KEY="sk-..."
```

```typescript
import OpenAI from 'openai';

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const response = await client.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Hello!' }]
});
```

## Current Models (2025)

- **gpt-5.2**: Most capable (128k context)
- **gpt-4o**: Fast multimodal (128k context)
- **gpt-4o-mini**: Cost-effective (128k context)
- **gpt-4o-transcribe**: Audio transcription optimized
- **gpt-4o-mini-transcribe**: Cost-effective transcription
- **o1-preview**: Advanced reasoning (128k context)
- **o1-mini**: Fast reasoning (128k context)

## Chat Completions

```typescript
const response = await client.chat.completions.create({
  model: 'gpt-4o',
  messages: [
    { role: 'system', content: 'You are a helpful assistant' },
    { role: 'user', content: 'Explain AI' }
  ],
  temperature: 0.7,
  max_tokens: 1000
});
```

## Streaming

```typescript
const stream = await client.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'Tell a story' }],
  stream: true
});

for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content || '');
}
```

## Function Calling

```typescript
const response = await client.chat.completions.create({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: 'What is the weather?' }],
  tools: [{
    type: 'function',
    function: {
      name: 'getWeather',
      parameters: {
        type: 'object',
        properties: { location: { type: 'string' } },
        required: ['location']
      }
    }
  }]
});
```

## Embeddings

```typescript
const response = await client.embeddings.create({
  model: 'text-embedding-3-small',
  input: 'Your text here'
});

const embedding = response.data[0].embedding; // 1536 dimensions
```

## Images (GPT-Image-1.5)

```typescript
const image = await client.images.generate({
  model: 'gpt-image-1.5',
  prompt: 'A serene landscape',
  size: '1024x1024',
  quality: 'standard'  // or 'hd'
});
```

## Audio

**Transcription (Whisper)**:
```typescript
const transcription = await client.audio.transcriptions.create({
  file: fs.createReadStream('audio.mp3'),
  model: 'whisper-1'
});
```

**Text-to-Speech**:
```typescript
const speech = await client.audio.speech.create({
  model: 'tts-1',
  voice: 'alloy',
  input: 'Hello world'
});
```

## Top Errors

1. **Invalid API Key (401)**: Verify OPENAI_API_KEY
2. **Rate Limit (429)**: Implement exponential backoff
3. **Model Not Found (404)**: Use correct model names
4. **Context Length (400)**: Reduce input size
5. **Invalid JSON**: Fix function calling schemas

**See**: `references/error-catalog.md`

## Resources

### Reference Guides
- `references/models-guide.md` - Complete model comparison and selection
- `references/function-calling-patterns.md` - Function calling best practices
- `references/structured-output-guide.md` - Structured outputs with JSON Schema
- `references/embeddings-guide.md` - Text embeddings and vector search
- `references/images-guide.md` - GPT-Image-1.5 image generation
- `references/audio-guide.md` - Whisper transcription + TTS
- `references/cost-optimization.md` - Token optimization and pricing
- `references/top-errors.md` - Top 20 errors with solutions
- `references/error-catalog.md` - Complete error reference

### Templates
- `templates/basic-usage.ts` - Quick start example
- `templates/chat-completion-basic.ts` - Basic chat completion
- `templates/chat-completion-nodejs.ts` - Node.js implementation
- `templates/streaming-chat.ts` - Streaming responses
- `templates/streaming-fetch.ts` - Streaming with fetch API
- `templates/function-calling.ts` - Tools and function calling
- `templates/structured-output.ts` - JSON Schema outputs
- `templates/vision-gpt4o.ts` - Vision with GPT-4o
- `templates/embeddings.ts` - Text embeddings
- `templates/image-generation.ts` - GPT-Image-1.5 generation
- `templates/image-editing.ts` - Image editing
- `templates/audio-transcription.ts` - Whisper transcription
- `templates/text-to-speech.ts` - TTS with voices
- `templates/moderation.ts` - Content moderation
- `templates/rate-limit-handling.ts` - Exponential backoff
- `templates/cloudflare-worker.ts` - Cloudflare Workers integration

**Docs**: https://platform.openai.com/docs
