---
name: api-vector-db-qdrant
description: Qdrant vector database -- collection management, point operations, payload filtering, named vectors, quantization, recommendations, snapshots
---

# Qdrant Patterns

> **Quick Guide:** Use `@qdrant/js-client-rest` (v1.17.x) for high-performance vector search. Collections define vector dimensions and distance metrics upfront -- mismatches cause silent failures. Use `must`/`should`/`must_not` filter clauses with payload conditions (not Pinecone-style `$eq`/`$and`). Payload indexes are optional but critical for filter performance at scale -- create them explicitly with `createPayloadIndex()`. Named vectors let you store multiple embeddings per point (e.g., title + content). Quantization (scalar/binary/product) trades accuracy for memory and speed. The `query()` method is the universal search endpoint -- prefer it over the older `search()` method.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST create payload indexes with `createPayloadIndex()` for any field used in filters -- unindexed fields cause full scans that degrade linearly with collection size)**

**(You MUST use `must`/`should`/`must_not` filter syntax -- Qdrant does NOT use `$eq`/`$and`/`$or` operators like Pinecone)**

**(You MUST match vector dimensions exactly between embedding model output and collection config -- dimension mismatches cause silent upsert failures or corrupt search results)**

**(You MUST set `wait: true` on writes when subsequent reads depend on the data -- Qdrant writes are asynchronous by default and may not be immediately visible)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Client setup, collection creation, upsert, query, scroll, delete
- [Filtering](examples/filtering.md) -- must/should/must_not conditions, match/range operators, payload indexes
- [Named Vectors & Quantization](examples/named-vectors-quantization.md) -- Multiple vectors per point, scalar/binary/product quantization
- [Recommendations & Batch](examples/recommendations-batch.md) -- Recommend API, batch operations, snapshots

**Additional resources:**

- [reference.md](reference.md) -- API quick reference, filter operators, limits, decision frameworks, production checklist

---

**Auto-detection:** Qdrant, QdrantClient, @qdrant/js-client-rest, createCollection, upsert, query, scroll, recommend, setPayload, createPayloadIndex, must, should, must_not, payload, named vectors, quantization, vector database, similarity search, semantic search, RAG retrieval, embedding search

**When to use:**

- Semantic search over document embeddings (RAG retrieval pipelines)
- Similarity search for recommendations, deduplication, or classification
- Multi-vector search with named vectors (e.g., title embedding + content embedding per document)
- Filtered vector search with complex payload conditions (must/should/must_not)
- Memory-optimized deployments using scalar, binary, or product quantization

**Key patterns covered:**

- Client setup and collection management (distance metrics, HNSW config)
- Point CRUD operations (upsert, query, scroll, retrieve, delete, count)
- Payload filtering with must/should/must_not and match/range conditions
- Named vectors for multiple embeddings per point
- Quantization configuration (scalar, binary, product)
- Recommendation API with positive/negative examples
- Batch operations and snapshot management
- Payload indexing for filter performance

**When NOT to use:**

- Full-text search with BM25 ranking (use a dedicated search engine)
- Relational data with joins and transactions (use a relational database)
- Key-value lookups without vector similarity (use a KV store)
- Storing large documents or binary blobs (store embeddings + metadata references only)

---

<philosophy>

## Philosophy

Qdrant is a **high-performance open-source vector database** built in Rust, designed for filtered similarity search at scale. The core principle: **store vectors with rich payloads, search by similarity, filter by payload conditions.**

**Core principles:**

1. **Payload is first-class** -- Unlike databases that treat metadata as secondary, Qdrant's payload system supports complex nested JSON, multiple data types, and granular indexing. Use payloads for filtering, not just annotation.
2. **Index what you filter** -- Payload indexes are not automatic. Create explicit indexes on fields used in filters via `createPayloadIndex()`. Without indexes, filters cause full collection scans.
3. **Named vectors for multi-modal** -- A single point can hold multiple named vectors (e.g., title embedding + content embedding). Search targets a specific named vector. This avoids duplicating payloads across collections.
4. **Quantization for scale** -- Scalar (4x compression), binary (32x), and product quantization trade accuracy for memory savings. Configure at collection or per-vector level. Use `always_ram: true` to keep quantized vectors in memory for speed.
5. **Writes are async by default** -- Upserts return before data is persisted to all replicas. Set `wait: true` when immediate consistency matters (e.g., read-after-write flows).

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Initialization

Create a QdrantClient connected to a local instance or Qdrant Cloud. See [examples/core.md](examples/core.md) for full examples.

