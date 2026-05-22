---
name: microservices-patterns
model: reasoning
---

# Microservices Patterns

## WHAT
Patterns for building distributed systems: service decomposition, inter-service communication, data management, and resilience. Helps you avoid the "distributed monolith" anti-pattern.

## WHEN
- Decomposing a monolith into microservices
- Designing service boundaries and contracts
- Implementing inter-service communication
- Managing distributed transactions
- Building resilient distributed systems

## KEYWORDS
microservices, service mesh, event-driven, saga, circuit breaker, API gateway, service discovery, distributed transactions, eventual consistency, CQRS


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install microservices-patterns
```


---

## Decision Framework: When to Use Microservices

| If you have... | Then... |
|----------------|---------|
| Small team (<5 devs), simple domain | Start with monolith |
| Need independent deployment/scaling | Consider microservices |
| Multiple teams, clear domain boundaries | Microservices work well |
| Tight deadlines, unknown requirements | Monolith first, extract later |

**Rule of thumb**: If you can't define clear service boundaries, you're not ready for microservices.

---

## Service Decomposition Patterns

### Pattern 1: By Business Capability

Organize services around business functions, not technical layers.

```
E-commerce Example:
├── order-service       # Order lifecycle
├── payment-service     # Payment processing
├── inventory-service   # Stock management
├── shipping-service    # Fulfillment
└── notification-service # Emails, SMS
```

### Pattern 2: Strangler Fig (Monolith Migration)

Gradually extract from monolith without big-bang rewrites.

```
1. Identify bounded context to extract
2. Create new microservice
3. Route new traffic to microservice
4. Gradually migrate existing functionality
5. Remove from monolith when complete
```

```python
# API Gateway routing during migration
async def route_orders(request):
    if request.path.startswith("/api/orders/v2"):
        return await new_order_service.forward(request)
    else:
        return await legacy_monolith.forward(request)
```

---

## Communication Patterns

### Pattern 1: Synchronous (REST/gRPC)

Use for: Queries, when you need immediate response.

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=5.0)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
    async def get(self, path: str):
        """GET with automatic retries."""
        response = await self.client.get(f"{self.base_url}{path}")
        response.raise_for_status()
        return response.json()

# Usage
payment_client = ServiceClient("http://payment-service:8001")
result = await payment_client.get(f"/payments/{payment_id}")
```

### Pattern 2: Asynchronous (Events)

Use for: Commands, when eventual consistency is acceptable.

```python
from aiokafka import AIOKafkaProducer
import json

@dataclass
class DomainEvent:
    event_id: str
    event_type: str
    aggregate_id: str
    occurred_at: datetime
    data: dict

class EventBus:
    def __init__(self, bootstrap_servers: List[str]):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode()
        )
    
    async def publish(self, event: DomainEvent):
        await self.producer.send_and_wait(
            event.event_type,  # Topic = event type
            value=asdict(event),
            key=event.aggregate_id.encode()
        )

# Order service publishes
await event_bus.publish(DomainEvent(
    event_id=str(uuid.uuid4()),
    event_type="OrderCreated",
    aggregate_id=order.id,
    occurred_at=datetime.now(),
    data={"order_id": order.id, "customer_id": order.customer_id}
))

# Inventory service subscribes and reacts
async def handle_order_created(event_data: dict):
    order_id = event_data["data"]["order_id"]
    items = event_data["data"]["items"]
    await reserve_inventory(order_id, items)
```

### When to Use Each

| Synchronous | Asynchronous |
|-------------|--------------|
| Need immediate response | Fire-and-forget |
| Simple query/response | Long-running operations |
| Low latency required | Decoupling is priority |
| Tight coupling acceptable | Eventual consistency OK |

---

## Data Patterns

### Database Per Service

Each service owns its data. **No shared databases.**

```
order-service     → orders_db (PostgreSQL)
payment-service   → payments_db (PostgreSQL)
product-service   → products_db (MongoDB)
analytics-service → analytics_db (ClickHouse)
```

### Saga Pattern (Distributed Transactions)

For operations spanning multiple services that need rollback capability.

