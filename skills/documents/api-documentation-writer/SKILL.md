---
name: api-documentation-writer
description: Expert guide for writing comprehensive API documentation including OpenAPI specs, endpoint references, authentication guides, and code examples. Use when documenting APIs, creating developer portals, or improving API discoverability.
---

# API Documentation Writer Skill

## Overview

This skill helps you create clear, comprehensive API documentation that developers love. Covers OpenAPI/Swagger specifications, endpoint references, authentication guides, code examples in multiple languages, and developer experience best practices.

## Documentation Philosophy

### The Three C's
1. **Clear**: Unambiguous, jargon-free explanations
2. **Complete**: All parameters, responses, and edge cases documented
3. **Current**: Always in sync with the actual API behavior

### What to Document
- **DO**: Document every public endpoint
- **DO**: Include request/response examples for all scenarios
- **DO**: Document error codes with remediation steps
- **DO**: Provide code examples in popular languages
- **DON'T**: Document internal/private endpoints
- **DON'T**: Assume readers know your domain
- **DON'T**: Let documentation drift from implementation

## OpenAPI Specification

### Basic Structure

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: |
    Welcome to the My API documentation.

    ## Getting Started
    1. Sign up for an API key at [dashboard.example.com](https://dashboard.example.com)
    2. Include your key in the `Authorization` header
    3. Start making requests!

    ## Rate Limits
    - Free tier: 100 requests/minute
    - Pro tier: 1000 requests/minute
  contact:
    name: API Support
    email: api@example.com
    url: https://support.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

tags:
  - name: Users
    description: User management operations
  - name: Items
    description: Item CRUD operations
```

### Endpoint Documentation

```yaml
paths:
  /users:
    get:
      tags:
        - Users
      summary: List all users
      description: |
        Retrieves a paginated list of users. Results are sorted by creation date (newest first).

        **Permissions required:** `users:read`
      operationId: listUsers
      parameters:
        - name: page
          in: query
          description: Page number (1-indexed)
          required: false
          schema:
            type: integer
            minimum: 1
            default: 1
          example: 1
        - name: limit
          in: query
          description: Number of results per page (max 100)
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
          example: 20
        - name: status
          in: query
          description: Filter by user status
          required: false
          schema:
            type: string
            enum: [active, inactive, pending]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              example:
                data:
                  - id: "usr_123"
                    email: "john@example.com"
                    name: "John Doe"
                    status: "active"
                    created_at: "2024-01-15T10:30:00Z"
                meta:
                  page: 1
                  limit: 20
                  total: 150
                  total_pages: 8
        '401':
          $ref: '#/components/responses/Unauthorized'
        '403':
          $ref: '#/components/responses/Forbidden'
        '429':
          $ref: '#/components/responses/RateLimited'

    post:
      tags:
        - Users
      summary: Create a new user
      description: |
        Creates a new user account. An email verification will be sent to the provided address.

        **Permissions required:** `users:write`
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            examples:
              basic:
                summary: Basic user creation
                value:
                  email: "jane@example.com"
                  name: "Jane Doe"
              with_metadata:
                summary: User with metadata
                value:
                  email: "jane@example.com"
                  name: "Jane Doe"
                  metadata:
                    department: "Engineering"
                    role: "Developer"
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: User with this email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error:
                  code: "USER_EXISTS"
                  message: "A user with this email already exists"
```

### Schema Definitions

```yaml
components:
  schemas:
    User:
      type: object
      description: Represents a user in the system
      required:
        - id
        - email
        - status
        - created_at
      properties:
        id:
          type: string
          description: Unique identifier (prefixed with `usr_`)
          pattern: '^usr_[a-zA-Z0-9]+$'
          example: "usr_123abc"
        email:
          type: string
          format: email
          description: User's email address (unique)
          example: "user@example.com"
        name:
          type: string
          description: User's display name
          maxLength: 100
          example: "John Doe"
        status:
          type: string
          enum: [active, inactive, pending]
          description: |
            Account status:
            - `active`: User can sign in and use the service
            - `inactive`: Account has been deactivated
            - `pending`: Awaiting email verification
          example: "active"
        metadata:
          type: object
          additionalProperties: true
          description: Custom key-value pairs for storing additional data
          example:
            department: "Engineering"
        created_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp of account creation
          example: "2024-01-15T10:30:00Z"
        updated_at:
          type: string
          format: date-time
          description: ISO 8601 timestamp of last update
          example: "2024-01-16T14:45:00Z"

    CreateUserRequest:
      type: object
      required:
        - email
      properties:
        email:
          type: string
          format: email
          description: Email address for the new user (must be unique)
        name:
          type: string
          description: User's display name
          maxLength: 100
        metadata:
          type: object
          additionalProperties: true

    Error:
      type: object
      required:
        - error
      properties:
        error:
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
              description: Human-readable error description
            details:
              type: array
              description: Additional error details for validation errors
              items:
                type: object
                properties:
                  field:
                    type: string
                  message:
                    type: string
```

### Authentication Documentation

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT token obtained from the `/auth/token` endpoint.

        Include in requests as:
        ```
        Authorization: Bearer <your-token>
        ```

        Tokens expire after 1 hour. Use refresh tokens for long-lived sessions.

    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: |
        API key for server-to-server communication.

        Obtain your key from the [Developer Dashboard](https://dashboard.example.com).

        Include in requests as:
        ```
        X-API-Key: <your-api-key>
        ```

security:
  - BearerAuth: []
  - ApiKeyAuth: []
```

### Reusable Responses

```yaml
components:
  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          examples:
            validation_error:
              summary: Validation error
              value:
                error:
                  code: "VALIDATION_ERROR"
                  message: "Request validation failed"
                  details:
                    - field: "email"
                      message: "Must be a valid email address"
            missing_field:
              summary: Missing required field
              value:
                error:
                  code: "MISSING_FIELD"
                  message: "Required field 'email' is missing"

    Unauthorized:
      description: Missing or invalid authentication
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "UNAUTHORIZED"
              message: "Invalid or expired authentication token"

    Forbidden:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "FORBIDDEN"
              message: "You don't have permission to access this resource"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "NOT_FOUND"
              message: "The requested resource was not found"

    RateLimited:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
          description: Request limit per minute
        X-RateLimit-Remaining:
          schema:
            type: integer
          description: Remaining requests in current window
        X-RateLimit-Reset:
          schema:
            type: integer
          description: Unix timestamp when the rate limit resets
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "RATE_LIMITED"
              message: "Too many requests. Please retry after 60 seconds"
```

## Markdown Documentation

### Endpoint Reference Template

```markdown
# Create User

Create a new user account.

## Endpoint

```
POST /v1/users
```

## Authentication

Requires API key with `users:write` permission.

## Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | User's email address (must be unique) |
| `name` | string | No | Display name (max 100 characters) |
| `metadata` | object | No | Custom key-value pairs |

### Example Request

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "name": "Jane Doe"
  }'
```

## Response

### Success (201 Created)

```json
{
  "id": "usr_abc123",
  "email": "jane@example.com",
  "name": "Jane Doe",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Errors

| Status | Code | Description |
|--------|------|-------------|
| 400 | `VALIDATION_ERROR` | Invalid email format or missing required field |
| 401 | `UNAUTHORIZED` | Invalid or missing authentication |
| 409 | `USER_EXISTS` | User with this email already exists |
| 429 | `RATE_LIMITED` | Too many requests |

### Error Example

```json
{
  "error": {
    "code": "USER_EXISTS",
    "message": "A user with this email already exists"
  }
}
```
```

## Code Examples

### Multi-Language Examples

```markdown
## Code Examples

### cURL

```bash
curl -X GET "https://api.example.com/v1/users?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### JavaScript (fetch)

```javascript
const response = await fetch('https://api.example.com/v1/users?limit=10', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});

const data = await response.json();
console.log(data);
```

### JavaScript (axios)

```javascript
import axios from 'axios';

const { data } = await axios.get('https://api.example.com/v1/users', {
  params: { limit: 10 },
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
});
```

### Python

```python
import requests

response = requests.get(
    'https://api.example.com/v1/users',
    params={'limit': 10},
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

data = response.json()
print(data)
```

### Ruby

```ruby
require 'net/http'
require 'json'

uri = URI('https://api.example.com/v1/users?limit=10')
request = Net::HTTP::Get.new(uri)
request['Authorization'] = 'Bearer YOUR_TOKEN'

response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
  http.request(request)
end

data = JSON.parse(response.body)
puts data
```

### Go

```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

func main() {
    req, _ := http.NewRequest("GET", "https://api.example.com/v1/users?limit=10", nil)
    req.Header.Set("Authorization", "Bearer YOUR_TOKEN")

    client := &http.Client{}
    resp, _ := client.Do(req)
    defer resp.Body.Close()

    var data map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&data)
    fmt.Println(data)
}
```
```

## Error Documentation

### Error Code Reference

```markdown
# Error Codes

All API errors follow a consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": []  // Optional additional information
  }
}
```

## Authentication Errors

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `UNAUTHORIZED` | 401 | Missing or invalid token | Include a valid `Authorization` header |
| `TOKEN_EXPIRED` | 401 | Token has expired | Obtain a new token via `/auth/token` |
| `INVALID_API_KEY` | 401 | API key not recognized | Check your API key in the dashboard |
| `FORBIDDEN` | 403 | Insufficient permissions | Request appropriate scopes for your token |

## Validation Errors

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `VALIDATION_ERROR` | 400 | Request body validation failed | Check the `details` array for specific fields |
| `MISSING_FIELD` | 400 | Required field not provided | Include all required fields |
| `INVALID_FORMAT` | 400 | Field format is incorrect | Match the expected format (see schema) |

## Resource Errors

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `NOT_FOUND` | 404 | Resource doesn't exist | Verify the resource ID is correct |
| `ALREADY_EXISTS` | 409 | Resource already exists | Use a different identifier or update existing |
| `CONFLICT` | 409 | State conflict | Refresh and retry the operation |

## Rate Limiting

| Code | HTTP Status | Description | Resolution |
|------|-------------|-------------|------------|
| `RATE_LIMITED` | 429 | Too many requests | Wait and retry (see `Retry-After` header) |
```

