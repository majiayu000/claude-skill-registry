---
name: ru
description: "Repo Updater - automation-friendly CLI for synchronizing GitHub repositories. Keep dozens or hundreds of repos in sync with a single command. Pure Bash with git plumbing, JSON output, meaningful exit codes, parallel sync, and conflict resolution."
---

# RU - Repo Updater

A beautiful, automation-friendly CLI for synchronizing GitHub repositories. Clone missing repos, pull updates, detect conflicts, and get actionable resolution commands—all in a single command.

## Why Use RU

| Without ru | With ru |
|------------|---------|
| `cd` into each of 47 directories and `git pull` | One command syncs everything |
| Forget which repos exist locally vs remotely | Automatically clones missing repos |
| Wonder if your local branch diverged | Clear status: behind, ahead, diverged, conflict |
| Google the right git commands for conflicts | Copy-paste resolution commands provided |
| Manual process breaks when network fails | Meaningful exit codes + `--resume` for restarts |

---

## Quick Reference for AI Agents

### Pre-Flight Check

```bash
# System diagnostics
ru doctor

# Check for updates
ru self-update --check
```

### The Core Workflow

```bash
# 1. Initialize config (first time only)
ru init

# 2. Add repos to sync
ru add owner/repo
ru add owner/repo@develop              # Pin to branch
ru add owner/repo as custom-name       # Custom local name

# 3. Sync everything
ru sync

# 4. Check status (read-only)
ru status
```

### Automation Mode

```bash
# JSON output for scripting
ru sync --json 2>/dev/null | jq '.summary'

# Non-interactive for CI
ru sync --non-interactive --json

# Dry run (show what would happen)
ru sync --dry-run
```

---

## Command Reference

### `ru sync` — Clone and Pull Repos

The primary command. Clones missing repos and pulls updates for existing ones.

```bash
# Basic sync
ru sync

# Clone only (skip pull)
ru sync --clone-only

# Pull only (skip clone)
ru sync --pull-only

# Use rebase instead of merge
ru sync --rebase

# Auto-stash local changes
ru sync --autostash

# Parallel sync (faster for many repos)
ru sync --parallel 4
ru sync -j 8

# Custom projects directory
ru sync --dir /path/to/projects

# Preview without making changes
ru sync --dry-run

# Network timeout for slow connections
ru sync --timeout 60

# Resume interrupted sync
ru sync --resume

# Discard interrupted state and start fresh
ru sync --restart
```

**Ad-hoc sync** (without adding to config):
```bash
ru sync owner/repo1 owner/repo2
ru sync https://github.com/owner/repo
```

### `ru status` — Check Repo Status

Read-only check of all configured repos.

```bash
# Fetch remotes and show status (default)
ru status

# Skip fetch, use cached state
ru status --no-fetch

# JSON output
ru status --json
```

### `ru add` / `ru remove` — Manage Repo List

```bash
# Add to public list (default)
ru add owner/repo

# Add to private list
ru add owner/repo --private

# Add from current directory's git remote
ru add --from-cwd

# Remove from all lists
ru remove owner/repo

# Remove from specific list
ru remove owner/repo --public
ru remove owner/repo --private
```

### `ru list` — Show Configured Repos

```bash
# Show all repos
ru list

# Filter by visibility
ru list --public
ru list --private

# Show local paths instead of URLs
ru list --paths

# JSON output
ru list --json
```

### `ru prune` — Manage Orphan Repos

Detect repos in your projects directory that aren't in your config.

```bash
# List orphans (dry run)
ru prune

# Archive orphans (non-destructive)
ru prune --archive

# Delete orphans (requires confirmation)
ru prune --delete

# Non-interactive delete
ru --non-interactive prune --delete
```

### `ru init` — Initialize Configuration

```bash
# Create config directory and files
ru init

# Include example repos
ru init --example
```

### `ru doctor` — System Diagnostics

```bash
ru doctor
```

**Checks:**
- Git installation and version
- GitHub CLI (gh) installation and auth status
- Config directory existence
- Repo count
- Projects directory permissions
- Optional tools: gum, flock

