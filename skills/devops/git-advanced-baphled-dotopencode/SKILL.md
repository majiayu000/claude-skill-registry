---
name: git-advanced
description: Advanced Git operations: rebasing, cherry-picking, bisect, history management
category: Git
---

# Skill: git-advanced

## What I do

I provide expertise in advanced Git operations to manage complex version control scenarios. I focus on history management, regression hunting, and clean collaboration workflows.

## When to use me

- When cleaning up a complex feature branch before a pull request
- When hunting for a commit that introduced a bug using bisect
- When moving specific commits between branches using cherry-pick
- When recovering lost work using the reflog

## Core principles

1. **History preservation**: Use rebase to keep a linear history, but avoid changing pushed public history.
2. **Atomic search**: Use bisect to find regression points quickly.
3. **Safety first**: Use the reflog as a safety net for any operation that modifies HEAD.
4. **Fixup discipline**: Use fixup commits to keep work-in-progress clean and easily squashable.

## Patterns & examples

**Interactive rebase:**
Use `git rebase -i HEAD~n` to squash, reword, or reorder the last `n` commits. This is standard before merging any feature branch.

**Git bisect:**
1. Start with `git bisect start`.
2. Mark the current (broken) commit: `git bisect bad`.
3. Mark a known good commit: `git bisect good <hash>`.
4. Git will then check out a commit in the middle for testing. Continue marking `good` or `bad` until the culprit is found.

**Fixup workflow:**
1. Make a small fix for a previous commit.
2. Commit with `git commit --fixup=<hash>`.
3. Later, use `git rebase -i --autosquash <base>` to automatically merge those fixes.

**Selective backporting:**
Use `git cherry-pick <hash>` to apply a specific commit from another branch to your current one.

## Anti-patterns to avoid

- ❌ **Rewriting public history**: Never rebase or squash commits that have already been pushed and shared with other developers.
- ❌ **Force pushing blindly**: Always use `--force-with-lease` when pushing rebased branches to ensure you don't overwrite others' work.
- ❌ **Large rebases**: Avoid rebasing branches with hundreds of commits. Rebase frequently to manage conflicts in small increments.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Git/Git Advanced.md`

## Related skills

- `git-master`: For standard Git workflows and search
- `git-worktree`: For managing multiple branches simultaneously
- `ai-commit`: For atomic commit discipline and attribution
