---
name: api-vector-db-weaviate
description: Weaviate vector database patterns with weaviate-client v3 -- collection management, vectorizer modules, hybrid search, filtering, generative search (RAG), multi-tenancy, batch imports
---

# Weaviate Patterns

> **Quick Guide:** Use Weaviate for semantic search and RAG applications. Use **weaviate-client** (v3.x) as the TypeScript client -- it uses gRPC for performance and provides full type safety with generics. Connect via `connectToWeaviateCloud()` for managed instances or `connectToLocal()` for Docker. Collections are the central abstraction -- configure vectorizers at collection level, not per-query. Use `collection.query.*` for search, `collection.generate.*` for RAG, and `collection.data.*` for CRUD. Always call `client.close()` when done. Increase query timeout to 60s+ when using generative search. The v3 client does NOT support browsers or Embedded Weaviate.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `client.close()` when done with the Weaviate client -- it maintains persistent gRPC connections that will leak if not closed)**

**(You MUST configure vectorizers at the COLLECTION level during `client.collections.create()` -- you cannot add a vectorizer after creation, only add new named vectors)**

**(You MUST use a SEPARATE `client.collections.use()` call with `.withTenant()` for multi-tenant queries -- queries without tenant context on multi-tenant collections will fail)**

**(You MUST increase query timeout to 60+ seconds when using `generate.*` (RAG) submodule -- generative model calls are slow and the default timeout causes failures)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Connection, collection setup, object CRUD, basic search
- [Search & Filtering](examples/search.md) -- nearText, nearVector, hybrid, bm25, filters, generative search (RAG)
- [Multi-Tenancy & Batch](examples/multi-tenancy.md) -- Tenant management, batch imports, cross-references

**Additional resources:**

- [reference.md](reference.md) -- API cheat sheet, vectorizer comparison, data types, decision frameworks

---

**Auto-detection:** Weaviate, weaviate-client, connectToWeaviateCloud, connectToLocal, nearText, nearVector, hybrid search, bm25, vector database, semantic search, RAG, generative search, generate.nearText, insertMany, vectorizer, text2vec, multi-tenancy, withTenant, collection.query, collection.generate, collection.data

**When to use:**

- Semantic search over text, images, or multimodal data
- Retrieval Augmented Generation (RAG) with built-in generative search
- Hybrid search combining vector similarity and keyword (BM25) ranking
- Multi-tenant applications needing isolated vector stores per customer
- Applications requiring built-in vectorization (no external embedding pipeline)
- Real-time similarity search with filtering on structured properties

**Key patterns covered:**

- weaviate-client v3 connection setup and configuration
- Collection management with vectorizer modules (text2vec-openai, text2vec-cohere, etc.)
- Object CRUD (insert, insertMany, update, replace, deleteById, deleteMany)
- Search types (nearText, nearVector, hybrid, bm25, fetchObjects)
- Filtering with operators (equal, greaterThan, like, containsAny, and/or/not)
- Generative search (RAG) with singlePrompt and groupedTask
- Multi-tenancy with tenant lifecycle management
- Batch imports with insertMany and error handling
- Cross-references between collections
- Named vectors for multi-vector collections

**When NOT to use:**

- Relational data with complex joins (use PostgreSQL)
- Full-text search without vector component (use Elasticsearch/Meilisearch)
- Key-value caching (use Redis)
- Time-series data (use TimescaleDB/InfluxDB)
- Graph traversal queries (use Neo4j)
- Browser-side applications (v3 client is Node.js only)

---

<philosophy>

## Philosophy

Weaviate is a **vector database** that stores data objects alongside their vector embeddings. The core principle: **configure once at the collection level, then query with simple method calls.**

**Core principles:**

1. **Collection-centric design** -- All configuration (vectorizer, generative model, reranker, properties) is set at collection creation. Queries operate on collection objects obtained via `client.collections.use()`.
2. **Built-in vectorization** -- Weaviate can vectorize data automatically using configured modules (text2vec-openai, text2vec-cohere, etc.). You don't need an external embedding pipeline unless you want one.
3. **Search is a spectrum** -- Use `nearText` for semantic similarity, `bm25` for keyword matching, `hybrid` for a weighted combination. The `alpha` parameter controls the vector-vs-keyword balance in hybrid search.
4. **RAG is a search mode, not a separate system** -- Switch from `collection.query.nearText()` to `collection.generate.nearText()` to add LLM generation on top of search results.
5. **Filters are additive** -- Filters narrow results after vector/keyword retrieval. Combine with `Filters.and()` and `Filters.or()` for complex conditions.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Connection Setup

Connect to Weaviate Cloud or local Docker instance. Always close the client when done. See [examples/core.md](examples/core.md) for full examples.

