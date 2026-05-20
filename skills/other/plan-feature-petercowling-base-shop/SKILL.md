---
name: plan-feature
description: Create a confidence-gated execution plan for a feature or business deliverable, then auto-continue to build if eligible. Produces a plan doc with atomic tasks, acceptance criteria, execution routing, and per-task confidence assessments.
---

# Plan Feature

Create a confidence-gated execution plan for a feature or business deliverable, then auto-continue to build when eligible. Produces a plan doc with atomic tasks, acceptance criteria, and per-task confidence assessments.

**CI policy:** CI≥90 is a motivation/diagnostic, not a quota. Preserve breadth by phasing/deferment and by adding "What would make this ≥90%" notes. The **build gate** is still confidence-based: only IMPLEMENT tasks ≥80% proceed to `/build-feature`.

**Auto-continue:** After planning completes, if there are no open questions and ≥1 IMPLEMENT task at ≥80% confidence, this skill automatically invokes `/build-feature` on the plan. No user intervention required for the handoff.

## Operating Mode

**PLANNING → AUTO-BUILD**

**Planning phase:** read files, search repo, inspect tests, trace dependencies, inspect business artifacts/channels, run validations (tests or artifact checks), run read-only commands (e.g., `rg`, `ls`, `cat`, `npm test -- --listTests`), consult existing `docs/plans`, consult external docs if needed, write test stubs for L-effort code tasks.

**Not allowed during planning:** implementation code changes, refactors, migrations applied, running destructive commands, opening PRs.

**Auto-continue phase:** After the plan is persisted and sequenced, if auto-continue criteria are met (see step 12), invoke `/build-feature` which transitions to full build mode.

**Commits allowed:**
- Plan file (`docs/plans/<slug>-plan.md`)
- Test stub files for L-effort code tasks
- If BOS integration active: card/stage-doc updates via agent API (no markdown writes)

## Inputs

Use the best available sources, in this priority order:

1. Fact-find brief from `/fact-find` (preferred)
2. Existing plan doc(s) in `docs/plans/`
3. Feature request / ticket / user prompt
4. Repo and operating reality (current systems, assets, channels, and validations)

If a fact-find brief does not exist, proceed only if the feature is genuinely well-understood; otherwise, create INVESTIGATION tasks to raise confidence rather than guessing.

### Validation Foundation Check (Required when fact-find exists)

When starting from a fact-find brief, verify the brief provides adequate validation foundation for the chosen execution track.

**Required in fact-find brief (all tracks):**
- [ ] `Deliverable-Type`, `Execution-Track`, and `Primary-Execution-Skill`
- [ ] `Startup-Deliverable-Alias` is set to a supported value for startup work, otherwise `none`
- [ ] `Delivery-Readiness` confidence input (0-100%)

**Additionally required for `code` or `mixed` tracks:**
- [ ] Test Landscape section with: infrastructure, patterns, coverage, gaps
- [ ] Testability assessment (easy/hard to test, seams needed)
- [ ] Testability confidence input (0-100%)

**Additionally required for `business-artifact` or `mixed` tracks:**
- [ ] Delivery & Channel Landscape section (audience, channel constraints, approvals, measurement)
- [ ] Hypothesis & Validation Landscape section (key hypotheses, existing signal coverage, falsifiability assessment, recommended validation approach) — this feeds the Business VC Quality Checklist

**If required validation foundation is missing or incomplete:**
- Do NOT proceed with planning
- Return to `/fact-find` to complete missing sections
- Planning without validation foundation leads to low-quality execution

### Consuming Fact-Find Confidence Inputs

If the fact-find brief includes Confidence Inputs (Implementation, Approach, Impact, Delivery-Readiness, Testability), use them as **starting baselines** for task confidence:

| Fact-Find Input | Informs |
|-----------------|---------|
| Implementation confidence | Individual task confidence scores |
| Approach confidence | Overall plan confidence; triggers DECISION tasks if <80% |
| Impact confidence | Blast radius accuracy; triggers INVESTIGATION tasks if <80% |
| Delivery-Readiness confidence | Execution feasibility by channel/owner/quality gate |
| Testability confidence | Validation contract completeness expectations (especially for code/mixed) |

**Handoff rules:**
- If any fact-find confidence input is <80%, the plan MUST include tasks to raise it (INVESTIGATION or DECISION)
- If Delivery-Readiness is <80%, add explicit enablement tasks (owner assignment, approval path, quality rubric, channel/tool setup)
- Do not claim 90%+ task confidence if fact-find's testability confidence was <70%
- Task confidence cannot exceed fact-find's implementation confidence by >10% without new evidence

### Slug Stability

When a Card-ID is present (BOS integration), read `Feature-Slug` from the card frontmatter rather than re-deriving it. This ensures consistency across fact-find → plan → build.

### Execution Routing Stability

When fact-find provides `Primary-Execution-Skill` and `Supporting-Skills`, preserve them unless new evidence justifies a change.

- If changing execution routing, record the reason in the plan Decision Log.
- Every IMPLEMENT task must carry an explicit `Execution-Skill` field.

## Outputs

- Create or update one plan file: `docs/plans/<feature-slug>-plan.md`
- For L-effort code tasks: test stub files (failing tests that define acceptance criteria)
- No implementation code changes
- Commits: plan file only (S/M) or plan file + test stubs (L code tasks)

## Non-goals

- Writing implementation code
- Producing vague "do X somehow" tasks
- Inflating confidence without evidence (pattern references, file paths, tests, etc.)
- Duplicating existing plan docs
- Under-classifying effort to avoid validation requirements
- Deferring complex tasks because they require more upfront validation
- Splitting L-effort tasks into smaller tasks solely to avoid writing test stubs
- Deleting planned work purely to raise confidence (phase or defer instead, unless the user explicitly changes scope)

## When to Use

Run `/plan-feature` when:

- A fact-find brief is complete and ready for planning (preferred entry point)
- The feature is well-understood and doesn't require extensive investigation
- An existing plan needs significant revision or new tasks added

Do **not** use `/plan-feature` if:
- You need to understand the current system first → use `/fact-find`
- You're addressing low-confidence tasks in an existing plan → use `/re-plan`
- You're ready to implement → use `/build-feature`

## Fast Path (with argument)

