---
name: Data Validation Rules
description: Implementing comprehensive validation rules across database, application, and pipeline layers to ensure data integrity.
---

# Data Validation Rules

## Overview

Data Validation Rules are constraints and checks that ensure data meets quality standards before being stored or processed. Validation should happen at multiple layers—database, application, API, and pipeline—to create defense in depth.

**Core Principle**: "Validate early, validate often. Never trust user input or upstream data."

---

## 1. Levels of Data Validation

| Layer | When | Tools | Pros | Cons |
|-------|------|-------|------|------|
| **Database** | On INSERT/UPDATE | Constraints, triggers | Guaranteed enforcement | Hard to change, limited logic |
| **Application** | Before save | Pydantic, Zod | Rich validation logic | Can be bypassed |
| **API** | On request | FastAPI, Joi | Early feedback to client | Duplicates app logic |
| **Pipeline** | During ETL | Great Expectations, dbt | Catches bad data | Runs after ingestion |

---

## 2. Common Validation Patterns

### Required Field Validation
```python
# Pydantic
from pydantic import BaseModel, Field

class User(BaseModel):
    email: str  # Required by default
    name: str = Field(..., min_length=1)  # Explicit required with constraint
```

### Type Validation
```typescript
// Zod (TypeScript)
import { z } from 'zod';

const UserSchema = z.object({
  age: z.number().int().positive(),
  email: z.string().email(),
  isActive: z.boolean()
});

// Validate
const result = UserSchema.safeParse(data);
if (!result.success) {
  console.error(result.error);
}
```

### Format Validation (Regex)
```python
import re
from pydantic import BaseModel, validator

class Contact(BaseModel):
    phone: str
    ssn: str
    
    @validator('phone')
    def validate_phone(cls, v):
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid phone number format')
        return v
    
    @validator('ssn')
    def validate_ssn(cls, v):
        pattern = r'^\d{3}-\d{2}-\d{4}$'
        if not re.match(pattern, v):
            raise ValueError('SSN must be in format XXX-XX-XXXX')
        return v
```

### Range Validation
```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    price: float = Field(gt=0, le=1000000)  # 0 < price <= 1,000,000
    quantity: int = Field(ge=0)  # quantity >= 0
    discount_percent: float = Field(ge=0, le=100)  # 0 <= discount <= 100
```

### Enum Validation
```typescript
// Zod
const OrderStatus = z.enum(['pending', 'processing', 'shipped', 'delivered', 'cancelled']);

const OrderSchema = z.object({
  orderId: z.string().uuid(),
  status: OrderStatus
});
```

### Cross-Field Validation
```python
from pydantic import BaseModel, root_validator

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime
    
    @root_validator
    def validate_date_range(cls, values):
        start = values.get('start_date')
        end = values.get('end_date')
        
        if start and end and start > end:
            raise ValueError('start_date must be before end_date')
        
        return values
```

### Conditional Validation
```python
from pydantic import BaseModel, validator

class ShippingAddress(BaseModel):
    country: str
    state: str | None = None
    postal_code: str
    
    @validator('state')
    def validate_state(cls, v, values):
        # State required for US addresses
        if values.get('country') == 'US' and not v:
            raise ValueError('State is required for US addresses')
        return v
```

---

## 3. Validation Libraries

### Python: Pydantic
```python
from pydantic import BaseModel, EmailStr, HttpUrl, constr, conint
from typing import List

class User(BaseModel):
    user_id: constr(regex=r'^[A-Z0-9]{8}$')  # Constrained string
    email: EmailStr  # Built-in email validation
    age: conint(ge=18, le=120)  # Constrained integer
    website: HttpUrl | None = None  # URL validation
    tags: List[str] = []
    
    class Config:
        # Validate on assignment
        validate_assignment = True

# Usage
try:
    user = User(
        user_id="ABC12345",
        email="user@example.com",
        age=25
    )
except ValidationError as e:
    print(e.json())
```

