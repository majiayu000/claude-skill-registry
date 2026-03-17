---
name: api-endpoint-implementation
description: Defines patterns for implementing FastAPI REST endpoints, including route definition, request/response models, error handling, and integration tests. Use when implementing any API endpoint to ensure consistency and best practices across endpoints.
license: MIT
metadata:
  version: "1.0.0"
  framework: "FastAPI"
  conventions: "Pydantic models, TestClient, error codes, HTTP status mapping"
---

# API Endpoint Implementation Pattern

This skill defines how to implement FastAPI REST endpoints following established patterns.

## Endpoint Structure

### Basic Endpoint

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from datetime import UTC, datetime

@app.get("/api/items")
async def list_items() -> JSONResponse:
    """List all items.

    Returns:
        JSONResponse with status 200 and list of items
    """
    # Implementation
    items = get_items()  # Your business logic
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "items": items,
            "count": len(items),
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z")
        }
    )
```

### Endpoint with Request Body

```python
from pydantic import BaseModel

class CreateItemRequest(BaseModel):
    """Request model for creating an item."""
    name: str
    description: str | None = None
    price: float = Field(ge=0, description="Price must be non-negative")

class ItemResponse(BaseModel):
    """Response model for item operations."""
    id: str
    name: str
    description: str | None
    price: float
    created_at: datetime

@app.post("/api/items")
async def create_item(request: CreateItemRequest) -> JSONResponse:
    """Create a new item.

    Args:
        request: Item creation request

    Returns:
        JSONResponse with created item data
    """
    # Validate and process
    item = create_item_logic(request)  # Your business logic
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=ItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            created_at=item.created_at
        ).model_dump()
    )
```

## Request/Response Models

### Request Models

Define Pydantic models for request validation:

```python
from pydantic import BaseModel, Field, field_validator

class CreateItemRequest(BaseModel):
    """Request model for creating an item."""

    name: str = Field(min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Optional description")
    price: float = Field(ge=0, description="Price must be non-negative")
    tags: list[str] = Field(default_factory=list, description="Item tags")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate item name."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
```

### Response Models

```python
class ItemResponse(BaseModel):
    """Response model for item operations."""

    id: str
    name: str
    description: str | None
    price: float
    tags: list[str]
    created_at: datetime
    updated_at: datetime

class ErrorResponse(BaseModel):
    """Standard error response model."""

    status: str = "failure"
    error_code: str
    message: str
    timestamp: datetime
    details: dict | None = None
```

## Error Handling

### Standard Error Response

Define error codes in your project (e.g., `errors.py` or constants):

```python
# Define error codes (e.g., in errors.py)
E_INVALID_REQUEST = "E_INVALID_REQUEST"
E_RESOURCE_NOT_FOUND = "E_RESOURCE_NOT_FOUND"
E_RESOURCE_CONFLICT = "E_RESOURCE_CONFLICT"
E_SERVICE_NOT_READY = "E_SERVICE_NOT_READY"
E_INTERNAL_ERROR = "E_INTERNAL_ERROR"

@app.post("/api/items")
async def create_item(request: CreateItemRequest) -> JSONResponse:
    """Create item endpoint."""
    try:
        # Validate business rules
        if item_exists(request.name):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "status": "failure",
                    "error_code": "E_RESOURCE_CONFLICT",
                    "message": f"Item with name '{request.name}' already exists",
                    "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                    "details": {"field": "name", "value": request.name}
                }
            )

        # Create item
        item = create_item_logic(request)
        return JSONResponse(status_code=201, content=item.model_dump())
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "status": "failure",
                "error_code": "E_INVALID_REQUEST",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "details": None
            }
        )
