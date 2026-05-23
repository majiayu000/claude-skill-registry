---
name: api-response-mocker
description: Generate realistic mock API responses with fake data. Use for testing, prototyping, or creating sample data for frontend development.
---

# API Response Mocker

Generate realistic mock API responses with fake data using Faker.

## Features

- **Schema-Based Generation**: Define response structure
- **Faker Integration**: Realistic fake data
- **Nested Objects**: Complex nested structures
- **Arrays**: Generate lists of objects
- **Relationships**: Reference other mock data
- **Multiple Formats**: JSON, XML output

## Quick Start

```python
from api_mocker import APIMocker

mocker = APIMocker()

# Generate user response
user = mocker.generate({
    "id": "uuid",
    "name": "name",
    "email": "email",
    "created_at": "datetime"
})

# Generate list of users
users = mocker.generate_list({
    "id": "uuid",
    "name": "name",
    "email": "email"
}, count=10)
```

## CLI Usage

```bash
# Generate from schema file
python api_mocker.py --schema user_schema.json --output user.json

# Generate list
python api_mocker.py --schema product.json --count 50 --output products.json

# Generate with seed (reproducible)
python api_mocker.py --schema order.json --seed 42 --output order.json

# Preview without saving
python api_mocker.py --schema customer.json --preview
```

## Schema Format

Define fields using Faker provider names:

```json
{
    "id": "uuid",
    "first_name": "first_name",
    "last_name": "last_name",
    "email": "email",
    "phone": "phone_number",
    "company": "company",
    "address": {
        "street": "street_address",
        "city": "city",
        "state": "state",
        "zip": "zipcode",
        "country": "country"
    },
    "created_at": "date_time_this_year",
    "is_active": "boolean"
}
```

## Available Data Types

### Personal
- `name`, `first_name`, `last_name`
- `email`, `safe_email`
- `phone_number`
- `ssn`

### Address
- `address`, `street_address`
- `city`, `state`, `state_abbr`
- `zipcode`, `postcode`
- `country`, `country_code`
- `latitude`, `longitude`

### Internet
- `url`, `domain_name`
- `ipv4`, `ipv6`
- `user_name`, `password`
- `uuid`, `uuid4`
- `mac_address`

### Business
- `company`, `company_suffix`
- `job`, `job_title`
- `bs`, `catch_phrase`

### Financial
- `credit_card_number`
- `iban`, `bban`
- `currency_code`
- `price` (custom: returns float)

### Date/Time
- `date`, `time`
- `date_time`, `date_time_this_year`
- `date_of_birth`
- `iso8601`

### Text
- `text`, `sentence`, `paragraph`
- `word`, `words`
- `slug`

### Numeric
- `random_int`, `random_number`
- `random_float` (use `{"type": "float", "min": 0, "max": 100}`)
- `boolean`

## Advanced Schemas

### Arrays
```json
{
    "id": "uuid",
    "name": "name",
    "tags": {
        "_array": true,
        "_count": 3,
        "_item": "word"
    },
    "orders": {
        "_array": true,
        "_count": 5,
        "_item": {
            "order_id": "uuid",
            "amount": "random_int",
            "date": "date"
        }
    }
}
```

### Custom Values
```json
{
    "id": "uuid",
    "status": {
        "_choice": ["pending", "active", "completed"]
    },
    "priority": {
        "_range": [1, 5]
    },
    "score": {
        "_float": {"min": 0.0, "max": 100.0, "decimals": 2}
    }
}
```

### Nested Objects
```json
{
    "user": {
        "id": "uuid",
        "profile": {
            "bio": "paragraph",
            "avatar_url": "image_url",
            "social": {
                "twitter": "user_name",
                "linkedin": "url"
            }
        }
    }
}
```

## API Reference

### APIMocker Class

```python
class APIMocker:
    def __init__(self, locale: str = "en_US", seed: int = None)

    # Generation
    def generate(self, schema: dict) -> dict
    def generate_list(self, schema: dict, count: int = 10) -> list

    # File operations
    def from_schema_file(self, filepath: str) -> dict
    def save(self, data: any, filepath: str, format: str = "json")

    # Utilities
    def set_seed(self, seed: int)
    def get_faker(self) -> Faker
```

## Example Schemas

### User Response
```json
{
    "id": "uuid",
    "username": "user_name",
    "email": "email",
    "profile": {
        "first_name": "first_name",
        "last_name": "last_name",
        "avatar": "image_url",
        "bio": "sentence"
    },
    "created_at": "iso8601",
    "last_login": "date_time_this_month"
}
```

### E-commerce Product
```json
{
    "sku": "uuid",
    "name": "catch_phrase",
    "description": "paragraph",
    "price": {"_float": {"min": 9.99, "max": 999.99}},
    "currency": "currency_code",
    "category": {"_choice": ["Electronics", "Clothing", "Home", "Sports"]},
    "in_stock": "boolean",
    "rating": {"_float": {"min": 1, "max": 5, "decimals": 1}},
    "reviews_count": {"_range": [0, 500]}
}
```

### API Error Response
```json
{
    "error": {
        "code": {"_choice": ["NOT_FOUND", "UNAUTHORIZED", "BAD_REQUEST"]},
        "message": "sentence",
        "request_id": "uuid",
        "timestamp": "iso8601"
    }
}
```

## Dependencies

- faker>=22.0.0
