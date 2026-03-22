---
name: lp-do-fact-find
description: Thin orchestrator for discovery, intake routing, and evidence-first fact-finding. Routes to specialized modules and emits analysis-ready artifacts for /lp-do-analysis. For understanding-only briefings, use /lp-do-briefing.
---

# Fact Find Orchestrator

`/lp-do-fact-find` is the intake and routing layer. Keep this file thin.

This orchestrator does five things:
1. Discovery and selection (topic)
2. Sufficiency gate
3. Classification (track, deliverable)
4. Module routing (load only one relevant module, plus mixed-track add-on when needed)
5. Artifact persistence using shared templates + automatic critique

Do not embed long templates, long checklists, or API payload blocks here.

## Global Invariants

### Operating mode

**FACT-FIND ONLY**

### Repo actions (allowed)

- Read/search files and docs.
- Run non-destructive commands (for example `rg`, targeted tests, targeted lint/typecheck) when needed for evidence.
- Inspect targeted git history.

### Prohibited actions

- Code changes, refactors, migrations, or production data writes.
- Destructive shell/git commands.
- Analysis/planning/build execution (this skill ends at fact-find output).

### Evidence and quality rules

- Evidence first: non-trivial claims require explicit pointers.
- Unknowns must include a concrete verification path.
- Omit sections with no evidence, or collapse to a one-line `Not investigated: <reason>`.
- Process-affecting work must capture the current process map area by area. A touched-file list is not enough when the change alters CI/deploy/release lanes, approvals, orchestration, lifecycle states, or multi-step operator flows.
- Keep signal high:
  - max 10 key files/modules in primary evidence list
  - max 10 risks
  - max 8 open questions

## Required Inputs

Minimum intake before investigation:

- Concrete area anchor (feature/component/system)
- At least one location anchor (path guess, route, endpoint, error/log, user flow)
- Provisional deliverable family

If any item is missing, ask only the minimum follow-up questions needed to unblock.

## Phase 0: Queue Check Gate

Load and follow: `../_shared/queue-check-gate.md` (fact-find mode).

## Phase 1: Discovery and Selection

- **Fast path** (argument provided): If argument is a topic, proceed directly to sufficiency gate.
- **Discovery path** (no argument): Scan `docs/plans/` for directories with `fact-find.md`; show list; ask user to select or provide new topic.

## Phase 2: Context Hydration

If a matching `fact-find.md` already exists at `docs/plans/<feature-slug>/fact-find.md`, read it and use existing findings and open questions as starting context. Otherwise, start fresh from the topic anchor.

### Optional CASS Retrieval (Pilot, recommended)

Before deep investigation, run CASS retrieval for reusable prior evidence:

```bash
pnpm startup-loop:cass-retrieve -- --mode fact-find --slug <feature-slug> --topic "<topic>"
```

Use output file (if generated) as advisory context:
- `docs/plans/<feature-slug>/artifacts/cass-context.md`

Rules:
- Retrieval is **fail-open**. If CASS is unavailable, continue with normal investigation.
- Keep canonical evidence in the fact-find artifact itself (paths, tests, docs, call sites).
- Do not treat retrieval snippets as proof without verifying source paths directly.

### Access Declarations

Before the investigation begins, list every external data source, service, or system that will be needed to answer the questions in this fact-find. For each source:

- Name the source and required access type.
- Check `memory/data-access.md` (`~/.claude/projects/<project-hash>/memory/data-access.md`); if absent/unlisted, mark `UNVERIFIED` (do not block).
- Record sources discovered mid-investigation under `## Access Declarations`.
- Follow schema: `docs/plans/startup-loop-build-reflection-gate/task-01-schema-spec.md` § 3. If no external dependencies, write `None`.

## Phase 3: Sufficiency Gate

Do not start repository investigation until minimum intake is satisfied. If insufficient, ask targeted questions only, each tied to a decision it unlocks.

## Phase 4: Classification

Compute this routing header first.

```yaml
Outcome: planning
Execution-Track: <code | business-artifact | mixed>
Deliverable-Family: <code-change | message | doc | spreadsheet | multi>
Deliverable-Channel: <none | email | whatsapp>
Deliverable-Subtype: <none | product-brief | marketing-asset>
Deliverable-Type: <canonical downstream type>
Startup-Deliverable-Alias: <none | startup-budget-envelope | startup-channel-plan | startup-demand-test-protocol | startup-supply-timeline | startup-weekly-kpcs-memo | website-first-build-backlog | website-upgrade-backlog | startup-loop-gap-fill>
Loop-Gap-Trigger: <none | block | bottleneck | feedback>
```

