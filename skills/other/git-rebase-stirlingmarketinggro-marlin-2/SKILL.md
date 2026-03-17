---
name: git-rebase
description: Performs git rebases with intelligent conflict resolution through commit message analysis. This skill should be used when rebasing branches, updating feature branches with latest main/master, resolving rebase conflicts, cleaning up commit history with interactive rebase, or when the user mentions "rebase", "squash commits", "update my branch", or has merge/rebase conflicts to resolve.
---

# Git Rebase Assistant

Performs safe, effective rebases with intelligent conflict detection and resolution. The key differentiator is **understanding the intent of both sides** through commit message analysis before resolving any conflicts.

## Core Principle: Intent Before Resolution

**Never resolve a conflict mechanically.** Before touching any conflict:

1. Understand what master/main changed and WHY
2. Understand what the feature branch changed and WHY
3. Only then decide how to combine the changes

## Workflow Decision Tree

```
User request
    │
    ├─► "rebase", "update branch", "get latest main"
    │       └─► Full Rebase Workflow (below)
    │
    ├─► Conflict during rebase
    │       └─► Conflict Resolution Workflow (below)
    │
    └─► "squash", "clean up commits", "interactive rebase"
            └─► Interactive Rebase Workflow (below)
```

## Full Rebase Workflow

### Step 1: Validate Prerequisites

```bash
git status                    # MUST be clean
git fetch origin              # Get latest
git branch --show-current     # Confirm correct branch
```

**Stop if**: uncommitted changes exist, wrong branch, or detached HEAD.

### Step 2: Create Safety Backup

```bash
git branch backup/$(git branch --show-current)-$(date +%Y%m%d-%H%M%S)
```

### Step 3: Gather Full Context (MANDATORY)

Run `scripts/rebase-context.sh` or manually gather:

```bash
# What's NEW in main since we branched?
git log --oneline HEAD..origin/main

# What are OUR commits?
git log --oneline origin/main..HEAD

# Files likely to conflict
git diff --name-only origin/main...HEAD

# Preview specific file changes on BOTH sides
git log -p origin/main..HEAD -- <file>   # Our changes to file
git log -p HEAD..origin/main -- <file>   # Their changes to file
```

**Read the commit messages.** Understand:
- What problems were solved in main?
- What new patterns/APIs were introduced?
- What assumptions might have changed?

### Step 4: Execute Rebase

```bash
git rebase origin/main           # Standard
git rebase -i origin/main        # Interactive (for squashing/reordering)
```

### Step 5: Handle Conflicts

See **Conflict Resolution Workflow** below.

### Step 6: Verify and Push

```bash
# Run tests/build
npm test        # or go test ./... or appropriate test command

# Verify log looks correct
git log --oneline -10

# Safe force push
git push --force-with-lease
```

### Step 7: Clean Up

```bash
git branch -d backup/<branch-name>-*
```

## Conflict Resolution Workflow

### Before Resolving ANY Conflict

**Read `references/conflict-analysis.md` for detailed guidance.**

For each conflicted file:

```bash
# 1. See the conflict
git diff --name-only --diff-filter=U    # List conflicted files

# 2. Understand THEIR side (what main added)
git log -p ORIG_HEAD..origin/main -- <conflicted-file>

# 3. Understand OUR side (what we're replaying)
git log -p origin/main..ORIG_HEAD -- <conflicted-file>
```

### Resolution Strategies

| Situation | Action |
|-----------|--------|
| Main refactored shared code | Adapt our changes to new structure |
| Main added new feature | Integrate with our changes |
| Main fixed bug we also fixed | Evaluate which fix is better |
| Main changed API signature | Update our code to use new API |
| Both added similar code | Combine, avoiding duplication |

### The Ours/Theirs Trap

**Read `references/ours-vs-theirs.md` - this is critical.**

During rebase, the meaning is REVERSED from merge:
- `--ours` = the base branch (main)
- `--theirs` = your commits being replayed

```bash
# Accept main's version (during rebase)
git checkout --ours <file>

# Accept our feature branch version (during rebase)
git checkout --theirs <file>
```

### After Each Resolution

```bash
git add <resolved-files>
git rebase --continue

# Run tests after EACH commit if possible
git rebase -i --exec "npm test" origin/main
```

## Interactive Rebase Workflow

For squashing, reordering, or editing commits:

```bash
git rebase -i origin/main     # Rebase onto main
git rebase -i HEAD~5          # Edit last 5 commits
```

### Interactive Commands

| Command | Use When |
|---------|----------|
| `pick` | Keep commit as-is |
| `reword` | Change commit message only |
| `edit` | Stop to amend commit |
| `squash` | Combine with previous, edit combined message |
| `fixup` | Combine with previous, discard this message |
| `drop` | Remove commit entirely |

### Squashing Best Practice

When squashing multiple commits:
1. Read ALL commit messages being combined
2. Craft a new message that captures the full intent
3. Don't just keep the first message if others add context

## Recovery

```bash
# Abort current rebase
git rebase --abort

# Restore from backup
git reset --hard backup/<branch-name>-*

# Find lost commits via reflog
git reflog
git reset --hard HEAD@{n}
```

## Advanced Techniques

### Autosquash Workflow

```bash
# During development, create fixup commits
git commit --fixup=<commit-hash>

# Later, autosquash during rebase
git rebase -i --autosquash origin/main
```

### Run Tests After Each Commit

```bash
git rebase -i --exec "npm test" origin/main
```

### Preserve Merge Commits

```bash
git rebase --rebase-merges origin/main
```

### Enable Rerere (Reuse Recorded Resolution)

```bash
git config --global rerere.enabled true
```

Git remembers conflict resolutions and auto-applies them next time.

## Resources

### scripts/

- `rebase-context.sh` - Gathers context from both sides before rebase

### references/

- `conflict-analysis.md` - Deep dive on understanding conflict intent
- `ours-vs-theirs.md` - Explains the confusing reversal during rebase