```typescript
// Good Example -- Cloud connection with API key headers
import weaviate from "weaviate-client";

const QUERY_TIMEOUT_SECONDS = 30;
const INSERT_TIMEOUT_SECONDS = 120;

async function createWeaviateClient() {
  const client = await weaviate.connectToWeaviateCloud(
    process.env.WEAVIATE_URL!,
    {
      authCredentials: new weaviate.ApiKey(process.env.WEAVIATE_API_KEY!),
      headers: {
        "X-OpenAI-Api-Key": process.env.OPENAI_API_KEY!,
      },
      timeout: {
        query: QUERY_TIMEOUT_SECONDS,
        insert: INSERT_TIMEOUT_SECONDS,
      },
    },
  );
  return client;
}

export { createWeaviateClient };
```

**Why good:** Environment variables for credentials, explicit timeouts, API key headers for vectorizer modules

```typescript
// Bad Example -- Missing cleanup, no timeout config
import weaviate from "weaviate-client";
const client = await weaviate.connectToLocal();
// No client.close() -- gRPC connections leak
// No timeout config -- generative queries will timeout
```

**Why bad:** Missing `client.close()` leaks gRPC connections, default timeout too short for RAG queries

---

### Pattern 2: Collection with Vectorizer

Configure vectorizer and properties at creation time. See [examples/core.md](examples/core.md) for named vectors and advanced configuration.

```typescript
// Good Example -- Collection with vectorizer and generative model
import { vectors, dataType, generative } from "weaviate-client";

await client.collections.create({
  name: "Article",
  vectorizers: vectors.text2VecOpenAI({
    model: "text-embedding-3-small",
  }),
  generative: generative.openAI({
    model: "gpt-4o",
  }),
  properties: [
    { name: "title", dataType: dataType.TEXT },
    { name: "body", dataType: dataType.TEXT },
    { name: "category", dataType: dataType.TEXT },
    { name: "publishedAt", dataType: dataType.DATE },
  ],
});
```

**Why good:** Vectorizer and generative model configured at collection level, typed properties with explicit data types

```typescript
// Bad Example -- Trying to add vectorizer after creation
await client.collections.create({ name: "Article" });
// No way to add a vectorizer to an existing collection without named vectors
// Must delete and recreate, or use addVector() for named vectors only
```

**Why bad:** Vectorizer must be set at creation time; cannot be added to an existing default vector after the fact

---

### Pattern 3: Hybrid Search with Filters

Combine vector and keyword search with property filters. See [examples/search.md](examples/search.md) for all search types.

```typescript
// Good Example -- Hybrid search with filter
import { Filters } from "weaviate-client";

const articles = client.collections.use("Article");
const SEARCH_LIMIT = 10;
const HYBRID_ALPHA = 0.75; // Favor vector search

const result = await articles.query.hybrid("machine learning trends", {
  alpha: HYBRID_ALPHA,
  limit: SEARCH_LIMIT,
  filters: Filters.and(
    articles.filter.byProperty("category").equal("technology"),
    articles.filter
      .byProperty("publishedAt")
      .greaterThan(new Date("2024-01-01")),
  ),
  returnMetadata: ["score", "explainScore"],
});

for (const obj of result.objects) {
  console.log(obj.properties.title, obj.metadata?.score);
}
```

**Why good:** Named constants for limits and alpha, combined filter with `Filters.and()`, metadata for debugging relevance

---

### Pattern 4: Generative Search (RAG)

Switch from `query.*` to `generate.*` for RAG. See [examples/search.md](examples/search.md) for singlePrompt and groupedTask patterns.

```typescript
// Good Example -- RAG with single prompt per result
const articles = client.collections.use("Article");
const RAG_RESULT_LIMIT = 5;

const result = await articles.generate.nearText(
  "climate change policy",
  {
    singlePrompt: "Summarize this article in one sentence: {title} - {body}",
  },
  {
    limit: RAG_RESULT_LIMIT,
    returnMetadata: ["distance"],
  },
);

for (const obj of result.objects) {
  console.log("Source:", obj.properties.title);
  console.log("Generated:", obj.generative?.text);
}
```

**Why good:** Uses property interpolation `{title}` in prompt, accesses generated text via `obj.generative?.text`

```typescript
// Bad Example -- Using query instead of generate for RAG
const result = await articles.query.nearText("climate change", { limit: 5 });
// Then manually calling OpenAI API with results
// Weaviate does this natively with generate.*
```

**Why bad:** Misses Weaviate's built-in RAG -- extra network hops, no automatic prompt interpolation

</patterns>

---

<decision_framework>

## Decision Framework

### Which Search Type?

