---
name: microservices-patterns
description: Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distributed systems, decomposing monoliths, or implementing microservices.
license: MIT
---

# Microservices Patterns

Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems.

## When to Use This Skill

- Decomposing monoliths into microservices
- Designing service boundaries and contracts
- Implementing inter-service communication
- Managing distributed data and transactions
- Building resilient distributed systems
- Implementing service discovery and load balancing
- Designing event-driven architectures

## Core Concepts

### 1. Service Decomposition Strategies

**By Business Capability**
- Organize services around business functions
- Each service owns its domain
- Example: OrderService, PaymentService, InventoryService

**By Subdomain (DDD)**
- Core domain, supporting subdomains
- Bounded contexts map to services
- Clear ownership and responsibility

**Strangler Fig Pattern**
- Gradually extract from monolith
- New functionality as microservices
- Proxy routes to old/new systems

### 2. Communication Patterns

**Synchronous (Request/Response)**
- REST APIs
- gRPC
- GraphQL

**Asynchronous (Events/Messages)**
- Event streaming (Kafka)
- Message queues (RabbitMQ, SQS)
- Pub/Sub patterns

### 3. Data Management

**Database Per Service**
- Each service owns its data
- No shared databases
- Loose coupling

**Saga Pattern**
- Distributed transactions
- Compensating actions
- Eventual consistency

### 4. Resilience Patterns

**Circuit Breaker**
- Fail fast on repeated errors
- Prevent cascade failures

**Retry with Backoff**
- Transient fault handling
- Exponential backoff

**Bulkhead**
- Isolate resources
- Limit impact of failures

## Service Decomposition Patterns

### Pattern 1: By Business Capability

```python
# Order Service
class OrderService:
    async def create_order(self, order_data: dict) -> Order:
        order = Order.create(order_data)
        await self.event_bus.publish(
            OrderCreatedEvent(order_id=order.id, customer_id=order.customer_id)
        )
        return order

# Payment Service (separate service)
class PaymentService:
    async def process_payment(self, payment_request: PaymentRequest) -> PaymentResult:
        result = await self.payment_gateway.charge(
            amount=payment_request.amount,
            customer=payment_request.customer_id
        )
        if result.success:
            await self.event_bus.publish(
                PaymentCompletedEvent(order_id=payment_request.order_id)
            )
        return result

# Inventory Service (separate service)
class InventoryService:
    async def reserve_items(self, order_id: str, items: List[OrderItem]) -> ReservationResult:
        for item in items:
            available = await self.inventory_repo.get_available(item.product_id)
            if available < item.quantity:
                return ReservationResult(success=False, error=f"Insufficient inventory")

        reservation = await self.create_reservation(order_id, items)
        await self.event_bus.publish(InventoryReservedEvent(order_id=order_id))
        return ReservationResult(success=True, reservation=reservation)
```

### Pattern 2: API Gateway

```python
from fastapi import FastAPI
import httpx

class APIGateway:
    """Central entry point for all client requests."""

    def __init__(self):
        self.order_service_url = "http://order-service:8000"
        self.payment_service_url = "http://payment-service:8001"
        self.http_client = httpx.AsyncClient(timeout=5.0)

    @circuit(failure_threshold=5, recovery_timeout=30)
    async def call_order_service(self, path: str, method: str = "GET", **kwargs):
        """Call order service with circuit breaker."""
        response = await self.http_client.request(
            method, f"{self.order_service_url}{path}", **kwargs
        )
        response.raise_for_status()
        return response.json()

    async def create_order_aggregate(self, order_id: str) -> dict:
        """Aggregate data from multiple services."""
        order, payment, inventory = await asyncio.gather(
            self.call_order_service(f"/orders/{order_id}"),
            self.call_payment_service(f"/payments/order/{order_id}"),
            self.call_inventory_service(f"/reservations/order/{order_id}"),
            return_exceptions=True
        )

        result = {"order": order}
        if not isinstance(payment, Exception):
            result["payment"] = payment
        if not isinstance(inventory, Exception):
            result["inventory"] = inventory
        return result
```

