---
description: Quick reference for Backlog.md CLI with critical file naming rules and workflow patterns
disable-model-invocation: false
---

# Backlog.md CLI Quick Reference Skill

## 🚨 CRITICAL: File Naming Convention

**Sacred Pattern**: `task-{id} - {title}.md`

### Examples
✅ `task-1 - Initial setup.md`
✅ `task-42 - Add authentication.md`
✅ `task-137 - Refactor API endpoints.md`

❌ `task-42-Add authentication.md` (missing spaces)
❌ `task42 - Title.md` (missing hyphen)
❌ `Add authentication.md` (missing task ID)
❌ `task-42.md` (missing title)

### Why This Matters

- CLI parses filenames to extract task ID and title
- Git tracking relies on consistent naming
- Metadata synchronization depends on format
- Breaking this format breaks Backlog.md functionality

### Golden Rule

**NEVER** manually create, rename, or edit task files.
**ALWAYS** use `backlog task create` and `backlog task edit`.

---

## Overview

Backlog.md is a comprehensive CLI tool for managing project tasks, acceptance criteria, and documentation. All task modifications MUST use CLI commands.

**Reference Guide**: For complete documentation, see `docs/backlog-md-cli-usage.md` in this plugin

---

## Quick Start

### Viewing Tasks
```bash
backlog task list --plain              # List all tasks
backlog task 42 --plain                # View specific task
backlog search "keyword" --plain       # Search for tasks
```

### Creating Tasks
```bash
# Basic task
backlog task create "Task title" -d "Description"

# With acceptance criteria
backlog task create "Title" -d "Desc" --ac "AC 1" --ac "AC 2"

# With all options
backlog task create "Title" -d "Desc" -a @sara -s "To Do" -l backend,api --priority high
```

### Working on a Task
```bash
# Start working on a task
backlog task edit 42 -s "In Progress" -a @myself

# Add implementation plan
backlog task edit 42 --plan $'1. Research\n2. Implement\n3. Test'

# Mark acceptance criteria complete (supports multiple)
backlog task edit 42 --check-ac 1 --check-ac 2 --check-ac 3

# Add implementation notes
backlog task edit 42 --notes "Implemented using pattern X because Y"

# Mark as done
backlog task edit 42 -s Done
```

---

## Essential Commands

### Editing Tasks

| What                | Command |
|---------------------|---------|
| Change status       | `backlog task edit 42 -s "In Progress"` |
| Assign task         | `backlog task edit 42 -a @sara` |
| Edit description    | `backlog task edit 42 -d "New description"` |
| Edit title          | `backlog task edit 42 -t "New Title"` |
| Add labels          | `backlog task edit 42 -l backend,api` |
| Set priority        | `backlog task edit 42 --priority high` |

### Acceptance Criteria (AC)

| What                | Command |
|---------------------|---------|
| Add AC              | `backlog task edit 42 --ac "New criterion"` |
| Add multiple AC     | `backlog task edit 42 --ac "First" --ac "Second"` |
| Check AC #1         | `backlog task edit 42 --check-ac 1` |
| Check multiple AC   | `backlog task edit 42 --check-ac 1 --check-ac 2` |
| Uncheck AC #2       | `backlog task edit 42 --uncheck-ac 2` |
| Remove AC #3        | `backlog task edit 42 --remove-ac 3` |
| Mixed ops           | `backlog task edit 42 --check-ac 1 --uncheck-ac 2 --ac "New"` |

### Implementation Planning & Notes

| What                | Command |
|---------------------|---------|
| Add plan            | `backlog task edit 42 --plan $'1. Step 1\n2. Step 2'` |
| Add notes           | `backlog task edit 42 --notes "Implementation details"` |
| Append notes        | `backlog task edit 42 --append-notes "Additional note"` |

### Searching & Filtering

