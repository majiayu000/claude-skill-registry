---
name: kafka-architecture
description: Expert knowledge of Apache Kafka architecture, cluster design, capacity planning, partitioning strategies, replication, and high availability. Auto-activates on keywords kafka architecture, cluster sizing, partition strategy, replication factor, kafka ha, kafka scalability, broker count, topic design, kafka performance, kafka capacity planning.
---

# Kafka Architecture & Design Expert

Comprehensive knowledge of Apache Kafka architecture patterns, cluster design principles, and production best practices for building resilient, scalable event streaming platforms.

## Core Architecture Concepts

### Kafka Cluster Components

**Brokers**:
- Individual Kafka servers that store and serve data
- Each broker handles thousands of partitions
- Typical: 3-10 brokers per cluster (small), 10-100+ (large enterprises)

**Controller**:
- One broker elected as controller (via KRaft or ZooKeeper)
- Manages partition leaders and replica assignments
- Failure triggers automatic re-election

**Topics**:
- Logical channels for message streams
- Divided into partitions for parallelism
- Can have different retention policies per topic

**Partitions**:
- Ordered, immutable sequence of records
- Unit of parallelism (1 partition = 1 consumer in a group)
- Distributed across brokers for load balancing

**Replicas**:
- Copies of partitions across multiple brokers
- 1 leader replica (serves reads/writes)
- N-1 follower replicas (replication only)
- In-Sync Replicas (ISR): Followers caught up with leader

### KRaft vs ZooKeeper Mode

**KRaft Mode** (Recommended, Kafka 3.3+):
```yaml
Cluster Metadata:
  - Stored in Kafka itself (no external ZooKeeper)
  - Metadata topic: __cluster_metadata
  - Controller quorum (3 or 5 nodes)
  - Faster failover (<1s vs 10-30s)
  - Simplified operations
```

**ZooKeeper Mode** (Legacy, deprecated in 4.0):
```yaml
External Coordination:
  - Requires separate ZooKeeper ensemble (3-5 nodes)
  - Stores cluster metadata, configs, ACLs
  - Slower failover (10-30 seconds)
  - More complex to operate
```

**Migration**: ZooKeeper → KRaft migration supported in Kafka 3.6+

## Cluster Sizing Guidelines

### Small Cluster (Development/Testing)

```yaml
Configuration:
  Brokers: 3
  Partitions per broker: ~100-500
  Total partitions: 300-1500
  Replication factor: 3
  Hardware:
    - CPU: 4-8 cores
    - RAM: 8-16 GB
    - Disk: 500 GB - 1 TB SSD
    - Network: 1 Gbps

Use Cases:
  - Development environments
  - Low-volume production (<10 MB/s)
  - Proof of concepts
  - Single datacenter

Example Workload:
  - 50 topics
  - 5-10 partitions per topic
  - 1 million messages/day
  - 7-day retention
```

### Medium Cluster (Standard Production)

```yaml
Configuration:
  Brokers: 6-12
  Partitions per broker: 500-2000
  Total partitions: 3K-24K
  Replication factor: 3
  Hardware:
    - CPU: 16-32 cores
    - RAM: 64-128 GB
    - Disk: 2-8 TB NVMe SSD
    - Network: 10 Gbps

Use Cases:
  - Standard production workloads
  - Multi-team environments
  - Regional deployments
  - Up to 500 MB/s throughput

Example Workload:
  - 200-500 topics
  - 10-50 partitions per topic
  - 100 million messages/day
  - 30-day retention
```

### Large Cluster (High-Scale Production)

```yaml
Configuration:
  Brokers: 20-100+
  Partitions per broker: 2000-4000
  Total partitions: 40K-400K+
  Replication factor: 3
  Hardware:
    - CPU: 32-64 cores
    - RAM: 128-256 GB
    - Disk: 8-20 TB NVMe SSD
    - Network: 25-100 Gbps

Use Cases:
  - Large enterprises
  - Multi-region deployments
  - Event-driven architectures
  - 1+ GB/s throughput

Example Workload:
  - 1000+ topics
  - 50-200 partitions per topic
  - 1+ billion messages/day
  - 90-365 day retention
```

### Kafka Streams / Exactly-Once Semantics (EOS) Clusters

