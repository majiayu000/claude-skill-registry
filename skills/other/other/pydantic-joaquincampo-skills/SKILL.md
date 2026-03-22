---
name: pydantic
description: "Pydantic v2 best practices and correct syntax. Use when code imports pydantic, uses BaseModel, Field, field_validator, model_validator, ConfigDict, TypeAdapter. Triggers on: Pydantic, data validation, model serialization, API schemas. Corrects common v1 patterns LLMs generate."
---

# Pydantic v2 (Latest: v2.12.5)

Write correct Pydantic v2 code. LLMs commonly generate deprecated v1 patterns — follow this guide strictly.

## Critical Rules — Never Violate These

### 1. No `class Config:` — Use `model_config = ConfigDict(...)`

```python
# WRONG
class MyModel(BaseModel):
    class Config:
        frozen = True

# CORRECT
from pydantic import BaseModel, ConfigDict

class MyModel(BaseModel):
    model_config = ConfigDict(frozen=True)
```

### 2. No `@validator` — Use `@field_validator`

```python
# WRONG
from pydantic import validator

@validator('name')
def check(cls, v):
    return v

# CORRECT
from pydantic import field_validator

@field_validator('name')
@classmethod
def check(cls, v: str) -> str:
    if not v.strip():
        raise ValueError('empty')
    return v.strip()
```

Key differences from v1:
- `@classmethod` is **required**
- `pre=True` becomes `mode='before'` (default is `mode='after'`)
- `each_item=True` is **removed** — use `Annotated` on inner type instead
- `always=True` is **removed** — use `validate_default=True` in Field() or config
- `values` parameter is **gone** — use `info: ValidationInfo` and `info.data`
- **Must explicitly return** the value (forgetting return silently sets field to None)

### 3. No `@root_validator` — Use `@model_validator`

```python
# WRONG
from pydantic import root_validator

@root_validator
def check(cls, values):
    return values

# CORRECT — mode='after' (instance method, NOT classmethod)
from pydantic import model_validator
from typing import Self

@model_validator(mode='after')
def check(self) -> Self:
    if self.password != self.confirm:
        raise ValueError('mismatch')
    return self

# CORRECT — mode='before' (classmethod, receives raw data)
@model_validator(mode='before')
@classmethod
def preprocess(cls, data: Any) -> Any:
    if isinstance(data, dict):
        # transform data
        pass
    return data
```

### 4. No `.dict()` / `.json()` — Use `.model_dump()` / `.model_dump_json()`

| v1 (REMOVED)              | v2 (CORRECT)                  |
|---------------------------|-------------------------------|
| `.dict()`                 | `.model_dump()`               |
| `.json()`                 | `.model_dump_json()`          |
| `.parse_obj(data)`        | `.model_validate(data)`       |
| `.parse_raw(json_str)`    | `.model_validate_json(json)`  |
| `.schema()`               | `.model_json_schema()`        |
| `.copy(update={...})`     | `.model_copy(update={...})`   |
| `.construct(**data)`      | `.model_construct(**data)`    |
| `.update_forward_refs()`  | `.model_rebuild()`            |
| `.__fields__`             | `.model_fields`               |
| `.__fields_set__`         | `.model_fields_set`           |

### 5. `constr` / `conint` / `confloat` Are Legacy — Prefer `Annotated`

These helpers still work in Pydantic v2 without deprecation warnings, but the `Annotated` pattern is the recommended modern style. Prefer `Annotated` in new code; no need to urgently rewrite existing uses.

```python
# LEGACY (works, but discouraged in new code)
from pydantic import constr, conint
name: constr(min_length=1, max_length=50)
age: conint(ge=0)

# RECOMMENDED
from typing import Annotated
from pydantic import Field
from pydantic.types import StringConstraints

name: Annotated[str, StringConstraints(min_length=1, max_length=50)]
age: Annotated[int, Field(ge=0)]
```

### 6. No `GenericModel` — Use `BaseModel` + `Generic[T]`

