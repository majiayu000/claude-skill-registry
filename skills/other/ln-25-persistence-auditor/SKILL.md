---
name: ln-25-persistence-auditor
description: "Audits queries, transactions, data-path performance, and persistence resource lifecycle. Use when data correctness or scalability is at risk; not for general performance tuning."
---

# Persistence Auditor

Perform a read-only audit of persistence and data-heavy runtime paths. Connect static candidates to real query, transaction, resource, or consistency mechanisms and avoid claiming performance impact without evidence.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Data-layer map | Native file search over manifests, models, mappings, repositories, migrations, queries, cache, queue, and pool configuration | Establishing stores, frameworks, ownership, and scope | Trace from known request, job, or command entrypoints |
| Call paths and resource ownership | Language server or host-native code intelligence | Following service calls, transaction boundaries, async flow, session scopes, and cleanup | Targeted search plus direct inspection of definitions and callers |
| Query behavior | Existing query logs, tracing, ORM diagnostics, and application metrics | Establishing frequency, duplication, timing, rows, and cache behavior | Static query-in-loop and fetch-shape analysis with explicit limits |
| Query plans | Database-native explain tooling on an approved non-production target | A safe read query and representative schema/data are available | Inspect indexes, predicates, joins, statistics assumptions, and generated SQL statically |
| Runtime performance | Existing profiler, benchmark, or repository diagnostic command | Allocation, blocking, loop amplification, or I/O cost needs measurement | Complete static cost path marked as unmeasured |
| Correctness verification | Repository-defined tests, integration environment, and migration checks | Reproducing transaction, retry, consistency, or lifecycle behavior safely | Static failure trace and required verification plan |
| External semantics | Official database, driver, framework, and runtime documentation matching installed versions | Isolation, pooling, cancellation, caching, trigger, or async semantics affect a finding | Primary-source web research; otherwise mark `UNVERIFIED` |

Never connect to production or run mutating diagnostics. `EXPLAIN ANALYZE` executes the statement: use it only for confirmed read-only queries on an approved disposable or non-production target. Do not create indexes, migrate, vacuum, rewrite data, or change pool settings during the audit.

## Evidence Rules

- Query count, duration, rows, plan, lock, or profile evidence is stronger than a static performance suspicion.
- Static evidence can prove correctness and lifecycle defects when the full path is visible, but performance impact must be labeled unmeasured.
- ORM conventions, bounded administrative paths, startup-only work, and intentionally small datasets require context before becoming findings.
- Transaction advice must match the actual database, isolation level, driver, framework, and retry model.
- Recommendations must preserve data integrity and failure semantics, not only reduce latency.

## Checklist

### 1. Establish the Data and Runtime Context

- [ ] Detect databases, ORMs, drivers, caches, queues, schemas, migrations, pools, dependency-injection scopes, and runtime entrypoints in scope.
- [ ] Resolve installed versions, database capabilities, deployment topology, consistency requirements, and expected workload from repository evidence.
- [ ] Identify critical data paths, high-volume paths, streaming paths, scheduled work, and operations that hold transactions or resources across external calls.
- [ ] Read repository instructions and inspect Git state before running diagnostics or interpreting current work.
- [ ] Establish available query logs, metrics, traces, profiles, representative data, test environments, and safe diagnostic permissions.
- [ ] Keep the audit read-only and document every executed query, command, target, and artifact created.

### 2. Audit Query and Cache Efficiency

- [ ] Trace representative paths from entrypoint through business logic to generated query and materialization.
- [ ] Find N+1 behavior, repeated identical fetches, query-in-loop patterns, sequential independent reads, and redundant existence or count queries.
- [ ] Check over-fetching, broad entity loading, unbounded reads, premature materialization, missing pagination, and user-controlled result amplification.
- [ ] Check missing bulk operations, per-row writes, avoidable round trips, fragmented commits, and opportunities for set-based work.
- [ ] Inspect predicates, joins, sort and group operations, index alignment, query-plan assumptions, and statistics only with schema and workload context.
- [ ] Check cache ownership, key design, scope, invalidation, stampede control, negative caching, staleness tolerance, and duplication with database guarantees.
- [ ] Distinguish latency caused by query shape, connection wait, locks, network, serialization, application work, or downstream services before recommending a fix.
- [ ] Measure or clearly label the expected impact; do not present a candidate index or cache as a proven optimization.

### 3. Audit Transactions and Consistency