### TypeScript: Zod
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  userId: z.string().regex(/^[A-Z0-9]{8}$/),
  email: z.string().email(),
  age: z.number().int().min(18).max(120),
  website: z.string().url().optional(),
  tags: z.array(z.string()).default([])
});

type User = z.infer<typeof UserSchema>;

// Validate
const result = UserSchema.safeParse(data);
if (result.success) {
  const user: User = result.data;
} else {
  console.error(result.error.format());
}
```

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "userId": {
      "type": "string",
      "pattern": "^[A-Z0-9]{8}$"
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 18,
      "maximum": 120
    }
  },
  "required": ["userId", "email", "age"]
}
```

---

## 4. Database-Level Validation

### CHECK Constraints
```sql
CREATE TABLE products (
    product_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0),
    discount_percent DECIMAL(5,2) CHECK (discount_percent >= 0 AND discount_percent <= 100),
    stock_quantity INT CHECK (stock_quantity >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Multi-column check
    CONSTRAINT valid_discount CHECK (
        (price * (1 - discount_percent/100)) > 0
    )
);
```

### Triggers for Complex Rules
```sql
-- Trigger to validate business hours
CREATE OR REPLACE FUNCTION validate_business_hours()
RETURNS TRIGGER AS $$
BEGIN
    IF EXTRACT(HOUR FROM NEW.order_time) < 9 OR 
       EXTRACT(HOUR FROM NEW.order_time) > 17 THEN
        RAISE EXCEPTION 'Orders can only be placed during business hours (9 AM - 5 PM)';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_business_hours
BEFORE INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION validate_business_hours();
```

### Domain Types (PostgreSQL)
```sql
-- Create reusable domain types with validation
CREATE DOMAIN email_address AS VARCHAR(255)
CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$');

CREATE DOMAIN us_phone AS VARCHAR(20)
CHECK (VALUE ~ '^\+?1?\d{10}$');

CREATE DOMAIN positive_price AS DECIMAL(10,2)
CHECK (VALUE > 0);

-- Use in table
CREATE TABLE customers (
    customer_id UUID PRIMARY KEY,
    email email_address NOT NULL,
    phone us_phone
);
```

---

## 5. API Validation

### FastAPI (Python)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    age: int = Field(..., ge=18, le=120)

@app.post("/users")
async def create_user(user: CreateUserRequest):
    # Validation happens automatically
    # If invalid, FastAPI returns 422 with detailed errors
    return {"user_id": "123", "email": user.email}
```

### Fastify (Node.js)
```javascript
const fastify = require('fastify')();

const userSchema = {
  body: {
    type: 'object',
    required: ['email', 'password', 'age'],
    properties: {
      email: { type: 'string', format: 'email' },
      password: { type: 'string', minLength: 8, maxLength: 100 },
      age: { type: 'integer', minimum: 18, maximum: 120 }
    }
  }
};

fastify.post('/users', { schema: userSchema }, async (request, reply) => {
  // Validation happens automatically
  return { userId: '123', email: request.body.email };
});
```

---

## 6. ETL Pipeline Validation

### Pre-Validation (Before Processing)
```python
def validate_input_file(filepath: str) -> bool:
    """Validate file before processing"""
    df = pd.read_csv(filepath)
    
    # Check required columns
    required_columns = ['user_id', 'email', 'created_at']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Check row count
    if len(df) == 0:
        raise ValueError("File is empty")
    
    # Check for nulls in critical columns
    null_counts = df[required_columns].isnull().sum()
    if null_counts.any():
        raise ValueError(f"Null values found: {null_counts[null_counts > 0]}")
    
    return True
