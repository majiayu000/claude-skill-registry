---
name: shared-conventions
description: |
  Project-wide conventions and patterns that apply to all apps/modules.
  Use when: asking about project structure, coding standards, or shared patterns.
  This skill loads for all work in the monorepo.
author: Memory Forge
version: 1.0.0
date: 2025-01-28
---

# Shared Conventions

This skill contains project-wide patterns that apply to all apps and modules.

## Conventions

### Commit Message Format

```
type(scope): description

Types: feat, fix, refactor, chore, docs, test
Scope: app name or module (e.g., booking, hermes, shared)
```

### Code Organization

All apps follow this structure:
```
src/
├── domain/         # Business logic, entities, value objects
├── application/    # Use cases, services
└── infrastructure/ # Controllers, repositories, external APIs
```

### Testing

- Unit tests: `*.spec.ts` (alongside source files)
- Integration tests: `*.test.ts` (alongside source files)
