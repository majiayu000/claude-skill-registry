---
name: api-design-principles
description: Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers. Use when designing new APIs, reviewing API specifications, or establishing API design standards.
license: MIT
---

# API Design Principles

Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that delight developers and stand the test of time.

## When to Use This Skill

- Designing new REST or GraphQL APIs
- Refactoring existing APIs for better usability
- Establishing API design standards for your team
- Reviewing API specifications before implementation
- Migrating between API paradigms (REST to GraphQL, etc.)
- Creating developer-friendly API documentation
- Optimizing APIs for specific use cases (mobile, third-party integrations)

## Core Concepts

### 1. RESTful Design Principles

**Resource-Oriented Architecture**
- Resources are nouns (users, orders, products), not verbs
- Use HTTP methods for actions (GET, POST, PUT, PATCH, DELETE)
- URLs represent resource hierarchies
- Consistent naming conventions

**HTTP Methods Semantics:**
- `GET`: Retrieve resources (idempotent, safe)
- `POST`: Create new resources
- `PUT`: Replace entire resource (idempotent)
- `PATCH`: Partial resource updates
- `DELETE`: Remove resources (idempotent)

### 2. GraphQL Design Principles

**Schema-First Development**
- Types define your domain model
- Queries for reading data
- Mutations for modifying data
- Subscriptions for real-time updates

**Query Structure:**
- Clients request exactly what they need
- Single endpoint, multiple operations
- Strongly typed schema
- Introspection built-in

### 3. API Versioning Strategies

**URL Versioning:**
```
/api/v1/users
/api/v2/users
```

**Header Versioning:**
```
Accept: application/vnd.api+json; version=1
```

**Query Parameter Versioning:**
```
/api/users?version=1
```

## REST API Design Patterns

### Pattern 1: Resource Collection Design

```python
# Good: Resource-oriented endpoints
GET    /api/users              # List users (with pagination)
POST   /api/users              # Create user
GET    /api/users/{id}         # Get specific user
PUT    /api/users/{id}         # Replace user
PATCH  /api/users/{id}         # Update user fields
DELETE /api/users/{id}         # Delete user

# Nested resources
GET    /api/users/{id}/orders  # Get user's orders
POST   /api/users/{id}/orders  # Create order for user

# Bad: Action-oriented endpoints (avoid)
POST   /api/createUser
POST   /api/getUserById
POST   /api/deleteUser
```

### Pattern 2: Pagination and Filtering

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

app = FastAPI()

@app.get("/api/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    query = build_query(status=status, search=search)
    total = await count_users(query)
    offset = (page - 1) * page_size
    users = await fetch_users(query, limit=page_size, offset=offset)

    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )
```

### Pattern 3: Error Handling and Status Codes

```python
from fastapi import HTTPException, status

STATUS_CODES = {
    "success": 200,
    "created": 201,
    "no_content": 204,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "conflict": 409,
    "unprocessable": 422,
    "internal_error": 500
}

def raise_not_found(resource: str, id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "NotFound",
            "message": f"{resource} not found",
            "details": {"id": id}
        }
    )
```

### Pattern 4: HATEOAS (Hypermedia as the Engine of Application State)

```python
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    _links: dict

    @classmethod
    def from_user(cls, user: User, base_url: str):
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            _links={
                "self": {"href": f"{base_url}/api/users/{user.id}"},
                "orders": {"href": f"{base_url}/api/users/{user.id}/orders"},
                "update": {"href": f"{base_url}/api/users/{user.id}", "method": "PATCH"},
                "delete": {"href": f"{base_url}/api/users/{user.id}", "method": "DELETE"}
            }
        )
```

## GraphQL Design Patterns

### Pattern 1: Schema Design

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  orders(first: Int = 20, after: String): OrderConnection!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

### Pattern 2: DataLoader (N+1 Prevention)

```python
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids: List[str]) -> List[Optional[dict]]:
        users = await fetch_users_by_ids(user_ids)
        user_map = {user["id"]: user for user in users}
        return [user_map.get(user_id) for user_id in user_ids]
```

## Best Practices

### REST APIs
1. **Consistent Naming**: Use plural nouns for collections
2. **Stateless**: Each request contains all necessary information
3. **Use HTTP Status Codes Correctly**: 2xx success, 4xx client errors, 5xx server errors
4. **Version Your API**: Plan for breaking changes from day one
5. **Pagination**: Always paginate large collections
6. **Rate Limiting**: Protect your API with rate limits
7. **Documentation**: Use OpenAPI/Swagger for interactive docs

### GraphQL APIs
1. **Schema First**: Design schema before writing resolvers
2. **Avoid N+1**: Use DataLoaders for efficient data fetching
3. **Input Validation**: Validate at schema and resolver levels
4. **Error Handling**: Return structured errors in mutation payloads
5. **Pagination**: Use cursor-based pagination (Relay spec)
6. **Deprecation**: Use `@deprecated` directive for gradual migration
7. **Monitoring**: Track query complexity and execution time

## Common Pitfalls

- **Over-fetching/Under-fetching (REST)**: Fixed in GraphQL but requires DataLoaders
- **Breaking Changes**: Version APIs or use deprecation strategies
- **Inconsistent Error Formats**: Standardize error responses
- **Missing Rate Limits**: APIs without limits are vulnerable to abuse
- **Poor Documentation**: Undocumented APIs frustrate developers
- **Ignoring HTTP Semantics**: POST for idempotent operations breaks expectations
- **Tight Coupling**: API structure shouldn't mirror database schema
