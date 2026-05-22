---
name: designing-distributed-systems
description: When designing distributed systems for scalability, reliability, and consistency. Covers CAP/PACELC theorems, consistency models (strong, eventual, causal), replication patterns (leader-follower, multi-leader, leaderless), partitioning strategies (hash, range, geographic), transaction patterns (saga, event sourcing, CQRS), resilience patterns (circuit breaker, bulkhead), service discovery, and caching strategies for building fault-tolerant distributed architectures.
---

# Designing Distributed Systems

Design scalable, reliable, and fault-tolerant distributed systems using proven patterns and consistency models.

## Purpose

Distributed systems are the foundation of modern cloud-native applications. Understanding fundamental trade-offs (CAP theorem, PACELC), consistency models, replication patterns, and resilience strategies is essential for building systems that scale globally while maintaining correctness and availability.

## When to Use This Skill

Apply when:
- Designing microservices architectures with multiple services
- Building systems that must scale across multiple datacenters or regions
- Choosing between consistency vs availability during network partitions
- Selecting replication strategies (single-leader, multi-leader, leaderless)
- Implementing distributed transactions (saga pattern, event sourcing, CQRS)
- Designing partition-tolerant systems with proper consistency guarantees
- Building resilient services with circuit breakers, bulkheads, retries
- Implementing service discovery and inter-service communication

## Core Concepts

### CAP Theorem Fundamentals

**CAP Theorem:** In a distributed system experiencing a network partition, choose between Consistency (C) or Availability (A). Partition tolerance (P) is mandatory.

```
Network partitions WILL occur → Always design for P

During partition:
├─ CP (Consistency + Partition Tolerance)
│  Use when: Financial transactions, inventory, seat booking
│  Trade-off: System unavailable during partition
│  Examples: HBase, MongoDB (default), etcd
│
└─ AP (Availability + Partition Tolerance)
   Use when: Social media, caching, analytics, shopping carts
   Trade-off: Stale reads possible, conflicts need resolution
   Examples: Cassandra, DynamoDB, Riak
```

**PACELC:** Extends CAP to consider normal operations (no partition).
- **If Partition:** Choose Availability (A) or Consistency (C)
- **Else (normal):** Choose Latency (L) or Consistency (C)

### Consistency Models Spectrum

```
Strong Consistency ◄─────────────────────► Eventual Consistency
      │                    │                      │
  Linearizable      Causal Consistency     Convergent
  (Slowest,         (Middle Ground,        (Fastest,
   Most Consistent)  Causally Ordered)     Eventually Consistent)
```

**Strong Consistency (Linearizability):**
- All operations appear atomically in sequential order
- Reads always return most recent write
- Use for: Bank balances, inventory stock, seat booking
- Trade-off: Higher latency, reduced availability

**Eventual Consistency:**
- If no new updates, all replicas eventually converge
- Use for: Social feeds, product catalogs, user profiles, DNS
- Trade-off: Stale reads possible, conflict resolution needed

**Causal Consistency:**
- Causally related operations seen in same order by all nodes
- Use for: Chat apps, collaborative editing, comment threads
- Trade-off: More complex than eventual, requires causality tracking

**Bounded Staleness:**
- Staleness bounded by time or version count
- Use for: Real-time dashboards, leaderboards, monitoring
- Trade-off: Must monitor lag, more complex than eventual

### Replication Patterns

**1. Leader-Follower (Single-Leader):**
- All writes to leader, replicated to followers
- Followers handle reads (load distribution)
- **Synchronous:** Wait for follower ACK (strong consistency, higher latency)
- **Asynchronous:** Don't wait (eventual consistency, possible data loss)
- Use for: Most common pattern, strong consistency with sync replication

**2. Multi-Leader:**
- Multiple leaders accept writes in different datacenters
- Leaders replicate to each other
- **Conflict resolution required:** Last-Write-Wins, application merge, vector clocks
- Use for: Multi-datacenter, low write latency, geo-distributed users
- Trade-off: Conflict resolution complexity

