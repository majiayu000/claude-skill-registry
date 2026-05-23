---
name: llm-gateway-routing
description: |
  LLM gateway and routing configuration using OpenRouter and LiteLLM.
  Invoke when:
  - Setting up multi-model access (OpenRouter, LiteLLM)
  - Configuring model fallbacks and reliability
  - Implementing cost-based or latency-based routing
  - A/B testing different models
  - Self-hosting an LLM proxy
  Keywords: openrouter, litellm, llm gateway, model routing, fallback, A/B testing
effort: high
---

# LLM Gateway & Routing

Configure multi-model access, fallbacks, cost optimization, and A/B testing.

## Why Use a Gateway?

**Without gateway:**
- Vendor lock-in (one provider)
- No fallbacks (provider down = app down)
- Hard to A/B test models
- Scattered API keys and configs

**With gateway:**
- Single API for 400+ models
- Automatic fallbacks
- Easy model switching
- Unified cost tracking

## Quick Decision

| Need | Solution |
|------|----------|
| Fastest setup, multi-model | **OpenRouter** |
| Full control, self-hosted | **LiteLLM** |
| Observability + routing | **Helicone** |
| Enterprise, guardrails | **Portkey** |

## OpenRouter (Recommended)

### Why OpenRouter

- **400+ models**: OpenAI, Anthropic, Google, Meta, Mistral, and more
- **Single API**: One key for all providers
- **Automatic fallbacks**: Built-in reliability
- **A/B testing**: Easy model comparison
- **Cost tracking**: Unified billing dashboard
- **Free credits**: $1 free to start

### Setup

```bash
# 1. Sign up at openrouter.ai
# 2. Get API key from dashboard
# 3. Add to .env:
OPENROUTER_API_KEY=sk-or-v1-...
```

### Basic Usage

```typescript
// Using fetch
const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'anthropic/claude-3-5-sonnet',
    messages: [{ role: 'user', content: 'Hello!' }],
  }),
});
```

### With Vercel AI SDK (Recommended)

```typescript
import { createOpenAI } from "@ai-sdk/openai";
import { generateText } from "ai";

const openrouter = createOpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
});

const { text } = await generateText({
  model: openrouter("anthropic/claude-3-5-sonnet"),
  prompt: "Explain quantum computing",
});
```

### Model IDs

```typescript
// Format: provider/model-name
const models = {
  // Anthropic
  claude35Sonnet: "anthropic/claude-3-5-sonnet",
  claudeHaiku: "anthropic/claude-3-5-haiku",

  // OpenAI
  gpt4o: "openai/gpt-4o",
  gpt4oMini: "openai/gpt-4o-mini",

  // Google
  geminiPro: "google/gemini-pro-1.5",
  geminiFlash: "google/gemini-flash-1.5",

  // Meta
  llama3: "meta-llama/llama-3.1-70b-instruct",

  // Auto (OpenRouter picks best)
  auto: "openrouter/auto",
};
```

### Fallback Chains

```typescript
// Define fallback order
const modelChain = [
  "anthropic/claude-3-5-sonnet",   // Primary
  "openai/gpt-4o",                  // Fallback 1
  "google/gemini-pro-1.5",          // Fallback 2
];

async function callWithFallback(messages: Message[]) {
  for (const model of modelChain) {
    try {
      return await openrouter.chat({ model, messages });
    } catch (error) {
      console.log(`${model} failed, trying next...`);
    }
  }
  throw new Error("All models failed");
}
```

### Cost Routing

```typescript
// Route based on query complexity
function selectModel(query: string): string {
  const complexity = analyzeComplexity(query);

  if (complexity === "simple") {
    // Simple queries → cheap model
    return "openai/gpt-4o-mini";  // ~$0.15/1M tokens
  } else if (complexity === "medium") {
    // Medium → balanced
    return "google/gemini-flash-1.5";  // ~$0.075/1M tokens
  } else {
    // Complex → best quality
    return "anthropic/claude-3-5-sonnet";  // ~$3/1M tokens
  }
}

function analyzeComplexity(query: string): "simple" | "medium" | "complex" {
  // Simple heuristics
  if (query.length < 50) return "simple";
  if (query.includes("explain") || query.includes("analyze")) return "complex";
  return "medium";
}
```

### A/B Testing

```typescript
// Random assignment
function getModel(userId: string): string {
  const hash = userId.charCodeAt(0) % 100;

  if (hash < 50) {
    return "anthropic/claude-3-5-sonnet";  // 50%
  } else {
    return "openai/gpt-4o";  // 50%
  }
}

// Track which model was used
const model = getModel(userId);
const response = await openrouter.chat({ model, messages });
await analytics.track("llm_call", { model, userId, latency, cost });
```

## LiteLLM (Self-Hosted)

### Why LiteLLM

- **Self-hosted**: Full control over data
- **100+ providers**: Same coverage as OpenRouter
- **Load balancing**: Distribute across providers
- **Cost tracking**: Built-in spend management
- **Caching**: Redis or in-memory
- **Rate limiting**: Per-user limits

### Setup

```bash
# Install
pip install litellm[proxy]

# Run proxy
litellm --config config.yaml

# Use as OpenAI-compatible endpoint
export OPENAI_API_BASE=http://localhost:4000
```

### Configuration

