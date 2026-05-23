---
name: phab
description: Use phab CLI for Phabricator task management, code review workflows, revision creation and updates, with Git integration and auto-detection features.
---
# Phabricator CLI Skill

You are a Phabricator workflow specialist using the `phab` CLI tool. This skill provides comprehensive guidance for working with Phabricator tasks, revisions, diffs, and other operations from the command line.

## Core Capabilities

The `phab` CLI provides comprehensive Phabricator integration:

1. **Tasks**: Create, search, edit, comment, view task trees and edges (relationships)
2. **Revisions**: Create, update, search, view diffs and comments
3. **Projects**: Search and edit projects
4. **Users**: Search users and view current user info
5. **Repositories**: Search, edit, and manage repository URIs
6. **Diffs**: Search and view diff details
7. **MCP Server**: Integration with Model Context Protocol
8. **LSP**: Language Server Protocol for editor integration

## Task Operations

### Searching Tasks

```bash
# Search all tasks
phab task search

# Search specific task IDs
phab task search --ids T123,T456

# Filter by author
phab task search --author username

# Filter by assignee
phab task search --assigned username

# Filter by status
phab task search --status open
phab task search --status resolved

# Filter by priority
phab task search --priority high
phab task search --priority 100

# Filter by project
phab task search --project project-slug

# Full-text search
phab task search --query "bug in login"

# Date filters
phab task search --created-start 2025-01-01
phab task search --modified-end 2025-01-31

# Combine filters
phab task search --assigned myusername --status open --project backend

# Sort order
phab task search --order priority
phab task search --order updated
phab task search --order newest

# Limit results
phab task search --limit 20

# Output formats
phab task search --output json
phab task search --output jsonl
phab task search --output table
phab task search --output markdown  # Default

# Include attachments
phab task search --attach-projects
phab task search --attach-subscribers
```

### Creating Tasks

```bash
# Basic task creation
phab task create --title "Fix login bug"

# With description
phab task create --title "Add feature" --description "Detailed description here"

# With priority (default: 50)
phab task create --title "Urgent fix" --priority 100

# Assign owner
phab task create --title "New task" --owner username

# Set status
phab task create --title "Task" --status open

# Add to projects
phab task create --title "Task" --projects "backend,frontend"

# Complete example
phab task create \
  --title "Implement user authentication" \
  --description "Add OAuth2 support for user login" \
  --priority 80 \
  --owner developer \
  --projects "backend,security" \
  --status open
```

### Editing Tasks

```bash
# Edit task title
phab task edit T123 --title "New title"

# Edit description
phab task edit T123 --description "Updated description"

# Change priority
phab task edit T123 --priority 90

# Reassign owner
phab task edit T123 --owner newuser

# Change status
phab task edit T123 --status resolved

# Add projects
phab task edit T123 --add-projects "qa,testing"

# Remove projects
phab task edit T123 --remove-projects "deprecated"

# Multiple changes at once
phab task edit T123 \
  --title "Updated title" \
  --priority 100 \
  --status "in progress" \
  --add-projects "urgent"
```

### Viewing Tasks

```bash
# View task as markdown with YAML front matter
phab task view T123

# Without front matter
phab task view T123 --no-front-matter

# Show only transaction history
phab task view T123 --transactions-only

# Output as JSON
phab task view T123 --output-json
```

### Commenting on Tasks

```bash
# Add comment to task
phab task comment T123 --comment "This is fixed in D456"

# Multi-line comments (using heredoc)
phab task comment T123 --comment "$(cat <<'EOF'
This has been resolved.

Testing notes:
- Verified on staging
- All tests pass
EOF
)"
```

### Viewing Task Comments

```bash
# Get all comments for a task
phab task get-comments T123

# Output as JSON
phab task get-comments T123 --json
```

### Task Edges (Relationships)

Task edges represent relationships between tasks, such as parent/child, blocking/blocked by, and related tasks.

```bash
# View all edges (relationships) for a task
phab task edges T123

# Output as JSON for programmatic access
phab task edges T123 --json

# Common edge types returned:
# - parent: Tasks that this task is a subtask of
# - subtask: Child tasks under this task
# - depends-on: Tasks that must be completed before this task
# - blocks: Tasks that are blocked by this task
# - related: Related tasks
# - duplicate: Duplicate tasks
# - merged-into: Tasks this was merged into
```

**Use Cases:**

```bash
# Understanding task dependencies
phab task edges T123

# Finding all subtasks for planning
phab task edges T123 | grep "subtask"

# Checking blocking relationships
phab task edges T123 | grep "blocks\|depends-on"

# Programmatic processing
phab task edges T123 --json | jq '.edges[] | select(.type == "subtask")'

# Finding parent tasks in a hierarchy
phab task edges T123 --json | jq '.edges[] | select(.type == "parent")'

# Tracing duplicate relationships
phab task edges T123 --json | jq '.edges[] | select(.type == "duplicate")'
```

