---
name: microservices-expert
version: 1.0.0
description: Expert-level microservices architecture, patterns, service mesh, and distributed systems
category: api
tags: [microservices, distributed-systems, service-mesh, architecture]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Microservices Expert

Expert guidance for microservices architecture, design patterns, service communication, and distributed system challenges.

## Core Concepts

### Microservices Principles
- Single responsibility per service
- Independently deployable
- Decentralized data management
- Infrastructure automation
- Design for failure
- Evolutionary design

### Architecture Patterns
- API Gateway
- Service Discovery
- Circuit Breaker
- Saga Pattern
- Event Sourcing
- CQRS

### Communication
- Synchronous (HTTP/REST, gRPC)
- Asynchronous (Message queues, Events)
- Service mesh
- API composition
- Backend for Frontend (BFF)

## Service Design

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from typing import List, Optional
from circuitbreaker import circuit
import asyncio

# Individual Microservice
app = FastAPI(title="Order Service", version="1.0.0")

class Order(BaseModel):
    id: str
    user_id: str
    items: List[dict]
    total: float
    status: str

class OrderService:
    def __init__(self, inventory_url: str, payment_url: str):
        self.inventory_url = inventory_url
        self.payment_url = payment_url
        self.client = httpx.AsyncClient()

    @circuit(failure_threshold=5, recovery_timeout=60)
    async def check_inventory(self, items: List[dict]) -> bool:
        """Check inventory availability with circuit breaker"""
        try:
            response = await self.client.post(
                f"{self.inventory_url}/check",
                json={"items": items},
                timeout=5.0
            )
            return response.json()["available"]
        except Exception as e:
            print(f"Inventory service error: {e}")
            raise

    @circuit(failure_threshold=5, recovery_timeout=60)
    async def process_payment(self, user_id: str, amount: float) -> dict:
        """Process payment with circuit breaker"""
        try:
            response = await self.client.post(
                f"{self.payment_url}/charge",
                json={"user_id": user_id, "amount": amount},
                timeout=10.0
            )
            return response.json()
        except Exception as e:
            print(f"Payment service error: {e}")
            raise

    async def create_order(self, order: Order) -> Order:
        """Create order with coordination"""
        # 1. Check inventory
        inventory_available = await self.check_inventory(order.items)
        if not inventory_available:
            raise HTTPException(400, "Items not available")

        # 2. Process payment
        payment = await self.process_payment(order.user_id, order.total)
        if payment["status"] != "success":
            raise HTTPException(400, "Payment failed")

        # 3. Reserve inventory
        await self.reserve_inventory(order.items)

        # 4. Create order record
        order.status = "confirmed"
        await self.save_order(order)

        return order

@app.post("/orders", response_model=Order)
async def create_order(order: Order):
    service = OrderService(
        inventory_url="http://inventory-service",
        payment_url="http://payment-service"
    )
    return await service.create_order(order)
```

## Saga Pattern (Distributed Transactions)

```python
from enum import Enum
from typing import List, Callable
import asyncio

class SagaStep:
    def __init__(self, action: Callable, compensation: Callable):
        self.action = action
        self.compensation = compensation

class SagaOrchestrator:
    """Orchestrate distributed transactions using Saga pattern"""

    def __init__(self):
        self.steps: List[SagaStep] = []
        self.completed_steps: List[SagaStep] = []

    def add_step(self, action: Callable, compensation: Callable):
        """Add a step to the saga"""
        self.steps.append(SagaStep(action, compensation))

    async def execute(self) -> bool:
        """Execute saga with compensation on failure"""
        try:
            # Execute all steps
            for step in self.steps:
                result = await step.action()
                self.completed_steps.append(step)

                if not result:
                    await self.compensate()
                    return False

            return True

        except Exception as e:
            print(f"Saga failed: {e}")
            await self.compensate()
            return False

    async def compensate(self):
        """Rollback completed steps"""
        # Execute compensations in reverse order
        for step in reversed(self.completed_steps):
            try:
                await step.compensation()
            except Exception as e:
                print(f"Compensation failed: {e}")

# Example: Order Saga
class OrderSaga:
    async def create_order_with_saga(self, order_data: dict):
        saga = SagaOrchestrator()

        # Step 1: Reserve inventory
        saga.add_step(
            action=lambda: self.reserve_inventory(order_data["items"]),
            compensation=lambda: self.release_inventory(order_data["items"])
        )

        # Step 2: Process payment
        saga.add_step(
            action=lambda: self.charge_payment(order_data["user_id"], order_data["total"]),
            compensation=lambda: self.refund_payment(order_data["user_id"], order_data["total"])
        )

        # Step 3: Create order
        saga.add_step(
            action=lambda: self.create_order_record(order_data),
            compensation=lambda: self.delete_order_record(order_data["id"])
        )

        # Execute saga
        success = await saga.execute()

        if success:
            await self.send_confirmation(order_data["user_id"])
            return {"status": "success", "order_id": order_data["id"]}
        else:
            return {"status": "failed", "message": "Order creation failed"}
```

## Service Discovery

```python
import consul
from typing import List, Optional
import random

