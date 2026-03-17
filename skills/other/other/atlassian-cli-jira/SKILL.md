---
name: atlassian-cli-jira
description: Search, create, update, and manage Jira tickets and sprints. Use when the user asks about their Jira tickets, wants to create issues, check sprint progress, transition ticket status, or query work items.
metadata:
  category: tooling
  tools: acli
---

# Atlassian CLI - Jira Workflows

Quick reference for common Atlassian CLI Jira operations. Requires `acli` to be installed and authenticated.

**Documentation:** https://developer.atlassian.com/cloud/acli/reference/commands/jira/

## Prerequisites

If `acli` is not installed or not authenticated, instruct the user to run:

```bash
acli auth login --web    # Opens browser for OAuth
acli auth status         # Verify authentication
```

## Common JQL Patterns

Use these JQL queries with `acli jira workitem search --jql "..."`:

### Find tickets assigned to you

```bash
acli jira workitem search --jql "assignee = currentUser()" --paginate
```

### Find tickets in a specific status

```bash
acli jira workitem search --jql 'status = "In Progress"'
acli jira workitem search --jql 'status IN ("To Do", "In Progress")'
```

### Find tickets by project

```bash
acli jira workitem search --jql "project = PROJECTKEY"
```

### Find tickets by reporter

```bash
acli jira workitem search --jql "reporter = currentUser()"
```

### Find unassigned tickets

```bash
acli jira workitem search --jql "assignee = EMPTY"
```

### Find recently updated tickets

```bash
acli jira workitem search --jql "updated >= -7d ORDER BY updated DESC"
```

### Find open bugs in a project

```bash
acli jira workitem search --jql "project = PROJECTKEY AND type = Bug AND status != Closed"
```

## Work Item Operations

### View a ticket

```bash
acli jira workitem view PROJECTKEY-123
```

### Create a new ticket

```bash
acli jira workitem create \
  --project PROJECTKEY \
  --type Task \
  --title "My new task" \
  --description "Task description"
```

### Edit a ticket

```bash
acli jira workitem edit PROJECTKEY-123 --summary "Updated title"
```

### Assign a ticket

```bash
acli jira workitem assign PROJECTKEY-123 --assignee user@example.com
```

### Transition a ticket (change status)

```bash
acli jira workitem transition PROJECTKEY-123 --transition "In Progress"
```

### Add a comment

```bash
acli jira workitem comment-create PROJECTKEY-123 --comment "This is my comment"
```

### Delete a ticket

```bash
acli jira workitem delete PROJECTKEY-123
```

## Board & Sprint Commands

```bash
acli jira board list-sprints --board BOARDKEY
acli jira sprint list-workitems --sprint SPRINTID
acli jira board search --name "My Board"
```

## Tips

- **JQL Documentation:** https://www.atlassian.com/software/jira/guides/expand-jira/jira-query-language
- Use `--paginate` when you expect many results (avoids truncation)
- Use `--json` for programmatic processing, `--csv` for spreadsheet export
- Add `ORDER BY updated DESC` to sort by most recent changes
- Use `--web` to open results in your browser
- Combine multiple conditions: `AND`, `OR`, `NOT`

For output formats, pagination, field customization, saved filters, and real-world query examples, see `references/search-patterns.md`.
