---
name: build-feature
description: Execute tasks from an approved plan, one task at a time, with strict confidence gating and mandatory validation for code and business-artifact deliverables.
---

# Build Feature

Execute tasks from an approved plan, one task at a time, with strict confidence gating and mandatory validation. Update the plan as execution proceeds.

**Confidence note:** Confidence ≥90% is a motivation/diagnostic, not a requirement. The implementation gate is still **≥80%** confidence for IMPLEMENT tasks.

## Operating Mode

**BUILDING ONLY**

**Allowed:** modify code, add/update tests, produce non-code artifacts, run validations, commit changes, update the plan doc.

**Not allowed:** implement tasks below threshold, do work not in the plan, skip validation, commit failing outputs, silently change scope.

## Prerequisites

- **Plan exists:** `docs/plans/<feature-slug>-plan.md`
- **Task(s) to build are:**
  - Type: `IMPLEMENT`
  - Confidence ≥80% (overall and all implied dimension minimums via the plan rubric)
  - All dependencies completed
  - No blockers noted in the task

**If any selected IMPLEMENT task is <80% → STOP and run `/re-plan` for that task.**

**If a selected task is 80–89%:** it is eligible to build, but treat the “unknowns” as real—ensure the task has explicit risks/verification steps (or update the plan before proceeding).

## Fast Path (with argument)

**If user provides a slug or card ID** (e.g., `/build-feature commerce-core` or `/build-feature BRIK-ENG-0020`):
- Skip discovery entirely
- If slug: read `docs/plans/<slug>-plan.md` directly
- If card ID: look up plan link from card file
- **Target: <2 seconds to start building**

## Discovery Path (no argument)

**If user provides no argument**, read the pre-computed index (single file):

```
docs/business-os/_meta/discovery-index.json
```

Present the `readyForBuild` array (filtered to those with pending tasks) as a table:

```markdown
## Ready for Build

| Slug | Title | Pending Tasks | Business |
|------|-------|---------------|----------|
| xa-client-readiness | XA Client Readiness | 15 | PIPE |

Enter a slug to start building, or a specific TASK-ID.
```

Also check the `planned` array for cards with plan links.

## Inputs

- The plan doc: `docs/plans/<feature-slug>-plan.md`
- Optional: fact-find brief: `docs/plans/<feature-slug>-fact-find.md`
- Optional: user-specified task IDs to build first

If the user does not specify tasks, build in ascending TASK order among eligible IMPLEMENT tasks.

## Execution Skill Dispatch (Progressive Disclosure)

For each task, read `Deliverable` and `Execution-Skill` from the plan and route accordingly:

| Deliverable Type | Primary Execution Skill | Notes |
|---|---|---|
| `code-change` | `/build-feature` | Native TDD path in this skill |
| `email-message` | `/draft-email-message` | Use `/process-emails` when tied to inbox triage |
| `product-brief` | `/write-product-brief` | Decision-quality brief artifact |
| `marketing-asset` | `/draft-marketing-asset` | Campaign/channel asset package |
| `spreadsheet` | `/create-ops-spreadsheet` | Spreadsheet spec + starter CSV |
| `whatsapp-message` | `/draft-whatsapp-message` | Channel-safe copy with compliance checks |
| `multi-deliverable` | `/build-feature` orchestrates per-task dispatch | One task per cycle still applies |

Startup aliases (from plan field `Startup-Deliverable-Alias`) are clarity labels, not replacement deliverable types:

| Startup-Deliverable-Alias | Canonical Deliverable Type | Dispatch Skill |
|---|---|---|
| `startup-budget-envelope` | `spreadsheet` | `/create-ops-spreadsheet` |
| `startup-channel-plan` | `product-brief` | `/write-product-brief` |
| `startup-demand-test-protocol` | `product-brief` | `/write-product-brief` |
| `startup-supply-timeline` | `spreadsheet` | `/create-ops-spreadsheet` |
| `startup-weekly-kpcs-memo` | `product-brief` | `/write-product-brief` |

