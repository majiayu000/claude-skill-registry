---
name: api-design-patterns
description: Comprehensive REST and GraphQL API design patterns with versioning, pagination, error handling, and HATEOAS principles. Use when designing APIs, defining endpoints, or architecting service contracts requiring production-grade patterns.
---

# API Design Patterns

Expert guidance for designing scalable, maintainable REST and GraphQL APIs with industry-standard patterns for versioning, pagination, error handling, authentication, and service contracts.

## When to Use This Skill

- Designing new REST or GraphQL APIs from scratch
- Refactoring existing APIs for better scalability and consistency
- Defining service contracts for microservices architectures
- Implementing versioning strategies for API evolution
- Standardizing error handling and response formats across services
- Designing pagination for large datasets
- Implementing HATEOAS or hypermedia-driven APIs
- Creating API specifications (OpenAPI, GraphQL Schema)

## Core Principles

### 1. Resource-Oriented Design (REST)

**URLs represent resources, not actions:**
```
✓ GET    /users/123
✓ POST   /users
✓ PUT    /users/123
✓ DELETE /users/123

✗ GET    /getUser?id=123
✗ POST   /createUser
✗ POST   /deleteUser
```

**Use HTTP methods semantically:**
- GET: Retrieve resource(s), idempotent, cacheable
- POST: Create resource, non-idempotent
- PUT: Replace entire resource, idempotent
- PATCH: Partial update, idempotent
- DELETE: Remove resource, idempotent

### 2. Consistent Naming Conventions

```
Resources:        /users, /orders, /products (plural nouns)
Nested:           /users/123/orders
Collections:      /users?status=active&page=2
Sub-resources:    /users/123/settings
Actions (rare):   /users/123/activate (POST)
```

### 3. HTTP Status Codes

**Success:**
- 200 OK: Standard response for GET, PUT, PATCH
- 201 Created: Resource created (POST), return Location header
- 202 Accepted: Async processing started
- 204 No Content: Success with no response body (DELETE)

**Client Errors:**
- 400 Bad Request: Invalid syntax or validation failure
- 401 Unauthorized: Authentication required or failed
- 403 Forbidden: Authenticated but insufficient permissions
- 404 Not Found: Resource doesn't exist
- 409 Conflict: State conflict (duplicate, version mismatch)
- 422 Unprocessable Entity: Semantic validation failure
- 429 Too Many Requests: Rate limit exceeded

**Server Errors:**
- 500 Internal Server Error: Unexpected server failure
- 502 Bad Gateway: Upstream service failure
- 503 Service Unavailable: Temporary overload or maintenance
- 504 Gateway Timeout: Upstream timeout

## Versioning Strategies

### URI Versioning (Most Common)
```
GET /v1/users/123
GET /v2/users/123

Pros: Clear, easy to route, browser-testable
Cons: URL proliferation, cache fragmentation
When: Public APIs, major breaking changes
```

### Header Versioning
```
GET /users/123
Accept: application/vnd.myapi.v2+json

Pros: Clean URLs, content negotiation
Cons: Harder to test, caching complexity
When: Internal APIs, minor version differences
```

### Query Parameter Versioning
```
GET /users/123?version=2

Pros: Simple, backward compatible
Cons: Pollutes query space, inconsistent
When: Rare, legacy compatibility
```

### Deprecation Headers
```http
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Deprecation: true
Link: <https://api.example.com/v2/users/123>; rel="successor-version"
```

## Pagination Patterns

### Offset-Based Pagination
```
GET /users?limit=20&offset=40

Response:
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 1543
  },
  "links": {
    "next": "/users?limit=20&offset=60",
    "prev": "/users?limit=20&offset=20"
  }
}

Pros: Simple, predictable, supports total count
Cons: Inconsistent with concurrent writes, performance degrades
When: Small datasets, stable data, admin UIs
```

