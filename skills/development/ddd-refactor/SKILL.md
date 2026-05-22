---
name: ddd-refactor
description: Analyzes and refactors code using Domain-Driven Design principles. Use when refactoring domain models, identifying DDD anti-patterns, improving domain clarity, or applying tactical/strategic DDD patterns.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# DDD Refactor Skill

Comprehensive Domain-Driven Design refactoring framework based on Eric Evans' DDD principles.

## When to Use This Skill

- Refactoring domain models and business logic
- Identifying anemic domain models
- Defining bounded contexts
- Applying tactical DDD patterns (Entity, Value Object, Aggregate)
- Improving domain clarity and ubiquitous language
- Analyzing code for DDD anti-patterns
- Architecting domain-centric systems

## Prerequisites

**CRITICAL**: Always load the DDD principles first:

```bash
Read: plugins/ddd-refactor/resources/ddd-principles.json
```

This JSON contains 19+ principles with definitions, code smells, and refactoring guidance.

## Refactoring Approach

### Four-Phase Strategy

#### Phase 1: Discovery & Analysis (15-20 min)

**Understand the Domain:**
1. Identify core domain vs supporting/generic subdomains
2. Map existing bounded contexts (explicit or implicit)
3. Document current ubiquitous language usage
4. Analyze domain model structure

**Scan for Code Smells:**
- Anemic domain models (all logic in services)
- Missing ubiquitous language (technical jargon)
- Blurred bounded context boundaries
- Mutable value objects
- Large aggregates without clear boundaries
- Domain logic in application/infrastructure layers
- Missing domain events
- Repositories exposing internal entities
- Bidirectional dependencies across contexts

**Technical Exploration:**
```bash
# Find potential entities
grep -r "class.*Entity" --include="*.{js,ts,java,cs,py}"

# Find service classes (potential logic that belongs in domain)
grep -r "class.*Service" --include="*.{js,ts,java,cs,py}"

# Find repositories
grep -r "Repository" --include="*.{js,ts,java,cs,py}"

# Find domain events (or lack thereof)
grep -r "Event\|event" --include="*.{js,ts,java,cs,py}"
```

#### Phase 2: Strategic Refactoring Plan (10-15 min)

Based on loaded DDD principles:

1. **Define Bounded Contexts**
   - Map natural domain boundaries
   - Identify context relationships (Shared Kernel, Customer-Supplier, etc.)
   - Plan integration strategies

2. **Establish Ubiquitous Language**
   - List terms needing renaming
   - Extract implicit concepts into explicit models
   - Create domain glossary

3. **Prioritize Refactoring**
   - **Critical**: Core domain models, aggregate boundaries, data consistency
   - **High**: Entity/Value Object patterns, domain events, repositories
   - **Medium**: Services, factories, layering
   - **Low**: Supporting subdomains, infrastructure

#### Phase 3: Tactical Pattern Application (30-45 min)

Apply patterns systematically:

**1. Entities** - Identity-based objects
- Extract objects with lifecycle and identity
- Add identity equality (not value equality)
- Encapsulate business rules within entities
- Make state changes explicit through methods

**2. Value Objects** - Immutable descriptive objects
- Convert primitive obsession to value objects
- Make all value objects immutable
- Implement value-based equality
- Create self-validating value objects

**3. Aggregates** - Consistency boundaries
- Group related entities under aggregate roots
- Enforce invariants at aggregate boundaries
- Make internal entities inaccessible from outside
- Use aggregate roots for all external access

**4. Domain Events** - Significant occurrences
- Identify state changes that matter to the domain
- Publish events from aggregates after state changes
- Use events to decouple bounded contexts
- Record event history for audit/debugging

**5. Repositories** - Aggregate persistence
- Create repositories only for aggregate roots
- Return reconstituted aggregates (not raw data)
- Abstract all storage concerns
- Use specification pattern for complex queries

**6. Domain Services** - Stateless operations
- Extract operations that don't belong to any entity
- Keep services thin (orchestration, not logic)
- Separate Domain/Application/Infrastructure services
- Make service operations explicit domain concepts

**7. Factories** - Complex creation
- Encapsulate complex aggregate construction
- Hide creation details from clients
- Ensure invariants are met at creation
- Provide convenient creation methods

**8. Layered Architecture**
- Move domain logic from controllers to domain layer
- Isolate external systems with anti-corruption layers
- Ensure dependencies point inward (domain is innermost)
- Keep domain layer free of infrastructure concerns

