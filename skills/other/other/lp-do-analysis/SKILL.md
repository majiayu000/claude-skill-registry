---
name: lp-do-analysis
description: Thin orchestrator for decision-grade approach selection. Converts evidence-first fact-finds into a chosen approach, rejected alternatives, and a planning handoff artifact ready for /lp-do-plan.
---

# Analysis Orchestrator

`/lp-do-analysis` is the convergence layer between fact-finding and planning.

It owns:
1. Discovery/intake/dedupe
2. Analysis gates
3. Track routing to specialized analysis modules
4. Analysis artifact persistence using external templates
5. Mandatory critique via `/lp-do-critique`
6. Optional handoff to `/lp-do-plan`

It does not decompose executable tasks. That is `/lp-do-plan`'s job.

## Global Invariants

### Operating mode

**ANALYSIS ONLY**

### Allowed actions

- Read/search files and docs.
- Run non-destructive validation commands needed for evidence.
- Edit analysis docs.

### Prohibited actions

- Production implementation changes, refactors, migrations, or deploy operations.
- Destructive shell/git commands.
- Task decomposition beyond planning handoff notes.
- Re-opening broad discovery that belongs in `/lp-do-fact-find` unless the fact-find is insufficient.

## Inputs Priority

1. Fact-find handoff packet (`docs/plans/<slug>/fact-find.packet.json`) when present
2. Fact-find brief (`docs/plans/<slug>/fact-find.md`)
3. Existing analysis (`docs/plans/<slug>/analysis.md`)
4. User request/topic/card ID
5. Current repository evidence

Use the packet-first load order from `docs/business-os/startup-loop/contracts/do-stage-handoff-packet-contract.md`. Read the full `fact-find.md` only when the packet is insufficient or a path-specific claim needs verification.

## Phase 1: Intake and Mode Selection

Determine analysis mode early:

- `analysis+auto` (default — proceeds to `/lp-do-plan` after analysis gates pass)
- `analysis-only` when any of the following apply:
  - `--notauto` flag passed explicitly by the user
  - user explicitly says "analysis only", "just analyze", "don't plan yet", or equivalent

## Phase 2: Discovery and De-duplication

### Fast path (argument provided)

- Slug or fact-find path -> open matching fact-find/analysis paths directly.

### Discovery path (no argument)

- Scan `docs/plans/*/fact-find.md` files for entries with `Status: Ready-for-analysis`.
- Present results as a short table (slug | title | track | effort).
- Ask user to select a slug or topic.

### De-duplication rule

Before creating a new analysis file:
- search `docs/plans/` for overlapping analysis docs,
- update existing canonical analysis when possible,
- avoid duplicate analysis files for the same feature slug.

## Phase 3: Analysis Gates

Populate and evaluate these gates in the analysis doc:

- Evidence Gate
- Option Gate
- Planning Handoff Gate

### Evidence Gate

Require:
- fact-find exists and is `Status: Ready-for-analysis`
- `Deliverable-Type`, `Execution-Track`, `Primary-Execution-Skill`
- `## Outcome Contract`
- for `Execution-Track: code | mixed`, a completed `## Engineering Coverage Matrix` in the fact-find
- enough current-state evidence to compare viable approaches

If missing, stop analysis and return to `/lp-do-fact-find`, or mark `Status: Needs-input` with explicit blockers.

### Option Gate

Require one of:
- at least 2 viable approaches compared explicitly, or
- one viable approach with explicit elimination rationale for rejected/infeasible alternatives

Do not skip option comparison by jumping straight to recommendation.

### Planning Handoff Gate

Require:
- chosen approach stated decisively
- rejected options documented with rationale
- planning handoff notes present (validation implications, sequencing constraints, risk transfer)
- for `Execution-Track: code | mixed`, engineering-coverage implications carried forward explicitly
- `## End-State Operating Model` present with area-by-area delivered flow, or explicit `None: no material process topology change`
- only operator-only questions remain open

If the recommendation is still hedged, analysis is not complete.

## Phase 4: Track Classification and Routing

Determine from the fact-find:
- `Execution-Track`: `code | business-artifact | mixed`
- `Deliverable-Type`
- `Primary-Execution-Skill` and `Supporting-Skills`

Route to one module only (or mixed pair):
- code -> `modules/analyze-code.md`
- business-artifact -> `modules/analyze-business.md`
- mixed -> `modules/analyze-mixed.md`

## Phase 4.5: Decision Boundary

`/lp-do-analysis` owns approach selection, not task planning.

- Resolve high-level approach choices here.
- Leave executable task design, validation contracts, and dependency sequencing to `/lp-do-plan`.
- Keep operator questions only for genuine undocumented preference or real-world information the operator holds.

## Phase 5: Produce Analysis Artifact with External Template

Use:
- Analysis template: `docs/plans/_templates/analysis.md`

