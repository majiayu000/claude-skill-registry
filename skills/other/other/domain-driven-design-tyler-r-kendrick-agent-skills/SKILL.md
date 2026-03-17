---
name: domain-driven-design
description: |
    Domain-Driven Design (DDD) strategic and tactical patterns based on Eric Evans' "Domain-Driven Design" -- covering bounded contexts, aggregates, context maps, and ubiquitous language for modeling complex domains.
    USE FOR: bounded context identification, context mapping, aggregate design, ubiquitous language, domain modeling, subdomain classification, strategic domain design, tactical DDD patterns
    DO NOT USE FOR: event sourcing mechanics (use event-driven), microservice decomposition (use microservices), hexagonal ports/adapters (use hexagonal)
license: MIT
metadata:
  displayName: "Domain-Driven Design"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Martin Fowler — Domain-Driven Design"
    url: "https://martinfowler.com/bliki/DomainDrivenDesign.html"
  - title: "Domain-Driven Design — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Domain-driven_design"
---

# Domain-Driven Design (DDD)

## Overview
Domain-Driven Design is a software design approach that centers the development process on the core business domain. It provides both strategic patterns for organizing large systems and tactical patterns for modeling individual domains. DDD is especially valuable for complex domains where the business logic is the primary source of difficulty.

The canonical reference is Eric Evans' *Domain-Driven Design: Tackling Complexity in the Heart of Software* (2003), supplemented by Vaughn Vernon's *Implementing Domain-Driven Design* (2013) and *Domain-Driven Design Distilled* (2016).

**Core premise:** The structure of the software should mirror the structure of the business domain. The language used by developers should be the same language used by domain experts.

## Strategic DDD

Strategic DDD deals with the big picture: how to decompose a large system into manageable parts, how those parts relate to each other, and how teams communicate across boundaries.

### Ubiquitous Language

A shared, precise language between developers and domain experts for each bounded context. The same term means the same thing everywhere within a context -- in conversations, documentation, code, and tests.

**Rules:**
- One bounded context, one ubiquitous language.
- If a term means different things to different people, you likely have multiple bounded contexts.
- The language should appear literally in the code: class names, method names, variable names.
- Refine the language continuously as understanding deepens.

**Example:** In an e-commerce system, "Order" means different things in different contexts:
- **Sales context:** An Order is a customer's purchase intent with line items and pricing.
- **Fulfillment context:** An Order is a set of items to pick, pack, and ship.
- **Billing context:** An Order is an invoice with payment terms.

Each context has its own Order model with its own ubiquitous language.

### Bounded Contexts

A bounded context is an explicit boundary within which a domain model is defined and applicable. Inside a bounded context, the ubiquitous language is consistent. Across bounded contexts, the same word may mean different things.

```
┌─────────────────────────────────────────────────────┐
│                    E-Commerce System                  │
│                                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │    Sales     │  │ Fulfillment │  │   Billing   │  │
│  │   Context    │  │   Context   │  │   Context   │  │
│  │             │  │             │  │             │  │
│  │ Order =     │  │ Order =     │  │ Order =     │  │
│  │ purchase    │  │ shipment    │  │ invoice     │  │
│  │ intent      │  │ items       │  │             │  │
│  │             │  │             │  │ Customer =  │  │
│  │ Customer =  │  │ Customer =  │  │ billing     │  │
│  │ buyer with  │  │ shipping    │  │ account     │  │
│  │ preferences │  │ address     │  │             │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                       │
│  Each context has its own model, language, and data   │
└─────────────────────────────────────────────────────┘
```

### Subdomains

Subdomains represent areas of the business. They exist independently of software -- they are about the business problem space, not the solution.

| Type | Description | Investment Strategy | Example |
|------|-------------|-------------------|---------|
| **Core** | Your competitive advantage; what differentiates the business | Build custom; invest the best talent | Pricing engine for an insurance company |
| **Supporting** | Necessary for the business but not differentiating | Build simpler custom solutions or customize off-the-shelf | Customer onboarding |
| **Generic** | Common to many businesses; commodity | Buy or use open-source | Authentication, email, payment processing |

**Key insight:** Align bounded contexts with subdomains where possible. Invest the most effort in core subdomains.

### Context Maps

A context map is a visualization of the relationships between bounded contexts. It shows how contexts integrate and what the power dynamics are.

