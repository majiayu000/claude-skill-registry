---
name: api-design-principles
model: reasoning
---

# API Design Principles

## WHAT
Design intuitive, scalable REST and GraphQL APIs that developers love. Covers resource modeling, HTTP semantics, pagination, error handling, versioning, and GraphQL schema patterns.

## WHEN
- Designing new REST or GraphQL APIs
- Reviewing API specifications before implementation
- Establishing API design standards for teams
- Refactoring APIs for better usability
- Migrating between API paradigms

## KEYWORDS
REST, GraphQL, API design, HTTP methods, pagination, error handling, versioning, OpenAPI, HATEOAS, schema design


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install api-design-principles
```


---

## Decision Framework: REST vs GraphQL

| Choose REST when... | Choose GraphQL when... |
|---------------------|------------------------|
| Simple CRUD operations | Complex nested data requirements |
| Public APIs with broad audience | Mobile apps needing bandwidth optimization |
| Heavy caching requirements | Clients need to specify exact data shape |
| Team is unfamiliar with GraphQL | Aggregating multiple data sources |
| Simple response structures | Rapidly evolving frontend requirements |

---

## REST API Design

### Resource Naming Rules

```
✓ Plural nouns for collections
  GET /api/users
  GET /api/orders
  GET /api/products

✗ Avoid verbs (let HTTP methods be the verb)
  POST /api/createUser     ← Wrong
  POST /api/users          ← Correct

✓ Nested resources (max 2 levels)
  GET /api/users/{id}/orders
  
✗ Avoid deep nesting
  GET /api/users/{id}/orders/{orderId}/items/{itemId}/reviews  ← Too deep
  GET /api/order-items/{id}/reviews                            ← Better
```

### HTTP Methods and Status Codes

| Method | Purpose | Success | Common Errors |
|--------|---------|---------|---------------|
| GET | Retrieve | 200 OK | 404 Not Found |
| POST | Create | 201 Created | 400/422 Validation |
| PUT | Replace | 200 OK | 404 Not Found |
| PATCH | Partial update | 200 OK | 404 Not Found |
| DELETE | Remove | 204 No Content | 404/409 Conflict |

### Complete Status Code Reference

```python
SUCCESS = {
    200: "OK",           # GET, PUT, PATCH success
    201: "Created",      # POST success
    204: "No Content",   # DELETE success
}

CLIENT_ERROR = {
    400: "Bad Request",           # Malformed syntax
    401: "Unauthorized",          # Missing/invalid auth
    403: "Forbidden",             # Valid auth, no permission
    404: "Not Found",             # Resource doesn't exist
    409: "Conflict",              # State conflict (duplicate email)
    422: "Unprocessable Entity",  # Validation errors
    429: "Too Many Requests",     # Rate limited
}

SERVER_ERROR = {
    500: "Internal Server Error",
    503: "Service Unavailable",   # Temporary downtime
}
```

### Pagination

#### Offset-Based (Simple)

```python
GET /api/users?page=2&page_size=20

{
  "items": [...],
  "page": 2,
  "page_size": 20,
  "total": 150,
  "pages": 8
}
```

#### Cursor-Based (For Large Datasets)

```python
GET /api/users?limit=20&cursor=eyJpZCI6MTIzfQ

{
  "items": [...],
  "next_cursor": "eyJpZCI6MTQzfQ",
  "has_more": true
}
```

### Filtering and Sorting

```
# Filtering
GET /api/users?status=active&role=admin

# Sorting (- prefix for descending)
GET /api/users?sort=-created_at,name

# Search
GET /api/users?search=john

# Field selection
GET /api/users?fields=id,name,email
```

### Error Response Format

Always use consistent structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ],
    "timestamp": "2025-10-16T12:00:00Z"
  }
}
```

### FastAPI Implementation

