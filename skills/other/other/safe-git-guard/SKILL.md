---
name: safe-git-guard
description: Prevents destructive Git operations by requiring backup and confirmation. Blocks git reset --hard, git push --force on main, git clean -fd. Requires backup before git checkout, git reset, git rebase. Activate on any destructive git command.
---

# Safe Git Guard

> Skill to prevent destructive Git operations

## Trigger

This skill activates automatically on these commands:

- `git reset --hard`
- `git checkout -- <file>`
- `git clean -fd`
- `git rebase` (without explicit confirmation)
- `git push --force`

## Rules

### FORBIDDEN (never execute):

1. **`git reset --hard`** - Deletes uncommitted changes irreversibly
2. **`git push --force` on main/master** - Can destroy remote history
3. **`git clean -fd`** - Deletes untracked files irreversibly

### WARNING + BACKUP required:

1. **`git checkout -- <file>`** - Overwrites local changes
   - BEFORE execution: Create backup
   - `git stash push -m "backup-before-checkout-$(date +%s)"`

2. **`git reset HEAD~n`** - Resets commits
   - BEFORE execution: Create tag
   - `git tag backup-before-reset-$(date +%s)`

3. **`git rebase`** - Modifies history
   - BEFORE execution: Create backup branch
   - `git branch backup-before-rebase-$(date +%s)`

## Workflow for Destructive Operations

```
1. STOP - Don't execute immediately
2. BACKUP - Save current state (tag/branch/stash)
3. ASK - "Are you sure? What will be lost?"
4. CONFIRM - Explicit "Yes, I understand the risk"
5. EXECUTE - Only then run the command
```

## Example Dialog

**User:** "Undo the last 3 commits"

**Claude (with this skill):**

```
WARNING: DESTRUCTIVE OPERATION DETECTED

You want to run `git reset HEAD~3`. This would:
- Remove 3 commits from history
- Changes become "unstaged" (--soft) or deleted (--hard)

Creating backup:
> git tag backup-YYYYMMDD-pre-reset

Should I proceed? (Answer with "Yes, proceed with reset")
```

## Protected Branches

Configure in your project's CLAUDE.md:

```yaml
protected_branches:
  - main      # Production branch, never force-push
  - master    # Legacy production branch
  - develop   # Development branch, PR only
  - release/* # Release branches, approval only
```

## Integration with No-Touch Zones

This skill respects No-Touch Zones defined in CLAUDE.md.
When changes affect protected files: Additional warning + Impact Analysis.

## Configuration

Add to your CLAUDE.md:

```markdown
### Git Safety Rules

Protected Branches:
- main, develop, release/*

No-Touch Zones (require explicit approval):
- src/auth/**
- src/core/**
- config/production.*
```

---

## Origin

Originally developed for [fabrikIQ](https://fabrikiq.com) - AI-powered manufacturing data analysis.

## License

MIT - Free to use and modify