```

### Error Code to HTTP Status Mapping

Map error codes to appropriate HTTP status codes:

| Error Code | HTTP Status | Use Case |
|------------|-------------|----------|
| `E_INVALID_REQUEST` | 400 Bad Request | Invalid input data, validation failures |
| `E_RESOURCE_NOT_FOUND` | 404 Not Found | Resource doesn't exist |
| `E_RESOURCE_CONFLICT` | 409 Conflict | Resource already exists, state conflict |
| `E_UNAUTHORIZED` | 401 Unauthorized | Authentication required |
| `E_FORBIDDEN` | 403 Forbidden | Insufficient permissions |
| `E_SERVICE_NOT_READY` | 503 Service Unavailable | Service dependencies not ready |
| `E_SERVICE_TIMEOUT` | 504 Gateway Timeout | External service timeout |
| `E_INTERNAL_ERROR` | 500 Internal Server Error | Unexpected server error |

## Integration Tests

### Test Structure

```python
"""Tests for GET /api/items endpoint.

Tests verify:
- Endpoint returns 200 with correct data
- Error handling works correctly
- Response format matches schema
- Request validation works
"""

import pytest
from fastapi.testclient import TestClient

from your_app import app  # Import your FastAPI app

@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)

class TestItemsEndpoint:
    """Test GET /api/items endpoint."""

    def test_get_items_returns_200(self, client: TestClient) -> None:
        """Test GET /api/items returns 200 with list of items."""
        response = client.get("/api/items")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "count" in data
        assert isinstance(data["items"], list)

    def test_create_item_returns_201(self, client: TestClient) -> None:
        """Test POST /api/items creates item successfully."""
        response = client.post(
            "/api/items",
            json={"name": "Test Item", "price": 10.99}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["price"] == 10.99
        assert "id" in data

    def test_create_item_validates_request(self, client: TestClient) -> None:
        """Test POST /api/items validates request data."""
        response = client.post(
            "/api/items",
            json={"name": "", "price": -5}  # Invalid data
        )

        assert response.status_code == 422  # Pydantic validation error
        data = response.json()
        assert "detail" in data

    def test_endpoint_handles_errors(self, client: TestClient) -> None:
        """Test endpoint handles business logic errors correctly."""
        # Simulate conflict scenario
        response = client.post(
            "/api/items",
            json={"name": "Existing Item", "price": 10.99}
        )

        assert response.status_code == 409
        data = response.json()
        assert data["status"] == "failure"
        assert data["error_code"] == "E_RESOURCE_CONFLICT"
```

## Health and Ready Endpoints

### Health Endpoint Pattern

```python
# Track server state
_server_start_time: float | None = None
_server_shutting_down: bool = False

@app.get("/health")
async def health() -> JSONResponse:
    """Health check endpoint (liveness probe)."""
    if _server_shutting_down:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", ...}
        )

    uptime_seconds = round(time.time() - _server_start_time, 2)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "healthy",
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "uptime_seconds": uptime_seconds,
            "version": "0.1.0"
        }
    )
```

### Ready Endpoint Pattern

```python
@app.get("/ready")
async def ready() -> JSONResponse:
    """Readiness probe - checks dependencies and service state."""
    checks = {
        "database": check_database_connection(),
        "cache": check_cache_connection(),
        "external_api": check_external_service(),
        # Add other critical dependencies
    }

    if all(v == "ok" for v in checks.values()):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "ready",
                "checks": checks,
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z")
            }
        )
    else:
        failed_checks = {k: v for k, v in checks.items() if v != "ok"}
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "checks": checks,
                "failed_checks": list(failed_checks.keys()),
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z")
            }
        )

def check_database_connection() -> str:
    """Check if database is accessible."""
    try:
        # Your database health check logic
        return "ok"
    except Exception:
        return "error"

def check_cache_connection() -> str:
    """Check if cache is accessible."""
    try:
        # Your cache health check logic
        return "ok"
    except Exception:
        return "error"

def check_external_service() -> str:
    """Check if external service is reachable."""
    try:
        # Your external service check logic
        return "ok"
    except Exception:
        return "error"
```

## Resource Management Endpoints

### CRUD Pattern Example

```python
import uuid
from fastapi import Path, Query

# GET - List resources
@app.get("/api/items")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
) -> JSONResponse:
    """List items with pagination."""
    items = get_items(skip=skip, limit=limit)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "items": [item.model_dump() for item in items],
            "count": len(items),
            "skip": skip,
            "limit": limit
        }
    )

