---
name: create-task-files
description: Export tasks from TodoWrite or feature plans into structured markdown files (epic, user-story, bug, issue) in a tasks/ directory. Use when the user wants to create task files, export tasks, track work in files, or mentions "create tasks", "export", "epic", "user story".
allowed-tools: Read, Write, Glob, AskUserQuestion, Bash
---

# Create Task Files Skill

Export planning tasks into structured, trackable markdown files organized by type (epic, user-story, bug, issue) in a `tasks/` directory. Integrates with git-based workflows for team collaboration.

## When to Use This Skill

Use this skill when:
- User wants to export TodoWrite tasks to files
- After completing `/plan-feature` and user wants task tracking
- User mentions "create tasks", "export tasks", "epic", "user story"
- Setting up project tracking in markdown files
- Need to track bugs or issues in files

## Task Types

This skill supports four task types:

| Type | Purpose | Example |
|------|---------|---------|
| **epic** | Large feature or initiative spanning multiple stories | "User Authentication System" |
| **user-story** | Single deliverable piece of functionality | "User can login with email/password" |
| **bug** | Defect or issue to fix | "Login form doesn't validate email format" |
| **issue** | General task, chore, or technical debt | "Refactor authentication controller" |

## Instructions

Follow these steps when creating task files:

### Step 1: Determine Task Source

Check if there are active TodoWrite tasks:

1. Ask the user: "I can create task files from your current todo list or from a feature description. Which would you prefer?"
2. If using todo list, analyze the current tasks
3. If using feature description, ask for the feature details

### Step 2: Gather Task Configuration

Use AskUserQuestion to ask:

**Question 1: Task Types**
- Which task types to create?
- Options: "All types (epic + stories)", "User stories only", "Custom selection"

**Question 2: Grouping Strategy**
- How to group tasks?
- Options: "By implementation layer (DB, Logic, UI, Tests)", "By feature area", "Chronological order"

**Question 3: Metadata**
- What additional metadata?
- Options: "Priority + Labels", "Just basics", "Full metadata (assignee, estimates)"

### Step 3: Create Tasks Directory

Create the directory structure:

```bash
mkdir -p tasks
```

Check if `tasks/README.md` exists. If not, create it with:

```markdown
# Project Tasks

This directory contains structured task tracking files for features, bugs, and issues.

## Task Types

- **epic-XXX**: Large features or initiatives
- **story-XXX**: User stories and deliverable functionality
- **bug-XXX**: Defects and issues to fix
- **issue-XXX**: General tasks, chores, technical debt

## Workflow

1. Tasks are created from feature planning
2. Update task status as work progresses
3. Check off acceptance criteria when complete
4. Link related tasks using task IDs

## Status Values

- `todo`: Not started
- `in-progress`: Currently being worked on
- `blocked`: Waiting on dependency
- `review`: Ready for review
- `done`: Completed

## File Naming

Format: `{type}-{number}-{slug}.md`

Examples:
- `epic-001-user-authentication.md`
- `story-001-login-form.md`
- `bug-001-email-validation.md`
```

### Step 4: Analyze and Structure Tasks

Based on the source (TodoWrite or description):

1. **Identify the Epic**: The main feature/initiative
2. **Break into User Stories**: Discrete deliverable pieces
3. **Identify Dependencies**: Which tasks block others
4. **Assign Priorities**: Based on dependencies and importance

**Example breakdown:**
```
Epic: Blog Post Commenting System
├── Story 1: Comment model and database
├── Story 2: Comment controller and routes
├── Story 3: Comment form UI with Turbo
├── Story 4: Comment listing with nested replies
└── Story 5: Email notifications for replies
```

### Step 5: Generate Task Files

Create files using the templates (see templates/ directory).

**Naming convention:** `{type}-{number}-{slug}.md`

**Numbering:**
- Check existing tasks: `ls tasks/{type}-* 2>/dev/null | wc -l`
- Increment from highest existing number
- Pad with zeros: `001`, `002`, etc.

**Slug generation:**
- Lowercase title
- Replace spaces with hyphens
- Remove special characters
- Max 50 characters

### Step 6: Create Task Files

For each task, create a markdown file using the templates in the `templates/` directory.

