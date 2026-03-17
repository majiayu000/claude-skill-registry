---
name: vector-databases
description: Vector database selection, embedding storage, approximate nearest neighbor (ANN) algorithms, and vector search optimization. Use when choosing vector stores, designing semantic search, or optimizing similarity search performance.
allowed-tools: Read, Glob, Grep
---

# Vector Databases

## When to Use This Skill

Use this skill when:

- Choosing between vector database options
- Designing semantic/similarity search systems
- Optimizing vector search performance
- Understanding ANN algorithm trade-offs
- Scaling vector search infrastructure
- Implementing hybrid search (vectors + filters)

**Keywords:** vector database, embeddings, vector search, similarity search, ANN, approximate nearest neighbor, HNSW, IVF, FAISS, Pinecone, Weaviate, Milvus, Qdrant, Chroma, pgvector, cosine similarity, semantic search

## Vector Database Comparison

### Managed Services

| Database | Strengths | Limitations | Best For |
| -------- | --------- | ----------- | -------- |
| **Pinecone** | Fully managed, easy scaling, enterprise | Vendor lock-in, cost at scale | Enterprise production |
| **Weaviate Cloud** | GraphQL, hybrid search, modules | Complexity | Knowledge graphs |
| **Zilliz Cloud** | Milvus-based, high performance | Learning curve | High-scale production |
| **MongoDB Atlas Vector** | Existing MongoDB users | Newer feature | MongoDB shops |
| **Elastic Vector** | Existing Elastic stack | Resource heavy | Search platforms |

### Self-Hosted Options

| Database | Strengths | Limitations | Best For |
| -------- | --------- | ----------- | -------- |
| **Milvus** | Feature-rich, scalable, GPU support | Operational complexity | Large-scale production |
| **Qdrant** | Rust performance, filtering, easy | Smaller ecosystem | Performance-focused |
| **Weaviate** | Modules, semantic, hybrid | Memory usage | Knowledge applications |
| **Chroma** | Simple, Python-native | Limited scale | Development, prototyping |
| **pgvector** | PostgreSQL extension | Performance limits | Postgres shops |
| **FAISS** | Library, not DB, fastest | No persistence, no filtering | Research, embedded |

### Selection Decision Tree

```text
Need managed, don't want operations?
├── Yes → Pinecone (simplest) or Weaviate Cloud
└── No (self-hosted)
    └── Already using PostgreSQL?
        ├── Yes, <1M vectors → pgvector
        └── No
            └── Need maximum performance at scale?
                ├── Yes → Milvus or Qdrant
                └── No
                    └── Prototyping/development?
                        ├── Yes → Chroma
                        └── No → Qdrant (balanced choice)
```

## ANN Algorithms

### Algorithm Overview

```text
Exact KNN:
• Search ALL vectors
• O(n) time complexity
• Perfect accuracy
• Impractical at scale

Approximate NN (ANN):
• Search SUBSET of vectors
• O(log n) to O(1) complexity
• Near-perfect accuracy
• Practical at any scale
```

### HNSW (Hierarchical Navigable Small World)

```text
Layer 3: ○───────────────────────○  (sparse, long connections)
          │                       │
Layer 2: ○───○───────○───────○───○  (medium density)
          │   │       │       │   │
Layer 1: ○─○─○─○─○─○─○─○─○─○─○─○─○  (denser)
          │││││││││││││││││││││││
Layer 0: ○○○○○○○○○○○○○○○○○○○○○○○○○  (all vectors)

Search: Start at top layer, greedily descend
• Fast: O(log n) search time
• High recall: >95% typically
• Memory: Extra graph storage
```

**HNSW Parameters:**

| Parameter | Description | Trade-off |
| --------- | ----------- | --------- |
| `M` | Connections per node | Memory vs. recall |
| `ef_construction` | Build-time search width | Build time vs. recall |
| `ef_search` | Query-time search width | Latency vs. recall |

### IVF (Inverted File Index)

```text
Clustering Phase:
┌─────────────────────────────────────────┐
│     Cluster vectors into K centroids    │
│                                         │
│    ●         ●         ●         ●     │
│   /│\       /│\       /│\       /│\    │
│  ○○○○○     ○○○○○     ○○○○○     ○○○○○   │
│ Cluster 1  Cluster 2 Cluster 3 Cluster 4│
└─────────────────────────────────────────┘

Search Phase:
1. Find nprobe nearest centroids
2. Search only those clusters
3. Much faster than exhaustive
```

**IVF Parameters:**

| Parameter | Description | Trade-off |
| --------- | ----------- | --------- |
| `nlist` | Number of clusters | Build time vs. search quality |
| `nprobe` | Clusters to search | Latency vs. recall |

### IVF-PQ (Product Quantization)

```text
Original Vector (128 dim):
[0.1, 0.2, ..., 0.9]  (128 × 4 bytes = 512 bytes)

PQ Compressed (8 subvectors, 8-bit codes):
[23, 45, 12, 89, 56, 34, 78, 90]  (8 bytes)

Memory reduction: 64x
Accuracy trade-off: ~5% recall drop
```