### `ru self-update` — Update ru

```bash
# Update to latest version
ru self-update

# Check for updates only
ru self-update --check
```

### `ru config` — Configuration Management

```bash
# Print all config values
ru config --print

# Set a value
ru config --set LAYOUT=owner-repo
ru config --set PARALLEL=4
ru config --set AUTOSTASH=true
```

---

## Repo Spec Syntax

Flexible format for specifying repositories:

```
<url_or_shorthand>[@<branch>] [as <local_name>]
```

| Spec | URL | Branch | Local Name |
|------|-----|--------|------------|
| `owner/repo` | github.com/owner/repo | (default) | `repo` |
| `owner/repo@develop` | github.com/owner/repo | `develop` | `repo` |
| `owner/repo as myrepo` | github.com/owner/repo | (default) | `myrepo` |
| `owner/repo@v2 as stable` | github.com/owner/repo | `v2` | `stable` |
| `git@github.com:o/r.git` | git@github.com:o/r.git | (default) | `r` |

**Supported URL formats (all equivalent):**
```
https://github.com/owner/repo
https://github.com/owner/repo.git
git@github.com:owner/repo.git
github.com/owner/repo
owner/repo
```

---

## Path Layouts

Configure how repos are organized locally:

| Layout | Input | Local Path |
|--------|-------|------------|
| `flat` (default) | `owner/repo` | `/data/projects/repo` |
| `owner-repo` | `owner/repo` | `/data/projects/owner/repo` |
| `full` | `owner/repo` | `/data/projects/github.com/owner/repo` |

```bash
# Set layout
ru config --set LAYOUT=owner-repo
```

**Path Collision Warning:** With `flat` layout, different owners with same repo name collide. Use `owner-repo` or custom names.

---

## Configuration

### Directory Structure

```
~/.config/ru/
├── config                    # Main configuration
└── repos.d/
    ├── public.txt            # Public repos
    └── private.txt           # Private repos

~/.local/state/ru/
├── logs/
│   ├── YYYY-MM-DD/
│   │   ├── run.log           # Main log
│   │   └── repos/
│   │       └── *.log         # Per-repo logs
│   └── latest -> YYYY-MM-DD  # Symlink
├── sync_state.json           # Resume state
└── archived/                 # Orphan repos (from prune)
```

### Config File Options

```bash
# ~/.config/ru/config

# Base directory for repositories
PROJECTS_DIR=/data/projects

# Directory layout: flat | owner-repo | full
LAYOUT=flat

# Update strategy: ff-only | rebase | merge
UPDATE_STRATEGY=ff-only

# Auto-stash local changes before pull
AUTOSTASH=false

# Parallel operations (1 = serial)
PARALLEL=1

# Network timeout in seconds
TIMEOUT=30

# Check for ru updates on run
CHECK_UPDATES=false
```

### Config Priority

1. Command-line arguments (`--dir`, `--rebase`, etc.)
2. Environment variables (`RU_PROJECTS_DIR`, `RU_LAYOUT`, etc.)
3. Config file (`~/.config/ru/config`)
4. Built-in defaults

---

## JSON Output

Use `--json` for structured output:

```bash
ru sync --json 2>/dev/null
```

```json
{
  "version": "1.0.0",
  "timestamp": "2025-01-03T14:30:00Z",
  "duration_seconds": 154,
  "config": {
    "projects_dir": "/data/projects",
    "layout": "flat",
    "update_strategy": "ff-only"
  },
  "summary": {
    "total": 47,
    "cloned": 8,
    "updated": 34,
    "current": 3,
    "conflicts": 2,
    "failed": 0
  },
  "repos": [
    {
      "name": "mcp_agent_mail",
      "path": "/data/projects/mcp_agent_mail",
      "action": "pull",
      "status": "updated",
      "duration": 2
    }
  ]
}
```

### jq Quick Reference

