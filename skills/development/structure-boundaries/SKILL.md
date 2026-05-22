---
name: structure-boundaries
description: 'Use when navigation is costly or module boundaries feel blurry due to messy directories, inconsistent naming, or cross-boundary imports. Goal: make architecture and dependency direction readable from the tree and imports, with minimal churn.'
metadata:
  short-description: Clear boundaries
---

# Structure & Boundaries

A good project layout makes intent obvious: where code belongs, what it does, and which parts depend on which.

## Core Principle

**Structure should reflect responsibility and boundaries.**
Directories and imports should let a reader infer the architecture without opening many files.

## Directory Organization

### List vs Dict

Use one of these meanings per directory level.

**List pattern**: children are interchangeable items of the same kind.
Use plural or category-like parent names.

```
operations/
  articles/
  comments/
  users/
```

Test: can you add another sibling without changing what the parent means?

**Dict pattern**: children are distinct roles (fixed set of responsibilities).

```
project/
  operations/   # business logic
  services/     # integrations / IO
  utils/        # domain-free primitives
```

Test: does each child have a unique, non-interchangeable purpose?

Avoid mixing both meanings at the same level.

### Flat when possible

Prefer shallow trees. Add a subdirectory only when a real grouping exists (many files, or clear sub-roles).

## Naming

### Names assume directory context

File names should describe *what it is*, not repeat the directory’s meaning.

```
operations/articles/
  publish.py
  validate.py
```

Avoid vague buckets (`misc`, `helpers`, `manager`) unless the responsibility is truly precise.

### Shared code conventions

- `…kit` suffix: shared code for a specific layer or domain boundary.
  - Use when code is reused across siblings within that boundary.
  - Meaning: “tooling/support code for X”, not a new domain.
- `utils/`: domain-free utilities only.
  - No business terms, no project-layer dependencies.
  - If something belongs to a domain or layer, prefer placing it in that domain/layer (or its `…kit`) instead of `utils`.

## Imports as Boundary Signals

Imports should make relationships obvious:

- **Within a boundary** (same directory/subtree): use the local convention (often relative or shortest local path).
- **Across boundaries** (parent/sibling/other layers/domains): use explicit absolute paths to make crossing visible.
- Avoid “upward” relative imports that hide boundary crossing.

A healthy codebase tends to have a clear dependency direction (e.g., higher-level logic depends on lower-level utilities/integrations, not the reverse). Flag boundary violations.

## Review Process

1. Identify the project’s main boundary axes (layer, domain). Keep one primary axis per directory level.
2. Classify each directory level as List or Dict; rename/restructure to remove ambiguity.
3. Flatten over-nesting; create subdirectories only for real grouping.
4. Fix naming to be context-aware and non-redundant.
5. Align imports so boundary crossings are visible and dependency direction is consistent.
6. Propose a minimal-change plan: smallest set of moves/renames that improves readability.

## Review Checklist

- Each directory level has a single meaning: List or Dict.
- The tree makes responsibilities and boundaries obvious.
- Names are concise given directory context.
- The hierarchy is flat unless grouping is justified.
- Imports make boundary crossings and dependency direction easy to see.
- `utils/` stays domain-free; shared code lives in the right `…kit` boundary when applicable.
