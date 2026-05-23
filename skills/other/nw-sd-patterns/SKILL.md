---
name: nw-sd-patterns
description: Core distributed systems patterns - load balancing, caching, sharding, consistent hashing, message queues, rate limiting, CDN, Bloom filters, ID generation, replication, conflict resolution, CAP theorem
user-invocable: false
disable-model-invocation: true
---

# Core Distributed Systems Patterns

## Load Balancing

**Problem**: single server can't handle all traffic.

**Approaches**: Round Robin (simple, ignores load) | Weighted Round Robin (accounts for capacity) | Least Connections (fewest active) | IP Hash (session affinity) | Layer 4/transport (IP/port, fast) | Layer 7/application (HTTP-aware, smarter)

**Placement**: client-to-web | web-to-app | app-to-database

**Trade-offs**: LB itself is SPOF -- use active-passive pair | session affinity complicates horizontal scaling -- prefer stateless servers | health checks critical

## Caching

**Problem**: repeated DB reads are slow.

**Strategies**: Cache-aside/lazy loading (app checks cache, fills on miss -- most common) | Write-through (write cache+DB simultaneously) | Write-behind (cache only, async to DB) | Read-through (cache fronts DB transparently)

**Cache-aside pattern**: Read: `cache.get(key) -> hit? return : db.read -> cache.set -> return` | Write: `db.write -> cache.delete(key)`

**Eviction**: LRU (most common) | LFU (skewed access) | TTL (time-based)

**Problems**: thundering herd (many misses simultaneously -- use locking/coalescing) | cache penetration (non-existent keys -- Bloom filter or cache null) | cache avalanche (mass expiration -- jittered TTLs) | size cache based on working set, not total data

## Database Replication

**Master-Slave**: all writes to master, reads to replicas | replication lag = eventual consistency | master fails: promote replica

**Multi-Master**: writes to any node, conflict resolution required | better write availability, much more complex | suitable for multi-region

**Trade-offs**: sync replication = consistency but higher write latency | async = lower latency but data loss risk on failure

## Database Sharding

**Problem**: single DB can't handle write volume or data size.

**Strategies**: Hash-based (hash(key) % N -- even but resharding painful) | Range-based (ranges, can have hotspots) | Directory-based (lookup table, flexible but SPOF)

**Partition key**: must distribute data AND queries evenly | must be in most queries | common: user_id, tenant_id, region

**Challenges**: resharding (consistent hashing helps) | celebrity/hotspot problem | cross-shard joins (expensive -- denormalize) | referential integrity (enforce in app) | schema changes across all shards

## Consistent Hashing

**Problem**: traditional hash(key) % N remaps almost all keys when N changes.

**How**: hash output space as ring (0 to 2^32-1) | servers at positions on ring | keys walk clockwise to first server | adding/removing server affects only adjacent keys

**Virtual nodes**: each physical server gets 100-200 positions | ensures even distribution | handles heterogeneous capacities

**Used in**: DynamoDB, Cassandra, Discord, Akamai CDN

## Message Queues

**Problem**: tight coupling; spikes overwhelm downstream.

**Properties**: decoupling | buffering (absorbs spikes) | async processing | guaranteed delivery

**Patterns**: Point-to-point (one consumer per message) | Pub/Sub (all subscribers get message) | Dead letter queue (failed messages for debugging)

**When**: email/notification sending | image/video processing | analytics ingestion | cross-service communication | any op where user doesn't need immediate result

**Technologies**: Kafka (high throughput, log-based, event streaming) | RabbitMQ (flexible routing, task queues) | SQS (managed, AWS) | Redis Streams (lightweight)

## Rate Limiting

**Problem**: protect services from abuse and cascading overload.

| Algorithm | Mechanism | Pros | Cons |
|-----------|-----------|------|------|
| Token Bucket | tokens refill at fixed rate | allows bursts, simple | memory per user |
| Leaking Bucket | queue with fixed processing rate | smooth output | no burst flexibility |
| Fixed Window | count per time window | simple | burst at edges |
| Sliding Window Log | track each request timestamp | precise | memory-intensive |
| Sliding Window Counter | hybrid fixed + weighted | good balance | approximate |

