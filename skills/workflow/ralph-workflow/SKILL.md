---
name: ralph-workflow
description: Autonomous backlog processing workflow for Brain Dump. Use when working through multiple tickets autonomously or when asked to process a backlog like Ralph.
---

# Ralph Workflow Skill

This skill provides the autonomous backlog processing workflow used by Ralph.

## When to Use This Skill

- Processing multiple tickets autonomously
- Working through a product backlog
- Implementing features from a PRD file
- Running in background agent mode

## The Ralph Workflow

### 1. Read Context Files

```
plans/prd.json     - Product requirements (auto-generated from tickets)
plans/progress.txt - Notes from previous iterations
```

### 2. Set Up Git Branch

Before any code changes:

```bash
git fetch origin
git checkout -b ralph/<ticket-id>-<description> origin/dev
# or origin/main if no dev branch
```

### 3. Pick ONE Task

From `prd.json`, find a user story where `passes: false`:

- Prioritize by priority field (high > medium > low)
- Only work on ONE task per iteration

### 4. Post Progress Update

```javascript
comment "add"({
  ticketId: "story-id",
  content: "Starting work on user authentication. Will implement login form and API endpoint.",
  author: "ralph",
  type: "comment"
})
```

### 5. Implement Feature

- Write the code
- Run type checks: `pnpm type-check` or `npm run type-check`
- Run tests: `pnpm test` or `npm test`
- Verify acceptance criteria

### 6. Commit Changes

```bash
git add -A
git commit -m "feat(<ticket-id>): <description>"
```

### 7. Update PRD

Edit `plans/prd.json` to set `passes: true` for the completed story.

### 8. Update Progress File

Append to `plans/progress.txt`:

```
## Iteration N - [timestamp]
- Completed: <ticket title>
- Changes: <brief summary>
- Notes: <any learnings or issues>
```

### 9. Update Ticket Status

```javascript
ticket "update-status"({ ticketId: "ticket-id", status: "done" })

comment "add"({
  ticketId: "ticket-id",
  content: "## Work Summary\n**Changes:**\n- ...\n**Tests:**\n- All passing",
  author: "ralph",
  type: "work_summary"
})
```

### 10. Check Completion

If ALL stories have `passes: true`:

- Push branch: `git push -u origin <branch-name>`
- Create PR using `gh pr create`
- Output: `PRD_COMPLETE`

Otherwise, the next iteration picks the next task.

## PRD File Format

```json
{
  "projectName": "My Project",
  "projectPath": "/path/to/project",
  "epicTitle": "Feature Name",
  "userStories": [
    {
      "id": "ticket-id",
      "title": "Task title",
      "description": "What to build",
      "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
      "priority": "high",
      "tags": ["frontend"],
      "passes": false
    }
  ],
  "generatedAt": "2024-01-01T00:00:00.000Z"
}
```

## Progress File Format

```markdown
# Ralph Progress Log

# Use this to leave notes for the next iteration

## Iteration 1 - 2024-01-01 10:00

- Completed: Add login form
- Changes: Created LoginForm.tsx, added validation
- Notes: Auth API returns different error format than expected

## Iteration 2 - 2024-01-01 10:30

- Completed: Add auth API integration
- Changes: Updated auth.ts, added error handling
- Notes: All tests passing
```

## Important Rules

1. **One task per iteration** - Keeps context focused
2. **Always test** - Run tests before marking complete
3. **Update status** - Use MCP tools to track progress
4. **Document issues** - Add blockers to progress.txt
5. **Never commit to main/dev** - Always use feature branches
