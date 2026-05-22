---
name: api-design-patterns
description: Comprehensive API design patterns covering REST, GraphQL, gRPC, versioning, authentication, and modern API best practices
license: Apache-2.0
compatibility: claude-code
metadata:
  version: 1.0.0
  category: universal
  related_skills: [graphql, typescript, nodejs-backend, django, fastapi, flask]
  token_budget:
    entry_point: 85
    full_content: 8500
  self_contained: true
tags: [api, rest, graphql, grpc, architecture, web, design-patterns]
progressive_disclosure:
  entry_point:
    summary: "Comprehensive API design patterns covering REST, GraphQL, gRPC, versioning, authentication, and modern API best practices"
    when_to_use: "When designing, implementing, or documenting APIs."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - authentication.md
    - graphql-patterns.md
    - grpc-patterns.md
    - rest-patterns.md
    - versioning-strategies.md
---
# API Design Patterns

Design robust, scalable APIs using proven patterns for REST, GraphQL, and gRPC with proper versioning, authentication, and error handling.

## Quick Reference

**API Style Selection**:
- REST: Resource-based CRUD, simple clients, HTTP-native caching
- GraphQL: Client-driven queries, complex data graphs, real-time subscriptions
- gRPC: High-performance RPC, microservices, strong typing, streaming

**Critical Patterns**:
- Versioning: URI (`/v1/users`), header (`Accept: application/vnd.api+json;version=1`), content negotiation
- Pagination: Offset (simple), cursor (stable), keyset (performant)
- Auth: OAuth2 (delegated), JWT (stateless), API keys (service-to-service)
- Rate limiting: Token bucket, fixed window, sliding window
- Idempotency: Idempotency keys, conditional requests, safe retry

**See references/ for deep dives**: `rest-patterns.md`, `graphql-patterns.md`, `grpc-patterns.md`, `versioning-strategies.md`, `authentication.md`

## Core Principles

### Universal API Design Standards

Apply these principles across all API styles:

**1. Consistency Over Cleverness**
- Follow established conventions for your API style
- Use predictable naming patterns (snake_case or camelCase, pick one)
- Maintain consistent error response formats
- Version breaking changes, never surprise clients

**2. Design for Evolution**
- Plan for versioning from day one
- Use optional fields with sensible defaults
- Deprecate gracefully with sunset dates
- Document breaking vs non-breaking changes

**3. Security by Default**
- Require authentication unless explicitly public
- Use HTTPS/TLS for all production endpoints
- Implement rate limiting and throttling
- Validate and sanitize all inputs
- Return minimal error details to clients

**4. Developer Experience First**
- Provide comprehensive documentation (OpenAPI, GraphQL schema)
- Return meaningful error messages with actionable guidance
- Use standard HTTP status codes correctly
- Include request IDs for debugging
- Offer SDKs and code generators

## API Style Decision Tree

### When to Choose REST

✅ **Use REST when:**
- Building CRUD-focused resource APIs
- Clients need HTTP caching (ETags, Cache-Control)
- Wide platform compatibility required (browsers, mobile, IoT)
- Simple, stateless client-server model fits
- Team familiar with HTTP/REST conventions

❌ **Avoid REST when:**
- Complex data fetching with nested relationships (N+1 queries)
- Real-time updates are primary use case
- Need strong typing and code generation
- High-performance RPC between microservices

**Example Use Cases**: Public APIs, mobile backends, traditional web services

### When to Choose GraphQL

✅ **Use GraphQL when:**
- Clients need flexible, client-driven queries
- Complex data graphs with nested relationships
- Multiple client types with different data needs
- Real-time subscriptions required
- Strong typing and schema validation needed

❌ **Avoid GraphQL when:**
- Simple CRUD operations dominate
- HTTP caching is critical (GraphQL uses POST)
- File uploads are primary feature (requires extensions)
- Team lacks GraphQL expertise
- Performance optimization is complex (N+1 problem)

