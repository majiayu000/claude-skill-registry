---
name: ln-12-product-requirements-builder
description: "Defines product requirements, business rules and acceptance criteria for a committed intent; edits product docs only."
---

# Product Requirements Builder

**Goal:** Create or update a usable product requirements artifact that preserves the owner's intent and makes expected behavior testable. Change only authorized product documentation; do not invent commitments, design architecture, or implement.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Intent and prior decisions | User request, product documents and accepted decisions | Bounded assumptions; ask only for missing consequential intent |
| Existing behavior | Focused repository, UI, contract and analytics evidence | Supplied examples with explicit uncertainty |
| Requirement artifact | Existing canonical product document and focused editor | User-approved destination; BLOCKED if no safe destination is available |

## Domain Rules

- Reuse the existing requirement owner; otherwise use an authorized docs/product/requirements.md. Do not impose a new document hierarchy on an established project.
- Separate observed behavior, owner preference, proposed requirements, accepted commitments, and unresolved choices. A discovery recommendation is not authorization to build.
- Use stable requirement identifiers when traceability spans artifacts. Keep functional rules here and reference architecture constraints by source; user stories are optional representations.

## Checklist

### 1. Establish Intent and Authority

- [ ] Resolve the problem, affected actors, intended outcome, horizon, approved documentation scope, and protected existing experience.
- [ ] Read repository instructions, relevant user evidence and existing requirements; inspect target files and user changes before editing.
- [ ] Identify one authoritative requirements destination and applicable decision owners; preserve unresolved conflicting sources.
- [ ] Separate non-goals, optional ideas and committed scope; clarify only choices that change acceptance or product intent.

### 2. Specify Observable Behavior

- [ ] Describe the initiating event, actor permissions, preconditions, successful outcome and meaningful alternatives for every in-scope journey.
- [ ] Specify business rules, calculations, entities and lifecycle transitions where they determine observable behavior.
- [ ] Specify applicable failure, empty, loading, retry, duplicate, cancellation and recovery behavior without inventing irrelevant states.
- [ ] Record affected integrations, external commitments, compatibility and data constraints from authoritative sources.
- [ ] Capture accessibility, privacy and other applicable user-facing constraints; reference architecture-driving targets without duplicating their owner.
- [ ] Separate required new UX from protected existing flows, copy and behavior.

### 3. Define Acceptance and Outcome

- [ ] Give each material requirement observable acceptance conditions with prerequisites and an expected result independent of implementation.
- [ ] Define the intended business effect, available baseline, measurement window and evidence source; keep unknown targets unknown.
- [ ] Identify dependencies and assumptions that can reverse scope, acceptance or the chosen product direction.
- [ ] Distinguish functional acceptance from product impact and from permission to publish or run an experiment.

### 4. Write and Validate

- [ ] Write the approved artifact with requirement IDs, source/status, acceptance, non-goals, assumptions and unresolved decisions.
- [ ] Preserve unrelated content and history of changed commitments; mark supersession instead of silently replacing accepted intent.
- [ ] Check consistency across rules, scenarios and acceptance; expose requirements that cannot yet be implemented or tested safely.
- [ ] Report the exact consequential gaps and next evidence actions; do not treat the document's existence as readiness.

## Verdict

- `READY`: requirements are consistent and testable, with no consequential unresolved intent preventing the next decision; proposed status does not imply owner acceptance.
- `INCOMPLETE`: a useful artifact exists but named requirements or decisions remain unresolved.
- `BLOCKED`: scope, authority, essential intent or a safe destination prevents responsible creation.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Artifact, intent, protected behavior, requirement/source/status/acceptance mapping, changed commitments, outcome measures, and consequential unknowns with their next evidence action.
