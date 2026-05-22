---
name: pep8
description: Enforces modern Python 3.11+ coding standards, PEP 8 compliance, and type-hinting best practices automatically. This skill should be used when writing, reviewing, or refactoring Python code to ensure consistency with PEP 8, proper type hints, Google-style docstrings, and modern Python idioms.
---

# Python Style & PEP 8 Enforcement

Auto-enforce Python 3.11+ standards.

## When to Use

- Writing/reviewing Python code
- Type hint issues or style violations
- User requests PEP 8 check

## Core Standards

| Standard | Desc |
|----------|------|
| PEP 8 | Naming, imports, spacing |
| PEP 484/585 | Type hints (modern) |
| PEP 257 | Docstrings |
| PEP 604 | Union `\|` |
| PEP 570/3102 | `/` positional, `*` keyword |

## Naming

```python
class UserAccount: pass        # PascalCase
class HTTPClient: pass         # Acronyms: all caps
def calculate_total(): pass    # snake_case
async def fetch_data(): pass   # async same

user_name = "john"             # Variables: snake_case
MAX_RETRIES = 3                # Constants: SCREAMING_SNAKE

def _internal(): pass          # Private: underscore
__mangled = "hidden"           # Name mangling: double

T = TypeVar("T")               # TypeVars: PascalCase
UserT = TypeVar("UserT", bound="User")
```

## Type Hints (3.11+)

### Modern Syntax (Required)

```python
# Built-in generics (NOT typing module)
def process(items: list[str]) -> dict[str, int]: ...

# Union w/ | (NOT Optional/Union)
def find_user(id: str) -> User | None: ...

# Self type
from typing import Self
class Builder:
    def chain(self) -> Self: return self
```

### Patterns

```python
from collections.abc import Callable, Awaitable
from typing import TypedDict, Literal, TypeAlias, ParamSpec, Generic

# Callable
Handler = Callable[[Request], Response]
AsyncHandler = Callable[[Request], Awaitable[Response]]

# TypedDict
class UserData(TypedDict):
    id: str
    email: Required[str]
    phone: NotRequired[str | None]

# Literal
Status = Literal["pending", "active", "disabled"]

# TypeAlias
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

# ParamSpec (decorators)
P = ParamSpec("P")
def logged(fn: Callable[P, T]) -> Callable[P, T]: ...

# Generic
class Repo(Generic[T]):
    def get(self, id: str) -> T | None: ...
```

### Deprecated (Never Use)

```python
# WRONG                          # RIGHT
List[str]                        # list[str]
Optional[int]                    # int | None
Dict[str, int]                   # dict[str, int]
Tuple[int, str]                  # tuple[int, str]
Union[int, str]                  # int | str
```

## Docstrings (Google Style)

```python
def calculate_discount(price: float, percent: float, min_price: float = 0.0) -> float:
    """Calculate discounted price w/ floor.

    Args:
        price: Original price.
        percent: Discount (0-100).
        min_price: Min allowed price.

    Returns:
        Final price, never below min_price.

    Raises:
        ValueError: If invalid inputs.
    """
```

**Skip docstrings for:** self-documenting fns, `_private` methods, trivial `@property`

## Imports

```python
# 1. Stdlib (alphabetical)
import asyncio
from pathlib import Path
from typing import Any

# 2. Third-party
import httpx
from fastapi import Depends, HTTPException
from pydantic import BaseModel

# 3. Local
from app.core.config import settings
from app.models import User
```

**Rules:** No wildcards (`*`), group from same module, parentheses for long imports

## Function Signatures (PEP 570/3102)

```python
def api_fn(
    x: int, y: int,           # positional-only
    /,
    z: int = 0,               # positional or keyword
    *,
    strict: bool = False,     # keyword-only
) -> Result: ...

# Prevents: api_fn(x=1, y=2) - forces positional
# Requires: api_fn(1, 2, strict=True) - explicit keyword
```

### Overloads

```python
from typing import overload

@overload
def process(v: int) -> int: ...
@overload
def process(v: str) -> str: ...
def process(v: int | str) -> int | str:
    return v * 2 if isinstance(v, int) else v.upper()
```

## Function Design

| Lines | Status |
|-------|--------|
| < 20 | Ideal |
| 20-30 | OK |
| 30-50 | Split |
| > 50 | Refactor |