**3. Leaderless (Dynamo-style):**
- No single leader, quorum-based reads/writes
- **Quorum rule:** W + R > N (W=write quorum, R=read quorum, N=replicas)
- Example: N=5, W=3, R=2 → Strong consistency (overlap guaranteed)
- Use for: Maximum availability, partition tolerance
- Trade-off: Complexity, read repair needed

### Partitioning Strategies

**Hash Partitioning (Consistent Hashing):**
- Key → Hash(Key) → Partition assignment
- Even distribution, minimal rebalancing when nodes added/removed
- Use for: Point queries by ID, even distribution critical
- Examples: Cassandra, DynamoDB, Redis Cluster

**Range Partitioning:**
- Key ranges assigned to partitions (A-F, G-M, N-S, T-Z)
- Enables range queries, ordered data
- Risk: Hot spots if data skewed
- Use for: Time-series data, leaderboards, range scans
- Examples: HBase, Bigtable

**Geographic Partitioning:**
- Partition by location (US-East, EU-West, APAC)
- Use for: Data locality, GDPR compliance, low latency
- Examples: Spanner, Cosmos DB

### Resilience Patterns

**Circuit Breaker:**
```
[Closed] → Normal operation
   │ (failures exceed threshold)
   ▼
[Open] → Fail fast (don't call failing service)
   │ (timeout expires)
   ▼
[Half-Open] → Try single request
   │ success → [Closed]
   │ failure → [Open]
```
- Prevents cascading failures
- Fast-fail instead of waiting for timeout
- See references/resilience-patterns.md

**Bulkhead Isolation:**
- Isolate resources (thread pools, connection pools)
- Failure in one partition doesn't affect others
- Like ship compartments preventing total flooding

**Timeout and Retry:**
- **Timeout:** Set deadlines, fail fast if exceeded
- **Retry:** Exponential backoff with jitter
- **Idempotency:** Ensure safe retry (critical)

**Rate Limiting and Backpressure:**
- Protect services from overload
- Token bucket, leaky bucket algorithms
- Backpressure: Signal upstream to slow down

### Transaction Patterns

**Saga Pattern:**
- Coordinate distributed transactions across services
- No distributed 2PC (two-phase commit)

**Choreography:** Services react to events
```
Order Service → OrderCreated event
Payment Service → listens → PaymentProcessed event
Inventory Service → listens → InventoryReserved event
(Compensating: if payment fails → InventoryReleased event)
```

**Orchestration:** Central coordinator
```
Saga Orchestrator:
1. Call Order Service
2. Call Payment Service
3. Call Inventory Service
(If step fails → call compensating transactions in reverse)
```

**Event Sourcing:**
- Store state changes as immutable events
- Rebuild state by replaying events
- Audit trail, time travel, debugging
- Trade-off: Query complexity, snapshot optimization

**CQRS (Command Query Responsibility Segregation):**
- Separate read and write models
- Write model: Normalized, transactional
- Read model: Denormalized, cached, optimized
- Use for: Different read/write patterns, high read:write ratio (10:1+)
- Often paired with Event Sourcing

### Service Discovery

**Client-Side Discovery:**
- Client queries service registry (Consul, etcd, Eureka)
- Client load balances and calls service directly
- Pro: No proxy overhead
- Con: Client complexity

**Server-Side Discovery:**
- Client calls load balancer
- Load balancer queries registry and routes
- Pro: Simple clients
- Con: Load balancer single point of failure

**Service Mesh:**
- Sidecar proxies handle discovery, routing, retry, circuit breaking
- Examples: Istio, Linkerd
- Pro: Decouples communication logic from services
- Con: Operational complexity

### Caching Strategies

**Cache-Aside (Lazy Loading):**
```
Read:
1. Check cache → hit? return
2. Miss? Query database
3. Store in cache, return
```

**Write-Through:**
```
Write:
1. Write to cache
2. Cache writes to database synchronously
3. Return success
```

**Write-Behind (Write-Back):**
```
Write:
1. Write to cache
2. Return success
3. Cache writes to database asynchronously (batched)
```

**Cache Invalidation:**
- TTL (Time-To-Live): Expire after duration
- Event-based: Invalidate on data change
- Manual: Explicit invalidation on update

## Decision Frameworks

### Choosing Consistency Model