**Example Use Cases**: Client-facing APIs, dashboards, mobile apps with varied UIs

### When to Choose gRPC

✅ **Use gRPC when:**
- Microservice-to-microservice communication
- High performance and low latency critical
- Bidirectional streaming needed
- Strong typing with Protocol Buffers
- Polyglot environments (language interop)

❌ **Avoid gRPC when:**
- Browser clients (limited support, needs grpc-web)
- HTTP/JSON required for compatibility
- Human-readable payloads preferred
- Simple request/response patterns

**Example Use Cases**: Internal microservices, streaming data, service mesh

## REST API Patterns

### Resource Naming

✅ **Good: Plural nouns, hierarchical**
```
GET    /users              # List users
GET    /users/123          # Get user
POST   /users              # Create user
PUT    /users/123          # Update user (full)
PATCH  /users/123          # Update user (partial)
DELETE /users/123          # Delete user
GET    /users/123/orders   # User's orders (sub-resource)
```

❌ **Bad: Verbs, mixed conventions**
```
GET    /getUsers           # Don't use verbs
POST   /user/create        # Don't use verbs
GET    /Users/123          # Don't capitalize
GET    /user/123           # Don't mix singular/plural
```

### HTTP Status Codes

**Success Codes**:
- `200 OK`: Successful GET, PUT, PATCH, DELETE with body
- `201 Created`: Successful POST, return Location header
- `202 Accepted`: Async operation started
- `204 No Content`: Successful DELETE, no body

**Client Error Codes**:
- `400 Bad Request`: Invalid input, validation error
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Authenticated but insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `409 Conflict`: State conflict (duplicate, version mismatch)
- `422 Unprocessable Entity`: Semantic validation error
- `429 Too Many Requests`: Rate limit exceeded

**Server Error Codes**:
- `500 Internal Server Error`: Unexpected error
- `502 Bad Gateway`: Upstream service error
- `503 Service Unavailable`: Temporary outage
- `504 Gateway Timeout`: Upstream timeout

### Error Response Format

✅ **Consistent error structure**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "INVALID_FORMAT"
      }
    ],
    "request_id": "req_abc123",
    "documentation_url": "https://api.example.com/docs/errors/validation"
  }
}
```

### Pagination Patterns

**Offset Pagination** (simple, familiar):
```
GET /users?limit=20&offset=40
```
✅ Use for: Small datasets, admin interfaces
❌ Avoid for: Large datasets (skips become expensive), real-time data

**Cursor Pagination** (stable, efficient):
```
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ
Response: { "data": [...], "next_cursor": "eyJpZCI6MTQzfQ" }
```
✅ Use for: Infinite scroll, real-time feeds, large datasets
❌ Avoid for: Random access, page numbers

**Keyset Pagination** (performant):
```
GET /users?limit=20&after_id=123
```
✅ Use for: Ordered data, database index friendly
❌ Avoid for: Complex sorting, multiple sort keys

See `references/rest-patterns.md` for filtering, sorting, field selection, HATEOAS

## GraphQL Patterns

### Schema Design

✅ **Good: Clear types, nullable by default**
```graphql
type User {
  id: ID!                    # Non-null ID
  email: String!             # Required field
  name: String               # Optional (nullable by default)
  createdAt: DateTime!
  orders: [Order!]!          # Non-null array of non-null orders
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

input CreateUserInput {
  email: String!
  name: String
}

type CreateUserPayload {
  user: User
  userEdge: UserEdge
  errors: [UserError!]
}
```

### Resolver Patterns

**Avoid N+1 Queries with DataLoader**:
```typescript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (userIds: string[]) => {
  const users = await db.users.findMany({ where: { id: { in: userIds } } });
  return userIds.map(id => users.find(u => u.id === id));
});

