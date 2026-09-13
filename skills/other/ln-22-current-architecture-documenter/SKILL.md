---
name: ln-22-current-architecture-documenter
description: "Documents current architecture from implementation evidence; does not propose a target or audit fitness."
---

# Current Architecture Documenter

**Goal:** Produce a trustworthy snapshot of the architecture implemented in the checked-out repository. Document what exists and how it behaves; do not score it, prescribe a target architecture, repair code, or turn intended diagrams into facts.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Snapshot identity and worktree state | Git status, branch, remote, and HEAD | Record the supplied snapshot as `UNVERIFIED` |
| Structure and configuration | Native listing, search, manifests, and direct file reads | Narrow manual inspection |
| Symbols, dependencies, and consumers | Language intelligence or resolved dependency tooling | Search definitions, registrations, imports, and callers |
| Runtime and deployment topology | Entrypoints, IaC, containers, CI, configuration, and runtime evidence | Mark deployment relationships `UNKNOWN` |
| Document mutation | Minimal patch to the approved architecture document | Return `BLOCKED` if no writable path is authorized |

Prefer local evidence over remote repository state. A path, diagram, or naming convention is a lead until executable wiring or an authoritative contract confirms it.

## Artifact Rules

- Reuse a clear current-state architecture document; otherwise use `docs/architecture/current-state.md`.
- Anchor the document to remote, branch, HEAD, worktree state, and observation date.
- Cite material claims with file paths, symbols, commands, or configuration keys.
- Label claims `OBSERVED`, `DOCUMENTED`, `INFERRED`, or `UNKNOWN`.
- Separate actual structure from intended target design and from audit findings.
- Map the declared system scope at a coarse level first, then deepen only what explains its critical behavior; do not expand a bounded request into a repository-wide inventory.
- Prefer responsibility-oriented descriptions over exhaustive file inventories.
- Record the evidence cutoff so readers can distinguish uninspected scope from genuine absence.
- Keep volatile counts or inventories only when they affect architectural understanding.

## Checklist

### 1. Establish the Documentation Contract

- [ ] Resolve repository scope, intended readers, approved destination, required depth, and language.
- [ ] Read repository instructions and record snapshot identity plus dirty-worktree limitations.
- [ ] Search for existing current-state, baseline, target-design, decision, diagram, and deployment artifacts.
- [ ] Reuse an unambiguous current-state document or select the default path without duplicating project knowledge.
- [ ] Keep the run read-only except for the approved architecture document.

### 2. Map the System Breadth

- [ ] Identify languages, frameworks, package roots, generated surfaces, and canonical build or run commands from manifests and CI.
- [ ] Identify users, external systems, entrypoints, applications, services, processes, workers, scheduled jobs, and deployment units.
- [ ] Map major domains or modules, responsibilities, ownership, and dependency direction.
- [ ] Map data stores, caches, queues, files, external APIs, schemas, and systems of record.
- [ ] Record public interfaces, runtime discovery, registration, configuration composition, and environment boundaries.
- [ ] Record build, deploy, scale, and failure boundaries without inferring independence from directory names.

### 3. Trace Critical Behavior

- [ ] Select representative critical flows based on business importance and architectural reach.
- [ ] Trace each flow from actor or trigger through entrypoint, runtime coordination, domain behavior, persistence or integration, and observable outcome.
- [ ] Record synchronous and asynchronous hops, transaction ownership, consistency, retry, timeout, idempotency, and error propagation where evidenced.
- [ ] Describe deployment, startup, shutdown, health, observability, and recovery paths visible from repository evidence.
- [ ] Deepen only subsystems whose complexity or uncertainty affects architectural understanding; keep ordinary implementation detail out of the architecture document.

### 4. Write the Current-State Artifact

- [ ] Write snapshot identity, system context, component inventory, responsibilities, dependency and data flow, runtime topology, critical flows, deployment, ownership, and evidence index.
- [ ] Include the minimum useful diagrams inline or link existing diagram artifacts by path.
- [ ] Distinguish observed implementation from documented intent and explicitly list drift or contradictions without assigning severity.
- [ ] Mark remote-only, runtime-only, organizational, or production facts `UNKNOWN` unless supplied authoritative evidence establishes them; distinguish declared deployment configuration from observed live topology.
- [ ] Preserve sourced manually maintained context with its evidence status; document contradictions and label unsupported historical claims instead of inheriting them as observed facts.

### 5. Verify and Report

- [ ] Verify every citation against inspected snapshot evidence and remove unsupported claims; reopen sources only if they changed or the prior inspection did not establish the claim.
- [ ] Confirm the map explains how critical behavior is discovered, executed, persisted, and deployed.
- [ ] Confirm abstraction levels are not mixed and names remain consistent across prose and diagrams.
- [ ] Use `DOCUMENTED` when the snapshot is evidence-backed and useful; use `INCONCLUSIVE` when material topology remains unknown; use `BLOCKED` when repository identity, scope, or destination cannot be established safely.

- [ ] Bind the current-state account to the inspected revision and relevant dirty/configuration state; identify changes that would make a documented boundary stale.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Artifact path and snapshot identity (remote, branch, HEAD, worktree, date); mapped context, modules, runtime/deployment, data/interfaces, ownership, and critical flows. Identify changed sections/diagrams and claims or areas needing runtime, organizational, or external confirmation with status, inspected evidence, and exact next action.
