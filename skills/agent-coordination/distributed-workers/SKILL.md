---
name: distributed-workers
description: Use when working on worker implementation, ServiceOrchestrator patterns, WorkerAPIBase, operation dispatch, progress tracking, cancellation, backend-to-worker communication, or adding new worker types.
---

# Distributed Workers Architecture

Load this skill when working on:

- Worker implementation or debugging
- ServiceOrchestrator or WorkerAPIBase patterns
- Operation dispatch, progress tracking, or cancellation
- Backend-to-worker communication
- Adding new worker types

---

## Architecture Overview

KTRDR uses a distributed workers architecture where the backend orchestrates operations across worker nodes:

```
┌─────────────────────────────────────────────────────────────────┐
│ Backend (Docker Container, Port 8000)                          │
│  ├─ API Layer (FastAPI)                                        │
│  ├─ Service Orchestrators (NEVER execute operations)           │
│  ├─ WorkerRegistry (tracks all workers)                        │
│  └─ OperationsService (tracks all operations)                  │
└─────────────────────────────────────────────────────────────────┘
         │
         ├─ HTTP (Worker Registration & Operation Dispatch)
         │
    ┌────┴────┬──────────┬──────────┬─────────────┐
    │         │          │          │             │
    ▼         ▼          ▼          ▼             ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   ┌──────────────┐
│Backtest││Backtest││Training││Training│   │IB Host Service│
│Worker 1││Worker 2││Worker 1││Worker 2│   │(Port 5001)   │
│:5003   ││:5003   ││:5004   ││:5004   │   │Direct IB TCP │
└────────┘└────────┘└────────┘└────────┘   └──────────────┘
CPU-only  CPU-only  CPU-only  CPU-only    Direct IB Gateway

         ┌─────────────────────┐
         │Training Host Service│
         │(Port 5002)          │
         │GPU Access (CUDA/MPS)│
         └─────────────────────┘
         10x-100x faster training
```

## Key Principles

1. **Backend as Orchestrator Only**: Backend does not execute operations locally — it only selects workers and dispatches operations
2. **Distributed-Only Execution**: All backtesting and training operations execute on workers (no local fallback)
3. **Self-Registering Workers**: Workers push-register with backend on startup (infrastructure-agnostic)
4. **GPU-First Routing**: Training operations prefer GPU workers (10x-100x faster) with CPU worker fallback
5. **Horizontal Scalability**: Add more workers = more concurrent operations

## Worker Types

| Worker | Location | Purpose | Scalability |
|--------|----------|---------|-------------|
| Backtest Workers | Containerized, CPU | Execute backtesting | Horizontal |
| Training Workers | Containerized, CPU | Training fallback | Horizontal |
| Training Host Service | Native, GPU | GPU training (priority) | Limited by hardware |
| IB Host Service | Native | IB Gateway access | Single instance |

---

## ServiceOrchestrator Pattern

**Location**: `ktrdr/async_infrastructure/service_orchestrator.py`

All service managers inherit from ServiceOrchestrator:

```python
class DataAcquisitionService(ServiceOrchestrator):
    def __init__(self):
        # Reads USE_IB_HOST_SERVICE env var
        self.provider = self._initialize_provider()

    async def download_data(self, ...):
        # Unified async pattern with progress tracking
        return await self._execute_with_progress(...)
```

Features provided:

- Environment-based configuration
- Adapter initialization (local vs. host service routing)
- Unified async operations with progress tracking
- Cancellation token support
- Operations service integration

---

## WorkerAPIBase Pattern

**Location**: `ktrdr/workers/base.py`

All workers inherit from WorkerAPIBase and get these features for free:

1. **OperationsService singleton** — Worker-local operation tracking
2. **Operations proxy endpoints**:
   - `GET /api/v1/operations/{id}` — Get operation status
   - `GET /api/v1/operations/{id}/metrics` — Get operation metrics
   - `GET /api/v1/operations` — List operations
   - `DELETE /api/v1/operations/{id}/cancel` — Cancel operation
3. **Health endpoint** — Reports busy/idle status (`GET /health`)
4. **FastAPI app with CORS** — Ready for Docker communication
5. **Self-registration** — Automatic registration with backend on startup

