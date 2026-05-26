---
name: api-search-meilisearch
description: Meilisearch search engine patterns -- client setup, indexing, search, filtering, facets, geo search, multi-tenancy, task management
---

# Meilisearch Patterns

> **Quick Guide:** Use `meilisearch` (v0.56+) as the TypeScript client for Meilisearch v1.x. All write operations (document adds, setting changes, index creation) are **asynchronous** -- they return an `EnqueuedTaskPromise` and are processed in a background queue. You MUST configure `filterableAttributes` and `sortableAttributes` on the index **before** using filter/sort in search queries -- this triggers a full re-index. Use `client.index("name")` for a lazy reference (no network call) vs `client.getIndex("name")` which fetches from server. Use `.waitTask()` on `EnqueuedTaskPromise` only in scripts/seeds/tests -- never in request handlers.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST configure `filterableAttributes` on the index BEFORE using `filter` in search queries -- filters silently return no results if the attribute is not in `filterableAttributes`)**

**(You MUST configure `sortableAttributes` on the index BEFORE using `sort` in search queries -- sort on unconfigured attributes is silently ignored)**

**(You MUST NOT call `.waitTask()` in production request handlers -- it blocks the event loop polling Meilisearch until the task completes; use it only in scripts, seeds, and tests)**

**(You MUST set the primary key explicitly when documents lack an `id` field -- Meilisearch auto-infers primary key only on first document add, and wrong inference causes indexing failures on subsequent batches)**

</critical_requirements>

---

## Examples

- [Core Patterns](examples/core.md) -- Client setup, document operations, search basics, task management, TypeScript integration
- [Filtering & Facets](examples/filtering.md) -- Filter syntax, faceted search, geo search, sortable attributes
- [Index Settings](examples/settings.md) -- Ranking rules, typo tolerance, synonyms, stop words, searchable attributes, pagination
- [Security & Multi-Tenancy](examples/security.md) -- API keys, tenant tokens, search rules, multi-tenant patterns

**Additional resources:**

- [reference.md](reference.md) -- Search parameter cheat sheet, settings defaults, decision frameworks, anti-patterns

---

**Auto-detection:** Meilisearch, meilisearch, MeiliSearch, meilisearch-js, client.index, addDocuments, updateDocuments, multiSearch, filterableAttributes, sortableAttributes, searchableAttributes, rankingRules, typoTolerance, tenant token, generateTenantToken, EnqueuedTaskPromise, waitTask, facets, \_geoRadius, \_geoBoundingBox, \_geoPoint, instantsearch

**When to use:**

- Adding full-text search to an application (product search, content search, autocomplete)
- Implementing faceted navigation (category filters, price ranges, attribute counts)
- Building geo-aware search (find nearby, sort by distance)
- Multi-tenant search where tenants share an index but see only their documents
- Search across multiple indexes simultaneously (multi-search, federated search)
- Real-time document indexing with typo-tolerant instant search

**Key patterns covered:**

- Client initialization and connection management
- Document CRUD operations with async task handling
- Search with filtering, sorting, facets, and highlighting
- Geo search with `_geoRadius`, `_geoBoundingBox`, and distance sorting
- Multi-search and federated search across indexes
- Index settings configuration (ranking rules, typo tolerance, synonyms, stop words)
- Tenant tokens for multi-tenant access control
- TypeScript generics for typed search results

**When NOT to use:**

- Full-text search on a relational database (use PostgreSQL full-text search for simple cases)
- Log aggregation or analytics queries (use Elasticsearch/OpenSearch)
- Vector-only semantic search without keyword component (use a dedicated vector database)
- Searching fewer than ~1,000 documents (client-side filtering is simpler)

---

<philosophy>

## Philosophy

Meilisearch is a **search engine**, not a database. It indexes documents for fast retrieval but is not the source of truth. The core principles:

1. **Async everything** -- All write operations (documents, settings, index management) are queued and processed asynchronously. The API returns a task ID immediately. Design your application to not depend on instant indexing.
2. **Configure before search** -- Filterable attributes, sortable attributes, and searchable attributes must be configured BEFORE they can be used in search queries. This triggers a re-index of all documents.
3. **Typo tolerance by default** -- Meilisearch handles typos out of the box. Tune `typoTolerance` settings to disable it for specific fields (product codes, serial numbers) rather than trying to implement exact matching manually.
4. **Primary key matters** -- Every document needs a unique primary key. Meilisearch auto-infers it from the first document, but explicit is better than implicit. Set it on index creation.
5. **Search, don't query** -- Meilisearch is optimized for human search queries (typo-tolerant, prefix matching, ranking). It is not a SQL replacement. Use filters for structured queries, search for natural language.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize the client with host and API key. Use `client.index()` for a lazy local reference (no network call) -- prefer this over `client.getIndex()` which hits the server.

```typescript
// Good Example -- Typed client setup
import { Meilisearch } from "meilisearch";

function createSearchClient(): Meilisearch {
  const host = process.env.MEILISEARCH_URL;
  const apiKey = process.env.MEILISEARCH_API_KEY;
  if (!host) {
    throw new Error("MEILISEARCH_URL environment variable is required");
  }

  return new Meilisearch({ host, apiKey });
}

export { createSearchClient };
```

