---
name: create-api-module
description: Creates a new API module following Clean Architecture with TDD. Use when adding new API endpoints, creating backend features, implementing domain entities, or when the user says "create module", "add endpoint", "new backend feature".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(uv run pytest:*), Bash(docker compose exec:*)
---

# Create API Module

Creates a new backend module following **Clean Architecture** with API, Domain, and Infrastructure layers.

## Workflow

1. **Create directory structure** at `back/src/api/{module}/`
2. **Create infrastructure layer**: models, repository (interface + implementation), dependencies
3. **Create domain layer**: business logic functions, exceptions
4. **Create API layer**: router, schemas
5. **Register router** in `back/src/api/routes.py`
6. **Create tests** in `back/tests/api/{module}/`
7. **Create migration**: `docker compose exec back uv run alembic revision --autogenerate -m "Add {module} table"`

## Directory Structure

```
back/src/api/{module}/
├── api/
│   ├── router.py         # FastAPI endpoints
│   └── schemas.py        # Pydantic request/response models
├── domain/
│   ├── exception.py      # Domain exceptions
│   └── {action}.py       # Business logic functions
└── infrastructure/
    ├── models.py         # SQLModel database models
    ├── repository.py     # Repository interface + implementation
    └── dependencies.py   # FastAPI dependency injection
```

## Quick Scaffold

Generate boilerplate structure:
```bash
python .claude/skills/create-api-module/scripts/scaffold_module.py {module_name}
```

## Code Patterns

For detailed code patterns, see [PATTERNS.md](PATTERNS.md).

## Real Examples

For complete working examples from this codebase, see [EXAMPLES.md](EXAMPLES.md).

## Important Conventions

- **Table names**: plural, lowercase (`items`, `users`, `notifications`)
- **Model class names**: `{Entity}Db` (`ItemDb`, `UserDb`)
- **Router names**: `{entity}_router` (`item_router`, `user_router`)
- **Test names**: `test_when_{condition}_then_{outcome}`
- **Always use UUID** for primary keys
- **Soft delete**: Use `deleted_at` field instead of hard delete
- **Type hints**: Required everywhere, use `|` for union types (not `Optional`)

## After Creating Module

1. Run tests: `uv run pytest tests/api/{module}/ -v`
2. Format code: `task format`
3. Create migration if needed
4. Test endpoints via `/docs` locally
