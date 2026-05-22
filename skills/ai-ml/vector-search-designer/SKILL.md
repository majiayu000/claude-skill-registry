---
name: Vector Search Designer
slug: vector-search-designer
description: Design vector similarity search systems for semantic retrieval at scale
category: ai-ml
complexity: advanced
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "vector search"
  - "similarity search"
  - "vector database"
  - "semantic search design"
  - "nearest neighbor"
tags:
  - vector-search
  - similarity
  - vector-database
  - ANN
  - semantic-search
---

# Vector Search Designer

The Vector Search Designer skill helps you architect and implement vector similarity search systems that power semantic search, recommendation engines, and AI applications. It guides you through selecting the right vector database, designing index structures, optimizing query performance, and scaling to millions or billions of vectors.

Vector search has become foundational to modern AI systems, from RAG pipelines to product recommendations. This skill covers the full stack: understanding approximate nearest neighbor (ANN) algorithms, choosing between database options, tuning recall vs latency tradeoffs, and implementing production-ready search infrastructure.

Whether you are building on Pinecone, Weaviate, Qdrant, pgvector, or implementing your own solution, this skill ensures your vector search system meets your performance and accuracy requirements.

## Core Workflows

### Workflow 1: Select Vector Database
1. **Gather** requirements:
   - Scale: How many vectors?
   - Query patterns: Single vs batch, filters needed?
   - Latency requirements: Real-time vs batch?
   - Update frequency: Static vs dynamic?
   - Infrastructure: Managed vs self-hosted?
2. **Compare** options:
   | Database | Scale | Managed | Features | Best For |
   |----------|-------|---------|----------|----------|
   | Pinecone | Billion+ | Yes | Hybrid, namespaces | Production, zero-ops |
   | Weaviate | 100M+ | Both | GraphQL, modules | Multi-modal, complex queries |
   | Qdrant | 100M+ | Both | Rust perf, filtering | High performance, self-hosted |
   | Milvus | Billion+ | Both | GPU support, clustering | Large scale, ML teams |
   | pgvector | 10M | No | PostgreSQL native | Existing Postgres, small scale |
   | Chroma | 1M | No | Simple API | Prototyping, embedded |
3. **Evaluate** with your data
4. **Document** decision rationale

### Workflow 2: Design Index Architecture
1. **Choose** ANN algorithm:
   - HNSW: Best recall/speed tradeoff, memory intensive
   - IVF: Good for very large datasets, requires training
   - PQ: Compression for scale, some accuracy loss
   - Flat: Exact search, small datasets only
2. **Configure** index parameters:
   ```python
   # HNSW example configuration
   hnsw_config = {
       "M": 16,  # Connections per node (higher = better recall, more memory)
       "efConstruction": 200,  # Build-time search depth
       "efSearch": 100,  # Query-time search depth
   }

   # IVF example configuration
   ivf_config = {
       "nlist": 1024,  # Number of clusters
       "nprobe": 32,  # Clusters to search at query time
   }
   ```
3. **Plan** sharding strategy for scale
4. **Design** metadata schema for filtering

### Workflow 3: Optimize Search Performance
1. **Benchmark** baseline performance:
   - Queries per second (QPS)
   - Latency (p50, p95, p99)
   - Recall@k accuracy
2. **Identify** bottlenecks:
   - Index loading time
   - Search latency
   - Filter computation
   - Network overhead
3. **Apply** optimizations:
   - Tune index parameters (ef, nprobe)
   - Implement query caching
   - Optimize filter expressions
   - Consider quantization for memory
4. **Validate** recall vs latency tradeoff
5. **Document** optimal configuration

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Choose database | "Which vector database for [use case]" |
| Design index | "Design vector index for [scale]" |
| Optimize search | "Speed up vector search" |
| Add filtering | "Add metadata filters to vector search" |
| Scale vectors | "Scale to [N] million vectors" |
| Benchmark search | "Benchmark vector search performance" |

## Best Practices

- **Right-Size Your Database**: Don't over-engineer for scale you don't need
  - <1M vectors: pgvector or Chroma often sufficient
  - 1-100M vectors: Qdrant, Weaviate, or Pinecone
  - 100M+ vectors: Milvus or Pinecone with careful design

