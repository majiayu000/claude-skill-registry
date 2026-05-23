---
name: python-data-classes
description: Use when Python data modeling with dataclasses, attrs, and Pydantic. Use when creating data structures and models.
allowed-tools:
  - Bash
  - Read
---

# Python Data Classes

Master Python data modeling using dataclasses, attrs, and Pydantic for
creating clean, type-safe data structures with validation and serialization.

## dataclasses Module

**Basic dataclass usage:**

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    is_active: bool = True  # Default value

# Create instance
user = User(
    id=1,
    name="Alice",
    email="alice@example.com"
)

print(user)
# User(id=1, name='Alice', email='alice@example.com', is_active=True)

print(user.name)  # Alice
```

**dataclass with methods:**

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def move(self, dx: float, dy: float) -> "Point":
        return Point(self.x + dx, self.y + dy)

point = Point(3.0, 4.0)
print(point.distance_from_origin())  # 5.0
new_point = point.move(1.0, 1.0)
print(new_point)  # Point(x=4.0, y=5.0)
```

## dataclass Parameters

**Controlling dataclass behavior:**

```python
from dataclasses import dataclass, field

# frozen=True makes it immutable
@dataclass(frozen=True)
class ImmutableUser:
    id: int
    name: str

# order=True enables comparison operators
@dataclass(order=True)
class Person:
    age: int
    name: str

p1 = Person(30, "Alice")
p2 = Person(25, "Bob")
print(p1 > p2)  # True (compares by age first)

# slots=True uses __slots__ for memory efficiency
@dataclass(slots=True)
class Coordinate:
    x: float
    y: float

# kw_only=True requires keyword arguments
@dataclass(kw_only=True)
class Config:
    host: str
    port: int

config = Config(host="localhost", port=8080)
```

## Field Configuration

**Using field() for advanced configuration:**

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    name: str
    price: float

    # Exclude from __init__
    id: int = field(init=False)

    # Exclude from __repr__
    secret: str = field(repr=False, default="")

    # Default factory for mutable defaults
    tags: List[str] = field(default_factory=list)

    # Exclude from comparison
    created_at: float = field(compare=False, default=0.0)

    def __post_init__(self) -> None:
        # Set id after initialization
        self.id = hash(self.name)

product = Product(name="Widget", price=9.99)
print(product.id)  # Auto-generated hash
```

**Computed fields:**

```python
from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self) -> None:
        self.area = self.width * self.height

rect = Rectangle(10, 20)
print(rect.area)  # 200.0
```

## Inheritance

**Dataclass inheritance:**

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str
    is_good_boy: bool = True

dog = Dog(name="Rex", age=5, breed="Labrador")
print(dog)
# Dog(name='Rex', age=5, breed='Labrador', is_good_boy=True)
```

## Conversion Methods

**Converting to/from dictionaries:**

```python
from dataclasses import dataclass, asdict, astuple

@dataclass
class User:
    id: int
    name: str
    email: str

user = User(1, "Alice", "alice@example.com")

# Convert to dict
user_dict = asdict(user)
print(user_dict)
# {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'}

# Convert to tuple
user_tuple = astuple(user)
print(user_tuple)
# (1, 'Alice', 'alice@example.com')

# Create from dict
data = {"id": 2, "name": "Bob", "email": "bob@example.com"}
bob = User(**data)
```

## attrs Library

**Using attrs for enhanced features:**

```bash
pip install attrs
```

**Basic attrs usage:**

```python
import attrs

@attrs.define
class User:
    id: int
    name: str
    email: str
    is_active: bool = True

user = User(1, "Alice", "alice@example.com")
print(user)
```

**attrs validators:**

```python
import attrs
from attrs import validators

@attrs.define
class User:
    id: int = attrs.field(validator=validators.instance_of(int))
    name: str = attrs.field(
        validator=[
            validators.instance_of(str),
            validators.min_len(1)
        ]
    )
    email: str = attrs.field(
        validator=validators.matches_re(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    )
    age: int = attrs.field(
        validator=validators.and_(
            validators.instance_of(int),
            validators.ge(0),
            validators.le(150)
        )
    )

# Validates on initialization
user = User(
    id=1,
    name="Alice",
    email="alice@example.com",
    age=30
)
```

**attrs converters:**

```python
import attrs

@attrs.define
class User:
    name: str = attrs.field(converter=str.strip)
    age: int = attrs.field(converter=int)
    tags: list[str] = attrs.field(
        factory=list,
        converter=lambda x: [tag.lower() for tag in x]
    )

user = User(
    name="  Alice  ",
    age="30",
    tags=["ADMIN", "User"]
)

print(user.name)  # "Alice"
print(user.age)   # 30 (int)
print(user.tags)  # ["admin", "user"]
```

## Pydantic Models

**Install Pydantic:**

```bash
pip install pydantic
```

**Basic Pydantic model:**

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True

# Automatic validation and conversion
user = User(
    id="1",           # Converted to int
    name="Alice",
    email="alice@example.com"
)

