---
name: ln-25-architecture-diagram-builder
description: "Creates evidence-backed current or target architecture diagrams; not UI design."
---

# Architecture Diagram Builder

**Goal:** Create the smallest set of understandable, evidence-backed diagrams needed to communicate current or proposed architecture. Change only approved architecture documentation; do not invent relationships, perform visual product design, replace prose evidence, audit fitness, or edit implementation.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Architecture evidence | Repository files, runtime wiring, IaC, contracts, and approved artifacts | User-provided model with `UNVERIFIED` labels |
| Relationship tracing | Language intelligence, dependency tools, and focused search | Direct inspection of producers, consumers, and registrations |
| Diagram format | Existing repository convention and renderer | Mermaid in Markdown, then plain ASCII |
| Syntax verification | Repository renderer, parser, or preview | Manual fence, identifier, and relationship inspection |
| Document mutation | Minimal patch to approved diagram artifacts | Return `BLOCKED` if path or evidence boundary is unsafe |

Diagrams communicate a model; executable behavior remains authoritative for current state. Keep current, target, and transition views visibly distinct.

## Artifact Rules

- Reuse an existing diagram convention or use `docs/architecture/diagrams/<view>.md`.
- Prefer Markdown with Mermaid for text-reviewable source; use ASCII when Mermaid is unsupported.
- For static structure, choose the context, container, or component level that answers the requested question; do not create prerequisite overview diagrams when existing context suffices.
- Keep diagram source reviewable in version control.
- Split views when one diagram needs multiple unrelated stories.
- Never use color as the only carrier of meaning.
- Use stable element identifiers and concise display labels so revisions produce reviewable diffs.
- Keep detailed evidence beside the diagram rather than crowding nodes and relationships.
- Preserve an understandable existing notation; introduce a new notation only when it answers the audience question better.

## Checklist

### 1. Establish the Diagram Contract

- [ ] Resolve audience, question, current or target state, scope, approved destination, and required notation.
- [ ] Read repository instructions, relevant architecture artifacts, and existing diagram conventions.
- [ ] Select the minimum useful view or views; reject diagrams that add no relationship clarity.
- [ ] Define the evidence boundary and label user-supplied or proposed elements separately.
- [ ] Keep the run read-only except for approved architecture diagram documentation.

### 2. Build the Architecture Model

- [ ] Identify relevant people, systems, applications/data stores (C4 containers when using C4), components, queues, and external dependencies; distinguish logical containers from OS/container-runtime deployment units.
- [ ] Record responsibility, type, technology when decision-relevant, owner when known, and current/target status for each element.
- [ ] Resolve relationship direction, label, protocol or data, synchronicity, and trust or network boundary where relevant.
- [ ] Trace runtime discovery and registration before including current-state routes, handlers, jobs, plugins, or consumers.
- [ ] Mark uncertain elements or relationships `UNKNOWN` rather than completing the picture aesthetically.

### 3. Select and Draw Views

- [ ] Create a system-context view when readers need system scope and external actors.
- [ ] Create a container or deployment view for responsibilities, deployability, stores, or operational topology; include nodes, regions, networks, scaling, and failover when relevant to the audience question.
- [ ] Create a component view only for a complex area whose internal boundaries change understanding.
- [ ] Create sequence or dynamic views for critical success, failure, retry, timeout, recovery, or migration interactions.
- [ ] Create data-flow or trust-boundary views when security, privacy, residency, or system-of-record questions require them.
- [ ] Avoid mixing abstraction levels in one view unless the exception is explicit and necessary.

### 4. Make the Diagram Self-Describing

- [ ] Add title, diagram type, scope, current/target marker, intended audience, and observation or proposal date.
- [ ] Add a legend for shapes, colors, line styles, abbreviations, and uncertainty markers.
- [ ] Label every relationship with intent or data; avoid generic arrows and unexplained acronyms.
- [ ] Keep names consistent with code, contracts, and shared architecture documents.
- [ ] Add compact evidence notes or links sufficient to trace current-state claims.

### 5. Verify and Report

- [ ] Validate syntax with the repository renderer or perform a complete manual syntax inspection.
- [ ] Inspect rendered readability when a preview is available and split overloaded views rather than shrinking labels. Without a renderer, record visual readability as `UNPROVEN`; manual syntax inspection is not render proof.
- [ ] Verify current-state elements and relationships against implementation evidence, and target-state elements against the declared proposal or explicitly labelled assumptions.
- [ ] Use `READY` when diagrams are valid, scoped, and evidenced; use `INCONCLUSIVE` when material relationships remain unknown; use `BLOCKED` when scope, evidence, format, or destination prevents a trustworthy diagram.

- [ ] Bind each view to current or proposed architecture and its authoritative source; expose contradictions rather than resolving them silently in a diagram.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Artifact paths; each view’s current/target state, audience question, and evidence basis. Report syntax/render verification and current-state relationship checks, unknown relationships, and rendering limits that affect interpretation.