## Changelog Documentation

### API Changelog Format

```markdown
# API Changelog

## 2024-01-15 - v1.2.0

### Added
- `GET /users/{id}/activity` - Retrieve user activity history
- `metadata` field on User object for custom data storage

### Changed
- Pagination now 1-indexed (previously 0-indexed)
- Rate limits increased: Free tier 100 → 200 req/min

### Deprecated
- `GET /users/search` - Use `GET /users` with query parameters instead
  - Will be removed in v2.0.0

### Fixed
- `created_at` now correctly returns UTC timezone

---

## 2024-01-01 - v1.1.0

### Added
- Webhook support for user events
- `status` filter on `GET /users`

### Security
- API keys now support IP allowlisting
```

## Interactive Documentation

### Swagger UI Configuration

```javascript
// swagger-config.js
const swaggerUiOptions = {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'API Documentation',
  customfavIcon: '/favicon.ico',
  swaggerOptions: {
    persistAuthorization: true,
    displayRequestDuration: true,
    filter: true,
    tryItOutEnabled: true,
  },
};
```

### Redoc Configuration

```yaml
# redoc.yaml
x-tagGroups:
  - name: Getting Started
    tags:
      - Authentication
  - name: Core Resources
    tags:
      - Users
      - Items
  - name: Utilities
    tags:
      - Webhooks
      - Health

x-logo:
  url: 'https://example.com/logo.png'
  altText: 'API Logo'
```

