---
name: api-portal-design
description: API documentation and developer portal design
allowed-tools: Read, Glob, Grep, Write, Edit
---

# API Portal Design Skill

## When to Use This Skill

Use this skill when:

- **Api Portal Design tasks** - Working on api documentation and developer portal design
- **Planning or design** - Need guidance on Api Portal Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Design comprehensive API documentation and developer portals for exceptional developer experience.

## MANDATORY: Documentation-First Approach

Before designing API portals:

1. **Invoke `docs-management` skill** for API documentation patterns
2. **Verify OpenAPI/AsyncAPI standards** via MCP servers (context7)
3. **Base guidance on industry API documentation best practices**

## Developer Portal Architecture

```text
Developer Portal Components:

┌─────────────────────────────────────────────────────────────────────────────┐
│                           Developer Portal                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Getting    │  │    API      │  │   Code      │  │   API       │        │
│  │  Started    │  │  Reference  │  │  Examples   │  │  Console    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   SDKs &    │  │  Change     │  │   Status    │  │   Support   │        │
│  │  Libraries  │  │    Log      │  │    Page     │  │   Center    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Authentication & API Keys                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Portal Content Structure

### Essential Sections

| Section | Purpose | Priority |
|---------|---------|----------|
| **Getting Started** | First-time user guide | P0 |
| **Authentication** | How to authenticate | P0 |
| **API Reference** | Complete endpoint docs | P0 |
| **Code Examples** | Copy-paste samples | P0 |
| **SDKs** | Client libraries | P1 |
| **Changelog** | Version history | P1 |
| **Rate Limits** | Usage constraints | P1 |
| **Errors** | Error handling guide | P1 |
| **Webhooks** | Event notifications | P2 |
| **Best Practices** | Usage recommendations | P2 |

### Getting Started Guide

```markdown
# Getting Started

Get up and running with the [Product] API in 5 minutes.

## Prerequisites

- An account on [Product] ([Sign up free](link))
- An API key ([Get your key](link))
- Basic knowledge of REST APIs

## Quick Start

### 1. Get Your API Key

