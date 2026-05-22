---
name: git-workflow
description: Use when the Integrator is performing git operations — committing, branching, merging feature branches, resolving conflicts, managing branch lifecycle, or maintaining commit history. Activates for any git-related work.
version: 1.0.0
---

# Git Workflow Expertise

## When This Applies

Apply this guidance when:
- Creating or managing branches
- Committing and pushing changes
- Merging feature branches into development
- Resolving merge conflicts
- Managing commit history

## Branch Management

### Branch Naming

- Feature branches: `feature/CR-NNN-short-description`
- Hotfix branches: `hotfix/NNN-short-description`
- Keep names lowercase with hyphens
- Always include the CR or issue number

### Branch Lifecycle

```
1. Create:   git checkout -b feature/CR-001-user-auth development
2. Work:     Multiple commits as work progresses
3. Update:   git merge development (keep in sync)
4. Test:     Run ALL tests before final merge
5. Merge:    git checkout development && git merge --no-ff feature/CR-001-user-auth
6. Cleanup:  git branch -d feature/CR-001-user-auth
```

### Keeping Branches Current

Regularly sync feature branches with development:
```
git checkout feature/CR-001-user-auth
git merge development
# Resolve any conflicts
# Run tests to verify
```

## Commit Practices

### Commit Message Format

```
[TASK-NNN] Brief description of what changed

Optional longer description explaining:
- Why this change was made
- What approach was taken
- Any notable decisions
```

### Commit Guidelines

1. **Atomic commits** — Each commit should be one logical change
2. **Meaningful messages** — "Fix bug" is bad; "[TASK-042] Fix null reference in auth token validation" is good
3. **Never commit broken code** — All tests must pass before committing
4. **Reference the task** — Always include the TASK-NNN in the commit message
5. **No merge commits in feature branches** — Use `merge` only when merging to development

### What to Include in a Commit

- Source code changes related to the task
- Related configuration changes
- Updated documentation if behavior changed

### What NOT to Commit

- Debug logging or temporary code
- IDE settings or personal configuration
- Unrelated changes (even if they're improvements)
- Files with secrets, tokens, or credentials

## Merge Conflict Resolution

### Process

1. Identify conflicting files: `git status`
2. For each conflict:
   - Read BOTH sides of the conflict
   - Understand the intent of each change
   - Choose the correct resolution (may be a combination)
   - Remove all conflict markers (`<<<<`, `====`, `>>>>`)
3. Run tests after resolving all conflicts
4. Commit the merge

### Conflict Prevention

- Sync feature branches with development frequently
- Communicate with other roles about shared file changes
- Keep changes focused — large diffs create more conflicts

## Pre-Merge Checklist (feature → development)

1. [ ] All tests pass on the feature branch
2. [ ] Feature branch is up to date with development
3. [ ] No unresolved merge conflicts
4. [ ] Commit messages reference task IDs
5. [ ] No debug code or temporary files
6. [ ] Changes match the task scope (no extras)
7. [ ] Notify Manager after successful merge
