---
name: python-ecosystem
description: Modern Python development patterns - uv, ruff, mypy, pyproject.toml, packaging, and Python 3.11+ features. Auto-triggers when working with Python projects.
---

# Python Ecosystem Skill

## Modern Tooling

### Package Management with uv

```bash
# Create new project
uv init my-project
cd my-project

# Add dependencies
uv add fastapi uvicorn
uv add --dev pytest ruff mypy

# Sync environment (replaces pip install -r)
uv sync

# Run commands in managed environment
uv run pytest
uv run python main.py

# Lock dependencies (deterministic builds)
uv lock
```

### pyproject.toml (Single Source of Truth)

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115",
    "uvicorn>=0.30",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.8",
    "mypy>=1.13",
    "pre-commit>=4.0",
]

[project.scripts]
my-cli = "my_project.cli:main"

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "RUF"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

### Linting with Ruff

```bash
# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code (replaces black)
ruff format .

# Check formatting without changes
ruff format --check .
```

| Ruff Rule Set | Purpose                      |
| ------------- | ---------------------------- |
| `E`           | pycodestyle errors           |
| `F`           | pyflakes                     |
| `I`           | isort (import sorting)       |
| `N`           | pep8-naming                  |
| `UP`          | pyupgrade (modernize syntax) |
| `B`           | flake8-bugbear               |
| `SIM`         | flake8-simplify              |
| `RUF`         | ruff-specific rules          |

### Type Checking with mypy

```python
# Type annotations (Python 3.10+ syntax)
def get_users(active: bool = True) -> list[dict[str, str]]:
    ...

# Union types (3.10+)
def parse(value: str | int) -> str:
    ...

# Optional shorthand
def find(name: str) -> User | None:
    ...

# TypedDict for structured dicts
from typing import TypedDict

class UserData(TypedDict):
    name: str
    email: str
    age: int | None
```

## Python 3.11+ Features

### Exception Groups (3.11)

```python
# Raise multiple exceptions
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(risky_operation_1())
        tg.create_task(risky_operation_2())
except* ValueError as eg:
    for exc in eg.exceptions:
        log.error(f"Validation: {exc}")
except* IOError as eg:
    for exc in eg.exceptions:
        log.error(f"IO: {exc}")
```

### tomllib (3.11 - built-in TOML parser)

```python
import tomllib
from pathlib import Path

config = tomllib.loads(Path("config.toml").read_text())
```

### TaskGroup (3.11 - structured concurrency)

```python
async def fetch_all(urls: list[str]) -> list[Response]:
    results = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch(url, results))
    return results
```

### Type Parameter Syntax (3.12)

```python
# 3.12+ generic syntax
type Point[T] = tuple[T, T]

def first[T](items: list[T]) -> T:
    return items[0]

class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)
```

### f-string improvements (3.12)

```python
# Nested quotes allowed in 3.12
msg = f"User {user['name']} has {len(user['items'])} items"
```

## Project Structure

```
my-project/
├── pyproject.toml           # All config in one place
├── uv.lock                  # Deterministic lock file
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   └── test_main.py
└── .pre-commit-config.yaml
```

### src layout vs flat layout

| Layout            | When to Use                              |
| ----------------- | ---------------------------------------- |
| `src/my_project/` | Libraries, packages distributed via PyPI |
| `my_project/`     | Applications, scripts, internal tools    |

## Testing with pytest

### Fixtures

```python
import pytest

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def sample_user(db_session):
    user = User(name="Test", email="test@example.com")
    db_session.add(user)
    db_session.flush()
    return user
```

### Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

### Async tests

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("https://api.example.com")
    assert result.status == 200
```

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

## Common Patterns

### Context Managers

```python
from contextlib import contextmanager, asynccontextmanager

@contextmanager
def managed_resource(path: str):
    resource = open_resource(path)
    try:
        yield resource
    finally:
        resource.close()

@asynccontextmanager
async def managed_connection(url: str):
    conn = await connect(url)
    try:
        yield conn
    finally:
        await conn.close()
```

### dataclasses vs Pydantic

| Use Case                     | Tool                 |
| ---------------------------- | -------------------- |
| Internal data structures     | `dataclasses`        |
| API input/output, validation | `pydantic.BaseModel` |
| Config files                 | `pydantic-settings`  |
| Simple containers            | `NamedTuple`         |

### Logging

```python
import logging

# Module-level logger (never root logger)
logger = logging.getLogger(__name__)

def process_data(data: list[dict]) -> None:
    logger.info("Processing %d items", len(data))
    for item in data:
        logger.debug("Item: %s", item["id"])
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "python", "pyproject", "uv add", "uv sync"
- "ruff", "mypy", "pytest", "type hint"
- "pip install", "requirements.txt", "virtual environment"
- "pydantic", "dataclass", "typing"

## Integration

- **@python-pro** agent: Deep Python expertise
- **testing-patterns** skill: pytest patterns
- **async-patterns** skill: asyncio patterns
