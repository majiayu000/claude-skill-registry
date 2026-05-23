---
name: faion-api-skill
user-invocable: false
description: ""
---

# API Design Mastery

**Build Production-Ready APIs with Modern Best Practices (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **REST** | Resources, HTTP methods, status codes, HATEOAS |
| **GraphQL** | Queries, mutations, subscriptions, federation |
| **OpenAPI** | Contract-first, schema definition, code generation |
| **Auth** | OAuth 2.0, JWT, API keys, scopes |
| **Quality** | Rate limiting, error handling, monitoring |
| **Documentation** | Swagger UI, Redoc, AsyncAPI |
| **Testing** | Contract testing, Postman, Pact |
| **Gateway** | Kong, AWS API Gateway, routing |

---

## M-API-001: REST API Design

### Problem

APIs without consistent design lead to confusion, integration failures, and maintenance nightmares.

### Framework

**Resource-Oriented Design:**

```
/users                  # Collection
/users/{id}             # Singleton
/users/{id}/orders      # Sub-collection
/users/{id}/orders/{id} # Nested singleton
```

**HTTP Methods:**

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Partial update | No | No |
| DELETE | Remove resource | Yes | No |

**Standard Patterns:**

```
GET    /users              # List all users
GET    /users?status=active&limit=10  # Filtered list
GET    /users/{id}         # Get single user
POST   /users              # Create user
PUT    /users/{id}         # Replace user
PATCH  /users/{id}         # Update user fields
DELETE /users/{id}         # Delete user
```

**Status Codes:**

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET/PUT/PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate/state conflict |
| 422 | Unprocessable Entity | Semantic validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server failure |
| 503 | Service Unavailable | Maintenance/overload |

### HATEOAS (Hypermedia)

```json
{
  "id": "123",
  "name": "John Doe",
  "_links": {
    "self": { "href": "/users/123" },
    "orders": { "href": "/users/123/orders" },
    "update": { "href": "/users/123", "method": "PATCH" }
  }
}
```

### Best Practices

- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural names: `/users` not `/user`
- Use lowercase: `/user-profiles` not `/UserProfiles`
- Use hyphens for readability: `/user-profiles` not `/user_profiles`
- Nest for relationships: `/users/{id}/orders` for user's orders
- Use query params for filtering: `?status=active&sort=-created_at`
- Include `Location` header for 201 responses
- Return created/updated resource in response body

### Agent

faion-api-agent

---

## M-API-002: GraphQL Patterns

### Problem

REST can lead to over-fetching/under-fetching. Complex UIs need flexible data queries.

### Framework

**Schema Definition:**

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  orders: [Order!]!
  createdAt: DateTime!
}

type Order {
  id: ID!
  total: Float!
  status: OrderStatus!
  items: [OrderItem!]!
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  orderStatusChanged(userId: ID!): Order!
}

input CreateUserInput {
  name: String!
  email: String!
}
```

**Query Example:**

```graphql
query GetUserWithOrders($id: ID!) {
  user(id: $id) {
    id
    name
    email
    orders(first: 5) {
      id
      total
      status
      items {
        name
        quantity
      }
    }
  }
}
```

**Mutation Example:**

```graphql
mutation CreateNewUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
```

### N+1 Prevention

**Problem:** Fetching related data causes multiple DB queries.

**Solution - DataLoader:**

```typescript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (userIds) => {
  const users = await db.users.findMany({ where: { id: { in: userIds } } });
  return userIds.map(id => users.find(u => u.id === id));
});

// In resolver
resolve: (order) => userLoader.load(order.userId)
```

### Pagination (Relay-style)

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### Error Handling

```json
{
  "data": null,
  "errors": [
    {
      "message": "User not found",
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND",
        "id": "123"
      }
    }
  ]
}
```

### Federation (Microservices)

```graphql
# Users service
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

# Orders service
extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}
```

### Best Practices

- Use input types for mutations
- Implement cursor-based pagination
- Use DataLoader for N+1 prevention
- Add depth limiting to prevent DoS
- Implement query complexity analysis
- Use persisted queries in production
- Add field-level authorization

### Agent

faion-api-agent

---

## M-API-003: API Versioning

### Problem

APIs evolve, but breaking changes break clients. Need backward compatibility strategy.

### Framework

**Strategy Comparison:**

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **URL Path** | `/v1/users` | Clear, cacheable | URL pollution |
| **Query Param** | `/users?version=1` | Easy to add | Caching issues |
| **Header** | `Accept-Version: v1` | Clean URLs | Less visible |
| **Content-Type** | `Accept: application/vnd.api+json;v=1` | Standards-based | Complex |

### URL Path Versioning (Recommended)

```
/api/v1/users
/api/v2/users
```

**Implementation:**

```python
# Django/FastAPI
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users")
async def get_users_v1():
    return {"format": "v1", "users": [...]}