```python
from fastapi import FastAPI, Query, Path, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="API", version="1.0.0")

# Models
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)

class User(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

class PaginatedResponse(BaseModel):
    items: List[User]
    total: int
    page: int
    page_size: int
    pages: int

# Endpoints
@app.get("/api/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """List users with pagination and filtering."""
    total = await count_users(status=status, search=search)
    offset = (page - 1) * page_size
    users = await fetch_users(limit=page_size, offset=offset, status=status, search=search)
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create new user."""
    if await user_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "EMAIL_EXISTS", "message": "Email already registered"}
        )
    return await save_user(user)

@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: str = Path(...)):
    """Get user by ID."""
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete user."""
    if not await fetch_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    await remove_user(user_id)
```

---

## GraphQL API Design

### Schema Structure

```graphql
# Types
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!
  orders(first: Int = 20, after: String): OrderConnection!
}

# Pagination (Relay-style)
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Queries
type Query {
  user(id: ID!): User
  users(first: Int = 20, after: String, search: String): UserConnection!
}

# Mutations with Input/Payload pattern
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
  code: String!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}
```

### DataLoader (Prevent N+1)

```python
from aiodataloader import DataLoader

class UserLoader(DataLoader):
    async def batch_load_fn(self, user_ids: List[str]) -> List[Optional[dict]]:
        """Load multiple users in single query."""
        users = await fetch_users_by_ids(user_ids)
        user_map = {user["id"]: user for user in users}
        return [user_map.get(uid) for uid in user_ids]

# In resolver
@user_type.field("orders")
async def resolve_orders(user: dict, info):
    loader = info.context["loaders"]["orders_by_user"]
    return await loader.load(user["id"])
```

### Query Protection

```python
# Depth limiting
MAX_QUERY_DEPTH = 5

# Complexity limiting
MAX_QUERY_COMPLEXITY = 100

# Timeout
QUERY_TIMEOUT_SECONDS = 10
```

---

## Versioning Strategies

### URL Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

**Pros**: Clear, easy to route, cacheable
**Cons**: Multiple URLs for same resource

### Header Versioning

```
GET /api/users
Accept: application/vnd.api+json; version=2
```

**Pros**: Clean URLs
**Cons**: Less visible, harder to test

### Deprecation Strategy

1. Add deprecation headers: `Deprecation: true`
2. Document migration path
3. Give 6-12 months notice
4. Monitor usage before removal

---

## Rate Limiting

### Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1640000000

# When limited:
429 Too Many Requests
Retry-After: 3600
```

### Implementation

```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.cache = {}
    
    def check(self, key: str) -> tuple[bool, dict]:
        now = datetime.now()
        if key not in self.cache:
            self.cache[key] = []
        
        # Remove old requests
        cutoff = now - timedelta(seconds=self.period)
        self.cache[key] = [ts for ts in self.cache[key] if ts > cutoff]
        
        remaining = self.calls - len(self.cache[key])
        
        if remaining <= 0:
            return False, {"limit": self.calls, "remaining": 0}
        
        self.cache[key].append(now)
        return True, {"limit": self.calls, "remaining": remaining - 1}
```

---

## Pre-Implementation Checklist

### Resources
- [ ] Nouns, not verbs
- [ ] Plural for collections
- [ ] Max 2 levels nesting

### HTTP
- [ ] Correct method for each action
- [ ] Correct status codes
- [ ] Idempotent operations are idempotent

### Data
- [ ] All collections paginated
- [ ] Filtering/sorting supported
- [ ] Error format consistent

### Security
- [ ] Authentication defined
- [ ] Rate limiting configured
- [ ] Input validation on all fields
- [ ] HTTPS enforced

### Documentation
- [ ] OpenAPI spec generated
- [ ] All endpoints documented
- [ ] Examples provided

---

## NEVER

- **Verbs in URLs**: `/api/getUser` → use `/api/users/{id}` with GET
- **POST for Retrieval**: Use GET for safe, idempotent reads
- **Inconsistent Errors**: Always same error format
- **Unbounded Lists**: Always paginate collections
- **Secrets in URLs**: Query params are logged
- **Breaking Changes Without Versioning**: Plan for evolution from day 1
- **Database Schema as API**: API should be stable even when schema changes
- **Ignoring HTTP Semantics**: Status codes and methods have meaning
