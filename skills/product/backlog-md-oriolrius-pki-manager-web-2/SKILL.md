---
name: Backlog.md
description: Expert guidance for Backlog.md CLI project management tool including task creation, editing, status management, acceptance criteria, search, and board visualization. Use this when managing project tasks, creating task lists, updating task status, or organizing project work.
---

# Backlog.md

Expert assistance with Backlog.md CLI project management tool.

## Overview

Backlog.md is a CLI-based project management tool that uses markdown files to track tasks, documentation, and decisions. All operations go through the `backlog` CLI command.

**Key Principle**: NEVER edit task files directly. Always use CLI commands.

## Quick Start

```bash
# List tasks
backlog task list --plain

# View task details
backlog task 42 --plain

# Create task
backlog task create "Task title" -d "Description" --ac "Acceptance criterion"

# Edit task
backlog task edit 42 -s "In Progress" -a @me

# Search
backlog search "keyword" --plain
```

## Task Creation

### Basic Task Creation
```bash
# Simple task
backlog task create "Implement user login"

# With description
backlog task create "Implement user login" -d "Add authentication flow"

# With acceptance criteria
backlog task create "Implement user login" \
  --ac "User can login with email and password" \
  --ac "Invalid credentials show error message"

# Complete task creation
backlog task create "Implement user login" \
  -d "Add authentication flow with session management" \
  --ac "User can login with valid credentials" \
  --ac "Session persists across page refreshes" \
  -s "To Do" \
  -a @developer \
  -l backend,auth \
  --priority high
```

### Advanced Creation
```bash
# Create draft task
backlog task create "Research options" --draft

# Create subtask
backlog task create "Implement feature component" -p 42

# With dependencies
backlog task create "Deploy to production" --dep task-40 --dep task-41

# With multiple labels
backlog task create "Fix bug" -l bug,urgent,frontend
```

## Task Modification

### Status Management
```bash
# Change status
backlog task edit 42 -s "In Progress"
backlog task edit 42 -s "Done"
backlog task edit 42 -s "Blocked"

# Common workflow: start work on task
backlog task edit 42 -s "In Progress" -a @me
```

### Basic Fields
```bash
# Update title
backlog task edit 42 -t "New title"

# Update description (with newlines)
backlog task edit 42 -d $'Multi-line\ndescription\nhere'

# Assign task
backlog task edit 42 -a @username

# Add/update labels
backlog task edit 42 -l backend,api,v2

# Set priority
backlog task edit 42 --priority high
backlog task edit 42 --priority medium
backlog task edit 42 --priority low
```

### Acceptance Criteria Management

**IMPORTANT**: Each flag accepts multiple values

```bash
# Add new criteria (multiple flags supported)
backlog task edit 42 --ac "User can login" --ac "Session persists"

# Check criteria by index (multiple flags supported)
backlog task edit 42 --check-ac 1 --check-ac 2 --check-ac 3

# Uncheck criteria
backlog task edit 42 --uncheck-ac 2

# Remove criteria (processed high-to-low)
backlog task edit 42 --remove-ac 3 --remove-ac 2

# Mixed operations in one command
backlog task edit 42 \
  --check-ac 1 \
  --uncheck-ac 2 \
  --remove-ac 4 \
  --ac "New criterion"
```

**Note**:
- ✅ Use multiple flags: `--check-ac 1 --check-ac 2`
- ❌ Don't use commas: `--check-ac 1,2,3`
- ❌ Don't use ranges: `--check-ac 1-3`

### Implementation Plan & Notes

```bash
# Add implementation plan (with newlines using ANSI-C quoting)
backlog task edit 42 --plan $'1. Research codebase\n2. Implement solution\n3. Write tests\n4. Update docs'

# POSIX portable (using printf)
backlog task edit 42 --plan "$(printf '1. Step one\n2. Step two')"

# Add implementation notes (replaces existing)
backlog task edit 42 --notes $'Implemented using strategy pattern\nUpdated all tests\nReady for review'

# Append to existing notes
backlog task edit 42 --append-notes $'- Fixed edge case\n- Added validation'

# Format notes as PR description (best practice)
backlog task edit 42 --notes $'## Changes\n- Implemented X\n- Fixed Y\n\n## Testing\n- Added unit tests\n- Manual testing complete'
```