**Integration with Task Trees:**

Use `phab task edges` to see raw relationship data, while `phab task tree` provides a formatted hierarchical view:

```bash
# Raw relationship data (all edge types)
phab task edges T123

# Formatted tree view (parent/child only)
phab task tree T123
```

### Task Trees

```bash
# Display task tree (parent/child relationships)
phab task tree T123

# Shows hierarchy of related tasks
```

## Revision Operations

### Creating Revisions

```bash
# Create revision from current branch (auto-detects changes)
phab revision create

# Specify commit range
phab revision create HEAD~3..HEAD

# With explicit title
phab revision create --title "Add new feature"

# With summary/description
phab revision create --summary "This adds support for X"

# With test plan
phab revision create --test-plan "Tested manually on local dev"

# Add reviewers
phab revision create --reviewers "user1,user2,team-name"

# Create as draft (default)
phab revision create --draft

# Publish immediately
phab revision create --publish

# Specify base branch for fork-point detection
phab revision create --base origin/develop

# Open in browser after creating
phab revision create --browse

# Complete example
phab revision create \
  --title "Implement user authentication" \
  --summary "Adds OAuth2 support with token refresh" \
  --test-plan "Unit tests added, manual testing completed" \
  --reviewers "security-team,backend-lead" \
  --publish \
  --browse
```

### Updating Revisions

```bash
# Update revision (auto-detects from git config or commit message)
phab revision update

# Explicit revision ID
phab revision update D123
phab revision update 123

# Update title
phab revision update D123 --title "Updated title"

# Update summary
phab revision update D123 --summary "New description"

# Update test plan
phab revision update D123 --test-plan "Additional tests added"

# Replace reviewers (completely replaces the list)
phab revision update D123 --reviewers "user1,user2"

# Publish draft
phab revision update D123 --publish

# Specify base branch
phab revision update D123 --base origin/main

# Open in browser
phab revision update D123 --browse

# Complete example
phab revision update D123 \
  --title "Updated implementation" \
  --summary "Addressed review feedback" \
  --test-plan "All edge cases now covered" \
  --publish \
  --browse
```

### Searching Revisions

```bash
# Search all revisions
phab revision search

# Search specific revision IDs
phab revision search --ids D123,D456

# Filter by author
phab revision search --author username

# Filter by reviewer
phab revision search --reviewer username

# Filter by status
phab revision search --status "needs-review"
phab revision search --status accepted
phab revision search --status published

# Filter by repository
phab revision search --repository repo-name

# Date filters
phab revision search --created-start 2025-01-01
phab revision search --modified-end 2025-01-31

# Combine filters
phab revision search --author me --status "needs-review"

# Sort order
phab revision search --order updated
phab revision search --order newest
phab revision search --order created

# Limit results
phab revision search --limit 10

# Output formats
phab revision search --output markdown  # Default
phab revision search --output json
phab revision search --output table

# Include attachments
phab revision search --attach-projects
phab revision search --attach-reviewers
phab revision search --attach-subscribers
```

### Viewing Revision Diffs

```bash
# Get diff for a revision
phab revision diff D123

# Output as JSON
phab revision diff D123 --json
```

### Viewing Revision Comments

```bash
# Get all comments on a revision
phab revision comments D123

# Output as JSON
phab revision comments D123 --json
```

### Editing Revisions

```bash
# Edit revision metadata
phab revision edit D123 --title "New title"
phab revision edit D123 --summary "Updated description"

# Change status
phab revision edit D123 --status accepted
phab revision edit D123 --status abandoned

# Update reviewers
phab revision edit D123 --reviewers "user1,user2"
```

## Project Operations

### Searching Projects

```bash
# Search all projects
phab project search

# Search by name
phab project search --query "backend"

# Output as JSON
phab project search --json
```

### Editing Projects

```bash
# Edit project details
phab project edit PROJECT-SLUG --name "New Name"

# Output as JSON
phab project edit PROJECT-SLUG --json
```

## User Operations

### Searching Users

```bash
# Search all users
phab user search

# Search by username
phab user search --usernames "user1,user2"

# Output as JSON
phab user search --json
```

### Current User Info

```bash
# Get information about authenticated user
phab user whoami

# Output as JSON
phab user whoami --json
```

## Repository Operations

### Searching Repositories

```bash
# Search all repositories
phab repository search

# Search by name
phab repository search --query "backend"

# Output as JSON
phab repository search --json
```

### Repository URIs

```bash
# List URIs for a repository
phab repository uri REPO-NAME

# Output as JSON
phab repository uri REPO-NAME --json
```

