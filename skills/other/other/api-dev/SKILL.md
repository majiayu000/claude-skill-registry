---
name: api-dev
description: Modern API development patterns for building high-performance, scalable web services. Expert in async/await patterns, REST/GraphQL APIs, middleware, error handling, rate limiting, OpenAPI documentation, testing, and production optimizations. Framework-agnostic patterns that work with Python, Node.js, Go, and other languages.
license: MIT
---

# API Development Patterns & Best Practices

This skill provides comprehensive patterns for building modern APIs in 2025, focusing on async/await patterns, performance optimization, security, testing, and production-ready configurations that work across different frameworks and languages.

## When to Use This Skill

Use this skill when you need to:
- Design RESTful or GraphQL APIs
- Implement async/await patterns for high performance
- Add middleware for authentication, logging, and validation
- Handle errors gracefully with proper HTTP status codes
- Implement rate limiting and throttling
- Generate OpenAPI/Swagger documentation
- Set up comprehensive testing strategies
- Optimize API performance with caching and connection pooling
- Implement API versioning and backward compatibility
- Set up monitoring and observability

## Core API Design Principles

### 1. Async/Await Patterns for Performance

```python
# patterns/async_patterns.py
import asyncio
import aiohttp
import aioredis
from typing import AsyncGenerator, Optional, List, Dict, Any
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import wraps
import time

@dataclass
class RequestMetrics:
    """Request metrics for monitoring"""
    duration: float
    status_code: int
    endpoint: str
    method: str
    user_id: Optional[str] = None

def with_metrics(func):
    """Decorator to add request metrics"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        status_code = 200
        endpoint = func.__name__
        method = kwargs.get('method', 'GET')

        try:
            result = await func(*args, **kwargs)
            if hasattr(result, 'status_code'):
                status_code = result.status_code
            return result
        except Exception as e:
            status_code = getattr(e, 'status_code', 500)
            raise
        finally:
            duration = time.time() - start_time
            metrics = RequestMetrics(
                duration=duration,
                status_code=status_code,
                endpoint=endpoint,
                method=method
            )
            # Send metrics to monitoring system
            await send_metrics(metrics)

    return wrapper

async def send_metrics(metrics: RequestMetrics):
    """Send metrics to monitoring system"""
    # Implementation depends on your monitoring system
    # Example: Prometheus, Datadog, or custom analytics
    pass

class AsyncAPIClient:
    """Generic async API client with connection pooling"""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_lock = asyncio.Lock()

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create session with connection pooling"""
        if self._session is None or self._session.closed:
            async with self._session_lock:
                if self._session is None or self._session.closed:
                    connector = aiohttp.TCPConnector(
                        limit=100,  # Total connection pool size
                        limit_per_host=30,  # Connections per host
                        force_close=False,
                        enable_cleanup_closed=True
                    )
                    self._session = aiohttp.ClientSession(
                        connector=connector,
                        timeout=self.timeout
                    )
        return self._session

    @with_metrics
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make GET request with retry logic"""
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"

        async with session.get(
            url,
            params=params,
            headers=headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    @with_metrics
    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make POST request with retry logic"""
        session = await self._get_session()
        url = f"{self.base_url}{endpoint}"

        async with session.post(
            url,
            data=data,
            json=json,
            headers=headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self):
        """Close the session"""
        if self._session:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
```

### 2. Circuit Breaker Pattern

```python
# patterns/circuit_breaker.py
import asyncio
import time
from enum import Enum
from typing import Callable, Any, Optional
from functools import wraps

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """Circuit breaker for fault tolerance"""

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: int = 60,
        expected_exception: Exception = Exception
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker is OPEN")

            try:
                result = await func(*args, **kwargs)
                if self.state == CircuitState.HALF_OPEN:
                    self._reset()
                return result
            except self.expected_exception as e:
                self._record_failure()
                raise

        return wrapper

    def _should_attempt_reset(self) -> bool:
        return time.time() - self.last_failure_time >= self.timeout

    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _reset(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

# Usage example
@circuit_breaker(failure_threshold=3, timeout=30)
async def external_api_call():
    """External API call with circuit breaker"""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as response:
            return await response.json()
```

### 3. Rate Limiting with Redis

