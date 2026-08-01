---
name: agentdb-vector-search-optimization
description: 'AgentDB Vector Search Optimization operates on 3 fundamental principles:'
---

---
name: agentdb-vector-search-optimization
description: AgentDB Vector Search Optimization operates on 3 fundamental principles:
allowed-tools: Read, Write, Edit, Task, TodoWrite, Glob, Grep
---

# AgentDB Vector Search Optimization



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

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

## MCP Requirements

This skill operates using AgentDB's npm package and API only. No additional MCP servers required.

All AgentDB optimization operations are performed through:
- npm CLI: `npx agentdb@latest`
- TypeScript/JavaScript API: `import { AgentDB, Quantization, QueryCache } from 'agentdb-optimization'`

## Additional Resources

- Full docs: SKILL.md
- AgentDB Optimization: https://agentdb.dev/docs/optimization

## Core Principles

AgentDB Vector Search Optimization operates on 3 fundamental principles:

### Principle 1: Quantization - Trade Negligible Accuracy for Massive Memory Reduction

Vector databases face a fundamental constraint: high-dimensional embeddings (768-1536 dimensions) consume enormous memory at scale. Quantization techniques compress vectors by 4-32x through codebook encoding, enabling systems to hold millions of vectors in memory while maintaining 95%+ accuracy.

In practice:
- Apply product quantization (4-8x compression) for production workloads requiring high accuracy
- Use scalar quantization (2-4x compression) when exact distances matter for ranking
- Deploy binary quantization (32x compression) for massive-scale approximate search where recall > precision

### Principle 2: HNSW Indexing - Logarithmic Search Instead of Linear Scan

Brute-force vector search scales O(n) - doubling vectors doubles search time. HNSW (Hierarchical Navigable Small World) indexes create multi-layer graphs that enable O(log n) search, delivering 150x speedups with tunable accuracy trade-offs through the efSearch parameter.

In practice:
- Build HNSW indexes with M=16 (connections per node) for balanced performance and recall
- Set efConstruction=200 during index building to ensure high-quality graph topology
- Tune efSearch=50-200 at query time to balance speed vs accuracy (higher = slower but more accurate)

### Principle 3: Caching - Exploit Query Locality for 10x Speedup

Real-world vector search exhibits extreme query locality - users repeatedly search similar queries, recommendation systems re-rank same candidates, RAG systems revisit common documents. LRU caches with 70%+ hit rates eliminate 70% of expensive vector computations.

In practice:
- Implement query result caching with TTL=1 hour to capture repeated searches
- Cache embedding computations for frequently accessed text (document titles, product names)
- Use cache key hashing (xxhash64) to handle high-dimensional query vectors efficiently

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Premature Quantization - Apply Compression Before Understanding Workload** | Blindly quantizing to 32x compression destroys accuracy for high-precision tasks (medical diagnosis, financial fraud detection). Optimizing the wrong metric creates worse outcomes. | Establish baseline metrics FIRST (Phase 1): measure unoptimized latency, throughput, memory, accuracy. Then apply quantization incrementally (4x -> 8x -> 16x) while validating accuracy > 95% at each step. |
| **Index Amnesia - Rebuild HNSW on Every Query** | HNSW indexes take minutes to build (efConstruction=200 for 1M vectors). Rebuilding on every query eliminates all speedup benefits. | Build indexes ONCE during initialization or batch updates. Persist indexes to disk. Use incremental updates for new vectors instead of full rebuilds. |
| **Cache Thrashing - TTL Too Short or Cache Too Small** | Setting TTL=60 seconds evicts results before reuse. Tiny cache (1000 entries) causes constant evictions in high-traffic systems. | Set TTL based on query frequency (1 hour for typical workloads, 24 hours for stable datasets). Size cache to capture 70%+ of traffic (10K-100K entries typical). Monitor hit rate and adjust. |

## Conclusion

AgentDB Vector Search Optimization unlocks production-scale performance for vector databases through three complementary techniques: quantization (4-32x memory reduction), HNSW indexing (150x search speedup), and caching (70%+ hit rate efficiency). The 5-phase SOP guides systematic optimization from baseline measurement through quantization, indexing, caching, and comprehensive benchmarking, ensuring improvements are validated with hard metrics rather than assumptions.

This skill is critical when scaling vector search beyond toy datasets to millions of vectors, reducing infrastructure costs by 75%+ through memory compression, or achieving sub-10ms latency requirements for real-time applications like recommendation engines and search APIs. The techniques are complementary, not competing - quantization reduces memory footprint enabling larger in-memory indexes, HNSW accelerates the search operation itself, and caching eliminates redundant computation for common queries.

The key insight is performance optimization requires measurement-driven iteration. Blindly applying "best practices" without understanding your workload's query patterns, accuracy requirements, and scale constraints leads to wasted effort or degraded quality. By establishing baselines first, applying optimizations incrementally, and validating improvements at each step, you achieve dramatic performance gains while maintaining the accuracy guarantees your application demands. The result is vector search systems that scale to billions of vectors while remaining responsive enough for interactive user experiences.