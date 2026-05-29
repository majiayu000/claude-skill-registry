---
name: budget-tracker-patterns
description: Backend budget tracking patterns for AI generation. Awareness-based tracking (not blocking), tool timeouts, per-tool rate limits, token estimates, context window management, truncation strategies, search quality detection. Triggers on "budget", "tool timeout", "rate limit", "token estimate", "truncation", "context window", "search quality", "diminishing returns".
---

# Budget Tracker Patterns

Awareness-based tracking for AI generation tool calls. Tracks context consumption, detects runaway patterns, provides visibility. Does NOT block tool calls - existing step limits handle that.

## BudgetState Interface

Core state tracked during generation:

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
export interface BudgetState {
  maxTokens: number;
  usedTokens: number;
  toolCallCount: number;
  searchHistory: Array<{
    query: string;
    resultCount: number;
    topScore: number;
  }>;
  toolCallCounts: Record<string, number>; // Per-tool counts for rate limiting
}
```

Initialize:
```typescript
const budget = createBudgetState(maxTokens);
```

Update immutably:
```typescript
budget = recordUsage(budget, tokens);
budget = recordToolCall(budget, toolName);
budget = recordSearch(budget, query, resultCount, topScore);
```

## Tool Timeout Pattern

Wall-clock timeout wrapper prevents stuck tools:

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
export async function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  operation: string,
): Promise<T> {
  let timeoutId: ReturnType<typeof setTimeout>;

  const timeoutPromise = new Promise<never>((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new TimeoutError(operation, timeoutMs));
    }, timeoutMs);
  });

  try {
    const result = await Promise.race([promise, timeoutPromise]);
    clearTimeout(timeoutId!);
    return result;
  } catch (error) {
    clearTimeout(timeoutId!);
    throw error;
  }
}
```

**Tool timeouts** (milliseconds):
```typescript
export const TOOL_TIMEOUTS: Record<string, number> = {
  searchAll: 30000,        // 30s - multiple parallel searches
  searchFiles: 15000,
  searchNotes: 15000,
  searchTasks: 15000,
  searchKnowledgeBank: 15000,
  queryHistory: 15000,
  urlReader: 120000,       // 2min - external fetch slow
  codeExecution: 120000,   // 2min - code execution takes time
  youtubeVideo: 300000,    // 5min - video processing slow
  weather: 60000,          // 1min - external API
  calculator: 5000,
  datetime: 1000,
  default: 30000,
};
```

Usage:
```typescript
const timeout = getToolTimeout(toolName);
const result = await withTimeout(toolPromise, timeout, `${toolName} call`);
```

## Per-Tool Rate Limits

Prevent tool abuse while allowing reasonable usage:

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
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

Check before calling:
```typescript
const { limited, message } = isToolRateLimited(budget, toolName);
if (limited) {
  return { error: message };
}
budget = recordToolCall(budget, toolName);
```

Returns:
```typescript
{
  limited: true,
  message: "searchAll limit reached (5/5). Try a different approach."
}
```

## Token Estimation

Rough estimates for context tracking (chars/4 approximation):

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
const TOOL_TOKEN_ESTIMATES: Record<string, number> = {
  searchAll: 800,
  searchFiles: 400,
  searchNotes: 300,
  searchTasks: 300,
  searchKnowledgeBank: 500,
  queryHistory: 400,
  urlReader: 1500,
  codeExecution: 600,
  calculator: 100,
  datetime: 50,
  weather: 200,
  default: 300,
};
```

Get estimate before tool execution:
```typescript
const estimatedCost = estimateToolCost(toolName);
```

Record actual usage after:
```typescript
const actualTokens = countTokens(toolResult);
budget = recordUsage(budget, actualTokens);
```

## Context Getting Full Detection

Tiered warnings based on usage:

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
export function formatStatus(state: BudgetState): string {
  const percentUsed = getContextPercent(state);
  const toolCount = state.toolCallCount;

  if (percentUsed >= 70) {
    return `[Budget Critical: ~${percentUsed}% context, ${toolCount} tools]
Answer now with current info or ask user for clarification.`;
  }

  if (percentUsed >= 50) {
    return `[Budget: ~${percentUsed}% context, ${toolCount} tools]