class ServiceRegistry:
    """Service discovery using Consul"""

    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)

    def register_service(self, service_name: str, service_id: str,
                        host: str, port: int, tags: List[str] = None):
        """Register service with Consul"""
        self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=host,
            port=port,
            tags=tags or [],
            check=consul.Check.http(
                f"http://{host}:{port}/health",
                interval="10s",
                timeout="5s"
            )
        )

    def deregister_service(self, service_id: str):
        """Deregister service"""
        self.consul.agent.service.deregister(service_id)

    def discover_service(self, service_name: str) -> Optional[dict]:
        """Discover healthy service instance"""
        _, services = self.consul.health.service(service_name, passing=True)

        if not services:
            return None

        # Load balance: random selection
        service = random.choice(services)

        return {
            "id": service["Service"]["ID"],
            "address": service["Service"]["Address"],
            "port": service["Service"]["Port"],
            "tags": service["Service"]["Tags"]
        }

    def get_all_services(self, service_name: str) -> List[dict]:
        """Get all healthy instances of a service"""
        _, services = self.consul.health.service(service_name, passing=True)

        return [
            {
                "id": s["Service"]["ID"],
                "address": s["Service"]["Address"],
                "port": s["Service"]["Port"]
            }
            for s in services
        ]
```

## API Gateway

```python
from fastapi import FastAPI, Request, Response
import httpx
from typing import Dict
import jwt

app = FastAPI(title="API Gateway")

class APIGateway:
    """API Gateway for routing and cross-cutting concerns"""

    def __init__(self):
        self.service_registry = ServiceRegistry()
        self.client = httpx.AsyncClient()

    async def route_request(self, service: str, path: str,
                           method: str, **kwargs) -> Response:
        """Route request to appropriate microservice"""
        # Discover service
        service_info = self.service_registry.discover_service(service)

        if not service_info:
            return Response(
                content={"error": "Service unavailable"},
                status_code=503
            )

        # Build URL
        url = f"http://{service_info['address']}:{service_info['port']}{path}"

        # Forward request
        response = await self.client.request(method, url, **kwargs)

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )

    async def authenticate(self, token: str) -> Optional[dict]:
        """Centralized authentication"""
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            return payload
        except jwt.JWTError:
            return None

    async def rate_limit(self, client_id: str) -> bool:
        """Centralized rate limiting"""
        # Implementation using Redis
        pass

# Gateway endpoints
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway_route(service: str, path: str, request: Request):
    gateway = APIGateway()

    # Authentication
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user = await gateway.authenticate(token)

    if not user:
        return Response(content={"error": "Unauthorized"}, status_code=401)

    # Rate limiting
    if not await gateway.rate_limit(user["id"]):
        return Response(content={"error": "Rate limit exceeded"}, status_code=429)

    # Route request
    return await gateway.route_request(
        service=service,
        path=f"/{path}",
        method=request.method,
        headers=dict(request.headers),
        content=await request.body()
    )
```

## Event-Driven Architecture

```python
import pika
import json
from typing import Callable, Dict
import asyncio

class EventBus:
    """Message broker for event-driven communication"""

    def __init__(self, rabbitmq_url: str):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(rabbitmq_url)
        )
        self.channel = self.connection.channel()
        self.handlers: Dict[str, Callable] = {}

    def publish_event(self, event_type: str, data: dict):
        """Publish event to all subscribers"""
        self.channel.exchange_declare(
            exchange='events',
            exchange_type='topic',
            durable=True
        )

        message = json.dumps({
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

        self.channel.basic_publish(
            exchange='events',
            routing_key=event_type,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # persistent
            )
        )

    def subscribe(self, event_type: str, handler: Callable):
        """Subscribe to event type"""
        self.handlers[event_type] = handler

        # Declare queue
        queue_name = f"{event_type}_queue"
        self.channel.queue_declare(queue=queue_name, durable=True)

        # Bind queue to exchange
        self.channel.queue_bind(
            queue=queue_name,
            exchange='events',
            routing_key=event_type
        )

        # Start consuming
        def callback(ch, method, properties, body):
            message = json.loads(body)
            handler(message["data"])
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback
        )

    def start_consuming(self):
        """Start consuming events"""
        self.channel.start_consuming()

# Usage Example
event_bus = EventBus("amqp://localhost")

# Service A publishes event
event_bus.publish_event("order.created", {
    "order_id": "12345",
    "user_id": "user_1",
    "total": 99.99
})

# Service B subscribes to event
def handle_order_created(data):
    print(f"Processing order: {data['order_id']}")
    # Send email, update inventory, etc.

event_bus.subscribe("order.created", handle_order_created)
```

## Best Practices

### Design
- Keep services small and focused
- Design for failure (circuit breakers, retries)
- Use asynchronous communication when possible
- Implement proper service boundaries
- Avoid distributed monoliths
- Use API versioning
- Implement health checks

### Data Management
- Database per service
- Use eventual consistency
- Implement saga pattern for distributed transactions
- Use event sourcing for audit trails
- Cache aggressively
- Avoid distributed joins

### Operations
- Implement distributed tracing
- Centralized logging
- Monitor service health
- Automate deployments
- Use service mesh for cross-cutting concerns
- Implement feature flags
- Practice chaos engineering

## Anti-Patterns

❌ Distributed monolith
❌ Shared database between services
❌ Synchronous communication everywhere
❌ No service versioning
❌ Tight coupling between services
❌ No circuit breakers
❌ Missing distributed tracing

## Resources

- Microservices Patterns: https://microservices.io/patterns/
- Building Microservices (book)
- Service Mesh: https://istio.io/
- Consul: https://www.consul.io/
- RabbitMQ: https://www.rabbitmq.com/
