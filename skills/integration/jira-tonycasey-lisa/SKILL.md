---
name: jira
description: "Create, list, view, and manage Jira issues via REST API; triggers on 'jira', 'create ticket', 'list issues', 'change type'."
---

## Purpose
Model-neutral helper to interact with Jira via Atlassian REST API v3. Supports creating issues, listing, viewing, assigning, and transitioning.

## Triggers
Use when the user says: "create a jira ticket", "list jira issues", "jira create", "show jira issue", "assign ticket".

## Configuration
Reads from `~/.jira.d/`:
- `config.yml` - endpoint, user, authentication-method
- `api-token` - raw API token (no variable assignment)

Example config.yml:
```yaml
endpoint: https://yourcompany.atlassian.net
user: your.email@company.com
authentication-method: api-token
```

## How to use

### Create Issue
```bash
# Create Epic
lisa jira create --type epic --project PROJ --summary "Feature title" --description "Description text"

# Create Story
lisa jira create --type story --project PROJ --summary "Story title" --parent PROJ-123

# Create Sub-task
lisa jira create --type subtask --project PROJ --summary "Sub-task title" --parent PROJ-123

# Create with assignment
lisa jira create --type task --project PROJ --summary "Task" --assign me
```

### List Issues
```bash
# List by project
lisa jira list --project PROJ --limit 10

# List with JQL
lisa jira list --jql "assignee = currentUser() ORDER BY created DESC" --limit 5

# List my issues
lisa jira list --mine --limit 10
```

### View Issue
```bash
lisa jira view PROJ-123
```

### Assign Issue
```bash
# Assign to self
lisa jira assign PROJ-123 --to me

# Assign to user
lisa jira assign PROJ-123 --to "user@company.com"
```

### Transition Issue
```bash
# Move to In Progress
lisa jira transition PROJ-123 --to "In Progress"

# Move to Done
lisa jira transition PROJ-123 --to "Done"

# Move to Code Review
lisa jira transition PROJ-123 --to "Code Review"
```

### Change Issue Type
```bash
# Change Epic to Story
lisa jira change-type PROJ-123 --to story

# Change to Task
lisa jira change-type PROJ-123 --to task
```

Valid types: `epic`, `story`, `task`, `subtask`, `bug`

## Workflow: PR Created

**When a Pull Request is created**, transition all associated Jira tickets to "Code Review":

1. Identify the ticket(s) from the branch name (e.g., `PROJ-123`)
2. Check if the ticket has subtasks (use `view` command)
3. Transition the main ticket and ALL subtasks to "Code Review"

```bash
# Example: Transition epic and all subtasks to Code Review
lisa jira transition PROJ-123 --to "Code Review"

# For subtasks (if in "To Do", first move to "In Progress")
for ticket in PROJ-124 PROJ-125 PROJ-126; do
  lisa jira transition "$ticket" --to "Code Review"
done
```

**Note:** If a ticket is in "To Do", you may need to transition through "In Progress" first:
```bash
lisa jira transition PROJ-123 --to "In Progress"
lisa jira transition PROJ-123 --to "Code Review"
```

**See also:** `git` skill for PR creation, CI triggers, and test retriggers.

## I/O Contract (examples)

### Create
```json
{
  "status": "ok",
  "action": "create",
  "issue": {
    "key": "PROJ-123",
    "url": "https://company.atlassian.net/browse/PROJ-123",
    "summary": "Feature title",
    "type": "Epic"
  }
}
```

### List
```json
{
  "status": "ok",
  "action": "list",
  "issues": [
    {"key": "PROJ-123", "summary": "...", "status": "To Do", "assignee": "John Doe"}
  ],
  "total": 10
}
```

### View
```json
{
  "status": "ok",
  "action": "view",
  "issue": {
    "key": "PROJ-123",
    "summary": "...",
    "description": "...",
    "status": "To Do",
    "assignee": "John Doe",
    "reporter": "...",
    "created": "2026-01-13T...",
    "subtasks": [...]
  }
}
```

### Change Type
```json
{
  "status": "ok",
  "action": "change-type",
  "issue": {
    "key": "PROJ-123",
    "url": "https://company.atlassian.net/browse/PROJ-123",
    "previousType": "Epic",
    "newType": "story"
  }
}
```

### Error
```json
{
  "status": "error",
  "error": "Authentication failed",
  "details": "..."
}
```

## Issue Types
Standard Jira issue types (IDs may vary by project):
- `epic` (10000) - Parent for features
- `story` (10001) - User stories
- `task` (10002) - General tasks
- `subtask` (10003) - Sub-tasks linked to parent
- `bug` (10004) - Bug reports

## Cross-model checklist
- Claude: concise instructions; use JSON output for parsing
- Gemini: explicit commands and minimal formatting

## Notes
- Requires Node.js >= 18 (uses native fetch)
- API token must have project access permissions
- Description uses Atlassian Document Format (ADF) internally
- Rate limits apply per Atlassian Cloud policies