If a referenced execution skill is missing, stop and run `/re-plan` to either:
- add the missing skill as a prerequisite task, or
- re-scope the task to an available execution path.

## Pre-Build Check (Required)

Before executing any task work, verify all of the following:

### A) Plan integrity

- The plan file exists and is the active source of truth.
- The target task exists and includes:
  - Type, Deliverable, Execution-Skill, Affects (file paths), Depends on, Confidence breakdown, Acceptance, Validation contract, Planning validation (for M/L effort), Rollout/rollback notes, Documentation impact.
  - For `business-artifact`/`mixed` tasks: Artifact-Destination, Reviewer, Approval-Evidence, Measurement-Readiness.
- The task is not marked `Superseded`/`Blocked`/`Needs-input`.

**If any required task fields are missing → treat as a confidence drop → STOP → `/re-plan`.**

### B) Eligibility gate

Confirm:
- Task Type = `IMPLEMENT`, `SPIKE`, or `INVESTIGATE`
- Overall confidence ≥80%
- All dependency tasks are complete (per plan status)
- No open DECISION tasks gate this work

**Task type differences:**
- **IMPLEMENT:** Standard execution work. Use TDD for code/mixed tasks, artifact cycle for business-artifact tasks.
- **SPIKE:** Produces a prototype or executable proof. Must have explicit validation criteria. On completion, its output (evidence) may be used by `/re-plan` to promote downstream tasks.
- **INVESTIGATE:** Produces a decision memo or analysis artifact — not implementation delivery. Validation is: the decision memo exists and answers the question. Commit the memo/notes, then mark complete. Skip step 3 execution cycles and instead: perform investigation, produce artifact, verify exit criteria, commit artifact, update plan.
- **CHECKPOINT:** Horizon re-assessment gate — not code. See "CHECKPOINT Handling" below.

**Execution-track differences (for IMPLEMENT tasks):**
- **`code` or `mixed`:** Use the TDD cycle (tests first, fail, implement, pass).
- **`business-artifact`:** Use the artifact cycle (draft, review against validation contract, finalize, evidence capture).

**If not eligible → STOP → `/re-plan`.**

### C) Local readiness gate

- Working tree is clean (or you explicitly understand any local diffs and they are unrelated and will not be mixed).
- Baseline is sane:
  - For code/mixed tasks: if the repo has a standard "quick check" (typecheck/lint/unit), run it before starting.
  - For business-artifact tasks: verify required source docs/data and channel constraints are available before drafting.
  - If baseline is failing for unrelated reasons, do not proceed without documenting it in the plan and/or resolving via a separate, explicitly planned task.

### D) File-reading gate

Before changing anything:
- Read **all** files listed in "Affects" (both primary and `[readonly]`)
- Read any immediately adjacent files needed to understand invariants (callers, types, schemas, tests)
- For code/mixed tasks, check for test stubs from planning (L-effort tasks should have them; use as starting point for TDD)

**Scope boundaries:**
- **Primary files** (no prefix): may be modified as part of this task
- **`[readonly]` files**: must NOT be modified — these are dependencies for understanding only

**If you need to modify:**
- A file not in "Affects" → STOP → `/re-plan` (new scope)
- A `[readonly]` file → STOP → `/re-plan` (scope was wrong, dependency is actually a modification target)

### E) Validation Contract Gate

Before implementing, verify the task has a complete validation contract:
- For code/mixed tasks:
  - [ ] Enumerated test cases (TC-XX) covering all acceptance criteria
  - [ ] Expected outcomes specified for each TC
  - [ ] Test type and location identified
  - [ ] For M/L tasks: test case specs are detailed enough to write tests
- For business-artifact tasks:
  - [ ] Enumerated validation checks (VC-XX) covering all acceptance criteria
  - [ ] Pass conditions specified for each VC
  - [ ] Artifact-Destination is explicit and actionable
  - [ ] Reviewer is named
  - [ ] Approval-Evidence capture path/method is defined
  - [ ] Measurement-Readiness is explicit (owner + cadence + tracking location)

