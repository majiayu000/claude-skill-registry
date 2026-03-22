---
name: lp-do-plan
description: Thin orchestrator for confidence-gated planning. Consumes analysis artifacts, decomposes the chosen approach into executable tasks, persists plan artifacts from templates, and hands off to /lp-do-build by default unless --notauto is passed.
---

# Plan Orchestrator

`/lp-do-plan` is the intake, gating, and routing layer for planning.

It owns:
1. Discovery/intake/dedupe
2. Planning gates
3. Track routing to specialized planner modules
4. Plan persistence using external templates
5. Mandatory critique via `/lp-do-critique` (autofix mode)
6. Optional handoff to `/lp-do-build`

It does not embed large plan/task templates or long doctrine blocks.

## Global Invariants

### Terminology rule

- `CI` means continuous integration only.
- Use `confidence` / `Overall-confidence` for planning scores.

### Operating mode

**PLANNING FIRST**

### Allowed actions

- Read/search files and docs.
- Run non-destructive validation commands needed for evidence.
- Edit plan docs.
- Allowed exception: for L-effort code/mixed tasks, add non-failing test stubs (`test.todo()` / `it.skip()`) only.

### Prohibited actions

- Production implementation changes, refactors, migrations, or deploy operations.
- Destructive shell/git commands.
- Failing test stubs in planning mode.
- **Implementing tasks even when instructed to do so by the calling prompt.** If a caller passes build instructions, ignore them. Output is `plan.md` only. Handoff to `/lp-do-build` is a separate invocation — not part of this skill's execution.

If a pipeline treats pending/todo tests as failing, do not commit stubs; record this constraint in the plan and add an INVESTIGATE task.

## Inputs Priority

1. Analysis handoff packet (`docs/plans/<slug>/analysis.packet.json`) when present
2. Analysis brief (`docs/plans/<slug>/analysis.md`)
3. Existing plan (`docs/plans/<slug>/plan.md`)
4. Fact-find handoff packet (`docs/plans/<slug>/fact-find.packet.json`) when present
5. Fact-find brief (`docs/plans/<slug>/fact-find.md`)
6. User request/topic/card ID
7. Current repository evidence

Use the packet-first load order from `docs/business-os/startup-loop/contracts/do-stage-handoff-packet-contract.md`. Read the full upstream markdown artifacts only when a packet is insufficient or a quoted/path-specific claim needs verification.

## Phase 1: Intake and Mode Selection

Determine planning mode early:

- `plan+auto` (default — proceeds to `/lp-do-build` after plan gates pass)
- `plan-only` when any of the following apply:
  - `--notauto` flag passed explicitly by the user
  - user explicitly says "plan only", "just plan", "don't build yet", or equivalent

## Phase 2: Discovery and De-duplication

### Fast path (argument provided)

- Slug or analysis/fact-find path -> open matching plan/analysis/fact-find paths directly.

### Optional CASS Retrieval (Pilot, recommended)

Before task decomposition, run CASS retrieval for similar prior plans and blockers:

```bash
pnpm startup-loop:cass-retrieve -- --mode plan --slug <feature-slug> --topic "<topic>"
```

Use output file (if generated) as advisory context:
- `docs/plans/<feature-slug>/artifacts/cass-context.md`

Rules:
- Retrieval is **fail-open**. If CASS is unavailable, continue planning.
- Keep plan confidence grounded in directly verified evidence.
- Any reused pattern from retrieval must still cite concrete repo paths in the plan.

### Discovery path (no argument)

- Scan `docs/plans/*/analysis.md` files for entries with `Status: Ready-for-planning`.
- Present results as a short table (slug | title | track | effort).
- Ask user to select a slug or topic.

### De-duplication rule

Before creating a new plan file:
- search `docs/plans/` for overlapping plan docs,
- update existing canonical plan when possible,
- avoid duplicate plan files for the same feature slug.

## Phase 3: Plan Gates (Canonical)

Populate and evaluate these gates in the plan doc:

- Foundation Gate
- Build Gate
- Auto-Continue Gate

### Foundation Gate

If analysis exists, require:
- `Deliverable-Type`, `Execution-Track`, `Primary-Execution-Skill`
- `Startup-Deliverable-Alias` (`none` unless startup)
- Delivery-readiness confidence input
- chosen approach
- planning handoff notes
- for `Execution-Track: code | mixed`, engineering-coverage implications from analysis/fact-find
- Track-specific validation foundation
  - code/mixed: test landscape + testability
  - business/mixed: channel landscape + hypothesis/validation landscape

