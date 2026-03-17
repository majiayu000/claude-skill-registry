---
name: data-modeler
description: Design data models with Pydantic schemas, comprehensive validation rules,
  type annotations, and relationship mappings.
allowed-tools: Read, Write, Edit
---

## Purpose

The data-modeler skill provides comprehensive guidance for designing robust data models using Pydantic, Python's most popular data validation library. This skill helps the Architecture Designer agent create type-safe, validated data structures that serve as the foundation for feature implementations.

This skill emphasizes:
- **Type Safety:** Complete type annotations for all fields
- **Validation:** Comprehensive validators for business rules
- **Documentation:** Clear field descriptions and constraints
- **Relationships:** Proper modeling of entity relationships
- **Serialization:** Correct handling of JSON/dict conversion

The data-modeler skill ensures that data models are not just simple data containers, but intelligent objects that enforce business rules, validate data integrity, and provide clear contracts for data interchange.

## When to Use

This skill auto-activates when the agent describes:
- "Design data models for..."
- "Create Pydantic schemas for..."
- "Define data structures with..."
- "Model the data with..."
- "Create validation rules for..."
- "Define entity relationships..."
- "Specify field constraints for..."
- "Design request/response schemas..."

## Provided Capabilities

### 1. Pydantic Schema Design

**What it provides:**
- BaseModel class structure
- Field definitions with types and constraints
- Default values and factory functions
- Optional vs required fields
- Nested model composition
- Model inheritance patterns

**Guidance:**
- Use `Field()` for metadata and constraints
- Provide `description` for all fields
- Set appropriate `default` or `default_factory`
- Use `Optional[T]` for nullable fields
- Validate field names follow conventions

**Example:**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Address(BaseModel):
    """Nested address model."""
    street: str = Field(..., description="Street address", min_length=1, max_length=200)
    city: str = Field(..., description="City name", min_length=1, max_length=100)
    state: str = Field(..., description="State/province code", min_length=2, max_length=2)
    postal_code: str = Field(..., description="Postal/ZIP code", regex=r"^\d{5}(-\d{4})?$")
    country: str = Field(default="US", description="Country code (ISO 3166-1 alpha-2)")

    class Config:
        schema_extra = {
            "example": {
                "street": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "postal_code": "62701",
                "country": "US"
            }
        }

class User(BaseModel):
    """User data model with comprehensive validation."""

    # Identity fields
    id: Optional[int] = Field(None, description="User ID (auto-generated)")
    username: str = Field(..., description="Unique username", min_length=3, max_length=50)
    email: str = Field(..., description="Email address (validated)")

    # Profile fields
    full_name: str = Field(..., description="User's full name", min_length=1, max_length=200)
    role: UserRole = Field(default=UserRole.USER, description="User role")
    is_active: bool = Field(default=True, description="Account active status")

    # Nested model
    address: Optional[Address] = Field(None, description="Mailing address")

    # Lists
    tags: List[str] = Field(default_factory=list, description="User tags")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        """Pydantic model configuration."""
        # Allow ORM models to be parsed
        orm_mode = True

        # Use enum values in JSON
        use_enum_values = True

        # Example for documentation
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "role": "user",
                "address": {
                    "street": "123 Main St",
                    "city": "Springfield",
                    "state": "IL",
                    "postal_code": "62701"
                },
                "tags": ["verified", "premium"]
            }
        }
```

### 2. Field-Level Validators

**What it provides:**
- `@validator` decorator usage
- Value transformation
- Cross-field validation
- Custom error messages
- Pre and post validation

**Validation Types:**
- **Format validation:** Email, URL, phone, regex
- **Range validation:** min/max for numbers, length for strings
- **Business rules:** Custom logic validation
- **Referential integrity:** Cross-field checks

**Example:**
```python
from pydantic import BaseModel, Field, validator, root_validator
import re

