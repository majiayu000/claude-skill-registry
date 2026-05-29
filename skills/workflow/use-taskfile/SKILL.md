---
name: use-taskfile
description: Run common project operations using the Taskfile. Use when building, testing, starting services, running migrations, or any project operation. Run `task` to discover available tasks.
---

# Use Taskfile Skill

Use this skill when running project operations. Prefer Taskfile tasks over manual commands.

---

## Discover Available Tasks

```bash
task
```

This lists all available tasks with descriptions.

## Common Task Categories

| Category | Example Tasks | Purpose |
|----------|--------------|---------|
| `api:*` | `api:build`, `api:start`, `api:start:docker` | Build and run the API |
| `compose:*` | `compose:up`, `compose:down` | Manage Docker services |
| `evaluator:*` | `evaluator:start`, `evaluator:start:test-mode` | Run the evaluator |
| `importer:*` | `importer:start`, `importer:start:use-cache` | Import data from tarkov.dev |
| `migrate:*` | `migrate:up`, `migrate:up:docker`, `migrate:down`, `migrate:create` | Database migrations |
| `test:*` | `test`, `test:unit`, `test:integration`, `test:integration:docker` | Run tests |
| `tarkovdev:*` | `tarkovdev:get-schema`, `tarkovdev:regenerate` | Update GraphQL schema |

## Running Tasks

```bash
# Run a specific task
task <task-name>

# Example: apply migrations (local/devcontainer)
task migrate:up

# Example: apply migrations (with docker)
task migrate:up:docker
```

## Key Tasks

- **`task init`** - Set up development environment
- **`task init:go-only`** - Set up Go-only development environment
- **`task test:unit`** - Run tests without database
- **`task migrate:up`** - Apply database migrations (local/devcontainer)
- **`task importer:start`** - Repopulate weapons/items from tarkov.dev API

## Repopulating the Database

If the database has been wiped or migrations rolled back, repopulate data with:

```bash
task compose:up        # Ensure database is running
task migrate:up        # Apply migrations
task importer:start    # Fetch and import all weapons/items from tarkov.dev
```

Use `task importer:start:use-cache` to import from local cache instead of fetching from the API.
