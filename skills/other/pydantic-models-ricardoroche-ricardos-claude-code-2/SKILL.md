---
name: pydantic-models
description: Automatically applies when creating data models for API responses and validation. Uses Pydantic BaseModel with validators, field definitions, and proper serialization.
---

# Pydantic Model Pattern Enforcer

When creating data models for API responses, validation, or configuration, follow Pydantic best practices.

## ✅ Correct Pattern

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    """User model with validation."""

    id: str = Field(..., description="User unique identifier")
    email: str = Field(..., description="User email address")
    name: str = Field(..., min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    created_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and clean name."""
        return v.strip()

    @model_validator(mode='after')
    def validate_model(self) -> 'User':
        """Cross-field validation."""
        if self.age and self.age < 13:
            if '@' in self.email and not self.email.endswith('@parent.com'):
                raise ValueError('Users under 13 must use parent email')
        return self

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "usr_123",
                "email": "user@example.com",
                "name": "John Doe",
                "age": 30,
                "tags": ["premium", "verified"]
            }
        }
```

## Field Definitions

```python
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Annotated
from decimal import Decimal

class Product(BaseModel):
    """Product with comprehensive field validation."""

    # Required field
    name: str = Field(..., min_length=1, max_length=200)

    # Optional with default
    description: str = Field("", max_length=1000)

    # Numeric constraints
    price: Decimal = Field(..., ge=0, decimal_places=2)
    quantity: int = Field(0, ge=0)

    # String patterns
    sku: str = Field(..., pattern=r'^[A-Z0-9-]+$')

    # URL validation
    image_url: Optional[HttpUrl] = None

    # Email validation (requires email-validator package)
    contact_email: Optional[EmailStr] = None

    # Annotated types
    weight: Annotated[float, Field(gt=0, description="Weight in kg")]

    # Enum field
    status: Literal["active", "inactive", "discontinued"] = "active"
```

## Field Validators

```python
from pydantic import BaseModel, field_validator
import re

class PhoneContact(BaseModel):
    phone: str
    country_code: str = "US"

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """Validate and normalize phone number."""
        # Remove non-digits
        digits = re.sub(r'\D', '', v)

        if len(digits) != 10:
            raise ValueError('Phone must be 10 digits')

        return digits

    @field_validator('country_code')
    @classmethod
    def validate_country(cls, v: str) -> str:
        """Validate country code."""
        allowed = ['US', 'CA', 'UK']
        if v not in allowed:
            raise ValueError(f'Country must be one of {allowed}')
        return v
```

## Model Validators

```python
from pydantic import BaseModel, model_validator
from datetime import datetime

class Booking(BaseModel):
    start_date: datetime
    end_date: datetime
    guests: int

    @model_validator(mode='after')
    def validate_dates(self) -> 'Booking':
        """Validate date range."""
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')

        duration = (self.end_date - self.start_date).days
        if duration > 30:
            raise ValueError('Booking cannot exceed 30 days')

        return self

    @model_validator(mode='after')
    def validate_capacity(self) -> 'Booking':
        """Validate guest count."""
        if self.guests < 1:
            raise ValueError('At least 1 guest required')
        if self.guests > 10:
            raise ValueError('Maximum 10 guests allowed')
        return self
```

## Nested Models

```python
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    """Address component."""
    street: str
    city: str
    state: str
    zip_code: str

class Customer(BaseModel):
    """Customer with nested address."""
    name: str
    email: str
    billing_address: Address
    shipping_address: Optional[Address] = None
    orders: List['Order'] = []

class Order(BaseModel):
    """Order model."""
    id: str
    total: Decimal
    items: List['OrderItem']

class OrderItem(BaseModel):
    """Order item."""
    product_id: str
    quantity: int
    price: Decimal

# Update forward references
Customer.model_rebuild()
```

## Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class StrictModel(BaseModel):
    """Model with strict validation."""

    model_config = ConfigDict(
        # Validation settings
        str_strip_whitespace=True,      # Strip whitespace from strings
        validate_assignment=True,        # Validate on field assignment
        validate_default=True,           # Validate default values
        strict=True,                     # Strict type checking

        # Serialization settings
        use_enum_values=True,            # Serialize enums as values
        populate_by_name=True,           # Allow field population by alias

        # Extra fields
        extra='forbid',                  # Forbid extra fields (default: 'ignore')

        # JSON schema
        json_schema_extra={
            "example": {...}
        }
    )
```

## Computed Fields

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        """Computed area."""
        return self.width * self.height

    @computed_field
    @property
    def perimeter(self) -> float:
        """Computed perimeter."""
        return 2 * (self.width + self.height)

# Usage
rect = Rectangle(width=10, height=5)
print(rect.area)       # 50.0
print(rect.perimeter)  # 30.0
print(rect.model_dump())  # Includes computed fields
```

## JSON Schema

```python
from pydantic import BaseModel

class APIResponse(BaseModel):
    """API response model."""
    data: dict
    message: str
    status: int = 200

# Generate JSON schema
schema = APIResponse.model_json_schema()

# Use in FastAPI (automatic)
@app.post("/api/endpoint")
async def endpoint(data: APIResponse) -> APIResponse:
    return data

# Custom schema
class CustomModel(BaseModel):
    name: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Example 1"},
                {"name": "Example 2"}
            ]
        }
    }
```

## Serialization

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime
    metadata: dict

    @field_serializer('timestamp')
    def serialize_timestamp(self, value: datetime) -> str:
        """Serialize timestamp as ISO string."""
        return value.isoformat()

    def model_dump_json(self, **kwargs) -> str:
        """Serialize to JSON string."""
        return super().model_dump_json(**kwargs)

# Usage
event = Event(name="test", timestamp=datetime.now(), metadata={})
json_str = event.model_dump_json()  # JSON string
dict_data = event.model_dump()       # Python dict
```

## ❌ Anti-Patterns

```python
# ❌ Using dict instead of model
def process_user(user: dict):  # No validation!
    pass

# ✅ Better: use Pydantic model
def process_user(user: User):  # Validated!
    pass

# ❌ Manual validation
def validate_email(email: str):
    if '@' not in email:
        raise ValueError("Invalid email")

# ✅ Better: use Pydantic validator
class User(BaseModel):
    email: EmailStr  # Built-in validation

# ❌ Mutable defaults
class Config(BaseModel):
    tags: List[str] = []  # ❌ Shared across instances!

# ✅ Better: use Field with default_factory
class Config(BaseModel):
    tags: List[str] = Field(default_factory=list)

# ❌ Not using Optional
class User(BaseModel):
    middle_name: str  # Required, but should be optional!

# ✅ Better
class User(BaseModel):
    middle_name: Optional[str] = None
```

## Best Practices Checklist

- ✅ Use `BaseModel` for all data models
- ✅ Add field descriptions with `Field(..., description="...")`
- ✅ Use appropriate validators for business logic
- ✅ Use `Optional` for nullable fields
- ✅ Use `Field(default_factory=list)` for mutable defaults
- ✅ Add JSON schema examples
- ✅ Use computed fields for derived data
- ✅ Configure strict validation when needed
- ✅ Document models with docstrings
- ✅ Use nested models for complex structures

## Auto-Apply

When creating models:
1. Use `BaseModel` as base class
2. Add type hints for all fields
3. Use `Field()` for constraints and descriptions
4. Add validators for business logic
5. Add JSON schema examples
6. Use nested models for complex data

## Related Skills

- structured-errors - For error response models
- docstring-format - For model documentation
- pytest-patterns - For testing models
