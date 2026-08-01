---
name: ln-73-system-design-proposal-builder
description: "Creates a decision-complete target system design from requirements and constraints. Use before implementation planning; not for requirements baselines, reviews, audits, or code changes."
---

# System Design Proposal Builder

**Goal:** Create a proportionate, evidence-backed target system design that turns requirements into explicit boundaries, contracts, data flow, failure behavior, operations, and tradeoffs. Change only the approved design document; do not implement, audit, or approve the delivery.

**Execution contract:** Treat the ordered checkbox workflow below as this skill's Definition of Done. Work through every item in order, and mark it complete only when its action and required evidence are complete. `N/A`, skipped, unavailable, or delegated items remain incomplete.
Before returning, apply this skill's verdict and approval rules to every incomplete item and prepend **Checklist: X/Y complete**<br>**Incomplete: None | section/item — reason; outcome impact; exact next action**; list every incomplete item.

## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Requirements and constraints | Approved requirements, baseline, decisions, and direct stakeholder input | Mark material gaps and ask the smallest decision question |
| Current implementation and conventions | Repository search, manifests, entrypoints, and architecture artifacts | Treat the design as greenfield and state the limitation |
| External capabilities and limits | Current official documentation and specifications | Mark claims `UNVERIFIED`; avoid vendor-dependent commitment |
| Estimates | Reproducible arithmetic from sourced workload assumptions | Use ranges and sensitivity; never present estimates as measurements |
| Document mutation | Minimal patch to the approved target-design artifact | Return `BLOCKED` if scope or path is unsafe |

Use patterns as candidate solutions, not goals. Introduce infrastructure only when a requirement, failure mode, ownership boundary, or measured horizon pays for its lifecycle cost.

## Artifact Rules

- Reuse a clear target-design document; otherwise use `docs/architecture/target-design.md`.
- Read available baseline, current-state, decision, interface, diagram, and migration artifacts by path; none is mandatory.
- Label facts, assumptions, estimates, proposed decisions, and unresolved choices separately.
- Start with requirements and estimates, then domains and contracts, HLD, and only the critical LLD.
- Consider at least two credible alternatives for consequential decisions, including the simplest option.
- Prefer reversible choices and a modular monolith unless evidence justifies independent service boundaries.
- Do not silently change an accepted decision; record the conflict and required governance action.

## Checklist

### 1. Frame the Design

- [ ] Resolve business outcome, actors, critical journeys, scope, non-goals, decision horizon, and intended readers.
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
- [ ] Deep-dive only the two or three components with the highest correctness, scale, security, or reversibility risk.
- [ ] Define observability, SLI measurement points, health, deployment strategy, rollback, backup, and operator actions.
- [ ] Define ownership, team impact, cost drivers, and operational burden for the proposed topology.

### 5. Decide and Validate

- [ ] Compare credible alternatives against requirements, estimates, failure behavior, complexity, cost, migration, and future triggers.
- [ ] State selected and rejected options with consequences, sensitivity points, and assumptions that would reopen the decision.
- [ ] Identify significant decisions that deserve their own compact decision records without requiring another workflow.
- [ ] Define architecture acceptance evidence: contract checks, load or failure experiments, security validation, recovery proof, and observability signals.
- [ ] Outline current-to-target implications and compatibility needs without expanding into a full implementation plan.

### 6. Write and Report

- [ ] Write context, drivers, estimates, domains, contracts, HLD, critical LLD, failure and operations model, security, alternatives, decisions, validation, open questions, and evolution triggers.
- [ ] Preserve existing content outside the approved scope and link shared artifacts only by document path or title.
- [ ] Re-read the proposal for unsupported facts, hidden decisions, mixed abstraction, and unjustified machinery.
- [ ] Confirm no code, tests, delivery plan, audit result, or external state changed.
- [ ] Use `READY` only when the design is decision-complete enough for implementation planning; use `REVISE` for material but solvable gaps; use `BLOCKED` when required intent, evidence, authority, or destination is unavailable.

## Output Contract

```markdown
# System Design Proposal

**Verdict:** READY | REVISE | BLOCKED
**Artifact:** path

## Target design
- Requirements, estimates, boundaries, contracts, HLD, and critical LLD

## Decisions and tradeoffs
| Decision | Selected option | Alternatives | Evidence | Reopen trigger |
|---|---|---|---|---|

## Validation and transition
- Required evidence, compatibility, rollout, rollback, and observability

## Open decisions and residual risks
Only items that can still change implementation planning.
```
