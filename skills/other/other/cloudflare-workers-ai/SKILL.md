---
name: cloudflare-workers-ai
description: |
  Run LLMs and AI models on Cloudflare's GPU network with Workers AI. Includes Llama 4, Gemma 3, Mistral 3.1, Flux images, BGE embeddings, streaming, and AI Gateway. Handles 2025 breaking changes. Prevents 7 documented errors.

  Use when: implementing LLM inference, images, RAG, or troubleshooting AI_ERROR, rate limits, max_tokens, BGE pooling, context window, neuron billing, Miniflare AI binding, NSFW filter, num_steps.
user-invocable: true
---

# Cloudflare Workers AI

**Status**: Production Ready ✅
**Last Updated**: 2026-01-21
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: wrangler@4.58.0, @cloudflare/workers-types@4.20260109.0, workers-ai-provider@3.0.2

**Recent Updates (2025)**:
- **April 2025 - Performance**: Llama 3.3 70B 2-4x faster (speculative decoding, prefix caching), BGE embeddings 2x faster
- **April 2025 - Breaking Changes**: max_tokens now correctly defaults to 256 (was not respected), BGE pooling parameter (cls NOT backwards compatible with mean)
- **2025 - New Models (14)**: Mistral 3.1 24B (vision+tools), Gemma 3 12B (128K context), EmbeddingGemma 300M, Llama 4 Scout, GPT-OSS 120B/20B, Qwen models (QwQ 32B, Coder 32B), Leonardo image gen, Deepgram Aura 2, Whisper v3 Turbo, IBM Granite, Nova 3
- **2025 - Platform**: Context windows API change (tokens not chars), unit-based pricing with per-model granularity, workers-ai-provider v3.0.2 (AI SDK v5), LoRA rank up to 32 (was 8), 100 adapters per account
- **October 2025**: Model deprecations (use Llama 4, GPT-OSS instead)

---

## Quick Start (5 Minutes)

```typescript
// 1. Add AI binding to wrangler.jsonc
{ "ai": { "binding": "AI" } }

// 2. Run model with streaming (recommended)
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const stream = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
      messages: [{ role: 'user', content: 'Tell me a story' }],
      stream: true, // Always stream for text generation!
    });

    return new Response(stream, {
      headers: { 'content-type': 'text/event-stream' },
    });
  },
};
```

**Why streaming?** Prevents buffering in memory, faster time-to-first-token, avoids Worker timeout issues.

---

## Known Issues Prevention

This skill prevents **7** documented issues:

### Issue #1: Context Window Validation Changed to Tokens (February 2025)

