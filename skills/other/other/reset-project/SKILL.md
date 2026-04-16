---
name: reset-project
description: Restore a project's .claude/ directory to the dotforge template from scratch, with backup and rollback option.
---

# Reset Project

Restore the current project's `.claude/` directory completely to the dotforge template, from scratch.

## Step 1: Confirm with the user (MANDATORY)

Show warning before proceeding:

```
╔══════════════════════════════════════════════════╗
║  RESET: .claude/ will be fully replaced         ║
║                                                  ║
║  The following will be lost:                     ║
║  - Customizations in settings.json               ║
║  - Custom rules                                  ║
║  - Custom hooks                                  ║
║  - Any manually created files in .claude/        ║
║                                                  ║
║  The following will be preserved:                ║
║  - settings.local.json (not touched)             ║
║  - CLAUDE.md (regenerated from template)         ║
║  - CLAUDE_ERRORS.md (preserved if it exists)     ║
║                                                  ║
║  A backup will be created at .claude.backup-YYYY-MM-DD/  ║
╚══════════════════════════════════════════════════╝

Confirm reset? (yes/no)
```

If the user says "no", cancel immediately. DO NOT proceed without explicit confirmation.

## Step 2: Detect stacks

Use detection rules from `$DOTFORGE_DIR/stacks/detect.md`.
Confirm detected stacks with the user.

## Step 3: Create backup

1. Create directory `.claude.backup-{YYYY-MM-DD}/` in the project root
2. Copy ALL of `.claude/` to the backup:
   ```bash
   cp -R .claude/ .claude.backup-$(date +%Y-%m-%d)/
   ```
3. If `CLAUDE_ERRORS.md` exists, copy it separately (it will be restored afterwards)
4. Verify the backup exists and has content

## Step 4: Re-run full bootstrap

1. Delete the current `.claude/`:
   ```bash
   rm -rf .claude/
   ```
2. Run the `/bootstrap-project` skill in full from scratch
3. If `CLAUDE_ERRORS.md` existed, restore the original file (not the empty template)

## Step 5: Show diff between backup and new

Compare backup vs new `.claude/`:

```
═══ RESET COMPLETE ═══

New files (did not exist before):
+ .claude/rules/agents.md
+ .claude/agents/researcher.md

Updated files (differences from backup):
~ .claude/settings.json — 3 new permissions in allow
~ .claude/hooks/block-destructive.sh — 2 new patterns

Deleted files (were in backup, not in template):
- .claude/rules/custom-strategy.md

Preserved files:
= CLAUDE_ERRORS.md (restored from backup)
```

## Step 6: Offer rollback

```
Backup available at: .claude.backup-YYYY-MM-DD/
To restore: rm -rf .claude && mv .claude.backup-YYYY-MM-DD .claude
Delete backup? (yes/no — recommended: no, at least until verified)
```

If the user wants to restore, execute the rollback immediately.
If the user wants to delete the backup, do it.
If the user does not decide, leave the backup (it can be cleaned up manually later).

## Installation

This skill is installed automatically if the symlink from `skills/` already exists in `~/.claude/skills/`. If not, create the symlink:
```bash
ln -sf $DOTFORGE_DIR/skills ~/.claude/skills
```