@v2_router.get("/users")
async def get_users_v2():
    return {"data": {"users": [...]}, "meta": {...}}
```

### Header Versioning

```http
GET /users HTTP/1.1
Host: api.example.com
Accept-Version: v2
```

```python
from fastapi import Header

@app.get("/users")
async def get_users(accept_version: str = Header("v1")):
    if accept_version == "v2":
        return v2_response()
    return v1_response()
```

### Deprecation Strategy

```http
HTTP/1.1 200 OK
Deprecation: Sun, 01 Jan 2026 00:00:00 GMT
Sunset: Sun, 01 Jul 2026 00:00:00 GMT
Link: </api/v2/users>; rel="successor-version"
```

**Response Warning:**

```json
{
  "data": [...],
  "_warnings": [
    {
      "code": "DEPRECATED_API",
      "message": "v1 API deprecated. Migrate to v2 by 2026-07-01",
      "documentation": "https://api.example.com/docs/migration"
    }
  ]
}
```

### Best Practices

- Default to latest stable version
- Support at least 2 versions simultaneously
- Announce deprecation 6+ months ahead
- Provide migration guides
- Log version usage for sunset planning
- Use feature flags for gradual rollout

### Agent

faion-api-agent

---

## M-API-004: OpenAPI Specification

### Problem

API documentation drifts from implementation. Need single source of truth.

### Framework

**OpenAPI 3.1 Structure:**

```yaml
openapi: 3.1.0
info:
  title: User Management API
  version: 1.0.0
  description: API for managing users and their resources
  contact:
    name: API Support
    email: api@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List all users
      operationId: listUsers
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/PageLimit'
        - $ref: '#/components/parameters/PageOffset'
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive]
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'
    post:
      summary: Create a new user
      operationId: createUser
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'

  /users/{userId}:
    get:
      summary: Get user by ID
      operationId: getUser
      tags: [Users]
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, email, name]
      properties:
        id:
          type: string
          format: uuid
          example: "550e8400-e29b-41d4-a716-446655440000"
        email:
          type: string
          format: email
          example: "user@example.com"
        name:
          type: string
          minLength: 1
          maxLength: 100
          example: "John Doe"
        status:
          type: string
          enum: [active, inactive]
          default: active
        createdAt:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required: [email, name]
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    PaginationMeta:
      type: object
      properties:
        total:
          type: integer
        limit:
          type: integer
        offset:
          type: integer

    Error:
      type: object
      required: [code, message]
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: array
          items:
            type: object

  parameters:
    UserId:
      name: userId
      in: path
      required: true
      schema:
        type: string
        format: uuid

    PageLimit:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    PageOffset:
      name: offset
      in: query
      schema:
        type: integer
        minimum: 0
        default: 0

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []

tags:
  - name: Users
    description: User management operations
```

### Code Generation

```bash
# Generate TypeScript client
npx openapi-typescript-codegen \
  --input ./openapi.yaml \
  --output ./src/api-client

# Generate Python client
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o ./python-client

# Generate server stubs
openapi-generator generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server
```

### Best Practices

- Use $ref for reusable components
- Include examples for every schema
- Add descriptions to all operations
- Use operationId for code generation
- Validate spec with spectral or redocly
- Version control your OpenAPI spec
- Generate SDK clients from spec

### Agent

faion-api-agent

---

## M-API-005: API Authentication

### Problem

APIs need secure, scalable authentication. Different use cases need different auth methods.

### Framework

**Auth Method Comparison:**

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| **API Keys** | Server-to-server | Simple, no expiry | Revocation hard |
| **JWT** | User sessions | Stateless, claims | Token size, revocation |
| **OAuth 2.0** | Third-party access | Scoped, standard | Complex implementation |
| **mTLS** | High-security | Very secure | Certificate management |

### API Keys

```http
GET /api/users HTTP/1.1
Authorization: Api-Key sk_live_abc123xyz
```

**Implementation:**

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    key = await db.api_keys.find(hashed=hash(x_api_key))
    if not key or key.revoked:
        raise HTTPException(401, "Invalid API key")
    if key.rate_limit_exceeded():
        raise HTTPException(429, "Rate limit exceeded")
    return key

@app.get("/users")
async def get_users(api_key: APIKey = Depends(verify_api_key)):
    # Authenticated request
    pass
```

**Best Practices:**
- Hash keys before storage (like passwords)
- Use prefix for identification: `sk_live_`, `sk_test_`
- Implement key rotation without downtime
- Log key usage for security audits

### JWT (JSON Web Tokens)

**Token Structure:**

