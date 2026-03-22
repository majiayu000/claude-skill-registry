---
name: task-coordination
description: >
  Patterns for using TaskCreate, TaskUpdate, TaskList, and TaskGet to coordinate
  multi-step work. Use when the user has a complex project with multiple steps,
  needs progress tracking, dependency management, or multi-agent task assignment.
---

# Task Coordination

The task system (TaskCreate, TaskUpdate, TaskList, TaskGet) provides structured tracking for multi-step projects. Use it to break down complex work, manage dependencies, assign owners, and track progress.

## When to Use
- User has a complex feature with multiple implementation steps
- Multiple agents need coordinated work assignment
- User asks about task tracking, dependencies, or progress
- Project requires sequential phases with blocking dependencies
- User wants visibility into what is done and what remains

## Core Patterns

### Creating a Task Breakdown

Break complex work into discrete, actionable tasks:

```
TaskCreate:
  subject: "Set up database schema for user profiles"
  description: "Create migration files for users table with fields:
    id, email, name, avatar_url, created_at, updated_at.
    Use the existing migration framework in src/db/migrations/"
  status: "pending"

TaskCreate:
  subject: "Implement user profile API endpoints"
  description: "Create CRUD endpoints: GET/POST/PUT/DELETE /api/users/:id
    Follow existing route patterns in src/api/routes/"
  status: "pending"
  blockedBy: ["1"]  # Depends on database schema

TaskCreate:
  subject: "Add user profile UI components"
  description: "Create ProfileCard, ProfileEditor, AvatarUpload components
    in src/components/profile/"
  status: "pending"
  blockedBy: ["2"]  # Depends on API endpoints
```

### Task Dependencies with blocks/blockedBy

Use `addBlocks` and `addBlockedBy` to express ordering constraints:

```
# Task 1: Database migration
# Task 2: API endpoints (blocked by 1)
# Task 3: UI components (blocked by 2)
# Task 4: E2E tests (blocked by 2 and 3)

TaskCreate:
  subject: "Write E2E tests for user profiles"
  status: "pending"
  blockedBy: ["2", "3"]  # Needs both API and UI

# Task 4 cannot start until tasks 2 AND 3 are completed.
```

Alternatively, set dependencies from the blocking task's side:

```
TaskUpdate:
  taskId: "1"
  addBlocks: ["2", "3"]  # Task 1 blocks tasks 2 and 3
```

### Status Tracking Workflow

Tasks follow a clear lifecycle:

```
pending  -->  in_progress  -->  completed
                                    |
                               (or deleted)
```

Claim and start a task:

```
TaskUpdate:
  taskId: "1"
  status: "in_progress"
  owner: "CoreWorkflow"
  activeForm: "Creating database migration"
```

Complete a task:

```
TaskUpdate:
  taskId: "1"
  status: "completed"
```

### Owner Assignment for Multi-Agent Teams

Assign tasks to specific agents or team members:

```
TaskUpdate:
  taskId: "1"
  owner: "DatabaseAgent"
  status: "in_progress"

TaskUpdate:
  taskId: "2"
  owner: "APIAgent"
  status: "pending"  # Still blocked, but assigned

TaskUpdate:
  taskId: "3"
  owner: "FrontendAgent"
  status: "pending"
```

### Checking Progress

Use TaskList to see overall status:

```
TaskList:
  # Returns:
  # #1 [completed] Set up database schema (DatabaseAgent)
  # #2 [in_progress] Implement user profile API (APIAgent)
  # #3 [pending] Add user profile UI (FrontendAgent) - blocked by #2
  # #4 [pending] Write E2E tests - blocked by #2, #3
```

Use TaskGet for full details on a specific task:

```
TaskGet:
  taskId: "2"
  # Returns full description, comments, status, owner, blockers
```

### Active Form for Spinner Display

Set `activeForm` to show what is happening during in_progress:

```
TaskUpdate:
  taskId: "2"
  activeForm: "Implementing GET /api/users/:id endpoint"
```

This shows a spinner with "Implementing GET /api/users/:id endpoint" in the UI.

### Post-Completion Flow

After completing a task, check for newly unblocked work:

```
# 1. Complete current task
TaskUpdate:
  taskId: "2"
  status: "completed"

# 2. Check what is now unblocked
TaskList:
  # #3 [pending] Add user profile UI - no longer blocked!
  # #4 [pending] Write E2E tests - still blocked by #3

# 3. Claim the next available task
TaskUpdate:
  taskId: "3"
  status: "in_progress"
  owner: "FrontendAgent"
```

### Task Granularity Guidelines

Right-sized tasks are:
- Completable in one focused session (15-60 minutes of work)
- Specific enough to verify completion
- Independent enough to have clear boundaries

```
# TOO COARSE:
"Build the entire authentication system"

# TOO FINE:
"Add import statement for bcrypt"

# RIGHT SIZE:
"Implement password hashing utility with bcrypt"
"Create login endpoint with JWT token generation"
"Add auth middleware for protected routes"
```

## Anti-Patterns

- **No dependencies**: Creating 10 tasks without dependency relationships leads to out-of-order execution. Always express ordering constraints.
- **Marking incomplete work as completed**: Never set status to "completed" if tests fail, implementation is partial, or errors remain unresolved. Keep as "in_progress" and create a new blocking task for the issue.
- **Skipping TaskList after completion**: Always check TaskList after completing a task. Dependencies may have unblocked new work that should be claimed immediately.
- **Monolithic tasks**: A single task covering an entire feature provides no progress visibility. Break it into 3-7 subtasks with clear completion criteria.
- **Orphaned tasks**: Tasks with no owner and no blocker that sit in "pending" forever. After creating tasks, assign owners or claim them.

## Quick Reference

| Tool | Purpose | Key Fields |
|------|---------|------------|
| TaskCreate | Create new task | subject, description, status, blockedBy |
| TaskUpdate | Modify task | taskId, status, owner, activeForm, addBlocks, addBlockedBy |
| TaskList | See all tasks | (no params) |
| TaskGet | Full task details | taskId |

**Status flow**: pending -> in_progress -> completed (or deleted)
**Dependencies**: Use blockedBy/addBlocks to express ordering
**After completion**: Always run TaskList to find unblocked work
**Task size**: 15-60 minutes of focused work per task
