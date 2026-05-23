---
name: designing-apis
description: Design APIs that are secure, scalable, and maintainable using RESTful, GraphQL, and event-driven patterns. Use when designing new APIs, evolving existing APIs, or establishing API standards for teams.
---

# Designing APIs

Design well-structured, scalable APIs using REST, GraphQL, or event-driven patterns. Focus on resource design, versioning, error handling, pagination, rate limiting, and security.

## When to Use This Skill

Use when:
- Designing a new REST, GraphQL, or event-driven API
- Establishing API design standards for a team or organization
- Choosing between REST, GraphQL, WebSockets, or message queues
- Planning API versioning and breaking change management
- Defining error response formats and HTTP status code usage
- Implementing pagination, filtering, and rate limiting patterns
- Designing OAuth2 flows or API key authentication
- Creating OpenAPI or AsyncAPI specifications

Do NOT use for:
- Implementation code (use `api-patterns` skill for Express, FastAPI code)
- Authentication implementation (use `auth-security` skill for JWT, sessions)
- API testing strategies (use `testing-strategies` skill)
- API deployment and infrastructure (use `deploying-applications` skill)

## Core Design Principles

### Resource-Oriented Design (REST)

Use nouns for resources, not verbs in URLs:
```
✓ GET    /users              List users
✓ GET    /users/123          Get user 123
✓ POST   /users              Create user
✓ PATCH  /users/123          Update user 123
✓ DELETE /users/123          Delete user 123

✗ GET    /getUsers
✗ POST   /createUser
```

Nest resources for relationships (limit depth to 2-3 levels):
```
✓ GET /users/123/posts
✓ GET /users/123/posts/456/comments
✗ GET /users/123/posts/456/comments/789/replies  (too deep)
```

For complete REST patterns, see references/rest-design.md

### HTTP Method Semantics

| Method | Idempotent | Safe | Use For | Success Status |
|--------|-----------|------|---------|----------------|
| GET | Yes | Yes | Read resource | 200 OK |
| POST | No | No | Create resource | 201 Created |
| PUT | Yes | No | Replace entire resource | 200 OK, 204 No Content |
| PATCH | No | No | Update specific fields | 200 OK, 204 No Content |
| DELETE | Yes | No | Remove resource | 204 No Content, 200 OK |

Idempotent means multiple identical requests have the same effect as one request.

### HTTP Status Codes

**Success (2xx):**
- 200 OK, 201 Created, 204 No Content

**Client Errors (4xx):**
- 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
- 409 Conflict, 422 Unprocessable Entity, 429 Too Many Requests

**Server Errors (5xx):**
- 500 Internal Server Error, 503 Service Unavailable

For complete status code guide, see references/rest-design.md

## API Style Selection

### Decision Matrix

| Factor | REST | GraphQL | WebSocket | Message Queue |
|--------|------|---------|-----------|---------------|
| Public API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| Complex Data | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Caching | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |
| Real-time | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

### Quick Selection

- **Public API, CRUD operations** → REST
- **Complex data, flexible queries** → GraphQL
- **Real-time, bidirectional** → WebSockets
- **Event-driven, microservices** → Message Queue

For detailed protocol selection, see references/protocol-selection.md

## API Versioning

### URL Path Versioning (Recommended)

```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

Pros: Explicit, easy to implement and test
Cons: Maintenance overhead

### Alternative Strategies

- Header-Based: `Accept-Version: v1`
- Media Type: `Accept: application/vnd.example.v1+json`
- Query Parameter: `?version=1` (not recommended)

### Breaking Change Management

Timeline:
1. Month 0: Announce deprecation
2. Months 1-3: Migration period
3. Months 4-6: Deprecation warnings
4. Month 6: Sunset (return 410 Gone)

Include deprecation headers:
```http
Deprecation: true
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
Link: </api/v2/users>; rel="successor-version"
```

For complete versioning guide, see references/versioning-strategies.md

## Error Response Standards

### RFC 7807 Problem Details (Recommended)

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 400,
  "detail": "One or more fields failed validation",
  "errors": [
    {
      "field": "email",
      "message": "Must be a valid email address",
      "code": "INVALID_EMAIL"
    }
  ]
}
```

Content-Type: `application/problem+json`

For complete error patterns, see references/error-handling.md

## Pagination Patterns

### Strategy Selection

| Scenario | Strategy | Why |
|----------|----------|-----|
| Small datasets (<1000) | Offset-based | Simple, page numbers |
| Large datasets (>10K) | Cursor-based | Efficient, handles writes |
| Sorted data | Keyset | Consistent results |
| Real-time feeds | Cursor-based | Handles new items |

### Offset-Based (Simple)

