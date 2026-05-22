---
name: api-design
description: REST and API design principles — resource naming, HTTP methods, status codes, pagination, versioning, and error responses. Reference when designing or reviewing APIs.
---

# API Design

## RESTful Resource Naming

### Conventions

| Rule                        | Good                              | Bad                                  |
|-----------------------------|-----------------------------------|--------------------------------------|
| Use plural nouns            | `/users`                          | `/user`, `/getUsers`                 |
| Use nouns, not verbs        | `POST /orders`                    | `POST /createOrder`                  |
| Nest for relationships      | `/users/123/orders`               | `/getUserOrders?userId=123`          |
| Use kebab-case              | `/user-profiles`                  | `/userProfiles`, `/user_profiles`    |
| Keep URLs shallow (max 3)   | `/users/123/orders`               | `/users/123/orders/456/items/789`    |
| Use query params for filters| `/orders?status=pending`          | `/orders/pending`                    |
| Collection + resource IDs   | `/users/123`                      | `/user?id=123`                       |

### URL Structure

```
https://api.example.com/v1/users                    # Collection
https://api.example.com/v1/users/123                # Single resource
https://api.example.com/v1/users/123/orders          # Nested collection
https://api.example.com/v1/users/123/orders/456      # Nested resource
https://api.example.com/v1/orders?status=pending     # Filtered collection
```

### Actions That Do Not Map to CRUD

For operations that are not simple CRUD, use a sub-resource or action noun:

```
POST /users/123/activate          # State transition
POST /orders/456/refund           # Domain action
POST /reports/export              # Process trigger
```

## HTTP Method Semantics

| Method   | Purpose              | Idempotent | Safe | Request Body | Success Code |
|----------|----------------------|------------|------|--------------|--------------|
| `GET`    | Retrieve resource(s) | Yes        | Yes  | No           | 200          |
| `POST`   | Create a resource    | No         | No   | Yes          | 201          |
| `PUT`    | Full replacement     | Yes        | No   | Yes          | 200          |
| `PATCH`  | Partial update       | No*        | No   | Yes          | 200          |
| `DELETE` | Remove a resource    | Yes        | No   | No           | 204          |

*`PATCH` can be made idempotent with proper implementation but is not guaranteed by the spec.

### Method Usage Rules

- [ ] `GET` must never modify server state
- [ ] `POST` is the only method for creating new resources
- [ ] `PUT` sends the complete resource; omitted fields are set to defaults or null
- [ ] `PATCH` sends only the fields to change; omitted fields remain unchanged
- [ ] `DELETE` returns 204 on success, and is a no-op if the resource already does not exist

### Examples

```http
GET /api/v1/users/123
Accept: application/json

---

POST /api/v1/users
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@example.com"
}

---

PUT /api/v1/users/123
Content-Type: application/json

{
  "name": "Jane Doe",
  "email": "jane@newdomain.com",
  "role": "admin"
}

---

PATCH /api/v1/users/123
Content-Type: application/json

{
  "role": "admin"
}

---

DELETE /api/v1/users/123
```

## Status Code Guide

### Success Codes

| Code  | Name         | When to Use                                          |
|-------|--------------|------------------------------------------------------|
| `200` | OK           | Successful GET, PUT, PATCH, or DELETE with body      |
| `201` | Created      | Successful POST that created a resource              |
| `204` | No Content   | Successful DELETE or PUT with no response body        |

### Client Error Codes

| Code  | Name                | When to Use                                        |
|-------|---------------------|----------------------------------------------------|
| `400` | Bad Request         | Malformed JSON, invalid syntax                     |
| `401` | Unauthorized        | Missing or invalid authentication credentials      |
| `403` | Forbidden           | Authenticated but not authorized for this action   |
| `404` | Not Found           | Resource does not exist at this URL                |
| `409` | Conflict            | Resource state conflict (duplicate, version mismatch)|
| `422` | Unprocessable Entity| Valid JSON but fails business validation           |
| `429` | Too Many Requests   | Rate limit exceeded                                |

