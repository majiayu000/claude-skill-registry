---
name: cmd-builder
description: Guides adding and structuring Go command entrypoints under cmd/: when to create a new cmd, layout, wiring only (no business logic), and use of internal packages. Use when creating or refactoring code under cmd/, adding a new executable, or when the user asks about cmd or entrypoint structure.
---

# Cmd Builder Skill

Use this skill when creating or modifying command entrypoints under `cmd/`.

---

## When to create a new cmd

- **New executable** (new binary, distinct from api/evaluator/importer/migrations) → new directory under `cmd/<name>/` with `main.go`.
- **Existing executable** → add flags or wiring in that cmd; do not add a second main for the same concern.
- **Shared orchestration or workflow** → implement in `internal/` and call from cmd; keep cmd thin.

## Layout

- One **entrypoint per directory**: `cmd/<name>/main.go`, `package main`.
- Each cmd builds to a single binary; the directory name is the conventional binary name (e.g. `cmd/api` → `api`).
- All **logic lives in internal/**; cmd only parses flags/env, opens resources (DB, etc.), and calls internal packages.

## What cmd does (and does not)

- **Does**: Parse flags (e.g. `internal/cli`) or env (`internal/env`); create DB client (`internal/db`); wire and call internal packages; log and exit on startup failure (`log.Fatal` or zerolog).
- **Does not**: Contain business logic, algorithms, or domain rules; those live in `internal/`. If a cmd grows a large loop or workflow, consider moving it into an `internal/` package so it can be tested and reused.

## Existing cmd apps (use as reference)

| Cmd | Role |
|-----|------|
| `cmd/api` | Load env, create DB client, start HTTP router (`internal/router`). |
| `cmd/evaluator` | Load env and CLI flags, create DB and cache, run evaluation workflow via `internal/evaluator` and `internal/candidate_tree`. |
| `cmd/importer` | Load env, create DB and tarkov.dev client, run `internal/importers` and `internal/models` purge/import. |
| `cmd/migrations` | Parse args, open DB, run goose migrations. |

## Imports

- Cmd imports **internal** by module path: `tarkov-build-optimiser/internal/<pkg>`.
- Example: `import "tarkov-build-optimiser/internal/env"`.
- **internal/** must not import **cmd/**.

## Checklist for a new cmd

1. Create `cmd/<name>/main.go` with `package main` and a `main()` that exits on error (e.g. `log.Fatal`).
2. Parse config: use `internal/env` for env vars and optionally `internal/cli` for flags.
3. Open resources (e.g. `internal/db`); defer or otherwise ensure cleanup where appropriate.
4. Construct and call internal packages only; no business logic in main.
5. If the workflow is more than a few calls, consider an orchestration function in `internal/` and call it from main.

## Boundaries to respect

- **No business logic in cmd/** — cmd wires and invokes; all domain and workflow logic stays in `internal/`.
- **One main per binary** — one `cmd/<name>/main.go` per distinct executable.
- **internal does not import cmd** — dependency flow is cmd → internal only.
