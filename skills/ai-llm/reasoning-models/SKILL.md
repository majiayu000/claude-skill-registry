---
name: reasoning-models
description: Multi-provider reasoning/thinking configuration. Discriminated unions for OpenAI effort, Anthropic budget, Google level/budget, DeepSeek middleware. Triggers on "reasoning", "thinking", "o1", "deepseek", "extended-thinking", "thinkingEffort", "reasoningEffort".
---

# Reasoning Models

Multi-provider reasoning system with discriminated union configs. Each provider has different API: OpenAI effort levels, Anthropic token budgets, Google level/budget, DeepSeek tag extraction. Registry pattern for handlers.

## Discriminated Union Types

One type per provider - TypeScript enforces which fields are valid:

```typescript
// From apps/web/src/lib/ai/reasoning/types.ts
export type ReasoningConfig =
  | {
      type: "openai-reasoning-effort";
      effortMapping: Record<ActiveThinkingEffort, string>;
      summaryLevel?: "brief" | "detailed";
      useResponsesAPI: boolean;
    }
  | {
      type: "anthropic-extended-thinking";
      budgetMapping: Record<ActiveThinkingEffort, number>; // Token budgets
      betaHeader: string; // e.g., "interleaved-thinking-2025-05-14"
    }
  | {
      type: "google-thinking-level"; // Gemini 3 family
      levelMapping: Record<ActiveThinkingEffort, "low" | "medium" | "high">;
      includeThoughts: boolean;
    }
  | {
      type: "google-thinking-budget"; // Gemini 2.5
      budgetMapping: Record<ActiveThinkingEffort, number>;
    }
  | {
      type: "deepseek-tag-extraction";
      tagName: string; // e.g., "think"
      applyMiddleware: true;
    }
  | {
      type: "generic-reasoning-effort"; // xAI, Perplexity, Groq
      parameterName: string; // e.g., "reasoningEffort"
    };
```

## Effort Levels

Thinking effort controls reasoning intensity:

```typescript
// "none" = disable reasoning entirely (model runs without thinking)
export type ThinkingEffort = "none" | "low" | "medium" | "high";

// Active effort levels (excludes "none" - used in mappings)
// "none" short-circuits in builder before reaching handlers
export type ActiveThinkingEffort = Exclude<ThinkingEffort, "none">;
```

**Type Guard** (avoid truthy string bugs - "none" is truthy but means disabled):

```typescript
export function isActiveThinkingEffort(
  effort: ThinkingEffort | undefined,
): effort is ActiveThinkingEffort {
  return effort !== undefined && effort !== "none";
}
```

## Model Config Integration

Add reasoning config to model definitions:

```typescript
// From apps/web/src/lib/ai/models.ts

// OpenAI GPT-5 - effort mapping
"openai:gpt-5": {
  id: "openai:gpt-5",
  provider: "openai",
  capabilities: ["thinking", "vision", "function-calling"],
  reasoning: {
    type: "openai-reasoning-effort",
    effortMapping: { low: "low", medium: "medium", high: "high" },
    summaryLevel: "detailed",
    useResponsesAPI: true,
  },
}

// Anthropic Claude - token budget
"anthropic:claude-opus-4.5": {
  id: "anthropic:claude-opus-4.5",
  provider: "anthropic",
  capabilities: ["extended-thinking"],
  reasoning: {
    type: "anthropic-extended-thinking",
    budgetMapping: { low: 5000, medium: 15000, high: 30000 },
    betaHeader: "interleaved-thinking-2025-05-14",
  },
}

// Google Gemini 2.5 - thinking budget
"google:gemini-2.5-flash": {
  id: "google:gemini-2.5-flash",
  provider: "google",
  capabilities: ["thinking"],
  reasoning: {
    type: "google-thinking-budget",
    budgetMapping: { low: 4096, medium: 12288, high: 24576 },
  },
}

// Google Gemini 3 - thinking level
"google:gemini-3-pro": {
  id: "google:gemini-3-pro",
  provider: "google",
  reasoning: {
    type: "google-thinking-level",
    levelMapping: { low: "low", medium: "medium", high: "high" },
    includeThoughts: true,
  },
}

// DeepSeek - tag extraction middleware
"deepseek:deepseek-r1": {
  id: "deepseek:deepseek-r1",
  provider: "deepseek",
  reasoning: {
    type: "deepseek-tag-extraction",
    tagName: "think",
    applyMiddleware: true,
  },
}
```

