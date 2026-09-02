---
name: worktree
description: 'Use when a new isolated worktree or branch is requested, or an existing ref or PR needs isolation. Creates or attaches an isolated git worktree the harness can see and reports its exact path and status. Don''t use for remote, credential, publish, deploy, or irreversible changes.'
---

# Worktree isolation

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A new isolated worktree or branch is requested, or an existing ref or PR needs isolation. |
| Authority | reversible-local: write only the worktree directory and a `.worktrees/` gitignore entry; rollback by removing the worktree and reverting that entry. |
| Side effect | Local write: creates or attaches an isolated git worktree and reports its exact path and status. |
| Done | An isolated workspace exists that the harness can see and manage, with no phantom state. |

## Inputs

1. **Ref to isolate** (optional): a PR head, branch, or commit for isolate-existing-ref mode. Omit for new-work mode.
2. **New branch name** (optional): derived from the work description when omitted.
3. **Base branch** (optional): defaults to origin's default branch, else `main`.

## Procedure

1. Determine the mode: if the caller named a ref (PR head, branch, or commit), this is isolate-existing-ref mode; otherwise new-work mode. Do not create a worktree for single-task work that can happen on a branch in the current checkout. Done when: the mode is decided and single-task work is ruled out.
2. Detect existing isolation before creating anything. Compare the resolved absolute git dir against the resolved absolute common git dir: run `git rev-parse --absolute-git-dir` and `(cd "$(git rev-parse --git-common-dir)" && pwd -P)`. If they are equal, this is a normal checkout; continue to step 3. Done when: the isolation state is known (normal checkout, submodule, or already isolated).
3. If the two paths differ, run `git rev-parse --show-superproject-working-tree`. Non-empty output means a submodule; treat it as a normal checkout and continue to step 4. Empty output means the run is already in an isolated worktree: report the worktree path (`git rev-parse --show-toplevel`) and current branch. In new-work mode, proceed in place and stop. In isolate-existing-ref mode, check the named ref out here unless it is already the current branch, then stop. Do not create another worktree. Done when: either already-isolated is handled and stopped, or the normal-checkout/submodule path continues to step 4.
4. Prefer the harness's native worktree primitive (for example Claude Code's `EnterWorktree`, a `/worktree` command, or a `--worktree` flag). Use it and stop. A behind-the-back `git worktree add` creates phantom state the harness cannot see, navigate to, or clean up. Done when: a native tool created the worktree, or no native tool exists and the git fallback is the next step.
5. If no native tool exists and step 2 or 3 found no existing isolation, fall back to manual git worktree creation following `references/git-fallback.md`. Done when: the worktree exists under `.worktrees/` and the harness can see it via the tracked convention.
6. Report the worktree's absolute path and current branch, and confirm the harness can see it (native tool) or that it lives under the tracked `.worktrees/` convention (git fallback). Done when: the path, branch, mode, and creation method are reported.

## Failure and recovery
- Already in an isolated worktree: do not create another. Report the existing path and proceed in place (new-work) or check out the named ref there (isolate-existing-ref).
- Ref already checked out elsewhere: report the existing checkout path; never create a second worktree for the same branch. Let the caller work in place or create a detached worktree at the same commit.
- "Worktree already exists": switch to it (`cd .worktrees/<branch>`) or remove it (`git worktree remove .worktrees/<branch>`) before recreating.
- "Cannot remove worktree: it is the current worktree": `cd` out first, then remove.
- Sandbox or permission error on `git worktree add`: report the failure and ask the user for a blocking decision (work in the current checkout vs stop). Work in the current checkout only on explicit confirmation.
- Non-converged: if isolation cannot be established and no fallback is confirmed, return the blocked result with the exact error and the paths inspected. Never claim the done predicate holds.

## Output
The isolated worktree's absolute path, current branch, mode used (new-work or isolate-existing-ref), and creation method (native tool or git fallback); or the existing worktree path and branch if already isolated.
