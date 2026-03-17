---
name: openapi-documentation
description: Эксперт по OpenAPI документации. Используй для создания Swagger спецификаций, API schemas и автогенерации документации.
---

# OpenAPI Documentation Expert

Expert in creating comprehensive OpenAPI/Swagger specifications and API documentation aligned with OpenAPI 3.0+ standards.

## Core Principles

### Specification Standards
- Use OpenAPI 3.0.3 or 3.1.0
- Consistent naming conventions (kebab-case for paths, camelCase for properties)
- Organize endpoints through tags
- Maintain reusable component schemas
- Document all response codes

### Documentation Quality
- Provide business logic context
- Include extensive realistic examples
- Document all error scenarios
- Define rate-limiting specifications
- Explicit data format definitions

## OpenAPI 3.0 Structure

### Basic Specification

```yaml
openapi: "3.0.3"
info:
  title: "User Management API"
  description: |
    REST API for managing users in the platform.

    ## Authentication
    All endpoints require Bearer token authentication.

    ## Rate Limiting
    - Standard: 100 requests/minute
    - Premium: 1000 requests/minute

    ## Versioning
    API version is included in the URL path (/v1/).
  version: "1.0.0"
  contact:
    name: "API Support"
    email: "api-support@example.com"
    url: "https://developer.example.com/support"
  license:
    name: "Apache 2.0"
    url: "https://www.apache.org/licenses/LICENSE-2.0"
  termsOfService: "https://example.com/terms"

servers:
  - url: "https://api.example.com/v1"
    description: "Production server"
  - url: "https://staging-api.example.com/v1"
    description: "Staging server"
  - url: "http://localhost:3000/v1"
    description: "Development server"

tags:
  - name: "users"
    description: "User management operations"
  - name: "authentication"
    description: "Authentication and authorization"
  - name: "admin"
    description: "Administrative operations"

security:
  - bearerAuth: []
```

### Path Documentation

```yaml
paths:
  /users:
    get:
      operationId: "listUsers"
      tags:
        - "users"
      summary: "List all users"
      description: |
        Retrieve a paginated list of users.

        Results can be filtered by status and sorted by various fields.
        Pagination is cursor-based for optimal performance.
      parameters:
        - $ref: "#/components/parameters/PageSize"
        - $ref: "#/components/parameters/PageCursor"
        - name: "status"
          in: "query"
          description: "Filter by user status"
          required: false
          schema:
            type: "string"
            enum: ["active", "inactive", "pending"]
            default: "active"
        - name: "sort"
          in: "query"
          description: "Sort field and direction"
          required: false
          schema:
            type: "string"
            enum: ["created_at:asc", "created_at:desc", "name:asc", "name:desc"]
            default: "created_at:desc"
      responses:
        "200":
          description: "Successful response"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserListResponse"
              examples:
                success:
                  $ref: "#/components/examples/UserListSuccess"
          headers:
            X-RateLimit-Limit:
              $ref: "#/components/headers/X-RateLimit-Limit"
            X-RateLimit-Remaining:
              $ref: "#/components/headers/X-RateLimit-Remaining"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
        "429":
          $ref: "#/components/responses/TooManyRequests"

    post:
      operationId: "createUser"
      tags:
        - "users"
      summary: "Create a new user"
      description: |
        Create a new user account.

        A verification email will be sent to the provided email address.
        The user must verify their email before they can log in.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUserRequest"
            examples:
              basic:
                summary: "Basic user creation"
                value:
                  email: "user@example.com"
                  name: "John Doe"
                  password: "SecurePassword123!"
              withProfile:
                summary: "User with profile data"
                value:
                  email: "user@example.com"
                  name: "John Doe"
                  password: "SecurePassword123!"
                  profile:
                    bio: "Software developer"
                    location: "San Francisco, CA"
      responses:
        "201":
          description: "User created successfully"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
              example:
                id: "usr_1234567890"
                email: "user@example.com"
                name: "John Doe"
                status: "pending"
                createdAt: "2024-03-15T10:30:00Z"
          headers:
            Location:
              description: "URL of the created user"
              schema:
                type: "string"
                format: "uri"
                example: "/users/usr_1234567890"
        "400":
          $ref: "#/components/responses/BadRequest"
        "409":
          description: "User already exists"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
              example:
                code: "USER_EXISTS"
                message: "A user with this email already exists"
        "422":
          $ref: "#/components/responses/ValidationError"

  /users/{userId}:
    parameters:
      - $ref: "#/components/parameters/UserId"

    get:
      operationId: "getUser"
      tags:
        - "users"
      summary: "Get user by ID"
      description: "Retrieve detailed information about a specific user"
      responses:
        "200":
          description: "Successful response"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          $ref: "#/components/responses/NotFound"

    patch:
      operationId: "updateUser"
      tags:
        - "users"
      summary: "Update user"
      description: |
        Partially update a user's information.

        Only the fields provided in the request body will be updated.
        To remove a field, set it to null explicitly.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateUserRequest"
      responses:
        "200":
          description: "User updated successfully"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "400":
          $ref: "#/components/responses/BadRequest"
        "404":
          $ref: "#/components/responses/NotFound"

    delete:
      operationId: "deleteUser"
      tags:
        - "users"
      summary: "Delete user"
      description: |
        Permanently delete a user account.

        This action cannot be undone. All associated data will be removed.
      responses:
        "204":
          description: "User deleted successfully"
        "404":
          $ref: "#/components/responses/NotFound"
```