```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Payload Claims:**

```json
{
  "sub": "user-123",
  "iss": "https://api.example.com",
  "aud": "https://api.example.com",
  "exp": 1735689600,
  "iat": 1735603200,
  "jti": "unique-token-id",
  "scope": "read:users write:users",
  "role": "admin"
}
```

**Implementation:**

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")
```

### OAuth 2.0 Flows

**Authorization Code (Web Apps):**

```
1. User clicks "Login with Google"
2. Redirect to: https://auth.example.com/authorize?
     client_id=abc&
     redirect_uri=https://app.com/callback&
     response_type=code&
     scope=read:profile&
     state=random123

3. User authenticates, grants permission
4. Redirect to: https://app.com/callback?code=AUTH_CODE&state=random123

5. Exchange code for tokens:
   POST https://auth.example.com/token
   grant_type=authorization_code&
   code=AUTH_CODE&
   client_id=abc&
   client_secret=xyz&
   redirect_uri=https://app.com/callback

6. Receive:
   {
     "access_token": "...",
     "refresh_token": "...",
     "expires_in": 3600,
     "token_type": "Bearer"
   }
```

**Client Credentials (Server-to-Server):**

```bash
curl -X POST https://auth.example.com/token \
  -d "grant_type=client_credentials" \
  -d "client_id=abc" \
  -d "client_secret=xyz" \
  -d "scope=read:users"
```

### Scope Management

```python
SCOPES = {
    "read:users": "Read user profiles",
    "write:users": "Create and update users",
    "delete:users": "Delete users",
    "admin": "Full administrative access"
}

def require_scope(required: str):
    def checker(token: dict = Depends(verify_token)):
        scopes = token.get("scope", "").split()
        if required not in scopes and "admin" not in scopes:
            raise HTTPException(403, f"Scope '{required}' required")
        return token
    return checker

@app.delete("/users/{id}")
async def delete_user(id: str, _: dict = Depends(require_scope("delete:users"))):
    pass
```

### Best Practices

- Use short-lived access tokens (15-60 min)
- Implement refresh token rotation
- Store secrets in environment variables
- Use HTTPS everywhere
- Implement token revocation
- Log authentication events
- Use asymmetric keys (RS256) for distributed systems

### Agent

faion-api-agent

---

## M-API-006: Rate Limiting

### Problem

APIs can be abused by malicious actors or overwhelmed by high traffic. Need protection.

### Framework

**Rate Limit Headers (Standard):**

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1735689600
Retry-After: 60
```

**429 Response:**

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60,
    "limit": 100,
    "window": "1h"
  }
}
```

### Algorithms

**Fixed Window:**

```python
# Simple but has burst at window edges
class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.counters = {}

    def is_allowed(self, key: str) -> bool:
        now = int(time.time())
        window_start = now - (now % self.window)
        counter_key = f"{key}:{window_start}"

        count = self.counters.get(counter_key, 0)
        if count >= self.limit:
            return False

        self.counters[counter_key] = count + 1
        return True
```

**Sliding Window:**

```python
# Smoother, no edge bursts
class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int, redis_client):
        self.limit = limit
        self.window = window_seconds
        self.redis = redis_client

    async def is_allowed(self, key: str) -> bool:
        now = time.time()
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - self.window)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, self.window)
        _, _, count, _ = await pipe.execute()
        return count <= self.limit
```

**Token Bucket:**

```python
# Allows bursts up to bucket size
class TokenBucketRateLimiter:
    def __init__(self, bucket_size: int, refill_rate: float):
        self.bucket_size = bucket_size
        self.refill_rate = refill_rate  # tokens per second
        self.buckets = {}

    def is_allowed(self, key: str, tokens: int = 1) -> bool:
        now = time.time()
        bucket = self.buckets.get(key, {
            "tokens": self.bucket_size,
            "last_refill": now
        })

        # Refill tokens
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(
            self.bucket_size,
            bucket["tokens"] + elapsed * self.refill_rate
        )
        bucket["last_refill"] = now

        # Check if allowed
        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            self.buckets[key] = bucket
            return True
        return False
```

### Implementation Strategies

**Per-User Limits:**

```python
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    user_id = get_user_from_request(request)
    key = f"rate_limit:{user_id}"

    if not await rate_limiter.is_allowed(key):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"},
            headers={"Retry-After": "60"}
        )

    return await call_next(request)
```

**Tiered Limits:**

| Tier | Requests/hour | Burst |
|------|---------------|-------|
| Free | 100 | 10 |
| Plus | 1,000 | 50 |
| Pro | 10,000 | 200 |
| Enterprise | Unlimited | N/A |

**Endpoint-Specific:**

```python
RATE_LIMITS = {
    "/api/search": {"limit": 10, "window": 60},
    "/api/export": {"limit": 5, "window": 3600},
    "/api/users": {"limit": 100, "window": 60}
}
```