# GET - Get single resource
@app.get("/api/items/{item_id}")
async def get_item(item_id: str = Path(...)) -> JSONResponse:
    """Get item by ID."""
    item = get_item_by_id(item_id)
    if not item:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "failure",
                "error_code": "E_RESOURCE_NOT_FOUND",
                "message": f"Item with ID '{item_id}' not found",
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z")
            }
        )
    return JSONResponse(status_code=200, content=item.model_dump())

# POST - Create resource
@app.post("/api/items")
async def create_item(request: CreateItemRequest) -> JSONResponse:
    """Create new item."""
    item = create_item_logic(request)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=item.model_dump()
    )

# PUT - Update resource
@app.put("/api/items/{item_id}")
async def update_item(
    item_id: str = Path(...),
    request: UpdateItemRequest
) -> JSONResponse:
    """Update existing item."""
    item = update_item_logic(item_id, request)
    if not item:
        return JSONResponse(status_code=404, content={"error": "Not found"})
    return JSONResponse(status_code=200, content=item.model_dump())

# DELETE - Delete resource
@app.delete("/api/items/{item_id}")
async def delete_item(item_id: str = Path(...)) -> JSONResponse:
    """Delete item."""
    success = delete_item_logic(item_id)
    if not success:
        return JSONResponse(status_code=404, content={"error": "Not found"})
    return JSONResponse(status_code=204)  # No Content
```

## Testing Requirements

### Minimum Test Coverage

Each endpoint should have tests for:

1. **Success case**: Returns 200 with correct data
2. **Error case**: Returns appropriate error status
3. **Request validation**: Invalid requests are rejected
4. **Response format**: Matches defined schema
5. **Edge cases**: Boundary conditions and error scenarios

### Test File Organization

Organize tests by feature or endpoint:

- Foundation tests: `tests/integration/api/test_foundation.py`
- Feature-specific tests: `tests/integration/api/test_items.py`
- Model validation tests: `tests/integration/api/test_models.py`
- Error handling tests: `tests/integration/api/test_errors.py`

Or organize by endpoint:

- `tests/integration/api/test_health.py`
- `tests/integration/api/test_ready.py`
- `tests/integration/api/test_items.py`

## Best Practices

1. **Use type hints**: All functions should have type annotations
2. **Document endpoints**: Include docstrings describing behavior
3. **Validate inputs**: Use Pydantic models for validation
4. **Handle errors**: Return appropriate error codes and status codes
5. **Test thoroughly**: Write tests for success and error cases
6. **Follow conventions**: Use established patterns from existing endpoints
7. **Return consistent format**: Use standard response models

## Common Patterns

### Stateful Endpoints

For endpoints that need to track state or sessions:

```python
# Use in-memory storage, database, or cache
_active_sessions: dict[str, SessionData] = {}

@app.post("/api/sessions/{session_id}/action")
async def perform_action(
    session_id: str = Path(...),
    request: ActionRequest
) -> JSONResponse:
    """Perform action on session."""
    if session_id not in _active_sessions:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "status": "failure",
                "error_code": "E_RESOURCE_NOT_FOUND",
                "message": f"Session '{session_id}' not found"
            }
        )

    session = _active_sessions[session_id]
    result = process_action(session, request)
    return JSONResponse(status_code=200, content=result)
```

### Async Operations

For endpoints that trigger async or long-running operations:

```python
import asyncio
from typing import Awaitable

@app.post("/api/items/{item_id}/process")
async def process_item(item_id: str = Path(...)) -> JSONResponse:
    """Trigger async processing for item."""
    # Validate item exists
    item = get_item_by_id(item_id)
    if not item:
        return JSONResponse(status_code=404, content={"error": "Not found"})

    # Trigger async processing
    task_id = str(uuid.uuid4())
    asyncio.create_task(process_item_async(item_id, task_id))

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "task_id": task_id,
            "status": "processing",
            "message": "Item processing started"
        }
    )

async def process_item_async(item_id: str, task_id: str) -> None:
    """Background task to process item."""
    # Long-running or async operation
    pass
```

### Dependency Injection

For endpoints that need shared dependencies:

```python
from fastapi import Depends

def get_database():
    """Dependency to get database connection."""
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/items")
async def list_items(db = Depends(get_database)) -> JSONResponse:
    """List items using database dependency."""
    items = db.query_items()
    return JSONResponse(status_code=200, content={"items": items})
```
