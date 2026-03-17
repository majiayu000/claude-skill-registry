---
name: re-plan
description: Resolve low-confidence tasks in an existing plan. Investigate, remove uncertainty, make decisions with evidence, and update the plan doc so that remaining work can proceed safely.
---

# Re-Plan

Resolve low-confidence tasks in an existing plan. Investigate, remove uncertainty, make decisions with evidence, and update the plan doc so that remaining work can proceed safely.

## Confidence Policy

- **Confidence ≥90 is a motivation, not a quota.** Increasing confidence should come from reducing uncertainty (evidence, tests, spikes), not from deleting planned work.
- If work is valuable but not yet high-confidence, preserve it as **deferred/Phase 3** and add **"What would make this ≥90%"** notes.

## Scientific Confidence Protocol (Mandatory)

Treat re-planning as hypothesis testing, not narrative scoring.

### Core rule

**Confidence may only increase when uncertainty is reduced by evidence.**

If uncertainty remains, do one of:
- keep confidence where it is (or lower it), or
- add explicit precursor work (INVESTIGATE/SPIKE) and make downstream tasks depend on it.

### Evidence ladder (use to justify confidence changes)

| Evidence class | Typical source | Allowed confidence uplift |
|----------------|----------------|---------------------------|
| **E0: Assumption** | Opinion, intuition, "seems easy" | **0%** |
| **E1: Static code/doc audit** | `rg`, file reads, call-site mapping, official doc lookups | **small uplift only** (typically +0 to +5) |
| **E2: Executable verification** | existing tests run, script outputs, runtime probes, **scout probe tests** | **moderate uplift** (typically +5 to +15) |
| **E3: Precursor spike/prototype result** | dedicated spike task with measurable outcome | **major uplift** (typically +10 to +25) |

### Promotion gate (hard rule)

A task should not be promoted from **<80%** to **≥80%** unless at least one is true:
1. The blocking unknowns are closed with **E2+** evidence, or
2. A precursor task is inserted with explicit exit criteria, and downstream implementation remains below 80% until that precursor is completed.

### Fail-first promotion caps (business-artifact/mixed IMPLEMENT tasks)

For non-code deliverables, confidence cannot be promoted above thresholds without fail-first evidence:
- No Red evidence (falsification probe) → cap at 79%
- Red complete but no Green pass evidence → cap at 84%
- Green complete but no Refactor evidence → cap at 89%

### Precursor task pattern

When evidence is insufficient to promote a task above 80%, **create formal precursor tasks in the plan** — not inline notes.

**Precursor tasks are first-class plan tasks.** They get their own TASK-ID, full confidence assessment, acceptance criteria, and validation contract (TC for code/mixed; VC for business-artifact/mixed when applicable), and appear in the task summary table. The blocked downstream task explicitly `Depends on` the precursor TASK-ID.

**Why formal tasks, not notes:** Inline "precursor evidence needed" notes hide real work behind a single confidence number. A task at 70% with "needs spike" looks like one task — but it's actually two: the spike and the implementation. Making precursors formal tasks means:
- The dependency chain is visible and sequenceable
- Precursor tasks get their own confidence assessment (they may themselves be blocked)
- `/build-feature` can build the precursor independently
- `/sequence-plan` correctly orders the full chain
- Progress tracking reflects actual work remaining

**Precursor task requirements:**
- **Type:** `INVESTIGATE` (research/decision) or `SPIKE` (code prototype with measurable outcome)
- **Purpose:** resolve exactly one uncertainty class (Implementation/Approach/Impact)
- **Outputs:** concrete artifact (`decision memo`, `call-site map`, `test/probe output`, `prototype result`)
- **Exit criteria:** binary pass/fail statement tied to evidence
- **Confidence:** assessed using the same min-of-dimensions rule as any other task
- **Dependency:** the blocked downstream task `Depends on` this precursor's TASK-ID
- **Validation contract:** SPIKE tasks that produce code require TC contracts; business-artifact/mixed precursor tasks require VC contracts plus fail-first evidence when they are IMPLEMENT-like. INVESTIGATE tasks that produce only a decision memo do not.