## Common Workflows

### Workflow 1: Create and Submit Code Review

```bash
# 1. Make changes on feature branch
git checkout -b feature/new-thing
# ... make changes ...
git add .
git commit -m "Add new feature"

# 2. Create revision
phab revision create \
  --title "Add new feature" \
  --summary "Implements X, Y, and Z" \
  --test-plan "Tested locally, unit tests added" \
  --reviewers "team-backend" \
  --browse

# 3. Address review feedback
# ... make more changes ...
git add .
git commit -m "Address review feedback"

# 4. Update revision
phab revision update --publish

# 5. After approval, land the revision
# (typically done through Phabricator UI or arc land)
```

### Workflow 2: Review Pending Revisions

```bash
# 1. Find revisions needing review
phab revision search --reviewer me --status "needs-review"

# 2. View specific revision diff
phab revision diff D123

# 3. View comments
phab revision comments D123

# 4. After reviewing (use web UI for acceptance)
```

### Workflow 3: Track Task Progress

```bash
# 1. Find your assigned tasks
phab task search --assigned me --status open

# 2. View task details
phab task view T123

# 3. Comment on progress
phab task comment T123 --comment "Working on this now"

# 4. Update status
phab task edit T123 --status "in progress"

# 5. When done
phab task edit T123 --status resolved --comment "Completed in D456"
```

### Workflow 4: Create Task from Bug Report

```bash
# 1. Create task
phab task create \
  --title "Bug: Login fails with special characters" \
  --description "Users report login failures when password contains @#$" \
  --priority 90 \
  --projects "bugs,backend,urgent" \
  --owner me

# 2. Get task ID (e.g., T789)

# 3. Create branch
git checkout -b fix/login-special-chars

# 4. Fix the bug and create revision
# ... make changes ...
phab revision create \
  --title "Fix login with special characters" \
  --summary "Fixes T789 - properly escape special characters" \
  --test-plan "Added unit tests for special character passwords"

# 5. Link revision to task
phab task comment T789 --comment "Fix available in D456"
```

### Workflow 5: Find Related Work

```bash
# 1. Search tasks in a project
phab task search --project backend --status open

# 2. Find recent revisions by author
phab revision search --author colleague --order updated --limit 5

# 3. View task tree to see related tasks
phab task tree T123

# 4. Check repository activity
phab revision search --repository main-repo --order updated --limit 10
```

### Workflow 6: Monitor Project Activity

```bash
# 1. Find recent tasks in project
phab task search \
  --project myproject \
  --order updated \
  --limit 20

# 2. Find active revisions
phab revision search \
  --repository myrepo \
  --status "needs-review" \
  --order updated

# 3. Check high-priority tasks
phab task search \
  --project myproject \
  --priority high \
  --status open
```

## Output Formats

### Markdown Format (Default)

Most commands default to markdown tables for human-readable output:

```bash
phab task search --assigned me
# Outputs nicely formatted markdown table
```

### JSON Format

For programmatic processing:

```bash
phab task search --assigned me --output json | jq '.data[].fields.name'
```

### JSON Lines Format

One JSON object per line:

```bash
phab revision search --output jsonl | while read line; do
  echo "$line" | jq '.id'
done
```

### Table Format

Compact table view:

```bash
phab task search --output table
```

## Best Practices

### Task Management

1. **Use descriptive titles**: Make tasks searchable
2. **Add to projects**: Organize work properly
3. **Set appropriate priority**: Default is 50
4. **Assign ownership**: Clear responsibility
5. **Update status**: Keep team informed
6. **Comment regularly**: Document progress

### Revision Workflow

1. **Create from feature branch**: Keep main clean
2. **Write good summaries**: Explain what and why
3. **Include test plan**: Help reviewers understand testing
4. **Add appropriate reviewers**: Get right expertise
5. **Use draft for WIP**: Publish when ready for review
6. **Update regularly**: Don't let reviews go stale

### Search Best Practices

1. **Use filters**: Narrow results with --status, --project, etc.
2. **Limit results**: Use --limit for large result sets
3. **Sort appropriately**: --order updated for recent work
4. **Attach data selectively**: Only use --attach-* when needed
5. **Use output formats**: JSON for scripts, markdown for viewing

## Integration with Git Workflow

### Typical Development Flow

```bash
# 1. Create feature branch
git checkout -b feature/new-thing

# 2. Make commits
git add .
git commit -m "Implement feature"

# 3. Create Phabricator revision
phab revision create \
  --title "Add new feature" \
  --reviewers "team-name"

# 4. Address feedback
git add .
git commit -m "Address review feedback"

# 5. Update revision
phab revision update

# 6. After approval, land via Phabricator
# (or use arc land if using Arcanist)
```

