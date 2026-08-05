# Performance Optimization Guide

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

This guide covers performance tuning strategies for AgentDB in production environments, including quantization, HNSW tuning, caching, and distributed optimization.

## Optimization Areas

### 1. Memory Optimization

#### Quantization Strategies

**No Quantization (Full Precision)**
- Memory: 100% (384D × 4 bytes = 1.5 KB/vector)
- Accuracy: 100%
- Speed: Baseline
- Use: When accuracy is critical

```typescript
const adapter = await createAgentDBAdapter({
  quantizationType: 'none',
});
```

**Scalar Quantization (4x reduction)**
- Memory: 25% (384D × 1 byte = 384 bytes/vector)
- Accuracy: 98-99%
- Speed: 1.2x faster
- Use: Best balance for most applications

```typescript
const adapter = await createAgentDBAdapter({
  quantizationType: 'scalar',
});
```

**Binary Quantization (32x reduction)**
- Memory: 3.1% (384D ÷ 8 = 48 bytes/vector)
- Accuracy: 90-95%
- Speed: 2x faster
- Use: Memory-constrained environments

```typescript
const adapter = await createAgentDBAdapter({
  quantizationType: 'binary',
});
```

**Product Quantization (8-16x reduction)**
- Memory: 6-12% (depends on configuration)
- Accuracy: 95-98%
- Speed: 1.5x faster
- Use: Advanced optimization

```typescript
const adapter = await createAgentDBAdapter({
  quantizationType: 'product',
  quantizationBits: 8,
  quantizationCentroids: 256,
});
```

#### Memory Usage Comparison (1M vectors)

| Quantization | Memory Usage | Accuracy Loss | Search Speed |
|--------------|--------------|---------------|--------------|
| None | 1,536 MB | 0% | 1.0x |
| Scalar | 384 MB | 1-2% | 1.2x |
| Product | 192 MB | 2-5% | 1.5x |
| Binary | 48 MB | 5-10% | 2.0x |

---

### 2. HNSW Index Tuning

#### Key Parameters

**M (Connections per layer)**
- Default: 16
- Range: 8-64
- Higher M = better accuracy, more memory
- Lower M = faster indexing, less memory

```typescript
const adapter = await createAgentDBAdapter({
  hnswM: 16,  // Good balance
});
```

**Recommendations**:
- **M=8**: Memory-constrained, 10K+ vectors
- **M=16**: Default (good balance)
- **M=32**: High accuracy, <100K vectors

**EF Construction (Index Build Quality)**
- Default: 100
- Range: 50-500
- Higher EF = better index quality, slower indexing
- Lower EF = faster indexing, lower quality

```typescript
const adapter = await createAgentDBAdapter({
  hnswEFConstruction: 100,  // Good balance
});
```

**EF Search (Query Accuracy)**
- Default: 100
- Range: 10-500
- Higher EF = better recall, slower search
- Lower EF = faster search, lower recall

```typescript
const results = await adapter.retrieveWithReasoning(embedding, {
  k: 10,
  hnswEF: 100,  // Override per-query
});
```

#### HNSW Performance Matrix

| M | EF (Build) | EF (Search) | Recall | Build Time | Search Time |
|---|------------|-------------|--------|------------|-------------|
| 8 | 50 | 50 | 0.85 | 1.0x | 0.5x |
| 16 | 100 | 100 | 0.95 | 2.0x | 1.0x |
| 32 | 200 | 200 | 0.98 | 4.0x | 1.5x |
| 64 | 500 | 500 | 0.99 | 8.0x | 2.0x |

---

### 3. Caching Strategies

#### LRU Cache Configuration

```typescript
const adapter = await createAgentDBAdapter({
  cacheSize: 2000,  // Cache 2000 most-accessed vectors
  cacheStrategy: 'lru',  // Least Recently Used
});
```

**Cache Size Recommendations**:
- **Small DB (<10K)**: cacheSize = 1000 (10%)
- **Medium DB (10K-100K)**: cacheSize = 2000 (2%)
- **Large DB (>100K)**: cacheSize = 5000 (0.5%)

#### Cache Hit Rate Monitoring

```typescript
const stats = await adapter.getStats();
console.log('Cache hit rate:', (stats.cacheHitRate * 100).toFixed(2), '%');

if (stats.cacheHitRate < 0.5) {
  console.log('Consider increasing cacheSize');
}
```

#### Multi-Level Caching

```typescript
class MultiLevelCache {
  private l1Cache = new LRUCache({ max: 1000 });  // Hot
  private l2Cache = new LRUCache({ max: 5000 });  // Warm

  async get(key: string) {
    // Try L1 first
    let value = this.l1Cache.get(key);
    if (value) return value;

    // Try L2
    value = this.l2Cache.get(key);
    if (value) {
      this.l1Cache.set(key, value);  // Promote to L1
      return value;
    }

    // Fetch from database
    value = await this.fetchFromDB(key);
    this.l2Cache.set(key, value);
    return value;
  }
}
```

