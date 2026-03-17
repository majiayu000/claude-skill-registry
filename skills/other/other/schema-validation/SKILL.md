---
slug: "schema-validation"
display_name: "Schema Validation"
description: "JSON/data schema validation for construction data exchange: API payloads, file imports, BIM exports. Ensure data structure compliance before processing."
---

# Schema Validation for Construction Data

## Overview

Validate data structures against defined schemas for construction data exchange. Ensure API payloads, file imports, and BIM exports conform to expected formats before processing.

## Schema Validation Framework

### Core Schema Validator

```python
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum
import json
import re
from datetime import datetime

class SchemaType(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    DATE = "date"
    DATETIME = "datetime"
    CSI_CODE = "csi_code"
    CURRENCY = "currency"
    GUID = "guid"

@dataclass
class SchemaField:
    name: str
    type: SchemaType
    required: bool = True
    nullable: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    enum_values: Optional[List[Any]] = None
    items_schema: Optional['Schema'] = None  # For arrays
    properties: Optional[Dict[str, 'SchemaField']] = None  # For objects
    description: str = ""

@dataclass
class Schema:
    name: str
    version: str
    fields: Dict[str, SchemaField]
    description: str = ""

@dataclass
class SchemaValidationError:
    path: str
    message: str
    expected: str
    actual: Any

@dataclass
class SchemaValidationResult:
    is_valid: bool
    errors: List[SchemaValidationError] = field(default_factory=list)
    schema_name: str = ""
    schema_version: str = ""

    def add_error(self, path: str, message: str, expected: str, actual: Any):
        self.errors.append(SchemaValidationError(path, message, expected, actual))
        self.is_valid = False

    def to_report(self) -> str:
        lines = [
            f"Schema Validation: {self.schema_name} v{self.schema_version}",
            "=" * 50,
            f"Status: {'✓ VALID' if self.is_valid else '✗ INVALID'}",
            f"Errors: {len(self.errors)}",
            ""
        ]

        for error in self.errors:
            lines.append(f"❌ {error.path}")
            lines.append(f"   {error.message}")
            lines.append(f"   Expected: {error.expected}")
            lines.append(f"   Actual: {error.actual}")
            lines.append("")

        return "\n".join(lines)


class SchemaValidator:
    """Validate data against schemas."""

    # Custom type patterns
    PATTERNS = {
        SchemaType.CSI_CODE: r'^\d{2}\s?\d{2}\s?\d{2}$',
        SchemaType.GUID: r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$',
        SchemaType.CURRENCY: r'^-?\d+(\.\d{2})?$',
        SchemaType.DATE: r'^\d{4}-\d{2}-\d{2}$',
        SchemaType.DATETIME: r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
    }

    def validate(self, data: Any, schema: Schema) -> SchemaValidationResult:
        result = SchemaValidationResult(
            is_valid=True,
            schema_name=schema.name,
            schema_version=schema.version
        )

        self._validate_object(data, schema.fields, "", result)
        return result

    def _validate_object(self, data: Any, fields: Dict[str, SchemaField], path: str, result: SchemaValidationResult):
        if not isinstance(data, dict):
            result.add_error(path or "root", "Expected object", "object", type(data).__name__)
            return

        # Check required fields
        for field_name, field_schema in fields.items():
            field_path = f"{path}.{field_name}" if path else field_name

            if field_name not in data:
                if field_schema.required:
                    result.add_error(field_path, "Required field missing", "present", "missing")
                continue

            value = data[field_name]

            # Check nullable
            if value is None:
                if not field_schema.nullable:
                    result.add_error(field_path, "Field cannot be null", "non-null", "null")
                continue

            # Validate type
            self._validate_field(value, field_schema, field_path, result)

        # Check for extra fields (warning only)
        for key in data.keys():
            if key not in fields:
                # Could add warning here if needed
                pass

    def _validate_field(self, value: Any, schema: SchemaField, path: str, result: SchemaValidationResult):
        # Type validation
        if not self._check_type(value, schema.type):
            result.add_error(path, f"Invalid type", schema.type.value, type(value).__name__)
            return

        # String validations
        if schema.type == SchemaType.STRING:
            if schema.min_length and len(value) < schema.min_length:
                result.add_error(path, f"String too short", f"min {schema.min_length}", len(value))
            if schema.max_length and len(value) > schema.max_length:
                result.add_error(path, f"String too long", f"max {schema.max_length}", len(value))
            if schema.pattern and not re.match(schema.pattern, value):
                result.add_error(path, "Pattern mismatch", schema.pattern, value)

        # Numeric validations
        if schema.type in (SchemaType.NUMBER, SchemaType.INTEGER):
            if schema.min_value is not None and value < schema.min_value:
                result.add_error(path, "Value below minimum", f">= {schema.min_value}", value)
            if schema.max_value is not None and value > schema.max_value:
                result.add_error(path, "Value above maximum", f"<= {schema.max_value}", value)

        # Enum validation
        if schema.enum_values and value not in schema.enum_values:
            result.add_error(path, "Invalid enum value", str(schema.enum_values), value)

        # Array validation
        if schema.type == SchemaType.ARRAY and schema.items_schema:
            for i, item in enumerate(value):
                item_path = f"{path}[{i}]"
                if schema.items_schema.fields:
                    self._validate_object(item, schema.items_schema.fields, item_path, result)

        # Nested object validation
        if schema.type == SchemaType.OBJECT and schema.properties:
            self._validate_object(value, schema.properties, path, result)

        # Custom type validation
        if schema.type in self.PATTERNS:
            pattern = self.PATTERNS[schema.type]
            if not re.match(pattern, str(value)):
                result.add_error(path, f"Invalid {schema.type.value} format", pattern, value)

    def _check_type(self, value: Any, expected: SchemaType) -> bool:
        type_checks = {
            SchemaType.STRING: lambda v: isinstance(v, str),
            SchemaType.NUMBER: lambda v: isinstance(v, (int, float)),
            SchemaType.INTEGER: lambda v: isinstance(v, int) and not isinstance(v, bool),
            SchemaType.BOOLEAN: lambda v: isinstance(v, bool),
            SchemaType.ARRAY: lambda v: isinstance(v, list),
            SchemaType.OBJECT: lambda v: isinstance(v, dict),
            SchemaType.DATE: lambda v: isinstance(v, str),
            SchemaType.DATETIME: lambda v: isinstance(v, str),
            SchemaType.CSI_CODE: lambda v: isinstance(v, str),
            SchemaType.CURRENCY: lambda v: isinstance(v, (int, float, str)),
            SchemaType.GUID: lambda v: isinstance(v, str),
        }
        return type_checks.get(expected, lambda v: True)(value)
```