**If user provides a slug or card ID** (e.g., `/plan-feature commerce-core` or `/plan-feature BRIK-ENG-0020`):
- Skip discovery entirely
- If slug: read `docs/plans/<slug>-fact-find.md` directly (or create new plan)
- If card ID: look up plan link from card file
- **Target: <2 seconds to start planning**

## Discovery Path (no argument)

**If user provides no argument**, read the pre-computed index (single file):

```
docs/business-os/_meta/discovery-index.json
```

Present the `readyForPlanning` array as a table:

```markdown
## Ready for Planning

| Slug | Title | Card | Business |
|------|-------|------|----------|
| commerce-core-readiness | Commerce Core Readiness | - | - |
| email-autodraft-response-system | Email Autodraft Response System | BRIK-ENG-0020 | BRIK |

Enter a slug to start planning, or describe a new feature.
```

## Status Vocabulary (canonical)

Use these values consistently across all plan documents:

**Plan Status** (frontmatter):
- `Draft` — plan is being written and not ready for build (do not ship as final output)
- `Active` — plan is approved and work may proceed (set when ready for `/build-feature`)
- `Complete` — all tasks done
- `Superseded` — replaced by a newer plan

**Transition to Active:** Set Status to `Active` when:
- All intended tasks are captured
- DECISION tasks are either resolved or explicitly marked non-blocking
- All IMPLEMENT tasks have validation contracts (TC-XX and/or VC-XX enumerated)
- The plan has been reviewed (by user or via explicit approval)

**Task Status** (per-task field):
- `Pending` — not yet started
- `In-Progress` — currently being worked
- `Complete (YYYY-MM-DD)` — done, with completion date
- `Blocked` — cannot proceed due to dependency or uncertainty
- `Superseded` — replaced by another task
- `Needs-Input` — waiting for user decision

## Workflow

### 1) Intake and scope alignment

- Identify the feature name and a stable **feature slug** for the plan filename.
- Define:
  - **Goals** (what success looks like)
  - **Non-goals** (explicit out-of-scope)
  - **Constraints** (performance, compatibility, security, rollout, deadlines if provided)
  - **Assumptions** (only if truly necessary; keep short)

### 2) Locate prior work and avoid duplicates

- Check `docs/plans/` for related work.
- If a plan exists: **update it** (preserve task IDs; append new tasks; mark superseded items).
- If multiple overlapping docs exist: consolidate into the most relevant plan and note consolidation in a short "Decision Log" entry.

### 3) Study the evidence base (evidence-first)

Do enough study to justify task confidence. Minimum checklist:

- For `code` or `mixed` tracks:
  - Identify entry points for the feature (routes/controllers/handlers/commands/UI components).
  - Identify data models touched (DB schema, domain models, API contracts).
  - Identify integration points (external services, queues, caches, auth).
  - Identify performance-sensitive paths (N+1 queries, missing caching, high-frequency code paths the feature touches).
  - Identify security boundaries (auth/authorization on affected routes, data access controls, input validation for untrusted data).
  - Identify test coverage and the correct test layer(s) (unit/integration/e2e).
  - Identify configuration/feature-flag patterns already used.
  - Identify observability patterns (logging, metrics, tracing, error reporting).
- For `business-artifact` or `mixed` tracks:
  - Identify channel/tool constraints and format requirements.
  - Identify source inputs and owners (data tables, campaign context, recipient segments, approvals).
  - Identify compliance/brand/privacy rules and failure modes.
  - Identify measurement/feedback loop needed post-delivery.
- Identify standing documentation that may need updates (playbooks, briefs, runbooks, channel docs).

When you reference patterns, include:
- File paths (and line numbers if easy)
- The name of an existing similar feature/module or artifact/playbook where applicable

### 4) Validate understanding through execution-relevant checks (effort-scaled)

Run validation appropriate to the execution track to verify understanding matches reality.

| Effort | Code / Mixed Validation | Business-Artifact Validation |
|--------|--------------------------|------------------------------|
| S | Run tests for directly affected files; ≥1 TC per acceptance criterion | Run one dry-run checklist against a sample deliverable |
| M | Run tests for affected modules + boundaries; test case specs with expected assertions | Run channel/approval checklist + one reviewed sample artifact |
| L | Run full test suites + write test stubs (`test.todo`) that implement TC specifications | Run full artifact acceptance rubric + at least one rehearsal/sample handoff |

**Check for extinct tests first (code/mixed only):**

Before relying on existing tests for validation, verify they are still valid:
- Read test assertions and confirm they test *current* behavior, not obsolete contracts
- Tests are "extinct" if they assert behavior that no longer exists or test removed APIs
- Note any extinct tests found — they must be updated or removed during `/build-feature`
- Do not count extinct test results as validation evidence

**What to capture for each task:**
- Which validation commands/checks ran and their results
- Any unexpected failures or behaviors discovered
- Validation evidence that exercises the contracts/boundaries you'll depend on
- Any extinct tests discovered (flag for update during build, code/mixed only)
- For L code tasks: file paths of test stubs written

**Confidence adjustment rules:**
- If validation reveals unexpected behavior → confidence drops (evidence trumps reasoning)
- For M/L tasks, confidence >80% requires documented validation evidence
- Pure reasoning without validation evidence caps M/L tasks at 75%
- For business-artifact/mixed tasks, confidence is capped unless the fail-first loop is evidenced:
  - No Red evidence (falsification attempt) → cap at 79%
  - Red complete but no Green pass evidence → cap at 84%
  - Green complete but no Refactor evidence → cap at 89%

**For L code or mixed tasks — write test stubs:**
- Translate acceptance criteria into test skeletons using `test.todo()` or `it.skip()` (non-failing)
- Include the test name, TC-XX reference, and a comment describing the expected assertion
- These validate that you understand what "done" looks like in executable terms
- Stubs become the starting point for build-feature's TDD cycle (code/mixed tasks only)
- Commit test stubs with the plan (allowed exception to "no code changes")

**Test stub format (non-failing):**
```typescript
describe('Feature: <feature-name>', () => {
  // TC-01: <scenario> → <expected outcome>
  test.todo('should <expected behavior>');

  // TC-02: <error case> → <expected outcome>
  test.todo('should return error when <condition>');
});
```

**Why non-failing:** Test stubs use `test.todo()` or `it.skip()` so they don't break CI. Build-feature converts them to active tests at task start, then watches them fail for the right reason.