```python
# patterns/rate_limiting.py
import asyncio
import aioredis
import time
from typing import Optional
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimiter:
    """Rate limiter using Redis sliding window"""

    def __init__(
        self,
        redis_url: str,
        requests_per_minute: int = 100,
        window_size: int = 60
    ):
        self.redis = None
        self.redis_url = redis_url
        self.requests_per_minute = requests_per_minute
        self.window_size = window_size

    async def initialize(self):
        """Initialize Redis connection"""
        self.redis = await aioredis.from_url(self.redis_url)

    async def is_allowed(
        self,
        key: str,
        limit: Optional[int] = None,
        window: Optional[int] = None
    ) -> bool:
        """Check if request is allowed"""
        if not self.redis:
            await self.initialize()

        limit = limit or self.requests_per_minute
        window = window or self.window_size
        current_time = time.time()

        # Remove old requests from the sliding window
        await self.redis.zremrangebyscore(
            key,
            0,
            current_time - window
        )

        # Count current requests in window
        current_requests = await self.redis.zcard(key)

        if current_requests >= limit:
            return False

        # Add current request to window
        await self.redis.zadd(key, {str(current_time): current_time})
        await self.redis.expire(key, window)

        return True

class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for rate limiting"""

    def __init__(
        self,
        app,
        redis_url: str,
        requests_per_minute: int = 100,
        identifier_func=None
    ):
        super().__init__(app)
        self.limiter = RateLimiter(redis_url, requests_per_minute)
        self.identifier_func = identifier_func or self._default_identifier

    def _default_identifier(self, request: Request) -> str:
        """Default identifier function"""
        # Use IP address as identifier
        return request.client.host

    async def dispatch(self, request: Request, call_next):
        identifier = self.identifier_func(request)
        key = f"rate_limit:{identifier}:{request.url.path}"

        if not await self.limiter.is_allowed(key):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )

        return await call_next(request)
```

### 4. API Versioning Strategy

```python
# patterns/versioning.py
from enum import Enum
from typing import Optional, Dict, Any, Type
from abc import ABC, abstractmethod

class APIVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"

class APIVersionStrategy(ABC):
    """Base class for API versioning strategies"""

    @abstractmethod
    def get_version_from_request(self, request) -> Optional[APIVersion]:
        """Extract version from request"""
        pass

class HeaderVersionStrategy(APIVersionStrategy):
    """Version from header strategy"""

    def __init__(self, header_name: str = "API-Version"):
        self.header_name = header_name

    def get_version_from_request(self, request) -> Optional[APIVersion]:
        version = request.headers.get(self.header_name)
        return APIVersion(version) if version in APIVersion.__members__ else None

class URLPathVersionStrategy(APIVersionStrategy):
    """Version from URL path strategy"""

    def __init__(self, prefix: str = "/api"):
        self.prefix = prefix

    def get_version_from_request(self, request) -> Optional[APIVersion]:
        path = request.url.path
        if not path.startswith(self.prefix):
            return None

        version_part = path[len(self.prefix):].split("/")[1]
        return APIVersion(version_part) if version_part in APIVersion.__members__ else None

class QueryParamVersionStrategy(APIVersionStrategy):
    """Version from query parameter strategy"""

    def __init__(self, param_name: str = "version"):
        self.param_name = param_name

    def get_version_from_request(self, request) -> Optional[APIVersion]:
        version = request.query_params.get(self.param_name)
        return APIVersion(version) if version in APIVersion.__members__ else None

class CompositeVersionStrategy(APIVersionStrategy):
    """Composite version strategy that tries multiple strategies"""

    def __init__(self, strategies: list[APIVersionStrategy]):
        self.strategies = strategies
        self.default_version = APIVersion.V1

    def get_version_from_request(self, request) -> Optional[APIVersion]:
        for strategy in self.strategies:
            version = strategy.get_version_from_request(request)
            if version:
                return version
        return self.default_version

# Version-specific handlers
class APIHandlerRegistry:
    """Registry for version-specific API handlers"""

    def __init__(self):
        self.handlers: Dict[APIVersion, Dict[str, Any]] = {
            version: {} for version in APIVersion
        }

    def register_handler(
        self,
        version: APIVersion,
        endpoint: str,
        handler: Any
    ):
        """Register handler for specific version"""
        if version not in self.handlers:
            self.handlers[version] = {}
        self.handlers[version][endpoint] = handler

    def get_handler(self, version: APIVersion, endpoint: str) -> Optional[Any]:
        """Get handler for version and endpoint"""
        return self.handlers.get(version, {}).get(endpoint)

# Usage example
version_strategy = CompositeVersionStrategy([
    HeaderVersionStrategy(),
    URLPathVersionStrategy(),
    QueryParamVersionStrategy()
])
```

### 5. OpenAPI Documentation Enhancement