**Recursive decomposition:** If a precursor task is itself below 80% confidence, it may need its own precursors. Work backwards from the blocked task until every task in the chain is ≥80%. This may produce a chain of 2-3 tasks — that's fine. The alternative (one task with hidden precursors) masks the true confidence.

**Example chain:**
```
TASK-54 (INVESTIGATE, 85%): Decision memo — Firebase custom claims vs PIN token
  ↓ unblocks
TASK-55 (SPIKE, 82%): Prototype Firebase Auth init + custom claims flow
  ↓ unblocks
TASK-51 (IMPLEMENT, 74% → conditional 82%): Staff auth replacement
  (confidence promotable to 82% only after TASK-54 + TASK-55 complete)
```

**Conditional confidence:** When a blocked task's confidence depends on precursor completion, record it as:
> **Confidence:** 74% (→ 82% conditional on TASK-54, TASK-55)

This makes the confidence chain transparent. The task stays at 74% until precursors are done.

## TDD / Fail-First Compliance Requirement

**Every IMPLEMENT task must have an enumerated validation contract before it can be marked Ready.**

- Code/mixed tasks require a `Test contract` with `TC-XX` cases.
- Business-artifact/mixed tasks require a `Validation contract` with `VC-XX` checks plus fail-first execution evidence (Red, Green, Refactor).

A task without required validation cases for its track (TC-XX or VC-XX) cannot proceed to `/build-feature`, regardless of confidence score. Re-plan must add missing contracts and evidence.

**Code/mixed test contract format:**
```markdown
- **Test contract:**
  - **TC-01:** <scenario> → <expected outcome>
  - **TC-02:** <error case> → <expected outcome>
  - **TC-03:** <edge case> → <expected outcome>
  - **Test type:** <unit | integration | e2e | contract>
  - **Test location:** <path/to/test.ts (existing) or path/to/new-test.ts (new)>
  - **Run:** <command to execute>
```

**Business-artifact/mixed validation contract format:**
```markdown
- **Validation contract:**
  - **VC-01:** <quality/channel/compliance scenario> → <pass condition>
  - **VC-02:** <failure/constraint scenario> → <pass condition>
  - **VC-03:** <edge/handoff/measurement scenario> → <pass condition>
  - **Validation type:** <review checklist | approval gate | dry-run | rehearsal | contract>
  - **Validation location/evidence:** <artifact path or checklist path>
  - **Run/verify:** <procedure>
- **Execution plan (business-artifact/mixed):** Red → Green → Refactor
  - **Red evidence:** <expected failure/gap probe + observed result>
  - **Green evidence:** <minimum artifact/process that passes VC checks>
  - **Refactor evidence:** <quality/operability hardening + VC re-pass result>
```

**Minimum validation contract requirements:**
- At least one TC/VC per acceptance criterion
- Happy path covered (TC-01 or VC-01)
- At least one error/edge case for M/L effort tasks
- Validation type/location/run procedure specified
- For business-artifact/mixed tasks claiming >80%: Red, Green, and Refactor evidence must be recorded

## Operating Mode

**RE-PLANNING ONLY**

**Allowed:** read files, search repo, inspect tests, trace call sites/dependencies, review `docs/plans/`, review targeted git history, consult external official docs if needed.

**Not allowed:** code changes, refactors, commits except plan/notes updates, applying migrations, destructive commands.

## Inputs

- An existing plan doc: `docs/plans/<feature-slug>-plan.md`
- The task IDs to re-plan (explicit from user or inferred from below-threshold tasks)
- Optional: fact-find brief `docs/plans/<feature-slug>-fact-find.md`

**If the plan doc does not exist:**
- **With fact-find:** Offer to create initial plan from fact-find, then proceed with re-planning
- **Without fact-find:** Stop and instruct: "No plan exists. Run `/plan-feature` to create initial plan first."

**If the plan doc is stale/out-of-sync:**
- Create a minimal recovery plan if salvageable (preserve task IDs, update with current reality)
- Otherwise, recommend `/plan-feature` for clean rebuild

## Outputs

- Update the existing plan doc in-place: `docs/plans/<feature-slug>-plan.md`
- Optional (only if the investigation is extensive): add a short supporting note: `docs/plans/<feature-slug>-replan-notes.md`
- No code changes. No commits except doc updates.

