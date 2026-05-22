---
name: pgvector-search
description: Production hybrid search combining PGVector HNSW with BM25 using Reciprocal Rank Fusion. Use when implementing hybrid search, semantic + keyword retrieval, vector search optimization, metadata filtering, or choosing between HNSW and IVFFlat indexes.
context: fork
agent: database-engineer
version: 1.2.0
author: SkillForge AI Agent Hub
tags: [pgvector-0.8, hybrid-search, bm25, rrf, semantic-search, retrieval, 2026]
user-invocable: false
---

# PGVector Hybrid Search

**Production-grade semantic + keyword search using PostgreSQL**

## Overview

**Architecture:**
```
Query
  |
[Generate embedding] --> Vector Search (PGVector) --> Top 30 results
  |
[Generate ts_query]  --> Keyword Search (BM25)    --> Top 30 results
  |
[Reciprocal Rank Fusion (RRF)] --> Merge & re-rank --> Top 10 final results
```

**When to use this skill:**
- Building semantic search (RAG, knowledge bases, recommendations)
- Implementing hybrid retrieval (vector + keyword)
- Optimizing PGVector performance
- Working with large document collections (1M+ chunks)

---

## Quick Reference

### Search Type Comparison

| Aspect | Semantic (Vector) | Keyword (BM25) |
|--------|-------------------|----------------|
| **Query** | Embedding similarity | Exact word matches |
| **Strengths** | Synonyms, concepts | Exact phrases, rare terms |
| **Weaknesses** | Exact matches, technical terms | No semantic understanding |
| **Index** | HNSW (pgvector) | GIN (tsvector) |

### Index Comparison

| Metric | IVFFlat | HNSW |
|--------|---------|------|
| **Query speed** | 50ms | 3ms (17x faster) |
| **Index time** | 2 min | 20 min |
| **Best for** | < 100k vectors | 100k+ vectors |
| **Recall@10** | 0.85-0.95 | 0.95-0.99 |

**Recommendation:** Use HNSW for production (scales to millions).

### RRF Formula

```python
rrf_score = 1/(k + vector_rank) + 1/(k + keyword_rank)  # k=60 (standard)
```

---

## Database Schema

```sql
CREATE TABLE chunks (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),
    content TEXT NOT NULL,
    embedding vector(1024),  -- PGVector
    content_tsvector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', content)
    ) STORED,
    section_title TEXT,
    content_type TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_chunks_embedding ON chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX idx_chunks_content_tsvector ON chunks
    USING gin (content_tsvector);
```

---

## Hybrid Search Query (SQLAlchemy)

```python
async def hybrid_search(
    query: str,
    query_embedding: list[float],
    top_k: int = 10
) -> list[Chunk]:
    FETCH_MULTIPLIER = 3  # Fetch 30 for better RRF coverage
    K = 60  # RRF smoothing constant

    # Vector search subquery
    vector_subq = (
        select(Chunk.id,
            func.row_number().over(
                order_by=Chunk.embedding.cosine_distance(query_embedding)
            ).label("vector_rank"))
        .limit(top_k * FETCH_MULTIPLIER)
        .subquery()
    )

    # Keyword search subquery
    ts_query = func.plainto_tsquery("english", query)
    keyword_subq = (
        select(Chunk.id,
            func.row_number().over(
                order_by=func.ts_rank_cd(Chunk.content_tsvector, ts_query).desc()
            ).label("keyword_rank"))
        .where(Chunk.content_tsvector.op("@@")(ts_query))
        .limit(top_k * FETCH_MULTIPLIER)
        .subquery()
    )

    # RRF fusion with FULL OUTER JOIN
    rrf_subq = (
        select(
            func.coalesce(vector_subq.c.id, keyword_subq.c.id).label("chunk_id"),
            (func.coalesce(1.0 / (K + vector_subq.c.vector_rank), 0.0) +
             func.coalesce(1.0 / (K + keyword_subq.c.keyword_rank), 0.0)
            ).label("rrf_score"))
        .select_from(vector_subq.outerjoin(keyword_subq, ..., full=True))
        .order_by("rrf_score DESC")
        .limit(top_k)
        .subquery()
    )

    return await session.execute(
        select(Chunk).join(rrf_subq, Chunk.id == rrf_subq.c.chunk_id)
    )
```

---

## Common Patterns

### Filtered Search
```python
results = await hybrid_search(
    query="binary search",
    query_embedding=embedding,
    content_type_filter=["code_block"]
)
```

