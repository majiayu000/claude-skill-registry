---
name: cloudflare-workers-ai
description: Cloudflare Workers AI for serverless GPU inference. Use for LLMs, text/image generation, embeddings, or encountering AI_ERROR, rate limits, token exceeded errors.

  Keywords: workers ai, cloudflare ai, ai bindings, llm workers, @cf/meta/llama, workers ai models,
  ai inference, cloudflare llm, ai streaming, text generation ai, ai embeddings, image generation ai,
  workers ai rag, ai gateway, llama workers, flux image generation, stable diffusion workers,
  vision models ai, ai chat completion, AI_ERROR, rate limit ai, model not found, token limit exceeded,
  neurons exceeded, ai quota exceeded, streaming failed, model unavailable, workers ai hono,
  ai gateway workers, vercel ai sdk workers, openai compatible workers, workers ai vectorize
license: MIT
---

# Cloudflare Workers AI - Complete Reference

Production-ready knowledge domain for building AI-powered applications with Cloudflare Workers AI.

**Status**: Production Ready ✅
**Last Updated**: 2025-11-21
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.43.0, @cloudflare/workers-types@4.20251014.0

---

## Table of Contents

1. [Quick Start (5 minutes)](#quick-start-5-minutes)
2. [Workers AI API Reference](#workers-ai-api-reference)
3. [Model Selection Guide](#model-selection-guide)
4. [Common Patterns](#common-patterns)
5. [AI Gateway Integration](#ai-gateway-integration)
6. [Rate Limits & Pricing](#rate-limits--pricing)
7. [Production Checklist](#production-checklist)

---

## Quick Start (5 minutes)

### 1. Add AI Binding

**wrangler.jsonc:**
```jsonc
{
  "ai": {
    "binding": "AI"
  }
}
```

### 2. Run Your First Model

```typescript
export interface Env {
  AI: Ai;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
      prompt: 'What is Cloudflare?',
    });

    return Response.json(response);
  },
};
```

### 3. Add Streaming (Recommended)

```typescript
const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{ role: 'user', content: 'Tell me a story' }],
  stream: true, // Always use streaming for text generation!
});

return new Response(stream, {
  headers: { 'content-type': 'text/event-stream' },
});
```

**Why streaming?**
- Prevents buffering large responses in memory
- Faster time-to-first-token
- Better user experience for long-form content
- Avoids Worker timeout issues

---

## Workers AI API Reference

### Core API: `env.AI.run()`

```typescript
const response = await env.AI.run(model, inputs, options?);
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (e.g., `@cf/meta/llama-3.1-8b-instruct`) |
| `inputs` | object | Model-specific inputs (see model type below) |
| `options.gateway.id` | string | AI Gateway ID for caching/logging |
| `options.gateway.skipCache` | boolean | Skip AI Gateway cache |

**Returns**: `Promise<ModelOutput>` (non-streaming) or `ReadableStream` (streaming)

### Input Types by Model Category

| Category | Key Inputs | Output |
|----------|------------|--------|
| **Text Generation** | `messages[]`, `stream`, `max_tokens`, `temperature` | `{ response: string }` |
| **Embeddings** | `text: string \| string[]` | `{ data: number[][], shape: number[] }` |
| **Image Generation** | `prompt`, `num_steps`, `guidance` | Binary PNG |
| **Vision** | `messages[].content[].image_url` | `{ response: string }` |

📄 **Full model details**: Load `references/models-catalog.md` for complete model list, parameters, and rate limits.

---

## Model Selection Guide

### Text Generation (LLMs)

| Model | Best For | Rate Limit | Size |
|-------|----------|------------|------|
| `@cf/meta/llama-3.1-8b-instruct` | General purpose, fast | 300/min | 8B |
| `@cf/meta/llama-3.2-1b-instruct` | Ultra-fast, simple tasks | 300/min | 1B |
| `@cf/qwen/qwen1.5-14b-chat-awq` | High quality, complex reasoning | 150/min | 14B |
| `@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | Coding, technical content | 300/min | 32B |
| `@hf/thebloke/mistral-7b-instruct-v0.1-awq` | Fast, efficient | 400/min | 7B |

### Text Embeddings

| Model | Dimensions | Best For | Rate Limit |
|-------|-----------|----------|------------|
| `@cf/baai/bge-base-en-v1.5` | 768 | General purpose RAG | 3000/min |
| `@cf/baai/bge-large-en-v1.5` | 1024 | High accuracy search | 1500/min |
| `@cf/baai/bge-small-en-v1.5` | 384 | Fast, low storage | 3000/min |

### Image Generation

| Model | Best For | Rate Limit | Speed |
|-------|----------|------------|-------|
| `@cf/black-forest-labs/flux-1-schnell` | High quality, photorealistic | 720/min | Fast |
| `@cf/stabilityai/stable-diffusion-xl-base-1.0` | General purpose | 720/min | Medium |
| `@cf/lykon/dreamshaper-8-lcm` | Artistic, stylized | 720/min | Fast |

### Vision Models

| Model | Best For | Rate Limit |
|-------|----------|------------|
| `@cf/meta/llama-3.2-11b-vision-instruct` | Image understanding | 720/min |
| `@cf/unum/uform-gen2-qwen-500m` | Fast image captioning | 720/min |

---

## Common Patterns

### Pattern 1: Chat with Streaming

```typescript
app.post('/chat', async (c) => {
  const { messages } = await c.req.json<{ messages: Array<{ role: string; content: string }> }>();
  const stream = await c.env.AI.run('@cf/meta/llama-3.1-8b-instruct', { messages, stream: true });
  return new Response(stream, { headers: { 'content-type': 'text/event-stream' } });
});
```

### Pattern 2: RAG (Retrieval Augmented Generation)

```typescript
// 1. Generate embedding for query
const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [userQuery] });
// 2. Search Vectorize
const matches = await env.VECTORIZE.query(embeddings.data[0], { topK: 3 });
// 3. Build context
const context = matches.matches.map((m) => m.metadata.text).join('\n\n');
// 4. Generate with context
const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [
    { role: 'system', content: `Answer using this context:\n${context}` },
    { role: 'user', content: userQuery },
  ],
  stream: true,
});
return new Response(stream, { headers: { 'content-type': 'text/event-stream' } });
```

📄 **More patterns**: Load `references/best-practices.md` for structured output, image generation, multi-model consensus, and production patterns.

---

## AI Gateway Integration

Enable caching, logging, and cost tracking with AI Gateway:

```typescript
const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', { prompt: 'Hello' }, {
  gateway: { id: 'my-gateway', skipCache: false },
});
```

**Benefits**: Cost tracking, response caching (50-90% savings on repeated queries), request logging, rate limiting, analytics.

---

## Rate Limits & Pricing

**Information last verified**: 2025-01-14

Rate limits and pricing vary significantly by model. Always check the official documentation for the most current information:

- **Rate Limits**: https://developers.cloudflare.com/workers-ai/platform/limits/
- **Pricing**: https://developers.cloudflare.com/workers-ai/platform/pricing/

**Free Tier**: 10,000 neurons/day
**Paid Tier**: $0.011 per 1,000 neurons

📄 **Per-model details**: See `references/models-catalog.md` for specific rate limits and pricing for each model.

---

## Production Checklist

**Essential before deploying:**
- [ ] Enable AI Gateway for cost tracking
- [ ] Implement streaming for text generation
- [ ] Add rate limit retry with exponential backoff
- [ ] Validate input length (prevent token limit errors)
- [ ] Add input sanitization (prevent prompt injection)

📄 **Full checklist**: Load `references/best-practices.md` for complete production checklist, error handling patterns, monitoring, and cost optimization.

---

## External SDK Integrations

Workers AI supports OpenAI SDK compatibility and Vercel AI SDK:

```typescript
// OpenAI SDK - use same patterns with Workers AI models
const openai = new OpenAI({
  apiKey: env.CLOUDFLARE_API_KEY,
  baseURL: `https://api.cloudflare.com/client/v4/accounts/${env.CLOUDFLARE_ACCOUNT_ID}/ai/v1`,
});

// Vercel AI SDK - native integration
import { createWorkersAI } from 'workers-ai-provider';
const workersai = createWorkersAI({ binding: env.AI });
```

📄 **Full integration guide**: Load `references/integrations.md` for OpenAI SDK, Vercel AI SDK, and REST API examples.

---

## Limits Summary

| Feature | Limit |
|---------|-------|
| Concurrent requests | No hard limit (rate limits apply) |
| Max input tokens | Varies by model (typically 2K-128K) |
| Max output tokens | Varies by model (typically 512-2048) |
| Streaming chunk size | ~1 KB |
| Image size (output) | ~5 MB |
| Request timeout | Workers timeout applies (30s default, 5m max CPU) |
| Daily free neurons | 10,000 |
| Rate limits | See "Rate Limits & Pricing" section |

---

## When to Load References

| Reference File | Load When... |
|----------------|--------------|
| `references/models-catalog.md` | Choosing a model, checking rate limits, comparing model capabilities |
| `references/best-practices.md` | Production deployment, error handling, cost optimization, security |
| `references/integrations.md` | Using OpenAI SDK, Vercel AI SDK, or REST API instead of native binding |

---

## References

- [Workers AI Docs](https://developers.cloudflare.com/workers-ai/)
- [Models Catalog](https://developers.cloudflare.com/workers-ai/models/)
- [AI Gateway](https://developers.cloudflare.com/ai-gateway/)
- [Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
