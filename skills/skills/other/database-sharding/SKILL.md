---
name: database-sharding
description: Database sharding for PostgreSQL/MySQL with hash/range/directory strategies. Use for horizontal scaling, multi-tenant isolation, billions of records, or encountering wrong shard keys, hotspots, cross-shard transactions, rebalancing issues.
keywords: database sharding, horizontal partitioning, shard key, consistent hashing,
  hash sharding, range sharding, directory sharding, cross-shard queries, shard rebalancing,
  scatter-gather pattern, multi-tenant sharding, shard router, distributed database,
  database scalability, shard migration, hotspot shards, shard key selection,
  cross-shard aggregation, two-phase commit, saga pattern, virtual shards
license: MIT
---

# database-sharding

Comprehensive database sharding patterns for horizontal scaling with hash, range, and directory-based strategies.

---

## Quick Start (10 Minutes)

**Step 1**: Choose sharding strategy from templates:
```bash
# Hash-based (even distribution)
cat templates/hash-router.ts

# Range-based (time-series data)
cat templates/range-router.ts

# Directory-based (multi-tenancy)
cat templates/directory-router.ts
```

**Step 2**: Select shard key criteria:
- ✅ **High cardinality** (millions of unique values)
- ✅ **Even distribution** (no single value > 5%)
- ✅ **Immutable** (never changes)
- ✅ **Query alignment** (in 80%+ of WHERE clauses)

**Step 3**: Implement router:
```typescript
import { HashRouter } from './hash-router';

const router = new HashRouter([
  { id: 'shard_0', connection: { host: 'db0.example.com' } },
  { id: 'shard_1', connection: { host: 'db1.example.com' } },
  { id: 'shard_2', connection: { host: 'db2.example.com' } },
  { id: 'shard_3', connection: { host: 'db3.example.com' } },
]);

// Query single shard
const user = await router.query('user_123', 'SELECT * FROM users WHERE id = $1', ['user_123']);
```

---

## Critical Rules

### ✓ Always Do

| Rule | Reason |
|------|--------|
| **Include shard key in queries** | Avoid scanning all shards (100x slower) |
| **Monitor shard distribution** | Detect hotspots before they cause outages |
| **Plan for rebalancing upfront** | Cannot easily add shards later |
| **Choose immutable shard key** | Changing key = data migration nightmare |
| **Test distribution with production data** | Synthetic data hides real hotspots |
| **Denormalize for data locality** | Keep related data on same shard |

### ✗ Never Do

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| **Sequential ID with range sharding** | Latest shard gets all writes (hotspot) |
| **Timestamp as shard key** | Recent shard overwhelmed |
| **Cross-shard transactions without 2PC** | Data corruption, inconsistency |
| **Simple modulo without consistent hashing** | Cannot add shards without full re-shard |
| **Nullable shard key** | Special NULL handling creates hotspots |
| **No shard routing layer** | Hardcoded shards = cannot rebalance |

---

## Top 7 Critical Errors

### Error 1: Wrong Shard Key Choice (Hotspots)
**Symptom**: One shard receives 80%+ of traffic
**Fix**:
```typescript
// ❌ Bad: Low cardinality (status field)
shard_key = order.status; // 90% are 'pending' → shard_0 overloaded

// ✅ Good: High cardinality (user_id)
shard_key = order.user_id; // Millions of users, even distribution
```

### Error 2: Missing Shard Key in Queries
**Symptom**: Queries scan ALL shards (extremely slow)
**Fix**:
```typescript
// ❌ Bad: No shard key
SELECT * FROM orders WHERE status = 'shipped'; // Scans all 100 shards!

// ✅ Good: Include shard key
SELECT * FROM orders WHERE user_id = ? AND status = 'shipped'; // Targets 1 shard
```

### Error 3: Sequential IDs with Range Sharding
**Symptom**: Latest shard gets all writes
**Fix**:
```typescript
// ❌ Bad: Range sharding with auto-increment
// Shard 0: 1-1M, Shard 1: 1M-2M, Shard 2: 2M+ → All new writes to Shard 2!

// ✅ Good: Hash-based sharding
const shardId = hash(id) % shardCount; // Even distribution
```

### Error 4: No Rebalancing Strategy
**Symptom**: Stuck with initial shard count, cannot scale
**Fix**:
```typescript
// ❌ Bad: Simple modulo
const shardId = hash(key) % shardCount; // Adding 5th shard breaks ALL keys

// ✅ Good: Consistent hashing
const ring = new ConsistentHashRing(shards);
const shardId = ring.getNode(key); // Only ~25% of keys move when adding shard
```

