---
name: ln-72-current-architecture-documenter
description: "Documents implemented current-state architecture from repository evidence. Use for onboarding or migration baselines; not for target design, audit verdicts, or code changes."
---

# Current Architecture Documenter

**Goal:** Produce a trustworthy snapshot of the architecture implemented in the checked-out repository. Document what exists and how it behaves; do not score it, prescribe a target architecture, repair code, or turn intended diagrams into facts.

**Execution contract:** Treat the ordered checkbox workflow below as this skill's Definition of Done. Work through every item in order, and mark it complete only when its action and required evidence are complete. `N/A`, skipped, unavailable, or delegated items remain incomplete.
Before returning, apply this skill's verdict and approval rules to every incomplete item and prepend **Checklist: X/Y complete**<br>**Incomplete: None | section/item — reason; outcome impact; exact next action**; list every incomplete item.

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
- Map the whole system first, then deepen only the two or three areas needed to explain critical behavior.
- Preserve contradictions and uncertainty instead of resolving them by preference.
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
- [ ] Deepen only the hardest two or three subsystems; keep ordinary implementation detail out of the architecture document.

### 4. Write the Current-State Artifact

- [ ] Write snapshot identity, system context, component inventory, responsibilities, dependency and data flow, runtime topology, critical flows, deployment, ownership, and evidence index.
- [ ] Include the minimum useful diagrams inline or link existing diagram artifacts by path.
- [ ] Distinguish observed implementation from documented intent and explicitly list drift or contradictions without assigning severity.
- [ ] Mark remote-only, runtime-only, organizational, or production facts `UNKNOWN` when local evidence cannot establish them.
- [ ] Preserve existing manually maintained context unless repository evidence disproves it; document the contradiction when it does.

### 5. Verify and Report

- [ ] Open every cited file or symbol and remove unsupported claims.
- [ ] Confirm the map explains how critical behavior is discovered, executed, persisted, and deployed.
- [ ] Confirm abstraction levels are not mixed and names remain consistent across prose and diagrams.
- [ ] Confirm no target recommendation, audit verdict, product code, test, or external state was introduced.
- [ ] Use `DOCUMENTED` when the snapshot is evidence-backed and useful; use `INCONCLUSIVE` when material topology remains unknown; use `BLOCKED` when repository identity, scope, or destination cannot be established safely.

## Output Contract

```markdown
# Current Architecture Documentation

**Verdict:** DOCUMENTED | INCONCLUSIVE | BLOCKED
**Artifact:** path
**Snapshot:** remote, branch, HEAD, worktree state, observed date

## Architecture mapped
- Context, modules, runtime and deployment units
- Data, interfaces, ownership, and critical flows

## Evidence limitations
| Claim or area | Status | Evidence inspected | Exact next action |
|---|---|---|---|

## Changes made
- Created or updated sections and diagrams

## Residual unknowns
Facts that require runtime, organizational, or external confirmation.
```
