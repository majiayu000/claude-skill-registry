---
name: internal-package-building
description: Guides adding and structuring internal Go packages: when to create a new package, import paths, cmd vs internal boundaries, and domain layout. Use when creating or refactoring code under internal/, adding a new domain, or when the user asks about internal package structure.
---

# Internal Package Building Skill

Use this skill when creating or refactoring internal Go packages.

---

## When to create a new package

- **New domain** → new directory under `internal/` (e.g. new feature area or bounded context).
- **Existing domain** → add or edit files in the existing package; do not split without a clear boundary.
- **Shared cross-cutting concern** (DB, config, models) → use or extend existing shared packages (`internal/db`, `internal/models`, `internal/env`) rather than creating a new one unless the concern is clearly separate.

## Layout

- One **package per directory**; package name = directory name (e.g. `internal/candidate_tree` → `package candidate_tree`).
- Entrypoints live only in **cmd/** (e.g. `cmd/api`, `cmd/evaluator`, `cmd/importer`). All shared logic lives in **internal/**.
- **internal/** must not import **cmd/**; cmd packages wire and call internal packages.

## Imports

- Import internal packages by **module path**:
  `tarkov-build-optimiser/internal/<pkg>`
- Example: `import "tarkov-build-optimiser/internal/models"`

## Existing internal packages (use, don’t duplicate)

| Package | Role |
|--------|------|
| `internal/db` | Database connections and pool |
| `internal/models` | Data types and SQL access (UpsertX, GetXById, etc.) |
| `internal/env` | Environment/config |
| `internal/helpers` | Shared pure helpers (e.g. maths) |
| `internal/cache` | Caching utilities |
| `internal/candidate_tree` | Build candidate tree logic |
| `internal/evaluator` | Build evaluation |
| `internal/importers` | Data import from external sources |
| `internal/router` | HTTP routing and handlers |
| `internal/tarkovdev` | tarkov.dev API client |

## Checklist for a new internal package

1. Create `internal/<name>/` with at least one `.go` file; package name = `<name>`.
2. Add only code that belongs to that domain; put shared DB/config in `internal/db` or `internal/env`.
3. Import other internal packages via `tarkov-build-optimiser/internal/...`.
4. Keep the package focused; if it grows into two clear domains, consider splitting into two packages only when the boundary is obvious.
5. Add tests in the same package (`*_test.go`); use `*_unit_test.go` or `*_integration_test.go` per project conventions.

## Boundaries to respect

- **No business logic in cmd/** — cmd only parses flags/env, opens DB, and calls internal packages.
- **No circular imports** — internal packages may depend on each other only acyclically; if you introduce a cycle, extract a shared type or helper into a lower-level package.
- **Database access** — use `internal/db` for connections and `internal/models` for SQL and data types; do not add new ad-hoc DB packages.
