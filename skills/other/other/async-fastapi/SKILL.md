---
name: async-fastapi
description: >
  Build async FastAPI applications with async/await endpoints, background tasks,
  middleware, lifespan events, WebSockets, and streaming responses. Use when the user
  builds a FastAPI app, asks about async patterns, implements real-time features,
  or needs non-blocking I/O. Trigger when you see synchronous code in FastAPI that
  should be async.
---

# Async FastAPI

Build high-performance async APIs with FastAPI. Async endpoints handle concurrent
requests efficiently without blocking the event loop, which is critical for I/O-bound
workloads like database queries, HTTP calls, and file operations.

## When to Use
- User creates or modifies FastAPI endpoints
- User needs concurrent I/O operations
- User implements WebSockets or streaming
- User asks about background processing
- User encounters event loop blocking or performance issues

## Core Patterns

### Async Endpoints

Use `async def` for I/O-bound endpoints. Use plain `def` for CPU-bound work (FastAPI
runs sync handlers in a threadpool automatically).

```python
from fastapi import FastAPI
import httpx

app = FastAPI()

# Async -- for I/O-bound operations (DB, HTTP, file)
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

# Sync -- for CPU-bound operations (FastAPI runs in threadpool)
@app.get("/compute/{n}")
def compute_heavy(n: int):
    return {"result": sum(i * i for i in range(n))}

# Concurrent async operations
import asyncio

@app.get("/dashboard/{user_id}")
async def get_dashboard(user_id: int):
    user_task = get_user_from_db(user_id)
    orders_task = get_orders_from_db(user_id)
    notifications_task = get_notifications(user_id)

    user, orders, notifications = await asyncio.gather(
        user_task, orders_task, notifications_task
    )

    return {"user": user, "orders": orders, "notifications": notifications}
```

### Lifespan Events

Use the lifespan context manager to handle startup and shutdown. This replaces the
deprecated `on_event` decorators.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize shared resources
    app.state.http_client = httpx.AsyncClient(timeout=30.0)
    app.state.db_pool = await create_db_pool()
    yield
    # Shutdown: clean up resources
    await app.state.http_client.aclose()
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/fetch")
async def fetch_data(url: str):
    response = await app.state.http_client.get(url)
    return response.json()
```

### Background Tasks

Use `BackgroundTasks` for fire-and-forget operations that should not block the response.

```python
from fastapi import BackgroundTasks

async def send_welcome_email(email: str, name: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://email-service.example.com/send",
            json={"to": email, "template": "welcome", "name": name},
        )

async def log_signup(user_id: int) -> None:
    async with get_db_session() as session:
        await session.execute(
            insert(AuditLog).values(action="signup", user_id=user_id)
        )

@app.post("/signup")
async def signup(user: UserCreate, background_tasks: BackgroundTasks):
    new_user = await create_user(user)
    background_tasks.add_task(send_welcome_email, new_user.email, new_user.name)
    background_tasks.add_task(log_signup, new_user.id)
    return {"id": new_user.id, "status": "created"}
```

### Middleware

```python
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{duration:.4f}"
        return response

app.add_middleware(TimingMiddleware)

# Pure ASGI middleware (more performant, no BaseHTTPMiddleware overhead)
from starlette.types import ASGIApp, Receive, Scope, Send

class CORSHeaderMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            async def send_with_cors(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    headers[b"access-control-allow-origin"] = b"*"
                    message["headers"] = list(headers.items())
                await send(message)
            await self.app(scope, receive, send_with_cors)
        else:
            await self.app(scope, receive, send)
```

### WebSockets

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Room {room_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Streaming Responses

```python
from fastapi.responses import StreamingResponse

async def generate_report_rows(query_params: dict):
    """Stream large dataset row by row."""
    async with get_db_session() as session:
        result = await session.stream(build_query(query_params))
        async for row in result:
            yield f"{row.id},{row.name},{row.value}\n"

@app.get("/export/csv")
async def export_csv():
    return StreamingResponse(
        generate_report_rows({"status": "active"}),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=report.csv"},
    )

# Server-sent events
async def event_stream():
    while True:
        data = await get_latest_event()
        yield f"data: {data}\n\n"
        await asyncio.sleep(1)

@app.get("/events")
async def sse():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

## Anti-Patterns

- **Blocking the event loop**: Never call synchronous I/O (e.g., `requests.get`,
  `time.sleep`, blocking DB drivers) inside `async def`. Use async libraries or
  `asyncio.to_thread()` for unavoidable sync code.
- **Creating new event loops**: Never call `asyncio.run()` or `loop.run_until_complete()`
  inside an async handler. The event loop is already running.
- **Using `on_event` decorators**: These are deprecated. Use the `lifespan` context
  manager instead.
- **Shared mutable state without locks**: If multiple async tasks access shared state,
  use `asyncio.Lock()` to prevent race conditions.
- **Not closing async clients**: Always use `async with` or clean up in lifespan
  shutdown. Leaked connections cause resource exhaustion.

## Quick Reference

| Pattern | Use Case |
|---|---|
| `async def endpoint()` | I/O-bound request handlers |
| `def endpoint()` | CPU-bound (auto-threadpooled) |
| `asyncio.gather()` | Concurrent async operations |
| `BackgroundTasks` | Fire-and-forget after response |
| `lifespan` context manager | App startup/shutdown |
| `StreamingResponse` | Large files, SSE, CSV export |
| `WebSocket` | Real-time bidirectional comms |
| `asyncio.to_thread()` | Run sync code without blocking |