### Components

```yaml
components:
  schemas:
    User:
      type: "object"
      description: "User account information"
      required:
        - "id"
        - "email"
        - "name"
        - "status"
        - "createdAt"
      properties:
        id:
          type: "string"
          description: "Unique user identifier"
          pattern: "^usr_[a-zA-Z0-9]{10}$"
          example: "usr_1234567890"
          readOnly: true
        email:
          type: "string"
          format: "email"
          description: "User's email address"
          example: "user@example.com"
        name:
          type: "string"
          description: "User's display name"
          minLength: 1
          maxLength: 100
          example: "John Doe"
        status:
          type: "string"
          description: "Account status"
          enum: ["active", "inactive", "pending", "suspended"]
          example: "active"
        profile:
          $ref: "#/components/schemas/UserProfile"
        createdAt:
          type: "string"
          format: "date-time"
          description: "Account creation timestamp"
          readOnly: true
          example: "2024-03-15T10:30:00Z"
        updatedAt:
          type: "string"
          format: "date-time"
          description: "Last update timestamp"
          readOnly: true
          example: "2024-03-15T10:30:00Z"

    UserProfile:
      type: "object"
      description: "Extended user profile information"
      properties:
        bio:
          type: "string"
          description: "User biography"
          maxLength: 500
          example: "Software developer passionate about APIs"
        location:
          type: "string"
          description: "User's location"
          maxLength: 100
          example: "San Francisco, CA"
        avatarUrl:
          type: "string"
          format: "uri"
          description: "URL to user's avatar image"
          example: "https://cdn.example.com/avatars/usr_123.jpg"
        timezone:
          type: "string"
          description: "User's timezone"
          example: "America/Los_Angeles"

    CreateUserRequest:
      type: "object"
      description: "Request body for creating a new user"
      required:
        - "email"
        - "name"
        - "password"
      properties:
        email:
          type: "string"
          format: "email"
          description: "User's email address"
          example: "user@example.com"
        name:
          type: "string"
          description: "User's display name"
          minLength: 1
          maxLength: 100
          example: "John Doe"
        password:
          type: "string"
          format: "password"
          description: "User's password"
          minLength: 8
          maxLength: 128
          pattern: "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$"
          example: "SecurePassword123!"
        profile:
          $ref: "#/components/schemas/UserProfile"

    UpdateUserRequest:
      type: "object"
      description: "Request body for updating a user"
      properties:
        name:
          type: "string"
          description: "User's display name"
          minLength: 1
          maxLength: 100
          nullable: true
        profile:
          $ref: "#/components/schemas/UserProfile"

    UserListResponse:
      type: "object"
      description: "Paginated list of users"
      required:
        - "data"
        - "pagination"
      properties:
        data:
          type: "array"
          items:
            $ref: "#/components/schemas/User"
        pagination:
          $ref: "#/components/schemas/Pagination"

    Pagination:
      type: "object"
      description: "Pagination metadata"
      required:
        - "total"
        - "hasMore"
      properties:
        total:
          type: "integer"
          description: "Total number of items"
          example: 150
        hasMore:
          type: "boolean"
          description: "Whether more items exist"
          example: true
        nextCursor:
          type: "string"
          description: "Cursor for next page"
          example: "eyJpZCI6MTAwfQ=="
        prevCursor:
          type: "string"
          description: "Cursor for previous page"
          example: "eyJpZCI6NTB9"

    Error:
      type: "object"
      description: "Error response"
      required:
        - "code"
        - "message"
      properties:
        code:
          type: "string"
          description: "Machine-readable error code"
          example: "VALIDATION_ERROR"
        message:
          type: "string"
          description: "Human-readable error message"
          example: "The request body is invalid"
        details:
          type: "array"
          description: "Detailed error information"
          items:
            type: "object"
            properties:
              field:
                type: "string"
                description: "Field that caused the error"
                example: "email"
              message:
                type: "string"
                description: "Error message for this field"
                example: "Must be a valid email address"
        requestId:
          type: "string"
          description: "Request ID for support"
          example: "req_abc123xyz"
        timestamp:
          type: "string"
          format: "date-time"
          description: "Error timestamp"
          example: "2024-03-15T10:30:00Z"

  parameters:
    UserId:
      name: "userId"
      in: "path"
      description: "User ID"
      required: true
      schema:
        type: "string"
        pattern: "^usr_[a-zA-Z0-9]{10}$"
      example: "usr_1234567890"

    PageSize:
      name: "limit"
      in: "query"
      description: "Number of items per page"
      required: false
      schema:
        type: "integer"
        minimum: 1
        maximum: 100
        default: 20

    PageCursor:
      name: "cursor"
      in: "query"
      description: "Pagination cursor"
      required: false
      schema:
        type: "string"

  headers:
    X-RateLimit-Limit:
      description: "Request limit per minute"
      schema:
        type: "integer"
      example: 100

    X-RateLimit-Remaining:
      description: "Remaining requests in current window"
      schema:
        type: "integer"
      example: 95

    X-RateLimit-Reset:
      description: "Unix timestamp when limit resets"
      schema:
        type: "integer"
      example: 1710500000

  responses:
    BadRequest:
      description: "Bad request"
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: "BAD_REQUEST"
            message: "The request could not be processed"
            requestId: "req_abc123xyz"

    Unauthorized:
      description: "Authentication required"
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: "UNAUTHORIZED"
            message: "Authentication credentials are missing or invalid"

    NotFound:
      description: "Resource not found"
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: "NOT_FOUND"
            message: "The requested resource was not found"

    ValidationError:
      description: "Validation error"
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: "VALIDATION_ERROR"
            message: "Request validation failed"
            details:
              - field: "email"
                message: "Must be a valid email address"
              - field: "password"
                message: "Must be at least 8 characters"

    TooManyRequests:
      description: "Rate limit exceeded"
      headers:
        Retry-After:
          description: "Seconds until rate limit resets"
          schema:
            type: "integer"
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
          example:
            code: "RATE_LIMIT_EXCEEDED"
            message: "Too many requests. Please try again later."

  securitySchemes:
    bearerAuth:
      type: "http"
      scheme: "bearer"
      bearerFormat: "JWT"
      description: |
        JWT authentication token.

        Include in the Authorization header:
        `Authorization: Bearer <token>`

        Tokens expire after 1 hour. Use the refresh token endpoint
        to obtain a new access token.

    apiKey:
      type: "apiKey"
      in: "header"
      name: "X-API-Key"
      description: "API key for server-to-server communication"

  examples:
    UserListSuccess:
      summary: "Successful user list"
      value:
        data:
          - id: "usr_1234567890"
            email: "user1@example.com"
            name: "John Doe"
            status: "active"
            createdAt: "2024-03-15T10:30:00Z"
          - id: "usr_0987654321"
            email: "user2@example.com"
            name: "Jane Smith"
            status: "active"
            createdAt: "2024-03-14T09:00:00Z"
        pagination:
          total: 150
          hasMore: true
          nextCursor: "eyJpZCI6MTAwfQ=="
```

