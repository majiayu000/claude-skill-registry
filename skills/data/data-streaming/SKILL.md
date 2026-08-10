---
name: data-streaming
description: "Designs streaming platforms for Kafka, Flink, CDC, and lakehouse ingestion. Use when planning event backbones, CDC pipelines, schema governance, or real-time lakehouse delivery."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.2"
last_validated: 2026-07-11
---

# Data Streaming

**Modern Best Practices:** choose the event backbone and stream processor separately, treat schemas and replay as product interfaces, default to event-time processing for stateful analytics, and verify managed-service behavior from primary docs before making vendor-specific recommendations.

Primary sources live in `data/sources.json`. Refresh time-sensitive claims against official docs before making definitive recommendations about managed services, version-specific features, limits, or pricing.

This skill covers the **data platform side** of streaming: event backbones, CDC, stateful processing, schema governance, and real-time delivery into lakes, warehouses, search, or serving systems.

## When to Use

- Choose between Kafka, Redpanda, Pulsar, Kinesis, or managed Kafka offerings
- Design topic strategy, partitioning, retention, replay, and ordering guarantees
- Build or fix CDC pipelines with Debezium, Flink CDC, or managed database-streaming tools
- Choose between Flink, Kafka Streams, Spark Structured Streaming, or lighter transformation paths
- Define schema registry, compatibility, contract, and tombstone handling rules
- Deliver streams into Iceberg, Hudi, Delta, ClickHouse, warehouses, caches, or search systems
- Review streaming SLOs, lag, checkpointing, reprocessing, and operational failure modes

## When NOT to Use

- Lakehouse storage formats, catalogs, or medallion architecture -> Use [data-lake-platform](../data-lake-platform/SKILL.md)
- OLTP schema tuning or transactional query optimization -> Use [data-sql-optimization](../data-sql-optimization/SKILL.md)
- Event-driven application architecture, CQRS, or domain event design -> Use [software-architecture-design](../software-architecture-design/SKILL.md)
- BI dashboard automation and Metabase APIs -> Use [data-metabase](../data-metabase/SKILL.md)
- Product instrumentation and attribution strategy -> Use `marketing-product-analytics`

## Triage Questions

1. What is the real requirement: operational events, CDC, analytical enrichment, or customer-facing low-latency delivery?
2. What matters most: portability, managed simplicity, geo-replication, cost, or end-to-end latency?
3. Where must ordering hold: globally, per key, or only within a local processing step?
4. What is the replay model: full retention, compacted snapshots, time-bounded backfills, or one-shot delivery?
5. Which guarantees are required: at-most-once, at-least-once, or business-level exactly-once with idempotent sinks?
6. Which downstream systems consume the stream: lakehouse tables, warehouses, search, caches, APIs, or ML features?
7. What is the operational baseline: small team, platform team, managed service, or self-hosted multi-region cluster?

## Default Workflow (Use Unless User Overrides)

1. Choose the backbone first with `references/platform-selection.md`.
2. Define topic, key, retention, replay, and schema strategy before discussing processors. Use `assets/topic-contract-template.md`.
3. Choose the processing model with `references/stream-processing-patterns.md`: pass-through, enrich, aggregate, join, dedupe, or CDC normalization.
4. Lock CDC and schema-governance rules with `references/cdc-and-schema-governance.md` and `assets/cdc-rollout-checklist.md`.
5. Define delivery and sink behavior: upserts, deletes, late data, watermarking, and reprocessing boundaries.
6. Add SLOs, lag monitoring, checkpoint and savepoint policy, and incident drills with `references/operations-and-slos.md`.
7. Score tradeoffs explicitly with `assets/streaming-platform-scorecard.md` when the user asks for the "best" platform.

## ASCII Flow

```text
streaming data request
  -> classify need: events, CDC, enrichment, analytics, or low-latency delivery
  -> choose backbone: Kafka-compatible, Pulsar, Kinesis, or managed service
  -> define topics: owner, key, partitions, retention, replay, schema
  -> choose processor: pass-through, enrich, join, aggregate, dedupe, CDC normalize
  -> define sink semantics: idempotency, deletes, late data, reprocessing
  -> add SLOs, lag alerts, checkpoints, DLQ/retry, and incident drills
  -> document tradeoffs and verify managed-service behavior
```

## Default Baseline