```
┌──────────────┐          ┌──────────────┐
│    Sales     │          │  Fulfillment │
│   (Core)     │─────────▶│ (Supporting) │
│              │  Customer │              │
│              │  -Supplier│              │
└──────┬───────┘          └──────────────┘
       │
       │ Published
       │ Language
       │
┌──────▼───────┐          ┌──────────────┐
│   Billing    │          │  Shipping    │
│   (Core)     │◀─────────│  (Generic)   │
│              │   ACL     │  (3rd party) │
└──────────────┘          └──────────────┘
```

### Context Mapping Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Shared Kernel** | Two contexts share a subset of the model (code, schema). Changes require coordination. | Closely collaborating teams; small shared concepts |
| **Customer-Supplier** | Upstream (supplier) provides what downstream (customer) needs. Customer can influence the API. | Teams with a cooperative relationship; downstream has negotiation power |
| **Conformist** | Downstream conforms to upstream's model without negotiation. | Upstream won't change for you (e.g., large legacy system, external API) |
| **Anti-Corruption Layer (ACL)** | Downstream translates the upstream model into its own model via a translation layer. | Protecting your domain model from a foreign or legacy model |
| **Open Host Service** | Upstream provides a well-defined, versioned API (protocol) for many consumers. | Serving multiple downstream contexts; public APIs |
| **Published Language** | A shared, documented data format (e.g., JSON schema, Protobuf, XML schema) used for integration. | Standardized exchange format; often combined with Open Host Service |
| **Separate Ways** | Contexts have no integration; they solve their own problems independently. | When integration cost exceeds benefit |
| **Partnership** | Two contexts evolve together with mutual coordination. Neither is upstream or downstream. | Co-developing teams with aligned release cadences |

## Tactical DDD

Tactical DDD provides the building blocks for modeling a single bounded context.

### Entities
Objects defined by their **identity**, not their attributes. Two entities with the same attributes but different IDs are different entities. Entities have a lifecycle and mutable state.

```
// An Order is identified by its OrderId, not its contents
public class Order
{
    public OrderId Id { get; }
    public CustomerId CustomerId { get; }
    public List<OrderLine> Lines { get; }
    public OrderStatus Status { get; private set; }

    public void Confirm() { ... }
    public void Cancel() { ... }
}
```

### Value Objects
Objects defined by their **attributes**, not by identity. Two value objects with the same attributes are equal. Value objects are immutable.

```
// A Money value is defined by its amount and currency
public record Money(decimal Amount, string Currency)
{
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new CurrencyMismatchException();
        return new Money(Amount + other.Amount, Currency);
    }
}
```

**Prefer value objects over entities.** Most concepts in a domain are values, not entities. Using value objects reduces bugs (immutability) and improves clarity.

### Aggregates and Aggregate Roots

An aggregate is a cluster of entities and value objects treated as a single unit for data changes. The **aggregate root** is the entry point -- all external access goes through the root. The root enforces invariants (business rules) for the entire aggregate.

```
┌──────────────────────────────────────┐
│  Order Aggregate                      │
│                                       │
│  ┌────────────────┐                  │
│  │ Order          │ ◄── Aggregate    │
│  │ (Root)         │     Root         │
│  │                │                  │
│  │ - orderId      │                  │
│  │ - status       │                  │
│  │ - totalAmount  │                  │
│  └───┬────────────┘                  │
│      │ contains                      │
│      │                               │
│  ┌───▼────────────┐  ┌───────────┐  │
│  │ OrderLine      │  │ Money     │  │
│  │ (Entity)       │  │ (Value)   │  │
│  │ - lineId       │  │ - amount  │  │
│  │ - productId    │  │ - currency│  │
│  │ - quantity     │  │           │  │
│  └────────────────┘  └───────────┘  │
│                                       │
│  Invariant: total = sum of lines      │
│  Invariant: max 20 lines per order    │
└──────────────────────────────────────┘
```

### Aggregate Design Rules

1. **Reference other aggregates by identity only.** An Order aggregate holds a `CustomerId`, not a `Customer` object.
2. **Keep aggregates small.** Large aggregates cause contention, slow loading, and complex invariants. Prefer small aggregates with eventual consistency between them.
3. **One transaction per aggregate.** Modify only one aggregate per transaction. Use domain events for cross-aggregate coordination.
4. **Protect invariants within the aggregate boundary.** Business rules that span multiple aggregates must be handled via eventual consistency (domain events, sagas).

### Aggregate Design Example