```python
# WRONG
from pydantic.generics import GenericModel

# CORRECT
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    count: int
```

### 7. No `__root__` — Use `RootModel`

```python
# WRONG
class Items(BaseModel):
    __root__: list[str]

# CORRECT
from pydantic import RootModel

class Items(RootModel[list[str]]):
    pass
```

### 8. `Optional[X]` Does NOT Imply `default=None`

```python
# v2: This is REQUIRED (no default!)
name: str | None

# v2: This has a default of None
name: str | None = None
```

---

## Config Renames (v1 -> v2)

| v1 (REMOVED)                        | v2 (CORRECT)           |
|--------------------------------------|------------------------|
| `orm_mode = True`                    | `from_attributes=True` |
| `allow_population_by_field_name`     | `populate_by_name`     |
| `validate_all`                       | `validate_default`     |
| `allow_mutation = False`             | `frozen=True`          |
| `schema_extra`                       | `json_schema_extra`    |
| `anystr_strip_whitespace`            | `str_strip_whitespace` |
| `anystr_lower` / `anystr_upper`      | `str_to_lower` / `str_to_upper` |
| `max_anystr_length` / `min_anystr_length` | `str_max_length` / `str_min_length` |

## Field() Parameter Renames

| v1 (REMOVED)        | v2 (CORRECT)                       |
|----------------------|------------------------------------|
| `regex=...`          | `pattern=...`                      |
| `min_items=...`      | `min_length=...`                   |
| `max_items=...`      | `max_length=...`                   |
| `const=True`         | Use `Literal[value]` type          |
| `unique_items=True`  | Use `set[T]` or `frozenset[T]`     |
| `allow_mutation=False`| `frozen=True`                     |

---

## Quick Reference: Common Patterns

### Model with Config

```python
from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
    model_config = ConfigDict(
        strict=True,
        frozen=True,
        extra='forbid',
        from_attributes=True,
    )

    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    email: str | None = None
```

### Validators (Decorator vs Annotated)

```python
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, AfterValidator, BeforeValidator

# Annotated style — preferred for reusable types
def ensure_positive(v: int) -> int:
    if v <= 0:
        raise ValueError('must be positive')
    return v

PositiveInt = Annotated[int, AfterValidator(ensure_positive)]

class Order(BaseModel):
    quantity: PositiveInt
    name: str

    # Decorator style — for model-specific logic
    @field_validator('name')
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()
```

### Serialization

```python
from pydantic import BaseModel, field_serializer, computed_field

class User(BaseModel):
    first: str
    last: str
    joined: datetime

    @computed_field
    @property
    def full_name(self) -> str:  # return type REQUIRED
        return f'{self.first} {self.last}'

    @field_serializer('joined')
    def ser_joined(self, v: datetime, _info) -> str:
        return v.isoformat()

# Dump options
u.model_dump(exclude_none=True, by_alias=True, mode='json')
u.model_dump_json(indent=2)
```

### Aliases (Three Types)

```python
from pydantic import BaseModel, Field, AliasPath, AliasChoices, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(alias='userName')                    # both input & output
    email: str = Field(validation_alias='email_address')   # input only
    age: int = Field(serialization_alias='user_age')       # output only

    # Nested access
    city: str = Field(validation_alias=AliasPath('address', 'city'))

    # Multiple options
    phone: str = Field(validation_alias=AliasChoices('phone', 'tel', 'mobile'))
```

### TypeAdapter (Validate Without a Model)

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
result = adapter.validate_python(['1', '2', '3'])  # [1, 2, 3]
json_bytes = adapter.dump_json(result)
schema = adapter.json_schema()
```

### Discriminated Unions

```python
from typing import Literal, Annotated, Union
from pydantic import BaseModel, Field, Discriminator, Tag

class Cat(BaseModel):
    pet_type: Literal['cat']
    meows: int

class Dog(BaseModel):
    pet_type: Literal['dog']
    barks: float

class Home(BaseModel):
    pet: Cat | Dog = Field(discriminator='pet_type')
