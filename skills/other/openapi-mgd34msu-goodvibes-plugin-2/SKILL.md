---
name: openapi
description: Defines and generates OpenAPI 3.1 specifications with TypeScript type generation, validation, and documentation. Use when documenting APIs, generating client SDKs, or implementing contract-first API design.
---

# OpenAPI

OpenAPI Specification (OAS) is a standard for describing REST APIs. It enables documentation, code generation, and validation.

## Quick Start

### OpenAPI Document

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: A sample API

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:3000/v1
    description: Development

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
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
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserInput'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'

  /users/{id}:
    get:
      summary: Get user by ID
      operationId: getUser
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/UserIdParam'
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, email, createdAt]
      properties:
        id:
          type: string
          example: usr_abc123
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time

    CreateUserInput:
      type: object
      required: [email]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100

    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer

    Error:
      type: object
      required: [error, message]
      properties:
        error:
          type: string
        message:
          type: string

  parameters:
    UserIdParam:
      name: id
      in: path
      required: true
      schema:
        type: string

    PageParam:
      name: page
      in: query
      schema:
        type: integer
        default: 1

    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        default: 20
        maximum: 100

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

## TypeScript Type Generation

### Using openapi-typescript

```bash
npm install -D openapi-typescript
npx openapi-typescript ./openapi.yaml -o ./types/api.d.ts
```

### Generated Types

```typescript
// types/api.d.ts (generated)
export interface paths {
  "/users": {
    get: operations["listUsers"];
    post: operations["createUser"];
  };
  "/users/{id}": {
    get: operations["getUser"];
  };
}

export interface components {
  schemas: {
    User: {
      id: string;
      email: string;
      name?: string;
      createdAt: string;
    };
    CreateUserInput: {
      email: string;
      name?: string;
    };
  };
}

export interface operations {
  listUsers: {
    parameters: {
      query?: {
        page?: number;
        limit?: number;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": {
            data: components["schemas"]["User"][];
            pagination: components["schemas"]["Pagination"];
          };
        };
      };
    };
  };
}
```

### Type-Safe Fetch Client

```bash
npm install openapi-fetch
```

```typescript
import createClient from 'openapi-fetch'
import type { paths } from './types/api'

const client = createClient<paths>({
  baseUrl: 'https://api.example.com/v1',
  headers: {
    Authorization: `Bearer ${token}`
  }
})

// Fully typed request and response
const { data, error } = await client.GET('/users', {
  params: {
    query: { page: 1, limit: 20 }
  }
})

// data is typed as { data: User[], pagination: Pagination }

const { data: user } = await client.POST('/users', {
  body: {
    email: 'user@example.com',
    name: 'John'
  }
})

// user is typed as User
```

## Schema Validation

### Using Zod with OpenAPI

```bash
npm install zod @anatine/zod-openapi
```

```typescript
import { z } from 'zod'
import { extendZodWithOpenApi } from '@anatine/zod-openapi'

extendZodWithOpenApi(z)

const UserSchema = z.object({
  id: z.string().openapi({ example: 'usr_abc123' }),
  email: z.string().email(),
  name: z.string().optional(),
  createdAt: z.string().datetime()
}).openapi('User')

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100).optional()
}).openapi('CreateUserInput')
```

### Generate OpenAPI from Zod

```typescript
import { generateOpenApi } from '@anatine/zod-openapi'

const document = generateOpenApi({
  info: {
    title: 'My API',
    version: '1.0.0'
  },
  paths: {
    '/users': {
      post: {
        requestBody: {
          content: {
            'application/json': { schema: CreateUserSchema }
          }
        },
        responses: {
          201: {
            content: {
              'application/json': { schema: UserSchema }
            }
          }
        }
      }
    }
  }
})
```

## Request Validation

### Express Middleware

```bash
npm install express-openapi-validator
```

```typescript
import express from 'express'
import * as OpenApiValidator from 'express-openapi-validator'

const app = express()

app.use(express.json())

app.use(
  OpenApiValidator.middleware({
    apiSpec: './openapi.yaml',
    validateRequests: true,
    validateResponses: true
  })
)

// Routes are automatically validated against the spec
app.post('/users', (req, res) => {
  // req.body is validated against CreateUserInput schema
  const user = createUser(req.body)
  res.status(201).json(user)
})

// Error handler for validation errors
app.use((err, req, res, next) => {
  if (err.status === 400) {
    return res.status(400).json({
      error: 'VALIDATION_ERROR',
      message: err.message,
      details: err.errors
    })
  }
  next(err)
})
```

## Documentation UI

### Swagger UI

```bash
npm install swagger-ui-express
```

```typescript
import swaggerUi from 'swagger-ui-express'
import YAML from 'yamljs'

const openApiDocument = YAML.load('./openapi.yaml')

app.use('/docs', swaggerUi.serve, swaggerUi.setup(openApiDocument, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'My API Docs'
}))
```

### Redoc

```typescript
import express from 'express'

app.get('/docs', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>API Docs</title>
        <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">
        <style>body { margin: 0; padding: 0; }</style>
      </head>
      <body>
        <redoc spec-url='/openapi.yaml'></redoc>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
      </body>
    </html>
  `)
})

app.get('/openapi.yaml', (req, res) => {
  res.sendFile('./openapi.yaml', { root: __dirname })
})
```

## Code Generation

### Generate API Client

```bash
# Using openapi-generator
npm install -g @openapitools/openapi-generator-cli

openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./generated/client

# Using openapi-typescript-codegen
npm install -D openapi-typescript-codegen

npx openapi-typescript-codegen \
  --input ./openapi.yaml \
  --output ./generated/client \
  --client fetch
```

### Generate Server Stubs

```bash
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-express-server \
  -o ./generated/server
```

## Advanced Patterns

### Discriminated Unions

```yaml
components:
  schemas:
    Event:
      oneOf:
        - $ref: '#/components/schemas/UserCreatedEvent'
        - $ref: '#/components/schemas/UserDeletedEvent'
      discriminator:
        propertyName: type
        mapping:
          user.created: '#/components/schemas/UserCreatedEvent'
          user.deleted: '#/components/schemas/UserDeletedEvent'

    UserCreatedEvent:
      type: object
      required: [type, user]
      properties:
        type:
          type: string
          enum: [user.created]
        user:
          $ref: '#/components/schemas/User'

    UserDeletedEvent:
      type: object
      required: [type, userId]
      properties:
        type:
          type: string
          enum: [user.deleted]
        userId:
          type: string
```

### Nullable Fields (3.1)

```yaml
# OpenAPI 3.1 uses JSON Schema null type
name:
  type: ['string', 'null']

# With oneOf
name:
  oneOf:
    - type: string
    - type: 'null'
```

### File Uploads

```yaml
/upload:
  post:
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
```

### Webhooks (3.1)

```yaml
webhooks:
  orderCreated:
    post:
      summary: Order created webhook
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/OrderEvent'
      responses:
        '200':
          description: Webhook processed
```

## Best Practices

1. **Use $ref** - Reuse schemas, parameters, responses
2. **Version your API** - Include in path or server URL
3. **Document errors** - Define all error responses
4. **Add examples** - Include realistic example values
5. **Use operationId** - Required for code generation
6. **Validate requests and responses** - Catch bugs early
7. **Keep spec in sync** - Generate from code or validate against it
8. **Use tags** - Organize endpoints by domain

## References

- [Schema Patterns](references/schema-patterns.md)
- [Code Generation](references/code-generation.md)