### Dependencies
```bash
# Add dependencies
backlog task edit 42 --dep task-1 --dep task-2

# Remove dependencies (edit task file or recreate without)
```

## Viewing Tasks

### List Tasks
```bash
# List all tasks (always use --plain for AI-readable output)
backlog task list --plain

# Filter by status
backlog task list -s "To Do" --plain
backlog task list -s "In Progress" --plain
backlog task list -s "Done" --plain

# Filter by assignee
backlog task list -a @username --plain
backlog task list -a @me --plain

# Filter by tag
backlog task list --tag backend --plain
backlog task list --tag bug --plain

# Combined filters
backlog task list -s "In Progress" -a @me --plain
```

### View Task Details
```bash
# View single task (always use --plain)
backlog task 42 --plain

# View in browser (if supported)
backlog task 42 --web
```

### Search
```bash
# Search across all content (uses fuzzy matching)
backlog search "authentication" --plain

# Search only tasks
backlog search "login" --type task --plain

# Search with filters
backlog search "api" --status "To Do" --plain
backlog search "bug" --priority high --plain

# Search in specific fields
backlog search "database" --in title --plain
```

## Task Workflow

### Complete Task Lifecycle
```bash
# 1. Create task
backlog task create "Implement feature X" \
  -d "Add new feature to handle Y" \
  --ac "Feature works as expected" \
  --ac "Tests are passing" \
  --ac "Documentation is updated"

# 2. Start work: assign and change status
backlog task edit 42 -s "In Progress" -a @me

# 3. Add implementation plan
backlog task edit 42 --plan $'1. Research existing code\n2. Implement core logic\n3. Add tests\n4. Update docs'

# 4. Work on task (write code, test, etc.)

# 5. Mark acceptance criteria as complete
backlog task edit 42 --check-ac 1 --check-ac 2 --check-ac 3

# 6. Add implementation notes (PR description)
backlog task edit 42 --notes $'## Changes\n- Implemented feature X using approach Y\n- Added comprehensive tests\n\n## Testing\n- Unit tests pass\n- Integration tests pass\n- Manual testing complete'

# 7. Mark task as done
backlog task edit 42 -s Done
```

### Starting a Task (Critical Steps)
```bash
# ALWAYS do these steps when starting a task:
# 1. Set status to In Progress
# 2. Assign to yourself
backlog task edit 42 -s "In Progress" -a @me

# 3. Review the task requirements
backlog task 42 --plain

# 4. Create implementation plan
backlog task edit 42 --plan $'1. Analyze requirements\n2. Design solution\n3. Implement\n4. Test\n5. Document'
```

## Board & Visualization

```bash
# View Kanban board in terminal
backlog board

# Open web UI
backlog browser

# Export board snapshot
backlog board --export board-snapshot.md

# Generate report
backlog report --output report.md
```

## Task Operations

### Archive & Promote
```bash
# Archive completed task
backlog task archive 42

# Demote task to draft
backlog task demote 42

# Promote draft to task (gets new ID)
backlog task promote draft-5
```

### Task History
```bash
# View task history (if supported)
backlog task history 42

# View changes
backlog task diff 42
```

## Documentation & Decisions

### Documents
```bash
# Create document
backlog doc create "API Documentation"

# List documents
backlog doc list --plain

# Edit document
backlog doc edit 1 --content "Updated content"
```

### Architectural Decisions
```bash
# Create decision record
backlog decision create "Use PostgreSQL for data storage"

# List decisions
backlog decision list --plain

# View decision
backlog decision 1 --plain
```

## Best Practices

### Writing Good Tasks

**Title**: Clear, concise, action-oriented
```bash
# ✅ Good
backlog task create "Implement user authentication"
backlog task create "Fix memory leak in image processor"

# ❌ Bad
backlog task create "Users"
backlog task create "There's a problem with the app"
```

**Description**: Explain the "why" and context
```bash
backlog task create "Add rate limiting to API" \
  -d "Current API has no rate limiting, causing server overload during peak hours. Need to implement per-user rate limiting to prevent abuse."
```