### Key Pattern Elements

- **Operation ID Synchronization**: Accepts optional `task_id` from backend, returns same `operation_id`
- **Progress Tracking**: Workers register progress bridges in their OperationsService
- **Remote Queryability**: Backend can query worker's operations endpoints directly (1s cache TTL)
- **Push-Based Registration**: Workers call `POST /workers/register` on startup

### Example Implementation

```python
class BacktestWorker(WorkerAPIBase):
    def __init__(self, worker_port=5003, backend_url="http://backend:8000"):
        super().__init__(
            worker_type=WorkerType.BACKTESTING,
            operation_type=OperationType.BACKTESTING,
            worker_port=worker_port,
            backend_url=backend_url,
        )

        # Register domain-specific endpoint
        @self.app.post("/backtests/start")
        async def start_backtest(request: BacktestStartRequest):
            operation_id = request.task_id or f"worker_backtest_{uuid.uuid4().hex[:12]}"
            result = await self._execute_backtest_work(operation_id, request)
            return {"success": True, "operation_id": operation_id, **result}
```

### Worker Implementations

- **BacktestWorker** (`ktrdr/backtesting/backtest_worker.py`):
  - Adds `/backtests/start` endpoint
  - Calls BacktestingEngine directly via `asyncio.to_thread`
  - Registers BacktestProgressBridge

- **TrainingWorker** (`ktrdr/training/training_worker.py`):
  - Adds `/training/start` endpoint
  - Calls TrainingManager directly (async)
  - Simplified progress tracking

---

## Host Service Integration

### IB Host Service (uses environment variables)

```bash
USE_IB_HOST_SERVICE=true
IB_HOST_SERVICE_URL=http://localhost:5001  # default
```

Why separate: IB Gateway requires direct TCP connection (Docker networking limitation)

### Training & Backtesting (uses WorkerRegistry)

Environment flags REMOVED in Phase 5.3:

- ❌ `USE_TRAINING_HOST_SERVICE`
- ❌ `REMOTE_BACKTEST_SERVICE_URL`

Now uses WorkerRegistry:

- Workers self-register with backend on startup
- Backend selects available workers automatically
- GPU workers register with `gpu: true` capability (prioritized)
- CPU workers register as fallback

---

## Starting Workers

```bash
# Docker Compose (development)
docker-compose up -d --scale backtest-worker=5 --scale training-worker=3

# Training Host Service (GPU, runs natively)
cd training-host-service && ./start.sh

# Workers self-register at:
# - Backtest: http://localhost:5003
# - Training (CPU): http://localhost:5004
# - Training (GPU): http://localhost:5002
```

### Verification

```bash
# Check registered workers
curl http://localhost:8000/api/v1/workers | jq

# Expected: All workers show as AVAILABLE with proper capabilities
```

---

## Cancellation Tokens

**Location**: `ktrdr/async_infrastructure/cancellation.py`

All long-running operations support cancellation:

```python
from ktrdr.async_infrastructure.cancellation import create_cancellation_token

token = create_cancellation_token()

# In operation loop
if token.is_cancelled():
    raise asyncio.CancelledError()
```

- Create tokens with `create_cancellation_token()`
- Check with `token.is_cancelled()`
- Operations service manages tokens globally
- CLI displays cancellation status

---

## Async Operations Pattern (CLI)

All CLI commands use `AsyncCLIClient` for API communication:

```python
from ktrdr.cli.helpers.async_cli_client import AsyncCLIClient

async def some_command(symbol: str):
    async with AsyncCLIClient() as client:
        result = await client.post("/endpoint", json=data)
```

Progress display: Use `GenericProgressManager` with `ProgressRenderer` for live updates

---

## Documentation

- **Architecture**: [docs/architecture-overviews/distributed-workers.md](docs/architecture-overviews/distributed-workers.md)
- **Developer Guide**: [docs/developer/distributed-workers-guide.md](docs/developer/distributed-workers-guide.md)
- **Deployment**: [docs/user-guides/deployment.md](docs/user-guides/deployment.md)
