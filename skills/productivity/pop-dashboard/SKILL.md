---
name: dashboard
description: "Multi-project dashboard for managing PopKit-enabled projects. Shows health scores, recent activity, and quick actions across all registered projects. Use when switching between projects, checking overall status, or managing project registry. Do NOT use if only working in a single project - use morning routine or next-action instead."
---

# Multi-Project Dashboard

## Overview

Provides a unified view across all PopKit-enabled projects, showing health scores, activity status, and enabling quick context switching.

**Core principle:** Quick status overview with actionable intelligence for multi-project developers.

**Trigger:** `/popkit:dashboard` command or skill invocation.

## When to Use

Invoke this skill when:

- Managing multiple projects
- Need quick overview of all project statuses
- Switching context between projects
- Registering new projects
- Checking for projects needing attention

## Registry Management

The project registry is stored globally at `~/.claude/popkit/projects.json`.

### Step 1: Load Registry

```python
from project_registry import load_registry, list_projects

# Load all registered projects
registry = load_registry()
projects = list_projects()

print(f"Total projects: {len(projects)}")
```

### Step 2: Display Dashboard

Show the main dashboard view:

```
+===============================================================+
|                      PopKit Dashboard                          |
+===============================================================+

  Total: 5  |  Healthy: 3  |  Warning: 1  |  Critical: 1

  -------------------------------------------------------------
  | Project          | Health | Issues | Last Active   |
  -------------------------------------------------------------
  | popkit           | + 92   |   5    | 2 min ago     |
  | popkit-cloud     | ~ 78   |   3    | 1 hour ago    |
  | reseller-central | + 88   |  12    | 3 days ago    |
  | my-website       | ! 45   |   0    | 2 weeks ago   |
  -------------------------------------------------------------

  Commands: add <path> | remove <name> | refresh | switch <name>
```

### Step 3: Health Score Calculation

Use the health calculator for detailed scores:

```python
from health_calculator import calculate_health_score, calculate_quick_health

# Full health check (slower, more accurate)
result = calculate_health_score("/path/to/project")
print(f"Health: {result['score']}/100")

# Quick health check (git + activity only)
quick_score = calculate_quick_health("/path/to/project")
print(f"Quick Health: {quick_score}/100")
```

### Health Score Breakdown

| Component         | Points | Criteria                                                                  |
| ----------------- | ------ | ------------------------------------------------------------------------- |
| **Git Status**    | 20     | Clean working tree (+20), uncommitted (-5/10 files), unpushed (-5/commit) |
| **Build Status**  | 20     | Passed (+20), warnings (-2 each), failed (0)                              |
| **Test Coverage** | 20     | >80% (+20), 60-80% (+15), <60% (+10), none (+5)                           |
| **Issue Health**  | 20     | No stale (+20), -2 per stale issue (>30 days)                             |
| **Activity**      | 20     | Today (+20), week (+15), month (+10), older (+5)                          |

### Step 4: Refresh Issue Counts

Fetch fresh GitHub issue counts for all projects:

```python
from project_registry import load_registry, refresh_project_issue_counts, save_registry

# Load registry
registry = load_registry()

# Fetch fresh issue counts for all projects
updated_count = refresh_project_issue_counts(registry)

# Save updated registry
save_registry(registry)

print(f"Updated issue counts for {updated_count} projects")
```

**Cache Behavior:**

- Issue counts are cached for 15 minutes (TTL)
- Dashboard displays cached counts when fresh (`< 15 min`)
- Stale cache displays `'--'` until refreshed
- Non-GitHub projects always show `'--'`

**Performance Considerations:**

- Dashboard loads instantly (uses cache, no network calls)
- Refresh fetches issue counts sequentially (~0.5s per project)
- 10 projects refresh in ~5-10 seconds
- Manual refresh gives user control over when to pay fetch cost
- Falls back gracefully if `gh` CLI is unavailable

## Subcommand Operations

### Show Dashboard (Default)

```bash
/popkit:dashboard
```

