---
name: nw-sd-case-studies
description: 25 real-world system design case studies condensed from Alex Xu's System Design Interview Vol 1 and 2 - requirements, architecture, deep dive insights, key takeaways
user-invocable: false
disable-model-invocation: true
---

# System Design Case Studies

Reference catalog of 25 real-world designs. Use when designing a similar system or needing precedent for architectural decisions.

---

## Volume 1 Case Studies

### Rate Limiter
**Scale**: API gateway middleware | **Core**: Token Bucket (industry standard) or Sliding Window Counter | **Storage**: Redis counters with TTL | **Distributed**: Lua scripts for atomic increment | **Key insight**: cross-cutting concern, belongs in middleware/gateway | **Headers**: 429 + Retry-After + X-RateLimit-Remaining

### Consistent Hashing
**Core**: hash ring 0 to 2^32-1, servers at positions, keys walk clockwise | **Virtual nodes**: 100-200 per server, reduces load deviation from ~40% to ~5% | **Used in**: DynamoDB, Cassandra, Akamai, Discord | **Key insight**: never deploy without virtual nodes

### Key-Value Store (Dynamo-style)
**Core**: consistent hashing for partitioning, N replicas on clockwise nodes, quorum W+R>N | **Conflict**: vector clocks, LWW, app-level merge | **Failures**: sloppy quorum + hinted handoff (temp), Merkle trees + anti-entropy (permanent), gossip for detection | **Write path**: WAL -> memtable -> SSTable (LSM-tree) | **Read path**: memtable -> Bloom filter -> SSTable(s)

### Unique ID Generator
**Winner**: Snowflake -- 64-bit, sortable, minimal coordination | `[1 unused | 41 timestamp | 5 DC | 5 machine | 12 sequence]` ~4M IDs/sec/DC | **Weakness**: clock sync (NTP) | **Alt**: UUID (128-bit, not sortable), ticket server (SPOF)

### URL Shortener
**Scale**: 100M/day ~ 1,160 QPS write, 11,600 read | **Short URL**: base62 with 7 chars = 3.5T combinations | **Approaches**: hash + collision resolution | base62 from auto-increment ID | pre-generated key service | **Redirect**: 301 (cached, no analytics) vs 302 (every click tracked) -- most use 302 | **Key**: caching critical (heavy-tailed distribution)

### Web Crawler
**Scale**: 1B pages/month ~ 400 pages/sec, 500TB storage/month | **Core**: URL Frontier with priority queues (importance) + politeness queues (per-domain rate limit) | **Dedup**: SHA-256 exact, simhash/MinHash near-duplicate | **Traps**: URL length limit, max depth, blacklist | **Key insight**: URL frontier is the most important component

### Notification System
**Scale**: 10M push, 1M SMS, 5M email/day | **Architecture**: Services -> Message Queue -> Workers -> Third-party (APNs, FCM, Twilio, SES) | **Reliability**: persist before sending, retry with exponential backoff, dedup via event_id | **Key**: decouple creation from delivery; user preferences are critical

### News Feed
**Core**: hybrid fan-out -- push for normal users (<10K followers), pull for celebrities | **Feed cache**: pre-computed for most users, celebrity posts merged at read time | **Ranking**: chronological simplest; ML-based for engagement optimization | **Pagination**: cursor-based (not offset) | **Media**: object storage + CDN

### Chat System
**Scale**: 50M DAU | **Protocol**: WebSocket (bidirectional, persistent) | **Storage**: KV store (HBase-like), partition by channel_id | **1-on-1**: message via WebSocket -> store -> push to recipient (or notification if offline) | **Group (<100)**: fan-out on write to member inboxes | **Presence**: heartbeat every 5s, offline after 30s missed, lazy propagation for large friend lists | **Multi-device**: per-device cursor of last-read message

