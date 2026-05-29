---
name: sync-migrations
description: Use when creating dotfiles migrations for one-time cleanup on existing machines (removing old tools, uninstalling replaced packages, cleaning deprecated files). Also use when a migration fails and user needs help diagnosing or recovering.
---

# Sync Migrations

One-time scripts that run on existing machines when dotfiles changes require cleanup.

## When to Use

**Create migration for:**
- Removing/uninstalling replaced tools (npm → brew)
- Deleting deprecated files/directories
- Cleaning stale symlinks

**Don't create for:**
- Adding new configs (sync handles this)
- Updating existing configs (symlinks auto-update)

## Quick Reference

| Item | Value |
|------|-------|
| Location | `migrations/YYYY-MM-DD-description.sh` |
| Marker | `~/.dotfiles-migration-marker` |

## CLI Flags

| Flag | Description |
|------|-------------|
| `./sync` | Full sync, no migrations |
| `./sync --migrate` | Full sync + run pending migrations at the end |
| `./sync --migrate-only` | Skip sync, run pending migrations only |

## Creating a Migration

```bash
#!/bin/bash
set -e

# Always check before acting (idempotent)
if [ -d ~/.old-thing ]; then
    rm -rf ~/.old-thing
fi

if command -v old-tool &>/dev/null; then
    brew uninstall old-tool
fi
```

**Requirements:**
- Timestamped filename: `YYYY-MM-DD-description.sh`
- `set -e` for fail-fast
- Idempotent checks before each action
- Make executable: `chmod +x`

## How It Works

1. Marker file stores last-run date
2. Migrations with timestamp > marker are pending
3. User confirms before running
4. Marker updates after each success

**New machines:** No marker = all pending. User decides to run or skip (fresh setup doesn't need cleanup).

## Troubleshooting Failures

When a migration fails, help the user recover:

1. **Read the failed migration script** to understand intent
2. **Check the sync log** at `/tmp/dotfiles-sync-*.log` for error details
3. **Diagnose the issue** - missing dependency, permission error, path doesn't exist, etc.
4. **Options:**
   - Fix the issue and re-run: `./sync --migrate-only`
   - Run commands manually, then update marker: `echo "YYYY-MM-DD" > ~/.dotfiles-migration-marker`
   - Skip the migration entirely by advancing the marker past it

**Common failure patterns:**
- `command not found` → tool not installed, check Brewfile ran first
- `permission denied` → may need sudo (sync doesn't have it)
- `No such file` → path changed or doesn't exist on this machine (make script idempotent)

**Recovery example:**
```bash
# Migration 2025-01-10-foo.sh failed
# Fix: run the commands manually
brew uninstall old-thing  # or whatever failed

# Then advance marker so it won't retry
echo "2025-01-10" > ~/.dotfiles-migration-marker
```
