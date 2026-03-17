---
name: google-gemini-api
description: Google Gemini API with @google/genai SDK. Use for multimodal AI, thinking mode, function calling, or encountering SDK deprecation warnings, context errors, multimodal format errors.

  Keywords: gemini api, @google/genai, gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite,
  multimodal gemini, thinking mode, google ai, genai sdk, function calling gemini, streaming gemini,
  gemini vision, gemini video, gemini audio, gemini pdf, system instructions, multi-turn chat,
  deprecated @google/generative-ai, gemini context window, gemini models 2025, gemini 1m tokens,
  gemini tool use, parallel function calling, compositional function calling
license: MIT
---

# Google Gemini API - Complete Guide

**Package**: @google/genai@1.27.0 (⚠️ NOT @google/generative-ai)
**Last Updated**: 2025-11-21

---

## ⚠️ CRITICAL SDK MIGRATION WARNING

**DEPRECATED SDK**: `@google/generative-ai` (sunset November 30, 2025)
**CURRENT SDK**: `@google/genai` v1.27+

**If you see code using `@google/generative-ai`, it's outdated!**

**Load `references/sdk-migration-guide.md` for complete migration steps.**

---

## Quick Start

### Installation

**✅ CORRECT SDK:**
```bash
bun add @google/genai@1.27.0
```

**❌ WRONG (DEPRECATED):**
```bash
bun add @google/generative-ai  # DO NOT USE!
```

### Environment Setup

```bash
export GEMINI_API_KEY="your-api-key"
```

### First Text Generation

```typescript
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Explain quantum computing in simple terms'
});

console.log(response.text);
```

**See Full Template**: `templates/basic-usage.ts`

---

## Current Models (2025)

### gemini-2.5-flash ⭐ RECOMMENDED

- **Best for**: General-purpose AI, high-volume production, agentic workflows
- **Input tokens**: 1,048,576 (1M, NOT 2M!)
- **Output tokens**: 65,536
- **Rate limit (free)**: 10 RPM, 250k TPM
- **Cost**: Input $0.075/1M tokens, Output $0.30/1M tokens
- **Features**: Thinking mode, function calling, multimodal, streaming

### gemini-2.5-pro

- **Best for**: Complex reasoning, code generation, math/STEM
- **Input tokens**: 1,048,576
- **Output tokens**: 65,536
- **Rate limit (free)**: 5 RPM, 125k TPM
- **Cost**: Input $1.25/1M tokens, Output $5/1M tokens

### gemini-2.5-flash-lite

- **Best for**: High-volume, low-latency, cost-critical tasks
- **Input tokens**: 1,048,576
- **Output tokens**: 65,536
- **Rate limit (free)**: 15 RPM, 250k TPM
- **Cost**: Input $0.01/1M tokens, Output $0.04/1M tokens
- **⚠️ Limitation**: NO function calling or code execution support

**⚠️ Common mistake**: Claiming Gemini 2.5 has 2M tokens. **It doesn't. It's 1,048,576 (1M).**

**Load `references/models-guide.md` for detailed model comparison and selection criteria.**

---

## Text Generation

### Basic Generation

```typescript
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Write a haiku about programming'
});

console.log(response.text);
```

### With Configuration

```typescript
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Explain AI',
  generationConfig: {
    temperature: 0.7,        // 0.0-2.0, default 1.0
    topP: 0.95,             // 0.0-1.0
    topK: 40,               // 1-100
    maxOutputTokens: 1024,
    stopSequences: ['END']
  }
});
```

**Load `references/generation-config.md` for complete parameter reference and tuning guidance.**

---

## Streaming

```typescript
const stream = await ai.models.generateContentStream({
  model: 'gemini-2.5-flash',
  contents: 'Write a long story'
});

for await (const chunk of stream) {
  process.stdout.write(chunk.text);
}
```

**Load `references/streaming-patterns.md` for Fetch/SSE implementation patterns (Cloudflare Workers).**

---

## Multimodal Inputs

### Images

