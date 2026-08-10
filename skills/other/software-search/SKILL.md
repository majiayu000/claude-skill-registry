---
name: software-search
description: "Designs application search systems. Use when choosing engines, indexing, relevance tuning, facets, autocomplete, or search analytics."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Search Engineering

Build search features that return the right results, fast.

## Quick Reference

| Need | Recommended Options |
|---|---|
| Full-text search (managed) | Algolia (fastest DX), Elasticsearch/OpenSearch (most flexible) |
| Full-text search (lightweight) | Typesense (simple), Meilisearch (developer-friendly) |
| Full-text search (embedded) | SQLite FTS5, Tantivy (Rust), Lunr.js (client-side) |
| PostgreSQL built-in | pg_trgm + tsvector/tsquery (good enough for many apps) |
| Vector search | pgvector, Pinecone, Weaviate, Qdrant |
| Hybrid search | Keyword + vector, reciprocal rank fusion |
| Autocomplete | Prefix matching, search-as-you-type index, debounced queries |
| Faceted search | Aggregation queries, filter counts, hierarchical facets |
| Search analytics | Click-through rate, zero-result queries, query refinement patterns |
| Search UI | InstantSearch.js (Algolia), SearchKit, custom |

## When to Use This Skill

- Choosing a search engine or evaluating whether PostgreSQL search is sufficient
- Building full-text search, autocomplete, or faceted filtering
- Designing an indexing pipeline from source data to search index
- Tuning relevance scoring, synonyms, or ranking signals
- Implementing search analytics to measure and improve quality
- Debugging search quality issues (missing results, poor ranking, slow queries)

## When NOT to Use This Skill

- **RAG and retrieval for LLM context augmentation** → [ai-rag](../ai-rag/SKILL.md)
- **Database query optimization (SQL performance)** → [data-sql-optimization](../data-sql-optimization/SKILL.md)
- **Marketing SEO and search visibility** → `marketing-seo`
- **Product analytics and event tracking** → `marketing-product-analytics`
- **Backend API design and architecture** → [software-backend](../software-backend/SKILL.md)

## Workflow

1. Confirm the search problem: engine choice, indexing pipeline, relevance, autocomplete, or analytics.
2. Route RAG, database tuning, SEO, or API-architecture questions to the adjacent skill when product search is not the real problem.
3. Choose PostgreSQL, a dedicated search engine, vector search, or hybrid search from the decision tree.
4. Apply the relevant guidance for indexing, ranking, facets, autocomplete, and measurement.
5. Verify current engine capabilities and hosted-service behavior through the navigation references before final recommendations.

## ASCII Flow

```text
Search task
  -> Define corpus, query intent, filters, and freshness needs
  -> Choose database search, dedicated engine, vector, or hybrid retrieval
  -> Design indexing, schema, ranking, synonyms, and hydration strategy
  -> Add relevance evals, analytics, and regression checks
  -> Verify engine-specific behavior and limits
  -> Report quality tradeoffs and rollout plan
```

## Decision Tree

```text
Which search engine?
├── Small dataset (<100K docs), PostgreSQL already in stack?
│   └── YES → PostgreSQL full-text search (pg_trgm + tsvector)
│       └── Outgrowing it? (facets, typo tolerance, sub-50ms at scale)
│           └── YES → Move to dedicated search engine (below)
├── Need instant search-as-you-type with zero ops?
│   └── YES → Algolia (managed, fastest DX)
├── Need full control, complex queries, large scale?
│   └── YES → Elasticsearch or OpenSearch
├── Developer-friendly, simpler than Elastic?
│   └── YES → Typesense or Meilisearch
├── Client-side search (static site, small dataset)?
│   └── YES → Lunr.js, Pagefind, or FlexSearch
├── Need semantic/meaning-based search?
│   └── YES → Vector search (pgvector, Pinecone, Qdrant, Weaviate)
└── Need both keyword AND semantic?
    └── YES → Hybrid search (keyword + vector + reciprocal rank fusion)
```

## Engine Capability Matrix

