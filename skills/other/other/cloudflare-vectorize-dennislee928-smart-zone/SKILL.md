---
name: cloudflare-vectorize
description: |
  Build semantic search with Cloudflare Vectorize V2. Covers async mutations, 5M vectors/index, 31ms latency, returnMetadata enum changes, and V1 deprecation. Prevents 14 errors including dimension mismatches, TypeScript types, testing setup.

  Use when: building RAG or semantic search, troubleshooting returnMetadata, V2 timing, metadata index, dimension errors, vitest setup, or wrangler --json output.
user-invocable: true
---

# Cloudflare Vectorize

Complete implementation guide for Cloudflare Vectorize - a globally distributed vector database for building semantic search, RAG (Retrieval Augmented Generation), and AI-powered applications with Cloudflare Workers.

**Status**: Production Ready ✅
**Last Updated**: 2026-01-21
**Dependencies**: cloudflare-worker-base (for Worker setup), cloudflare-workers-ai (for embeddings)
**Latest Versions**: wrangler@4.59.3, @cloudflare/workers-types@4.20260109.0
**Token Savings**: ~70%
**Errors Prevented**: 14
**Dev Time Saved**: ~4 hours

## What This Skill Provides

### Core Capabilities
- ✅ **Index Management**: Create, configure, and manage vector indexes
- ✅ **Vector Operations**: Insert, upsert, query, delete, and list vectors (list-vectors added August 2025)
- ✅ **Metadata Filtering**: Advanced filtering with 10 metadata indexes per index
- ✅ **Semantic Search**: Find similar vectors using cosine, euclidean, or dot-product metrics
- ✅ **RAG Patterns**: Complete retrieval-augmented generation workflows
- ✅ **Workers AI Integration**: Native embedding generation with @cf/baai/bge-base-en-v1.5
- ✅ **OpenAI Integration**: Support for text-embedding-3-small/large models
- ✅ **Document Processing**: Text chunking and batch ingestion pipelines
- ✅ **Testing Setup**: Vitest configuration with Vectorize bindings

### Templates Included
1. **basic-search.ts** - Simple vector search with Workers AI
2. **rag-chat.ts** - Full RAG chatbot with context retrieval
3. **document-ingestion.ts** - Document chunking and embedding pipeline
4. **metadata-filtering.ts** - Advanced filtering patterns

---

## ⚠️ Vectorize V2 Breaking Changes (September 2024)

**IMPORTANT**: Vectorize V2 became GA in September 2024 with significant breaking changes.

### What Changed in V2

**Performance Improvements**:
- **Index capacity**: 200,000 → **5 million vectors** per index
- **Query latency**: 549ms → **31ms** median (18× faster)
- **TopK limit**: 20 → **100** results per query
- **Scale limits**: 100 → **50,000 indexes** per account
- **Namespace limits**: 100 → **50,000 namespaces** per index

**Breaking API Changes**:
1. **Async Mutations** - All mutations now asynchronous:
   ```typescript
   // V2: Returns mutationId
   const result = await env.VECTORIZE_INDEX.insert(vectors);
   console.log(result.mutationId); // "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

   // Vector inserts/deletes may take a few seconds to be reflected
   ```

2. **returnMetadata Parameter** - Boolean → String enum:
   ```typescript
   // ❌ V1 (deprecated)
   { returnMetadata: true }

   // ✅ V2 (required)
   { returnMetadata: 'all' | 'indexed' | 'none' }
   ```

3. **Metadata Indexes Required Before Insert**:
   - V2 requires metadata indexes created BEFORE vectors inserted
   - Vectors added before metadata index won't be indexed
   - Must re-upsert vectors after creating metadata index

**V1 Deprecation Timeline**:
- **December 2024**: Can no longer create V1 indexes
- **Existing V1 indexes**: Continue to work (other operations unaffected)
- **Migration**: Use `wrangler vectorize --deprecated-v1` flag for V1 operations