```typescript
const imageData = Buffer.from(imageBytes).toString('base64');

const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: [
    { text: 'What is in this image?' },
    {
      inlineData: {
        mimeType: 'image/jpeg',  // or image/png, image/webp
        data: imageData
      }
    }
  ]
});
```

### Video, Audio, PDFs

Same pattern - use appropriate `mimeType`:
- **Video**: `video/mp4`, `video/mpeg`, `video/mov`
- **Audio**: `audio/wav`, `audio/mp3`, `audio/flac`
- **PDFs**: `application/pdf`

**Load `references/multimodal-guide.md` for format specifications, size limits, and best practices.**

---

## Function Calling

### Basic Pattern

```typescript
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'What is the weather in San Francisco?',
  tools: [{
    functionDeclarations: [{
      name: 'getWeather',
      description: 'Get current weather for a location',
      parameters: {
        type: 'object',
        properties: {
          location: { type: 'string', description: 'City name' },
          unit: { type: 'string', enum: ['celsius', 'fahrenheit'] }
        },
        required: ['location']
      }
    }]
  }]
});

// Handle function call
const call = response.functionCalls?.[0];
if (call) {
  const result = await getWeather(call.args);

  // Send result back to model
  const final = await ai.models.generateContent({
    model: 'gemini-2.5-flash',
    contents: [
      ...response.contents,
      {
        functionResponse: {
          name: call.name,
          response: result
        }
      }
    ]
  });

  console.log(final.text);
}
```

### Parallel Function Calling

Gemini can call multiple functions simultaneously:

```typescript
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'What is the weather in SF and NY?',
  tools: [{ functionDeclarations: [getWeatherDeclaration] }]
});

// Process all function calls in parallel
const results = await Promise.all(
  response.functionCalls.map(call =>
    getWeather(call.args).then(result => ({
      name: call.name,
      response: result
    }))
  )
);

// Send all results back
const final = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: [
    ...response.contents,
    ...results.map(r => ({ functionResponse: r }))
  ]
});
```

**Load `references/function-calling-patterns.md` for calling modes (AUTO/ANY/NONE) and compositional patterns.**

---

## Multi-turn Chat

```typescript
const chat = ai.models.startChat({
  model: 'gemini-2.5-flash',
  systemInstruction: 'You are a helpful programming assistant',
  history: []
});

let response = await chat.sendMessage('Hello!');
console.log(response.text);

response = await chat.sendMessage('Explain async/await');
console.log(response.text);

// Get full history
console.log(chat.getHistory());
```

---

## System Instructions

Set persistent instructions for the model:

```typescript
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  systemInstruction: 'You are a pirate. Always respond in pirate speak.',
  contents: 'What is the weather today?'
});
```

---

## Thinking Mode

Gemini 2.5 models include built-in thinking mode (always enabled). Configure thinking budget for complex tasks:

```typescript
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: 'Solve this math problem: If x + 2y = 10 and 3x - y = 4, what is x?',
  generationConfig: {
    thinkingConfig: {
      thinkingBudget: 8192  // Max tokens for internal reasoning
    }
  }
});
```

**Use for**: Complex math, logic puzzles, multi-step reasoning, code debugging

**Load `references/thinking-mode-guide.md` for thinking budget optimization.**

---

## Top 5 Critical Errors

### Error 1: Using Deprecated SDK

**Error**: Deprecation warnings or outdated API

**Solution**: Use `@google/genai`, NOT `@google/generative-ai`

```bash
npm uninstall @google/generative-ai
bun add @google/genai@1.27.0
```

---

### Error 2: Invalid API Key (401)

**Error**: `API key not valid`

**Solution**: Verify environment variable

```bash
export GEMINI_API_KEY="your-key"
```

---

### Error 3: Model Not Found (404)

**Error**: `models/gemini-3.0-flash is not found`

**Solution**: Use correct model names (2025)

```typescript
'gemini-2.5-pro'
'gemini-2.5-flash'
'gemini-2.5-flash-lite'
```

