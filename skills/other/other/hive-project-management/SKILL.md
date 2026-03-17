---
name: hive-project-management
description: Manage Agent Hive projects using AGENCY.md files. Use this skill when creating, updating, or working with AGENCY.md project files, managing project metadata (status, owner, blocked, priority), marking tasks complete, adding agent notes, or understanding the Agent Hive shared memory system.
---

# Hive Project Management

This skill guides you in managing Agent Hive projects through AGENCY.md files - the shared memory primitive that enables coordination between humans and AI agents.

## AGENCY.md Structure

Every project has an AGENCY.md file with YAML frontmatter:

```markdown
---
project_id: unique-identifier
status: active              # active, pending, blocked, completed
owner: null                 # null or agent name (e.g., "claude-3.5-sonnet")
last_updated: 2025-01-15T10:30:00Z
blocked: false
blocking_reason: null
priority: high              # low, medium, high, critical
tags: [feature, backend]
dependencies:               # Optional dependency tracking
  blocked_by: []            # Projects that must complete first
  blocks: []                # Projects this blocks
  parent: null              # Parent project ID
  related: []               # Related projects
---

# Project Title

## Objective
What this project aims to achieve.

## Tasks
- [ ] Task 1
- [ ] Task 2
- [x] Completed task

## Agent Notes
- **2025-01-15 10:30 - Claude**: Started work on Task 1
```

## Frontmatter Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `project_id` | string | Unique identifier for the project |
| `status` | enum | `active`, `pending`, `blocked`, `completed` |
| `owner` | string/null | Agent name currently working, or null if unclaimed |
| `last_updated` | ISO timestamp | When the file was last modified |
| `blocked` | boolean | Set to true if human intervention needed |
| `blocking_reason` | string/null | Explanation of what's blocking |
| `priority` | enum | `low`, `medium`, `high`, `critical` |
| `tags` | array | Organizational labels |
| `dependencies` | object | Dependency relationships (see below) |

### Dependencies Object

```yaml
dependencies:
  blocked_by: [project-a, project-b]  # Must wait for these to complete
  blocks: [project-c]                  # These projects wait for this one
  parent: parent-project-id            # Hierarchical relationship
  related: [sibling-project]           # Informational links
```

## Working with Projects

### Claiming a Project

Before starting work on a project:

1. Check that `owner` is `null` (unclaimed)
2. Check that `status` is `active`
3. Check that `blocked` is `false`
4. Verify no unresolved `dependencies.blocked_by`
5. Set `owner` to your agent name

```yaml
owner: "claude-sonnet-4"
```

### Updating Progress

When completing tasks:

1. Mark tasks with `[x]` in the markdown content
2. Update `last_updated` timestamp
3. Add a note to the "Agent Notes" section

### Adding Agent Notes

Format notes with timestamp and agent name:

```markdown
## Agent Notes
- **2025-01-15 14:30 - claude-sonnet-4**: Completed research phase. Found 5 sources.
- **2025-01-15 10:00 - claude-sonnet-4**: Starting work on research tasks.
```

### Setting Blocked Status

If you need human intervention:

```yaml
blocked: true
blocking_reason: "Need API credentials for external service"
```

### Completing a Project

When finished:

1. Mark all tasks complete
2. Set `status: completed`
3. Set `owner: null`
4. Add final notes

### Releasing Without Completing

If handing off to another agent:

1. Set `owner: null`
2. Add notes about current state
3. Leave `status` unchanged

## Creating New Projects

To create a new project:

1. Create directory: `projects/your-project-name/`
2. Create `AGENCY.md` with proper frontmatter
3. Define clear objectives and tasks
4. Set initial `status: pending` or `status: active`

## Best Practices

1. **Always claim before working** - Set `owner` to prevent conflicts
2. **Update frequently** - Keep `last_updated` current
3. **Be descriptive in notes** - Future agents need context
4. **Use blocking correctly** - Only set `blocked: true` for external dependencies
5. **Manage dependencies** - Keep `blocked_by`/`blocks` accurate
6. **Release when done** - Set `owner: null` when finished or handing off
7. **Follow priority** - Work on `critical` and `high` priority first

## Common Patterns

### Research then Implementation

```markdown
## Tasks

### Research Phase
- [x] Find sources
- [x] Summarize findings

### Implementation Phase
- [ ] Design solution
- [ ] Implement feature
- [ ] Test changes
```

### Phased Rollout

Use `dependencies.blocked_by` to sequence phases:

```yaml
# Phase 2 project
dependencies:
  blocked_by: [phase-1-project]
```

### Parent-Child Projects

```yaml
# Child project
dependencies:
  parent: main-feature-project
```