## Construction Data Schemas

### Cost Estimate Schema

```python
# Define schema for cost estimate data
COST_ESTIMATE_SCHEMA = Schema(
    name="CostEstimate",
    version="1.0",
    description="Schema for construction cost estimates",
    fields={
        "project_id": SchemaField(
            name="project_id",
            type=SchemaType.STRING,
            required=True,
            description="Unique project identifier"
        ),
        "project_name": SchemaField(
            name="project_name",
            type=SchemaType.STRING,
            required=True,
            max_length=200
        ),
        "estimate_type": SchemaField(
            name="estimate_type",
            type=SchemaType.STRING,
            required=True,
            enum_values=["conceptual", "schematic", "design_development", "construction_documents", "bid"]
        ),
        "estimate_date": SchemaField(
            name="estimate_date",
            type=SchemaType.DATE,
            required=True
        ),
        "currency": SchemaField(
            name="currency",
            type=SchemaType.STRING,
            required=False,
            enum_values=["USD", "EUR", "GBP", "CAD"],
            nullable=True
        ),
        "gross_area": SchemaField(
            name="gross_area",
            type=SchemaType.NUMBER,
            required=True,
            min_value=0,
            description="Gross floor area in SF or SM"
        ),
        "line_items": SchemaField(
            name="line_items",
            type=SchemaType.ARRAY,
            required=True,
            items_schema=Schema(
                name="LineItem",
                version="1.0",
                fields={
                    "id": SchemaField(name="id", type=SchemaType.STRING, required=True),
                    "csi_code": SchemaField(name="csi_code", type=SchemaType.CSI_CODE, required=False, nullable=True),
                    "description": SchemaField(name="description", type=SchemaType.STRING, required=True, max_length=500),
                    "quantity": SchemaField(name="quantity", type=SchemaType.NUMBER, required=True, min_value=0),
                    "unit": SchemaField(name="unit", type=SchemaType.STRING, required=True),
                    "unit_cost": SchemaField(name="unit_cost", type=SchemaType.NUMBER, required=True, min_value=0),
                    "amount": SchemaField(name="amount", type=SchemaType.NUMBER, required=True, min_value=0),
                }
            )
        ),
        "subtotal": SchemaField(
            name="subtotal",
            type=SchemaType.NUMBER,
            required=True,
            min_value=0
        ),
        "contingency_percent": SchemaField(
            name="contingency_percent",
            type=SchemaType.NUMBER,
            required=False,
            min_value=0,
            max_value=50
        ),
        "total": SchemaField(
            name="total",
            type=SchemaType.NUMBER,
            required=True,
            min_value=0
        )
    }
)
```