// Resolver batches queries automatically
const resolvers = {
  Order: {
    user: (order) => userLoader.load(order.userId)
  }
};
```

### Query Complexity Analysis

Prevent expensive queries:
```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  schema,
  validationRules: [
    createComplexityLimitRule(1000, {
      onCost: (cost) => console.log('Query cost:', cost),
    }),
  ],
});
```

See `references/graphql-patterns.md` for subscriptions, relay cursor connections, error handling

## gRPC Patterns

### Service Definition

```protobuf
syntax = "proto3";

package users.v1;

service UserService {
  rpc GetUser (GetUserRequest) returns (User) {}
  rpc ListUsers (ListUsersRequest) returns (ListUsersResponse) {}
  rpc CreateUser (CreateUserRequest) returns (User) {}
  rpc StreamUsers (StreamUsersRequest) returns (stream User) {}
  rpc BidiChat (stream ChatMessage) returns (stream ChatMessage) {}
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
}

message ListUsersResponse {
  repeated User users = 1;
  string next_page_token = 2;
}
```

### Error Handling

```go
import (
    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"
)

func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    if req.Id == "" {
        return nil, status.Error(codes.InvalidArgument, "user ID is required")
    }

    user, err := s.db.GetUser(ctx, req.Id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, status.Error(codes.NotFound, "user not found")
        }
        return nil, status.Error(codes.Internal, "database error")
    }

    return user, nil
}
```

See `references/grpc-patterns.md` for streaming, interceptors, metadata, health checks

## Versioning Strategies

### URI Versioning (Simple, Explicit)

✅ **Most common, easy to understand**
```
GET /v1/users/123
GET /v2/users/123
```

**Pros**: Clear, easy to route, browser-friendly
**Cons**: Couples version to URL, duplicates routes

### Header Versioning (Clean URLs)

```
GET /users/123
Accept: application/vnd.myapi.v2+json
```

**Pros**: Clean URLs, version separate from resource
**Cons**: Less visible, harder to test manually

### Content Negotiation (Granular)

```
GET /users/123
Accept: application/vnd.myapi.user.v2+json
```

**Pros**: Resource-level versioning, backward compatible
**Cons**: Complex, harder to implement

### Version Deprecation Process

```json
{
  "version": "1.0",
  "deprecated": true,
  "sunset_date": "2025-12-31",
  "migration_guide": "https://docs.api.com/v1-to-v2",
  "replacement_version": "2.0"
}
```

**Include deprecation warnings**:
```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
Link: <https://docs.api.com/v1-to-v2>; rel="deprecation"
```

See `references/versioning-strategies.md` for detailed migration patterns

## Authentication & Authorization

### OAuth 2.0 (Delegated Access)

**Use for**: Third-party access, user consent, token refresh

**Authorization Code Flow** (most secure for web/mobile):
```
1. Client redirects to /authorize
2. User authenticates, grants permissions
3. Auth server redirects to callback with code
4. Client exchanges code for access token
5. Client uses access token for API requests
```

```http
# Request token
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=AUTH_CODE
&redirect_uri=https://client.com/callback
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET

# Response
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
  "scope": "read write"
}

# Use token
GET /v1/users/me
Authorization: Bearer eyJhbGc...
```

### JWT (Stateless Auth)

**Use for**: Microservices, stateless API auth, short-lived tokens

✅ **Good: Minimal claims, short expiry**
```json
{
  "sub": "user_123",
  "iat": 1516239022,
  "exp": 1516242622,
  "scope": "read:users write:orders"
}
```

**Validation**:
```typescript
import jwt from 'jsonwebtoken';

const token = req.headers.authorization?.split(' ')[1];
const payload = jwt.verify(token, process.env.JWT_SECRET);
req.userId = payload.sub;
```

### API Keys (Service-to-Service)

**Use for**: Server-to-server, CLI tools, webhooks

```http
GET /v1/users
X-API-Key: sk_live_abc123...