class UserRegistration(BaseModel):
    """User registration with comprehensive validation."""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(...)
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)
    age: int = Field(..., ge=13, le=120)
    phone: Optional[str] = Field(None)

    @validator('username')
    def validate_username(cls, v):
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must contain only letters, numbers, hyphens, and underscores')

        # Check against reserved names
        reserved = ['admin', 'root', 'system']
        if v.lower() in reserved:
            raise ValueError(f'Username "{v}" is reserved')

        return v.lower()  # Normalize to lowercase

    @validator('email')
    def validate_email(cls, v):
        """Validate email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email format')

        return v.lower()  # Normalize to lowercase

    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password strength."""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')

        return v

    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is None:
            return v

        # Remove all non-digit characters
        digits = re.sub(r'\D', '', v)

        if len(digits) != 10:
            raise ValueError('Phone number must be 10 digits')

        # Return formatted phone
        return f'({digits[:3]}) {digits[3:6]}-{digits[6:]}'

    @root_validator
    def validate_passwords_match(cls, values):
        """Validate that passwords match (cross-field validation)."""
        password = values.get('password')
        password_confirm = values.get('password_confirm')

        if password != password_confirm:
            raise ValueError('Passwords do not match')

        return values
```

### 3. Model-Level Validators

**What it provides:**
- `@root_validator` for cross-field validation
- Pre-validation transformations
- Post-validation checks
- Complex business rule enforcement

**Example:**
```python
from pydantic import BaseModel, Field, root_validator
from datetime import date, datetime
from typing import Optional

class EventBooking(BaseModel):
    """Event booking with complex validation."""

    event_name: str = Field(...)
    start_date: date = Field(...)
    end_date: date = Field(...)
    attendees: int = Field(..., ge=1, le=1000)
    room_capacity: int = Field(..., ge=1)
    is_catering: bool = Field(default=False)
    catering_headcount: Optional[int] = Field(None, ge=1)

    @root_validator(pre=True)
    def convert_date_strings(cls, values):
        """Pre-validation: Convert date strings to date objects."""
        for field in ['start_date', 'end_date']:
            if field in values and isinstance(values[field], str):
                values[field] = datetime.strptime(values[field], '%Y-%m-%d').date()
        return values

    @root_validator
    def validate_dates(cls, values):
        """Validate date logic."""
        start = values.get('start_date')
        end = values.get('end_date')

        if start and end:
            # End must be after start
            if end < start:
                raise ValueError('End date must be after start date')

            # Maximum event duration: 30 days
            if (end - start).days > 30:
                raise ValueError('Event duration cannot exceed 30 days')

            # Must be future dates
            if start < date.today():
                raise ValueError('Event cannot be in the past')

        return values

    @root_validator
    def validate_capacity(cls, values):
        """Validate room capacity vs attendees."""
        attendees = values.get('attendees')
        capacity = values.get('room_capacity')

        if attendees and capacity:
            if attendees > capacity:
                raise ValueError(f'Attendees ({attendees}) exceeds room capacity ({capacity})')

        return values

    @root_validator
    def validate_catering(cls, values):
        """Validate catering requirements."""
        is_catering = values.get('is_catering')
        catering_headcount = values.get('catering_headcount')
        attendees = values.get('attendees')

        if is_catering:
            # Catering headcount required if catering enabled
            if not catering_headcount:
                raise ValueError('Catering headcount required when catering is enabled')

            # Catering headcount cannot exceed attendees
            if catering_headcount > attendees:
                raise ValueError('Catering headcount cannot exceed number of attendees')
        else:
            # No catering headcount if catering disabled
            if catering_headcount:
                raise ValueError('Catering headcount specified but catering is disabled')

        return values
```

### 4. Type Annotations and Constraints

**What it provides:**
- Proper use of typing module
- Generic types (List, Dict, Set, Tuple)
- Union types and Optional
- Literal types for constants
- Custom types

**Example:**
```python
from pydantic import BaseModel, Field, constr, conint, confloat, conlist
from typing import List, Dict, Set, Optional, Union, Literal, Any
from datetime import datetime

# Custom constrained types
Username = constr(regex=r'^[a-zA-Z0-9_-]+$', min_length=3, max_length=50)
PositiveInt = conint(gt=0)
Percentage = confloat(ge=0.0, le=100.0)
NonEmptyList = conlist(str, min_items=1)

