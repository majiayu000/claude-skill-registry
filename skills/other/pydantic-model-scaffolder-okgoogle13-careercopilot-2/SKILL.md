---
name: pydantic-model-scaffolder
description: "Scaffolds Pydantic models for request/response validation with advanced validation rules. Use for complex data models. Related: fastapi-endpoint-scaffolder for quick endpoint creation."
---

# Pydantic Model Scaffolder Workflow

This skill creates type-safe Pydantic models with validation, documentation, and examples.

## Workflow Steps

1. **Ask for model details:**
   - Model name (PascalCase, e.g., `NotificationPreferences`, `EmailTemplate`)
   - Purpose (e.g., "User notification settings", "Email template data")
   - Model type: Request, Response, Database, or All

2. **Ask for fields:**
   - Field names and types (e.g., `email_enabled: bool`, `push_enabled: bool`, `frequency: str`)
   - Optional fields (mark with `Optional[type]`)
   - Default values if any
   - Field descriptions for documentation
   - Validation rules (e.g., email format, string length, numeric ranges)

3. **Generate model file:**
   - Read template based on model type:
     - `request_model.py.tpl` for request models
     - `response_model.py.tpl` for response models
     - `database_model.py.tpl` for database models
     - `complete_model.py.tpl` for all model types
   - Replace placeholders:
     - `{{MODEL_NAME}}` - PascalCase model name
     - `{{MODEL_DESCRIPTION}}` - Purpose description
     - `{{FIELDS}}` - Field definitions with types
     - `{{VALIDATORS}}` - Custom validators
     - `{{EXAMPLE}}` - Example data for documentation
   - Write to: `backend/app/models/{{model_name_snake}}_schemas.py`

4. **Update models **init**.py:**
   - Read: `backend/app/models/__init__.py`
   - Add import statement for new model
   - Add to `__all__` list
   - Write updated file

5. **Generate validation patterns:**
   - Add field validators for:
     - Email format validation
     - String length constraints
     - Numeric ranges
     - Enum validation
     - Custom business rules

6. **Report success:**
   - Show file path
   - Display generated model structure
   - Show example usage code
   - List validation rules applied

## Model Types

### Request Model

- Used for incoming API requests
- Strict validation
- Required fields enforced
- Examples for OpenAPI docs

### Response Model

- Used for API responses
- May include computed fields
- Documentation for frontend
- Consistent structure

### Database Model

- Used for Firestore/database operations
- May include timestamps
- Conversion methods (to_dict, from_dict)
- Field mapping

## Example Usage

```
User: Create a Pydantic model for notification preferences
Assistant: I'll create a notification preferences model. Let me ask for the details...

- Model name: NotificationPreferences
- Fields:
  - email_enabled: bool (default: True)
  - push_enabled: bool (default: False)
  - sms_enabled: bool (default: False)
  - frequency: str (options: "instant", "daily", "weekly")
  - quiet_hours_start: Optional[int] (0-23)
  - quiet_hours_end: Optional[int] (0-23)
```

## Template Variables

- `{{MODEL_NAME}}`: PascalCase model name
- `{{MODEL_DESCRIPTION}}`: Description of the model's purpose
- `{{FIELDS}}`: Field definitions with types and defaults
- `{{VALIDATORS}}`: Custom validation functions
- `{{EXAMPLE}}`: Example JSON for documentation
- `{{IMPORTS}}`: Required imports based on field types
