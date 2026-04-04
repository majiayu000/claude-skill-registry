---
name: api-development
description: Use when creating new API endpoints, working with async operations, implementing long-running tasks with progress tracking, adding Pydantic models, or designing request/response schemas.
---

# API Development

Load this skill when:
- Creating new API endpoints
- Working with async operations
- Implementing long-running tasks with progress tracking
- Adding Pydantic models or request/response schemas

---

## API Structure

```
ktrdr/api/
├── endpoints/      # Route handlers
├── models/         # Pydantic request/response models
├── services/       # Business logic
└── main.py         # Router registration
```

## Adding New Endpoints

1. **Create endpoint** in `ktrdr/api/endpoints/`
2. **Define Pydantic models** in `ktrdr/api/models/`
3. **Implement business logic** in `ktrdr/api/services/`
4. **Register router** in `ktrdr/api/main.py`
5. **Add tests** in `tests/api/`

---

## Async Operation Pattern

For long-running tasks (training, backtesting, data downloads), KTRDR uses **ServiceOrchestrator** pattern (not FastAPI's BackgroundTasks):

```python
from ktrdr.api.services.operations_service import OperationsService
from ktrdr.api.models.operations import OperationMetadata, OperationType

@router.post("/long-operation")
async def start_operation(
    request: OperationRequest,
    operations_service: OperationsService = Depends(get_operations_service)
):
    # Create operation metadata
    metadata = OperationMetadata(
        symbol=request.symbol,
        timeframe=request.timeframe,
        parameters={"strategy": request.strategy_name}
    )

    # Create operation (returns OperationInfo, not just operation_id)
    operation_info = await operations_service.create_operation(
        operation_type=OperationType.TRAINING,
        metadata=metadata
    )

    # Dispatch to worker via ServiceOrchestrator
    # Workers handle execution; backend just orchestrates
    await service_orchestrator.dispatch_to_worker(operation_info.operation_id, request)

    return {"operation_id": operation_info.operation_id}
```

### Key Components

- **OperationsService**: Tracks all operations, progress, and status
- **ServiceOrchestrator**: Dispatches work to workers (never executes locally)
- **operation_id**: Returned immediately so client can poll for status

> **Note:** KTRDR does NOT use FastAPI's `BackgroundTasks`. All long-running operations are dispatched to workers.

---

## Progress Tracking

Operations report progress via `OperationProgress` object:

```python
from ktrdr.api.services.operations_service import OperationsService
from ktrdr.api.models.operations import OperationProgress

async def run_operation(operation_id: str, ops_service: OperationsService):
    try:
        # update_status takes a string, not enum
        await ops_service.update_status(operation_id, "running")

        for i, step in enumerate(steps):
            await process_step(step)

            # update_progress takes an OperationProgress object
            # Fields: percentage, current_step, steps_completed, steps_total, items_processed, items_total
            progress = OperationProgress(
                percentage=(i + 1) / len(steps) * 100,
                current_step=f"Processing step {i + 1}",
                steps_completed=i + 1,
                steps_total=len(steps)
            )
            await ops_service.update_progress(operation_id, progress)

        await ops_service.update_status(operation_id, "completed")
    except Exception as e:
        await ops_service.update_status(operation_id, "failed")
        raise
```

---

## Operation Status Endpoints

Standard endpoints for operation management:

```python
@router.get("/operations/{operation_id}")
async def get_operation_status(operation_id: str):
    """Get current status of an operation."""

@router.get("/operations/{operation_id}/metrics")
async def get_operation_metrics(operation_id: str):
    """Get detailed metrics for an operation."""

# Cancel uses DELETE on the operation resource (no /cancel suffix)
@router.delete("/operations/{operation_id}")
async def cancel_operation(operation_id: str):
    """Request cancellation of a running operation."""
```

---

## Pydantic Models

### Request Models (Pydantic v2)

```python
from pydantic import BaseModel, Field, ConfigDict

class TrainingRequest(BaseModel):
    strategy_path: str = Field(..., description="Path to strategy YAML")
    symbol: str = Field(..., description="Trading symbol")

    # Pydantic v2 uses model_config, NOT class Config:
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "strategy_path": "config/strategies/example.yaml",
                "symbol": "AAPL"
            }
        }
    )
```

### Response Models

```python
class OperationResponse(BaseModel):
    operation_id: str
    status: OperationStatus
    progress: float = 0.0
    phase: str | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime
```

---

## Error Handling

Use HTTPException for API errors:

```python
from fastapi import HTTPException

@router.get("/resource/{id}")
async def get_resource(id: str):
    resource = await fetch_resource(id)
    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource {id} not found"
        )
    return resource
```

---

## Documentation

Once server is running:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

---

## Testing API Endpoints

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_operation(client: AsyncClient):
    response = await client.post(
        "/api/v1/operations",
        json={"type": "training", "params": {...}}
    )
    assert response.status_code == 200
    assert "operation_id" in response.json()
```

---

## Key Files

- `ktrdr/api/main.py` — App setup and router registration
- `ktrdr/api/services/operations_service.py` — Operation tracking
- `ktrdr/api/dependencies.py` — Dependency injection
