---
name: pydantic
description: Data validation library using Python type hints to validate, serialize, and document data structures
version: 2.12.5
ecosystem: python
license: MIT
generated_with: claude-sonnet-4-5-20250929
---

## Imports

```python
from pydantic import BaseModel, Field, ValidationError
from pydantic import field_validator, model_validator
from pydantic import computed_field, field_serializer, model_serializer
from pydantic import ConfigDict, RootModel, TypeAdapter
from pydantic import BeforeValidator, AfterValidator, PlainValidator, WrapValidator
from pydantic import AliasPath, AliasChoices
```

## Core Patterns

### Basic Model Definition ✅ Current
```python
from pydantic import BaseModel, Field, ValidationError

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: str
    age: int | None = Field(default=None, ge=0, le=120)

# Valid case: all fields, age in bounds
u = User(id=1, name="Alice", email="alice@example.com", age=30)
assert u.id == 1
assert 1 <= len(u.name) <= 100
assert u.email.count("@") == 1
assert u.age == 30

# Valid case: age omitted (should default to None)
u2 = User(id=2, name="Bob", email="bob@example.com")
assert u2.age is None

# Invalid: name too short
try:
    User(id=3, name="", email="c@example.com")
except ValidationError as e:
    # Pydantic 2 error messages include error type, check for that
    assert "string_too_short" in str(e)

# Invalid: name too long
try:
    User(id=4, name="x"*101, email="d@example.com")
except ValidationError as e:
    assert "string_too_long" in str(e)

# Invalid: age too low
try:
    User(id=5, name="Ed", email="e@example.com", age=-1)
except ValidationError as e:
    assert "greater_than_or_equal" in str(e) or "ge" in str(e) or "Value error, got -1" in str(e)

# Invalid: age too high
try:
    User(id=6, name="Fay", email="f@example.com", age=121)
except ValidationError as e:
    assert "less_than_or_equal" in str(e) or "le" in str(e) or "Value error, got 121" in str(e)
```
* Define models by subclassing `BaseModel` with type-annotated fields
* Use `Field()` to add constraints, defaults, descriptions, and metadata
* Fields without defaults must appear before fields with defaults

### Model Validation and Serialization ✅ Current
```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str

# Validate input data
try:
    user = User.model_validate({'id': '123', 'name': 'John'})
    # Coerces '123' to int(123)
except ValidationError as e:
    print(e.errors())

# Serialize to dict or JSON
user_dict = user.model_dump()  # {'id': 123, 'name': 'John'}
user_json = user.model_dump_json()  # '{"id":123,"name":"John"}'
```
* Use `model_validate()` for validation from dicts or objects
* Use `model_dump()` for dict serialization, `model_dump_json()` for JSON
* `ValidationError` provides detailed error information with `errors()` method

### Field Validators ✅ Current
```python
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    name: str
    price: float
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('price must be positive')
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        return v.strip().title()
```
* Use `@field_validator` decorator to define custom field validation
* Validators must be class methods in V2 (use `@classmethod`)
* Mode can be `'before'`, `'after'` (default), `'wrap'`, or `'plain'`
* Validators can transform values by returning modified value

### Computed Fields ✅ Current
```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: int
    length: int
    
    @computed_field
    @property
    def area(self) -> int:
        return self.width * self.length
    
    @area.setter
    def area(self, new_area: int):
        self.width = int(new_area ** 0.5)
        self.length = self.width

rect = Rectangle(width=10, length=5)
# Computed fields included in serialization
rect.model_dump()  # {'width': 10, 'length': 5, 'area': 50}
```
* Use `@computed_field` with `@property` to define calculated fields
* Computed fields are automatically included in `model_dump()` output
* Can define setters and deleters for computed fields
* Use `exclude_computed_fields=True` to exclude from serialization

