---
name: brain-dump-tickets
description: Manage Brain Dump tickets - create, update, track progress, and complete work items. Use when working with Brain Dump task management or when asked to create/update tickets.
---

# Brain Dump Ticket Management Skill

This skill provides the knowledge and workflows for managing Brain Dump tickets.

## When to Use This Skill

- Creating new tickets or epics
- Updating ticket status
- Adding work summaries or progress updates
- Starting or completing work on a ticket
- Linking commits or files to tickets

## Available MCP Tools

Brain Dump provides these MCP tools (prefix with `brain-dump/` if needed):

### Project Management

| Tool                   | Description                    |
| ---------------------- | ------------------------------ |
| `list_projects`        | List all registered projects   |
| `find_project_by_path` | Find project by directory path |
| `create_project`       | Register a new project         |

### Ticket Operations

| Tool + Action              | Description                        |
| -------------------------- | ---------------------------------- |
| `ticket "list"`            | List tickets (optionally filtered) |
| `ticket "create"`          | Create a new ticket                |
| `ticket "update-status"`   | Update ticket status               |
| `workflow "start-work"`    | Start working (creates git branch) |
| `workflow "complete-work"` | Complete and move to review        |

### Epic Management

| Tool + Action   | Description              |
| --------------- | ------------------------ |
| `epic "list"`   | List epics for a project |
| `epic "create"` | Create a new epic        |

### Progress Tracking

| Tool + Action            | Description               |
| ------------------------ | ------------------------- |
| `comment "add"`          | Add comment/work summary  |
| `comment "list"`         | Get comments for a ticket |
| `workflow "link-commit"` | Link a git commit         |
| `ticket "link-files"`    | Link files to a ticket    |

## Ticket Status Flow

```
backlog → ready → in_progress → review → done
                              ↘ ai_review → human_review → done
```

## Creating Good Tickets

### Required Fields

- `projectId`: Get from `find_project_by_path` or `list_projects`
- `title`: Clear, action-oriented title

### Optional Fields

- `description`: Detailed description (markdown supported)
- `priority`: "low", "medium", or "high"
- `epicId`: Group with related tickets
- `tags`: Array of categorization tags

### Example

```javascript
create_ticket({
  projectId: "abc-123",
  title: "Add user authentication",
  description: "Implement login/logout functionality with JWT tokens",
  priority: "high",
  tags: ["backend", "auth", "security"],
});
```

## Work Summary Format

When completing a ticket, add a work summary:

```javascript
comment "add"({
  ticketId: "ticket-id",
  content: `## Work Summary
**Changes Made:**
- Added LoginForm component
- Integrated with auth API
- Added validation

**Tests:**
- Unit tests passing
- E2E login flow tested

**Notes:**
- Consider adding rate limiting later`,
  author: "claude",
  type: "work_summary"
})
```

## Progress Updates

Keep users informed during work:

```javascript
comment "add"({
  ticketId: "ticket-id",
  content: "Starting implementation of login form. Will add validation and error handling.",
  author: "claude",
  type: "comment"
})
```

## Linking Work

### Link Commits

```javascript
workflow "link-commit"({
  ticketId: "ticket-id",
  commitHash: "abc123",
  commitMessage: "feat: add login form component"
})
```

### Link Files

```javascript
ticket "link-files"({
  ticketId: "ticket-id",
  files: ["src/components/LoginForm.tsx", "src/api/auth.ts"]
})
```