**For business-artifact or mixed tasks — use a fail-first validation loop (non-code TDD analog):**
- **Red (falsify first):** Define VC-XX checks, then run a disconfirming probe (sample artifact, model run, market-research slice, or checklist dry-run) expected to fail at least one VC or expose a missing input/constraint.
- **Green (minimum pass):** Produce the smallest viable artifact/process update that passes all scoped VC-XX checks.
- **Refactor (harden):** Improve clarity/reuse/operability without changing scope; rerun VC checks to confirm no regression.
- This loop is required evidence for business-artifact tasks claiming >80% confidence.
- All VC-XX checks must satisfy the **Business VC Quality Checklist** (see below).

#### Business VC Quality Checklist

Good unit tests are fast, isolated, repeatable, and self-validating. Business VCs must meet equivalent standards. Every VC-XX check must satisfy ALL of the following:

| Principle | Code TDD analog | Business VC requirement |
|-----------|-----------------|------------------------|
| **Isolated** | Test one unit | Test one variable. A VC that conflates price AND channel AND audience is untestable — split into separate VCs. |
| **Pre-committed** | Assert before run | State the pass/fail decision before seeing data. "If <5 preorders in 7 days → kill" not "we'll see how it goes." |
| **Time-boxed** | Test runs in ms | Define when the result will be read. Every VC has a measurement deadline, not an open-ended observation window. |
| **Minimum viable sample** | Smallest fixture | Define the smallest signal that constitutes evidence. "3 conversions from 200 visitors" not "enough traction." |
| **Diagnostic** | Failure message | A failing VC must indicate *why* it failed, not just *that* it failed. Structure the check so the failure mode is attributable (wrong price vs. wrong audience vs. wrong channel). |
| **Repeatable** | Deterministic | Another operator running the same check with the same inputs should reach the same pass/fail conclusion. Avoid VCs that depend on subjective judgment without a rubric. |
| **Observable** | No side effects | The metric is directly measurable, not inferred. "Preorder count" not "perceived demand." |

**Anti-patterns (reject these):**
- `VC-01: Validate demand is sufficient` — not isolated, not pre-committed, not observable
- `VC-02: Check market response` — no sample size, no deadline, not diagnostic
- `VC-03: Confirm unit economics work` — conflates margin, CAC, and LTV in one check

**Good examples:**
- `VC-01: Price acceptance — ≥5 completed preorders at €X within 14 days of ad launch → pass; <5 → kill or reprice`
- `VC-02: Channel viability — CAC from Instagram ads ≤€Y over first €Z spend → pass; >€Y → test alternate channel`
- `VC-03: Margin floor — landed COGS ≤40% of retail price per supplier quote → pass; >40% → renegotiate or kill`

**If validation reveals problems:**
- Document unexpected findings in the task
- Adjust confidence scores based on evidence
- Create INVESTIGATION tasks for areas that need deeper understanding

#### Assumption scouting (proactive dead-end prevention)

Beyond running existing tests, **actively probe risky assumptions** before they become embedded in the plan. The goal is to discover dead ends during planning (cheap) rather than during build (expensive).

**What to scout:**
- **API/library feasibility:** If the plan depends on a library or framework supporting X, look up the official docs and verify. Write a minimal probe test if the docs are ambiguous.
- **Contract compatibility:** If task N depends on a data shape or interface from task N-1, write a type-level or schema-level test that verifies the contract exists or can be created.
- **Integration seams:** If two systems need to connect, verify both sides of the seam exist and are compatible. Run existing integration tests that cross the boundary.
- **Platform constraints:** If deploying to a specific environment (Cloudflare Workers, static export, etc.), verify the feature is supported in that runtime.

**How to scout:**
- **Doc lookup:** Check official docs for the exact version in use (verify against `package.json` / lockfile). Cite the doc URL and version.
- **Probe test:** Write a small, throwaway test that exercises the assumption. If it passes, you have E2 evidence. If it fails, you've caught a dead end before planning around it.
- **Existing test run:** Run tests that exercise the contract or boundary you'll depend on.
- **Type-level check:** Run `tsc` against a minimal type assertion to verify a contract holds.

**Scout results feed confidence:**
- Scout passes → E2 evidence → confidence can increase
- Scout fails → assumption disproved → create INVESTIGATION task or revise approach
- Scout inconclusive → flag as risk, keep confidence where it is

**Where scouts appear in the plan:**
Each IMPLEMENT task that depends on a non-obvious assumption should include a `Scouts` field listing what was probed and what was found. This is distinct from the validation contract (which verifies the deliverable) — scouts test the assumptions the deliverable depends on.

### 5) Decide the approach (with alternatives when warranted)

- Write the proposed approach as a concise execution design (architecture for code tasks, operating design for business-artifact tasks).
- If there are multiple viable approaches, document:
  - Option A / Option B
  - Trade-offs
  - Why the chosen approach is best long-term (or why the decision is deferred via a DECISION task)

### 6) Break work into atomic tasks

#### Planning Horizon & Risk Front-Loading

Plans with many tasks in a dependency chain carry **compounding uncertainty** — task 8 depends on assumptions from tasks 1–7, any of which could prove wrong. Mitigate this:

**Front-load risk validation:**
- Order tasks so the riskiest assumptions are tested first. If the whole feature depends on "X is possible," task 1 should prove X.
- Early tasks should be the ones most likely to reveal dead ends. If task 1 fails, you've wasted one task, not eight.
- Each task should leave the codebase in a valid state — no task should be a "point of no return" that commits you to the full plan.

**Keep tasks independently valuable:**
- Prefer tasks that deliver incremental value even if later tasks are abandoned or replanned.
- Avoid tasks that only make sense if all subsequent tasks also land (unless truly unavoidable).
- If a task creates a new abstraction, it should be usable even if the planned consumers change.

**Insert CHECKPOINT tasks at horizon boundaries:**
- When a plan has **>3 IMPLEMENT tasks in a dependency chain**, insert a `CHECKPOINT` task after the first 2–3 IMPLEMENT tasks.
- A CHECKPOINT is a lightweight re-assessment gate: "Given what we've built so far, does the rest of the plan still make sense?"
- CHECKPOINTs don't produce code — they produce an updated plan (via `/re-plan`).
- Auto-continue builds up to the first CHECKPOINT, then pauses for re-assessment before continuing.