Use `routing/deliverable-routing.yaml` to map family/channel/subtype to canonical `Deliverable-Type`. Keep `Deliverable-Type` in canonical downstream format expected by `/lp-do-plan` and `/lp-do-build`. Execution skill IDs are canonicalized without leading slash (e.g., `lp-do-build`).

Hard branches:
- If invocation includes `--website-first-build-backlog`, set `Startup-Deliverable-Alias: website-first-build-backlog` before routing.
- If `Startup-Deliverable-Alias: website-first-build-backlog`, route immediately to the website-first-build module and skip generic business/code checklists that do not apply.
- If `Startup-Deliverable-Alias: website-upgrade-backlog`, route immediately to the website-upgrade module and skip generic business/code checklists that do not apply.
- If `Startup-Deliverable-Alias: startup-loop-gap-fill`, route immediately to the loop-gap module. Set `Loop-Gap-Trigger` from the argument (block/bottleneck/feedback) or ask one targeted question. Output path and outcome (briefing vs planning) are determined by the module based on trigger type. Skip Phase 6 standard output paths — use trigger-specific paths defined in the module.

## Phase 5: Route to a Single Module

Load only the relevant module file(s):

- `code` track: `modules/outcome-a-code.md`
- `business-artifact` track: `modules/outcome-a-business.md`
- `mixed` track: load both code and business modules; merge evidence
- `website-first-build-backlog` alias: `modules/outcome-a-website-first-build.md`
- `website-upgrade-backlog` alias: `modules/outcome-a-website-upgrade.md`
- `startup-loop-gap-fill` alias: `modules/outcome-a-loop-gap.md` (output path determined by trigger type inside the module)

For `Execution-Track: code | mixed`, also load:
- `../_shared/engineering-coverage-matrix.md`

Use it to fill `## Engineering Coverage Matrix` in the artifact with explicit `Required` / `N/A` treatment for every canonical row.

## Phase 5.4: Current Process Map (Non-omittable)

Before rehearsal, write `## Current Process Map` in the fact-find draft.

This section may be a single line `None: local code path only` only when the work does not change any multi-step process, workflow, lifecycle state, CI/deploy/release lane, approval path, or operator runbook.

For process-affecting work, map the current state area by area:
- trigger/start condition
- step-by-step current flow
- owners/systems/handoffs
- end condition
- known issues already visible in current state
- evidence refs for each area

If you cannot explain the current process end-to-end from trigger to end state, the fact-find is not ready for analysis. Expand the investigation first.

## Phase 5.5: Scope Rehearsal

Load and follow: `../_shared/simulation-protocol.md`

Run a scope rehearsal of the investigation completed in Phase 5. This is not a code execution trace — it is a scope-gap check. Walk through each evidence area identified in the investigation and apply the scope rehearsal checklist defined in the shared protocol (5 categories: concrete investigation path, investigation ordering, system boundary coverage, circular investigation dependency, missing domain coverage).

Write a `## Rehearsal Trace` section into the fact-find draft (before persisting in Phase 6) with one row per scope area:

| Scope Area | Coverage Confirmed | Issues Found | Resolution Required |
|---|---|---|---|
| <evidence domain or entry point> | Yes / Partial / No | None — or: [Category] [Severity]: description | Yes / No |

Apply the blocking/advisory threshold exactly as defined in `../_shared/simulation-protocol.md`. Do not restate or weaken the threshold here.

## Phase 5.6: Scope Signal (Two-Way)

After rehearsal, classify scope posture using evidence from the investigation:

- `constrained`: scope is too broad/risky for current evidence or capacity; narrow it.
- `right-sized`: scope is realistic and appropriately bounded.
- `limited-thinking`: scope is safely expandable now based on clear evidence.

When `limited-thinking`, add 1-3 concrete expansion suggestions. Each suggestion must include:
- what to add now,
- expected upside,
- added risk/cost.

Do not emit `limited-thinking` without explicit evidence that dependencies, risks, and validation burden remain manageable.

## Phase 6: Persist Artifact with Shared Templates