#### Phase 4: Validation & Testing (10-15 min)

**Verify Improvements:**
- [ ] Ubiquitous language is reflected in code
- [ ] Business rules are explicit and testable
- [ ] Bounded contexts have clear boundaries
- [ ] Aggregates enforce their invariants
- [ ] Domain events capture significant changes
- [ ] Repositories work with aggregate roots
- [ ] Domain layer is free of infrastructure
- [ ] Integration points are explicit and controlled

**Testing Strategy:**
- Unit test entity/value object logic
- Test aggregate invariant enforcement
- Test domain event publication
- Integration test repositories
- Test anti-corruption layers

## Core DDD Principles Reference

### Strategic Design
1. **Ubiquitous Language** - Domain vocabulary in code
2. **Bounded Context** - Explicit model boundaries
3. **Context Map** - Relationships between contexts
4. **Continuous Integration** - Prevent fragmentation

### Tactical Patterns
5. **Entity** - Identity-based objects with lifecycle
6. **Value Object** - Immutable, attribute-based objects
7. **Aggregate** - Consistency boundary and transaction scope
8. **Repository** - Collection-like access to aggregates
9. **Factory** - Complex object creation
10. **Domain Service** - Stateless domain operations
11. **Domain Event** - Record of domain occurrence

### Architecture
12. **Layered Architecture** - Separation of concerns
13. **Anti-Corruption Layer** - Isolation from external systems

### Context Mapping
14. **Shared Kernel** - Explicit sharing between contexts
15. **Customer-Supplier** - Upstream-downstream relationship
16. **Conformist** - Adopt upstream model
17. **Open Host Service** - Standardized API
18. **Published Language** - Documented interchange format

## Code Smell Detection Checklist

### Strategic Anti-Patterns
- [ ] No explicit bounded contexts
- [ ] Technical names instead of domain language
- [ ] Mixed business logic across contexts
- [ ] No context integration strategy
- [ ] Same entity meaning different things in different places

### Tactical Anti-Patterns
- [ ] Anemic domain model (getters/setters only)
- [ ] Entities without clear identity
- [ ] Mutable value objects
- [ ] Large aggregates (>5-7 entities)
- [ ] Repositories for non-root entities
- [ ] Domain logic in services instead of entities
- [ ] No domain events for state changes
- [ ] Primitive obsession (no value objects)

### Architecture Anti-Patterns
- [ ] Domain logic in controllers/UI
- [ ] Direct database access from domain
- [ ] No anti-corruption layer for external systems
- [ ] Infrastructure concerns in domain layer
- [ ] Bidirectional dependencies between contexts

## Output Format

### 1. Anti-Pattern Identified
```
File: src/orders/OrderService.java:45-78
Smell: Anemic domain model - Order entity has only getters/setters
Principle Violated: Entity Pattern
Impact: Business logic scattered in services, hard to test and maintain
```

### 2. DDD Principle to Apply
```
Principle: Entity (from ddd-principles.json)
Category: Tactical Pattern
Key Point: Entities should encapsulate business rules and behavior
When to Apply: Objects with identity that change over time
```

### 3. Refactoring Steps
```
Step 1: Move validation logic from OrderService to Order entity
Step 2: Add domain methods: order.cancel(), order.ship(), order.addItem()
Step 3: Enforce invariants within entity methods
Step 4: Raise domain events for significant state changes
Step 5: Update OrderService to orchestrate, not contain logic
```