**Error**: `"Exceeded character limit"` despite model supporting larger context
**Source**: [Cloudflare Changelog](https://developers.cloudflare.com/changelog/2025-02-24-context-windows/)
**Why It Happens**: Before February 2025, Workers AI validated prompts using a hard 6144 character limit, even for models with larger token-based context windows (e.g., Mistral with 32K tokens). After the update, validation switched to token-based counting.
**Prevention**: Calculate tokens (not characters) when checking context window limits.

```typescript
import { encode } from 'gpt-tokenizer'; // or model-specific tokenizer

const tokens = encode(prompt);
const contextWindow = 32768; // Model's max tokens (check docs)
const maxResponseTokens = 2048;

if (tokens.length + maxResponseTokens > contextWindow) {
  throw new Error(`Prompt exceeds context window: ${tokens.length} tokens`);
}

const response = await env.AI.run('@cf/mistral/mistral-7b-instruct-v0.2', {
  messages: [{ role: 'user', content: prompt }],
  max_tokens: maxResponseTokens,
});
```

### Issue #2: Neuron Consumption Discrepancies in Dashboard

**Error**: Dashboard neuron usage significantly exceeds expected token-based calculations
**Source**: [Cloudflare Community Discussion](https://community.cloudflare.com/t/amount-of-the-neurons-used-for-the-text-generation-does-not-correspond-pricing-doc/788301)
**Why It Happens**: Users report dashboard showing hundred-million-level neuron consumption for K-level token usage, particularly with AutoRAG features and certain models. The discrepancy between expected neuron consumption (based on pricing docs) and actual dashboard metrics is not fully documented.
**Prevention**: Monitor neuron usage via AI Gateway logs and correlate with requests. File support ticket if consumption significantly exceeds expectations.

```typescript
// Use AI Gateway for detailed request logging
const response = await env.AI.run(
  '@cf/meta/llama-3.1-8b-instruct',
  { messages: [{ role: 'user', content: query }] },
  { gateway: { id: 'my-gateway' } }
);

// Monitor dashboard at: https://dash.cloudflare.com → AI → Workers AI
// Compare neuron usage with token counts
// File support ticket with details if discrepancy persists
```

### Issue #3: AI Binding Requires Remote or Latest Tooling in Local Dev

**Error**: `"MiniflareCoreError: wrapped binding module can't be resolved (internal modules only)"`
**Source**: [GitHub Issue #6796](https://github.com/cloudflare/workers-sdk/issues/6796)
**Why It Happens**: When using Workers AI bindings with Miniflare in local development (particularly with custom Vite plugins), the AI binding requires external workers that aren't properly exposed by older `unstable_getMiniflareWorkerOptions`. The error occurs when Miniflare can't resolve the internal AI worker module.
**Prevention**: Use remote bindings for AI in local dev, or update to latest @cloudflare/vite-plugin.

```jsonc
// wrangler.jsonc - Option 1: Use remote AI binding in local dev
{
  "ai": { "binding": "AI" },
  "dev": {
    "remote": true // Use production AI binding locally
  }
}
```

```bash
# Option 2: Update to latest tooling
npm install -D @cloudflare/vite-plugin@latest

# Option 3: Use wrangler dev instead of custom Miniflare
npm run dev
```

### Issue #4: Flux Image Generation NSFW Filter False Positives

**Error**: `"AiError: Input prompt contains NSFW content (code 3030)"` for innocent prompts
**Source**: [Cloudflare Community Discussion](https://community.cloudflare.com/t/image-rendering-issue-with-flux-api-nsfw-warning/729440)
**Why It Happens**: Flux image generation models (`@cf/black-forest-labs/flux-1-schnell`) sometimes trigger false positive NSFW content errors even with innocent single-word prompts like "hamburger". The NSFW filter can be overly sensitive without context.
**Prevention**: Add descriptive context around potential trigger words instead of using single-word prompts.

```typescript
// ❌ May trigger error 3030
const response = await env.AI.run('@cf/black-forest-labs/flux-1-schnell', {
  prompt: 'hamburger', // Single word triggers filter
});

// ✅ Add context to avoid false positives
const response = await env.AI.run('@cf/black-forest-labs/flux-1-schnell', {
  prompt: 'A photo of a delicious large hamburger on a plate with lettuce and tomato',
  num_steps: 4,
});
```

### Issue #5: Image Generation Error 1000 - Missing num_steps Parameter

**Error**: `"Error: unexpected type 'int32' with value 'undefined' (code 1000)"`
**Source**: [Cloudflare Community Discussion](https://community.cloudflare.com/t/ai-api-call-for-image-generation-returns-1000-error-minimal-error-msg/616994)
**Why It Happens**: Image generation API calls return error code 1000 when the `num_steps` parameter is not provided, even though documentation suggests it's optional. The parameter is actually required for most Flux models.
**Prevention**: Always include `num_steps: 4` for image generation models (typically 4 for Flux Schnell).

```typescript
// ✅ Always include num_steps for image generation
const image = await env.AI.run('@cf/black-forest-labs/flux-1-schnell', {
  prompt: 'A beautiful sunset over mountains',
  num_steps: 4, // Required - typically 4 for Flux Schnell
});

// Note: FLUX.2 [klein] 4B has fixed steps=4 (cannot be adjusted)
```

### Issue #6: Zod v4 Incompatibility with Structured Output Tools

**Error**: Syntax errors and failed transpilation when using Stagehand with Zod v4
**Source**: [GitHub Issue #10798](https://github.com/cloudflare/workers-sdk/issues/10798)
**Why It Happens**: Stagehand (browser automation) and some structured output examples in Workers AI fail with Zod v4 (now default). The underlying `zod-to-json-schema` library doesn't yet support Zod v4, causing transpilation failures.
**Prevention**: Pin Zod to v3 until zod-to-json-schema supports v4.

```bash
# Install Zod v3 specifically
npm install zod@3

# Or pin in package.json
{
  "dependencies": {
    "zod": "~3.23.8" // Pin to v3 for compatibility
  }
}
```

### Issue #7: AI Gateway Cache Headers for Per-Request Control

**Not an error, but important feature**: AI Gateway supports per-request cache control via HTTP headers for custom TTL, cache bypass, and custom cache keys beyond dashboard defaults.
**Source**: [AI Gateway Caching Documentation](https://developers.cloudflare.com/ai-gateway/features/caching/)
**Use When**: You need different caching behavior for different requests (e.g., 1 hour for expensive queries, skip cache for real-time data).
**Implementation**: See AI Gateway Integration section below for header usage.

---

## API Reference

```typescript
env.AI.run(
  model: string,
  inputs: ModelInputs,
  options?: { gateway?: { id: string; skipCache?: boolean } }
): Promise<ModelOutput | ReadableStream>
```

---

## Model Selection Guide (Updated 2025)

### Text Generation (LLMs)

| Model | Best For | Rate Limit | Size | Notes |
|-------|----------|------------|------|-------|
| **2025 Models** |
| `@cf/meta/llama-4-scout-17b-16e-instruct` | Latest Llama, general purpose | 300/min | 17B | NEW 2025 |
| `@cf/openai/gpt-oss-120b` | Largest open-source GPT | 300/min | 120B | NEW 2025 |
| `@cf/openai/gpt-oss-20b` | Smaller open-source GPT | 300/min | 20B | NEW 2025 |
| `@cf/google/gemma-3-12b-it` | 128K context, 140+ languages | 300/min | 12B | NEW 2025, vision |
| `@cf/mistralai/mistral-small-3.1-24b-instruct` | Vision + tool calling | 300/min | 24B | NEW 2025 |
| `@cf/qwen/qwq-32b` | Reasoning, complex tasks | 300/min | 32B | NEW 2025 |
| `@cf/qwen/qwen2.5-coder-32b-instruct` | Coding specialist | 300/min | 32B | NEW 2025 |
| `@cf/qwen/qwen3-30b-a3b-fp8` | Fast quantized | 300/min | 30B | NEW 2025 |
| `@cf/ibm-granite/granite-4.0-h-micro` | Small, efficient | 300/min | Micro | NEW 2025 |
| **Performance (2025)** |
| `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | 2-4x faster (2025 update) | 300/min | 70B | Speculative decoding |
| `@cf/meta/llama-3.1-8b-instruct-fp8-fast` | Fast 8B variant | 300/min | 8B | - |
| **Standard Models** |
| `@cf/meta/llama-3.1-8b-instruct` | General purpose | 300/min | 8B | - |
| `@cf/meta/llama-3.2-1b-instruct` | Ultra-fast, simple tasks | 300/min | 1B | - |
| `@cf/deepseek-ai/deepseek-r1-distill-qwen-32b` | Coding, technical | 300/min | 32B | - |

### Text Embeddings (2x Faster - 2025)

| Model | Dimensions | Best For | Rate Limit | Notes |
|-------|-----------|----------|------------|-------|
| `@cf/google/embeddinggemma-300m` | 768 | Best-in-class RAG | 3000/min | **NEW 2025** |
| `@cf/baai/bge-base-en-v1.5` | 768 | General RAG (2x faster) | 3000/min | **pooling: "cls"** recommended |
| `@cf/baai/bge-large-en-v1.5` | 1024 | High accuracy (2x faster) | 1500/min | **pooling: "cls"** recommended |
| `@cf/baai/bge-small-en-v1.5` | 384 | Fast, low storage (2x faster) | 3000/min | **pooling: "cls"** recommended |
| `@cf/qwen/qwen3-embedding-0.6b` | 768 | Qwen embeddings | 3000/min | NEW 2025 |

**CRITICAL (2025)**: BGE models now support `pooling: "cls"` parameter (recommended) but NOT backwards compatible with `pooling: "mean"` (default).

### Image Generation

| Model | Best For | Rate Limit | Notes |
|-------|----------|------------|-------|
| `@cf/black-forest-labs/flux-1-schnell` | High quality, photorealistic | 720/min | ⚠️ See warnings below |
| `@cf/leonardo/lucid-origin` | Leonardo AI style | 720/min | NEW 2025, requires num_steps |
| `@cf/leonardo/phoenix-1.0` | Leonardo AI variant | 720/min | NEW 2025, requires num_steps |
| `@cf/stabilityai/stable-diffusion-xl-base-1.0` | General purpose | 720/min | Requires num_steps |

**⚠️ Common Image Generation Issues:**
- **Error 1000**: Always include `num_steps: 4` parameter (required despite docs suggesting optional)
- **Error 3030 (NSFW filter)**: Single words like "hamburger" may trigger false positives - add descriptive context to prompts

```typescript
// ✅ Correct pattern for image generation
const image = await env.AI.run('@cf/black-forest-labs/flux-1-schnell', {
  prompt: 'A photo of a delicious hamburger on a plate with fresh vegetables',
  num_steps: 4, // Required to avoid error 1000
});
// Descriptive context helps avoid NSFW false positives (error 3030)
```

### Vision Models

| Model | Best For | Rate Limit | Notes |
|-------|----------|------------|-------|
| `@cf/meta/llama-3.2-11b-vision-instruct` | Image understanding | 720/min | - |
| `@cf/google/gemma-3-12b-it` | Vision + text (128K context) | 300/min | NEW 2025 |

### Audio Models (2025)

| Model | Type | Rate Limit | Notes |
|-------|------|------------|-------|
| `@cf/deepgram/aura-2-en` | Text-to-speech (English) | 720/min | NEW 2025 |
| `@cf/deepgram/aura-2-es` | Text-to-speech (Spanish) | 720/min | NEW 2025 |
| `@cf/deepgram/nova-3` | Speech-to-text (+ WebSocket) | 720/min | NEW 2025 |
| `@cf/openai/whisper-large-v3-turbo` | Speech-to-text (faster) | 720/min | NEW 2025 |

---

## Common Patterns

### RAG (Retrieval Augmented Generation)

```typescript
// 1. Generate embeddings
const embeddings = await env.AI.run('@cf/baai/bge-base-en-v1.5', { text: [userQuery] });

// 2. Search Vectorize
const matches = await env.VECTORIZE.query(embeddings.data[0], { topK: 3 });
const context = matches.matches.map((m) => m.metadata.text).join('\n\n');

// 3. Generate with context
const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [
    { role: 'system', content: `Answer using this context:\n${context}` },
    { role: 'user', content: userQuery },
  ],
  stream: true,
});
```

---

### Structured Output with Zod

```typescript
import { z } from 'zod';

const Schema = z.object({ name: z.string(), items: z.array(z.string()) });

const response = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
  messages: [{
    role: 'user',
    content: `Generate JSON matching: ${JSON.stringify(Schema.shape)}`
  }],
});

const validated = Schema.parse(JSON.parse(response.response));
```

---

## AI Gateway Integration

Provides caching, logging, cost tracking, and analytics for AI requests.

### Basic Gateway Usage

```typescript
const response = await env.AI.run(
  '@cf/meta/llama-3.1-8b-instruct',
  { prompt: 'Hello' },
  { gateway: { id: 'my-gateway', skipCache: false } }
);

// Access logs and send feedback
const gateway = env.AI.gateway('my-gateway');
await gateway.patchLog(env.AI.aiGatewayLogId, {
  feedback: { rating: 1, comment: 'Great response' },
});
```

### Per-Request Cache Control (Advanced)

Override default cache behavior with HTTP headers for fine-grained control:

```typescript
// Custom cache TTL (1 hour for expensive queries)
const response = await fetch(
  `https://gateway.ai.cloudflare.com/v1/${accountId}/${gatewayId}/workers-ai/@cf/meta/llama-3.1-8b-instruct`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.CLOUDFLARE_API_KEY}`,
      'Content-Type': 'application/json',
      'cf-aig-cache-ttl': '3600', // 1 hour in seconds (min: 60, max: 2592000)
    },
    body: JSON.stringify({
      messages: [{ role: 'user', content: prompt }],
    }),
  }
);

// Skip cache for real-time data
const response = await fetch(gatewayUrl, {
  headers: {
    'cf-aig-skip-cache': 'true', // Bypass cache entirely
  },
  // ...
});

// Check if response was cached
const cacheStatus = response.headers.get('cf-aig-cache-status'); // "HIT" or "MISS"
```

**Available Cache Headers:**
- `cf-aig-cache-ttl`: Set custom TTL in seconds (60s to 1 month)
- `cf-aig-skip-cache`: Bypass cache entirely (`'true'`)
- `cf-aig-cache-key`: Custom cache key for granular control
- `cf-aig-cache-status`: Response header showing `"HIT"` or `"MISS"`

**Benefits:** Cost tracking, caching (reduces duplicate inference), logging, rate limiting, analytics, per-request cache customization.

---

## Rate Limits & Pricing (Updated 2025)

### Rate Limits (per minute)

| Task Type | Default Limit | Notes |
|-----------|---------------|-------|
| **Text Generation** | 300/min | Some fast models: 400-1500/min |
| **Text Embeddings** | 3000/min | BGE-large: 1500/min |
| **Image Generation** | 720/min | All image models |
| **Vision Models** | 720/min | Image understanding |
| **Audio (TTS/STT)** | 720/min | Deepgram, Whisper |
| **Translation** | 720/min | M2M100, Opus MT |
| **Classification** | 2000/min | Text classification |

### Pricing (Unit-Based, Billed in Neurons - 2025)

**Free Tier:**
- 10,000 neurons per day
- Resets daily at 00:00 UTC

**Paid Tier ($0.011 per 1,000 neurons):**
- 10,000 neurons/day included
- Unlimited usage above free allocation

**2025 Model Costs (per 1M tokens):**

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| **2025 Models** |
| Llama 4 Scout 17B | $0.270 | $0.850 | NEW 2025 |
| GPT-OSS 120B | $0.350 | $0.750 | NEW 2025 |
| GPT-OSS 20B | $0.200 | $0.300 | NEW 2025 |
| Gemma 3 12B | $0.345 | $0.556 | NEW 2025 |
| Mistral 3.1 24B | $0.351 | $0.555 | NEW 2025 |
| Qwen QwQ 32B | $0.660 | $1.000 | NEW 2025 |
| Qwen Coder 32B | $0.660 | $1.000 | NEW 2025 |
| IBM Granite Micro | $0.017 | $0.112 | NEW 2025 |
| EmbeddingGemma 300M | $0.012 | N/A | NEW 2025 |
| Qwen3 Embedding 0.6B | $0.012 | N/A | NEW 2025 |
| **Performance (2025)** |
| Llama 3.3 70B Fast | $0.293 | $2.253 | 2-4x faster |
| Llama 3.1 8B FP8 Fast | $0.045 | $0.384 | Fast variant |
| **Standard Models** |
| Llama 3.2 1B | $0.027 | $0.201 | - |
| Llama 3.1 8B | $0.282 | $0.827 | - |
| Deepseek R1 32B | $0.497 | $4.881 | - |
| BGE-base (2x faster) | $0.067 | N/A | 2025 speedup |
| BGE-large (2x faster) | $0.204 | N/A | 2025 speedup |
| **Image Models (2025)** |
| Flux 1 Schnell | $0.0000528 per 512x512 tile | - |
| Leonardo Lucid | $0.006996 per 512x512 tile | NEW 2025 |
| Leonardo Phoenix | $0.005830 per 512x512 tile | NEW 2025 |
| **Audio Models (2025)** |
| Deepgram Aura 2 | $0.030 per 1k chars | NEW 2025 |
| Deepgram Nova 3 | $0.0052 per audio min | NEW 2025 |
| Whisper v3 Turbo | $0.0005 per audio min | NEW 2025 |

---

## Error Handling with Retry

```typescript
async function runAIWithRetry(
  env: Env,
  model: string,
  inputs: any,
  maxRetries = 3
): Promise<any> {
  let lastError: Error;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await env.AI.run(model, inputs);
    } catch (error) {
      lastError = error as Error;

      // Rate limit - retry with exponential backoff
      if (lastError.message.toLowerCase().includes('rate limit')) {
        await new Promise((resolve) => setTimeout(resolve, Math.pow(2, i) * 1000));
        continue;
      }

      throw error; // Other errors - fail immediately
    }
  }

  throw lastError!;
}
```

---

## OpenAI Compatibility

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: env.CLOUDFLARE_API_KEY,
  baseURL: `https://api.cloudflare.com/client/v4/accounts/${env.ACCOUNT_ID}/ai/v1`,
});

// Chat completions
await openai.chat.completions.create({
  model: '@cf/meta/llama-3.1-8b-instruct',
  messages: [{ role: 'user', content: 'Hello!' }],
});
```

**Endpoints:** `/v1/chat/completions`, `/v1/embeddings`

---

## Vercel AI SDK Integration (workers-ai-provider v3.0.2)

```typescript
import { createWorkersAI } from 'workers-ai-provider'; // v3.0.2 with AI SDK v5
import { generateText, streamText } from 'ai';

const workersai = createWorkersAI({ binding: env.AI });

// Generate or stream
await generateText({
  model: workersai('@cf/meta/llama-3.1-8b-instruct'),
  prompt: 'Write a poem',
});
```

---

## Community Tips

> **Note**: These tips come from community discussions and production experience.

### Hono Framework Streaming Pattern

When using Workers AI streaming with Hono, return the stream directly as a Response (not through Hono's streaming utilities):

```typescript
import { Hono } from 'hono';

type Bindings = { AI: Ai };
const app = new Hono<{ Bindings: Bindings }>();

app.post('/chat', async (c) => {
  const { prompt } = await c.req.json();

  const stream = await c.env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [{ role: 'user', content: prompt }],
    stream: true,
  });

  // Return stream directly (not c.stream())
  return new Response(stream, {
    headers: {
      'content-type': 'text/event-stream',
      'cache-control': 'no-cache',
      'connection': 'keep-alive',
    },
  });
});
```

**Source**: [Hono Discussion #2409](https://github.com/orgs/honojs/discussions/2409)

### Troubleshooting Unexplained AI Binding Failures

If experiencing unexplained Workers AI failures:

```bash
# 1. Check wrangler version
npx wrangler --version

# 2. Clear wrangler cache
rm -rf ~/.wrangler

# 3. Update to latest stable
npm install -D wrangler@latest

# 4. Check local network/firewall settings
# Some corporate firewalls block Workers AI endpoints
```

**Note**: Most "version incompatibility" issues turn out to be network configuration problems.

---

## References

- [Workers AI Docs](https://developers.cloudflare.com/workers-ai/)
- [Models Catalog](https://developers.cloudflare.com/workers-ai/models/)
- [AI Gateway](https://developers.cloudflare.com/ai-gateway/)
- [Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Changelog](https://developers.cloudflare.com/workers-ai/changelog/)
- [LoRA Adapters](https://developers.cloudflare.com/workers-ai/features/fine-tunes/loras/)
- **MCP Tool**: Use `mcp__cloudflare-docs__search_cloudflare_documentation` for latest docs
