---
name: api-vector-db-chroma
description: Chroma vector database -- collection management, automatic embedding, metadata filtering, document storage, query patterns
---

# Chroma Patterns

> **Quick Guide:** Use `chromadb` (v3.x) with `@chroma-core/default-embed` for automatic embedding. Chroma auto-embeds documents if no embeddings are provided -- just pass `documents` and `ids` to `collection.add()`. Use `where` for metadata filtering and `whereDocument` for document content filtering (`$contains`, `$regex`). Default distance metric is `l2` (Euclidean); use `cosine` for most embedding models via `configuration: { hnsw: { space: "cosine" } }`. Query results return nested arrays (`ids: string[][]`) because queries are batched -- always access `results.ids[0]` for a single query. Include only the fields you need via the `include` parameter to reduce payload size.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST install `@chroma-core/default-embed` alongside `chromadb` -- the default embedding function ships as a separate package since v3)**

**(You MUST access query results as nested arrays -- `results.ids[0]`, `results.documents[0]` -- because Chroma batches queries and returns `string[][]` not `string[]`)**

**(You MUST use the `configuration` parameter for HNSW settings -- the legacy `metadata: { "hnsw:space": "cosine" }` approach is deprecated)**

**(You MUST use flat metadata values only (string, number, boolean, typed arrays) -- nested objects are not supported and will be rejected)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Client setup, collection management, add, query, get, update, upsert, delete
- [Metadata Filtering](examples/metadata-filtering.md) -- Filter operators, compound filters, document content filters, whereDocument
- [Embedding Functions](examples/embedding-functions.md) -- Default, OpenAI, custom embedding functions, provider packages

**Additional resources:**

- [reference.md](reference.md) -- API quick reference, filter operators, include options, limits, production checklist

---

**Auto-detection:** Chroma, chromadb, ChromaClient, CloudClient, createCollection, getOrCreateCollection, collection.add, collection.query, collection.get, collection.upsert, queryTexts, queryEmbeddings, nResults, whereDocument, $contains, @chroma-core/default-embed, @chroma-core/openai, EmbeddingFunction, vector database, semantic search, embedding, RAG retrieval, hnsw:space

**When to use:**

- Semantic search over document embeddings (RAG retrieval)
- Rapid prototyping with automatic embedding generation (no external embedding pipeline needed)
- Metadata-filtered vector search with compound logical operators
- Document content filtering with `$contains` and `$regex`
- Local development with in-process or Docker-based Chroma server

**Key patterns covered:**

- Client setup (HTTP, Cloud, Docker)
- Collection management (create, get, delete, configure HNSW)
- Document CRUD with automatic embedding (add, query, get, update, upsert, delete)
- Metadata filtering (`where`) with comparison, set, array, and logical operators
- Document content filtering (`whereDocument`) with `$contains` and `$regex`
- Embedding function configuration (default, OpenAI, custom)
- Query result handling (nested array structure, include options)

**When NOT to use:**

- Full-text search with complex boolean ranking (use a dedicated search engine)
- Relational data with joins and transactions (use a relational database)
- Multi-modal image+text embeddings in TypeScript (currently Python-only in Chroma)
- High-scale production with millions of vectors and strict SLAs (evaluate managed vector databases)

---

<philosophy>

## Philosophy

Chroma is a **lightweight, developer-friendly embedding database** designed for rapid prototyping and production RAG applications. The core principle: **pass documents in, get relevant results out -- Chroma handles embedding automatically.**

**Core principles:**

1. **Documents first, vectors optional** -- Unlike most vector databases, Chroma can embed documents automatically using a configured embedding function. You never need to manage embeddings directly unless you want to.
2. **Collections are self-contained** -- Each collection has its own embedding function, distance metric, and HNSW configuration. No global index management needed.
3. **Metadata is for filtering, documents are for content** -- Use `where` for structured metadata filters and `whereDocument` for full-text content filters. Both can be combined in a single query.
4. **Batteries included** -- The default embedding function (`all-MiniLM-L6-v2` via `@chroma-core/default-embed`) works out of the box for English text. Swap to OpenAI, Cohere, or any provider with a single package change.
5. **Query results are batched** -- Chroma supports multiple queries in a single call. Results are always nested arrays (`string[][]`), even for single queries. Always access `[0]` for the first query's results.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Initialization

Create a ChromaClient connected to a running Chroma server. See [examples/core.md](examples/core.md) for full examples.

```typescript
// Good Example
import { ChromaClient } from "chromadb";

function createChromaClient(): ChromaClient {
  const chromaUrl = process.env.CHROMA_URL;
  if (!chromaUrl) {
    throw new Error("CHROMA_URL environment variable is required");
  }
  return new ChromaClient({ path: chromaUrl });
}

export { createChromaClient };
```

**Why good:** Server URL from environment variable, validation before construction, named export

