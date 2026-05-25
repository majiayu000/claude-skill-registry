---
name: nw-sd-patterns-advanced
description: Advanced distributed patterns - event sourcing, CQRS, saga, stream processing, append-only log, exactly-once delivery, sequencer, double-entry ledger, erasure coding, order book, watermarks
user-invocable: false
disable-model-invocation: true
---

# Advanced Distributed Patterns

## Event Sourcing

**Problem**: need audit trail, state reconstruction, temporal queries.

**Core idea**: store every state change as immutable event, not current state.

```
Events: [WalletCreated: balance=0] [Deposited: +100] [Transferred: -30] [Deposited: +50]
Current state: 0 + 100 - 30 + 50 = 120
```

**Benefits**: complete audit trail | temporal queries ("balance on Jan 15?") | rebuild state from scratch | debug by replay | event-driven architecture

**Challenges**: computing state requires replaying all events -- use snapshots | schema evolution (events immutable) | store grows indefinitely -- compaction/archiving | eventual consistency for read models

**Snapshots**: periodically save computed state | current state = latest snapshot + events after it | trade-off: recovery speed vs storage

**Used in**: payment systems, banking, trading platforms, audit-critical systems

## CQRS (Command Query Responsibility Segregation)

**Problem**: read and write models have different optimization needs.

**Architecture**: Commands -> Write Model (normalized, consistency) -> events/CDC -> Read Model (denormalized, query-optimized) <- Queries

**When**: very different read/write patterns | read model needs heavy denormalization | different scaling for reads vs writes | paired with Event Sourcing

**Trade-offs**: eventual consistency between models | increased complexity (two models) | sync lag

## Saga Pattern

**Problem**: distributed transactions across services without 2PC.

**Core idea**: sequence of local transactions, each with compensating action.

### Choreography Saga
Each service listens for events and acts | no central coordinator | simpler but harder to track/debug

### Orchestration Saga
Central orchestrator coordinates sequence | more control, easier to reason about | orchestrator is SPOF

**Example -- money transfer**: 1. Debit A $100 -> success | 2. Credit B $100 -> FAIL | 3. Compensate: credit A back $100

**TCC variant (Try-Confirm/Cancel)**: Try: reserve resources | Confirm: finalize | Cancel: release. Better for inventory/booking.

**Trade-offs**: no ACID across services | compensating actions must be idempotent | temporary inconsistency visible | complex failure scenarios

## Stream Processing

**Windowing**: Tumbling (fixed, non-overlapping) | Sliding (fixed, overlapping) | Session (gap-based, closes after inactivity)

**Processing guarantees**: at-most-once (fire-and-forget, may lose) | at-least-once (retry, may duplicate) | exactly-once (hardest, checkpointing + idempotent sinks)

**Checkpointing**: periodically save processor state | on failure restart from checkpoint | Flink: barrier-based (Chandy-Lamport)

**Backpressure**: consumer slower than producer | buffer, drop, or slow producer | Kafka handles naturally (consumer pulls at own pace)

## Append-Only Log (Kafka-style)

**Structure**: segments of sequential offsets | Segment 0: [0..999] | Segment 1: [1000..1999]

**Why fast**: sequential writes only (saturates disk) | OS page cache for reads | zero-copy (sendfile) disk-to-network | batch writes amortize syscalls

**Retention**: time-based (delete old segments) | size-based (cap total) | compaction (keep latest per key)

## Exactly-Once Delivery

True exactly-once is theoretically impossible. Achieve effectively-once through:

**Idempotent producer**: sequence number per message, broker deduplicates | Kafka supports natively

**Transactional processing**: read -> process -> write output + commit offset atomically | crash mid-tx -> abort -> replay

**Idempotent consumer**: track processed message IDs | check before processing, skip if seen | DB unique constraint or dedup cache

**End-to-end**: idempotent producer + transactional processing + idempotent consumer

## Sequencer Pattern

**Problem**: multiple inputs need deterministic ordered processing.

All events pass through single sequencer | assigns monotonic sequence number | downstream processes in order | deterministic: same sequence = same state

**Properties**: single-threaded (ordering guarantee) | append to durable log | throughput limited -- shard by entity (per-symbol in exchange)

**Recovery**: standby reads same log | on primary failure: standby continues | downstream replays from last processed sequence

**Used in**: stock exchanges, matching engines, event sourcing

## Double-Entry Ledger

**Rule**: every transaction produces exactly two entries -- debit and credit of equal amount.

```
Transaction: A pays $100 to B
Entry 1: DEBIT  A $100
Entry 2: CREDIT B $100
Invariant: SUM(debits) = SUM(credits) -- always
```

Immutable entries (corrections via counter-entries) | balance = SUM(credits) - SUM(debits) | self-balancing: errors immediately detectable | regulatory requirement for financial systems

## Reconciliation

Export records from each system | match by transaction_id | identify: missing records, amount mismatches, status discrepancies | alert on mismatches

**Schedule**: T+1 (most common) | real-time (critical systems) | monthly full balance

## Erasure Coding

**Problem**: high durability without 3x storage overhead.

Split data into k data + m parity chunks (Reed-Solomon) | store k+m across nodes | any k of k+m can reconstruct

**Example (4+2)**: 6 chunks total, 1.5x overhead (vs 3x for triple replication), tolerates 2 failures

**Trade-offs**: storage efficient | higher CPU for encode/decode | higher read latency (multiple nodes) | expensive repair

**Used in**: S3, HDFS, Azure Storage, Google Colossus

## Time-Series Data Management

**Write**: append-only, batch, compress (delta-of-delta timestamps, XOR values)

**Storage tiering**: Hot (<24h, raw, memory/SSD) | Warm (1-30d, 1-min aggregates, SSD/HDD) | Cold (>30d, 1-hour aggregates, HDD/object)

**Downsampling**: reduce resolution over time, keep aggregates (min, max, avg, p99)

## Map Tile Rendering

**Tile pyramid**: zoom 0 = 1 tile, zoom N = 4^N tiles, max ~21 (~0.3m/pixel)

**Approaches**: pre-render (offline, static files) | dynamic (on-the-fly from vector data) | hybrid (popular zooms pre-rendered)

**Vector tiles (modern)**: send geometry + styling to client, client renders | smaller, flexible, smooth zoom | CDN-perfect (static URLs)

## Order Book and Matching Engine

**Data structure**: buy side = max-heap (highest price first) | sell side = min-heap (lowest first) | at each price: FIFO queue

**Matching**: new buy at 107 matches sell at 106 (best ask) | price-time priority | partial fills stay in book

**Latency techniques**: single-threaded per symbol (no locks) | pre-allocated memory pools (no GC) | kernel bypass (DPDK) | lock-free ring buffers | colocation

## Watermarks (Stream Processing)

**Concept**: watermark W(t) asserts "all events with timestamp <= t have arrived"

Window closes when watermark passes end time | events after watermark = "late events"

**Handling late**: drop (simplest) | side output (separate stream) | allowed lateness (keep window open) | retracting results

**Strategies**: perfect (rare) | heuristic (estimate + buffer) | tight = low latency but may miss events | loose = higher latency but more complete