```
What kind of search do I need?
├─ Natural language query, semantic meaning? -> nearText (requires vectorizer module)
├─ Have pre-computed vector embedding? -> nearVector
├─ Exact keyword matching? -> bm25
├─ Both semantic and keyword relevance? -> hybrid (alpha controls blend)
├─ Just list/filter objects without search? -> fetchObjects
└─ Search + LLM generation? -> generate.nearText / generate.hybrid
```

### Which Vectorizer?

```
Which vectorizer module should I use?
├─ OpenAI models (text-embedding-3-small/large)? -> text2VecOpenAI
├─ Cohere models (embed-v3)? -> text2VecCohere
├─ Self-hosted models? -> text2VecOllama or text2VecTransformers
├─ Bring your own embeddings? -> none (use selfProvided for named vectors)
├─ Multimodal (images + text)? -> multi2VecClip or multi2VecBind
└─ Multiple embedding strategies? -> Named vectors (array of vectorizers)
```

### Single vs Named Vectors?

```
How many vector representations do I need?
├─ One embedding per object (most common)? -> Single default vectorizer
├─ Different embeddings for different properties? -> Named vectors
├─ Mix of auto-vectorized and self-provided? -> Named vectors with selfProvided
└─ Different models for different search use cases? -> Named vectors
```

### When to Use Multi-Tenancy?

```
Do I need data isolation?
├─ Each customer/user needs isolated data? -> Enable multi-tenancy
├─ Shared dataset, filter by user? -> Single tenant with filters
├─ Need to offload inactive tenants? -> Multi-tenancy with tenant states
└─ Small number of distinct datasets? -> Separate collections may be simpler
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `client.close()` -- gRPC connections persist and leak memory/file descriptors
- Trying to add a default vectorizer after collection creation -- vectorizer must be configured in `create()`. Only named vectors can be added later with `config.addVector()`
- Querying a multi-tenant collection without `.withTenant()` -- all operations fail with an error
- Using default query timeout with `generate.*` -- generative calls need 60+ seconds; default is often too short

**Medium Priority Issues:**

- Using `replace()` when `update()` is intended -- `replace` deletes all properties not included in the call; `update` merges
- Not checking `insertMany` response for errors -- partial failures are silent; check `response.hasErrors` and `response.errors`
- Passing `alpha: 1.0` to hybrid search -- equivalent to pure vector search; use `nearText` instead for clarity
- Not specifying `targetVector` with named vectors -- queries default to the first vector, which may not be the intended one

**Common Mistakes:**

- Using v2 class-based API (`client.schema.classCreator()`) with v3 client -- the API is completely different; v3 uses `client.collections.create()`
- Forgetting to pass API key headers for vectorizer modules -- `X-OpenAI-Api-Key`, `X-Cohere-Api-Key` etc. must be in connection headers
- Using `connectToWCS()` (deprecated) instead of `connectToWeaviateCloud()`
- Adding a property after data import without reindexing -- pre-existing objects won't have that property indexed

**Gotchas & Edge Cases:**

- `insertMany` uses server-side batching but the TS client does NOT have a streaming batch API -- for very large imports (100K+), chunk into batches of 100-1000 objects
- `Filters.and()` and `Filters.or()` take a flat list of filter conditions, NOT nested arrays -- `Filters.and(a, b, c)` not `Filters.and([a, b, c])`
- `fetchObjects()` without `limit` returns 25 objects by default (server-side default), not all objects
- Property names in Weaviate must start with a lowercase letter -- the client silently lowercases the first character
- `distance` metadata varies by vector distance metric -- cosine distance range [0, 2], not [0, 1]
- `deleteMany` has a server-side maximum of 10,000 objects per call (configurable via `QUERY_MAXIMUM_RESULTS`)
- Weaviate auto-detects property types on first insert if not defined in the schema -- this can cause type mismatches if first object has atypical data
- `fetchObjectById` returns `null` for non-existent IDs, not an empty object -- always check for null before accessing properties
- Cross-references in multi-tenant collections can only reference objects in the same tenant or in non-multi-tenant collections

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `client.close()` when done with the Weaviate client -- it maintains persistent gRPC connections that will leak if not closed)**

**(You MUST configure vectorizers at the COLLECTION level during `client.collections.create()` -- you cannot add a vectorizer after creation, only add new named vectors)**

**(You MUST use a SEPARATE `client.collections.use()` call with `.withTenant()` for multi-tenant queries -- queries without tenant context on multi-tenant collections will fail)**

**(You MUST increase query timeout to 60+ seconds when using `generate.*` (RAG) submodule -- generative model calls are slow and the default timeout causes failures)**

**Failure to follow these rules will cause connection leaks, missing vectorization, multi-tenant query failures, and RAG timeouts.**

</critical_reminders>