### Search Autocomplete
**Scale**: 24K QPS avg, 48K peak | **Core**: trie with cached top-K at each node, O(prefix_length) query | **Update**: offline aggregation (weekly rebuild), NOT real-time; separate trending pipeline | **Scaling**: shard by first character(s), replicate each shard | **Client**: debounce 100-200ms, cache recent results, pre-fetch

### YouTube (Video Platform)
**Scale**: 5M DAU, 150TB storage/day | **Upload**: upload -> transcoding queue -> workers (DAG pipeline: split->encode->merge) -> object storage -> CDN | **Streaming**: adaptive bitrate (DASH/HLS), manifest + segment-based | **Transcoding**: multiple resolutions (360p-4K) + formats (H.264, VP9, AV1) | **Cost**: popular videos on CDN, long-tail from origin; encode popular formats eagerly

### Google Drive (Cloud Storage)
**Scale**: 50M users, 500PB total | **Core optimization**: block-level sync -- split files into ~4MB blocks, detect changed blocks (delta sync), upload only changed | **Notification**: long polling for sync events | **Dedup**: same block hash = same storage across users | **Versioning**: store block lists per version, not full copies | **Conflict**: first upload wins, second gets notification, user resolves

---

## Volume 2 Case Studies

### Proximity Service (Yelp)
**Scale**: 100M DAU, 200M businesses | **Core**: geospatial indexing -- geohash (string prefix queries, DB-friendly) or quadtree (adaptive density, in-memory ~1.7GB) | **Boundary problem**: geohash neighbors may have different prefixes -- query target + 8 neighbors | **Architecture**: separate LBS (read-heavy, stateless) from Business Service (CRUD)

### Nearby Friends
**Scale**: 10M concurrent, 334K location updates/sec | **Core**: Pub/Sub with geohash-based channels (not per-user -- too many) | **Connection**: WebSocket (bidirectional, persistent) | **Location cache**: Redis with TTL 60s | **Optimization**: subscribe to own geohash cell + 8 neighbors; resubscribe on cell change

### Google Maps
**Map rendering**: pre-rendered tile pyramid (zoom N = 4^N tiles), served via CDN | **Tile addressing**: `/tiles/{zoom}/{x}/{y}.png` | **Routing**: hierarchical graph (local -> regional -> interstate), not naive Dijkstra -- Contraction Hierarchies | **ETA**: base distance/speed + real-time traffic + historical patterns + ML | **Traffic**: crowdsourced GPS traces, aggregated per road segment

### Distributed Message Queue (Kafka)
**Core**: topics divided into partitions (unit of parallelism + ordering) | **Storage**: append-only log segments, sequential I/O, zero-copy, batching | **Producer**: partition via round-robin/key-hash, ack modes (0/1/all) | **Consumer groups**: each partition to one consumer in group, offset tracking | **Replication**: leader + ISR followers, elect from ISR on failure | **Why fast**: sequential writes (~600MB/s), zero-copy, page cache, batching

### Metrics Monitoring
**Data model**: (metric_name, tags, timestamp, value) | **TSDB**: specialized for high write throughput + time-range queries | **Compression**: delta-of-delta timestamps, XOR values (Gorilla) | **Storage tiering**: hot (raw, memory) -> warm (1-min aggregates) -> cold (1-hour aggregates) | **Ingestion**: pull (Prometheus) or push (Datadog), buffer with Kafka | **Alerting**: rules against TSDB, dedup, escalation

### Ad Click Aggregation
**Scale**: 1B clicks/day, 10K-50K QPS | **Architecture**: Kafka -> Flink (stream) -> Aggregation DB + Reconciliation (batch) | **Windows**: tumbling (1-min for billing) or sliding (rolling) | **Exactly-once**: Kafka transactions + Flink checkpointing | **Late events**: watermarks with trade-off (longer delay = more accuracy) | **Reconciliation**: batch corrects stream inaccuracies for billing