```

---

## More Common Patterns

### Forward References & model_rebuild()

- Self-referencing models need `model_rebuild()` after definition
- `from __future__ import annotations` works but requires `model_rebuild()`

```python
from __future__ import annotations
from pydantic import BaseModel

class Node(BaseModel):
    value: int
    children: list[Node] = []

Node.model_rebuild()  # Required when using forward references

node = Node(value=1, children=[Node(value=2)])
```

### model_construct() — Skip Validation

- For creating instances from trusted data without validation overhead

```python
user = User.model_construct(name='John', age=30)
# No validation runs — use only with trusted data
# _fields_set parameter tracks which fields were explicitly provided
user = User.model_construct(_fields_set={'name'}, name='John', age=30)
```

### Extra Fields Handling

- Three modes: `'ignore'` (default), `'forbid'`, `'allow'`

```python
from pydantic import BaseModel, ConfigDict

class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')  # Raises on unknown fields
    name: str

class Flexible(BaseModel):
    model_config = ConfigDict(extra='allow')  # Stores unknown fields
    name: str

f = Flexible(name='John', role='admin')
f.model_extra  # {'role': 'admin'}  — access via model_extra
f.model_dump()  # {'name': 'John', 'role': 'admin'}
```

---

## Key Imports Cheat Sheet

```python
# Core
from pydantic import BaseModel, Field, ConfigDict, RootModel, PrivateAttr

# Validators
from pydantic import field_validator, model_validator, validate_call
from pydantic import AfterValidator, BeforeValidator, PlainValidator, WrapValidator
from pydantic import ValidationError, ValidationInfo

# Serialization
from pydantic import field_serializer, model_serializer, computed_field
from pydantic import PlainSerializer, WrapSerializer

# Aliases
from pydantic import AliasPath, AliasChoices, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake, to_pascal

# Types & Constraints
from pydantic import TypeAdapter, create_model
from pydantic.types import StringConstraints, Strict
from pydantic import Discriminator, Tag

# Errors
from pydantic_core import PydanticCustomError

# Self type for model_validator(mode='after')
from typing import Self
```

---

## Gotchas — Top LLM Mistakes

The most common errors Claude and other LLMs make with Pydantic. Full 28-item catalogue in `references/v1-to-v2-migration.md § 9`.

1. **`@validator` → `@field_validator`** — and you MUST add `@classmethod` (v2 does not infer it)
2. **`class Config:` → `model_config = ConfigDict(...)`** — inner Config class is deprecated
3. **`.dict()` / `.json()` → `.model_dump()` / `.model_dump_json()`** — all old method names removed
4. **`@root_validator` → `@model_validator`** — `mode='after'` is an instance method (`self`), NOT a classmethod; `mode='before'` IS a classmethod
5. **Forgetting `return v` in validators** — silently sets the field to `None`
6. **`Optional[X]` no longer implies `default=None`** — `str | None` is REQUIRED; you must write `str | None = None` for a default
7. **`pre=True` → `mode='before'`**, **`values` → `info: ValidationInfo` + `info.data`**
8. **`orm_mode=True` → `from_attributes=True`**, **`schema_extra` → `json_schema_extra`**
9. **`GenericModel` removed** — use `BaseModel, Generic[T]` directly
10. **`BaseSettings` moved** — `from pydantic_settings import BaseSettings` (separate package)

---

## Reference Files

Read these on-demand for deeper details:

- **`references/v1-to-v2-migration.md`** — **Start here when debugging wrong Pydantic output.** Exhaustive v1→v2 migration guide: every renamed method, removed feature, behavioral change, and the full 28-item LLM mistakes catalogue (§ 9)
- **`references/validators-serializers.md`** — Complete validator and serializer reference: all 4 modes, Annotated vs decorator patterns, model validators, computed fields, @validate_call
- **`references/advanced-features.md`** — TypeAdapter, custom types, generic models, dynamic models, BaseSettings, discriminated unions, aliases, JSON Schema customization, dataclasses