Display the full dashboard with all projects, health scores, and quick actions.

### Add Project

```bash
/popkit:dashboard add /path/to/project
/popkit:dashboard add . # Current directory
```

Register a project in the global registry. Auto-detects:

- Project name from package.json/pyproject.toml
- GitHub repo from git remote
- Initial health score

```python
from project_registry import add_project

success, message = add_project("/path/to/project", tags=["active"])
print(message)
```

### Remove Project

```bash
/popkit:dashboard remove project-name
```

Remove a project from registry (does not delete files).

```python
from project_registry import remove_project

success, message = remove_project("my-project")
print(message)
```

### Refresh Health Scores

```bash
/popkit:dashboard refresh           # Refresh all
/popkit:dashboard refresh popkit    # Refresh one
```

Recalculate health scores for all or specific projects:

```python
from project_registry import list_projects, update_health_score
from health_calculator import calculate_health_score

for project in list_projects():
    result = calculate_health_score(project["path"])
    update_health_score(project["name"], result["score"])
    print(f"{project['name']}: {result['score']}/100")
```

### Switch Project

```bash
/popkit:dashboard switch project-name
```

Change context to a different project. Updates activity timestamp and provides project summary.

```python
from project_registry import get_project, touch_project
import os

project = get_project("popkit")
if project:
    os.chdir(project["path"])
    touch_project(project["path"])
    print(f"Switched to: {project['name']}")
```

## Auto-Discovery

Automatically discover projects in common locations:

```python
from project_registry import discover_projects, add_project

# Search common dev directories
discovered = discover_projects()

for project in discovered:
    print(f"Found: {project['name']} at {project['path']}")

# Add discovered projects
for project in discovered:
    add_project(project["path"])
```

## Output Format

Use AskUserQuestion for interactive operations:

```
Use AskUserQuestion tool with:
- question: "Which project would you like to switch to?"
- header: "Switch"
- options:
  - label: "popkit"
    description: "Health: 92 | Last active: 2 min ago"
  - label: "popkit-cloud"
    description: "Health: 78 | Last active: 1 hour ago"
  - label: "reseller-central"
    description: "Health: 88 | Last active: 3 days ago"
- multiSelect: false
```

## Cross-Project Activity Feed

Show recent activity across all projects:

```
Recent Activity (across all projects)
-------------------------------------
| Project          | Action           | Time       |
|------------------|------------------|------------|
| popkit           | Closed #117      | 2 min ago  |
| popkit-cloud     | Pushed main      | 1 hour ago |
| reseller-central | Failed build     | 3 days ago |
```

## Project Tags

Tag projects for filtering:

```python
from project_registry import add_tag, get_projects_by_tag

# Add tags
add_tag("popkit", "active")
add_tag("reseller-central", "client-work")

# Filter by tag
active_projects = get_projects_by_tag("active")
```

## Unhealthy Project Alerts

Identify projects needing attention:

```python
from project_registry import get_unhealthy_projects

# Projects with health < 70
unhealthy = get_unhealthy_projects(threshold=70)

if unhealthy:
    print("Projects needing attention:")
    for p in unhealthy:
        print(f"  ! {p['name']}: {p['healthScore']}/100")
```

## Settings

Configure dashboard behavior in registry:

```json
{
  "settings": {
    "autoDiscover": true,
    "healthCheckInterval": "daily",
    "maxInactiveProjects": 20
  }
}
```

## Error Handling

| Situation              | Response                          |
| ---------------------- | --------------------------------- |
| No projects registered | Suggest `/popkit:dashboard add .` |
| Project path not found | Remove from registry with warning |
| Health check fails     | Show "--" for health, log error   |
| gh CLI unavailable     | Skip issue counts                 |

## Related

- `/popkit:dashboard` command - User-facing wrapper
- `/popkit:routine morning` - Single-project health check
- `/popkit:next` - Context-aware recommendations
- `hooks/utils/project_registry.py` - Registry CRUD operations
- `hooks/utils/health_calculator.py` - Health score calculation
