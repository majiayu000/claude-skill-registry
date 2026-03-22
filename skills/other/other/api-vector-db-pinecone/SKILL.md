---
name: api-vector-db-pinecone
description: Pinecone serverless vector database -- index management, vector operations, metadata filtering, namespaces, hybrid search, inference API
---

# Pinecone Patterns

> **Quick Guide:** Use `@pinecone-database/pinecone` (v7.x) for serverless vector database operations. Target indexes by host (`pc.index({ host })`), not by name. Use namespaces for multi-tenant isolation (physically separate, cheaper queries). Batch upserts at 200 records (max 1,000 or 2 MB). Metadata is limited to 40 KB per record with flat key-value pairs only (no nested objects). Pinecone is eventually consistent -- vectors may not appear in queries immediately after upsert. Use `describeIndexStats()` to verify indexing progress. For hybrid search, use `dotproduct` metric with sparse+dense vectors in a single index.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST target indexes by host URL, not by name -- `pc.index({ host })` is the v7 API; `pc.index('name')` is deprecated)**

**(You MUST batch upserts to max 1,000 records or 2 MB per request -- exceeding either limit causes a 400 error)**

**(You MUST use flat key-value metadata only -- nested objects, null values, and keys starting with `$` are rejected by Pinecone)**

**(You MUST handle eventual consistency -- vectors are not queryable immediately after upsert; use `describeIndexStats()` or retry logic for freshness-critical flows)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Client setup, index creation, upsert, query, fetch, update, delete
- [Namespaces & Multi-Tenancy](examples/namespaces.md) -- Namespace isolation, multi-tenant patterns, namespace management API
- [Metadata Filtering](examples/metadata-filtering.md) -- Filter operators, compound filters, best practices
- [Hybrid Search](examples/hybrid-search.md) -- Sparse-dense vectors, hybrid index setup, alpha weighting
- [Inference API](examples/inference.md) -- Embedding generation, reranking, integrated inference indexes
- [Batch Operations](examples/batch-operations.md) -- Chunked upserts, parallel ingestion, bulk import

**Additional resources:**

- [reference.md](reference.md) -- API quick reference, filter operators, limits, decision frameworks, production checklist

---

**Auto-detection:** Pinecone, @pinecone-database/pinecone, createIndex, createIndexForModel, upsert, query, topK, includeMetadata, sparseValues, namespace, describeIndexStats, vector database, similarity search, embedding, cosine, dotproduct, euclidean, RAG retrieval, semantic search, pinecone-sparse-english, rerank, searchRecords, upsertRecords, fetchByMetadata

**When to use:**

- Semantic search over document embeddings (RAG retrieval)
- Similarity search for recommendations, deduplication, or classification
- Multi-tenant vector isolation using namespaces
- Hybrid semantic + keyword search using sparse-dense vectors
- Embedding generation and result reranking via Pinecone Inference API

**Key patterns covered:**

- Client setup and index management (serverless vs pod-based)
- Vector CRUD operations (upsert, query, fetch, update, delete)
- Metadata filtering with compound operators
- Namespace-based multi-tenancy
- Sparse-dense hybrid search
- Pinecone Inference API (embed, rerank)
- Batch ingestion with chunking and parallelism
- Integrated inference indexes (automatic embedding)

**When NOT to use:**

- Full-text search with complex boolean queries (use a dedicated search engine)
- Relational data with joins and transactions (use a relational database)
- Real-time streaming or pub/sub messaging (use a message broker)
- Storing large binary blobs or documents (use object storage; store only embeddings + metadata references)

---

<philosophy>

## Philosophy

Pinecone is a **managed serverless vector database** purpose-built for similarity search at scale. The core principle: **store embeddings and metadata, query by vector similarity, filter by metadata.**

**Core principles:**

1. **Vectors in, results out** -- Pinecone stores high-dimensional vectors and returns the most similar ones. It is not a general-purpose database. Structure your data as embeddings + metadata references.
2. **Namespaces for isolation** -- Use namespaces to physically separate tenant data. Queries scan only the target namespace, reducing cost and latency compared to metadata filtering across a shared namespace.
3. **Metadata is for filtering, not storage** -- Keep metadata small (40 KB limit) and flat. Store document content in your primary database; store only filterable attributes (category, date, tenant ID) as Pinecone metadata.
4. **Batch for throughput** -- Individual upserts are inefficient. Batch at 200 records for optimal throughput (max 1,000 or 2 MB per request).
5. **Eventual consistency is normal** -- Freshly upserted vectors may not appear in query results immediately. Design your application to tolerate brief staleness or poll `describeIndexStats()` before querying.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Initialization

Create a Pinecone client from an API key. See [examples/core.md](examples/core.md) for full examples.

```typescript
// Good Example
import { Pinecone } from "@pinecone-database/pinecone";

function createPineconeClient(): Pinecone {
  const apiKey = process.env.PINECONE_API_KEY;
  if (!apiKey) {
    throw new Error("PINECONE_API_KEY environment variable is required");
  }
  return new Pinecone({ apiKey });
}

export { createPineconeClient };
```

