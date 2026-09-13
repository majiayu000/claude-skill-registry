---
name: ln-21-system-design-baseline-builder
description: "Defines measurable architecture drivers and constraints before system design; edits architecture docs only."
---

# System Design Baseline Builder

**Goal:** Create or update one durable source of truth for the project's architecture-driving requirements and constraints. Change only the approved architecture document; do not design the solution, review a plan, audit implementation, edit product code, or invent missing targets.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Repository rules and document conventions | Native file reads plus focused search | User-provided convention with an explicit limitation |
| Existing requirements and architecture artifacts | Narrow repository search and direct reads | Conversation evidence marked with its source |
| Current workload or service evidence | Metrics, dashboards, logs, manifests, or checked-in reports | Mark `UNKNOWN`; never manufacture production numbers |
| Current external limits or standards | Official documentation or specifications | Mark the claim `UNVERIFIED` |
| Document mutation | Minimal patch to the approved Markdown artifact | Return `BLOCKED` if no safe writable path is authorized |

Use external research only when a time-sensitive fact changes a constraint. Do not browse for values that must come from product owners, operators, the repository, or measured workload.

## Artifact Rules

- Prefer an existing unambiguous architecture-requirements document.
- Otherwise use `docs/architecture/system-design-baseline.md`.
- Read before writing, preserve unrelated content, and update facts in place instead of creating parallel truth.
- Classify applicability separately as `APPLICABLE` or `NOT_APPLICABLE`, with evidence for exclusions.
- Rank each applicable item as `DRIVER`, `SUPPORTING`, or `INFORMATIONAL`.
- Classify evidence separately as `CONFIRMED`, `ASSUMED`, or `UNKNOWN`.
- Separate observed current values, required targets, hard limits, and future evolution triggers.
- Express quality attributes through observable scenarios and response measures; record undecided targets as missing decisions rather than inventing numbers.
- Treat the baseline as versioned project knowledge, not an immutable promise.

## Checklist

### 1. Establish Scope and Destination

- [ ] Resolve the project, business outcome, intended readers, approved documentation scope, and language.
- [ ] Read applicable repository instructions and inspect Git state so unrelated changes remain untouched.
- [ ] Search for existing requirement, architecture, SLO, recovery, security, cost, and ownership documents.
- [ ] Select one canonical artifact: reuse a clear equivalent or choose the default path; explain why no duplicate will be created.
- [ ] Return `BLOCKED` if the destination is ambiguous and choosing one could split project truth.

### 2. Build the Evidence Ledger

- [ ] Collect business goals, actors, journeys, scope, non-goals, and decision horizon with their sources and confidence for the driver analysis; do not create a second context inventory.
- [ ] Record sources for current workload, data volume, service behavior, platform limits, and existing commitments.
- [ ] Separate repository facts from stakeholder choices and estimates.
- [ ] Detect contradictions between documents, code, configuration, and stated requirements; preserve both claims until resolved.
- [ ] Ask only for choices whose absence materially changes architecture; mark all other gaps `UNKNOWN`.

### 3. Define and Prioritize Architecture Drivers

- [ ] **Business and scope:** Record actors, critical journeys, business horizon, scope, non-goals, and externally committed outcomes.
- [ ] **Demand and data scale:** Record current and target users, rates, concurrency, payloads, growth, retention, and forecast horizon where relevant.
- [ ] **User-observable service quality:** Define SLIs and SLOs for availability, latency, throughput, error rate, correctness, or freshness with measurement windows.
- [ ] **Data semantics and recovery:** Define consistency, ordering, idempotency, reconciliation, durability, backup, RTO, RPO, and acceptable data loss at affected boundaries.
- [ ] **Security, privacy, and compliance:** Define trust boundaries, data classification, residency, access, audit, and destructive-action constraints.
- [ ] **Operations and economics:** Define ownership, operational capacity, cost envelope, supported regions, delivery cadence, and platform or vendor constraints.
- [ ] **Evolution:** Record thresholds, business events, or evidence that justify revisiting an assumption, target, or deferred capability.
- [ ] Separate applicability, criticality, and evidence status; do not use `UNKNOWN` to mean unimportant or `NOT_APPLICABLE`.
- [ ] Prioritize the few scenarios most likely to shape architecture and express each as source/stimulus/environment/artifact/response/measure.

### 4. Write the Baseline

- [ ] Create or update the artifact with: identity and status; business context; scope and non-goals; critical scenarios; workload and data; quality targets; recovery; consistency; security; cost and operations; constraints; assumptions and unknowns; review triggers.
- [ ] Give material parameters their theme, applicability, criticality, evidence status, value/range, source, owner, as-of date, and review trigger. State shared metadata once with explicit inheritance; use `UNKNOWN` for missing ownership or values.
- [ ] Keep calculations reproducible and label estimates separately from observed measurements.
- [ ] Link shared architecture artifacts only by repository path or document title; never require a particular workflow or tool.
- [ ] Preserve historical context needed to understand changed requirements instead of silently rewriting prior commitments.

### 5. Validate and Report

- [ ] Re-read the written artifact and verify that no unknown was converted into a confident fact.
- [ ] Check that targets are measurable, internally consistent, and proportionate to the evidenced business horizon.
- [ ] Check that every architecture-critical gap has an owner or exact next evidence action.
- [ ] Use `READY` only when the baseline is usable for decisions and no material unknown lacks a safe handling rule; use `INCOMPLETE` for a useful artifact with consequential open drivers; use `BLOCKED` when scope, authority, or destination prevents safe creation.

- [ ] Link architecture drivers to their source product requirements; preserve the product source as owner of functional rules rather than copying a second requirements baseline.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Artifact path, established drivers and prioritized quality scenarios, applicable constraints, and changed sections. The artifact owns the driver register: theme/parameter, applicability, criticality, evidence status, value/measure, source/owner, as-of date, and review trigger. Summarize only decision-changing gaps; do not copy the register into the response.
