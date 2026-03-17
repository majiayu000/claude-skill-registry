---
name: df:add-todo
description: |
  Capture idea or task as todo from current conversation context.
  Use when the user wants to save something for later, note an idea, or track a task.
  Triggers on: "remember to", "add a todo", "note this for later", "save this idea", "track this"
argument-hint: [optional description]
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
---

<objective>
Capture an idea, task, or issue that surfaces during a DevFlow session as a structured todo for later work.

Routes to the add-todo workflow which handles:
- Directory structure creation
- Content extraction from arguments or conversation
- Area inference from file paths
- Duplicate detection and resolution
- Todo file creation with frontmatter
- STATE.md updates
- Git commits
</objective>

<execution_context>
@.planning/STATE.md
@~/.claude/devflow/workflows/add-todo.md
</execution_context>

<process>
**Follow the add-todo workflow** from `@~/.claude/devflow/workflows/add-todo.md`.

The workflow handles all logic including:
1. Directory ensuring
2. Existing area checking
3. Content extraction (arguments or conversation)
4. Area inference
5. Duplicate checking
6. File creation with slug generation
7. STATE.md updates
8. Git commits
</process>
