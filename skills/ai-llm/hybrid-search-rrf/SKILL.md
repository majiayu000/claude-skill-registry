---
name: hybrid-search-rrf
description: Reciprocal Rank Fusion for merging full-text and vector search results in this project. Convex native searchIndex + vectorIndex integration with admin-toggleable hybrid search. Triggers on "hybrid search", "RRF", "full-text", "vector search", "mergeMessagesWithRRF", "searchIndex", "vectorIndex".
---

# Hybrid Search with RRF

Project combines Convex full-text search (keyword matching) with vector search (semantic similarity) using Reciprocal Rank Fusion algorithm. Admin-controlled feature for messages and memories.

## Why Hybrid Search

**Coverage gap**: Full-text finds exact keywords, vector finds meaning. Neither is complete.

Examples:
- User searches "cancel subscription" - vector finds "terminate my plan"
- User searches "GPT-4" - full-text finds exact model name missed by embeddings
- Overlapping results get boosted (appear in both = high relevance)

**When enabled**: Check admin settings in actions, fallback to text-only if disabled.

```typescript
// From convex/search/hybrid.ts
const adminSettings = (await (ctx.runQuery as any)(
  api.adminSettings.get,
  {},
)) as { enableHybridSearch?: boolean } | null;
const hybridSearchEnabled = adminSettings?.enableHybridSearch ?? false;

if (!hybridSearchEnabled) {
  return textResults.slice(0, limit);
}
```

## RRF Algorithm

**Formula**: `score = weight * 1 / (k + rank + 1)`

- `k = 60` (default constant, smooths ranking differences)
- Higher rank = lower score
- Overlapping results: sum scores from both sources (boosted)
- Optional source weights (knowledge bank > files > conversations)

```typescript
// From convex/lib/utils/search.ts
export function applyRRF<T extends { _id: { toString(): string }; source?: string }>(
  textResults: T[],
  vectorResults: T[],
  k = 60,
  sourceWeights?: Record<string, number>,
): (T & { score: number })[] {
  const scores = new Map<string, { score: number; item: T }>();

  const getWeight = (item: T): number => {
    if (!sourceWeights || !item.source) return 1.0;
    return sourceWeights[item.source] ?? 1.0;
  };

  // Score text results
  textResults.forEach((item, idx) => {
    const id = item._id.toString();
    const weight = getWeight(item);
    scores.set(id, { score: weight * (1 / (k + idx + 1)), item });
  });

  // Score vector results, boost if already exists
  vectorResults.forEach((item, idx) => {
    const id = item._id.toString();
    const weight = getWeight(item);
    const score = weight * (1 / (k + idx + 1));
    const existing = scores.get(id);
    if (existing) {
      existing.score += score; // Key: overlapping results boosted
    } else {
      scores.set(id, { score, item });
    }
  });

  return Array.from(scores.values())
    .sort((a, b) => b.score - a.score)
    .map(({ item, score }) => ({ ...item, score }));
}
```

**Source weights** (when available):
```typescript
// From convex/lib/utils/search.ts
export const DEFAULT_SOURCE_WEIGHTS: Record<string, number> = {
  knowledgeBank: 1.5,
  files: 1.2,
  notes: 1.0,
  tasks: 1.0,
  conversations: 0.8,
};
```

## Full-Text Search (Convex searchIndex)

**Schema requirement**: Add search index to `schema.ts`:
```typescript
defineTable("messages", { ... })
  .searchIndex("search_content", {
    searchField: "content",
    filterFields: ["userId"],
  })
```

**Query pattern**:
```typescript
// From convex/search/hybrid.ts
export const fullTextSearch = query({
  handler: async (ctx, args) => {
    let results = await ctx.db
      .query("messages")
      .withSearchIndex("search_content", (q) => q.search("content", args.query))
      .filter((q) => q.eq(q.field("userId"), args.userId))
      .take(args.limit);

    // Apply additional filters not in index
    if (args.conversationId) {
      results = results.filter((m) => m.conversationId === args.conversationId);
    }

    if (args.dateFrom !== undefined && args.dateTo !== undefined) {
      results = results.filter(
        (m) => m.createdAt >= args.dateFrom! && m.createdAt <= args.dateTo!,
      );
    }

    return results;
  },
});
```

**Limitations**: filterFields only support equality checks. Date ranges, complex conditions need post-filter.

## Vector Search (Convex vectorIndex)