**If validation contract is incomplete → treat as confidence drop → STOP → `/re-plan`.**

A task without enumerated validation cases cannot be built, regardless of its stated confidence.

### F) Scout verification gate (when Scouts field is present)

If the task has a `Scouts` field, verify each scouted assumption still holds before building:

- **Re-run any probe tests** from planning — if they now fail, the assumption has changed. STOP → `/re-plan`.
- **Re-check doc lookups** if a dependency version has changed since planning.
- **Verify type-level scouts** by running `tsc` on any type assertions from planning.

If scouts were marked "inconclusive" during planning, treat them as risks — proceed cautiously but be ready to stop if the assumption proves false during implementation.

**If any scout fails → treat as confidence drop → STOP → `/re-plan`.**

### G) Topology freshness gate (required after re-plan decomposition)

If the most recent `/re-plan` split tasks, added/removed tasks, or changed dependency topology, ensure `/sequence-plan` has already run on the updated plan before continuing build.

- Verify active task IDs/dependencies/`Blocks` are internally consistent and the Parallelism Guide reflects the current graph.
- If decomposition occurred but sequencing is stale or missing, STOP and run `/sequence-plan` first, then resume `/build-feature`.

## Build Loop (One Task per Cycle)

### 1) Select the next eligible task

**Rules:**
- Only one IMPLEMENT task at a time.
- Only tasks ≥80% confidence.
- Dependencies must be done.
- **If the next task is a CHECKPOINT → execute the checkpoint protocol (see below) instead of the normal build loop.**

**Dispatch rule:**
- If `Execution-Skill` for the selected task is not `build-feature`, invoke that specialized skill with the task context and expected output path.
- After specialized execution, return to this workflow for confidence reassessment, final validation, commit, and plan updates.

### 2) Restate the task constraints (from the plan)

Extract from the plan into your working context:
- Acceptance criteria
- Validation plan (tests/checklists/reviews to run)
- Rollout/rollback requirements (flags, migrations, backwards compatibility)
- Observability expectations (logging/metrics)
- Documentation impact (standing docs to update)

**If any of these are unclear during execution → treat as confidence drop → STOP → `/re-plan`.**

### 3) Execute using track-appropriate cycle

Choose the execution cycle based on the task's `Execution-Track` / `Deliverable` in the plan:

- **Code/mixed:** follow TDD path (3a–3f)
- **Business-artifact:** follow artifact path (3g–3l)

**a) [Code/mixed] Audit existing tests for extinction**

Before writing new tests, check for existing tests related to the code you're modifying:

1. **Find related tests:** Search for test files covering the affected modules/components
2. **Evaluate test validity:** Read each test and verify it tests *current* behavior, not obsolete contracts
3. **Identify extinct tests:** Tests are "extinct" if they:
   - Assert behavior that no longer exists
   - Test removed/renamed APIs or props
   - Pass or fail for reasons unrelated to current functionality
   - Were not updated when the functional code last changed
4. **Update or remove extinct tests:** Do not layer new tests on top of outdated ones
   - Update extinct tests to reflect current behavior
   - Remove tests for functionality that no longer exists
   - Document any test removals in the commit message

**Why this matters:** Extinct tests give false confidence signals. A passing test suite that includes outdated tests does not validate current behavior.

**b) [Code/mixed] Write or complete tests first**
- If test stubs exist from planning (L-effort tasks):
  1. Convert `test.todo()` / `it.skip()` to active tests with full assertions
  2. Remove the `.todo` or `.skip` modifier
  3. Implement the test body based on the TC-XX specification in the stub comment
- If no stubs exist: write tests based on the task's validation contract (TC-XX specifications)
- Tests should cover the expected behavior before any implementation code is written
- **Mock accuracy gate (before writing any mock):**
  - Read the source file for each component under test and each module/hook you plan to mock.
  - Verify real import paths from source (do not assume module locations).
  - Verify hook return shapes (all properties/destructured fields used by the component).
  - Verify export patterns (`default`, named exports, wrappers like `memo(...)`) before using `jest.requireActual` or module destructuring.
  - Define mocked object returns as stable `const` references outside mock factory functions to avoid React dependency-array re-render loops (see `docs/testing-policy.md`, Rule 6).

