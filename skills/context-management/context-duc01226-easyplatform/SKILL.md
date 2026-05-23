---
name: context
version: 1.0.0
description: '[Utilities] Load project context for current session'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Load project context for the current session (git status, branch info, recent changes).

**Workflow:**

1. **Gather** -- Run git status, branch info, recent commits
2. **Analyze** -- Identify current work context and pending changes
3. **Present** -- Summarize context for session awareness

**Key Rules:**

- Provides situational awareness at session start
- Shows branch, uncommitted changes, recent commits
- Non-destructive: read-only operation

# Load Project Context

Load current development context to help with subsequent tasks.

## Git Status

```bash
git status --short
git branch --show-current
```

## Recent Activity

```bash
# Recent commits
git log --oneline -5

# Uncommitted changes
git diff --stat
```

## Project Pattern Discovery

Before reporting project structure, search the codebase for actual services and apps:

- Search for: project services (`ls src/Services/`), frontend apps, key libraries
- Look for: service directories, app directories, shared library directories

> **MANDATORY IMPORTANT MUST** Read the `project-structure-reference.md` companion doc for project-specific patterns.
> If file not found, continue with search-based discovery above.

## Project Structure Reminder

Discover the actual project structure by running:

```bash
# Backend services
ls -d src/Services/*/

# Frontend apps
ls -d {frontend-apps-dir}/*/

# Key libraries
ls -d {frontend-libs-dir}/*/
```

## Development Patterns

**Backend:** Clean Architecture + CQRS + Entity Events
**Frontend:** Component framework + state management

## Current Session Focus

Based on the git status, identify:

- What files are being worked on
- What feature/fix is in progress
- Any uncommitted changes that need attention

Summarize the current state to help with subsequent tasks.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