### Best Practices

- Use sliding window for fairness
- Implement tiered limits by plan
- Return clear error messages
- Include Retry-After header
- Log rate limit events
- Use Redis for distributed rate limiting
- Whitelist internal services

### Agent

faion-api-agent

---

## M-API-007: Error Handling

### Problem

Inconsistent error responses make debugging difficult. Need standardized error format.

### Framework

**RFC 7807 (Problem Details):**

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 400,
  "detail": "The request body contains invalid fields",
  "instance": "/users/create",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Must be a valid email address"
    },
    {
      "field": "age",
      "code": "out_of_range",
      "message": "Must be between 18 and 120"
    }
  ],
  "traceId": "abc-123-xyz"
}
```

**Error Response Schema:**

```yaml
components:
  schemas:
    ProblemDetail:
      type: object
      required: [type, title, status]
      properties:
        type:
          type: string
          format: uri
          description: URI identifying the problem type
        title:
          type: string
          description: Short summary of the problem
        status:
          type: integer
          description: HTTP status code
        detail:
          type: string
          description: Detailed explanation
        instance:
          type: string
          format: uri
          description: URI of the specific occurrence
        traceId:
          type: string
          description: Request trace ID for debugging
        errors:
          type: array
          items:
            $ref: '#/components/schemas/FieldError'

    FieldError:
      type: object
      properties:
        field:
          type: string
        code:
          type: string
        message:
          type: string
```

### Error Codes

```python
class ErrorCode:
    # Client Errors (4xx)
    VALIDATION_ERROR = "validation_error"
    INVALID_FORMAT = "invalid_format"
    MISSING_FIELD = "missing_field"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    RATE_LIMITED = "rate_limited"

    # Server Errors (5xx)
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"
    TIMEOUT = "timeout"
```

### Implementation

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import uuid

class ProblemDetail(BaseModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    trace_id: str | None = None
    errors: list[dict] | None = None

app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=ProblemDetail(
            type="https://api.example.com/errors/validation-error",
            title="Validation Error",
            status=400,
            detail="Request validation failed",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4()),
            errors=[
                {"field": e["loc"][-1], "code": e["type"], "message": e["msg"]}
                for e in exc.errors()
            ]
        ).model_dump()
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Log the full exception for debugging
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content=ProblemDetail(
            type="https://api.example.com/errors/internal-error",
            title="Internal Server Error",
            status=500,
            detail="An unexpected error occurred",
            instance=str(request.url.path),
            trace_id=str(uuid.uuid4())
        ).model_dump()
    )
```

### Error Messages

| Type | Bad | Good |
|------|-----|------|
| Generic | "Error occurred" | "User not found with ID 'abc123'" |
| Technical | "NullPointerException" | "Required field 'email' is missing" |
| Actionable | "Invalid input" | "Email must be in format user@domain.com" |

### Best Practices

- Always include trace ID for debugging
- Use consistent error format across all endpoints
- Never expose internal errors to users
- Log detailed errors server-side
- Provide actionable error messages
- Document all error codes in API docs
- Include links to documentation in error type

### Agent

faion-api-agent

---

## M-API-008: API Documentation

### Problem

Good API needs good documentation. Developers won't use what they don't understand.

### Framework

**Documentation Tools:**

| Tool | Type | Best For |
|------|------|----------|
| **Swagger UI** | Interactive | Try-it-out testing |
| **Redoc** | Reference | Clean, readable docs |
| **Stoplight** | Design-first | Visual API design |
| **Postman** | Testing + Docs | Team collaboration |
| **AsyncAPI** | Event-driven | WebSocket, Kafka |

### Swagger UI Setup

```python
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="User Management API",
    description="""
    ## Overview

    This API provides user management capabilities.

    ## Authentication

    All endpoints require Bearer token authentication.

    ```
    Authorization: Bearer <your-token>
    ```

    ## Rate Limits

    - Free: 100 requests/hour
    - Pro: 10,000 requests/hour
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

### Documentation Structure

```markdown
# User Management API

## Overview
Brief description of what the API does.

## Quick Start
```bash
# Get your API key
curl -X POST https://api.example.com/auth/register

# Make your first request
curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.example.com/users
```

## Authentication
How to authenticate with the API.

## Endpoints
### Users
- GET /users - List all users
- POST /users - Create a user
- GET /users/{id} - Get user by ID

## Error Codes
| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check request body |
| 401 | Unauthorized | Verify API key |

## SDKs
- JavaScript: `npm install @example/api-client`
- Python: `pip install example-api`

