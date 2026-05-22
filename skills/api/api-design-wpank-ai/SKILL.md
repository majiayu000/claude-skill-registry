---
name: api-design
model: reasoning
description: REST and GraphQL API design principles — resource modeling, HTTP semantics, pagination, error handling, HATEOAS, schema design, and DataLoader patterns. Use when designing new APIs, reviewing specs, or establishing team API standards.
---

# API Design Principles

Design intuitive, scalable, and maintainable APIs that delight developers. Covers both REST and GraphQL paradigms with production-ready patterns.

## When to Use This Skill

- Designing new REST or GraphQL APIs
- Refactoring existing APIs for better usability
- Establishing API design standards for a team
- Reviewing API specifications before implementation
- Migrating between API paradigms (REST ↔ GraphQL)
- Optimizing APIs for specific consumers (mobile, third-party)


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install api-design
```


---

## REST Design Principles

### Resource-Oriented Architecture

Resources are nouns, actions are HTTP methods.

| Method | Semantics | Idempotent | Safe |
|--------|-----------|------------|------|
| `GET` | Retrieve resource(s) | Yes | Yes |
| `POST` | Create new resource | No | No |
| `PUT` | Replace entire resource | Yes | No |
| `PATCH` | Partial update | No | No |
| `DELETE` | Remove resource | Yes | No |

### Resource Collection Design

```
# Resource-oriented endpoints
GET    /api/users              # List users (paginated)
POST   /api/users              # Create user
GET    /api/users/{id}         # Get specific user
PUT    /api/users/{id}         # Replace user
PATCH  /api/users/{id}         # Update user fields
DELETE /api/users/{id}         # Delete user

# Nested resources (max 2 levels deep)
GET    /api/users/{id}/orders  # Get user's orders
POST   /api/users/{id}/orders  # Create order for user

# Anti-pattern: action-oriented endpoints
POST   /api/createUser         # ✗ verb as URL
POST   /api/getUserById        # ✗ GET semantics via POST
```

### Pagination

**Offset-based** — simple, supports random page access:

```json
GET /api/users?page=2&page_size=20

{
  "items": [...],
  "total": 150,
  "page": 2,
  "page_size": 20,
  "pages": 8
}
```

**Cursor-based** — efficient for large datasets, no drift:

```json
GET /api/users?limit=20&cursor=eyJpZCI6MTIzfQ

{
  "items": [...],
  "next_cursor": "eyJpZCI6MTQzfQ",
  "has_more": true
}
```

Always paginate collections. Enforce a `page_size` maximum (e.g., 100).

### Filtering, Sorting, and Search

```
GET /api/users?status=active&role=admin       # Filtering
GET /api/users?sort=-created_at               # Sorting (- for descending)
GET /api/users?search=john                    # Full-text search
GET /api/users?fields=id,name,email           # Sparse fieldsets
```

### Error Response Format

Standardize all error responses with a consistent envelope:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body contains invalid fields.",
    "details": [
      { "field": "email", "message": "Must be a valid email address" },
      { "field": "age", "message": "Must be a positive integer" }
    ],
    "requestId": "req_abc123xyz"
  }
}
```

### Status Code Usage

| Code | Name | When to Use |
|------|------|-------------|
| `200` | OK | Successful GET, PATCH, PUT |
| `201` | Created | Successful POST (include `Location` header) |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Malformed syntax, invalid JSON |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Authenticated but insufficient permissions |
| `404` | Not Found | Resource does not exist |
| `409` | Conflict | State conflict (duplicate email, concurrent edit) |
| `422` | Unprocessable Entity | Valid syntax but semantic errors |
| `429` | Too Many Requests | Rate limit exceeded (include `Retry-After`) |
| `500` | Internal Server Error | Unexpected server failure |

### HATEOAS

Include navigational links in responses to make the API self-describing:

```json
{
  "id": "123",
  "name": "Alice",
  "_links": {
    "self": { "href": "/api/users/123" },
    "orders": { "href": "/api/users/123/orders" },
    "update": { "href": "/api/users/123", "method": "PATCH" }
  }
}
```

### Idempotency

For non-idempotent operations (POST), accept an `Idempotency-Key` header to prevent duplicate processing:

```
POST /api/orders
Idempotency-Key: unique-key-123
```

---

## GraphQL Design Principles

### Schema-First Development

Design the schema before writing resolvers. Types define your domain model.

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
  orders(first: Int = 20, after: String): OrderConnection!
  profile: UserProfile
}

# Relay-style cursor pagination
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Enums for type safety
enum OrderStatus { PENDING CONFIRMED SHIPPED DELIVERED CANCELLED }

