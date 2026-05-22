---
name: backend-fastapi-python
description: "Use this skill for any Python backend work in this project: building FastAPI endpoints, writing service functions, defining Pydantic/SQLModel schemas, running Alembic migrations, or debugging 422 errors. Essential for authentication and authorization patterns — setting up get_current_user, is_superuser checks, admin-only guards, role-based access, and dependency injection chains like Depends(). Also covers middleware, background tasks, async SQLAlchemy sessions, ORM relationship loading, and request/response design. Activate whenever the question involves Python API code, FastAPI patterns, or backend architecture in this codebase. Not for frontend, Docker, CI/CD, or infrastructure."
---

# Backend FastAPI Python

Project-specific conventions for FastAPI with SQLModel, pydantic-settings, and async SQLAlchemy.

## Architecture Decisions

1. **Services are stateless functions** — Not classes. First param is `db: AsyncSession`.
2. **Generic response wrapper** — Always use `ApiResponse[T]` for consistency.
3. **Dependencies chain** — `get_current_user` -> `require_auth` -> `require_admin`.
4. **Module-scoped config** — Each module can have its own `{module}_config.py`.
5. **Error codes for frontend** — `AppException(status, message, error_code)`.

## Gotchas

- SQLModel `Relationship()` fields are NOT included in API responses by default. You must explicitly add them to `model_config` or use a separate response schema with those fields.
- `AsyncSession.refresh()` does not load relationships. After commit, re-query with `.options(selectinload(...))` if you need related objects.
- Pydantic V2 uses `model_validator` not `validator`. The `@validator` decorator is V1 and will break silently or raise deprecation warnings.
- `Depends()` in FastAPI creates a NEW instance per request — don't store state in dependency return values expecting it to persist.
- Background tasks (`BackgroundTasks`) run AFTER the response is sent. If they fail, the client already got a 200. Use proper task queues (Celery, ARQ) for anything that must not silently fail.
- Alembic `--autogenerate` misses: table renames (generates drop+create), index changes on existing columns, and `Enum` type modifications in PostgreSQL. Always review generated migrations.
- `async def` endpoints block the event loop if you call sync I/O inside them. Use `run_in_executor` for sync libraries or define the endpoint as `def` (FastAPI runs sync endpoints in a threadpool).
- `HTTPException` from FastAPI and `HTTPException` from Starlette are different classes. Importing the wrong one causes middleware to miss exception handlers.
- SQLAlchemy's `lazy="selectin"` on relationships causes N+1 queries in async sessions. Use explicit `selectinload()` in queries instead.
- `Optional[str] = None` in query params makes the field optional. `str = None` also works but loses type information — prefer the explicit `Optional` form.
- When using `response_model`, FastAPI filters OUT any fields not in the model. If your response is missing data, check that the response model includes all fields, not just the ORM model.

## References

| When you need... | Read |
|------------------|------|
| Directory layout | [file-structure.md](./references/file-structure.md) |
| Settings and env vars | [configuration.md](./references/configuration.md) |
| Database sessions and connections | [database.md](./references/database.md) |
| ORM models | [models.md](./references/models.md) |
| Request/response schemas | [schemas.md](./references/schemas.md) |
| Router and endpoint patterns | [routing.md](./references/routing.md) |
| Service layer patterns | [services.md](./references/services.md) |
| Dependency injection | [dependencies.md](./references/dependencies.md) |
| Middleware setup | [middleware.md](./references/middleware.md) |
| Error handling | [error-handling.md](./references/error-handling.md) |
| Auth flow example | [auth.md](./references/auth.md) |