```typescript
// Good Example
import { QdrantClient } from "@qdrant/js-client-rest";

function createQdrantClient(): QdrantClient {
  const url = process.env.QDRANT_URL;
  const apiKey = process.env.QDRANT_API_KEY;
  if (!url) {
    throw new Error("QDRANT_URL environment variable is required");
  }
  return new QdrantClient({ url, apiKey });
}

export { createQdrantClient };
```

**Why good:** URL and API key from environment, validation before construction, named export

```typescript
// Bad Example
import { QdrantClient } from "@qdrant/js-client-rest";
const client = new QdrantClient({
  host: "my-cluster.cloud.qdrant.io",
  apiKey: "sk-abc123...",
});
// Hardcoded credentials leak in version control
```

**Why bad:** Hardcoded API key, host without HTTPS (use `url` with full protocol for cloud)

---

### Pattern 2: Collection Creation

Define vector dimensions and distance metric. Dimension must exactly match your embedding model output. See [examples/core.md](examples/core.md).

```typescript
// Good Example
const EMBEDDING_DIMENSION = 1536;

await client.createCollection("documents", {
  vectors: {
    size: EMBEDDING_DIMENSION,
    distance: "Cosine",
  },
});

export { EMBEDDING_DIMENSION };
```

**Why good:** Named constant for dimension, explicit distance metric, clean config

```typescript
// Bad Example
await client.createCollection("documents", {
  vectors: { size: 768, distance: "Cosine" },
  // Dimension mismatch if using a 1536-dim model -- upserts may silently fail or produce garbage search results
});
```

**Why bad:** Hardcoded dimension that may not match embedding model, no named constant

---

### Pattern 3: Upsert Points with Payload