**Activating test stubs:**
```typescript
// Before (from planning):
test.todo('should return 409 when entity was modified'); // TC-02

// After (build starts):
test('should return 409 when entity was modified', async () => {
  // TC-02: Concurrent modification → 409 Conflict
  const result = await updateCard(id, { baseEntitySha: 'stale' });
  expect(result.status).toBe(409);
  expect(result.body.error).toBe('CONFLICT');
});
```

**c) [Code/mixed] Run tests — verify they fail for the right reasons**
- Tests should fail because the feature/fix doesn't exist yet
- If tests pass unexpectedly → investigate (feature may already exist, or test is wrong)
- If tests fail for unexpected reasons → STOP → `/re-plan`

**d) [Code/mixed] Implement minimum code to make tests pass**
- Write only what's needed to make tests green
- Keep changes tightly scoped to the task
- Follow established patterns referenced in the plan (or discovered during file-reading)
- If implementation duplicates existing code, use the existing pattern or extract a shared utility — note any new shared abstractions in the commit message
- Do not "sneak in" refactors or over-engineer; if refactor is required, add a new task via `/re-plan`

**e) [Code/mixed] Refactor if needed (tests stay green)**
- Clean up implementation while keeping tests passing
- This is for minor cleanup only, not architectural changes

**f) [Code/mixed] Update documentation**
- Update all docs listed in the task's "Documentation impact" field
- If the task specifies "None", skip this step
- If implementation revealed additional docs needing updates not listed in the plan, update them and note the deviation

**g) [Business-artifact] Staleness check on hypothesis landscape**
- If the fact-find brief includes a Hypothesis & Validation Landscape, scan it for time-sensitive assumptions (supplier quotes, market pricing, regulatory rules, competitor positioning, demand signals) whose validity may have decayed since planning.
- If any key hypothesis depends on data older than 14 days, flag it and verify before drafting. If the assumption no longer holds, STOP → `/re-plan`.
- If no hypothesis landscape exists or all inputs are fresh, proceed.

**h) [Business-artifact] Draft the artifact**
- Produce the minimum viable artifact described in task acceptance.
- Keep scope tightly aligned to task and deliverable type (email/brief/asset/sheet/message).
- Save/update at the path or destination defined in the plan.

**i) [Business-artifact] Run validation checks (VC-XX)**
- Execute every enumerated VC from the validation contract.
- Verify channel/format constraints and compliance/brand requirements.
- If any VC fails unexpectedly and fix is non-obvious → STOP → `/re-plan`.

**j) [Business-artifact] Review and approval handoff**
- Route artifact to the owner/reviewer specified in the plan (or capture review-ready evidence if async).
- Capture explicit owner acknowledgement (who, when, where) and store proof at the `Approval-Evidence` destination defined in plan.
- Record approval status (approved / changes requested / blocked).
- If blocked by unresolved preference/decision → STOP and surface DECISION task.

**k) [Business-artifact] Finalize artifact**
- Incorporate approved revisions.
- Re-run affected VC checks after changes.
- Confirm final artifact destination publish/handoff is complete.
- Confirm measurement tracking is ready at the declared `Measurement-Readiness` location.

**l) [Business-artifact] Update documentation**
- Update playbooks/runbooks/docs listed in "Documentation impact".
- Record any deviations discovered during artifact execution.

### 3b) Confidence Reassessment Based on Validation Outcomes (Mandatory)

After the execution cycle completes, reassess task confidence based on what validation revealed.

#### Validation Outcome → Confidence Impact