```yaml
# config.yaml
model_list:
  # Claude models
  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
      api_key: sk-ant-...

  # OpenAI models
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: sk-...

  # Load balanced (multiple providers)
  - model_name: balanced
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
    litellm_params:
      model: openai/gpt-4o
    # Requests distributed across both

# General settings
general_settings:
  master_key: sk-master-...
  database_url: postgresql://...

# Routing
router_settings:
  routing_strategy: simple-shuffle  # or latency-based-routing
  num_retries: 3
  timeout: 30

# Rate limiting
litellm_settings:
  max_budget: 100  # $100/month
  budget_duration: monthly
```

### Fallbacks in LiteLLM

```yaml
model_list:
  - model_name: primary
    litellm_params:
      model: anthropic/claude-3-5-sonnet-latest
    fallbacks:
      - model_name: fallback-1
        litellm_params:
          model: openai/gpt-4o
      - model_name: fallback-2
        litellm_params:
          model: google/gemini-pro
```

### Usage

```typescript
// Use like OpenAI SDK
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:4000",
  apiKey: "sk-master-...",
});

const response = await client.chat.completions.create({
  model: "claude-sonnet",  // Maps to configured model
  messages: [{ role: "user", content: "Hello!" }],
});
```

## Routing Strategies

### 1. Cost-Based Routing

```typescript
const costTiers = {
  cheap: ["openai/gpt-4o-mini", "google/gemini-flash-1.5"],
  balanced: ["anthropic/claude-3-5-haiku", "openai/gpt-4o"],
  premium: ["anthropic/claude-3-5-sonnet", "openai/o1-preview"],
};

function routeByCost(budget: "cheap" | "balanced" | "premium"): string {
  const models = costTiers[budget];
  return models[Math.floor(Math.random() * models.length)];
}
```

### 2. Latency-Based Routing

```typescript
// Track latency per model
const latencyStats: Record<string, number[]> = {};

function routeByLatency(): string {
  const avgLatencies = Object.entries(latencyStats)
    .map(([model, times]) => ({
      model,
      avg: times.reduce((a, b) => a + b, 0) / times.length,
    }))
    .sort((a, b) => a.avg - b.avg);

  return avgLatencies[0].model;
}

// Update after each call
function recordLatency(model: string, latencyMs: number) {
  if (!latencyStats[model]) latencyStats[model] = [];
  latencyStats[model].push(latencyMs);
  // Keep last 100 samples
  if (latencyStats[model].length > 100) {
    latencyStats[model].shift();
  }
}
```

### 3. Task-Based Routing

```typescript
const taskModels = {
  coding: "anthropic/claude-3-5-sonnet",  // Best for code
  reasoning: "openai/o1-preview",          // Best for logic
  creative: "anthropic/claude-3-5-sonnet", // Best for writing
  simple: "openai/gpt-4o-mini",            // Cheap and fast
  multimodal: "google/gemini-pro-1.5",     // Vision + text
};

function routeByTask(task: keyof typeof taskModels): string {
  return taskModels[task];
}
```

### 4. Hybrid Routing

```typescript
interface RoutingConfig {
  task: string;
  maxCost: number;
  maxLatency: number;
}

function hybridRoute(config: RoutingConfig): string {
  // Filter by cost
  const affordable = models.filter(m => m.cost <= config.maxCost);

  // Filter by latency
  const fast = affordable.filter(m => m.avgLatency <= config.maxLatency);

  // Select best for task
  const taskScores = fast.map(m => ({
    model: m.id,
    score: getTaskScore(m.id, config.task),
  }));

  return taskScores.sort((a, b) => b.score - a.score)[0].model;
}
```

## Best Practices

### 1. Always Have Fallbacks

```typescript
// Bad: Single point of failure
const response = await openai.chat({ model: "gpt-4o", messages });

// Good: Fallback chain
const models = ["gpt-4o", "claude-3-5-sonnet", "gemini-pro"];
for (const model of models) {
  try {
    return await gateway.chat({ model, messages });
  } catch (e) {
    continue;
  }
}
```

### 2. Pin Model Versions

```typescript
// Bad: Model can change
const model = "gpt-4";

// Good: Pinned version
const model = "openai/gpt-4-0125-preview";
```

### 3. Track Costs

```typescript
// Log every call
async function trackedCall(model: string, messages: Message[]) {
  const start = Date.now();
  const response = await gateway.chat({ model, messages });
  const latency = Date.now() - start;

  await analytics.track("llm_call", {
    model,
    inputTokens: response.usage.prompt_tokens,
    outputTokens: response.usage.completion_tokens,
    cost: calculateCost(model, response.usage),
    latency,
  });

  return response;
}
```

### 4. Set Token Limits

```typescript
// Prevent runaway costs
const response = await gateway.chat({
  model,
  messages,
  max_tokens: 500,  // Limit output length
});
```

### 5. Use Caching

```typescript
// LiteLLM caching
litellm_settings:
  cache: true
  cache_params:
    type: redis
    host: localhost
    port: 6379
    ttl: 3600  # 1 hour
```

## References

- `references/openrouter-guide.md` - OpenRouter deep dive
- `references/litellm-guide.md` - LiteLLM self-hosting
- `references/routing-strategies.md` - Advanced routing patterns
- `references/alternatives.md` - Helicone, Portkey, etc.

## Templates

- `templates/openrouter-config.ts` - TypeScript OpenRouter setup
- `templates/litellm-config.yaml` - LiteLLM proxy config
- `templates/fallback-chain.ts` - Fallback implementation