Upsert vectors with payload (Qdrant's term for metadata). See [examples/core.md](examples/core.md).

```typescript
// Good Example
interface DocumentPayload {
  title: string;
  category: string;
  createdAt: number;
  tags: string[];
}

await client.upsert("documents", {
  wait: true,
  points: [
    {
      id: "doc-1",
      vector: embedding,
      payload: {
        title: "Guide",
        category: "tutorial",
        createdAt: 1710000000,
        tags: ["ai", "search"],
      },
    },
  ],
});
```

**Why good:** Typed payload interface, `wait: true` for immediate consistency, structured payload

---

### Pattern 4: Query with Payload Filter

Use `must`/`should`/`must_not` filter clauses -- NOT Pinecone-style `$eq`/`$and`. See [examples/filtering.md](examples/filtering.md).

```typescript
// Good Example
const TOP_K = 10;

const results = await client.query("documents", {
  query: queryEmbedding,
  filter: {
    must: [
      { key: "category", match: { value: "tutorial" } },
      { key: "createdAt", range: { gte: 1700000000 } },
    ],
  },
  with_payload: true,
  limit: TOP_K,
});

for (const point of results.points) {
  console.log(point.id, point.score, point.payload);
}
```

**Why good:** Named constant for limit, Qdrant filter syntax (must + match/range), `with_payload` included

```typescript
// Bad Example -- Pinecone syntax does NOT work in Qdrant
const results = await client.query("documents", {
  query: embedding,
  filter: {
    $and: [{ category: { $eq: "tutorial" } }],
  },
  limit: 100,
});
```

**Why bad:** Pinecone-style `$and`/`$eq` operators are invalid in Qdrant, magic number for limit

---

### Pattern 5: Named Vectors

Store multiple embeddings per point. See [examples/named-vectors-quantization.md](examples/named-vectors-quantization.md).

```typescript
// Good Example
const TITLE_DIM = 384;
const CONTENT_DIM = 1536;

await client.createCollection("articles", {
  vectors: {
    title: { size: TITLE_DIM, distance: "Cosine" },
    content: { size: CONTENT_DIM, distance: "Cosine" },
  },
});

// Upsert with named vectors
await client.upsert("articles", {
  wait: true,
  points: [
    {
      id: "article-1",
      vector: { title: titleEmbedding, content: contentEmbedding },
      payload: { title: "Intro to Vectors" },
    },
  ],
});

// Search by specific named vector
const results = await client.query("articles", {
  query: queryEmbedding,
  using: "content",
  limit: TOP_K,
});
```

**Why good:** Different dimensions per named vector, `using` specifies which vector to search, avoids duplicating payloads across collections

---

### Pattern 6: Recommendation API

Find similar points using positive/negative examples. See [examples/recommendations-batch.md](examples/recommendations-batch.md).

```typescript
// Good Example
const results = await client.query("documents", {
  query: {
    recommend: {
      positive: [1, 42],
      negative: [7],
      strategy: "best_score",
    },
  },
  limit: TOP_K,
  with_payload: true,
});
```

**Why good:** Uses point IDs as positive/negative examples, `best_score` strategy handles negatives better than default `average_vector`

</patterns>

---

<decision_framework>

## Decision Framework

### Which Distance Metric?

```
Which distance metric should I use?
|-- Using normalized embeddings (OpenAI, Cohere)? -> Cosine (most common, safe default)
|-- Pre-normalized embeddings and need speed? -> Dot (faster, same results as Cosine for unit vectors)
|-- Raw feature vectors where magnitude matters? -> Euclid (L2 distance)
|-- City-block distance needed? -> Manhattan
'-- Unsure? -> Cosine (works with any embedding model)
```

### Single Vector vs Named Vectors?

```
How many embeddings per point?
|-- One embedding model? -> Single vector (simpler config)
|-- Multiple embedding models (title + content)? -> Named vectors
|-- Same model, different text segments? -> Named vectors
|-- Multi-modal (text + image)? -> Named vectors with different dimensions
'-- Want to avoid duplicating payloads across collections? -> Named vectors
```

### Which Quantization Method?

```
How should I optimize memory?
|-- Good default, balanced accuracy/speed? -> Scalar (int8, 4x compression)
|-- Maximum speed, can tolerate accuracy loss? -> Binary (32x compression)
|   '-- Best with high-dimensional models (>= 1024 dims)
|-- Maximum compression, speed not critical? -> Product (up to 64x compression)
|   '-- Slowest quantization, most accuracy loss
'-- No memory pressure? -> Skip quantization (full float32 precision)
```

### Payload Index Strategy?

```
Should I create a payload index?
|-- Field used in filter conditions? -> YES, always index
|-- Field used in order_by for scroll? -> YES, index for sort performance
|-- Field only read after search (display only)? -> NO, skip index
|-- High-cardinality field (UUIDs, timestamps)? -> YES, but evaluate index type
'-- Low-cardinality field (enum-like)? -> YES, keyword index is very efficient
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using Pinecone-style filter syntax (`$eq`, `$and`, `$or`) -- Qdrant uses `must`/`should`/`must_not` with `match`/`range` conditions
- Vector dimension mismatch between embedding model and collection config -- causes silent failures or garbage results
- Missing payload indexes on filtered fields -- causes full collection scans that degrade linearly with size
- Not setting `wait: true` when read-after-write consistency is needed -- writes are async by default

**Medium Priority Issues:**

- Using deprecated `search()` method instead of `query()` -- `query()` is the universal endpoint with prefetch and fusion support
- Forgetting `with_payload: true` in queries -- payload is NOT included by default
- Creating payload indexes after bulk upsert instead of before -- retroactive indexing is slower than indexing during upsert
- Using `offset` for deep pagination in scroll -- performance degrades; use `offset` as cursor (point ID), not page number

**Common Mistakes:**

- Passing `filter` at the wrong nesting level -- filter goes at the top level of the query args, not nested inside another object
- Using `id: 0` as a point ID -- Qdrant requires positive integers or UUID strings; 0 is invalid
- Confusing `setPayload` (merge) with `overwritePayload` (replace) -- `setPayload` merges fields, `overwritePayload` replaces the entire payload
- Calling `deletePayload` with field names but no point selector -- you must specify which points to update via `points` array or `filter`

**Gotchas & Edge Cases:**

- Point IDs must be positive integers or UUID strings -- negative numbers, zero, and non-UUID strings are rejected
- `scroll()` with `order_by` requires a payload index on the sort field -- without it, the request fails
- `count()` with `exact: true` is slow on large collections -- use `exact: false` (default) for approximate counts
- Snapshot recovery requires matching Qdrant minor versions -- a v1.14.x snapshot cannot be restored to a v1.15.x cluster
- Binary quantization works best with high-dimensional vectors (>= 1024 dims) -- for smaller vectors, scalar quantization is more accurate
- `query()` with `prefetch` enables multi-stage retrieval (retrieve 1000, then re-rank to top 10) -- but requires understanding the prefetch pipeline
- Named vector search requires the `using` parameter -- omitting it searches the default (unnamed) vector, which may not exist
- `deletePayload` removes specific keys, `clearPayload` removes ALL keys -- they are different operations

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST create payload indexes with `createPayloadIndex()` for any field used in filters -- unindexed fields cause full scans that degrade linearly with collection size)**

**(You MUST use `must`/`should`/`must_not` filter syntax -- Qdrant does NOT use `$eq`/`$and`/`$or` operators like Pinecone)**

**(You MUST match vector dimensions exactly between embedding model output and collection config -- dimension mismatches cause silent upsert failures or corrupt search results)**

**(You MUST set `wait: true` on writes when subsequent reads depend on the data -- Qdrant writes are asynchronous by default and may not be immediately visible)**

**Failure to follow these rules will cause empty search results, degraded filter performance, data consistency issues, and hard-to-debug dimension mismatch errors.**

</critical_reminders>
