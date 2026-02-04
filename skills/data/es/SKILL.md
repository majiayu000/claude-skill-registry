---
name: elasticsearch
description: Elasticsearch DBA skill for index/mapping design, query tuning, cluster sizing and operations, shard/replica strategy, ILM, monitoring, troubleshooting (hot nodes, GC, rejected requests), and safe reindexing/upgrades. Use for tasks like designing search schemas, diagnosing performance issues, and operating ES in production.
---

# elasticsearch

Use this skill for Elasticsearch（ES）相关设计、性能与运维（DBA/中间件）任务。

## Defaults / assumptions to confirm

- ES version and deployment (self-hosted / managed)
- Cluster topology (nodes, roles, storage type)
- Data volume and retention requirements
- Query patterns (search vs analytics) and latency SLO

## Workflow

1) Understand use-cases and query patterns
- Primary user journeys: keyword search, filtering, aggregations, sorting.
- Write patterns: append-only logs vs frequent updates.
- Required consistency and freshness (near real-time delay tolerance).

2) Index & mapping design
- Define index naming convention and templates.
- Choose correct field types (`keyword` vs `text`, `date`, `long`, `scaled_float`).
- Analyze/analyzer strategy for language (e.g., Chinese tokenizer) if needed.
- Avoid mapping explosion; control dynamic mappings.
- Plan `_source` and stored fields usage; consider doc values.

3) Shards and replicas
- Pick shard count with future growth and reindex cost in mind.
- Avoid too many small shards; target shard size range (e.g., 10–50GB) depending on workload.
- Set replicas for availability and read scaling.

4) Query tuning
- Use `profile` and slow logs to find bottlenecks.
- Reduce heavy aggregations; precompute when possible.
- Use filters with `keyword` fields; cache-friendly queries.
- Pagination: prefer `search_after` for deep pages; avoid large `from+size`.

5) Lifecycle management
- Use ILM (hot-warm-cold-delete) for time-series data.
- Rollover policies by size/time; manage retention.

6) Cluster operations & stability
- Monitor heap, GC, CPU, disk watermarks, thread pool rejections.
- Detect hot keys/indices; rebalance shards carefully.
- Snapshot/restore; restore drills; retention policy.

7) Safe changes
- Mapping changes often require reindex; plan alias-based migrations.
- Use index aliases for zero-downtime cutover.
- Upgrade runbook: compatibility, rolling upgrade, backout plan.

## Outputs

- Mapping/index template proposal + rationale.
- Shard/replica sizing plan + expected capacity.
- Performance diagnosis report (evidence → root cause → fixes).
- Migration plan (reindex + alias cutover + verification).