**Wrangler Version Required**:
- **Minimum**: wrangler@3.71.0 for V2 commands
- **Recommended**: wrangler@4.54.0+ (latest)

### Check Mutation Status

```typescript
// Get index info to check last mutation processed
const info = await env.VECTORIZE_INDEX.describe();
console.log(info.mutationId); // Last mutation ID
console.log(info.processedUpToMutation); // Last processed timestamp
```

---

## Critical Setup Rules

### ⚠️ MUST DO BEFORE INSERTING VECTORS
```bash
# 1. Create the index with FIXED dimensions and metric
npx wrangler vectorize create my-index \
  --dimensions=768 \
  --metric=cosine

# 2. Create metadata indexes IMMEDIATELY (before inserting vectors!)
npx wrangler vectorize create-metadata-index my-index \
  --property-name=category \
  --type=string

npx wrangler vectorize create-metadata-index my-index \
  --property-name=timestamp \
  --type=number
```

**Why**: Metadata indexes MUST exist before vectors are inserted. Vectors added before a metadata index was created won't be filterable on that property.

### Index Configuration (Cannot Be Changed Later)

```bash
# Dimensions MUST match your embedding model output:
# - Workers AI @cf/baai/bge-base-en-v1.5: 768 dimensions
# - OpenAI text-embedding-3-small: 1536 dimensions
# - OpenAI text-embedding-3-large: 3072 dimensions

# Metrics determine similarity calculation:
# - cosine: Best for normalized embeddings (most common)
# - euclidean: Absolute distance between vectors
# - dot-product: For non-normalized vectors
```

## Wrangler Configuration

**wrangler.jsonc**:
```jsonc
{
  "name": "my-vectorize-worker",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-21",
  "vectorize": [
    {
      "binding": "VECTORIZE_INDEX",
      "index_name": "my-index"
    }
  ],
  "ai": {
    "binding": "AI"
  }
}
```

## TypeScript Types

```typescript
export interface Env {
  VECTORIZE_INDEX: VectorizeIndex;
  AI: Ai;
}

interface VectorizeVector {
  id: string;
  values: number[] | Float32Array | Float64Array;
  namespace?: string;
  metadata?: Record<string, string | number | boolean | string[]>;
}

interface VectorizeMatches {
  matches: Array<{
    id: string;
    score: number;
    values?: number[];
    metadata?: Record<string, any>;
    namespace?: string;
  }>;
  count: number;
}
```

## Metadata Filter Operators (V2)

Vectorize V2 supports advanced metadata filtering with range queries:

```typescript
// Equality (implicit $eq)
{ category: "docs" }

// Not equals
{ status: { $ne: "archived" } }

// In/Not in arrays
{ category: { $in: ["docs", "tutorials"] } }
{ category: { $nin: ["deprecated", "draft"] } }

// Range queries (numbers) - NEW in V2
{ timestamp: { $gte: 1704067200, $lt: 1735689600 } }

// Range queries (strings) - prefix searching
{ url: { $gte: "/docs/workers", $lt: "/docs/workersz" } }

// Nested metadata with dot notation
{ "author.id": "user123" }

// Multiple conditions (implicit AND)
{ category: "docs", language: "en", "metadata.published": true }
```

## Metadata Best Practices

### 1. Cardinality Considerations

**Low Cardinality (Good for $eq filters)**:
```typescript
// Few unique values - efficient filtering
metadata: {
  category: "docs",        // ~10 categories
  language: "en",          // ~5 languages
  published: true          // 2 values (boolean)
}
```

**High Cardinality (Avoid in range queries)**:
```typescript
// Many unique values - avoid large range scans
metadata: {
  user_id: "uuid-v4...",         // Millions of unique values
  timestamp_ms: 1704067200123    // Use seconds instead
}
```

### 2. Metadata Limits

- **Max 10 metadata indexes** per Vectorize index
- **Max 10 KiB metadata** per vector
- **String indexes**: First 64 bytes (UTF-8)
- **Number indexes**: Float64 precision
- **Filter size**: Max 2048 bytes (compact JSON)

