---
name: openapi
description: "OpenAPI Specification (OAS 3.x): document structure, paths, operations, schemas, parameters, security schemes, and validation."
version: "3.2.0"
release_date: "2025-09-19"
---

# OpenAPI Specification

This skill provides guidance for working with OpenAPI Specification (OAS) documents.

**Current version:** OpenAPI 3.2.0 (September 2025)

## Quick Navigation

- Document structure: `references/document-structure.md`
- Operations & paths: `references/operations.md`
- Schemas & data types: `references/schemas.md`
- Parameters & serialization: `references/parameters.md`
- Security: `references/security.md`

## When to Use

- Creating a new OpenAPI specification document
- Describing HTTP API endpoints
- Defining request/response schemas
- Configuring API security (OAuth2, API keys, JWT)
- Validating an existing OpenAPI document
- Generating client/server code from specs

## Document Structure Overview

An OpenAPI document MUST have either an OpenAPI Object or Schema Object at the root.

### Required Fields

```yaml
openapi: 3.2.0 # REQUIRED: OAS version
info: # REQUIRED: API metadata
  title: My API
  version: 1.0.0
```

### Complete Structure

```yaml
openapi: 3.2.0
info:
  title: Example API
  version: 1.0.0
  description: API description (supports CommonMark)
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get:
      summary: List resources
      responses:
        "200":
          description: Success
components:
  schemas: {}
  parameters: {}
  responses: {}
  securitySchemes: {}
security:
  - apiKey: []
tags:
  - name: resources
    description: Resource operations
```

## Core Objects Reference

### Info Object

```yaml
info:
  title: Example API # REQUIRED
  version: 1.0.0 # REQUIRED (API version, NOT OAS version)
  summary: Short summary
  description: Full description (CommonMark)
  termsOfService: https://example.com/terms
  contact:
    name: API Support
    url: https://example.com/support
    email: support@example.com
  license:
    name: Apache 2.0
    identifier: Apache-2.0 # OR url (mutually exclusive)
```

### Server Object

```yaml
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://{environment}.example.com:{port}/v1
    description: Configurable
    variables:
      environment:
        default: api
        enum: [api, staging, dev]
      port:
        default: "443"
```

### Path Item Object

```yaml
/users/{id}:
  summary: User operations
  parameters:
    - $ref: "#/components/parameters/userId"
  get:
    operationId: getUser
    responses:
      "200":
        description: User found
  put:
    operationId: updateUser
    requestBody:
      $ref: "#/components/requestBodies/UserUpdate"
    responses:
      "200":
        description: User updated
```

### Operation Object

```yaml
get:
  tags: [users]
  summary: Get user by ID
  description: Returns a single user
  operationId: getUserById # MUST be unique across all operations
  parameters:
    - name: id
      in: path
      required: true
      schema:
        type: string
  responses:
    "200":
      description: Success
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/User"
    "404":
      description: Not found
  security:
    - bearerAuth: []
  deprecated: false
```

## Schema Recipes

### Basic Object

```yaml
components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        age:
          type: integer
          minimum: 0
```

### Composition with allOf

```yaml
ExtendedUser:
  allOf:
    - $ref: "#/components/schemas/User"
    - type: object
      properties:
        role:
          type: string
          enum: [admin, user, guest]
```

### Polymorphism with oneOf

```yaml
Pet:
  oneOf:
    - $ref: "#/components/schemas/Cat"
    - $ref: "#/components/schemas/Dog"
  discriminator:
    propertyName: petType
    mapping:
      cat: "#/components/schemas/Cat"
      dog: "#/components/schemas/Dog"
```

### Nullable and Optional

```yaml
# OAS 3.1+ uses JSON Schema type arrays
properties:
  nickname:
    type: [string, "null"] # nullable
```

## Parameter Locations

