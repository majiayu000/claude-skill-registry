---
name: land
description: Merge the current PR and clean up the feature branch
disable-model-invocation: true
---

Merge the current branch's PR and clean up.

Steps:

1. Find the PR for the current branch using `gh pr view`.
2. Merge the PR with `gh pr merge <url> --merge`.
3. Switch to local main: `git checkout main`.
4. Pull remote main into local: `git pull origin main`.
5. Delete the feature branch on local and remote:
   - `git branch -d <branch-name>`
   - `git push origin --delete <branch-name>`
6. Confirm cleanup is complete with `git branch` and `git status`.