**Schema requirement**: Add vector index to `schema.ts`:
```typescript
defineTable("messages", {
  embedding: v.optional(v.array(v.float64())),
  ...
})
  .vectorIndex("by_embedding", {
    vectorField: "embedding",
    dimensions: 1536, // text-embedding-3-small
    filterFields: ["userId", "conversationId"],
  })
```

**Query pattern**:
```typescript
// From convex/search/hybrid.ts
const { embedding } = await embed({
  model: EMBEDDING_MODEL,
  value: args.query,
});

const vectorResults = await ctx.vectorSearch("messages", "by_embedding", {
  vector: embedding,
  limit: 40,
  filter: (q: any) =>
    args.conversationId
      ? q.eq("userId", user._id).eq("conversationId", args.conversationId)
      : q.eq("userId", user._id),
});

// Extract Doc<"messages"> (vectorSearch adds _score field)
const vectorResultMessages = vectorResults.map((r) => {
  const { _score, ...messageDoc } = r;
  return messageDoc as Doc<"messages">;
});
```

**Post-filter unsupported fields**:
```typescript
// From convex/search/hybrid.ts
let filteredVectorResults = vectorResultMessages;

if (args.dateFrom !== undefined && args.dateTo !== undefined) {
  filteredVectorResults = filteredVectorResults.filter(
    (m) => m.createdAt >= args.dateFrom! && m.createdAt <= args.dateTo!,
  );
}

if (args.messageType) {
  filteredVectorResults = filteredVectorResults.filter(
    (m) => m.role === args.messageType,
  );
}
```

## Hybrid Search Action (Messages)

**Pattern**: Action (not query) because generates embedding.

```typescript
// From convex/search/hybrid.ts
export const hybridSearch = action({
  args: {
    query: v.string(),
    limit: v.optional(v.number()),
    conversationId: v.optional(v.id("conversations")),
    dateFrom: v.optional(v.number()),
    dateTo: v.optional(v.number()),
    messageType: v.optional(v.union(v.literal("user"), v.literal("assistant"))),
  },
  handler: async (ctx, args): Promise<Doc<"messages">[]> => {
    const user = await getCurrentUser(ctx);
    if (!user) return [];

    const limit = args.limit || 20;

    // Check admin toggle
    const adminSettings = await ctx.runQuery(api.adminSettings.get, {});
    const hybridSearchEnabled = adminSettings?.enableHybridSearch ?? false;

    // 1. Full-text (always)
    const textResults = await ctx.runQuery(api.search.fullTextSearch, {
      query: args.query,
      userId: user._id,
      conversationId: args.conversationId,
      dateFrom: args.dateFrom,
      dateTo: args.dateTo,
      messageType: args.messageType,
      limit: hybridSearchEnabled ? 40 : limit, // Fetch more for RRF
    });

    // 2. Early return if hybrid disabled
    if (!hybridSearchEnabled) {
      return textResults.slice(0, limit);
    }

    // 3. Vector search with fallback
    try {
      const tokenCount = estimateTokens(args.query);
      const { embedding } = await embed({
        model: EMBEDDING_MODEL,
        value: args.query,
      });

      // Track cost
      await ctx.scheduler.runAfter(
        0,
        internal.usage.mutations.recordEmbedding,
        {
          userId: user._id,
          model: EMBEDDING_PRICING.model,
          tokenCount,
          cost: calculateEmbeddingCost(tokenCount),
          feature: "chat",
        },
      );

      const vectorResults = await ctx.vectorSearch("messages", "by_embedding", {
        vector: embedding,
        limit: 40,
        filter: (q: any) =>
          args.conversationId
            ? q.eq("userId", user._id).eq("conversationId", args.conversationId)
            : q.eq("userId", user._id),
      });

      const vectorResultMessages = vectorResults.map((r) => {
        const { _score, ...messageDoc } = r;
        return messageDoc as Doc<"messages">;
      });

      // Apply post-filters
      let filteredVectorResults = vectorResultMessages;
      if (args.dateFrom !== undefined && args.dateTo !== undefined) {
        filteredVectorResults = filteredVectorResults.filter(
          (m) => m.createdAt >= args.dateFrom! && m.createdAt <= args.dateTo!,
        );
      }
      if (args.messageType) {
        filteredVectorResults = filteredVectorResults.filter(
          (m) => m.role === args.messageType,
        );
      }

      // 4. RRF merge
      return mergeMessagesWithRRF(
        textResults,
        filteredVectorResults.slice(0, 40),
        limit,
      );
    } catch (error) {
      logger.error("Vector search failed, falling back to text-only", {
        tag: "HybridSearch",
        error: String(error),
      });
      return textResults.slice(0, limit);
    }
  },
});
```