## buildReasoningOptions

Main entry point - converts model config + effort to provider options:

```typescript
// From apps/web/src/lib/ai/reasoning/builder.ts
import { buildReasoningOptions } from "@/lib/ai/reasoning/builder";

const result = buildReasoningOptions(modelConfig, effortLevel);

// Returns ReasoningResult or null
// null = graceful degradation (no reasoning config or effort="none")
export interface ReasoningResult {
  providerOptions?: any;
  headers?: Record<string, string>;
  useResponsesAPI?: boolean;
  applyMiddleware?: (model: any) => any;
}
```

**Implementation**:

```typescript
export function buildReasoningOptions(
  modelConfig: ModelConfig,
  effortLevel: ThinkingEffort,
): ReasoningResult | null {
  // "none" effort = skip reasoning entirely
  if (effortLevel === "none") return null;

  // No reasoning config? Graceful degradation
  if (!modelConfig.reasoning) return null;

  // Lookup handler from registry
  const handler = REASONING_HANDLERS[modelConfig.reasoning.type];
  if (!handler) {
    console.warn(`No handler for type: ${modelConfig.reasoning.type}`);
    return null;
  }

  // Call handler with config + effort
  try {
    return handler(modelConfig.reasoning, effortLevel as ActiveThinkingEffort);
  } catch (error) {
    console.error("[Reasoning] Handler failed:", error);
    return null;
  }
}
```

## Handler Registry Pattern

Map config type → handler (NO if-blocks, TypeScript enforces completeness):

```typescript
// From apps/web/src/lib/ai/reasoning/registry.ts
export const REASONING_HANDLERS: Record<
  ReasoningConfig["type"],
  ReasoningHandler
> = {
  "openai-reasoning-effort": buildOpenAIReasoning,
  "anthropic-extended-thinking": buildAnthropicReasoning,
  "google-thinking-level": buildGoogleReasoning,
  "google-thinking-budget": buildGoogleReasoning, // Same handler
  "deepseek-tag-extraction": buildDeepSeekReasoning,
  "generic-reasoning-effort": buildGenericReasoning,
};

// Handler signature
export type ReasoningHandler = (
  config: ReasoningConfig,
  effort: ActiveThinkingEffort,
) => {
  providerOptions?: ProviderOptions;
  headers?: Record<string, string>;
  useResponsesAPI?: boolean;
  applyMiddleware?: (model: any) => any;
};
```

## Provider-Specific Handlers

### OpenAI - Reasoning Effort

```typescript
// From apps/web/src/lib/ai/reasoning/handlers/openai.ts
export function buildOpenAIReasoning(
  config: ReasoningConfig,
  effort: ActiveThinkingEffort,
): ReasoningResult {
  if (config.type !== "openai-reasoning-effort") {
    throw new Error(`Invalid config type: ${config.type}`);
  }

  const mappedEffort = config.effortMapping[effort];

  return {
    providerOptions: {
      openai: {
        reasoningEffort: mappedEffort,
        reasoningSummary: config.summaryLevel || "detailed",
      },
    },
    useResponsesAPI: config.useResponsesAPI,
  };
}
```

### Anthropic - Extended Thinking Budget

```typescript
// From apps/web/src/lib/ai/reasoning/handlers/anthropic.ts
export function buildAnthropicReasoning(
  config: ReasoningConfig,
  effort: ActiveThinkingEffort,
): ReasoningResult {
  if (config.type !== "anthropic-extended-thinking") {
    throw new Error(`Invalid config type: ${config.type}`);
  }

  const budgetTokens = config.budgetMapping[effort];

  return {
    providerOptions: {
      anthropic: {
        thinking: {
          type: "enabled",
          budgetTokens,
        },
      },
    },
    headers: {
      "anthropic-beta": config.betaHeader,
    },
  };
}
```

### Google - Thinking Level/Budget