### Schedule Data Schema

```python
SCHEDULE_SCHEMA = Schema(
    name="ProjectSchedule",
    version="1.0",
    description="Schema for project schedule data",
    fields={
        "project_id": SchemaField(name="project_id", type=SchemaType.STRING, required=True),
        "schedule_name": SchemaField(name="schedule_name", type=SchemaType.STRING, required=True),
        "data_date": SchemaField(name="data_date", type=SchemaType.DATE, required=True),
        "start_date": SchemaField(name="start_date", type=SchemaType.DATE, required=True),
        "finish_date": SchemaField(name="finish_date", type=SchemaType.DATE, required=True),
        "calendar": SchemaField(
            name="calendar",
            type=SchemaType.STRING,
            required=False,
            enum_values=["5-day", "6-day", "7-day"],
            nullable=True
        ),
        "tasks": SchemaField(
            name="tasks",
            type=SchemaType.ARRAY,
            required=True,
            items_schema=Schema(
                name="Task",
                version="1.0",
                fields={
                    "id": SchemaField(name="id", type=SchemaType.STRING, required=True),
                    "wbs": SchemaField(name="wbs", type=SchemaType.STRING, required=False, nullable=True),
                    "name": SchemaField(name="name", type=SchemaType.STRING, required=True, max_length=300),
                    "start_date": SchemaField(name="start_date", type=SchemaType.DATE, required=True),
                    "finish_date": SchemaField(name="finish_date", type=SchemaType.DATE, required=True),
                    "duration": SchemaField(name="duration", type=SchemaType.INTEGER, required=True, min_value=0),
                    "percent_complete": SchemaField(name="percent_complete", type=SchemaType.NUMBER, required=False, min_value=0, max_value=100),
                    "predecessors": SchemaField(name="predecessors", type=SchemaType.ARRAY, required=False, nullable=True),
                    "resources": SchemaField(name="resources", type=SchemaType.ARRAY, required=False, nullable=True),
                }
            )
        )
    }
)
```

### BIM Element Schema

```python
BIM_ELEMENT_SCHEMA = Schema(
    name="BIMElement",
    version="1.0",
    description="Schema for BIM element data",
    fields={
        "guid": SchemaField(name="guid", type=SchemaType.GUID, required=True),
        "ifc_class": SchemaField(
            name="ifc_class",
            type=SchemaType.STRING,
            required=True,
            pattern=r'^Ifc[A-Z][a-zA-Z]+$'
        ),
        "name": SchemaField(name="name", type=SchemaType.STRING, required=False, nullable=True),
        "description": SchemaField(name="description", type=SchemaType.STRING, required=False, nullable=True),
        "level": SchemaField(name="level", type=SchemaType.STRING, required=False, nullable=True),
        "classification": SchemaField(
            name="classification",
            type=SchemaType.OBJECT,
            required=False,
            nullable=True,
            properties={
                "system": SchemaField(name="system", type=SchemaType.STRING, required=True),
                "code": SchemaField(name="code", type=SchemaType.STRING, required=True),
                "name": SchemaField(name="name", type=SchemaType.STRING, required=False, nullable=True),
            }
        ),
        "quantities": SchemaField(
            name="quantities",
            type=SchemaType.OBJECT,
            required=False,
            nullable=True,
            properties={
                "area": SchemaField(name="area", type=SchemaType.NUMBER, required=False, min_value=0, nullable=True),
                "volume": SchemaField(name="volume", type=SchemaType.NUMBER, required=False, min_value=0, nullable=True),
                "length": SchemaField(name="length", type=SchemaType.NUMBER, required=False, min_value=0, nullable=True),
                "count": SchemaField(name="count", type=SchemaType.INTEGER, required=False, min_value=0, nullable=True),
            }
        ),
        "properties": SchemaField(name="properties", type=SchemaType.OBJECT, required=False, nullable=True)
    }
)
```

