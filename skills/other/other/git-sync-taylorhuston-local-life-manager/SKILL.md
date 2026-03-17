---
name: git-sync
description: "Sync all git repos - my-life top repo and spaces/ projects"
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob, Bash
---

# /git-sync

Synchronize all git repositories: the top-level `my-life` repo and the `spaces/` projects.

## Usage

```bash
/git-sync              # Check status of all repos and branches
/git-sync --pull       # Pull updates for all branches
/git-sync --push       # Push local commits for all branches
/git-sync --clone      # Clone missing repos
```

## Implementation

This skill uses a Python script for reliable validation:

```bash
python .claude/skills/git-sync/scripts/sync.py --check   # Status report
python .claude/skills/git-sync/scripts/sync.py --pull    # Pull behind branches
python .claude/skills/git-sync/scripts/sync.py --push    # Push ahead branches
python .claude/skills/git-sync/scripts/sync.py --clone   # Clone missing repos
python .claude/skills/git-sync/scripts/sync.py --json    # JSON output
python .claude/skills/git-sync/scripts/sync.py --suggest-additions  # YAML for untracked repos
```

Run the script from the my-life repo root directory.

## What It Validates

### Top-Level Repo (my-life)
- Branch status (ahead/behind/dirty/diverged)
- Uncommitted changes
- Sync status with remote

### Index → Filesystem
- Each project with `code:` path exists in spaces/
- Git remote matches `remote:` in index
- Branch status (ahead/behind/dirty/diverged)

### Filesystem → Index
- Finds repos in spaces/ not listed in CLAUDE.md
- Suggests YAML to add them with `--suggest-additions`

## Report Format

```
============================================================
GIT SYNC REPORT
============================================================

## Top-Level Repo (my-life)

  my-life (1 branch)
    ✓ main - Up to date

## Issues

  missing-repo
    Status: missing
    Directory does not exist
    Remote: https://github.com/user/repo.git

## Repositories

  coordinatr (2 branches)
    ✓ main - Up to date
    ↑ feature/001 - 3 commits to push

  yourbench (1 branch)
    ! main - 2 uncommitted files

## Not in Index

  ? django-tutorial
    Path: spaces/django-tutorial
    Remote: https://github.com/user/django-tutorial.git

------------------------------------------------------------
SUMMARY
------------------------------------------------------------
  Top-level repo:   1 (main: up to date)
  Indexed repos:    15 (14 ok, 1 missing)
  Remote-only:      6
  Not in index:     2

  Branches ahead:   1
  Branches behind:  0
  Branches dirty:   1
  Branches diverged:0
  Local-only:       0
```

## Status Symbols

| Symbol | Meaning |
|--------|---------|
| ✓ | Up to date |
| ↓ | Behind remote (can pull) |
| ↑ | Ahead of remote (can push) |
| ↕ | Diverged (manual merge needed) |
| + | Local only (no remote tracking) |
| ? | Not in index |
| ! | Dirty (uncommitted changes) |
| ✗ | Error (check manually) |

## Safety

- **Never force push** - if diverged, report and let user handle
- **Never auto-commit** - dirty repos are reported, not modified
- **Fetch before status** - ensure latest remote info
- **Fast-forward only** - pulls fail safely if not fast-forward
- **Skip dirty branches** - don't pull if uncommitted changes

## Adding Repos to Index

Use `--suggest-additions` to get YAML:

```bash
python .claude/skills/git-sync/scripts/sync.py --suggest-additions
```

Output:
```yaml
# Add to CLAUDE.md Projects Index:

  - name: django-tutorial
    code: spaces/django-tutorial/
    remote: https://github.com/user/django-tutorial.git
    branch: main
    status: active  # or: on-hold, archived, experiment
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Clone fails | Check network, SSH keys, permissions |
| Remote mismatch | Update CLAUDE.md or fix remote |
| Diverged branches | Manual merge/rebase required |
| Missing remote | Repo may be local-only, skip sync |