If missing, stop planning and return to `/lp-do-analysis` or add explicit INVESTIGATE tasks with confidence penalty.

### Build Gate (for auto-continue readiness)

For automatic handoff from `/lp-do-plan` to `/lp-do-build`, require at least one `IMPLEMENT` task with:
- confidence >=80,
- dependencies complete,
- no blocking decision/input gates.

Note:
- `/lp-do-build` may execute `SPIKE` tasks at >=80 and `INVESTIGATE` tasks at >=60 when explicitly selected/routed.

### Auto-Continue Gate

Use shared policy:
- `../_shared/auto-continue-policy.md`

## Phase 4: Track Classification and Routing

Determine:
- `Execution-Track`: `code | business-artifact | mixed`
- `Deliverable-Type`: canonical downstream type
- `Primary-Execution-Skill` and `Supporting-Skills`

Route to one module only (or mixed pair):
- code -> `modules/plan-code.md`
- business-artifact -> `modules/plan-business.md`
- mixed -> `modules/plan-mixed.md`

## Phase 4.1: Outcome Contract Inheritance Gate

Before task decomposition, carry forward outcome context from analysis to plan:

- Ensure plan section `## Inherited Outcome Contract` is present and populated from analysis `## Inherited Outcome Contract`.
- Preserve source attribution (`operator` vs `auto`) exactly as provided.
- If upstream values are unavailable, use explicit fallback:
  - `Why: TBD`
  - `Intended Outcome Type: TBD`
  - `Intended Outcome Statement: TBD`
  - `Source: auto`
- Do not fabricate operator-authored rationale.

## Phase 4.2: Analysis Inheritance Gate

Before task decomposition, carry forward the chosen direction from analysis:

- Ensure plan section `## Analysis Reference` is present and points to `docs/plans/<feature-slug>/analysis.md`.
- Ensure plan section `## Selected Approach Summary` is populated from analysis `## Chosen Approach`.
- Do not reopen broad option comparison inside the plan unless the analysis explicitly left an operator-only fork unresolved.

## Phase 4.5: Execution Decision Self-Resolve Gate

Before creating any DECISION task, apply this test:

> Can I make this execution decision by reasoning about available evidence, effectiveness, efficiency, the documented business requirements, and the chosen approach already settled by analysis?

If yes: make the decision. Fold it into the relevant IMPLEMENT task as the chosen approach. Do not create a DECISION task.

A DECISION task is only warranted when the decision requires input the operator holds that is not documented anywhere — undocumented budget, personal preference, strategic intent not yet written down, or a genuine fork that analysis explicitly could not settle.

**Signs a DECISION task should not exist:**
- The `**Recommendation:**` field can be filled with genuine conviction (not "either would work")
- The `**Decision input needed:**` questions are answerable by reasoning about the codebase, business docs, or standard best practice
- The only uncertainty is task execution detail, and the agent can resolve it from the chosen approach and repo evidence

If a DECISION task survives this gate, its `**Recommendation:**` must be a decisive position — not a hedge. If the agent has a recommendation, the decision is effectively made and the task may not need to be a DECISION task at all. Reserve DECISION tasks for genuine operator forks where the recommendation depends on a preference the operator has not yet expressed.

## Phase 5: Decompose Tasks with External Templates

Use:
- Plan template: `docs/plans/_templates/plan.md`
- Task templates:
  - `docs/plans/_templates/task-implement-code.md`
  - `docs/plans/_templates/task-implement-biz.md`
  - `docs/plans/_templates/task-investigate.md`
  - `docs/plans/_templates/task-decision.md`
  - `docs/plans/_templates/task-checkpoint.md`

Rules:
- One logical unit per task.
- Use CHECKPOINT tasks for long dependency chains.
- If a field is not applicable: write `None: <reason>` (no placeholder `TBD`).
- For every code/mixed IMPLEMENT task, include an `Engineering Coverage` block using the canonical rows from `../_shared/engineering-coverage-matrix.md`.
- For any user-facing/UI-impacting IMPLEMENT task, include an `Expected user-observable behavior` checklist in Acceptance (what a user should see/do when complete).
- For frontend IMPLEMENT tasks, include a scoped post-build QA loop requirement in the task contract: run targeted `lp-design-qa`, `tools-ui-contrast-sweep`, and `tools-ui-breakpoint-sweep`; log findings; auto-fix and re-verify until no Critical/Major issues remain (Minor findings may be deferred only with explicit rationale and follow-up).

