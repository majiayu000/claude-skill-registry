---
name: bl-sync
description: Sync git-branchless stack with main branch - fetch, rebase, and handle merges
argument-hint: "[--pull] [--after-merge]"
---

# /bl-sync - Git-Branchless Stack Sync

**Category:** Git Workflow

Sync your commit stack with the main branch. Fetches remote changes, rebases your stack, and handles post-merge cleanup.

## Usage

```
/bl-sync [options]
```

## Options

| Option | Description |
|--------|-------------|
| (none) | Sync with local main branch |
| `--pull` | Fetch remote + sync with updated main |
| `--after-merge` | Clean up after a PR was merged |

## Examples

```bash
# Sync with local main
/bl-sync

# Fetch and sync (most common)
/bl-sync --pull

# After your PR was merged on GitHub
/bl-sync --after-merge
```

## Execution

This command delegates to the `bl-sync-expert` agent:

```
Task(subagent_type="git-workflow:bl-sync-expert",
     prompt="Execute sync: <options>")
```

## Execution Instructions

1. **Verify Prerequisites**
   - Check git-branchless is installed
   - Check working directory is clean

2. **Show Current State**
   - Run `git sl` to display the stack
   - Show divergence from main if any

3. **Execute Sync**
   - For basic sync: `git sync`
   - For pull + sync: `git sync --pull`
   - For after-merge: `git pull origin main` then `git move`

4. **Handle Conflicts**
   - Show conflicting files
   - Guide through resolution
   - Continue with `git rebase --continue`

5. **Remind About PRs**
   - If branches exist, suggest `git submit` to update PRs

6. **Confirm Result**
   - Show final state with `git sl`

## Interactive Flow

```
User: /bl-sync --pull

Agent: Fetching and syncing with main...

Fetching from origin...
remote: Counting objects: 5, done.

Current stack:
◆ old-main (main) old commit
┃
◯ abc123 feat: add User class
┃
● def456 feat: add validation

Syncing onto updated main...
[1/2] feat: add User class - ✓
[2/2] feat: add validation - ✓

◆ new-main (main) teammate's feature  ← Updated
┃
◯ xyz789 feat: add User class
┃
● uvw012 feat: add validation

Stack synced! 2 commits rebased onto updated main.

Note: Run `git submit` to update your PRs.
```

```
User: /bl-sync --after-merge

Agent: Cleaning up after PR merge...

Pulling latest main...
Already up to date with merge commit.

Current state:
◆ merge123 (main) Merge pull request #1
┃
✕ old-abc feat: add User class (merged)
┃
◯ def456 feat: add validation  ← Needs moving
┃
● ghi789 feat: add repository

Moving remaining commits onto merge...
git move -s def456 -d merge123

◆ merge123 (main) Merge pull request #1
┃
◯ new-def feat: add validation  ← Moved
┃
● new-ghi feat: add repository

Cleanup complete!

Next steps:
1. Recreate branch: git switch -c pr/validation
2. Push to remote: git submit -c @
3. Update PR base branch on GitHub
```

```
User: /bl-sync --pull
(with conflicts)

Agent: Fetching and syncing with main...

Syncing onto updated main...
[1/2] feat: add User class - ✓
[2/2] feat: add validation - CONFLICT

Conflict in: src/validation.py

<<<<<<< HEAD
def validate_email(email):
    # teammate's version
=======
def validate_email(email):
    # your version
>>>>>>> feat: add validation

To resolve:
1. Edit src/validation.py - choose correct version
2. git add src/validation.py
3. git rebase --continue

Or to abort: git rebase --abort
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Dirty working directory | Prompt to commit or stash |
| No remote configured | Suggest `git remote add origin <url>` |
| Conflicts during sync | Guide through resolution |
| Lost commits | Use `git undo -i` to recover |
