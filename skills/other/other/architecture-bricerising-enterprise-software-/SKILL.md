---
name: architecture
description: "Design or refactor multi-service system architecture (domain boundaries, service decomposition, event-driven vs request/response, CQRS, sagas, API gateways, data ownership). Use when work spans multiple processes/services, needs eventual consistency, or requires clearer integration seams. NOT for in-process code structure like GoF patterns (use design); NOT for applying timeouts/retries/breakers to a single call (use resilience)."
metadata: {"stage":"Define","tags":["system-patterns","distributed-systems","consistency","microservices","integration","domain-boundaries","event-driven","saga"],"aliases":["system-design","distributed","multi-service","cross-service","decomposition","bounded-context","technical-design-review"]}
---

# Architecture (System Pattern Chooser)

## Overview

Pick the smallest system/architecture pattern that addresses the pressure (reliability, consistency, domain boundaries, scalability).

Use code patterns for in-process structure; use system patterns when the problem is cross-process or cross-team.

## Workflow

0. **Gather empirical data** (required — wait for completion):
   - If `.archobs/file_metrics.parquet` already exists and is newer than the most recent commit, reuse it; otherwise run `archobs report --repo <path> --out .archobs --suggestions-provider rules` and **wait for the report to complete** before continuing.
   - Read results: `archobs show all --format json` (or query `archobs show risks`, `archobs show clusters` individually).
   - Use cluster leakage data to identify where boundaries are already porous.
   - Use file-level risk scores to focus on the highest-impact areas.
   - Skip this step only if the repo is too small (< 10 files) for meaningful analysis.

