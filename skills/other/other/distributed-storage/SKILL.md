---
name: distributed-storage
description: Distributed storage systems design and operation for cloud platforms. Covers the GFS/HDFS block-and-master pattern, object storage (Swift/S3) with consistent hashing and eventual consistency, block storage semantics, replication vs erasure coding, the CAP theorem in practice, read-repair and anti-entropy, snapshot chains, and the GFS/BigTable/Spanner evolution. Use when designing a storage subsystem, choosing between object/block/file, or reviewing a replication and consistency strategy.
type: skill
category: cloud-systems
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/cloud-systems/distributed-storage/SKILL.md
superseded_by: null
---
# Distributed Storage

Distributed storage is where durability, consistency, latency, and cost collide. Every design choice trades among them, and the trade-offs cannot be hidden from applications for long. This skill covers the landmark systems and the recurring patterns they embody, from the GFS master-chunkserver split that defined cloud-scale storage, to the Dynamo-style consistent-hash rings that power modern object stores, to the Spanner-style externally consistent databases built on TrueTime.

**Agent affinity:** ghemawat (GFS and storage systems craftsmanship), dean (BigTable, Spanner, and the evolution from GFS), decandia (Dynamo and eventually consistent stores)

**Concept IDs:** cloud-cinder-block-storage, cloud-swift-glance-object-image, cloud-nova-instances

## The Three Storage Shapes

Cloud platforms expose storage in three shapes, each with a different access model and consistency profile.

**Object storage.** Immutable blobs with rich metadata, accessed by key, usually over HTTP. Examples: Amazon S3, OpenStack Swift, Google Cloud Storage. Consistent hashing distributes objects across nodes; replication or erasure coding provides durability. Objects are typically append-or-replace — partial updates are not the native operation. Best for: media, backups, logs, analytics input, static web content.

**Block storage.** Virtual disks presented as block devices to virtual machines. Examples: Amazon EBS, OpenStack Cinder, Google Persistent Disk. Provides the POSIX-ish semantics of a local disk but with the durability and mobility of a network service. Typically attached to a single instance at a time. Best for: databases, filesystems, anything that expects random-access block semantics.

**File storage.** Shared filesystem accessed via NFS, SMB, or similar protocols. Examples: Amazon EFS, OpenStack Manila, GCS Filestore. Multiple clients mount the same filesystem and see each other's writes. Best for: legacy applications expecting a POSIX filesystem and shared access.

These are not interchangeable. Picking the wrong shape — object where you need block, block where you need file, file where you need object — produces workarounds that dominate the cost of running the system.

## The GFS Pattern: Master and Chunkservers

The Google File System (Ghemawat, Gobioff, Leung, 2003) introduced the architecture that most large distributed filesystems still use:

- **Single master.** Holds all metadata: namespace, access control, mapping from files to chunks, mapping from chunks to chunkservers. Metadata fits in RAM for the scales GFS was built for.
- **Chunkservers.** Hold actual file data in 64 MB chunks (later 64-256 MB in successors). Each chunk is replicated 3 times across different failure domains.
- **Clients.** Query the master for chunk locations, then read and write directly from/to chunkservers. The master is not on the data path.

Key design decisions that shaped the cloud era:

- Optimize for large files and append-heavy workloads, not random writes.
- Assume component failures are routine, not exceptional.
- Push consistency compromises to the application — GFS is "consistent but defined" (all mutations succeed in the same order on all replicas) rather than fully linearizable.
- The master's single point of failure is mitigated by a shadow master and operational processes, not by distributed consensus.

HDFS (Hadoop Distributed File System) is an open-source reimplementation of GFS with slightly different choices (smaller default chunk size, different consistency model).

## Object Storage: Consistent Hashing and Eventual Consistency

Object stores at cloud scale are built around consistent hashing rings (Swift, Ceph RADOS, Riak, Cassandra). The ring distributes objects across nodes without a central metadata server, and tolerates node additions and removals with minimal data movement.

**Consistent hashing basics.**

1. Hash each node onto a ring (a large integer space).
2. Hash each object key onto the same ring.
3. An object is assigned to the first node found by walking clockwise from its hash.
4. For replication, use the first N nodes.

**Virtual nodes.** To smooth load imbalances, each physical node contributes many "virtual nodes" at different ring positions. This reduces the variance of the load distribution.

**Consistency profile.** Object stores typically provide strong read-your-writes consistency for a single object (after a write, subsequent reads from the same client see the new value) and eventual consistency across replicas (all replicas converge to the same value over time, but a read right after a write from a different client may see the old value).

## Replication vs Erasure Coding

Two ways to achieve durability:

**Replication.** Store N complete copies. Simple, fast reads (read any replica), survives N-1 failures. Storage overhead is N:1.

**Erasure coding.** Encode an object as K data chunks plus M parity chunks such that any K chunks can reconstruct the original. Storage overhead is (K+M)/K. Example: Reed-Solomon (10,4) needs 14 chunks total to store 10 chunks of data, survives 4 failures, storage overhead 1.4x.

Erasure coding is dramatically more space-efficient but slower to read (may need to reconstruct from multiple chunks) and more complex to repair. Modern object stores use both: replication for hot data and recent writes, erasure coding for cold data.

## CAP Theorem in Practice

Brewer's CAP theorem says that in the presence of a network partition, you can have Consistency (every read sees the latest write) or Availability (every request gets a response), but not both. You cannot opt out of partitions — they happen — so the real choice is between CP and AP during a partition.