### Server Error Codes

| Code  | Name                 | When to Use                                       |
|-------|----------------------|---------------------------------------------------|
| `500` | Internal Server Error| Unexpected server failure                         |
| `503` | Service Unavailable  | Server is down for maintenance or overloaded      |

### Decision Tree

```
Is the request well-formed?
  No  --> 400 Bad Request
  Yes --> Is the client authenticated?
    No  --> 401 Unauthorized
    Yes --> Is the client authorized?
      No  --> 403 Forbidden
      Yes --> Does the resource exist?
        No  --> 404 Not Found
        Yes --> Does the request pass validation?
          No  --> 422 Unprocessable Entity
          Yes --> Is there a conflict?
            No  --> 2xx Success
            Yes --> 409 Conflict
```

## Structured Error Response Format

All error responses must follow this format:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The request could not be processed due to validation errors.",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address.",
        "code": "INVALID_FORMAT"
      },
      {
        "field": "age",
        "message": "Must be at least 18.",
        "code": "OUT_OF_RANGE"
      }
    ],
    "request_id": "req_abc123def456"
  }
}
```

### Error Response Rules

- [ ] Always include a machine-readable `code` (uppercase snake_case)
- [ ] Always include a human-readable `message`
- [ ] Include `details` array for field-level validation errors
- [ ] Include `request_id` for traceability
- [ ] Never expose stack traces, internal paths, or database details
- [ ] Use consistent error codes across the entire API

### Standard Error Codes

| Error Code              | HTTP Status | Description                        |
|-------------------------|-------------|------------------------------------|
| `VALIDATION_FAILED`     | 422         | One or more fields are invalid     |
| `RESOURCE_NOT_FOUND`    | 404         | Requested resource does not exist  |
| `AUTHENTICATION_REQUIRED`| 401        | No valid credentials provided      |
| `PERMISSION_DENIED`     | 403         | Insufficient permissions           |
| `CONFLICT`              | 409         | Resource state conflict            |
| `RATE_LIMIT_EXCEEDED`   | 429         | Too many requests                  |
| `INTERNAL_ERROR`        | 500         | Unexpected server error            |
| `SERVICE_UNAVAILABLE`   | 503         | Dependency or server is down       |

## Pagination

### Cursor-Based Pagination (Preferred)

Best for real-time data, large datasets, and consistent results.

**Request:**
```http
GET /api/v1/orders?limit=20&cursor=eyJpZCI6MTAwfQ
```

**Response:**
```json
{
  "data": [ ... ],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIwfQ",
    "has_more": true
  }
}
```

**Implementation notes:**
- Encode cursor as base64 of the last item's sort key
- Cursor is opaque to the client; never expose internal IDs directly
- Always include `has_more` boolean

### Offset-Based Pagination

Simpler but has consistency issues on changing data.

**Request:**
```http
GET /api/v1/products?page=3&per_page=25
```

**Response:**
```json
{
  "data": [ ... ],
  "pagination": {
    "page": 3,
    "per_page": 25,
    "total_count": 342,
    "total_pages": 14
  }
}
```

### When to Use Each

| Approach       | Use When                                             |
|----------------|------------------------------------------------------|
| Cursor-based   | Real-time data, infinite scroll, large datasets      |
| Offset-based   | Admin panels, reports where total count is needed    |

### Pagination Rules

- [ ] Default `limit` or `per_page` to a sensible value (e.g., 20)
- [ ] Enforce a maximum limit (e.g., 100) to prevent abuse
- [ ] Always include pagination metadata in the response
- [ ] Return an empty `data` array (not null) when no results match

## Versioning Strategies

| Strategy       | Example                          | Pros                                 | Cons                               |
|----------------|----------------------------------|--------------------------------------|------------------------------------|
| URL path       | `/api/v1/users`                  | Explicit, easy to route              | URL changes on version bump        |
| Header         | `Accept: application/vnd.api+json; version=1` | Clean URLs         | Hidden, harder to test             |
| Query param    | `/api/users?version=1`           | Easy to add                          | Not standard, clutters query       |

### Recommended: URL Path Versioning

```
/api/v1/users    # Version 1
/api/v2/users    # Version 2 (breaking changes)
```

### Versioning Rules

- [ ] Only increment the major version for breaking changes
- [ ] Support at least N-1 version in production
- [ ] Document the deprecation timeline (minimum 6 months notice)
- [ ] Use `Sunset` header to communicate deprecation date
- [ ] Non-breaking changes (new fields, new endpoints) do not require a version bump

## Rate Limiting

### Headers

Include these headers in every response:

| Header                  | Value                                    |
|-------------------------|------------------------------------------|
| `X-RateLimit-Limit`    | Maximum requests per window              |
| `X-RateLimit-Remaining`| Requests remaining in current window     |
| `X-RateLimit-Reset`    | Unix timestamp when the window resets    |
| `Retry-After`          | Seconds to wait (on 429 responses only)  |

### Example 429 Response

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1700000000
Retry-After: 30
Content-Type: application/json

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "You have exceeded the rate limit. Please retry after 30 seconds.",
    "request_id": "req_xyz789"
  }
}
```

