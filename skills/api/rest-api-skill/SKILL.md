---
name: rest-api-skill
description: Reusable REST API skill with HTTP methods, status codes, error handling, and API design patterns.
---

# REST API Skill

Use this skill when designing or consuming REST APIs.

## HTTP Methods

| Method | Usage | Idempotent |
|--------|-------|------------|
| `GET` | Retrieve resource(s) | Yes |
| `POST` | Create new resource | No |
| `PUT` | Replace entire resource | Yes |
| `PATCH` | Partial update | No |
| `DELETE` | Remove resource | Yes |

## Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | Valid token, insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

## URL Design

```
# Resource naming (plural nouns)
GET    /api/users              # List all users
GET    /api/users/:id          # Get single user
POST   /api/users              # Create user
PUT    /api/users/:id          # Replace user
PATCH  /api/users/:id          # Partial update
DELETE /api/users/:id          # Delete user

# Nested resources
GET    /api/users/:id/tasks    # Get user's tasks
POST   /api/users/:id/tasks    # Create task for user

# Query parameters
GET    /api/tasks?status=pending&limit=10
GET    /api/tasks?sort=created_at&order=desc
```

## Request/Response Formats

### Request Body (JSON)
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```

### Success Response (201 Created)
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:00:00Z"
}
```

### Error Response (400)
```json
{
  "error": "Validation Error",
  "message": "Title must be between 1 and 200 characters",
  "details": [
    {
      "field": "title",
      "message": "String must have at least 1 character"
    }
  ]
}
```

### Error Response (401)
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### Error Response (404)
```json
{
  "error": "Not Found",
  "message": "Task 5 not found"
}
```

## Authentication Header

```
Authorization: Bearer <jwt_token>
```

## Pagination

```typescript
// Request with pagination
GET /api/tasks?page=1&limit=10

// Response with pagination metadata
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "total_pages": 5
  }
}
```

## API Client Pattern (Frontend)

```typescript
class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  setToken(token: string) {
    this.token = token;
  }

  private async request<T>(
    method: string,
    endpoint: string,
    data?: object
  ): Promise<T> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method,
      headers,
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || "API Error");
    }

    return response.json();
  }

  get<T>(endpoint: string) {
    return this.request<T>("GET", endpoint);
  }

  post<T>(endpoint: string, data: object) {
    return this", endpoint, data.request<T>("POST);
  }

  put<T>(endpoint: string, data: object) {
    return this.request<T>("PUT", endpoint, data);
  }

  patch<T>(endpoint: string, data: object) {
    return this.request<T>("PATCH", endpoint, data);
  }

  delete<T>(endpoint: string) {
    return this.request<T>("DELETE", endpoint);
  }
}
```

## Best Practices

1. Use plural nouns for resource names
2. Use HTTP methods semantically (GET for read, POST for create)
3. Return appropriate status codes
4. Use JSON for request/response bodies
5. Include pagination for list endpoints
6. Use ISO 8601 for dates
7. Include error messages in responses
8. Use versioning in URL (`/api/v1/`) for breaking changes
9. Document all endpoints (OpenAPI/Swagger)