# Or query parameter (less secure)
GET /v1/users?api_key=sk_live_abc123
```

**Key Practices**:
- Prefix keys with environment (`sk_live_`, `sk_test_`)
- Hash keys before storage (bcrypt, scrypt)
- Allow key rotation without downtime
- Support multiple keys per user
- Rate limit per key

See `references/authentication.md` for API key rotation, scopes, RBAC

## Rate Limiting

### Token Bucket (Burst-Friendly)

```
Bucket: 100 tokens, refill 10/second
Request costs 1 token
Allows bursts up to bucket size
```

**Headers**:
```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1640995200
```

**429 Response**:
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640995200

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds.",
    "limit": 100,
    "reset_at": "2025-01-01T00:00:00Z"
  }
}
```

### Sliding Window (Fair Distribution)

Counts requests in rolling time window. More accurate than fixed window.

### Per-User vs Per-IP

- **Per-User**: Authenticated requests, fair quotas
- **Per-IP**: Unauthenticated requests, prevent abuse
- **Combined**: Both limits, take stricter

## Idempotency

### Idempotent Methods (HTTP Spec)

**Naturally Idempotent**: GET, PUT, DELETE, HEAD, OPTIONS
**Not Idempotent**: POST, PATCH

### Idempotency Keys

Make POST requests idempotent:
```http
POST /v1/payments
Idempotency-Key: uuid-or-client-generated-key
Content-Type: application/json

{
  "amount": 1000,
  "currency": "USD",
  "customer": "cust_123"
}
```

**Server behavior**:
1. First request: Process and store result with key
2. Duplicate request (same key): Return stored result (200 or 201)
3. Different request (same key): Return 409 Conflict

**Implementation**:
```typescript
const idempotencyKey = req.headers['idempotency-key'];
if (idempotencyKey) {
  const cached = await redis.get(`idempotency:${idempotencyKey}`);
  if (cached) {
    return res.status(cached.status).json(cached.body);
  }
}

const result = await processPayment(req.body);
await redis.setex(`idempotency:${idempotencyKey}`, 86400, {
  status: 201,
  body: result
});
```

### Conditional Requests

Use ETags for safe updates:
```http
# Get resource with ETag
GET /v1/users/123
Response: ETag: "abc123"

# Update only if unchanged
PUT /v1/users/123
If-Match: "abc123"

# 412 Precondition Failed if ETag changed
```

## Caching Strategies

### HTTP Caching Headers

```http
# Public, cacheable for 1 hour
Cache-Control: public, max-age=3600

# Private (user-specific), revalidate
Cache-Control: private, must-revalidate, max-age=0

# No caching
Cache-Control: no-store, no-cache, must-revalidate
```

### ETag Validation

```http
# Server returns ETag
GET /v1/users/123
Response:
  ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
  Cache-Control: max-age=3600

# Client conditional request
GET /v1/users/123
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"

# 304 Not Modified if unchanged (saves bandwidth)
HTTP/1.1 304 Not Modified
```

### Last-Modified

```http
GET /v1/users/123
Response:
  Last-Modified: Wed, 21 Oct 2025 07:28:00 GMT

# Conditional request
GET /v1/users/123
If-Modified-Since: Wed, 21 Oct 2025 07:28:00 GMT

# 304 Not Modified if not modified
```

## Webhooks

### Event Delivery

```http
POST https://client.com/webhooks/payments
Content-Type: application/json
X-Webhook-Signature: sha256=abc123...
X-Webhook-Id: evt_abc123
X-Webhook-Timestamp: 1640995200

{
  "id": "evt_abc123",
  "type": "payment.succeeded",
  "created": 1640995200,
  "data": {
    "object": {
      "id": "pay_123",
      "amount": 1000,
      "status": "succeeded"
    }
  }
}
```

### Signature Verification

```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(`sha256=${expectedSignature}`)
  );
}
```

### Retry Strategy

- **Exponential backoff**: 1s, 2s, 4s, 8s, 16s, 32s, 64s
- **Timeout**: 5-30 seconds per attempt
- **Max attempts**: 3-7 attempts
- **Dead letter queue**: Store failed events
- **Manual retry**: UI for re-sending failed events

