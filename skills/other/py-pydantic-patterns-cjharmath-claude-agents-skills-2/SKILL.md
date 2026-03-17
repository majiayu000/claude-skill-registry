---
name: py-pydantic-patterns
description: Pydantic v2 patterns for validation and serialization. Use when creating schemas, validating data, or working with request/response models.
---

# Pydantic v2 Patterns

## Problem Statement

Pydantic v2 has significant API changes from v1. This codebase uses v2. Wrong patterns cause validation failures, serialization bugs, and frontend integration issues.

---

## Pattern: v1 to v2 Migration

**Critical changes to know:**

```python
# ❌ v1 (OLD - don't use)
from pydantic import validator
class Model(BaseModel):
    class Config:
        orm_mode = True
    
    @validator("email")
    def validate_email(cls, v):
        return v.lower()
    
    def dict(self):
        ...

# ✅ v2 (CURRENT)
from pydantic import field_validator, ConfigDict
class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.lower()
    
    def model_dump(self):
        ...
```

**Quick reference:**

| v1 | v2 |
|----|-----|
| `class Config` | `model_config = ConfigDict(...)` |
| `orm_mode = True` | `from_attributes=True` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |
| `parse_obj()` | `model_validate()` |
| `update_forward_refs()` | `model_rebuild()` |

---

## Pattern: Field Validators

```python
from pydantic import BaseModel, field_validator, ValidationInfo

class AssessmentCreate(BaseModel):
    title: str
    skill_areas: list[str]
    max_score: int
    
    # Single field validator
    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()
    
    # Validator with access to other fields
    @field_validator("max_score")
    @classmethod
    def validate_max_score(cls, v: int, info: ValidationInfo) -> int:
        if v < 1:
            raise ValueError("Max score must be positive")
        return v
    
    # Multiple fields
    @field_validator("skill_areas")
    @classmethod
    def validate_skill_areas(cls, v: list[str]) -> list[str]:
        valid = {"fundamentals", "advanced", "strategy"}
        for area in v:
            if area not in valid:
                raise ValueError(f"Invalid skill area: {area}")
        return v
```

---

## Pattern: Model Validators

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime
    
    # Before validation (raw input)
    @model_validator(mode="before")
    @classmethod
    def parse_dates(cls, data: dict) -> dict:
        # Handle string dates
        if isinstance(data.get("start_date"), str):
            data["start_date"] = datetime.fromisoformat(data["start_date"])
        return data
    
    # After validation (validated model)
    @model_validator(mode="after")
    def validate_range(self) -> "DateRange":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self
```

---

## Pattern: Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class UserRead(BaseModel):
    # Configure model behavior
    model_config = ConfigDict(
        from_attributes=True,      # Allow from ORM objects
        str_strip_whitespace=True, # Strip strings
        str_min_length=1,          # No empty strings by default
        validate_default=True,     # Validate default values
        extra="forbid",            # Error on extra fields
        frozen=False,              # Allow mutation
    )
    
    id: UUID
    email: str
    created_at: datetime

# Usage with SQLModel objects
user_db = await session.get(User, user_id)
user_read = UserRead.model_validate(user_db)  # Works due to from_attributes
```

---

## Pattern: Field Definitions

```python
from pydantic import BaseModel, Field
from typing import Annotated

class AssessmentCreate(BaseModel):
    # Basic constraints
    title: str = Field(min_length=1, max_length=200)
    score: int = Field(ge=0, le=100)  # 0 <= score <= 100
    rating: float = Field(gt=0, lt=5.5)  # 0 < rating < 5.5
    
    # With description (shows in OpenAPI)
    skill_areas: list[str] = Field(
        min_length=1,
        description="List of skill areas to assess",
        examples=[["fundamentals", "strategy"]],
    )
    
    # Optional with default
    notes: str | None = Field(default=None, max_length=1000)
    
    # Computed default
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Reusable type with constraints
PositiveInt = Annotated[int, Field(gt=0)]
Rating = Annotated[float, Field(ge=1.0, le=5.5)]

class Result(BaseModel):
    count: PositiveInt
    rating: Rating
```