**Why good:** API key from environment variable, validation before construction, named export

```typescript
// Bad Example
import { Pinecone } from "@pinecone-database/pinecone";
const pc = new Pinecone({ apiKey: "sk-abc123..." });
// Hardcoded key leaks in version control
```

**Why bad:** Hardcoded API key is a security risk, no validation

---

### Pattern 2: Index Targeting (v7 API)

Always target an index by its host URL, not its name. See [examples/core.md](examples/core.md).

```typescript
// Good Example -- target by host
const indexModel = await pc.createIndex({
  name: "products",
  dimension: EMBEDDING_DIMENSION,
  metric: "cosine",
  spec: { serverless: { cloud: "aws", region: "us-east-1" } },
});

const index = pc.index({ host: indexModel.host });
```

**Why good:** `pc.index({ host })` is the v7 API, avoids an extra API call to resolve the name to a host

```typescript
// Bad Example -- target by name (deprecated)
const index = pc.index("products");
// Triggers an extra describeIndex call to resolve the host URL
```

**Why bad:** Targeting by name requires an extra network call and is deprecated in v7

---

### Pattern 3: Upsert with Metadata

Upsert vectors with flat metadata for filtering. See [examples/core.md](examples/core.md) for typed metadata.

```typescript
// Good Example
interface DocumentMetadata {
  title: string;
  category: string;
  createdAt: number; // Unix timestamp (numbers only, no Date objects)
}

const NAMESPACE = "articles";

await index.namespace(NAMESPACE).upsert({
  records: [
    {
      id: "doc-1",
      values: embedding, // number[] matching index dimension
      metadata: { title: "Guide", category: "tutorial", createdAt: 1710000000 },
    },
  ],
});
```

**Why good:** Typed metadata interface, flat key-value pairs, numeric timestamp (not Date), namespace isolation

---

### Pattern 4: Query with Metadata Filter

Query for similar vectors with metadata filtering. See [examples/metadata-filtering.md](examples/metadata-filtering.md) for all operators.

```typescript
// Good Example
const TOP_K = 10;

const results = await index.namespace(NAMESPACE).query({
  vector: queryEmbedding,
  topK: TOP_K,
  includeMetadata: true,
  filter: {
    $and: [
      { category: { $eq: "tutorial" } },
      { createdAt: { $gte: 1700000000 } },
    ],
  },
});

for (const match of results.matches) {
  console.log(match.id, match.score, match.metadata);
}
```

**Why good:** Named constant for topK, structured filter with `$and`, includes metadata in response

```typescript
// Bad Example
const results = await index.query({
  vector: queryEmbedding,
  topK: 100,
  includeMetadata: true,
  filter: { tags: ["a", "b"] }, // INVALID: arrays are not valid filter values
});
```

**Why bad:** Missing namespace (queries default namespace), array filter syntax is invalid (use `$in`), no named constant for topK

---

### Pattern 5: Namespace-Based Multi-Tenancy

Use namespaces for tenant isolation. See [examples/namespaces.md](examples/namespaces.md).

```typescript
// Good Example -- physically isolated tenant data
function getTenantIndex(pc: Pinecone, host: string, tenantId: string) {
  return pc.index({ host }).namespace(`tenant-${tenantId}`);
}

// Each tenant's queries scan only their namespace
const tenantIndex = getTenantIndex(pc, INDEX_HOST, "acme-corp");
const results = await tenantIndex.query({ vector: embedding, topK: TOP_K });
```

**Why good:** Physical isolation per tenant, queries scan only the target namespace (lower cost and latency)

```typescript
// Bad Example -- metadata filtering for multi-tenancy
await index.query({
  vector: embedding,
  topK: 10,
  filter: { tenantId: { $eq: "acme-corp" } },
  // Scans ENTIRE index, filters after -- expensive at scale
});
```

**Why bad:** Metadata filtering scans the full namespace regardless of filter selectivity, cost scales with total data not tenant data

---

### Pattern 6: Pinecone Inference API

Generate embeddings and rerank results. See [examples/inference.md](examples/inference.md).

```typescript
// Good Example -- embed text
const embedResult = await pc.inference.embed({
  model: "multilingual-e5-large",
  inputs: [{ text: "What is machine learning?" }],
  parameters: { inputType: "query", truncate: "END" },
});
const queryVector = embedResult.data[0].values;
```

**Why good:** Specifies `inputType` (query vs passage), handles truncation for long inputs

```typescript
// Good Example -- rerank results
const rerankResult = await pc.inference.rerank({
  model: "pinecone-rerank-v0",
  query: "machine learning basics",
  documents: results.matches.map((m) => ({
    id: m.id,
    text: m.metadata?.content as string,
  })),
  topN: 5,
  returnDocuments: true,
});
```

**Why good:** Reranks query results for better relevance, limits output with `topN`

</patterns>

---

<decision_framework>

## Decision Framework

### Which Index Type?

