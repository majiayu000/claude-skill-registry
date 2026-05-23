---
name: model-management
description: CLI commands to add, update, list, and deprecate AI models in the database. Triggers on "add model", "new model", "update model", "deprecate model", "model pricing", "model cli".
---

# Model Management CLI

Manage AI models directly in the database via CLI commands. No UI interaction required.

## Commands

### Add a new model

```bash
bun run model:add --json '{
  "modelId": "openai:gpt-6",
  "provider": "openai",
  "name": "GPT-6",
  "contextWindow": 200000,
  "inputCost": 2.5,
  "outputCost": 10,
  "capabilities": ["vision", "function-calling"],
  "status": "active",
  "userFriendlyDescription": "Next generation GPT with advanced capabilities",
  "bestFor": "Complex reasoning, research, advanced multimodal tasks",
  "knowledgeCutoff": "January 2026"
}'
```

### List models

```bash
# All models
bun run model:list

# Filter by provider
bun run model:list --provider openai
bun run model:list --provider anthropic

# Filter by status
bun run model:list --status active
bun run model:list --status deprecated
bun run model:list --status beta
```

### Get a single model

```bash
bun run model:get --id "openai:gpt-5"
```

### Update model

```bash
# Update pricing
bun run model:update --id "openai:gpt-5" --json '{"inputCost": 2.0, "outputCost": 8.0}'

# Update with reason
bun run model:update --id "openai:gpt-5" --json '{"inputCost": 2.0}' --reason "Price reduction announced"

# Update multiple fields
bun run model:update --id "openai:gpt-5" --json '{
  "inputCost": 2.0,
  "outputCost": 8.0,
  "contextWindow": 250000,
  "userFriendlyDescription": "Updated description"
}'
```

### Deprecate model

```bash
# Simple deprecation
bun run model:deprecate --id "openai:gpt-4"

# With reason
bun run model:deprecate --id "openai:gpt-4" --reason "Replaced by GPT-5"
```

## Required Fields (for add)

| Field | Type | Description |
|-------|------|-------------|
| `modelId` | string | Unique ID: "provider:model-name" |
| `provider` | string | openai, anthropic, google, xai, perplexity, groq, cerebras, minimax, deepseek, kimi, zai, meta, mistral, alibaba, zhipu |
| `name` | string | Display name |
| `contextWindow` | number | Max tokens |
| `inputCost` | number | Cost per 1M input tokens (USD) |
| `outputCost` | number | Cost per 1M output tokens (USD) |
| `capabilities` | array | vision, function-calling, thinking, extended-thinking, image-generation |
| `status` | string | active, deprecated, beta |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Internal description |
| `userFriendlyDescription` | string | User-facing description |
| `bestFor` | string | Use case recommendations |
| `knowledgeCutoff` | string | Knowledge cutoff date |
| `cachedInputCost` | number | Cost per 1M cached input tokens |
| `reasoningCost` | number | Cost per 1M reasoning tokens |
| `reasoningConfig` | string | JSON string for reasoning configuration |
| `gateway` | string | "vercel" or "openrouter" |
| `hostOrder` | array | Fallback hosts (e.g., ["cerebras", "groq"]) |
| `actualModelId` | string | Override for API calls |
| `speedTier` | string | "ultra-fast", "fast", "medium", "slow" |
| `isPro` | boolean | Requires tier access |
| `isInternalOnly` | boolean | Hidden from model picker |
| `isExperimental` | boolean | Preview/beta flag |
| `isLocal` | boolean | Ollama models |
| `benchmarks` | string | JSON string for benchmark scores |

## Full Example: Adding a New OpenAI Model

```bash
bun run model:add --json '{
  "modelId": "openai:gpt-6",
  "provider": "openai",
  "name": "GPT-6",
  "description": "Next generation flagship with advanced reasoning and multimodal capabilities",
  "contextWindow": 400000,
  "inputCost": 3.0,
  "outputCost": 12.0,
  "cachedInputCost": 0.3,
  "capabilities": ["thinking", "vision", "function-calling"],
  "status": "active",
  "reasoningConfig": "{\"type\":\"openai-reasoning-effort\",\"effortMapping\":{\"low\":\"low\",\"medium\":\"medium\",\"high\":\"high\"},\"summaryLevel\":\"detailed\",\"useResponsesAPI\":true}",
  "knowledgeCutoff": "January 2026",
  "userFriendlyDescription": "Most powerful GPT-6. Handles the most complex tasks with advanced reasoning, vision, and deep thinking.",
  "bestFor": "Complex reasoning, research, advanced multimodal tasks",
  "speedTier": "medium"
}'
```

## Full Example: Adding a Free OpenRouter Model

```bash
bun run model:add --json '{
  "modelId": "openrouter:new-free-model",
  "provider": "deepseek",
  "name": "New Free Model",
  "description": "Free model via OpenRouter",
  "contextWindow": 128000,
  "inputCost": 0,
  "outputCost": 0,
  "capabilities": ["thinking"],
  "status": "active",
  "gateway": "openrouter",
  "actualModelId": "deepseek/new-model:free",
  "reasoningConfig": "{\"type\":\"deepseek-tag-extraction\",\"tagName\":\"think\",\"applyMiddleware\":true}",
  "userFriendlyDescription": "Free reasoning model",
  "bestFor": "Complex reasoning, experimentation"
}'
```

## Reasoning Config Templates

### OpenAI (Reasoning Effort API)

```json
{
  "type": "openai-reasoning-effort",
  "effortMapping": { "low": "low", "medium": "medium", "high": "high" },
  "summaryLevel": "detailed",
  "useResponsesAPI": true
}
```

### Anthropic (Extended Thinking)

```json
{
  "type": "anthropic-extended-thinking",
  "budgetMapping": { "low": 5000, "medium": 15000, "high": 30000 },
  "betaHeader": "interleaved-thinking-2025-05-14"
}
```

### Google (Thinking Budget)

```json
{
  "type": "google-thinking-budget",
  "budgetMapping": { "low": 4096, "medium": 12288, "high": 24576 }
}
```

### DeepSeek (Tag Extraction)

```json
{
  "type": "deepseek-tag-extraction",
  "tagName": "think",
  "applyMiddleware": true
}
```

## Key Files

- `packages/backend/convex/models/cli.ts` - Internal mutations for CLI
- `scripts/model-cli.ts` - CLI wrapper script
- `packages/backend/convex/models/mutations.ts` - Admin UI mutations (auth required)
- `packages/backend/convex/schema/models.ts` - Database schema

## History Tracking

All changes are automatically tracked in `modelHistory` table:
- Version number increments on each change
- Change type: created, updated, deprecated, reactivated
- Field-level changes with old/new values
- Timestamp and reason

## Common Workflows

### New model announced

1. Check existing: `bun run model:list --provider openai`
2. Add model: `bun run model:add --json '{...}'`
3. Verify: `bun run model:get --id "openai:new-model"`

### Model pricing changed

1. Get current: `bun run model:get --id "openai:gpt-5"`
2. Update pricing: `bun run model:update --id "openai:gpt-5" --json '{"inputCost": 2.0}' --reason "Price reduction"`

### Model deprecated by provider

1. Deprecate: `bun run model:deprecate --id "openai:gpt-4" --reason "Replaced by GPT-5"`
2. Verify: `bun run model:list --status deprecated`
