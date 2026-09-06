---
name: git-cleanup
description: 'Use when the user explicitly invokes branch or worktree cleanup for a repo with accumulated local branches. Don''t use for remote branch deletion or force-push operations.'
disable-model-invocation: true
---

# Git cleanup

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user explicitly invokes branch/worktree cleanup for a repository with accumulated local branches or worktrees. |
| Authority | Reversible local: writes only VCS-tracked local branches and clean worktrees; rollback is git reflog and remote refs. No remote mutation. Show the exact set before any deletion. |
| Side effect | Delete confirmed local git branches and clean worktrees only; dirty worktrees and protected branches are refused. |
| Done | Every local branch is categorized or surfaced as unanalyzed, every recommended deletion has evidence, exact quoted commands receive final confirmation, and each command is reported as deleted or failed. |

## Inputs

A local git repository path (defaults to the current working directory). No remote credentials, no force-push targets, no protected-branch list beyond the repository's own configuration. The user supplies final confirmation for each deletion command; nothing is deleted without it.

## Procedure

1. Run `git branch -vv` and `git worktree list` to enumerate every local branch and worktree. Record the current branch and the default upstream branch as protected; never propose their deletion. Done when: every local branch and worktree is enumerated and the current branch plus default upstream are marked protected.
2. For each local branch, determine merge status against its upstream and against the current branch: run `git branch --merged` and `git branch --no-merged`, then `git log <branch> --not <upstream> --oneline` to surface unmerged commits. Categorize each branch as `merged`, `unmerged-with-evidence`, or `unanalyzed` when the upstream is missing or the comparison is ambiguous. Done when: each branch carries one of `merged`, `unmerged-with-evidence`, or `unanalyzed` with its evidence.
3. For each worktree, run `git -C <path> status --porcelain` to classify it as `clean` or `dirty`. Mark dirty worktrees as refused for deletion. Done when: every worktree is classified `clean` or `dirty`.
4. For every branch or clean worktree recommended for deletion, attach the evidence that justifies it: the merge commit SHA, the empty `git log` output proving no unique commits, or the worktree's clean status. Branches categorized `unanalyzed` are surfaced with their reason and never recommended for deletion. Done when: each recommended deletion has its evidence attached and no `unanalyzed` branch is recommended.
5. Present the full categorized list and, for each recommended deletion, the exact quoted command the user must confirm (for example `git branch -d <name>` or `git worktree remove <path>`). Do not execute any command yet. Done when: the categorized list and every recommended deletion's exact quoted command are shown, with nothing executed.
6. Wait for explicit human confirmation of each exact quoted command. Refuse to batch, abbreviate, or infer confirmation. Done when: the user confirms each exact quoted command individually, or declines.
7. Execute only the confirmed commands, one at a time, in the order confirmed. After each command, record whether it succeeded (`deleted`) or failed, capturing the exact git error message. Done when: each confirmed command ran and is recorded `deleted` or `failed` with its git error message.
## Failure and recovery
- `Dirty worktree`: refuse deletion, report the uncommitted changes, and stop. The user must commit, stash, or discard changes before retrying.
- `Protected branch`: refuse deletion, name the branch, and stop. Protected branches are the current branch, the default upstream, and any branch the repository marks protected.
- `Unanalyzed branch`: surface the branch with its reason (missing upstream, ambiguous merge comparison) and never delete it. Deletion requires the user to resolve the ambiguity and re-invoke.
- `Command failure`: record the exact git error, leave all other confirmed commands pending, and report the failure. Do not retry automatically or widen scope.
- `Missing confirmation`: stop before execution. No deletion occurs. Partial results are the categorized analysis only; no branch or worktree is removed without per-command confirmation.
- Recovery for an accidental deletion is `git reflog` and `git branch <name> <sha>` for branches, or re-adding a worktree with `git worktree add`; state this recovery path when reporting any deletion.

## Output
A categorized report of every local branch (`merged`, `unmerged-with-evidence`, `unanalyzed`, or `protected`) and every worktree (`clean`, `dirty`, or `protected`), each recommended deletion with its evidence and exact quoted command, the set of confirmed commands, and a per-command result of `deleted` or `failed` with the git error message. Branches or worktrees never confirmed remain listed as not deleted.