1. Log in to your [Product] dashboard
2. Navigate to **Settings → API Keys**
3. Click **Create New Key**
4. Copy your key (you won't see it again!)

### 2. Make Your First Request

```bash
curl -X GET "https://api.example.com/v1/users/me" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response:**

```json
{
  "id": "usr_123abc",
  "email": "developer@example.com",
  "name": "Jane Developer",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### 3. Explore the API

- [API Reference](/docs/api-reference) - Complete endpoint documentation
- [Code Examples](/docs/examples) - Ready-to-use samples
- [SDKs](/docs/sdks) - Official client libraries

## Next Steps

| Goal | Resource |
|------|----------|
| Understand authentication | [Authentication Guide](/docs/auth) |
| Browse all endpoints | [API Reference](/docs/api-reference) |
| Handle errors gracefully | [Error Handling](/docs/errors) |
| Go to production | [Production Checklist](/docs/production) |

## Need Help?

- [FAQ](/docs/faq)
- [Community Forum](link)
- [Support](mailto:support@example.com)

```text

```

### Authentication Documentation

```markdown
# Authentication

All API requests require authentication using Bearer tokens.

## API Keys

API keys are long-lived credentials for server-to-server communication.

### Creating API Keys

1. Go to **Dashboard → Settings → API Keys**
2. Click **Create New Key**
3. Give it a descriptive name
4. Select the appropriate permissions
5. Copy and securely store the key

### Using API Keys

Include your API key in the `Authorization` header:

```bash
curl -X GET "https://api.example.com/v1/resource" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Key Security Best Practices

| Do | Don't |
|----|-------|
| Store keys in environment variables | Commit keys to source control |
| Use separate keys per environment | Share keys between services |
| Rotate keys regularly | Use keys in client-side code |
| Set minimum required permissions | Use admin keys for all operations |

---

## OAuth 2.0

For user-facing applications, use OAuth 2.0 for secure delegated access.

### Authorization Code Flow

```text
┌──────────┐                               ┌──────────┐
│  Client  │                               │   Auth   │
│   App    │                               │  Server  │
└────┬─────┘                               └────┬─────┘
     │                                          │
     │ 1. Redirect to authorization endpoint    │
     │─────────────────────────────────────────►│
     │                                          │
     │ 2. User authenticates and consents       │
     │                                          │
     │ 3. Redirect back with authorization code │
     │◄─────────────────────────────────────────│
     │                                          │
     │ 4. Exchange code for tokens              │
     │─────────────────────────────────────────►│
     │                                          │
     │ 5. Return access_token and refresh_token │
     │◄─────────────────────────────────────────│
     │                                          │
```

### OAuth Endpoints

| Endpoint | URL |
|----------|-----|
| Authorization | `https://auth.example.com/oauth/authorize` |
| Token | `https://auth.example.com/oauth/token` |
| Revoke | `https://auth.example.com/oauth/revoke` |

### Scopes

| Scope | Description |
|-------|-------------|
| `read:users` | Read user information |
| `write:users` | Create and update users |
| `read:orders` | Read order data |
| `write:orders` | Create and modify orders |

### Token Refresh

```bash
curl -X POST "https://auth.example.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=YOUR_REFRESH_TOKEN" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

```text

```

## OpenAPI Specification Template

```yaml
openapi: 3.1.0
info:
  title: Product API
  version: 1.0.0
  description: |
    The Product API provides programmatic access to [Product] features.

    ## Authentication

    All endpoints require authentication via Bearer token.
    Get your API key from the [Dashboard](https://dashboard.example.com).

    ## Rate Limiting

    - Standard: 100 requests/minute
    - Premium: 1000 requests/minute

    See [Rate Limits](/docs/rate-limits) for details.

  contact:
    name: API Support
    email: api-support@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api-staging.example.com/v1
    description: Staging

security:
  - bearerAuth: []

tags:
  - name: Users
    description: User management operations
  - name: Orders
    description: Order processing operations

paths:
  /users:
    get:
      tags: [Users]
      operationId: listUsers
      summary: List all users
      description: |
        Returns a paginated list of users in your organization.

        Results are sorted by creation date, newest first.
      parameters:
        - name: limit
          in: query
          description: Maximum number of results to return
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: cursor
          in: query
          description: Pagination cursor from previous response
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              examples:
                default:
                  summary: Example response
                  value:
                    data:
                      - id: "usr_123"
                        email: "jane@example.com"
                        name: "Jane Doe"
                        created_at: "2025-01-15T10:30:00Z"
                    has_more: true
                    next_cursor: "cur_abc123"
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'

    post:
      tags: [Users]
      operationId: createUser
      summary: Create a user
      description: Creates a new user in your organization.
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
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          description: User already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /users/{userId}:
    get:
      tags: [Users]
      operationId: getUser
      summary: Get a user
      description: Retrieves a user by their ID.
      parameters:
        - name: userId
          in: path
          required: true
          description: The user's unique identifier
          schema:
            type: string
            pattern: '^usr_[a-zA-Z0-9]+$'
          example: usr_123abc
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        Use your API key as the Bearer token.

        Example: `Authorization: Bearer sk_live_abc123`

  schemas:
    User:
      type: object
      required: [id, email, created_at]
      properties:
        id:
          type: string
          description: Unique identifier for the user
          example: usr_123abc
        email:
          type: string
          format: email
          description: User's email address
          example: jane@example.com
        name:
          type: string
          description: User's display name
          example: Jane Doe
        created_at:
          type: string
          format: date-time
          description: When the user was created
          example: "2025-01-15T10:30:00Z"
        metadata:
          type: object
          additionalProperties: true
          description: Custom key-value pairs

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        has_more:
          type: boolean
          description: Whether more results are available
        next_cursor:
          type: string
          description: Cursor for fetching next page

    CreateUserRequest:
      type: object
      required: [email]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
        metadata:
          type: object
          additionalProperties: true

    Error:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code:
              type: string
              description: Error code
              example: invalid_request
            message:
              type: string
              description: Human-readable error message
              example: The email field is required
            details:
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
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: invalid_request
              message: Validation failed
              details:
                - field: email
                  message: Invalid email format

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: unauthorized
              message: Invalid or missing API key

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: not_found
              message: User not found

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
          description: Unix timestamp when limit resets
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: rate_limited
              message: Too many requests. Please retry after 60 seconds.
```

## Error Documentation

```markdown
# Error Handling

The API uses conventional HTTP response codes and returns detailed error information.

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing credentials |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable - Validation failed |
| 429 | Too Many Requests - Rate limited |
| 500 | Internal Error - Server-side issue |

## Error Response Format

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The email field is required",
    "request_id": "req_abc123",
    "details": [
      {
        "field": "email",
        "message": "This field is required"
      }
    ]
  }
}
```

## Error Codes Reference

### Authentication Errors

| Code | Description | Resolution |
|------|-------------|------------|
| `unauthorized` | Missing or invalid API key | Check your API key is correct |
| `token_expired` | Access token has expired | Refresh your token |
| `insufficient_scope` | Token lacks required scope | Request additional scopes |

### Validation Errors

| Code | Description | Resolution |
|------|-------------|------------|
| `invalid_request` | Request body is malformed | Check JSON syntax |
| `validation_failed` | One or more fields invalid | See `details` array |
| `missing_required_field` | Required field not provided | Include all required fields |

### Resource Errors

| Code | Description | Resolution |
|------|-------------|------------|
| `not_found` | Resource doesn't exist | Verify the ID is correct |
| `already_exists` | Resource already exists | Use existing resource or change identifier |
| `resource_locked` | Resource is being modified | Retry after a short delay |

## Handling Errors in Code

### csharp

```csharp
try
{
    var user = await client.Users.GetAsync(userId, ct);
}
catch (ApiException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
{
    _logger.LogWarning("User {UserId} not found", userId);
    return NotFound();
}
catch (ApiException ex) when (ex.StatusCode == HttpStatusCode.TooManyRequests)
{
    var retryAfter = ex.Headers.RetryAfter?.Delta ?? TimeSpan.FromSeconds(60);
    await Task.Delay(retryAfter, ct);
    // Retry request
}
catch (ApiException ex)
{
    _logger.LogError(ex, "API error: {Code} - {Message}", ex.Error.Code, ex.Error.Message);
    throw;
}
```

### TypeScript

```typescript
try {
  const user = await client.users.get(userId);
} catch (error) {
  if (error instanceof ApiError) {
    switch (error.code) {
      case 'not_found':
        console.warn(`User ${userId} not found`);
        return null;
      case 'rate_limited':
        await sleep(error.retryAfter ?? 60000);
        return client.users.get(userId); // Retry
      default:
        console.error(`API error: ${error.code} - ${error.message}`);
        throw error;
    }
  }
  throw error;
}
```

```text

```

## Code Examples Section

```markdown
# Code Examples

Ready-to-use examples in popular languages.

## Create a User

### cURL

```bash
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "name": "Jane Doe"
  }'
```

### C# (.NET)

```csharp
using var client = new ProductApiClient(apiKey);

var user = await client.Users.CreateAsync(new CreateUserRequest
{
    Email = "jane@example.com",
    Name = "Jane Doe"
});

Console.WriteLine($"Created user: {user.Id}");
```

### TypeScript

```typescript
import { ProductApi } from '@example/sdk';

const client = new ProductApi({ apiKey: process.env.API_KEY });

const user = await client.users.create({
  email: 'jane@example.com',
  name: 'Jane Doe',
});

console.log(`Created user: ${user.id}`);
```

### Python

```python
from example_sdk import ProductApi

client = ProductApi(api_key=os.environ["API_KEY"])

user = client.users.create(
    email="jane@example.com",
    name="Jane Doe"
)

print(f"Created user: {user.id}")
```

```text

```

## Portal Tooling Options

| Tool | Type | Best For |
|------|------|----------|
| **Stoplight** | Hosted | Design-first, collaboration |
| **Redocly** | Hosted/Self | OpenAPI rendering |
| **ReadMe** | Hosted | Full portal, interactive |
| **SwaggerHub** | Hosted | Swagger ecosystem |
| **Scalar** | Open Source | Modern, customizable |
| **Docusaurus + Plugin** | Open Source | Full control |

## Best Practices

### Developer Experience Principles

| Principle | Implementation |
|-----------|----------------|
| **Time to First Call** | Minimize steps to make first API call |
| **Copy-Paste Ready** | All examples should work immediately |
| **Error Messages** | Clear, actionable error responses |
| **Consistency** | Same patterns across all endpoints |
| **Discoverability** | Easy to find and navigate |

### Documentation Quality Checklist

- [ ] Every endpoint has description and examples
- [ ] All parameters documented with types and constraints
- [ ] Response schemas fully documented
- [ ] Error codes explained with resolutions
- [ ] Authentication clearly explained
- [ ] Rate limits documented
- [ ] Code examples in multiple languages
- [ ] Getting started guide under 5 minutes

## Workflow

When designing API portals:

1. **Define Audience**: Who will use the API?
2. **Structure Content**: Organize by user journey
3. **Write OpenAPI Spec**: Complete specification
4. **Add Examples**: Working code in target languages
5. **Build Portal**: Choose tooling, implement
6. **Test with Users**: Validate time-to-first-call
7. **Iterate**: Improve based on feedback

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
