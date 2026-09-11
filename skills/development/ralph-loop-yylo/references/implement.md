<!-- GENERATED DESTINATIONS: edit this canonical source, then run `npm run generate:implementation-contract`. -->
---
description: Implement exactly one assigned Kanban task in its admitted Bolt product worktree and stop after queueing it.
---

# Bolt implementation worker contract

An implementation worker owns one explicitly assigned task. It does not select
other work, mutate the product target, merge, release, deploy, or clean another
task's workspace.

## 1. Resolve and preserve admission

1. Read `AGENTS.md` and the complete assigned task from the canonical controller.
2. Run `yy task start TASK_ID` unless the handoff already contains the matching
   active Bolt task record. Verify the returned worktree, branch, full target ref,
   and exact base SHA before editing; stop on missing or contradictory evidence.
3. Work only in that product worktree. Never edit product files in the controller
   or copy controller ledgers, specs, state, or artifacts into a task worktree.
4. Preserve controller identity and workspace-role checks. Controller checkpoints
   are best-effort local durability warnings after terminal metadata is durable;
   they are not product inputs or lifecycle gates.

## 2. Implement

1. Edit only requested product paths and preserve project sources of truth.
2. Use focused affected tests in the edit loop. Other feature worktrees may run
   concurrently; do not wait for or modify them.
3. Never launch lifecycle-semantic reviewers.
   The managed merge queue is the sole lifecycle-semantic review owner. Candidate
   review is risk-based: low gets zero,
   normal gets at most one, and high gets exactly Reviewer A then Reviewer B on
   one frozen candidate.
4. If blocked, record bounded truthful state and stop without claiming success.

## 3. Queue and hand off

1. Run focused tests, required dangerous-path checks, parity checks, and
   `git diff --check`.
2. Stage only task-owned paths, commit coherently, and leave the worktree clean.
3. Run `yy task preflight TASK_ID` before expensive final validation. Repair any
   admission, generated-output, runtime, or closure refusal while the task is
   still `WORKING`.
4. Run `yy task finish TASK_ID`; it validates the exact preflighted tip and
   records `QUEUED` with its immutable review-ready closure.
5. Record the commit and bounded response in Kanban. A lifecycle finalizer may
   attempt a controller checkpoint after terminal metadata is durable; checkpoint
   failure remains a warning and must not change the task or merge outcome.

Stop after queueing. Read-only delivery observation uses `yy merge status` or
`yy merge arbiter status`. One fenced target owner runs `yy merge arbiter run`
(or typed `yy merge drive`) through the expected-SHA CAS gate and exits when idle
or blocked; implementation agents
do not poll, steal on timeout, discard dirty bytes, or invoke `next|resolve`
except under explicit recovery authority. The merge owner applies the bounded
risk-based review sequence and permits at most one repair candidate. A second
material finding terminalizes as `REVIEW_FINDINGS_EXHAUSTED`.

Release-version changes use this same ordinary task/merge lifecycle. Package
preparation is maintainer-only and outside `yy`. Never create a tag, push,
publish, deploy, mutate production, restart services, run post-deploy E2E, or
clean worktrees without separate authority.