## Advanced Features

### Webhooks (OpenAPI 3.1)

```yaml
webhooks:
  userCreated:
    post:
      operationId: "userCreatedWebhook"
      summary: "User created event"
      description: |
        Triggered when a new user account is created.

        Your endpoint must respond with a 2xx status code within 30 seconds.
        Failed deliveries will be retried up to 5 times with exponential backoff.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: "object"
              required:
                - "event"
                - "timestamp"
                - "data"
              properties:
                event:
                  type: "string"
                  const: "user.created"
                timestamp:
                  type: "string"
                  format: "date-time"
                data:
                  $ref: "#/components/schemas/User"
      responses:
        "200":
          description: "Webhook received successfully"
      security:
        - webhookSignature: []

  userUpdated:
    post:
      operationId: "userUpdatedWebhook"
      summary: "User updated event"
      description: "Triggered when a user's information is modified"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: "object"
              properties:
                event:
                  type: "string"
                  const: "user.updated"
                timestamp:
                  type: "string"
                  format: "date-time"
                data:
                  type: "object"
                  properties:
                    user:
                      $ref: "#/components/schemas/User"
                    changes:
                      type: "object"
                      description: "Fields that were changed"
      responses:
        "200":
          description: "Webhook received successfully"
```

### Custom Extensions

