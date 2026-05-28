---
name: json-schema-validator
description: Validate JSON data against JSON Schema specifications. Use for API validation, config file validation, or data quality checks.
---

# JSON Schema Validator

Validate JSON documents against JSON Schema (Draft 7) specifications.

## Features

- **Schema Validation**: Validate JSON against schema
- **Error Details**: Detailed validation error messages
- **Batch Validation**: Validate multiple files
- **Schema Generation**: Generate schema from examples
- **Multiple Drafts**: Support for Draft 4, 6, 7

## Quick Start

```python
from json_validator import JSONValidator

validator = JSONValidator()

# Validate data against schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0}
    },
    "required": ["name"]
}

data = {"name": "John", "age": 30}
result = validator.validate(data, schema)
print(f"Valid: {result['valid']}")
```

## CLI Usage

```bash
# Validate JSON file against schema
python json_validator.py --data user.json --schema user_schema.json

# Validate with inline schema
python json_validator.py --data config.json --schema '{"type": "object"}'

# Generate schema from sample
python json_validator.py --generate sample.json --output schema.json

# Batch validate directory
python json_validator.py --data-dir ./configs/ --schema config_schema.json
```

## API Reference

### JSONValidator Class

```python
class JSONValidator:
    def __init__(self, draft: str = "draft7")

    # Validation
    def validate(self, data: dict, schema: dict) -> dict
    def validate_file(self, data_path: str, schema_path: str) -> dict
    def validate_batch(self, data_files: list, schema: dict) -> list

    # Schema operations
    def generate_schema(self, data: dict) -> dict
    def check_schema(self, schema: dict) -> dict
```

## Validation Result

```python
{
    "valid": True,  # or False
    "errors": [],   # List of error details
    "path": "$",    # JSON path to data root
}

# With errors:
{
    "valid": False,
    "errors": [
        {
            "message": "'name' is a required property",
            "path": "$",
            "schema_path": "required"
        },
        {
            "message": "-5 is less than minimum 0",
            "path": "$.age",
            "schema_path": "properties.age.minimum"
        }
    ]
}
```

## Schema Examples

### Object Schema
```python
schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "active": {"type": "boolean", "default": True}
    },
    "required": ["id", "name", "email"],
    "additionalProperties": False
}
```

### Array Schema
```python
schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "value": {"type": "number"}
        }
    },
    "minItems": 1,
    "uniqueItems": True
}
```

### Nested Schema
```python
schema = {
    "type": "object",
    "properties": {
        "user": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"}
                    }
                }
            }
        }
    }
}
```

## Generate Schema from Data

```python
validator = JSONValidator()

sample_data = {
    "name": "Product A",
    "price": 29.99,
    "tags": ["electronics", "sale"],
    "inStock": True
}

schema = validator.generate_schema(sample_data)
# Returns inferred schema based on data types
```

## Supported Keywords

### Type Validation
- `type`: string, number, integer, boolean, array, object, null
- `enum`: allowed values
- `const`: exact value

### String Validation
- `minLength`, `maxLength`
- `pattern`: regex pattern
- `format`: email, uri, date, date-time, ipv4, ipv6, uuid

### Number Validation
- `minimum`, `maximum`
- `exclusiveMinimum`, `exclusiveMaximum`
- `multipleOf`

### Array Validation
- `items`: schema for items
- `minItems`, `maxItems`
- `uniqueItems`
- `contains`

### Object Validation
- `properties`: property schemas
- `required`: required properties
- `additionalProperties`
- `minProperties`, `maxProperties`
- `patternProperties`

## Error Handling

```python
result = validator.validate(data, schema)

if not result['valid']:
    for error in result['errors']:
        print(f"Error at {error['path']}: {error['message']}")
```

## Dependencies

- jsonschema>=4.20.0