## When to Use

Run `/re-plan` when any of the following occurs:

- A plan task has overall confidence <80% (or is explicitly flagged as blocked).
- **A task is missing a required validation contract (TC-XX or VC-XX) — cannot proceed to build without it.**
- During implementation, confidence drops due to unexpected complexity or new evidence.
- A fact-check or repo audit finds factual inaccuracies in the plan that materially affect confidence.
- New information invalidates assumptions, dependencies, or approach decisions.
- Build was stopped due to uncertainty and needs a structured reset.
- `/build-feature` rejected a task due to missing validation contract/evidence.
- **A CHECKPOINT task was reached during `/build-feature`** — triggers a mid-build reassessment of all remaining tasks using evidence from completed work.

**Note:** `/re-plan` is not for generating a plan from scratch; that is `/plan-feature`. `/re-plan` operates on a specific plan and task IDs.

### Checkpoint-Triggered Re-Assessment

When `/re-plan` is invoked at a CHECKPOINT during `/build-feature`, it operates in **mid-build reassessment mode**:

1. **Gather implementation evidence:** Read the completed tasks' build completion notes, commits, and confidence reassessments. This is E2/E3 evidence (executable verification from real implementation).

2. **Validate horizon assumptions:** Each CHECKPOINT lists "Horizon assumptions to validate." Check each one against the evidence from completed tasks:
   - **Confirmed:** The assumption held — downstream tasks can retain or increase confidence.
   - **Partially confirmed:** Some aspects held, others were more complex than expected — downstream tasks need revision.
   - **Disproved:** The assumption was wrong — downstream tasks that depend on it need major revision or abandonment.

3. **Scout ahead for remaining tasks:** Before reassessing confidence, proactively validate assumptions that remaining tasks depend on:

   **Code/mixed scouts:**
   - **Doc lookups:** Verify any library/API/framework capabilities the remaining tasks assume — check against the exact versions in use.
   - **Probe tests:** Write small throwaway tests that exercise critical assumptions (e.g., "can Prisma do nested creates with this schema?", "does this API accept this payload shape?"). These are E2 evidence.
   - **Contract checks:** Run `tsc` or schema validation against type/contract assumptions that downstream tasks depend on.
   - **Integration boundary tests:** Run existing tests that cross boundaries the remaining tasks will depend on.

   **Business-artifact/mixed scouts:**
   - **Hypothesis freshness:** Check whether key hypotheses from the fact-find's Hypothesis & Validation Landscape still hold (supplier quotes, pricing, channel costs, regulatory rules, competitive positioning). Flag any >14 days old with time-sensitive dependencies.
   - **Signal updates:** Check whether new evidence has appeared since planning (completed demand tests, conversion data, competitor launches) that changes existing signal coverage.
   - **Channel/approval drift:** Verify platform policies, approval paths, and compliance constraints haven't changed.

   Scout results directly feed the reassessment — a failed scout disproves an assumption before you build on it.

4. **Reassess remaining tasks:** For each task after the CHECKPOINT:
   - Re-evaluate confidence using evidence from completed work AND scout results (not just static analysis)
   - Split tasks that are now understood to be larger than planned
   - Remove or defer tasks that are no longer viable
   - Add new tasks discovered during implementation or scouting

5. **Apply the standard re-plan workflow** (steps 1–7) to the remaining tasks, with the key difference that completed tasks and scout results provide E2/E3 evidence that was unavailable during initial planning.

6. **After re-plan completes:** `/build-feature` will check the results and either continue building or stop if remaining tasks dropped below threshold.

## Workflow

### 1) Select tasks and establish the re-plan scope

Identify the target tasks:
- Prefer explicit task IDs provided by the user.
- Otherwise, scan the plan and select any tasks with overall confidence <80% **and** any tasks that depend on them.
- **Also select any IMPLEMENT tasks missing required validation contracts (TC-XX/VC-XX)** — these cannot proceed to build regardless of confidence.

For each target task, record:
- current confidence (overall + per dimension)
- current acceptance criteria
- dependencies (TASK-IDs)
- affected files/modules
- **validation contract status:** code/mixed TC complete|incomplete|missing OR business-artifact/mixed VC complete|incomplete|missing
- **fail-first evidence status (business-artifact/mixed):** complete | incomplete | missing