**Why good:** Environment variable validation, named export, apiKey is optional (Meilisearch allows unauthenticated access in development)

```typescript
// Bad Example -- Hardcoded credentials
import { Meilisearch } from "meilisearch";
const client = new Meilisearch({
  host: "http://localhost:7700",
  apiKey: "masterKey123",
});
```

**Why bad:** Hardcoded host and API key leak in version control, master key exposed (use scoped API keys in production)

See [examples/core.md](examples/core.md) for health checks, AbortController usage, and custom request configuration.

---

### Pattern 2: Document Indexing (Async)

All document operations return `EnqueuedTaskPromise`. The documents are NOT searchable immediately -- they enter a task queue.

```typescript
// Good Example -- Add documents with explicit primary key
interface Product {
  productId: string;
  name: string;
  description: string;
  price: number;
  categories: string[];
}

const index = client.index<Product>("products");

// First add: set primary key explicitly
const task = await index.addDocuments(products, { primaryKey: "productId" });
// task.taskUid: number -- use this to track progress
```

**Why good:** Explicit primary key prevents auto-inference issues, TypeScript generic provides type safety on document shape

```typescript
// Bad Example -- Relying on auto-inference
const index = client.index("products");
await index.addDocuments(products); // No primary key specified
// If first document has both 'id' and 'productId', Meilisearch guesses wrong
```

**Why bad:** Meilisearch infers primary key from the first document -- if it guesses wrong, all subsequent adds may fail with primary key conflicts

See [examples/core.md](examples/core.md) for update, delete, batching, and task management patterns.

---

### Pattern 3: Search with Filters

Filters require `filterableAttributes` to be configured first. Filter syntax uses SQL-like operators with `AND`/`OR`/`NOT`.

```typescript
// Good Example -- Search with filter and sort
const MIN_PRICE = 10;
const MAX_PRICE = 100;

const results = await index.search("wireless headphones", {
  filter: `price >= ${MIN_PRICE} AND price <= ${MAX_PRICE} AND categories = "electronics"`,
  sort: ["price:asc"],
  limit: 20,
});
// results.hits: Product[], results.estimatedTotalHits: number
```

**Why good:** Named constants for filter values, combined text search with structured filtering, explicit limit

```typescript
// Bad Example -- Filtering without configuring filterableAttributes
const index = client.index("products");
// MISSING: await index.updateFilterableAttributes(["price", "categories"])
const results = await index.search("headphones", {
  filter: "price < 50", // Returns 0 results -- silently fails!
});
```

**Why bad:** Filters return empty results without error when the attribute is not in `filterableAttributes` -- this is the most common Meilisearch gotcha

See [examples/filtering.md](examples/filtering.md) for faceted search, geo filters, and advanced filter syntax.

---

### Pattern 4: Multi-Search

Search across multiple indexes in a single request. Federated search merges results into a unified list.

```typescript
// Good Example -- Multi-search across indexes
const results = await client.multiSearch({
  queries: [
    { indexUid: "products", q: "laptop", limit: 5 },
    { indexUid: "articles", q: "laptop review", limit: 5 },
  ],
});
// results.results[0].hits -- products
// results.results[1].hits -- articles

// Federated search -- merged results
const federated = await client.multiSearch({
  federation: {},
  queries: [
    { indexUid: "products", q: "laptop" },
    { indexUid: "articles", q: "laptop" },
  ],
});
// federated.hits -- single merged list sorted by relevance
```

**Why good:** Single network request for multiple index searches, federated search provides unified ranking across indexes

See [examples/core.md](examples/core.md) for federated search with query weighting.

---

### Pattern 5: Task Management

Write operations are async. Use task UIDs to track progress. Use `.waitTask()` only in scripts and tests.

```typescript
// Good Example -- Task tracking in a seed script
const task = await index.addDocuments(products, {
  primaryKey: "productId",
});

// In scripts/seeds: wait for completion
const completed = await task.waitTask();
if (completed.status === "failed") {
  throw new Error(`Indexing failed: ${completed.error?.message}`);
}
console.log(`Indexed ${completed.details?.indexedDocuments} documents`);
```

**Why good:** `.waitTask()` used in seed script (not request handler), error status checked, task details inspected

```typescript
// Bad Example -- Waiting in a request handler
app.post("/products", async (req, res) => {
  const task = await index.addDocuments([req.body]);
  await task.waitTask(); // BLOCKS the request until Meilisearch processes the task!
  res.json({ success: true });
});
```

**Why bad:** `.waitTask()` polls Meilisearch repeatedly, blocking the request handler -- tasks may take seconds or minutes depending on queue depth

See [examples/core.md](examples/core.md) for batch task management and task status polling.

---

### Pattern 6: Index Settings Configuration

Settings changes trigger a full re-index. Configure settings BEFORE adding documents to avoid re-indexing.

