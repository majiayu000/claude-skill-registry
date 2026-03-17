---
name: API Designer
description: Design REST and GraphQL APIs. Use when creating backend APIs, defining API contracts, or integrating third-party services. Covers endpoint design, authentication, versioning, documentation, and best practices.
version: 1.0.0
---

# API Designer

Design robust, scalable, and developer-friendly APIs.

## Core Principles

### 1. Developer Experience First

- Clear, predictable naming conventions
- Comprehensive documentation
- Helpful error messages
- Consistent patterns across endpoints

### 2. Design for Evolution

- Versioning strategy from day one
- Backward compatibility
- Deprecation process
- Migration guides for breaking changes

### 3. Security by Default

- Authentication and authorization
- Rate limiting and throttling
- Input validation and sanitization
- HTTPS only, no exceptions

### 4. Performance Matters

- Efficient queries and indexing
- Caching strategies
- Pagination for large datasets
- Compression (gzip, brotli)

## REST API Design

### Resource Naming Conventions

```
✅ Good (Nouns, plural, hierarchical):
GET    /users                  # List all users
GET    /users/123              # Get specific user
POST   /users                  # Create user
PUT    /users/123              # Replace user
PATCH  /users/123              # Update user
DELETE /users/123              # Delete user
GET    /users/123/posts        # User's posts (nested)
GET    /users/123/posts/456    # Specific post

❌ Bad (Verbs, inconsistent, unclear):
GET /getUsers
POST /createUser
GET /user-list
GET /UserData?id=123
```

### HTTP Methods & Semantics

| Method     | Purpose          | Idempotent | Safe | Request Body | Response Body   |
| ---------- | ---------------- | ---------- | ---- | ------------ | --------------- |
| **GET**    | Retrieve data    | Yes        | Yes  | No           | Yes             |
| **POST**   | Create resource  | No         | No   | Yes          | Yes (created)   |
| **PUT**    | Replace resource | Yes        | No   | Yes          | Yes (optional)  |
| **PATCH**  | Partial update   | No         | No   | Yes          | Yes (optional)  |
| **DELETE** | Remove resource  | Yes        | No   | No           | No (204) or Yes |

**Idempotent**: Multiple identical requests have same effect as single request
**Safe**: Request doesn't modify server state

### HTTP Status Codes

**Success (2xx)**:

- `200 OK` - Successful GET, PUT, PATCH, DELETE
- `201 Created` - Successful POST, includes `Location` header
- `204 No Content` - Successful request, no response body (often DELETE)

**Client Errors (4xx)**:

- `400 Bad Request` - Invalid syntax, validation error
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Authenticated but lacks permission
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Request conflicts with current state
- `422 Unprocessable Entity` - Validation error (semantic)
- `429 Too Many Requests` - Rate limit exceeded

**Server Errors (5xx)**:

- `500 Internal Server Error` - Generic server error
- `502 Bad Gateway` - Upstream service error
- `503 Service Unavailable` - Temporary unavailability
- `504 Gateway Timeout` - Upstream timeout

### Response Format Standards

**Success Response**:

```json
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2025-01-15T10:30:00Z"
    }
  }
}
```

**Error Response**:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "REQUIRED",
        "message": "Email is required"
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Age must be between 18 and 120"
      }
    ],
    "request_id": "req_abc123",
    "documentation_url": "https://api.example.com/docs/errors/validation"
  }
}
```

**List Response with Pagination**:

```json
{
  "data": [...],
  "pagination": {
    "cursor": "eyJpZCI6MTIzfQ==",
    "has_more": true,
    "total_count": 1000
  },
  "links": {
    "next": "/users?cursor=eyJpZCI6MTIzfQ==&limit=20",
    "prev": "/users?cursor=eyJpZCI6MTAwfQ==&limit=20"
  }
}
```

### Pagination Strategies

**Cursor-based (Recommended)**:

```
GET /users?cursor=abc123&limit=20

Pros: Consistent results, efficient, handles real-time data
Cons: Can't jump to arbitrary page
Use when: Large datasets, real-time data, performance critical
```

**Offset-based**:

```
GET /users?page=1&per_page=20
GET /users?offset=0&limit=20

Pros: Simple, can jump to any page
Cons: Inconsistent with concurrent writes, inefficient at scale
Use when: Small datasets, admin interfaces, simple use cases
```

### Filtering, Sorting, and Search

**Filtering**:

```
GET /users?status=active&role=admin&created_after=2025-01-01
```

**Sorting**:

```
GET /users?sort=-created_at,name  # Descending created_at, then ascending name
```

**Search**:

```
GET /users?q=john&fields=name,email  # Search across specified fields
```

### Authentication & Authorization

**JWT Bearer Token (Recommended for SPAs)**:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Pros: Stateless, includes user claims, works across domains
Cons: Can't revoke until expiry, larger payload
```

