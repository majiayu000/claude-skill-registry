---
name: api-design-framework
description: Comprehensive API design patterns for REST, GraphQL, and gRPC. Use when designing APIs, creating endpoints, adding routes, implementing pagination, rate limiting, or authentication patterns.
context: fork
agent: backend-system-architect
version: 1.2.0
author: AI Agent Hub
tags: [api, rest, graphql, grpc, backend, documentation]
user-invocable: false
---

# API Design Framework

This skill provides comprehensive guidance for designing robust, scalable, and developer-friendly APIs. Whether building REST, GraphQL, or gRPC services, this framework ensures consistency, usability, and maintainability.

## When to Use
- Designing new API endpoints or services
- Establishing API conventions for a team or organization
- Reviewing API designs for consistency and best practices
- Migrating or versioning existing APIs
- Creating API documentation (OpenAPI, AsyncAPI)
- Choosing between REST, GraphQL, or gRPC

## API Design Principles

### 1. Developer Experience First
APIs should be intuitive and self-documenting:
- Clear, consistent naming conventions
- Predictable behavior and responses
- Comprehensive documentation
- Helpful error messages

### 2. Consistency Over Cleverness
Follow established patterns rather than inventing new ones:
- Standard HTTP methods and status codes (REST)
- Conventional query structures (GraphQL)
- Idiomatic proto definitions (gRPC)

### 3. Evolution Without Breaking Changes
Design for change from day one:
- API versioning strategy
- Backward compatibility considerations
- Deprecation policies
- Migration paths

### 4. Performance by Design
Consider performance implications:
- Pagination for large datasets
- Filtering and partial responses
- Caching strategies
- Rate limiting

---

## Protocol References

### REST API Design
**See: `references/rest-api.md`**

Key topics covered:
- Resource naming conventions (plural nouns, hierarchical relationships)
- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Status codes (2xx, 4xx, 5xx)
- Request/response formats
- Pagination (cursor-based vs offset-based)
- Filtering, sorting, field selection
- API versioning strategies
- Rate limiting headers
- Authentication patterns (Bearer, API Key)

### GraphQL API Design
**See: `references/graphql-api.md`**

Key topics covered:
- Schema design principles (nullable by default)
- Connection pattern for lists (edges, nodes, pageInfo)
- Input types for mutations
- Query design patterns
- Field-level error handling

### gRPC API Design
**See: `references/grpc-api.md`**

Key topics covered:
- Proto file structure
- Service and message definitions
- gRPC status codes mapping to HTTP equivalents

### Frontend API Integration
**See: `references/frontend-integration.md`**

Key topics covered:
- Runtime validation with Zod
- Request interceptors with ky
- Error enrichment pattern
- TanStack Query integration

---

## Quick Reference: HTTP Status Codes

| Code | Name | Use Case |
|------|------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Missing auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource missing |
| 409 | Conflict | Duplicate |
| 422 | Unprocessable | Validation failed |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Error | Server error |

## Quick Reference: Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "Email is already registered" }
    ],
    "request_id": "req_abc123"
  }
}
```

---

## Common Pitfalls

| Pitfall | Bad | Good |
|---------|-----|------|
| Verbs in URLs | `POST /createUser` | `POST /users` |
| Inconsistent naming | `/users, /userOrders` | `/users, /orders` |
| Ignoring HTTP methods | `POST /users/123/delete` | `DELETE /users/123` |
| Exposing internals | `/users-table` | `/users` |
| Generic errors | `"Something went wrong"` | `"Email already exists"` |

---

## Best Practices Summary

1. **Use plural nouns** for resources: `/users`, `/orders`
2. **Use kebab-case** for multi-word: `/user-preferences`
3. **Use hierarchical URLs**: `/users/123/orders`
4. **Cursor pagination** for large datasets
5. **URI versioning** for public APIs: `/api/v1/users`
6. **Include rate limit headers** in responses
7. **Validate with Zod** on frontend boundary
8. **Include request_id** in error responses

---

## Integration with Agents

| Agent | Usage |
|-------|-------|
| **backend-system-architect** | Designs new APIs using this framework |
| **frontend-ui-developer** | Reviews contracts, integrates with APIs |
| **code-quality-reviewer** | Validates API designs against standards |

---

## Related Skills

- `fastapi-advanced` - FastAPI-specific implementation patterns for the API designs in this skill
- `error-handling-rfc9457` - RFC 9457 Problem Details standard for structured error responses
- `api-versioning` - Detailed versioning strategies beyond the basics covered here
- `rate-limiting` - Advanced rate limiting implementations and algorithms

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Pagination default | Cursor-based | More efficient for large datasets, stable under inserts/deletes |
| Error format | Structured JSON with request_id | Enables debugging, correlation, and consistent client handling |
| Versioning strategy | URI path (`/api/v1/`) | Most explicit, works with all clients, easy to document |
| Resource naming | Plural nouns, kebab-case | Industry standard, consistent, avoids verb confusion |

---

**Skill Version**: 1.2.0
**Last Updated**: 2026-01-14

## Changelog

### v1.2.0 (2026-01-14)
- Split into reference files for progressive loading
- Added `references/rest-api.md`
- Added `references/graphql-api.md`
- Added `references/grpc-api.md`
- Added `references/frontend-integration.md`
- Fixed malformed YAML frontmatter

### v1.1.0 (2025-12-29)
- Added Frontend API Integration section
- Added Zod runtime validation patterns
- Added request interceptors with ky
- Added TanStack Query integration examples

## Capability Details

### rest-design
**Keywords:** rest, restful, http, endpoint, route, path, resource, CRUD
**Solves:**
- How do I design RESTful APIs?
- REST endpoint patterns and conventions
- HTTP methods and status codes
- API versioning and pagination

### graphql-design
**Keywords:** graphql, schema, query, mutation, connection, relay
**Solves:**
- How do I design GraphQL APIs?
- Schema design best practices
- Connection pattern for pagination

### grpc-design
**Keywords:** grpc, protobuf, proto, rpc, streaming
**Solves:**
- How do I design gRPC services?
- Proto file structure
- gRPC status codes

### endpoint-design
**Keywords:** endpoint, route, path, resource, CRUD
**Solves:**
- How do I structure API endpoints?
- What's the best URL pattern for this resource?
- RESTful endpoint naming conventions

### pagination
**Keywords:** pagination, paginate, paging, offset, cursor, limit
**Solves:**
- How do I add pagination to an endpoint?
- Cursor vs offset pagination
- Pagination best practices

### versioning
**Keywords:** version, v1, v2, api version, breaking change
**Solves:**
- How do I version my API?
- When to create a new API version
- URL vs header versioning

### error-handling
**Keywords:** error, exception, status code, error response, validation error
**Solves:**
- How do I structure error responses?
- Which HTTP status codes to use
- Error message best practices

### rate-limiting
**Keywords:** rate limit, throttle, quota, requests per second, 429
**Solves:**
- How do I implement rate limiting?
- Rate limit headers and responses
- Tiered rate limiting strategies

### authentication
**Keywords:** auth, authentication, bearer, jwt, oauth, api key
**Solves:**
- How do I secure API endpoints?
- JWT vs API key authentication
- OAuth2 flow for APIs

### frontend-integration
**Keywords:** zod, validation, fetch, ky, tanstack, react-query
**Solves:**
- How do I consume APIs with type safety?
- Runtime validation of API responses
- Request interceptors and error handling