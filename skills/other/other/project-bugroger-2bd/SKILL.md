---
name: project
description: Project lifecycle management. Dispatches to Ada.
argument-hint: "[action: create|archive] [args...]"
---

# Project

Manage project lifecycle. This skill dispatches to Ada.

## Usage

- `/project create "Project Name"` — Create a new project
- `/project archive "project-slug"` — Archive completed project

## Dispatch

Parse first argument and invoke Ada with the corresponding reference:
- `create` → Invoke @ada to execute `references/project/create.md`
- `archive` → Invoke @ada to execute `references/project/archive.md`

If no subaction provided, show usage and ask which action to run.