### Cursor-Based Pagination
```
GET /users?limit=20&cursor=eyJpZCI6MTIzfQ

Response:
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTQzfQ",
    "has_more": true
  },
  "links": {
    "next": "/users?limit=20&cursor=eyJpZCI6MTQzfQ"
  }
}

Pros: Consistent with writes, scalable, efficient
Cons: No total count, can't jump to arbitrary page
When: Large datasets, real-time feeds, infinite scroll
```

### Keyset Pagination (Seek Method)
```
GET /users?limit=20&after_id=123&created_after=2024-01-01T00:00:00Z

Pros: Most performant, index-friendly
Cons: Requires sortable field, complex queries
When: Very large datasets, time-series data
```

## Error Response Format

### Standard Error Schema
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email format is invalid"
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Age must be between 18 and 120"
      }
    ],
    "request_id": "req_a3f7c9b2",
    "timestamp": "2024-01-15T10:30:00Z",
    "documentation_url": "https://docs.api.com/errors/VALIDATION_ERROR"
  }
}
```

### Error Code Patterns
```
Format: CATEGORY_SPECIFIC_REASON

Authentication:
- AUTH_MISSING_TOKEN
- AUTH_INVALID_TOKEN
- AUTH_EXPIRED_TOKEN

Authorization:
- AUTHZ_INSUFFICIENT_PERMISSIONS
- AUTHZ_RESOURCE_FORBIDDEN

Validation:
- VALIDATION_MISSING_FIELD
- VALIDATION_INVALID_FORMAT
- VALIDATION_OUT_OF_RANGE

Business Logic:
- BUSINESS_DUPLICATE_EMAIL
- BUSINESS_INSUFFICIENT_BALANCE
- BUSINESS_OPERATION_NOT_ALLOWED

System:
- SYSTEM_INTERNAL_ERROR
- SYSTEM_SERVICE_UNAVAILABLE
- SYSTEM_RATE_LIMIT_EXCEEDED
```

## Filtering and Searching

### Query Parameters for Filtering
```
GET /users?status=active&role=admin&created_after=2024-01-01

GET /users?search=john&fields=name,email

GET /users?sort=-created_at,name  # - prefix for descending
```

### Complex Filtering (FIQL/RSQL)
```
GET /users?filter=status==active;role==admin,role==moderator
               # AND between semicolons, OR between commas

GET /products?filter=price>100;price<500;category==electronics
```

### Full-Text Search
```
GET /users?q=john+smith&fields=name,bio,company

Response includes relevance scoring:
{
  "data": [
    {
      "id": 123,
      "name": "John Smith",
      "_score": 0.95
    }
  ]
}
```

## Field Selection (Sparse Fieldsets)

```
GET /users/123?fields=id,name,email

Response:
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}

# Nested resources
GET /users/123?fields=id,name,profile(avatar,bio)

Benefits:
- Reduced payload size
- Faster response times
- Lower bandwidth consumption
- Better mobile performance
```

## HATEOAS (Hypermedia)

### HAL (Hypertext Application Language)
```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "_links": {
    "self": { "href": "/users/123" },
    "orders": { "href": "/users/123/orders" },
    "update": { "href": "/users/123", "method": "PUT" },
    "delete": { "href": "/users/123", "method": "DELETE" }
  },
  "_embedded": {
    "recent_orders": [
      {
        "id": 456,
        "total": 99.99,
        "_links": {
          "self": { "href": "/orders/456" }
        }
      }
    ]
  }
}
```

### JSON:API Format
```json
{
  "data": {
    "type": "users",
    "id": "123",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "relationships": {
      "orders": {
        "links": {
          "self": "/users/123/relationships/orders",
          "related": "/users/123/orders"
        }
      }
    },
    "links": {
      "self": "/users/123"
    }
  }
}
```

## Rate Limiting Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1705320000
Retry-After: 3600

# Standard (RFC 6585)
RateLimit-Limit: 1000
RateLimit-Remaining: 742
RateLimit-Reset: 3600
```

