---
name: ship-develop
description: "Ship the current branch into `develop` with the full GitHub flow: verify repo state, run the right tests, commit if needed, push, create or reuse a PR, request Codex review, address findings until clean, and merge when safe. Use when the user asks to merge the current branch into `develop`, create a PR and let Codex review it, or finish a reviewed PR merge automatically."
---

# Ship Develop

Use this skill to finish the branch shipping workflow end to end instead of stopping at local edits.

For this repository, do not assume the GitHub default branch is `develop`. Verify the target base branch first. At the time this skill was created, the repo default branch is `master`, while `develop` exists as a working integration branch.

## Quick Start

1. Check `git status --short --branch` and confirm what branch you are on.
2. Run tests or validation proportional to the change.
3. If the tree is dirty, create the commit before shipping.
4. For the default flow, run `scripts/ship_develop.py --base develop --codex-review --wait-codex-seconds 300 --wait-seconds 600`.
5. If the script reports `codex-review-findings`, read the PR review comments, fix them, rerun validation, and run the same command again.
6. Use `--require-review` only when the user explicitly wants human approval before merge.

## Workflow

### 1. Verify the branch is really ready

- Read the current diff and make sure there are no unresolved conflicts or unrelated edits.
- Use the existing project rules in `AGENTS.md` before shipping.
- If the branch contains only doc or config changes, use lighter verification and say so explicitly.

### 2. Commit before you ship

- If `git status --porcelain` is non-empty, review the files, stage intentionally, and create a commit.
- Do not run the shipping script against a dirty tree unless you are only doing a dry run.
- Use a concise commit message that reflects the branch delta.

### 3. Use the shipping script

- The script handles:
  - branch and worktree checks
  - push with upstream setup
  - PR create or reuse
  - Codex review request and polling
  - human review gate inspection when requested
  - check status inspection
  - merge when safe after Codex is clean
  - checkout `develop` and delete the local branch after a successful merge
- Preferred command:

```powershell
.\.venv\Scripts\python .agents/skills/ship-develop/scripts/ship_develop.py --base develop --codex-review --wait-codex-seconds 300 --wait-seconds 600
```

### 4. Interpret outcomes conservatively

- If the script reports `codex-review-findings`, inspect the PR review comments from `chatgpt-codex-connector[bot]`, fix them locally, rerun tests, push, and rerun the same command.
- If the script reports `codex-review-pending`, wait and rerun instead of merging blind.
- If checks fail, stop and summarize the failure.
- If human review is required and the PR is not approved yet, stop after PR creation or reuse and report the PR URL.
- If the PR has `CHANGES_REQUESTED` or merge conflicts, stop and report exactly that.
- If checks are still pending and the wait budget expires, return the PR URL and current state instead of guessing.
- If merge succeeds, report the PR URL, merge method, and local branch cleanup result.

## Script Flags

- `--base develop`: target branch
- `--merge-method squash|merge|rebase`: default is `squash`
- `--create-only`: stop after PR creation or lookup
- `--codex-review`: comment `@codex review` on the PR and wait for Codex review status
- `--wait-codex-seconds N`: poll Codex review status for up to `N` seconds
- `--require-review`: require `APPROVED` before merge
- `--wait-review-seconds N`: optionally poll for review state before giving up
- `--wait-seconds N`: poll checks for up to `N` seconds before deciding
- `--interval-seconds N`: polling interval, default `20`
- `--keep-remote-branch`: do not request remote branch deletion during merge
- `--keep-local-branch`: do not switch to base and delete the local branch after merge
- `--dry-run`: print the plan without changing GitHub or Git state
- `--allow-dirty`: only for dry-run or unusual debugging; do not use for normal shipping

## Repo-Specific Notes

- `gh` may not be on `PATH` in this environment. The script already falls back to `C:\Program Files\GitHub CLI\gh.exe`.
- This repo currently has no branch protection on `develop`, so the review gate lives in this script rather than GitHub policy.
- The default practical workflow is iterative:
  - pass 1: create or update the PR, request Codex review, and stop if findings appear
  - middle passes: fix findings, push, request Codex review again
  - final pass: Codex returns clean, checks are green, and the script merges
- Human approval remains an optional second gate when the user explicitly asks for it.
- This repo currently has `delete_branch_on_merge=false`, so local cleanup is handled by the script after a successful merge.

## Done When

- The branch is pushed.
- A PR to `develop` exists or was reused.
- The merge either completed safely or stopped with a concrete reason.
- If merge completed, the workspace is on `develop` and the local feature branch is removed unless the user asked to keep it.
