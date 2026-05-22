---
name: implement-project
description: Full-lifecycle project workflow. Takes batched tickets, implements via /implement-batch, runs smoke tests, then executes a comprehensive quality pipeline (refactor, review-arch, review-test, tidy-docs, review-release). Maximizes autonomy with andon cord escape.
model: opus
---

# Implement-Project - Full-Lifecycle Project Workflow

Orchestrates an entire project from tickets to release-ready code. Implements batched tickets via `/implement-batch`, runs smoke tests, then executes a comprehensive quality pipeline. Maximizes autonomy — the andon cord is the only planned escalation path.

## Philosophy

This skill implements the autonomy discipline documented in [`references/autonomy.md`](../../references/autonomy.md): the five levers (altitude rule, pre-loaded options, pre-rebutted recommendation, commander's intent, risk budgets), the cascade rule, the shared handoff template, and the "log instead of escalate" pattern. Its commander's-intent schema is the four-field variant defined there (tickets, acceptance bar, constraints, non-goals).

**Autonomy is the default; escalation is the exception.** The goal is to complete an entire project — multiple batches of tickets, quality passes, and verification — without user intervention. When stuck, try `/think-deliberate` first. Only pull the andon cord when autonomous resolution has failed or is clearly futile.

**The project branch is the single integration point.** All work flows into the project branch. Batches merge into it, quality passes commit to it, and the user makes one decision at the end: merge or don't.

**Quality is layered.** Each quality pass builds on the previous one. Refactoring cleans the code so review-arch can focus on structure. Arch-review surfaces structural recommendations (advisory only — `/review-arch` no longer implements changes; see the "Advisory aspiration" section of [`references/autonomy.md`](../../references/autonomy.md)) so review-test can survey coverage of the current form. Review-test surfaces ticket-shaped test work (advisory only — `/review-test` no longer writes tests in-skill). Tidy-docs documents what actually shipped. Release-review validates the whole.

**Fresh eyes catch what familiarity misses.** Each quality pass runs its full workflow, including any embedded sub-passes (e.g., `/refactor` runs its own `/tidy-docs`). Redundancy is intentional — each agent sees the project with fresh context and may catch issues that prior passes normalized.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     PROJECT WORKFLOW                         │
├──────────────────────────────────────────────────────────────┤
│  1. Gather tickets and batching strategy                     │
│  2. Discuss smoke testing procedures                         │
│  3. Plan execution + elicit commander's intent               │
│  4. Create project branch                                    │
│  5. Per-batch loop:                                          │
│     ├─ 5a. Create batch branch from project branch           │
│     ├─ 5b. Run /implement-batch workflow (autonomous mode)   │
│     ├─ 5c. Merge batch branch → project branch               │
│     ├─ 5d. Post-merge verification                           │
│     └─ 5e. Clean up and checkpoint                           │
│  6. Smoke testing                                            │
│  7. Quality pipeline:                                        │
│     ├─ 7a. /refactor (MAXIMUM aggression)                    │
│     ├─ 7b. /review-arch (advisory; ticket proposal)          │
│     ├─ 7c. /review-test (advisory; ticket proposal)          │
│     ├─ 7d. /tidy-docs                                       │
│     └─ 7e. /review-release                                   │
│  8. Final report                                             │
└──────────────────────────────────────────────────────────────┘
```

The former conditional second `/refactor` (previously step 7c, which ran when `/review-arch` made substantive changes) is removed. `/review-arch` is now advisory and does not make changes; the conditional can never fire.

## Available Tools

Beyond the mainline workflow, the orchestrator has access to additional workflows:

- **`/think-deliberate`**: Adversarial deliberation for difficult autonomous decisions. Spawns advocates to argue options before rendering a verdict. Prefer this over gut-feel decisions when stakes are high or trade-offs are unclear.
- **`/bug-fix`**: Coordinated bug-fixing for challenging issues encountered during any phase. Handles diagnosis, reproduction, and targeted fixes.

## Andon Cord Protocol

**This protocol applies throughout the entire workflow.** The andon cord is the escape valve for problems that cannot be resolved autonomously.

**Before pulling the andon cord:**
1. Attempt autonomous resolution first.
2. For judgment calls, run `/think-deliberate` to reason through options.
3. Only escalate if autonomous resolution has failed or is clearly futile.

**When the andon cord is pulled:**
1. **Stop all work immediately** — do not attempt to continue with other batches or steps.
2. Produce a handoff using the **shared handoff template** in [`references/autonomy.md`](../../references/autonomy.md). The escalation must include pre-loaded options (2–3 named choices), an explicit recommendation, the one tradeoff that would flip the recommendation, and a pre-rebutted counterargument. Include the skill-specific state: current phase and step, what `/think-deliberate` was already considered, current state of all branches (what's merged into the project branch, what's in-progress), and how far through the per-batch loop or quality pipeline the run is.
3. Wait for user guidance before resuming.

**Andon cord triggers (skill-specific):**
- Batch workflow pulls its own andon cord (cascades up)
- Merge conflict between batch branch and project branch
- Smoke testing reveals fundamental design issues that can't be fixed locally
- Quality pass reveals blocking issues the orchestrator can't resolve
- Project branch already exists (step 4)
- Any situation where continuing would compound errors rather than resolve them

## Workflow Details

### 1. Gather Tickets and Batching Strategy

**Ask the user:**
- Which tickets belong to this project? (IDs, tags, milestones, etc.)
- How are they batched? (e.g., tagged `batch-1`, `batch-2`; or user specifies explicit grouping)
- What's the batch execution order?

**If batching is unclear:** Ask. Do not guess at grouping — the user has a reason for the batch structure.

**Fetch all tickets** using the shared tracker detection from [`references/trackers.md`](../../references/trackers.md). Gather title, description, acceptance criteria, labels, and dependencies for each.

### 2. Discuss Smoke Testing Procedures

**Ask the user:** "What smoke testing should be performed after implementation? This varies by project type."

**Offer examples if the user needs prompts:**
- CLI tool: run the binary with representative commands, verify output
- MCP server: build the binary, send JSON-RPC commands, verify responses
- Web app: use Playwright MCP for browser testing
- Library: run integration tests, verify public API works end-to-end
- API server: hit key endpoints, verify responses

**Record the procedure.** It will be used for:
- Step 6 (smoke testing)
- QA instructions passed to quality passes (steps 7a-7e)

### 3. Plan Execution Across Batches + Elicit Commander's Intent

Analyze all tickets across all batches and produce an execution plan, and elicit the commander's-intent fields beyond the tickets themselves.

**Per-batch analysis:**
- Tickets in this batch and their dependencies
- Estimated scope (qualitative)
- Any concerns about ambiguous or under-specified tickets

**Cross-batch analysis:**
- Dependencies between batches (batch 2 might depend on batch 1's changes)
- Optimal batch ordering
- Risk areas where batches might conflict

**Elicit commander's intent** (the four-field schema from [`references/autonomy.md`](../../references/autonomy.md)):

| Field           | Default                                                            | Notes                                                                               |
|-----------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Tickets         | Already gathered in step 1                                         | Pre-filled; operator confirms.                                                      |
| Acceptance bar  | "All tickets implemented, full pipeline passes"                    | Operator may extend (e.g., "and CHANGELOG mentions every user-visible change").     |
| Constraints     | None                                                               | Cross-cutting limits not encoded in individual tickets (e.g., "must remain compatible with library version X"). |
| Non-goals       | None                                                               | Explicit out-of-scope items. The orchestrator will not touch these even if it sees opportunity. |

Acceptance bar, constraints, and non-goals frame the orchestrator's judgment for the rest of the run. When the quality pipeline surfaces opportunities outside these bounds, they are deferred to the final report rather than acted on.

**Present the plan to the user.** This is the primary planned user interaction point. Include:
- Proposed batch execution order with rationale
- Per-batch ticket listing with brief scope assessment
- Any concerns about ticket specifications
- Smoke testing procedure (confirmed)
- Commander's intent (the four fields above)
- Branch naming: `feat/project-<name>`, with `feat/batch-<name>` per batch

**Wait for user approval before proceeding.**

### 4. Create Project Branch

- Identify the main branch (`main` or `master`)
- Create project branch from current HEAD: `feat/project-<descriptive-name>`
- **Andon cord** if branch already exists — ask user whether to resume or start fresh
- Initialize `PROJECT_PROGRESS.md` with project metadata and batch plan

### 5. Per-Batch Execution Loop

For each batch in the planned order:

#### 5a. Create Batch Branch

- Checkout project branch (ensure it's current)
- Create batch branch: `feat/batch-<descriptive-name>`

#### 5b. Run `/implement-batch` Workflow (Autonomous Mode)

Invoke the `/implement-batch` workflow with these autonomous overrides:

| `/implement-batch` Step                 | Autonomous Override                                                                                                                                                                                                    |
|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Step 1** (receive tickets)  | Pre-loaded — pass the batch's ticket list directly                                                                                                                                                                     |
| **Step 2** (detect tracker & fetch) | Normal operation                                                                                                                                                                                                 |
| **Step 3** (batch planning)   | **Orchestrator approves the plan autonomously.** Review the proposed execution order. Use `/think-deliberate` if the ordering is unclear or if there are concerning dependency patterns. Only pull the andon cord if tickets are fundamentally incoherent. |
| **Step 4** (create project branch) | **Skip — already on the batch branch.** The batch branch serves as `/implement-batch`'s "project branch." Topic branches are created from it.                                                                             |
| **Steps 5a-5e** (per-ticket loop)  | Normal operation. Topic branches are created from the batch branch. Andon cord triggers cascade up to the project orchestrator.                                                                                  |
| **Step 6** (quality passes)   | Normal operation. Let `/implement-batch` run its own refactor + tidy-docs.                                                                                                                                                      |
| **Step 7** (final review)     | **Orchestrator reviews autonomously.** Log the summary to `PROJECT_PROGRESS.md`. Do not wait for user input.                                                                                                          |

#### 5c. Merge Batch Branch into Project Branch

- Checkout project branch
- Merge: `git merge --no-ff feat/batch-<name>`
- The `--no-ff` preserves batch branch history for clarity
- **Andon cord** on merge conflict — do not attempt auto-resolution

#### 5d. Post-Merge Verification

- Run the full test suite on the project branch
- Run linters/formatters
- **Andon cord** if tests fail — the merge introduced a regression

#### 5e. Clean Up and Checkpoint

- Delete the merged batch branch: `git branch -d feat/batch-<name>`
- Update `PROJECT_PROGRESS.md`: mark batch as complete, record summary

### 6. Smoke Testing

Execute the smoke testing procedure established in step 2.

**On issues found:**
1. Diagnose the issue
2. For straightforward fixes: implement, verify, commit
3. For complex bugs: invoke the `/bug-fix` workflow
4. For design-level problems: try `/think-deliberate` first, then andon cord if unresolvable
5. Re-run smoke tests after fixes until clean

**Update `PROJECT_PROGRESS.md`** with smoke test results and any fixes applied.

### 7. Quality Pipeline

Run each quality pass sequentially. The orchestrator may use judgment to skip passes for trivial projects (e.g., 2 small tickets with no architectural impact may not need `/review-arch`). If skipping, note the reason in the final report.

#### 7a. Refactor

Run the `/refactor` workflow with:
- **Aggression ceiling:** MAXIMUM
- **QA instructions:** The smoke testing procedure from step 2
- **Scope:** Entire codebase

#### 7b. Arch Review (Advisory)

Run the `/review-arch` workflow. As of v8.0.0, `/review-arch` no longer makes changes — it produces an analysis and proposes a ticket structure for the recommended work.

Invocation parameters:
- **Scope:** Entire codebase

The orchestrator receives `/review-arch`'s ticket-structure proposal and applies its own judgment per [`references/autonomy.md`](../../references/autonomy.md):

- **Approve** items that should be tracked for follow-up (typically items that are out of scope for the current project but worth capturing durably).
- **Edit** the proposed structure if finer-grained or coarser-grained tickets would compose better with other planned work.
- **Decline** items that the orchestrator will implement inline as part of the quality pipeline.

For items the orchestrator declines (intending to handle inline), surface them in the final report (step 8) under "Architectural Recommendations Acted On" along with what was actually implemented. For items where tickets were cut, surface them under "Deferred Items / Architectural Recommendations" with their ticket numbers, so the operator knows to follow up after the project ships.

The orchestrator should be conservative: cutting a ticket for a finding is always safer than declining it (declining commits the orchestrator to handling it inline, which may not actually happen in the current pipeline).

#### 7c. Test Review (Advisory)

Run the `/review-test` workflow. As of v9.0.0, `/review-test` is advisory only — it surveys all five phases (unit coverage, integration, E2E, fuzz, quality) and produces a ticket-structure proposal rather than implementing test changes in-skill. The orchestrator receives the proposal and applies its own autonomy judgment per `references/autonomy.md`:

- **Approve a ticket** when the work is well-scoped, the implementation requires deliberation (test design, mocking strategy, infrastructure setup), or the orchestrator does not intend to implement it inline within this project.
- **Edit the structure** to merge, split, drop, or promote items (including refactor-for-testability suggestions) before approval.
- **Decline a ticket** if the orchestrator intends to implement the work inline within this project — typically the unit-coverage gaps the orchestrator wants to close as part of the current pipeline.

For items the orchestrator declines (intending to handle inline), surface them in the final report (step 8) under "Test Recommendations Acted On" along with what was actually implemented. For items where tickets were cut, surface them under "Deferred Items / Test Recommendations" with their ticket numbers.

Phase 3's journey-classification confirmation step still requires user input even when invoked autonomously — the classification shapes ticket priorities and is the most subjective input in the analysis. The orchestrator should answer based on the project's commander's intent (which user journeys are critical to this project) and surface any uncertainty as an andon-cord pull rather than guessing.

The orchestrator should be conservative: cutting a ticket for a test finding is safer than declining it (declining commits the orchestrator to handling it inline, which may not actually happen in the current pipeline).

#### 7d. Tidy-Docs

Run the `/tidy-docs` workflow:
- Full documentation audit
- Fixes committed separately

#### 7e. Release Review

Run the `/review-release` workflow with autonomous overrides:

For each finding the release review surfaces:
- **Auto-fix:** Debug artifacts, version mismatches, changelog gaps, formatting issues
- **Deliberate:** Ambiguous findings, trade-off decisions
- **Defer to final report:** Items that require user judgment (e.g., "should this breaking change be noted in CHANGELOG?")
- **Andon cord:** Blocking issues that can't be resolved (e.g., tests fail, build broken)

### 8. Final Report

Present comprehensive summary to user:

```
## Project Complete

### Batches Implemented
- Batch 1 (<name>): N tickets completed
  - #12: <title> — <brief outcome>
  - #15: <title> — <brief outcome>
- Batch 2 (<name>): N tickets completed
  - #18: <title> — <brief outcome>

### Smoke Testing
- Result: PASS / N issues found and fixed
- [Brief description of any fixes applied]

### Quality Pipeline Results
- Refactor (pass 1): N commits, net -XXX lines
- Arch Review: advisory report produced (no changes made — /review-arch is advisory)
- Test Review: advisory report produced; N tickets created / N declined / N approved-inline
- Tidy-Docs: N documentation updates
- Release Review: N findings resolved, N deferred

### Deferred Items / Architectural Recommendations
[Items the orchestrator chose not to implement, with rationale.
 Includes /review-arch's recommendations from step 7b — each names
 a specific follow-up skill with scope hint (e.g.,
 "Dead code in src/foo/: /refactor scoped to that directory").
 These are actionable next steps for the user.]

### Deferred Items / Test Recommendations
[Tickets cut from step 7c that the orchestrator chose not to handle
 inline, plus any items it implemented inline alongside the ticket
 numbers. Each ticket names a specific follow-up skill with scope hint.]

### Statistics
- Total commits: N
- Net lines changed: +/-N
- Tests added during batch implementation: N (this counts tests written
  by SMEs during ticket implementation in step 5; /review-test does not
  add tests itself — it surfaces ticket-shaped work)
- Documentation files updated: N

### Branch Status
- Project branch: feat/project-<name>
- Base branch: <main branch>
- Ready for review and merge
```

User decides next steps: merge to main, further work, or discard.

## State Management

### PROJECT_PROGRESS.md

Maintain a progress file at the repository root throughout the workflow. This file is gitignored and serves two purposes: human-readable progress tracking and crash recovery context.

**Structure:**
```markdown
# Project: <name>
Started: <timestamp>
Branch: feat/project-<name>
Status: <current phase>

## Configuration
- Smoke testing: <procedure summary>
- Batches: <count>

## Batch Progress

### Batch 1: <name> — COMPLETE
- Tickets: #12, #15
- Commits: N
- Summary: <brief>

### Batch 2: <name> — IN PROGRESS
- Tickets: #18, #20
- Current ticket: #20
- Status: implementing

## Quality Pipeline
- [x] Refactor
- [ ] Arch Review (advisory)
- [ ] Test Review
- [ ] Tidy-Docs
- [ ] Release Review

## Issues Log
- <timestamp>: <issue description and resolution>
```

**Update at every major transition:** batch start/complete, quality pass start/complete, andon cord events, smoke test results.

## Agent Coordination

**Sequential execution:**
- One batch at a time, one quality pass at a time
- Each sub-workflow completes before the next begins
- No parallel execution

**Context management:**
- The project orchestrator is a thin coordinator
- It delegates all implementation to sub-workflows
- It maintains only summary-level state in its context
- `PROJECT_PROGRESS.md` provides durable state outside the context window
- Keep per-batch and per-pass summaries brief to avoid context bloat

**Sub-workflow invocation:**
- Quality passes (`/refactor`, `/review-arch`, `/review-test`, `/tidy-docs`, `/review-release`): invoke as skills
- `/implement-batch`: invoke as a skill with autonomous overrides
- `/think-deliberate`, `/bug-fix`: invoke as skills when needed

## Abort Conditions

**Abort current batch:**
- Batch workflow's own andon cord triggers
- Merge conflict into project branch
- Post-merge test failures

**Abort quality pass:**
- Quality pass encounters unresolvable issues after `/think-deliberate`
- Skip the pass, log the issue, continue with next pass
- Include in final report

**Abort entire workflow:**
- User interrupts
- Git repository in unclean state that can't be resolved
- Multiple consecutive andon cord pulls suggest fundamental problems
- Critical system error

**Do NOT abort for:**
- Individual ticket failures within a batch (handled by `/implement-batch`)
- Quality pass recommendations the orchestrator disagrees with (defer them)
- Minor issues that can be noted in the final report

## Integration with Other Skills

**Relationship to `/implement-batch`:**
- `/implement-project` is a higher-level orchestrator that runs `/implement-batch` for each batch of tickets
- `/implement-batch` handles the per-ticket implementation loop via `/implement`
- `/implement-project` adds: multi-batch coordination, smoke testing, comprehensive quality pipeline

**Relationship to `/scope`:**
- `/scope` creates tickets; `/implement-project` consumes them
- Typical flow: `/scope` to plan → organize tickets into batches → `/implement-project` to implement

**Relationship to quality passes:**
- `/implement-project` runs each quality pass as a complete workflow
- Each pass operates on the full codebase with fresh context
- Passes build on each other: refactor → review-arch (advisory) → test → doc → release

**Hierarchy:**
```
/implement-project
├── /implement-batch (per batch)
│   ├── /implement (per ticket)
│   ├── /refactor (per-batch quality)
│   └── /tidy-docs (per-batch quality)
├── /refactor (project-level quality)
├── /review-arch (project-level quality, advisory; ticket proposal)
├── /review-test (project-level quality)
├── /tidy-docs (project-level quality)
└── /review-release (project-level quality)
```