---

### 4. Query Optimization

#### Batch Queries

**Bad**: Sequential queries

```typescript
// ❌ Slow - sequential
for (const embedding of embeddings) {
  await adapter.retrieveWithReasoning(embedding, { k: 10 });
}
```

**Good**: Parallel queries

```typescript
// ✅ Fast - parallel
await Promise.all(
  embeddings.map(embedding =>
    adapter.retrieveWithReasoning(embedding, { k: 10 })
  )
);
```

#### Pre-filtering

**Bad**: Post-filtering

```typescript
// ❌ Slow - retrieve 1000, then filter
const results = await adapter.retrieveWithReasoning(embedding, { k: 1000 });
const filtered = results.filter(r => r.metadata.category === 'tech');
```

**Good**: Pre-filtering

```typescript
// ✅ Fast - filter during retrieval
const results = await adapter.retrieveWithReasoning(embedding, {
  k: 10,
  filters: {
    'metadata.category': 'tech',
  },
});
```

#### MMR for Diversity

```typescript
// Without MMR - may return similar results
const results = await adapter.retrieveWithReasoning(embedding, {
  k: 10,
  useMMR: false,
});

// With MMR - diverse results
const diverseResults = await adapter.retrieveWithReasoning(embedding, {
  k: 10,
  useMMR: true,
  mmrLambda: 0.5,  // Balance relevance vs diversity
});
```

---

### 5. Database Optimization

#### SQLite Configuration

```typescript
const adapter = await createAgentDBAdapter({
  dbPath: '.agentdb/optimized.db',
  sqliteOptions: {
    journalMode: 'WAL',        // Write-Ahead Logging
    synchronous: 'NORMAL',     // Balance safety vs speed
    cacheSize: -64000,         // 64MB page cache
    mmapSize: 268435456,       // 256MB memory-mapped I/O
    tempStore: 'MEMORY',       // In-memory temp tables
  },
});
```

**Key Settings**:
- **WAL mode**: Better concurrency, faster writes
- **Synchronous NORMAL**: 2x faster writes, low risk
- **Cache size**: More cache = faster reads
- **Mmap**: Faster reads for large DBs

#### Periodic Maintenance

```bash
# Reclaim unused space
sqlite3 .agentdb/vectors.db "VACUUM;"

# Update query planner statistics
sqlite3 .agentdb/vectors.db "ANALYZE;"

# Rebuild indices
npx agentdb@latest reindex ./vectors.db
```

#### Auto-vacuum Configuration

```typescript
const adapter = await createAgentDBAdapter({
  sqliteOptions: {
    autoVacuum: 'INCREMENTAL',  // Reclaim space automatically
  },
});
```

---

### 6. Distributed Optimization

#### QUIC Sync Tuning

```typescript
const adapter = await createAgentDBAdapter({
  enableQUICSync: true,
  syncInterval: 1000,        // Sync every 1s (lower = more up-to-date)
  syncBatchSize: 100,        // Batch size (higher = fewer syncs)
  maxConcurrentStreams: 100, // Parallel streams
  compression: true,         // Compress sync payload
  compressionLevel: 6,       // zlib level (1=fast, 9=best)
});
```

**Tuning Guidelines**:
- **Low latency**: syncInterval=500, compression=false
- **Bandwidth limited**: syncInterval=5000, compression=true, compressionLevel=9
- **High throughput**: syncBatchSize=500, maxConcurrentStreams=200

#### Sharding Optimization

```typescript
class OptimizedShardRouter {
  // Use more shards for better parallelism
  private numShards = Math.ceil(totalVectors / 2_500_000);

  // Route reads to nearest shard (locality)
  getShardForRead(key: string) {
    const preferredShards = this.getLocalShards();
    return preferredShards[this.hash(key) % preferredShards.length];
  }

  // Parallel search with early termination
  async searchWithEarlyStop(embedding: number[], options: { k: number }) {
    const results: any[] = [];
    const minConfidence = 0.8;

    for (const shard of this.shards) {
      const shardResults = await shard.retrieveWithReasoning(embedding, {
        k: options.k * 2,  // Over-fetch
      });

      results.push(...shardResults);

      // Early termination if we have enough high-confidence results
      const highConfResults = results.filter(r => r.confidence > minConfidence);
      if (highConfResults.length >= options.k) {
        break;
      }
    }

    return results.slice(0, options.k);
  }
}
```

---

### 7. Monitoring and Profiling

#### Performance Metrics