### 2) Diagnose the confidence gap by dimension

For each low-confidence task, identify which dimension(s) caused the min-score:

| Weak Dimension | Typical Symptoms | Primary Work to Do |
|----------------|------------------|-------------------|
| **Implementation (<80%)** | unclear API, unknown how to integrate, no precedent | find analogous code; inspect interfaces; confirm library/framework behavior |
| **Approach (<80%)** | multiple viable designs; unclear long-term fit | enumerate options; evaluate tradeoffs; align to repo conventions; decide |
| **Impact (<80%)** | uncertain blast radius; hidden consumers; migration risk | trace call sites; map contracts; identify side effects; check tests and boundaries |

Record the diagnosis per task explicitly in the plan update.

### 2b) Define falsifiable checks (before scoring)

For each target task, define:
- **Uncertainty statement:** what is unknown right now?
- **Falsifiable check:** what observation would prove/disprove the current approach?
- **Evidence target class:** E1, E2, or E3 (from the evidence ladder)

If you cannot define a falsifiable check, confidence must not increase.

### 3) Perform targeted investigation (evidence-driven)

#### A) Close Implementation gaps

**Minimum actions (code/mixed):**
- Locate at least one analogous pattern in the repo.
- Identify the exact integration seam (function/class/module boundaries).
- Confirm required types/contracts and where they are validated.
- Identify the correct test layer(s) that can prove correctness.
- Run at least one executable check where possible (existing targeted test, probe, or script) for high-impact claims.

**Minimum actions (business-artifact/mixed):**
- Verify the fact-find's Hypothesis & Validation Landscape is still current (key hypotheses, existing signal coverage, falsifiability assessment).
- Confirm channel constraints and format requirements haven't changed since planning.
- Verify the approval path still works (reviewer available, process unchanged).
- Check whether existing signal coverage has improved or decayed since fact-find (new data available? prior signals stale?).

**Evidence to capture:**
- file paths (and key symbol names) for code/mixed
- pattern references ("this matches pattern used in X")
- relevant tests and how they assert behavior
- for business-artifact/mixed: hypothesis validity status, channel constraint confirmations, signal freshness assessment

#### B) Close Approach gaps

**Minimum actions (code/mixed):**
- List at least two viable approaches (A/B).
- Evaluate each for:
  - consistency with existing architecture and conventions
  - coupling and maintainability
  - migration/rollout complexity
  - operational risk and observability

**Minimum actions (business-artifact/mixed):**
- List at least two viable approaches (A/B).
- Evaluate each for:
  - channel fit for the target audience
  - test design quality — are VCs isolated and diagnostic per the Business VC Quality Checklist?
  - measurement feasibility — can the pass/fail signal actually be observed?
  - cost and time to run the validation (falsification cost from hypothesis landscape)

**Both tracks:**
- Decide on a chosen approach based on evidence.
- If the decision is genuinely a product preference, escalate to the user with a precise choice and recommendation.
- If no approach can be selected confidently, create a precursor INVESTIGATE/SPIKE task instead of forcing a score increase.

**Deliverable:**
- A short "Decision" paragraph added to the plan (and a Decision Log entry).

#### C) Close Impact gaps

**Minimum actions (code/mixed):**
- Map upstream and downstream dependencies:
  - what this change depends on
  - who/what consumes it
- Identify integration boundaries:
  - package boundaries, service boundaries, API/event contracts
- Inventory existing tests that cover impacted paths, plus gaps.
- **Check for extinct tests:** Tests that assert obsolete behavior give false confidence. Flag any tests that:
  - Test removed/renamed APIs or contracts
  - Assert behavior that no longer exists
  - Were not updated when functional code last changed
- Identify rollout/rollback requirements:
  - feature flags, backward compatibility, migration sequencing
- Add quantitative blast-radius notes where possible (number of files, call-sites, tests likely affected).

**Minimum actions (business-artifact/mixed):**
- Check whether market, competitive, or regulatory landscape has shifted since planning.
- Verify supplier quotes, pricing assumptions, or availability timelines are still valid.
- Confirm audience/channel assumptions haven't drifted (ad costs, platform policy changes, audience behaviour shifts).
- Check whether any hypothesis from the fact-find's Hypothesis & Validation Landscape has been confirmed or invalidated by events since planning.
- Identify rollback/pivot requirements: what happens if the VC fails after execution (sunk cost, reversibility).