```typescript
// Good Example -- Configure index before adding documents
const index = client.index("products");

// Step 1: Configure settings (triggers re-index)
await index
  .updateSettings({
    filterableAttributes: ["price", "categories", "brand", "inStock"],
    sortableAttributes: ["price", "createdAt"],
    searchableAttributes: ["name", "description", "brand"],
    rankingRules: [
      "words",
      "typo",
      "proximity",
      "attribute",
      "sort",
      "exactness",
      "price:asc",
    ],
    typoTolerance: {
      disableOnAttributes: ["sku", "barcode"],
    },
    synonyms: {
      phone: ["smartphone", "mobile"],
      laptop: ["notebook"],
    },
  })
  .waitTask(); // OK in setup script

// Step 2: Add documents (indexes with correct settings)
await index.addDocuments(products, { primaryKey: "productId" });
```

**Why good:** Settings configured before documents avoids double re-index, typo tolerance disabled on exact-match fields, synonyms defined for common aliases

See [examples/settings.md](examples/settings.md) for all settings options, stop words, and pagination configuration.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Search Approach?

```
What kind of search do I need?
-- Single index, text query? -> index.search(query, options)
-- Multiple indexes, separate results? -> client.multiSearch({ queries })
-- Multiple indexes, merged results? -> client.multiSearch({ federation: {}, queries })
-- Browse/filter without text? -> index.search("", { filter, sort })  (placeholder search)
```

### Filter vs Search?

```
How should users find data?
-- Natural language, typo-tolerant? -> Use the `q` parameter (search)
-- Exact attribute matching? -> Use `filter` parameter
-- Both? -> Combine: search("query", { filter: "category = 'X'" })
-- Browsing without a query? -> Placeholder search: search("", { filter, sort })
```

### Pagination Strategy?

```
How should I paginate results?
-- Infinite scroll / load more? -> Use offset + limit (default)
-- Page numbers (page 1, 2, 3)? -> Use page + hitsPerPage
-- NOTE: Default maxTotalHits is 1000 -- increase in pagination settings if needed
```

### Task Management Strategy?

```
How should I handle async operations?
-- Seed script / migration? -> .waitTask() is fine
-- Test setup? -> .waitTask() to ensure data is ready
-- API request handler? -> Fire-and-forget, return task UID to client
-- Need confirmation? -> Return taskUid, let client poll GET /tasks/:uid
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Filtering or sorting without first configuring `filterableAttributes` / `sortableAttributes` -- filters silently return empty results, sorts are silently ignored
- Using `.waitTask()` in production request handlers -- blocks the event loop, causes request timeouts under load
- Using the master key in client-side code -- exposes full admin access; use search-only API keys or tenant tokens
- Not setting the primary key explicitly -- Meilisearch auto-infers from the first document and may pick the wrong field, causing all subsequent indexing to fail

**Medium Priority Issues:**

- Configuring settings AFTER adding documents -- triggers a full re-index of all documents, which can take minutes on large datasets
- Exceeding the default `maxTotalHits: 1000` pagination limit -- search silently caps results at 1000; increase via `pagination.maxTotalHits` in settings if you need deeper pagination
- Using `AND`/`OR` in filters without parentheses -- `AND` has higher precedence than `OR`, leading to unexpected filter results
- Not handling task failures -- failed tasks leave the index unchanged but the error is only visible by checking the task status

**Gotchas & Edge Cases:**

- `filterableAttributes` must include `_geo` for geo search -- adding documents with `_geo` fields is not enough, the attribute must be explicitly listed
- `client.index("name")` does NOT create the index or verify it exists -- it returns a local reference; use `client.createIndex("name")` to actually create it
- Empty string search (`search("")`) is a valid "placeholder search" -- returns all documents matching filters, useful for browsing/faceted navigation
- Meilisearch task queue has a ~10 GiB limit -- if the queue fills up, new write operations fail with `no_space_left_on_device`; delete finished tasks periodically
- Synonyms do NOT apply to filters -- filtering by "phone" will not match documents with "smartphone" even if they are configured as synonyms
- `_geo` field format is strict: must be `{ lat: number, lng: number }` -- `longitude` instead of `lng` causes `invalid_document_geo_field` errors
- Setting changes (filterableAttributes, etc.) queue as tasks too -- they are not instant; wait for the task to complete before relying on the new settings
- `hitsPerPage` and `page` parameters override `offset`/`limit` -- do not mix both pagination styles in the same query
- Default `maxTotalHits` is 1000 -- even with offset-based pagination, you cannot access documents beyond position 1000 without increasing this setting

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST configure `filterableAttributes` on the index BEFORE using `filter` in search queries -- filters silently return no results if the attribute is not in `filterableAttributes`)**

**(You MUST configure `sortableAttributes` on the index BEFORE using `sort` in search queries -- sort on unconfigured attributes is silently ignored)**

**(You MUST NOT call `.waitTask()` in production request handlers -- it blocks the event loop polling Meilisearch until the task completes; use it only in scripts, seeds, and tests)**

**(You MUST set the primary key explicitly when documents lack an `id` field -- Meilisearch auto-infers primary key only on first document add, and wrong inference causes indexing failures on subsequent batches)**

**Failure to follow these rules will cause silent search failures, request timeouts, and indexing errors.**

</critical_reminders>
