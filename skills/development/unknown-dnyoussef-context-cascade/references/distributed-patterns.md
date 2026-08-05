# Distributed Patterns for Multi-Database Coordination

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

This reference covers architectural patterns for coordinating multiple AgentDB instances in distributed systems. These patterns enable horizontal scaling, fault tolerance, and domain-specific optimization.

## Pattern Catalog

### 1. Database Per Domain Pattern

**Problem**: Single database becomes bottleneck for diverse data types

**Solution**: Separate databases for different domains with specialized configurations

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Router                       │
│  • Analyze query intent                                     │
│  • Route to appropriate database(s)                         │
│  • Aggregate cross-database results                         │
└────────┬─────────────┬─────────────┬────────────────────────┘
         │             │             │
         ▼             ▼             ▼
    ┌────────┐    ┌────────┐    ┌────────┐
    │ Domain │    │ Domain │    │ Domain │
    │   A    │    │   B    │    │   C    │
    └────────┘    └────────┘    └────────┘
```

**Use Cases**:
- Multi-tenant applications
- Microservices with domain-driven design
- Polyglot data requirements

**Implementation**:

```typescript
class DomainDatabaseRouter {
  private databases = {
    'user-profiles': await createAgentDBAdapter({
      dbPath: '.agentdb/users.db',
      quantizationType: 'scalar',
    }),
    'product-catalog': await createAgentDBAdapter({
      dbPath: '.agentdb/products.db',
      quantizationType: 'binary',
    }),
    'analytics': await createAgentDBAdapter({
      dbPath: '.agentdb/analytics.db',
      quantizationType: 'none',
    }),
  };

  async query(domain: string, embedding: number[], options: any) {
    const db = this.databases[domain];
    if (!db) throw new Error(`Unknown domain: ${domain}`);
    return await db.retrieveWithReasoning(embedding, options);
  }

  async crossDomainQuery(embedding: number[], domains: string[]) {
    const results = await Promise.all(
      domains.map(domain => this.query(domain, embedding, { k: 10 }))
    );
    return this.aggregateResults(results);
  }
}
```

**Advantages**:
- Independent scaling per domain
- Domain-specific optimization
- Failure isolation

**Disadvantages**:
- Cross-domain queries more complex
- Increased operational overhead

---

### 2. Hash-Based Sharding Pattern

**Problem**: Single database can't scale beyond memory/CPU limits

**Solution**: Distribute data across shards using consistent hashing

```
┌─────────────────────────────────────────────────────────────┐
│                     Shard Router                            │
│  hash(key) → shard_id                                       │
│  Consistent Hashing Ring                                    │
└────────┬───────────┬───────────┬───────────┬────────────────┘
         │           │           │           │
         ▼           ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
    │Shard 0 │  │Shard 1 │  │Shard 2 │  │Shard 3 │
    │Hash:   │  │Hash:   │  │Hash:   │  │Hash:   │
    │0-63    │  │64-127  │  │128-191 │  │192-255 │
    └────────┘  └────────┘  └────────┘  └────────┘
```

**Use Cases**:
- Massive datasets (10M+ vectors)
- Write-heavy workloads
- Horizontal scalability requirements

**Implementation**:

```typescript
import crypto from 'crypto';

class ConsistentHashRouter {
  private shards: AgentDBAdapter[];
  private virtualNodes = 150;  // Virtual nodes per shard

  constructor(numShards: number) {
    this.shards = Array.from({ length: numShards }, (_, i) =>
      createAgentDBAdapter({ dbPath: `.agentdb/shard-${i}.db` })
    );
  }

  private hash(key: string): number {
    return crypto.createHash('sha256').update(key).digest()[0];
  }

  getShardForKey(key: string): AgentDBAdapter {
    const hash = this.hash(key);
    const shardIndex = hash % this.shards.length;
    return this.shards[shardIndex];
  }

  async insertPattern(key: string, pattern: any) {
    const shard = this.getShardForKey(key);
    await shard.insertPattern(pattern);
  }