## Changelog
### v1.1.0 (2026-01-15)
- Added user search endpoint
- Fixed pagination bug
```

### Code Examples

```yaml
# OpenAPI with examples
paths:
  /users:
    post:
      summary: Create user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
            examples:
              basic:
                summary: Basic user
                value:
                  name: "John Doe"
                  email: "john@example.com"
              with-role:
                summary: User with admin role
                value:
                  name: "Admin User"
                  email: "admin@example.com"
                  role: "admin"
```

### Best Practices

- Include working code examples in multiple languages
- Provide copy-paste ready curl commands
- Document all error scenarios
- Keep examples up-to-date with tests
- Add changelog for version history
- Include rate limit information
- Show authentication flow
- Provide SDKs for popular languages

### Agent

faion-api-agent

---

## M-API-009: API Testing

### Problem

APIs without tests break silently. Need comprehensive testing strategy.

### Framework

**Testing Pyramid:**

```
          /\
         /  \      E2E Tests (few)
        /----\     Integration Tests (some)
       /      \    Contract Tests (more)
      /--------\   Unit Tests (many)
     /__________\
```

### Contract Testing with Pact

**Consumer Side (Frontend):**

```javascript
const { Pact } = require('@pact-foundation/pact');

const provider = new Pact({
  consumer: 'Frontend',
  provider: 'UserAPI',
  port: 8080
});

describe('User API', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it('should get user by id', async () => {
    await provider.addInteraction({
      state: 'user exists',
      uponReceiving: 'a request for user 123',
      withRequest: {
        method: 'GET',
        path: '/users/123',
        headers: { Authorization: 'Bearer token' }
      },
      willRespondWith: {
        status: 200,
        body: {
          id: '123',
          name: Matchers.string('John'),
          email: Matchers.email()
        }
      }
    });

    const response = await userClient.getUser('123');
    expect(response.id).toBe('123');
  });
});
```

**Provider Side (Backend):**

```python
from pactman import verify_pacts

def test_provider():
    verify_pacts(
        pact_broker_url="https://pact-broker.example.com",
        provider="UserAPI",
        provider_base_url="http://localhost:8000",
        provider_states_url="http://localhost:8000/_pact/states"
    )
```

### Integration Testing

```python
import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestUsers:
    def test_create_user(self, client, auth_headers):
        response = client.post(
            "/users",
            json={"name": "New User", "email": "new@example.com"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["name"] == "New User"

    def test_get_user_not_found(self, client, auth_headers):
        response = client.get("/users/nonexistent", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["type"].endswith("/not-found")

    def test_validation_error(self, client, auth_headers):
        response = client.post(
            "/users",
            json={"name": "", "email": "invalid"},
            headers=auth_headers
        )
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert any(e["field"] == "email" for e in errors)
```

### OpenAPI Validation

```python
from openapi_core import OpenAPI
from openapi_core.testing.mock import MockRequest, MockResponse

spec = OpenAPI.from_file_path("openapi.yaml")

def test_response_matches_spec():
    response = client.get("/users")

    mock_request = MockRequest("http://localhost", "GET", "/users")
    mock_response = MockResponse(
        data=response.content,
        status_code=response.status_code
    )

    result = spec.validate_response(mock_request, mock_response)
    assert not result.errors
```

### Postman Collection

```json
{
  "info": {
    "name": "User API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create User",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Authorization", "value": "Bearer {{token}}"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"name\": \"Test\", \"email\": \"test@example.com\"}"
        },
        "url": "{{baseUrl}}/users"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status is 201', () => pm.response.to.have.status(201));",
              "pm.test('Has user ID', () => pm.expect(pm.response.json().id).to.exist);"
            ]
          }
        }
      ]
    }
  ]
}
```

### Best Practices

- Test happy path and error scenarios
- Use contract tests for consumer-provider relationships
- Validate responses against OpenAPI spec
- Run tests in CI/CD pipeline
- Mock external dependencies
- Test rate limiting behavior
- Include security tests (auth, injection)

### Agent

faion-api-agent

---

## M-API-010: API Monitoring

### Problem

APIs fail silently without monitoring. Need visibility into health, performance, and errors.

### Framework

**Key Metrics:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Availability | 99.9% | < 99% |
| Response Time (p50) | < 100ms | > 200ms |
| Response Time (p95) | < 500ms | > 1s |
| Response Time (p99) | < 1s | > 2s |
| Error Rate | < 0.1% | > 1% |
| Rate Limit Hits | Low | Sudden spike |

### Health Check Endpoints

```python
from fastapi import FastAPI, Response
from datetime import datetime
import asyncpg
import aioredis

app = FastAPI()

