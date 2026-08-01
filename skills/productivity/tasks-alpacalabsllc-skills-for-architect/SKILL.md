---
name: tasks
description: Lightweight task list kept in TASKS.md in the current folder — add, complete, and review tasks across sessions. Use when the user runs /tasks, says "add a task", or asks what's on their list.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
---

# /tasks — A Task List That Survives Sessions

You maintain `TASKS.md` in the current folder. The file is the memory — sessions end, the list persists.

## Usage

```
/tasks                     → show open tasks, oldest first
/tasks add call Marcus re zoning memo
/tasks done 3              → check off task 3
/tasks all                 → include completed tasks
```

## Steps

1. Read `TASKS.md` if it exists; offer to create it if not.
2. Apply the command: add appends with today's date, done checks off with completion date, bare `/tasks` just lists.
3. Write the file, then show the current open list — always end by showing the list, so the user never wonders what state it's in.

## Format

```markdown
# Tasks

- [ ] call Marcus re zoning memo (added 2026-07-09)
- [x] send Daniel the site-visit recap (added 2026-07-08 · done 2026-07-09)
```

## Rules

- One flat list. No priorities, tags, or projects — if the user wants those, suggest they modify this skill (that's the point of owning it).
- Never delete a task, even a completed one. History stays.
