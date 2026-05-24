---
name: nw-sd-framework
description: 4-step system design framework with back-of-envelope estimation, scaling ladder, and common pitfalls
user-invocable: false
disable-model-invocation: true
---

# System Design Framework

## The 4-Step Process

Every system design follows this structure. Skipping steps is the top mistake.

### Step 1: Understand the Problem and Establish Design Scope (3-10 min)

Narrow an impossibly broad question into a tractable problem.

**Ask about**: users and scale | most important features | read/write ratio | non-functional requirements (latency, availability, consistency) | existing infrastructure | special constraints (mobile-first, offline, regulatory)

**Produce**: functional requirements (3-5 bullets) | non-functional requirements (scale, latency, availability, consistency model) | capacity estimation (QPS, storage, bandwidth)

**Red flags if skipped**: designing a system nobody asked for | over-engineering for imaginary scale | missing critical constraints (GDPR, real-time)

### Step 2: Propose High-Level Design and Get Buy-In (10-15 min)

Sketch the big picture. Validate before diving deep.

**Do**: draw architecture diagram (clients, servers, databases, caches, queues) | define API contract (REST/GraphQL/gRPC -- key endpoints) | design data model (entities, relationships, access patterns) | walk through 1-2 core use cases end-to-end | get buy-in: "Does this make sense before I go deeper?"

**API patterns**: RESTful for CRUD-heavy | GraphQL for flexible client queries | gRPC for internal service-to-service | WebSocket/SSE for real-time

**Data model**: SQL vs NoSQL based on access patterns, not hype | denormalization trade-offs | partitioning key selection (directly impacts scalability)

### Step 3: Design Deep Dive (10-25 min)

Go deep on 2-3 components.

**Choose**: most technically challenging | most interesting trade-offs | bottleneck components (highest load, most failure-prone)

**Depth means**: specific algorithms (consistent hashing, Bloom filters) | failure modes and handling | scaling strategy per component | data flow with edge cases | monitoring and operational concerns

### Step 4: Wrap Up (3-5 min)

**Cover**: summarize design in 2-3 sentences | identify known bottlenecks | what you'd improve with more time | operational concerns (monitoring, alerting, deployment) | future enhancements

**Avoid**: introducing entirely new components at this stage | second-guessing your design

---

## Back-of-Envelope Estimation

### Powers of 2 Reference

| Power | Value | Meaning |
|-------|-------|---------|
| 10 | 1 Thousand | 1 KB |
| 20 | 1 Million | 1 MB |
| 30 | 1 Billion | 1 GB |
| 40 | 1 Trillion | 1 TB |
| 50 | 1 Quadrillion | 1 PB |

### Latency Numbers Every Engineer Should Know

| Operation | Latency |
|-----------|---------|
| L1 cache reference | 0.5 ns |
| L2 cache reference | 7 ns |
| Main memory reference | 100 ns |
| Compress 1KB (Zippy) | 10 us |
| Send 2KB over 1 Gbps | 20 us |
| Read 1 MB from memory | 250 us |
| Datacenter round trip | 500 us |
| Disk seek | 10 ms |
| Read 1 MB from network | 10 ms |
| Read 1 MB from disk | 30 ms |
| CA to Netherlands round trip | 150 ms |

**Key takeaways**: memory fast, disk slow -- cache aggressively | compress before network send | inter-datacenter trips expensive -- minimize cross-region calls

### Common Estimation Patterns

**DAU to QPS**: `QPS = DAU * actions_per_user / 86400` | Peak QPS = QPS * 2 (or *3 for spiky)

**Storage**: `daily = DAU * actions * avg_size` | yearly = daily * 365 | 5-year = yearly * 5

**Bandwidth**: `QPS * average_response_size`

**Servers**: `Peak QPS / QPS_per_server` where CPU-bound ~hundreds | IO-bound with cache ~thousands | static content ~tens of thousands

### Estimation Example: Twitter-like Service

```
150M DAU, 2 tweets/day, 10 reads/day
Write QPS = 150M * 2 / 86400 ~ 3,500
Read QPS = 150M * 10 / 86400 ~ 17,000; Peak ~ 50,000
Storage: 300M tweets * 1KB + 30M media * 500KB ~ 15.3 TB/day
```

---

## Scaling Ladder

Each step solves a specific bottleneck. Never introduce a component without articulating which bottleneck it addresses.

1. **Load balancer** -- distribute traffic across web servers
2. **Database replication** -- master-slave for read scaling
3. **Cache layer** -- reduce database load (Redis/Memcached)
4. **CDN** -- serve static content from edge
5. **Stateless web tier** -- move session state to shared store
6. **Database sharding** -- horizontal partitioning for write scaling
7. **Message queue** -- decouple components, handle spikes
8. **Logging, metrics, monitoring** -- observability at scale
9. **Multiple data centers** -- geographic redundancy and latency reduction

---

## Common Pitfalls

1. **Jumping to solutions** -- design before understanding requirements
2. **Over-engineering** -- adding components for imaginary scale
3. **Ignoring trade-offs** -- every choice has a cost; name it
4. **SPOF blindness** -- always ask "what if this dies?"
5. **Neglecting data** -- the data model drives everything
6. **Forgetting operations** -- a system you can't monitor is one you can't run
7. **Not doing math** -- gut feelings are wrong; estimates keep you honest