```yaml
Configuration:
  Brokers: 6-12+ (same as standard, but more control plane load)
  Partitions per broker: 500-1500 (fewer due to transaction overhead)
  Total partitions: 3K-18K
  Replication factor: 3
  Hardware:
    - CPU: 16-32 cores (more CPU for transactions)
    - RAM: 64-128 GB
    - Disk: 4-12 TB NVMe SSD (more for transaction logs)
    - Network: 10-25 Gbps

Special Considerations:
  - More brokers due to transaction coordinator load
  - Lower partition count per broker (transactions = more overhead)
  - Higher disk IOPS for transaction logs
  - min.insync.replicas=2 mandatory for EOS
  - acks=all required for producers

Use Cases:
  - Stream processing with exactly-once guarantees
  - Financial transactions
  - Event sourcing with strict ordering
  - Multi-step workflows requiring atomicity
```

## Partitioning Strategy

### How Many Partitions?

**Formula**:
```
Partitions = max(
  Target Throughput / Single Partition Throughput,
  Number of Consumers (for parallelism),
  Future Growth Factor (2-3x)
)

Single Partition Limits:
  - Write throughput: ~10-50 MB/s
  - Read throughput: ~30-100 MB/s
  - Message rate: ~10K-100K msg/s
```

**Examples**:

**High Throughput Topic** (Logs, Events):
```yaml
Requirements:
  - Write: 200 MB/s
  - Read: 500 MB/s (multiple consumers)
  - Expected growth: 3x in 1 year

Calculation:
  Write partitions: 200 MB/s ÷ 20 MB/s = 10
  Read partitions: 500 MB/s ÷ 40 MB/s = 13
  Growth factor: 13 × 3 = 39

Recommendation: 40-50 partitions
```

**Low-Latency Topic** (Commands, Requests):
```yaml
Requirements:
  - Write: 5 MB/s
  - Read: 10 MB/s
  - Latency: <10ms p99
  - Order preservation: By user ID

Calculation:
  Throughput partitions: 5 MB/s ÷ 20 MB/s = 1
  Parallelism: 4 (for redundancy)

Recommendation: 4-6 partitions (keyed by user ID)
```

**Dead Letter Queue**:
```yaml
Recommendation: 1-3 partitions
Reason: Low volume, order less important
```

### Partition Key Selection

**Good Keys** (High Cardinality, Even Distribution):
```yaml
✅ User ID (UUIDs):
  - Millions of unique values
  - Even distribution
  - Example: "user-123e4567-e89b-12d3-a456-426614174000"

✅ Device ID (IoT):
  - Unique per device
  - Natural sharding
  - Example: "device-sensor-001-zone-a"

✅ Order ID (E-commerce):
  - Unique per transaction
  - Even temporal distribution
  - Example: "order-2024-11-15-abc123"
```

**Bad Keys** (Low Cardinality, Hotspots):
```yaml
❌ Country Code:
  - Only ~200 values
  - Uneven (US, CN >> others)
  - Creates partition hotspots

❌ Boolean Flags:
  - Only 2 values (true/false)
  - Severe imbalance

❌ Date (YYYY-MM-DD):
  - All today's traffic → 1 partition
  - Temporal hotspot
```

**Compound Keys** (Best of Both):
```yaml
✅ Country + User ID:
  - Partition by country for locality
  - Sub-partition by user for distribution
  - Example: "US:user-123" → hash("US:user-123")

✅ Tenant + Event Type + Timestamp:
  - Multi-tenant isolation
  - Event type grouping
  - Temporal ordering
```

## Replication & High Availability

### Replication Factor Guidelines

```yaml
Development:
  Replication Factor: 1
  Reason: Fast, no durability needed

Production (Standard):
  Replication Factor: 3
  Reason: Balance durability vs cost
  Tolerates: 2 broker failures (with min.insync.replicas=2)

Production (Critical):
  Replication Factor: 5
  Reason: Maximum durability
  Tolerates: 4 broker failures (with min.insync.replicas=3)
  Use Cases: Financial transactions, audit logs

Multi-Datacenter:
  Replication Factor: 3 per DC (6 total)
  Reason: DC-level fault tolerance
  Requires: MirrorMaker 2 or Confluent Replicator
```

### min.insync.replicas

**Configuration**:
```yaml
min.insync.replicas=2:
  - At least 2 replicas must acknowledge writes
  - Typical for replication.factor=3
  - Prevents data loss if 1 broker fails

min.insync.replicas=1:
  - Only leader must acknowledge (dangerous!)
  - Use only for non-critical topics

min.insync.replicas=3:
  - At least 3 replicas must acknowledge
  - For replication.factor=5 (critical systems)
```