## Hybrid Search with Reranking (Memories)

**Advanced pattern**: RRF merge + quality filtering + LLM reranking.

```typescript
// From convex/memories/search.ts
export const hybridSearch = internalAction({
  args: {
    userId: v.id("users"),
    query: v.string(),
    limit: v.optional(v.number()),
    category: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const limit = args.limit ?? 10;
    const searchLimit = Math.min(limit * 4, 40); // RRF needs more

    // 1. Generate embedding
    const { embedding } = await embed({
      model: EMBEDDING_MODEL,
      value: args.query,
    });

    // 2. Run both searches in parallel
    const [textResults, vectorResults] = await Promise.all([
      ctx.runQuery(internal.memories.search.keywordSearch, {
        userId: args.userId,
        query: args.query,
        limit: searchLimit,
        category: args.category,
      }),
      ctx.runAction(internal.memories.search.vectorSearch, {
        userId: args.userId,
        embedding,
        limit: searchLimit,
        category: args.category,
      }),
    ]);

    // 3. Merge with RRF
    const merged = applyRRF(textResults, vectorResults, 60);

    // 4. Filter by quality
    const now = Date.now();
    const filtered = merged.filter((m) => {
      if (m.metadata?.confidence && m.metadata.confidence < MIN_CONFIDENCE) {
        return false;
      }
      if (m.metadata?.expiresAt && m.metadata.expiresAt < now) {
        return false;
      }
      if (m.metadata?.supersededBy) {
        return false;
      }
      return true;
    });

    // 5. Take top 20 for reranking
    const candidates = filtered.slice(0, 20);

    // 6. Rerank with LLM
    const reranked = await rerankMemories(args.query, candidates, ctx, args.userId);

    // 7. Return final top N
    return reranked.slice(0, limit);
  },
});
```

**Reranking**: Use small model (gpt-4o-mini) to reorder top candidates based on relevance.

## Fallback Pattern

**Always have text-only fallback** if vector fails or disabled.

```typescript
// From convex/search/hybrid.ts
try {
  const { embedding } = await embed({ ... });
  const vectorResults = await ctx.vectorSearch(...);
  return mergeMessagesWithRRF(textResults, vectorResults, limit);
} catch (error) {
  logger.error("Vector search failed, falling back to text-only", {
    tag: "HybridSearch",
    error: String(error),
  });
  return textResults.slice(0, limit);
}
```

## Quality Thresholds

**For filtering search results**:
```typescript
// From convex/lib/utils/search.ts
const HIGH_QUALITY_THRESHOLD = 0.85;
const MEDIUM_QUALITY_THRESHOLD = 0.7;

export function getQualityLevel(scores: number[]): QualityResult {
  if (scores.length === 0) return { level: "low", topScore: 0 };
  const topScore = Math.max(...scores);
  if (topScore >= HIGH_QUALITY_THRESHOLD) return { level: "high", topScore };
  if (topScore >= MEDIUM_QUALITY_THRESHOLD) return { level: "medium", topScore };
  return { level: "low", topScore };
}
```

**Used to decide**: early return vs reranking in memories search.

## Key Files

- `packages/backend/convex/search/hybrid.ts` - Messages hybrid search action
- `packages/backend/convex/lib/utils/search.ts` - RRF algorithm, quality thresholds
- `packages/backend/convex/memories/search.ts` - Memories hybrid search with reranking
- `packages/backend/convex/schema.ts` - searchIndex and vectorIndex definitions

## Common Patterns

**Fetch more for RRF**: Request 40 results from each source to have enough for merging.

**Extract score field**: `vectorSearch` returns `{ _score, ...doc }`, strip before type casting.

**Post-filter complex conditions**: searchIndex/vectorIndex limited filterFields, apply JS filter after.

**Track embedding cost**: Always record usage when generating embeddings for vector search.

**Admin toggle**: Check `adminSettings.enableHybridSearch` in actions, default false.

## Avoid

- Don't use hybrid search in queries (embedding generation requires action)
- Don't skip fallback to text-only if vector fails
- Don't forget to strip `_score` field from vectorSearch results before type casting
- Don't apply RRF with same limit as final (fetch 40, merge, slice to limit)
- Don't use vector search without checking admin settings first