| Validation Outcome | Confidence Impact | Action |
|--------------------|-------------------|--------|
| All TCs/VCs pass on first execution | Confidence holds or +5% (max) | Note in plan: "Validation confirmed assumptions" |
| TC/VC reveals edge case not in plan | Confidence -5 to -10% | Add case to plan; note the gap |
| TC/VC reveals missing dependency/contract | Confidence -10 to -20% | May need to update "Affects" or routing; consider `/re-plan` |
| Validation reveals architectural/strategic issue | Confidence drops to <80% | STOP → `/re-plan` |
| Validation case was wrong (not execution) | Confidence holds | Fix case; note correction |
| Execution required >1 cycle (red-green or draft-review) | Confidence -5% per additional cycle | Document iteration in plan |

#### Hard Stop on Confidence Drop

**If post-validation confidence drops below 80%:**
- STOP immediately — do not commit
- Document what validation revealed
- Run `/re-plan` for this task and any dependent tasks

This creates a feedback loop: validation outcomes directly inform confidence, which gates further work.

### 4) Final validation (mandatory)

Run validation aligned to execution track:
- For code/mixed tasks: Typecheck, lint, and full relevant test suites (not just new tests)
- For business-artifact tasks: all VC checks pass, artifact is published to Artifact-Destination, reviewer/owner acknowledgement is captured with Approval-Evidence, and measurement readiness/tracking is confirmed

**Rule: never commit failing execution outputs.** If failures occur:
- If the fix is straightforward and clearly within the task scope, fix it
- If the failure indicates unclear behavior, unexpected dependencies, or uncertain approach:
  - STOP → `/re-plan`

### 5) Confidence and effort re-check during execution

If you encounter any of the following, treat it as a **confidence regression**:
- unexpected dependency or integration boundary
- ambiguous long-term design choice not addressed in the plan
- blast radius larger than documented
- unclear contract/data shape
- unclear channel/approval/compliance requirement for business artifacts
- validation failures that are non-obvious

**Effort misclassification check:**

If the actual work exceeds the classified effort level, STOP and `/re-plan`:
- S-effort task requires 3+ files → should be M or L
- M-effort task requires 6+ files or 3+ integration boundaries → should be L
- Any task introduces a new pattern but wasn't classified L → should be L
- Any task needs e2e tests but wasn't classified L → should be L

Do not continue building an under-classified task. The validation requirements exist to match the actual risk.

**Action:**
- STOP immediately
- Capture what you learned (files, symptoms, failing tests, actual scope)
- Run `/re-plan` for the task with corrected effort classification

### 6) Commit (task-scoped)

Create commits that are unambiguously tied to the task.

**Commit requirements:**
- Include the TASK ID in the subject line.
- Keep the commit scope limited to the task.
- Include the repository's required AI co-author trailer.

**Recommended format:**
```
feat(<feature-slug>): <short change summary> (TASK-XX)
fix(<feature-slug>): <short change summary> (TASK-XX)
test(<feature-slug>): <short change summary> (TASK-XX)
docs(plans): mark TASK-XX complete
```

**Co-authorship:** include `Co-authored-by:` using the exact convention already present in this repo's history/policy.

### 7) Update the plan (required after each task)

After committing the task, update `docs/plans/<feature-slug>-plan.md`:

**Per-task updates:**

Add or update:
- **Status:** `Complete (YYYY-MM-DD)`
- **Implementation Notes:** what changed, and where
- **Validation Evidence:** commands run + results summary
- **Commit(s):** commit hash(es) for traceability

If execution changed understanding:
- note confidence changes (and why)
- if confidence would now be <80%, do not "paper over" it—stop and `/re-plan`

**Plan-level updates:**
- Update `Last-updated`
- If your plan uses an effort-weighted `Overall-confidence`, recompute only if you materially changed confidence values (optional; do not churn it unnecessarily)
- If the plan has a Task Summary table, update it (e.g., add a Status column if not present, or mark TASK-XX as Done). If it does not, do status tracking inside each TASK section.

**Suggested per-task completion snippet:**

Add under the task:

```markdown
#### Build Completion (YYYY-MM-DD)
- **Status:** Complete
- **Commits:** <hash1>, <hash2>
- **Execution cycle:**
  - Validation cases executed: <TC-XX and/or VC-XX>
  - Cycles: <red-green count or draft-review count>
  - Initial validation: <FAIL expected / draft pending review>
  - Final validation: PASS
- **Confidence reassessment:**
  - Original: XX%
  - Post-validation: YY%
  - Delta reason: <validation confirmed | edge case found | dependency discovered>
- **Validation:**
  - Ran: `<commands/checklists>` — PASS
- **Documentation updated:** <list of docs updated, or "None required">
- **Implementation notes:** <what changed, any deviations from plan>
```

### 8) Repeat

Move to the next eligible IMPLEMENT task and repeat the cycle.

### 9) Archive completed plan

When all tasks in the plan are marked Complete, archive the plan:

1. Set frontmatter `Status: Archived` (not `Complete`).
2. Move the plan file to `docs/plans/archive/`.
3. Commit: `docs(plans): archive <plan-name> — all tasks complete`

## CHECKPOINT Handling

When the next task in sequence is a `CHECKPOINT` task, execute this protocol instead of the normal build loop:

### 1) Gather evidence from completed tasks

Summarize what was learned during the build so far:
- Which tasks completed successfully and what they revealed
- Any unexpected findings, scope changes, or confidence adjustments
- Whether the "Horizon assumptions to validate" listed in the CHECKPOINT have been confirmed or disproved

### 2) Run `/re-plan` on remaining tasks

Invoke `/re-plan` targeting all tasks that come **after** the CHECKPOINT in the plan. This re-assessment uses evidence from completed tasks (E2/E3 class) to:
- Reassess confidence on remaining tasks using real implementation evidence
- Split tasks that are too large or depend on unproven assumptions
- Abandon or defer tasks that are no longer viable given what was learned
- Insert new tasks discovered during execution
- Update the plan with any new findings

If `/re-plan` decomposes or topology-edits the remaining tasks, run `/sequence-plan` before evaluating readiness to continue building.

### 3) Evaluate re-plan results

After `/re-plan` completes:

- **If decomposition/topology changes occurred and sequencing has not run yet:** STOP and run `/sequence-plan`, then re-evaluate.
- **If remaining tasks are ≥80% and no open questions:** Mark the CHECKPOINT as complete, then continue the build loop with the next eligible task.
- **If some tasks were revised but are still ≥80%:** Mark CHECKPOINT complete, continue building the revised tasks.
- **If remaining tasks dropped below 80%:** Mark CHECKPOINT complete, then follow the normal below-threshold protocol (stop building those tasks, report to user).
- **If the approach was fundamentally invalidated:** Mark CHECKPOINT complete, stop building, and report the dead end with evidence for what went wrong and what alternatives exist.

### 4) Update the plan

Mark the CHECKPOINT task as `Complete (YYYY-MM-DD)` with a note summarizing:
- Assumptions validated / invalidated
- Tasks revised, added, or removed
- Decision to continue, revise, or stop

### Why CHECKPOINTs matter

Without CHECKPOINTs, a plan with 8 dependent tasks could build all 8 before discovering task 2's assumption was wrong — wasting tasks 3–8. With a CHECKPOINT after task 3, the re-assessment catches the problem after 3 tasks instead of 8. The cost of a CHECKPOINT (one `/re-plan` invocation) is far less than the cost of a dead-end deep in implementation.

## Stopping Conditions (Hard Stops)

| Condition | Action |
|-----------|--------|
| Task is <80% confidence (or becomes unclear mid-build) | Stop immediately → `/re-plan` |
| Task requires modifying files not listed in "Affects" | Stop → update plan or `/re-plan` |
| Unexpected dependency / larger blast radius discovered | Stop → `/re-plan` (and update affected tasks) |
| Actual scope exceeds classified effort level | Stop → `/re-plan` with corrected effort (validation must match risk) |
| Validation fails and fix is non-obvious | Stop → `/re-plan` |
| A DECISION is required (product/UX preference) | Stop → ask user via DECISION task in plan |
| Baseline repo is failing unrelated checks | Stop → document and resolve via separate planned work |
| Re-plan decomposed tasks but plan was not re-sequenced | Stop → run `/sequence-plan`, then resume build |
| Next task is a CHECKPOINT | Pause build → execute CHECKPOINT protocol → `/re-plan` remaining tasks → resume if still viable |

