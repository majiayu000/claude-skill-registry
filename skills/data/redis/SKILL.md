---
name: redis
description: Redis DBA skill for cache/data-structure design, performance tuning, memory optimization, persistence (RDB/AOF), replication/cluster, high availability (Sentinel), and operational troubleshooting. Use for tasks like diagnosing latency spikes, eviction issues, hot keys, and designing safe cache patterns.
---

# redis

Use this skill for Redis 相关设计、性能与运维（DBA/中间件）任务。

## Defaults / assumptions to confirm

- Redis mode: single instance / Sentinel / Cluster
- Version and deployment (bare metal, Docker, managed)
- Persistence: RDB / AOF / both
- Memory policy and eviction strategy

## Workflow

1) Understand use-cases
- Cache vs primary store vs queue/stream.
- Data size, TTL distribution, QPS, latency SLO.
- Consistency requirements and acceptable staleness.

2) Key design
- Namespacing: `{app}:{domain}:{entity}:{id}` (or similar)
- Avoid overly long keys; ensure stable prefixes for metrics.
- Plan for multi-tenant isolation if needed.

3) Data structures & patterns
- Strings/Hashes for objects, Sets/ZSets for membership/ranking, Streams for event pipelines.
- Avoid large values; prefer hashes for many small fields.
- Choose one cache pattern explicitly: Cache-Aside / Write-Through / Write-Behind.
- Prevent cache stampede: singleflight/mutex, request coalescing, jittered TTL.

4) Performance & reliability
- Identify hot keys, big keys, slow commands.
- Use pipelining where safe; avoid blocking commands on large collections.
- Track latency with `LATENCY DOCTOR` / slowlog; instrument at client.

5) Memory management
- Set `maxmemory` and an eviction policy suitable for workload (`allkeys-lru`, `volatile-ttl`, etc.).
- Watch fragmentation and RSS vs used_memory.
- Use key TTLs and size controls to avoid unbounded growth.

6) Persistence & durability
- RDB: snapshot intervals, fork time, disk IO impact.
- AOF: fsync policy, rewrite, size growth.
- Define recovery objectives (RPO/RTO) explicitly.

7) HA / scaling
- Sentinel: failover behavior, client reconnection strategy.
- Cluster: hash slots, resharding plan, multi-key operations constraints.
- Plan for multi-AZ and network partitions.

8) Operations checklist
- Backups and restore drills (test in staging).
- Capacity planning: memory headroom, CPU, network bandwidth.
- Upgrade playbook and rollback plan.

## Outputs

- Key/TTL design doc (prefixes, structures, TTL, max size).
- Config recommendations (`maxmemory`, persistence, replication).
- Troubleshooting report (symptoms → evidence → root cause → fixes).

