---
name: python-core
description: "Comprehensive Python development expertise covering modern best practices, type hints, FastAPI web development, async/await, testing, and performance optimization. Use when working on Python projects requiring guidance on: (1) Modern Python features and best practices, (2) Type hints and static typing with mypy, (3) FastAPI web development, (4) Async/await and asyncio patterns, (5) Testing with pytest, (6) Data validation with Pydantic, (7) Database integration (SQLAlchemy), (8) Project structure and dependencies, (9) Performance optimization, (10) Logging and observability, or (11) Code reviews and common errors."
---

# Python Core Development

Comprehensive guidance for modern Python development with focus on FastAPI, type safety, and best practices.

## Quick Reference Guide

### By Task Type

**Getting Started**
- **New Project**: Use `scripts/init_python_project.sh` for FastAPI or package projects
- **Core Principles**: See [references/principles.md](references/principles.md) for PEP 8 and Python philosophy
- **Common Errors**: See [references/common-errors.md](references/common-errors.md) for solutions

**Writing Code**
- **Type Hints**: See [references/type-hints.md](references/type-hints.md) for annotations and mypy
- **Async Programming**: See [references/async-patterns.md](references/async-patterns.md) for asyncio patterns
- **Testing**: See [references/testing.md](references/testing.md) for pytest strategies

**Web Development (FastAPI)**
- **FastAPI Guide**: See [references/fastapi-guide.md](references/fastapi-guide.md) for comprehensive tutorial
- **Essential Libraries**: See [references/common-libraries.md](references/common-libraries.md)

**Code Quality**
- **Code Review**: See [references/code-review.md](references/code-review.md) for checklist
- **Performance**: See [references/performance.md](references/performance.md) for optimization

**Project Management**
- **Dependencies**: See [references/dependencies.md](references/dependencies.md) for pip, poetry, uv
- **Project Structure**: See [references/project-structure.md](references/project-structure.md)

### By Question Type

| Question | Reference |
|----------|-----------|
| "How do I build a FastAPI app?" | [fastapi-guide.md](references/fastapi-guide.md) |
| "How do I add type hints?" | [type-hints.md](references/type-hints.md) |
| "How do I use async/await?" | [async-patterns.md](references/async-patterns.md) |
| "How do I test this?" | [testing.md](references/testing.md) |
| "What are Python best practices?" | [principles.md](references/principles.md) |
| "How do I structure my project?" | [project-structure.md](references/project-structure.md) |
| "What libraries should I use?" | [common-libraries.md](references/common-libraries.md) |
| "How do I manage dependencies?" | [dependencies.md](references/dependencies.md) |
| "How do I improve performance?" | [performance.md](references/performance.md) |
| "Why am I getting this error?" | [common-errors.md](references/common-errors.md) |

## Core Workflows

### 1. Starting a FastAPI Project

1. **Initialize Project**
   ```bash
   ./scripts/init_python_project.sh my-api fastapi
   cd my-api
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install fastapi uvicorn[standard] sqlalchemy pydantic
   pip install pytest mypy ruff --dev
   ```

3. **Configure Tools**
   - Copy `assets/configs/ruff.toml` for linting
   - Copy `assets/configs/mypy.ini` for type checking
   - Copy `assets/configs/pytest.ini` for testing

4. **Start Development**
   ```bash
   uvicorn app.main:app --reload
   ```
   Visit `http://localhost:8000/docs` for automatic API documentation

### 2. Building a FastAPI Endpoint

1. **Define Pydantic Models**
   ```python
   from pydantic import BaseModel, EmailStr

   class UserCreate(BaseModel):
       username: str
       email: EmailStr
       password: str

   class User(BaseModel):
       id: int
       username: str
       email: EmailStr
       is_active: bool = True
   ```

2. **Create Endpoint**
   ```python
   from fastapi import FastAPI, Depends, HTTPException
   from sqlalchemy.orm import Session

   app = FastAPI()

   @app.post("/users/", response_model=User)
   async def create_user(
       user: UserCreate,
       db: Session = Depends(get_db)
   ):
       db_user = crud.create_user(db, user)
       return db_user
   ```

3. **Add Tests**
   ```python
   from fastapi.testclient import TestClient

   def test_create_user():
       response = client.post(
           "/users/",
           json={"username": "test", "email": "test@example.com", "password": "secret"}
       )
       assert response.status_code == 200
       assert response.json()["username"] == "test"
   ```

### 3. Code Quality Workflow

1. **Type Check**
   ```bash
   mypy app/
   ```

2. **Lint and Format**
   ```bash
   ruff check app/
   ruff format app/
   ```

3. **Run Tests**
   ```bash
   pytest --cov=app
   ```

4. **Security Audit**
   ```bash
   ./scripts/audit_dependencies.sh
   ```

## Decision Guides

### When to Use FastAPI vs Django vs Flask

**Use FastAPI when:**
- Building modern REST APIs
- Need automatic OpenAPI/Swagger docs
- Want async/await support
- Type safety is important
- Performance is critical

**Use Django when:**
- Building full-stack web applications
- Need admin interface out of the box
- Want ORM with migrations
- Building monolithic applications

