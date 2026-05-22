---
name: arcanea-api-design
description: Design APIs that developers love. RESTful principles, GraphQL patterns, versioning strategies, and the art of creating interfaces that are intuitive, consistent, and future-proof.
version: 2.0.0
author: Arcanea
tags: [api, rest, graphql, design, interfaces, development]
triggers:
  - api design
  - rest api
  - graphql
  - endpoints
  - api versioning
  - interface design
---

# The API Design Codex

> *"An API is a user interface for developers. Design it with the same care you'd design a UI for users."*

---

## The API Design Philosophy

### First Principles

```
GOOD APIs ARE:
• Predictable   - Behavior matches expectations
• Consistent    - Same patterns everywhere
• Simple        - Easy to use, hard to misuse
• Evolvable     - Can change without breaking
• Documented    - Self-describing where possible

GOOD APIs DO NOT:
• Surprise developers
• Require reading implementation
• Change behavior silently
• Expose internal details
• Force awkward workarounds
```

---

## RESTful API Design

### The REST Maturity Model

```
╔═══════════════════════════════════════════════════════════════════╗
║                    RICHARDSON MATURITY MODEL                       ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   LEVEL 0: The Swamp of POX                                       ║
║   Single endpoint, RPC-style                                       ║
║   POST /api → {action: "getUser", id: 1}                          ║
║                                                                    ║
║   LEVEL 1: Resources                                               ║
║   Multiple endpoints, still mostly POST                            ║
║   POST /users/1 → {action: "get"}                                 ║
║                                                                    ║
║   LEVEL 2: HTTP Verbs                                              ║
║   Proper use of GET, POST, PUT, DELETE                             ║
║   GET /users/1                                                     ║
║                                                                    ║
║   LEVEL 3: Hypermedia (HATEOAS)                                    ║
║   Responses include links to related actions                       ║
║   GET /users/1 → {..., links: [{rel: "orders", href: "/..."}]}    ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

### Resource Naming

```
NOUNS, NOT VERBS:
✓ GET /users          ✗ GET /getUsers
✓ POST /orders        ✗ POST /createOrder
✓ DELETE /items/1     ✗ POST /deleteItem

PLURAL FOR COLLECTIONS:
✓ /users              ✗ /user
✓ /orders             ✗ /order

HIERARCHY FOR RELATIONSHIPS:
✓ /users/1/orders     ✗ /getUserOrders?userId=1
✓ /orders/1/items     ✗ /orderItems?orderId=1

KEBAB-CASE FOR MULTI-WORD:
✓ /user-profiles      ✗ /userProfiles
✓ /order-items        ✗ /order_items
```

### HTTP Methods

```
┌────────┬────────────────┬──────────────┬──────────────┐
│ Method │ Purpose        │ Idempotent   │ Safe         │
├────────┼────────────────┼──────────────┼──────────────┤
│ GET    │ Read resource  │ Yes          │ Yes          │
│ POST   │ Create new     │ No           │ No           │
│ PUT    │ Replace all    │ Yes          │ No           │
│ PATCH  │ Partial update │ No*          │ No           │
│ DELETE │ Remove         │ Yes          │ No           │
└────────┴────────────────┴──────────────┴──────────────┘

*PATCH can be idempotent if designed carefully
```

### Status Codes

```
2XX SUCCESS:
200 OK           - General success
201 Created      - Resource created (include Location header)
202 Accepted     - Processing started (async operations)
204 No Content   - Success with no body (DELETE, PUT)

4XX CLIENT ERRORS:
400 Bad Request  - Malformed request
401 Unauthorized - Authentication required
403 Forbidden    - Authenticated but not permitted
404 Not Found    - Resource doesn't exist
409 Conflict     - State conflict (e.g., duplicate)
422 Unprocessable - Valid syntax, invalid semantics

5XX SERVER ERRORS:
500 Internal     - Unexpected error
502 Bad Gateway  - Upstream service failed
503 Unavailable  - Temporarily overloaded
504 Gateway Timeout - Upstream timeout
```

### Request/Response Design

```json
// GOOD REQUEST
POST /api/v1/users
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member"
}

// GOOD RESPONSE
{
  "data": {
    "id": "usr_123abc",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "member",
    "createdAt": "2024-01-15T10:30:00Z"
  },
  "links": {
    "self": "/api/v1/users/usr_123abc",
    "orders": "/api/v1/users/usr_123abc/orders"
  }
}

// GOOD ERROR
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  }
}
```

---

## Pagination, Filtering, Sorting

### Pagination Patterns

```
OFFSET-BASED (Simple, but has issues at scale):
GET /users?offset=20&limit=10

CURSOR-BASED (Better for large datasets):
GET /users?cursor=eyJpZCI6MTAwfQ&limit=10

Response:
{
  "data": [...],
  "pagination": {
    "total": 1000,
    "limit": 10,
    "nextCursor": "eyJpZCI6MTEwfQ",
    "prevCursor": "eyJpZCI6OTB9"
  }
}
```

### Filtering

```
SIMPLE EQUALITY:
GET /users?status=active&role=admin

COMPARISON OPERATORS:
GET /orders?total[gte]=100&total[lte]=500
GET /users?createdAt[gt]=2024-01-01

ARRAY VALUES:
GET /users?status[]=active&status[]=pending

SEARCH:
GET /users?q=john
GET /products?search=widget
```

### Sorting

```
SINGLE FIELD:
GET /users?sort=createdAt
GET /users?sort=-createdAt  (descending)

MULTIPLE FIELDS:
GET /users?sort=-createdAt,name
GET /users?orderBy=createdAt:desc,name:asc
```

---

## API Versioning

### Versioning Strategies

```
URL PATH (Most common, explicit):
GET /api/v1/users
GET /api/v2/users