```typescript
// Bad Example
import { ChromaClient } from "chromadb";
const client = new ChromaClient(); // Silently defaults to http://localhost:8000
```

**Why bad:** Implicit default URL makes deployment-specific bugs hard to trace, no validation

---

### Pattern 2: Collection with Distance Metric

Create a collection with a specific distance metric via the `configuration` parameter. See [examples/core.md](examples/core.md).

```typescript
// Good Example
import { ChromaClient } from "chromadb";

const COLLECTION_NAME = "documents";

async function createCosineCollection(client: ChromaClient) {
  const collection = await client.createCollection({
    name: COLLECTION_NAME,
    configuration: {
      hnsw: { space: "cosine" },
    },
  });
  return collection;
}

export { createCosineCollection };
```

**Why good:** Uses `configuration` parameter (not deprecated metadata approach), named constant for collection name, `cosine` metric for most embedding models

```typescript
// Bad Example -- deprecated metadata approach
const collection = await client.createCollection({
  name: "docs",
  metadata: { "hnsw:space": "cosine" }, // DEPRECATED: use configuration instead
});
```

**Why bad:** `metadata` prefix for HNSW settings is deprecated in v3; use `configuration: { hnsw: { space } }` instead

---

### Pattern 3: Add Documents with Automatic Embedding

Add documents and let Chroma embed them automatically. See [examples/core.md](examples/core.md).

```typescript
// Good Example
const COLLECTION_NAME = "articles";

async function addArticles(
  client: ChromaClient,
  articles: Array<{ id: string; text: string; category: string }>,
): Promise<void> {
  const collection = await client.getOrCreateCollection({
    name: COLLECTION_NAME,
  });

  await collection.add({
    ids: articles.map((a) => a.id),
    documents: articles.map((a) => a.text),
    metadatas: articles.map((a) => ({ category: a.category })),
  });
}

export { addArticles };
```

**Why good:** `getOrCreateCollection` is idempotent, documents auto-embedded, structured metadata for filtering

```typescript
// Bad Example
await collection.add({
  ids: ["1"],
  // Neither documents nor embeddings provided -- throws error
  metadatas: [{ category: "tutorial" }],
});
```

**Why bad:** Either `documents` or `embeddings` must be provided; metadata alone is insufficient

---

### Pattern 4: Query with Metadata and Document Filters

Query using both metadata filtering (`where`) and document content filtering (`whereDocument`). See [examples/metadata-filtering.md](examples/metadata-filtering.md) for all operators.

```typescript
// Good Example
const N_RESULTS = 10;

const results = await collection.query({
  queryTexts: ["machine learning fundamentals"],
  nResults: N_RESULTS,
  where: {
    $and: [{ category: { $eq: "tutorial" } }, { year: { $gte: 2023 } }],
  },
  whereDocument: { $contains: "neural network" },
  include: ["documents", "metadatas", "distances"],
});

// Results are nested arrays -- access [0] for first query
for (let i = 0; i < results.ids[0].length; i++) {
  console.log(results.ids[0][i], results.distances?.[0][i]);
}
```

**Why good:** Combined metadata + document filter, named constant for nResults, correct nested array access `[0]`, explicit `include` to control response payload

```typescript
// Bad Example
const results = await collection.query({
  queryTexts: ["query"],
  nResults: 5,
});
// BUG: treats results.ids as flat array
for (const id of results.ids) {
  console.log(id); // Prints the inner array, not individual IDs!
}
```

**Why bad:** `results.ids` is `string[][]` not `string[]`; must access `results.ids[0]` for the first query's results

---

### Pattern 5: Get with Pagination

Retrieve documents by ID or metadata filter with pagination. See [examples/core.md](examples/core.md).

```typescript
// Good Example
const PAGE_SIZE = 50;

async function getDocumentsByCategory(
  collection: Awaited<ReturnType<ChromaClient["getCollection"]>>,
  category: string,
  offset: number = 0,
) {
  const results = await collection.get({
    where: { category: { $eq: category } },
    limit: PAGE_SIZE,
    offset,
    include: ["documents", "metadatas"],
  });

  return results;
}

export { getDocumentsByCategory };
```

**Why good:** Pagination via `limit`/`offset`, metadata filtering without vector query, explicit include

---

### Pattern 6: Upsert for Idempotent Operations

Upsert creates new records or updates existing ones by ID. See [examples/core.md](examples/core.md).

```typescript
// Good Example
async function upsertDocuments(
  collection: Awaited<ReturnType<ChromaClient["getCollection"]>>,
  docs: Array<{
    id: string;
    text: string;
    metadata: Record<string, string | number | boolean>;
  }>,
): Promise<void> {
  await collection.upsert({
    ids: docs.map((d) => d.id),
    documents: docs.map((d) => d.text),
    metadatas: docs.map((d) => d.metadata),
  });
}

export { upsertDocuments };
```