---

## Pattern: Discriminated Unions

**Problem:** Polymorphic responses where type depends on a field.

```python
from pydantic import BaseModel, Field
from typing import Literal, Union
from typing_extensions import Annotated

class TextQuestion(BaseModel):
    type: Literal["text"] = "text"
    prompt: str
    max_length: int

class MultipleChoiceQuestion(BaseModel):
    type: Literal["multiple_choice"] = "multiple_choice"
    prompt: str
    options: list[str]

class RatingQuestion(BaseModel):
    type: Literal["rating"] = "rating"
    prompt: str
    min_value: int
    max_value: int

# Discriminated union - Pydantic uses 'type' field to determine class
Question = Annotated[
    Union[TextQuestion, MultipleChoiceQuestion, RatingQuestion],
    Field(discriminator="type"),
]

class Assessment(BaseModel):
    questions: list[Question]

# Pydantic automatically deserializes to correct type
data = {
    "questions": [
        {"type": "text", "prompt": "Describe...", "max_length": 500},
        {"type": "rating", "prompt": "Rate...", "min_value": 1, "max_value": 5},
    ]
}
assessment = Assessment.model_validate(data)
# assessment.questions[0] is TextQuestion
# assessment.questions[1] is RatingQuestion
```

---

## Pattern: Custom Types

```python
from pydantic import BaseModel, AfterValidator, BeforeValidator
from typing import Annotated
import re

# Email normalization
def normalize_email(v: str) -> str:
    return v.lower().strip()

Email = Annotated[str, AfterValidator(normalize_email)]

# Phone validation
def validate_phone(v: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", v)
    if not re.match(r"^\+?1?\d{10,14}$", cleaned):
        raise ValueError("Invalid phone number")
    return cleaned

PhoneNumber = Annotated[str, BeforeValidator(validate_phone)]

# UUID from string
def parse_uuid(v: str | UUID) -> UUID:
    if isinstance(v, str):
        return UUID(v)
    return v

UUIDStr = Annotated[UUID, BeforeValidator(parse_uuid)]

class User(BaseModel):
    email: Email
    phone: PhoneNumber | None = None
    id: UUIDStr
```

---

## Pattern: Serialization Control

```python
from pydantic import BaseModel, field_serializer, computed_field

class User(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    
    # Custom serialization
    @field_serializer("created_at")
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat()
    
    @field_serializer("id")
    def serialize_uuid(self, id: UUID) -> str:
        return str(id)
    
    # Computed field (included in serialization)
    @computed_field
    @property
    def display_name(self) -> str:
        return self.email.split("@")[0]

# Serialization options
user.model_dump()                          # Full dict
user.model_dump(exclude={"created_at"})    # Exclude fields
user.model_dump(include={"id", "email"})   # Include only
user.model_dump(exclude_none=True)         # Skip None values
user.model_dump(by_alias=True)             # Use field aliases
user.model_dump_json()                     # JSON string
```

---

## Pattern: Schema Inheritance

```python
class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str  # Only for creation

class UserRead(UserBase):
    id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    # All optional for partial updates
    email: str | None = None
    name: str | None = None
    password: str | None = None
```

---

## Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| "X is not a valid dict" | Using `.dict()` (v1) | Use `.model_dump()` |
| "Unable to parse ORM object" | Missing `from_attributes` | Add `ConfigDict(from_attributes=True)` |
| "@validator not recognized" | v1 decorator | Use `@field_validator` with `@classmethod` |
| "Extra fields not permitted" | `extra="forbid"` | Remove extra fields or change config |
| Validation not running | Default value not validated | Add `validate_default=True` |

---

## Detection Commands

```bash
# Find v1 patterns
grep -rn "class Config:" --include="*.py"
grep -rn "@validator" --include="*.py"
grep -rn "\.dict()" --include="*.py"
grep -rn "orm_mode" --include="*.py"
```
