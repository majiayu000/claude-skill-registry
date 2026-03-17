---
name: task-management
description: Guide for managing tasks within a session using bd (beads) for subtasks and local todo lists. Use this skill when breaking down plans into issues, tracking progress, managing dependencies, or coordinating work across sessions and agents. Triggers include requests to "manage tasks", "track progress", "break down this work", or questions about bd workflow.
---

# Task Management

At the user level, we use Linear to manage tasks. When the Linear MCP is available, you can consult this directly.

Our workflow is to run many worktrees and checkouts of the repo and work on multiple research tasks and tasks in parallel. For managing todos and progress WITHIN a session you are encouraged to use `bd` (beads) to manage the work - falling back to a NOTES.md text based flow otherwise. 

If available, use `bd` to manage subtasks and local todo lists (`bd quickstart` and `bd --help`)
  - Break down plans into issues with dependencies and keep up-to-date during development
  - Instruct subagents to consult `bd` regularly
  - Use this to offload detail from your working memory and record extra details, bugs along the way with the user
  
The goal is to avoid 'clinging' to a context window, making it trivial to clear the session and re-hydrate context from `bd`. When you start a task, update FOCUS.md with a high-level understanding of the task. If a user, or another agent, reads your `bd` issues, commits and `FOCUS.md` they should be able to immediately take over and help with the work.
