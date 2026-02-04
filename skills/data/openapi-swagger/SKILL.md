---
name: openapi-swagger
description: Design, document, and generate APIs using OpenAPI/Swagger specifications. Create interactive API documentation, generate client SDKs, validate schemas, and build mock servers. Use when designing REST APIs, creating API documentation, generating client libraries, or validating API contracts. Triggers on openapi, swagger, api spec, api documentation, sdk generation, api design, redoc, prism mock.
---

# OpenAPI/Swagger API Development

Expert guidance for API design, documentation, and SDK generation.

## Triggers

Use this skill when:
- Writing OpenAPI/Swagger specifications
- Creating interactive API documentation
- Generating client SDKs from API specs
- Validating API schemas
- Building mock servers for development
- API contract testing and design-first development
- Keywords: openapi, swagger, api spec, api documentation, sdk generation, redoc, prism, spectral

## When to Use This Skill

- Designing REST API specifications
- Creating interactive API documentation
- Generating client SDKs
- Validating API schemas
- Building mock servers for development
- API contract testing

---

## OpenAPI Specification Basics

### Minimal OpenAPI 3.0 Spec

```yaml
# api.yaml
openapi: 3.0.3
info:
  title: My API
  description: API description
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Development

paths:
  /health:
    get:
      summary: Health check
      operationId: healthCheck
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: healthy
```

---

## Path Operations

### CRUD Operations

```yaml
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags:
        - Users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
        - name: sort
          in: query
          schema:
            type: string
            enum: [asc, desc]
            default: asc
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

    post:
      summary: Create user
      operationId: createUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'

  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid

    get:
      summary: Get user by ID
      operationId: getUser
      tags:
        - Users
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    put:
      summary: Update user
      operationId: updateUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete user
      operationId: deleteUser
      tags:
        - Users
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'
```

---

## Components (Schemas)

### Data Models

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [admin, user, guest]
          default: user
        isActive:
          type: boolean
          default: true
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true

    CreateUserRequest:
      type: object
      required:
        - email
      properties:
        email:
          type: string
          format: email
        name:
          type: string
        password:
          type: string
          format: password
          minLength: 8
          writeOnly: true

    UpdateUserRequest:
      type: object
      properties:
        name:
          type: string
        role:
          type: string
          enum: [admin, user, guest]

    Pagination:
      type: object
      properties:
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer
        hasMore:
          type: boolean

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
```

### Reusable Responses

```yaml
components:
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: BAD_REQUEST
            message: Invalid request parameters

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required

    Forbidden:
      description: Forbidden
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: FORBIDDEN
            message: Insufficient permissions

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: Resource not found

    Conflict:
      description: Conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: CONFLICT
            message: Resource already exists

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: INTERNAL_ERROR
            message: An unexpected error occurred
```

---

## Security Schemes

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

    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          scopes:
            read:users: Read user information
            write:users: Modify user information
            admin: Full administrative access

    BasicAuth:
      type: http
      scheme: basic

# Apply globally
security:
  - BearerAuth: []

# Or per-operation
paths:
  /public:
    get:
      security: []  # No auth required
  /admin:
    get:
      security:
        - BearerAuth: []
        - OAuth2: [admin]
```

---

## Advanced Features

### File Uploads

```yaml
paths:
  /upload:
    post:
      summary: Upload file
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
                description:
                  type: string
      responses:
        '200':
          description: File uploaded
          content:
            application/json:
              schema:
                type: object
                properties:
                  fileId:
                    type: string
                  url:
                    type: string
                    format: uri
```

### Webhooks (OpenAPI 3.1)

```yaml
webhooks:
  userCreated:
    post:
      summary: User created webhook
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                event:
                  type: string
                  const: user.created
                data:
                  $ref: '#/components/schemas/User'
      responses:
        '200':
          description: Webhook processed
```

### Polymorphism