Token Bucket is industry standard (AWS, Stripe, GitHub). Implementation: API gateway or per-service | Redis counters with TTL | return 429 with Retry-After and X-RateLimit headers

## CDN

**Problem**: static content from origin adds latency for distant users.

**How**: assets cached at edge servers worldwide | DNS routes to nearest edge | cache miss fetches from origin

**Push vs Pull**: Push (upload to CDN, infrequent changes) | Pull (CDN fetches on first request, simpler)

**Invalidation**: URL versioning (preferred) | CDN API purge | TTL expiration

## Bloom Filters

**Problem**: quickly check "is X in set?" without storing full set.

**How**: bit array + k hash functions | insert sets k bits | query checks k bits | false positives possible, false negatives impossible

**Used for**: cache penetration prevention | duplicate URL detection (crawlers) | spam filtering

**Config**: 10 bits per element ~ 1% false positive rate | cannot delete (use Counting Bloom Filter)

## Unique ID Generation

| Approach | Sortable | Size | Coordination | Throughput |
|----------|----------|------|-------------|------------|
| UUID v4 | No | 128b | None | Unlimited |
| DB auto-inc | Yes | 64b | High | Limited |
| Ticket server | Yes | 64b | Medium | Limited |
| Snowflake | Yes | 64b | Minimal | Very high |

**Snowflake**: `[1 unused | 41 timestamp | 5 datacenter | 5 machine | 12 sequence]` -- ~4M IDs/sec/DC | clock sync via NTP is Achilles heel

## Fan-out Strategies

**Fan-out on write (push)**: post immediately written to all followers' feeds | read is instant | expensive for celebrities

**Fan-out on read (pull)**: feed computed at read time | write is fast | read is slow

**Hybrid (production)**: push for normal users | pull for celebrities (>10K followers)

## Real-time Communication

**Long Polling**: server holds request open until data or timeout | simple, resource-intensive

**WebSocket**: full-duplex persistent | low latency | stateful (complicates LB -- need sticky sessions)

**SSE**: server pushes over HTTP | unidirectional | auto-reconnect | simpler for notification/feed

## Geohashing and Spatial Indexing

**Geohash**: encodes lat/lon to string, nearby share prefix | precision by length (4=39km, 6=1.2km, 8=38m) | boundary problem: query target + 8 neighbors

**Quadtree**: recursive subdivision into 4 quadrants | adaptive to density | in-memory, 200M items ~1.7GB

**Geohash vs Quadtree**: geohash simpler (string prefix), DB-friendly | quadtree adaptive to density, in-memory only

## Data Replication Strategies

**Single-leader**: one primary writes, replicas read | simple but SPOF

**Multi-leader**: multiple write nodes, conflict resolution | better for multi-DC

**Leaderless (Dynamo)**: any node reads/writes | quorum W+R>N | W=1,R=N fast writes | W=N,R=1 fast reads | W=R=N/2+1 balanced | anti-entropy + read repair

## Conflict Resolution

**LWW**: timestamp-based, simple but lossy | **Vector clocks**: detect conflicts, app resolves | **CRDTs**: auto-merge data types | **Application-level**: present to user (like Git)

## CAP Theorem

**CP (consistency)**: reject writes during partition | HBase, MongoDB, Redis Cluster | financial transactions

**AP (availability)**: accept writes, resolve later | Cassandra, DynamoDB, CouchDB | social feeds, shopping carts

**Real question**: "what happens during network partition?" | most systems need availability for reads, consistency for certain writes | tunable consistency (Cassandra) gives flexibility

## Write-Ahead Log (WAL)

Before applying mutation, write to append-only log | acknowledge to client | periodically apply to data structure | on crash: replay from last checkpoint. Used in PostgreSQL, MySQL, Cassandra, Kafka.

## Gossip Protocol

Each node maintains member list with heartbeat counters | periodically exchanges state with random peer | propagates in O(log N) rounds. Used for membership, failure detection, config propagation.

## Trie (Prefix Tree)

Each node = character, root-to-leaf = string | optimizations: compress single-child chains, cache top results at each node, shard by first character. Used in: search autocomplete, spell checking, IP routing.