- Backbone: Kafka-compatible event log unless a clear managed-service or multi-tenant requirement pushes elsewhere
- Stream processing: Flink for stateful event-time pipelines; Kafka Streams for lighter in-app processing
- CDC: log-based CDC first; avoid trigger-based CDC unless constraints force it
- Contracts: registry-backed schemas for shared or long-lived topics
- Reprocessing: plan for replay before launch; do not treat backfills as exceptional
- Sinks: design sink idempotency explicitly; "exactly-once" claims are incomplete without sink behavior

## Backbone Decision Table

| Requirement | Kafka (self-hosted) | Redpanda | WarpStream / AutoMQ | Pulsar | Kinesis |
|---|---|---|---|---|---|
| Broadest connector/CDC ecosystem | best | good | good (Kafka API) | limited | limited |
| Operational simplicity | poor (ZK removed in 4.x, KRaft only) | good (single binary) | best (serverless or S3-backed) | poor | best |
| Cost at high throughput | medium | medium | lowest (storage on S3) | medium | high (shard cost) |
| Multi-tenancy / namespace isolation | limited | limited | limited | best | AWS-only |
| Geo-replication built-in | via MirrorMaker 2 | via MirrorMaker 2 | limited | native | AWS-only |
| Kafka API compatibility | canonical | full | full | partial | no |
| Queue semantics (share groups) | 4.2+ GA | roadmap | roadmap | native | no |
| Cloud portability | high | high | medium (S3 dependency) | high | none |

**WarpStream context (July 2026):** Confluent acquired WarpStream (Sept 2024); IBM completed its $11B acquisition of Confluent on March 17, 2026 — WarpStream is now part of IBM's streaming portfolio. Production customers: Grafana Labs, Cursor, Robinhood. AutoMQ production: JD.com (13T msgs/day), Grab, HubSpot.

## Exactly-Once Decision Path

```text
Need exactly-once?
  -> Is the sink idempotent or transactional?
       No  -> Add sink-level deduplication key or upsert semantics first
       Yes -> Enable broker/processor exactly-once:
                Kafka: enable.idempotence=true + transactional.id
                Flink: CheckpointingMode.EXACTLY_ONCE + two-phase commit sink
  -> Does the sink support two-phase commit?
       No  -> Business-level idempotency (dedupe key + conditional write)
       Yes -> End-to-end exactly-once boundary confirmed
  -> Document the exact guarantee boundary — broker, processor, AND sink
```

## Kafka Version Quick-Ref (July 2026)

| Version | Released | Key change |
|---|---|---|
| 4.0 | March 2025 | ZooKeeper removed; KRaft-only; KIP-848 next-gen consumer rebalance |
| 4.1 | ~mid 2025 | KIP-932 share groups protocol/schema stabilized |
| 4.2 | Feb 2026 | KIP-932 (Queues/share groups) GA; performance/reliability |
| 4.3.0 | May 22 2026 | 25 KIPs, 600+ commits |
| 4.3.1 | Jun 25 2026 | Patch release; fixes ~15 issues including a critical Kafka Streams RocksDB native memory leak — latest stable |

**KRaft migration note:** All 4.x clusters are KRaft-only. Controller quorum sizing differs from ZooKeeper ensemble sizing — do not map 1:1. Migrate non-production first; use the provided migration tool; verify controller quorum before cutting over.

**KIP-932 (Queues for Kafka):** GA as of 4.2. Share groups allow multiple consumers to cooperate on the same partition with per-record acknowledgment — enables queue semantics without strict partition-per-consumer assignment. Evaluate for fan-out and task-queue workloads that previously required topic-per-consumer workarounds.

## Flink Version Quick-Ref (July 2026)

| Version | Status | Notes |
|---|---|---|
| 2.3.0 (Jun 25 2026) | latest stable | Changelog conversion SQL operators (`FROM_CHANGELOG`/`TO_CHANGELOG`); redesigned native S3 filesystem on AWS SDK v2; adaptive partition selection for backpressure; ordered late-data handling for Process Table Functions |
| 2.2.0 (Dec 2025) | stable | Real-time data + AI integrations; Paimon integration |
| 2.0.x (2.0.2, May 11 2026) | stable/maintained | Disaggregated state (remote primary storage); async execution model; Materialized Tables GA |
| 1.x | EOL path | Savepoints not forward-compatible with 2.x without explicit migration |

