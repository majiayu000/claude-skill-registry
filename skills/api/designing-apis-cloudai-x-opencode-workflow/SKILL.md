---
name: designing-apis
description: Guides REST and GraphQL API design, endpoint patterns, request/response schemas, versioning, and API best practices. Use when building APIs, designing endpoints, or reviewing API contracts.
license: MIT
compatibility: opencode
metadata:
  category: design
  audience: developers
---

# Designing APIs

Principles and patterns for designing clean, consistent, and maintainable APIs.

## When to Use This Skill

- Designing new API endpoints
- Reviewing API contracts
- Planning API versioning strategies
- Defining request/response schemas
- Building GraphQL schemas
- Documenting APIs

---

## REST API Design Principles

### Resource-Oriented Design

APIs should be organized around **resources**, not actions:

```
GOOD (Resource-oriented):
GET    /users           → List users
GET    /users/123       → Get user 123
POST   /users           → Create user
PUT    /users/123       → Update user 123
DELETE /users/123       → Delete user 123

BAD (Action-oriented):
POST   /getUsers
POST   /createUser
POST   /updateUser
POST   /deleteUser
```

### HTTP Method Semantics

| Method | Purpose | Idempotent | Safe | Request Body |
|--------|---------|------------|------|--------------|
| GET | Retrieve resource(s) | Yes | Yes | No |
| POST | Create resource | No | No | Yes |
| PUT | Replace resource | Yes | No | Yes |
| PATCH | Partial update | Yes | No | Yes |
| DELETE | Remove resource | Yes | No | Optional |

### URL Structure Patterns

```
Collection:     /users
Item:           /users/{id}
Nested:         /users/{id}/posts
Action:         /users/{id}/activate (POST only, for non-CRUD)
Filter:         /users?status=active&role=admin
Pagination:     /users?page=2&limit=20
Sort:           /users?sort=created_at&order=desc
```

---

## Request Design

### Path Parameters vs Query Parameters

| Use | Path Parameters | Query Parameters |
|-----|-----------------|------------------|
| Resource identification | `/users/123` | - |
| Required filters | `/orgs/456/users` | - |
| Optional filters | - | `?status=active` |
| Pagination | - | `?page=2&limit=20` |
| Sorting | - | `?sort=name&order=asc` |
| Search | - | `?q=searchterm` |

### Request Body Patterns

```json
// POST /users - Create
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "admin"
}

// PATCH /users/123 - Partial update
{
  "name": "Jane Doe"
}

// Bulk operations - POST /users/bulk
{
  "operations": [
    { "action": "create", "data": { "email": "..." } },
    { "action": "update", "id": "123", "data": { "name": "..." } }
  ]
}
```

---

## Response Design

### Consistent Response Envelope

```json
// Success response
{
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "abc123"
  }
}

// Collection response with pagination
{
  "data": [ ... ],
  "meta": {
    "total": 100,
    "page": 2,
    "limit": 20,
    "hasMore": true
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "abc123"
  }
}
```

### HTTP Status Code Guidelines

| Range | Category | Common Codes |
|-------|----------|--------------|
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirect | 301 Moved, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Unprocessable |
| 5xx | Server Error | 500 Internal, 502 Bad Gateway, 503 Unavailable |

### Status Code Decision Tree

```
Success?
├─ Yes
│  ├─ Returning data? → 200 OK
│  ├─ Created resource? → 201 Created
│  └─ No content? → 204 No Content
└─ No
   ├─ Client's fault?
   │  ├─ Bad syntax? → 400 Bad Request
   │  ├─ Not authenticated? → 401 Unauthorized
   │  ├─ Not authorized? → 403 Forbidden
   │  ├─ Not found? → 404 Not Found
   │  └─ Validation failed? → 422 Unprocessable Entity
   └─ Server's fault? → 500 Internal Server Error
```

---

## API Versioning Strategies

### URL Path Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

**Pros**: Explicit, easy to understand, easy to route
**Cons**: URL changes between versions

### Header Versioning

```
GET /api/users
Accept: application/vnd.myapi.v2+json
```

**Pros**: Clean URLs
**Cons**: Hidden version, harder to test

### Query Parameter Versioning

```
/api/users?version=2
```

**Pros**: Flexible, easy to test
**Cons**: Can be forgotten, pollutes query string

---

## GraphQL Design Patterns

### Schema-First Design

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  createdAt: DateTime!
}

type Query {
  user(id: ID!): User
  users(filter: UserFilter, page: PageInput): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}
```

### Input Types Pattern

```graphql
input CreateUserInput {
  email: String!
  name: String!
  role: Role = USER
}

input UpdateUserInput {
  email: String
  name: String
  role: Role
}

input UserFilter {
  status: UserStatus
  role: Role
  search: String
}
```

### Pagination Patterns

```graphql
# Cursor-based (recommended for large datasets)
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Offset-based (simpler, for smaller datasets)
type UserList {
  items: [User!]!
  total: Int!
  page: Int!
  limit: Int!
}
```

---

## Authentication & Authorization

### Authentication Patterns

| Pattern | Use Case | Header |
|---------|----------|--------|
| Bearer Token | Standard API auth | `Authorization: Bearer <token>` |
| API Key | Server-to-server | `X-API-Key: <key>` |
| Basic Auth | Simple/legacy systems | `Authorization: Basic <base64>` |
| OAuth 2.0 | Third-party integration | OAuth flow |

### Authorization Responses

```
Not authenticated → 401 Unauthorized
  (User identity unknown)

Not authorized → 403 Forbidden
  (User known, but lacks permission)
```

---

## Error Handling Patterns

### Standardized Error Format

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 123 not found",
    "target": "user",
    "details": [
      {
        "code": "INVALID_ID",
        "message": "The provided ID does not exist",
        "target": "id"
      }
    ],
    "innererror": {
      "trace": "abc123",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  }
}
```

### Common Error Codes

| Code | HTTP Status | When |
|------|-------------|------|
| `VALIDATION_ERROR` | 400/422 | Request data invalid |
| `UNAUTHORIZED` | 401 | Auth required |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `CONFLICT` | 409 | State conflict (duplicate) |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server failure |

---

## API Documentation

### OpenAPI/Swagger Structure

```yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

components:
  schemas:
    User:
      type: object
      required: [id, email]
      properties:
        id:
          type: string
        email:
          type: string
          format: email
```

---

## Anti-Patterns to Avoid

1. **Verbs in URLs** - Use `/users` not `/getUsers`
2. **Ignoring HTTP Methods** - Use proper methods, not POST for everything
3. **Inconsistent Naming** - Pick snake_case or camelCase, stick with it
4. **Leaking Implementation** - Don't expose internal IDs or DB structure
5. **Missing Pagination** - Always paginate collections
6. **Ignoring Idempotency** - PUT/DELETE must be idempotent
7. **No Versioning** - Plan for API evolution from day one

---

## Quick Reference

```
RESOURCE DESIGN:
  /resources           → Collection
  /resources/{id}      → Item
  /resources/{id}/sub  → Nested

HTTP METHODS:
  GET     → Read (safe, idempotent)
  POST    → Create (not idempotent)
  PUT     → Replace (idempotent)
  PATCH   → Update (idempotent)
  DELETE  → Remove (idempotent)

STATUS CODES:
  200 OK, 201 Created, 204 No Content
  400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
  500 Internal Server Error

VERSIONING:
  /api/v1/resources (recommended)

PAGINATION:
  ?page=2&limit=20 (offset)
  ?cursor=abc123&limit=20 (cursor)
```