```yaml
components:
  schemas:
    Pet:
      oneOf:
        - $ref: '#/components/schemas/Dog'
        - $ref: '#/components/schemas/Cat'
      discriminator:
        propertyName: petType
        mapping:
          dog: '#/components/schemas/Dog'
          cat: '#/components/schemas/Cat'

    Dog:
      type: object
      properties:
        petType:
          type: string
        breed:
          type: string
        barkVolume:
          type: integer

    Cat:
      type: object
      properties:
        petType:
          type: string
        breed:
          type: string
        meowPitch:
          type: integer
```

---

## Tools & CLI Commands

### Swagger CLI

```bash
# Install
npm install -g @apidevtools/swagger-cli

# Validate spec
swagger-cli validate api.yaml

# Bundle multiple files
swagger-cli bundle api.yaml -o bundled.yaml

# Convert to JSON
swagger-cli bundle api.yaml -o api.json -t json
```

### OpenAPI Generator

```bash
# Install
npm install -g @openapitools/openapi-generator-cli

# Generate TypeScript client
openapi-generator-cli generate \
  -i api.yaml \
  -g typescript-axios \
  -o ./generated/client

# Generate Python client
openapi-generator-cli generate \
  -i api.yaml \
  -g python \
  -o ./generated/python-client

# Generate server stub (Node.js Express)
openapi-generator-cli generate \
  -i api.yaml \
  -g nodejs-express-server \
  -o ./generated/server

# List available generators
openapi-generator-cli list

# Common generators:
# typescript-axios, typescript-fetch, python, java, go, csharp
# nodejs-express-server, python-flask, spring, go-server
```

### Spectral (Linting)

```bash
# Install
npm install -g @stoplight/spectral-cli

# Lint spec
spectral lint api.yaml

# Custom ruleset (.spectral.yaml)
extends: spectral:oas
rules:
  operation-operationId: error
  operation-tags: error
  info-contact: warn
```

### Prism (Mock Server)

```bash
# Install
npm install -g @stoplight/prism-cli

# Start mock server
prism mock api.yaml

# With dynamic responses
prism mock api.yaml --dynamic

# Proxy mode (validate against real server)
prism proxy api.yaml https://api.example.com
```

---

## Swagger UI / Redoc

### Docker Swagger UI

```yaml
# docker-compose.yml
services:
  swagger-ui:
    image: swaggerapi/swagger-ui
    ports:
      - "8080:8080"
    environment:
      - SWAGGER_JSON=/api/openapi.yaml
    volumes:
      - ./api.yaml:/api/openapi.yaml
```

### Redoc

```html
<!-- Static HTML -->
<!DOCTYPE html>
<html>
<head>
  <title>API Documentation</title>
  <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
  <style>body { margin: 0; padding: 0; }</style>
</head>
<body>
  <redoc spec-url='./api.yaml'></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

```bash
# CLI
npm install -g @redocly/cli
redocly build-docs api.yaml -o docs.html
redocly preview-docs api.yaml
```

---

## Code Generation Examples

### TypeScript Types

```typescript
// Generated from OpenAPI spec
export interface User {
  id: string;
  email: string;
  name?: string;
  role: 'admin' | 'user' | 'guest';
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateUserRequest {
  email: string;
  name?: string;
  password: string;
}

export interface ApiResponse<T> {
  data: T;
  pagination?: Pagination;
}
```

### API Client Usage

```typescript
import { UsersApi, Configuration } from './generated/client';

const config = new Configuration({
  basePath: 'https://api.example.com/v1',
  accessToken: 'your-jwt-token'
});

const usersApi = new UsersApi(config);

// List users
const users = await usersApi.listUsers({ limit: 10 });

// Create user
const newUser = await usersApi.createUser({
  createUserRequest: {
    email: 'user@example.com',
    name: 'John Doe',
    password: 'securepassword'
  }
});

// Get user
const user = await usersApi.getUser({ userId: 'uuid-here' });
```

---

## Best Practices

1. **Use semantic versioning** for API versions
2. **Define reusable components** (schemas, responses, parameters)
3. **Include examples** for all schemas and responses
4. **Use operationId** for code generation
5. **Tag operations** for logical grouping
6. **Document all error responses**
7. **Use $ref** to avoid duplication
8. **Validate specs** before publishing
9. **Version control** your API specs
10. **Generate SDKs** for consistent client implementations