| Engine | Typo tolerance | Facets | Geo | Vector | Self-host | Managed |
|--------|---------------|--------|-----|--------|-----------|---------|
| PostgreSQL (tsvector + pg_trgm) | Partial (pg_trgm) | Manual aggregation | PostGIS | pgvector | Yes | RDS/Supabase |
| Algolia | Built-in | Native | Native | Yes — native hybrid (NeuralSearch merges keyword + vector per query) | No | Yes |
| Elasticsearch / OpenSearch | Built-in | Native | Native | Dense vector, native RRF retriever/fusion | Yes | AWS/Elastic |
| Typesense | Built-in | Native | Native | Yes, built-in (rank-fusion hybrid; verify current default fusion weights) | Yes | Typesense Cloud |
| Meilisearch | Built-in | Native | Limited | Yes, built-in hybrid (BM25 + embeddings) since v1.6+ | Yes | Meilisearch Cloud |
| Lunr.js / Pagefind | No | No | No | No | Client-side | N/A |
| Pinecone / Qdrant / Weaviate | N/A (Qdrant/Weaviate: native BM25 sparse-vector support) | Filter | No | Yes | Qdrant/Weaviate yes | Yes |

Capability availability shifts release to release (Algolia added native vector fusion; Qdrant and Weaviate added native BM25). Reverify each engine's `current` docs before finalizing a recommendation — do not rely on this table's exact wording beyond "capability exists in some form."

## PostgreSQL Search (Start Here)

For most applications, PostgreSQL is good enough. Evaluate dedicated engines only when you hit real limits.

**tsvector/tsquery** — full-text search with language-aware stemming, ranking, and phrase matching. Create a `tsvector` column, build a GIN index, query with `tsquery`. Supports `ts_rank` for relevance scoring and `ts_headline` for result highlighting.

**pg_trgm** — trigram-based fuzzy matching. Handles typos and partial matches. Create a GIN index with `gin_trgm_ops`. Use `similarity()` or `word_similarity()` for ranking. Combine with `tsvector` for both exact and fuzzy results.

**GIN indexes** — generalized inverted indexes that make full-text and trigram queries fast. Essential for any non-trivial search workload in PostgreSQL.

**When to outgrow PostgreSQL search:**
- You need faceted search with filter counts (aggregation queries are expensive in PG)
- Sub-50ms latency requirements at scale (>1M docs with complex queries)
- Complex relevance tuning with field boosting, custom scoring, decay functions
- Search-as-you-type with typo tolerance and instant feedback
- You need synonyms, stemming, and language analysis beyond what `tsvector` provides

## Search Engine Architecture

**Indexing pipeline**: Extract data from source (database, CMS, API) → transform into search documents (flatten, denormalize, enrich) → push to search index. Keep the pipeline idempotent — re-running should produce the same index state.

**Index schema design**: Define fields, types, and which fields are searchable vs. filterable vs. stored-only. Denormalize aggressively — search indexes are not relational databases. Include all data needed for display in search results to avoid hydration round-trips.

**Analyzers and tokenizers**: Control how text is broken into searchable tokens. Standard analyzer handles most Western languages. Configure language-specific analyzers for stemming. Add custom analyzers for domain-specific tokenization (email addresses, part numbers, code identifiers).

**Synonyms and stop words**: Maintain a synonym list for domain terms (e.g., "laptop" = "notebook"). Remove low-value stop words from indexing but keep them in phrase queries. Synonym expansion happens at index time or query time — query-time is more flexible, index-time is faster.

**Index lifecycle**: Never mutate a live index schema in production. Use index aliases: build new index → swap alias → delete old index. This gives zero-downtime reindexing. For incremental updates, use upsert operations keyed on document ID.

## Relevance Tuning

**BM25 scoring** — the default ranking algorithm in most search engines. Balances term frequency (how often the term appears in a document) against inverse document frequency (how rare the term is across all documents). Handles document length normalization automatically.

**Field boosting** — weight fields differently. Title matches are typically 3-5x more important than body matches. Boost exact matches over partial matches. Common hierarchy: title > headings > tags > description > body.

