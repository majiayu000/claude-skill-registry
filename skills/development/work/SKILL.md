---
name: work
description: 'Use when implementing from a plan or spec path, a clear build request, or a single settled ticket. Single-unit executor with two caller modes: orchestrated (stops after implementation and local verification, returns a structured result) and standalone (delegates finalization to review-and-ship). Never commits, pushes, or opens a PR. Don''t use for open-ended debugging (use debug), exploration, or read-only research.'
disable-model-invocation: true
---

# Work execution

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Implementation starts from a plan or spec path or a clear build request (not an open-ended bug). |
| Authority | Write named local artifacts only. Never commit, push, or open a PR. Rollback path is VCS. Finalization belongs to a separate finalizer reachable only in standalone mode. |
| Caller mode | Orchestrated or standalone, set by the caller. Orchestrated: a supervisor passes an explicit orchestrated signal. Standalone: invoked directly by a human. The mode governs where execution stops. |
| Side effect (orchestrated) | Implements plan units, runs local verification, returns a structured result. No review, commit, push, or PR. |
| Side effect (standalone) | Implements plan units, runs local verification, then delegates finalization to review-and-ship with explicit delegated authority. |
| Done (orchestrated) | All plan units implemented and locally verified; structured result returned. |
| Done (standalone) | All plan units implemented and locally verified; finalization delegated to review-and-ship. |

## Inputs

- `$ARGUMENTS`: plan path, spec path, or bare work description. Blank to auto-detect the newest implementation-ready code plan in `docs/plans/`. Non-empty string is treated as a path only when it resolves to an existing readable file.
- Plan document (path input resolves to file): read metadata before body.
- Bare prompt (no file resolves): scan work area, assess complexity, route.
- Caller mode signal: orchestrated (from a supervisor) or standalone (from a human).
- Repository test and lint commands: the project's test suite and lint check for the changed surface.

## Procedure

### Phase 0: input triage

1. Route the input following the triage rules in `references/execution-detail.md`: plan document (classify `artifact_readiness`), blank invocation (auto-select newest implementation-ready plan), or bare prompt (scan and assess complexity). Stop on requirements-only, invalid readiness, or ambiguous artifacts. Done when: input is routed to Phase 1 or stopped with a named blocking condition.

### Phase 1: quick start

2. Read plan and clarify (skip if arriving from Phase 0 with a bare prompt). Do not read the whole plan first. Build a section map, then read: metadata, `Goal Capsule`, `Verification Contract`, `Definition of Done`, the `Implementation Units` heading list, and only the active U-ID section plus referenced R/F/AE/KTD excerpts. Note `Execution note`, `Deferred to Implementation`, and `Scope Boundaries` before starting. If anything is unclear, ask clarifying questions now. Do not edit the plan body during execution. Done when: relevant plan sections are read and clarifications are resolved.
3. Setup environment. Determine current and default branch. On a feature branch with an opaque name, suggest renaming. On the default branch, offer new branch, worktree, or explicit permission to work on default. Done when: branch strategy is confirmed.
4. Create task list (skip if Phase 0 routed as Trivial). Derive tasks from implementation units, dependencies, files, test targets, and verification criteria. Preserve U-IDs as prefixes. Carry each unit's `Execution note` and `Patterns to follow`. Use each unit's `Verification` field as the primary done signal. Done when: task list is created with U-ID prefixes and dependencies.
5. Choose execution engine and strategy. Probe the harness for engine availability per `references/execution-detail.md`. Prefer subagents for structured multi-unit plans. Parallelize independent units only after confirming harness isolation capability. Never nest worktrees. Done when: execution engine is selected and dispatch strategy is confirmed.

### Phase 2: execute