  async searchAllShards(embedding: number[], options: any) {
    const results = await Promise.all(
      this.shards.map(shard =>
        shard.retrieveWithReasoning(embedding, options)
      )
    );
    return this.aggregateAndRank(results, options.k);
  }
}
```

**Advantages**:
- Linear scalability
- Predictable performance
- Easy to add/remove shards

**Disadvantages**:
- Cross-shard queries require scatter-gather
- Resharding complexity
- No range queries

---

### 3. Replication Pattern

**Problem**: Single point of failure, read scalability

**Solution**: Replicate databases for high availability and read scaling

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer                            │
│  • Health checks                                            │
│  • Read routing (round-robin)                               │
│  • Write routing (primary only)                             │
└────────┬───────────┬───────────┬──────────────────────────┘
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │Primary │  │Replica │  │Replica │
    │ (R/W)  │  │  (R)   │  │  (R)   │
    └───┬────┘  └───┬────┘  └───┬────┘
        │           │           │
        └───────────┴───────────┘
           Async Replication
```

**Replication Strategies**:

**Master-Replica (Async)**:
- Primary handles writes
- Replicas handle reads
- Async replication for performance
- Eventual consistency

**Master-Master (Sync)**:
- All nodes handle writes
- Sync replication for consistency
- Conflict resolution required
- Higher write latency

**Implementation**:

```typescript
class ReplicationManager {
  private primary: AgentDBAdapter;
  private replicas: AgentDBAdapter[];

  async insert(pattern: any) {
    // Write to primary
    await this.primary.insertPattern(pattern);

    // Async replication to replicas
    this.replicas.forEach(replica => {
      replica.insertPattern(pattern).catch(err => {
        console.error('Replication failed:', err);
        this.handleReplicationFailure(replica, pattern);
      });
    });
  }

  async search(embedding: number[], options: any) {
    // Load balance across replicas (primary + replicas)
    const allNodes = [this.primary, ...this.replicas];
    const node = allNodes[Math.floor(Math.random() * allNodes.length)];
    return await node.retrieveWithReasoning(embedding, options);
  }
}
```

**Advantages**:
- High availability
- Read scalability
- Fault tolerance

**Disadvantages**:
- Replication lag (async)
- Higher storage costs
- Complexity in conflict resolution

---

### 4. Federated Search Pattern

**Problem**: Need to search across independent databases

**Solution**: Federated query coordinator aggregates results

```
┌─────────────────────────────────────────────────────────────┐
│                Federated Query Coordinator                  │
│  1. Broadcast query to all databases                        │
│  2. Collect results in parallel                             │
│  3. Aggregate and re-rank                                   │
│  4. Apply global filters                                    │
└────────┬───────────┬───────────┬──────────────────────────┘
         │           │           │
         v           v           v
    ┌────────┐  ┌────────┐  ┌────────┐
    │  DB A  │  │  DB B  │  │  DB C  │
    │Independent│Independent│Independent│
    └────────┘  └────────┘  └────────┘
```

**Implementation**:

```typescript
class FederatedSearchCoordinator {
  private databases: AgentDBAdapter[];

  async federatedSearch(
    embedding: number[],
    options: { k: number; filters?: any }
  ) {
    // Parallel search across all databases
    const startTime = Date.now();

    const results = await Promise.all(
      this.databases.map(async (db, idx) => {
        try {
          const dbResults = await db.retrieveWithReasoning(embedding, {
            k: options.k * 2,  // Over-fetch for better aggregation
          });
          return { dbId: idx, results: dbResults };
        } catch (err) {
          console.error(`Database ${idx} search failed:`, err);
          return { dbId: idx, results: [] };
        }
      })
    );

    // Aggregate results
    const allResults = results.flatMap(r =>
      r.results.map(pattern => ({ ...pattern, sourceDb: r.dbId }))
    );

    // Re-rank by confidence score
    allResults.sort((a, b) => b.confidence - a.confidence);

    // Apply global filters
    const filtered = this.applyFilters(allResults, options.filters);

    // Take top k
    const topResults = filtered.slice(0, options.k);

    const latency = Date.now() - startTime;
    console.log(`Federated search: ${topResults.length} results in ${latency}ms`);

    return {
      results: topResults,
      metadata: {
        totalDatabases: this.databases.length,
        responseTimes: results.map(r => r.latency),
        aggregationLatency: latency,
      },
    };
  }
}
```