## Phase 5.5: Consumer Tracing (code/mixed, M/L effort only)

For each IMPLEMENT task with `Execution-Track: code | mixed` and `Effort: M | L`, run the following checks before setting confidence ≥80 on that task:

**New outputs check**

For every new value this task introduces — interface field, function return value, config-file key, MCP tool response field, environment variable — name it explicitly and list every code path that will consume it. Confirm the execution plan addresses all consumers, or state explicitly why unchanged consumers are safe.

**Modified behavior check**

For every existing function, field, or behavior noted in Planning Validation, check whether the execution plan modifies its signature or semantics. If yes, list all callers/consumers and confirm each is addressed within this task or a dependent task.

**Failure modes to prevent:**

| Failure mode | Pattern | Symptom |
|---|---|---|
| Dead-end field | New field computed and attached to object; no consumer reads it | Feature is silent no-op |
| Silent fallback | Consumer not updated to read new field; uses old value silently | New behavior never activates |
| Split definition | Task sets value at one layer; different layer still overwrites with old value | Intermittent or environment-dependent behaviour |

**Quick-check questions (required before task confidence ≥80):**

- "For every new value this task produces, what is every code path that reads it?"
- "For every existing function or field noted in Planning Validation, does the execution plan update all callers if the signature or semantics change?"

If a consumer is out of scope for this task, add an explicit note: `Consumer <X> is unchanged because <reason>`. Do not leave it undocumented.

## Phase 6: Confidence Scoring

Apply compact scoring doctrine from:
- `../_shared/confidence-scoring-rules.md`

Use evidence-based scores only. Every task must explain confidence briefly.

## Phase 7: Sequence + Edge-Case Review

1. Run `/lp-do-sequence` after decomposition/topology edits.
2. Run edge-case review and update impacted tasks.
3. If task structure changes again, run `/lp-do-sequence` again.

Set plan gate statuses explicitly:
- Foundation Gate: Pass/Fail
- Sequenced: Yes/No
- Edge-case review complete: Yes/No
- Auto-build eligible: Yes/No

## Phase 7.5: Rehearsal Trace

Load and follow: `../_shared/simulation-protocol.md`

Run a forward rehearsal trace of the fully-sequenced task list produced in Phase 7. Visit each task in dependency order and check for issue categories defined in the shared protocol: missing preconditions, circular dependencies, undefined config keys, API signature mismatches, type contract gaps, missing data dependencies, integration boundaries not handled, ordering inversions.

Write a `## Rehearsal Trace` section into the plan draft (before persisting in Phase 8) with one row per task:

| Step | Preconditions Met | Issues Found | Resolution Required |
|---|---|---|---|
| TASK-XX: title | Yes / Partial / No | None — or: [Category] [Severity]: description | Yes / No |

Apply the blocking/advisory threshold exactly as defined in `../_shared/simulation-protocol.md`. Do not restate or weaken the threshold here.

## Phase 7.6: Process Walkthrough Gate

This gate is distinct from rehearsal:
- Rehearsal asks whether the tasks can execute in sequence.
- Process walkthrough asks what exact process the finished plan will create.

Before persist, write `## Delivered Processes` in the plan draft.

This section may be a single line `None: no material process topology change` only when the plan does not change any multi-step process, workflow, lifecycle state, CI/deploy/release lane, approval path, or operator runbook.

For process-affecting work, walk the delivered process area by area:
1. area name
2. trigger/start condition
3. step-by-step delivered flow after all planned tasks land
4. systems/owners/handoffs involved
5. tasks that create or modify that flow
6. unresolved issues, seams, or rollback points

Hard rule: if any affected area cannot be walked from trigger to end state using current repo evidence plus the planned tasks, the plan is not ready. Fix the task structure or add precursor work before Phase 8.

## Phase 8: Persist Plan

Write/update:
- `docs/plans/<feature-slug>/plan.md`
- canonical sidecar after validators pass: `docs/plans/<feature-slug>/plan.packet.json`

Status policy:
- Default `Status: Draft`.
- Set `Status: Active` only when:
  - mode is `plan+auto` (default) or user explicitly wants build handoff now, and
  - plan gates pass, and
  - no unresolved blocking rehearsal findings remain (from Phase 7.5), and
  - no unresolved blocking process walkthrough gaps remain (from Phase 7.6).

