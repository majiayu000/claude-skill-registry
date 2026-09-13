---
name: ln-23-system-design-proposal-builder
description: "Designs target system boundaries, contracts and tradeoffs from requirements; does not plan tasks or implement."
---

# System Design Proposal Builder

**Goal:** Create a proportionate, evidence-backed target system design that turns requirements into explicit boundaries, contracts, data flow, failure behavior, operations, and tradeoffs. Change only the approved design document; do not implement, audit, or approve the delivery.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Requirements and constraints | Approved requirements, baseline, decisions, and direct stakeholder input | Mark material gaps and ask the smallest decision question |
| Current implementation and conventions | Repository search, manifests, entrypoints, and architecture artifacts | Treat as greenfield only when the user or repository establishes that fact; otherwise mark current state `UNKNOWN` and return `REVISE` or `BLOCKED` when the gap can change boundaries, compatibility, or migration |
| External capabilities and limits | Current official documentation and specifications | Mark claims `UNVERIFIED`; avoid vendor-dependent commitment |
| Estimates | Reproducible arithmetic from sourced workload assumptions | Use ranges and sensitivity; never present estimates as measurements |
| Document mutation | Minimal patch to the approved target-design artifact | Return `BLOCKED` if scope or path is unsafe |

Use patterns as candidate solutions, not goals. Introduce infrastructure only when a requirement, failure mode, ownership boundary, or measured horizon pays for its lifecycle cost.

## Artifact Rules

- Reuse a clear target-design document; otherwise use `docs/architecture/target-design.md`.
- Read available baseline, current-state, decision, interface, diagram, and migration artifacts by path; none is mandatory.
- Label facts, assumptions, estimates, proposed decisions, and unresolved choices separately.
- Compare credible alternatives for consequential decisions, including the simplest feasible option; when constraints permit only one, document why rather than inventing another.
- Prefer reversible choices and the simplest topology fitting the system. For a new application, consider a modular monolith before independent services; do not force that shape onto libraries, plugins, or an established topology.
- Do not silently change an accepted decision; record the conflict and required governance action.

## Checklist

### 1. Frame the Design

- [ ] Resolve business outcome, actors, journeys, scope, non-goals, horizon, readers, language, and the approved canonical destination before editing.
- [ ] Read repository instructions and inspect relevant architecture artifacts and current implementation.
- [ ] Extract functional requirements and measurable quality drivers, preserving their source and status.
- [ ] Identify architecture-critical unknowns and ask only questions whose answers change the target shape.
- [ ] Return `BLOCKED` when a required business boundary or safety constraint cannot be responsibly assumed.

### 2. Estimate Before Choosing Components

- [ ] Estimate average and peak request or event rates, concurrency, payload and bandwidth, storage growth, retention, and recovery volume where relevant.
- [ ] Show formulas, ranges, growth horizon, and assumptions; identify the variables that can reverse a choice.
- [ ] Identify likely first bottlenecks and explicit thresholds for deferred scaling mechanisms.
- [ ] Separate availability, latency, durability, consistency, security, cost, and operability requirements from implementation preferences.
- [ ] Reject speculative scale and list complex mechanisms intentionally deferred.

### 3. Define Domains, Data, and Contracts

- [ ] Map business capabilities, domains or modules, ownership, invariants, and allowed dependency direction.
- [ ] Define systems of record, data models at architecture depth, lifecycle, retention, consistency, and transaction boundaries.
- [ ] Define public APIs, events, commands, schemas, errors, idempotency, ordering, versioning, and compatibility expectations.
- [ ] Define trust boundaries, identities, authorization, sensitive data, secrets, abuse controls, and audit needs proportionate to risk.
- [ ] Keep framework and vendor details outside the core model unless they are genuine constraints.

### 4. Build HLD and Critical LLD

- [ ] Describe system context, deployable units, stores, queues, external systems, responsibilities, and labeled data flows.
- [ ] Trace success, overload, dependency failure, partial failure, retry, timeout, degradation, recovery, and cancellation for critical journeys.
- [ ] Deep-dive only components whose correctness, scale, security, or reversibility risk warrants implementation-level detail.
- [ ] Define observability, SLI measurement points, health, deployment strategy, rollback, backup, and operator actions.
- [ ] Define ownership, team impact, cost drivers, and operational burden for the proposed topology.

### 5. Decide and Validate

- [ ] Compare credible alternatives against requirements, estimates, failure behavior, complexity, cost, migration, and future triggers.
- [ ] State selected and rejected options with consequences, sensitivity points, and assumptions that would reopen the decision.
- [ ] Identify significant decisions that deserve their own compact decision records without requiring another workflow.
- [ ] Define architecture acceptance evidence appropriate to each material driver: contract checks, load/failure experiments, security validation, recovery proof, or observability signals. Specify prerequisites and pass criteria; do not execute them during design.
- [ ] Outline current-to-target implications and compatibility needs without expanding into a full implementation plan.

### 6. Write and Report

- [ ] Write context, drivers, estimates, domains, contracts, HLD, critical LLD, failure and operations model, security, alternatives, decisions, validation, open questions, and evolution triggers.
- [ ] Preserve existing content outside the approved scope and link shared artifacts only by document path or title.
- [ ] Re-read the proposal for unsupported facts, hidden decisions, mixed abstraction, and unjustified machinery.
- [ ] Use `READY` only when the design is decision-complete enough for implementation planning; use `REVISE` for material but solvable gaps; use `BLOCKED` when required intent, evidence, authority, or destination is unavailable.

- [ ] Demonstrate that each material design boundary is implementable: link source requirements to contracts, data, failure behavior, unresolved choices, and acceptance evidence; distinguish a ready proposal from an accepted decision.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Artifact path; requirements, estimates, boundaries, contracts, HLD/critical LLD, selected decisions, alternatives, evidence, and reopen triggers. Summarize validation/transition needs, compatibility, rollout, rollback, observability, and only unresolved choices that affect implementation planning.