Rules:
- Compare approaches explicitly.
- Make the recommendation decisive.
- Keep the artifact decision-grade, not task-grade.
- Carry forward the outcome contract from the fact-find without fabricating operator-authored rationale.
- For `Execution-Track: code | mixed`, fill `## Engineering Coverage Comparison` using `../_shared/engineering-coverage-matrix.md`.

## Phase 5.5: End-State Operating Model (Non-omittable)

Before persist, write `## End-State Operating Model`.

This section may be a single line `None: no material process topology change` only when the chosen approach does not alter any multi-step process, workflow, lifecycle state, CI/deploy/release lane, approval path, or operator runbook.

For process-affecting work, describe the target state area by area:
- current state
- trigger/start condition
- step-by-step end-state flow after the chosen approach lands
- what remains unchanged
- unresolved seams/risks that planning must absorb

If the target process cannot be explained without hiding behind task-level detail, the analysis is not decision-grade yet.

## Phase 6: Persist Analysis

Write/update:
- `docs/plans/<feature-slug>/analysis.md`
- canonical sidecar after validators pass: `docs/plans/<feature-slug>/analysis.packet.json`

Status policy:
- Default `Status: Draft`.
- Set `Status: Ready-for-planning` only when:
  - mode is `analysis+auto` (default) or user explicitly wants planning handoff now, and
  - analysis gates pass, and
  - no unresolved blocker remains in the chosen approach

## Phase 7: Critique Loop (1–3 rounds, mandatory)

After the analysis is persisted (Phase 6), run the critique loop in analysis mode.

Load and follow: `../_shared/critique-loop-protocol.md`

## Phase 7.5: Deterministic Validation

Run:

```bash
scripts/validate-analysis.sh docs/plans/<feature-slug>/analysis.md
```

For `Execution-Track: code | mixed`, also run:

```bash
scripts/validate-engineering-coverage.sh docs/plans/<feature-slug>/analysis.md
```

Rules:
- `validate-analysis.sh` is required for all analyses.
- `validate-engineering-coverage.sh` is required for `Execution-Track: code | mixed`.
- If any required validator fails, analysis is not ready for planning.

After required validators pass, generate the stage handoff packet:

```bash
scripts/generate-stage-handoff-packet.sh docs/plans/<feature-slug>/analysis.md
```

After required validators pass, append workflow-step telemetry:

```bash
pnpm --filter scripts startup-loop:lp-do-ideas-record-workflow-telemetry -- --stage lp-do-analysis --feature-slug <feature-slug> --module <loaded-module-relative-to-stage-skill> [--module <additional-module>] [--input-path docs/plans/<feature-slug>/fact-find.packet.json] [--input-path docs/plans/<feature-slug>/fact-find.md] --deterministic-check scripts/validate-analysis.sh [--deterministic-check scripts/validate-engineering-coverage.sh]
```

Rules:
- Record once per materially updated analysis artifact.
- Include the analysis module(s) actually loaded plus the upstream packet and any full upstream artifact paths that were materially loaded as context.
- Include `scripts/validate-analysis.sh` on every analysis telemetry record, plus `scripts/validate-engineering-coverage.sh` when required by track.
- Codex token usage is auto-captured when `CODEX_THREAD_ID` is available.
- Claude token usage is auto-captured via project session logs (sessions-index.json → debug/latest fallback). Explicit `--claude-session-id` still takes priority when supplied.

## Phase 8: Optional Handoff to Plan

If eligible and mode is `analysis+auto`, invoke `/lp-do-plan <feature-slug>`.

## Completion Messages

Analysis-only:

> Analysis complete. Saved to `docs/plans/<feature-slug>/analysis.md`. Status: `<Draft | Ready-for-planning | Needs-input | Infeasible>`. Gates: Evidence `<Pass/Fail>`, Options `<Pass/Fail>`, Planning handoff `<Pass/Fail>`. Critique: `<N>` round(s), final verdict `<credible | partially credible | not credible>` (score: `<X.X>`).

Analysis+auto:

> Analysis complete and eligible. Saved to `docs/plans/<feature-slug>/analysis.md`. Status: `Ready-for-planning`. Gates passed. Critique: `<N>` round(s), final verdict `credible` (score: `<X.X>`). Auto-continuing to `/lp-do-plan <feature-slug>`.

## Quick Checklist

- [ ] No duplicate analysis doc created
- [ ] Analysis template loaded from file (not inlined)
- [ ] Evidence Gate populated and evaluated
- [ ] Option Gate populated and evaluated
- [ ] Planning Handoff Gate populated and evaluated
- [ ] `## End-State Operating Model` present (or explicit `None: no material process topology change`)
- [ ] For code/mixed work, `## Engineering Coverage Comparison` is complete
- [ ] Chosen approach is decisive, not hedged
- [ ] Rejected options have explicit rationale
- [ ] Only operator-only questions remain open
- [ ] `validate-analysis.sh` passed
- [ ] For code/mixed work, `validate-engineering-coverage.sh` passed
- [ ] `analysis.packet.json` generated after validators pass
- [ ] Workflow-step telemetry appended after validators pass
- [ ] Critique loop run (1–3 rounds, mandatory)
