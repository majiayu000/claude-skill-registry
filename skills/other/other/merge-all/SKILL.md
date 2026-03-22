---
name: merge-all
description: Merge all open PRs into main with testing between each
user-invocable: true
disable-model-invocation: true
---
Merge all open PRs into main, testing between each merge.

1. List open PRs with `gh pr list`. Include PRs from Claude agents and the repo owner.
2. For each PR, in order by PR number:
   a. Check mergeable status. If conflicts exist, stop and report — do not force merge.
   b. Merge with `gh pr merge N --merge --delete-branch`.
   c. Pull to local main: `git pull origin main`.
   d. Run full test suite: `.\tests\test.ps1 --live`
   e. If tests **fail**: stop immediately, report which PR broke tests and what failed. Do not proceed to the next PR.
   f. If tests **pass**: clean up the local worktree if one exists for this branch (`git worktree remove .claude/worktrees/<name>` then `git branch -d <branch>`). Continue to next PR.
3. After all PRs merged and all tests green, `git push origin main`.
4. Report summary: how many PRs merged, worktrees cleaned, any issues encountered.

If there are no open PRs, just say so.
