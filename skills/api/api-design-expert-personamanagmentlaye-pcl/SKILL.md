---
name: api-design-expert
version: 1.0.0
description: Expert-level API design principles, REST, GraphQL, versioning, and API best practices
category: api
tags: [api-design, rest, graphql, api-versioning, api-security]
allowed-tools:
  - Read
  - Write
  - Edit
---

# API Design Expert

Expert guidance for API design, RESTful principles, GraphQL, versioning strategies, and API best practices.

## Core Concepts

### API Design Principles
- RESTful architecture
- Resource-oriented design
- Uniform interface
- Statelessness
- Cacheability
- Layered system

### API Styles
- REST (Representational State Transfer)
- GraphQL
- RPC (Remote Procedure Call)
- WebSocket
- Server-Sent Events (SSE)
- gRPC

### Key Considerations
- Versioning strategies
- Authentication and authorization
- Rate limiting
- Error handling
- Documentation
- Backward compatibility

## REST API Design

```python
from fastapi import FastAPI, HTTPException, Query, Path, Header
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="User Management API",
    version="1.0.0",
    description="RESTful API for user management"
)

# Models
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.USER

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "name": "John Doe",
                "role": "user",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None

# REST Endpoints following best practices
@app.get("/api/v1/users",
         response_model=List[UserResponse],
         summary="List all users",
         tags=["Users"])
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort: str = Query("created_at", description="Sort field"),
    order: str = Query("desc", regex="^(asc|desc)$")
):
    """
    Retrieve a paginated list of users.

    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (1-100)
    - **sort**: Field to sort by
    - **order**: Sort order (asc or desc)
    """
    # Implementation
    return []

@app.get("/api/v1/users/{user_id}",
         response_model=UserResponse,
         summary="Get user by ID",
         tags=["Users"])
async def get_user(
    user_id: str = Path(..., description="User ID")
):
    """Retrieve a specific user by ID."""
    # Implementation
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/v1/users",
          response_model=UserResponse,
          status_code=201,
          summary="Create new user",
          tags=["Users"])
async def create_user(user: UserCreate):
    """Create a new user."""
    # Implementation
    return UserResponse(
        id="123e4567-e89b-12d3-a456-426614174000",
        email=user.email,
        name=user.name,
        role=user.role,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@app.patch("/api/v1/users/{user_id}",
           response_model=UserResponse,
           summary="Update user",
           tags=["Users"])
async def update_user(
    user_id: str = Path(..., description="User ID"),
    user: UserUpdate = None
):
    """Partially update a user."""
    # Implementation
    pass

@app.delete("/api/v1/users/{user_id}",
            status_code=204,
            summary="Delete user",
            tags=["Users"])
async def delete_user(
    user_id: str = Path(..., description="User ID")
):
    """Delete a user."""
    # Implementation
    pass

# Nested resources
@app.get("/api/v1/users/{user_id}/posts",
         summary="Get user posts",
         tags=["Users", "Posts"])
async def get_user_posts(user_id: str):
    """Retrieve all posts for a specific user."""
    return []
```

## API Versioning

```python
from fastapi import APIRouter, Request

# URL Path Versioning (Recommended)
v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users")
async def get_users_v1():
    """Version 1: Returns basic user info"""
    return [{"id": 1, "name": "John"}]

@v2_router.get("/users")
async def get_users_v2():
    """Version 2: Returns enhanced user info"""
    return [{"id": 1, "name": "John", "email": "john@example.com"}]

# Header Versioning
async def version_from_header(request: Request):
    version = request.headers.get("API-Version", "1")
    return version

@app.get("/api/users")
async def get_users(version: str = Depends(version_from_header)):
    if version == "2":
        return get_users_v2()
    return get_users_v1()

# Content Negotiation Versioning
@app.get("/api/users")
async def get_users_content_negotiation(
    accept: str = Header("application/vnd.api+json; version=1")
):
    if "version=2" in accept:
        return get_users_v2()
    return get_users_v1()
```

## Error Handling

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None
    timestamp: datetime
    path: str

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.status_code,
            message=exc.detail,
            timestamp=datetime.now(),
            path=request.url.path
        ).dict()
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="validation_error",
            message="Request validation failed",
            details=exc.errors(),
            timestamp=datetime.now(),
            path=request.url.path
        ).dict()
    )

