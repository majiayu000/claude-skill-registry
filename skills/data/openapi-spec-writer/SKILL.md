---
name: openapi-spec-writer
description: Expert in writing OpenAPI 3.0/3.1 specifications for REST APIs. Specializes in schema design, documentation best practices, API-first development, and tooling integration. Generates comprehensive API documentation that serves as both documentation and contract.
version: 1.0.0
category: documentation
tags: [openapi, swagger, api-documentation, rest, api-design]
---

# OpenAPI Spec Writer

## Overview

Expert in writing OpenAPI 3.0/3.1 specifications for REST APIs. Specializes in schema design, documentation best practices, API-first development, and tooling integration. Generates comprehensive API documentation that serves as both documentation and contract.

## When to Use

- Creating OpenAPI specifications for new APIs
- Documenting existing REST APIs
- Designing API contracts before implementation
- Generating client SDKs from specs
- Setting up interactive API documentation (Swagger UI, Redoc)
- Validating API responses against schemas
- Migrating from OpenAPI 2.0 (Swagger) to 3.x

## Capabilities

### Specification Writing
- OpenAPI 3.0 and 3.1 syntax
- Path and operation definitions
- Request/response schemas
- Authentication schemes
- Server configurations

### Schema Design
- JSON Schema with OpenAPI extensions
- Reusable component schemas
- Discriminators for polymorphism
- oneOf, anyOf, allOf composition
- Nullable types and defaults

### Documentation Quality
- Meaningful descriptions and examples
- Markdown in descriptions
- Request/response examples
- Error response documentation
- Deprecation notices

### Tooling Integration
- Swagger UI configuration
- Redoc customization
- Spectral linting rules
- SDK generation setup
- Mock server configuration

## Dependencies

Works well with:
- `api-architect` - API design patterns
- `rest-api-design` - RESTful conventions
- `typescript-pro` - Generated client types
- `github-actions-pipeline-builder` - CI validation

## Examples

### Complete OpenAPI 3.1 Spec
```yaml
openapi: 3.1.0
info:
  title: Task Management API
  description: |
    RESTful API for managing tasks and projects.

    ## Authentication
    All endpoints require a Bearer token in the Authorization header.

    ## Rate Limiting
    - 1000 requests per hour per API key
    - Rate limit headers included in all responses
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com
    url: https://docs.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
  - url: http://localhost:3000/v1
    description: Local development

tags:
  - name: Tasks
    description: Task management operations
  - name: Projects
    description: Project management operations

paths:
  /tasks:
    get:
      operationId: listTasks
      summary: List all tasks
      description: Returns a paginated list of tasks with optional filtering.
      tags:
        - Tasks
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
        - name: status
          in: query
          description: Filter by task status
          schema:
            $ref: '#/components/schemas/TaskStatus'
        - name: project_id
          in: query
          description: Filter by project ID
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskListResponse'
              examples:
                default:
                  $ref: '#/components/examples/TaskListExample'
          headers:
            X-Total-Count:
              schema:
                type: integer
              description: Total number of tasks matching the query
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      operationId: createTask
      summary: Create a new task
      description: Creates a new task and returns the created resource.
      tags:
        - Tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskRequest'
            examples:
              minimal:
                summary: Minimal task
                value:
                  title: "Complete documentation"
              full:
                summary: Full task with all fields
                value:
                  title: "Complete documentation"
                  description: "Write API docs for v1.0"
                  project_id: "550e8400-e29b-41d4-a716-446655440000"
                  due_date: "2024-12-31"
                  priority: "high"
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
          headers:
            Location:
              schema:
                type: string
                format: uri
              description: URL of the created resource
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/ValidationError'

  /tasks/{taskId}:
    parameters:
      - $ref: '#/components/parameters/TaskIdParam'

    get:
      operationId: getTask
      summary: Get a task by ID
      tags:
        - Tasks
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      operationId: updateTask
      summary: Update a task
      description: Partially updates a task. Only provided fields are updated.
      tags:
        - Tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateTaskRequest'
      responses:
        '200':
          description: Task updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '404':
          $ref: '#/components/responses/NotFound'
        '422':
          $ref: '#/components/responses/ValidationError'

    delete:
      operationId: deleteTask
      summary: Delete a task
      tags:
        - Tasks
      responses:
        '204':
          description: Task deleted successfully
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login

  parameters:
    TaskIdParam:
      name: taskId
      in: path
      required: true
      description: Unique task identifier
      schema:
        type: string
        format: uuid
      example: "550e8400-e29b-41d4-a716-446655440000"

    PageParam:
      name: page
      in: query
      description: Page number for pagination (1-indexed)
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: Number of items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  schemas:
    Task:
      type: object
      required:
        - id
        - title
        - status
        - created_at
        - updated_at
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
          readOnly: true
        title:
          type: string
          minLength: 1
          maxLength: 200
          description: Task title
        description:
          type: string
          maxLength: 5000
          description: Detailed task description (supports Markdown)
        status:
          $ref: '#/components/schemas/TaskStatus'
        priority:
          $ref: '#/components/schemas/Priority'
        project_id:
          type: string
          format: uuid
          description: Associated project ID
        due_date:
          type: string
          format: date
          description: Due date (ISO 8601)
        created_at:
          type: string
          format: date-time
          readOnly: true
        updated_at:
          type: string
          format: date-time
          readOnly: true

    TaskStatus:
      type: string
      enum:
        - pending
        - in_progress
        - completed
        - cancelled
      description: Current task status
      default: pending

    Priority:
      type: string
      enum:
        - low
        - medium
        - high
        - urgent
      default: medium

    CreateTaskRequest:
      type: object
      required:
        - title
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 5000
        project_id:
          type: string
          format: uuid
        due_date:
          type: string
          format: date
        priority:
          $ref: '#/components/schemas/Priority'

    UpdateTaskRequest:
      type: object
      minProperties: 1
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 5000
        status:
          $ref: '#/components/schemas/TaskStatus'
        priority:
          $ref: '#/components/schemas/Priority'
        due_date:
          type: string
          format: date

    TaskListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Task'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required:
        - page
        - limit
        - total
        - total_pages
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        total_pages:
          type: integer
        has_next:
          type: boolean
        has_prev:
          type: boolean

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Machine-readable error code
        message:
          type: string
          description: Human-readable error message
        details:
          type: object
          additionalProperties: true
          description: Additional error details

    ValidationError:
      allOf:
        - $ref: '#/components/schemas/Error'
        - type: object
          properties:
            errors:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string

  responses:
    BadRequest:
      description: Bad request - invalid parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "BAD_REQUEST"
            message: "Invalid query parameters"

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "UNAUTHORIZED"
            message: "Invalid or expired token"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: "NOT_FOUND"
            message: "Task not found"

    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ValidationError'
          example:
            code: "VALIDATION_ERROR"
            message: "Request validation failed"
            errors:
              - field: "title"
                message: "Title is required"

  examples:
    TaskListExample:
      value:
        data:
          - id: "550e8400-e29b-41d4-a716-446655440000"
            title: "Complete documentation"
            status: "in_progress"
            priority: "high"
            created_at: "2024-01-15T10:30:00Z"
            updated_at: "2024-01-15T10:30:00Z"
        pagination:
          page: 1
          limit: 20
          total: 42
          total_pages: 3
          has_next: true
          has_prev: false

security:
  - bearerAuth: []
```

