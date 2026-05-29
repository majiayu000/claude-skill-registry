---
name: ralph-next
description: Select and execute the next TDD task phase from SCOPES.yml
---

Your job is to select which task should be worked on next and execute the appropriate TDD skill for its current phase.

## Selection Priority (highest to lowest)

1. **In-progress tasks** - Tasks with status "testing" or "implementing" (work already started)
2. **New tasks** - Tasks with status "scoped" that have all dependencies "completed"
3. Never select tasks with status "completed"

## Tie-breaking

When multiple tasks have the same priority:
- Prefer lower effort over higher effort
- Prefer tasks appearing earlier in the file

## Branch Handling

Each task gets its own branch. The branch name is derived from the task:
- Format: `task-<id>-<slugified-title>`
- Example: Task 1 "Initialize Expo project" → `task-1-initialize-expo-project`

The base branch for a task is determined by its milestone's `base_branch`:
```yaml
milestones:
  - number: 1
    title: "1. Foundation"
    base_branch: main  # Tasks in milestone 1 branch from main

tasks:
  - id: 1
    milestone: 1  # This task branches from main
    ...
```

Before starting work on a task:
1. Generate the task branch name: `task-<id>-<slugified-title>`
2. Look up the task's milestone to get `base_branch`
3. Check if the task branch exists locally
4. If it exists, switch to that branch
5. If it does NOT exist:
   - Fetch the latest from origin
   - Create the branch from `base_branch` (e.g., `git checkout -b task-1-init-expo origin/main`)
   - Push the new branch to origin with tracking (`git push -u origin task-1-init-expo`)

### Slugifying the title
- Lowercase the title
- Replace spaces with hyphens
- Remove special characters
- Truncate to ~50 chars max for readability

## Workflow

1. Read the SCOPES.yml file (full path provided in arguments)
2. Select the highest priority task based on above rules
3. Handle branch setup as described above (per-task branch)
4. Based on the task's status, call the appropriate skill using the Skill tool:
   - `"scoped"` -> call skill `ralph-test` with arguments: `<scopes-path> <task-id>`
   - `"testing"` -> call skill `ralph-code` with arguments: `<scopes-path> <task-id>`
   - `"implementing"` -> call skill `ralph-refactor` with arguments: `<scopes-path> <task-id>`
5. If no tasks qualify, respond with "NO WORK"

Execute the next skill immediately based on the task status or return "NO WORK" if there is nothing to work on.

The ralph-test, ralph-code, and ralph-refactor skills automatically chain together and handle updating the task status after they complete their work. The ralph-refactor skill will call ralph-pr to create a PR for the completed task.