**CHECKPOINT task format:**
```markdown
### TASK-XX: Horizon checkpoint — reassess remaining plan
- **Type:** CHECKPOINT
- **Depends on:** <last IMPLEMENT task before the boundary>
- **Blocks:** <first IMPLEMENT task after the boundary>
- **Confidence:** 95%
- **Acceptance:**
  - Run `/re-plan` on all tasks after this checkpoint
  - Reassess remaining task confidence using evidence from completed tasks
  - Confirm or revise the approach for remaining work
  - Update plan with any new findings, splits, or abandoned tasks
- **Horizon assumptions to validate:**
  - <assumption 1 that later tasks depend on — should now be verified by completed work>
  - <assumption 2>
```

**When to insert CHECKPOINTs:**
- After the first 2–3 tasks that validate the core approach
- At natural phase boundaries (e.g., data layer done → UI layer starts)
- Before any task that depends on assumptions not yet proven by completed work
- When the dependency chain crosses 3+ waves in the Parallelism Guide

**When NOT to insert CHECKPOINTs:**
- Plans with ≤3 total IMPLEMENT tasks (too short to need them)
- All tasks are independent (no dependency chain to compound uncertainty)
- All tasks follow well-established patterns with E2+ evidence

**Rules:**
- One logical unit per task (typically one file or one cohesive change set).
- Order tasks so riskiest assumptions are validated first, then by prerequisites (infra/contracts before consumers). This is an initial authoring heuristic — `/sequence-plan` (step 10a) will formalize the ordering, renumber tasks, and add blocker metadata.
- If decomposition is needed (for example, splitting one task into precursor + implementation tasks), complete all task content edits first, then run `/sequence-plan` before any completion message or auto-continue handoff.
- Each task must include:
  - **Affects** (file paths/modules — see format below)
  - **Deliverable** (type + artifact/output location)
  - **Startup-Deliverable-Alias** (`none` unless startup-specific)
  - **Execution-Skill** (primary skill to execute task work)
  - **Dependencies** (TASK-IDs)
  - **Acceptance criteria**
  - **Validation contract** (test contract for code, quality rubric for non-code)
  - **Rollout/rollback** (feature flag, migration strategy, safe deploy)
  - **Documentation impact** (standing docs to update, or "None" if no docs affected)
  - **Notes** (links/pattern references)
  - For `business-artifact` or `mixed` tasks (mandatory):
    - **Artifact-Destination** (where the final artifact is published/handed off)
    - **Reviewer** (named person/role that must acknowledge completion)
    - **Approval-Evidence** (path/link/comment proving reviewer acknowledgement)
    - **Measurement-Readiness** (metric owner + cadence + tracking location)

**Affects field format:**
- **Primary** (files being modified): `src/path/to/file.ts`
- **Secondary** (read-only dependencies): `[readonly] src/path/to/types.ts`

Use `[readonly]` prefix for files that must be read to understand contracts but won't be changed. This helps `/build-feature` distinguish scope boundaries — modifying a `[readonly]` file is a scope expansion that requires re-planning.

**Validation contract requirements:**
- Every acceptance criterion must map to a concrete verification step.
- Use one of the following formats:
  - Code/mixed tasks: `TC-XX: <scenario> → <expected outcome>`
  - Business-artifact tasks: `VC-XX: <quality check> → <pass condition>`
- Include happy path, error/failure cases, and edge conditions relevant to the channel.
- For M/L tasks, validation cases become the execution contract.
- "Validate quality" is not sufficient; enumerate the scenarios/checks.
- Every IMPLEMENT task must include an explicit execution plan:
  - Code/mixed tasks: **Red → Green → Refactor**
  - Business-artifact tasks: **Red → Green → Refactor (VC-first fail-first loop)**
    - Red: run a falsification probe before drafting final output
    - Green: minimum deliverable that passes VC checks
    - Refactor: improve quality/operability while keeping VC checks green
- If a task spans multiple apps/services/packages, include cross-boundary **contract tests** for shared schemas/nodes/events.
- If a task spans multiple channels/teams, include cross-boundary validation (handoff, approval, and measurement readiness).
- For `business-artifact` or `mixed` tasks, `Artifact-Destination`, `Reviewer`, `Approval-Evidence`, and `Measurement-Readiness` are required fields, not optional notes.

If something is uncertain, create an explicit **INVESTIGATION** task (to raise confidence) or a **DECISION** task (to choose between alternatives). Do not bury uncertainty inside implementation tasks.

If the planning horizon is long, insert a **CHECKPOINT** task at natural boundaries (see "Planning Horizon & Risk Front-Loading" above). CHECKPOINTs force a re-assessment before committing to deep implementation.

### 7) Classify effort honestly (no gaming)

Effort classification determines validation requirements. Classify based on objective criteria, not to minimize validation work.

#### Effort criteria (use the HIGHEST applicable level)

| Criterion | S | M | L |
|-----------|---|---|---|
| Files affected | 1–2 | 3–5 | 6+ |
| Integration boundaries crossed | 0 | 1–2 | 3+ |
| New patterns introduced | None | Minor variation | New pattern |
| External dependencies touched | None | Existing only | New or modified |
| Data model changes | None | Additive only | Schema migration |
| Test layers needed | Unit only | Unit + integration | Unit + integration + e2e |

**Rules:**
- If ANY criterion hits L → the task is L-effort
- If ANY criterion hits M (and none hit L) → the task is M-effort
- S-effort only if ALL criteria are S-level

**Anti-gaming provisions:**
- Do not artificially split tasks to reduce effort classification. If the logical unit of work is L-effort, plan it as L-effort.
- Do not defer complex tasks because they require stronger validation artifacts (test stubs, rehearsal evidence, or approval gates). The validation work is proportional to the risk—skipping it doesn't reduce the risk, it just hides it.
- If during build the actual scope exceeds the classified effort, build-feature will trigger `/re-plan`.

### 8) Confidence scoring (per task, evidence-based)

For each task, assign three dimension scores (0–100%). The overall confidence = min(Implementation, Approach, Impact).

#### Dimension definitions

| Dimension | What it measures | Evidence to cite |
|-----------|------------------|------------------|
| **Implementation** | We know how to execute the deliverable correctly | Existing pattern/playbook, known tools/APIs, similar prior deliverables, validation harness exists |
| **Approach** | This is the right long-term design | Architectural fit, avoids tech debt, aligns with conventions |
| **Impact** | We understand what it touches and how to avoid regressions | Dependencies identified, contracts/channels clear, rollout/send path understood |