- Output path: `docs/plans/<feature-slug>/fact-find.md`
- Template: `docs/plans/_templates/fact-find-planning.md`
- Always include the routing header fields in frontmatter.
- Dispatch-routed path:
  - single packet -> write `Dispatch-ID`
  - bundled work package -> write `Dispatch-IDs` and `Work-Package-Reason`
- **Canonical artifact name:** `fact-find.md` is the formal loop output artifact for this skill. Required sections and frontmatter fields are defined in `docs/business-os/startup-loop/contracts/loop-output-contracts.md` (Artifact 1). The path above is authoritative; do not store this artifact at any other location.
- Progressive-disclosure sidecar: after validators pass, generate `docs/plans/<feature-slug>/fact-find.packet.json` per `docs/business-os/startup-loop/contracts/do-stage-handoff-packet-contract.md`.
- Include `## Scope Signal` in the artifact body:
  - `Signal: <constrained | right-sized | limited-thinking>`
  - `Rationale: <evidence-based reason>`
  - `Expansion suggestions` subsection is required only when signal is `limited-thinking`.

## Phase 6.1: Outcome Contract Gate (Non-Omittable)

Before moving to Phase 6.5, enforce outcome-contract continuity:

- `## Outcome Contract` section must exist in `fact-find.md` (non-omittable).
- Dispatch-routed path: populate `Why` and `Intended Outcome` from dispatch payload fields (`why`, `intended_outcome`) when present.
- Direct-inject path: populate from frontmatter `Trigger-Why` and `Trigger-Intended-Outcome`.
- If values are unavailable, set explicit fallback:
  - `Why: TBD`
  - `Source: auto`
- Do not leave outcome fields blank and do not fabricate operator-authored values.

## Phase 6.2: Unknown Prescription Discovery Contract (When Present)

If the queued work item carries `self_evolving.discovery_contract`, the fact-find must emit a machine-readable discovery output in the brief body. This is required for unknown or hypothesized prescriptions and is not optional narrative.

Write a `## Discovery Contract Output` section with:
- `Gap Case ID: <gap_case_id>`
- `Recommended First Prescription: <prescription_id>`
- `Required Inputs:` flat list
- `Expected Artifacts:` flat list
- `Expected Signals:` flat list
- `Prescription Candidates:` one flat bullet per candidate, each including:
  - `Prescription ID`
  - `Prescription Family`
  - `Required Route`
  - `Required Inputs`
  - `Expected Artifacts`
  - `Expected Signals`

Rules:
- Narrative may explain the recommendation, but it cannot replace these machine fields.
- `Recommended First Prescription` must match one candidate in `Prescription Candidates`.
- If evidence is still insufficient, keep the section but mark unresolved fields explicitly; do not omit the section.

## Phase 6.5: Open Question Self-Resolve Gate

Before running the evidence gap review or critique, review every question currently marked as Open.

Self-resolve any question answerable from available evidence and business constraints; move it to `Resolved` with evidence/logic. Keep a question in `Open` only when operator-only knowledge is required (undocumented preference/intent, unavailable real-world fact, or genuine preference fork). Default posture: reason and recommend rather than defer.

## Phase 7: Mandatory Evidence Gap Review (Outcome A)

Before marking `Ready-for-analysis`, run checklist:

- `docs/plans/_templates/evidence-gap-review-checklist.md`

Then write outcomes into the brief section:

- `## Evidence Gap Review`
- `### Gaps Addressed`
- `### Confidence Adjustments`
- `### Remaining Assumptions`

If unresolved blockers remain, classify the blocker type before setting status:

- **Recoverable** (missing evidence, awaiting user input, resolvable with more investigation): set `Status: Needs-input`, ask the minimal blocking questions, and stop.
- **Structural / infeasible** (architecture prevents this, risk is prohibitive, fundamental scope mismatch, or no viable path exists regardless of evidence gathered): set `Status: Infeasible`, write a `## Kill Rationale` section with a one-sentence explanation, and stop. Do not route to planning.

### Minimum Evidence Floor Gate

Before critique, ensure minimum substance exists. If floor fails, set `Status: Needs-input` and stop (do not critique empty briefs):
- Code: ≥1 entry-point path, ≥1 key module with role, test landscape present.
- Business: ≥1 hypothesis, `Delivery-Readiness` ≥ 60%.
- Mixed: must pass both.

## Phase 7a: Critique Loop (1–3 rounds, mandatory)

After persisting the fact-find artifact and completing the evidence gap review, run the critique loop in **fact-find mode**.

