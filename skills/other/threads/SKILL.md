---
name: threads
description: Coordinate Codex-native parallel thread workflows for repo issue and PR queues, multi-agent research, implementation worktrees, independent code review, merge gates, and final cleanup. Use when the user says Codex threads, open threads, 开几个 thread, 子agent, 并行, worktree, thread review, review then merge, or asks to plan and execute several issues or PRs in parallel.
---

# Threads

Use this skill to turn a broad request into controlled Codex-native subthreads with explicit lanes, file ownership, review gates, and verifiable closure.

Native Codex threads are short-lived parallel work lines inside the Codex workflow. They are not the same as OMX/tmux workers. If native subagent tools are not visible, discover them with tool search. If no native subagent capability is available, produce the thread prompt pack and execution plan instead of pretending threads were launched.

## Decision

Choose one mode:

- **plan_only**: map issues, PRs, risks, and parallelization without edits.
- **execute_direct**: run one or more bounded implementation lanes after planning.
- **review_only**: launch independent reviewers for PRs, diffs, or risky code.
- **research_spec**: split exploration by angle, then synthesize docs/spec/issues.
- **clarify_first**: ask only when repo, target queue, permission, or done-when is missing.

For any implementation mode, start with a lane map before spawning workers.

## Lane Map

Write a short lane map before dispatch:

```text
mode:
repo:
base_ref:
global_constraints:
verification_owner:
stop_conditions:
lanes:
- id:
  role: planner | worker | reviewer | merge_reviewer | researcher
  target:
  worktree:
  writable_files:
  forbidden_files:
  expected_output:
  verification:
```

Rules:

- Search first: inspect repo state, open issues/PRs, current branch, dirty files, and applicable instructions before assigning work.
- Keep planners and reviewers read-only.
- Give implementation workers disjoint writable paths. Never assign two workers the same writable file.
- Put high-context files such as `AGENTS.md`, `CLAUDE.md`, settings, hooks, and setup scripts in `forbidden_files` unless the user explicitly asks to modify them.
- Prefer existing worktrees when they are already tied to the target branch. Otherwise create clean worktrees from `origin/main` or the requested base.
- Require fresh verification from the worker or the verification owner before claiming success.

## Dispatch

Use native subagents when available. If the multi-agent tool is not loaded, search for it using tool discovery. Do not use shell/tmux/OMX orchestration unless explicitly requested.

Use these lane types:

- **Planner**: read issues/PRs/code and output dependency graph, worktree plan, file ownership, and risk.
- **Worker**: implement the smallest mergeable slice in one worktree; do not merge.
- **Reviewer**: inspect one PR/diff/worktree read-only; return findings first.
- **Fix Worker**: address concrete reviewer findings in the original worker worktree.
- **Merge Reviewer**: independently verify the final head and CI before merge.
- **Researcher**: inspect one external/source angle and return evidence with uncertainty.

Load [prompt-patterns.md](references/prompt-patterns.md) when you need ready-to-use prompts for planners, workers, reviewers, or research lanes.

## Merge Gate

Do not merge from worker output alone. Merge only after:

- The PR/diff has at least one independent review lane.
- Blocking findings are fixed or explicitly ruled out with evidence.
- Required checks are fresh and tied to the current head.
- The final answer can state exact PR numbers, commits, changed files, and verification commands.

If the user asked for “review then merge,” the merge reviewer should be a separate lane from the implementation worker.

## Final Report

End with a compact status table:

```text
completed:
- lane:
  result:
  artifact:
  verification:

merged:
- PR:
  commit:

remaining:
- blocker_or_risk:
  next_action:

local_state:
- dirty_worktree:
- stale_worktree:
- high_context_file:
```

Separate remote truth from local machine state. State when a branch is merged remotely but local main is stale, dirty, or diverged.

## Failure Rules

- If a subthread returns vague output, ask for evidence or redo that lane with a stricter prompt.
- If a worker touches unassigned files, stop that lane and audit before proceeding.
- If three attempts fail on the same problem, stop and challenge the hypothesis or split the issue differently.
- If a hook/UI status looks stuck, verify process/log evidence before calling the task stuck.
- If no native subagent capability is available, return the lane map and exact prompts so the user can launch them manually.