@app.get("/health")
async def health_check():
    """Simple liveness probe."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health/ready")
async def readiness_check():
    """Comprehensive readiness probe."""
    checks = {}

    # Database
    try:
        async with asyncpg.create_pool(DATABASE_URL) as pool:
            await pool.fetchval("SELECT 1")
        checks["database"] = {"status": "ok"}
    except Exception as e:
        checks["database"] = {"status": "error", "error": str(e)}

    # Redis
    try:
        redis = await aioredis.from_url(REDIS_URL)
        await redis.ping()
        checks["redis"] = {"status": "ok"}
    except Exception as e:
        checks["redis"] = {"status": "error", "error": str(e)}

    # External API
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://api.stripe.com/health", timeout=5)
            checks["stripe"] = {"status": "ok" if r.status_code == 200 else "degraded"}
    except Exception as e:
        checks["stripe"] = {"status": "error", "error": str(e)}

    all_ok = all(c["status"] == "ok" for c in checks.values())

    return Response(
        content=json.dumps({
            "status": "ok" if all_ok else "degraded",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        }),
        status_code=200 if all_ok else 503,
        media_type="application/json"
    )
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware
import time

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        latency = time.time() - start_time
        endpoint = request.url.path
        method = request.method
        status = response.status_code

        REQUEST_COUNT.labels(method, endpoint, status).inc()
        REQUEST_LATENCY.labels(method, endpoint).observe(latency)

        return response

app.add_middleware(MetricsMiddleware)

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Logging

```python
import structlog
import uuid

logger = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    log = logger.bind(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host
    )

    log.info("request_started")
    start = time.time()

    try:
        response = await call_next(request)
        log.info(
            "request_completed",
            status=response.status_code,
            duration_ms=round((time.time() - start) * 1000, 2)
        )
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        log.error("request_failed", error=str(e))
        raise
```

### Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"

      - alert: SlowResponses
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency above 1s"

      - alert: HighRateLimitHits
        expr: rate(rate_limit_exceeded_total[5m]) > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High rate of rate limit hits"
```

### Best Practices

- Implement both liveness and readiness probes
- Use structured logging (JSON)
- Include request ID in all logs
- Set up dashboards for key metrics
- Configure alerts for SLO breaches
- Monitor downstream dependencies
- Track business metrics alongside technical

### Agent

faion-api-agent

---

## M-API-011: API Gateway Patterns

### Problem

Direct API access creates security, scaling, and management challenges. Need unified entry point.

### Framework

**Gateway Functions:**

| Function | Description |
|----------|-------------|
| Routing | Direct requests to correct service |
| Load Balancing | Distribute traffic across instances |
| Authentication | Validate tokens, API keys |
| Rate Limiting | Protect services from overload |
| Caching | Reduce backend load |
| Request/Response Transform | Modify payloads |
| SSL Termination | Handle HTTPS |
| Logging/Monitoring | Centralized observability |

### Kong Gateway

```yaml
# kong.yml
_format_version: "3.0"

services:
  - name: user-service
    url: http://user-service:8080
    routes:
      - name: users-route
        paths:
          - /api/users
        strip_path: false

  - name: order-service
    url: http://order-service:8080
    routes:
      - name: orders-route
        paths:
          - /api/orders

plugins:
  - name: rate-limiting
    config:
      minute: 100
      policy: local

  - name: jwt
    config:
      secret_is_base64: false
      claims_to_verify:
        - exp

  - name: cors
    config:
      origins:
        - https://app.example.com
      methods:
        - GET
        - POST
        - PUT
        - DELETE
      headers:
        - Authorization
        - Content-Type

  - name: request-transformer
    config:
      add:
        headers:
          - X-Request-ID:$(uuid)
```

### AWS API Gateway

```yaml
# serverless.yml (Serverless Framework)
service: user-api

provider:
  name: aws
  runtime: python3.11

functions:
  getUsers:
    handler: handlers.get_users
    events:
      - http:
          path: /users
          method: get
          cors: true
          authorizer:
            type: COGNITO_USER_POOLS
            authorizerId:
              Ref: ApiGatewayAuthorizer

  createUser:
    handler: handlers.create_user
    events:
      - http:
          path: /users
          method: post
          cors: true

resources:
  Resources:
    ApiGatewayAuthorizer:
      Type: AWS::ApiGateway::Authorizer
      Properties:
        Name: CognitoAuthorizer
        Type: COGNITO_USER_POOLS
        IdentitySource: method.request.header.Authorization
        RestApiId:
          Ref: ApiGatewayRestApi
        ProviderARNs:
          - arn:aws:cognito-idp:us-east-1:123456789:userpool/us-east-1_abc123

    UsagePlan:
      Type: AWS::ApiGateway::UsagePlan
      Properties:
        UsagePlanName: BasicPlan
        Throttle:
          BurstLimit: 100
          RateLimit: 50
        Quota:
          Limit: 1000
          Period: DAY
```

### Nginx as Gateway

```nginx
# /etc/nginx/nginx.conf
upstream user_service {
    server user-service-1:8080 weight=3;
    server user-service-2:8080 weight=2;
    keepalive 32;
}

upstream order_service {
    server order-service:8080;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/ssl/certs/api.crt;
    ssl_certificate_key /etc/ssl/private/api.key;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # CORS
    add_header 'Access-Control-Allow-Origin' 'https://app.example.com';
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS';

    location /api/users {
        proxy_pass http://user_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Request-ID $request_id;
    }

    location /api/orders {
        proxy_pass http://order_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Health check
    location /health {
        return 200 '{"status":"ok"}';
        add_header Content-Type application/json;
    }
}
```

### Gateway Patterns

**Backend for Frontend (BFF):**

```
Mobile App  →  Mobile BFF  →  Microservices
Web App     →  Web BFF     →  Microservices
```

**API Composition:**

```python
# Gateway aggregates multiple service calls
@app.get("/api/dashboard")
async def get_dashboard(user_id: str):
    async with httpx.AsyncClient() as client:
        user, orders, notifications = await asyncio.gather(
            client.get(f"http://user-service/users/{user_id}"),
            client.get(f"http://order-service/users/{user_id}/orders?limit=5"),
            client.get(f"http://notification-service/users/{user_id}/unread")
        )

    return {
        "user": user.json(),
        "recentOrders": orders.json(),
        "notifications": notifications.json()
    }
```

### Best Practices

- Keep gateway stateless
- Implement circuit breakers
- Cache responses at edge
- Use async for downstream calls
- Monitor gateway performance
- Version gateway configuration
- Implement request tracing

### Agent

faion-api-agent

---

## M-API-012: Contract-First Development

### Problem

Code-first leads to inconsistent APIs. Teams wait for implementation to integrate.

### Framework

**Development Workflow:**

```
1. Design API (OpenAPI spec)
        ↓
2. Review & Approve (Team)
        ↓
3. Generate (Server stubs, Client SDKs, Tests)
        ↓
4. Implement (Fill in business logic)
        ↓
5. Validate (Spec compliance)
        ↓
6. Deploy
```

### Design Phase

```yaml
# 1. Start with OpenAPI spec
openapi: 3.1.0
info:
  title: Payment API
  version: 1.0.0

paths:
  /payments:
    post:
      operationId: createPayment
      summary: Create a new payment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePaymentRequest'
      responses:
        '201':
          description: Payment created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Payment'
        '400':
          $ref: '#/components/responses/ValidationError'

components:
  schemas:
    CreatePaymentRequest:
      type: object
      required: [amount, currency, customer_id]
      properties:
        amount:
          type: integer
          minimum: 1
          description: Amount in cents
        currency:
          type: string
          enum: [USD, EUR, GBP]
        customer_id:
          type: string
          format: uuid
```

### Code Generation

```bash
# Generate Python server with FastAPI
openapi-generator generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server \
  --additional-properties=packageName=payment_api

# Generate TypeScript client
openapi-generator generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./client

# Generate test stubs
openapi-generator generate \
  -i openapi.yaml \
  -g python \
  -o ./tests \
  --global-property=apiTests=true
```

### Implementation

```python
# Generated stub (server/payment_api/apis/payments_api.py)
from payment_api.models import CreatePaymentRequest, Payment

class PaymentsApi:
    async def create_payment(
        self,
        create_payment_request: CreatePaymentRequest
    ) -> Payment:
        # TODO: Implement business logic
        raise NotImplementedError()

# Your implementation
class PaymentsApiImpl(PaymentsApi):
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    async def create_payment(
        self,
        create_payment_request: CreatePaymentRequest
    ) -> Payment:
        payment = await self.payment_service.process_payment(
            amount=create_payment_request.amount,
            currency=create_payment_request.currency,
            customer_id=create_payment_request.customer_id
        )
        return Payment(
            id=payment.id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status
        )
```

### Validation

```python
# Validate implementation against spec
from openapi_core import OpenAPI
from openapi_core.testing.mock import MockRequest, MockResponse

spec = OpenAPI.from_file_path("openapi.yaml")

def test_create_payment_matches_spec():
    # Make real request
    response = client.post("/payments", json={
        "amount": 1000,
        "currency": "USD",
        "customer_id": "550e8400-e29b-41d4-a716-446655440000"
    })

    # Validate against spec
    mock_request = MockRequest("http://localhost", "POST", "/payments")
    mock_response = MockResponse(
        data=response.content,
        status_code=response.status_code
    )

    result = spec.validate_response(mock_request, mock_response)
    assert not result.errors, f"Spec validation failed: {result.errors}"
```

### Linting & Review

```bash
# Lint OpenAPI spec with Spectral
spectral lint openapi.yaml

# Rules (.spectral.yaml)
extends: spectral:oas
rules:
  operation-operationId: error
  operation-description: warn
  info-contact: warn
  oas3-schema: error

# Redocly CLI for validation
redocly lint openapi.yaml
redocly preview-docs openapi.yaml
```

### CI/CD Integration

```yaml
# .github/workflows/api.yml
name: API Contract CI

on:
  pull_request:
    paths:
      - 'openapi.yaml'
      - 'server/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint OpenAPI spec
        run: npx spectral lint openapi.yaml

      - name: Generate server code
        run: |
          openapi-generator generate \
            -i openapi.yaml \
            -g python-fastapi \
            -o ./generated

      - name: Compare with implementation
        run: diff -r ./generated/models ./server/models

      - name: Run contract tests
        run: pytest tests/contract/
```

### Best Practices

- Treat OpenAPI spec as source of truth
- Review spec changes like code
- Regenerate clients on spec changes
- Run spec validation in CI
- Use breaking change detection
- Version your API contracts
- Generate documentation from spec

### Agent

faion-api-agent

---

## Quick Audit Checklist

### REST API Review

- [ ] Resources use nouns (not verbs)
- [ ] HTTP methods used correctly
- [ ] Status codes are appropriate
- [ ] Consistent error format (RFC 7807)
- [ ] Pagination implemented
- [ ] Rate limiting headers included

### Security Review

- [ ] Authentication implemented (JWT/OAuth/API Key)
- [ ] Authorization checked per endpoint
- [ ] Input validation on all fields
- [ ] HTTPS enforced
- [ ] CORS configured properly
- [ ] Sensitive data not exposed in errors

### Documentation Review

- [ ] OpenAPI spec complete and current
- [ ] All endpoints documented
- [ ] Examples for every request/response
- [ ] Error codes documented
- [ ] Authentication flow explained

### Testing Review

- [ ] Unit tests for business logic
- [ ] Integration tests for endpoints
- [ ] Contract tests with consumers
- [ ] Security/penetration tests
- [ ] Load tests for performance

---

## Tools

| Tool | Purpose |
|------|---------|
| [Swagger Editor](https://editor.swagger.io/) | OpenAPI design |
| [Postman](https://postman.com/) | API testing, docs |
| [Insomnia](https://insomnia.rest/) | API client |
| [Pact](https://pact.io/) | Contract testing |
| [Spectral](https://stoplight.io/spectral) | OpenAPI linting |
| [Kong](https://konghq.com/) | API Gateway |
| [Prometheus](https://prometheus.io/) | Metrics collection |
| [Grafana](https://grafana.com/) | Dashboards |

---

## Sources

- [REST API Design Rulebook](https://www.oreilly.com/library/view/rest-api-design/9781449317904/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [RFC 7807 - Problem Details](https://www.rfc-editor.org/rfc/rfc7807)
- [OAuth 2.0 RFC 6749](https://www.rfc-editor.org/rfc/rfc6749)
- [JWT RFC 7519](https://www.rfc-editor.org/rfc/rfc7519)
- [Google API Design Guide](https://cloud.google.com/apis/design)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-API-001 | Rest Api Design | [methodologies/M-API-001_rest_api_design.md](methodologies/M-API-001_rest_api_design.md) |
| M-API-002 | Graphql Patterns | [methodologies/M-API-002_graphql_patterns.md](methodologies/M-API-002_graphql_patterns.md) |
| M-API-003 | Api Versioning | [methodologies/M-API-003_api_versioning.md](methodologies/M-API-003_api_versioning.md) |
| M-API-004 | Openapi Specification | [methodologies/M-API-004_openapi_specification.md](methodologies/M-API-004_openapi_specification.md) |
| M-API-005 | Api Authentication | [methodologies/M-API-005_api_authentication.md](methodologies/M-API-005_api_authentication.md) |
| M-API-006 | Rate Limiting | [methodologies/M-API-006_rate_limiting.md](methodologies/M-API-006_rate_limiting.md) |
| M-API-007 | Error Handling | [methodologies/M-API-007_error_handling.md](methodologies/M-API-007_error_handling.md) |
| M-API-008 | Api Documentation | [methodologies/M-API-008_api_documentation.md](methodologies/M-API-008_api_documentation.md) |
| M-API-009 | Api Testing | [methodologies/M-API-009_api_testing.md](methodologies/M-API-009_api_testing.md) |
| M-API-010 | Api Monitoring | [methodologies/M-API-010_api_monitoring.md](methodologies/M-API-010_api_monitoring.md) |
| M-API-011 | Api Gateway Patterns | [methodologies/M-API-011_api_gateway_patterns.md](methodologies/M-API-011_api_gateway_patterns.md) |
| M-API-012 | Contract First Development | [methodologies/M-API-012_contract_first_development.md](methodologies/M-API-012_contract_first_development.md) |