| Location     | `in` value    | Notes                               |
| ------------ | ------------- | ----------------------------------- |
| Path         | `path`        | MUST be required: true              |
| Query        | `query`       | Standard query parameters           |
| Query string | `querystring` | Entire query string as single param |
| Header       | `header`      | Case-insensitive names              |
| Cookie       | `cookie`      | Cookie values                       |

### Parameter Styles

| Style      | `in`  | Type                   | Example (color=blue,black) |
| ---------- | ----- | ---------------------- | -------------------------- |
| simple     | path  | array                  | blue,black                 |
| form       | query | primitive/array/object | color=blue,black           |
| matrix     | path  | primitive/array/object | ;color=blue,black          |
| label      | path  | primitive/array/object | .blue.black                |
| deepObject | query | object                 | color[R]=100&color[G]=200  |

## Security Schemes

### API Key

```yaml
components:
  securitySchemes:
    apiKey:
      type: apiKey
      in: header # header, query, or cookie
      name: X-API-Key
```

### Bearer Token (JWT)

```yaml
bearerAuth:
  type: http
  scheme: bearer
  bearerFormat: JWT
```

### OAuth2

```yaml
oauth2:
  type: oauth2
  flows:
    authorizationCode:
      authorizationUrl: https://auth.example.com/authorize
      tokenUrl: https://auth.example.com/token
      scopes:
        read:users: Read user data
        write:users: Modify user data
```

### Apply Security

```yaml
# Global (all operations)
security:
  - bearerAuth: []

# Per-operation
paths:
  /public:
    get:
      security: [] # Override: no auth required
  /protected:
    get:
      security:
        - oauth2: [read:users]
```

## Reference Object

Use `$ref` to avoid duplication:

```yaml
# Reference within same document
$ref: '#/components/schemas/User'

# Reference to external file
$ref: './schemas/user.yaml'
$ref: './common.yaml#/components/schemas/Error'
```

## Components Object

Reusable building blocks:

```yaml
components:
  schemas: # Data models
  responses: # Reusable responses
  parameters: # Reusable parameters
  examples: # Reusable examples
  requestBodies: # Reusable request bodies
  headers: # Reusable headers
  securitySchemes: # Security definitions
  links: # Links between operations
  callbacks: # Webhook definitions
  pathItems: # Reusable path items
```

## Best Practices Checklist

- [ ] Include `operationId` for all operations (unique, programming-friendly)
- [ ] Use `$ref` for reusable components
- [ ] Add meaningful `description` fields (supports CommonMark)
- [ ] Define all possible response codes
- [ ] Include `examples` for complex schemas
- [ ] Use `tags` to group related operations
- [ ] Mark deprecated operations with `deprecated: true`
- [ ] Use semantic versioning for `info.version`

## Critical Prohibitions

- Do NOT omit `openapi` and `info` fields (they are REQUIRED)
- Do NOT use duplicate `operationId` values
- Do NOT mix `$ref` with sibling properties in Reference Objects
- Do NOT use path parameters without `required: true`
- Do NOT use implicit OAuth2 flow in new APIs (deprecated)
- Do NOT forget security for protected endpoints

## Validation

### File Naming

- Entry document: `openapi.json` or `openapi.yaml` (recommended)
- Format: JSON or YAML (equivalent)
- All field names are case-sensitive

### Common Validation Errors

| Error                      | Fix                                                   |
| -------------------------- | ----------------------------------------------------- |
| Missing required field     | Add `openapi`, `info.title`, `info.version`           |
| Invalid operationId        | Use unique, valid identifier                          |
| Path parameter not in path | Ensure `{param}` matches parameter name               |
| Duplicate path template    | Remove conflicting `/users/{id}` vs `/users/{userId}` |
| Invalid $ref               | Check URI syntax and target existence                 |

## Links

- Official spec: https://spec.openapis.org/oas/latest.html
- Learning resources: https://learn.openapis.org/
- JSON Schema (for schemas): https://json-schema.org/