- **CP systems.** Consistency over availability. During a partition, minority partitions stop serving. Examples: ZooKeeper, etcd, Spanner.
- **AP systems.** Availability over consistency. During a partition, all partitions keep serving but may see different values. Examples: Dynamo, Cassandra, Riak.

CAP is a useful compass but often overstated. In practice, most partitions are brief and most applications can tolerate seconds of reduced consistency or reduced availability. The interesting trade-offs happen at steady state, not during rare partitions. PACELC (Abadi) extends CAP: during a Partition, choose A or C; Else, choose Latency or Consistency. That is the trade-off you make every millisecond, and it deserves more attention than pure CAP thinking.

## Read Repair and Anti-Entropy

Eventually consistent systems need background mechanisms to converge divergent replicas.

**Read repair.** When a client reads from multiple replicas and finds disagreement, the coordinator writes the latest version back to stale replicas. Cheap and immediate, but only repairs data that is actually read.

**Anti-entropy / Merkle trees.** Replicas periodically exchange Merkle tree hashes of their data ranges. Differences indicate ranges to compare more carefully. Found differences are repaired by copying the winning version. Repairs all data, including cold data, at the cost of background I/O.

**Hinted handoff.** During a transient failure, the coordinator accepts writes targeted at the failed node and stores them locally as "hints." When the failed node recovers, hints are delivered. This preserves write availability without sacrificing durability.

## Snapshots and Copy-on-Write

Block storage typically supports snapshots: a point-in-time image of a volume that can be used for backup, cloning, or rollback. Efficient implementations use copy-on-write:

- Initially, the snapshot shares all blocks with the volume.
- When a block is written on the volume, the original is first copied to snapshot-owned storage, then the new value is written to the volume.
- Reads from the snapshot check for CoW copies first, then fall through to shared blocks.

Snapshot chains (A -> B -> C where B was a snapshot of A and C a snapshot of B) compose as long as you track parentage. Deleting snapshots in the middle of a chain requires merging data back into the parent or the child.

## The GFS -> BigTable -> Spanner Arc

This progression is worth studying as a microcosm of distributed storage evolution:

- **GFS (2003).** Large file storage, append-oriented, relaxed consistency. Optimal for MapReduce inputs and outputs.
- **BigTable (2006).** A sparse, distributed, multidimensional sorted map built on top of GFS. Row-level atomicity, no cross-row transactions. Good fit for logging, time-series, analytical workloads.
- **Spanner (2012).** A globally distributed relational database with external consistency, built on Paxos and TrueTime. External consistency means: if transaction T1 commits before T2 starts (in real time), then T1's commit timestamp is before T2's. Achieved by bounding clock uncertainty with GPS and atomic clocks (TrueTime), then waiting out the uncertainty window before committing.

Each system was built because the previous one's consistency model was insufficient for the next class of application. The progression illustrates that storage is an application-driven field: the right system depends on what you are storing and why.

## Common Failure Modes

| Failure | Symptom | Cause |
|---|---|---|
| Lost updates | New write silently overwritten | Missing conditional updates / CAS |
| Split-brain writes | Divergent replicas after partition | No quorum protection on writes |
| Long tail on reads | P99 latency >> P50 | Unlucky replica placement, hedged reads needed |
| Durability loss | Data unrecoverable after multi-node failure | Replicas in same failure domain (same rack, same PSU) |
| Metadata corruption | Whole filesystem inaccessible | Single master point of failure without recovery procedure |
| Snapshot bloat | Volumes can't be deleted | CoW chains not merged, reference tracking broken |

## When to Use This Skill

- Choosing between object, block, and file storage for a new application.
- Designing a storage subsystem or evaluating an existing one.
- Picking a replication strategy (full replication vs erasure coding).
- Reviewing consistency claims and failure modes of a proposed storage layer.
- Capacity planning and failure domain placement.
- Incident response for storage-related outages.

## When NOT to Use This Skill

- Single-node, single-user storage. Local filesystems are fine.
- Ephemeral data that does not need to survive process restart (use memory, not storage).

## Decision Guidance

| Workload | Recommended shape |
|---|---|
| Media, backups, logs, archives | Object storage |
| VM disks, database storage | Block storage |
| Legacy NFS dependency | File storage |
| OLTP with strong consistency | Spanner-style (if available), or Raft-backed SQL |
| OLAP / analytics | Object storage + query engine (Presto, Spark) |
| Time-series | Purpose-built TSDB or wide-column (Cassandra, BigTable) |
| Global strong consistency | Spanner-style with TrueTime, or CP consensus + app-level coordination |

## References

- Ghemawat, S., Gobioff, H., Leung, S.-T. (2003). "The Google File System." SOSP.
- Chang, F., et al. (2006). "Bigtable: A Distributed Storage System for Structured Data." OSDI.
- Corbett, J., et al. (2012). "Spanner: Google's Globally-Distributed Database." OSDI.
- DeCandia, G., et al. (2007). "Dynamo: Amazon's Highly Available Key-value Store." SOSP.
- Lakshman, A., Malik, P. (2010). "Cassandra: A Decentralized Structured Storage System." SIGOPS OSR.
- Brewer, E. (2012). "CAP Twelve Years Later: How the 'Rules' Have Changed." IEEE Computer.
- Abadi, D. (2012). "Consistency Tradeoffs in Modern Distributed Database System Design." IEEE Computer.
