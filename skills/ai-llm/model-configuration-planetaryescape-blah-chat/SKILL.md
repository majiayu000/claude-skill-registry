---
name: model-configuration
description: AI model configuration patterns for this project. Single source of truth for model definitions. Triggers on "MODEL_CONFIG", "model", "pricing", "capabilities", "auto router", "gateway".
---

# Model Configuration

Single source of truth for AI model definitions. **Never hardcode model IDs as strings**.

## Critical Anti-Pattern

```typescript
// ❌ NEVER DO THIS
const response = await generateText({
  model: "gpt-4",  // Hardcoded string
  ...
});

// ✅ ALWAYS DO THIS
import { MODEL_CONFIG } from "@/lib/ai/models";
const response = await generateText({
  model: getModel(MODEL_CONFIG["openai:gpt-5.1"].id),
  ...
});
```

## MODEL_CONFIG Structure

Every model has standardized config:

```typescript
// From apps/web/src/lib/ai/models.ts
"openai:gpt-5.1": {
  id: "openai:gpt-5.1",              // Full model identifier
  provider: "openai",                 // Creator/vendor
  name: "GPT-5.1",                    // Display name
  description: "Latest flagship...",  // Technical description
  contextWindow: 256000,              // Max tokens
  pricing: {
    input: 1.25,                      // $/MTok input
    output: 10.0,                     // $/MTok output
    cached: 0.125,                    // $/MTok cached (optional)
    reasoning: 3.5,                   // $/MTok reasoning output (optional)
  },
  capabilities: [
    "thinking",                       // Extended reasoning
    "vision",                         // Image understanding
    "function-calling"                // Tool use
  ],
  knowledgeCutoff: "November 2025",
  userFriendlyDescription: "...",     // Plain-language for users
  bestFor: "...",                     // Use case guidance
}
```

## AUTO_MODEL Pattern

Special "auto" model for intelligent routing:

```typescript
// From apps/web/src/lib/ai/models.ts
export const AUTO_MODEL = {
  id: "auto",
  provider: "auto" as const,
  name: "Auto",
  description: "Intelligently routes to optimal model based on your task",
  contextWindow: 0,                   // N/A - depends on selected model
  pricing: { input: 0, output: 0 },  // Variable - depends on selected model
  capabilities: [],
  userFriendlyDescription:
    "Let blah.chat pick the best model for each message. Analyzes your task and routes to the optimal model.",
  bestFor:
    "When you want the best model for each task without manual selection",
};

export const isAutoModel = (modelId: string): boolean => modelId === "auto";
```

AUTO_MODEL is in MODEL_CONFIG as `auto` key. Check with `isAutoModel()`.

## Pricing Configuration

Four pricing types:

```typescript
pricing: {
  input: 1.25,      // Standard input tokens
  output: 10.0,     // Standard output tokens
  cached: 0.125,    // Cached input (prompt caching) - optional
  reasoning: 3.5,   // Reasoning output (thinking tokens) - optional
}
```

Example from Gemini 2.5 Flash:
```typescript
// From apps/web/src/lib/ai/models.ts
"google:gemini-2.5-flash": {
  pricing: {
    input: 0.15,
    output: 0.6,
    cached: 0.019,
    reasoning: 3.5,  // Thinking output 6x higher!
  },
}
```

Free models (OpenRouter):
```typescript
"openrouter:deepseek-r1-0528": {
  pricing: { input: 0, output: 0 },
  gateway: "openrouter",
}
```

## Capabilities Flags

```typescript
capabilities: [
  "vision",              // Image understanding
  "thinking",            // Extended reasoning (DeepSeek, Gemini, OpenAI)
  "extended-thinking",   // Anthropic's version with budget control
  "function-calling",    // Tool/function execution
  "image-generation",    // Generate images (Gemini 3 Pro Image)
]
```

Check capabilities:
```typescript
const model = MODEL_CONFIG["openai:gpt-5.1"];
if (model.capabilities.includes("vision")) {
  // Can handle images
}
```

## Gateway Configuration

Three gateway types:

1. **Vercel AI Gateway** (default) - aggregates all providers
2. **OpenRouter** - free models, community hosting
3. **Direct SDK** - OpenAI, Anthropic, Google direct

```typescript
// Default: Vercel AI Gateway (no gateway field)
"openai:gpt-5.1": {
  // gateway: "vercel" is implicit
}

// OpenRouter for free models
"openrouter:deepseek-r1-0528": {
  gateway: "openrouter",
  actualModelId: "deepseek/deepseek-r1-0528:free",  // OpenRouter format
}

// xAI models - different naming
"xai:grok-4-fast": {
  actualModelId: "grok-4-fast-non-reasoning",  // Vercel gateway uses different ID
}
```

Use `getModel()` to instantiate:

```typescript
// From apps/web/src/lib/ai/registry.ts
import { getModel } from "@/lib/ai/registry";

const model = getModel("openai:gpt-5.1");  // Auto-selects gateway
const model = getModel("openrouter:deepseek-r1-0528");  // Uses OpenRouter
```

## Host Order Fallbacks