Load and follow: `../_shared/critique-loop-protocol.md`

## Phase 7b: Deterministic Validators

After critique and before setting `Status: Ready-for-analysis`, run:

```bash
scripts/validate-fact-find.sh docs/plans/<feature-slug>/fact-find.md docs/plans/<feature-slug>/critique-history.md
scripts/validate-engineering-coverage.sh docs/plans/<feature-slug>/fact-find.md
```

Rules:
- `validate-fact-find.sh` is required for all fact-finds.
- `validate-engineering-coverage.sh` is required for `Execution-Track: code | mixed`.
- If either required validator fails, fix the artifact or keep status below `Ready-for-analysis`.

After required validators pass, generate the stage handoff packet:

```bash
scripts/generate-stage-handoff-packet.sh docs/plans/<feature-slug>/fact-find.md
```

After required validators pass, emit a skill liveness observation so the BOS in-progress dashboard shows this fact-find as actively running:

```bash
pnpm --filter scripts tsx scripts/src/startup-loop/write-skill-observation.ts -- \
  --slug <feature-slug> --skill lp-do-fact-find --step fact-find --business <BUSINESS>
```

Fail-open: if the script exits non-zero, log a warning and continue. The fact-find must not be blocked by observation write failures.

After required validators pass, append workflow-step telemetry:

```bash
pnpm --filter scripts startup-loop:lp-do-ideas-record-workflow-telemetry -- --stage lp-do-fact-find --feature-slug <feature-slug> --module <loaded-module-relative-to-stage-skill> [--module <additional-module>] [--input-path <repo-relative-extra-input>] --deterministic-check scripts/validate-fact-find.sh [--deterministic-check scripts/validate-engineering-coverage.sh]
```

Rules:
- Record once per materially updated fact-find artifact.
- Include the actual stage-local modules loaded in Phase 5 and any extra repo inputs that materially contributed context size.
- Codex token usage is auto-captured when `CODEX_THREAD_ID` is available.
- Claude token usage is auto-captured via project session logs (sessions-index.json → debug/latest fallback). Explicit `--claude-session-id` still takes priority when supplied.

## Completion Message

> Fact-find complete. Brief saved to `docs/plans/<feature-slug>/fact-find.md`. Status: `<Ready-for-analysis | Needs-input | Infeasible>`. Primary execution skill: `<skill>`. Evidence gap review complete. Critique: `<N>` round(s), final verdict `<credible | partially credible | not credible>`, score `<X.X>`/5.0.

Status-dependent next action (execute immediately, do not wait for user):

- `Ready-for-analysis` → automatically invoke `/lp-do-analysis <feature-slug>` to continue the pipeline.
- `Needs-input` → surface the specific blocking questions, then stop. Do not invoke `/lp-do-analysis`.
- `Infeasible` → surface the kill rationale, then stop. Pipeline ends here.

## Quick Validation Gate

- [ ] Phase 0 queue check run — matching queued packet confirmed or direct-inject path taken
- [ ] Access declarations listed and verified (or `None` recorded) before investigation begins
- [ ] Routing header computed and written to frontmatter
- [ ] Dispatch-routed metadata written correctly (`Dispatch-ID` for single packet, `Dispatch-IDs` + `Work-Package-Reason` for bundled packet sets)
- [ ] Only relevant module(s) loaded
- [ ] Scope signal classified (`constrained`, `right-sized`, or `limited-thinking`) with evidence-backed rationale
- [ ] `## Outcome Contract` present and populated (dispatch payload or trigger frontmatter; fallback `Why: TBD`, `Source: auto` when unavailable)
- [ ] `## Current Process Map` present (or explicit `None: local code path only`)
- [ ] For code/mixed work, `## Engineering Coverage Matrix` present with all canonical rows
- [ ] Outcome A evidence gap review completed and recorded
- [ ] lp-do-factcheck run if fact-find contains codebase claims (file paths, function names, coverage assertions)
- [ ] Deterministic validators run (`validate-fact-find.sh`; and for code/mixed `validate-engineering-coverage.sh`)
- [ ] `fact-find.packet.json` generated after validators pass
- [ ] Workflow-step telemetry appended after validators pass
- [ ] Status classified as `Ready-for-analysis`, `Needs-input`, or `Infeasible` (not left ambiguous)
- [ ] If `Ready-for-analysis`: `/lp-do-analysis <feature-slug>` automatically invoked
