---
name: god-mode
description: Developer oversight and AI agent coaching. Use when viewing project status across repos, syncing GitHub data, or analyzing agents.md against commit patterns.
metadata: {"openclaw": {"requires": {"bins": ["gh", "sqlite3", "jq"]}}}
user-invocable: true
---

# god-mode Skill

> Developer oversight and AI agent coaching for OpenClaw.

## Overview

**god-mode** gives you a bird's-eye view of all your coding projects and coaches you to write better AI agent instructions.

**Key features:**
- Multi-project status dashboard
- Incremental sync from GitHub (Azure/GitLab coming)
- Agent instruction analysis based on commit patterns
- Local SQLite cache for fast queries

## Quick Start

```bash
# First-run setup
god setup

# Add a project
god projects add github:myuser/myrepo

# Sync data
god sync

# See overview
god status

# Analyze your agents.md
god agents analyze myrepo
```

## Commands

### `god status [project]`
Show overview of all projects, or details for one:
```bash
god status              # All projects
god status myproject    # One project in detail
```

### `god sync [project] [--force]`
Fetch/update data from repositories:
```bash
god sync                # Incremental sync all
god sync myproject      # Just one project
god sync --force        # Full refresh (ignore cache)
```

### `god projects`
Manage configured projects:
```bash
god projects                        # List all
god projects add github:user/repo   # Add project
god projects remove myproject       # Remove project
```

### `god agents analyze <project>`
Analyze agents.md against commit history:
```bash
god agents analyze myproject
```

Finds gaps between your agent instructions and actual work patterns, suggests improvements.

### `god agents generate <project>` (Coming Soon)
Bootstrap agents.md for a new project by analyzing repo structure.

## Configuration

Config file: `~/.config/god-mode/config.yaml`

```yaml
projects:
  - id: github:user/repo
    name: My Project      # Display name
    priority: high        # high/medium/low
    tags: [work, api]
    local: ~/code/myrepo  # Local clone path

sync:
  initialDays: 90         # First sync lookback
  commitsCacheMinutes: 60

analysis:
  agentFiles:             # Files to search for
    - agents.md
    - AGENTS.md
    - CLAUDE.md
    - .github/copilot-instructions.md
```

## Data Storage

All data stored locally in `~/.god-mode/`:
- `cache.db` - SQLite database (commits, PRs, issues, analyses)
- `contexts/` - Saved workspace contexts (v0.2)

## Authentication

god-mode uses your existing CLI authentication:

| Provider | CLI | Setup |
|----------|-----|-------|
| GitHub | `gh` | `gh auth login` |
| Azure | `az` | `az login` |
| GitLab | `glab` | `glab auth login` |

**No tokens stored by god-mode.** We delegate to CLIs you already trust.

## Requirements

- `gh` - GitHub CLI (for GitHub repos)
- `sqlite3` - Database
- `jq` - JSON processing

## Examples

### Morning Check-In
```bash
god status
# See all projects at a glance
# Notice any stale PRs or quiet projects
```

### Before Switching Projects
```bash
god status myproject
# See recent activity, open PRs, issues
# Remember where you left off
```

### Improving Your AI Assistant
```bash
god agents analyze myproject
# Get suggestions based on your actual commit patterns
# Apply recommendations to your agents.md
```

### Weekly Review
```bash
god status
# Review activity across all projects
# Identify projects needing attention
```

## Agent Workflows

### Daily Briefing (Heartbeat)
```markdown
# HEARTBEAT.md
- Run `god status` and summarize:
  - Projects with stale PRs (>3 days)
  - Projects with no activity (>5 days)
  - Open PRs needing review
```

### Agent Analysis (Cron)
```yaml
# Weekly agent instruction review
schedule: "0 9 * * 1"  # Monday 9am
task: |
  Run `god agents analyze` on high-priority projects.
  If gaps found, notify with suggestions.
```

## Troubleshooting

### "gh: command not found"
Install GitHub CLI: https://cli.github.com/

### "Not logged in to GitHub"
Run: `gh auth login`

### "No projects configured"
Add a project: `god projects add github:user/repo`

### Stale data
Force refresh: `god sync --force`

---

*OpenClaw Community Skill*  
*License: MIT*  
*Repository: https://github.com/InfantLab/god-mode-skill*