**API Keys (for service-to-service)**:

```
X-API-Key: sk_live_abc123...

Pros: Simple, easy to rotate, per-service keys
Cons: No user context, must be kept secret
```

**OAuth 2.0 (for third-party access)**:

```
Authorization: Bearer access_token

Pros: Delegated auth, scoped permissions, industry standard
Cons: Complex setup, requires OAuth server
```

**Basic Auth (only for internal/admin tools)**:

```
Authorization: Basic base64(username:password)

Pros: Simple, built-in to HTTP
Cons: Credentials in every request, must use HTTPS
```

### Rate Limiting

**Standard Headers**:

```
X-RateLimit-Limit: 1000          # Max requests per window
X-RateLimit-Remaining: 999       # Requests left
X-RateLimit-Reset: 1640995200    # Unix timestamp when limit resets
Retry-After: 60                  # Seconds to wait (on 429)
```

**Common Strategies**:

- Fixed window: 1000 requests per hour
- Sliding window: 1000 requests per rolling hour
- Token bucket: Burst allowance with refill rate
- Per-user, per-IP, or per-API-key limits

### Versioning Strategies

**URL Versioning (Recommended)**:

```
/v1/users
/v2/users

Pros: Explicit, easy to route, clear in logs
Cons: URL pollution, harder to evolve incrementally
```

**Header Versioning**:

```
Accept: application/vnd.myapp.v2+json
API-Version: 2

Pros: Clean URLs, follows REST principles
Cons: Less visible, harder to test in browser
```

**Best Practices**:

- Start with v1, not v0
- Only increment for breaking changes
- Support N and N-1 versions simultaneously
- Provide migration guides
- Announce deprecation 6-12 months ahead

---

## GraphQL API Design

### Schema Design

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
  createdAt: DateTime!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type PostEdge {
  node: Post!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

input CreateUserInput {
  name: String!
  email: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

### GraphQL Best Practices

**1. Use Relay Connection Pattern for Pagination**:

```graphql
query {
  users(first: 10, after: "cursor") {
    edges {
      node {
        id
        name
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

**2. Input Types for Mutations**:

```graphql
# ✅ Good: Input type + payload
mutation {
  createUser(input: { name: "John", email: "john@example.com" }) {
    user {
      id
      name
    }
    errors {
      field
      message
    }
  }
}

# ❌ Bad: Flat arguments
mutation {
  createUser(name: "John", email: "john@example.com") {
    id
    name
  }
}
```

**3. Error Handling**:

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User # Null if errors
  errors: [Error!] # Field-level errors
}

type Error {
  field: String!
  code: String!
  message: String!
}
```

### REST vs GraphQL Decision

**Use REST when**:

- Simple CRUD operations
- Caching is critical (HTTP caching)
- Public API for third-parties
- File uploads/downloads
- Team unfamiliar with GraphQL

**Use GraphQL when**:

- Clients need flexible queries
- Reducing over-fetching/under-fetching
- Rapid frontend iteration
- Complex nested data relationships
- Strong typing and schema benefits

---

## API Documentation

### OpenAPI/Swagger Specification

```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
  description: API for managing users and posts
servers:
  - url: https://api.example.com/v1
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'
    post:
      summary: Create user
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
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Documentation Best Practices

- ✅ Include request/response examples
- ✅ Document all error codes
- ✅ Provide authentication guides
- ✅ Interactive API playground (Swagger UI, GraphQL Playground)
- ✅ Code examples in multiple languages
- ✅ Rate limit information
- ✅ Changelog for API updates

---

## Security Checklist

- [ ] HTTPS only (redirect HTTP → HTTPS)
- [ ] Authentication required for protected endpoints
- [ ] Authorization checks (user can only access own data)
- [ ] Input validation (schema validation, sanitization)
- [ ] Rate limiting per user/IP
- [ ] CORS configuration (whitelist origins)
- [ ] SQL injection prevention (parameterized queries)
- [ ] No sensitive data in URLs (use headers/body)
- [ ] Audit logging for sensitive operations
- [ ] API keys rotatable and revocable

---

## Related Resources

**Related Skills**:

- `frontend-builder` - For consuming APIs from frontend
- `deployment-advisor` - For API hosting decisions
- `performance-optimizer` - For API performance tuning

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - REST vs GraphQL decisions
- `STANDARDS/architecture-patterns/api-gateway-pattern.md` - API gateway architecture (when created)

**Related Playbooks**:

- `PLAYBOOKS/deploy-api.md` - API deployment procedure (when created)
- `PLAYBOOKS/version-api.md` - API versioning workflow (when created)