### Error 5: Cross-Shard Transactions
**Symptom**: Data inconsistency, partial writes
**Fix**:
```typescript
// ❌ Bad: Cross-shard transaction (will corrupt)
BEGIN;
UPDATE shard_1.accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE shard_2.accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT; // If shard_2 fails, shard_1 already committed!

// ✅ Good: Two-Phase Commit or Saga pattern
const txn = new TwoPhaseCommitTransaction();
txn.addOperation(shard_1, 'UPDATE accounts SET balance = balance - 100 WHERE id = ?', ['A']);
txn.addOperation(shard_2, 'UPDATE accounts SET balance = balance + 100 WHERE id = ?', ['B']);
await txn.execute(); // Atomic across shards
```

### Error 6: Mutable Shard Key
**Symptom**: Records move shards, causing duplicates
**Fix**:
```typescript
// ❌ Bad: Shard by country (user relocates)
shard_key = user.country; // User moves US → CA, now in different shard!

// ✅ Good: Shard by immutable user_id
shard_key = user.id; // Never changes
```

### Error 7: No Monitoring
**Symptom**: Silent hotspots, sudden performance degradation
**Fix**:
```typescript
// ✅ Required metrics
- Per-shard record counts (should be within 20%)
- Query distribution (no shard > 40% of queries)
- Storage per shard (alert at 80%)
- Latency p99 per shard
```

**Load** `references/error-catalog.md` for all 10 errors with detailed fixes.

---

## Sharding Strategies

| Strategy | Best For | Pros | Cons |
|----------|----------|------|------|
| **Hash** | User data, even load critical | No hotspots, predictable | Range queries scatter |
| **Range** | Time-series, logs, append-only | Range queries efficient, archival | Recent shard hotspot |
| **Directory** | Multi-tenancy, complex routing | Flexible, easy rebalancing | Lookup overhead, SPOF |

**Load** `references/sharding-strategies.md` for detailed comparisons with production examples (Instagram, Discord, Salesforce).

---

## Shard Key Selection Criteria

| Criterion | Importance | Check Method |
|-----------|------------|--------------|
| **High cardinality** | Critical | `COUNT(DISTINCT shard_key)` > shard_count × 100 |
| **Even distribution** | Critical | No value > 5% of total |
| **Immutable** | Critical | Value never changes |
| **Query alignment** | High | 80%+ queries include it |
| **Data locality** | Medium | Related records together |

**Decision Tree**:
- User-focused app → `user_id`
- Multi-tenant SaaS → `tenant_id`
- Time-series/logs → `timestamp` (range sharding)
- Product catalog → `product_id`

**Load** `references/shard-key-selection.md` for comprehensive decision trees and testing strategies.

---

## Configuration Summary

### Hash-Based Router

```typescript
import { HashRouter } from './templates/hash-router';

const router = new HashRouter([
  { id: 'shard_0', connection: { /* PostgreSQL config */ } },
  { id: 'shard_1', connection: { /* PostgreSQL config */ } },
]);

// Automatically routes to correct shard
const user = await router.query('user_123', 'SELECT * FROM users WHERE id = $1', ['user_123']);
```

### Range-Based Router

```typescript
import { RangeRouter } from './templates/range-router';

const router = new RangeRouter(shardConfigs, [
  { start: Date.parse('2024-01-01'), end: Date.parse('2024-04-01'), shardId: 'shard_q1' },
  { start: Date.parse('2024-04-01'), end: Date.parse('2024-07-01'), shardId: 'shard_q2' },
  { start: Date.parse('2024-07-01'), end: Infinity, shardId: 'shard_q3' },
]);

// Range queries target specific shards
const janEvents = await router.queryRange(
  Date.parse('2024-01-01'),
  Date.parse('2024-02-01'),
  'SELECT * FROM events WHERE created_at BETWEEN $1 AND $2'
);
```

### Directory-Based Router

```typescript
import { DirectoryRouter } from './templates/directory-router';

const router = new DirectoryRouter(directoryDBConfig, shardConfigs);

// Assign tenant to specific shard
await router.assignShard('tenant_acme', 'shard_enterprise');

// Route automatically
const users = await router.query('tenant_acme', 'SELECT * FROM users');
```

---

## When to Load References

### Choosing Strategy
**Load** `references/sharding-strategies.md` when:
- Deciding between hash, range, directory
- Need production examples (Instagram, Discord)
- Planning hybrid approaches

### Selecting Shard Key
**Load** `references/shard-key-selection.md` when:
- Choosing shard key for new project
- Evaluating existing shard key
- Testing distribution with production data

