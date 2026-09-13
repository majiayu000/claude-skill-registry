---
name: ln-24-architecture-decision-recorder
description: "Records one architecture decision with alternatives, consequences and status; does not design the whole system."
---

# Architecture Decision Recorder

**Goal:** Preserve the context, forces, alternatives, decision, and consequences of one architecturally significant choice in a compact durable record. Change only approved decision documentation; do not design the whole system, approve a decision silently, delete history, audit code, or implement the choice.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


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
- Never renumber, delete, or rewrite the decision and rationale of historical records. Permit scoped status and supersession-link updates under the rules below; distinguish evolving proposed drafts from accepted history.
- Default a new record to `Proposed`.
- Use `Accepted` only after explicit confirmation from an authorized decision-maker.
- A proposed replacement links to the current decision without changing its effective status. Mark the old record `Superseded` and link both directions only after the replacement is explicitly accepted; preserve historical content.
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
- [ ] Apply the Artifact Rules for proposed or accepted supersession; verify links and preserve prior rationale.

### 5. Validate and Report

- [ ] Confirm the record contains one decision and can be understood without conversation history.
- [ ] Confirm consequential claims have evidence or labelled assumptions/unknowns with validation actions; never invent historical rationale or rejected alternatives for a retrospective record.
- [ ] Confirm `Accepted` was not assigned without explicit authority.
- [ ] Use `RECORDED` when the record and status are valid; use `INCOMPLETE` when material context or required acceptance authority remains unresolved; a complete explicitly Proposed record does not require acceptance to be `RECORDED`; use `BLOCKED` for ambiguous scope, unsafe numbering, conflicting ownership, or no writable destination.

- [ ] Identify the requirements, interfaces, and downstream decisions affected by this decision or its supersession; preserve the accepted/proposed distinction and historical rationale.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Artifact path, decision identity/status/owner, selected option, alternatives, consequences, evidence, and acceptance/validation needs. Report links or status changes to historical records, preserving their rationale; identify unresolved choices and review triggers without implying acceptance of a proposal.