- [ ] Identify who begins, commits, rolls back, retries, and disposes each transaction and whether ownership matches the business operation.
- [ ] Check atomicity across related writes, early commits, missing rollback, swallowed exceptions, nested transaction behavior, and partial-success states.
- [ ] Find long-held transactions, network or file calls inside transactions, user interaction during locks, and transactions spanning unnecessary computation.
- [ ] Check isolation assumptions, lost updates, write skew, duplicate processing, optimistic or pessimistic locking, and retry safety.
- [ ] Verify idempotency keys, unique constraints, deduplication, outbox or inbox behavior, and at-least-once delivery paths where applicable.
- [ ] Check triggers, notifications, events, and subscribers for naming, commit-time visibility, payload compatibility, ordering, duplicate delivery, and orphan consumers; do not add intermediate commits merely to expose progress if that breaks business atomicity.
- [ ] Check migrations and backfills for transactional behavior, lock duration, mixed-version compatibility, resumability, and failure recovery.
- [ ] Verify recommendations against official semantics for the installed database, driver, and framework when behavior is version-sensitive.

### 4. Audit Runtime and Resource Lifecycle

- [ ] Check blocking database, filesystem, or network I/O in asynchronous paths and synchronous waits that can starve workers or event loops.
- [ ] Check repeated allocation, copying, serialization, string building, conversion, and collection growth on data-heavy loops.
- [ ] Trace sessions, connections, cursors, readers, streams, locks, subscriptions, and temporary files through success, error, timeout, cancellation, and streaming completion.
- [ ] Include consumer abandonment and partial enumeration: generators, async iterators, streaming responses, and client disconnects must release resources even when normal completion never occurs.
- [ ] Check dependency-injection scope against resource lifetime, especially singleton access to scoped state and request resources held by background or streaming work.
- [ ] For background, streaming, or otherwise longer-lived work, verify bounded resource ownership and acquisition at the point of need instead of retaining a shorter-lived session or connection; a passed factory or pool is one valid design, not a universal requirement.
- [ ] Inspect pool size, timeouts, acquisition, validation, recycling, leak evidence, and the total connection budget across replicas, processes, workers, and failover capacity—not only one process's setting.
- [ ] Check cancellation propagation, command timeouts, retry storms, circuit behavior, and cleanup between retry attempts and after abandoned work.
- [ ] Check ORM expiration, lazy loading, detached entities, and implicit autoflush so no query or write occurs outside the intended session or transaction lifetime.
- [ ] Use runtime measurements where available to separate hot paths from low-frequency or bounded code before assigning performance severity.

### 5. Validate Findings and Report

- [ ] Reproduce high-severity correctness defects with a safe test or complete failure trace and performance defects with query, plan, lock, or profile evidence where possible.
- [ ] Filter framework-managed lifecycle, bounded maintenance tasks, fixtures, migrations kept for history, and documented consistency tradeoffs before confirming findings.
- [ ] Deduplicate symptoms that share one root query, transaction boundary, scope mismatch, or pool configuration.
- [ ] Classify findings as `P0`-`P3` based on data corruption, security, outage risk, scalability, latency, resource exhaustion, and recurrence.
- [ ] Include call path, query or resource, evidence, failure or cost mechanism, impact, confidence, and smallest safe remediation.
- [ ] Use `BLOCKED` when a critical data path, database semantic, or required non-production environment cannot be verified without a credible fallback; use `FAIL` for an evidenced unresolved corruption, atomicity, outage, resource-exhaustion risk, required failing gate, or another `P0/P1`; use `CONCERNS` only for evidenced non-blocking risk or material unmeasured uncertainty, and `PASS` only when critical paths are trustworthy with no material finding.
- [ ] Return the verdict with measured and static scope separated, remediation order, limitations, and residual persistence risks.

## Output Contract

```markdown
# Persistence Audit

**Verdict:** PASS | CONCERNS | FAIL | BLOCKED

## Data context and evidence
- Stores, frameworks, versions, and deployment topology
- Critical and measured paths
- Diagnostics, commands, and environments used

## Health summary
| Area | Status | Evidence basis |
|---|---|---|
| Query and cache efficiency | PASS / CONCERNS / FAIL | measured / static |
| Transactions and consistency | PASS / CONCERNS / FAIL | ... |
| Runtime performance | PASS / CONCERNS / FAIL | measured / static |
| Resource lifecycle | PASS / CONCERNS / FAIL | ... |

## Findings
### [P0 | P1 | P2 | P3] Finding title
- Call path, query, transaction, or resource
- Evidence and confidence
- Failure or cost mechanism
- Required change and verification

## Measurement gaps and residual risks
Unmeasured candidates, unavailable environments, and accepted consistency tradeoffs.
```
