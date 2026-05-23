---
name: auto-router-patterns
description: Auto router patterns for this project. Intelligent model selection via task classification, cost tier diversity, high-stakes override, weighted tier selection. Triggers on "auto router", "model selection", "classification", "cost tier", "exploration", "high stakes", "routing", "router".
---

# Auto Router Patterns

System intelligently routes user messages to optimal models via task classification, cost-based diversity, and high-stakes safety overrides.

## Classification with gpt-oss-120b

Router uses `gpt-oss-120b` via Cerebras for fast classification (~1000 tokens/sec):

```typescript
// From autoRouter.ts
function getRouterModel() {
  const openai = createOpenAI({
    apiKey: process.env.AI_GATEWAY_API_KEY,
    baseURL: "https://gateway.ai.cloudflare.com/v1/planetaryescape/blah-chat-dev-gateway/openai",
  });
  return openai("gpt-oss-120b"); // Via Cerebras
}

const ROUTER_MODEL_ID = "openai:gpt-oss-120b";
```

Classification schema with generateObject:

```typescript
// From autoRouter.ts
const classificationSchema = z.object({
  primaryCategory: z.enum(TASK_CATEGORIES),
  secondaryCategory: z.enum(TASK_CATEGORIES).optional().nullable(),
  complexity: z.enum(["simple", "moderate", "complex"]),
  requiresVision: z.boolean(),
  requiresLongContext: z.boolean(),
  requiresReasoning: z.boolean(),
  confidence: z.number().min(0).max(1),
  isHighStakes: z.boolean(),
  highStakesDomain: z.enum(HIGH_STAKES_DOMAINS).optional().nullable(),
});
```

Task categories: coding, reasoning, creative, factual, analysis, conversation, multimodal, research.

## Cost Tier Categorization

Models categorized by average pricing (input + output / 2):

```typescript
// From autoRouter.ts
type CostTier = "cheap" | "mid" | "premium";

function getCostTier(pricing: { input: number; output: number }): CostTier {
  const avgCost = (pricing.input + pricing.output) / 2;
  if (avgCost < 1.0) return "cheap";
  if (avgCost < 5.0) return "mid";
  return "premium";
}
```

Examples:
- Cheap: gpt-5-nano ($0.04/$0.16), gemini-2.0-flash ($0.1/$0.4)
- Mid: gpt-5-mini ($0.15/$0.6), claude-3.5-haiku ($0.8/$4.0)
- Premium: gpt-5 ($2.5/$10.0), claude-opus-4 ($15.0/$75.0)

## Weighted Tier Selection by Complexity

Diversity via weighted random selection, NOT top-N then random:

```typescript
// From autoRouter.ts
const TIER_WEIGHTS: Record<string, Record<CostTier, number>> = {
  simple: { cheap: 0.6, mid: 0.25, premium: 0.15 },
  moderate: { cheap: 0.5, mid: 0.3, premium: 0.2 },
  complex: { cheap: 0.3, mid: 0.4, premium: 0.3 },
};
```

Critical: Groups ALL models by tier, not just top N. Simple tasks get cheap models 60% of time, premium 15%.

Selection logic:

```typescript
// From autoRouter.ts
function selectWithExploration(
  scoredModels: Array<{ modelId: string; score: number }>,
  classification: { complexity: string; isHighStakes?: boolean },
) {
  // Group ALL models by tier
  const tiers: Record<CostTier, Array<{ modelId: string; score: number }>> = {
    cheap: [], mid: [], premium: [],
  };

  for (const model of sorted) {
    const tier = getCostTier(MODEL_CONFIG[model.modelId].pricing);
    tiers[tier].push(model);
  }

  // Get weights for complexity
  const weights = TIER_WEIGHTS[classification.complexity] ?? TIER_WEIGHTS.simple;
  const roll = Math.random();

  // Select tier based on weighted random
  if (roll < weights.cheap && tiers.cheap.length > 0) {
    selectedTier = "cheap";
  } else if (roll < weights.cheap + weights.mid && tiers.mid.length > 0) {
    selectedTier = "mid";
    explorationPick = true;
  } else if (tiers.premium.length > 0) {
    selectedTier = "premium";
    explorationPick = true;
  }

  // Random selection within chosen tier
  const pool = tiers[selectedTier];
  return pool[Math.floor(Math.random() * pool.length)];
}
```