**Custom ranking signals** — layer business logic onto relevance scores. Common signals: popularity (views, purchases), recency (newer content ranked higher via decay function), editorial boost (curated/featured content), user behavior (personalized ranking from click history).

**Query understanding** — improve what the user meant, not just what they typed. Spell correction (did-you-mean). Intent detection (navigational vs. informational queries). Query expansion (add related terms). Query relaxation (broaden if too few results).

**Relevance tuning loop** — ship a baseline, measure with analytics, tune iteratively, repeat. Each iteration should move a measurable metric (zero-result rate, MRR, CTR at position 1) not just "feel better."

## Vector Search API Pattern

Use this pattern when semantic search is a product feature, not just an LLM
context retriever.

**Request contract**:

- `query`: required non-empty string, with length and character-class limits
- `limit`: bounded integer, default 10, hard max 50
- `offset` or cursor: optional pagination, only if the engine supports stable
  ordering
- `filters`: allowlisted fields only; never pass arbitrary filter JSON through
  to the search engine

**Response contract**:

- stable result ID and display fields
- relevance score or rank, clearly marked as diagnostic when the score is not
  user-meaningful
- matched source metadata needed for display
- applied query preprocessing version

**Operational rules**:

- Keep the endpoint stateless and idempotent even if implemented as `POST`.
- Validate and sanitize input before embedding or query construction.
- Rate-limit by authenticated actor or API key; IP-only limits are weak for
  logged-in products.
- Add structured errors for invalid input, unavailable embedder, search timeout,
  and backend failure.
- Log raw query, cleaned query, retrieval mode, top result IDs, latency, and
  result count.
- Start with exact or small-corpus search to debug embeddings, then move to an
  index once quality is proven.

### Ranking Signal Mix

For product search, semantic similarity is usually one leg of ranking, not the
whole ranker. Typical final scoring candidates:

- vector or hybrid relevance
- recency decay
- popularity or engagement
- editorial boost or business rule
- personalization, only when user consent and isolation rules are clear

Do not hand-pick weights from intuition. Calibrate weights against judged
queries and analytics slices. If scores come from different systems and cannot
be normalized safely, prefer rank-based fusion such as RRF before applying
business boosts.

### Vector Memory Sizing (Worked Example)

Estimate before choosing a vector index type — memory, not disk, is usually the
binding constraint for in-memory ANN indexes (HNSW).

**Formula**: `raw_bytes = num_vectors × dims × bytes_per_value`. Add HNSW graph
overhead on top (graph edges + metadata); treat 20-50% of raw size as a
starting planning range and verify the actual multiplier against the specific
engine's current documentation before sizing hardware.

**Worked derivation** — 1,000,000 documents, 768-dimension embeddings (a common
mid-size embedding model output), three storage precisions:

| Precision | Bytes/dim | Raw size = 1,000,000 × 768 × bytes/dim | Raw size (GiB) |
|---|---|---|---|
| float32 (full precision) | 4 | 3,072,000,000 bytes | ≈ 2.86 GiB |
| halfvec / float16 | 2 | 1,536,000,000 bytes | ≈ 1.43 GiB |
| binary quantized (1 bit) | 0.125 | 96,000,000 bytes | ≈ 0.09 GiB |

Adding a 30% HNSW graph overhead to the float32 case: `2.86 GiB × 1.3 ≈ 3.72 GiB`
of working memory for one million 768-dim vectors — before the rest of the
document payload (text, metadata) is counted.

**How to use this**: re-run the same formula with your own `num_vectors` and
`dims` — never scale a neighboring number instead of recomputing from your
corpus size and embedding dimension. Binary and scalar quantization trade
recall for memory; validate the recall drop against your judged-query set
before committing to a lower precision in production. Confirm current
quantization support (halfvec, binary, product quantization) in the specific
engine's docs — pgvector, Elasticsearch, OpenSearch, and Qdrant each expose
different quantization options and defaults that change across releases.

## Common Misdiagnoses

Symptoms that get the wrong fix more often than the right one:

- **"Search is slow" → jumping straight to a dedicated engine.** Check for a
  missing GIN index, an N+1 hydration query per result, or an unbounded
  `LIKE '%term%'` scan first. Many "we need Elasticsearch" tickets are fixed by
  an index that was never created.
- **"Relevance is bad" → adding vector search.** Verify analyzers, stemming,
  and field boosting are configured correctly before assuming lexical search
  is semantically incapable. A missing stemmer or unboosted title field often
  looks identical to "BM25 can't understand meaning."
- **"Zero-result spike" → assumed content gap.** Check first whether a recent
  synonym, analyzer, or tokenizer change caused a regression. Content gaps and
  indexing regressions produce the same symptom but need opposite fixes.
- **"Hybrid search will fix our recall" → skipping the judged-query set.**
  Hybrid retrieval reduces but does not eliminate poor recall if the underlying
  embedding model was never validated against the domain's vocabulary.
- **"Facets are slow" → blaming the engine instead of cardinality.** Faceting
  on a free-text or unbounded-cardinality field is usually the actual cause,
  not an engine limitation.
- **"Autocomplete is laggy" → tuning the main index.** Autocomplete usually
  needs its own latency budget and often its own lightweight index or cache;
  it should not share load or latency budget with full search.

## Faceted Search and Filtering

**Aggregation queries** — compute filter counts alongside search results. Show users how many results match each filter value before they click. This is where PostgreSQL struggles and dedicated engines shine.

**Hierarchical facets** — nested categories (e.g., Electronics > Phones > Smartphones). Implement with path-based tokens or nested aggregations. Allow drill-down and drill-up navigation.

**Range facets** — numeric or date ranges (price $0-50, $50-100; last 24 hours, last week). Pre-define meaningful ranges or use dynamic bucketing.

**Multi-select vs. single-select** — multi-select filters use OR within a facet and AND across facets. Single-select uses exclusive selection. Multi-select requires disjunctive faceting (count all values, not just those matching current filter).

**Performance** — apply filters before scoring when possible (filter context vs. query context in Elasticsearch). Cache frequently used filter combinations. Pre-compute facet counts for high-traffic pages.

## Autocomplete and Search-as-You-Type

**Prefix matching** — match documents where a field starts with the typed characters. Fast but limited to prefix positions.

**Edge n-gram indexing** — at index time, generate token prefixes ("search" → "s", "se", "sea", "sear", "searc", "search"). Converts prefix queries into exact match lookups, which are faster.

**Completion suggesters** — dedicated data structures optimized for prefix completion. Elasticsearch has a built-in completion suggester. Algolia and Typesense handle this natively.

**Client-side debouncing** — wait 150-300ms after the user stops typing before sending the query. Reduces server load and prevents UI flicker. 200ms is a good default.

**Highlight matching terms** — show users why a result matched by bolding the matching portion. Most search engines provide highlighting out of the box.

**Zero-state and popular suggestions** — before the user types, show trending queries, recent searches, or popular categories. Pre-compute these from search analytics data.

## Search Analytics

**What to track**: every query (with timestamp, user ID, session), every click (which result, position clicked), conversions (did the user complete their goal after clicking), zero-result queries, query refinements (user searched again after seeing results).

**Zero-result queries** — the most actionable metric. These reveal content gaps (you don't have what users want) or search quality issues (you have it but search can't find it). Review weekly and take action: add content, add synonyms, or fix indexing.

**Click position** — which position users click in search results. If users consistently click result #4 instead of #1, your relevance ranking is wrong. Use mean reciprocal rank (MRR) as a quality metric.

**Build the feedback loop**: search query → user clicks result → click signals feed back into relevance tuning (boost documents that get clicked, demote documents that get skipped). This is the core mechanism for search quality improvement over time.

## Search Quality Evaluation

Analytics are not enough on their own. Keep a judged-query set for the product's most important search intents and re-run it whenever you change ranking, analyzers, synonyms, or business boosts.

**Minimum loop**:

- define representative queries across navigational, informational, autocomplete, and zero-result-recovery paths
- rate a small set of expected results for each query
- run the engine's native rank-evaluation API or an equivalent offline harness
- compare score deltas before and after relevance changes
- review failures manually before shipping boosts or synonym changes

Use click data to find candidates for the judged set, but do not let click-through alone define quality. Position bias, sparse traffic, and merchandising effects can hide bad ranking decisions.

## Common Anti-Patterns

- **`LIKE '%query%'` at scale** — full table scan, no index usage, gets slower linearly with data growth. Use proper full-text search instead.
- **No analyzers configured** — raw text matching misses stemming, case folding, and accent normalization. Users searching "running" won't find "run."
- **Ignoring zero-result queries** — the cheapest way to improve search quality, and most teams never look at them.
- **Re-indexing full dataset on every change** — use incremental updates (upsert by document ID) for individual changes and reserve full reindex for schema changes.
- **Coupling search schema to database schema** — search documents should be denormalized and optimized for query patterns, not mirror your relational schema.
- **Not measuring search quality** — if you don't track click-through rate, zero-result rate, and query refinement rate, you cannot improve search. Instrument from day one.
- **Over-engineering early** — starting with Elasticsearch when PostgreSQL `tsvector` would handle the workload for the next two years.

## Known Traps

- Semantic or vector retrieval added as a replacement for lexical recall instead of a complement to it.
- Faceting on fields with unbounded cardinality, leading to expensive aggregations and unusable filter UX.
- Autocomplete implemented against the main search index with no latency budget, flooding the cluster on every keystroke.
- Synonym expansion shipped without governance, creating silent relevance regressions and impossible-to-debug ranking changes.
- Index freshness assumed to be real-time when ingestion pipelines are actually batched or eventually consistent.
- Relevance tuning done from intuition alone instead of using click data, zero-result analysis, and query reformulation behavior.

## Verification Gate

Before calling a search design or implementation ready:

- [ ] Engine matches current corpus size, query shape, and latency budget
- [ ] Latency budgets defined separately for full search (≤200ms p95) and autocomplete (≤100ms p95)
- [ ] Index freshness mechanism documented and measured (real-time, near-real-time, or scheduled batch)
- [ ] Zero-result rate instrumented and baseline established (target below 5% for mature catalog)
- [ ] Click position and refinement rate tracked from day one
- [ ] Judged-query evaluation covers navigational, informational, autocomplete, and zero-result-recovery paths
- [ ] Representative queries tested — not only happy-path keyword matches
- [ ] Synonym and analyzer changes logged with rollback plan

## Scenarios

Recipes keyed to common search implementation moments. Each lists the shortest path using patterns above.

### S1 — Hybrid BM25 + vector with RRF for a product catalog

1. Index each product document in both a keyword (BM25) index and a vector index (pgvector, Qdrant, or Weaviate).
2. At query time, run the keyword search and the vector search in parallel; collect both ranked result lists.
3. Apply Reciprocal Rank Fusion: score each document as `Σ 1/(k + rank)` across both lists, where `k=60` is a safe default.
4. Re-rank the merged list by RRF score; apply any business boosts (popularity, recency) on top.
5. Tune the relative weight of keyword vs. vector by evaluating against a judged-query set, not by intuition.
6. Monitor zero-result rate; hybrid rarely returns zero, but confirm semantic recall improves tail queries.

### S2 — Zero-downtime reindex via index alias swap

1. Create a new index with the updated schema (e.g., `products_v2`); leave the live alias pointing to `products_v1`.
2. Run the full reindex pipeline against `products_v2`; writes to `products_v1` continue serving production traffic.
3. Verify document count, spot-check relevance on representative queries against `products_v2` before swap.
4. Atomically update the alias: remove `products_v1`, add `products_v2` in a single alias-update call.
5. Confirm production traffic is now routing to `products_v2`; monitor error rate and latency for 10 minutes.
6. Delete `products_v1` only after the monitoring window is clean; keep it for one more deploy cycle if in doubt.

### S3 — Autocomplete debounce + per-user prefix prefetch