### Custom Serialization ✅ Current
```python
from pydantic import BaseModel, field_serializer, model_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime
    
    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime, _info):
        return dt.isoformat()
    
    @model_serializer(mode='wrap')
    def serialize_model(self, serializer, info):
        data = serializer(self)
        data['_version'] = '1.0'
        return data
```
* Use `@field_serializer` to customize individual field serialization
* Use `@model_serializer` for model-level serialization control
* Mode can be `'plain'` (replace) or `'wrap'` (wrap default serializer)
* Field serializers receive the field value and serialization info

## Configuration

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        # Validate assignments after model creation
        validate_assignment=True,
        
        # Allow arbitrary types (disable strict type checking)
        arbitrary_types_allowed=True,
        
        # Populate from object attributes (was orm_mode in V1)
        from_attributes=True,
        
        # Make model immutable
        frozen=True,
        
        # Field alias generator
        alias_generator=lambda field_name: field_name.upper(),
        
        # Additional fields allowed beyond those defined
        extra='allow',  # 'forbid' or 'ignore'
        
        # Strict mode (no coercion)
        strict=False,
        
        # Use enum values instead of enum instances
        use_enum_values=True,
    )
    
    name: str
    age: int
```

**Common ConfigDict options:**
* `validate_assignment=True` - Validate when setting attributes after creation
* `from_attributes=True` - Enable validation from object attributes (replaces `orm_mode`)
* `frozen=True` - Make instances immutable
* `extra='forbid'` - Raise error on extra fields (default is `'ignore'`)
* `strict=True` - Disable type coercion

## Pitfalls

### Wrong: Comparing models to dicts
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

user = User(id=1, name='John')
# This is False in V2!
user == {'id': 1, 'name': 'John'}
```

### Right: Compare models to models
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

user1 = User(id=1, name='John')
user2 = User(id=1, name='John')
# Models only equal to other instances of same type
user1 == user2  # True
# Or compare to dict explicitly
user1.model_dump() == {'id': 1, 'name': 'John'}  # True
```

### Wrong: Using Field constraints on generic parameters
```python
from pydantic import BaseModel, Field

class Items(BaseModel):
    # This applies to the list, not the strings!
    tags: list[str] = Field(min_length=3)
```

### Right: Use Annotated for constraints on generic items
```python
from pydantic import BaseModel, Field
from typing import Annotated

class Items(BaseModel):
    # Constraint applies to each string in the list
    tags: list[Annotated[str, Field(min_length=3)]]
```

### Wrong: Using deprecated json_encoders ⚠️
```python
from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    model_config = {
        # Deprecated and removed!
        'json_encoders': {
            datetime: lambda v: v.isoformat()
        }
    }
    timestamp: datetime
```

### Right: Use field_serializer decorator
```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    timestamp: datetime
    
    @field_serializer('timestamp')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()
```

### Wrong: Passing mutable defaults directly
```python
from pydantic import BaseModel

class User(BaseModel):
    # Dangerous! Shares same list across instances
    tags: list[str] = []
```

### Right: Use default_factory for mutable defaults
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    tags: list[str] = Field(default_factory=list)
```

### Wrong: Using class methods for 'after' model validators ⚠️
```python
from pydantic import BaseModel, model_validator

class User(BaseModel):
    password: str
    password_confirm: str
    
    # Deprecated as classmethod for mode='after'
    @model_validator(mode='after')
    @classmethod
    def check_passwords(cls, values):
        if values.password != values.password_confirm:
            raise ValueError('passwords do not match')
        return values
```

### Right: Use instance methods for 'after' model validators
```python
from pydantic import BaseModel, model_validator

class User(BaseModel):
    password: str
    password_confirm: str
    
    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.password_confirm:
            raise ValueError('passwords do not match')
        return self
```

## Migration

### Breaking and Deprecating Changes

**Method and API deprecations:**  
Pydantic v2.12.x continues to deprecate classmethod-based 'after' model validators:  
- Using a `@classmethod` for an `'after'` model validator now emits a warning (since 2.12.0).  
  Update usage to use instance methods for `'after'` model validation.  