## Authentication Patterns

### Bearer Token (OAuth 2.0, JWT)
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

Pros: Stateless, scalable, standard
Cons: Token size, revocation complexity
When: Modern APIs, microservices
```

### API Key
```http
X-API-Key: ak_live_a3f7c9b2d8e1f4g6h9

Pros: Simple, server-side management
Cons: Less secure, harder to scope
When: Internal services, admin APIs
```

### Basic Auth
```http
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=

Pros: Simple, built-in browser support
Cons: Credentials in every request
When: Internal tools, development only
```

## Idempotency

### Idempotency Keys (POST)
```http
POST /payments
Idempotency-Key: a3f7c9b2-d8e1-4f6g-h9i0-j1k2l3m4n5o6
Content-Type: application/json

{
  "amount": 100.00,
  "currency": "USD",
  "description": "Payment for order #123"
}

# Server stores key + response for 24 hours
# Duplicate requests return cached response with 200 OK
```

### Natural Idempotency
```
PUT /users/123          # Always idempotent
DELETE /users/123       # Idempotent (404 on repeat)
POST /users/123/follow  # Use PUT for idempotency
```

## Caching Strategies

### ETags (Conditional Requests)
```http
# Initial request
GET /users/123
ETag: "a3f7c9b2"

# Subsequent request
GET /users/123
If-None-Match: "a3f7c9b2"

# Response if unchanged:
304 Not Modified
```

### Cache-Control Headers
```http
# Never cache
Cache-Control: no-store

# Cache for 1 hour, revalidate
Cache-Control: max-age=3600, must-revalidate

# Cache forever (immutable)
Cache-Control: public, max-age=31536000, immutable
```

## GraphQL Patterns

### Query Structure
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    orders(first: 10) {
      edges {
        node {
          id
          total
          status
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

### Error Handling
```json
{
  "data": {
    "user": null
  },
  "errors": [
    {
      "message": "User not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND",
        "userId": "123"
      }
    }
  ]
}
```

### Mutation Patterns
```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      name
      email
    }
    errors {
      field
      message
    }
  }
}
```

## Best Practices Summary

1. **Consistency**: Follow conventions across all endpoints
2. **Versioning**: Plan deprecation strategy from day one
3. **Documentation**: Use OpenAPI/GraphQL schemas, keep updated
4. **Error Handling**: Detailed, actionable error messages with codes
5. **Security**: Always use HTTPS, validate inputs, rate limit
6. **Performance**: Implement caching, pagination, field selection
7. **Monitoring**: Log request IDs, track latency and error rates
8. **Backward Compatibility**: Additive changes only within versions
9. **Testing**: Contract tests, integration tests, load tests
10. **Documentation**: Interactive docs (Swagger UI, GraphQL Playground)

## Anti-Patterns to Avoid

1. **Chatty APIs**: Too many round trips (use batching, GraphQL)
2. **Over-fetching**: Returning unnecessary data (use field selection)
3. **Under-fetching**: Requiring multiple calls (use includes/embeds)
4. **Leaking Implementation**: Exposing DB structure in API
5. **Poor Error Messages**: Generic errors without details
6. **Breaking Changes**: Modifying existing fields without versioning
7. **No Rate Limiting**: Allowing resource exhaustion
8. **Missing Documentation**: Undocumented endpoints and parameters
9. **Inconsistent Naming**: Mixed conventions across endpoints
10. **Ignoring HTTP Semantics**: Misusing status codes and methods

## Resources

- **REST**: Roy Fielding's dissertation, RFC 7231 (HTTP semantics)
- **OpenAPI**: https://spec.openapis.org/oas/latest.html
- **GraphQL**: https://graphql.org/learn/
- **HAL**: https://stateless.group/hal_specification.html
- **JSON:API**: https://jsonapi.org/
- **RFC 7807**: Problem Details for HTTP APIs