**Upgrade rule:** Audit savepoints before upgrading from 1.x — checkpoint format changed. Review connector compatibility. Validate SQL Gateway behavior for complex queries before migrating Table API jobs.

## Iceberg Streaming Ingestion Pattern (June 2026)

Standard production stack: Kafka -> Flink (Dynamic Iceberg Sink) -> Iceberg table -> compaction job.

```
# Flink Dynamic Iceberg Sink — baseline config
checkpoint.interval = 5 min          # drives commit frequency
write.target-file-size-bytes = 128MB  # reduces small-file problem
write.fanout.enabled = true           # unordered writes across partitions
schema-registry.compatibility = FULL_TRANSITIVE
# Compaction: run on cold partitions; skip hot (current) partition
```

- Every streaming approach produces small files — pair ingestion with a scheduled compaction job.
- 5-minute checkpoint interval produces ~90% fewer small files vs 1-minute.
- Iceberg v3 (ratified): deletion vectors, row lineage (`_row_id`), variant data, default column values, geometry/geography types, nanosecond timestamps, encryption foundations. GA on Snowflake (May 7, 2026) and Databricks Runtime 18.0+ (Unity Catalog, all clouds). Trino is not yet v3-ready as of mid-2026 — verify per-engine v3 support before committing a multi-engine stack to v3 features.

## Quick Reference

| Task | Resource | When to Use |
|------|----------|-------------|
| Choose Kafka vs Redpanda vs Pulsar vs Kinesis | `references/platform-selection.md` | New platform selection or platform migration |
| Choose Flink vs Kafka Streams vs Spark | `references/stream-processing-patterns.md` | Stateful processing, joins, windows, or low-latency transforms |
| Design CDC and schema evolution | `references/cdc-and-schema-governance.md` | Debezium, snapshots, tombstones, contracts, registry policy |
| Define lag, replay, failover, and checkpoint policy | `references/operations-and-slos.md` | Production hardening and incident prevention |
| Draft topic naming, keys, retention, and schema rules | `assets/topic-contract-template.md` | New topic or shared event contract |
| Plan a CDC rollout safely | `assets/cdc-rollout-checklist.md` | Database-to-stream launch or CDC migration |
| Compare platform options side by side | `assets/streaming-platform-scorecard.md` | Decision reviews and recommendation memos |

## Operating Principles

### 1. Ordering Is Scoped, Not Global

- Promise ordering only where the platform can really preserve it, usually per partition and key.
- If the business process needs entity-level sequencing, make the key choice explicit.

### 2. Schemas Are Contracts

- Shared topics need governed evolution rules, owners, compatibility mode, and deprecation windows.
- Plain JSON is acceptable for prototyping, not for durable shared interfaces.

### 3. Replay Is A First-Class Operation

- Retention, compaction, checkpoints, and sink idempotency define whether replay is safe.
- Do not ship a pipeline that cannot be re-run after bad code or bad data.

### 4. "Exactly-Once" Is End-To-End, Not A Checkbox

- Broker or processor guarantees are insufficient if the sink can duplicate writes or mishandle deletes.
- State the exact boundary where deduplication or transactional guarantees end.

### 5. CDC Needs Delete And Snapshot Strategy

- Decide how snapshots, schema changes, tombstones, and source failover behave before launch.
- Downstream consumers must know whether deletes arrive as tombstones, hard deletes, or soft-delete flags.

## Templates

- `assets/topic-contract-template.md`
- `assets/cdc-rollout-checklist.md`
- `assets/streaming-platform-scorecard.md`

## Known Traps

- Designing the event backbone around broker features before defining domain ownership, event contracts, and replay expectations.
- Treating topic retention as a substitute for a durable system of record, replay plan, or downstream recovery workflow.
- Claiming exactly-once behavior without specifying the guarantee boundary across broker, processor, sink, and side effects.
- Mixing operational events, analytical CDC, and integration commands into the same topics without independent retention, schema, and consumer-SLA rules.
- Shipping CDC streams without idempotency keys, snapshot semantics, tombstone handling, and late-arrival rules agreed by consumers.
- Scaling partitions, consumer groups, and stateful processors independently and then discovering the keying model breaks ordering or hotspot behavior.

### Kafka 4.x KRaft-only

