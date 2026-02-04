---
name: vector-databases
description: Design vector database ingestion and retrieval pipelines (points + payloads, filtered similarity search, multi-stage hybrid retrieval, index maintenance). Use when building RAG/vector search flows or debugging retrieval quality; triggers: vector database, RAG, embeddings, hybrid search, filtered search, Qdrant, Weaviate, Chroma.
---

# Vector Databases

## Overview
Model data as vectors with payload metadata, then run similarity search with optional filters or multi-stage retrieval. Keep index maintenance in the loop so performance does not degrade as the collection changes.

## When to Use
- Use this skill when the frontmatter triggers apply; otherwise start with a simple keyword search or database query.

## Decision Tree
1. Do you need metadata filters for access control or faceting?
   - Yes: store payloads and use filtered search.
2. Do you need to blend multiple signals (dense + sparse or multi-step)?
   - Yes: use a multi-stage hybrid query plan.
3. Is search latency degrading after heavy updates or deletes?
   - Yes: run optimizer/maintenance operations.

## Workflows

### 1. Point Ingestion With Payloads
1. Generate embeddings for each document or chunk.
2. Attach a payload with filterable fields (tenant, source, timestamp).
3. Upsert points into a collection with consistent vector dimensions.

### 2. Filtered Similarity Search
1. Build a metadata filter from the request constraints.
2. Embed the query and run a similarity search scoped to the filter.
3. Return the top-k results with payload metadata for downstream ranking.

### 3. Multi-Stage Hybrid Retrieval
1. Run a first-stage query to get broad recall (dense or sparse).
2. Use a second-stage query or re-ranker to refine results.
3. Merge and normalize scores before returning the final list.

### 4. Index Maintenance Pass
1. Monitor update/delete volume and query latency.
2. Run optimizer operations (vacuum/merge/index rebuild) on a schedule.
3. Verify recall/latency before and after maintenance.

## Non-Obvious Insights
- Payload design is retrieval design: without payload fields, you cannot filter or enforce access constraints.
- Hybrid retrieval is often multi-stage; plan for intermediate candidate sets and score normalization.
- Optimizer operations are part of normal maintenance, not one-off recovery tasks.

## Evidence
- "Points are a record which consists of a vector and an optional payload." - [Qdrant](https://qdrant.tech/documentation/concepts/)
- "there are use-cases when the best search is obtained by combining multiple queries, or by performing the search in more than one stage." - [Qdrant](https://qdrant.tech/documentation/concepts/hybrid-queries/)
- "inverted index, a vector index and an object store interact with each other" - [Weaviate](https://weaviate.io/developers/weaviate/concepts)
- "Optimizer describes options to rebuild database structures for faster search. They include a vacuum, a merge, and an indexing optimizer." - [Qdrant](https://qdrant.tech/documentation/concepts/)

## Scripts
- `scripts/vector-databases_tool.py`: CLI for building points, validating dimensions, and combining hybrid scores.
- `scripts/vector-databases_tool.js`: Node.js CLI for the same tasks.

## Dependencies
- Python 3.11+ or Node 18+. Use your DB client for actual ingestion/search.

## References
- [references/README.md](references/README.md)