## API Documentation

### OpenAPI/Swagger (REST)

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
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
        name:
          type: string
```

### GraphQL Schema (Self-Documenting)

GraphQL introspection provides automatic documentation. Use descriptions:

```graphql
"""
Represents a user account in the system.
Created via the createUser mutation.
"""
type User {
  """Unique identifier for the user"""
  id: ID!

  """Email address, must be unique"""
  email: String!

  """Optional display name"""
  name: String
}
```

### API Documentation Best Practices

1. **Interactive examples**: Provide working code samples
2. **Authentication guide**: Step-by-step auth setup
3. **Error catalog**: Document all error codes with examples
4. **Rate limits**: Clearly state limits and headers
5. **Changelog**: Track breaking and non-breaking changes
6. **Migration guides**: Version upgrade instructions
7. **SDKs**: Provide client libraries for popular languages

## Anti-Patterns

❌ **Over-fetching (REST)**: Returning entire objects when fields are unused
✅ **Solution**: Support field selection (`?fields=id,name,email`)

❌ **Under-fetching (REST)**: Requiring multiple requests for related data
✅ **Solution**: Support expansion (`?expand=orders,profile`) or use GraphQL

❌ **Chatty APIs**: Too many round-trips for common operations
✅ **Solution**: Batch endpoints, compound documents, or GraphQL

❌ **Ignoring HTTP semantics**: Using GET for mutations, wrong status codes
✅ **Solution**: Follow HTTP spec, use correct methods and status codes

❌ **Exposing internal structure**: URLs/schemas mirror database
✅ **Solution**: Design resource-oriented APIs independent of storage

❌ **Missing versioning**: Breaking changes without version increments
✅ **Solution**: Version from day one, never break existing versions

❌ **Poor error messages**: Generic "An error occurred"
✅ **Solution**: Specific, actionable error messages with codes

❌ **No rate limiting**: APIs vulnerable to abuse
✅ **Solution**: Implement rate limiting from the start

## Testing Strategies

### Contract Testing

```typescript
// Pact contract test
import { PactV3 } from '@pact-foundation/pact';

const provider = new PactV3({
  consumer: 'FrontendApp',
  provider: 'UserAPI'
});

it('gets a user by ID', () => {
  provider
    .given('user 123 exists')
    .uponReceiving('a request for user 123')
    .withRequest({
      method: 'GET',
      path: '/users/123'
    })
    .willRespondWith({
      status: 200,
      body: { id: '123', email: 'user@example.com' }
    });
});
```

### Load Testing

```javascript
// k6 load test
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m', target: 20 },
    { duration: '10s', target: 0 }
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01']    // <1% errors
  }
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500
  });
}
```

## Related Skills

- **graphql**: Deep GraphQL schema design, resolvers, Apollo Server
- **typescript**: Type-safe API clients and servers
- **nodejs-backend**: Express/Fastify REST API implementation
- **django**: Django REST Framework patterns
- **fastapi**: FastAPI Python REST/GraphQL APIs
- **flask**: Flask-RESTful patterns

## References

- **rest-patterns.md**: Deep REST coverage (HATEOAS, filtering, field selection)
- **graphql-patterns.md**: GraphQL subscriptions, relay cursor connections, federation
- **grpc-patterns.md**: Streaming patterns, interceptors, service mesh integration
- **versioning-strategies.md**: Detailed versioning approaches and migration patterns
- **authentication.md**: OAuth flows, JWT best practices, API key rotation, RBAC

## Additional Resources

- [REST API Design Rulebook](https://www.oreilly.com/library/view/rest-api-design/9781449317904/) - O'Reilly REST guide
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/) - Official GraphQL guide
- [gRPC Best Practices](https://grpc.io/docs/guides/performance/) - Official gRPC guide
- [RFC 7807: Problem Details for HTTP APIs](https://tools.ietf.org/html/rfc7807) - Standard error format
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) - REST documentation standard
