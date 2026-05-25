---
name: api-design
description: REST/GraphQL/gRPC API design best practices. Use when designing APIs, defining contracts, handling versioning. Covers OpenAPI 3.2, GraphQL Federation, gRPC streaming.
---
# API Design

## Core Principles

- **Contract-First** — Define API spec before implementation
- **OpenAPI 3.2** — Use OpenAPI for REST API documentation
- **URL Versioning** — Version in path `/v1/`, with Sunset headers
- **Idempotency** — PUT/DELETE must be idempotent, POST uses Idempotency-Key
- **Cursor Pagination** — Avoid offset-based pagination
- **RFC 7807 Errors** — Standard Problem Details format
- **No backwards compatibility** — Delete, don't deprecate

---

## Quick Reference

### When to Use What

| Scenario | Choice | Reason |
|----------|--------|--------|
| Public API / MVP | REST | Simple, universal, easy debugging |
| Frontend-driven / Mobile | GraphQL | Fetch exactly what you need |
| Microservices internal | gRPC | High performance, strong typing |
| Real-time data | gRPC / GraphQL Subscriptions | Bidirectional streaming |

---

## REST API Design

### Resource Naming

```
# Good
GET  /users              # List users
GET  /users/123          # Get user
POST /users              # Create user
PUT  /users/123          # Replace user
PATCH /users/123         # Update user
DELETE /users/123        # Delete user

# Nested resources
GET /users/123/orders    # User's orders

# Actions (when CRUD doesn't fit)
POST /users/123/activate # Action on resource

# Query parameters for filtering
GET /users?status=active&role=admin&limit=20
```

### HTTP Methods

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read | Yes | Yes |
| POST | Create | No | No |
| PUT | Replace | Yes | No |
| PATCH | Update | No | No |
| DELETE | Remove | Yes | No |

### Status Codes

```
# Success
200 OK              - Successful GET/PUT/PATCH
201 Created         - Successful POST (include Location header)
204 No Content      - Successful DELETE

# Client Errors
400 Bad Request     - Malformed request syntax
401 Unauthorized    - Missing/invalid authentication
403 Forbidden       - Authenticated but not authorized
404 Not Found       - Resource doesn't exist
409 Conflict        - Duplicate/conflict (e.g., unique constraint)
422 Unprocessable   - Validation failed
429 Too Many        - Rate limited

# Server Errors
500 Internal Error  - Unexpected server error
503 Unavailable     - Service temporarily down
```

### Error Response (RFC 7807)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request contains invalid parameters",
  "instance": "/users/123",
  "errors": [
    { "field": "email", "message": "Invalid email format" },
    { "field": "age", "message": "Must be positive integer" }
  ]
}
```

### Pagination (Cursor-Based)

```json
// Request
GET /users?limit=20&cursor=eyJpZCI6MTAwfQ

// Response
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIwfQ",
    "prev_cursor": "eyJpZCI6ODB9",
    "has_next": true,
    "has_prev": true,
    "limit": 20
  }
}
```

### Versioning

```
# URL versioning (recommended)
GET /v1/users
GET /v2/users

# Deprecation headers
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
Deprecation: true
Link: </v2/users>; rel="successor-version"
```

### Idempotency

```
# For non-idempotent operations (POST)
POST /orders
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000

# Server stores result and returns same response for duplicate key
```

---

## GraphQL Design

### Schema Principles

- **Domain-driven** — Schema reflects business domain, not database
- **Descriptive names** — Clear field/type names for monitoring
- **Limit nesting** — Deep nesting hurts performance
- **Use @key** — Mark entity identifiers for Federation

### Type Definitions

```graphql
type Query {
  user(id: ID!): User
  users(first: Int, after: String, filter: UserFilter): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

type User @key(fields: "id") {
  id: ID!
  email: String!
  name: String!
  orders(first: Int, after: String): OrderConnection!
  createdAt: DateTime!
}

# Relay-style pagination
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
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
```

### Error Handling

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

# Union for typed errors
union CreateUserPayload = User | ValidationError | ConflictError

type ValidationError {
  message: String!
  field: String
  code: String!
}

type ConflictError {
  message: String!
  existingId: ID!
}
```

### N+1 Prevention

```typescript
// Use DataLoader for batching
const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await db.user.findMany({
    where: { id: { in: ids } }
  });
  return ids.map(id => users.find(u => u.id === id));
});

// Resolver
const resolvers = {
  Order: {
    user: (order) => userLoader.load(order.userId),
  },
};
```

---

## gRPC Design

### Proto Definition

```protobuf
syntax = "proto3";

package api.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

service UserService {
  // Unary
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);

  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream User);

  // Client streaming
  rpc BatchCreateUsers(stream CreateUserRequest) returns (BatchCreateResponse);

  // Bidirectional streaming
  rpc SyncUsers(stream UserUpdate) returns (stream UserUpdate);
}

message User {
  string id = 1;
  string email = 2;
  string name = 3;
  google.protobuf.Timestamp created_at = 4;
}

message GetUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  UserFilter filter = 3;
}

message UserFilter {
  optional string status = 1;
  optional string role = 2;
}
```

### Error Handling

```protobuf
// Use Google's richer error model
import "google/rpc/status.proto";
import "google/rpc/error_details.proto";

// For streaming: embed errors in response
message StreamResponse {
  oneof result {
    User user = 1;
    StreamError error = 2;
  }
}

message StreamError {
  string code = 1;
  string message = 2;
  map<string, string> details = 3;
}
```

### Deadlines & Retries

```typescript
// Always set deadlines
const deadline = new Date();
deadline.setSeconds(deadline.getSeconds() + 5);

const user = await client.getUser(
  { id: '123' },
  { deadline }
);

// Configure retry policy
const retryPolicy = {
  maxAttempts: 3,
  initialBackoff: '0.1s',
  maxBackoff: '1s',
  backoffMultiplier: 2,
  retryableStatusCodes: ['UNAVAILABLE', 'DEADLINE_EXCEEDED'],
};
```

---

## Rate Limiting

### Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
Retry-After: 60
```

### Response (429)

```json
{
  "type": "https://api.example.com/errors/rate-limited",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded the rate limit of 100 requests per minute",
  "retryAfter": 60
}
```

---

## Checklist

```markdown
## Design
- [ ] API spec defined before implementation
- [ ] Resources use plural nouns
- [ ] Correct HTTP methods/status codes
- [ ] RFC 7807 error format

## Features
- [ ] Cursor-based pagination
- [ ] Rate limiting with headers
- [ ] Idempotency keys for POST
- [ ] API versioning strategy

## Documentation
- [ ] OpenAPI/GraphQL schema published
- [ ] Examples for all endpoints
- [ ] Error codes documented

## Operations
- [ ] Request/response logging
- [ ] Latency and error rate metrics
- [ ] Deprecation notices for old versions
```

---

## See Also

- [reference/rest.md](reference/rest.md) — REST deep dive
- [reference/graphql.md](reference/graphql.md) — GraphQL patterns
- [reference/grpc.md](reference/grpc.md) — gRPC patterns
- [reference/comparison.md](reference/comparison.md) — Selection guide
