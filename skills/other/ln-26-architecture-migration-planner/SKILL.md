---
name: ln-26-architecture-migration-planner
description: "Plans architecture migrations with compatibility, data safety, rollout and recovery; does not execute them."
---

# Architecture Migration Planner

**Goal:** Plan a safe transition from evidenced current architecture to an explicit target, with reversibility limits and recovery actions. Change only the approved migration document; do not execute migrations, edit product code, build a generic task plan, approve delivery, or hide irreversible steps.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Current and target states | Repository evidence plus approved architecture artifacts | Explicit user-provided states with limitations |
| Consumers and compatibility | Language intelligence, schema tools, config search, telemetry, and direct inspection | Conservative inventory marked `UNVERIFIED` |
| Data scale and runtime risk | Production metrics, checked-in reports, migrations, and workload evidence | Ranges with validation gates before execution |
| External migration constraints | Official vendor migration and compatibility guidance | Mark dependent phases `BLOCKED` or `UNVERIFIED` |
| Document mutation | Minimal patch to the approved migration-plan artifact | Return `BLOCKED` when authority or path is unclear |

A migration phase must leave the system in a supported state. Additive and reversible steps precede cutover; destructive cleanup follows verified zero use.

## Artifact Rules

- Reuse a clear architecture migration document; otherwise use `docs/architecture/migration-plan.md`.
- Treat current-state, target-design, baseline, decisions, diagrams, interfaces, and telemetry as optional shared evidence.
- Keep the plan architectural: phases, compatibility, data, topology, gates, rollback, ownership, and removal.
- Leave file-level implementation tasks to downstream planning.
- Never describe rollback as "revert" when data or external effects are not reversible.
- Give every destructive step explicit approval, backup, restoration, and zero-consumer evidence requirements.

## Checklist

### 1. Establish the Transition Contract

- [ ] Resolve migration scope, business outcome, current state, target state, non-goals, deadline or horizon, owners, and approved destination.
- [ ] Read repository instructions, Git state, relevant architecture artifacts, migrations, deployment configuration, and compatibility policies.
- [ ] Verify that current and target states are specific enough to compute a gap; return `BLOCKED` rather than invent either state.
- [ ] Identify protected user journeys, invariants, SLOs, recovery objectives, compliance duties, and change windows.
- [ ] Keep the run read-only except for the approved migration document.

### 2. Build the Gap and Dependency Map

- [ ] Inventory affected modules, deployables, data stores, schemas, APIs, events, configuration, infrastructure, and operational procedures.
- [ ] Inventory internal and external consumers, owners, versions, traffic, data volume, and evidence quality.
- [ ] Map current-to-target changes in boundaries, ownership, contracts, data, runtime topology, observability, and failure behavior.
- [ ] Identify shared mutable resources, sequencing dependencies, long-running work, mixed-version windows, and irreversible effects.
- [ ] Record unknown consumers or usage as migration risks; absence of search results is not zero usage.

### 3. Design Compatibility and Data Safety

- [ ] Define old/new contract compatibility, version negotiation, adapters, dual-read or dual-write behavior, and deprecation policy where relevant.
- [ ] Use expand/migrate/contract when mixed versions or online migration require coexistence; separate additive and destructive releases in that case. For an approved offline atomic transition, document the equivalent compatibility, recovery, and downtime controls.
- [ ] Define backfill selection, batching, throttling, idempotency, checkpoints, retries, reconciliation, and correctness oracle.
- [ ] Define source of truth during coexistence, concurrent-write conflict handling, and detection, retry, and reconciliation of partial dual-write failure; do not assume two writes are atomic.
- [ ] Define backup, restore, RPO/RTO impact, privacy, retention, and audit evidence for data movement.

### 4. Build Reversible Phases

- [ ] Define preparation, shadow or coexistence, progressive migration, cutover, stabilization, and old-path removal as independently verifiable phases.
- [ ] For every phase, state prerequisites, changed architecture state, owner, entry gate, observable success, abort condition, rollback or roll-forward action, and exit evidence.
- [ ] Define feature flags, routing controls, canary cohorts, rate limits, maintenance windows, and blast-radius controls where justified.
- [ ] Define metrics, logs, traces, reconciliation reports, dashboards, alerts, and SLO gates needed before traffic or data movement.
- [ ] Keep old and new versions interoperable through realistic deployment ordering and rollback windows.

### 5. Plan Cutover and Removal

- [ ] Define go/no-go authority, communication, freeze conditions, exact cutover control, and immediate verification.
- [ ] Define rollback boundaries separately for code, configuration, traffic, schema, and migrated data, including points of no return and roll-forward recovery when rollback would lose accepted writes.
- [ ] Before destructive removal, require usage evidence over a window covering relevant schedules and offline consumers, migrated consumers, applicable retention expiry, and explicit approval. A short zero-traffic sample cannot establish zero use.
- [ ] List old code paths, contracts, flags, adapters, jobs, data, infrastructure, dashboards, and documentation to remove.
- [ ] Define post-cutover observation period, ownership handoff, incident response, and closure evidence.

### 6. Write and Report

- [ ] Write transition summary, state gap, dependencies, compatibility, data plan, phased sequence, gates, observability, rollback, removal, owners, assumptions, and open decisions.
- [ ] Link shared artifacts by stable repository path or title without requiring a particular workflow.
- [ ] Re-read every phase for unsupported zero-downtime, zero-loss, consumer, capacity, or reversibility claims.
- [ ] Use `READY` only when phases are safely executable inputs to implementation planning; use `REVISE` for material compatibility, data, gate, or rollback gaps; use `BLOCKED` when current state, target state, authority, or safety evidence is unavailable.

- [ ] Link each transition unit to the protected requirement, current/target boundary, entry evidence, observed success, and irreversible point; identify dependent plans affected by a migration change.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Artifact path; current/target gap, consumers, dependencies, and protected invariants. Summarize phases with entry gates, changes, success evidence, abort conditions, rollback/roll-forward; data/coexistence/reconciliation/cutover/removal proof; and open decisions that affect safety, ordering, or reversibility.