class ProductStatus(str, Enum):
    """Product status enum."""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"

class Product(BaseModel):
    """Product model with advanced type annotations."""

    # Basic types with constraints
    id: Optional[int] = None
    name: constr(min_length=1, max_length=200)
    sku: constr(regex=r'^[A-Z]{3}-\d{6}$')  # Format: ABC-123456

    # Numeric types with constraints
    price: confloat(gt=0.0, le=1000000.0)
    discount_percentage: Percentage = 0.0
    stock_quantity: PositiveInt

    # Enum
    status: ProductStatus = ProductStatus.DRAFT

    # Collections
    tags: List[str] = Field(default_factory=list)
    categories: Set[str] = Field(default_factory=set)
    attributes: Dict[str, Any] = Field(default_factory=dict)

    # Union types
    metadata: Union[Dict[str, str], None] = None

    # Literal type (specific values only)
    measurement_unit: Literal["kg", "lb", "oz", "g"]

    # Nested models
    dimensions: Optional['ProductDimensions'] = None

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class ProductDimensions(BaseModel):
    """Product dimensions (nested model)."""
    length: confloat(gt=0)
    width: confloat(gt=0)
    height: confloat(gt=0)
    unit: Literal["cm", "in", "m"]

    @property
    def volume(self) -> float:
        """Calculate volume."""
        return self.length * self.width * self.height

# Enable forward reference
Product.update_forward_refs()
```

### 5. Relationship Mappings

**What it provides:**
- One-to-one relationships
- One-to-many relationships
- Many-to-many relationships
- Foreign key references
- Embedded vs referenced documents

**Relationship Patterns:**

**One-to-One:**
```python
class UserProfile(BaseModel):
    """User profile (one-to-one with User)."""
    user_id: int = Field(..., description="Foreign key to User")
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None

class User(BaseModel):
    """User with one-to-one profile."""
    id: int
    username: str
    profile: Optional[UserProfile] = None  # Embedded relationship
```

**One-to-Many:**
```python
class Comment(BaseModel):
    """Comment (many comments per post)."""
    id: int
    post_id: int = Field(..., description="Foreign key to Post")
    content: str
    created_at: datetime

class Post(BaseModel):
    """Post with many comments."""
    id: int
    title: str
    content: str
    comments: List[Comment] = Field(default_factory=list)  # Embedded list
```

**Many-to-Many:**
```python
class Tag(BaseModel):
    """Tag entity."""
    id: int
    name: str

class Article(BaseModel):
    """Article with many tags."""
    id: int
    title: str
    tag_ids: List[int] = Field(default_factory=list)  # Reference by ID
    # OR
    tags: List[Tag] = Field(default_factory=list)  # Embedded tags
```

### 6. Serialization Strategies

**What it provides:**
- JSON serialization/deserialization
- `dict()` conversion with exclusions
- `json()` output with formatting
- Custom serializers for complex types
- Alias usage for field naming

**Example:**
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ApiResponse(BaseModel):
    """API response with serialization control."""

    id: int
    name: str
    internal_code: str = Field(..., alias="code")  # Use 'code' in JSON
    created_at: datetime
    secret_key: Optional[str] = None  # Should not be exposed
    _internal_state: str = "processing"  # Private field (not serialized)

    class Config:
        # Allow field aliases
        allow_population_by_field_name = True

        # Custom JSON encoders
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Usage
response = ApiResponse(
    id=1,
    name="Test",
    code="ABC123",
    created_at=datetime.utcnow(),
    secret_key="secret"
)

# Serialize to dict (exclude secret)
data = response.dict(exclude={'secret_key'})
# {'id': 1, 'name': 'Test', 'internal_code': 'ABC123', 'created_at': datetime(...)}

# Serialize to JSON with alias
json_str = response.json(by_alias=True, exclude={'secret_key'})
# {"id": 1, "name": "Test", "code": "ABC123", "created_at": "2025-10-29T..."}

# Include/exclude specific fields
data = response.dict(include={'id', 'name'})
# {'id': 1, 'name': 'Test'}
```

## Usage Guide

### Step 1: Identify Data Entities
```
Requirements → Entities → Attributes → Relationships
```