### Similarity Threshold
```python
results = await hybrid_search(query, embedding, top_k=50)
filtered = [r for r in results if (1 - r.vector_distance) >= 0.75][:10]
```

### Multi-Query Retrieval
```python
queries = ["machine learning", "ML algorithms", "neural networks"]
all_results = [await hybrid_search(q, embed(q)) for q in queries]
final = deduplicate_and_rerank(all_results)
```

---

## Performance Tips

1. **Pre-compute tsvector** - 5-10x faster than `to_tsvector()` at query time
2. **Use HNSW index** - 17x faster queries than IVFFlat
3. **3x fetch multiplier** - Better RRF coverage (30 results per search for top 10)
4. **Iterative scan** for filtered queries - Set `hnsw.iterative_scan = 'relaxed_order'`
5. **Metadata boosting** - +6% MRR with title/path matching

---

## References

### Detailed Implementation Guides

| Reference | Description | Use When |
|-----------|-------------|----------|
| [index-strategies.md](references/indexing-strategies.md) | HNSW vs IVFFlat, tuning, iterative scans | Choosing/optimizing indexes |
| [hybrid-search-rrf.md](references/hybrid-search-rrf.md) | RRF algorithm, SQL implementation, debugging | Implementing hybrid search |
| [metadata-filtering.md](references/metadata-filtering.md) | Pre/post filtering, score boosting | Improving relevance |

### External Resources
- [PGVector GitHub](https://github.com/pgvector/pgvector)
- [HNSW Index Guide](https://github.com/pgvector/pgvector#hnsw)

### Related Skills
- `ai-native-development` - Embeddings and vector concepts
- `database-schema-designer` - Schema design for vector search

---

**Version:** 1.2.0 | **Status:** Production-ready | **Updated:** pgvector 0.8.1

---

## Capability Details

### hybrid-search-rrf
**Keywords:** hybrid search, rrf, reciprocal rank fusion, vector bm25, semantic keyword search
**Solves:**
- How do I combine vector and keyword search?
- Implement hybrid retrieval with RRF
- Merge semantic and BM25 results

### semantic-search
**Keywords:** semantic search, vector similarity, embedding, nearest neighbor, cosine distance
**Solves:**
- How does semantic search work?
- When to use semantic vs keyword search
- Semantic search strengths and weaknesses

### keyword-search-bm25
**Keywords:** bm25, full-text search, tsvector, tsquery, keyword search
**Solves:**
- How does BM25 keyword search work?
- Implement PostgreSQL full-text search
- BM25 vs semantic search trade-offs

### rrf-algorithm
**Keywords:** rrf, reciprocal rank fusion, rank-based fusion, score normalization
**Solves:**
- How does Reciprocal Rank Fusion work?
- Why use rank instead of scores?
- RRF smoothing constant (k parameter)

### database-schema
**Keywords:** pgvector schema, chunk table, embedding column, tsvector, generated column
**Solves:**
- How do I design schema for hybrid search?
- Store embeddings with vector(1024)
- Pre-compute tsvector for performance

### search-query-implementation
**Keywords:** hybrid search query, sqlalchemy, vector distance, ts_rank_cd, full outer join
**Solves:**
- How do I write hybrid search SQL?
- Implement RRF in SQLAlchemy
- Use fetch multiplier for better coverage

### indexing-strategies
**Keywords:** pgvector index, hnsw, ivfflat, vector index performance, index tuning
**Solves:**
- HNSW vs IVFFlat comparison
- Optimize vector search speed
- Scale to millions of vectors

### pre-computed-tsvector
**Keywords:** tsvector, gin index, full-text index, pre-computed column, generated column
**Solves:**
- Optimize keyword search performance
- 5-10x speedup with indexed tsvector

### metadata-filtering
**Keywords:** metadata filter, faceted search, content type filter, score boosting
**Solves:**
- Filter search by metadata
- Boost results by section title
- Pre-filter by content type

### common-patterns
**Keywords:** filtered search, similarity threshold, multi-query retrieval, search patterns
**Solves:**
- Filter search by content type
- Set minimum similarity threshold
- Implement multi-query retrieval

### golden-dataset-testing
**Keywords:** golden dataset, search evaluation, pass rate, mrr, retrieval testing
**Solves:**
- Test hybrid search quality
- Evaluate search with golden queries
- Calculate pass rate and MRR metrics