**Advantages**:
- Search across heterogeneous databases
- Resilient to individual database failures
- Easy to add new databases

**Disadvantages**:
- Higher search latency
- Complex result aggregation
- No cross-database transactions

---

### 5. Hierarchical Tiering Pattern

**Problem**: Hot and cold data mixed in single database

**Solution**: Tier data by access frequency (hot/warm/cold)

```
┌─────────────────────────────────────────────────────────────┐
│                    Tiering Manager                          │
│  • Access frequency tracking                                │
│  • Automatic promotion/demotion                             │
│  • Query routing by tier                                    │
└────────┬───────────┬──────────────────────────────────────┘
         │           │
         ▼           ▼
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │  Hot   │  │  Warm   │  │  Cold    │
    │  Tier  │  │  Tier   │  │  Tier    │
    │        │  │         │  │          │
    │In-mem  │  │SSD      │  │HDD/S3    │
    │No quant│  │Scalar   │  │Binary    │
    │Fast    │  │Medium   │  │Slow      │
    └────────┘  └─────────┘  └──────────┘
```

**Implementation**:

```typescript
class TieringManager {
  private tiers = {
    hot: await createAgentDBAdapter({
      dbPath: '.agentdb/hot.db',
      quantizationType: 'none',
      cacheSize: 5000,
    }),
    warm: await createAgentDBAdapter({
      dbPath: '.agentdb/warm.db',
      quantizationType: 'scalar',
      cacheSize: 1000,
    }),
    cold: await createAgentDBAdapter({
      dbPath: '.agentdb/cold.db',
      quantizationType: 'binary',
      cacheSize: 100,
    }),
  };

  async search(embedding: number[], options: any) {
    // Search hot tier first (fastest)
    let results = await this.tiers.hot.retrieveWithReasoning(embedding, options);

    // If insufficient results, search warm tier
    if (results.length < options.k) {
      const warmResults = await this.tiers.warm.retrieveWithReasoning(
        embedding,
        { k: options.k - results.length }
      );
      results = [...results, ...warmResults];
    }

    // If still insufficient, search cold tier
    if (results.length < options.k) {
      const coldResults = await this.tiers.cold.retrieveWithReasoning(
        embedding,
        { k: options.k - results.length }
      );
      results = [...results, ...coldResults];
    }

    return results;
  }

  async promoteToHot(patternId: string) {
    // Move pattern from warm/cold to hot tier
    // ... implementation
  }

  async demoteToCold(patternId: string) {
    // Move pattern from hot/warm to cold tier
    // ... implementation
  }
}
```

**Advantages**:
- Cost optimization
- Better cache utilization
- Automatic performance tuning

**Disadvantages**:
- Tiering overhead
- Complex migration logic
- Potential data inconsistency during migration

---

## Comparison Matrix

| Pattern | Scalability | Complexity | Consistency | Use Case |
|---------|-------------|------------|-------------|----------|
| **Domain-based** | Medium | Low | Strong | Multi-domain apps |
| **Hash Sharding** | High | High | Eventual | Massive datasets |
| **Replication** | Medium | Medium | Eventual | HA + read scaling |
| **Federated** | Medium | Medium | None | Independent DBs |
| **Tiering** | Medium | Medium | Strong | Cost optimization |

## Best Practices

1. **Start Simple**: Begin with domain-based pattern
2. **Monitor First**: Measure before optimizing
3. **Incremental Scaling**: Add complexity as needed
4. **Test Failure Scenarios**: Chaos engineering
5. **Document Topology**: Keep architecture diagrams updated

## References

- [Example 2: Multi-Database Management](../examples/example-2-multi-database.md)
- [Example 3: Horizontal Sharding](../examples/example-3-sharding.md)
- [QUIC Protocol Deep Dive](./quic-protocol.md)
- [Performance Optimization Guide](./performance-optimization.md)


---
*Promise: `<promise>DISTRIBUTED_PATTERNS_VERIX_COMPLIANT</promise>`*