### RFI Schema

```python
RFI_SCHEMA = Schema(
    name="RFI",
    version="1.0",
    description="Schema for Request for Information",
    fields={
        "rfi_number": SchemaField(name="rfi_number", type=SchemaType.STRING, required=True, pattern=r'^RFI-\d+$'),
        "project_id": SchemaField(name="project_id", type=SchemaType.STRING, required=True),
        "subject": SchemaField(name="subject", type=SchemaType.STRING, required=True, max_length=500),
        "status": SchemaField(
            name="status",
            type=SchemaType.STRING,
            required=True,
            enum_values=["draft", "submitted", "in_review", "answered", "closed"]
        ),
        "priority": SchemaField(
            name="priority",
            type=SchemaType.STRING,
            required=False,
            enum_values=["low", "medium", "high", "critical"],
            nullable=True
        ),
        "date_submitted": SchemaField(name="date_submitted", type=SchemaType.DATE, required=True),
        "date_required": SchemaField(name="date_required", type=SchemaType.DATE, required=True),
        "from_company": SchemaField(name="from_company", type=SchemaType.STRING, required=True),
        "to_company": SchemaField(name="to_company", type=SchemaType.STRING, required=True),
        "spec_section": SchemaField(name="spec_section", type=SchemaType.CSI_CODE, required=False, nullable=True),
        "drawing_reference": SchemaField(name="drawing_reference", type=SchemaType.STRING, required=False, nullable=True),
        "question": SchemaField(name="question", type=SchemaType.STRING, required=True),
        "response": SchemaField(name="response", type=SchemaType.STRING, required=False, nullable=True),
        "date_responded": SchemaField(name="date_responded", type=SchemaType.DATE, required=False, nullable=True),
        "attachments": SchemaField(name="attachments", type=SchemaType.ARRAY, required=False, nullable=True)
    }
)
```

## Schema Registry

```python
class ConstructionSchemaRegistry:
    """Registry of construction data schemas."""

    def __init__(self):
        self.schemas: Dict[str, Schema] = {}
        self._register_defaults()

    def _register_defaults(self):
        self.register(COST_ESTIMATE_SCHEMA)
        self.register(SCHEDULE_SCHEMA)
        self.register(BIM_ELEMENT_SCHEMA)
        self.register(RFI_SCHEMA)

    def register(self, schema: Schema):
        key = f"{schema.name}:{schema.version}"
        self.schemas[key] = schema
        # Also register without version for latest
        self.schemas[schema.name] = schema

    def get(self, name: str, version: str = None) -> Optional[Schema]:
        if version:
            return self.schemas.get(f"{name}:{version}")
        return self.schemas.get(name)

    def validate(self, data: Any, schema_name: str, version: str = None) -> SchemaValidationResult:
        schema = self.get(schema_name, version)
        if not schema:
            result = SchemaValidationResult(is_valid=False)
            result.add_error("schema", f"Schema '{schema_name}' not found", "valid schema", "not found")
            return result

        validator = SchemaValidator()
        return validator.validate(data, schema)

    def list_schemas(self) -> List[str]:
        return [k for k in self.schemas.keys() if ':' in k]
```

## Usage Examples