0b. **Ecosystem Pressure Check** (conditional — run when the architecture decision involves adopting or replacing a technology, defining boundaries around external dependencies, or planning work with a time horizon > 6 months):

   ```bash
   intel forecast    # external engine — lifecycle phases and chains
   ```

   **Decision mapping**: See [Lifecycle Decision Mapping — Architecture: Boundary Design](../references/lifecycle-decision-mapping.md#architecture-boundary-design) for lifecycle phase → boundary design tables and dynamic signal implications.

1. Externalize the system model:
   - objective function (goal, constraints, anti-goals)
   - boundary (in/out), time horizon, actors/incentives, and key flows
2. Classify the problem: single-process design vs multi-process/distributed.
3. Identify the main pressure (pick 1):
   - Reliability under partial failure (timeouts/retries/circuit breaker/bulkheads)
   - Data consistency across boundaries (saga, event sourcing, CQRS)
   - Domain complexity and ownership (bounded contexts, aggregates, repositories, domain events)
   - Scalable coordination (leader election, sharding)
   - Migration/integration (anti-corruption layer, strangler fig, API gateway/BFF)
   - Streaming/reactivity (pub/sub, reactive streams/backpressure)
   - ML lifecycle (data pipeline, feature store, canary/blue-green, transfer learning)
4. State what’s stable and what can change (contracts, schemas, SLAs).
5. Build a compact decision table (2–3 options including no-pattern baseline):
   - what each option optimizes
   - what each option knowingly worsens (degrades an existing quality)
   - explicit opportunity cost (what this option prevents us from doing or building)
   - kill criteria / reversal trigger
6. Stress-test the decision (if 2+ viable approaches exist; skip for single viable approach):
   - **Assumptions**: What are facts vs assumptions? Which assumption is least certain — how will we validate it? Cross-reference with ecosystem pressure check from step 0b (if applicable). *(attach to decision table)*
   - **Second-Order Effects**: What happens next week / next quarter / next year? What new load, toil, coupling, or failure mode? Which team absorbs the downside? Cross-reference with ecosystem pressure check from step 0b (if applicable). *(attach to system sketch)*
   - **Opportunity Cost**: What are we saying "no" to? Are we favoring this due to sunk cost, familiarity, or novelty? *(attach to decision table)*
   - If probe output already exists from an earlier Define-stage skill in this flow (including `workflow` orchestration), refine it instead of re-running.
   - Note: Feedback Loops are covered natively by step 9 (dynamics check). Pre-mortem is normally part of the Second-Order Effects probe but is already covered in step 8 (blast-radius path); do not duplicate either.
7. Choose a primary pattern and 0–2 supporting ones (avoid "pattern soup").
8. Stress-test with: happy path, failure path, ops path, and blast-radius path:
   - if X degrades, what breaks next?
   - what breaks silently?
   - what is the organizational cascade (handoffs/approvals/ownership gaps)?
   - pre-mortem: if this fails in 6-12 months, what likely caused failure?
9. Run a dynamics check:
   - where are delays (feedback, approvals, recovery)?
   - what accumulates (toil, backlog, queue lag, exceptions)?
   - what balancing loop prevents runaway growth?
   - cross-reference with ecosystem pressure check from step 0b (if applicable) for empirically detected reinforcing loops, delays, and accumulations that may confirm or challenge the qualitative assessment
10. Map to implementation tactics (often code-pattern wrappers/pipelines), testing strategy, and measurement ritual.

## Clarifying Questions

- What are the deployable units and trust boundaries (processes/services/teams)?
- Is failure partial (network timeouts, 5xx, queue backlog)? What are the SLOs?
- Do we require strong consistency, or is eventual consistency acceptable?
- Who owns each piece of data? What is the source of truth?
- What is the integration style: synchronous RPC, async events, or both?
- Do operations need to be idempotent? Do we have request IDs?
- What is the expected load profile (spikes, fan-out, long tails)?
- Can we tolerate duplication / reordering of messages?
- Where are the key delays between signal and action?
- What work or risk accumulates if this runs “hot” for weeks?
- What behavior might teams game once metrics are introduced?

## Pattern Chooser

### Cloud-Native / Microservices

- **Circuit Breaker**: stop cascading failures when a dependency is down/flaky.
- **Bulkhead**: isolate resource pools so one dependency can’t starve everything.
- **Saga**: multi-step business workflow across services with compensations.
- **API Gateway / BFF**: one entry point / client-specific API to avoid chatty clients.
- **API Composition**: implement a “distributed query” by aggregating responses from multiple services.
- **Database per Service**: keep each service’s data private; integrate via APIs and domain events.
- **Service Discovery (client-side/server-side) + Service Registry**: route service-to-service calls without hardcoding hostnames.
- **Externalized Configuration**: keep per-environment config outside the deployable artifact.
- **Health Check API**: standardize liveness/readiness signals for orchestration and ops.
- **Service Mesh**: offload retries/mTLS/routing/telemetry to infrastructure (still own correctness at the app layer).
- **Sidecar / Ambassador**: move cross-cutting networking concerns out of the app process (mesh/proxy).
- **Strangler Fig**: migrate a monolith incrementally by routing slices to new services.

### Functional / Safer Flow

- **Immutability & pure functions**: reduce shared state; make concurrency and testing easier.
- **Higher-order functions & composition**: prefer passing behavior directly over object-heavy indirection.
- **Option/Maybe (and Either/Result)**: make absence and expected failures explicit (avoid `null`).

### Reactive / Event-Driven

- **Pub/Sub**: decouple producers/consumers via events.
- **Transactional outbox + idempotent consumer (inbox)**: avoid dual-write bugs; make at-least-once delivery safe with dedupe.
- **Reactive streams + backpressure**: prevent fast producers from overwhelming slow consumers.
- **Event Sourcing**: store events as source of truth; rebuild state by replay.
- **CQRS**: separate command (write) model from query (read) model.
- **Command-side replica**: replicate reference data into the command service to avoid synchronous cross-service reads.

### Domain-Driven Design (DDD)

- **Bounded Context**: define model boundaries + translations/anti-corruption layers.
- **Aggregate**: enforce invariants within a consistency boundary.
- **Repository**: hide persistence behind an in-memory collection-like interface.
- **Domain Events**: publish business facts; decouple side effects.
- **Anti-Corruption Layer**: translate external/legacy concepts to protect your domain.
- **Hexagonal architecture (ports & adapters)**: keep domain core independent from infrastructure.

### Distributed Coordination & Scale

- **Actor model**: concurrency via message-passing, isolation, supervision.
- **Leader election**: choose a single coordinator for exclusive work.
- **Sharding**: partition data/work across nodes.
- **Idempotency + retries/backoff**: tolerate duplicates and transient failures safely.
- **MapReduce**: batch/distributed processing by map then reduce.

### AI/ML Lifecycle

- **Data pipeline (batch vs streaming; lambda/kappa)**: move data reliably into training/serving.
- **Feature store**: single source of truth for feature definitions/serving.
- **Transfer learning**: adapt a pre-trained model instead of training from scratch.
- **Blue-green/canary model deploys**: reduce risk when shipping new model versions.

## Map To Existing Skills

- Empirical coupling data and boundary health metrics: [`archobs`](../archobs/SKILL.md).
- Spec + contracts + plans: [`spec`](../spec/SKILL.md).
- Shared primitives across services: [`platform`](../platform/SKILL.md).
- Observability (logs/metrics/traces correlation): [`observability`](../observability/SKILL.md).
- Timeouts / retries / idempotency / circuit breaker / bulkheads: [`resilience`](../resilience/SKILL.md) (often implemented via `Proxy`/`Decorator`).
- Circuit breaker / caching / rate limiting (in-process structure): often a `Proxy` or `Decorator` ([`patterns-structural`](../patterns-structural/SKILL.md)).
- Saga orchestration: often a `State` machine + `Command` objects ([`patterns-behavioral`](../patterns-behavioral/SKILL.md)).
- Pub/sub + domain events: `Observer` ([`patterns-behavioral`](../patterns-behavioral/SKILL.md)).
- Hexagonal architecture: ports are interfaces; adapters are often `Adapter` or `Facade` ([`patterns-structural`](../patterns-structural/SKILL.md)).
- Option/Result: aligns with typed error boundaries ([`typescript`](../typescript/SKILL.md)).

## References

- Decision tree (pressure → patterns → risks): [`references/decision-tree.md`](references/decision-tree.md)
- Pattern index (one file per pattern): [`references/patterns.md`](references/patterns.md)
- Structured-thinking probes + templates: [`../references/`](../references/) (checklists for inline probes, templates for escalation)

## Output Template

When recommending a pattern:

- 1–2 sentences: pattern + why it fits (pressure, assumptions).
- Decision table summary: options considered, explicit trade-offs, kill criteria, and assumptions (facts vs assumptions).
- Blast-radius + dynamics notes: failure propagation, silent failures, feedback loops, delays, accumulations, pre-mortem cause.
- A minimal implementation plan (boundaries, contracts, data ownership, tests/metrics, and review ritual owner/cadence).