**Evidence to capture:**
- callers / references (file paths) for code/mixed
- contracts (types/schemas/endpoints)
- tests and commands
- extinct tests flagged for update during build
- for business-artifact/mixed: hypothesis validity status, market/regulatory change notes, updated signal coverage assessment

### 3b) Complete validation contracts for tasks missing them

For each IMPLEMENT task missing required validation contract elements:

**Step 1: Review acceptance criteria**
- Each acceptance criterion must map to at least one validation case
- Identify gaps: criteria without corresponding TC/VC cases

**Step 2: Enumerate validation cases by track**
- **Code/mixed:** TC-01 happy path; TC-02+ error/edge/boundary cases
- **Business-artifact/mixed:** VC-01 happy path; VC-02+ failure/constraint/edge/handoff checks
- For M/L effort tasks: at least 3 validation cases required
- For S effort tasks: at least 1 validation case required (may be more based on complexity)

**Step 3: Specify validation metadata**
- **Code/mixed:** test type, test location, run command
- **Business-artifact/mixed:** validation type, evidence location, run/verify procedure

**Step 4: Add track-specific contract to the task**
Code/mixed format:
```markdown
- **Test contract:**
  - **TC-01:** <scenario> → <expected outcome>
  - **TC-02:** <error case> → <expected outcome>
  - **Acceptance coverage:** TC-01 covers criteria 1,2; TC-02 covers criteria 3
  - **Test type:** <unit | integration | e2e>
  - **Test location:** `path/to/test.ts`
  - **Run:** `pnpm test --testPathPattern=<pattern>`
```

Business-artifact/mixed format:
```markdown
- **Validation contract:**
  - **VC-01:** <scenario> → <pass condition>
  - **VC-02:** <failure case> → <pass condition>
  - **Acceptance coverage:** VC-01 covers criteria 1,2; VC-02 covers criteria 3
  - **Validation type:** <review checklist | approval gate | dry-run | rehearsal | contract>
  - **Validation location/evidence:** `path/to/review-checklist.md`
  - **Run/verify:** <exact review/rehearsal procedure>
- **Execution plan (business-artifact/mixed):** Red → Green → Refactor
  - **Red evidence:** <falsification probe + observed failure/gap>
  - **Green evidence:** <minimum artifact/process + VC pass result>
  - **Refactor evidence:** <improvement + VC regression check result>
```

**Deriving validation cases from acceptance criteria:**

| Acceptance Criterion Type | Code/mixed (TC) Pattern | Business-artifact/mixed (VC) Pattern |
|---------------------------|-------------------------|--------------------------------------|
| "X returns Y" | TC: Call X → assert Y | VC: produce X artifact/process → verify Y pass condition |
| "X validates Y" | TC-a: Valid input → success; TC-b: Invalid input → error | VC-a: compliant input/source → pass; VC-b: non-compliant input/source → fail/reject |
| "X handles error Z" | TC: Trigger Z → assert error handling | VC: trigger Z in rehearsal/dry-run → verify fallback/handoff response |
| "X is visible in Y" | TC: Create X → query Y → assert presence | VC: produce/publish X → verify it appears correctly in channel Y |
| "X with approval/auth" | TC-a: With auth → success; TC-b: Without auth → 401 | VC-a: with approval path → pass; VC-b: missing approval → blocked |

### 4) Resolve open questions (self-serve first; escalate last)

**Rules:**
- Investigate the repo and official docs first.
- Only ask the user when:
  - business rules/UX intent cannot be inferred,
  - two approaches are truly equivalent and require preference,
  - or you have exhausted evidence sources and the uncertainty remains.

**If user input is needed:**
- Ask only the minimum set of questions required to proceed.
- Each question must include:
  - why it matters
  - what decision it affects
  - a recommended default with risk (if appropriate)

### 5) Update the plan doc with deltas (mandatory structure)

Update `docs/plans/<feature-slug>-plan.md` as follows:

**Plan frontmatter:**
- Set `Status: Active` after re-plan updates unless the user explicitly wants it to remain Draft.

**For each re-planned task:**
- Preserve the same TASK-ID (do not renumber).
- Add a **Re-plan Update** block containing:
  - Previous confidence → new confidence
  - Evidence class used for uplift (E1/E2/E3)
  - What was investigated (repo areas, tests, docs)
  - Decisions made (and why)
  - Updated dependencies/order (if changed)
  - Updated acceptance criteria/validation plan/rollout notes as needed

**If confidence remains <80% after investigation — create formal precursor tasks:**

Do NOT add inline "Precursor evidence needed" notes. Instead:

1. **Create a new task section** in the plan with the next available TASK-ID
2. **Full task definition** — same structure as any IMPLEMENT task:
   - Type (INVESTIGATE or SPIKE)
   - Effort (S/M/L)
   - Confidence (min-of-dimensions, assessed normally)
   - Acceptance criteria (what artifact is produced, what question is answered)
   - Validation contract (TC/VC based on execution track; required for SPIKE/IMPLEMENT-like precursors)
   - Exit criteria (binary pass/fail)
   - Affects (files to read/modify)
3. **Add to task summary table** with confidence, effort, and dependencies
4. **Update the blocked task's `Depends on`** to include the new precursor TASK-ID
5. **Record conditional confidence** on the blocked task:
   > **Confidence:** 70% (→ 84% conditional on TASK-XX, TASK-YY)
6. **Recursively assess** — if the precursor itself is <80%, it needs its own precursors

**The blocked task's confidence stays at its current value** until precursors are completed and provide E2/E3 evidence. Do not speculatively raise it.

**After creating precursor tasks, re-assess the full dependency graph** — new tasks may unblock or reorder existing work.

**Decomposition closure rule:** after all confidence/dependency/content edits are complete, run `/sequence-plan` as the final structural step before deciding readiness or handing off to `/build-feature`.

**Also update:**
- `Last-updated` in frontmatter
- `Overall-confidence` (effort-weighted as defined in `/plan-feature`)
- Task Summary table (confidence, effort, dependencies)

### 5a) Confidence Score Validation Checklist (Mandatory Before Finalizing)

Before marking any task as Ready or finalizing confidence scores, verify:

- [ ] **Evidence citation:** Every non-trivial claim includes file path + line number
  - Example: "Bug location: `metadata.ts:56-60`" not "metadata.ts has a bug"
- [ ] **Code verification:** If claiming something exists/doesn't exist, you've read the file
  - Example: "No tests exist: `rg generateMetadata apps/brikette/src/test` → zero hits"
- [ ] **Min-of-dimensions:** Overall confidence = min(Implementation, Approach, Impact), not weighted average
- [ ] **Internal consistency:** Confidence in task body matches confidence in summary table
- [ ] **No assumptions:** If you haven't verified in code, it's an "Unknown" not a confident claim
- [ ] **Test impact quantified:** If tests will break, list how many and which files
- [ ] **Evidence class stated:** Any confidence uplift cites E1/E2/E3 and corresponding artifact(s)
- [ ] **No narrative promotion:** Task is not promoted to ≥80 solely from E1 static audit when key unknowns remain
- [ ] **Precursor enforcement:** Remaining unknowns are converted into explicit precursor tasks with dependencies

**If any checklist item fails, do NOT finalize the confidence score. Investigate or mark as Unknown.**

### 5b) Validation Contract Checklist (Mandatory for all IMPLEMENT tasks)

Before marking any IMPLEMENT task as Ready, verify:

- [ ] **Track-appropriate enumeration exists:**
  - Code/mixed: task has at least one `TC-XX:` line
  - Business-artifact/mixed: task has at least one `VC-XX:` line
- [ ] **Acceptance coverage:** Every acceptance criterion maps to at least one TC/VC
- [ ] **Scenario + outcome:** Each case has format `<scenario> → <expected outcome/pass condition>`
- [ ] **Validation metadata specified:**
  - Code/mixed: test type + test location + run command
  - Business-artifact/mixed: validation type + evidence location + run/verify procedure