6. Task execution loop: for each task in priority order: mark in-progress; read referenced files; check for existing matching work; find similar patterns and existing tests; implement following existing conventions; honor `Execution note` (offensive-first TDD, characterization-first, or pragmatic); add, update, or remove tests; run the System-Wide Test Check from `references/execution-detail.md`; mark the task complete only when that check passes. Done when: the task is implemented and its system-wide check is green.
7. Test continuously: run relevant tests after each behavior-bearing change. Fix failures immediately. Add new tests for new behavior. Done when: tests pass for the current change.
8. Simplify opportunistically: at phase boundaries or when the diff reaches 30 lines, reread the changed units and remove dead branches, repeated logic, tiny one-use wrappers, and special cases the general path can absorb. Preserve observable behavior and rerun changed-path checks. Done when: simplification pass is complete with behavior preserved.
9. Track progress: update the task tracker as tasks complete. Note blockers using plan IDs (U-IDs, R/F/AE IDs); do not invent IDs the plan does not supply. For long-running work, write progress to `local://work-<run-id>-progress.json` so state survives context compaction. Done when: progress is recorded.

### Phase 3: local verification and mode split

10. Run local verification: execute the project's test suite and lint check for the changed surface. Fix failures immediately. Never suppress a check or widen scope to unrelated code. Done when: tests and lint pass for the changed surface.
11. Mode split.
    - Orchestrated mode: stop. Return a structured result containing the implementation summary (units completed), verification results (tests, lint), diff summary (files changed), working-tree state (branch, HEAD), and any residuals or blockers. Do not review, commit, push, or create a PR.
    - Standalone mode: delegate finalization to review-and-ship. Pass explicit delegated shipping authority (`authority: delegated`), the implementation context (branch, diff summary, verification results), and any residuals. review-and-ship owns review, commit packaging, publication classification, checks, push, and PR. Do not ship directly.

## Single-ticket mode

A single settled ticket or spec is the narrow entry of the end-to-end pipeline. Phase 0 routes it here instead of building a multi-unit task list. Read the settled plan or ticket end to end and extract the contract: the behaviour promised, the inputs and outputs that define it, and the seams the plan names for behavioural tests. Then implement the contract in code following existing project conventions, reuse existing patterns rather than introducing new ones, and write behavioural tests at each named seam that verify the contract from the caller's perspective (tests must fail on a plausible bug, not restate the source). Run the project's check suite; fix the implementation, never suppress a check or widen scope to unrelated code.

Never reopen or redesign the plan during single-ticket execution. If the plan is ambiguous, contradictory, or missing a named seam, stop and report the gap; do not infer scope. If the implementation reopens a settled plan decision, revert the overreach and implement only what the plan names. If a named seam has no behavioural test, add it before local verification; do not defer. If scope widens beyond the plan, revert the unrelated changes and keep only the contracted work. Work never commits partial or complete results; the finalizer owns commit packaging. If the procedure cannot reach the done predicate, report the blocker and leave the partial diff for the caller to inspect or revert.

## Failure and recovery
| Failure | Rule |
|---|---|
| Requirements-only plan | Stop. Request implementation-ready plan. |
| Invalid readiness value | Stop. Request plan repair. |
| Non-code or unclassified mode | Stop. Request explicit human decision. |
| Blank invocation, no implementation-ready plan | Stop. Ask for explicit path. |
| Ambiguous plan | Stop. Report the specific gap. Do not guess or redesign. |
| Large work, user declines planning pass | Proceed with task list and execution. |
| Harness isolation unavailable for parallel | Fall back to serial subagents or inline. |
| Contending units in shared workspace | Fall back to serial. |
| Serial unit review diff out of scope | Fix before next unit. |
| Local verification cannot reach green | Report the failure and any partial fix in the structured result (orchestrated) or pass to review-and-ship as a blocker (standalone). Do not ship. |
| Single-ticket plan ambiguous or contradictory | Stop. Report the specific gap. Do not guess or redesign. |
| Single-ticket implementation reopens a settled decision | Revert the overreach. Implement only what the plan names. |
| Named seam has no behavioural test | Add the test before local verification. Do not defer. |
| Single-ticket scope widens beyond the plan | Revert unrelated changes. Keep only the contracted work. |

Partial-result rule: report what is implemented and verified. Never claim done when tests fail. In orchestrated mode, name residuals in the structured result. In standalone mode, pass residuals to review-and-ship.

## Output
- Orchestrated mode: a structured result: implementation summary, verification results, diff summary, working-tree state, and residuals or blockers.
- Standalone mode: implementation and local verification complete; finalization delegated to review-and-ship. The final report comes from review-and-ship.
- Blocked: a terminal yield naming the blocker and what was tried.

Zero commits, pushes, or PRs are attributable to this skill in either mode.