#### Scoring rubric (use consistently)

- **90–100:** Clear precedent + low novelty + testable + isolated impact
- **80–89:** Straightforward, minor unknowns, mitigations identified
- **60–79:** Material uncertainty remains; proceed only with explicit risks and verification steps
- **<60:** Do not build. Convert to INVESTIGATION/DECISION and trigger `/re-plan` for that area.

**Interpretation note:** Confidence ≥90% is not required to plan or build. If a task is <90, keep it in scope but include a short “What would make this ≥90%” note (tests, spikes, evidence, rollout rehearsal) that would raise confidence without deleting work.

#### Required "why" text

For each dimension, include one sentence explaining the score and what evidence supports it.

#### Evidence requirements by effort (for >80% confidence)

| Effort | Required Evidence |
|--------|-------------------|
| S | Patterns identified; file paths/artifact destinations documented; ≥1 validation case per acceptance criterion |
| M | Above + validation evidence captured (tests pass or checklist/review pass) + expected outcomes documented |
| L | Above + (code tasks) failing test stubs committed OR (business-artifact tasks) rehearsal/sample artifact evidence committed |

**Validation coverage gate:** A task cannot exceed 80% confidence without validation cases that cover all acceptance criteria. Vague plans ("we will validate later") cap confidence at 70%.

A task cannot exceed 80% confidence without executable or review evidence proportional to its effort level. Pure reasoning without validation evidence caps M/L tasks at 75%.

**Fail-first evidence gate (business-artifact/mixed tasks):**
- >79% requires explicit Red evidence (failed falsification or surfaced blocking gap)
- >84% requires Green evidence (all scoped VC checks pass)
- >89% requires Refactor evidence (quality/operability improvement with VC re-pass)

### 9) Resolve open questions yourself (before asking the user)

When confidence is low:
- Read more repo code (neighbors, call sites, types, tests)
- Trace dependencies (imports, routes, service wiring)
- Validate assumptions by locating authoritative sources (internal docs, official library docs)
- Prefer evidence over inference

Only ask the user when:
- Business rules/UX intent cannot be inferred from repo or docs
- Two approaches are truly equivalent and require preference
- You have exhausted evidence sources and the uncertainty remains

When you do ask:
- Ask the minimum number of questions required to proceed
- Each question must state what decision it gates
- Include a recommended default with risk assessment if appropriate

### 10) Persist the plan doc

Write/update `docs/plans/<feature-slug>-plan.md` using the template below.

Set frontmatter `Status: Active` in the final persisted plan unless the user explicitly says the plan should remain Draft.

### 10a) Sequence the plan (automatic; mandatory after decomposition)

After persisting the plan doc, run `/sequence-plan` on it. This:

- Topologically sorts tasks into correct implementation order based on explicit dependencies, file-overlap analysis, and phase ordering
- Renumbers tasks sequentially (`TASK-01`, `TASK-02`, ... or `DS-01`, `DS-02`, ... preserving domain prefix)
- Adds a `Blocks` field to every task (inverse of `Depends on`) so agents know what they unblock
- Generates a **Parallelism Guide** showing which tasks can be dispatched to concurrent subagents

**Decomposition rule:** if any task was split, added, removed, or had dependency topology changes during planning, `/sequence-plan` is required and cannot be skipped.

**This step modifies the plan doc that was just persisted in step 10.** The completion message (step 11) should reflect the sequenced state.

**Skip conditions:** Only skip this step if the plan has fewer than 2 active tasks **and** no decomposition/topology edits occurred.

### 11) Completion message (decision-oriented)

At the end, tell the user:
- Which tasks are **Ready** (≥80%)
- Which are **Caution** (60–79%)
- Which are **Blocked** (<60%) and require `/re-plan`
- The recommended next action (`/build-feature` or `/re-plan`)

## Plan Template

