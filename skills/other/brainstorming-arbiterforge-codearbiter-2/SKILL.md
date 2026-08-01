---
name: brainstorming
description: The Socratic spec-refinement front of /feature, and the planning front of /sprint. Routed to BEFORE any code — it takes a one-line idea and drives it to an approved, concrete spec with testable acceptance criteria. Four gated phases — frame, refine, write, approve. No implementation and no handoff to tdd until the spec is on disk and approved; each acceptance criterion becomes one tdd Phase 1 obligation.
---

# brainstorming

Refine the idea before it touches code. Routed to by `/feature` (before `tdd`) and by `/sprint` (the planning front).

## Pre-flight

Read these, or STOP and surface the gap — never guess scope or stack:

- `{{PROJECT_DIR}}/.codearbiter/CONTEXT.md` — the `stage:` frontmatter (the maturity value), domain vocabulary, and what the project is NOT building.
- `{{PROJECT_DIR}}/.codearbiter/tech-stack.md` — the stack the feature must fit; rule out incompatible designs early.
- `{{PROJECT_DIR}}/.codearbiter/open-questions.md` — existing `[CONFIRM-NN]` items; new ones number sequentially from here.

Per-feature and light. NOT decompose's whole-project six-layer interview — one feature, four phases.

## Phase 1 — Frame the problem · gate: BLOCK

Take the one-line idea and pin its boundaries before asking anything else:

- State the problem in one sentence — the concrete pain, not the proposed solution.
- Name the user or caller who feels it, and what "done" looks like to them.
- Name what this feature explicitly does NOT do — the boundary that keeps scope honest.
- Check the framing against `CONTEXT.md`: it never contradicts the NOT-building list or redefines domain vocabulary. A contradiction is a conflict — surface it, do not reconcile it silently.

Gate: problem, caller, and out-of-scope boundary stated and consistent with `CONTEXT.md`.

## Phase 2 — Socratic refinement loop · gate: BLOCK

One focused question at a time. Never advance on a hand-wavy answer. Run every answer through three lenses:

- **Vague language** — Force concrete nouns, numbers, and verbs. "Manage", "handle", "support" are not verbs. "Fast", "secure", "scalable" are not specifications. "We'll figure it out later" is not an answer — every "later" becomes a `[CONFIRM-NN]`.
- **Hidden complexity** — Name what the user assumes is easy but is hard: state, concurrency, edge cases, failure modes, validation, idempotency, migration of existing data. Surface it now or it surfaces in `tdd`.
- **Trade-off forcing** — When a real decision exists, frame it: "X gives you A but costs B; Y gives you C but costs D — choose." Do not pick for the user.

Record every genuinely-unresolved unknown as `[CONFIRM-NN]` in `{{PROJECT_DIR}}/.codearbiter/open-questions.md`, numbered sequentially. A finding that belongs to a different feature or a future scope gets an inline `[NEEDS-TRIAGE]` marker in the notes — never route it to a ticket.

Gate: every vague term made concrete; every forced trade-off resolved or recorded as `[CONFIRM-NN]`; no unresolved "later" outside a `[CONFIRM-NN]`. A blocking `[CONFIRM-NN]` that gates the spec's core stops the loop — surface it and STOP.

## Phase 3 — Write the spec · gate: BLOCK

Write the agreed spec to `{{PROJECT_DIR}}/.codearbiter/specs/<slug>.md`. The slug is derived from the feature. The spec holds:

- **Problem** — the Phase 1 framing in final form.
- **Scope** — what is in, and the explicit out-of-scope boundary.
- **Acceptance criteria** — a numbered list, each criterion concrete and testable: a specific input, the observable output, the boundary or failure behavior. Each criterion is verifiable by a single test. "It works well" is not a criterion. These become `tdd` Phase 1 obligations — one obligation per criterion, so an untestable criterion is a defect to fix here, not in `tdd`.
- **Open questions** — every `[CONFIRM-NN]` raised, cross-referenced to `open-questions.md`.
- **Governs** *(optional)* — a spec-header line `**Governs:** <comma-separated globs>` that enrolls the approved spec in file-scoped just-in-time context injection: on a Read of any file matching one of the listed globs, a pointer to this spec is surfaced to the agent (tier 3 of the file→knowledge map). Adding the line is sufficient to enroll; no other change required.

Gate: the spec file exists on disk under `specs/`, with at least one acceptance criterion and every criterion individually testable.

## Phase 4 — Approval & handoff · gate: STOP

The spec is approved before any code is written or any handoff to `tdd` occurs — no exceptions:

- **Under `/feature`** — present the spec and request explicit user approval. Iterate on the file in place until the user approves. A blocking `[CONFIRM-NN]` must be resolved by the user before approval — never auto-resolve it.
- **Under `/sprint`** — approval may be granted automatically by SMARTS scoring, logged to the `.codearbiter/` audit trail. A blocking `[CONFIRM-NN]` is never auto-approvable; it escalates to the user and STOPs the sprint flow.

On approval, hand off to the `tdd` skill, which enters Phase 1 against the approved spec — one obligation per acceptance criterion.

Gate: the spec is approved (by the user under `/feature`, or by logged SMARTS auto-approval under `/sprint`) with no unresolved blocking `[CONFIRM-NN]`. Only then does control pass to `tdd`.

## Hard rules

- MUST NOT write implementation code or route to `tdd` before the spec is on disk under `specs/` AND approved.
- MUST NOT write an acceptance criterion that cannot be verified by a single test.
- MUST NOT resolve a `[CONFIRM-NN]` by guessing — surface it and record it in `open-questions.md`.
- MUST NOT auto-approve a spec carrying a blocking `[CONFIRM-NN]`, even under `/sprint` — it escalates to the user.
- MUST NOT contradict the NOT-building list or redefine domain vocabulary in `CONTEXT.md` — a contradiction is a conflict to surface, not reconcile.
- MUST NOT run decompose's six-layer whole-project interview — this is one feature, four phases.
- MUST log a `/sprint` auto-approval to the `.codearbiter/` audit trail.
- MUST, at exit, run the follow-up harvest (`{{PLUGIN_ROOT}}/includes/harvest.md`) over any `[NEEDS-TRIAGE]` notes raised this run — batch-confirm promoting them to `open-tasks.md` (work) or `open-questions.md` (decisions) so out-of-scope ideas don't vanish.
