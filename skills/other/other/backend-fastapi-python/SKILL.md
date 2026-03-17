---
name: backend-fastapi-python
description: "FastAPI backend in Python conventions and patterns. Use this skill when building REST APIs, working with databases, implementing authentication, creating service layers or anything related to backend. Covers stateless services, response wrappers, and dependency chains."
---

# Backend FastAPI Python

Conventions for FastAPI applications using SQLModel, pydantic-settings, and async SQLAlchemy.

## Core Principles (See detailed in references)

### Key Conventions

1. **Services are stateless functions** - Not classes. First param is `db: AsyncSession`
2. **Generic response wrapper** - Always use `ApiResponse[T]` for consistency
3. **Dependencies chain** - `get_current_user` → `require_auth` → `require_admin`
4. **Module-scoped config** - Each module can have its own `{module}_config.py`
5. **Error codes for frontend** - `AppException(status, message, error_code)`

## References

| Topic | Reference |
|-------|-----------|
| Project Layout | [file-structure.md](./references/file-structure.md) |
| Configuration | [configuration.md](./references/configuration.md) |
| Database | [database.md](./references/database.md) |
| Models | [models.md](./references/models.md) |
| Schemas | [schemas.md](./references/schemas.md) |
| Routing | [routing.md](./references/routing.md) |
| Services | [services.md](./references/services.md) |
| Dependencies | [dependencies.md](./references/dependencies.md) |
| Middleware | [middleware.md](./references/middleware.md) |
| Error Handling | [error-handling.md](./references/error-handling.md) |
| Auth (Example) | [auth.md](./references/auth.md) |
