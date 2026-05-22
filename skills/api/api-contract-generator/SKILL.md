---
name: api-contract-generator
description: Generates OpenAPI/Swagger schemas for API endpoints. Creates comprehensive API contracts from endpoint implementations, ensuring consistency between code and documentation.
context:fork: true
model: sonnet
allowed-tools: read, write, grep, codebase_search
---

# API Contract Generator Skill

Generates OpenAPI/Swagger schemas for API endpoints, creating comprehensive API contracts from endpoint implementations.

## When to Use

- After creating new API endpoints
- When updating existing endpoints
- To ensure API documentation matches implementation
- To generate client SDKs from contracts

## Instructions

### Step 1: Analyze Endpoint Implementation

1. **Read endpoint code**:
   - Identify route handlers (Next.js App Router, FastAPI, Express, etc.)
   - Extract HTTP methods (GET, POST, PUT, DELETE, etc.)
   - Identify request/response types

2. **Extract route information**:
   - Path parameters (e.g., `/api/users/{id}`)
   - Query parameters (e.g., `?page=1&limit=10`)
   - Request body structure
   - Response structure

3. **Identify data models**:
   - Find TypeScript interfaces or Python Pydantic models
   - Extract field types and validation rules
   - Identify nested objects and arrays

### Step 2: Generate OpenAPI Schema

1. **Create OpenAPI 3.0 structure**:

   ```yaml
   openapi: 3.0.0
   info:
     title: API Name
     version: 1.0.0
   paths:
     /api/endpoint:
       get:
         summary: Endpoint description
         parameters: [...]
         responses: { ... }
   ```

2. **Map request/response types**:
   - Convert TypeScript interfaces to JSON Schema
   - Convert Pydantic models to JSON Schema
   - Handle nested types and arrays
   - Include validation constraints (min, max, pattern, etc.)

3. **Add endpoint documentation**:
   - Extract JSDoc/Python docstrings for descriptions
   - Include parameter descriptions
   - Document response codes and error cases

### Step 3: Validate Schema

1. **Schema validation**:
   - Verify OpenAPI schema is valid
   - Check all referenced schemas exist
   - Ensure required fields are marked

2. **Implementation validation**:
   - Verify schema matches actual implementation
   - Check all endpoints are documented
   - Ensure response types match

### Step 4: Save Contract

1. **Save OpenAPI schema**:
   - Location: `.claude/context/artifacts/api-contract-{endpoint}.yaml`
   - Or: `docs/api/openapi.yaml` (project convention)
   - Include in artifact registry

2. **Generate documentation** (optional):
   - Use Swagger UI or Redoc for visualization
   - Generate HTML documentation
   - Include in project docs

## Supported Frameworks

- **Next.js App Router**: Analyzes `app/api/**/route.ts` files
- **FastAPI**: Analyzes Pydantic models and route decorators
- **Express**: Analyzes route handlers and middleware
- **Django REST Framework**: Analyzes serializers and viewsets

## Example Output

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /api/users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
```

## Related Documentation

- [CUJ-010](../../docs/cujs/CUJ-010.md) - API Endpoint Development
- [OpenAPI Specification](https://swagger.io/specification/)