**Acceptance Criteria**: Focus on outcomes, not implementation
```bash
# ✅ Good - Testable outcomes
--ac "API rejects requests after 100 requests per minute per user"
--ac "User receives clear error message when rate limited"
--ac "Rate limit resets after 60 seconds"

# ❌ Bad - Implementation details
--ac "Add a rate limiter middleware"
--ac "Use Redis for tracking"
```

### Task Organization

**Use Labels Effectively**
```bash
# Organize by type, area, and priority
backlog task create "Fix login bug" -l bug,urgent,auth
backlog task create "Optimize queries" -l enhancement,backend,performance
backlog task create "Update docs" -l documentation,frontend
```

**Use Tags for Metadata**
```bash
# Tags for filtering and organization
--tag "sprint:23"
--tag "epic:user-management"
--tag "team:backend"
```

### Task Breakdown

**Atomic Tasks**: Each task should be independently deliverable
```bash
# ✅ Good - One PR per task
backlog task create "Add login endpoint"
backlog task create "Add logout endpoint"
backlog task create "Add session refresh endpoint"

# ❌ Bad - Too large for one PR
backlog task create "Implement entire authentication system"
```

**Avoid Future Dependencies**: Never reference tasks that don't exist yet
```bash
# ✅ Good - Reference existing tasks
backlog task create "Deploy auth API" --dep task-40 --dep task-41

# ❌ Bad - Reference future tasks
backlog task create "Add feature A" -d "This will be used by future tasks"
```

### Implementation Notes

**Format as PR Description**: Make notes ready for GitHub
```bash
backlog task edit 42 --notes $'## Summary
- Implemented user authentication with JWT
- Added password hashing with bcrypt
- Created login/logout endpoints

## Changes
- Added auth middleware
- Updated user model
- Added auth routes

## Testing
- Unit tests for auth functions
- Integration tests for endpoints
- Manual testing with Postman

## Breaking Changes
None

## Follow-up
- Add refresh token rotation
- Implement rate limiting'
```

**Progressive Notes**: Append as you work
```bash
# As you make progress
backlog task edit 42 --append-notes "- Implemented core auth logic"
backlog task edit 42 --append-notes "- Added tests"
backlog task edit 42 --append-notes "- Updated documentation"
```

## Definition of Done

**A task is Done only when ALL of these are complete:**

Via CLI:
1. ✅ All acceptance criteria checked: `--check-ac 1 --check-ac 2 ...`
2. ✅ Implementation notes added: `--notes "..."`
3. ✅ Status set to Done: `-s Done`

Via Code/Testing:
4. ✅ Tests pass
5. ✅ Documentation updated
6. ✅ Code reviewed
7. ✅ No regressions

**Never mark task as Done without completing ALL items**

## Common Patterns

### Daily Workflow
```bash
# Morning: Check your tasks
backlog task list -a @me -s "In Progress" --plain

# Start working on next task
backlog task edit 42 -s "In Progress" -a @me
backlog task 42 --plain  # Read requirements

# Add plan
backlog task edit 42 --plan $'1. Analyze\n2. Implement\n3. Test'

# As you work, check off AC
backlog task edit 42 --check-ac 1
# ... continue working ...
backlog task edit 42 --check-ac 2

# End of day: Add notes
backlog task edit 42 --append-notes "- Completed X, Y pending"
```

### Sprint Planning
```bash
# Review backlog
backlog task list -s "To Do" --plain

# Tag tasks for sprint
backlog task edit 42 --tag "sprint:23"
backlog task edit 43 --tag "sprint:23"

# Assign tasks
backlog task edit 42 -a @developer1
backlog task edit 43 -a @developer2

# View sprint board
backlog board
```

### Bug Fix Workflow
```bash
# Create bug task
backlog task create "Fix login timeout issue" \
  -d "Users report login times out after 30 seconds on slow connections" \
  --ac "Login works on slow connections (tested with throttling)" \
  --ac "Timeout increased to 60 seconds" \
  --ac "User sees loading indicator during login" \
  -l bug,urgent,auth \
  --priority high

# Start work
backlog task edit 42 -s "In Progress" -a @me

# Implement fix and add notes
backlog task edit 42 --notes $'## Root Cause
Login timeout was set to 30s, causing issues on slow connections.

## Fix
- Increased timeout to 60s
- Added exponential backoff for retries
- Improved loading indicator visibility

## Testing
- Tested with Chrome network throttling (Slow 3G)
- Verified timeout works correctly
- All existing auth tests pass'

# Complete
backlog task edit 42 --check-ac 1 --check-ac 2 --check-ac 3
backlog task edit 42 -s Done
```

