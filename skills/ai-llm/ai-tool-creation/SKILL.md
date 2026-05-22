---
name: ai-tool-creation
description: AI SDK v5 tool creation patterns for this project. Factory functions, Zod schemas, budget tracking, rate limiting, caching, timeout handling. Triggers on "tool", "ai tool", "searchAll", "codeExecution", "urlReader", "tool creation".
---

# AI Tool Creation

Tools for Vercel AI SDK v5. All tools use factory pattern, Zod validation, budget tracking, rate limiting, search caching, timeout enforcement.

## Tool Factory Pattern

Tools created via factory functions accepting `ctx`, `userId`, optional params:

```typescript
// From convex/ai/tools/search/searchAll.ts
export function createSearchAllTool(
  ctx: ActionCtx,
  userId: Id<"users">,
  currentConversationId?: Id<"conversations">,
  searchCache?: Map<string, unknown>,
  budgetState?: {
    current: BudgetState;
    update: (newState: BudgetState) => void;
  },
) {
  return tool({
    description: `Search across ALL resource types...`,
    inputSchema: z.object({ ... }),
    execute: async ({ query, projectId, resourceTypes, limit }) => { ... },
  });
}
```

**Pattern**: Factory wraps `tool()` from AI SDK, captures context in closure.

## Zod Input Schema

Describe all parameters clearly - AI reads these to understand tool usage:

```typescript
// From convex/ai/tools/search/searchAll.ts
inputSchema: z.object({
  query: z.string().describe("What to search for across all resources"),
  projectId: z
    .string()
    .optional()
    .describe("Optional project ID to filter results to a specific project"),
  resourceTypes: z
    .array(z.enum(["files", "notes", "tasks", "conversations", "knowledgeBank"]))
    .optional()
    .default(["knowledgeBank", "files", "notes", "tasks", "conversations"])
    .describe("Which resource types to search (default: all including knowledgeBank)"),
  limit: z
    .number()
    .min(1)
    .max(10)
    .optional()
    .default(3)
    .describe("Number of results per resource type (1-10, default: 3)"),
}),
```

**Key**: Use `.describe()` on every field. Default values in schema, not execute logic.

## Description Format

Multi-line with usage guidance:

```typescript
// From convex/ai/tools/urlReader.ts
description: `Read and extract content from web pages.

✅ USE FOR:
- Documentation, articles, blog posts
- Web pages, news articles
- Any non-video URL content

⚠️ FOR YOUTUBE LINKS: Use the youtubeVideo tool instead - it can analyze the actual video content, not just the page text.

Returns clean markdown or text content.`,
```

**Pattern**: Brief summary, use cases (✅ USE FOR), anti-patterns (❌ DO NOT USE FOR), output format.

## Budget State Integration

Rate limiting + token tracking:

```typescript
// From convex/ai/tools/search/searchAll.ts
execute: async ({ query, projectId, resourceTypes, limit }) => {
  // Rate limit check
  if (budgetState) {
    const rateCheck = isToolRateLimited(budgetState.current, "searchAll");
    if (rateCheck.limited) {
      return {
        success: false,
        error: rateCheck.message,
        results: [],
        totalResults: 0,
        quality: { level: "low" as const, topScore: 0 },
        searchedSources: [],
        earlyReturn: false,
      };
    }
    budgetState.update(recordToolCall(budgetState.current, "searchAll"));
  }

  // ... tool logic ...

  // Track search in budget state for diminishing returns detection
  if (budgetState && result.success) {
    const topScore = result.quality?.topScore ?? 0;
    const resultCount = Array.isArray(result.results) ? result.results.length : 0;
    const newState = recordSearch(
      budgetState.current,
      query,
      resultCount,
      topScore,
    );
    budgetState.update(newState);

    // Check for diminishing returns warning
    const warning = formatSearchWarning(newState);
    if (warning) {
      result.warning = warning;
    }
  }

  return result;
},
```

**Pattern**: Check rate limit first, record tool call, track search quality, inject warnings.

## Rate Limit Configuration

Per-tool limits in `convex/lib/budgetTracker.ts`:

```typescript
const TOOL_RATE_LIMITS: Record<string, number> = {
  searchAll: 5,
  searchFiles: 5,
  searchNotes: 5,
  searchTasks: 5,
  searchKnowledgeBank: 5,
  queryHistory: 5,
  urlReader: 3,
  codeExecution: 2,
  weather: 3,
  default: 10,
};
```

**Pattern**: Lower limits for expensive tools (codeExecution: 2), higher for cheap searches (default: 10).

## Timeout Configuration

Per-tool timeouts in `convex/lib/budgetTracker.ts`:

```typescript
export const TOOL_TIMEOUTS: Record<string, number> = {
  searchAll: 30000, // 30s - multiple parallel searches
  searchFiles: 15000,
  searchNotes: 15000,
  searchTasks: 15000,
  searchKnowledgeBank: 15000,
  queryHistory: 15000,
  urlReader: 120000, // 2min - external fetch can be slow
  codeExecution: 120000, // 2min - code execution can take time
  youtubeVideo: 300000, // 5min - video processing is slow
  weather: 60000, // 1min - external API
  calculator: 5000,
  datetime: 1000,
  default: 30000,
};
```

**Pattern**: Higher timeouts for external APIs/processing (urlReader: 2min, youtubeVideo: 5min), lower for local ops (calculator: 5s).

Use with `withTimeout()`:

```typescript
import { withTimeout, getToolTimeout } from "../../lib/budgetTracker";

const result = await withTimeout(
  someOperation(),
  getToolTimeout("urlReader"),
  "urlReader",
);
```

## Search Cache Pattern

Deduplicate identical searches within generation:

