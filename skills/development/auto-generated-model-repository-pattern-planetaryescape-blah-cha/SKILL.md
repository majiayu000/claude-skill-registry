---
name: auto-generated-model-repository-pattern
description: Database-backed model configuration with static fallback for this project. Hook-based reactive queries (useModels, useModel), static sync helpers, AUTO_MODEL injection, type depth workarounds. Triggers on "useModels", "useModel", "model repository", "database models", "model queries", "model picker", "model config".
---

# Model Repository Pattern

This project migrated from static MODEL_CONFIG to database-backed model storage. Models live in Convex DB, accessed via hooks on client, static helpers on server.

## Core Pattern

**Client-side (reactive)**: Use hooks that return `undefined` while loading
**Server-side (sync)**: Use static helpers from MODEL_CONFIG fallback
**AUTO_MODEL**: Always injected separately (not in database)

## Hook Usage (Client)

All hooks return `undefined` during loading. Never return empty object.

```typescript
// From apps/web/src/lib/models/repository.ts
import { useModels, useModel } from "@/lib/models/repository";

// Get all models
const models = useModels({
  includeDeprecated: false,
  includeInternalOnly: false
});

if (models === undefined) {
  return <Loading />;
}

// Models loaded - use Record<string, ModelConfig>
const modelIds = Object.keys(models); // includes "auto"
```

### Single Model Hook

```typescript
const model = useModel("openai:gpt-5");

if (model === undefined) {
  return <Loading />; // Either loading or not found
}

// Model loaded
console.log(model.name); // "GPT-5"
```

### AUTO_MODEL Handling

AUTO_MODEL is injected client-side, not stored in database:

```typescript
// From repository.ts lines 65-68
const configs = dbModelsToConfigRecord(dbModels);
configs.auto = AUTO_MODEL; // Always inject

return configs;
```

AUTO_MODEL definition from `apps/web/src/lib/ai/models.ts`:

```typescript
export const AUTO_MODEL = {
  id: "auto",
  provider: "auto" as const,
  name: "Auto",
  description: "Intelligently routes to optimal model based on your task",
  contextWindow: 0,
  pricing: { input: 0, output: 0 },
  capabilities: [],
  userFriendlyDescription:
    "Let blah.chat pick the best model for each message...",
  bestFor: "When you want the best model for each task...",
};
```

Hook checks for "auto" before querying DB:

```typescript
// From repository.ts lines 81-83
if (modelId === "auto") {
  return AUTO_MODEL;
}
```

## Static Helpers (Server)

For server code (API routes, Convex actions), use synchronous helpers:

```typescript
import { getStaticModels, getStaticModel } from "@/lib/models/repository";

// Get all static models
const models = getStaticModels({ includeDeprecated: false });
// Returns immediately from MODEL_CONFIG

// Get single model
const model = getStaticModel("openai:gpt-5");
if (!model) {
  throw new Error("Model not found");
}
```

Static helpers use MODEL_CONFIG from `apps/web/src/lib/ai/models.ts` as fallback.

## Type Depth Workaround

With 94+ Convex modules, TypeScript hits recursion limits on `api.*` imports. Use lazy loading:

```typescript
// From repository.ts lines 17-32
const typedQuery = useQuery as any;

let _modelsApi: any = null;
function getModelsApi() {
  if (!_modelsApi) {
    // Dynamic require avoids type inference at import time
    const { api } = require("@blah-chat/backend/convex/_generated/api");
    _modelsApi = api.models;
  }
  return _modelsApi;
}

// Usage in hook:
const dbModels = typedQuery(getModelsApi().queries.list, {
  includeDeprecated: options?.includeDeprecated,
  includeInternalOnly: options?.includeInternalOnly,
}) as Doc<"models">[] | undefined;
```

**Key points**:
- Cast `useQuery` to `any` (line 19)
- Lazy-load `api` via `require()` to defer type resolution
- Manually type-assert return value
- Avoids "Type instantiation excessively deep" error

## Database Queries (Backend)

Located in `packages/backend/convex/models/queries.ts`:

```typescript
// Get model by ID
export const getById = query({
  args: { modelId: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("models")
      .withIndex("by_modelId", (q) => q.eq("modelId", args.modelId))
      .first();
  },
});

// Get all active models
export const list = query({
  args: {
    includeDeprecated: v.optional(v.boolean()),
    includeInternalOnly: v.optional(v.boolean()),
  },
  handler: async (ctx, args) => {
    let models = await ctx.db
      .query("models")
      .withIndex("by_status", (q) => q.eq("status", "active"))
      .collect();

    if (args.includeDeprecated) {
      // Fetch deprecated + beta
    }

    if (!args.includeInternalOnly) {
      models = models.filter((m) => !m.isInternalOnly);
    }

    return models;
  },
});
```

Admin-only queries check authorization:

```typescript
// From queries.ts lines 121-130
export const listAll = query({
  args: {},
  handler: async (ctx) => {
    const user = await getCurrentUser(ctx);
    if (!user || user.isAdmin !== true) {
      throw new Error("Unauthorized: Admin access required");
    }
    return await ctx.db.query("models").collect();
  },
});
```

## Transforms (DB ↔ ModelConfig)

Located in `apps/web/src/lib/models/transforms.ts`:

