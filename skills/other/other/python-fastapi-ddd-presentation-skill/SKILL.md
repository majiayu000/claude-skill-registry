---
name: python-fastapi-ddd-presentation-skill
description: Guides the FastAPI Presentation layer in a Python DDD + Onion Architecture app (route handler structure, Pydantic request/response schemas, mapping Domain exceptions to HTTP errors, and OpenAPI error documentation), based on the dddpy reference. Use when adding/refactoring endpoints that call UseCases and convert primitives ↔ Value Objects/Entities.
license: Apache-2.0
metadata:
  author: Takahiro Ikeuchi
  version: "1.0.0"
---

# FastAPI Presentation Layer (DDD / Onion Architecture)

This skill focuses on the **Presentation** layer only: FastAPI routes/handlers, Pydantic schemas, and HTTP error mapping. It assumes you already have Domain + UseCase layers and repository wiring.

## Non-negotiables (Onion rule)

- Presentation is the *outermost* layer: it can depend on UseCase and Domain types, but **Domain must not depend on FastAPI/Pydantic**.
- Keep business rules inside Domain/UseCase. Presentation does:
  - request parsing/validation (shape, basic constraints)
  - conversion primitives → Value Objects
  - calling `usecase.execute(...)`
  - mapping Domain exceptions → `HTTPException`
  - conversion Entity → response schema

## Recommended structure (per aggregate)

```
presentation/
  api/
    {aggregate}/
      handlers/
      schemas/
      error_messages/
```

## Implementation checklist (per endpoint)

1. **Depend on UseCase interface** via `Depends(get_*_usecase)`.
2. **Convert** inputs (`UUID`, `str`, etc.) into Domain Value Objects.
3. **Handle ValueError** (from Value Objects) as `400 Bad Request`.
4. **Execute** the use case.
5. **Map Domain exceptions** (e.g., `NotFound`, lifecycle errors) to `404/400`.
6. **Return response model** using `Schema.from_entity(entity)` (or equivalent).
7. **Document errors in OpenAPI** using `responses={...: {'model': ...}}`.

## Route handler pattern (based on dddpy)

Prefer a small “route registrar” class per aggregate.

```python
class TodoApiRouteHandler:
    def register_routes(self, app: FastAPI):
        @app.post("/todos", response_model=TodoSchema, status_code=201)
        def create_todo(
            data: TodoCreateSchema,
            usecase: CreateTodoUseCase = Depends(get_create_todo_usecase),
        ):
            try:
                title = TodoTitle(data.title)
                description = (
                    TodoDescription(data.description) if data.description else None
                )
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e)) from e

            todo = usecase.execute(title, description)
            return TodoSchema.from_entity(todo)
```

## Pydantic schemas

- Request schemas: validate shape + basic constraints (min/max length, optional fields).
- Response schemas: provide `from_entity()` to convert Domain types (UUID/datetime) into JSON-friendly primitives (e.g., timestamps as milliseconds).

For detailed templates and a fuller walk-through, read `references/PRESENTATION.md`.