### Hotel Reservation
**Scale**: low QPS (~35), HIGH correctness | **Core challenge**: concurrency control, not scale | **Solution**: optimistic locking + DB constraint: `UPDATE WHERE version=? AND reserved < total` | **Flow**: select -> PENDING -> payment -> CONFIRMED/CANCELLED, 10-min timeout | **Idempotency**: client-generated key prevents double-booking | **Overbooking**: business decision (~110%), built into model

### Email Service
**Scale**: 1B users, 460K receive QPS, ~10 EB storage | **Architecture**: SMTP for send/receive, separate metadata (relational/wide-column) from body/attachments (blob) | **Labels**: Gmail-style (not folders), email can have multiple | **Search**: Elasticsearch, indexed async, per-user scope | **Sync**: push-then-pull (notification triggers device pull), per-device cursor | **Anti-spam**: ML + sender reputation + SPF/DKIM/DMARC + rate limiting

### S3 Object Storage
**Scale**: 100 PB, 11 nines durability | **Architecture**: API Service + Metadata Service + Data Service (separate metadata from data) | **Durability**: replication + erasure coding + checksums + cross-AZ + self-healing | **Write**: replicate data first, then commit metadata | **Versioning**: version chain in metadata, each PUT = new version, soft delete | **Listing**: prefix queries on flat namespace with '/' convention

### Gaming Leaderboard
**Scale**: 250M score updates/day ~ 2,900 QPS | **Solution**: Redis Sorted Set (ZADD, ZREVRANGE, ZREVRANK -- all O(log N), sub-ms) | **Why Redis**: purpose-built data structure, correct complexity, single instance handles millions | **Periodic**: separate sorted set per period (`leaderboard:2024-01-15`) | **Scaling**: single Redis sufficient for most cases; shard by score range for billions

### Payment System
**Scale**: 12 TPS (LOW throughput, HIGH reliability) | **Core**: idempotency key per payment (non-negotiable) | **Flow**: receive -> PENDING -> call PSP -> SUCCESS/FAILED + webhook confirmation | **Ledger**: double-entry (every tx = debit + credit, SUM(debits) = SUM(credits)) | **Reconciliation**: nightly batch compare internal ledger vs PSP settlement | **Failures**: retry with same idempotency key, event sourcing for replay

### Digital Wallet
**Core challenge**: distributed transactions (debit A + credit B must be atomic) | **Approach 1**: single DB with ACID (simple, limited scale) | **Approach 2**: event sourcing (immutable events, balance = sum, perfect audit) | **Approach 3**: CQRS + event sourcing (write: append events, read: materialized balance) | **Cross-shard**: Saga (debit then credit, compensate on failure) or TCC (try-confirm/cancel) | **Key**: balance derived from transaction history, not stored independently

### Stock Exchange
**Scale**: microsecond latency, millions of orders/day | **Architecture**: Gateway -> Sequencer -> Matching Engine -> Execution Reports | **Sequencer**: single-threaded, monotonic sequence numbers, deterministic processing | **Order book**: per-symbol, buy max-heap + sell min-heap, FIFO at each price level | **Latency**: single-threaded (no locks), pre-allocated memory (no GC), kernel bypass (DPDK) | **Recovery**: replay from sequencer log (deterministic = same sequence -> same state)

---

## Cross-Cutting Themes

1. **Start simple, scale incrementally** -- every system starts as monolith
2. **Decouple with queues** -- async processing in nearly every design
3. **Cache is king** -- Redis/Memcached in every high-read system
4. **Consistent hashing everywhere** -- data distribution's universal tool
5. **Monitor everything** -- logging, metrics, alerting in every design
6. **Trade-offs are the answer** -- never one right architecture
7. **Numbers matter** -- estimation validates or kills a design choice
8. **Data model drives architecture** -- get it right first
9. **Event sourcing appears everywhere** -- payments, wallets, exchanges
10. **Exactly-once via idempotency** -- idempotency keys + deduplication
11. **Right data structure wins** -- Redis Sorted Set, append-only log, heap