| What                | Command |
|---------------------|---------|
| Search tasks        | `backlog search "auth" --plain` |
| Filter by status    | `backlog task list -s "To Do" --plain` |
| Filter by assignee  | `backlog task list -a @sara --plain` |
| Search type filter  | `backlog search "api" --type task --plain` |

---

## Multi-line Input Tips

For descriptions, plans, and notes with multiple lines, use Bash ANSI-C quoting:

```bash
# Example with newlines
backlog task edit 42 --plan $'1. Research\n2. Implement\n3. Test'

# Multi-paragraph notes
backlog task edit 42 --notes $'Implemented feature X\n\nAdded comprehensive tests\nUpdated documentation'
```

---

## Workflow Example

```bash
# 1. Create a task
backlog task create "Add user authentication" \
  -d "Implement login/logout functionality" \
  --ac "Login with valid credentials" \
  --ac "Session persists across page reloads" \
  --ac "Logout clears session"

# 2. Start working (assuming task ID is 42)
backlog task edit 42 -s "In Progress" -a @myself

# 3. Add implementation plan
backlog task edit 42 --plan $'1. Research auth patterns\n2. Implement login endpoint\n3. Add session management\n4. Write tests'

# 4. During implementation, check off ACs as you complete them
backlog task edit 42 --check-ac 1

# 5. When done, add implementation notes
backlog task edit 42 --notes "Implemented JWT-based auth with HTTP-only cookies for security"

# 6. Mark all remaining ACs complete
backlog task edit 42 --check-ac 2 --check-ac 3

# 7. Mark task as done
backlog task edit 42 -s Done
```

---

## Definition of Done Checklist

A task is Done only when ALL of these are complete:

- [ ] All acceptance criteria checked via CLI (`--check-ac`)
- [ ] Implementation notes added via CLI (`--notes`)
- [ ] Status set to "Done" via CLI (`-s Done`)
- [ ] Tests pass and linting checks pass
- [ ] Documentation updated if needed
- [ ] Code reviewed
- [ ] No regressions detected

---

## Golden Rules

1. **Never edit task files directly** - Use CLI commands only
2. **Always use `--plain` flag** when listing/viewing tasks
3. **Mark ACs as you complete them** - Don't wait until the end
4. **Share implementation plans with user** before coding
5. **Use newlines in descriptions/plans/notes** for readability
6. **Respect the naming pattern** - `task-{id} - {title}.md`

---

## Task Status Flow

- New task → "To Do"
- Starting work → "In Progress" (+ assign yourself)
- Work complete → "Done" (all ACs checked, notes added)

---

## Acceptance Criteria Strategy

- **Outcome-focused** - What does the user/system do, not implementation details
- **Testable** - Can be objectively verified
- **Independent** - Each AC is a unit of work
- **Complete** - Together they define the full task scope

### Good ACs (outcome-focused)
- "User can log in with valid credentials"
- "System returns 404 for non-existent resources"

### Bad ACs (implementation-focused)
- "Add login() function to auth.ts"
- "Use bcrypt for password hashing"

---

## Notes Format (PR Description Style)

```
- Outcome: What was implemented
- Implementation: How it was done and why
- Testing: What was tested
- Follow-up: Any next steps or known issues
```

---

## Common Patterns

### DO vs DON'T

| Task          | ✅ DO                                 | ❌ DON'T                           |
|---------------|--------------------------------------|-----------------------------------|
| View task     | `backlog task 42 --plain`            | Read .md file directly            |
| Check AC      | `backlog task edit 42 --check-ac 1`  | Change `- [ ]` to `- [x]` in file |
| Add notes     | `backlog task edit 42 --notes "..."` | Type notes into .md file          |
| Change status | `backlog task edit 42 -s Done`       | Edit status in frontmatter        |

---

## Full Documentation

For complete documentation including all options and advanced features:
```bash
# Read comprehensive guide
cat docs/backlog-md-cli-usage.md

# CLI help
backlog --help
```