```markdown
---
Type: Plan
Status: Active
Domain: <CMS | Platform | UI | API | Data | Infra | etc.>
Workstream: <Engineering | Product | Marketing | Sales | Operations | Finance | Mixed>
Created: YYYY-MM-DD
Last-updated: YYYY-MM-DD
Feature-Slug: <kebab-case>
Deliverable-Type: <code-change | email-message | product-brief | marketing-asset | spreadsheet | whatsapp-message | multi-deliverable>
Startup-Deliverable-Alias: <none | startup-budget-envelope | startup-channel-plan | startup-demand-test-protocol | startup-supply-timeline | startup-weekly-kpcs-memo>
Execution-Track: <code | business-artifact | mixed>
Primary-Execution-Skill: <build-feature | draft-email-message | write-product-brief | draft-marketing-asset | create-ops-spreadsheet | draft-whatsapp-message>
Supporting-Skills: <comma-separated or none>
Overall-confidence: <weighted average %>
Confidence-Method: min(Implementation,Approach,Impact); Overall weighted by Effort
# Business OS Integration (default-on; set Business-OS-Integration: off for standalone work)
Business-OS-Integration: <on | off>  # default: on
Business-Unit: <BRIK | PLAT | PIPE | BOS | etc.>
Card-ID: <from fact-find or manually provided>
---

# <Feature Name> Plan

## Summary
<What we're building and why. 3–6 sentences max.>

## Goals
- <Goal 1>
- <Goal 2>

## Non-goals
- <Non-goal 1>
- <Non-goal 2>

## Constraints & Assumptions
- Constraints:
  - <perf/security/compatibility/rollout constraints>
- Assumptions:
  - <only if necessary>

## Fact-Find Reference
- Related brief: `docs/plans/<feature-slug>-fact-find.md` (if exists)
- Key findings: <inline bullets of key findings + resolved questions>

## Existing System Notes
- Key modules/files:
  - `path/to/area` — <why relevant>
- Patterns to follow:
  - <reference similar code by path/module name>

## Proposed Approach
<High-level design, data flow, contracts. Include alternatives if relevant.>
- Option A: <summary + trade-offs>
- Option B: <summary + trade-offs>
- Chosen: <A/B> because <reason>

## Task Summary
| Task ID | Type | Description | Confidence | Effort | Status | Depends on | Blocks |
|---|---|---|---:|---:|---|---|---|
| TASK-01 | IMPLEMENT | ... | 92% | M | Pending | - | TASK-02 |
| TASK-02 | INVESTIGATE | ... | 55% ⚠️ | S | Pending | TASK-01 | - |
| TASK-03 | DECISION | ... | 60% ⚠️ | S | Needs-Input | - | - |

> Effort scale: S=1, M=2, L=3 (used for Overall-confidence weighting)

## Parallelism Guide

_Generated by `/sequence-plan` (step 10a). Shows which tasks can run concurrently via subagents._

| Wave | Tasks | Prerequisites | Notes |
|------|-------|---------------|-------|
| 1 | ... | - | ... |

**Max parallelism:** N | **Critical path:** W waves | **Total tasks:** T

## Tasks

### TASK-01: <description>
- **Type:** IMPLEMENT
- **Deliverable:** <deliverable type + output location/path>
- **Startup-Deliverable-Alias:** <none | startup-budget-envelope | startup-channel-plan | startup-demand-test-protocol | startup-supply-timeline | startup-weekly-kpcs-memo>
- **Execution-Skill:** <build-feature | draft-email-message | write-product-brief | draft-marketing-asset | create-ops-spreadsheet | draft-whatsapp-message>
- **Artifact-Destination:** <required for business-artifact/mixed; where final output is published/handed off>
- **Reviewer:** <required for business-artifact/mixed; named owner/approver>
- **Approval-Evidence:** <required for business-artifact/mixed; link/path/comment proving acknowledgement>
- **Measurement-Readiness:** <required for business-artifact/mixed; metric owner + cadence + tracking location>
- **Affects:** `path/to/file.ts`, `path/to/other.ts`
- **Depends on:** <TASK-IDs or "-">
- **Blocks:** <TASK-IDs or "-"> _(populated by `/sequence-plan`)_
- **Confidence:** 92%
  - Implementation: 95% — <why>
  - Approach: 90% — <why>
  - Impact: 90% — <why>
- **Acceptance:**
  - <bullet list of verifiable outcomes>
- **Validation contract:**
  - **Code/mixed tasks (TC format):**
    - TC-01: <scenario> → <expected outcome>
    - TC-02: <error case> → <expected outcome>
    - TC-03: <edge case> → <expected outcome>
  - **Business-artifact tasks (VC format — each VC must pass the Business VC Quality Checklist):**
    - VC-01: <quality/brand/compliance check> → <pass condition + measurement deadline>
    - VC-02: <channel/format check> → <pass condition + minimum sample>
    - VC-03: <reviewer acknowledgement + approval evidence check> → <pass condition>
    - VC-04: <measurement readiness check (owner/cadence/tracking)> → <pass condition>
  - **Acceptance coverage:** <which acceptance criteria each TC/VC covers>
  - **Validation type:** <unit | integration | e2e | contract | review checklist | approval gate | dry-run>
  - **Validation location/evidence:** <test file path(s) or artifact review checklist path>
  - **Run/verify:** <command or review procedure>
  - **Cross-boundary coverage (if applicable):** <shared contract tests or cross-team/channel handoff checks>
- **Execution plan:**
  - **Code/mixed tasks:** Red → Green → Refactor
  - **Business-artifact tasks:** Red → Green → Refactor (VC-first fail-first loop)
  - **Red evidence:** <what was expected to fail, command/check run, observed failure or surfaced gap>
  - **Green evidence:** <minimum deliverable + VC checks that passed>
  - **Refactor evidence:** <what was improved and VC regression check result>
- **Scouts:** (include when task depends on non-obvious assumptions)
  - <assumption> → <how validated: doc lookup / probe test / existing test / type check> → <result: confirmed / disproved / inconclusive>
- **Planning validation:** (required for M/L effort)
  - Checks run: `<commands/procedures>` — <pass/fail, count>
  - Validation artifacts written: <test stubs, rehearsal samples, or checklist evidence paths>
  - Unexpected findings: <any behavior that differed from expectation, or "None">
- **What would make this ≥90%:** (include when task confidence <90%)
  - <concrete evidence/tests/spike that would raise confidence>
- **Rollout / rollback:**
  - Rollout: <flag/gradual rollout/migration steps>
  - Rollback: <safe revert strategy>
- **Documentation impact:**
  - <docs to update: e.g., `docs/architecture.md`, `README.md`, API docs — or "None">
- **Notes / references:**
  - <links to internal docs or code patterns>

### TASK-02: <description>
- **Type:** INVESTIGATE
- **Deliverable:** <analysis artifact output path>
- **Execution-Skill:** <build-feature or specialized skill>
- **Affects:** <areas to inspect>
- **Depends on:** <TASK-IDs or "-">
- **Blocks:** <TASK-IDs or "-"> _(populated by `/sequence-plan`)_
- **Confidence:** 55% ⚠️ BELOW THRESHOLD
  - Implementation: 70% — <why unknown>
  - Approach: 50% — <decision unresolved>
  - Impact: 45% — <unknown blast radius>
- **Blockers / questions to answer:**
  - <specific questions with concrete outputs>
- **Acceptance:**
  - <what evidence will raise confidence, e.g., "identify call sites; confirm contract; propose chosen approach; update plan">
- **Notes / references:**
  - <where to look in repo, likely files>

### TASK-03: <description>
- **Type:** DECISION
- **Deliverable:** <decision artifact output path>
- **Execution-Skill:** <build-feature or specialized skill>
- **Affects:** <areas impacted by this decision>
- **Depends on:** <TASK-IDs or "-">
- **Blocks:** <TASK-IDs or "-"> _(populated by `/sequence-plan`)_
- **Confidence:** 60% ⚠️ BELOW THRESHOLD
  - Implementation: 80% — both options are implementable
  - Approach: 50% — genuinely equivalent options; requires preference
  - Impact: 70% — impact understood but varies by choice
- **Options:**
  - **Option A:** <description + trade-offs>
  - **Option B:** <description + trade-offs>
- **Recommendation:** <A or B> because <rationale>
- **Question for user:**
  - <precise question that gates the decision>
  - Why it matters: <context>
  - Default if no answer: <option + risk>
- **Acceptance:**
  - User selects option; plan updated with decision; dependent tasks unblocked

## Risks & Mitigations
- <Risk>: <Mitigation>
- <Risk>: <Mitigation>

## Observability
- Logging: <what events/errors should be logged>
- Metrics: <key counters/timers>
- Alerts/Dashboards: <if applicable>

## Acceptance Criteria (overall)
- [ ] <Criterion 1>
- [ ] <Criterion 2>
- [ ] <No regressions / required validations passing>

## Decision Log
- YYYY-MM-DD: <Decision made> — <rationale>
```