```typescript
// From convex/ai/tools/search/searchAll.ts
function getCacheKey(
  query: string,
  resourceTypes: string[],
  projectId?: string,
): string {
  return `${query}:${resourceTypes.sort().join(",")}:${projectId ?? ""}`;
}

// In execute:
const cacheKey = getCacheKey(query, resourceTypes, projectId);
if (searchCache?.has(cacheKey)) {
  return searchCache.get(cacheKey);
}

// ... perform search ...

// Cache successful result
searchCache?.set(cacheKey, result);
return result;
```

**Pattern**: Check cache before work, cache after success. Cache key includes all params. Cache cleared after each generation (not persisted).

## ProjectId Filtering

Optional `projectId` parameter - null = search all resources:

```typescript
// From convex/ai/tools/search/searchAll.ts
projectId: z
  .string()
  .optional()
  .describe("Optional project ID to filter results to a specific project"),

// Pass to internal action:
await (ctx.runAction as any)(
  // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
  internal.tools.search.searchAll.searchAll,
  {
    userId,
    query,
    projectId: projectId as Id<"projects"> | undefined,
    resourceTypes,
    limit,
    currentConversationId,
  },
);

// Error handling for invalid projectId:
catch (error: any) {
  if (error.message?.includes("does not match the table name")) {
    return {
      success: false,
      error: "Invalid projectId - the ID provided is not a valid project ID",
      // ... return error shape matching success shape ...
    };
  }
  throw error;
}
```

**Pattern**: Optional `.string()` in schema, cast to `Id<"projects"> | undefined` when calling action. Handle validation errors gracefully.

## Tool Registration

Register tools in `convex/generation/tools.ts`:

```typescript
// From convex/generation/tools.ts
export function buildTools(config: BuildToolsConfig): Record<string, unknown> {
  const { ctx, userId, conversationId, searchCache, budgetState } = config;

  // Capability tools: ALWAYS available
  const calculatorTool = createCalculatorTool();
  const urlReaderTool = createUrlReaderTool(ctx);
  const codeExecutionTool = createCodeExecutionTool(ctx);

  const tools: Record<string, any> = {
    calculator: calculatorTool,
    urlReader: urlReaderTool,
    codeExecution: codeExecutionTool,
  };

  // Conditional tools based on incognito/mode
  if (enableReadTools) {
    tools.searchAll = createSearchAllTool(
      ctx,
      userId,
      conversationId,
      searchCache,
      budgetState,
    );
  }

  return tools;
}
```

**Pattern**: Tools categorized (capability, write, read, document). Conditional registration based on conversation settings.

## Multi-Step Tool Calling

Use `stopWhen: stepCountIs(N)` for multi-step continuation:

```typescript
import { streamText, stepCountIs } from "ai";

const result = streamText({
  model,
  messages,
  tools: buildTools(config),
  stopWhen: stepCountIs(5), // Continue until 5 steps OR no more tool calls
});
```

**NOT** `maxSteps` (deprecated in AI SDK v5). `stopWhen` enables proper multi-step continuation.

## Tool Result Truncation

Truncate large results for context management:

```typescript
// From convex/lib/budgetTracker.ts
export function truncateToolResult(
  result: unknown,
  maxChars: number = 500,
): unknown {
  const str = JSON.stringify(result);
  if (str.length <= maxChars) return result;

  // Preserve structure for arrays - keep first N items
  if (Array.isArray(result)) {
    return result
      .slice(0, MAX_TRUNCATED_ARRAY_ITEMS)
      .map((item) =>
        truncateToolResult(item, Math.floor(maxChars / MAX_TRUNCATED_ARRAY_ITEMS)),
      );
  }

  // Truncate string content
  if (typeof result === "string") {
    return `${result.slice(0, maxChars)}... [truncated]`;
  }

  // For objects, truncate string values
  if (typeof result === "object" && result !== null) {
    const truncated: Record<string, unknown> = {};
    const keys = Object.keys(result);
    if (keys.length === 0) return result;
    const charPerKey = Math.floor(maxChars / keys.length);
    for (const key of keys) {
      truncated[key] = truncateToolResult(
        (result as Record<string, unknown>)[key],
        charPerKey,
      );
    }
    return truncated;
  }

  return result;
}
```

**Pattern**: Preserve structure (arrays → first N items, objects → truncate values per key). Use after `MIN_TOOL_CALLS_FOR_TRUNCATION` (2) calls.

## Type Casting Pattern

TypeScript recursion workaround for 94+ Convex modules:

```typescript
// From convex/ai/tools/urlReader.ts
const result = (await (ctx.runAction as any)(
  // @ts-ignore - TypeScript recursion limit with 94+ Convex modules
  internal.tools.urlReader.readUrl,
  { url, maxLength, format },
)) as { content: string; title?: string; error?: string };
```

**Pattern**: Cast `ctx.runAction` to `any`, add `@ts-ignore` with explanation, assert return type. Full type safety on return, bypass on parameters.

## Key Files

- `packages/backend/convex/generation/tools.ts` - Tool registry, buildTools()
- `packages/backend/convex/ai/tools/search/searchAll.ts` - Search tool with caching
- `packages/backend/convex/ai/tools/urlReader.ts` - External API tool
- `packages/backend/convex/ai/tools/codeExecution.ts` - Long-running tool
- `packages/backend/convex/lib/budgetTracker.ts` - Rate limits, timeouts, tracking

## Avoid

- Don't hardcode rate limits in tools - use `TOOL_RATE_LIMITS` config
- Don't skip budget state integration for search tools
- Don't use `maxSteps` (deprecated) - use `stopWhen: stepCountIs(N)`
- Don't forget to cache search results - identical queries waste tokens
- Don't return different shapes for success/error - keep consistent structure
- Don't skip projectId validation errors - handle gracefully with user-friendly messages
