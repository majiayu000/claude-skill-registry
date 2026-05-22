---
name: microservices
description: Microservices architecture patterns. Use when designing service decomposition, inter-service communication, API gateways, service discovery, event-driven architecture, or distributed systems.
---

# Microservices Architecture Patterns

## Service Structure
```
services/
  api-gateway/          # Entry point, routing, auth
  user-service/         # User management, auth
  product-service/      # Products, catalog, inventory
  order-service/        # Orders, checkout flow
  notification-service/ # Email, push, SMS (event-driven)
  payment-service/      # Stripe, billing
shared/
  proto/                # gRPC definitions (if used)
  events/               # Event schemas (Pydantic/TypeScript)
  libs/                 # Shared utilities
docker-compose.yml
```

## API Gateway (FastAPI)
```python
# api-gateway/main.py
import httpx
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

SERVICE_URLS = {
    "users": "http://user-service:8001",
    "products": "http://product-service:8002",
    "orders": "http://order-service:8003",
}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request, user=Depends(verify_token)):
    if service not in SERVICE_URLS:
        raise HTTPException(404, "Service not found")

    url = f"{SERVICE_URLS[service]}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers={"X-User-Id": str(user.id), "X-User-Role": user.role},
            content=await request.body(),
            params=dict(request.query_params),
            timeout=30,
        )
    return Response(content=response.content, status_code=response.status_code,
                   media_type=response.headers.get("content-type"))
```

## Inter-Service Communication

### Synchronous (HTTP)
```python
# Shared HTTP client with circuit breaker
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ServiceClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url, timeout=10)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get(self, path: str, **kwargs):
        response = await self.client.get(path, **kwargs)
        response.raise_for_status()
        return response.json()

# order-service calling user-service
user_client = ServiceClient("http://user-service:8001")

async def get_order_with_user(order_id: str):
    order = await db.orders.find_one(order_id)
    user = await user_client.get(f"/users/{order['user_id']}")  # Retries on failure
    return {**order, "user": user}
```

### Asynchronous (Events via Redis/RabbitMQ)
```python
# events/schemas.py
from pydantic import BaseModel
from datetime import datetime

class OrderPlacedEvent(BaseModel):
    event_type: str = "order.placed"
    order_id: str
    user_id: str
    amount: float
    items: list[dict]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserRegisteredEvent(BaseModel):
    event_type: str = "user.registered"
    user_id: str
    email: str
    name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Publisher
import aioredis, json

redis = aioredis.from_url(settings.REDIS_URL)

async def publish_event(event: BaseModel):
    channel = event.event_type.replace(".", ":")
    await redis.publish(channel, event.model_dump_json())

# In order-service after creating order:
await publish_event(OrderPlacedEvent(
    order_id=order.id,
    user_id=user_id,
    amount=total,
    items=items,
))

# Subscriber (notification-service)
async def start_consumers():
    pubsub = redis.pubsub()
    await pubsub.subscribe("order:placed", "user:registered")

    async for message in pubsub.listen():
        if message["type"] == "message":
            channel = message["channel"]
            data = json.loads(message["data"])

            if channel == "order:placed":
                event = OrderPlacedEvent(**data)
                await send_order_confirmation_email(event)

            elif channel == "user:registered":
                event = UserRegisteredEvent(**data)
                await send_welcome_email(event)
```

## Service Template (Individual Service)
```python
# user-service/main.py
from fastapi import FastAPI, Header, HTTPException
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await create_db_pool()
    yield
    await app.state.db.close()

app = FastAPI(lifespan=lifespan)

# Services trust X-User-Id header from gateway (already authenticated)
def get_current_user_id(x_user_id: str = Header(...)):
    return x_user_id

@app.get("/users/me")
async def get_me(user_id: str = Depends(get_current_user_id)):
    return await db.get_user(user_id)

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Internal endpoint — called by other services."""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

## Docker Compose (Development)
```yaml
# docker-compose.yml
version: '3.9'

services:
  api-gateway:
    build: ./api-gateway
    ports: ["8000:8000"]
    environment:
      - USER_SERVICE_URL=http://user-service:8001
    depends_on: [user-service, product-service]

  user-service:
    build: ./user-service
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/users
      - REDIS_URL=redis://redis:6379
    depends_on: [postgres, redis]

  product-service:
    build: ./product-service
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/products
    depends_on: [postgres]

  notification-service:
    build: ./notification-service
    environment:
      - REDIS_URL=redis://redis:6379
      - RESEND_API_KEY=${RESEND_API_KEY}
    depends_on: [redis]

  postgres:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    volumes: [redis_data:/data]

volumes:
  postgres_data:
  redis_data:
```

## Health Checks
```python
@app.get("/health")
async def health():
    """Standard health check endpoint for load balancers."""
    checks = {}
    try:
        await db.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"

    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"

    status = "ok" if all(v == "ok" for v in checks.values()) else "degraded"
    return {"status": status, "service": "user-service", "checks": checks}
```

## Rules
- Each service owns its database — NEVER share databases between services
- API Gateway handles auth — services trust X-User-Id header (don't re-verify JWT)
- Use events (pub/sub) for cross-service side effects (emails, notifications, analytics)
- Use HTTP for synchronous reads where you need a response immediately
- Each service has its own docker image + migrations — deployable independently
- Retry with exponential backoff for inter-service HTTP calls
- Circuit breaker: after 5 failures, stop calling the service for 30s
- Idempotent event handlers: consuming same event twice should be safe
- One database schema per service (prefix tables: `users_*`, `products_*`)
- Service discovery: use Docker DNS (service name = hostname) in compose