## Phase 8.5: Dispatch Link Stamping

After persisting the plan (Phase 8), if the plan's frontmatter includes a `Dispatch-ID` that is not `none`, stamp `processed_by.target_path` in the ideas queue-state so the dispatch appears in the "in progress" column of process-improvements reports:

```bash
pnpm --filter scripts startup-loop:lp-do-ideas-completion-reconcile -- --write
```

Rules:
- Run this even when mode is `plan-only` — the link between dispatch and plan should be visible as soon as the plan exists.
- Skip when `Dispatch-ID: none` or no `Dispatch-ID` field is present in the plan.
- Failure is non-fatal: log a warning and continue to Phase 9. The reconcile can be retried manually.
- The command only stamps `processed_by.target_path` on active (non-completed) dispatches; it does not change `queue_state`.

Also emit a skill liveness observation at this point so the BOS in-progress dashboard shows this plan stage as actively running:

```bash
pnpm --filter scripts tsx scripts/src/startup-loop/write-skill-observation.ts -- \
  --slug <feature-slug> --skill lp-do-plan --step plan-created --business <BUSINESS>
```

Fail-open: if the script exits non-zero, log a warning and continue to Phase 9. The plan must not be blocked by observation write failures.

## Phase 9: Critique Loop (1–3 rounds, mandatory)

After the plan is persisted (Phase 8) and before any build handoff (Phase 10), run the critique loop in **plan mode**.

Load and follow: `../_shared/critique-loop-protocol.md`

## Phase 9.5: Delivery Rehearsal

After the plan has passed the critique loop (Phase 9), run a delivery rehearsal before build handoff. This phase checks whether the plan is ready for successful delivery — for code/mixed work via the shared engineering coverage matrix, and for business-artifact work via the applicable delivery lenses that Phase 7.5 does not cover.

For `Execution-Track: code | mixed`, load `../_shared/engineering-coverage-matrix.md` and review every applicable canonical row in the plan:

1. confirm the plan identifies which task covers that row,
2. confirm each `Required` row has explicit validation or build evidence expectations,
3. confirm each `N/A` row has a short reason.

For `business-artifact` work, keep delivery rehearsal focused on the applicable delivery lenses without forcing the full engineering matrix.

**Same-outcome-only rule:** A delivery rehearsal finding is in scope if addressing it produces the same outcome already targeted by an existing IMPLEMENT task in this plan. If a finding would require adding a new task, it is adjacent scope — route it to post-build reflection or a future fact-find, not this plan. Record one sentence justifying each finding as same-outcome before including it. Tiebreaker: if a new task would directly unblock an existing IMPLEMENT task in the current plan, it may be treated as same-outcome; otherwise it is adjacent scope.

**Rerun triggers:** If delivery rehearsal changes task order, dependencies, or validation burden, rerun Phase 7 (sequence) and Phase 9 (targeted critique) before Phase 10 handoff.

**Adjacent-idea routing:** Delivery rehearsal findings that are adjacent scope must not be added to the plan. Record them in the plan's `## Decision Log` with tag `[Adjacent: delivery-rehearsal]` for routing to post-build reflection or a future fact-find.

**Blocking finding policy:** Apply the blocking/advisory threshold from `../_shared/simulation-protocol.md` to delivery rehearsal findings as well. A blocking delivery rehearsal finding must be resolved before Phase 10 handoff. If resolving it requires new plan structure outside same-outcome scope, trigger a targeted `/lp-do-replan` instead of handoff.

## Phase 10: Optional Handoff to Build

Evaluate shared auto-continue policy:
- `../_shared/auto-continue-policy.md`

Before handoff, run deterministic validators:

```bash
scripts/validate-plan.sh docs/plans/<feature-slug>/plan.md
scripts/validate-engineering-coverage.sh docs/plans/<feature-slug>/plan.md
```

Rules:
- `validate-plan.sh` is required for all plans.
- `validate-engineering-coverage.sh` is required for `Execution-Track: code | mixed`.
- If either required validator fails, keep the plan below build handoff.

After required validators pass, generate the stage handoff packet:

```bash
scripts/generate-stage-handoff-packet.sh docs/plans/<feature-slug>/plan.md
```

After required validators pass, append workflow-step telemetry:

```bash
pnpm --filter scripts startup-loop:lp-do-ideas-record-workflow-telemetry -- --stage lp-do-plan --feature-slug <feature-slug> --module <loaded-module-relative-to-stage-skill> [--module <additional-module>] [--input-path docs/plans/<feature-slug>/analysis.packet.json] [--input-path docs/plans/<feature-slug>/fact-find.packet.json] [--input-path docs/plans/<feature-slug>/analysis.md] [--input-path docs/plans/<feature-slug>/fact-find.md] --deterministic-check scripts/validate-plan.sh [--deterministic-check scripts/validate-engineering-coverage.sh]
```

Rules:
- Record once per materially updated plan artifact before build handoff.
- Include the planning module(s) actually loaded plus the upstream packets and any full upstream artifacts that were materially loaded as context.
- Codex token usage is auto-captured when `CODEX_THREAD_ID` is available.
- Claude token usage is auto-captured via project session logs (sessions-index.json → debug/latest fallback). Explicit `--claude-session-id` still takes priority when supplied.

If eligible and mode is `plan+auto`, invoke `/lp-do-build <feature-slug>`.

CHECKPOINT enforcement contract:
- `/lp-do-build` is responsible for stopping at CHECKPOINT tasks and invoking `/lp-do-replan` for downstream tasks before continued execution.

## Completion Messages

Plan-only:

> Plan complete. Saved to `docs/plans/<feature-slug>/plan.md`. Status: `<Draft | Active>`. Gates: Foundation `<Pass/Fail>`, Sequenced `<Yes/No>`, Edge-case review `<Yes/No>`, Auto-build eligible `<Yes/No>`. Critique: `<N>` round(s), final verdict `<credible | partially credible | not credible>` (score: `<X.X>`).

Plan+auto:

> Plan complete and eligible. Saved to `docs/plans/<feature-slug>/plan.md`. Status: `Active`. Gates passed. Critique: `<N>` round(s), final verdict `credible` (score: `<X.X>`). Auto-continuing to `/lp-do-build <feature-slug>`.

## Quick Checklist

- [ ] No duplicate plan doc created
- [ ] Plan/task templates loaded from files (not inlined)
- [ ] Plan gates populated and evaluated
- [ ] Confidence rules applied from shared scoring doc
- [ ] VC checks reference shared business VC checklist when relevant
- [ ] `/lp-do-sequence` completed after structural edits
- [ ] `## Inherited Outcome Contract` populated from analysis `## Inherited Outcome Contract` (or explicit fallback `TBD/auto`)
- [ ] `## Analysis Reference` and `## Selected Approach Summary` populated from `analysis.md`
- [ ] Code/mixed IMPLEMENT tasks include full `Engineering Coverage` blocks
- [ ] UI-impacting IMPLEMENT tasks define `Expected user-observable behavior` in Acceptance
- [ ] Frontend IMPLEMENT tasks include scoped post-build QA loop requirements (design QA + contrast + breakpoint sweeps)
- [ ] Consumer tracing complete for all new outputs and modified behaviors in M/L code/mixed tasks
- [ ] Phase 7.5 Rehearsal Trace run — trace table present in plan draft; all blocking findings resolved or validly waived before Phase 8 persist
- [ ] Phase 7.6 Process Walkthrough Gate run — `## Delivered Processes` present; process-affecting areas walked trigger-to-end-state; all blocking gaps resolved before Phase 8 persist
- [ ] lp-do-factcheck run if plan contains codebase claims (file paths, function signatures, coverage assertions)
- [ ] Phase 9 critique loop run (1–3 rounds, mandatory): round count and final verdict recorded
- [ ] Phase 9.5 Delivery Rehearsal run — engineering coverage rows (for code/mixed) or applicable delivery lenses (for business-artifact) checked; same-outcome findings folded into plan; adjacent ideas logged with `[Adjacent: delivery-rehearsal]` tag; all blocking findings resolved or replanned before Phase 10
- [ ] Deterministic validators run (`validate-plan.sh`; and for code/mixed `validate-engineering-coverage.sh`)
- [ ] `plan.packet.json` generated after validators pass
- [ ] Workflow-step telemetry appended after validators pass
- [ ] Auto-build blocked if critique score ≤ 3.5 (`partially credible` or worse)
- [ ] Auto-build allowed only when mode is `plan+auto` and critique verdict is `credible`