**Use Flask when:**
- Need maximum flexibility
- Building small to medium APIs
- Want lightweight framework
- Learning web development

See [fastapi-guide.md](references/fastapi-guide.md) for comprehensive FastAPI patterns.

### Type Hints Strategy

**Always use type hints for:**
- Public function signatures
- Class attributes
- Function return types
- Complex data structures

**Example:**
```python
from typing import Optional

def process_data(
    items: list[str],
    filter_fn: Optional[callable] = None
) -> dict[str, int]:
    """Process items and return counts."""
    return {item: len(item) for item in items}
```

See [type-hints.md](references/type-hints.md) for advanced patterns.

### Async vs Sync

**Use async when:**
- I/O-bound operations (HTTP requests, database queries)
- Need high concurrency
- Using FastAPI (built for async)
- Working with async libraries (httpx, asyncpg)

**Use sync when:**
- CPU-bound operations
- Simple scripts
- Libraries don't support async
- Complexity isn't justified

See [async-patterns.md](references/async-patterns.md) for asyncio patterns.

## Automation Scripts

### `scripts/init_python_project.sh`
Initialize a new Python project with best practices:
- FastAPI or package structure
- pyproject.toml with modern config
- Development dependencies (pytest, mypy, ruff)
- Proper .gitignore

Usage: `./scripts/init_python_project.sh my-project [package|fastapi]`

### `scripts/audit_dependencies.sh`
Audit dependencies for security vulnerabilities:
- Runs pip-audit for known CVEs
- Checks for outdated packages

Usage: `./scripts/audit_dependencies.sh`

### `scripts/setup_logging.sh`
Set up structured logging with structlog:
- Installs structlog
- Creates configuration file
- JSON logging for production

Usage: `./scripts/setup_logging.sh`

## Configuration Templates

### `assets/configs/ruff.toml`
Modern Python linter and formatter configuration:
- 100 character line length
- Comprehensive rule selection
- Import sorting

### `assets/configs/mypy.ini`
Static type checker configuration:
- Strict mode enabled
- Python 3.11+ features
- Comprehensive warnings

### `assets/configs/pytest.ini`
Testing framework configuration:
- Coverage reporting
- Async test support
- HTML coverage reports

### `assets/configs/pyproject.toml`
Complete project configuration template:
- FastAPI dependencies
- Development tools
- Tool configurations

## Reference Documentation

### Core Python
- **[principles.md](references/principles.md)** - PEP 8, Zen of Python, best practices
- **[type-hints.md](references/type-hints.md)** - Type annotations, mypy, protocols
- **[async-patterns.md](references/async-patterns.md)** - asyncio, async/await, concurrency

### Development
- **[testing.md](references/testing.md)** - pytest, fixtures, mocking, coverage
- **[project-structure.md](references/project-structure.md)** - Package layout, src/ pattern
- **[dependencies.md](references/dependencies.md)** - pip, poetry, uv, pyproject.toml
- **[performance.md](references/performance.md)** - Profiling, optimization strategies
- **[code-review.md](references/code-review.md)** - Review checklist, anti-patterns

### Web Development
- **[fastapi-guide.md](references/fastapi-guide.md)** - Comprehensive FastAPI tutorial
- **[common-libraries.md](references/common-libraries.md)** - Essential Python packages

### Troubleshooting
- **[common-errors.md](references/common-errors.md)** - Common mistakes and solutions

## FastAPI Quick Start

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My API")

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

Run: `uvicorn main:app --reload`

Docs: `http://localhost:8000/docs`

## Best Practices Summary

1. **Use type hints everywhere** - Enable mypy strict mode
2. **Follow PEP 8** - Use ruff for linting and formatting
3. **Write tests** - Aim for 80%+ coverage with pytest
4. **Use async for I/O** - FastAPI is built for async
5. **Validate with Pydantic** - Type-safe data validation
6. **Structure projects properly** - Use src/ layout
7. **Document code** - Docstrings and type hints
8. **Handle errors explicitly** - Specific exception types
9. **Audit dependencies** - Regular security checks
10. **Profile before optimizing** - Measure, don't guess

## Example: Complete FastAPI Application

See [fastapi-guide.md](references/fastapi-guide.md) for:
- Database integration with SQLAlchemy
- Authentication with JWT
- File uploads
- WebSocket support
- Background tasks
- Testing strategies
- Deployment patterns
- Project structure

## When to Consult References

**Load references progressively:**

1. **Starting out**: Read [principles.md](references/principles.md) for Python fundamentals
2. **Building web API**: Consult [fastapi-guide.md](references/fastapi-guide.md)
3. **Adding types**: Reference [type-hints.md](references/type-hints.md)
4. **Going async**: See [async-patterns.md](references/async-patterns.md)
5. **Testing**: Use [testing.md](references/testing.md)
6. **Debugging**: Check [common-errors.md](references/common-errors.md)
7. **Reviewing**: Use [code-review.md](references/code-review.md) checklist
8. **Optimizing**: See [performance.md](references/performance.md)

Don't load all references at once—consult them as needs arise.