## Communication Patterns

### Pattern 1: Synchronous REST Communication

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class ServiceClient:
    """HTTP client with retries and timeout."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(5.0, connect=2.0))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def get(self, path: str, **kwargs):
        """GET with automatic retries."""
        response = await self.client.get(f"{self.base_url}{path}", **kwargs)
        response.raise_for_status()
        return response.json()

payment_client = ServiceClient("http://payment-service:8001")
result = await payment_client.get("/payments/123")
```

### Pattern 2: Asynchronous Event-Driven

```python
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json

class EventBus:
    """Event publishing and subscription."""

    async def publish(self, event: DomainEvent):
        """Publish event to Kafka topic."""
        await self.producer.send_and_wait(
            event.event_type,
            value=asdict(event),
            key=event.aggregate_id.encode()
        )

    async def subscribe(self, topic: str, handler: callable):
        """Subscribe to events."""
        consumer = AIOKafkaConsumer(topic, bootstrap_servers=self.bootstrap_servers)
        await consumer.start()
        async for message in consumer:
            await handler(message.value)

# Order Service publishes
await event_bus.publish(OrderCreatedEvent(order_id=order.id))

# Inventory Service subscribes
async def handle_order_created(event_data: dict):
    await reserve_inventory(event_data["order_id"], event_data["items"])
```

### Pattern 3: Saga Pattern (Distributed Transactions)

```python
class OrderFulfillmentSaga:
    """Orchestrated saga for order fulfillment."""

    def __init__(self):
        self.steps = [
            SagaStep("create_order", self.create_order, self.cancel_order),
            SagaStep("reserve_inventory", self.reserve_inventory, self.release_inventory),
            SagaStep("process_payment", self.process_payment, self.refund_payment),
            SagaStep("confirm_order", self.confirm_order, self.cancel_order_confirmation)
        ]

    async def execute(self, order_data: dict) -> SagaResult:
        completed_steps = []
        context = {"order_data": order_data}

        try:
            for step in self.steps:
                result = await step.action(context)
                if not result.success:
                    await self.compensate(completed_steps, context)
                    return SagaResult(status=SagaStatus.FAILED, error=result.error)

                completed_steps.append(step)
                context.update(result.data)

            return SagaResult(status=SagaStatus.COMPLETED, data=context)
        except Exception as e:
            await self.compensate(completed_steps, context)
            return SagaResult(status=SagaStatus.FAILED, error=str(e))

    async def compensate(self, completed_steps: List[SagaStep], context: dict):
        """Execute compensating actions in reverse order."""
        for step in reversed(completed_steps):
            await step.compensation(context)
```

## Resilience Patterns

### Circuit Breaker Pattern

```python
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"   # Normal operation
    OPEN = "open"       # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit breaker is open")

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
            self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = datetime.now()

breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30)
result = await breaker.call(payment_client.process_payment, payment_data)
```

## Best Practices

1. **Service Boundaries**: Align with business capabilities
2. **Database Per Service**: No shared databases
3. **API Contracts**: Versioned, backward compatible
4. **Async When Possible**: Events over direct calls
5. **Circuit Breakers**: Fail fast on service failures
6. **Distributed Tracing**: Track requests across services
7. **Service Registry**: Dynamic service discovery
8. **Health Checks**: Liveness and readiness probes

## Common Pitfalls

- **Distributed Monolith**: Tightly coupled services
- **Chatty Services**: Too many inter-service calls
- **Shared Databases**: Tight coupling through data
- **No Circuit Breakers**: Cascade failures
- **Synchronous Everything**: Tight coupling, poor resilience
- **Premature Microservices**: Starting with microservices
- **Ignoring Network Failures**: Assuming reliable network
- **No Compensation Logic**: Can't undo failed transactions
