---
name: beads-workflow
description: AI-native issue tracking with Beads. Use when managing work items, tracking issues, or coordinating tasks in multi-agent workflows. Covers bd commands, dependencies, and sync patterns.
allowed-tools: Read, Bash, Glob, Grep, mcp__github__*
---

# Beads Workflow

## Overview

Beads is an AI-native issue tracker designed for agent workflows. Issues live in your repo, sync via git, and require no web UI.

## MCP Tools

**GitHub** (remote collaboration):
- Link Beads issues to GitHub PRs
- Create GitHub issues for team visibility
- Track PR status for blocked work
- Auto-close Beads issues when PRs merge

## Core Commands

### Issue Management

```bash
# Create a new issue
bd create "Title" -t feature -p 2

# List open issues
bd list --status open

# View issue details
bd show <issue-id>

# Update issue
bd update <id> --status in_progress
bd update <id> --assignee claude

# Close issue
bd close <id> --reason "Completed: description"
```

### Finding Work

```bash
# Get unblocked issues (no dependencies blocking)
bd ready --sort hybrid

# Filter by priority
bd list --priority 1 --status open

# Filter by labels
bd list --label backend
```

### Dependencies

```bash
# Add dependency (X blocks Y)
bd dep add <blocking-id> <blocked-id> --type blocks

# View dependency tree
bd dep tree <id>

# Remove dependency
bd dep rm <blocking-id> <blocked-id>
```

### Syncing

```bash
# Sync with git remote
bd sync

# Force flush to JSONL
bd flush
```

## GitHub Integration Patterns

### Linking Issues to PRs

1. Create Beads issue: `bd create "Feature X"`
2. Implement and create PR via GitHub MCP
3. Reference Beads ID in PR description
4. When PR merges, close Beads issue: `bd close <id>`

### Syncing Status

```bash
# Check if related PR is merged (use GitHub MCP)
# Then update Beads status accordingly
bd update <id> --status done
```

### Team Visibility

For issues that need team visibility:
1. Create in Beads for local tracking
2. Use GitHub MCP to create corresponding GitHub issue
3. Link both in descriptions
4. Keep Beads as source of truth for agents

## Workflow Patterns

### Starting a Session

1. **Check ready work**: `bd ready --sort hybrid`
2. **Check GitHub**: Use GitHub MCP to verify no blocking PRs
3. **Claim an issue**: `bd update <id> --status in_progress`
4. **Review dependencies**: `bd dep tree <id>`
5. **Begin implementation**

### During Implementation

1. **Track sub-tasks**: `bd create "Sub-task" --parent <id>`
2. **Add blockers**: `bd dep add <new-blocker> <id> --type blocks`
3. **Update progress**: `bd comment <id> "Progress update"`
4. **Create PR**: Use GitHub MCP when ready

### Completing Work

1. **Verify completion**: All acceptance criteria met
2. **PR status**: Use GitHub MCP to check CI/review status
3. **Close issue**: `bd close <id> --reason "Implemented X, PR #123"`
4. **Sync**: `bd sync`
5. **Check next**: `bd ready`

### Multi-Agent Coordination

```bash
# See who's working on what
bd list --status in_progress --json | jq '.[] | {id, title, assignee}'

# Avoid conflicts - check before claiming
bd show <id>  # Check assignee field

# Hand off work
bd update <id> --assignee other-agent
bd comment <id> "Handoff: context and next steps"
```

## Issue Types

| Type | When to Use |
|------|-------------|
| `feature` | New functionality |
| `bug` | Defect fixes |
| `task` | General work items |
| `spike` | Research/investigation |
| `chore` | Maintenance, cleanup |

## Priority Levels

| Priority | Meaning |
|----------|---------|
| 0 | Critical - Drop everything |
| 1 | High - Next up |
| 2 | Medium - Normal flow |
| 3 | Low - When time permits |
| 4 | Backlog - Future consideration |

## Status Flow

```
open -> in_progress -> done
         |-> blocked -> in_progress
```

## Best Practices

1. **One issue per logical unit**: Don't combine unrelated work
2. **Clear titles**: Should explain what, not how
3. **Use dependencies**: Makes ready work visible
4. **Sync frequently**: Keep other agents informed
5. **Close promptly**: Don't leave stale in_progress issues
6. **Link to GitHub**: Create GitHub issues for team-visible work

## Integration with Swarm

When working in a swarm:

1. **Check active work**: `bd list --status in_progress`
2. **Claim before editing**: Update status before touching code
3. **Document blockers**: Create issues for discovered blockers
4. **Handoff cleanly**: Update assignee and add context
5. **Sync before ending**: `bd sync` to share state
6. **Create PRs**: Use GitHub MCP for review visibility

## Troubleshooting

```bash
# Check daemon health
bd daemons health

# View daemon logs
bd daemons logs

# Force reimport from JSONL
bd import --force

# Check for conflicts
bd sync --dry-run
```
