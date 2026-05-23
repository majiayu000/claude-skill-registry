---
name: openapi-spec-generation
description: Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns.

summary: |
  - Use `openapi: 3.1.0` with JSON Schema support
  - Design-first for new APIs, code-first for existing
  - Structure: info → servers → paths → components
  - Validate with: spectral, openapi-generator validate
  - Generate SDKs: `openapi-generator generate -i spec.yaml -g typescript-axios`

context_cost: high
load_when:
  - 'openapi'
  - 'swagger'
  - 'api documentation'
  - 'api spec'
  - 'sdk generation'

enhances:
  - api-design-principles
---

# OpenAPI Spec Generation

Patterns for creating and validating OpenAPI 3.1 specifications.

## When to Use

- Creating API documentation from scratch
- Generating OpenAPI specs from existing code
- Designing API contracts (design-first approach)
- Validating API implementations against specs
- Generating client SDKs from specs

## Core Concepts

### OpenAPI 3.1 Structure

```yaml
openapi: 3.1.0
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

### Design Approaches

| Approach         | Description                  | Best For            |
| ---------------- | ---------------------------- | ------------------- |
| **Design-First** | Write spec before code       | New APIs, contracts |
| **Code-First**   | Generate spec from code      | Existing APIs       |
| **Hybrid**       | Annotate code, generate spec | Evolving APIs       |

## Quick Reference

### Common Components

```yaml
components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id: { type: string, format: uuid }
        email: { type: string, format: email }

  parameters:
    PageParam:
      name: page
      in: query
      schema: { type: integer, minimum: 1, default: 1 }

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema: { $ref: '#/components/schemas/Error' }
```

### Authentication Patterns

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - BearerAuth: []
```

## Validation Commands

```bash
# Validate spec
npx @stoplight/spectral-cli lint openapi.yaml

# Generate TypeScript client
npx openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./generated-client

# Generate server stub
npx openapi-generator-cli generate \
  -i openapi.yaml \
  -g nodejs-express-server \
  -o ./generated-server
```

## Best Practices

1. **Use $ref extensively** — DRY principle for schemas
2. **Include examples** — Real data helps consumers
3. **Document errors** — All possible error responses
4. **Version in URL** — `/v1/`, `/v2/` for breaking changes
5. **Use operationId** — Unique, descriptive IDs for SDK generation

---

_For detailed templates, see [templates.md](./templates.md)_
_For validation patterns, see [validation.md](./validation.md)_