- The `json_encoders` config option is removed/deprecated.  
  Use `@field_serializer` and `@model_serializer` for custom serialization.

**Recent breaking changes (summarized):**
- `after` model validators as classmethods now emit a warning, not an error.  
- `build()` method of `AnyUrl` and `Dsn` reverted percent-encoding of credentials in 2.12.4 (no action needed unless you relied on this).

**Migration tips:**  
- If your code uses classmethod-based `@model_validator(mode='after')`, convert these to instance methods.
- Refactor custom serialization logic to use the new `@field_serializer` or `@model_serializer` decorators.
- If you migrated from v1, see the full migration table and notes below.

## References

- [Homepage](https://github.com/pydantic/pydantic)
- [Documentation](https://docs.pydantic.dev)
- [Funding](https://github.com/sponsors/samuelcolvin)
- [Source](https://github.com/pydantic/pydantic)
- [Changelog](https://docs.pydantic.dev/latest/changelog/)

## Migration from v1

### Breaking Changes

**Method renames:**
```python
# V1 → V2
__fields__ → model_fields
construct() → model_construct()
copy() → model_copy()
dict() → model_dump()
json() → model_dump_json()
parse_obj() → model_validate()
parse_raw() → model_validate_json()  # for JSON strings
schema() → model_json_schema()
update_forward_refs() → model_rebuild()
from_orm() → model_validate() + from_attributes=True
```

**Custom root types:**
```python
# V1
class MyList(BaseModel):
    __root__: list[int]

# V2
from pydantic import RootModel

class MyList(RootModel[list[int]]):
    pass
```

**Generic models:**
```python
# V1
from pydantic.generics import GenericModel
from typing import Generic, TypeVar

T = TypeVar('T')

class Response(GenericModel, Generic[T]):
    data: T

# V2
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
```

**Field parameter changes:**
```python
# V1 → V2
allow_mutation=False → frozen=True
regex='...' → pattern='...'
min_items/max_items → min_length/max_length
final=True → use typing.Final type hint
const=True → use typing.Literal type hint
```

**Config changes:**
```python
# V1
class User(BaseModel):
    class Config:
        orm_mode = True
        allow_mutation = False

# V2
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True
    )
```

**Migration tool:**
```bash
pip install bump-pydantic
bump-pydantic my_package
```

## API Reference

- **BaseModel** - Base class for all Pydantic models; subclass to define validated data structures
- **Field(default, ...)** - Define field metadata including constraints, aliases, descriptions, and examples
- **model_validate(obj)** - Validate and parse input data from dict or object; raises ValidationError
- **model_dump(...)** - Serialize model to dict with options for include/exclude, aliases, and serialization modes
- **model_dump_json(...)** - Serialize model directly to JSON string
- **model_json_schema(...)** - Generate JSON Schema for the model
- **field_validator(*fields, mode='after')** - Decorator for field-level validation; modes: 'before', 'after', 'wrap', 'plain'
- **model_validator(mode)** - Decorator for model-level validation; modes: 'before', 'after', 'wrap'
- **computed_field** - Decorator to mark property as computed field included in serialization
- **field_serializer(*fields, mode='plain')** - Decorator for custom field serialization
- **model_serializer(mode)** - Decorator for custom model-level serialization
- **ValidationError** - Exception raised on validation failure; use `.errors()` for detailed error list
- **ConfigDict** - TypedDict for model configuration options
- **RootModel[T]** - Model with single root field for validating simple types like lists or primitives
- **TypeAdapter(type)** - Validate and serialize arbitrary types without creating a model class
- **PrivateAttr(default)** - Define private attributes excluded from validation and serialization
- **BeforeValidator(func)** - Validator annotation that runs before core validation
- **AfterValidator(func)** - Validator annotation that runs after core validation