**Params:** Max 5 → use dataclass/config obj for more
**Returns:** Always annotate; no flag-based return types

## Exception Handling

```python
# DO: Specific exceptions w/ context
try:
    user = await db.get(User, id)
except IntegrityError as e:
    raise UserExistsError(id) from e

# DO: Context managers
async with AsyncSession(engine) as session:
    async with session.begin(): ...

# DON'T
except:           # bare - catches SystemExit
except Exception: # swallows errors
    pass          # silent - at minimum log
```

## Constants

```python
MAX_RETRIES = 3
DEFAULT_TIMEOUT = timedelta(seconds=30)
FORMATS = frozenset({"json", "xml"})

class Status(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"

# NO magic values
await asyncio.sleep(5)         # Bad
await asyncio.sleep(INTERVAL)  # Good
```

## Async

```python
# Context managers
async with httpx.AsyncClient() as client:
    resp = await client.get(url)

# Concurrent
results = await asyncio.gather(fetch_a(), fetch_b(), return_exceptions=True)

# TaskGroup (3.11+)
async with asyncio.TaskGroup() as tg:
    tg.create_task(fetch_a())
    tg.create_task(fetch_b())

# Timeout
async with asyncio.timeout(5.0):
    await slow_op()

# Never block loop
await asyncio.to_thread(blocking_io)  # sync I/O
await asyncio.sleep(1)                # NOT time.sleep()
```

## Pathlib (NOT os.path)

```python
from pathlib import Path

data = Path("data") / "config.json"
text = data.read_text(encoding="utf-8")
data.write_text(json.dumps(obj))

path.parent   # dir
path.stem     # name w/o ext
path.suffix   # .ext
path.name     # filename
```

## Logging

```python
logger = logging.getLogger(__name__)

# Lazy formatting (NOT f-strings)
logger.info("Processing %s items", count)  # YES
logger.info(f"Processing {count}")         # NO - always evaluated

# Exception
logger.exception("Failed")  # auto-includes traceback
```

## Data Models

| Type | Use Case |
|------|----------|
| TypedDict | External JSON/dicts |
| dataclass | Internal DTOs |
| Pydantic | Validation needed |
| NamedTuple | Immutable, hashable |

## Context Managers

```python
from contextlib import suppress, asynccontextmanager

# suppress replaces try/except pass
with suppress(FileNotFoundError):
    Path("temp.txt").unlink()

@asynccontextmanager
async def connection():
    conn = await create()
    try: yield conn
    finally: await conn.close()
```

## Anti-Patterns

| Bad | Fix |
|-----|-----|
| No type hints | Type all params & returns |
| `List`, `Optional` | `list`, `\| None` |
| Bare `except:` | Specific exceptions |
| Magic numbers | Named constants |
| `d`, `x`, `temp` | Descriptive names |
| `process()` | `process_orders()` |
| > 50 lines | Split fn |
| Mutable defaults | `None` + factory |
| `== None` | `is None` |
| f-strings in logger | `%s` formatting |
| os.path | pathlib |

## Python 3.11+ Features

```python
# match/case
match cmd:
    case {"action": "create", "data": d}: create(d)
    case _: raise ValueError()

# Exception groups
except* ValueError as eg:
    for e in eg.exceptions: handle(e)

# tomllib (built-in TOML)
import tomllib
config = tomllib.load(open("config.toml", "rb"))

# Self type
from typing import Self
def build(self) -> Self: return self
```

## Formatting

- Line: 88 (Black) or 79 (strict PEP 8)
- Indent: 4 spaces
- Blanks: 2 top-level, 1 methods
- Trailing commas in multi-line

## Scripts

Available in `scripts/`:

| Script | Purpose | Usage |
|--------|---------|-------|
| `check_style.py` | Full check (ruff + pycodestyle + mypy) | `python check_style.py src/ --fix` |
| `check_pep8.sh` | Quick PEP 8 only | `./check_pep8.sh script.py` |
| `check_types.sh` | Type hints only | `./check_types.sh src/ --strict` |
| `fix_style.sh` | Auto-fix issues | `./fix_style.sh src/` |

**Install deps:** `pip install ruff pycodestyle mypy`

## Tooling

### pyproject.toml

```toml
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "N", "RUF", "ASYNC", "S"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.mypy]
python_version = "3.11"
strict = true
```

### Pre-commit

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
```