### Auto-detection Features

The `phab` CLI includes smart auto-detection:

**For revisions:**
- Detects fork point from main/master branch
- Reads commit messages for title/summary
- Finds existing revision ID from git config or commit messages
- Auto-detects base branch (origin/master by default)

**For tasks:**
- Parses task IDs from commit messages
- Links revisions to tasks automatically

## Advanced Features

### Fork-Point Detection

```bash
# Auto-detects where your branch diverged from main
phab revision create

# Specify different base branch
phab revision create --base origin/develop

# Explicit commit range (overrides fork-point detection)
phab revision create HEAD~5..HEAD
```

### Browser Integration

```bash
# Open in browser after creating
phab revision create --browse

# Open after updating
phab revision update --browse
```

### Pagination

For large result sets:

```bash
# Get first page
phab task search --limit 100

# Get next page using cursor
phab task search --after <cursor-from-previous-response>

# Previous page
phab task search --before <cursor>
```

### Raw API Output

For debugging or advanced use:

```bash
# Get complete API response without trimming
phab task search --raw
```

## Common Patterns

### Pattern 1: Daily Standup Prep

```bash
# What I'm working on
phab task search --assigned me --status open --order priority

# My pending reviews
phab revision search --author me --status "needs-review"

# Reviews I need to do
phab revision search --reviewer me --status "needs-review"
```

### Pattern 2: Project Health Check

```bash
# Open tasks
phab task search --project myproject --status open --order priority

# Active revisions
phab revision search --repository myrepo --status "needs-review"

# Recent activity
phab task search --project myproject --order updated --limit 10
```

### Pattern 3: Bug Triage

```bash
# All open bugs
phab task search --project bugs --status open --order priority

# High priority bugs
phab task search --project bugs --priority high --status open

# Unassigned bugs
phab task search --project bugs --status open | grep "Unassigned"
```

### Pattern 4: Code Review Queue

```bash
# Find reviews awaiting my feedback
phab revision search --reviewer me --status "needs-review" --order updated

# My revisions needing updates
phab revision search --author me --status "needs-revision" --order updated

# Accepted but not landed
phab revision search --author me --status accepted --order updated
```

### Pattern 5: Linking Work

```bash
# Create task for feature
TASK_ID=$(phab task create --title "Feature X" --json | jq -r '.object.id')

# Create revision mentioning task
phab revision create --summary "Implements $TASK_ID"

# Comment on task with revision
phab task comment $TASK_ID --comment "Implementation in D123"
```

## Configuration

The `phab` CLI typically uses configuration from:
- `~/.arcrc` (Arcanist config)
- Environment variables
- Project-specific `.arcconfig`

### Required Configuration

Ensure you have:
1. Phabricator API token configured
2. Proper authentication set up
3. Repository callsign/PHID mapping (for revision operations)

## Troubleshooting

### Issue: "Not authenticated"

**Solution**: Configure API token in `~/.arcrc` or environment variables

### Issue: "Repository not found"

**Solution**: Ensure repository is configured in Phabricator and callsign is correct

### Issue: "Cannot detect fork point"

**Solution**: Specify explicit commit range or base branch:
```bash
phab revision create --base origin/main
phab revision create HEAD~3..HEAD
```

### Issue: "Revision not found when updating"

**Solution**: Specify explicit revision ID:
```bash
phab revision update D123
```

## Quick Reference

```bash
# Tasks
phab task search --assigned me --status open
phab task create --title "Title" --description "Desc"
phab task edit T123 --status resolved
phab task comment T123 --comment "Comment"
phab task view T123
phab task edges T123
phab task tree T123

# Revisions
phab revision create --title "Title" --reviewers "team"
phab revision update D123 --publish
phab revision search --author me --status "needs-review"
phab revision diff D123
phab revision comments D123

# Projects
phab project search --query "name"

# Users
phab user search
phab user whoami

# Repositories
phab repository search --query "name"
phab repository uri REPO-NAME
```

## Integration with Phabricator Ticket Writer Agent

When creating tasks programmatically, you can use the phabricator-ticket-writer agent for well-structured task creation with proper formatting.

## Summary

**Primary commands:**
- `phab task search` - Find tasks
- `phab task create` - Create new task
- `phab revision create` - Submit code for review
- `phab revision update` - Update existing review
- `phab revision search` - Find revisions

**Key features:**
- Auto-detection of branches and changes
- Multiple output formats (markdown, JSON, table)
- Rich filtering and search capabilities
- Git workflow integration
- Browser integration with --browse flag

**Best practices:**
- Use descriptive titles and summaries
- Include test plans in revisions
- Keep tasks organized in projects
- Update work regularly
- Link related tasks and revisions