```
Which Pinecone index type should I use?
|-- Serverless? (recommended for most use cases)
|   |-- Variable or unpredictable traffic? -> Serverless (auto-scales, pay-per-use)
|   |-- Starting a new project? -> Serverless (simpler, no capacity planning)
|   '-- Need hybrid sparse-dense search? -> Serverless with dotproduct metric
|
'-- Pod-based? (legacy, specific needs)
    |-- Need guaranteed low latency SLAs? -> Pod-based (dedicated compute)
    '-- Using collections for snapshots? -> Pod-based (collections are pod-only)
```

### Which Metric?

```
Which distance metric should I use?
|-- Using embeddings from a language model? -> cosine (normalized, most common)
|-- Need hybrid search (sparse + dense)? -> dotproduct (REQUIRED for hybrid)
|-- Comparing raw feature vectors? -> euclidean (absolute distance matters)
'-- Unsure? -> cosine (safe default for most embedding models)
```

### Namespaces vs Metadata Filtering?

```
How should I isolate tenant data?
|-- Strict data isolation required? -> Namespaces (physical separation)
|-- Need to query across tenants? -> Metadata filtering (logical separation)
|-- Cost-sensitive at scale? -> Namespaces (query cost = tenant size, not total)
|-- Few tenants (< 10)? -> Either approach works
'-- Many tenants (100+)? -> Namespaces (metadata filtering scans everything)
```

### Embedded Inference vs External Embeddings?

```
How should I generate embeddings?
|-- Want simplest architecture? -> Integrated inference (createIndexForModel)
|   (Pinecone handles embedding automatically on upsert/query)
|
|-- Need a specific embedding model not hosted by Pinecone? -> External
|   (Generate embeddings yourself, upsert raw vectors)
|
|-- Need hybrid search with sparse vectors? -> External sparse model
|   (Use pinecone-sparse-english-v0 via inference API + your dense model)
|
'-- Need full control over embedding pipeline? -> External
    (Custom preprocessing, chunking, model selection)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Targeting index by name instead of host -- `pc.index("name")` is deprecated in v7; use `pc.index({ host })` to avoid an extra API call
- Upserting vectors with wrong dimensions -- dimension mismatch causes a 400 error; verify your embedding model's output dimension matches the index
- Nested metadata objects -- Pinecone only supports flat key-value metadata; nested objects are silently ignored or rejected
- Using metadata filtering for multi-tenancy at scale -- scans the entire namespace regardless of filter selectivity; use namespaces instead

**Medium Priority Issues:**

- Missing `includeMetadata: true` in queries -- metadata is NOT included by default; omitting this returns only IDs and scores
- Upsert batches exceeding 1,000 records or 2 MB -- triggers a 400 error; chunk at 200 records for safety margin
- Using `Date` objects in metadata -- Pinecone metadata supports strings, numbers, booleans, and string arrays only; convert dates to Unix timestamps
- Not awaiting `createIndex()` readiness -- index creation is async; the index is not ready for operations immediately after `createIndex()` returns

**Common Mistakes:**

- Querying immediately after upsert and expecting results -- eventual consistency means freshly upserted vectors may not be queryable for seconds
- Using `topK` > 1,000 with `includeMetadata: true` -- the max `topK` is 1,000 when including metadata or values; without them, max is 10,000
- Passing array values as metadata filter values (`{ tags: ["a", "b"] }`) -- use `$in` operator instead: `{ tags: { $in: ["a", "b"] } }`
- Forgetting that `deleteAll()` without a namespace deletes from the default namespace only, not the entire index

**Gotchas & Edge Cases:**

- `describeIndexStats()` returns approximate counts -- record counts are not exact in real-time, especially after recent upserts or deletes
- Metadata values are always returned as their original types, but filter comparisons are type-strict -- `$eq: "42"` does not match numeric `42`
- Sparse vector indices must be positive 32-bit integers (uint32), and values must be non-zero floats -- zero values are silently dropped
- `listPaginated()` returns vector IDs only (no values or metadata) -- use `fetch()` to get full vector data
- The `$in` and `$nin` operators accept a maximum of 10,000 values each
- Metadata keys cannot start with `$` (reserved for operators)
- `upsert` is an upsert, not an insert -- upserting with an existing ID overwrites the previous vector and metadata entirely (no partial merge)
- `update()` merges metadata by default -- updating metadata replaces only the fields you specify, not the entire metadata object
- The v7 SDK includes built-in automatic retry with exponential backoff for transient errors -- custom retry logic is only needed for fine-grained control or non-default retry policies
- `upsertRecords` (integrated inference) accepts a direct array, not `{ records: [...] }` -- this differs from the regular `upsert` method which uses `{ records: [...] }`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST target indexes by host URL, not by name -- `pc.index({ host })` is the v7 API; `pc.index('name')` is deprecated)**

**(You MUST batch upserts to max 1,000 records or 2 MB per request -- exceeding either limit causes a 400 error)**

**(You MUST use flat key-value metadata only -- nested objects, null values, and keys starting with `$` are rejected by Pinecone)**

**(You MUST handle eventual consistency -- vectors are not queryable immediately after upsert; use `describeIndexStats()` or retry logic for freshness-critical flows)**

**Failure to follow these rules will cause index creation failures, rejected upserts, empty query results, and degraded multi-tenant performance.**

</critical_reminders>