Kafka 4.0+ is KRaft-only — no ZooKeeper path exists. Controller quorum sizing differs from ZooKeeper ensemble sizing; do not map 1:1. Migrate non-production first; validate quorum before cutting over production. Latest stable: 4.3.1 (Jun 25, 2026) — a patch release; upgrade past 4.3.0 promptly if running Kafka Streams, since 4.3.0 shipped a RocksDB native memory leak. KIP-932 share groups (queue semantics) are GA as of 4.2.

### Flink 2.x

Flink 2.0 changed checkpoint format and removed deprecated 1.x APIs. Savepoints from 1.x require explicit migration before restoring on 2.x state backends. Audit savepoints and connector compatibility before upgrading. Latest stable: 2.3.0 (Jun 25, 2026), which adds changelog-conversion SQL operators and a redesigned native S3 filesystem. Disaggregated state (remote primary storage) and Materialized Tables are production features since the 2.0.x line.

## Common Anti-Patterns

- Using the stream platform as a generic dumping ground for every event rather than curating contracts by domain and use case.
- Putting business-critical enrichment or policy decisions in opaque stream jobs with no replay procedure, lineage, or owner.
- Letting producers evolve schemas opportunistically while expecting consumers to absorb breaking changes.
- Building low-latency pipelines on top of unstable event keys, non-deterministic joins, or external side-effect calls inside hot-path processors.
- Choosing real-time processing because it sounds strategic when batch or micro-batch would meet the product and cost requirements.
- Treating DLQs as the main error-handling strategy instead of fixing classifier logic, validation, backpressure, and recovery paths upstream.

## Navigation

- [references/platform-selection.md](references/platform-selection.md) — Load when choosing between Kafka, Redpanda, Pulsar, Kinesis, or managed offerings; includes decision axes and recommendation protocol.
- [references/stream-processing-patterns.md](references/stream-processing-patterns.md) — Load when designing topology, windows, joins, deduplication, or delivery semantics.
- [references/cdc-and-schema-governance.md](references/cdc-and-schema-governance.md) — Load when building CDC pipelines, handling deletes/tombstones, or setting schema registry policy.
- [references/operations-and-slos.md](references/operations-and-slos.md) — Load when defining SLOs, dashboards, incident patterns, or consumer commit/DLQ policy.
- [references/engine-table-format-state.md](references/engine-table-format-state.md) — Load when reasoning about Iceberg v3, Paimon, or Kafka KIP-1150 diskless status.
- [references/control-theory-applied.md](references/control-theory-applied.md) — Load when designing lag-aware autoscalers, producer flow control, or watermark tuning.
- [references/queueing-theory-applied.md](references/queueing-theory-applied.md) — Load when sizing partitions, modeling lag SLOs, or scaling coordinator throughput.
- [references/distributed-systems-applied.md](references/distributed-systems-applied.md) — Load when reasoning about ISR quorum, exactly-once via idempotency, leader-epoch fencing, or consumer-group rebalance correctness.
- `data/sources.json` — Primary-source URLs for all platforms, processors, CDC tools, and table formats.

## Current-Source Policy

- Prefer `trust_tier: primary` entries in `data/sources.json` for platform capabilities, service limits, compatibility, and release-sensitive behavior.
- For recommendation questions, verify current managed-service behavior, connector support, quotas, and pricing from official docs instead of relying on frozen comparisons.
- Separate verified facts from judgment calls when comparing Kafka, Redpanda, Pulsar, Kinesis, Flink, and managed offerings.
- If web access is unavailable, say the recommendation is partially unverified.

## Related Skills

- [data-lake-platform](../data-lake-platform/SKILL.md) for storage formats, catalogs, serving layers, and lakehouse architecture
- [data-analytics-engineering](../data-analytics-engineering/SKILL.md) for marts, semantic layers, and metric governance on top of streaming data
- [data-sql-optimization](../data-sql-optimization/SKILL.md) for database-side performance and transactional operations
- [software-architecture-design](../software-architecture-design/SKILL.md) for application eventing, CQRS, and domain architecture
- [ops-devops-platform](../ops-devops-platform/SKILL.md) for deployment, infra automation, and runbook operations

## Fact-Checking

- Use web search or web fetch to verify current external facts, versions, managed-service behavior, quotas, pricing, and release-specific capabilities before final answers.
- Prefer primary sources; include source links and dates for volatile recommendations.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

