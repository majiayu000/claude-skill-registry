---
name: ln-71-system-design-baseline-builder
description: "Creates a project baseline of architecture drivers and constraints. Use before design or planning; not for target design, plan review, implementation, or architecture audit."
---

# System Design Baseline Builder

**Goal:** Create or update one durable source of truth for the project's architecture-driving requirements and constraints. Change only the approved architecture document; do not design the solution, review a plan, audit implementation, edit product code, or invent missing targets.

**Execution contract:** Treat the ordered checkbox workflow below as this skill's Definition of Done. Work through every item in order, and mark it complete only when its action and required evidence are complete. `N/A`, skipped, unavailable, or delegated items remain incomplete.
Before returning, apply this skill's verdict and approval rules to every incomplete item and prepend **Checklist: X/Y complete**<br>**Incomplete: None | section/item — reason; outcome impact; exact next action**; list every incomplete item.

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
- Record source, owner, confirmation date, and review trigger for each architecture driver.
- Separate observed current values, required targets, hard limits, and future evolution triggers.
- Use measurable quality-attribute scenarios; avoid words such as "fast", "scalable", or "secure" without a response measure.
- Treat the baseline as versioned project knowledge, not an immutable promise.

## Checklist

### 1. Establish Scope and Destination

- [ ] Resolve the project, business outcome, intended readers, approved documentation scope, and language.
- [ ] Read applicable repository instructions and inspect Git state so unrelated changes remain untouched.
- [ ] Search for existing requirement, architecture, SLO, recovery, security, cost, and ownership documents.
- [ ] Select one canonical artifact: reuse a clear equivalent or choose the default path; explain why no duplicate will be created.
- [ ] Return `BLOCKED` if the destination is ambiguous and choosing one could split project truth.

### 2. Build the Evidence Ledger

- [ ] Extract confirmed business goals, actors, critical journeys, scope, non-goals, and decision horizon.
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
- [ ] Give every material parameter its theme, applicability, criticality, evidence status, value or range, source, owner, as-of date, and review trigger.
- [ ] Keep calculations reproducible and label estimates separately from observed measurements.
- [ ] Link shared architecture artifacts only by repository path or document title; never require a particular workflow or tool.
- [ ] Preserve historical context needed to understand changed requirements instead of silently rewriting prior commitments.

### 5. Validate and Report

- [ ] Re-read the written artifact and verify that no unknown was converted into a confident fact.
- [ ] Check that targets are measurable, internally consistent, and proportionate to the evidenced business horizon.
- [ ] Check that every architecture-critical gap has an owner or exact next evidence action.
- [ ] Confirm no product code, tests, unrelated documents, or external systems changed.
- [ ] Use `READY` only when the baseline is usable for decisions and no material unknown lacks a safe handling rule; use `INCOMPLETE` for a useful artifact with consequential open drivers; use `BLOCKED` when scope, authority, or destination prevents safe creation.

## Output Contract

```markdown
# System Design Baseline

**Verdict:** READY | INCOMPLETE | BLOCKED
**Artifact:** path

## Established drivers
- Prioritized architecture-driving scenarios
- Applicable business, demand, quality, data, security, operational, economic, and evolution constraints

## Driver register
| Theme | Parameter | Applicability | Criticality | Evidence status | Value or measure | Source and owner | Review trigger |
|---|---|---|---|---|---|---|---|

## Changes made
- Created or updated sections
- Preserved conventions and related artifacts

## Residual risks
Only constraints that can still reverse an architecture decision.
```