QUERY PARAMETER:
GET /api/users?version=1
GET /api/users?v=2

HEADER (Clean URLs, hidden version):
GET /api/users
Accept: application/vnd.api+json;version=1

CONTENT NEGOTIATION:
GET /api/users
Accept: application/vnd.company.v2+json
```

### Version Lifecycle

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Alpha  │────▶│  Beta   │────▶│ Stable  │────▶│ Sunset  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
    ↓               ↓               ↓               ↓
 Breaking        Breaking        Backward        Deprecation
 changes OK      with notice     compatible      warnings
```

### Breaking vs Non-Breaking Changes

```
NON-BREAKING (Safe to add):
✓ New optional fields
✓ New endpoints
✓ New query parameters
✓ New response fields

BREAKING (Requires new version):
✗ Removing fields
✗ Renaming fields
✗ Changing field types
✗ Changing URL structure
✗ Changing validation rules
```

---

## GraphQL Design

### Schema Design

```graphql
# Type definitions
type User {
  id: ID!
  email: String!
  name: String!
  orders(first: Int, after: String): OrderConnection!
  createdAt: DateTime!
}

type Order {
  id: ID!
  user: User!
  items: [OrderItem!]!
  total: Money!
  status: OrderStatus!
}

enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

# Connections for pagination
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

### Query Design

```graphql
type Query {
  # Single resource
  user(id: ID!): User

  # Collection with filtering
  users(
    filter: UserFilter
    orderBy: UserOrderBy
    first: Int
    after: String
  ): UserConnection!

  # Viewer pattern for current user
  viewer: User
}

input UserFilter {
  status: UserStatus
  role: UserRole
  search: String
}

input UserOrderBy {
  field: UserOrderField!
  direction: OrderDirection!
}
```

### Mutation Design

```graphql
type Mutation {
  # Create with input type
  createUser(input: CreateUserInput!): CreateUserPayload!

  # Update with partial input
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!

  # Delete returns deleted item or boolean
  deleteUser(id: ID!): DeleteUserPayload!
}

input CreateUserInput {
  email: String!
  name: String!
  role: UserRole
}

type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}
```

---

## Security Best Practices

### Authentication

```
TOKEN-BASED:
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

API KEY:
X-API-Key: sk_live_abcd1234

OAUTH 2.0 FLOWS:
• Authorization Code - Web apps
• Client Credentials - Server-to-server
• PKCE - Mobile/SPA apps
```

### Rate Limiting

```
HEADERS:
X-RateLimit-Limit: 1000        # Total allowed
X-RateLimit-Remaining: 999     # Remaining
X-RateLimit-Reset: 1609459200  # Reset timestamp

RESPONSE WHEN LIMITED:
HTTP/1.1 429 Too Many Requests
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "retryAfter": 60
  }
}
```

### Input Validation

```
ALWAYS VALIDATE:
□ Type (string, number, boolean)
□ Format (email, URL, UUID)
□ Length (min, max)
□ Range (min, max for numbers)
□ Allowed values (enums)
□ Required fields

SANITIZE:
□ Strip HTML
□ Escape special characters
□ Normalize unicode
□ Limit nested depth
```

---

## Documentation

### OpenAPI/Swagger

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    get:
      summary: List all users
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
      responses:
        200:
          description: User list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

### Self-Documenting APIs

```json
// HATEOAS - Include discoverable links
{
  "data": { ... },
  "links": {
    "self": "/api/users/1",
    "edit": "/api/users/1",
    "delete": "/api/users/1",
    "orders": "/api/users/1/orders"
  },
  "actions": [
    {
      "name": "deactivate",
      "method": "POST",
      "href": "/api/users/1/deactivate"
    }
  ]
}
```

---

## Error Handling

### Error Response Structure

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with ID 'usr_123' not found",
    "target": "user",
    "details": [
      {
        "code": "INVALID_ID",
        "target": "id",
        "message": "ID format is invalid"
      }
    ],
    "innererror": {
      "trace": "abc123",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  }
}
```

### Error Code Conventions

```
Use consistent, meaningful codes:

AUTHENTICATION:
• AUTH_REQUIRED
• AUTH_INVALID_TOKEN
• AUTH_TOKEN_EXPIRED

AUTHORIZATION:
• FORBIDDEN
• INSUFFICIENT_PERMISSIONS

VALIDATION:
• VALIDATION_ERROR
• INVALID_FORMAT
• MISSING_FIELD
• FIELD_TOO_LONG

RESOURCE:
• RESOURCE_NOT_FOUND
• RESOURCE_ALREADY_EXISTS
• RESOURCE_CONFLICT

RATE LIMITING:
• RATE_LIMIT_EXCEEDED
• QUOTA_EXCEEDED
```

---

## Quick Reference

### API Design Checklist

```
□ Resources are nouns, plural
□ HTTP methods used correctly
□ Status codes are semantic
□ Consistent naming conventions
□ Pagination for lists
□ Filtering and sorting
□ Versioning strategy defined
□ Error format standardized
□ Rate limiting implemented
□ Authentication documented
□ OpenAPI spec available
□ Examples for all endpoints
```

### REST vs GraphQL Decision

```
CHOOSE REST WHEN:
• Simple CRUD operations
• Caching is important
• Team knows REST well
• Multiple simple clients
• Request patterns are predictable

CHOOSE GRAPHQL WHEN:
• Complex, nested data
• Mobile apps with bandwidth concerns
• Frontend needs flexibility
• Multiple related resources
• Rapid frontend iteration
```

---

*"The best API is invisible. Developers use it without thinking about it because it does what they expect."*
