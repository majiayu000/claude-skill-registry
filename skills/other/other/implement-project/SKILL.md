---
name: implement-project
description: Full-lifecycle project workflow. Takes batched tickets, implements via /implement-batch, runs smoke tests, then executes a comprehensive quality pipeline (refactor, review-arch, review-test, review-doc, review-release). Maximizes autonomy with andon cord escape.
model: opus
---

# Implement-Project - Full-Lifecycle Project Workflow

Orchestrates an entire project from tickets to release-ready code. Implements batched tickets via `/implement-batch`, runs smoke tests, then executes a comprehensive quality pipeline. Maximizes autonomy — the andon cord is the only planned escalation path.

## Philosophy

**Autonomy is the default; escalation is the exception.** The goal is to complete an entire project — multiple batches of tickets, quality passes, and verification — without user intervention. When stuck, try `/deliberate` first. Only pull the andon cord when autonomous resolution has failed or is clearly futile.

**The project branch is the single integration point.** All work flows into the project branch. Batches merge into it, quality passes commit to it, and the user makes one decision at the end: merge or don't.

**Quality is layered.** Each quality pass builds on the previous one. Refactoring cleans the code so review-arch can focus on structure. Arch-review restructures so review-test can assess coverage of the final form. Doc-review documents what actually shipped. Release-review validates the whole.

