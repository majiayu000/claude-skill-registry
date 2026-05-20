---
name: python-guide
description: |
  Python guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Python files (.py), requirements.txt, pyproject.toml,
  or when the user mentions Python. Provides type hint conventions, virtual environment
  standards, testing with pytest, and async patterns.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: python
  extensions: ".py"
---

# Python Guide

> Applies to: Python 3.11+, APIs, CLIs, Data Pipelines, Automation

## Core Principles

1. **Type Hints Everywhere**: All function signatures, class attributes, and module-level variables must have type annotations
2. **Explicit Over Implicit**: No `*` imports, no mutable default arguments, no implicit type coercions
3. **Virtual Environments Always**: Never install into system Python; use `venv`, `uv`, or `poetry`
4. **Pytest Over unittest**: Use pytest for all testing; fixtures and parametrize over setUp/tearDown
5. **PEP 8 + Ruff**: Enforce style mechanically; never rely on manual formatting

## Guardrails

### Python Version

- Target Python 3.11+ (use `match` statements, `ExceptionGroup`, `tomllib`)
- Set `requires-python = ">=3.11"` in `pyproject.toml`
- Use `from __future__ import annotations` for forward references in 3.11
- Never use features removed in 3.12+ (`distutils`, `imp`, legacy `typing` aliases)

### Code Style

- Run `ruff check` and `ruff format` before every commit
- Max line length: 88 characters (Black default)
- Imports: stdlib, blank line, third-party, blank line, local (enforced by `isort`/`ruff`)
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_SNAKE` for constants
- No bare `except:` — always catch specific exceptions
- No mutable default arguments (`def f(items=None):` not `def f(items=[]):`)
- Prefer f-strings over `.format()` or `%` formatting
- Use `pathlib.Path` instead of `os.path` for all file operations

### Type Hints

- All public functions MUST have full type annotations (params + return)
- Use `collections.abc` types: `Sequence`, `Mapping`, `Iterable` (not `List`, `Dict`)
- Use `X | None` union syntax (not `Optional[X]`)
- Use `TypeAlias` for complex types: `UserMap: TypeAlias = dict[str, User]`
- Use `Protocol` for structural subtyping (duck typing with safety)
- Use `@overload` for functions returning different types based on input
- Run `mypy --strict` in CI (no `type: ignore` without explanation)

```python
from collections.abc import Sequence

def find_users(
    ids: Sequence[str],
    *,
    active_only: bool = True,
) -> list[User]:
    """Fetch users by ID list, optionally filtering inactive."""
    ...
```

### Error Handling

- Never use bare `except:` or `except Exception:` without re-raising
- Create domain-specific exception hierarchies rooted in a base class
- Use `raise ... from err` to preserve exception chains
- Log at the boundary, raise in the interior (don't log-and-raise)
- Use `contextlib.suppress()` instead of empty except blocks
- Always close resources with `with` statements or `contextlib.closing`

### Dependencies

- Define all deps in `pyproject.toml` (not `setup.py` or bare `requirements.txt`)
- Pin exact versions in lock files (`uv.lock`, `poetry.lock`, `pip-compile` output)
- Keep `requirements.txt` only as a generated artifact, never hand-edited
- Separate `[project.optional-dependencies]` for dev, test, docs
- Audit with `pip-audit` or `safety` before adding new packages
- Prefer stdlib solutions: `tomllib`, `pathlib`, `dataclasses`, `enum`, `logging`

## Project Structure

```
myproject/
├── src/
│   └── myproject/          # Importable package (src layout)
│       ├── __init__.py
│       ├── py.typed         # PEP 561 marker for type stubs
│       ├── domain/          # Business logic, entities
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── exceptions.py
│       ├── service/         # Application services
│       │   └── __init__.py
│       ├── repository/      # Data access layer
│       │   └── __init__.py
│       └── api/             # HTTP/CLI interface
│           └── __init__.py
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── unit/
│   └── integration/
├── pyproject.toml           # Single source of truth for config
├── uv.lock                  # Or poetry.lock
└── README.md
```

- Use **src layout** (`src/myproject/`) to prevent accidental local imports
- Keep `conftest.py` at test root for shared fixtures; nest for scope
- Include `py.typed` marker for downstream type checking
- No `__init__.py` in `tests/` (pytest discovers without it)
- One module = one responsibility; split at ~200 lines

## Error Handling Patterns

### Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for the application."""

    def __init__(self, message: str, *, code: str = "UNKNOWN") -> None:
        super().__init__(message)
        self.code = code


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            f"{resource} with id '{identifier}' not found",
            code="NOT_FOUND",
        )
        self.resource = resource
        self.identifier = identifier


class ValidationError(AppError):
    """Raised when input data fails validation."""

    def __init__(self, field: str, reason: str) -> None:
        super().__init__(
            f"Validation failed for '{field}': {reason}",
            code="VALIDATION_ERROR",
        )
```