# Custom business logic errors
class BusinessError(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=exc.code,
            message=exc.message,
            timestamp=datetime.now(),
            path=request.url.path
        ).dict()
    )
```

## Rate Limiting

```python
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
import redis
from typing import Dict

class RateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def check_rate_limit(self,
                               key: str,
                               max_requests: int,
                               window_seconds: int) -> Dict:
        """
        Token bucket algorithm for rate limiting
        """
        now = datetime.now().timestamp()
        window_key = f"rate_limit:{key}:{int(now // window_seconds)}"

        pipe = self.redis.pipeline()
        pipe.incr(window_key)
        pipe.expire(window_key, window_seconds)
        result = pipe.execute()

        request_count = result[0]

        if request_count > max_requests:
            reset_time = (int(now // window_seconds) + 1) * window_seconds
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time)
                }
            )

        return {
            "limit": max_requests,
            "remaining": max_requests - request_count,
            "reset": (int(now // window_seconds) + 1) * window_seconds
        }

# Middleware for rate limiting
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    limiter = RateLimiter(redis_client)

    # Get client identifier (IP, API key, etc.)
    client_id = request.client.host

    try:
        rate_info = await limiter.check_rate_limit(
            client_id,
            max_requests=100,
            window_seconds=60
        )

        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset"])

        return response
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"error": e.detail},
            headers=e.headers
        )
```

## HATEOAS Implementation

```python
from typing import Dict, List

class HATEOASResponse(BaseModel):
    data: dict
    links: Dict[str, str]

def create_links(resource_id: str, resource_type: str) -> Dict[str, str]:
    """Create HATEOAS links for a resource"""
    return {
        "self": f"/api/v1/{resource_type}/{resource_id}",
        "update": f"/api/v1/{resource_type}/{resource_id}",
        "delete": f"/api/v1/{resource_type}/{resource_id}",
        "collection": f"/api/v1/{resource_type}"
    }

@app.get("/api/v1/users/{user_id}", response_model=HATEOASResponse)
async def get_user_with_links(user_id: str):
    user = get_user_from_db(user_id)

    return HATEOASResponse(
        data=user,
        links={
            "self": f"/api/v1/users/{user_id}",
            "posts": f"/api/v1/users/{user_id}/posts",
            "profile": f"/api/v1/users/{user_id}/profile",
            "update": f"/api/v1/users/{user_id}",
            "delete": f"/api/v1/users/{user_id}"
        }
    )
```

## API Security

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

@app.get("/api/v1/protected")
async def protected_route(token_payload: dict = Depends(verify_token)):
    return {"message": "Access granted", "user": token_payload}

# API Key Authentication
async def verify_api_key(api_key: str = Header(...)):
    """Verify API key"""
    if api_key not in valid_api_keys:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

## Best Practices

### Design
- Use nouns for resources, not verbs
- Use plural names for collections
- Use HTTP methods correctly (GET, POST, PUT, PATCH, DELETE)
- Return appropriate status codes
- Support filtering, sorting, and pagination
- Use consistent naming conventions
- Version APIs from the start

### Documentation
- Use OpenAPI/Swagger
- Provide example requests and responses
- Document error codes and messages
- Include authentication requirements
- Keep documentation up-to-date
- Provide SDKs when possible

### Performance
- Implement caching (ETags, Cache-Control)
- Support compression (gzip)
- Paginate large result sets
- Use async operations for long tasks
- Implement rate limiting
- Monitor API performance

### Security
- Use HTTPS always
- Implement authentication and authorization
- Validate all inputs
- Rate limit to prevent abuse
- Log security events
- Use API keys or OAuth 2.0
- Implement CORS properly

## Anti-Patterns

❌ Using GET for state-changing operations
❌ Returning inconsistent response formats
❌ No versioning strategy
❌ Poor error messages
❌ No rate limiting
❌ Exposing internal implementation details
❌ Breaking changes without versioning

## Resources

- REST API Design Best Practices: https://restfulapi.net/
- OpenAPI Specification: https://swagger.io/specification/
- API Design Guide: https://cloud.google.com/apis/design
- Microsoft REST API Guidelines: https://github.com/microsoft/api-guidelines
- FastAPI: https://fastapi.tiangolo.com/
