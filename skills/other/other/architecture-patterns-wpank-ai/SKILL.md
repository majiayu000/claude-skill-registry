---
name: architecture-patterns
model: reasoning
---

# Architecture Patterns

## WHAT
Backend architecture patterns for building maintainable, testable systems: Clean Architecture, Hexagonal Architecture, and Domain-Driven Design.

## WHEN
- Designing new backend systems from scratch
- Refactoring monoliths for better maintainability
- Establishing architecture standards for teams
- Creating testable, mockable codebases
- Planning microservices decomposition

## KEYWORDS
clean architecture, hexagonal, ports and adapters, DDD, domain-driven design, layers, entities, use cases, repositories, aggregates, bounded contexts


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install architecture-patterns
```


---

## Decision Framework: Which Pattern?

| Situation | Recommended Pattern |
|-----------|---------------------|
| Simple CRUD app | None (over-engineering) |
| Medium complexity, team standardization | Clean Architecture |
| Multiple external integrations that change frequently | Hexagonal (Ports & Adapters) |
| Complex business domain with many rules | Domain-Driven Design |
| Large system with multiple teams | DDD + Bounded Contexts |

## Quick Reference

### Clean Architecture Layers

```
┌──────────────────────────────────────┐
│      Frameworks & Drivers (UI, DB)   │  ← Outer: Can change
├──────────────────────────────────────┤
│      Interface Adapters              │  ← Controllers, Gateways
├──────────────────────────────────────┤
│      Use Cases                       │  ← Application Logic
├──────────────────────────────────────┤
│      Entities                        │  ← Core Business Rules
└──────────────────────────────────────┘
```

**Dependency Rule**: Dependencies point INWARD only. Inner layers never import outer layers.

### Hexagonal Architecture

```
         ┌─────────────┐
    ┌────│   Adapter   │────┐    (REST API)
    │    └─────────────┘    │
    ▼                       ▼
┌──────┐              ┌──────────┐
│ Port │◄────────────►│  Domain  │
└──────┘              └──────────┘
    ▲                       ▲
    │    ┌─────────────┐    │
    └────│   Adapter   │────┘    (Database)
         └─────────────┘
```

**Ports**: Interfaces defining what the domain needs
**Adapters**: Implementations (swappable for testing)

---

## Directory Structure

```
app/
├── domain/           # Entities & business rules (innermost)
│   ├── entities/
│   │   └── user.py
│   ├── value_objects/
│   │   └── email.py
│   └── interfaces/   # Ports
│       └── user_repository.py
├── use_cases/        # Application business rules
│   └── create_user.py
├── adapters/         # Interface implementations
│   ├── repositories/
│   │   └── postgres_user_repository.py
│   └── controllers/
│       └── user_controller.py
└── infrastructure/   # Framework & external concerns
    ├── database.py
    └── config.py
```

---

## Pattern 1: Clean Architecture

### Entity (Domain Layer)

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """Core entity - NO framework dependencies."""
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self):
        """Business rule in entity."""
        self.is_active = False

    def can_place_order(self) -> bool:
        return self.is_active
```

### Port (Interface)

```python
from abc import ABC, abstractmethod
from typing import Optional

class IUserRepository(ABC):
    """Port: defines contract, no implementation."""
    
    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
```

### Use Case (Application Layer)

```python
@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass  
class CreateUserResponse:
    user: Optional[User]
    success: bool
    error: Optional[str] = None

class CreateUserUseCase:
    """Use case: orchestrates business logic."""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository  # Injected dependency
    
    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # Business validation
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(user=None, success=False, error="Email exists")
        
        # Create entity
        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
            created_at=datetime.now()
        )
        
        saved = await self.user_repository.save(user)
        return CreateUserResponse(user=saved, success=True)
```

### Adapter (Implementation)

```python
class PostgresUserRepository(IUserRepository):
    """Adapter: PostgreSQL implementation of the port."""
    
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            return self._to_entity(row) if row else None
    
    async def save(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO users (id, email, name, created_at, is_active)
                   VALUES ($1, $2, $3, $4, $5)
                   ON CONFLICT (id) DO UPDATE SET email=$2, name=$3, is_active=$5""",
                user.id, user.email, user.name, user.created_at, user.is_active
            )
            return user
```

---

## Pattern 2: Hexagonal (Ports & Adapters)

Best when you have multiple external integrations that may change.

```python
# Domain Service (Core)
class OrderService:
    def __init__(
        self,
        order_repo: OrderRepositoryPort,      # Port
        payment: PaymentGatewayPort,          # Port
        notifications: NotificationPort       # Port
    ):
        self.orders = order_repo
        self.payments = payment
        self.notifications = notifications
    
    async def place_order(self, order: Order) -> OrderResult:
        # Pure business logic - no infrastructure details
        if not order.is_valid():
            return OrderResult(success=False, error="Invalid order")
        
        payment = await self.payments.charge(order.total, order.customer_id)
        if not payment.success:
            return OrderResult(success=False, error="Payment failed")
        
        order.mark_as_paid()
        saved = await self.orders.save(order)
        await self.notifications.send(order.customer_email, "Order confirmed")
        
        return OrderResult(success=True, order=saved)

# Adapters (swap these for testing or changing providers)
class StripePaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        # Real Stripe implementation
        ...

class MockPaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        return PaymentResult(success=True, transaction_id="mock-123")
```

---

## Pattern 3: Domain-Driven Design

For complex business domains with many rules.

### Value Objects (Immutable)

```python
@dataclass(frozen=True)
class Email:
    """Value object: validated, immutable."""
    value: str
    
    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email")

@dataclass(frozen=True)
class Money:
    amount: int  # cents
    currency: str
    
    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)
```

### Aggregates (Consistency Boundaries)

```python
class Order:
    """Aggregate root: enforces invariants."""
    
    def __init__(self, id: str, customer: Customer):
        self.id = id
        self.customer = customer
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: List[DomainEvent] = []
    
    def add_item(self, product: Product, quantity: int):
        """Business logic in aggregate."""
        if quantity > product.max_quantity:
            raise ValueError(f"Max {product.max_quantity} allowed")
        
        item = OrderItem(product, quantity)
        self.items.append(item)
        self._events.append(ItemAddedEvent(self.id, item))
    
    def submit(self):
        """State transition with invariant enforcement."""
        if not self.items:
            raise ValueError("Cannot submit empty order")
        if self.status != OrderStatus.PENDING:
            raise ValueError("Order already submitted")
        
        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(self.id))
```

### Repository Pattern

```python
class OrderRepository:
    """Persist/retrieve aggregates, publish domain events."""
    
    async def save(self, order: Order):
        await self._persist(order)
        await self._publish_events(order._events)
        order._events.clear()
```

---

## Testing Benefits

All patterns enable the same testing approach:

```python
# Test with mock adapter
async def test_create_user():
    mock_repo = MockUserRepository()
    use_case = CreateUserUseCase(user_repository=mock_repo)
    
    result = await use_case.execute(CreateUserRequest(
        email="test@example.com",
        name="Test User"
    ))
    
    assert result.success
    assert result.user.email == "test@example.com"
```

---

## NEVER

- **Anemic Domain Models**: Entities with only data, no behavior (put logic IN entities)
- **Framework Coupling**: Business logic importing Flask, FastAPI, Django ORM
- **Fat Controllers**: Business logic in HTTP handlers
- **Leaky Abstractions**: Repository returning ORM objects instead of domain entities
- **Skipping Layers**: Controller directly accessing database
- **Over-Engineering**: Using Clean Architecture for simple CRUD apps
- **Circular Dependencies**: Use cases importing controllers