- **Understand Recall vs Speed Tradeoff**: ANN is approximate by design
  - Higher recall = slower queries
  - Tune based on your accuracy requirements
  - Measure actual recall, don't assume

- **Use Hybrid Search When Needed**: Combine vector and keyword search
  - Vector: semantic similarity
  - Keyword (BM25): exact terms, names, codes
  - Typically improves results for mixed queries

- **Design Metadata for Filtering**: Plan your filter strategy upfront
  - Indexed fields for frequent filters
  - Avoid filtering on high-cardinality fields
  - Pre-filter vs post-filter tradeoffs

- **Batch Operations When Possible**: Reduce network overhead
  - Batch upserts for ingestion
  - Batch queries when latency allows
  - Use async operations

- **Monitor and Alert**: Production search needs observability
  - Query latency percentiles
  - Index size and memory usage
  - Recall degradation over time

## Advanced Techniques

### Multi-Vector Search
Handle documents with multiple representations:
```python
class MultiVectorIndex:
    def __init__(self):
        self.title_index = VectorIndex(dim=768)
        self.content_index = VectorIndex(dim=768)
        self.summary_index = VectorIndex(dim=768)

    def search(self, query_embedding, weights=None):
        weights = weights or {"title": 0.3, "content": 0.5, "summary": 0.2}

        results = {}
        for field, weight in weights.items():
            index = getattr(self, f"{field}_index")
            field_results = index.search(query_embedding, k=20)
            for doc_id, score in field_results:
                results[doc_id] = results.get(doc_id, 0) + score * weight

        return sorted(results.items(), key=lambda x: x[1], reverse=True)[:10]
```

### Filtered Vector Search Strategies
Optimize search with filters:
```python
def filtered_search(query_embedding, filters, k=10):
    # Strategy 1: Pre-filter (for selective filters)
    if estimate_selectivity(filters) < 0.1:
        candidate_ids = apply_filters(filters)
        return vector_search_subset(query_embedding, candidate_ids, k)

    # Strategy 2: Post-filter (for non-selective filters)
    elif estimate_selectivity(filters) > 0.5:
        results = vector_search(query_embedding, k * 3)
        filtered = [r for r in results if matches_filters(r, filters)]
        return filtered[:k]

    # Strategy 3: Hybrid (general case)
    else:
        return vector_search_with_filters(query_embedding, filters, k)
```

### Quantization for Scale
Reduce memory with acceptable accuracy loss:
```python
# Product Quantization configuration
pq_config = {
    "nbits": 8,  # Bits per sub-quantizer
    "m": 16,  # Number of sub-quantizers
    # 768-dim * 4 bytes = 3KB/vector -> 16 * 1 byte = 16 bytes/vector
}

# Binary quantization (extreme compression)
binary_config = {
    "threshold": 0,  # Values > 0 -> 1, else -> 0
    # 768-dim * 4 bytes = 3KB/vector -> 768 bits = 96 bytes/vector
}
```

### Incremental Index Updates
Handle dynamic data efficiently:
```python
class DynamicVectorIndex:
    def __init__(self, rebuild_threshold=10000):
        self.main_index = build_optimized_index()
        self.delta_index = []  # Recent additions
        self.rebuild_threshold = rebuild_threshold

    def add(self, vector, metadata):
        self.delta_index.append((vector, metadata))
        if len(self.delta_index) >= self.rebuild_threshold:
            self.rebuild()

    def search(self, query, k):
        main_results = self.main_index.search(query, k)
        delta_results = brute_force_search(self.delta_index, query, k)
        return merge_results(main_results, delta_results, k)

    def rebuild(self):
        all_data = self.main_index.get_all() + self.delta_index
        self.main_index = build_optimized_index(all_data)
        self.delta_index = []
```

## Common Pitfalls to Avoid

- Using exact (flat) search at scale instead of ANN
- Not measuring actual recall, assuming ANN is "good enough"
- Over-indexing metadata fields, slowing down updates
- Ignoring the memory requirements of HNSW indexes
- Not planning for index rebuilds and maintenance windows
- Assuming vector databases handle all use cases (sometimes Elasticsearch is better)
- Forgetting to normalize vectors for cosine similarity
- Mixing embeddings from different models in the same index