```python
# patterns/openapi.py
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class ErrorSchema(BaseModel):
    """Standard error response schema"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional error details"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )

class PaginationLinks(BaseModel):
    """Pagination links schema"""
    first: Optional[str] = Field(None, description="First page link")
    last: Optional[str] = Field(None, description="Last page link")
    next: Optional[str] = Field(None, description="Next page link")
    prev: Optional[str] = Field(None, description="Previous page link")

class PaginationMeta(BaseModel):
    """Pagination metadata schema"""
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")

class PaginatedResponse(BaseModel):
    """Generic paginated response schema"""
    data: List[Any] = Field(..., description="Response data")
    meta: PaginationMeta = Field(..., description="Pagination metadata")
    links: PaginationLinks = Field(..., description="Pagination links")

# Enhanced OpenAPI configuration
OPENAPI_CONFIG = {
    "title": "Modern API",
    "description": "A modern REST API with async patterns",
    "version": "1.0.0",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_url": "/openapi.json",
    "servers": [
        {
            "url": "https://api.example.com/v1",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.example.com/v1",
            "description": "Staging server"
        }
    ],
    "components": {
        "schemas": {
            "Error": ErrorSchema.model_json_schema(),
            "PaginatedResponse": PaginatedResponse.model_json_schema()
        },
        "responses": {
            "ValidationError": {
                "description": "Validation error",
                "content": {
                    "application/json": {
                        "schema": ErrorSchema.model_json_schema()
                    }
                }
            },
            "UnauthorizedError": {
                "description": "Unauthorized error",
                "content": {
                    "application/json": {
                        "schema": ErrorSchema.model_json_schema()
                    }
                }
            },
            "NotFoundError": {
                "description": "Resource not found",
                "content": {
                    "application/json": {
                        "schema": ErrorSchema.model_json_schema()
                    }
                }
            },
            "RateLimitError": {
                "description": "Rate limit exceeded",
                "content": {
                    "application/json": {
                        "schema": ErrorSchema.model_json_schema()
                    }
                }
            }
        }
    }
}
```

### 6. Testing Patterns for APIs

```python
# patterns/testing.py
import pytest
import asyncio
from typing import AsyncGenerator
import httpx
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

class AsyncAPITestCase:
    """Base class for async API tests"""

    @pytest.fixture(scope="class")
    async def async_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Create async test client"""
        async with httpx.AsyncClient(
            app=self.app,
            base_url="http://test"
        ) as client:
            yield client

    @pytest.fixture
    def mock_external_service(self):
        """Mock external service"""
        with patch("external_api_client.ExternalAPIClient") as mock:
            client = mock.return_value
            client.get.return_value = {"status": "ok"}
            yield client

# Example test cases
@pytest.mark.asyncio
class TestUserAPI(AsyncAPITestCase):
    """Test user API endpoints"""

    async def test_create_user(self, async_client: httpx.AsyncClient):
        """Test user creation"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword123"
        }

        response = await async_client.post(
            "/api/users",
            json=user_data
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "password" not in data

    async def test_get_user(self, async_client: httpx.AsyncClient):
        """Test get user"""
        # First create a user
        create_response = await async_client.post(
            "/api/users",
            json={
                "email": "test2@example.com",
                "username": "testuser2",
                "password": "securepassword123"
            }
        )
        user_id = create_response.json()["id"]

        # Get user
        response = await async_client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id

    async def test_list_users_with_pagination(
        self,
        async_client: httpx.AsyncClient
    ):
        """Test user listing with pagination"""
        response = await async_client.get("/api/users?page=1&per_page=10")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert "links" in data
        assert data["meta"]["page"] == 1
        assert data["meta"]["per_page"] == 10

    async def test_rate_limiting(
        self,
        async_client: httpx.AsyncClient
    ):
        """Test rate limiting"""
        # Make multiple requests quickly
        responses = []
        for _ in range(150):  # Assuming rate limit is 100/minute
            response = await async_client.get("/api/users")
            responses.append(response)

        # Check if rate limiting kicked in
        rate_limited = any(
            r.status_code == 429 for r in responses
        )
        assert rate_limited

# Integration tests
@pytest.mark.asyncio
async def test_full_user_flow():
    """Test complete user workflow"""
    async with httpx.AsyncClient(
        app=app,
        base_url="http://test"
    ) as client:

        # Create user
        user_data = {
            "email": "flowtest@example.com",
            "username": "flowtest",
            "password": "securepassword123"
        }
        create_resp = await client.post("/api/users", json=user_data)
        assert create_resp.status_code == 201
        user = create_resp.json()
        user_id = user["id"]

        # Get user
        get_resp = await client.get(f"/api/users/{user_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == user_id

        # Update user
        update_data = {"username": "updateduser"}
        update_resp = await client.patch(
            f"/api/users/{user_id}",
            json=update_data
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["username"] == "updateduser"

        # Delete user
        delete_resp = await client.delete(f"/api/users/{user_id}")
        assert delete_resp.status_code == 204

        # Verify user is deleted
        get_resp = await client.get(f"/api/users/{user_id}")
        assert get_resp.status_code == 404
```

### 7. Performance Optimization Patterns

