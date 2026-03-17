---
name: git-committer-atomic
description: Plan and create atomic commits ordered by dependencies
version: 1.1.0
tags: [git, workflow, atomic]
owner: engineering
status: active
---

# Git Committer Atomic Skill

## Overview

Split changes into atomic commits ordered by dependency.

## Usage

```
/git-committer-atomic
```

## Identity
**Role**: Git Operations Specialist
**Objective**: Break down the current set of changes into atomic, logical commits, ensuring dependencies are committed before consumers.

## Context
You are working in a dirty git state. Your goal is to reach a clean git state (`git status` clean) by creating a series of well-structured commits.

## Workflow Rules

### 1. Analysis Phase
- Run `git status --porcelain` to see all changes.
- Analyze dependencies between changed files.
- **Dependency Hierarchy** (Commit in this order):
  1.  **Infrastructure**: Config files, build scripts, strict types (`tsconfig.json`, `package.json`).
  2.  **Core/Utils**: Shared libraries, helper functions, base classes.
  3.  **Domain/Models**: Database schemas, entity definitions, DTOs.
  4.  **Services**: Business logic, API handlers.
  5.  **Features/UI**: React components, pages, routes.
  6.  **Tests**: Unit and integration tests (can be committed with features if tight, but often separate).

### 2. Execution Loop
While `git status` is not clean:
1.  **Identify** the next logical group of files based on the hierarchy above.
2.  **Stage** these files: `git add <file1> <file2>`.
    - If a file contains multiple logical changes (e.g., a fix AND a feature), instruct the user to use `git add -p` or split it yourself if capable.
3.  **Verify** (Mental Check): Does this commit compile/make sense on its own?
4.  **Commit**: Generate a conventional commit message (ref: `git-commit-conventional`).
    - Format: `type(scope): description`
    - Example: `feat(utils): add date formatting helper`
5.  **Repeat**.

## Constraints
- **Atomic**: Each commit must do one thing.
- **Buildable**: Avoid leaving the repo in a broken state between commits if possible.
- **No "WIP"**: Do not create "Work in progress" commits unless explicitly asked.

## Agent Compatibility
- **Claude**: Use strict ordering.
- **Cursor**: Focus on file grouping logic.
- **Gemini**: verification of dependency graph logic.

## Outputs

- Ordered list of atomic commits with rationale.

## Related Skills

- `/git-commit-conventional` - Message formatting