## Rules

- One IMPLEMENT task per cycle.
- Never build below 80% confidence.
- Never skip validation.
- Never commit failing execution outputs.
- Do not expand scope beyond the plan.
- Update the plan after every completed task.

## Feedback to Future Planning

When confidence changes based on validation outcomes, capture the learning for future work:

| Finding Type | Feedback Action |
|--------------|-----------------|
| Edge case was missed | Note category of edge case for future fact-finds |
| Dependency was missed | Note discovery pattern for future impact analysis |
| Architecture issue found | Flag for architectural review; update conventions docs |
| Validation revealed undocumented behavior | Update system docs or briefs/playbooks |

This feedback loop improves future `/fact-find` and `/plan-feature` accuracy. When completing a task, explicitly note any learnings that should inform future planning.

**Escalation to user:** Only ask the user when:
- Business rules/UX intent cannot be inferred from repo or docs
- Two approaches are truly equivalent and require preference
- You have exhausted evidence sources and the uncertainty remains

When you do ask:
- Ask the minimum number of questions required to proceed
- Each question must state what decision it gates
- Include a recommended default with risk assessment if appropriate

## Quality Checks

A build cycle is considered complete only if:

- [ ] Pre-build checks (A–E) all passed before executing task work.
- [ ] Existing related tests were audited for extinction (code/mixed tasks).
- [ ] Code/mixed tasks: tests were written/completed BEFORE implementation code (TDD).
- [ ] Code/mixed tasks: tests initially failed for the expected reasons (feature not yet implemented).
- [ ] Business-artifact tasks: hypothesis landscape staleness checked before drafting (if available).
- [ ] Business-artifact tasks: artifact drafted, reviewed, finalized, and published/handoff completed against VC checks.
- [ ] Business-artifact tasks: reviewer/owner acknowledgement captured and linked in Approval-Evidence.
- [ ] Business-artifact tasks: post-delivery tracking readiness confirmed in Measurement-Readiness destination.
- [ ] Implementation is scoped exactly to the task (no scope creep).
- [ ] Actual scope matched classified effort (if not, stopped and re-planned with correct effort).
- [ ] Standing documentation updated per "Documentation impact" field (or confirmed "None").
- [ ] All required validations passed (code commands and/or VC checklists).
- [ ] Commits include TASK ID and are scoped to the task.
- [ ] Plan doc updated with Status, Commits, Validation evidence.
- [ ] Confidence was re-assessed; if <80%, stopped and triggered `/re-plan`.
- [ ] No failing execution output was committed.

### Execution Quality Checks

- [ ] Confidence was reassessed after execution cycle completed.
- [ ] Post-validation confidence is documented in plan.
- [ ] If confidence dropped below 80%, stopped and triggered `/re-plan`.
- [ ] Cycle counts documented (red-green for code, draft-review for business artifacts).
- [ ] All enumerated validation cases (TC-XX and/or VC-XX) from plan were executed.

## Completion Messages

Use one of the following outcomes:

**A) All eligible tasks complete:**
> "All eligible IMPLEMENT tasks are complete and validated. Plan updated with completion status and validation evidence. Remaining work: <none / list>. Ready for PR review."

**B) Some tasks remain but are not eligible:**
> "Completed N/M IMPLEMENT tasks (≥80% confidence). Tasks <IDs> are not eligible (confidence <80% or blocked). Recommend `/re-plan` for those tasks before continuing."

**C) Stopped mid-task due to confidence regression:**
> "Stopped during TASK-XX due to newly discovered complexity or unclear blast radius. No further execution will proceed until `/re-plan` updates the plan for TASK-XX (and any dependent tasks)."

