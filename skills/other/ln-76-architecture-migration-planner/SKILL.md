---
name: ln-76-architecture-migration-planner
description: "Plans a reversible architecture migration with compatibility, data movement, rollout, and rollback. Use for current-to-target transitions; not execution, generic planning, or delivery review."
---

# Architecture Migration Planner

**Goal:** Create a safe, reversible transition from an evidenced current architecture to an explicit target architecture. Change only the approved migration document; do not execute migrations, edit product code, build a generic task plan, approve delivery, or hide irreversible steps.

**Execution contract:** Treat the ordered checkbox workflow below as this skill's Definition of Done. Work through every item in order, and mark it complete only when its action and required evidence are complete. `N/A`, skipped, unavailable, or delegated items remain incomplete.
Before returning, apply this skill's verdict and approval rules to every incomplete item and prepend **Checklist: X/Y complete**<br>**Incomplete: None | section/item — reason; outcome impact; exact next action**; list every incomplete item.

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
- Separate preparation, coexistence, migration, cutover, stabilization, and removal.
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
- [ ] Use expand/migrate/contract for schema and data-shape changes; keep additive and destructive operations in separate releases.
- [ ] Define backfill selection, batching, throttling, idempotency, checkpoints, retries, reconciliation, and correctness oracle.
- [ ] Define source of truth during coexistence and conflict handling for concurrent writes.
- [ ] Define backup, restore, RPO/RTO impact, privacy, retention, and audit evidence for data movement.

### 4. Build Reversible Phases

- [ ] Define preparation, shadow or coexistence, progressive migration, cutover, stabilization, and old-path removal as independently verifiable phases.
- [ ] For every phase, state prerequisites, changed architecture state, owner, entry gate, observable success, abort condition, rollback or roll-forward action, and exit evidence.
- [ ] Define feature flags, routing controls, canary cohorts, rate limits, maintenance windows, and blast-radius controls where justified.
- [ ] Define metrics, logs, traces, reconciliation reports, dashboards, alerts, and SLO gates needed before traffic or data movement.
- [ ] Keep old and new versions interoperable through realistic deployment ordering and rollback windows.

### 5. Plan Cutover and Removal

- [ ] Define go/no-go authority, communication, freeze conditions, exact cutover control, and immediate verification.
- [ ] Define rollback boundaries separately for code, configuration, traffic, schema, and already-migrated data.
- [ ] Require measured zero use, migrated consumers, retention expiry, and explicit approval before destructive removal.
- [ ] List old code paths, contracts, flags, adapters, jobs, data, infrastructure, dashboards, and documentation to remove.
- [ ] Define post-cutover observation period, ownership handoff, incident response, and closure evidence.

### 6. Write and Report

- [ ] Write transition summary, state gap, dependencies, compatibility, data plan, phased sequence, gates, observability, rollback, removal, owners, assumptions, and open decisions.
- [ ] Link shared artifacts by stable repository path or title without requiring a particular workflow.
- [ ] Re-read every phase for unsupported zero-downtime, zero-loss, consumer, capacity, or reversibility claims.
- [ ] Confirm no migration, code, test, deployment, task tracker, or external change was executed.
- [ ] Use `READY` only when phases are safely executable inputs to implementation planning; use `REVISE` for material compatibility, data, gate, or rollback gaps; use `BLOCKED` when current state, target state, authority, or safety evidence is unavailable.

## Output Contract

```markdown
# Architecture Migration Plan

**Verdict:** READY | REVISE | BLOCKED
**Artifact:** path

## State transition
- Current state, target state, gap, consumers, and invariants

## Phases
| Phase | Entry gate | Change | Success evidence | Abort condition | Rollback or roll-forward |
|---|---|---|---|---|---|

## Data, compatibility, and removal
- Coexistence, migration, reconciliation, cutover, and zero-use proof

## Open decisions and residual risks
Only items that can change safety, ordering, or reversibility.
```