Prioritize essential searches only.`;
  }

  return `[Context: ${toolCount} tool calls, ~${percentUsed}% of context used]`;
}
```

Check programmatically:
```typescript
if (isContextGettingFull(budget)) {
  // >= 50% used - inject warning into prompt
}
```

## Truncation Strategy

Preserve structure while managing context:

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
export const MIN_TOOL_CALLS_FOR_TRUNCATION = 2; // Don't truncate first tool call

export function truncateToolResult(
  result: unknown,
  maxChars: number = 500,
): unknown {
  const str = JSON.stringify(result);
  if (str.length <= maxChars) return result;

  // Arrays: keep first 3 items
  if (Array.isArray(result)) {
    return result
      .slice(0, 3)
      .map((item) => truncateToolResult(item, Math.floor(maxChars / 3)));
  }

  // Strings: truncate with marker
  if (typeof result === "string") {
    return `${result.slice(0, maxChars)}... [truncated]`;
  }

  // Objects: truncate string values
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

Apply after MIN_TOOL_CALLS_FOR_TRUNCATION:
```typescript
if (budget.toolCallCount >= MIN_TOOL_CALLS_FOR_TRUNCATION) {
  toolResult = truncateToolResult(toolResult);
}
```

## Search Quality Detection

Detect diminishing returns from repeated searches:

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
export const LOW_QUALITY_SCORE_THRESHOLD = 0.7;

export function formatSearchWarning(state: BudgetState): string | null {
  const { searchHistory } = state;
  if (searchHistory.length === 0) return null;

  const latest = searchHistory[searchHistory.length - 1];

  // Repeated query
  const isDuplicate = searchHistory
    .slice(0, -1)
    .some((h) => h.query.toLowerCase().trim() === latest.query.toLowerCase().trim());
  if (isDuplicate) {
    return `Already searched "${latest.query}". Try different terms or answer with current info.`;
  }

  // Decreasing quality (3+ searches)
  if (searchHistory.length >= 3) {
    const last3 = searchHistory.slice(-3).map((h) => h.topScore);
    if (last3[0] > last3[1] && last3[1] > last3[2] && last3[2] < 0.5) {
      return "Search quality declining. Consider different approach or ask user.";
    }
  }

  // Many searches without good results
  if (searchHistory.length >= 4) {
    return "Multiple searches performed. Consider answering with current info.";
  }

  return null;
}
```

Check for stuck patterns:
```typescript
export function shouldSuggestAskUser(state: BudgetState): boolean {
  const { searchHistory } = state;

  // 3+ searches with all low quality results
  if (searchHistory.length >= 3) {
    const recentScores = searchHistory.slice(-3).map((h) => h.topScore);
    if (recentScores.every((s) => s < 0.7)) return true;
  }

  // Budget critical (>= 70%)
  if (getContextPercent(state) >= 70) return true;

  return false;
}
```

## Key Files

- `packages/backend/convex/lib/budgetTracker.ts` - Budget tracking, timeouts, truncation
- `packages/backend/convex/generation/tools.ts` - Tool building with budget integration

## BuildTools Integration

Pass budget state to tools for rate limiting:

```typescript
// From packages/backend/convex/generation/tools.ts
export interface BuildToolsConfig {
  ctx: ActionCtx;
  userId: Id<"users">;
  conversationId: Id<"conversations">;
  budgetState?: {
    current: BudgetState;
    update: (newState: BudgetState) => void;
  };
  // ... other config
}

export function buildTools(config: BuildToolsConfig): Record<string, unknown> {
  const { budgetState } = config;

  // Pass budgetState to tools that need it (searchAll, etc.)
  tools.searchAll = createSearchAllTool(
    ctx,
    userId,
    conversationId,
    searchCache,
    budgetState, // Tool can check limits and update state
  );
}
```

## Avoid

- Don't block tool calls based on budget - use for awareness only
- Don't skip timeout wrapper - prevents generation hangs
- Don't ignore rate limits - prevents tool abuse
- Don't truncate first tool call - need full initial context
- Don't ignore search quality warnings - indicates stuck patterns