### 4. Code Example
```typescript
// BEFORE: Anemic Domain Model (Anti-pattern)
class Order {
  private id: string;
  private items: OrderItem[];
  private status: string;

  // Only getters and setters
  getId(): string { return this.id; }
  getStatus(): string { return this.status; }
  setStatus(status: string): void { this.status = status; }
}

class OrderService {
  cancelOrder(order: Order): void {
    // Business logic in service layer
    if (order.getStatus() === 'SHIPPED') {
      throw new Error('Cannot cancel shipped order');
    }
    order.setStatus('CANCELLED');
    this.emailService.sendCancellationEmail(order);
  }
}

// AFTER: Rich Domain Model (DDD Pattern)
class Order {
  private id: OrderId;
  private items: OrderItem[];
  private status: OrderStatus;
  private events: DomainEvent[] = [];

  constructor(id: OrderId, items: OrderItem[]) {
    this.id = id;
    this.items = items;
    this.status = OrderStatus.PENDING;
  }

  // Business logic in entity
  cancel(): void {
    if (!this.canBeCancelled()) {
      throw new OrderCannotBeCancelledException(
        'Cannot cancel order in status: ' + this.status
      );
    }
    this.status = OrderStatus.CANCELLED;
    this.recordEvent(new OrderCancelled(this.id, new Date()));
  }

  private canBeCancelled(): boolean {
    return this.status !== OrderStatus.SHIPPED
        && this.status !== OrderStatus.DELIVERED;
  }

  getDomainEvents(): DomainEvent[] {
    return [...this.events];
  }

  private recordEvent(event: DomainEvent): void {
    this.events.push(event);
  }
}

// Service becomes thin orchestrator
class OrderService {
  constructor(
    private orderRepository: OrderRepository,
    private eventBus: EventBus
  ) {}

  async cancelOrder(orderId: string): Promise<void> {
    const order = await this.orderRepository.findById(orderId);

    order.cancel(); // Domain logic stays in domain

    await this.orderRepository.save(order);

    // Publish events for other bounded contexts
    order.getDomainEvents().forEach(event => {
      this.eventBus.publish(event);
    });
  }
}
```

### 5. Impact Assessment
**Benefits:**
- Business rules are explicit and self-documenting
- Order enforces its own invariants
- Easier to test (unit test the entity)
- Domain events enable loose coupling
- Service layer is thin and focused

**Metrics:**
- Reduced cyclomatic complexity in services
- Increased testability (pure domain logic)
- Better domain language alignment
- Clearer responsibility boundaries

## Language-Specific Patterns

### TypeScript/JavaScript
```typescript
// Value Object with immutability
class Money {
  constructor(
    private readonly amount: number,
    private readonly currency: string
  ) {
    if (amount < 0) throw new Error('Amount cannot be negative');
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error('Currency mismatch');
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount
        && this.currency === other.currency;
  }
}
```

### Java
```java
// Aggregate with encapsulation
public class Order {
  private final OrderId id;
  private final List<OrderLine> lines;
  private OrderStatus status;

  // Package-private constructor (use factory)
  Order(OrderId id) {
    this.id = Objects.requireNonNull(id);
    this.lines = new ArrayList<>();
    this.status = OrderStatus.DRAFT;
  }

  public void addLine(Product product, Quantity quantity) {
    if (this.status != OrderStatus.DRAFT) {
      throw new OrderAlreadySubmittedException();
    }
    this.lines.add(new OrderLine(product, quantity));
  }

  // Factory method
  public static Order create(OrderId id) {
    return new Order(id);
  }
}
```

### Python
```python
from dataclasses import dataclass
from typing import List

# Value Object with frozen dataclass
@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self):
        if '@' not in self.value:
            raise ValueError('Invalid email address')

# Entity with behavior
class Customer:
    def __init__(self, customer_id: str, email: EmailAddress):
        self._id = customer_id
        self._email = email
        self._events: List[DomainEvent] = []

    def change_email(self, new_email: EmailAddress) -> None:
        if self._email != new_email:
            old_email = self._email
            self._email = new_email
            self._events.append(
                EmailChanged(self._id, old_email, new_email)
            )
```

## Best Practices

### Do
- Start with the domain model, not the database
- Use domain language everywhere (code, tests, docs)
- Make implicit concepts explicit
- Favor immutability where possible
- Test domain logic in isolation
- Keep aggregates small (2-5 entities max)
- Use domain events for inter-context communication
- Apply anti-corruption layers for external systems

### Don't
- Don't let infrastructure drive the domain model
- Don't skip domain events for significant changes
- Don't make value objects mutable
- Don't expose aggregate internals
- Don't create repositories for non-aggregate roots
- Don't put domain logic in services
- Don't share entities across bounded contexts
- Don't over-engineer - apply DDD where complexity justifies it

## Resources

- **DDD Principles**: See `resources/ddd-principles.json` for complete definitions
- **Checklist**: See `CHECKLIST.md` for full anti-pattern list
- **Book**: "Domain-Driven Design" by Eric Evans

## Workflow Integration

This skill can be:
- Invoked from `/refactor` command
- Used by `ddd-analyzer` agent for autonomous analysis
- Triggered by pre-commit hooks to check for anti-patterns
- Called from other skills for domain model improvements