**Fresh eyes catch what familiarity misses.** Each quality pass runs its full workflow, including any embedded sub-passes (e.g., `/refactor` runs its own `/review-doc`). Redundancy is intentional — each agent sees the project with fresh context and may catch issues that prior passes normalized.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     PROJECT WORKFLOW                         │
├──────────────────────────────────────────────────────────────┤
│  1. Gather tickets and batching strategy                     │
│  2. Discuss smoke testing procedures                         │
│  3. Plan execution across batches                            │
│  4. Create project branch                                    │
│  5. Per-batch loop:                                          │
│     ├─ 5a. Create batch branch from project branch           │
│     ├─ 5b. Run /implement-batch workflow (autonomous mode)             │
│     ├─ 5c. Merge batch branch → project branch               │
│     ├─ 5d. Post-merge verification                           │
│     └─ 5e. Clean up and checkpoint                           │
│  6. Smoke testing                                            │
│  7. Quality pipeline:                                        │
│     ├─ 7a. /refactor (MAXIMUM aggression)                    │
│     ├─ 7b. /review-arch (autonomous mode)                    │
│     ├─ 7c. /refactor again (conditional)                     │
│     ├─ 7d. /review-test                                      │
│     ├─ 7e. /review-doc                                       │
│     └─ 7f. /review-release                                   │
│  8. Final report                                             │
└──────────────────────────────────────────────────────────────┘
```

## Available Tools

Beyond the mainline workflow, the orchestrator has access to additional workflows:

- **`/deliberate`**: Adversarial deliberation for difficult autonomous decisions. Spawns advocates to argue options before rendering a verdict. Prefer this over gut-feel decisions when stakes are high or trade-offs are unclear.
- **`/bugfix`**: Coordinated bug-fixing for challenging issues encountered during any phase. Handles diagnosis, reproduction, and targeted fixes.

## Andon Cord Protocol

**This protocol applies throughout the entire workflow.** The andon cord is the escape valve for problems that cannot be resolved autonomously.

**Before pulling the andon cord:**
1. Attempt autonomous resolution first
2. For judgment calls, run `/deliberate` to reason through options
3. Only escalate if autonomous resolution has failed or is clearly futile

**When the andon cord is pulled:**
1. **Stop all work immediately** — do not attempt to continue with other batches or steps
2. Present to user:
   - Current phase and step
   - What was attempted and what went wrong
   - What autonomous resolution was tried (including any `/deliberate` results)
   - Current state of all branches (what's merged, what's in-progress)
   - Recommended path forward (if you have one)
3. Wait for user guidance before resuming

**Andon cord triggers:**
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

**Fetch all tickets** using the same tracker detection as `/implement-batch` (GitHub → `gh`, Gitea → MCP tools, etc.). Gather title, description, acceptance criteria, labels, and dependencies for each.

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
- QA instructions passed to quality passes (steps 7a-7f)

### 3. Plan Execution Across Batches

Analyze all tickets across all batches and produce an execution plan.

**Per-batch analysis:**
- Tickets in this batch and their dependencies
- Estimated scope (qualitative)
- Any concerns about ambiguous or under-specified tickets

**Cross-batch analysis:**
- Dependencies between batches (batch 2 might depend on batch 1's changes)
- Optimal batch ordering
- Risk areas where batches might conflict

**Present the plan to the user.** This is the primary planned user interaction point. Include:
- Proposed batch execution order with rationale
- Per-batch ticket listing with brief scope assessment
- Any concerns about ticket specifications
- Smoke testing procedure (confirmed)
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
| **Step 3** (batch planning)   | **Orchestrator approves the plan autonomously.** Review the proposed execution order. Use `/deliberate` if the ordering is unclear or if there are concerning dependency patterns. Only pull the andon cord if tickets are fundamentally incoherent. |
| **Step 4** (create project branch) | **Skip — already on the batch branch.** The batch branch serves as `/implement-batch`'s "project branch." Topic branches are created from it.                                                                             |
| **Steps 5a-5e** (per-ticket loop)  | Normal operation. Topic branches are created from the batch branch. Andon cord triggers cascade up to the project orchestrator.                                                                                  |
| **Step 6** (quality passes)   | Normal operation. Let `/implement-batch` run its own refactor + review-doc.                                                                                                                                                      |
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
3. For complex bugs: invoke the `/bugfix` workflow
4. For design-level problems: try `/deliberate` first, then andon cord if unresolvable
5. Re-run smoke tests after fixes until clean

**Update `PROJECT_PROGRESS.md`** with smoke test results and any fixes applied.

### 7. Quality Pipeline

Run each quality pass sequentially. The orchestrator may use judgment to skip passes for trivial projects (e.g., 2 small tickets with no architectural impact may not need `/review-arch`). If skipping, note the reason in the final report.

#### 7a. Refactor

Run the `/refactor` workflow with:
- **Aggression ceiling:** MAXIMUM
- **QA instructions:** The smoke testing procedure from step 2
- **Scope:** Entire codebase

#### 7b. Arch Review (Autonomous Mode)

Run the `/review-arch` workflow with autonomous overrides:

| `/review-arch` Step                  | Autonomous Override                                                                                                                                                                                                                                      |
|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Step 1** (scope)                   | Entire codebase                                                                                                                                                                                                                                          |
| **Step 2** (QA instructions)         | The smoke testing procedure from step 2                                                                                                                                                                                                                  |
| **Step 3** (analyze)                 | Normal operation                                                                                                                                                                                                                                         |
| **Step 4** (present analysis)        | **Orchestrator reviews the analysis.** Do not present to user.                                                                                                                                                                                           |
| **Step 5** (iterate on plan)         | **Orchestrator decides what to implement.** Approve items that are clearly beneficial (dead code removal, obvious naming improvements, clear function ownership fixes). For high-impact items (module dissolution, major restructuring, new module creation), use `/deliberate` to reason through the trade-offs. Defer items that seem out of scope for this project — note them in the final report as recommendations. |
| **Step 6** (how to proceed)          | Proceed with implementation of approved items                                                                                                                                                                                                            |
| **Steps 7-9** (implement + summary)  | Normal operation                                                                                                                                                                                                                                         |
| **Step 10** (review-doc)             | Normal operation                                                                                                                                                                                                                                         |

**Track whether review-arch made substantive changes** — module restructuring, function moves, new modules. Dead code removal and naming fixes do not count. This determines whether step 7c runs.

#### 7c. Refactor Again (Conditional)

**Only run if review-arch made substantive changes** in step 7b.

Run `/refactor` again with the same parameters as step 7a. Architectural restructuring often introduces code that benefits from tactical cleanup.

#### 7d. Test Review

Run the `/review-test` workflow.

The orchestrator handles any interactive steps autonomously, applying the same pattern: implement what's clearly beneficial, `/deliberate` for judgment calls, andon cord as last resort.

#### 7e. Doc Review

Run the `/review-doc` workflow:
- Full documentation audit
- Fixes committed separately

#### 7f. Release Review

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
- Arch Review: N items implemented, N deferred
- Refactor (pass 2): [ran/skipped] — N commits, net -XXX lines
- Test Review: N tests added, N gaps filled
- Doc Review: N documentation updates
- Release Review: N findings resolved, N deferred

### Deferred Items
[Items the orchestrator chose not to implement, with rationale.
 These are recommendations for the user to consider.]

### Statistics
- Total commits: N
- Net lines changed: +/-N
- Tests added/modified: N
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
- [x] Refactor (pass 1)
- [ ] Arch Review
- [ ] Refactor (pass 2)
- [ ] Test Review
- [ ] Doc Review
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
- Quality passes (`/refactor`, `/review-arch`, `/review-test`, `/review-doc`, `/review-release`): invoke as skills
- `/implement-batch`: invoke as a skill with autonomous overrides
- `/deliberate`, `/bugfix`: invoke as skills when needed

## Abort Conditions

**Abort current batch:**
- Batch workflow's own andon cord triggers
- Merge conflict into project branch
- Post-merge test failures

**Abort quality pass:**
- Quality pass encounters unresolvable issues after `/deliberate`
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
- Passes build on each other: refactor → review-arch → refactor → test → doc → release

**Hierarchy:**
```
/implement-project
├── /implement-batch (per batch)
│   ├── /implement (per ticket)
│   ├── /refactor (per-batch quality)
│   └── /review-doc (per-batch quality)
├── /refactor (project-level quality)
├── /review-arch (project-level quality)
├── /refactor (conditional second pass)
├── /review-test (project-level quality)
├── /review-doc (project-level quality)
└── /review-release (project-level quality)
```