## Business OS Integration (Default)

When plan frontmatter includes `Card-ID`, `/build-feature` integrates with Business OS by default.

**Escape hatch:** set `Business-OS-Integration: off` in plan frontmatter to skip card/stage-doc/lane writes for intentionally standalone work.

**Fail-closed rule:** if any API call fails, stop and surface the error.

### When Card-ID is Present (and integration is on)

#### Step 1: Start Build Transition (First Task Only)

Before starting first task, perform build-start transition via API.

**1a) Read the card to get current lane + entity SHA:**

```json
{
  "method": "GET",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/cards/PLAT-ENG-0023",
  "headers": { "X-Agent-API-Key": "${BOS_AGENT_API_KEY}" }
}
```

Response includes `{ entity, entitySha }`.

**1b) Create build stage doc if missing:**

```json
{
  "method": "GET",
  "url": "${BOS_AGENT_API_BASE_URL}/api/agent/stage-docs?cardId=PLAT-ENG-0023&stage=build",
  "headers": { "X-Agent-API-Key": "${BOS_AGENT_API_KEY}" }
}
```

If none exists, create it via `POST /api/agent/stage-docs`.

**1c) Deterministic lane transition (Planned -> In progress):**

If current `Lane` is `Planned`, update directly and set `Last-Progress`:

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
      "Lane": "In progress",
      "Last-Progress": "YYYY-MM-DD"
    }
  }
}
```

**Conflict handling:** on `409 CONFLICT`, refetch and retry once. If retry conflicts, stop.

#### Step 2: Update Card Progress (After Each Task)

After each task commit + plan update:
- PATCH card `Last-Progress`
- PATCH build stage doc content (progress tracker + build log)

#### Step 3: Check for Completion (After Each Task)

When all eligible IMPLEMENT tasks are complete and validations passed:
- Update build stage doc transition checklist
- Perform deterministic Done transition (Step 4)

#### Step 4: Deterministic lane transition (In progress -> Done)

Move card directly to `Done` when all completion-gate criteria are true:
- All eligible IMPLEMENT tasks complete with evidence
- All required validations passing (tests and/or VC checks)
- Documentation impact addressed
- No unresolved blocking DECISION tasks

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
      "Lane": "Done",
      "Last-Progress": "YYYY-MM-DD"
    }
  }
}
```

Do not move to `Done` if any completion criterion is unmet.

#### Step 5: Discovery index freshness

After card/stage-doc writes and deterministic lane transitions, rebuild discovery index:

```bash
docs/business-os/_meta/rebuild-discovery-index.sh > docs/business-os/_meta/discovery-index.json
```

Retry once; if it still fails, stop and surface `discovery-index stale`.

On repeated failure, include:
- failing command,
- retry count,
- stderr summary,
- exact operator rerun command.

Do not emit a clean completion message while index state is stale.

### Completion Messages (with Card-ID)

**A) All eligible tasks complete:**
> "All eligible IMPLEMENT tasks are complete and validated. Plan updated with completion status and validation evidence. Card {CARD-ID} Last-Progress updated via API. Build stage doc updated via API. Deterministic lane transition applied: `In progress -> Done`."

**B) Some tasks remain:**
> "Completed N/M IMPLEMENT tasks. Card {CARD-ID} Last-Progress updated to {DATE} via API. Build stage doc updated with progress. Lane remains `In progress` until completion gate is satisfied."

**C) Stopped mid-task:**
> "Stopped during TASK-XX. Card {CARD-ID} Last-Progress remains at previous value. Build stage doc records the blocker."

### Without Card-ID (or Integration Off)

Skip all Business OS integration steps and use standard completion messages.

### Related Resources

- Card operations: `.claude/skills/_shared/card-operations.md`
- Stage doc operations: `.claude/skills/_shared/stage-doc-operations.md`
- Exception-only/manual lane proposals (non-mechanical transitions): `.claude/skills/propose-lane-move/SKILL.md`
