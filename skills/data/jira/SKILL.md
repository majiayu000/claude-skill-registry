---
name: jira
description: Use jira CLI for Jira operations including issue management, project queries, transitions, and JQL search
---
# Jira CLI Skill

You are a Jira specialist using the `jira` CLI tool. This skill provides comprehensive guidance for working with Jira through a custom CLI.

## Core Commands

### Authentication

```bash
# Check authentication status
jira auth check

# Login to Jira
jira auth login
```

### Issue Management

```bash
# View issue details
jira issue get ISSUE-123

# Create new issue
jira issue create --project PROJ --type Bug --summary "Issue summary" --description "Description"

# Update issue
jira issue update ISSUE-123 --summary "New summary"

# Add comment to issue
jira comment add ISSUE-123 "Comment text"

# List comments on issue
jira comment list ISSUE-123
```

### Issue Transitions

```bash
# List available transitions for an issue
jira transition list ISSUE-123

# Transition issue to new status
jira transition ISSUE-123 "In Progress"
```

### Searching with JQL

```bash
# Search issues with JQL
jira search "project = PROJ AND status = Open"

# Search with output format
jira search "assignee = currentUser()" --format json

# Search with field selection
jira search "project = PROJ" --fields summary,status,assignee
```

### Project Operations

```bash
# List all projects
jira project list

# Get project details
jira project get PROJ
```

### Watching and Assigning

```bash
# Watch an issue
jira watch add ISSUE-123

# Stop watching an issue
jira watch remove ISSUE-123

# Assign issue
jira assign ISSUE-123 username

# Assign to self
jira assign ISSUE-123 me
```

## Common Workflows

### Viewing Your Work

```bash
# View issues assigned to you
jira search "assignee = currentUser() AND status != Done"

# View issues you're watching
jira search "watcher = currentUser()"

# View recent activity
jira search "updatedDate >= -7d AND assignee = currentUser()"
```

### Creating and Updating Issues

```bash
# Create a bug
jira issue create --project PROJ --type Bug \
  --summary "Login button not working" \
  --description "Steps to reproduce..."

# Update priority
jira issue update ISSUE-123 --priority High

# Add labels
jira issue update ISSUE-123 --labels bug,frontend

# Link issues
jira link add ISSUE-123 ISSUE-456 "blocks"
```

### Moving Issues Through Workflow

```bash
# Start work on issue
jira transition ISSUE-123 "In Progress"

# Mark as done
jira transition ISSUE-123 "Done"

# Reopen issue
jira transition ISSUE-123 "Reopen"
```

## JQL Reference

### Common JQL Patterns

```bash
# Issues in specific project
jira search "project = MYPROJ"

# Open issues assigned to you
jira search "assignee = currentUser() AND status in (Open, 'In Progress')"

# High priority bugs
jira search "type = Bug AND priority = High"

# Recently updated issues
jira search "updated >= -1w"

# Issues created this sprint
jira search "sprint in openSprints() AND created >= startOfWeek()"

# Issues with specific label
jira search "labels = urgent"

# Issues in epic
jira search "'Epic Link' = EPIC-123"
```

### JQL Field Reference

- `project` - Project key or name
- `status` - Issue status (Open, In Progress, Done, etc.)
- `assignee` - Assigned user (use `currentUser()` for yourself)
- `reporter` - Issue reporter
- `priority` - Priority level (Highest, High, Medium, Low, Lowest)
- `type` - Issue type (Bug, Story, Task, Epic, etc.)
- `labels` - Issue labels
- `created` - Creation date
- `updated` - Last update date
- `resolution` - Resolution status

### JQL Functions

- `currentUser()` - Current logged-in user
- `startOfDay()`, `startOfWeek()`, `startOfMonth()` - Date functions
- `now()` - Current timestamp
- `openSprints()` - Currently active sprints
- `closedSprints()` - Completed sprints

## Output Formats

```bash
# JSON output (for scripting)
jira search "project = PROJ" --format json

# Table output (human-readable, default)
jira search "project = PROJ" --format table

# CSV output
jira search "project = PROJ" --format csv
```

## Best Practices

1. **Always authenticate first**: Run `jira auth check` before operations
2. **Use JQL for complex queries**: More powerful than simple filters
3. **Specify output format**: Use `--format json` for scripting
4. **Include field selection**: Use `--fields` to limit returned data
5. **Test transitions**: Use `jira transition list` before transitioning
6. **Be specific with JQL**: Use quotes for multi-word values

## Common Use Cases

### Daily Standup Prep

```bash
# What you worked on yesterday
jira search "assignee = currentUser() AND updated >= -1d"

# What you're working on today
jira search "assignee = currentUser() AND status = 'In Progress'"
```

### Bug Triage

```bash
# Unassigned bugs
jira search "type = Bug AND assignee is EMPTY AND status = Open"

# Critical bugs in project
jira search "project = PROJ AND type = Bug AND priority in (Highest, High)"
```

### Sprint Planning

```bash
# Issues in backlog
jira search "project = PROJ AND status = 'To Do' AND sprint is EMPTY"

# Issues in current sprint
jira search "project = PROJ AND sprint in openSprints()"

# Completed this sprint
jira search "project = PROJ AND sprint in openSprints() AND status = Done"
```

## Error Handling

If you encounter authentication errors:
```bash
jira auth login
```

If JQL syntax errors occur:
- Check for proper quoting of multi-word values
- Verify field names are correct
- Use `AND`, `OR`, `NOT` operators (uppercase)

## Quick Reference

```bash
# View issue
jira issue get ISSUE-123

# Search
jira search "JQL query here"

# Create
jira issue create --project PROJ --type TYPE --summary "text"

# Update
jira issue update ISSUE-123 --field value

# Transition
jira transition ISSUE-123 "Status Name"

# Comment
jira comment add ISSUE-123 "Comment text"

# Assign
jira assign ISSUE-123 username
```
