---
name: ln-74-architecture-decision-recorder
description: "Records one architecture decision with context, alternatives, tradeoffs, and consequences. Use for a significant choice; not for broad design, audit, or implementation."
---

# Architecture Decision Recorder

**Goal:** Preserve the context, forces, alternatives, decision, and consequences of one architecturally significant choice in a compact durable record. Change only approved decision documentation; do not design the whole system, approve a decision silently, delete history, audit code, or implement the choice.

**Execution contract:** Treat the ordered checkbox workflow below as this skill's Definition of Done. Work through every item in order, and mark it complete only when its action and required evidence are complete. `N/A`, skipped, unavailable, or delegated items remain incomplete.
Before returning, apply this skill's verdict and approval rules to every incomplete item and prepend **Checklist: X/Y complete**<br>**Incomplete: None | section/item — reason; outcome impact; exact next action**; list every incomplete item.

## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Existing decision convention | Repository search and direct document reads | Use the default path and compact format |
| Decision drivers | Requirements, architecture artifacts, implementation evidence, and stakeholder statements | Mark unsupported drivers `UNKNOWN` |
| Alternatives and external claims | Repository evidence plus current official sources | Mark time-sensitive claims `UNVERIFIED` |
| Sequence and supersession | Existing filenames, indexes, and decision links | Return `BLOCKED` rather than reuse a number |
| Document mutation | Minimal patch to one approved decision record and necessary supersession links | Return `BLOCKED` if authority or path is unclear |

One record captures one decision. If the request contains independent decisions with different drivers or lifecycles, split them only with explicit approval.

## Artifact Rules

- Reuse the repository's established ADR convention when one exists.
- Otherwise use `docs/architecture/decisions/NNNN-<slug>.md` with the next unused monotonic number.
- Never renumber, overwrite, or delete historical records.
- Default a new record to `Proposed`.
- Use `Accepted` only after explicit confirmation from an authorized decision-maker.
- Mark a replaced record `Superseded` and link both directions; preserve its original content.
- Link shared requirements and architecture artifacts only by path or title.
- Record positive, negative, and neutral consequences without advocacy language.
- Keep the record short enough to review as a single decision.
- Preserve the rationale a future maintainer needs to reconsider it safely.
- Label retrospective records explicitly; do not imply that documentation created after implementation was prior approval.
- Separate evidence needed before acceptance from monitoring required after adoption.
- Prefer stable repository references over conversation, branch-local, or ephemeral links.

## Checklist

### 1. Establish the Decision Contract

- [ ] Resolve the exact decision, scope, owner or deciders, affected system, and why the choice is architecturally significant.
- [ ] Read repository instructions, Git state, and existing decision conventions.
- [ ] Search for duplicate, conflicting, deprecated, or superseding decisions before allocating a new record.
- [ ] Confirm the request is one decision rather than a broad design or implementation plan.
- [ ] Resolve the approved status; default to `Proposed` when acceptance is not explicit.

### 2. Gather Context and Forces

- [ ] State the current context and problem in value-neutral language.
- [ ] Extract business drivers, quality attributes, constraints, assumptions, and decision horizon from available evidence.
- [ ] Identify affected boundaries, contracts, data, security, operations, cost, ownership, and migration implications.
- [ ] Separate present facts from forecasts and preferences.
- [ ] Record contradictions or missing evidence that could change the choice.

### 3. Evaluate Alternatives

- [ ] Include the status quo and the simplest credible option unless they are demonstrably infeasible.
- [ ] Include materially different alternatives rather than cosmetic variants.
- [ ] Compare options against the same drivers: correctness, quality targets, complexity, reversibility, cost, operations, team fit, and evolution.
- [ ] State why each rejected alternative loses in this context without claiming universal inferiority.
- [ ] Record sensitivity or review triggers that would make a rejected option preferable later.

### 4. Record the Decision

- [ ] Write title, status, date, deciders or owner, context, drivers, considered options, decision, consequences, validation, and review triggers.
- [ ] State the decision in active, testable language and name what remains deliberately undecided.
- [ ] Record positive, negative, and neutral consequences plus accepted risks.
- [ ] Link affected requirements, designs, diagrams, interfaces, migration documents, or issues by stable repository reference.
- [ ] For supersession, update status and cross-links without erasing prior rationale.

### 5. Validate and Report

- [ ] Confirm the record contains one decision and can be understood without conversation history.
- [ ] Confirm every consequential claim has evidence, a named assumption, or an explicit owner.
- [ ] Confirm `Accepted` was not assigned without explicit authority.
- [ ] Confirm no architecture, code, tests, task tracker, or external system changed beyond approved decision documentation.
- [ ] Use `RECORDED` when the record and status are valid; use `INCOMPLETE` when material context or authority remains open; use `BLOCKED` for ambiguous scope, unsafe numbering, conflicting ownership, or no writable destination.

## Output Contract

```markdown
# Architecture Decision Record

**Verdict:** RECORDED | INCOMPLETE | BLOCKED
**Artifact:** path
**Decision status:** Proposed | Accepted | Deprecated | Superseded

## Decision captured
- Context, selected option, and decisive drivers

## Alternatives and consequences
- Rejected options, accepted costs, and review triggers

## Links changed
- New record and any supersession links

## Open authority or evidence
Only items that prevent acceptance or could reverse the decision.
```
