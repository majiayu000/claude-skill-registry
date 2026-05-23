---
name: create-api-design
description: Design a REST or GraphQL API from a feature specification when the user asks to design an API, create endpoints, define an API contract, or plan API resources
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write, Grep
argument-hint: "[feature name or resource to design API for]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: api, design, docs
---

# Create API Design

## Overview

Design a complete, production-ready API from a feature specification or resource description. The output is a comprehensive API design document covering endpoints, schemas, error contracts, pagination, auth, rate limiting, and caching -- consistent with existing API patterns in the project.

## Workflow

1. **Read existing API patterns** -- Read `.chalk/docs/engineering/` for:
   - Existing API design documents (match naming, URL structure, and conventions)
   - Architecture docs describing the current API layer
   - Auth patterns and middleware
   - Error handling conventions
   - If no docs exist, scan the codebase for route definitions to infer patterns

2. **Scan codebase for current conventions** -- Use Grep to find:
   - Route definitions (e.g., `router.get`, `app.post`, `@GetMapping`, `@api_view`)
   - Error response shapes (look for error middleware, error classes)
   - Pagination patterns (cursor vs. offset, parameter names)
   - Auth middleware usage (JWT, API key, OAuth scopes)
   - Response envelope patterns (do responses wrap in `{ data, meta }` or return raw?)
   - Store these conventions; the new API must follow them exactly

3. **Determine the next document number** -- List files in `.chalk/docs/engineering/` matching `*_api_design_*.md`. Find the highest number and increment by 1.

4. **Clarify the resource and operations** -- From `$ARGUMENTS` and conversation context, identify:
   - The resource(s) being designed (nouns, not verbs)
   - The operations needed (CRUD, plus any domain-specific actions)
   - Who consumes this API (frontend, mobile, third-party, internal service)
   - Auth requirements (public, authenticated, role-based, scope-based)
   - Ask the user for clarification if the resource boundaries are unclear

5. **Design the endpoints** -- Follow REST conventions strictly:
   - Use plural nouns for resource paths (`/users`, not `/user`)
   - Use nested resources for ownership (`/users/{id}/posts`, not `/user-posts`)
   - Limit nesting to 2 levels maximum
   - Use HTTP methods correctly (GET reads, POST creates, PUT replaces, PATCH updates, DELETE removes)
   - Use query parameters for filtering, sorting, and pagination on collection endpoints
   - Use path parameters only for resource identifiers

6. **Define schemas** -- For each endpoint, define:
   - Request body JSON schema (for POST/PUT/PATCH)
   - Response body JSON schema (for all methods)
   - Query parameter schema (for GET collection endpoints)
   - Use consistent field naming (camelCase or snake_case -- match existing convention)

7. **Define error contract** -- Design a consistent error response shape used across all endpoints. Include validation errors, business logic errors, and system errors.

8. **Write the document** -- Save to `.chalk/docs/engineering/<n>_api_design_<resource_slug>.md`.

9. **Confirm** -- Tell the user the API design was created with its path and a summary of the endpoints defined.

## Filename Convention

```
<number>_api_design_<snake_case_resource>.md
```

Examples:
- `4_api_design_user_profiles.md`
- `8_api_design_billing_subscriptions.md`
- `11_api_design_notification_preferences.md`

## API Design Document Format

```markdown
# API Design: <Resource Name>

Last updated: <YYYY-MM-DD>

## Overview

<1-2 sentences describing what this API enables and who consumes it.>

## Base URL

<e.g., `/api/v1` -- match existing project convention>

## Authentication

<Describe auth requirements. Reference existing auth middleware if applicable.>

| Endpoint Pattern | Auth Required | Scopes / Roles |
|-----------------|---------------|----------------|
| `GET /resources` | Yes | `read:resources` |
| `POST /resources` | Yes | `write:resources` |
| `GET /resources/public` | No | — |

## Endpoints

### Resource Collection

#### List Resources

`GET /resources`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (if offset pagination) |
| `limit` | integer | No | 20 | Items per page (max 100) |
| `sort` | string | No | `created_at` | Sort field |
| `order` | string | No | `desc` | Sort direction: `asc` or `desc` |
| `filter[status]` | string | No | — | Filter by status |

**Response: `200 OK`**

```json
{
  "data": [
    {
      "id": "res_abc123",
      "type": "resource",
      "attributes": {}
    }
  ],
  "meta": {
    "total": 142,
    "page": 1,
    "limit": 20,
    "total_pages": 8
  }
}
```

#### Create Resource

`POST /resources`

**Request Body:**

```json
{
  "name": "string (required, 1-255 chars)",
  "description": "string (optional, max 2000 chars)",
  "status": "string (optional, enum: draft|active|archived, default: draft)"
}
```

**Response: `201 Created`**

```json
{
  "data": {
    "id": "res_abc123",
    "type": "resource",
    "attributes": {
      "name": "Example",
      "description": null,
      "status": "draft",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  }
}
```

### Individual Resource

#### Get Resource

`GET /resources/{id}`

#### Update Resource

`PATCH /resources/{id}`

#### Delete Resource

`DELETE /resources/{id}`

<Continue for all endpoints...>

## Request / Response Schemas

### Resource Schema

| Field | Type | Constraints | Description |
|-------|------|------------|-------------|
| `id` | string | Read-only, prefixed | Unique identifier |
| `name` | string | Required, 1-255 chars | Display name |
| `created_at` | ISO 8601 | Read-only | Creation timestamp |
| `updated_at` | ISO 8601 | Read-only | Last modification timestamp |

## Error Contract

All errors follow a consistent shape:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource does not exist.",
    "status": 404,
    "details": []
  }
}
```

### Validation Errors (`422`)

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "status": 422,
    "details": [
      {
        "field": "name",
        "constraint": "required",
        "message": "Name is required."
      },
      {
        "field": "email",
        "constraint": "format",
        "message": "Email must be a valid email address."
      }
    ]
  }
}
```

### Error Codes

| HTTP Status | Error Code | When Used |
|-------------|-----------|-----------|
| 400 | `BAD_REQUEST` | Malformed request syntax |
| 401 | `UNAUTHORIZED` | Missing or invalid auth token |
| 403 | `FORBIDDEN` | Valid auth but insufficient permissions |
| 404 | `RESOURCE_NOT_FOUND` | Resource does not exist |
| 409 | `CONFLICT` | Resource state conflict (e.g., duplicate) |
| 422 | `VALIDATION_ERROR` | Request body fails validation |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

## Pagination Strategy

<Choose one and document it. Match existing project convention.>

### Offset Pagination (simpler, suitable for most cases)

- Parameters: `page` (1-indexed), `limit` (default 20, max 100)
- Response meta: `total`, `page`, `limit`, `total_pages`
- Drawback: inconsistent results if data changes between pages

### Cursor Pagination (for large or frequently changing datasets)

- Parameters: `cursor` (opaque string), `limit` (default 20, max 100)
- Response meta: `next_cursor`, `has_more`
- Advantage: consistent results regardless of data changes

## Rate Limiting

| Tier | Limit | Window | Scope |
|------|-------|--------|-------|
| Standard | 100 requests | 1 minute | Per API key |
| Elevated | 1000 requests | 1 minute | Per API key |
| Webhook delivery | 10 requests | 1 second | Per endpoint |

**Rate limit headers:**

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1705312800
```