1. Add 200ms client-side debounce before firing autocomplete queries; cancel in-flight requests on each keystroke.
2. On focus of the search input, prefetch popular completions for the empty-string state from a cached endpoint.
3. After the user's first two characters, shift to a live prefix query against a completion suggester or edge-ngram index.
4. Return a maximum of 5–8 suggestions per query; more options slow perceived response and increase cognitive load.
5. Log every prefix query with the user session; feed click data back into the popular-completion cache weekly.
6. Set a strict 100ms server-side latency budget for autocomplete; use a dedicated index or cache layer to meet it.

### S4 — Faceted drill-down with cardinality limits

1. Define facet fields explicitly in the index schema; do not facet on free-text or high-cardinality fields.
2. Cap returned facet values per field (e.g., top 20 by count); expose a "show more" call for long-tail values.
3. Use filter context (not query context) for active facet filters so they do not affect relevance scores.
4. Implement disjunctive faceting for multi-select: recompute counts for each facet excluding its own active filter.
5. Test aggregation query latency at expected data scale; move expensive facets to a pre-computed cache if needed.
6. Monitor facet click patterns in search analytics; remove facets that are never interacted with.

### S5 — Zero-result rate dashboard + query rewrite trigger

1. Log every search query with its result count; compute the zero-result rate as a daily metric.
2. Build a dashboard showing the top 50 zero-result queries ordered by frequency; review weekly.
3. For each zero-result query, classify: missing content, synonym gap, tokenization mismatch, or indexing bug.
4. Add synonyms or query expansion rules for synonym-gap cases; update the index for indexing bugs.
5. Add a query-rewrite rule (fuzzy match, spell correction, or query relaxation) for tokenization mismatches.
6. Re-evaluate the top-50 list after each change; target zero-result rate below 5% for a mature catalog.

## Navigation

### References
- [Skill Sources](data/sources.json): curated primary sources for search engineering guidance.
- [Hybrid Search and Reranking](references/hybrid-search-and-reranking.md): production pipeline — BM25 + dense vector, RRF fusion, cross-encoder reranking, pgvector in-Postgres option, engine capability classes.

### Related Skills

> **Gate before invoking any foundation below:** Each foundation has a `When to Apply` / `When to Skip` section. If your task matches a skip-condition, route to the foundation it names instead — don't pull in primitives the task doesn't need.

- [ai-rag](../ai-rag/SKILL.md) — Retrieval-augmented generation and vector retrieval for LLM context
- [data-sql-optimization](../data-sql-optimization/SKILL.md) — Database query performance and indexing
- [software-backend](../software-backend/SKILL.md) — Backend API design and service architecture
- [software-frontend](../software-frontend/SKILL.md) — Frontend implementation including search UI components
- [software-architecture-design](../software-architecture-design/SKILL.md) — System design and component boundaries
- [foundations-information-theory](../foundations-information-theory/SKILL.md) — Entropy, mutual information, and KL divergence are the math behind BM25, TF-IDF, and the relevance-tuning section

## Freshness Protocol

Search engines, managed services, and client libraries evolve frequently. Verify current information before recommending specific versions or providers.

### Trigger Conditions

- "Which search engine should I use?"
- "Is Algolia/Typesense/Meilisearch still the best option for...?"
- "What's new in Elasticsearch/OpenSearch?"
- "Should I use PostgreSQL search or a dedicated engine?"
- "How does pgvector compare to Pinecone/Weaviate?"

### How to Freshness-Check

1. Start from [data/sources.json](data/sources.json) for official documentation links.
2. Run a targeted web search for the specific engine or library.
3. Prefer official docs and release notes over blog posts for version and feature claims.
4. Prefer official engine docs for rank-evaluation APIs, relevance-debugging tools, and analyzer behavior.

### What to Report

- **Current landscape**: what is stable and widely used now
- **Emerging trends**: what is gaining traction (and why)
- **Deprecated/declining**: what is falling out of favor (and why)
- **Recommendation**: default choice + 1-2 alternatives, with trade-offs

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
