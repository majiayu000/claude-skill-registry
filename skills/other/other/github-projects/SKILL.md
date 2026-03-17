---
name: github-projects
description: GitHub Projects management via gh CLI for creating projects, managing items, fields, and workflows. Use when working with GitHub Projects (v2), adding issues/PRs to projects, creating custom fields, tracking project items, or automating project workflows. Triggers on gh project, project board, kanban, GitHub project, project items.
---

# GitHub Projects CLI

GitHub Projects (v2) management via `gh project` commands. Requires the `project` scope which can be added with `gh auth refresh -s project`.

## Prerequisites

Verify authentication includes project scope:

```bash
gh auth status  # Check current scopes
gh auth refresh -s project  # Add project scope if missing
```

## Quick Reference

### List & View Projects

```bash
# List your projects
gh project list

# List org projects (including closed)
gh project list --owner ORG_NAME --closed

# View project details
gh project view PROJECT_NUM --owner OWNER

# Open in browser
gh project view PROJECT_NUM --owner OWNER --web

# JSON output with jq filtering
gh project list --format json | jq '.projects[] | {number, title}'
```

### Create & Edit Projects

```bash
# Create project
gh project create --owner OWNER --title "Project Title"

# Edit project
gh project edit PROJECT_NUM --owner OWNER --title "New Title"
gh project edit PROJECT_NUM --owner OWNER --description "New description"
gh project edit PROJECT_NUM --owner OWNER --visibility PUBLIC

# Close/reopen project
gh project close PROJECT_NUM --owner OWNER
gh project close PROJECT_NUM --owner OWNER --undo  # Reopen
```

### Link Projects to Repos

```bash
# Link to repo
gh project link PROJECT_NUM --owner OWNER --repo REPO_NAME

# Link to team
gh project link PROJECT_NUM --owner ORG --team TEAM_NAME

# Unlink
gh project unlink PROJECT_NUM --owner OWNER --repo REPO_NAME
```

## Project Items

### Add Existing Issues/PRs

```bash
# Add issue to project
gh project item-add PROJECT_NUM --owner OWNER --url https://github.com/OWNER/REPO/issues/123

# Add PR to project
gh project item-add PROJECT_NUM --owner OWNER --url https://github.com/OWNER/REPO/pull/456
```

### Create Draft Items

```bash
gh project item-create PROJECT_NUM --owner OWNER --title "Draft item" --body "Description"
```

### List Items

```bash
# List items (default 30)
gh project item-list PROJECT_NUM --owner OWNER

# List more items
gh project item-list PROJECT_NUM --owner OWNER --limit 100

# JSON output
gh project item-list PROJECT_NUM --owner OWNER --format json
```

### Edit Items

Items are edited by their ID (obtained from `item-list --format json`).

```bash
# Edit draft issue title/body
gh project item-edit --id ITEM_ID --title "New Title" --body "New body"

# Update field value (requires field-id and project-id)
gh project item-edit --id ITEM_ID --project-id PROJECT_ID --field-id FIELD_ID --text "value"
gh project item-edit --id ITEM_ID --project-id PROJECT_ID --field-id FIELD_ID --number 42
gh project item-edit --id ITEM_ID --project-id PROJECT_ID --field-id FIELD_ID --date "2024-12-31"
gh project item-edit --id ITEM_ID --project-id PROJECT_ID --field-id FIELD_ID --single-select-option-id OPTION_ID
gh project item-edit --id ITEM_ID --project-id PROJECT_ID --field-id FIELD_ID --iteration-id ITER_ID

# Clear field value
gh project item-edit --id ITEM_ID --project-id PROJECT_ID --field-id FIELD_ID --clear
```

### Archive/Delete Items

```bash
gh project item-archive PROJECT_NUM --owner OWNER --id ITEM_ID
gh project item-delete PROJECT_NUM --owner OWNER --id ITEM_ID
```

## Project Fields

### List Fields

```bash
gh project field-list PROJECT_NUM --owner OWNER
gh project field-list PROJECT_NUM --owner OWNER --format json
```

### Create Fields

```bash
# Text field
gh project field-create PROJECT_NUM --owner OWNER --name "Notes" --data-type TEXT

# Number field
gh project field-create PROJECT_NUM --owner OWNER --name "Points" --data-type NUMBER

# Date field
gh project field-create PROJECT_NUM --owner OWNER --name "Due Date" --data-type DATE

# Single select with options
gh project field-create PROJECT_NUM --owner OWNER --name "Priority" \
  --data-type SINGLE_SELECT \
  --single-select-options "Low,Medium,High,Critical"
```

### Delete Fields

```bash
gh project field-delete --id FIELD_ID
```

## Common Workflows

### Add Issue and Set Status

```bash
# 1. Add issue to project
gh project item-add 1 --owner "@me" --url https://github.com/owner/repo/issues/123

# 2. Get item ID and field IDs
gh project item-list 1 --owner "@me" --format json | jq '.items[-1]'
gh project field-list 1 --owner "@me" --format json

# 3. Update status field
gh project item-edit --id ITEM_ID --project-id PROJECT_ID \
  --field-id STATUS_FIELD_ID --single-select-option-id OPTION_ID
```

### Bulk Add Issues

```bash
# Add all open issues from a repo
gh issue list --repo owner/repo --state open --json url -q '.[].url' | \
  xargs -I {} gh project item-add 1 --owner "@me" --url {}
```

## JSON Output & jq Patterns

```bash
# Get project IDs
gh project list --format json | jq '.projects[] | {number, id, title}'

# Get field IDs and options
gh project field-list 1 --owner "@me" --format json | jq '.fields[] | {id, name, options}'

# Get item IDs with field values
gh project item-list 1 --owner "@me" --format json | jq '.items[] | {id, title, fieldValues}'

# Filter items by status
gh project item-list 1 --owner "@me" --format json | \
  jq '.items[] | select(.status == "In Progress")'
```

## Reference Files

- **[items.md](references/items.md)**: Item management, editing field values, bulk operations
- **[fields.md](references/fields.md)**: Field types, creating custom fields, option management

## Command Summary

| Command | Purpose |
|---------|---------|
| `project list` | List projects |
| `project view` | View project details |
| `project create` | Create new project |
| `project edit` | Modify project settings |
| `project close` | Close/reopen project |
| `project link/unlink` | Connect to repo/team |
| `project item-add` | Add existing issue/PR |
| `project item-create` | Create draft item |
| `project item-list` | List project items |
| `project item-edit` | Update item fields |
| `project item-archive` | Archive item |
| `project item-delete` | Remove item |
| `project field-list` | List project fields |
| `project field-create` | Add custom field |
| `project field-delete` | Remove field |
