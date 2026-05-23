---
name: fdb-layer-engineering
description: Guide for building FoundationDB layers in Rust. Use when designing
  key schemas, handling transactions, implementing indexes, or troubleshooting
  FDB errors. Covers tuple layer, atomic ops, retries, and performance patterns.
allowed-tools: Read, Grep, Edit, Write
---

# FoundationDB Layer Engineering

Patterns for building robust FDB layers with the `foundationdb` crate.

## Transaction Limits

| Resource | Target | Hard Limit |
|----------|--------|------------|
| Duration | <1 sec | 5 sec (MVCC window) |
| Transaction size | <8 MB | 10 MB |
| Key size | — | 10 KB |
| Value size | — | 100 KB |
| Batch size | 100-1000 records | — |

Keep transactions short—autothrottle can't rate-limit large transactions effectively.

## Transaction Rules

| Rule | Details |
|------|---------|
| **Always use `db.run()`** | Handles retry loop with exponential backoff |
| **Design for OCC** | Conflicts detected at commit, not during reads |
| **Automatic idempotency** | FDB 7.3+: use `TransactionOption::AutomaticIdempotency` |
| **Use Batch priority** | Set `TransactionOption::PriorityBatch` for background jobs |
| **Idempotent writes** | Generate unique IDs OUTSIDE retry loop |

## Critical Error Codes

| Code | Name | Action |
|------|------|--------|
| 1007 | `transaction_too_old` | Retry—exceeded 5s limit |
| 1020 | `not_committed` | Retry—conflict detected |
| 1021 | `commit_unknown_result` | May have committed—check `maybe_committed` |
| 2101 | `transaction_too_large` | Reduce size (non-retryable) |

## Key Design Patterns

- **Tuple layer**: Always use `pack()`/`unpack()` for order-preserving keys
- **Subspaces**: Isolate tenant data in contiguous key ranges
- **Sharded counters**: Split hot keys across multiple shards
- **Snapshot reads**: `trx.get(key, true)` to skip conflict range

### Hotspot Prevention

| Technique | When to Use |
|-----------|-------------|
| **Salting** | Prepend hash prefix to distribute sequential writes |
| **Reversed numbers** | `MAX_VALUE - ts` for latest-first ordering |
| **Avoid monotonic keys** | Sequential IDs/timestamps hotspot single storage nodes |

## Atomic Operations

| Operation | Use Case |
|-----------|----------|
| `Add` | Counters (conflict-free increments) |
| `Max`/`Min` | High/low watermarks |
| `SetVersionstampedKey` | Ordered logs, event sourcing |
| `CompareAndClear` | Conditional deletion |

## Secondary Indexes

- Index key format: `(index_prefix, indexed_value, primary_key)`
- Always update indexes in same transaction as primary data
- Covering indexes store full value to avoid second lookup

## Decision Matrix

| Scenario | Strategy |
|----------|----------|
| Single record CRUD | One txn, <100ms |
| Bulk import (100s) | Batched, 100-200 records/txn |
| Bulk import (millions) | Batched + continuation + Batch priority |
| Read then external API | Separate transactions |
| Hot key | Atomic ops or sharding |
| Background job | Batched + Batch priority |

## Anti-patterns

1. **Long transactions** - Break large ops into continuations
2. **Holding txn during external calls** - Separate read and write transactions
3. **Fixed batch sizes** - Use size-aware batching (~1MB per batch)
4. **Ignoring `maybe_committed`** - Causes duplicate side effects on retry
5. **Hot keys without sharding** - Shard frequently updated keys
6. **Atomic ops + reads on same key** - Loses conflict-free benefit
7. **Low-level `get_range`** - Use `get_ranges`/`get_ranges_keyvalues` instead

## Full Reference

- FDB Developer Guide: https://apple.github.io/foundationdb/developer-guide.html
- FDB Known Limitations: https://apple.github.io/foundationdb/known-limitations.html
- Automatic Idempotency (7.3+): https://pierrezemb.fr/posts/automatic-txn-fdb-730/
- HBase Data Model: https://pierrezemb.fr/posts/hbase-data-model/
- Reverse Number Scanning: https://pierrezemb.fr/posts/reverse-number-scanning/
