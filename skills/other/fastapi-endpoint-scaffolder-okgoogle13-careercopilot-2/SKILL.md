---
name: fastapi-endpoint-scaffolder
description: "Scaffolds a new FastAPI endpoint with Pydantic models, router registration, and tests. Use when creating new backend API endpoints. Related: pydantic-model-scaffolder for complex model validation."
---

# FastAPI Endpoint Scaffolder Workflow

This skill creates a complete FastAPI endpoint with proper structure, type safety, and testing scaffolding.

## Workflow Steps

1. **Ask for endpoint details:**
   - Endpoint name (e.g., `notifications`, `email_templates`)
   - HTTP methods needed (GET, POST, PUT, DELETE, PATCH)
   - URL path (e.g., `/notifications`, `/email/templates`)
   - Brief description of what this endpoint does

2. **Ask for model fields:**
   - Request model fields (e.g., `email: str, subject: str, body: str`)
   - Response model fields (e.g., `id: str, status: str, sent_at: datetime`)
   - Optional fields (mark with `Optional[type]`)

3. **Generate endpoint file:**
   - Read template: `.claude/skills/fastapi-endpoint-scaffolder/templates/endpoint.py.tpl`
   - Replace placeholders:
     - `{{ENDPOINT_NAME}}` - Snake_case name (e.g., `notifications`)
     - `{{ENDPOINT_PATH}}` - URL path (e.g., `/notifications`)
     - `{{ENDPOINT_DESCRIPTION}}` - Brief description
     - `{{REQUEST_MODEL}}` - PascalCase request model name
     - `{{RESPONSE_MODEL}}` - PascalCase response model name
     - `{{HTTP_METHOD}}` - HTTP method (post, get, put, delete)
   - Write to: `backend/app/api/endpoints/{{ENDPOINT_NAME}}.py`

4. **Generate models file:**
   - Read template: `.claude/skills/fastapi-endpoint-scaffolder/templates/models.py.tpl`
   - Replace placeholders:
     - `{{MODEL_NAME}}` - PascalCase model name
     - `{{REQUEST_FIELDS}}` - Request model fields
     - `{{RESPONSE_FIELDS}}` - Response model fields
   - Write to: `backend/app/models/{{ENDPOINT_NAME}}_schemas.py`

5. **Update router registration:**
   - Read: `backend/app/api/router.py`
   - Add import: `from .endpoints import {{ENDPOINT_NAME}}`
   - Add router tuple: `({{ENDPOINT_NAME}}.router, "/{{ENDPOINT_PATH}}", "{{TAG_NAME}}")`
   - Write updated file

6. **Update models **init**.py:**
   - Read: `backend/app/models/__init__.py`
   - Add imports from new schema file
   - Add to `__all__` list
   - Write updated file

7. **Generate test file:**
   - Read template: `.claude/skills/fastapi-endpoint-scaffolder/templates/test_endpoint.py.tpl`
   - Replace placeholders
   - Write to: `backend/app/tests/api/test_{{ENDPOINT_NAME}}.py`

8. **Report success:**
   - List all created/modified files
   - Show example curl command for testing
   - Remind user to implement business logic in the endpoint

## Example Usage

```
User: Create a new endpoint for managing user notifications
```