```
// GOOD: Small aggregates, reference by ID, domain events

public class Order    // Aggregate root
{
    public OrderId Id { get; }
    private List<OrderLine> _lines = new();

    public void AddLine(ProductId productId, int quantity, Money price)
    {
        if (_lines.Count >= 20)
            throw new TooManyLinesException();
        _lines.Add(new OrderLine(productId, quantity, price));
        AddDomainEvent(new OrderLineAdded(Id, productId, quantity));
    }

    public void Confirm()
    {
        if (!_lines.Any()) throw new EmptyOrderException();
        Status = OrderStatus.Confirmed;
        AddDomainEvent(new OrderConfirmed(Id, TotalAmount));
    }
}

public class Inventory    // Separate aggregate
{
    public ProductId ProductId { get; }
    public int AvailableQuantity { get; private set; }

    // Reacts to OrderConfirmed event (eventual consistency)
    public void Reserve(int quantity)
    {
        if (AvailableQuantity < quantity)
            throw new InsufficientStockException();
        AvailableQuantity -= quantity;
        AddDomainEvent(new StockReserved(ProductId, quantity));
    }
}
```

### Domain Events
Events that represent something significant that happened in the domain. Domain events enable loose coupling between aggregates and bounded contexts.

**Naming convention:** Past tense, describing what happened -- `OrderPlaced`, `PaymentReceived`, `ShipmentDispatched`.

See `dev/architecture/event-driven` for event sourcing and event-driven architecture patterns.

### Repositories
Provide collection-like access to aggregates. One repository per aggregate root. Repositories abstract the persistence mechanism.

```
public interface IOrderRepository
{
    Task<Order?> GetById(OrderId id);
    Task Save(Order order);
    Task Delete(OrderId id);
    // No query methods here -- queries belong in the read model (CQRS)
}
```

### Domain Services
Operations that don't naturally belong to any single entity or value object. Domain services are stateless and express domain logic.

```
// Pricing logic that spans multiple aggregates
public class PricingService
{
    public Money CalculateDiscount(
        Order order, CustomerTier tier, IReadOnlyList<Promotion> activePromotions)
    {
        // Complex pricing logic that doesn't belong in Order or Customer
    }
}
```

### Application Services
Orchestrate use cases by coordinating domain objects, repositories, and infrastructure concerns. Application services are the entry point from the outside world (API controllers, message handlers) into the domain.

```
public class PlaceOrderHandler
{
    public async Task Handle(PlaceOrderCommand command)
    {
        var order = new Order(command.CustomerId);
        foreach (var item in command.Items)
            order.AddLine(item.ProductId, item.Quantity, item.Price);
        order.Confirm();
        await _orderRepository.Save(order);
        await _eventPublisher.Publish(order.DomainEvents);
    }
}
```

### Factories
Encapsulate complex aggregate creation logic. Use factories when object construction involves business rules, validation, or coordination.

## Strategic + Tactical DDD Together

```
Strategic (System Level):
  Identify Subdomains → Define Bounded Contexts → Map Context Relationships

Tactical (Within Each Context):
  Model Aggregates → Define Entities & Value Objects →
  Publish Domain Events → Implement Repositories & Services
```

## Common DDD Anti-Patterns

| Anti-Pattern | Problem | Solution |
|-------------|---------|----------|
| **Anemic Domain Model** | Entities are just data bags; logic lives in services | Move behavior into entities and value objects |
| **God Aggregate** | One massive aggregate with many entities | Break into smaller aggregates; use eventual consistency |
| **Shared Database across Contexts** | Bounded contexts lose independence | Each context owns its data; integrate through events or APIs |
| **Ubiquitous Language mismatch** | Code uses different terms than domain experts | Refactor code to match the domain language exactly |
| **DDD everywhere** | Applying DDD to simple CRUD domains | Use DDD for core subdomains; use simpler approaches for generic/supporting |

## Best Practices
- Apply DDD only where the domain complexity justifies it (core subdomains). For CRUD-heavy generic subdomains, simpler approaches are fine.
- Invest heavily in ubiquitous language. If developers and domain experts use different words, the design will drift.
- Keep aggregates small. The default should be a single entity as the aggregate root. Add more only when invariants require it.
- Reference other aggregates by identity, never by direct object reference.
- Use domain events for cross-aggregate and cross-context communication.
- Collaborate with domain experts continuously -- DDD is not a solo developer activity.
- Draw context maps early and revisit them as the system evolves.
- Bounded context boundaries often align well with microservice boundaries (see `dev/architecture/microservices`), but they don't have to -- a modular monolith can also respect bounded contexts (see `dev/architecture/monoliths`).