**Rule**: `min.insync.replicas ≤ replication.factor - 1` (to allow 1 replica failure)

### Rack Awareness

```yaml
Configuration:
  broker.rack=rack1  # Broker 1
  broker.rack=rack2  # Broker 2
  broker.rack=rack3  # Broker 3

Benefit:
  - Replicas spread across racks
  - Survives rack-level failures (power, network)
  - Example: Topic with RF=3 → 1 replica per rack

Placement:
  Leader: rack1
  Follower 1: rack2
  Follower 2: rack3
```

## Retention Strategies

### Time-Based Retention

```yaml
Short-Term (Events, Logs):
  retention.ms: 86400000  # 1 day
  Use Cases: Real-time analytics, monitoring

Medium-Term (Transactions):
  retention.ms: 604800000  # 7 days
  Use Cases: Standard business events

Long-Term (Audit, Compliance):
  retention.ms: 31536000000  # 365 days
  Use Cases: Regulatory requirements, event sourcing

Infinite (Event Sourcing):
  retention.ms: -1  # Forever
  cleanup.policy: compact
  Use Cases: Source of truth, state rebuilding
```

### Size-Based Retention

```yaml
retention.bytes: 10737418240  # 10 GB per partition

Combined (Time OR Size):
  retention.ms: 604800000      # 7 days
  retention.bytes: 107374182400  # 100 GB
  # Whichever limit is reached first
```

### Compaction (Log Compaction)

```yaml
cleanup.policy: compact

How It Works:
  - Keeps only latest value per key
  - Deletes old versions
  - Preserves full history initially, compacts later

Use Cases:
  - Database changelogs (CDC)
  - User profile updates
  - Configuration management
  - State stores

Example:
  Before Compaction:
    user:123 → {name: "Alice", v:1}
    user:123 → {name: "Alice", v:2, email: "alice@ex.com"}
    user:123 → {name: "Alice A.", v:3}

  After Compaction:
    user:123 → {name: "Alice A.", v:3}  # Latest only
```

## Performance Optimization

### Broker Configuration

```yaml
# Network threads (handle client connections)
num.network.threads: 8  # Increase for high connection count

# I/O threads (disk operations)
num.io.threads: 16  # Set to number of disks × 2

# Replica fetcher threads
num.replica.fetchers: 4  # Increase for many partitions

# Socket buffer sizes
socket.send.buffer.bytes: 1048576    # 1 MB
socket.receive.buffer.bytes: 1048576  # 1 MB

# Log flush (default: OS handles flushing)
log.flush.interval.messages: 10000  # Flush every 10K messages
log.flush.interval.ms: 1000         # Or every 1 second
```

### Producer Optimization

```yaml
High Throughput:
  batch.size: 65536            # 64 KB
  linger.ms: 100               # Wait 100ms for batching
  compression.type: lz4        # Fast compression
  acks: 1                      # Leader only

Low Latency:
  batch.size: 16384            # 16 KB (default)
  linger.ms: 0                 # Send immediately
  compression.type: none
  acks: 1

Durability (Exactly-Once):
  batch.size: 16384
  linger.ms: 10
  compression.type: lz4
  acks: all
  enable.idempotence: true
  transactional.id: "producer-1"
```

### Consumer Optimization

```yaml
High Throughput:
  fetch.min.bytes: 1048576     # 1 MB
  fetch.max.wait.ms: 500       # Wait 500ms to accumulate

Low Latency:
  fetch.min.bytes: 1           # Immediate fetch
  fetch.max.wait.ms: 100       # Short wait

Max Parallelism:
  # Deploy consumers = number of partitions
  # More consumers than partitions = idle consumers
```

## Multi-Datacenter Patterns

### Active-Passive (Disaster Recovery)

```yaml
Architecture:
  Primary DC: Full Kafka cluster
  Secondary DC: Replica cluster (MirrorMaker 2)

Configuration:
  - Producers → Primary only
  - Consumers → Primary only
  - MirrorMaker 2: Primary → Secondary (async replication)

Failover:
  1. Detect primary failure
  2. Switch producers/consumers to secondary
  3. Promote secondary to primary

Recovery Time: 5-30 minutes (manual)
Data Loss: Potential (async replication lag)
```