- [ ] **Minimum case count met (TC or VC):**
  - S-effort: ≥1
  - M-effort: ≥3 (including at least one error/edge case)
  - L-effort: ≥5 (including failure/edge/integration or handoff scenarios)
- [ ] **Fail-first evidence (business-artifact/mixed):**
  - Red evidence present
  - Green evidence present
  - Refactor evidence present
- [ ] **Fail-first confidence caps respected (business-artifact/mixed):**
  - >79% only with Red evidence
  - >84% only with Green evidence
  - >89% only with Refactor evidence

**If any checklist item fails, the task is NOT ready for build. Add the missing validation contract/evidence elements.**

### 6) Re-assess knock-on effects

After resolving the target tasks:

Identify any tasks whose confidence should change due to:
- new constraints
- new dependencies
- revised approach
- newly discovered blast radius
- factual corrections from fact-checks or audits

Update those tasks' confidence (and notes) if materially affected.

### 6a) Sequence the plan (mandatory after decomposition/topology changes)

After updating tasks and re-assessing knock-on effects, run `/sequence-plan` on the plan. This:

- Re-sorts tasks into correct implementation order (accounting for new/changed dependencies)
- Renumbers tasks sequentially (preserving domain prefix)
- Updates all `Depends on` and `Blocks` fields with new IDs
- Regenerates the **Parallelism Guide** to reflect the current dependency graph

**Mandatory when:** tasks were decomposed (split), added, removed, or dependencies changed. New tasks must appear in correct execution order — precursors before the tasks they unblock.

**Execution order rule:** complete all substantive re-plan edits first (confidence updates, acceptance changes, dependency rewrites), then run `/sequence-plan`, then move to step 7 handoff.

**Skip conditions:** Only skip if re-plan touched a single task with no dependency changes and no tasks were created/split/removed.

**Note:** `/sequence-plan` does not change task scope, confidence, or acceptance — it only reorders, renumbers, and maps dependencies. All substantive changes were made in steps 1–6.

### 7) Decision point and handoff

End by classifying the plan state:

- **Ready to build:** all IMPLEMENT tasks are ≥80% confidence **AND** have complete validation contracts (TC/VC) with required fail-first evidence
- **Validation incomplete:** confidence ≥80% but some tasks are missing validation contracts/evidence — add them before proceeding
- **Partially ready:** some tasks are 60–79% with explicit precursor tasks/verification steps; none below 60%
- **Blocked:** any IMPLEMENT task is <60% or requires user input to proceed safely

**Validation gate is mandatory.** A task with 90% confidence but missing required TC/VC or fail-first evidence is NOT ready for build.

Provide the recommended next action:
- `/build-feature` if ready (confidence ≥80% AND validation contracts complete) — and sequencing is up-to-date after any decomposition
- `/re-plan` again if remaining blocked tasks exist or validation contracts/evidence are missing
- Ask user questions if genuinely required

## Plan Update Snippet (insert into each affected task)

Add this block inside the task section:

```markdown
#### Re-plan Update (YYYY-MM-DD)
- **Previous confidence:** 55%
- **Updated confidence:** 84%
  - **Evidence class:** E2 (executable verification)
  - Implementation: 84% — <why + evidence>
  - Approach: 88% — <why + evidence>
  - Impact: 84% — <why + evidence>
- **Investigation performed:**
  - Repo: `path/to/file.ts`, `path/to/other.ts`
  - Tests: `path/to/test.spec.ts` (notes)
  - Docs: <internal/external reference>
- **Decision / resolution:**
  - <what was decided and why>
- **Changes to task:**
  - Dependencies: <updated TASK-IDs (including new precursor tasks)>
  - Acceptance: <updated bullets if changed>
  - Validation plan: <updated bullets if changed>
  - Rollout/rollback: <updated notes if changed>
```

**When confidence remains <80%, use the conditional confidence pattern instead of inline precursor notes:**

```markdown
#### Re-plan Update (YYYY-MM-DD)
- **Previous confidence:** 70%
- **Updated confidence:** 70% (→ 84% conditional on TASK-54, TASK-55)
  - Confidence cannot be promoted until precursor tasks complete and provide E2/E3 evidence
- **Investigation performed:**
  - <what was investigated>
- **Precursor tasks created:**
  - TASK-54 (INVESTIGATE): <description> — resolves <uncertainty>
  - TASK-55 (SPIKE): <description> — resolves <uncertainty>
- **Dependencies updated:** Now depends on TASK-54, TASK-55
```