```typescript
// DB model to ModelConfig
export function dbToModelConfig(dbModel: Doc<"models">): ModelConfig {
  return {
    id: dbModel.modelId,
    provider: dbModel.provider as ModelConfig["provider"],
    name: dbModel.name,
    description: dbModel.description,
    contextWindow: dbModel.contextWindow,
    pricing: {
      input: dbModel.inputCost,
      output: dbModel.outputCost,
      cached: dbModel.cachedInputCost,
      reasoning: dbModel.reasoningCost,
    },
    capabilities: dbModel.capabilities as ModelConfig["capabilities"],
    // ... other fields
    reasoning: safeJsonParse<ReasoningConfig>(dbModel.reasoningConfig),
    benchmarks: safeJsonParse(dbModel.benchmarks),
    // ...
  };
}
```

Safe JSON parsing for complex fields:

```typescript
// From transforms.ts lines 16-24
function safeJsonParse<T>(json: string | undefined): T | undefined {
  if (!json) return undefined;
  try {
    return JSON.parse(json) as T;
  } catch {
    console.error("Failed to parse JSON:", json.slice(0, 100));
    return undefined;
  }
}
```

## Schema (Database)

Located in `packages/backend/convex/schema/models.ts`:

```typescript
export const modelsTable = defineTable({
  // Identity
  modelId: v.string(), // "openai:gpt-5"
  provider: providerValidator,
  name: v.string(),
  description: v.optional(v.string()),

  // Context
  contextWindow: v.number(),
  actualModelId: v.optional(v.string()),
  isLocal: v.optional(v.boolean()),

  // Pricing (per 1M tokens, USD)
  inputCost: v.number(),
  outputCost: v.number(),
  cachedInputCost: v.optional(v.number()),
  reasoningCost: v.optional(v.number()),

  // Capabilities
  capabilities: v.array(capabilityValidator),

  // Complex fields as JSON strings
  reasoningConfig: v.optional(v.string()),
  benchmarks: v.optional(v.string()),

  // Status
  status: statusValidator, // "active" | "deprecated" | "beta"

  // Access control
  isPro: v.optional(v.boolean()),
  isInternalOnly: v.optional(v.boolean()),
  isExperimental: v.optional(v.boolean()),

  // Audit
  createdAt: v.number(),
  updatedAt: v.number(),
  createdBy: v.optional(v.id("users")),
  updatedBy: v.optional(v.id("users")),
})
  .index("by_modelId", ["modelId"])
  .index("by_provider", ["provider"])
  .index("by_status", ["status"])
  .searchIndex("search_models", { searchField: "name" });
```

## Filter Options

Both hooks and queries support filtering:

```typescript
// Include deprecated models
const allModels = useModels({ includeDeprecated: true });

// Include internal-only models (admin)
const adminModels = useModels({ includeInternalOnly: true });

// Both
const everything = useModels({
  includeDeprecated: true,
  includeInternalOnly: true,
});
```

Backend filtering logic:

```typescript
// From queries.ts lines 40-70
let models = await ctx.db
  .query("models")
  .withIndex("by_status", (q) => q.eq("status", "active"))
  .collect();

if (args.includeDeprecated) {
  const deprecated = await ctx.db
    .query("models")
    .withIndex("by_status", (q) => q.eq("status", "deprecated"))
    .collect();
  const beta = await ctx.db
    .query("models")
    .withIndex("by_status", (q) => q.eq("status", "beta"))
    .collect();
  models = [...models, ...deprecated, ...beta];
}

if (!args.includeInternalOnly) {
  models = models.filter((m) => !m.isInternalOnly);
}
```

## Loading States

**Critical**: Never check `if (!models)` - use strict `=== undefined`:

```typescript
// ❌ Wrong - treats empty object as falsy
if (!models) {
  return <Loading />;
}

// ✅ Correct - distinguishes undefined from empty
if (models === undefined) {
  return <Loading />;
}

// After loaded, models can be empty Record
const modelCount = Object.keys(models).length; // 0 or more
```

## Additional Hooks

```typescript
// Model profiles for auto-router
const profiles = useModelProfiles();
// Returns Doc<"modelProfiles">[] | undefined

// Auto-router config
const routerConfig = useRouterConfig();
// Returns Doc<"autoRouterConfig"> | null | undefined

// Model history (admin)
const history = useModelHistory("openai:gpt-5", 50);
// Returns Doc<"modelHistory">[] | undefined

// Model stats (admin)
const stats = useModelStats();
// Returns { total, byStatus, byProvider } | undefined

// All models including internal (admin)
const allModels = useAllModels();
// Returns Doc<"models">[] | undefined
```

## Key Files

- `apps/web/src/lib/models/repository.ts` - Hooks + static helpers
- `apps/web/src/lib/models/transforms.ts` - DB ↔ ModelConfig transforms
- `packages/backend/convex/models/queries.ts` - Database queries
- `packages/backend/convex/schema/models.ts` - Schema definitions
- `apps/web/src/lib/ai/models.ts` - MODEL_CONFIG, AUTO_MODEL, ModelConfig interface

## Anti-Patterns

**Don't**:
- Import `api.models` at module top level (type depth errors)
- Check `if (!models)` for loading (use `=== undefined`)
- Store AUTO_MODEL in database (inject client-side)
- Use hooks in server code (use static helpers)
- Assume empty models means loading (could be legit empty)

**Do**:
- Lazy-load `api` via `require()` in getter function
- Type-assert hook return values manually
- Inject AUTO_MODEL after transforming DB models
- Handle `undefined` explicitly in loading checks
- Use `includeInternalOnly: true` for admin views
