---
name: pydantic-validation
description: >
  Validate data with Pydantic v2: BaseModel, Field validators, model validators,
  computed fields, discriminated unions, and custom types. Use when the user defines
  API schemas, validates input data, works with Pydantic models, or asks about
  data validation in Python. Trigger when you see dict-based data handling that
  should use Pydantic models.
---

# Pydantic Validation

Define strict, self-documenting data schemas with Pydantic v2. Pydantic validates
data at the boundary between your application and the outside world, catching bad
data before it causes bugs deep in business logic.

## When to Use
- User defines FastAPI request/response models
- User validates configuration, API payloads, or form data
- User asks about data validation or serialization
- User builds complex nested data structures
- User needs discriminated unions or custom type validation

## Core Patterns

### BaseModel and Field Configuration

```python
from pydantic import BaseModel, Field
from datetime import datetime

class CreateUserRequest(BaseModel):
    """Request body for creating a user."""

    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(ge=0, le=150)
    role: str = Field(default="user", description="User role")
    tags: list[str] = Field(default_factory=list, max_length=10)

    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "examples": [
                {"name": "Alice", "email": "alice@example.com", "age": 30}
            ]
        },
    }
```

### Field Validators

Use `@field_validator` for single-field validation and transformation.

```python
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    name: str
    sku: str
    price_cents: int
    category: str

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, v: str) -> str:
        if not v.startswith(("SKU-", "PRD-")):
            raise ValueError("SKU must start with 'SKU-' or 'PRD-'")
        return v.upper()

    @field_validator("price_cents")
    @classmethod
    def validate_price(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        return v.lower().strip().replace(" ", "-")
```

### Model Validators

Use `@model_validator` when validation depends on multiple fields.

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime
    label: str = ""

    @model_validator(mode="after")
    def validate_date_range(self) -> "DateRange":
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        if not self.label:
            # Compute default label from dates
            return DateRange(
                start_date=self.start_date,
                end_date=self.end_date,
                label=f"{self.start_date.date()} to {self.end_date.date()}",
            )
        return self

    @model_validator(mode="before")
    @classmethod
    def preprocess(cls, data: dict) -> dict:
        """Transform raw input before field validation."""
        if isinstance(data, dict) and "dates" in data:
            start, end = data.pop("dates").split("/")
            return {**data, "start_date": start, "end_date": end}
        return data
```

### Computed Fields

```python
from pydantic import BaseModel, computed_field
from decimal import Decimal

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: Decimal

    @computed_field
    @property
    def total_price(self) -> Decimal:
        return self.quantity * self.unit_price

class Order(BaseModel):
    items: list[OrderItem]
    discount_percent: Decimal = Decimal("0")

    @computed_field
    @property
    def subtotal(self) -> Decimal:
        return sum(item.total_price for item in self.items)

    @computed_field
    @property
    def total(self) -> Decimal:
        discount = self.subtotal * self.discount_percent / 100
        return self.subtotal - discount
```

### Discriminated Unions

Use discriminated unions for polymorphic data with a type field.

```python
from pydantic import BaseModel, Field
from typing import Annotated, Literal, Union

class EmailNotification(BaseModel):
    type: Literal["email"] = "email"
    to_address: str
    subject: str
    body: str

class SmsNotification(BaseModel):
    type: Literal["sms"] = "sms"
    phone_number: str
    message: str = Field(max_length=160)

class PushNotification(BaseModel):
    type: Literal["push"] = "push"
    device_token: str
    title: str
    body: str

# Discriminated union -- Pydantic checks "type" field first for fast routing
Notification = Annotated[
    Union[EmailNotification, SmsNotification, PushNotification],
    Field(discriminator="type"),
]

class NotificationBatch(BaseModel):
    notifications: list[Notification]

# Parsing automatically routes to the correct model
batch = NotificationBatch.model_validate({
    "notifications": [
        {"type": "email", "to_address": "a@b.com", "subject": "Hi", "body": "Hello"},
        {"type": "sms", "phone_number": "+1234567890", "message": "Hey"},
    ]
})
```

### Custom Types with Annotated

```python
from typing import Annotated
from pydantic import AfterValidator, BeforeValidator, PlainSerializer

def validate_non_empty(v: str) -> str:
    if not v.strip():
        raise ValueError("String must not be empty or whitespace")
    return v.strip()

def validate_positive(v: int) -> int:
    if v <= 0:
        raise ValueError("Must be positive")
    return v

NonEmptyStr = Annotated[str, AfterValidator(validate_non_empty)]
PositiveInt = Annotated[int, AfterValidator(validate_positive)]

# Custom serialization
from datetime import datetime

UnixTimestamp = Annotated[
    datetime,
    BeforeValidator(lambda v: datetime.fromtimestamp(v) if isinstance(v, (int, float)) else v),
    PlainSerializer(lambda v: int(v.timestamp()), return_type=int),
]

class Event(BaseModel):
    name: NonEmptyStr
    priority: PositiveInt
    created_at: UnixTimestamp
```

### Separating Input and Output Models

```python
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}  # Enable ORM mode
```

## Anti-Patterns

- **Using dicts instead of models**: Raw dicts bypass validation entirely. Define a
  Pydantic model for any external data boundary.
- **Validating inside business logic**: Validate at the boundary (API layer), not deep
  in service functions. By the time data reaches business logic, it should already be
  a validated model.
- **Single model for create/read/update**: Use separate models (`UserCreate`,
  `UserResponse`, `UserUpdate`) to keep concerns clean.
- **Overusing `model_validator(mode="before")`**: Prefer field validators when possible.
  `mode="before"` receives raw unvalidated data and is harder to type correctly.
- **Mutable model instances**: Use `model_copy(update={...})` to create modified copies
  instead of mutating fields directly.

## Quick Reference

| Feature | Syntax |
|---|---|
| Field constraints | `Field(ge=0, max_length=100)` |
| Field validator | `@field_validator("field_name")` |
| Model validator | `@model_validator(mode="after")` |
| Computed field | `@computed_field` + `@property` |
| Discriminated union | `Field(discriminator="type")` |
| Custom type | `Annotated[str, AfterValidator(fn)]` |
| ORM mode | `model_config = {"from_attributes": True}` |
| Immutable copy | `obj.model_copy(update={"field": value})` |
| JSON schema | `Model.model_json_schema()` |