### Implementation
**Load** `references/implementation-patterns.md` when:
- Building shard router from scratch
- Implementing consistent hashing
- Need transaction handling (2PC, Saga)
- Setting up monitoring/metrics

### Cross-Shard Operations
**Load** `references/cross-shard-queries.md` when:
- Need to aggregate across shards (COUNT, SUM, AVG)
- Implementing cross-shard joins
- Building pagination across shards
- Optimizing scatter-gather patterns

### Rebalancing
**Load** `references/rebalancing-guide.md` when:
- Adding new shards
- Migrating data between shards
- Planning zero-downtime migrations
- Balancing uneven load

### Error Prevention
**Load** `references/error-catalog.md` when:
- Troubleshooting performance issues
- Reviewing shard architecture
- All 10 documented errors with fixes

---

## Complete Setup Checklist

**Before Sharding**:
- [ ] Tested shard key distribution with production data
- [ ] Shard key in 80%+ of queries
- [ ] Monitoring infrastructure ready
- [ ] Rebalancing strategy planned

**Router Implementation**:
- [ ] Shard routing layer (not hardcoded shards)
- [ ] Connection pooling per shard
- [ ] Error handling and retries
- [ ] Metrics collection (queries/shard, latency)

**Shard Configuration**:
- [ ] 4-8 shards initially (room to grow)
- [ ] Consistent hashing or virtual shards
- [ ] Replicas per shard (HA)
- [ ] Backup strategy per shard

**Application Changes**:
- [ ] All queries include shard key
- [ ] Cross-shard joins eliminated (denormalized)
- [ ] Transaction boundaries respected
- [ ] Connection pooling configured

---

## Production Example

**Before** (Single database overwhelmed):
```typescript
// Single PostgreSQL instance
const db = new Pool({ host: 'db.example.com' });

// All 10M users on one server
const users = await db.query('SELECT * FROM users WHERE status = $1', ['active']);
// Query time: 5000ms (slow!)
// DB CPU: 95%
// Disk: 500GB, growing
```

**After** (Sharded across 8 servers):
```typescript
// Hash-based sharding with 8 shards
const router = new HashRouter([
  { id: 'shard_0', connection: { host: 'db0.example.com' } },
  { id: 'shard_1', connection: { host: 'db1.example.com' } },
  // ... 6 more shards
]);

// Query single user (targets 1 shard)
const user = await router.query('user_123', 'SELECT * FROM users WHERE id = $1', ['user_123']);
// Query time: 10ms (500x faster!)

// Query all shards (scatter-gather)
const allActive = await router.queryAll('SELECT * FROM users WHERE status = $1', ['active']);
// Query time: 800ms (parallelized across 8 shards, 6x faster than single)

// Result: Each shard handles ~1.25M users
// DB CPU per shard: 20%
// Disk per shard: 65GB
// Can scale to 16 shards easily (consistent hashing)
```

---

## Known Issues Prevention

All 10 documented errors prevented:
1. ✅ Wrong shard key (hotspots) → Test distribution first
2. ✅ Missing shard key in queries → Code review, linting
3. ✅ Cross-shard transactions → Use 2PC or Saga pattern
4. ✅ Sequential ID hotspots → Use hash-based sharding
5. ✅ No rebalancing strategy → Consistent hashing from day 1
6. ✅ Timestamp sharding hotspots → Hybrid hash+range approach
7. ✅ Mutable shard key → Choose immutable keys (user_id)
8. ✅ No routing layer → Abstract with router from start
9. ✅ No monitoring → Track per-shard metrics
10. ✅ Weak hash function → Use MD5, MurmurHash3, xxHash

**See**: `references/error-catalog.md` for detailed fixes

---

## Resources

**Templates**:
- `templates/hash-router.ts` - Hash-based sharding
- `templates/range-router.ts` - Range-based sharding
- `templates/directory-router.ts` - Directory-based sharding
- `templates/cross-shard-aggregation.ts` - Aggregation patterns

**References**:
- `references/sharding-strategies.md` - Strategy comparison
- `references/shard-key-selection.md` - Key selection guide
- `references/implementation-patterns.md` - Router implementations
- `references/cross-shard-queries.md` - Query patterns
- `references/rebalancing-guide.md` - Migration strategies
- `references/error-catalog.md` - All 10 errors documented

**Production Examples**:
- Instagram: Range sharding for media
- Discord: Hash sharding for messages
- Salesforce: Directory sharding for orgs

---

**Production-tested** | **10 errors prevented** | **MIT License**