```python
class SagaStep:
    def __init__(self, name: str, action: Callable, compensation: Callable):
        self.name = name
        self.action = action
        self.compensation = compensation

class OrderFulfillmentSaga:
    def __init__(self):
        self.steps = [
            SagaStep("create_order", self.create_order, self.cancel_order),
            SagaStep("reserve_inventory", self.reserve_inventory, self.release_inventory),
            SagaStep("process_payment", self.process_payment, self.refund_payment),
            SagaStep("confirm_order", self.confirm_order, self.cancel_confirmation),
        ]
    
    async def execute(self, order_data: dict) -> SagaResult:
        completed_steps = []
        context = {"order_data": order_data}
        
        for step in self.steps:
            try:
                result = await step.action(context)
                if not result.success:
                    await self.compensate(completed_steps, context)
                    return SagaResult(status="failed", error=result.error)
                completed_steps.append(step)
                context.update(result.data)
            except Exception as e:
                await self.compensate(completed_steps, context)
                return SagaResult(status="failed", error=str(e))
        
        return SagaResult(status="completed", data=context)
    
    async def compensate(self, completed_steps: List[SagaStep], context: dict):
        """Execute compensating actions in reverse order."""
        for step in reversed(completed_steps):
            try:
                await step.compensation(context)
            except Exception as e:
                # Log but continue compensating
                logger.error(f"Compensation failed for {step.name}: {e}")
```

---

## Resilience Patterns

### Circuit Breaker

Fail fast when a service is down. Prevents cascade failures.

```python
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing recovery

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None
    
    async def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpen("Service unavailable")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def _on_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()
    
    def _should_attempt_reset(self) -> bool:
        return datetime.now() - self.opened_at > timedelta(seconds=self.recovery_timeout)

# Usage
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)

async def call_payment_service(data: dict):
    return await breaker.call(payment_client.post, "/payments", json=data)
```

### Retry with Exponential Backoff

For transient failures.

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError))
)
async def fetch_user(user_id: str):
    response = await client.get(f"/users/{user_id}")
    response.raise_for_status()
    return response.json()
```

### Bulkhead

Isolate resources to limit impact of failures.

```python
import asyncio

class Bulkhead:
    def __init__(self, max_concurrent: int):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def call(self, func: Callable, *args, **kwargs):
        async with self.semaphore:
            return await func(*args, **kwargs)

# Limit concurrent calls to each service
payment_bulkhead = Bulkhead(max_concurrent=10)
inventory_bulkhead = Bulkhead(max_concurrent=20)

result = await payment_bulkhead.call(payment_service.charge, amount)
```

---

## API Gateway Pattern

Single entry point for all clients.

```python
from fastapi import FastAPI, Depends, HTTPException
from circuitbreaker import circuit

app = FastAPI()

class APIGateway:
    def __init__(self):
        self.clients = {
            "orders": httpx.AsyncClient(base_url="http://order-service:8000"),
            "payments": httpx.AsyncClient(base_url="http://payment-service:8001"),
            "inventory": httpx.AsyncClient(base_url="http://inventory-service:8002"),
        }
    
    @circuit(failure_threshold=5, recovery_timeout=30)
    async def forward(self, service: str, path: str, **kwargs):
        client = self.clients[service]
        response = await client.request(**kwargs, url=path)
        response.raise_for_status()
        return response.json()
    
    async def aggregate(self, order_id: str) -> dict:
        """Aggregate data from multiple services."""
        results = await asyncio.gather(
            self.forward("orders", f"/orders/{order_id}", method="GET"),
            self.forward("payments", f"/payments/order/{order_id}", method="GET"),
            self.forward("inventory", f"/reservations/order/{order_id}", method="GET"),
            return_exceptions=True
        )
        
        return {
            "order": results[0] if not isinstance(results[0], Exception) else None,
            "payment": results[1] if not isinstance(results[1], Exception) else None,
            "inventory": results[2] if not isinstance(results[2], Exception) else None,
        }

gateway = APIGateway()

@app.get("/api/orders/{order_id}")
async def get_order_aggregate(order_id: str):
    return await gateway.aggregate(order_id)
```

---

## Health Checks

Every service needs liveness and readiness probes.

```python
@app.get("/health/live")
async def liveness():
    """Is the process running?"""
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    """Can we serve traffic?"""
    checks = {
        "database": await check_database(),
        "cache": await check_redis(),
    }
    
    all_healthy = all(checks.values())
    status = "ready" if all_healthy else "not_ready"
    
    return {"status": status, "checks": checks}
```

---

## NEVER

- **Shared Databases**: Creates tight coupling, defeats the purpose
- **Synchronous Chains**: A → B → C → D = fragile, slow
- **No Circuit Breakers**: One service down takes everything down
- **Distributed Monolith**: Services that must deploy together
- **Ignoring Network Failures**: Assume the network WILL fail
- **No Compensation Logic**: Can't undo failed distributed transactions
- **Starting with Microservices**: Always start with a well-structured monolith
- **Chatty Services**: Too many inter-service calls = latency death
