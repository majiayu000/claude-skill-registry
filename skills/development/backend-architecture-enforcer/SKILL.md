---
name: backend-architecture-enforcer
description: Enforces FastAPI Clean Architecture with blocking validation. Use when implementing router-service-repository patterns, enforcing layer separation, or validating dependency injection in backend code.
context: fork
agent: backend-system-architect
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [backend, fastapi, architecture, enforcement, blocking, clean-architecture, di]
user-invocable: false
---

Enforce FastAPI Clean Architecture with **BLOCKING** validation.

## When to Use

- Building FastAPI endpoints
- Creating services or repositories
- Reviewing backend architecture
- Refactoring legacy code

## Architecture Overview

```
+-------------------------------------------------------------------+
|                        ROUTERS LAYER                               |
|  HTTP concerns only: request parsing, response formatting          |
|  Files: router_*.py, routes_*.py, api_*.py                        |
+-------------------------------------------------------------------+
|                        SERVICES LAYER                              |
|  Business logic: orchestration, validation, transformations        |
|  Files: *_service.py                                              |
+-------------------------------------------------------------------+
|                      REPOSITORIES LAYER                            |
|  Data access: database queries, external API calls                 |
|  Files: *_repository.py, *_repo.py                                |
+-------------------------------------------------------------------+
|                        MODELS LAYER                                |
|  Data structures: SQLAlchemy models, Pydantic schemas             |
|  Files: *_model.py (ORM), *_schema.py (Pydantic)                 |
+-------------------------------------------------------------------+
```

## Validation Rules (BLOCKING)

| Rule | Check | Layer |
|------|-------|-------|
| **No DB in Routers** | Database operations blocked | routers/ |
| **No HTTP in Services** | HTTPException blocked | services/ |
| **No Business Logic in Routers** | Complex logic blocked | routers/ |
| **Use Depends()** | Direct instantiation blocked | routers/ |
| **Async Consistency** | Sync calls in async blocked | all |
| **File Naming** | Must follow naming convention | all |

## File Naming Conventions

### Quick Reference

| Layer | Allowed Patterns | Blocked Patterns |
|-------|-----------------|------------------|
| **Routers** | `router_*.py`, `routes_*.py`, `api_*.py`, `deps.py` | `users.py`, `UserRouter.py` |
| **Services** | `*_service.py` | `users.py`, `UserService.py`, `service_*.py` |
| **Repositories** | `*_repository.py`, `*_repo.py` | `users.py`, `repository_*.py` |
| **Schemas** | `*_schema.py`, `*_dto.py`, `*_request.py`, `*_response.py` | `users.py`, `UserSchema.py` |
| **Models** | `*_model.py`, `*_entity.py`, `*_orm.py`, `base.py` | `users.py`, `UserModel.py` |

## Layer Separation Summary

### Routers (HTTP Only)
- Request parsing and response formatting
- HTTP status codes and auth checks
- Delegate to services via `Depends()`

### Services (Business Logic)
- Validation and orchestration
- Data transformations
- Raise domain exceptions (NOT HTTPException)

### Repositories (Data Access)
- Database queries and persistence
- External API calls
- Return domain objects or None

## Dependency Injection Quick Reference

```python
# deps.py - Dependency providers
def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)

def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repo)

# router_users.py - Usage
@router.get("/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user(user_id)
```

### Blocked DI Patterns

```python
# BLOCKED - Direct instantiation
service = UserService()

# BLOCKED - Global instance
user_service = UserService()

# BLOCKED - Missing Depends()
async def get_users(db: AsyncSession):  # Missing Depends()
```

## Common Violations

| Violation | Detection | Fix |
|-----------|-----------|-----|
| DB in router | `db.add`, `db.execute` in routers/ | Move to repository |
| HTTPException in service | `raise HTTPException` in services/ | Use domain exceptions |
| Direct instantiation | `Service()` without Depends | Use `Depends(get_service)` |
| Wrong naming | Missing suffix/prefix | Rename per convention |
| Sync in async | Missing `await` | Add `await` or use executor |

## Exception Pattern

```python
# Domain exceptions (services/repositories)
class UserNotFoundError(DomainException):
    def __init__(self, user_id: int):
        super().__init__(f"User {user_id} not found")

# Router converts to HTTP
@router.get("/{user_id}")
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        return await service.get_user(user_id)
    except UserNotFoundError:
        raise HTTPException(404, "User not found")
```

## Async Rules

```python
# GOOD - Async all the way
result = await db.execute(select(User))

# BLOCKED - Sync in async function
result = db.execute(select(User))  # Missing await

# For sync code, use executor
await loop.run_in_executor(None, sync_function)
```

## References

For detailed patterns and examples, see:

| Reference | Content |
|-----------|---------|
| [layer-rules.md](references/layer-rules.md) | Detailed layer separation rules with code examples |
| [dependency-injection.md](references/dependency-injection.md) | DI patterns, authentication, testing with overrides |
| [violation-examples.md](references/violation-examples.md) | Common violations with proper patterns and auto-fix suggestions |

## Related Skills

- `clean-architecture` - DDD patterns
- `fastapi-advanced` - Advanced FastAPI patterns
- `dependency-injection` - DI patterns
- `project-structure-enforcer` - Folder structure

## Capability Details

### layer-separation
**Keywords:** router, service, repository, layer, clean architecture, separation
**Solves:**
- Prevent database operations in routers
- Block business logic in route handlers
- Ensure proper layer boundaries

### dependency-injection
**Keywords:** depends, dependency injection, DI, fastapi depends, inject
**Solves:**
- Enforce use of FastAPI Depends() pattern
- Block direct instantiation in routers
- Ensure testable code structure

### file-naming
**Keywords:** naming convention, file name, router_, _service, _repository
**Solves:**
- Enforce consistent file naming patterns
- Validate router/service/repository naming
- Maintain codebase consistency

### async-patterns
**Keywords:** async, await, sync, blocking call, asyncio
**Solves:**
- Detect sync calls in async functions
- Prevent blocking operations in async code
- Ensure async consistency