```python
# patterns/performance.py
import asyncio
import asyncio.cache
import aioredis
from typing import Any, Optional, Callable
from functools import wraps
import hashlib
import json
import pickle

class ResponseCache:
    """Response caching with Redis"""

    def __init__(self, redis_url: str, default_ttl: int = 300):
        self.redis = None
        self.redis_url = redis_url
        self.default_ttl = default_ttl

    async def initialize(self):
        """Initialize Redis connection"""
        self.redis = await aioredis.from_url(self.redis_url)

    def _make_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {
            "args": args,
            "kwargs": kwargs
        }
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.sha256(key_str.encode()).hexdigest()
        return f"{prefix}:{key_hash}"

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if not self.redis:
            await self.initialize()

        cached = await self.redis.get(key)
        if cached:
            return pickle.loads(cached)
        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        """Set cached value"""
        if not self.redis:
            await self.initialize()

        ttl = ttl or self.default_ttl
        serialized = pickle.dumps(value)
        await self.redis.setex(key, ttl, serialized)

    async def delete(self, key: str):
        """Delete cached value"""
        if self.redis:
            await self.redis.delete(key)

def cache_response(
    prefix: str,
    ttl: Optional[int] = None,
    cache: Optional[ResponseCache] = None
):
    """Decorator to cache response"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_instance = cache or ResponseCache("redis://localhost")

            # Generate cache key
            cache_key = cache_instance._make_cache_key(prefix, *args, **kwargs)

            # Try to get from cache
            cached_result = await cache_instance.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            await cache_instance.set(cache_key, result, ttl)

            return result

        return wrapper
    return decorator

# Usage example
@cache_response(prefix="user_data", ttl=300)
async def get_user_data(user_id: int) -> Dict[str, Any]:
    """Get user data with caching"""
    # Expensive database operation or API call
    await asyncio.sleep(1)  # Simulate slow operation
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

# Batch processing for performance
class BatchProcessor:
    """Batch processor for optimizing multiple operations"""

    def __init__(self, batch_size: int = 100, flush_interval: int = 5):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.queue = asyncio.Queue()
        self.processing = False

    async def add(self, item: Any):
        """Add item to batch queue"""
        await self.queue.put(item)
        if not self.processing:
            self.processing = True
            asyncio.create_task(self._process_batch())

    async def _process_batch(self):
        """Process items in batches"""
        while True:
            batch = []

            # Collect batch items
            try:
                deadline = asyncio.get_event_loop().time() + self.flush_interval

                while len(batch) < self.batch_size:
                    try:
                        timeout = max(0, deadline - asyncio.get_event_loop().time())
                        item = await asyncio.wait_for(
                            self.queue.get(),
                            timeout=timeout
                        )
                        batch.append(item)
                    except asyncio.TimeoutError:
                        break

                if batch:
                    await self._process_batch_items(batch)

            except Exception as e:
                print(f"Error processing batch: {e}")
                continue

    async def _process_batch_items(self, batch: list[Any]):
        """Process a batch of items"""
        # Override in subclasses
        # Example: batch database insert, batch API calls, etc.
        print(f"Processing batch of {len(batch)} items")
```

### 8. Production Configuration Checklist

```yaml
# api/production_checklist.yaml
performance:
  async_patterns:
    connection_pooling: true
    max_connections: 100
    connection_timeout: 30
    keep_alive: true

  caching:
    redis_cache: true
    default_ttl: 300
    cache_headers: true

  compression:
    gzip: true
    level: 6
    threshold: 1024

  rate_limiting:
    enabled: true
    default_limit: 100/minute
    burst_limit: 200
    sliding_window: true

security:
  authentication:
    jwt_validation: true
    token_refresh: true
    revoke_tokens: true

  authorization:
    rbac: true
    rate_limit_by_role: true

  validation:
    input_validation: true
    sql_injection_protection: true
    xss_protection: true

  headers:
    security_headers: true
    cors: true
    csrf_protection: true

monitoring:
  metrics:
    prometheus: true
    request_duration: true
    error_rate: true
    throughput: true

  logging:
    structured_logging: true
    correlation_ids: true
    error_tracking: true

  health_checks:
    liveness_probe: true
    readiness_probe: true
    dependency_checks: true

documentation:
  openapi:
    auto_generation: true
    examples: true
    schemas: true

  versioning:
    strategy: "header_path_query"
    deprecation_warnings: true
    backward_compatibility: true

  testing:
    unit_tests: true
    integration_tests: true
    performance_tests: true
    contract_tests: true
```

This comprehensive API development skill provides modern patterns for building high-performance APIs in 2025, including async/await patterns, circuit breakers, rate limiting, versioning strategies, comprehensive testing, and production optimization techniques that work across different frameworks.