Google has TWO config types - same handler handles both:

```typescript
// From apps/web/src/lib/ai/reasoning/handlers/google.ts
export function buildGoogleReasoning(
  config: ReasoningConfig,
  effort: ActiveThinkingEffort,
): ReasoningResult {
  // Gemini 2.5 uses thinking budgets
  if (config.type === "google-thinking-budget") {
    const budget = config.budgetMapping[effort];
    return {
      providerOptions: {
        google: {
          thinkingConfig: {
            thinkingBudget: budget,
          },
        },
      },
    };
  }

  // Gemini 3 family uses thinking levels (low/medium/high)
  if (config.type === "google-thinking-level") {
    const level = config.levelMapping[effort];
    return {
      providerOptions: {
        google: {
          thinkingConfig: {
            thinkingLevel: level,
            includeThoughts: config.includeThoughts,
          },
        },
      },
    };
  }

  throw new Error(`Invalid config type: ${config.type}`);
}
```

### DeepSeek - Tag Extraction Middleware

Uses Vercel AI SDK middleware to extract `<think>` tags:

```typescript
// From apps/web/src/lib/ai/reasoning/handlers/deepseek.ts
import { extractReasoningMiddleware, wrapLanguageModel } from "ai";

export function buildDeepSeekReasoning(
  config: ReasoningConfig,
  _effort: ActiveThinkingEffort, // Not used (tag extraction always enabled)
): ReasoningResult {
  if (config.type !== "deepseek-tag-extraction") {
    throw new Error(`Invalid config type: ${config.type}`);
  }

  return {
    applyMiddleware: (model) =>
      wrapLanguageModel({
        model,
        middleware: extractReasoningMiddleware({ tagName: config.tagName }),
      }),
  };
}
```

### Generic - Simple Effort Parameter

For providers with simple effort parameters (xAI, Perplexity, Groq):

```typescript
// From apps/web/src/lib/ai/reasoning/registry.ts
function buildGenericReasoning(
  config: ReasoningConfig,
  effort: ActiveThinkingEffort,
) {
  if (config.type !== "generic-reasoning-effort") {
    throw new Error(`Invalid config type: ${config.type}`);
  }

  return {
    providerOptions: {
      [config.parameterName]: effort, // Dynamic parameter name
    },
  };
}
```

## Provider Options Output

Type-safe output for API request construction:

```typescript
// From apps/web/src/lib/ai/reasoning/types.ts
export type ProviderOptions = {
  openai?: {
    reasoningEffort?: string;
    reasoningSummary?: "brief" | "detailed";
  };
  anthropic?: {
    thinking?: {
      type: "enabled";
      budgetTokens: number;
    };
  };
  google?: {
    thinkingConfig?: {
      thinkingLevel?: "low" | "medium" | "high";
      thinkingBudget?: number;
      includeThoughts?: boolean;
    };
  };
  xai?: {
    reasoningEffort?: string;
  };
  perplexity?: {
    reasoningMode?: string;
  };
  groq?: {
    reasoningLevel?: string;
  };
};
```

## Key Files

- `apps/web/src/lib/ai/reasoning/types.ts` - Discriminated union types, type guards
- `apps/web/src/lib/ai/reasoning/builder.ts` - buildReasoningOptions entry point
- `apps/web/src/lib/ai/reasoning/registry.ts` - Handler registry + generic handler
- `apps/web/src/lib/ai/reasoning/handlers/openai.ts` - OpenAI effort mapping
- `apps/web/src/lib/ai/reasoning/handlers/anthropic.ts` - Anthropic budget + beta header
- `apps/web/src/lib/ai/reasoning/handlers/google.ts` - Google level/budget (two types)
- `apps/web/src/lib/ai/reasoning/handlers/deepseek.ts` - DeepSeek middleware
- `apps/web/src/lib/ai/models.ts` - Model configs with reasoning field

## Avoid

- Don't check `if (effort)` - use `isActiveThinkingEffort()` (avoids "none" being truthy)
- Don't hardcode provider options - use handlers
- Don't add if-blocks for config types - add to registry instead
- Don't skip type guards in handlers - always validate config.type
- Don't forget graceful degradation - return null if no config
