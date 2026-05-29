---
name: spaces-sync
description: "Sync spaces/ directory with Projects Index - clone missing, push/pull all branches"
model: claude-haiku-4-5-20251001
allowed-tools: Read, Glob, Bash
---

# /spaces-sync

Synchronize the `spaces/` directory with the Projects Index in CLAUDE.md.

## Usage

```bash
/spaces-sync              # Check status of all repos and branches
/spaces-sync --pull       # Pull updates for all branches
/spaces-sync --push       # Push local commits for all branches
/spaces-sync --clone      # Clone missing repos
```

## Implementation

This skill uses a Python script for reliable validation:

```bash
python .claude/skills/spaces-sync/scripts/sync.py --check   # Status report
python .claude/skills/spaces-sync/scripts/sync.py --pull    # Pull behind branches
python .claude/skills/spaces-sync/scripts/sync.py --push    # Push ahead branches
python .claude/skills/spaces-sync/scripts/sync.py --clone   # Clone missing repos
python .claude/skills/spaces-sync/scripts/sync.py --json    # JSON output
python .claude/skills/spaces-sync/scripts/sync.py --suggest-additions  # YAML for untracked repos
```

Run the script from the ideas repo root directory.

## What It Validates

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
SPACES SYNC REPORT
============================================================

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
python .claude/skills/spaces-sync/scripts/sync.py --suggest-additions
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