```http
GET /users?limit=20&offset=40
```

Response includes: `limit`, `offset`, `total`, `currentPage`

### Cursor-Based (Scalable)

```http
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ==
```

Cursor is base64-encoded JSON with position information.
Response includes: `nextCursor`, `hasNext`

For implementation details, see references/pagination-patterns.md

## Rate Limiting

### Token Bucket Algorithm

- Each user has bucket with tokens
- Each request consumes 1 token
- Tokens refill at constant rate
- Empty bucket rejects request

### Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1672531200
```

When exceeded (429):
```http
Retry-After: 3600
```

### Strategies

- Per User: 100 requests/hour
- Per API Key: 1000 requests/hour
- Per IP: 50 requests/hour (unauthenticated)
- Tiered: Free (100/hr), Pro (1000/hr), Enterprise (10000/hr)

For implementation patterns, see references/rate-limiting.md

## API Security Design

### OAuth 2.0 Flows

**Authorization Code Flow (Web Apps):**
1. Redirect user to authorization server
2. User grants permission
3. Exchange code for access token
4. Use token for API requests

**Client Credentials Flow (Service-to-Service):**
1. Authenticate with client ID and secret
2. Receive access token
3. Use token for API requests

### Scope-Based Authorization

Define granular permissions:
```
read:users    - Read user data
write:users   - Create/update users
delete:users  - Delete users
admin:*       - Full admin access
```

### API Key Management

Use header-based keys:
```http
X-API-Key: sk_live_abc123xyz456
```

Best practices:
- Prefix with environment: `sk_live_*`, `sk_test_*`
- Store hashed keys only
- Support key rotation
- Track last-used timestamp

For complete security patterns, see references/authentication.md

## OpenAPI Specification

### Basic Structure

```yaml
openapi: 3.1.0
info:
  title: User Management API
  version: 2.0.0

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

OpenAPI enables:
- Code generation (server stubs, client SDKs)
- Validation (request/response checking)
- Mock servers (testing against spec)
- Documentation (interactive docs)

For complete OpenAPI examples, see examples/openapi/

## AsyncAPI Specification

### Event-Driven APIs

AsyncAPI defines message-based APIs (WebSockets, Kafka, MQTT):

```yaml
asyncapi: 3.0.0
info:
  title: Order Events API

channels:
  orders/created:
    address: orders.created
    messages:
      orderCreated:
        payload:
          type: object
          properties:
            orderId:
              type: string
```

For AsyncAPI examples, see examples/asyncapi/

## GraphQL Design

### Schema Structure

```graphql
type User {
  id: ID!
  username: String!
  posts(limit: Int): [Post!]!
}

type Query {
  user(id: ID!): User
  users(limit: Int): [User!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}
```

### N+1 Problem Solution

Use DataLoader to batch requests:
```javascript
const userLoader = new DataLoader(async (userIds) => {
  // Single query for all users
  const users = await db.users.findByIds(userIds);
  return userIds.map(id => users.find(u => u.id === id));
});
```

For GraphQL patterns, see references/graphql-design.md

## Quick Reference Tables

### Pagination Strategy Selection

| Scenario | Strategy |
|----------|----------|
| Small datasets | Offset-based |
| Large datasets | Cursor-based |
| Sorted data | Keyset |
| Real-time feeds | Cursor-based |

### Versioning Strategy Selection

| Factor | URL Path | Header | Media Type |
|--------|----------|--------|------------|
| Visibility | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Simplicity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Best For | Most APIs | Internal APIs | Content negotiation |

## Integration with Other Skills

- **api-patterns**: Implement API designs in Express, FastAPI, Go
- **auth-security**: Implement OAuth2, JWT, session management
- **database-design**: Design database schemas for API resources
- **testing-strategies**: API testing (integration, contract, load)
- **deploying-applications**: Deploy and scale APIs
- **observability**: Monitor API performance and errors

## Additional Resources

**Detailed guidance:**
- references/rest-design.md - RESTful patterns and best practices
- references/graphql-design.md - GraphQL schema and resolver patterns
- references/versioning-strategies.md - Comprehensive versioning guide
- references/error-handling.md - RFC 7807 implementation details
- references/pagination-patterns.md - Pagination implementation patterns
- references/rate-limiting.md - Rate limiting algorithms and strategies
- references/authentication.md - OAuth2, API keys, scopes
- references/protocol-selection.md - Choosing the right API style

**Working examples:**
- examples/openapi/ - Complete OpenAPI 3.1 specifications
- examples/asyncapi/ - Event-driven API specifications
- examples/graphql/ - GraphQL schemas and patterns

**Validation and tooling:**
- scripts/validate-openapi.sh - Validate OpenAPI specifications