print(user.id)  # 1 (int)
print(user.model_dump())  # Dict representation
print(user.model_dump_json())  # JSON string
```

**Pydantic validators:**

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Annotated

class User(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: Annotated[int, Field(ge=0, le=150)]
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip().title()

user = User(
    id=1,
    name="  alice  ",
    email="alice@example.com",
    age=30,
    username="ALICE123"
)

print(user.name)      # "Alice"
print(user.username)  # "alice123"
```

**Pydantic model configuration:**

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=False,
        extra="forbid"
    )

    id: int
    name: str
    email: str

# Strips whitespace automatically
user = User(id=1, name="  Alice  ", email="alice@example.com")
print(user.name)  # "Alice"

# Validates on assignment
user.name = "  Bob  "
print(user.name)  # "Bob"
```

## Pydantic Advanced Features

**Computed fields:**

```python
from pydantic import BaseModel, computed_field

class User(BaseModel):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

user = User(first_name="Alice", last_name="Smith")
print(user.full_name)  # "Alice Smith"
print(user.model_dump())
# {'first_name': 'Alice', 'last_name': 'Smith', 'full_name': 'Alice Smith'}
```

**Model validators:**

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode="after")
    def validate_date_range(self) -> "DateRange":
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")
        return self

range_obj = DateRange(
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

**Nested models:**

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    email: str
    address: Address

user = User(
    name="Alice",
    email="alice@example.com",
    address={
        "street": "123 Main St",
        "city": "New York",
        "country": "USA"
    }
)

print(user.address.city)  # "New York"
```

**Generic models:**

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    data: T
    message: str
    success: bool

class User(BaseModel):
    id: int
    name: str

# Create typed response
response = Response[User](
    data=User(id=1, name="Alice"),
    message="User retrieved",
    success=True
)

print(response.data.name)  # "Alice"
```

## Serialization and Deserialization

**Pydantic JSON handling:**

```python
from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime
    metadata: dict[str, str]

# From JSON
json_data = '''
{
    "name": "User Login",
    "timestamp": "2024-01-15T10:30:00",
    "metadata": {"ip": "192.168.1.1"}
}
'''

event = Event.model_validate_json(json_data)
print(event.timestamp)

# To JSON
json_output = event.model_dump_json(indent=2)
print(json_output)
```

**Custom serialization:**

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

event = Event(name="Test", timestamp=datetime.now())
print(event.model_dump())
# {'name': 'Test', 'timestamp': '2024-01-15 10:30:00'}
```

## Comparison: dataclasses vs attrs vs Pydantic

**When to use dataclasses:**

- Simple data containers with type hints
- Part of standard library (no dependencies)
- Basic validation not required
- Python 3.7+ compatibility needed
- Immutability with frozen=True

**When to use attrs:**

- More features than dataclasses (validators, converters)
- Better performance than dataclasses
- Advanced field configuration needed
- Backward compatibility (Python 2.7+)
- Custom initialization logic

**When to use Pydantic:**

- Automatic data validation required
- JSON/dict serialization/deserialization
- API request/response models
- Configuration management
- Type coercion needed
- OpenAPI/JSON schema generation

## Best Practices

- Use type hints for all fields
- Provide default values for optional fields
- Use default_factory for mutable defaults
- Validate data at boundaries (API, database)
- Keep dataclasses focused and cohesive
- Use frozen=True for immutable data
- Leverage validators for business rules
- Use computed fields for derived data
- Document complex field requirements
- Choose the right tool for your use case

## Common Patterns

**Builder pattern with dataclass:**

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class QueryBuilder:
    _select: list[str] = field(default_factory=list)
    _where: list[str] = field(default_factory=list)
    _limit: Optional[int] = None

    def select(self, *columns: str) -> "QueryBuilder":
        self._select.extend(columns)
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._where.append(condition)
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def build(self) -> str:
        query = f"SELECT {', '.join(self._select)}"
        if self._where:
            query += f" WHERE {' AND '.join(self._where)}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

query = (
    QueryBuilder()
    .select("id", "name")
    .where("active = true")
    .limit(10)
    .build()
)
```

**Configuration with Pydantic:**

```python
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My App"
    database_url: str = Field(..., env="DATABASE_URL")
    debug: bool = False
    max_connections: int = Field(10, ge=1, le=100)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

## When to Use This Skill

Use python-data-classes when you need to:

- Create data transfer objects (DTOs)
- Model API request/response payloads
- Define configuration structures
- Implement value objects in domain models
- Build type-safe data containers
- Handle JSON serialization/deserialization
- Validate user input or external data
- Create immutable data structures
- Implement builder or factory patterns
- Model database schemas or ORM entities

## Common Pitfalls

- Using mutable defaults (list, dict) without default_factory
- Not validating data from external sources
- Over-complicating simple data structures
- Mixing business logic with data models
- Not using frozen for immutable data
- Forgetting to handle None values properly
- Not leveraging type hints effectively
- Using wrong tool (dataclass vs attrs vs Pydantic)
- Not documenting field constraints
- Ignoring validation performance in hot paths

## Resources

- [dataclasses Documentation](https://docs.python.org/3/library/dataclasses.html)
- [attrs Documentation](https://www.attrs.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
