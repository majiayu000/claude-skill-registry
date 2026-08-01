---
name: ln-75-architecture-diagram-builder
description: "Creates evidence-backed current or target architecture diagrams. Use when relationships need visualization; not for UI design, architecture audit, or invented structure."
---

# Architecture Diagram Builder

**Goal:** Create the smallest set of understandable, evidence-backed diagrams needed to communicate current or proposed architecture. Change only approved architecture documentation; do not invent relationships, perform visual product design, replace prose evidence, audit fitness, or edit implementation.

**Execution contract:** Treat the ordered checkbox workflow below as this skill's Definition of Done. Work through every item in order, and mark it complete only when its action and required evidence are complete. `N/A`, skipped, unavailable, or delegated items remain incomplete.
Before returning, apply this skill's verdict and approval rules to every incomplete item and prepend **Checklist: X/Y complete**<br>**Incomplete: None | section/item — reason; outcome impact; exact next action**; list every incomplete item.

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
- Choose only views that answer a named audience question.
- For static structure, start with system context and container views; add component depth only when it changes a decision.
- Use sequence or dynamic views for critical runtime interactions and failure paths.
- Use data-flow views for stores, sensitive data, trust boundaries, and transformations.
- Use deployment views for runtime nodes, regions, networks, scaling, and failover.
- Give every diagram a title, scope, audience, legend, element descriptions, and labeled relationships.
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

- [ ] Identify people, software systems, deployable containers, components, stores, queues, and external dependencies relevant to the question.
- [ ] Record responsibility, type, technology when decision-relevant, owner when known, and current/target status for each element.
- [ ] Resolve relationship direction, label, protocol or data, synchronicity, and trust or network boundary where relevant.
- [ ] Trace runtime discovery and registration before including current-state routes, handlers, jobs, plugins, or consumers.
- [ ] Mark uncertain elements or relationships `UNKNOWN` rather than completing the picture aesthetically.

### 3. Select and Draw Views

- [ ] Create a system-context view when readers need system scope and external actors.
- [ ] Create a container or deployment view when readers need responsibilities, deployability, stores, or operational topology.
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
- [ ] Check readability at normal rendering size and split overloaded views rather than shrinking labels.
- [ ] Verify each current-state element and relationship against repository evidence.
- [ ] Confirm no UI design, audit verdict, code, tests, or external state changed.
- [ ] Use `READY` when diagrams are valid, scoped, and evidenced; use `INCONCLUSIVE` when material relationships remain unknown; use `BLOCKED` when scope, evidence, format, or destination prevents a trustworthy diagram.

## Output Contract

```markdown
# Architecture Diagrams

**Verdict:** READY | INCONCLUSIVE | BLOCKED
**Artifacts:** paths

## Views created or updated
| View | State | Audience question | Evidence basis |
|---|---|---|---|

## Verification
- Syntax or render check
- Current-state relationship checks

## Unknowns and residual risks
Only missing relationships or rendering limits that affect interpretation.
```