### Context Managers for Cleanup

```python
from contextlib import contextmanager
from collections.abc import Generator

@contextmanager
def managed_connection(url: str) -> Generator[Connection, None, None]:
    conn = Connection(url)
    try:
        conn.open()
        yield conn
    except ConnectionError as err:
        raise AppError("Database unavailable") from err
    finally:
        conn.close()
```

### Error Chaining

```python
def get_user(user_id: str) -> User:
    try:
        row = db.fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
    except DatabaseError as err:
        raise AppError(f"Failed to fetch user {user_id}") from err
    if row is None:
        raise NotFoundError("User", user_id)
    return User.from_row(row)
```

## Testing

### Standards

- Test files: `test_*.py` (same name as module: `models.py` -> `test_models.py`)
- Test functions: `test_<unit>_<scenario>_<expected>` (e.g., `test_get_user_not_found_raises`)
- Use `conftest.py` for fixtures shared across a directory
- Coverage target: >80% for business logic, >60% overall
- Mark slow tests: `@pytest.mark.slow` and exclude from default runs
- No `unittest.TestCase` — use plain functions with pytest assertions
- Use `tmp_path` fixture for file operations (auto-cleanup)

### Fixtures and Parametrize

```python
import pytest
from myproject.domain.models import User

@pytest.fixture
def sample_user() -> User:
    return User(id="u-123", name="Ada Lovelace", email="ada@example.com")


@pytest.mark.parametrize(
    ("email", "is_valid"),
    [
        ("user@example.com", True),
        ("user@.com", False),
        ("", False),
        ("user@domain", False),
    ],
)
def test_validate_email(email: str, is_valid: bool) -> None:
    assert validate_email(email) == is_valid


def test_get_user_returns_user(sample_user: User) -> None:
    repo = InMemoryUserRepo(users=[sample_user])
    result = repo.get("u-123")
    assert result == sample_user


def test_get_user_not_found_raises() -> None:
    repo = InMemoryUserRepo(users=[])
    with pytest.raises(NotFoundError, match="User.*not found"):
        repo.get("nonexistent")
```

### Mocking External Dependencies

```python
from unittest.mock import AsyncMock, patch

async def test_send_notification_retries_on_failure() -> None:
    mock_client = AsyncMock()
    mock_client.post.side_effect = [ConnectionError, None]

    with patch("myproject.service.notify.http_client", mock_client):
        await send_notification(user_id="u-123", message="hello")

    assert mock_client.post.call_count == 2
```

## Tooling

### pyproject.toml Configuration

```toml
[project]
name = "myproject"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = ["ruff", "mypy", "pytest", "pytest-cov", "pytest-asyncio"]

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "S",    # flake8-bandit (security)
    "A",    # flake8-builtins
    "C4",   # flake8-comprehensions
    "SIM",  # flake8-simplify
    "RUF",  # ruff-specific rules
]

[tool.mypy]
strict = true
warn_return_any = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["slow: marks tests as slow (deselect with '-m \"not slow\"')"]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["src/myproject"]
branch = true

[tool.coverage.report]
fail_under = 60
show_missing = true
exclude_lines = ["if TYPE_CHECKING:", "pragma: no cover"]
```

### Essential Commands

```bash
ruff check .                 # Lint (replaces flake8, isort, pyupgrade)
ruff format .                # Format (replaces black)
mypy .                       # Type check (strict mode)
pytest                       # Run all tests
pytest --cov=src -q          # Coverage summary
pytest -m "not slow"         # Skip slow tests
pip-audit                    # Check dependencies for vulnerabilities
python -m build              # Build sdist + wheel
```

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Async patterns, dataclass/Pydantic models, context managers, decorators, type hints (generics, Protocol, TypeVar)
- [references/pitfalls.md](references/pitfalls.md) -- Common Python gotchas and do/don't examples
- [references/security.md](references/security.md) -- Input sanitization, secrets management, SQL injection prevention

## External References

- [PEP 8 -- Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 -- Type Hints](https://peps.python.org/pep-0484/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Effective Python (Brett Slatkin)](https://effectivepython.com/)
