---
name: bump-actions
description: Bump GitHub Actions versions for lun. Use this skill when the user wants to update the install-lun action to use a newer lun version, or update the lun action to reference the latest install-lun. Triggers include requests to "bump actions", "update action versions", or "sync action versions".
---

# Bump Actions

Automate bumping the `lun` version in GitHub Actions and keeping `install-lun` references in sync.

## Overview

This skill bumps versions in two actions:

1. **install-lun**: Downloads and installs a specific lun version
2. **lun**: Uses install-lun to install lun and then runs it

The process creates 2-3 commits:

1. First commit: Bump `lun` version in `install-lun/action.yml`
2. Second commit: Bump `install-lun` SHA reference (to HEAD) and `lun` version in `lun/action.yml`
3. Third commit (if needed): Update workflow files that reference the `lun` action to use the new SHA

## Usage

Run the script:

```bash
python3 .claude/skills/bump-actions/scripts/bump_actions.py
```

By default, it fetches the latest release version. To specify a version:

```bash
python3 .claude/skills/bump-actions/scripts/bump_actions.py --version 0.8.0
```

To skip pushing and CI wait (for local testing):

```bash
python3 .claude/skills/bump-actions/scripts/bump_actions.py --no-push
```

## What the Script Does

1. Gets the latest lun release version (or uses `--version`)
2. Updates `install-lun/action.yml` with the new default version
3. Commits: `chore(actions): Bump \`lun\` version to vX.Y.Z`
4. Gets the HEAD SHA (from the commit just made)
5. Updates `lun/action.yml`:
   - Changes the `install-lun@SHA` reference to HEAD
   - Updates the default version to match
6. Commits: `chore(actions): Bump \`install-lun\` version`
7. Gets the new HEAD SHA (from the commit just made)
8. Updates workflow files in `.github/workflows/` that reference `langston-barrett/lun/.github/actions/lun@SHA` to use the new SHA
9. Commits (if workflows were updated): `chore(ci): Update workflows to use new lun action SHA`
10. Pushes and waits for CI to pass using `gh run watch`