## Troubleshooting

### Task Not Found
```bash
# List all tasks to find ID
backlog task list --plain

# Search for task
backlog search "keyword" --type task --plain
```

### Acceptance Criteria Issues
```bash
# View task to see AC numbers
backlog task 42 --plain

# AC numbering starts at 1
backlog task edit 42 --check-ac 1  # First AC

# Check multiple at once
backlog task edit 42 --check-ac 1 --check-ac 2 --check-ac 3
```

### Metadata Out of Sync
```bash
# Re-edit via CLI to fix
backlog task edit 42 -s "In Progress"

# If persistent, check file permissions
ls -la backlog/tasks/
```

### Multiline Input
```bash
# Use ANSI-C quoting (bash/zsh)
backlog task edit 42 --notes $'Line 1\nLine 2'

# Use printf (POSIX portable)
backlog task edit 42 --notes "$(printf 'Line 1\nLine 2')"

# PowerShell
backlog task edit 42 --notes "Line 1`nLine 2"

# Don't use literal \n - it won't work
# ❌ backlog task edit 42 --notes "Line 1\nLine 2"
```

## Command Reference

### Core Commands
```bash
# Tasks
backlog task create <title> [options]
backlog task list [filters] --plain
backlog task <id> --plain
backlog task edit <id> [options]
backlog task archive <id>
backlog task demote <id>

# Search
backlog search <query> [filters] --plain

# Board & Reports
backlog board
backlog browser
backlog report --output <file>

# Documents
backlog doc create <title>
backlog doc list --plain
backlog doc edit <id>

# Decisions
backlog decision create <title>
backlog decision list --plain
backlog decision <id> --plain
```

### Common Options
```bash
# Task creation/editing
-t, --title           Task title
-d, --description     Task description
-s, --status          Status (To Do, In Progress, Done, Blocked)
-a, --assignee        Assignee (@username)
-l, --labels          Comma-separated labels
--priority            Priority (low, medium, high)
--ac                  Add acceptance criterion
--check-ac            Check AC by index
--uncheck-ac          Uncheck AC by index
--remove-ac           Remove AC by index
--plan                Implementation plan
--notes               Implementation notes
--append-notes        Append to notes
--dep                 Add dependency (task-id)
--draft               Create as draft
-p, --parent          Parent task ID

# Filters
--plain               Plain text output (AI-friendly)
--status              Filter by status
--assignee            Filter by assignee
--tag                 Filter by tag
--priority            Filter by priority
--type                Filter by type (task, doc, decision)
```

## Tips

1. **Always use `--plain`** when listing or viewing for AI processing
2. **Start tasks properly**: Set In Progress and assign to yourself
3. **Check AC as you go**: Don't wait until end to mark them complete
4. **Use multiline properly**: Use `$'...\n...'` syntax for newlines
5. **Multiple flags work**: `--check-ac 1 --check-ac 2 --check-ac 3`
6. **Organize with labels**: Use consistent labeling scheme
7. **Atomic tasks**: One PR = One task
8. **PR-ready notes**: Format notes as GitHub PR description
9. **Never edit files directly**: Always use CLI commands
10. **Search is fuzzy**: "auth" finds "authentication"

## Integration with Git

```bash
# Workflow
git checkout -b task-42-implement-feature
# ... implement task 42 ...
backlog task edit 42 --check-ac 1 --check-ac 2
backlog task edit 42 --notes "Implementation complete"
backlog task edit 42 -s Done
git add .
git commit -m "Implement feature X

Refs: task-42"
git push
```

## Remember

**🎯 Golden Rule**: Always use CLI commands. Never edit markdown files directly.

**📋 Task Quality**: Good AC = Testable outcomes, not implementation steps.

**✅ Definition of Done**: All AC checked + notes + tests passing + status Done.
