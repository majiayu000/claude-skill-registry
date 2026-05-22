---
name: api-design-patterns
description: RESTful API design patterns including URL structure, HTTP methods, and idempotency. Use when designing new API endpoints or reviewing API architecture. For existing projects, follow the project's established conventions instead.
durability: encoded-preference
---

# API Design Patterns

## Core Principle

For new projects, enforce RESTful URL structure. For existing projects, follow the project's established API conventions.

## RESTful URL Structure

```
GET    /api/resources              # List resources
GET    /api/resources/:id          # Get single resource
POST   /api/resources              # Create (server assigns ID)
PUT    /api/resources/:id          # Create or replace at specific ID
PATCH  /api/resources/:id          # Partial update
DELETE /api/resources/:id          # Delete resource

# Query parameters for filtering, sorting, pagination
GET /api/resources?status=active&sort=created_at&limit=20&offset=0
```

## HTTP Methods and Idempotency

| Method | Idempotent | Use Case |
|--------|------------|----------|
| GET | Yes | Retrieve resource(s) |
| PUT | Yes | Create or replace at specific URI |
| PATCH | No* | Partial update |
| DELETE | Yes | Remove resource |
| POST | No | Non-idempotent operations |

### PUT vs POST

**Common misconception**: "POST = create, PUT = update"
**Reality**: PUT can create, POST can do various things. The difference is idempotency.

- **PUT**: Client specifies the ID. Idempotent (running twice = same result)
- **POST**: Server assigns the ID. Non-idempotent (running twice = two resources)

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Verbs in URLs (`/getUser/123`) | Use HTTP methods (`GET /users/123`) |
| Ignoring idempotency | PUT for idempotent creates, POST for non-idempotent |
| Inconsistent pluralization | Always use plural nouns (`/users`, not `/user`) |
| Deeply nested resources (`/a/1/b/2/c/3`) | Flatten beyond 2 levels |
