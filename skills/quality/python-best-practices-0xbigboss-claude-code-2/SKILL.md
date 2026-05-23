---
name: python-best-practices
description: Provides Python patterns for type-first development with dataclasses, discriminated unions, NewType, and Protocol. Must use when reading or writing Python files.
---

# Python Best Practices

## Type-First Development

Types define the contract before implementation. Follow this workflow:

1. **Define data models** - dataclasses, Pydantic models, or TypedDict first
2. **Define function signatures** - parameter and return type hints
3. **Implement to satisfy types** - let the type checker guide completeness
4. **Validate at boundaries** - runtime checks where data enters the system

### Make Illegal States Unrepresentable

Use Python's type system to prevent invalid states at type-check time.

**Dataclasses for structured data:**
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class User:
    id: str
    email: str
    name: str
    created_at: datetime

@dataclass(frozen=True)
class CreateUser:
    email: str
    name: str

# Frozen dataclasses are immutable - no accidental mutation
```

**Discriminated unions with Literal:**
```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class Idle:
    status: Literal["idle"] = "idle"

@dataclass
class Loading:
    status: Literal["loading"] = "loading"

@dataclass
class Success:
    status: Literal["success"] = "success"
    data: str

@dataclass
class Failure:
    status: Literal["error"] = "error"
    error: Exception

RequestState = Idle | Loading | Success | Failure

def handle_state(state: RequestState) -> None:
    match state:
        case Idle():
            pass
        case Loading():
            show_spinner()
        case Success(data=data):
            render(data)
        case Failure(error=err):
            show_error(err)
```

**NewType for domain primitives:**
```python
from typing import NewType

UserId = NewType("UserId", str)
OrderId = NewType("OrderId", str)

def get_user(user_id: UserId) -> User:
    # Type checker prevents passing OrderId here
    ...

def create_user_id(raw: str) -> UserId:
    return UserId(raw)
```

**Enums for constrained values:**
```python
from enum import Enum, auto

class Role(Enum):
    ADMIN = auto()
    USER = auto()
    GUEST = auto()

def check_permission(role: Role) -> bool:
    match role:
        case Role.ADMIN:
            return True
        case Role.USER:
            return limited_check()
        case Role.GUEST:
            return False
    # Type checker warns if case is missing
```

**Protocol for structural typing:**
```python
from typing import Protocol

class Readable(Protocol):
    def read(self, n: int = -1) -> bytes: ...

def process_input(source: Readable) -> bytes:
    # Accepts any object with a read() method
    return source.read()
```

**TypedDict for external data shapes:**
```python
from typing import TypedDict, Required, NotRequired

class UserResponse(TypedDict):
    id: Required[str]
    email: Required[str]
    name: Required[str]
    avatar_url: NotRequired[str]

def parse_user(data: dict) -> UserResponse:
    # Runtime validation needed - TypedDict is structural
    return UserResponse(
        id=data["id"],
        email=data["email"],
        name=data["name"],
    )
```

## Module Structure

Prefer smaller, focused files: one class or closely related set of functions per module. Split when a file handles multiple concerns or exceeds ~300 lines. Use `__init__.py` to expose public API; keep implementation details in private modules (`_internal.py`). Colocate tests in `tests/` mirroring the source structure.

## Functional Patterns

- Use list/dict/set comprehensions and generator expressions over explicit loops.
- Prefer `@dataclass(frozen=True)` for immutable data; avoid mutable default arguments.
- Use `functools.partial` for partial application; compose small functions over large classes.
- Avoid class-level mutable state; prefer pure functions that take inputs and return outputs.

## Instructions

- Raise descriptive exceptions for unsupported cases; every code path returns a value or raises. This makes failures debuggable and prevents silent corruption.
- Propagate exceptions with context using `from err`; catching requires re-raising or returning a meaningful result. Swallowed exceptions hide root causes.
- Handle edge cases explicitly: empty inputs, `None`, boundary values. Include `else` clauses in conditionals where appropriate.
- Use context managers for I/O; prefer `pathlib` and explicit encodings. Resource leaks cause production issues.
- Add or adjust unit tests when touching logic; prefer minimal repros that isolate the failure.

## Examples

Explicit failure for unimplemented logic:
```python
def build_widget(widget_type: str) -> Widget:
    raise NotImplementedError(f"build_widget not implemented for type: {widget_type}")
```

Propagate with context to preserve the original traceback:
```python
try:
    data = json.loads(raw)
except json.JSONDecodeError as err:
    raise ValueError(f"invalid JSON payload: {err}") from err
```

Exhaustive match with explicit default:
```python
def process_status(status: str) -> str:
    match status:
        case "active":
            return "processing"
        case "inactive":
            return "skipped"
        case _:
            raise ValueError(f"unhandled status: {status}")
```

Debug-level tracing with namespaced logger:
```python
import logging

logger = logging.getLogger("myapp.widgets")

def create_widget(name: str) -> Widget:
    logger.debug("creating widget: %s", name)
    widget = Widget(name=name)
    logger.debug("created widget id=%s", widget.id)
    return widget
```

## Configuration

- Load config from environment variables at startup; validate required values before use. Missing config should fail immediately.
- Define a config dataclass or Pydantic model as single source of truth; avoid `os.getenv` scattered throughout code.
- Use sensible defaults for development; require explicit values for production secrets.

### Examples

Typed config with dataclass:
```python
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    port: int = 3000
    database_url: str = ""
    api_key: str = ""
    env: str = "development"

    @classmethod
    def from_env(cls) -> "Config":
        database_url = os.environ.get("DATABASE_URL", "")
        if not database_url:
            raise ValueError("DATABASE_URL is required")
        return cls(
            port=int(os.environ.get("PORT", "3000")),
            database_url=database_url,
            api_key=os.environ["API_KEY"],  # required, will raise if missing
            env=os.environ.get("ENV", "development"),
        )

config = Config.from_env()
```

## Optional: ty

For fast type checking, consider [ty](https://docs.astral.sh/ty/) from Astral (creators of ruff and uv). Written in Rust, it's significantly faster than mypy or pyright.

**Installation and usage:**
```bash
# Run directly with uvx (no install needed)
uvx ty check

# Check specific files
uvx ty check src/main.py

# Install permanently
uv tool install ty
```

**Key features:**
- Automatic virtual environment detection (via `VIRTUAL_ENV` or `.venv`)
- Project discovery from `pyproject.toml`
- Fast incremental checking
- Compatible with standard Python type hints

**Configuration in `pyproject.toml`:**
```toml
[tool.ty]
python-version = "3.12"
```

**When to use ty vs alternatives:**
- `ty` - fastest, good for CI and large codebases (early stage, rapidly evolving)
- `pyright` - most complete type inference, VS Code integration
- `mypy` - mature, extensive plugin ecosystem