```bash
# Get paths of cloned repos
ru sync --json 2>/dev/null | jq -r '.repos[] | select(.action=="clone") | .path'

# Count failures
ru sync --json 2>/dev/null | jq '.summary.failed'

# List conflicts
ru sync --json 2>/dev/null | jq -r '.repos[] | select(.status=="conflict") | .name'

# Get summary
ru sync --json 2>/dev/null | jq '.summary'
```

---

## Exit Codes

| Code | Meaning | When |
|------|---------|------|
| `0` | Success | All repos synced or already current |
| `1` | Partial failure | Some repos failed (network/auth/remote error) |
| `2` | Conflicts exist | Some repos have unresolved conflicts |
| `3` | Dependency error | gh CLI missing, auth failed, etc. |
| `4` | Invalid arguments | Bad CLI options, missing config files |
| `5` | Interrupted | Sync interrupted; use `--resume` to continue |

### CI Usage

```bash
#!/bin/bash
ru sync --non-interactive
exit_code=$?

case $exit_code in
    0) echo "All repos synchronized successfully" ;;
    1) echo "Some repos failed - check logs" ;;
    2) echo "Conflicts detected - manual resolution required" ;;
    3) echo "Missing dependencies - run 'ru doctor'" ;;
    4) echo "Invalid configuration" ;;
    5) echo "Sync interrupted - run 'ru sync --resume'" ;;
esac
```

---

## Parallel Sync

Sync multiple repos concurrently for faster updates:

```bash
# Sync 4 repos at a time
ru sync --parallel 4

# Short form
ru sync -j 8

# Set default in config
ru config --set PARALLEL=4
```

**How it works:**
- Worker pool with flock-based coordination
- Aggregated results in unified summary
- Falls back to serial if flock unavailable

**Requirements:** `flock` (Linux default; `brew install util-linux` on macOS)

---

## Resuming Interrupted Syncs

If sync is interrupted (Ctrl+C, network failure), resume from where you left off:

```bash
# Resume from last checkpoint
ru sync --resume

# Start fresh, discard state
ru sync --restart
```

State saved to `~/.local/state/ru/sync_state.json`.

---

## Conflict Resolution

When ru encounters issues, it provides copy-paste resolution commands:

```
╭─────────────────────────────────────────────────────────────╮
│  ⚠️  Repositories Needing Attention                         │
╰─────────────────────────────────────────────────────────────╯

1. mcp_agent_mail
   Path:   /data/projects/mcp_agent_mail
   Issue:  Dirty working tree (3 files modified)

   Resolution options:
     a) Stash and pull:
        cd /data/projects/mcp_agent_mail && git stash && git pull && git stash pop

     b) Commit your changes:
        cd /data/projects/mcp_agent_mail && git add . && git commit -m "WIP"

     c) Discard local changes (DESTRUCTIVE):
        cd /data/projects/mcp_agent_mail && git checkout . && git clean -fd

2. beads_viewer
   Issue:  Diverged (2 ahead, 5 behind)

   Resolution options:
     a) Rebase your changes:
        cd /data/projects/beads_viewer && git pull --rebase

     b) Merge (creates merge commit):
        cd /data/projects/beads_viewer && git pull --no-ff
```

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Dirty working tree | Uncommitted changes | Stash, commit, or discard |
| Diverged | Local and remote both have commits | Rebase, merge, or push |
| No upstream | Branch doesn't track remote | `git branch --set-upstream-to=origin/main` |
| Remote mismatch | Different repo at same path | Remove directory or update list |
| Auth failed | gh not authenticated | `gh auth login` or set `GH_TOKEN` |

---

## Git Status Detection

ru uses git plumbing for reliable, locale-independent status:

```bash
# NOT this (fragile, locale-dependent):
git pull 2>&1 | grep "Already up to date"

# THIS (robust plumbing):
git rev-list --left-right --count HEAD...@{u}
git status --porcelain
```

### Status States

| State | Ahead | Behind | Meaning |
|-------|-------|--------|---------|
| `current` | 0 | 0 | Fully synchronized |
| `behind` | 0 | >0 | Remote has new commits |
| `ahead` | >0 | 0 | Local has unpushed commits |
| `diverged` | >0 | >0 | Both have new commits |
| `dirty` | — | — | Uncommitted local changes |