### Active-Active (Geo-Replication)

```yaml
Architecture:
  DC1: Kafka cluster (region A)
  DC2: Kafka cluster (region B)
  Bidirectional replication via MirrorMaker 2

Configuration:
  - Producers → Nearest DC
  - Consumers → Nearest DC or both
  - Conflict resolution: Last-write-wins or custom

Challenges:
  - Duplicate messages (at-least-once delivery)
  - Ordering across DCs not guaranteed
  - Circular replication prevention

Use Cases:
  - Global applications
  - Regional compliance (GDPR)
  - Load distribution
```

### Stretch Cluster (Synchronous Replication)

```yaml
Architecture:
  Single Kafka cluster spanning 2 DCs
  Rack awareness: DC1 = rack1, DC2 = rack2

Configuration:
  min.insync.replicas: 2
  replication.factor: 4 (2 per DC)
  acks: all

Requirements:
  - Low latency between DCs (<10ms)
  - High bandwidth link (10+ Gbps)
  - Dedicated fiber

Trade-offs:
  Pros: Synchronous replication, zero data loss
  Cons: Latency penalty, network dependency
```

## Monitoring & Observability

### Key Metrics

**Broker Metrics**:
```yaml
UnderReplicatedPartitions:
  Alert: > 0 for > 5 minutes
  Indicates: Replica lag, broker failure

OfflinePartitionsCount:
  Alert: > 0
  Indicates: No leader elected (critical!)

ActiveControllerCount:
  Alert: != 1 (should be exactly 1)
  Indicates: Split brain or no controller

RequestHandlerAvgIdlePercent:
  Alert: < 20%
  Indicates: Broker CPU saturation
```

**Topic Metrics**:
```yaml
MessagesInPerSec:
  Monitor: Throughput trends
  Alert: Sudden drops (producer failure)

BytesInPerSec / BytesOutPerSec:
  Monitor: Network utilization
  Alert: Approaching NIC limits

RecordsLagMax (Consumer):
  Alert: > 10000 or growing
  Indicates: Consumer can't keep up
```

**Disk Metrics**:
```yaml
LogSegmentSize:
  Monitor: Disk usage trends
  Alert: > 80% capacity

LogFlushRateAndTimeMs:
  Monitor: Disk write latency
  Alert: > 100ms p99 (slow disk)
```

## Security Patterns

### Authentication & Authorization

```yaml
SASL/SCRAM-SHA-512:
  - Industry standard
  - User/password authentication
  - Stored in ZooKeeper/KRaft

ACLs (Access Control Lists):
  - Per-topic, per-group permissions
  - Operations: READ, WRITE, CREATE, DELETE, ALTER
  - Example:
      bin/kafka-acls.sh --add \
        --allow-principal User:alice \
        --operation READ \
        --topic orders

mTLS (Mutual TLS):
  - Certificate-based auth
  - Strong cryptographic identity
  - Best for service-to-service
```

## Integration with SpecWeave

**Automatic Architecture Detection**:
```typescript
import { ClusterSizingCalculator } from './lib/utils/sizing';

const calculator = new ClusterSizingCalculator();
const recommendation = calculator.calculate({
  throughputMBps: 200,
  retentionDays: 30,
  replicationFactor: 3,
  topicCount: 100
});

console.log(recommendation);
// {
//   brokers: 8,
//   partitionsPerBroker: 1500,
//   diskPerBroker: 6000 GB,
//   ramPerBroker: 64 GB
// }
```

**SpecWeave Commands**:
- `/sw-kafka:deploy` - Validates cluster sizing before deployment
- `/sw-kafka:monitor-setup` - Configures metrics for key indicators

## Related Skills

- `/sw-kafka:kafka-mcp-integration` - MCP server setup
- `/sw-kafka:kafka-cli-tools` - CLI operations

## External Links

- [Kafka Documentation - Architecture](https://kafka.apache.org/documentation/#design)
- [Confluent - Kafka Sizing](https://www.confluent.io/blog/how-to-choose-the-number-of-topics-partitions-in-a-kafka-cluster/)
- [KRaft Mode Overview](https://kafka.apache.org/documentation/#kraft)
- [LinkedIn Engineering - Kafka at Scale](https://engineering.linkedin.com/kafka/running-kafka-scale)
