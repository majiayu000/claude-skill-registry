---
context: fork
---

# Skill: Todo List Management

Guidelines for managing the Claude Code todo list during sessions.

## Core Principles

### 1. Only Track Active Work

The todo list should only contain:
- Tasks currently in progress
- Tasks to be done in the current session
- Recently completed tasks (for context)

### 2. Future-Dated Tasks

**Do NOT add future-dated tasks to the todo list.**

Tasks with due dates in the future should:
- Be stored in the vault as Task notes (using `/task` skill)
- Be tracked in Jira/external systems
- Only appear in the todo list on or after their due date

**Why**: The todo list is for immediate work tracking, not a calendar or reminder system.

### 3. When to Add Tasks

Add to todo list when:
- User explicitly asks you to do something now
- Breaking down a complex current task into steps
- Tracking multi-step work in the current session

Do NOT add when:
- Task is scheduled for a future date
- Task is a reminder/calendar item
- Task belongs in an external system (Jira, calendar)

### 4. Cleaning Up

Regularly clean the todo list:
- Remove completed tasks after they're no longer relevant for context
- Remove tasks that have been deferred to future dates
- Keep the list focused on current work

## Examples

### Good Usage

```
User: "Help me refactor the authentication module"

Todo list:
- [in_progress] Analyse current auth module structure
- [pending] Identify refactoring opportunities
- [pending] Implement changes
- [pending] Update tests
```

### Bad Usage

```
User: "Remind me to review the ADR process in April"

❌ Don't add: [pending] Review ADR process (due 2026-04-07)
✅ Do: Create a Task note with due date, or note it will surface when due
```

## Integration with Task Notes

For future tasks, use the `/task` skill instead:

```
/task Review ADR process due 2026-04-07
```

This creates a proper Task note in the vault that can be:
- Queried by Dataview
- Shown in daily notes when due
- Tracked properly with full metadata

## Summary

| Task Type | Where to Track |
|-----------|---------------|
| Current session work | Todo list |
| Today's tasks | Todo list |
| Future dated | Task note in vault |
| Recurring reminders | Task note or calendar |
| Project work items | Jira + Task notes |
