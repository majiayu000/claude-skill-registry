---
name: "commit"
description: "Stage and commit changes in semantic groups. Use when the user wants to commit, organize commits, or clean up a branch before pushing."
---

1. Read `git status --short` first and identify only the files touched by the current task or explicitly requested by the user.
2. Leave unrelated dirty files untouched unless the user explicitly asks for a whole-tree commit.
3. If the tree is mixed, inspect diffs before staging and keep the staged set scoped to one semantic change.
4. Stage files by purpose, not with `git add .`, unless the whole task is intentionally one coherent change.
5. Default to one scoped conventional commit when the task is cohesive. Split into multiple commits only when there are clearly separate semantic groups.
6. When multiple commits are needed, prefer this order: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`.
7. Use short scoped conventional commit messages that match exactly what changed.
8. Keep each commit minimal, reviewable, and scoped to one change type.
9. Run `git status -sb` between groups to confirm the next commit only contains intended files.
10. Stop and ask before staging unrelated user changes, generated churn you do not understand, or a dirty tree that makes ownership ambiguous.
