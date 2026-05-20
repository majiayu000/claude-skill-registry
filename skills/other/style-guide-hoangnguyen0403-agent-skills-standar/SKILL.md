---
name: Angular Style Guide
description: Naming conventions, file structure, and coding standards for Angular projects.
metadata:
  labels: [angular, style, naming, structure]
  triggers:
    files: ['**/*.ts']
    keywords: [angular style, naming convention, file structure]
---

# Angular Style Guide

## **Priority: P0 (CRITICAL)**

## Principles

- **Single Responsibility**: One component/service per file. Small functions (< 75 lines).
- **Size Limits**: Keep files under 400 lines. Refactor if larger.
- **Strict Naming**: `feature.type.ts` (e.g., `hero-list.component.ts`).
- **Barrels**: Use `index.ts` only for public APIs of specific features/libraries. Avoid deep barrel imports within the same feature.
- **LIFT**: **L**ocate, **I**dentify, **F**lat structure, **T**ry DRY.

## Naming Standards

- **Files**: `kebab-case.type.ts`
- **Classes**: `PascalCase` + `Type` suffix (`HeroListComponent`)
- **Directives**: `camelCase` selector (`appHighlight`)
- **Pipes**: `camelCase` name (`truncate`)
- **Services**: `PascalCase` + `Service` suffix (`HeroService`)

## Anti-Patterns

- **Logic in Templates**: Move complex logic to the component class or a computed signal.
- **Deep Nesting**: Avoid $>3$ levels of folder nesting.
- **Prefixing interfaces**: No `IUser`. Use `User`.

## References

- [Naming Conventions](references/naming-convention.md)