## Authentication Patterns

| Pattern         | Use Case                                    | Header                               |
|-----------------|---------------------------------------------|--------------------------------------|
| Bearer Token    | User authentication (JWT, OAuth2)           | `Authorization: Bearer <token>`      |
| API Key         | Service-to-service, third-party integrations| `X-API-Key: <key>` or query param    |
| OAuth2          | Third-party user authorization              | `Authorization: Bearer <access_token>`|
| Basic Auth      | Simple internal services (over HTTPS only)  | `Authorization: Basic <base64>`      |

### Authentication Rules

- [ ] Always use HTTPS in production
- [ ] Never pass tokens or keys in URL query params for GET requests (they appear in logs)
- [ ] API keys should be rotatable without downtime
- [ ] Return 401 for missing/invalid credentials, 403 for insufficient permissions
- [ ] Include `WWW-Authenticate` header in 401 responses

## Input Validation

### Validation Order

1. **Type validation** - Is the JSON well-formed? Are types correct?
2. **Presence validation** - Are all required fields present?
3. **Format validation** - Do values match expected patterns (email, URL, UUID)?
4. **Range validation** - Are numbers within bounds? Are strings within length limits?
5. **Business validation** - Does the data make sense in context?

### Return All Errors at Once

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Multiple validation errors occurred.",
    "details": [
      { "field": "email", "message": "Required field.", "code": "REQUIRED" },
      { "field": "age", "message": "Must be between 0 and 150.", "code": "OUT_OF_RANGE" },
      { "field": "name", "message": "Must be 1-100 characters.", "code": "INVALID_LENGTH" }
    ]
  }
}
```

Never return one error at a time forcing clients to resubmit repeatedly.

## Filtering, Sorting, and Field Selection

### Filtering

```http
GET /api/v1/orders?status=pending&created_after=2025-01-01
GET /api/v1/products?category=electronics&min_price=100&max_price=500
```

### Sorting

```http
GET /api/v1/users?sort=created_at       # Ascending (default)
GET /api/v1/users?sort=-created_at      # Descending (prefix with -)
GET /api/v1/users?sort=name,-created_at  # Multiple fields
```

### Field Selection (Sparse Fieldsets)

```http
GET /api/v1/users?fields=id,name,email
GET /api/v1/orders?fields=id,total,status
```

### Query Parameter Rules

- [ ] Use consistent naming across all endpoints
- [ ] Document every supported filter, sort field, and selectable field
- [ ] Ignore unknown query parameters (do not error)
- [ ] Apply sensible defaults when parameters are omitted
- [ ] Validate and sanitize all query parameter values