### Algorithm Comparison

| Algorithm | Search Speed | Memory | Build Time | Recall |
| --------- | ------------ | ------ | ---------- | ------ |
| **Flat/Brute** | Slow (O(n)) | Low | None | 100% |
| **IVF** | Fast | Low | Medium | 90-95% |
| **IVF-PQ** | Very fast | Very low | Medium | 85-92% |
| **HNSW** | Very fast | High | Slow | 95-99% |
| **HNSW+PQ** | Very fast | Medium | Slow | 90-95% |

### When to Use Which

```text
< 100K vectors:
└── Flat index (exact search is fast enough)

100K - 1M vectors:
└── HNSW (best recall/speed trade-off)

1M - 100M vectors:
├── Memory available → HNSW
└── Memory constrained → IVF-PQ or HNSW+PQ

> 100M vectors:
└── Sharded IVF-PQ or distributed HNSW
```

## Distance Metrics

### Common Metrics

| Metric | Formula | Range | Best For |
| ------ | ------- | ----- | -------- |
| **Cosine Similarity** | `A·B / (\|\|A\|\| \|\|B\|\|)` | [-1, 1] | Normalized embeddings |
| **Dot Product** | `A·B` | (-∞, ∞) | When magnitude matters |
| **Euclidean (L2)** | `√Σ(A-B)²` | [0, ∞) | Absolute distances |
| **Manhattan (L1)** | `Σ\|A-B\|` | [0, ∞) | High-dimensional sparse |

### Metric Selection

```text
Embeddings pre-normalized (unit vectors)?
├── Yes → Cosine = Dot Product (use Dot, faster)
└── No
    └── Magnitude meaningful?
        ├── Yes → Dot Product
        └── No → Cosine Similarity

Note: Most embedding models output normalized vectors
      → Dot product is usually the best choice
```

## Filtering and Hybrid Search

### Pre-filtering vs Post-filtering

```text
Pre-filtering (Filter → Search):
┌─────────────────────────────────────────┐
│ 1. Apply metadata filter               │
│    (category = "electronics")           │
│    Result: 10K of 1M vectors           │
│                                         │
│ 2. Vector search on 10K vectors        │
│    Much faster, guaranteed filter match │
└─────────────────────────────────────────┘

Post-filtering (Search → Filter):
┌─────────────────────────────────────────┐
│ 1. Vector search on 1M vectors         │
│    Return top-1000                      │
│                                         │
│ 2. Apply metadata filter               │
│    May return < K results!             │
└─────────────────────────────────────────┘
```

### Hybrid Search Architecture

```text
Query: "wireless headphones under $100"
           │
     ┌─────┴─────┐
     ▼           ▼
 ┌───────┐  ┌───────┐
 │Vector │  │Filter │
 │Search │  │ Build │
 │"wire- │  │price  │
 │less   │  │< 100  │
 │head-  │  │       │
 │phones"│  │       │
 └───────┘  └───────┘
     │           │
     └─────┬─────┘
           ▼
    ┌───────────┐
    │  Combine  │
    │  Results  │
    └───────────┘
```

### Metadata Index Design

| Metadata Type | Index Strategy | Query Example |
| ------------- | -------------- | ------------- |
| **Categorical** | Bitmap/hash index | category = "books" |
| **Numeric range** | B-tree | price BETWEEN 10 AND 50 |
| **Keyword search** | Inverted index | tags CONTAINS "sale" |
| **Geospatial** | R-tree/geohash | location NEAR (lat, lng) |

## Scaling Strategies

### Sharding Approaches

```text
Naive Sharding (by ID):
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Shard 1 │ │ Shard 2 │ │ Shard 3 │
│ IDs 0-N │ │IDs N-2N │ │IDs 2N-3N│
└─────────┘ └─────────┘ └─────────┘
Query → Search ALL shards → Merge results

Semantic Sharding (by cluster):
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Shard 1 │ │ Shard 2 │ │ Shard 3 │
│ Tech    │ │ Health  │ │ Finance │
│ docs    │ │ docs    │ │ docs    │
└─────────┘ └─────────┘ └─────────┘
Query → Route to relevant shard(s) → Faster!
```

### Replication

```text
┌─────────────────────────────────────────┐
│              Load Balancer              │
└─────────────────────────────────────────┘
         │           │           │
         ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │Replica 1│ │Replica 2│ │Replica 3│
    │  (Read) │ │  (Read) │ │  (Read) │
    └─────────┘ └─────────┘ └─────────┘
         │           │           │
         └───────────┼───────────┘
                     │
                ┌─────────┐
                │ Primary │
                │ (Write) │
                └─────────┘
```

### Scaling Decision Matrix

| Scale (vectors) | Architecture | Replication |
| --------------- | ------------ | ----------- |
| < 1M | Single node | Optional |
| 1-10M | Single node, more RAM | For HA |
| 10-100M | Sharded, few nodes | Required |
| 100M-1B | Sharded, many nodes | Required |
| > 1B | Sharded + tiered | Required |