```python
# Initialize registry
registry = ConstructionSchemaRegistry()

# Validate cost estimate
estimate_data = {
    "project_id": "PROJ-001",
    "project_name": "Downtown Office Tower",
    "estimate_type": "schematic",
    "estimate_date": "2026-01-15",
    "gross_area": 50000,
    "line_items": [
        {
            "id": "1",
            "csi_code": "03 30 00",
            "description": "Cast-in-place concrete",
            "quantity": 5000,
            "unit": "CY",
            "unit_cost": 150.00,
            "amount": 750000.00
        }
    ],
    "subtotal": 750000.00,
    "contingency_percent": 10,
    "total": 825000.00
}

result = registry.validate(estimate_data, "CostEstimate")
print(result.to_report())

# Validate RFI
rfi_data = {
    "rfi_number": "RFI-042",
    "project_id": "PROJ-001",
    "subject": "Concrete mix design clarification",
    "status": "submitted",
    "priority": "high",
    "date_submitted": "2026-01-20",
    "date_required": "2026-01-27",
    "from_company": "ABC Concrete",
    "to_company": "XYZ Architects",
    "spec_section": "03 30 00",
    "question": "Please clarify the required PSI for the foundation pour."
}

result = registry.validate(rfi_data, "RFI")
if result.is_valid:
    print("RFI data is valid")
else:
    print(result.to_report())
```

## JSON Schema Export

```python
def export_to_json_schema(schema: Schema) -> dict:
    """Export DDC schema to JSON Schema format."""

    def field_to_json_schema(field: SchemaField) -> dict:
        type_map = {
            SchemaType.STRING: "string",
            SchemaType.NUMBER: "number",
            SchemaType.INTEGER: "integer",
            SchemaType.BOOLEAN: "boolean",
            SchemaType.ARRAY: "array",
            SchemaType.OBJECT: "object",
            SchemaType.DATE: "string",
            SchemaType.DATETIME: "string",
            SchemaType.CSI_CODE: "string",
            SchemaType.CURRENCY: "number",
            SchemaType.GUID: "string",
        }

        js = {"type": type_map.get(field.type, "string")}

        if field.description:
            js["description"] = field.description
        if field.min_value is not None:
            js["minimum"] = field.min_value
        if field.max_value is not None:
            js["maximum"] = field.max_value
        if field.min_length is not None:
            js["minLength"] = field.min_length
        if field.max_length is not None:
            js["maxLength"] = field.max_length
        if field.pattern:
            js["pattern"] = field.pattern
        if field.enum_values:
            js["enum"] = field.enum_values

        if field.type == SchemaType.DATE:
            js["format"] = "date"
        if field.type == SchemaType.DATETIME:
            js["format"] = "date-time"
        if field.type == SchemaType.GUID:
            js["format"] = "uuid"

        return js

    properties = {}
    required = []

    for name, field in schema.fields.items():
        properties[name] = field_to_json_schema(field)
        if field.required:
            required.append(name)

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": schema.name,
        "description": schema.description,
        "type": "object",
        "properties": properties,
        "required": required
    }

# Export to JSON Schema
json_schema = export_to_json_schema(COST_ESTIMATE_SCHEMA)
print(json.dumps(json_schema, indent=2))
```

## Integration with DDC Pipeline

```python
# Validate API request before processing
def validate_api_request(endpoint: str, payload: dict) -> SchemaValidationResult:
    schema_map = {
        '/api/estimates': 'CostEstimate',
        '/api/schedules': 'ProjectSchedule',
        '/api/rfis': 'RFI',
        '/api/bim/elements': 'BIMElement'
    }

    schema_name = schema_map.get(endpoint)
    if not schema_name:
        result = SchemaValidationResult(is_valid=True)
        return result

    registry = ConstructionSchemaRegistry()
    return registry.validate(payload, schema_name)

# Use in API handler
@app.post('/api/estimates')
def create_estimate(payload: dict):
    validation = validate_api_request('/api/estimates', payload)
    if not validation.is_valid:
        return {'error': 'Validation failed', 'details': [e.__dict__ for e in validation.errors]}, 400

    # Process valid data
    return process_estimate(payload)
```

## Resources

- **JSON Schema**: https://json-schema.org/
- **CSI MasterFormat**: Standard classification codes
- **IFC Schema**: https://standards.buildingsmart.org/IFC/