# Custom scalars
scalar DateTime
scalar Money
```

### Mutation Pattern — Input/Payload

Always use dedicated `Input` and `Payload` types:

```graphql
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
  success: Boolean!
}

type Error {
  field: String
  message: String!
  code: String!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}
```

### Union Error Pattern

Return typed errors as union members for granular client handling:

```graphql
union UserResult = User | NotFoundError | ValidationError | AuthorizationError

type Query {
  user(id: ID!): UserResult!
}
```

### DataLoader — N+1 Prevention

Batch relationship lookups with DataLoaders to avoid N+1 queries:

```python
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        users = await fetch_users_by_ids(user_ids)
        user_map = {u["id"]: u for u in users}
        return [user_map.get(uid) for uid in user_ids]

# In resolver
@user_type.field("orders")
async def resolve_orders(user, info, first=20):
    loader = info.context["loaders"]["orders_by_user"]
    return await loader.load(user["id"])
```

### Schema Evolution

Use `@deprecated` instead of removing fields:

```graphql
type User {
  name: String! @deprecated(reason: "Use firstName and lastName")
  firstName: String!
  lastName: String!
}
```

---

## REST vs GraphQL vs gRPC

| Criteria | REST | GraphQL | gRPC |
|----------|------|---------|------|
| **Best for** | CRUD public APIs | Complex relational data, client-driven queries | Internal microservices, high-throughput |
| **Over/under-fetching** | Common problem | Solved by design | Minimal — schema is explicit |
| **Caching** | Native HTTP caching | Requires custom caching | No built-in HTTP caching |
| **Real-time** | Polling / WebSockets | Subscriptions (built-in) | Bidirectional streaming |
| **Versioning** | URL or header versioning | Schema evolution with `@deprecated` | Package versioning in `.proto` |
| **Error handling** | HTTP status codes + body | Always 200 — errors in response | gRPC status codes |

**Rule of thumb:** Default to REST for public APIs. Use GraphQL when clients need flexible queries across related data. Use gRPC for internal service-to-service communication.

---

## Best Practices

### REST

1. **Consistent naming** — plural nouns for collections (`/users`, not `/user`)
2. **Stateless** — each request contains all necessary information
3. **Correct status codes** — 2xx success, 4xx client errors, 5xx server errors
4. **Version your API** — plan for breaking changes from day one
5. **Paginate everything** — never return unbounded collections
6. **Document with OpenAPI** — generate interactive docs from spec
7. **CORS** — whitelist specific origins, never `*` with credentials

### GraphQL

1. **Schema first** — design schema before writing resolvers
2. **DataLoaders everywhere** — prevent N+1 on every relationship
3. **Input validation** — validate at schema and resolver levels
4. **Structured errors** — return errors in mutation payloads
5. **Cursor pagination** — use Relay spec for large datasets
6. **Depth/complexity limits** — protect against expensive queries
7. **Deprecation over removal** — use `@deprecated` directive

---

## NEVER Do

1. **NEVER use verbs in REST URLs** — resources are nouns, HTTP methods are verbs
2. **NEVER return unbounded collections** — always paginate with a page_size maximum
3. **NEVER expose database schema directly** — API resources are not database tables
4. **NEVER use inconsistent error formats** — every error follows the same envelope
5. **NEVER break a published API without versioning** — breaking changes require a new version, migration guide, and deprecation timeline
6. **NEVER skip authentication on production endpoints** — even public read-only APIs need API keys for tracking and rate limiting
7. **NEVER return stack traces or internal details in error responses** — log details server-side, return safe messages to clients
8. **NEVER cache GraphQL queries without considering user context** — personalized data requires per-user cache keys

## Resources

- **references/rest-best-practices.md** — URL structure, HTTP methods, status codes, pagination, caching, CORS, and rate limiting patterns
- **references/graphql-schema-design.md** — Schema patterns including type design, Relay pagination, mutations, subscriptions, N+1 prevention, and custom directives
- **references/api-versioning-strategies.md** — Versioning approaches (URL, header, query param, content negotiation), breaking change classification, and deprecation with Sunset headers
- **assets/rest-api-template.py** — Production-ready FastAPI REST API template with CRUD, pagination, filtering, and error handling
- **assets/graphql-schema-template.graphql** — Complete GraphQL schema template with Relay pagination, input/payload pattern, subscriptions, and error handling
- **assets/openapi-template.yaml** — OpenAPI 3.0 spec template with authentication schemes, error responses, pagination, and rate limiting headers
- **assets/api-design-checklist.md** — Pre-implementation review checklist for REST and GraphQL APIs