## High-Stakes Override

Medical/legal/financial/safety questions force premium tier for accuracy:

```typescript
// From autoRouter.ts
const HIGH_STAKES_DOMAINS = [
  "medical", "legal", "financial", "safety",
  "mental_health", "privacy", "immigration", "domestic_abuse",
] as const;

// HIGH-STAKES OVERRIDE at top of selectWithExploration
if (classification.isHighStakes) {
  if (tiers.premium.length > 0) {
    const pool = tiers.premium;
    const picked = pool[Math.floor(Math.random() * pool.length)];
    return { ...picked, explorationPick: false };
  }
  // Fallback with warning if no premium models
  logger.warn("High-stakes query but no premium models available");
  return { ...sorted[0], explorationPick: false };
}
```

Classification prompt emphasizes advice vs information:

```typescript
// From routerPrompts.ts
RULES:
1. Must seek ADVICE or ACTION, not just information
2. "What is a heart attack?" = NOT high stakes (educational)
3. "Am I having a heart attack?" = HIGH STAKES (medical)
4. "What does liability mean?" = NOT high stakes (definition)
5. "Can my employer fire me for this?" = HIGH STAKES (legal)
```

## Diversity vs Top-Score Trade-off

System balances model quality with cost/speed diversity:

**Scoring phase** (autoRouter.ts):
- Base: category match score (0-100 from MODEL_PROFILES)
- Secondary category bonus: +30% of secondary score
- Complexity: simple tasks penalized 0.7x (prefer cheap), complex boosted 1.2x (prefer capable)
- Cost bias: `-(avgCost / 30) * (costBias / 100) * 20`
- Speed bias: `+speedBonus * (speedBias / 100)`
- Stickiness: +25 if model already selected in conversation
- Reasoning bonus: +15 if task requires thinking and model has it
- Research bonus: +25 for Perplexity models on research tasks

**Selection phase** (selectWithExploration):
- NOT greedy (always top score)
- NOT pure random (chaos)
- Weighted probabilistic by cost tier AND complexity
- Ensures variety across conversations without sacrificing appropriateness

## Excluded Models Tracking for Retries

Failed models excluded from retry attempts:

```typescript
// From autoRouter.ts routeMessage args
export const routeMessage = internalAction({
  args: {
    // ...
    excludedModels: v.optional(v.array(v.string())), // Failed models
  },
  handler: async (ctx, args) => {
    // Filter eligible models
    const eligibleModels = getEligibleModels(
      classification,
      args.currentContextTokens ?? 0,
      args.excludedModels, // ← Passed to filter
    );

    // Check if all models exhausted
    if (eligibleModels.length === 0) {
      const fallbackModel = "openai:gpt-5-mini";
      if (args.excludedModels?.includes(fallbackModel)) {
        throw new Error("All models exhausted including fallback");
      }
      return { selectedModelId: fallbackModel, /* ... */ };
    }
  },
});

function getEligibleModels(
  classification: TaskClassification,
  currentContextTokens: number,
  excludedModels?: string[],
): string[] {
  return Object.keys(MODEL_CONFIG).filter((modelId) => {
    // Exclude failed models from retry attempts
    if (excludedModels?.includes(modelId)) return false;
    // ... other filters
  });
}
```

Caller (chat.ts or generation retry logic) tracks failed models and passes them to router.

## Key Files

- `packages/backend/convex/ai/autoRouter.ts` - Main routing action, classification, selection
- `packages/backend/convex/ai/modelProfiles.ts` - MODEL_CONFIG, MODEL_PROFILES, category scores
- `packages/backend/convex/ai/routerPrompts.ts` - Classification prompt, reasoning template
- `packages/backend/convex/chat.ts` - Calls routeMessage when user has "auto" selected
- `packages/backend/convex/generation.ts` - Retry logic with excludedModels

## Avoid

- Don't use top-N greedy selection - breaks diversity
- Don't skip high-stakes override - safety critical
- Don't hardcode tier weights - use complexity-based config
- Don't forget to track router usage for cost monitoring (recordTextGeneration)
- Don't use classification model for generation - gpt-oss-120b is internal-only