Vercel AI Gateway supports fallback inference hosts (Cerebras, Groq, etc.):

```typescript
// From apps/web/src/lib/ai/models.ts
"openai:gpt-oss-20b": {
  hostOrder: ["cerebras", "groq"],  // Try Cerebras first, fallback to Groq
}

"meta:llama-3.3-70b": {
  hostOrder: ["cerebras", "groq"],
}

"deepseek:deepseek-r1": {
  hostOrder: ["cerebras", "groq"],
}
```

Only applies to Vercel AI Gateway. Ignored for direct SDKs.

## Reasoning Config

Different providers have different reasoning APIs:

```typescript
// OpenAI - Reasoning Effort API
reasoning: {
  type: "openai-reasoning-effort",
  effortMapping: { low: "low", medium: "medium", high: "high" },
  summaryLevel: "detailed",
  useResponsesAPI: true,
}

// Anthropic - Extended Thinking with Token Budget
reasoning: {
  type: "anthropic-extended-thinking",
  budgetMapping: { low: 5000, medium: 15000, high: 30000 },
  betaHeader: "interleaved-thinking-2025-05-14",
}

// Google - Thinking Budget
reasoning: {
  type: "google-thinking-budget",
  budgetMapping: { low: 4096, medium: 12288, high: 24576 },
}

// DeepSeek - Tag Extraction (<think> tags)
reasoning: {
  type: "deepseek-tag-extraction",
  tagName: "think",
  applyMiddleware: true,
}
```

## Pro Model Tier System

```typescript
// From apps/web/src/lib/ai/models.ts - Future feature
isPro: true,  // Requires tier access (not yet implemented)
```

Check tier with utility:

```typescript
// From packages/ai/src/models.ts
export function getModelTier(model: ModelConfig): ModelTier {
  if (model.pricing.input === 0 && model.pricing.output === 0) {
    return "free";
  }
  if (
    model.capabilities.includes("thinking") ||
    model.capabilities.includes("extended-thinking")
  ) {
    return "reasoning";
  }
  if (model.pricing.input < 0.5) {
    return "fast";
  }
  return "flagship";
}
```

## Internal-Only Models

Hide from UI but keep in config:

```typescript
"meta:llama-3.3-70b": {
  isInternalOnly: true,  // Not shown in model picker
}

"alibaba:qwen3-coder-480b": {
  isInternalOnly: true,
}
```

Filter for UI:

```typescript
// From packages/ai/src/models.ts
export function getMobileModels(): ModelConfig[] {
  return Object.values(MODEL_CONFIG).filter(
    (model) => !model.isInternalOnly && !model.isExperimental,
  );
}
```

## Experimental Models

```typescript
"google:gemini-3-pro-preview": {
  isExperimental: true,  // Mark as preview/beta
}

"google:gemini-2.5-flash-image": {
  isExperimental: true,
}
```

## Key Files

- `apps/web/src/lib/ai/models.ts` - Web-specific config + AUTO_MODEL
- `packages/ai/src/models.ts` - Shared config (source of truth for mobile)
- `apps/web/src/lib/ai/registry.ts` - Gateway instantiation via `getModel()`
- `apps/web/src/lib/ai/providers.ts` - Gateway client initialization

## Common Operations

### Adding a new model

```typescript
// In apps/web/src/lib/ai/models.ts or packages/ai/src/models.ts
export const MODEL_CONFIG: Record<string, ModelConfig> = {
  "provider:model-name": {
    id: "provider:model-name",
    provider: "provider",
    name: "Display Name",
    description: "Technical description",
    contextWindow: 128000,
    pricing: { input: 0.5, output: 2.0 },
    capabilities: ["function-calling"],
    knowledgeCutoff: "January 2025",
    userFriendlyDescription: "Plain-language description",
    bestFor: "Use case guidance",
  },
};
```

### Using a model

```typescript
import { MODEL_CONFIG } from "@/lib/ai/models";
import { getModel } from "@/lib/ai/registry";

const modelId = MODEL_CONFIG["openai:gpt-5.1"].id;
const model = getModel(modelId);

const result = await generateText({
  model,
  messages,
});
```

### Checking capabilities

```typescript
const model = MODEL_CONFIG["google:gemini-2.5-flash"];
const hasVision = model.capabilities.includes("vision");
const hasThinking = model.capabilities.includes("thinking");
const costPerMillion = model.pricing.input;
```

### Gateway override

```typescript
import { getModelWithGateway } from "@/lib/ai/registry";

// Force OpenRouter even if model config says Vercel
const model = getModelWithGateway("openai:gpt-5.1", "openrouter");
```

## Avoid

- **Never hardcode model IDs** - always import from MODEL_CONFIG
- **Never create duplicate configs** - shared config is in `packages/ai/src/models.ts`
- **Never skip pricing** - always include `input` and `output`, optional `cached` and `reasoning`
- **Never modify directly in generation code** - update MODEL_CONFIG, not ad-hoc overrides
- **Never assume capabilities** - check `capabilities` array before using features
- **Never use old model IDs** - check current MODEL_CONFIG for updated names (e.g., `gpt-4` → `openai:gpt-5.1`)