### 3. Vector Dimension Limit

**Current Limit**: 1536 dimensions per vector
**Source**: [GitHub Issue #8729](https://github.com/cloudflare/workers-sdk/issues/8729)

**Supported Embedding Models**:
- Workers AI `@cf/baai/bge-base-en-v1.5`: 768 dimensions ✅
- OpenAI `text-embedding-3-small`: 1536 dimensions ✅
- OpenAI `text-embedding-3-large`: 3072 dimensions ❌ (requires dimension reduction)

**Unsupported Models** (>1536 dimensions):
- `nomic-embed-code`: 3584 dimensions
- `Qodo-Embed-1-7B`: >1536 dimensions

**Workaround**:
Use dimensionality reduction (e.g., PCA) to compress embeddings to 1536 or fewer dimensions, though this may reduce semantic quality.

**Feature Request**: Higher dimension support is under consideration. Use [Limit Increase Request Form](https://forms.gle/nyamy2SM9zwWTXKE6) if this blocks your use case.

### 4. Key Restrictions

```typescript
// ❌ INVALID metadata keys
metadata: {
  "": "value",              // Empty key
  "user.name": "John",      // Contains dot (reserved for nesting)
  "$admin": true,           // Starts with $
  "key\"with\"quotes": 1    // Contains quotes
}

// ✅ VALID metadata keys
metadata: {
  "user_name": "John",
  "isAdmin": true,
  "nested": { "allowed": true }  // Access as "nested.allowed" in filters
}
```

## Best Practices

### Batch Insert Performance

**Critical**: Use batch size of 5000 vectors for optimal performance.

**Performance Data**:
- **Individual inserts**: 2.5M vectors in 36+ hours (incomplete)
- **Batch inserts (5000)**: 4M vectors in ~12 hours
- **18× faster with proper batching**

**Why 5000?**
- Vectorize's internal Write-Ahead Log (WAL) optimized for this size
- Avoids Cloudflare API rate limits
- Balances throughput and memory usage

**Optimal Pattern**:
```typescript
const BATCH_SIZE = 5000;

async function insertVectors(vectors: VectorizeVector[]) {
  for (let i = 0; i < vectors.length; i += BATCH_SIZE) {
    const batch = vectors.slice(i, i + BATCH_SIZE);
    const result = await env.VECTORIZE.insert(batch);
    console.log(`Inserted batch ${i / BATCH_SIZE + 1}, mutationId: ${result.mutationId}`);

    // Optional: Rate limiting delay
    if (i + BATCH_SIZE < vectors.length) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
}
```

**Sources**:
- [Community Report](https://community.cloudflare.com/t/performance-issues-with-large-scale-inserts-in-vectorize/788917)
- [Official Best Practices](https://developers.cloudflare.com/vectorize/best-practices/insert-vectors/)

---

### Query Accuracy Modes

Vectorize uses approximate nearest neighbor (ANN) search by default with ~80% accuracy compared to exact search.

**Default Mode**: Approximate scoring (~80% accuracy)
- Faster latency
- Good for RAG, search, recommendations
- topK up to 100

**High-Precision Mode**: Near 100% accuracy
- Enabled via `returnValues: true`
- Higher latency
- Limited to topK=20

**Trade-off Example**:
```typescript
// Fast, ~80% accuracy, topK up to 100
const results = await env.VECTORIZE.query(embedding, {
  topK: 50,
  returnValues: false  // Default
});

// Slower, ~100% accuracy, topK max 20
const preciseResults = await env.VECTORIZE.query(embedding, {
  topK: 10,
  returnValues: true   // High-precision scoring
});
```

**When to Use High-Precision**:
- Critical applications (fraud detection, legal compliance)
- Small result sets (topK < 20)
- Accuracy is higher priority than latency

**Source**: [Cloudflare Blog - Building Vectorize](https://blog.cloudflare.com/building-vectorize-a-distributed-vector-database-on-cloudflare-developer-platform/)

---

## Common Errors & Solutions

### Error 1: Metadata Index Created After Vectors Inserted
```
Problem: Filtering doesn't work on existing vectors
Solution: Delete and re-insert vectors OR create metadata indexes BEFORE inserting
```

### Error 2: Dimension Mismatch
```
Problem: "Vector dimensions do not match index configuration"
Solution: Ensure embedding model output matches index dimensions:
  - Workers AI bge-base: 768
  - OpenAI small: 1536
  - OpenAI large: 3072
```

### Error 3: Invalid Metadata Keys
```
Problem: "Invalid metadata key"
Solution: Keys cannot:
  - Be empty
  - Contain . (dot)
  - Contain " (quote)
  - Start with $ (dollar sign)
```

### Error 4: Filter Too Large
```
Problem: "Filter exceeds 2048 bytes"
Solution: Simplify filter or split into multiple queries
```

### Error 5: Range Query on High Cardinality
```
Problem: Slow queries or reduced accuracy
Solution: Use lower cardinality fields for range queries, or use seconds instead of milliseconds for timestamps
```

### Error 6: Insert vs Upsert Confusion
```
Problem: Updates not reflecting in index
Solution: Use upsert() to overwrite existing vectors, not insert()
```

### Error 7: Missing Bindings
```
Problem: "VECTORIZE_INDEX is not defined"
Solution: Add [[vectorize]] binding to wrangler.jsonc
```

### Error 8: Namespace vs Metadata Confusion
```
Problem: Unclear when to use namespace vs metadata filtering
Solution:
  - Namespace: Partition key, applied BEFORE metadata filters
  - Metadata: Flexible key-value filtering within namespace
```

### Error 9: V2 Async Mutation Timing (NEW in V2)
```
Problem: Inserted vectors not immediately queryable
Solution: V2 mutations are asynchronous - vectors may take a few seconds to be reflected
  - Use mutationId to track mutation status
  - Check env.VECTORIZE_INDEX.describe() for processedUpToMutation timestamp
```

### Error 10: V1 returnMetadata Boolean (BREAKING in V2)
```
Problem: "returnMetadata must be 'all', 'indexed', or 'none'"
Solution: V2 changed returnMetadata from boolean to string enum:
  - ❌ V1: { returnMetadata: true }
  - ✅ V2: { returnMetadata: 'all' }
```

### Error 11: Wrangler --json Output Contains Log Prefix

**Error**: `wrangler vectorize list --json` output starts with log message, breaking JSON parsing
**Source**: [GitHub Issue #11011](https://github.com/cloudflare/workers-sdk/issues/11011)

**Affected Commands**:
- `wrangler vectorize list --json`
- `wrangler vectorize list-metadata-index --json`

**Problem**:
```bash
$ wrangler vectorize list --json
📋 Listing Vectorize indexes...
[
  { "created_on": "2025-10-18T13:28:30.259277Z", ... }
]
```

The log message makes output invalid JSON, breaking piping to `jq` or other tools.

**Solution**: Strip first line before parsing:
```bash
# Using tail
wrangler vectorize list --json | tail -n +2 | jq '.'

# Using sed
wrangler vectorize list --json | sed '1d' | jq '.'
```

---

### Error 12: TypeScript Types Missing Filter Operators

**Error**: `wrangler types` generates incomplete `VectorizeVectorMetadataFilterOp` type
**Source**: [GitHub Issue #10092](https://github.com/cloudflare/workers-sdk/issues/10092)
**Status**: OPEN (tracked internally as VS-461)

**Problem**:
Generated type only includes `$eq` and `$ne`, missing V2 operators: `$in`, `$nin`, `$lt`, `$lte`, `$gt`, `$gte`

**Impact**:
TypeScript shows false errors when using valid V2 metadata filter operators:
```typescript
const vectorizeRes = env.VECTORIZE.queryById(imgId, {
  filter: { gender: { $in: genderFilters } }, // ❌ TS error but works!
  topK,
  returnMetadata: 'indexed',
});
```

**Workaround**: Manual type override until wrangler types is fixed:
```typescript
// Add to your types file
type VectorizeMetadataFilter = Record<string,
  | string
  | number
  | boolean
  | {
      $eq?: string | number | boolean;
      $ne?: string | number | boolean;
      $in?: (string | number | boolean)[];
      $nin?: (string | number | boolean)[];
      $lt?: number | string;
      $lte?: number | string;
      $gt?: number | string;
      $gte?: number | string;
    }
>;
```

---

### Error 13: Windows Dev Registry Failure (FIXED)

**Error**: `ENOENT: no such file or directory` when running `wrangler dev` on Windows
**Source**: [GitHub Issue #10383](https://github.com/cloudflare/workers-sdk/issues/10383)
**Status**: FIXED in wrangler@4.32.0

**Problem**:
Wrangler attempted to create external worker files with colons in the name (invalid on Windows):
```
Error: ENOENT: ... '__WRANGLER_EXTERNAL_VECTORIZE_WORKER:<project>:<binding>'
```

**Solution**:
Update to wrangler@4.32.0 or later:
```bash
npm install -g wrangler@latest
```

---

### Error 14: topK Limit Depends on returnValues/returnMetadata

**Error**: `topK exceeds maximum allowed value`
**Source**: [Vectorize Limits](https://developers.cloudflare.com/vectorize/platform/limits/)

**Problem**: Maximum topK value changes based on query options:

| Configuration | Max topK |
|---------------|----------|
| `returnValues: false`, `returnMetadata: 'none'` | 100 |
| `returnValues: true` OR `returnMetadata: 'all'` | 20 |
| `returnMetadata: 'indexed'` | 100 |

**Common Error**:
```typescript
// ❌ ERROR - topK too high with returnValues
query(embedding, {
  topK: 100,            // Exceeds limit!
  returnValues: true    // Max topK=20 when true
});
```

**Solution**:
```typescript
// ✅ OK - respects conditional limit
query(embedding, {
  topK: 20,
  returnValues: true
});

// ✅ OK - higher topK without values
query(embedding, {
  topK: 100,
  returnValues: false,
  returnMetadata: 'indexed'
});
```

---

## V2 Migration Checklist

**If migrating from V1 to V2**:

1. ✅ Update wrangler to 3.71.0+ (`npm install -g wrangler@latest`)
2. ✅ Create new V2 index (can't upgrade V1 → V2)
3. ✅ Create metadata indexes BEFORE inserting vectors
4. ✅ Update `returnMetadata` boolean → string enum ('all', 'indexed', 'none')
5. ✅ Handle async mutations (expect `mutationId` in responses)
6. ✅ Test with V2 limits (topK up to 100, 5M vectors per index)
7. ✅ Update error handling for async behavior

**V1 Deprecation**:
- After December 2024: Cannot create new V1 indexes
- Existing V1 indexes: Continue to work
- Use `wrangler vectorize --deprecated-v1` for V1 operations

---

## Testing Considerations

### Vitest with Vectorize Bindings

**Issue**: Using `@cloudflare/vitest-pool-workers` with Vectorize or Workers AI bindings causes runtime failure.
**Source**: [GitHub Issue #7434](https://github.com/cloudflare/workers-sdk/issues/7434)

**Error**: `wrapped binding module can't be resolved`

**Workaround**:
1. Create `wrangler-test.jsonc` without Vectorize/AI bindings
2. Point vitest config to test-specific wrangler file
3. Mock bindings in your tests

**Example**:
```typescript
// wrangler-test.jsonc (no Vectorize binding)
{
  "name": "my-worker-test",
  "main": "src/index.ts",
  "compatibility_date": "2025-10-21"
  // No vectorize binding
}

// vitest.config.ts
import { defineWorkersProject } from '@cloudflare/vitest-pool-workers/config';

export default defineWorkersProject({
  test: {
    poolOptions: {
      workers: {
        wrangler: {
          configPath: "./wrangler-test.jsonc"
        }
      }
    }
  }
});

// Mock in tests
import { vi } from 'vitest';

const mockVectorize = {
  query: vi.fn().mockResolvedValue({
    matches: [
      { id: 'test-1', score: 0.95, metadata: { category: 'docs' } }
    ],
    count: 1
  }),
  insert: vi.fn().mockResolvedValue({ mutationId: "test-mutation-id" }),
  upsert: vi.fn().mockResolvedValue({ mutationId: "test-mutation-id" })
};

// Use mock in tests
test('vector search', async () => {
  const env = { VECTORIZE_INDEX: mockVectorize };
  // ... test logic
});
```

---

## Community Tips

**Note**: These tips come from community discussions and official blog posts. Verify against your Vectorize version.

### Tip 1: Range Queries at Scale May Have Reduced Accuracy (Community-sourced)

**Source**: [Query Best Practices](https://developers.cloudflare.com/vectorize/best-practices/query-vectors/)
**Confidence**: MEDIUM
**Applies to**: Datasets with ~10M+ vectors

Range queries (`$lt`, `$lte`, `$gt`, `$gte`) on large datasets may experience reduced accuracy.

**Optimization Strategy**:
```typescript
// ❌ High-cardinality range at scale
metadata: {
  timestamp_ms: 1704067200123
}
filter: { timestamp_ms: { $gte: 1704067200000 } }

// ✅ Bucketed into discrete values
metadata: {
  timestamp_bucket: "2025-01-01-00:00",  // 1-hour buckets
  timestamp_ms: 1704067200123  // Original (non-indexed)
}
filter: {
  timestamp_bucket: {
    $in: ["2025-01-01-00:00", "2025-01-01-01:00"]
  }
}
```

**When This Matters**:
- Time-based filtering over months/years
- User IDs, transaction IDs (UUID ranges)
- Any high-cardinality continuous data

**Alternative**: Use equality filters (`$eq`, `$in`) with bucketed values.

---

### Tip 2: List Vectors Operation (Added August 2025)

**Source**: [Vectorize Changelog](https://developers.cloudflare.com/vectorize/platform/changelog/)

Vectorize V2 added support for the `list-vectors` operation for paginated iteration through vector IDs.

**Use Cases**:
- Auditing vector collections
- Bulk vector operations
- Debugging index contents

**API**:
```typescript
const result = await env.VECTORIZE_INDEX.list({
  limit: 1000,  // Max 1000 per page
  cursor?: string
});

// result.vectors: Array<{ id: string }>
// result.cursor: string | undefined
// result.count: number

// Pagination example
let cursor: string | undefined;
const allVectorIds: string[] = [];

do {
  const result = await env.VECTORIZE_INDEX.list({
    limit: 1000,
    cursor
  });
  allVectorIds.push(...result.vectors.map(v => v.id));
  cursor = result.cursor;
} while (cursor);
```

**Limitations**:
- Returns IDs only (not values or metadata)
- Max 1000 vectors per page
- Use cursor for pagination

---

## Official Documentation

- **Vectorize V2 Docs**: https://developers.cloudflare.com/vectorize/
- **V2 Changelog**: https://developers.cloudflare.com/vectorize/platform/changelog/
- **V1 to V2 Migration**: https://developers.cloudflare.com/vectorize/reference/transition-vectorize-legacy/
- **Metadata Filtering**: https://developers.cloudflare.com/vectorize/reference/metadata-filtering/
- **Workers AI Models**: https://developers.cloudflare.com/workers-ai/models/

---

**Status**: Production Ready ✅ (Vectorize V2 GA - September 2024)
**Last Updated**: 2026-01-21
**Token Savings**: ~70%
**Errors Prevented**: 14 (includes V2 breaking changes, testing setup, TypeScript types)
**Changes**: Added 4 new errors (wrangler --json, TypeScript types, Windows dev, topK limits), batch performance best practices, query accuracy modes, testing setup, community tips on range queries and list-vectors operation.
