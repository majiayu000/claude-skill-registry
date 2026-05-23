---
name: ops-claude
description: >
  Claude Code maintenance and diagnostics. Check inotify limits, clean caches,
  diagnose startup failures, and manage skills directories across projects.
allowed-tools: Bash, Read
triggers:
  - claude won't start
  - claude crashes
  - claude out of memory
  - inotify limit
  - file watcher error
  - ENOSPC
  - clean claude cache
  - claude diagnostics
  - ops claude
metadata:
  short-description: Claude Code maintenance and diagnostics
---

# Ops-Claude Skill

Maintenance and diagnostics for Claude Code installations.

## Supported IDEs/CLIs

| IDE | Skills Path | User-level |
|-----|-------------|------------|
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| Pi Agent | `.pi/skills` | `~/.pi/skills` |
| Codex | `.codex/skills` | `~/.codex/skills` |
| KiloCode | `.kilocode/skills` | `~/.kilocode/skills` |
| GitHub Copilot | `.github/skills` | - |
| Antigravity/Gemini | `.gemini/skills` | `~/.gemini/skills` |
| Agent (generic) | `.agent/skills` | `~/.agent/skills` |

## Common Issues Addressed

| Error | Cause | Fix Command |
|-------|-------|-------------|
| `ENOSPC: System limit for number of file watchers` | inotify exhaustion | `./run.sh fix-inotify` |
| `JavaScript heap out of memory` | Too many files in skills | `./run.sh clean-skills` |
| `Allocation failed` | Node.js heap limit | `./run.sh fix-heap` |
| Claude hangs on startup | Corrupted cache | `./run.sh clean-cache` |

## Commands

### diagnose
Run full diagnostics and report issues.

```bash
./run.sh diagnose
```

### fix-inotify
Increase inotify limits (requires sudo).

```bash
./run.sh fix-inotify
```

### fix-heap
Set NODE_OPTIONS for larger heap.

```bash
./run.sh fix-heap
```

### clean-skills
Remove .venv, __pycache__, .pytest_cache from all skills directories.

```bash
./run.sh clean-skills
```

### clean-cache
Clear Claude Code's cache directories.

```bash
./run.sh clean-cache
```

### status
Show current resource usage and limits.

```bash
./run.sh status
```

### gitignore
Add/update .gitignore in all skills directories.

```bash
./run.sh gitignore
```

## Quick Fixes

```bash
# Full diagnostic + automatic fixes
./run.sh diagnose --fix

# Just see status
./run.sh status

# Emergency cleanup (all caches)
./run.sh clean-all
```

## Proactive Usage

Run `./run.sh diagnose` when:
- Claude Code fails to start
- Claude Code crashes with memory errors
- After syncing skills across projects
- System feels sluggish with many projects open
