---
name: inv-runner
description: Python Invoke task automation for DTX website. This skill should be used when running repo commands, backend tests via Docker, database migrations, updating invoke tasks, Docker operations, or workflow automation. Supports dev/test/prod environments with run, exec, up, down commands. References docs/development/invoke-tasks.md for complete command reference.
---

# Invoke Runner Skill

Python Invoke task automation for the DTX website project.

## Documentation References (Single Source of Truth)

For complete command reference, consult these mkdocs files:

| Document | Content |
|----------|---------|
| `docs/development/invoke-tasks.md` | Complete invoke command reference |
| `docs/development/backend-quickstart.md` | Backend development quickstart |
| `docs/development/testing.md` | Testing procedures including worktree verification |

## Running Invoke Commands

### Method 1: PATH Prefix (Recommended for Claude)

When bash hooks block `source` commands, prepend the venv bin to PATH:

```bash
PATH=".venv/bin:$PATH" inv <command>
```

For worktrees, use the full path:

```bash
PATH="/path/to/worktree/.venv/bin:$PATH" /path/to/worktree/.venv/bin/inv <command>
```

### Method 2: Poetry Run

```bash
poetry run inv <command>
```

### Method 3: Activate venv

```bash
source .venv/bin/activate
inv <command>
```

## Why PATH Matters

Invoke tasks call `python manage.py` or other Python commands. Without venv bin in PATH:
```
/bin/bash: line 1: python: command not found
```

PATH prefix ensures subprocess calls find the correct Python interpreter.

## Key Patterns

### Run vs Exec

**`run`** - One-off command in NEW container (with --rm):
```bash
inv test.run --cmd 'python manage.py test app.tests -v 2'
```

**`exec`** - Command in RUNNING container:
```bash
inv dev.exec backend 'python manage.py shell'
```

### Environment-Specific Commands

All environments (dev, test, prod) support:
```bash
inv <env>.up       # Start
inv <env>.down     # Stop and remove
inv <env>.logs     # Follow logs
inv <env>.run --cmd '<cmd>'  # One-off command
```

### Database Operations

```bash
inv db.migrate.all       # Migrations for all environments
inv db.migrate.test      # Test environment only
inv db.populate.all      # Reset and populate test DB
```

### Testing (Docker - Recommended)

Avoid Redis hanging issues by running tests in Docker:
```bash
inv test.run --cmd 'python manage.py test app.tests -v 2'
```

### Cypress E2E

```bash
inv test.setup           # Full setup
inv test.spec --spec navigation  # Specific spec
inv test.headless        # All tests headless
```

## Worktree Workflow

From worktree root:
```bash
cd /path/to/worktree
PATH=".venv/bin:$PATH" inv test.down
PATH=".venv/bin:$PATH" inv test.setup
PATH=".venv/bin:$PATH" inv db.migrate.test
PATH=".venv/bin:$PATH" inv db.populate.all
PATH=".venv/bin:$PATH" inv test.up
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `python: command not found` | Use PATH prefix method |
| Redis connection errors | Use Docker: `inv test.run --cmd '...'` |
| Tests hang on cleanup | Use Docker: `inv test.run --cmd '...'` |
| Module not found | Ensure correct venv is activated |

## When Modifying Tasks

Update these files when changing invoke tasks:
- `docs/development/invoke-tasks.md` (primary reference)
- `docs/development/backend-quickstart.md` (if backend-related)