## Documentation Checklist

### Per Endpoint
- [ ] Summary (one line)
- [ ] Description (detailed explanation)
- [ ] All parameters documented with types and examples
- [ ] All response codes with examples
- [ ] Error codes with remediation steps
- [ ] Code examples in at least 2 languages
- [ ] Authentication requirements stated

### Overall API
- [ ] Getting started guide
- [ ] Authentication guide with examples
- [ ] Rate limiting documentation
- [ ] Pagination patterns
- [ ] Error handling guide
- [ ] Changelog maintained
- [ ] Versioning strategy documented
- [ ] SDK/library links

### Developer Experience
- [ ] Interactive "Try It" functionality
- [ ] Copy-paste ready examples
- [ ] Consistent terminology
- [ ] Search functionality
- [ ] Mobile-friendly rendering

## Tools Integration

### Generate from Code

```bash
# From Express/Node.js routes
npx swagger-jsdoc -d swaggerDef.js -o openapi.yaml

# From TypeScript types
npx openapi-typescript-codegen --input openapi.yaml --output ./sdk
```

### Validate OpenAPI

```bash
# Validate spec
npx @redocly/cli lint openapi.yaml

# Preview documentation
npx @redocly/cli preview-docs openapi.yaml
```

## When to Use This Skill

Invoke this skill when:
- Creating new API documentation from scratch
- Adding documentation for new endpoints
- Writing OpenAPI/Swagger specifications
- Creating code examples for multiple languages
- Documenting authentication flows
- Building developer portals
- Improving existing API documentation
- Setting up interactive documentation (Swagger UI, Redoc)
