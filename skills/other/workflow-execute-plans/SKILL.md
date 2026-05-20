---
name: workflow-execute-plans
description: "Execute written implementation plans: first read and critically review the plan, then implement in small batches (default 3 tasks), produce verification evidence per batch and pause for feedback; must stop immediately and ask for help when blocked/tests fail/plan unclear. Trigger words: execute plan, implement plan, batch execution, follow the plan."
---

# Executing Plans (Batch Execution + Checkpoints)

## Goal

Reliably turn a "written plan file" into implementation results, avoiding drift or accumulated risk from doing everything at once.

**Core strategy: Batch execution + pause for feedback after each batch.**

## Input/Output (Recommended for Chaining)

Input (pass paths only):
- `plan_path`: Plan file (usually in `run_dir/03-plans/`)
- `repo_root`
- `run_dir`

Output (persisted):
- Plan execution status: `logs/state.json` (or `03-plans/<plan>-status.md`)
- Per-batch verification evidence: append to the corresponding plan file or `05-final/` summary

## Execution Flow

### Step 1) Read and Review Plan (Critical Review First)

1. Read `plan_path`
2. Review if the plan has these issues:
   - Missing dependencies (packages to install/env vars/external services)
   - Task granularity too large (can't verify, hard to rollback)
   - Missing acceptance criteria or verification commands
   - Obviously wrong task ordering
3. If critical issues found: **Stop first**, present concerns as 1-3 bullet points, let human confirm before starting execution.

> Rule: Don't "guess while doing". Clarify when plan is unclear.

### Step 2) Batch Execution (Default 3 Tasks per Batch)

Execute the first 3 tasks from the plan, then stop and report.

For each task:
1. Mark as `in_progress`
2. Execute strictly per plan (don't expand scope)
3. Run verification per plan (tests / build / typecheck / lint / manual verification steps)
4. Mark as `completed`

**Status recording (choose one, prefer structured):**
- Update task status in `logs/state.json`
- Or maintain checklist in `plan_path` (`[ ]`→`[x]`), recording verification results alongside

### Step 3) Batch Report (Must Pause for Feedback)

After each batch, report three things:
- **What changed**: Which files changed/what was implemented (brief)
- **Verification**: What verification was run, what were the results (key info only, no long logs)
- **Next batch**: Which 3 tasks are next

Optional but recommended:
- Use `review-merge-readiness` for a conclusive review on this batch (especially for cross-module changes, risky changes, or approaching merge)

Last line must be:
> Ready for feedback.

Then wait for human feedback—don't automatically continue to next batch.

### Step 4) Continue Based on Feedback

- If feedback requests changes: fix first, re-verify, then continue next batch
- If feedback is OK: continue to next batch (still default 3 tasks)

### Step 5) Wrap Up (After All Complete)

When all tasks are complete and verified:
- Run full tests/build (per project conventions)
- Write `05-final/summary.md` (what was done/how verified/risks & rollback/next steps)
- Do a `skill-evolution` **Evolution checkpoint** (3 questions); if user chooses "want to optimize", run `skill-improver` based on this `run_dir` to produce minimal patch suggestions
- If `finishing-a-development-branch` skill exists: follow that skill to complete merge/PR/cleanup options

## When to Stop and Ask for Help (Hard Rules)

Encounter any of these, **stop execution immediately** and report the issue:
- Blocked mid-way (missing dependency, wrong environment, permission issues)
- Tests/verification failed and can't quickly identify the cause
- Plan step unclear (can't determine correct implementation approach)
- Action that could cause data loss or wide-ranging side effects appears but plan doesn't include confirmation point

## Remember

- Review plan critically before starting
- Small batch execution (default 3 tasks)
- Every batch requires verification and reporting, then wait for feedback
- When blocked, stop—don't guess