```

### Post-Validation (After Load)
```python
def validate_loaded_data(table_name: str):
    """Validate data after loading to database"""
    
    # Check referential integrity
    orphaned_records = db.execute(f"""
        SELECT COUNT(*) FROM {table_name} t
        LEFT JOIN users u ON t.user_id = u.user_id
        WHERE u.user_id IS NULL
    """).fetchone()[0]
    
    if orphaned_records > 0:
        raise ValueError(f"Found {orphaned_records} orphaned records")
    
    # Check for duplicates
    duplicates = db.execute(f"""
        SELECT user_id, COUNT(*) as cnt
        FROM {table_name}
        GROUP BY user_id
        HAVING COUNT(*) > 1
    """).fetchall()
    
    if duplicates:
        raise ValueError(f"Found {len(duplicates)} duplicate user_ids")
```

---

## 7. Validation Error Handling

### Meaningful Error Messages
```python
from pydantic import BaseModel, validator, ValidationError

class Order(BaseModel):
    order_id: str
    total_amount: float
    
    @validator('total_amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError(
                f'Total amount must be positive, got {v}. '
                'Please check the order items and try again.'
            )
        return v

try:
    order = Order(order_id="123", total_amount=-10)
except ValidationError as e:
    # Returns user-friendly error
    print(e.errors())
    # [{'loc': ('total_amount',), 'msg': 'Total amount must be positive...', 'type': 'value_error'}]
```

### Error Aggregation
```python
def validate_batch(records: List[dict]) -> dict:
    """Validate multiple records and aggregate errors"""
    valid_records = []
    errors = []
    
    for idx, record in enumerate(records):
        try:
            validated = UserSchema(**record)
            valid_records.append(validated)
        except ValidationError as e:
            errors.append({
                'record_index': idx,
                'record': record,
                'errors': e.errors()
            })
    
    return {
        'valid_count': len(valid_records),
        'error_count': len(errors),
        'valid_records': valid_records,
        'errors': errors
    }
```

---

## 8. Performance Considerations

### Batch Validation
```python
# ❌ Slow: Validate one by one
for record in records:
    validate(record)

# ✅ Fast: Validate in batch
df = pd.DataFrame(records)
validate_dataframe(df)
```

### Caching Validation Results
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def is_valid_email(email: str) -> bool:
    """Cache validation results for frequently checked emails"""
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))
```

---

## 9. Real-World Validation Scenarios

### User Registration
```python
class UserRegistration(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str
    age: int = Field(..., ge=13)  # COPPA compliance
    terms_accepted: bool
    
    @validator('password')
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
    
    @root_validator
    def validate_passwords_match(cls, values):
        pw1 = values.get('password')
        pw2 = values.get('password_confirm')
        if pw1 != pw2:
            raise ValueError('Passwords do not match')
        return values
    
    @validator('terms_accepted')
    def validate_terms(cls, v):
        if not v:
            raise ValueError('You must accept the terms and conditions')
        return v
```

### Payment Processing
```python
class PaymentRequest(BaseModel):
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    currency: str = Field(..., regex=r'^[A-Z]{3}$')
    card_number: str
    cvv: str = Field(..., regex=r'^\d{3,4}$')
    
    @validator('card_number')
    def validate_card(cls, v):
        # Luhn algorithm
        def luhn_check(card_num):
            digits = [int(d) for d in card_num if d.isdigit()]
            checksum = sum(digits[-1::-2]) + sum(sum(divmod(2*d, 10)) for d in digits[-2::-2])
            return checksum % 10 == 0
        
        if not luhn_check(v):
            raise ValueError('Invalid card number')
        return v
```

---

## 10. Data Validation Checklist

- [ ] **Database**: Are constraints (NOT NULL, CHECK, FK) in place?
- [ ] **Application**: Is input validated before database writes?
- [ ] **API**: Are request/response schemas enforced?
- [ ] **Pipeline**: Is data validated before and after ETL?
- [ ] **Errors**: Are validation errors user-friendly and actionable?
- [ ] **Performance**: Is validation optimized for batch operations?
- [ ] **Testing**: Are validation rules themselves tested?
- [ ] **Documentation**: Are validation rules documented for API consumers?

---

## Related Skills
- `43-data-reliability/data-quality-checks`
- `43-data-reliability/data-contracts`
- `43-data-reliability/schema-management`