## Caching

| Endpoint | Cache Strategy | TTL | Invalidation |
|----------|---------------|-----|--------------|
| `GET /resources` | Private, no-store | — | — |
| `GET /resources/{id}` | Private, max-age | 60s | On PATCH/DELETE |
| `GET /resources/{id}/stats` | Private, max-age | 300s | On data change |

**Headers:**

```
Cache-Control: private, max-age=60
ETag: "abc123"
```

## Example Requests

### cURL

```bash
# List resources
curl -X GET "https://api.example.com/api/v1/resources?limit=10&sort=name" \
  -H "Authorization: Bearer <token>" \
  -H "Accept: application/json"

# Create resource
curl -X POST "https://api.example.com/api/v1/resources" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Resource", "status": "active"}'
```

### Fetch (JavaScript)

```javascript
// List resources
const response = await fetch('/api/v1/resources?limit=10', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Accept': 'application/json',
  },
});
const { data, meta } = await response.json();

// Create resource
const response = await fetch('/api/v1/resources', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ name: 'My Resource', status: 'active' }),
});
```
```

## URL Design Rules

- **Plural nouns**: `/users`, `/orders`, `/invoices` -- never singular
- **Kebab-case**: `/user-profiles`, not `/userProfiles` or `/user_profiles`
- **No verbs in URLs**: `/orders/{id}/cancel` (POST) is acceptable for non-CRUD actions, but prefer state transitions via PATCH when possible
- **Max 2 levels of nesting**: `/users/{id}/orders` is fine; `/users/{id}/orders/{id}/items/{id}/variants` is not -- flatten it
- **Consistent ID format**: Use prefixed IDs (`usr_abc123`) or UUIDs, never auto-increment integers in URLs
- **Version in URL**: `/api/v1/` -- match existing project convention; if no convention exists, use URL-based versioning

## Field Naming Rules

- Match existing project convention (camelCase or snake_case) -- never mix
- Boolean fields: prefix with `is_`, `has_`, `can_` (e.g., `is_active`, `has_password`)
- Timestamps: suffix with `_at` (e.g., `created_at`, `deleted_at`)
- Counts: suffix with `_count` (e.g., `comment_count`)
- IDs: suffix with `_id` for foreign keys (e.g., `user_id`)

## Anti-patterns

- **Inconsistent error shapes** -- Every endpoint must return errors in the same structure. If one endpoint returns `{ "error": "message" }` and another returns `{ "errors": [{ "msg": "..." }] }`, clients cannot write generic error handling. Define the contract once and enforce it everywhere.
- **No pagination** -- Any endpoint that returns a list must be paginated. Unbounded list responses will eventually cause timeouts, OOM errors, or degraded client performance. There is no "the list is small" exception -- lists grow.
- **RPC-style URLs** -- `/api/getUser`, `/api/createOrder`, `/api/deleteInvoice` are RPC, not REST. Use resource nouns with HTTP methods: `GET /users/{id}`, `POST /orders`, `DELETE /invoices/{id}`.
- **No auth specification** -- Every endpoint must document its auth requirements. "Auth: TBD" is not a design -- it is a security gap. If auth is genuinely not yet decided, flag it as an unresolved question with your recommendation.
- **Breaking existing naming conventions** -- If the existing API uses `camelCase`, the new endpoints must use `camelCase`. Inconsistency across endpoints is worse than a suboptimal convention applied consistently.
- **Exposing internal IDs** -- Auto-increment database IDs leak information (total count, creation order) and are enumerable. Use UUIDs or prefixed opaque IDs.
- **No versioning strategy** -- APIs evolve. If there is no versioning mechanism, the first breaking change will be a crisis. Decide on URL-based or header-based versioning before shipping.
- **Inconsistent status codes** -- POST that returns 200 instead of 201, DELETE that returns 204 sometimes and 200 other times. Map each operation to its correct status code and be consistent.
