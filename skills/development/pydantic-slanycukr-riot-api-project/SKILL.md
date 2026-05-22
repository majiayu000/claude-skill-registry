---
name: pydantic
description: Data validation and settings management using Python type annotations with Pydantic v2
when_to_use: When you need to validate data structures, create settings models, serialize/deserialize data, or ensure type safety in Python applications
---

# Pydantic v2 Framework Skill

Pydantic is a data validation library that uses Python type annotations to define data schemas, offering fast and extensible validation with automatic type coercion.

## Quick Start

### Basic Model Definition

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    email: str
    signup_ts: Optional[datetime] = None
    is_active: bool = True

# Automatic type coercion
user = User(
    id='123',  # String → int
    name='John Doe',
    email='john@example.com',
    signup_ts='2017-06-01 12:22'  # String → datetime
)
```

### Validation from Data Sources

```python
# From dict
user = User.model_validate({'id': 1, 'name': 'Alice', 'email': 'alice@test.com'})

# From JSON
user = User.model_validate_json('{"id": 1, "name": "Alice", "email": "alice@test.com"}')

# Serialization
print(user.model_dump())  # Python dict
print(user.model_dump_json())  # JSON string
```

## Common Patterns

### Field Configuration

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Annotated

class Product(BaseModel):
    product_id: int = Field(alias='id', ge=1, description='Unique product identifier')
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0, le=1000000)
    email: EmailStr
    website: HttpUrl
    tags: list[str] = Field(default_factory=list, max_length=10)
    internal_code: str = Field(exclude=True, default='N/A')

class User(BaseModel):
    username: Annotated[str, Field(min_length=3, pattern=r'^[a-zA-Z0-9_]+$')]
    age: int = Field(ge=0, le=150)
```

### Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    model_config = ConfigDict(
        strict=True,              # No type coercion
        frozen=True,              # Immutable instances
        validate_assignment=True, # Validate on attribute assignment
        extra='forbid',           # Reject extra fields
        str_strip_whitespace=True,
        populate_by_name=True,    # Accept both alias and field name
        use_enum_values=True,     # Serialize enums as values
    )

    id: int
    name: str
```

### Custom Validation

```python
from pydantic import BaseModel, model_validator, field_validator, ValidationError
from typing import Any

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @field_validator('start_date', 'end_date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        # Custom validation logic
        if not v:
            raise ValueError('Date cannot be empty')
        return v

    @model_validator(mode='after')
    def check_dates_order(self) -> 'DateRange':
        # Cross-field validation
        if self.start_date > self.end_date:
            raise ValueError('start_date must be before end_date')
        return self

# Using the model
try:
    date_range = DateRange(start_date='2024-01-01', end_date='2024-01-31')
except ValidationError as e:
    for error in e.errors():
        print(f"{error['loc']}: {error['msg']}")
```

### Serialization Control

```python
from pydantic import BaseModel, Field, SecretStr
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    password: SecretStr
    created_at: datetime
    internal_data: dict = Field(exclude=True, default_factory=dict)

# Serialization options
user = User(
    id=1,
    username='john',
    password='secret',
    created_at=datetime.now()
)

# Basic serialization
print(user.model_dump())  # Python dict
print(user.model_dump_json())  # JSON string

# Excluding fields
print(user.model_dump(exclude={'password'}))
print(user.model_dump(exclude={'username', 'created_at'}))

# Include only specific fields
print(user.model_dump(include={'id', 'username'}))

# JSON-compatible serialization
print(user.model_dump(mode='json'))  # datetime → string
print(user.model_dump(by_alias=True))  # Use field aliases
```

### Custom Serialization

```python
from typing import Annotated, Any
from pydantic import BaseModel, field_serializer, PlainSerializer

class Model(BaseModel):
    number: int
    created_at: datetime

    @field_serializer('number')
    def serialize_number(self, value: int) -> str:
        return f"{value:,}"  # Format with commas

    # Using Annotated with PlainSerializer
    custom_field: Annotated[
        float,
        PlainSerializer(lambda x: round(x, 2), return_type=float)
    ]
```

### Nested Models and Relationships

```python
from pydantic import BaseModel
from typing import Optional, List

class Address(BaseModel):
    street: str
    city: str
    country: str = 'USA'
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    addresses: List[Address]
    primary_address: Optional[Address] = None

# Usage
user = User(
    id=1,
    name='John Doe',
    addresses=[
        {'street': '123 Main St', 'city': 'New York', 'zip_code': '10001'},
        {'street': '456 Oak Ave', 'city': 'Boston', 'zip_code': '02101'}
    ],
    primary_address={'street': '123 Main St', 'city': 'New York', 'zip_code': '10001'}
)
```

### Enum Integration

```python
from enum import Enum, IntEnum
from pydantic import BaseModel

class Status(str, Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    COMPLETED = 'completed'

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task(BaseModel):
    title: str
    status: Status = Status.PENDING
    priority: Priority = Priority.MEDIUM

    model_config = ConfigDict(use_enum_values=True)

# Can use enum values or names
task1 = Task(title='Task 1', status='active', priority=3)
task2 = Task(title='Task 2', status=Status.ACTIVE, priority=Priority.HIGH)
```

### TypeAdapter for Standalone Validation

```python
from pydantic import TypeAdapter
from typing import List, Optional

# Validate individual types without full models
int_adapter = TypeAdapter(int)
print(int_adapter.validate_python('123'))  # 123

list_adapter = TypeAdapter(List[int])
print(list_adapter.validate_python(['1', '2', '3']))  # [1, 2, 3]

# Generate JSON schemas
print(int_adapter.json_schema())
print(list_adapter.json_schema())
```

### Data Validation Patterns

```python
from pydantic import BaseModel, ValidationError
from typing import Union

class EmailValidator(BaseModel):
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

# Validation error handling
try:
    user = User(id='invalid', name='', email='test')
except ValidationError as e:
    print(f"Errors: {e.error_count()}")
    for error in e.errors():
        print(f"  {error['loc']}: {error['msg']} ({error['type']})")
```

## Requirements

- Python 3.8+
- Pydantic v2.x: `pip install pydantic`
- Optional dependencies for enhanced types:
  - `pip install pydantic[email]` for EmailStr
  - `pip install pydantic[url]` for HttpUrl
  - `pip install pydantic[typing-extensions]` for extended type support

## Best Practices

1. **Use specific types**: Prefer `conint(gt=0)` over `int` for positive numbers
2. **Configure models**: Use `ConfigDict` to set global model behavior
3. **Handle validation errors**: Always wrap model creation in try/catch blocks
4. **Use field validators**: Implement custom validation logic with `@field_validator`
5. **Control serialization**: Use `model_dump()` parameters to control output format
6. **Leverage type coercion**: Pydantic automatically converts compatible types
7. **Use nested models**: Break complex data into smaller, reusable models