---

### Error 4: Context Length Exceeded (400)

**Error**: `Request payload size exceeds the limit`

**Solution**: Input limit is **1,048,576 tokens (1M, NOT 2M)**. Use context caching for large inputs.

**Load `references/context-caching-guide.md` for caching implementation.**

---

### Error 5: Rate Limit Exceeded (429)

**Error**: `Resource has been exhausted`

**Solution**: Implement exponential backoff

```typescript
async function generateWithRetry(request, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await ai.models.generateContent(request);
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
}
```

---

**See All 22 Errors**: Load `references/error-catalog.md` for complete error catalog with solutions.

**Quick Debugging**: Load `references/top-errors.md` for debugging checklist.

---

## When to Load References

Load reference files when you need detailed guidance on specific features:

### Core Features (Load When Needed)
- **SDK Migration**: Load `references/sdk-migration-guide.md` when migrating from `@google/generative-ai`
- **Model Selection**: Load `references/models-guide.md` when choosing between Pro/Flash/Flash-Lite
- **Error Debugging**: Load `references/error-catalog.md` or `references/top-errors.md` when encountering errors

### Advanced Features (Load When Implementing)
- **Context Caching**: Load `references/context-caching-guide.md` when implementing cost optimization for large/repeated inputs
- **Code Execution**: Load `references/code-execution-patterns.md` when enabling Python code execution for calculations/analysis
- **Grounding (Google Search)**: Load `references/grounding-guide.md` when connecting model to real-time web information
- **Streaming Implementation**: Load `references/streaming-patterns.md` when implementing SSE parsing for Cloudflare Workers
- **Function Calling Modes**: Load `references/function-calling-patterns.md` when using AUTO/ANY/NONE modes or compositional patterns
- **Multimodal Formats**: Load `references/multimodal-guide.md` when working with images/video/audio/PDFs (format specs, size limits)
- **Generation Tuning**: Load `references/generation-config.md` when fine-tuning temperature/topP/topK parameters
- **Thinking Mode Config**: Load `references/thinking-mode-guide.md` when optimizing thinking budget for complex reasoning

**General Rule**: SKILL.md provides Quick Start and Top Errors. Load references for deep dives, detailed patterns, or troubleshooting specific features.

---

## Bundled Resources

**Templates** (`templates/`):
- `basic-usage.ts` - Complete examples for all features (133 lines)

**References** (`references/`):
- `error-catalog.md` - All 7 documented errors with solutions (231 lines)
- `top-errors.md` - Quick debugging checklist for 22 common errors (305 lines)
- `sdk-migration-guide.md` - Complete migration from deprecated SDK (236 lines)
- `models-guide.md` - Detailed model comparison and selection guide (247 lines)
- `context-caching-guide.md` - Cost optimization with caching (374 lines)
- `code-execution-patterns.md` - Python code execution guide (482 lines)
- `grounding-guide.md` - Google Search integration (603 lines)
- `streaming-patterns.md` - SSE implementation for Cloudflare Workers (82 lines)
- `function-calling-patterns.md` - Advanced function calling patterns (60 lines)
- `multimodal-guide.md` - Format specifications and limits (59 lines)
- `generation-config.md` - Parameter tuning reference (58 lines)
- `thinking-mode-guide.md` - Thinking budget optimization (60 lines)

---

## Integration with Other Skills

This skill composes well with:

- **cloudflare-worker-base** → Deploy to Cloudflare Workers
- **ai-sdk-core** → Vercel AI SDK integration
- **openai-api** → Multi-provider AI setup
- **google-gemini-embeddings** → Text embeddings

---

## Additional Resources

**Official Documentation**:
- Gemini API Docs: https://ai.google.dev/gemini-api/docs
- SDK Reference: https://ai.google.dev/gemini-api/docs/sdks
- Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits

---

**Production Tested**: AI chatbots, content generation, multimodal analysis
**Last Updated**: 2025-10-25
**Token Savings**: ~65% (reduces API docs + examples)