---

## NDJSON Results Logging

Per-repo results logged in Newline-Delimited JSON:

```json
{"repo":"mcp_agent_mail","path":"/data/projects/mcp_agent_mail","action":"pull","status":"updated","duration":2,"message":"","timestamp":"2025-01-03T14:30:00Z"}
{"repo":"beads_viewer","path":"/data/projects/beads_viewer","action":"clone","status":"cloned","duration":5,"message":"","timestamp":"2025-01-03T14:30:05Z"}
```

```bash
# Find failures
cat ~/.local/state/ru/logs/latest/results.ndjson | jq -r 'select(.status == "failed") | "\(.repo): \(.message)"'

# Count by status
cat ~/.local/state/ru/logs/latest/results.ndjson | jq -s 'group_by(.status) | map({status: .[0].status, count: length})'
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RU_PROJECTS_DIR` | Base directory for repos | `/data/projects` |
| `RU_LAYOUT` | Path layout (flat/owner-repo/full) | `flat` |
| `RU_PARALLEL` | Number of parallel workers | `1` |
| `RU_TIMEOUT` | Network timeout in seconds | `30` |
| `RU_AUTOSTASH` | Auto-stash before pull | `false` |
| `RU_UPDATE_STRATEGY` | Pull strategy (ff-only/rebase/merge) | `ff-only` |
| `RU_CONFIG_DIR` | Configuration directory | `~/.config/ru` |
| `RU_LOG_DIR` | Log directory | `~/.local/state/ru/logs` |
| `GH_TOKEN` | GitHub token for authentication | (from gh CLI) |
| `CI` | Detected CI environment | unset |

---

## Dependencies

### Required

| Dependency | Version | Purpose |
|------------|---------|---------|
| Bash | 4.0+ | Script runtime |
| git | 2.0+ | Repository operations |
| gh | 2.0+ | GitHub CLI for cloning |
| curl | any | Installation and updates |

### Optional

| Dependency | Purpose |
|------------|---------|
| gum | Beautiful terminal UI |
| jq | JSON processing |
| flock | Parallel sync coordination |

---

## Stream Separation

ru follows Unix conventions:
- **stderr**: Human-readable output (progress, errors, summary)
- **stdout**: Structured data (JSON, paths)

```bash
# Progress shows in terminal, JSON pipes to jq
ru sync --json | jq '.summary'

# Capture only paths
ru sync 2>/dev/null  # stdout = paths
```

---

## Troubleshooting

### Debug Mode

```bash
# View latest run log
cat ~/.local/state/ru/logs/latest/run.log

# View specific repo log
cat ~/.local/state/ru/logs/latest/repos/mcp_agent_mail.log
```

### Common Fixes

| Problem | Solution |
|---------|----------|
| "gh: command not found" | `brew install gh` or `apt install gh`, then `gh auth login` |
| "gh: auth required" | `gh auth login` or set `GH_TOKEN` |
| "Cannot fast-forward" | Use `--rebase` or resolve divergence |
| "dirty working tree" | Use `--autostash` or commit/stash manually |
| Config missing | Run `ru init` |

---

## Ready-to-Paste AGENTS.md Blurb

```
## ru - Repo Updater

ru is an automation-friendly CLI for synchronizing GitHub repositories.
Keep dozens or hundreds of repos in sync with a single command.

### Quick Start
ru doctor                              # Check dependencies
ru init                                # Initialize config
ru add owner/repo                      # Add a repo
ru sync                                # Sync everything
ru status --json                       # Check status

### Key Options
| Flag | Purpose |
|------|---------|
| --json | Structured output for scripting |
| --non-interactive | CI mode (no prompts) |
| --parallel N | Sync N repos concurrently |
| --resume | Continue interrupted sync |
| --dry-run | Preview without changes |

### Exit Codes
0=success, 1=partial fail, 2=conflicts, 3=deps, 4=args, 5=interrupted

stdout = data (JSON/paths), stderr = human output
```

---

## Installation

```bash
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/repo_updater/main/install.sh | bash
```