```typescript
async function monitorPerformance(adapter: AgentDBAdapter) {
  const stats = await adapter.getStats();

  console.log('=== AgentDB Performance ===');
  console.log('Total patterns:', stats.totalPatterns.toLocaleString());
  console.log('Database size:', (stats.dbSize / 1024 / 1024).toFixed(2), 'MB');
  console.log('Memory usage:', (stats.memoryUsage / 1024 / 1024).toFixed(2), 'MB');
  console.log('Cache hit rate:', (stats.cacheHitRate * 100).toFixed(2), '%');
  console.log('Avg search latency:', stats.avgSearchLatency.toFixed(2), 'ms');
  console.log('Avg insert latency:', stats.avgInsertLatency.toFixed(2), 'ms');
  console.log('HNSW index size:', (stats.hnswIndexSize / 1024 / 1024).toFixed(2), 'MB');

  // Recommendations
  if (stats.cacheHitRate < 0.5) {
    console.log('\n⚠️  Low cache hit rate - consider increasing cacheSize');
  }

  if (stats.avgSearchLatency > 10) {
    console.log('\n⚠️  High search latency - consider:');
    console.log('  • Reducing hnswEF for search');
    console.log('  • Adding more shards');
    console.log('  • Using scalar/binary quantization');
  }

  if (stats.memoryUsage / stats.dbSize > 0.5) {
    console.log('\n⚠️  High memory usage - consider quantization');
  }
}
```

#### Query Profiling

```typescript
async function profileQuery(adapter: AgentDBAdapter, embedding: number[]) {
  const startTime = performance.now();

  const result = await adapter.retrieveWithReasoning(embedding, {
    k: 10,
  });

  const endTime = performance.now();
  const latency = endTime - startTime;

  console.log('Query latency:', latency.toFixed(2), 'ms');
  console.log('Results:', result.length);
  console.log('Avg confidence:', (result.reduce((sum, r) => sum + r.confidence, 0) / result.length).toFixed(4));

  if (latency > 50) {
    console.log('⚠️  Slow query detected');
  }
}
```

---

## Performance Tuning Checklist

### Memory Optimization
- [ ] Enable quantization (scalar/binary)
- [ ] Tune cache size based on DB size
- [ ] Monitor memory usage
- [ ] Consider tiering for hot/cold data

### Index Optimization
- [ ] Adjust HNSW M parameter (8-32)
- [ ] Tune EF for search (50-200)
- [ ] Rebuild indices periodically
- [ ] Monitor recall vs latency

### Query Optimization
- [ ] Use pre-filtering instead of post-filtering
- [ ] Batch queries with Promise.all
- [ ] Enable MMR for diverse results
- [ ] Cache frequent queries

### Database Optimization
- [ ] Enable WAL mode
- [ ] Increase SQLite cache size
- [ ] Run VACUUM periodically
- [ ] Update ANALYZE statistics

### Distributed Optimization
- [ ] Tune QUIC sync parameters
- [ ] Use compression for bandwidth
- [ ] Implement sharding for scale
- [ ] Monitor replication lag

---

## Benchmarking

### Load Test Script

```typescript
async function loadTest(adapter: AgentDBAdapter) {
  const numQueries = 1000;
  const queryEmbeddings = Array.from({ length: numQueries }, () =>
    Array.from({ length: 384 }, () => Math.random())
  );

  console.log(`Running ${numQueries} queries...`);

  const startTime = Date.now();

  await Promise.all(
    queryEmbeddings.map(embedding =>
      adapter.retrieveWithReasoning(embedding, { k: 10 })
    )
  );

  const totalTime = Date.now() - startTime;
  const qps = numQueries / (totalTime / 1000);

  console.log(`\nLoad Test Results:`);
  console.log(`Total time: ${totalTime}ms`);
  console.log(`Queries per second: ${qps.toFixed(2)}`);
  console.log(`Avg latency: ${(totalTime / numQueries).toFixed(2)}ms`);
}
```

### Expected Performance

| DB Size | Quantization | QPS | Latency (p50) | Latency (p99) |
|---------|--------------|-----|---------------|---------------|
| 10K | None | 800 | 1.2ms | 3.5ms |
| 10K | Scalar | 1200 | 0.8ms | 2.1ms |
| 100K | Scalar | 500 | 2.0ms | 6.0ms |
| 1M | Scalar | 150 | 6.5ms | 18ms |
| 1M | Binary | 300 | 3.2ms | 9.5ms |

---

## References

- [QUIC Protocol](./quic-protocol.md)
- [Distributed Patterns](./distributed-patterns.md)
- [Example 1: QUIC Sync](../examples/example-1-quic-sync.md)
- [Example 3: Sharding](../examples/example-3-sharding.md)


---
*Promise: `<promise>PERFORMANCE_OPTIMIZATION_VERIX_COMPLIANT</promise>`*
