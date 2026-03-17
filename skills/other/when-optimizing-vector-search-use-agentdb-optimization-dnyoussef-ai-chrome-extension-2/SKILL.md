---
skill_id: when-optimizing-vector-search-use-agentdb-optimization
name: AgentDB Vector Search Optimization
version: 1.0.0
category: agentdb
subcategory: performance-optimization
trigger_pattern: "when-optimizing-vector-search"
agents:
  - performance-analyzer
  - ml-developer
  - backend-dev
complexity: intermediate
estimated_duration: 5-7 hours
prerequisites:
  - AgentDB basics
  - Vector search concepts
  - Performance profiling skills
outputs:
  - Optimized vector database
  - 4-32x memory reduction
  - 150x faster search
  - Performance benchmarks
validation_criteria:
  - Memory usage reduced by 4x minimum
  - Search latency < 10ms (p95)
  - Throughput > 50K ops/sec
  - Accuracy maintained > 95%
evidence_based_techniques:
  - Quantitative benchmarking
  - A/B comparison testing
  - Performance profiling
metadata:
  author: claude-flow
  created: 2025-10-30
  tags:
    - agentdb
    - optimization
    - quantization
    - hnsw-indexing
    - performance
---

# AgentDB Vector Search Optimization

## Overview

Optimize AgentDB performance with quantization (4-32x memory reduction), HNSW indexing (150x faster search), caching, and batch operations for scaling to millions of vectors.

## SOP Framework: 5-Phase Optimization

### Phase 1: Baseline Performance (1 hour)
- Measure current metrics (latency, throughput, memory)
- Identify bottlenecks
- Set optimization targets

### Phase 2: Apply Quantization (1-2 hours)
- Configure product quantization
- Train codebooks
- Apply compression
- Validate accuracy

### Phase 3: Implement HNSW Indexing (1-2 hours)
- Build HNSW index
- Tune parameters (M, efConstruction, efSearch)
- Benchmark speedup

### Phase 4: Configure Caching (1 hour)
- Implement query cache
- Set TTL and eviction policies
- Monitor hit rates

### Phase 5: Benchmark Results (1-2 hours)
- Run comprehensive benchmarks
- Compare before/after
- Validate improvements

## Quick Start

```typescript
import { AgentDB, Quantization, QueryCache } from 'agentdb-optimization';

const db = new AgentDB({ name: 'optimized-db', dimensions: 1536 });

// Quantization (4x memory reduction)
const quantizer = new Quantization({
  method: 'product-quantization',
  compressionRatio: 4
});
await db.applyQuantization(quantizer);

// HNSW indexing (150x speedup)
await db.createIndex({
  type: 'hnsw',
  params: { M: 16, efConstruction: 200 }
});

// Caching
db.setCache(new QueryCache({
  maxSize: 10000,
  ttl: 3600000
}));
```

## Optimization Techniques

### Quantization
- **Product Quantization**: 4-8x compression
- **Scalar Quantization**: 2-4x compression
- **Binary Quantization**: 32x compression

### Indexing
- **HNSW**: 150x faster, high accuracy
- **IVF**: Fast, partitioned search
- **LSH**: Approximate search

### Caching
- **Query Cache**: LRU eviction
- **Result Cache**: TTL-based
- **Embedding Cache**: Reuse embeddings

## Success Metrics

- Memory reduction: 4-32x
- Search speedup: 150x
- Accuracy maintained: > 95%
- Cache hit rate: > 70%

## Additional Resources

- Full docs: SKILL.md
- AgentDB Optimization: https://agentdb.dev/docs/optimization