```
Decision Tree:
├─ Money involved? → Strong Consistency
├─ Double-booking unacceptable? → Strong Consistency
├─ Causality important (chat, edits)? → Causal Consistency
├─ Read-heavy, stale tolerable? → Eventual Consistency
└─ Default? → Eventual (then strengthen if needed)
```

### Choosing Replication Pattern

```
├─ Single region writes? → Leader-Follower
├─ Multi-region writes + conflicts OK? → Multi-Leader
├─ Multi-region writes + no conflicts? → Leader-Follower with failover
└─ Maximum availability? → Leaderless (quorum)
```

### Choosing Partitioning Strategy

```
├─ Need range scans? → Range Partitioning (risk: hot spots)
├─ Data residency requirements? → Geographic Partitioning
└─ Default? → Hash Partitioning (consistent hashing)
```

## Quick Reference Tables

### CAP/PACELC System Comparison

| System     | If Partition | Else (Normal) | Use Case           |
|------------|--------------|---------------|--------------------|
| Spanner    | PC           | EC (strong)   | Global SQL         |
| DynamoDB   | PA           | EL (eventual) | High availability  |
| Cassandra  | PA           | EL (tunable)  | Wide-column store  |
| MongoDB    | PC           | EC (default)  | Document store     |
| Cosmos DB  | PA/PC        | EL/EC (5 levels) | Multi-model     |

### Consistency Model Use Cases

| Use Case                   | Consistency Model       |
|----------------------------|------------------------|
| Bank account balance       | Strong (Linearizable)  |
| Seat booking (airline)     | Strong (Linearizable)  |
| Inventory stock count      | Strong or Bounded      |
| Shopping cart              | Eventual               |
| Product catalog            | Eventual               |
| Collaborative editing      | Causal                 |
| Chat messages              | Causal                 |
| Social media likes         | Eventual               |
| DNS records                | Eventual               |

### Quorum Configurations

| Configuration | W | R | N | Consistency | Use Case    |
|--------------|---|---|---|-------------|-------------|
| Strong       | 3 | 3 | 5 | Strong      | Banking     |
| Balanced     | 3 | 2 | 5 | Strong      | Default     |
| Write-heavy  | 2 | 3 | 5 | Strong      | Logs        |
| Read-heavy   | 3 | 1 | 5 | Eventual    | Cache       |
| Max Avail    | 1 | 1 | 5 | Eventual    | Analytics   |

## Progressive Disclosure

### Detailed References

For comprehensive coverage of specific topics, see:

- **references/cap-pacelc-theorem.md** - CAP and PACELC deep-dive with PACELC matrix
- **references/consistency-models.md** - Strong, eventual, causal, bounded staleness patterns
- **references/replication-patterns.md** - Leader-follower, multi-leader, leaderless replication
- **references/partitioning-strategies.md** - Hash, range, geographic partitioning with examples
- **references/consensus-algorithms.md** - Raft and Paxos overview (when consensus needed)
- **references/resilience-patterns.md** - Circuit breaker, bulkhead, timeout, retry, rate limiting
- **references/saga-pattern.md** - Choreography vs orchestration with working examples
- **references/event-sourcing-cqrs.md** - Event sourcing and CQRS implementation patterns
- **references/service-discovery.md** - Client-side, server-side, service mesh patterns
- **references/caching-strategies.md** - Cache-aside, write-through, write-behind, invalidation

### Working Examples

Complete, runnable examples demonstrating patterns:

- **examples/consistent-hashing/** - Consistent hashing implementation with virtual nodes
- **examples/circuit-breaker/** - Circuit breaker pattern with state transitions
- **examples/saga-orchestration/** - Saga orchestrator with compensating transactions
- **examples/event-sourcing/** - Event store with replay and snapshots
- **examples/cqrs/** - CQRS with separate read/write models
- **examples/service-discovery/** - Consul-based service discovery and registration

### ASCII Diagrams

Visual representations for complex concepts:

- **diagrams/cap-theorem.txt** - CAP theorem decision tree
- **diagrams/replication-topologies.txt** - Leader-follower, multi-leader, leaderless
- **diagrams/saga-flow.txt** - Saga choreography and orchestration flows
- **diagrams/caching-patterns.txt** - Cache-aside, write-through, write-behind

## Integration with Other Skills

**Related Skills:**

For Kubernetes deployment: See `kubernetes-operations` skill for pod anti-affinity, service mesh
For infrastructure: See `infrastructure-as-code` skill for deploying distributed systems
For databases: See `databases-sql` and `databases-nosql` for replication configuration
For messaging: See `message-queues` skill for event-driven architectures, saga orchestration
For monitoring: See `observability` skill for distributed tracing, monitoring patterns
For testing: See `performance-engineering` skill for load testing distributed systems
For security: See `security-hardening` skill for mTLS, service authentication

## Common Patterns

### Multi-Datacenter Pattern

```
1. Choose replication: Multi-leader or Leaderless
2. Partition data geographically
3. Implement conflict resolution (LWW, vector clocks, app-specific)
4. Monitor replication lag
5. Add circuit breakers between datacenters
```

### Event-Driven Saga Pattern

```
1. Define saga steps and compensating actions
2. Choose choreography (events) or orchestration (coordinator)
3. Implement idempotent handlers (retries safe)
4. Publish events with outbox pattern (transactional)
5. Monitor saga progress and timeouts
```

### High-Availability Pattern

```
1. Use leaderless replication (N=5, W=3, R=2)
2. Partition with consistent hashing
3. Add circuit breakers for failing nodes
4. Implement read repair and anti-entropy
5. Monitor quorum health
```

## Best Practices

**Design for Failure:**
- Network partitions will occur - always design for partition tolerance
- Use timeouts, retries with exponential backoff
- Implement circuit breakers to prevent cascading failures
- Test chaos engineering scenarios (partition nodes, inject latency)

**Choose Consistency Carefully:**
- Default to eventual consistency, strengthen only where needed
- Strong consistency has real costs (latency, availability)
- Use bounded staleness for middle ground

**Idempotency is Critical:**
- Design operations to be safely retryable
- Use unique request IDs for deduplication
- Essential for saga compensating transactions

**Monitor and Observe:**
- Distributed tracing with correlation IDs
- Monitor replication lag, quorum health
- Alert on circuit breaker state changes
- Track saga progress and failures

**Partition Strategically:**
- Hash partitioning for even distribution
- Range partitioning for range queries (monitor hot spots)
- Geographic partitioning for compliance, latency

**Version Everything:**
- Event schemas evolve - use versioning
- API versioning for service compatibility
- Database schema migrations in distributed systems

## Anti-Patterns to Avoid

**Distributed Monolith:**
- Microservices with tight coupling
- Shared database across services
- Fix: Database per service, async communication

**Two-Phase Commit (2PC) Overuse:**
- Slow, blocking, reduces availability
- Fix: Use saga pattern for distributed transactions

**Ignoring Network Failures:**
- Assuming network is reliable
- Fix: Always add timeouts, retries, circuit breakers

**Strong Consistency Everywhere:**
- Unnecessary latency and complexity
- Fix: Use eventual consistency by default, strengthen where needed

**No Conflict Resolution Strategy:**
- Multi-leader without handling conflicts
- Fix: Choose LWW, vector clocks, or app-specific merge

**Cache Stampede:**
- TTL expires, all clients query database
- Fix: Probabilistic early expiration, request coalescing

## Troubleshooting

**Replication Lag Too High:**
- Check network bandwidth between datacenters
- Monitor write throughput on leader
- Consider async replication or multi-leader

**Split-Brain Scenario:**
- Multiple leaders elected during partition
- Fix: Use consensus (Raft, Paxos) for leader election
- Implement fencing tokens to prevent dual writes

**Hot Partitions:**
- Range partitioning with skewed data
- Fix: Add hash component, manually redistribute, use composite keys

**Saga Timeout/Stalled:**
- Service unavailable, saga can't complete
- Fix: Implement saga timeout with automated rollback
- Dead letter queue for manual intervention

**Conflict Resolution Failures:**
- Multi-leader conflicts unhandled
- Fix: Implement clear resolution strategy (LWW, merge, manual)
- Monitor conflict rate, alert on spikes
