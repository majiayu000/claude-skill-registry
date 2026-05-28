---
name: project-management
description: Manage projects and tasks across domains. USE WHEN create project OR new project OR pull tasks OR sync tasks OR update plan OR project status OR list projects OR task dashboard OR archive project OR project management OR track tasks.
user-invocable: false
---

# Project Management Skill

Centralized project and task management across PAL domains with bidirectional sync between project files and a master task list.

## Workflow Routing

| Workflow          | Trigger                                                               | File                             |
| ----------------- | --------------------------------------------------------------------- | -------------------------------- |
| Create Project    | "create project", "new project", "start project"                      | `workflows/create_project.md`    |
| Pull Tasks        | "pull tasks", "sync tasks", "aggregate tasks", "gather tasks"         | `workflows/pull_tasks.md`        |
| Update Tasks      | "update tasks", "push tasks", "sync back", "update projects"          | `workflows/update_tasks.md`      |
| Project Dashboard | "project dashboard", "list projects", "task summary", "show projects" | `workflows/project_dashboard.md` |
| Archive Project   | "archive project", "complete project", "close project"                | `workflows/archive_project.md`   |

## Examples

### Example 1: Create a New Project

**User:** "I want to create a new project for the API integration work"

**Workflow:** `create_project`

**Process:**

1. List available domains for selection
2. Ask for project name: "API Integration"
3. Ask for objective: "Integrate third-party payment API"
4. Ask for initial tasks: "Research API docs, Create auth flow, Implement endpoints"
5. Ask for priority: "high"
6. Generate `API_INTEGRATION_PROJECT.md` in selected domain

**Output:**

```
Project created: domains/example-domain/01_PROJECTS/API_INTEGRATION_PROJECT.md
- Status: planning
- Priority: high
- Tasks: 3 open
- Updated domain INDEX.md
```

### Example 2: Pull Tasks from All Projects

**User:** "Pull all open tasks into the master list"

**Workflow:** `pull_tasks`

**Process:**

1. Scan `Domains/*/01_PROJECTS/PROJECT_*.md` — tagged `#ProjectName`
2. Scan `Domains/*/01_PROJECTS/AD_HOC_TASKS.md` — tagged `#AdHoc:DomainName`
3. Scan `Inbox/Daily/*.md` — unsynced `- [ ]` items tagged `#Daily:YYYY-MM-DD`
4. Scan `Inbox/Notes/*.md` — unsynced `[action]` and `- [ ]` items tagged `#Note:slug`
5. Generate `Inbox/Dashboards/TASKS.md` with sections per source

**Output:**

```
Tasks pulled!
  Domain projects:  7 files → 12 tasks
  Domain ad-hoc:    3 files → 4 tasks
  Inbox/Daily:      5 files → 3 unsynced tasks
  Inbox/Notes:      2 files → 2 unsynced tasks
  Tasks file: Inbox/Dashboards/TASKS.md
```

### Example 3: View Project Dashboard

**User:** "Show me all projects and their status"

**Workflow:** `project_dashboard`

**Process:**

1. Scan all \*\_PROJECT.md files across domains
2. Parse status, priority, and task counts
3. Generate summary view

**Output:**

```
PROJECT DASHBOARD

By Status:
  Planning:    2 projects
  In Progress: 3 projects
  Review:      1 project
  Completed:   1 project

High Priority:
  - API_INTEGRATION_PROJECT (example-domain) - 3 open tasks
  - SECURITY_AUDIT_PROJECT (security-domain) - 5 open tasks

Overdue: None
```

## Task Format

Tasks use **checkbox symbols** to indicate status. The symbol inside the checkbox determines the task state.

### Checkbox Symbol Reference

| Symbol | Status | Meaning | Section |
|--------|--------|---------|---------|
| `[ ]` | To Do | Task not started, ready to work on | Active |
| `[/]` | In Progress | Task actively being worked on | Active |
| `[!]` | Blocked | Cannot proceed (dependency, external blocker) | Inactive |
| `[?]` | Paused | Intentionally paused or temporarily deprioritized | Inactive |
| `[I]` | Backlog | Moved to backlog (not doing now, might do later) | Inactive |
| `[-]` | Not Doing | Decided not to do this task | Inactive |
| `[x]` | Done | Task completed | Done |

### Example Project Tasks

```markdown
### Active
- [ ] Research API documentation
- [/] Implement user authentication

### Inactive
- [!] Deploy to production (waiting for security review)
- [?] Add advanced analytics (paused until Q2)
- [I] Internationalization support
- [-] Add GraphQL support (decided against)

### Done
- [x] Set up project repository
- [x] Create initial documentation
```

### Section Structure

- `### Active` - Contains `[ ]` (to do) and `[/]` (in-progress) tasks
- `### Inactive` - Contains `[!]` (blocked), `[?]` (paused), `[I]` (backlog), `[-]` (not doing) tasks
- `### Done` - Contains `[x]` (done) tasks

## Quick Reference

| Location | Purpose |
|---|---|
| `Domains/*/01_PROJECTS/PROJECT_*.md` | Project task files → tagged `#ProjectName` |
| `Domains/*/01_PROJECTS/AD_HOC_TASKS.md` | Domain-level ad hoc tasks → tagged `#AdHoc:DomainName` |
| `Inbox/Daily/*.md` | Daily notes with unsynced tasks → tagged `#Daily:YYYY-MM-DD` |
| `Inbox/Notes/*.md` | Inbox notes with unsynced `[action]` items → tagged `#Note:slug` |
| `Inbox/Dashboards/TASKS.md` | Aggregated task dashboard (all sources) |
| `templates/project_template.md` | Template for new projects |

### Project Tags

Tasks use `#ProjectName` suffix to identify their source project:

- `- [ ] Task description #APIIntegration` → belongs to API_INTEGRATION_PROJECT
- `- [ ] Task without tag` → ad-hoc task (from AD_HOC_TASKS.md)

Tag format: `#` + project name in PascalCase (derived from PROJECT_NAME → ProjectName)

### AD_HOC_TASKS.md

Every domain has one `AD_HOC_TASKS.md` in `01_PROJECTS/`. It captures standalone tasks with no parent project. Frontmatter schema:

```yaml
name: AD_HOC_TASKS
type: task-list
domain: DomainName
last_updated: YYYY-MM-DD
```

Pull Tasks and Update Plan workflows must scan `AD_HOC_TASKS.md` alongside `PROJECT_*.md` files.

## Related Documentation

- [DOMAINS_LOGIC.md](../../.claude/core/system/DOMAINS_LOGIC.md) - Domain structure
- [create-domain skill](../create-domain/SKILL.md) - Domain creation