**Available templates:**
- [templates/epic.md](templates/epic.md) - For large features/initiatives
- [templates/user-story.md](templates/user-story.md) - For deliverable functionality
- [templates/bug.md](templates/bug.md) - For defects and bugs
- [templates/issue.md](templates/issue.md) - For chores and technical debt

**Template usage:**
- Read the appropriate template file from `templates/` directory
- Replace placeholder values: `{number}`, `{Epic Title}`, `{YYYY-MM-DD}`, etc.
- Use Write tool to create the task file in `tasks/` directory

For full template details, see the files in `templates/` directory.

### Step 7: Create Task Index

After creating all task files, update or create `tasks/INDEX.md`:

```markdown
# Task Index

Generated: {YYYY-MM-DD HH:MM}

## Epics

- [epic-001](epic-001-slug.md) - {Title} `[status]`

## User Stories

- [story-001](story-001-slug.md) - {Title} `[status]` (epic-001)
- [story-002](story-002-slug.md) - {Title} `[status]` (epic-001)

## Bugs

- [bug-001](bug-001-slug.md) - {Title} `[status]`

## Issues

- [issue-001](issue-001-slug.md) - {Title} `[status]`

## By Status

### Todo
- story-001, bug-001

### In Progress
- story-002

### Done
- issue-001
```

### Step 8: Present Summary

Show the user what was created:

```
## Task Files Created

Created {N} task files in tasks/ directory:

### Epic
- tasks/epic-001-feature-name.md

### User Stories (5)
- tasks/story-001-database-setup.md
- tasks/story-002-business-logic.md
- tasks/story-003-ui-implementation.md
- tasks/story-004-testing.md
- tasks/story-005-polish.md

### Structure
tasks/
├── README.md
├── INDEX.md
├── epic-001-feature-name.md
└── story-001-database-setup.md

### Next Steps
1. Review task files and update priorities
2. Assign tasks to team members (update frontmatter)
3. Start with: tasks/story-001-database-setup.md
4. Update status as work progresses
5. Commit to git: git add tasks/ && git commit -m "Add tasks for {feature}"

Tasks are now tracked in markdown files and can be committed to version control.
```

## Best Practices

**Do:**
- ✅ Create one epic per feature/initiative
- ✅ Break epics into 3-7 user stories
- ✅ Use clear, actionable titles
- ✅ Include acceptance criteria
- ✅ Link related tasks with IDs
- ✅ Update task status as work progresses
- ✅ Commit task files to git

**Don't:**
- ❌ Create too many task types (keep it simple)
- ❌ Make user stories too large (split them)
- ❌ Skip acceptance criteria
- ❌ Forget to update task status
- ❌ Duplicate tasks between TodoWrite and files
- ❌ Create tasks without clear ownership

## Integration

**With plan-feature skill:**
After `/plan-feature` completes, it will suggest running this skill to export tasks to files.

**With TodoWrite:**
Can read current TodoWrite tasks and convert them to structured files.

**With Git:**
Task files are designed to be committed to version control for team collaboration.

## File Structure

```
tasks/
├── README.md                      # Overview of task system
├── INDEX.md                       # Auto-generated index of all tasks
├── epic-001-user-auth.md         # Epic for authentication
├── story-001-login-model.md      # User story for login model
├── story-002-login-controller.md # User story for login controller
├── story-003-login-ui.md         # User story for login UI
├── bug-001-email-validation.md   # Bug fix task
└── issue-001-refactor-auth.md    # Technical debt task
```

## Example Usage

**Scenario 1: After planning**
```bash
/plan-feature "Add user authentication"
# ... planning completes ...
/create-task-files
# Creates epic + 5 user stories in tasks/
```

**Scenario 2: Standalone**
```bash
/create-task-files
# Asks: "Create tasks from todo list or feature description?"
# Creates structured task files based on input
```

**Scenario 3: Bug tracking**
```bash
/create-task-files
# Select: "Bug only"
# Creates bug-001-description.md with proper template
```

## Output

Creates structured markdown files in `tasks/` directory with:
- Proper frontmatter (YAML)
- Consistent formatting
- Clear acceptance criteria
- Dependency tracking
- Status management
- Git-friendly format

This enables team collaboration, progress tracking, and version-controlled project management.