```yaml
x-code-samples:
  - lang: "curl"
    label: "cURL"
    source: |
      curl -X GET "https://api.example.com/v1/users" \
        -H "Authorization: Bearer your_token_here" \
        -H "Accept: application/json"

  - lang: "javascript"
    label: "JavaScript"
    source: |
      const response = await fetch('https://api.example.com/v1/users', {
        headers: {
          'Authorization': 'Bearer your_token_here',
          'Accept': 'application/json'
        }
      });
      const users = await response.json();

  - lang: "python"
    label: "Python"
    source: |
      import requests

      response = requests.get(
          'https://api.example.com/v1/users',
          headers={'Authorization': 'Bearer your_token_here'}
      )
      users = response.json()

x-rate-limiting:
  standard:
    limit: 100
    window: "1 minute"
  premium:
    limit: 1000
    window: "1 minute"

x-changelog:
  - version: "1.0.0"
    date: "2024-03-15"
    changes:
      - "Initial release"
  - version: "1.1.0"
    date: "2024-04-01"
    changes:
      - "Added user profile endpoints"
      - "Added pagination support"
```

## Validation & Quality

### Schema Validation Rules

```yaml
validation_patterns:
  strings:
    email:
      format: "email"
      maxLength: 254

    uuid:
      format: "uuid"
      pattern: "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"

    phone:
      pattern: "^\\+[1-9]\\d{1,14}$"

    url:
      format: "uri"
      pattern: "^https?://"

  numbers:
    positive_integer:
      type: "integer"
      minimum: 1

    percentage:
      type: "number"
      minimum: 0
      maximum: 100

    currency:
      type: "number"
      multipleOf: 0.01
      minimum: 0

  dates:
    date_only:
      type: "string"
      format: "date"
      pattern: "^\\d{4}-\\d{2}-\\d{2}$"

    datetime:
      type: "string"
      format: "date-time"

  arrays:
    non_empty_array:
      type: "array"
      minItems: 1

    unique_array:
      type: "array"
      uniqueItems: true
```

### Linting Configuration

```yaml
# .spectral.yaml
extends: ["spectral:oas"]

rules:
  # Naming conventions
  operation-operationId-valid-in-url: true
  path-keys-no-trailing-slash: true

  # Documentation requirements
  operation-description: true
  operation-tag-defined: true
  info-contact: true

  # Schema quality
  oas3-schema: true
  typed-enum: true

  # Custom rules
  operation-summary-length:
    description: "Operation summary should be concise"
    severity: warn
    given: "$.paths.*[get,post,put,patch,delete]"
    then:
      field: "summary"
      function: length
      functionOptions:
        max: 80

  must-have-examples:
    description: "Responses should have examples"
    severity: warn
    given: "$.paths.*.*.responses.*.content.*"
    then:
      field: "examples"
      function: truthy
```