## Performance Optimization

### Index Build Optimization

| Optimization | Description | Impact |
| ------------ | ----------- | ------ |
| **Batch insertion** | Insert in batches of 1K-10K | 10x faster |
| **Parallel build** | Multi-threaded index construction | 2-4x faster |
| **Incremental index** | Add to existing index | Avoids rebuild |
| **GPU acceleration** | Use GPU for training (IVF) | 10-100x faster |

### Query Optimization

| Optimization | Description | Impact |
| ------------ | ----------- | ------ |
| **Warm cache** | Keep index in memory | 10x latency reduction |
| **Query batching** | Batch similar queries | Higher throughput |
| **Reduce dimensions** | PCA, random projection | 2-4x faster |
| **Early termination** | Stop when "good enough" | Lower latency |

### Memory Optimization

```text
Memory per vector:
┌────────────────────────────────────────┐
│ 1536 dims × 4 bytes = 6KB per vector   │
│                                        │
│ 1M vectors:                            │
│   Raw: 6GB                             │
│   + HNSW graph: +2-4GB (M-dependent)   │
│   = 8-10GB total                       │
│                                        │
│ With PQ (64 subquantizers):            │
│   1M vectors: ~64MB                    │
│   = 100x reduction                     │
└────────────────────────────────────────┘
```

## Operational Considerations

### Backup and Recovery

| Strategy | Description | RPO/RTO |
| -------- | ----------- | ------- |
| **Snapshots** | Periodic full backup | Hours |
| **WAL replication** | Write-ahead log streaming | Minutes |
| **Real-time sync** | Synchronous replication | Seconds |

### Monitoring Metrics

| Metric | Description | Alert Threshold |
| ------ | ----------- | --------------- |
| **Query latency p99** | 99th percentile latency | > 100ms |
| **Recall** | Search accuracy | < 90% |
| **QPS** | Queries per second | Capacity dependent |
| **Memory usage** | Index memory | > 80% |
| **Index freshness** | Time since last update | Domain dependent |

### Index Maintenance

```text
┌─────────────────────────────────────────┐
│        Index Maintenance Tasks          │
├─────────────────────────────────────────┤
│ • Compaction: Merge small segments      │
│ • Reindex: Rebuild degraded index       │
│ • Vacuum: Remove deleted vectors        │
│ • Optimize: Tune parameters             │
│                                         │
│ Schedule during low-traffic periods     │
└─────────────────────────────────────────┘
```

## Common Patterns

### Multi-Tenant Vector Search

```text
Option 1: Namespace/Collection per tenant
┌─────────────────────────────────────────┐
│ tenant_1_collection                     │
│ tenant_2_collection                     │
│ tenant_3_collection                     │
└─────────────────────────────────────────┘
Pro: Complete isolation
Con: Many indexes, operational overhead

Option 2: Single collection + tenant filter
┌─────────────────────────────────────────┐
│ shared_collection                       │
│   metadata: { tenant_id: "..." }        │
│   Pre-filter by tenant_id               │
└─────────────────────────────────────────┘
Pro: Simpler operations
Con: Requires efficient filtering
```

### Real-Time Updates

```text
Write Path:
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Write     │    │   Buffer    │    │   Merge     │
│   Request   │───▶│   (Memory)  │───▶│   to Index  │
└─────────────┘    └─────────────┘    └─────────────┘

Strategy:
1. Buffer writes in memory
2. Periodically merge to main index
3. Search: main index + buffer
4. Compact periodically
```

### Embedding Versioning

```text
Version 1 embeddings ──┐
                       │
Version 2 embeddings ──┼──▶ Parallel indexes during migration
                       │
                       │    ┌─────────────────────┐
                       └───▶│ Gradual reindexing  │
                            │ Blue-green switch   │
                            └─────────────────────┘
```

## Cost Estimation

### Storage Costs

```text
Cost = (vectors × dimensions × bytes × replication) / GB × $/GB/month

Example:
10M vectors × 1536 dims × 4 bytes × 3 replicas = 184 GB
At $0.10/GB/month = $18.40/month storage

Note: Memory (for serving) costs more than storage
```

### Compute Costs

```text
Factors:
• QPS (queries per second)
• Latency requirements
• Index type (HNSW needs more RAM)
• Filtering complexity

Rule of thumb:
• 1M vectors, HNSW, <50ms latency: 16GB RAM
• 10M vectors, HNSW, <50ms latency: 64-128GB RAM
• 100M vectors: Distributed system required
```

## Related Skills

- `rag-architecture` - Using vector databases in RAG systems
- `llm-serving-patterns` - LLM inference with vector retrieval
- `ml-system-design` - End-to-end ML pipeline design
- `estimation-techniques` - Capacity planning for vector systems

## Version History

- v1.0.0 (2025-12-26): Initial release - Vector database patterns for systems design

---

## Last Updated

**Date:** 2025-12-26