## Overall-confidence calculation

Use Effort-weighted average of task overall confidence:

- S=1, M=2, L=3
- Overall-confidence = sum(confidence × weight) / sum(weight)

Note: This is informational only; build gating is still per-task.

## Quality Checks

A plan is considered complete only if:

- [ ] All potentially affected areas have been studied (not assumed).
- [ ] Each task has all required fields: Type, Deliverable, Execution-Skill, Affects, Depends on, Confidence (with dimension breakdown), Acceptance, Validation contract, Planning validation (for M/L), Rollout/rollback, Documentation impact.
- [ ] For `business-artifact`/`mixed` tasks, mandatory fields are present: Artifact-Destination, Reviewer, Approval-Evidence, Measurement-Readiness.
- [ ] Confidence scores are justified with evidence (file paths, patterns, tests).
- [ ] Validation completed per effort level (tests for code/mixed tasks; channel/approval checks for business-artifact tasks).
- [ ] For M/L tasks claiming >80% confidence: validation evidence is documented.
- [ ] INVESTIGATE/DECISION tasks are used for uncertainty (not buried in IMPLEMENT tasks).
- [ ] Dependencies are explicitly mapped and ordered correctly.
- [ ] `/sequence-plan` has been run: tasks are topologically sorted, renumbered, `Blocks` fields added, and Parallelism Guide generated.
- [ ] If tasks were decomposed (split/added/removed) during planning, `/sequence-plan` ran after the final structural edit and before any `/build-feature` handoff.
- [ ] Risks and mitigations are documented.
- [ ] User questions were asked only when genuinely unavoidable.
- [ ] Auto-continue criteria evaluated: no open questions + ≥1 task ≥80% → `/build-feature` invoked; otherwise reason for stopping documented.

### Validation Quality Checks

- [ ] Every acceptance criterion maps to ≥1 enumerated validation case (TC-XX or VC-XX).
- [ ] Validation cases include happy path, error cases, and edge cases.
- [ ] M/L tasks have validation case specifications with expected outcomes/pass conditions.
- [ ] `business-artifact`/`mixed` tasks do not use placeholder values (`TBD`, `TBC`, `later`) for Artifact-Destination, Reviewer, Approval-Evidence, or Measurement-Readiness when claiming >80% confidence.
- [ ] L code/mixed tasks have test stubs committed with the plan.
- [ ] L business-artifact/mixed tasks have rehearsal/sample validation evidence committed with the plan.
- [ ] No task claims >80% confidence without enumerated validation cases.
- [ ] Every IMPLEMENT task includes an explicit execution plan (Red→Green→Refactor for all tracks; business-artifact uses VC-first fail-first loop).
- [ ] Business-artifact/mixed tasks claiming >80% include Red, Green, and Refactor evidence fields with concrete checks/results.
- [ ] Every VC-XX check on business-artifact/mixed tasks passes the Business VC Quality Checklist (isolated, pre-committed, time-boxed, minimum viable sample, diagnostic, repeatable, observable).
- [ ] Tasks spanning multiple apps/services include cross-app contract tests for shared data contracts.
- [ ] Tasks spanning multiple channels/teams include cross-boundary handoff and approval checks.

### Validation Foundation Check (from Fact-Find)

Before planning tasks, verify the fact-find brief includes:
- [ ] Deliverable-Type, Execution-Track, Primary-Execution-Skill
- [ ] Startup-Deliverable-Alias (startup task) or `none` (non-startup task)
- [ ] Delivery-Readiness confidence input
- [ ] For code/mixed tracks: test infrastructure + patterns + coverage gaps + testability assessment
- [ ] For business-artifact/mixed tracks: delivery/channel landscape + approval + measurement constraints
- [ ] For business-artifact/mixed tracks: hypothesis & validation landscape (key hypotheses, signal coverage, falsifiability, recommended approach)

**If missing:** Create an INVESTIGATION task to complete the missing foundation, OR incorporate into first IMPLEMENT task with confidence penalty (-10% for missing foundation).

## Decision Points

| Situation | Action |
|-----------|--------|
| All IMPLEMENT tasks ≥80%, no open questions | **Auto-continue:** invoke `/build-feature` immediately |
| Some tasks ≥80%, others 60–79%, no open questions | **Auto-continue:** invoke `/build-feature` for eligible tasks; note remaining tasks need `/re-plan` |
| ≥1 IMPLEMENT task ≥80% but open DECISION/Needs-Input tasks exist | **Stop and ask:** present open questions to user; do NOT auto-continue |
| All IMPLEMENT tasks <80% | Do NOT build. Recommend `/re-plan` |
| Any IMPLEMENT task <60% | Do NOT build it. Convert to INVESTIGATE/DECISION and run `/re-plan` for that area |
| Genuine product/UX ambiguity | Ask the user only after repo/doc investigation |

## Auto-Continue to Build (Step 12)

After the completion message (step 11), evaluate whether to auto-continue:

### Auto-continue criteria (ALL must be true)

1. **No open questions:** No DECISION tasks with status `Needs-Input`, no unresolved user questions
2. **≥1 eligible task:** At least one IMPLEMENT task has confidence ≥80%
3. **Plan status is Active:** The plan was set to `Active` (not left as `Draft`)
4. **Topology is sequenced:** If tasks were decomposed or dependencies changed, `/sequence-plan` has run after those edits

### Auto-continue scope (CHECKPOINT-bounded)

Auto-continue builds only up to the **first CHECKPOINT task** in the plan. This prevents committing to deep implementation before validating near-horizon assumptions.

- If the plan has no CHECKPOINTs: auto-continue builds all eligible tasks (plan is short enough that horizon risk is acceptable)
- If the plan has CHECKPOINTs: auto-continue builds eligible tasks up to the first CHECKPOINT, then the CHECKPOINT triggers `/re-plan` on remaining tasks before continuing

This means a plan with 8 tasks and a CHECKPOINT after task 3 will:
1. Auto-continue → build tasks 1–3
2. Hit CHECKPOINT → run `/re-plan` on tasks 5–8 using evidence from tasks 1–3
3. If re-plan confirms remaining tasks → continue building
4. If re-plan reveals problems → revise before wasting more effort

### When criteria are met

