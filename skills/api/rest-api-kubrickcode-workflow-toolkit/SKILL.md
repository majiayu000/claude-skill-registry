---
name: rest-api
description: |
  Provides REST API design and implementation standards. Ensures proper URL structure, pagination, sorting, filtering, and error handling patterns. Specializes in RESTful principles, HTTP method semantics, status code usage, versioning strategies, HATEOAS, and API documentation. Implements consistent response structures and content negotiation.
  Use when: designing REST API endpoints, defining URL structures and naming conventions, implementing pagination/sorting/filtering, choosing appropriate HTTP methods (GET/POST/PUT/PATCH/DELETE), selecting HTTP status codes, designing request/response schemas, handling API errors and validation, implementing API versioning, documenting APIs with OpenAPI/Swagger, or designing hypermedia controls (HATEOAS).
---

# REST API Design Standards

## Naming Conventions

### Field Naming

- Boolean: Require `is/has/can` prefix
- Date: Require `~At` suffix
- Use consistent terminology throughout the project (unify on either "create" or "add")

## Date Format

- ISO 8601 UTC
- Use DateTime type

## Pagination

### Cursor-Based (Industry Standard)

- Parameters: `?cursor=xyz&limit=20`
- Response: `{ data: [...], nextCursor: "abc", hasNext: true }`

## Sorting

- `?sortBy=createdAt&sortOrder=desc`
- Support multiple sort
- Specify defaults

## Filtering

- Range: `{ min, max }` or `{ gte, lte }`
- Complex conditions use nested objects

## URL Structure

### Nested Resources

- Maximum 2 levels

### Actions

- Allow verbs only when unable to represent as resource
- `/users/:id/activate`

## Response

### List

- `data` + pagination info

### Creation

- 201 + resource (excluding sensitive information)

### Error (RFC 7807 ProblemDetail)

- Required: `type`, `title`, `status`, `detail`, `instance`
- Optional: `errors` array

## Batch

- `/batch` suffix
- Success/failure count + results