### Polymorphic Schemas (Discriminator)
```yaml
components:
  schemas:
    Notification:
      type: object
      required:
        - id
        - type
        - created_at
      discriminator:
        propertyName: type
        mapping:
          email: '#/components/schemas/EmailNotification'
          sms: '#/components/schemas/SmsNotification'
          push: '#/components/schemas/PushNotification'
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
          enum: [email, sms, push]
        created_at:
          type: string
          format: date-time

    EmailNotification:
      allOf:
        - $ref: '#/components/schemas/Notification'
        - type: object
          required:
            - to
            - subject
          properties:
            to:
              type: string
              format: email
            subject:
              type: string
            body:
              type: string

    SmsNotification:
      allOf:
        - $ref: '#/components/schemas/Notification'
        - type: object
          required:
            - phone_number
            - message
          properties:
            phone_number:
              type: string
              pattern: '^\+[1-9]\d{1,14}$'
            message:
              type: string
              maxLength: 160
```

### Spectral Linting Rules
```yaml
# .spectral.yaml
extends: ["spectral:oas"]

rules:
  # Enforce operation IDs
  operation-operationId: error

  # Require descriptions
  operation-description: error
  oas3-schema-description: warn

  # Naming conventions
  path-casing:
    given: "$.paths[*]~"
    then:
      function: casing
      functionOptions:
        type: kebab

  # Security requirements
  operation-security-defined: error

  # Response codes
  operation-success-response: error

  # Custom: require examples
  require-examples:
    message: "Responses should have examples"
    given: "$.paths.*.*.responses.*.content.*.schema"
    then:
      field: example
      function: truthy
```

## Best Practices

1. **Use components** - Extract reusable schemas, parameters, responses
2. **Provide examples** - Real-world examples for every schema
3. **Meaningful descriptions** - Markdown-formatted, explain business context
4. **Consistent naming** - kebab-case paths, camelCase properties
5. **Version your API** - Include version in URL or header
6. **Document errors** - Define all error responses with examples
7. **Use operationId** - Unique, descriptive IDs for SDK generation
8. **Validate with linting** - Use Spectral to enforce standards
9. **Keep spec in sync** - Automate validation in CI

## Common Pitfalls

- **Missing required fields** - Forgetting to mark fields as required
- **Inconsistent naming** - Mixing snake_case and camelCase
- **Generic descriptions** - "Returns data" instead of specific details
- **No examples** - Makes spec hard to understand
- **Outdated spec** - Spec doesn't match implementation
- **Overusing anyOf** - Makes schemas hard to understand
- **Missing error responses** - Only documenting happy path
- **No pagination** - List endpoints without pagination info