- Output the completion message (step 11) noting auto-continuation
- Invoke `/build-feature <feature-slug>` immediately
- The build skill takes over from here with its own operating mode
- Build will automatically pause at the first CHECKPOINT for re-assessment

### When criteria are NOT met

- Output the completion message (step 11) with the blocking reason
- Do NOT invoke `/build-feature`
- Recommend the appropriate next action (`/re-plan`, answer DECISION tasks, etc.)

### Override

If the user explicitly says the plan should remain Draft or asks NOT to auto-build, respect that and stop after the completion message.

## Completion Output (what to say to the user)

**If all ≥80% and auto-continuing:**
> "Plan ready. All implementation tasks are ≥80% confidence. Tasks sequenced into N execution waves (max parallelism: P). Auto-continuing to `/build-feature`..."

**If some ≥80% and auto-continuing (others below threshold):**
> "Plan ready with blockers. Tasks <IDs> are below threshold (<%>). Tasks sequenced into N execution waves. Auto-continuing to `/build-feature` for eligible tasks. Recommend `/re-plan` for blocked tasks after initial build completes."

**If blocked from auto-continue (open questions):**
> "Plan ready but has open questions. Tasks <IDs> need decisions before build can proceed. Please resolve DECISION tasks, then run `/build-feature`."

**If blocked from auto-continue (all tasks <80%):**
> "Plan ready with blockers. No tasks are above the 80% build threshold. Recommend `/re-plan` to raise confidence before building."

---

## Business OS Integration (Default)

Plan documents integrate with Business OS by default when `Card-ID` is present.

### Escape Hatch (Exception Only)

Set `Business-OS-Integration: off` in plan frontmatter for intentionally standalone work.

### Planned Stage Doc Workflow (After Plan Completion)

**When:** after persisting the plan document, if `Card-ID` is present and `Business-OS-Integration` is omitted or `on`.

**Fail-closed:** if any API call fails, stop and surface the error.

**Step 1: Read card via API and lock Feature-Slug**

- Fetch the card via API.
- If card is missing: stop (it should exist from `/fact-find` or explicit setup).
- Read `Feature-Slug` from card frontmatter (do not re-derive from title).

```json
{
  "method": "GET",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards/PLAT-ENG-0023",
  "headers": { "X-Agent-API-Key": "${BOS_AGENT_API_KEY}" }
}
```

**Step 2: Create planned stage doc via API**

```json
{
  "method": "POST",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/stage-docs",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "cardId": "PLAT-ENG-0023",
    "stage": "plan",
    "content": "# Planned: {Feature Title}\n\n## Plan Reference\n\n**Plan Document:** `docs/plans/{feature-slug}-plan.md`\n\n**Overall Confidence:** {OVERALL-CONFIDENCE}%\n\n## Task Summary\n\n| Task ID | Description | Confidence | Status |\n|---------|-------------|------------|--------|\n{Table from plan document}\n\n## Key Decisions\n\n{Summarize key decisions from plan document}\n\n## Build Prerequisites\n\n- [ ] All IMPLEMENT tasks >=80% confidence\n- [ ] Dependencies resolved\n- [ ] Validation foundation ready for execution track\n\n## Transition Criteria\n\n**To Planned lane:**\n- Plan approved\n- No open `Needs-Input` decision gates\n- At least one build-eligible IMPLEMENT task\n"
  }
}
```

**Note:** `content` is markdown body only (no frontmatter). Export job adds frontmatter.

**Step 3: Update card Plan-Link via API**

```json
{
  "method": "PATCH",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards/PLAT-ENG-0023",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "baseEntitySha": "<entitySha from GET>",
    "patch": { "Plan-Link": "docs/plans/{feature-slug}-plan.md" }
  }
}
```

**Conflict handling:** if PATCH returns 409, refetch and retry once. If it conflicts again, stop and surface the error.

**Step 4: Deterministic lane transition (Fact-finding -> Planned)**

If all IMPLEMENT tasks are >=80% confidence and no `Needs-Input` DECISION tasks remain, move card directly:

```json
{
  "method": "PATCH",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards/PLAT-ENG-0023",
  "headers": {
    "X-Agent-API-Key": "${BOS_AGENT_API_KEY}",
    "Content-Type": "application/json"
  },
  "body": {
    "baseEntitySha": "<entitySha from GET>",
    "patch": {
      "Lane": "Planned",
      "Last-Progress": "YYYY-MM-DD"
    }
  }
}
```

If criteria are not met, keep lane `Fact-finding` and report blockers.

**Step 5: Discovery index freshness**

After card/stage-doc writes (and lane update when performed), rebuild discovery index:

```bash
docs/business-os/_meta/rebuild-discovery-index.sh > docs/business-os/_meta/discovery-index.json
```

Retry once; on repeated failure, stop and surface `discovery-index stale`.

On repeated failure, include:
- failing command,
- retry count,
- stderr summary,
- exact operator rerun command.

Do not emit an auto-continue success message while index state is stale.

### Completion Message (with Business OS)

When Card-ID is present and auto-continuing:

> "Plan ready. All implementation tasks are >=80% confidence.
>
> **Business OS Integration (default-on):**
> - Card: `<Card-ID>`
> - Planned stage doc created via API: `plan`
> - Card updated with Plan-Link via API
> - Deterministic lane transition applied: `Fact-finding -> Planned`
>
> Auto-continuing to `/build-feature`..."

When Card-ID is present but some tasks are below threshold:

> "Plan ready with blockers. Tasks <IDs> are below threshold (<%).
>
> **Business OS Integration (default-on):**
> - Card: `<Card-ID>`
> - Planned stage doc created via API: `plan`
> - Card updated with Plan-Link via API
> - Lane remains `Fact-finding` until blockers are resolved
>
> Auto-continuing to `/build-feature` for eligible tasks. Recommend `/re-plan` for blocked tasks after initial build."

When Card-ID is present but auto-continue is blocked:

> "Plan ready but cannot auto-continue. <reason>.
>
> **Business OS Integration (default-on):**
> - Card: `<Card-ID>`
> - Planned stage doc created via API: `plan`
> - Card updated with Plan-Link via API
> - Lane remains `Fact-finding` until gating conditions are met
>
> Recommend `/re-plan` for blocked tasks."

### Backward Compatibility

- Plans with `Business-OS-Integration: off` skip card/stage-doc/lane writes.
- Existing plans without the field default to `on`.