**Why good:** Idempotent -- creates or updates depending on ID existence, re-embeds documents automatically

</patterns>

---

<decision_framework>

## Decision Framework

### Which Distance Metric?

```
Which distance metric should I use?
|-- Using embeddings from a language model? -> cosine (normalized, most common)
|-- Need dot product similarity? -> ip (inner product)
|-- Comparing raw feature vectors? -> l2 (Euclidean, Chroma default)
'-- Unsure? -> cosine (safe default for most embedding models)
```

### Which Embedding Function?

```
Which embedding function should I use?
|-- Quick prototyping, English text? -> @chroma-core/default-embed (all-MiniLM-L6-v2, runs locally)
|-- Need high-quality embeddings? -> @chroma-core/openai (text-embedding-3-small)
|-- Have your own embedding pipeline? -> Pass embeddings directly (skip embedding function)
|-- Need custom model? -> Implement EmbeddingFunction interface
'-- Want all providers? -> npm install @chroma-core/all
```

### Where vs WhereDocument?

```
How should I filter results?
|-- Structured attributes (category, year, status)? -> where (metadata filter)
|-- Full-text content search? -> whereDocument ($contains, $regex)
|-- Both? -> Combine where + whereDocument in same query
'-- Need exact match on specific IDs? -> get({ ids: [...] })
```

### ChromaClient vs CloudClient?

```
Which client should I use?
|-- Local development or self-hosted? -> ChromaClient({ path: "http://localhost:8000" })
|-- Chroma Cloud (managed)? -> CloudClient({ apiKey, tenant, database })
|-- Docker deployment? -> ChromaClient with Docker host URL
'-- Testing? -> ChromaClient against local Docker container
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Accessing query results as flat arrays instead of nested -- `results.ids` is `string[][]`, not `string[]`; always use `results.ids[0]` for single-query results
- Missing `@chroma-core/default-embed` package -- since v3, the default embedding function ships separately; `npm install chromadb @chroma-core/default-embed`
- Using deprecated `metadata: { "hnsw:space": "cosine" }` for HNSW config -- use `configuration: { hnsw: { space: "cosine" } }` instead
- Nested objects in metadata -- Chroma only supports flat key-value metadata; nested objects are rejected

**Medium Priority Issues:**

- Not specifying `include` in queries -- default includes vary (`query` returns documents, metadatas, distances; `get` returns documents, metadatas); explicitly set `include` for clarity and to control payload size
- Using `l2` (default) when `cosine` is appropriate -- most embedding models are normalized for cosine similarity; `l2` may produce worse results
- Calling `add()` without `documents` or `embeddings` -- at least one must be provided; metadata alone is insufficient
- Not handling empty results -- `results.ids[0]` may be an empty array; check length before processing

**Common Mistakes:**

- Passing `queryEmbeddings` AND `queryTexts` together -- use one or the other, not both
- Expecting `update()` to create missing records -- `update()` silently ignores non-existent IDs; use `upsert()` for create-or-update semantics
- Calling `delete()` with no arguments -- deletes nothing (not everything); pass `ids` or `where` to target specific records
- Using `$gt`/`$lt` on string metadata -- comparison operators only work on numeric values (int or float)

**Gotchas & Edge Cases:**

- HNSW configuration (`space`, `ef_construction`, `max_neighbors`) cannot be changed after collection creation -- you must delete and recreate the collection
- `collection.count()` returns total records in the collection, not filtered counts -- there is no filtered count API
- `peek()` returns the first `limit` items (default 10) in insertion order, not by relevance -- useful for debugging, not querying
- `$contains` in `whereDocument` is case-sensitive -- searching for "Neural" will not match "neural"
- `$regex` in `whereDocument` uses full regex syntax but can be slow on large collections
- Array metadata values (`string[]`, `number[]`) must be homogeneous -- mixing types within an array is rejected
- Metadata keys are case-sensitive -- `Category` and `category` are different fields
- The `nResults` default is 10 if not specified in `query()`
- Multimodal embedding (images + text) is currently Python-only -- TypeScript support is not yet available

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST install `@chroma-core/default-embed` alongside `chromadb` -- the default embedding function ships as a separate package since v3)**

**(You MUST access query results as nested arrays -- `results.ids[0]`, `results.documents[0]` -- because Chroma batches queries and returns `string[][]` not `string[]`)**

**(You MUST use the `configuration` parameter for HNSW settings -- the legacy `metadata: { "hnsw:space": "cosine" }` approach is deprecated)**

**(You MUST use flat metadata values only (string, number, boolean, typed arrays) -- nested objects are not supported and will be rejected)**

**Failure to follow these rules will cause embedding failures, incorrect result access, deprecated configuration warnings, and rejected metadata.**

</critical_reminders>
