---
name: fastapi-rest-api-skill
description: A skill for building RESTful APIs with FastAPI. Use this skill to create a new FastAPI project with a standard project structure, including routers, models, schemas, and services. This skill provides a boilerplate project, CRUD endpoint templates, Pydantic validation examples, and guidance on dependency injection, background tasks, file uploads, and pagination. It leverages async/await for efficient I/O operations. Trigger this skill when a user wants to build a RESTful API using FastAPI, needs a starter project, or wants to learn best practices for FastAPI development.
---

# FastAPI RESTful API Builder Skill

This skill helps you build robust and scalable RESTful APIs using FastAPI. It provides a boilerplate project and documentation on best practices.

## Quickstart

To create a new FastAPI project, copy the boilerplate project from the `assets/fastapi-boilerplate` directory.

```bash
cp -r assets/fastapi-boilerplate /path/to/your/new/project
```

This boilerplate includes:
- A recommended project structure with `app/routers`, `app/models`, `app/schemas`, and `app/services`.
- A working example of a CRUD API for an `items` resource.
- SQLAlchemy integration with a SQLite database.
- Pydantic models for request and response validation.

## Core Concepts and Patterns

This skill promotes a set of best practices for FastAPI development. For detailed explanations and code examples, refer to the following documents in the `references/` directory.

- **[CRUD Router Template](references/crud_template.md)**: A template for creating CRUD endpoints for a resource.
- **[Pydantic Schemas for Validation](references/pydantic_schemas.md)**: How to use Pydantic for data validation and serialization.
- **[Service Layer Pattern](references/service_layer.md)**: How to separate business logic from the API layer.
- **[Dependency Injection](references/dependency_injection.md)**: How to use FastAPI's dependency injection system.
- **[Advanced Features](references/advanced_features.md)**: Covers background tasks, file uploads, and pagination.

## Asynchronous Operations

FastAPI is built on `asyncio` and supports asynchronous code using `async` and `await`. This is crucial for I/O-bound operations like database queries or external API calls, as it allows your server to handle multiple requests concurrently without blocking.

When defining your path operations, you can use `async def`:

```python
@app.get("/")
async def read_root():
    # Asynchronous database call
    results = await db.fetch_all("SELECT * FROM items")
    return results
```

Ensure that any I/O-bound libraries you use have async support (e.g., `databases`, `httpx`).
