---
name: dashboard
description: "Multi-project dashboard for managing PopKit-enabled projects. Shows health scores, recent activity, and quick actions across all registered projects. Use when switching between projects, checking overall status, or managing project registry. Do NOT use if only working in a single project - use morning routine or next-action instead."
---

# Multi-Project Dashboard

## Overview

Unified view across all PopKit-enabled projects, showing health scores, activity status, and enabling quick context switching.

**Core principle:** Quick status overview with actionable intelligence for multi-project developers.

**Trigger:** `/popkit:dashboard` command

## When to Use

Invoke when:

- Managing multiple projects
- Need quick overview of all project statuses
- Switching context between projects
- Registering new projects
- Checking for projects needing attention

**Do NOT use** when working in single project - use `/popkit:routine morning` or `/popkit:next` instead.

## Registry

Projects stored globally at `~/.claude/popkit/projects.json`

See [examples/registry-operations.md](examples/registry-operations.md) for all operations.

**Key operations:**

- Load/list projects
- Add/remove projects
- Switch projects
- Auto-discover projects
- Tag management
- Refresh issue counts

## Dashboard Display

```
+============================================================+
|                   PopKit Dashboard                          |
+============================================================+

  Total: 5  |  Healthy: 3  |  Warning: 1  |  Critical: 1

  ----------------------------------------------------------
  | Project          | Health | Issues | Last Active   |
  ----------------------------------------------------------
  | popkit           | + 92   |   5    | 2 min ago     |
  | popkit-cloud     | ~ 78   |   3    | 1 hour ago    |
  | reseller-central | + 88   |  12    | 3 days ago    |
  | my-website       | ! 45   |   0    | 2 weeks ago   |
  ----------------------------------------------------------

  Commands: add <path> | remove <name> | refresh | switch <name>
```

## Health Scoring

See [examples/health-scoring.md](examples/health-scoring.md) for complete scoring details.

**Score components** (100 points total):

- **Git Status** (20): Clean working tree, commits, push status
- **Build Status** (20): Passing builds, warnings, failures
- **Test Coverage** (20): Coverage percentage
- **Issue Health** (20): Stale issue count
- **Activity** (20): Last activity timestamp

**Quick vs Full checks:**

- **Quick** (~0.5s): Git + activity only (dashboard default)
- **Full** (~2-3s): All components including tests

## Subcommands

See [examples/subcommands.md](examples/subcommands.md) for all commands and examples.

**Available commands:**

- `/popkit:dashboard` - Show dashboard (default)
- `/popkit:dashboard add <path>` - Register project
- `/popkit:dashboard remove <name>` - Unregister project
- `/popkit:dashboard refresh [name]` - Update health scores
- `/popkit:dashboard switch <name>` - Change project context

## Features

### Auto-Discovery

Automatically find projects in common dev directories.

### Project Tags

Filter and organize projects by tags (`active`, `client-work`, etc.).

### Activity Feed

Show recent activity across all projects.

### Unhealthy Alerts

Identify projects needing attention (health < 70).

### Issue Count Cache

- Cached for 15 minutes (no network calls on dashboard load)
- Manual refresh available
- Graceful fallback if `gh` CLI unavailable

See [examples/registry-operations.md](examples/registry-operations.md) for implementation details.

## Integration

**Related commands:**

- `/popkit:routine morning` - Single-project health check
- `/popkit:next` - Context-aware recommendations

**Implementation files:**

- `hooks/utils/project_registry.py` - Registry CRUD operations
- `hooks/utils/health_calculator.py` - Health score calculation

## Error Handling

| Situation              | Response                          |
| ---------------------- | --------------------------------- |
| No projects registered | Suggest `/popkit:dashboard add .` |
| Project path not found | Remove from registry with warning |
| Health check fails     | Show "--" for health, log error   |
| gh CLI unavailable     | Skip issue counts                 |

## Examples

See [examples/](examples/) directory for:

- Complete health scoring details
- All registry operations with code
- Subcommand reference and usage
- Configuration examples

---

**Version**: 1.0.0
**Category**: Project Management
**Tier**: Core
