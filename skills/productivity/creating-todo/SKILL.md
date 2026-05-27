---
name: creating-todo
description: Use when the user wants to create a todo, add a task, or add a to-do in Things. Triggers include "things todo", "things task", "add to Things", "create a Things todo".
allowed-tools: Bash, mcp__things__get_projects, mcp__things__add_todo, mcp__things__add_project, AskUserQuestion
argument-hint: [todo-description]
model: sonnet
---

# Creating Todo

Add current work as **exactly one** to-do item in Things, mapped to the correct Things project.

## Scope

- **One todo per invocation** — always create exactly one top-level todo
- Multiple related items go inside the **Notes** field of that todo (as a checklist or bullet list)
- Do NOT create multiple `mcp__things__add_todo` calls in a single invocation

## Workflow

### 1. Prepare task content

- If `$ARGUMENTS` is provided → use it directly as the todo title/description
- If user provided a description in the message → use it directly
- Otherwise → summarize current work from conversation context, confirm with user before continuing

### 2. Detect current project name (git repos only)

In a git repo (including worktrees) → `git worktree list --porcelain 2>/dev/null | head -1 | sed 's/^worktree //' | xargs basename`

If not in a git repo, skip to step 3 (will ask user directly).

### 3. Resolve Things project

Call `mcp__things__get_projects` to list all projects, then do a case-insensitive partial match against the name from step 2.

- **In a git repo + match found** → use it directly, no confirmation needed
- **In a git repo + no match** → ask: *"No matching Things project found for 'X'. Which project should I add this to?"*
- **Not in a git repo** → ask: *"Which Things project should I add this to?"*

### 4. Create project if needed

If the project name given in step 3 does not exist in Things, call `mcp__things__add_project` directly — no additional confirmation needed.

### 5. Add the to-do (requires confirmation)

Show the user the full details and ask for confirmation before submitting:

```
Title:   <title>
Notes:   <notes>   (if any)
Project: <project name>
```

*"Shall I add this to Things?"*

Only call `mcp__things__add_todo` with the project's UUID after user confirms. Pass only `title`, `notes`, and `list_id` — do not add `when`, `tags`, `deadline`, or any other fields unless the user explicitly requests them.

## Rules

- **Only activate** when the user explicitly mentions "Things"
- **One todo per invocation** — never call `mcp__things__add_todo` more than once
- **In a git repo with a matching Things project** → use it automatically without confirmation
- **Never** add a to-do without showing details and waiting for approval
- **Never** pass extra fields (`when`, `tags`, `deadline`, etc.) to `mcp__things__add_todo` unless user explicitly requests them
