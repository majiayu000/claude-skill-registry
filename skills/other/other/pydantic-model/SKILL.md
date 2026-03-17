---
name: pydantic-model
description: Pydantic v2 model patterns for req/res validation, MongoDB conversion, validation rules. Travel Panel conventions.
---

# Pydantic Model Skill

Pydantic v2 model guidance for Travel Panel.

## When to Use

- Creating req/res models for endpoints
- Defining DTOs
- Adding validation rules
- MongoDB ↔ API response conversion

## Project Context

- Models: `app/classes/<feature>/`
- Version: Pydantic v2 only
- Docs: `docs/endpoint-development-guide.md`

## CRITICAL: v2 API Only

| Deprecated (v1)  | Use (v2)              |
|------------------|-----------------------|
| `__fields__`     | `model_fields`        |
| `__validators__` | `model_validators`    |
| `schema()`       | `model_json_schema()` |
| `parse_obj()`    | `model_validate()`    |
| `dict()`         | `model_dump()`        |
| `json()`         | `model_dump_json()`   |

## Model Creation

### Step 1: Create Model File

Location: `app/classes/<feature>/<feature>_models.py`

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class ItemCreate(BaseModel):
    """Create item request."""
    name: str = Field(..., min_length=1, max_length=255, examples=["My Item"])
    description: Optional[str] = Field(None, max_length=2000)
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)
    tags: List[str] = Field(default_factory=list, max_length=10)
    price: float = Field(..., gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        return list(set(tag.lower().strip() for tag in v if tag.strip()))


class ItemUpdate(BaseModel):
    """Update item request (all opt)."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[StatusEnum] = None
    tags: Optional[List[str]] = None
    price: Optional[float] = Field(None, gt=0)

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "ItemUpdate":
        if not self.model_dump(exclude_unset=True):
            raise ValueError("At least one field must be provided")
        return self


class ItemGet(BaseModel):
    """Item response."""
    id: str
    name: str
    description: Optional[str] = None
    status: str
    tags: List[str] = Field(default_factory=list)
    price: float
    company_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None

    @classmethod
    def from_mongo(cls, doc: dict) -> "ItemGet":
        return cls(
            id=str(doc.get("_id", "")),
            name=doc.get("name", ""),
            description=doc.get("description"),
            status=doc.get("status", "active"),
            tags=doc.get("tags", []),
            price=doc.get("price", 0.0),
            company_id=doc.get("company_id", ""),
            created_at=doc.get("created_at", datetime.now(timezone.utc)),
            updated_at=doc.get("updated_at"),
            created_by=doc.get("created_by"),
        )


class ItemListMeta(BaseModel):
    totalRowCount: int
    page: Optional[int] = None
    pageSize: Optional[int] = None
    stats: Optional[dict] = None


class ItemListResponse(BaseModel):
    data: List[ItemGet]
    meta: ItemListMeta
```

### Step 2: Export from Package

Location: `app/classes/<feature>/__init__.py`

```python
from .feature_models import (
    ItemCreate, ItemUpdate, ItemGet,
    ItemListResponse, ItemListMeta, StatusEnum,
)

__all__ = [
    "ItemCreate", "ItemUpdate", "ItemGet",
    "ItemListResponse", "ItemListMeta", "StatusEnum",
]
```

## Model Patterns

### Create Request

```python
class BookingCreate(BaseModel):
    customer_id: str = Field(..., description="Customer ObjectId")
    product_id: str = Field(..., description="Product ObjectId")
    check_in: datetime
    check_out: datetime
    guests: int = Field(..., ge=1, le=20)
    special_requests: Optional[str] = Field(None, max_length=1000)

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingCreate":
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self
```

### Update Request (Partial)

```python
class BookingUpdate(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    guests: Optional[int] = Field(None, ge=1, le=20)
    special_requests: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = None

    model_config = {"extra": "forbid"}
```

### Response w/ MongoDB Conversion

```python
class BookingGet(BaseModel):
    id: str
    customer_id: str
    product_id: str
    check_in: datetime
    check_out: datetime
    guests: int
    status: str
    total_price: float
    created_at: datetime
    customer: Optional[dict] = None
    product: Optional[dict] = None

    @classmethod
    def from_mongo(cls, doc: dict) -> "BookingGet":
        return cls(
            id=str(doc["_id"]),
            customer_id=str(doc.get("customer_id", "")),
            product_id=str(doc.get("product_id", "")),
            check_in=doc["check_in"],
            check_out=doc["check_out"],
            guests=doc.get("guests", 1),
            status=doc.get("status", "pending"),
            total_price=doc.get("total_price", 0.0),
            created_at=doc.get("created_at", datetime.now(timezone.utc)),
            customer=doc.get("customer"),
            product=doc.get("product"),
        )
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: Optional[str] = None


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[Address] = None
```

### Enum Validation

```python
class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentUpdate(BaseModel):
    status: PaymentStatus  # Auto-validated
```

### Field Validators

```python
import re

class CustomerCreate(BaseModel):
    email: str
    phone: Optional[str] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.lower().strip()
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        digits = re.sub(r"\D", "", v)
        if len(digits) < 10:
            raise ValueError("Phone number too short")
        return digits
```

### Model Validators

```python
class DateRangeFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_date_range(self) -> "DateRangeFilter":
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date must be >= start_date")
        return self
```

### Generic Responses

```python
from typing import TypeVar, Generic

T = TypeVar("T")


class SuccessResponse(BaseModel):
    success: bool = True
    message: str


class CreateResponse(SuccessResponse):
    _id: str
    item_id: Optional[str] = None


class ListResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: dict
```

### MongoDB Doc Prep

```python
class ItemCreate(BaseModel):
    name: str
    status: str = "active"

    def to_mongo(self, company_id: str, user_id: str) -> dict:
        now = datetime.now(timezone.utc)
        return {
            **self.model_dump(),
            "company_id": company_id,
            "created_at": now,
            "updated_at": now,
            "created_by": user_id,
        }
```

## Field Constraints

```python
# String
name: str = Field(..., min_length=1, max_length=100)
code: str = Field(..., pattern=r"^[A-Z]{3}-\d{4}$")

# Numeric
price: float = Field(..., gt=0)
quantity: int = Field(..., ge=0, le=1000)
rating: float = Field(..., ge=0, le=5)

# List
tags: List[str] = Field(default_factory=list, max_length=10)

# Optional w/ default
status: str = Field(default="active")
notes: Optional[str] = Field(default=None, max_length=5000)
```

## Model Config

```python
class MyModel(BaseModel):
    model_config = {
        "extra": "forbid",            # Reject unknown fields
        "str_strip_whitespace": True, # Auto-strip strings
        "validate_assignment": True,  # Validate on attr set
        "populate_by_name": True,     # Allow field aliases
        "json_schema_extra": {"examples": [{"name": "Example"}]},
    }
```

## Checklist

- [ ] Use Pydantic v2 API only
- [ ] Separate models: Create, Update, Get
- [ ] Add `from_mongo()` for response models
- [ ] Use `Field()` for constraints & descriptions
- [ ] `@field_validator` for custom validation
- [ ] `@model_validator` for cross-field validation
- [ ] Define enums for fixed values
- [ ] Export from `__init__.py`
- [ ] Add docstrings
- [ ] Use `Optional[]` for nullable fields
- [ ] Use `datetime.now(timezone.utc)` for timestamps