Also add a short entry to the plan's **Decision Log** whenever an approach decision is made or reversed.

## Quality Checks (must pass)

- [ ] Each low-confidence task has the weak dimension(s) explicitly diagnosed.
- [ ] Investigation is targeted and evidenced (file paths/tests/docs).
- [ ] Any approach decision includes alternatives, tradeoffs, and rationale.
- [ ] Impact is mapped (upstream/downstream) with explicit blast radius notes.
- [ ] Plan doc updated: task confidence deltas, dependencies, acceptance criteria, validation contract, rollout/rollback.
- [ ] Related tasks re-assessed and updated where necessary.
- [ ] User questions are only asked when genuinely unavoidable and are decision-framed.
- [ ] **TDD/fail-first compliance:** Every IMPLEMENT task has complete track-appropriate validation contracts (TC for code/mixed; VC + Red/Green/Refactor evidence for business-artifact/mixed).
- [ ] **Validation contract checks:** All items in 5b) checklist pass for every IMPLEMENT task.
- [ ] **Scientific uplift compliance:** each confidence increase is tied to E1/E2/E3 evidence and uncertainty reduction.
- [ ] **Precursor compliance:** unresolved unknowns are represented as formal precursor tasks (with TASK-ID, confidence, acceptance) — not inline notes or "precursor evidence needed" bullets.
- [ ] **Precursor confidence:** each precursor task has its own min-of-dimensions confidence assessment. If a precursor is <80%, it has its own precursors (recursive decomposition).
- [ ] **Dependency chain:** blocked tasks have explicit `Depends on` referencing precursor TASK-IDs. Conditional confidence recorded on the blocked task.
- [ ] **Sequencing applied:** `/sequence-plan` has been run — tasks reordered, renumbered, `Blocks` fields updated, Parallelism Guide regenerated.
- [ ] **Decomposition closure:** when tasks were split/added/removed, sequencing was run after final structural edits and before handoff.

## Completion Messages

**All ≥80% with complete validation contracts:**
> "Re-plan complete. Updated `docs/plans/<feature-slug>-plan.md`. All implementation tasks are ≥80% confidence with complete validation contracts (TC/VC + required fail-first evidence). Tasks re-sequenced into N execution waves (max parallelism: P). Proceed to `/build-feature`."

**Confidence ≥80% but missing validation contracts/evidence:**
> "Re-plan complete. Updated plan. Tasks <IDs> are ≥80% confidence but missing required validation contracts/evidence (TC/VC or Red/Green/Refactor). Tasks re-sequenced. Run `/re-plan` again to add missing validation elements before proceeding to build."

**Some tasks <80% with precursor chain created:**
> "Re-plan complete. Updated plan. Tasks <IDs> remain <80% with conditional confidence pending precursor completion. Created N new precursor tasks (TASK-XX, TASK-YY) — all ≥80% and ready for `/build-feature`. Tasks re-sequenced into N execution waves. Build precursor tasks first, then `/re-plan` to promote blocked tasks."

**Blocked / needs user input:**
> "Re-plan complete but still blocked on <IDs> (<%>) due to <dimension>. Tasks re-sequenced where possible. I need the following decisions from you: <questions>."

**Checkpoint-triggered — remaining tasks confirmed:**
> "Checkpoint re-assessment complete. Horizon assumptions validated against completed work. N remaining tasks reassessed — all ≥80% with complete validation contracts/evidence. Tasks re-sequenced. Resuming `/build-feature`."

**Checkpoint-triggered — remaining tasks revised:**
> "Checkpoint re-assessment complete. Found: <findings from completed work>. Revised N tasks, added M new tasks, deferred/removed K tasks. Updated plan re-sequenced into N execution waves. Resuming `/build-feature` for eligible tasks."

**Checkpoint-triggered — approach invalidated:**
> "Checkpoint re-assessment complete. Completed work revealed: <evidence>. Remaining approach is no longer viable because: <reason>. Recommend: <alternative approach or scope reduction>. Build paused pending direction."
