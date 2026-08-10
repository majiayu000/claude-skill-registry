---
name: api-design
description: Design RESTful APIs with proper resource modeling, HTTP method semantics, status codes, pagination, versioning, and documentation. Use when the user requests api design or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# API Design

This skill enables an AI agent to design production-quality RESTful APIs. The agent models resources, defines endpoints with correct HTTP method semantics, selects appropriate status codes, implements pagination and versioning strategies, and produces OpenAPI documentation. The output follows REST constraints including statelessness, uniform interface, and resource-based URIs.

## Workflow

1. **Identify resources and relationships:** Analyze the application domain to extract nouns as resources (e.g., users, tasks, comments). Map relationships between resources—one-to-many, many-to-many—and determine whether sub-resources or independent collections are appropriate. Avoid verb-based endpoints; resources should represent entities, not actions.

2. **Define endpoints and HTTP methods:** For each resource, define CRUD endpoints using the correct HTTP methods. Use GET for retrieval (safe, idempotent), POST for creation (not idempotent), PUT for full replacement (idempotent), PATCH for partial updates (idempotent), and DELETE for removal (idempotent). Nest sub-resources under their parent when the relationship is strong (e.g., `/tasks/{id}/comments`).

3. **Design request and response schemas:** Define JSON request bodies, response payloads, and query parameters for each endpoint. Include field names in snake_case or camelCase consistently. Specify required vs. optional fields, data types, and validation constraints. Design a consistent error response envelope used across all endpoints.

4. **Implement pagination, filtering, and sorting:** For list endpoints, add cursor-based or offset pagination with `limit` and `offset` (or `cursor`) query parameters. Support filtering via query parameters (e.g., `?status=active`) and sorting with `sort` and `order` parameters. Return pagination metadata in the response body including total count, next/previous links.

5. **Define versioning and content negotiation:** Choose a versioning strategy—URI path (`/v1/tasks`), query parameter (`?version=1`), or Accept header (`Accept: application/vnd.api.v1+json`). URI path versioning is simplest and most common. Ensure backward compatibility within a version and document deprecation timelines.

6. **Generate OpenAPI documentation:** Produce a complete OpenAPI 3.0 specification with paths, schemas, security schemes, and example requests/responses. Include rate limiting headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) in response documentation.

## Supported Technologies

- **Specification formats:** OpenAPI 3.0/3.1, JSON Schema, AsyncAPI (for event-driven extensions)
- **Frameworks:** Express.js, FastAPI, Django REST Framework, Spring Boot, Rails API
- **Documentation tools:** Swagger UI, Redoc, Stoplight
- **Testing:** Postman, Insomnia, REST Client (VS Code), curl

## Usage

Provide the agent with a description of the application domain, the entities involved, and the operations users need to perform. The agent will produce endpoint definitions, request/response schemas, and an OpenAPI specification. You can iterate by requesting changes to specific endpoints, adding pagination, or adjusting error formats.

## Examples

### Example 1: Task Management API (OpenAPI Spec Snippet)

```yaml
openapi: 3.0.3
info:
  title: Task Management API
  version: 1.0.0
  description: RESTful API for managing tasks and projects.

servers:
  - url: https://api.example.com/v1

paths:
  /tasks:
    get:
      summary: List all tasks
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, in_progress, done]
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: cursor
          in: query
          schema:
            type: string
      responses:
        "200":
          description: Paginated list of tasks
          headers:
            X-RateLimit-Limit:
              schema:
                type: integer
            X-RateLimit-Remaining:
              schema:
                type: integer
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/Task"
                  pagination:
                    $ref: "#/components/schemas/CursorPagination"
    post:
      summary: Create a new task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TaskCreate"
      responses:
        "201":
          description: Task created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Task"
        "422":
          description: Validation error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"

  /tasks/{taskId}:
    get:
      summary: Get a task by ID
      parameters:
        - name: taskId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        "200":
          description: Task details
        "404":
          description: Task not found

components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
        description:
          type: string
        status:
          type: string
          enum: [pending, in_progress, done]
        created_at:
          type: string
          format: date-time
    TaskCreate:
      type: object
      required: [title]
      properties:
        title:
          type: string
          maxLength: 255
        description:
          type: string
        assignee_id:
          type: string
          format: uuid
    CursorPagination:
      type: object
      properties:
        next_cursor:
          type: string
          nullable: true
        has_more:
          type: boolean
    ErrorResponse:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                  reason:
                    type: string
```

### Example 2: Consistent Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      {
        "field": "title",
        "reason": "Title is required and cannot be empty."
      },
      {
        "field": "assignee_id",
        "reason": "Must be a valid UUID."
      }
    ],
    "request_id": "req_abc123",
    "documentation_url": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

Standard error codes to use consistently across all endpoints:

| HTTP Status | Error Code | Meaning |
|---|---|---|
| 400 | `BAD_REQUEST` | Malformed request syntax |
| 401 | `UNAUTHORIZED` | Missing or invalid authentication |
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions |
| 404 | `NOT_FOUND` | Resource does not exist |
| 409 | `CONFLICT` | Resource state conflict (e.g., duplicate) |
| 422 | `VALIDATION_ERROR` | Semantic validation failure |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

## Best Practices

- **Use plural nouns for resource paths** (`/tasks`, not `/task`) and avoid verbs in URIs. Actions that don't map to CRUD should use sub-resources (e.g., `POST /tasks/{id}/archive`).
- **Design for idempotency** by supporting `Idempotency-Key` headers on POST requests. PUT and DELETE are naturally idempotent; document this behavior clearly.
- **Include rate limiting headers** (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`) on every response so clients can self-throttle.
- **Use HATEOAS links** in responses to enable API discoverability. Include `_links` with `self`, `next`, `prev`, and related resource URIs where appropriate.
- **Version from day one** even if you only have v1. This prevents painful migrations later. Deprecate old versions with `Sunset` and `Deprecation` headers.
- **Return `Location` header** on 201 Created responses pointing to the newly created resource URI.

## Edge Cases

- **Empty collections:** Return `200 OK` with an empty `data` array and `has_more: false`, not `404`.
- **Deleted resources:** Return `404 Not Found` for hard-deleted resources. For soft-deleted resources, return `410 Gone` with metadata about when the resource was deleted.
- **Concurrent updates:** Use `ETag` and `If-Match` headers for optimistic concurrency control. Return `412 Precondition Failed` if the resource has changed since the client last fetched it.
- **Partial failures in batch operations:** Return `207 Multi-Status` with per-item status codes so clients know which items succeeded and which failed.
- **Trailing slashes:** Normalize `/tasks/` and `/tasks` to the same handler. Return `301` redirects if you enforce one canonical form.
- **Unknown query parameters:** Ignore unknown parameters silently or return `400` with a clear message—pick one strategy and be consistent.