## Code Generation

### Generator Configuration

```yaml
# openapi-generator-cli.yaml
$schema: https://raw.githubusercontent.com/OpenAPITools/openapi-generator-cli/master/schema.json

spaces: 2

generators:
  typescript-axios:
    inputSpec: ./api/openapi.yaml
    output: ./generated/typescript-client
    generatorName: typescript-axios
    additionalProperties:
      npmName: "@example/api-client"
      supportsES6: true
      withInterfaces: true
      withSeparateModelsAndApi: true

  python-client:
    inputSpec: ./api/openapi.yaml
    output: ./generated/python-client
    generatorName: python
    additionalProperties:
      packageName: "example_api_client"
      projectName: "example-api-client"

  go-server:
    inputSpec: ./api/openapi.yaml
    output: ./generated/go-server
    generatorName: go-server
    additionalProperties:
      packageName: "api"
      serverPort: 8080
```

### SDK Generation Script

```bash
#!/bin/bash
# generate-sdks.sh

SPEC_FILE="./api/openapi.yaml"
OUTPUT_DIR="./generated"

# Validate spec first
npx @redocly/cli lint $SPEC_FILE

if [ $? -ne 0 ]; then
    echo "Spec validation failed"
    exit 1
fi

# Generate TypeScript client
npx openapi-generator-cli generate \
    -i $SPEC_FILE \
    -g typescript-axios \
    -o $OUTPUT_DIR/typescript \
    --additional-properties=npmName=@example/api-client,supportsES6=true

# Generate Python client
npx openapi-generator-cli generate \
    -i $SPEC_FILE \
    -g python \
    -o $OUTPUT_DIR/python \
    --additional-properties=packageName=example_api

echo "SDK generation complete"
```

## Documentation Tools

### Redoc Configuration

```yaml
# redoc.yaml
openapi: "./api/openapi.yaml"
output: "./docs/index.html"

options:
  theme:
    colors:
      primary:
        main: "#1976d2"
    typography:
      fontSize: "15px"
      fontFamily: "Inter, sans-serif"
      code:
        fontSize: "13px"
        fontFamily: "JetBrains Mono, monospace"

  hideDownloadButton: false
  hideHostname: false
  pathInMiddlePanel: true
  requiredPropsFirst: true
  sortPropsAlphabetically: false
  hideLoading: false
  nativeScrollbars: true

  jsonSampleExpandLevel: 2
  enumSkipQuotes: false
  showExtensions: true
```

### Swagger UI Configuration

```javascript
// swagger-ui-config.js
const swaggerUiOptions = {
  dom_id: '#swagger-ui',
  url: '/api/openapi.yaml',

  // Display options
  deepLinking: true,
  displayOperationId: false,
  defaultModelsExpandDepth: 2,
  defaultModelExpandDepth: 2,
  displayRequestDuration: true,
  docExpansion: 'list',
  filter: true,
  showExtensions: true,
  showCommonExtensions: true,

  // Try it out configuration
  tryItOutEnabled: true,
  supportedSubmitMethods: ['get', 'post', 'put', 'patch', 'delete'],

  // Request interceptor for auth
  requestInterceptor: (request) => {
    const token = localStorage.getItem('api_token');
    if (token) {
      request.headers.Authorization = `Bearer ${token}`;
    }
    return request;
  },

  // Plugins
  plugins: [
    SwaggerUIBundle.plugins.DownloadUrl
  ],

  // Layout
  layout: "StandaloneLayout",
  presets: [
    SwaggerUIBundle.presets.apis,
    SwaggerUIStandalonePreset
  ]
};
```

## Лучшие практики

1. **Version everything** — используйте семантическое версионирование
2. **Examples for all** — добавляйте реалистичные примеры для всех схем
3. **Error documentation** — документируйте все возможные коды ошибок
4. **Consistent naming** — kebab-case для paths, camelCase для properties
5. **Reusable components** — выносите общие схемы в components
6. **Validate specs** — используйте линтеры (Spectral, Redocly)