### Step 2: Define Base Models
```
Create BaseModel → Add fields → Set types → Add descriptions
```

### Step 3: Add Constraints
```
Field(...) → min/max → regex → custom constraints
```

### Step 4: Implement Validators
```
@validator → business rules → error messages → transformations
```

### Step 5: Model Relationships
```
Identify relationships → Choose embedding vs reference → Add foreign keys
```

### Step 6: Configure Serialization
```
Config class → JSON encoders → Aliases → ORM mode
```

### Step 7: Add Examples
```
schema_extra → Example data → Documentation
```

### Step 8: Test Models
```
Create instances → Validate data → Test edge cases → Check errors
```

## Best Practices

1. **Use Field() for Metadata**
   - Always provide descriptions
   - Set constraints (min/max, regex)
   - Provide examples in Config

2. **Comprehensive Validation**
   - Validate at field level when possible
   - Use root_validator for cross-field logic
   - Provide clear error messages

3. **Type Safety**
   - Use specific types, not Any
   - Use Optional[T] for nullable fields
   - Use Enum for fixed choices

4. **Documentation**
   - Description for every field
   - Examples in schema_extra
   - Docstrings for complex logic

5. **Serialization Control**
   - Use aliases for API compatibility
   - Exclude sensitive fields
   - Custom encoders for complex types

6. **Model Organization**
   - Group related models in same file
   - Use inheritance for shared fields
   - Keep models focused and cohesive

## Resources

### data-model-guide.md
Comprehensive data modeling guide including:
- Entity-relationship principles
- Normalization guidelines
- Pydantic model structure best practices
- Validation strategies and patterns
- Type hints and annotations guide
- Field constraints catalog

### pydantic-patterns.md
Pydantic-specific patterns and examples:
- BaseModel advanced usage
- Custom validators (field and model level)
- Field validators with dependencies
- Root validators for complex logic
- Config options and settings
- Nested models and composition
- Serialization and deserialization
- ORM mode and database integration
- Complete code examples

## Example Usage

### Input (from Architecture Designer agent):
```
"Design data models for a user management system with user profiles, addresses, roles, and audit logging."
```

### Output (data-modeler skill provides):
```python
# Comprehensive data models with validation

from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    """User roles."""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class Address(BaseModel):
    """User address."""
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    postal_code: str = Field(..., regex=r'^\d{5}(-\d{4})?$')

class UserProfile(BaseModel):
    """User profile information."""
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    phone: Optional[str] = Field(None, regex=r'^\(\d{3}\) \d{3}-\d{4}$')

    @validator('avatar_url')
    def validate_avatar_url(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            raise ValueError('Avatar URL must be HTTP/HTTPS')
        return v

class User(BaseModel):
    """Main user model."""
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(...)
    full_name: str = Field(..., min_length=1, max_length=200)
    role: UserRole = UserRole.USER
    is_active: bool = True

    # Relationships
    profile: Optional[UserProfile] = None
    addresses: List[Address] = Field(default_factory=list)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

    @validator('email')
    def validate_email(cls, v):
        import re
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email format')
        return v.lower()

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "role": "user",
                "profile": {
                    "bio": "Software engineer",
                    "phone": "(555) 123-4567"
                },
                "addresses": [{
                    "street": "123 Main St",
                    "city": "Springfield",
                    "state": "IL",
                    "postal_code": "62701"
                }]
            }
        }
```

## Integration

### Used By:
- **@architecture-designer** (Primary) - Phase 2 sub-agent for architecture design

### Integrates With:
- **architecture-planner** skill - Data models designed after component structure
- **api-designer** skill - Data models used in API request/response schemas

### Workflow Position:
1. Analysis Specialist completes requirements analysis
2. Architecture Designer receives analysis
3. architecture-planner skill designs component structure (Step 3)
4. **data-modeler skill** designs data models (Step 4)
5. api-designer skill designs API contracts using these models (Step 5)
6. Results synthesized into PRP

---

**Version:** 2.0.0
**Auto-Activation:** Yes
**Phase:** 2 - Design & Planning
**Created:** 2025-10-29