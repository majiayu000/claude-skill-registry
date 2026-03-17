---
name: event-driven
description: |
  Use when designing event-driven architectures and patterns for loosely coupled, asynchronous .NET systems.
  USE FOR: event-driven architecture patterns, domain events, integration events, event sourcing fundamentals, pub/sub design, event bus abstraction
  DO NOT USE FOR: specific message bus implementation (use masstransit, nservicebus, or rebus), actor model concurrency (use akka-net), simple request/response mediation (use mediatr)
license: MIT
metadata:
  displayName: "Event-Driven Architecture"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "Event-Driven Architecture Style"
    url: "https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven"
  - title: ".NET Microservices Architecture Guidance"
    url: "https://learn.microsoft.com/en-us/dotnet/architecture/microservices/"
---

# Event-Driven Architecture

## Overview
Event-Driven Architecture (EDA) is a design paradigm where system components communicate through events -- immutable records of significant state changes or occurrences. Producers emit events without knowledge of consumers, and consumers react asynchronously. This decoupling enables independent scaling, deployment, and evolution of services. In .NET, EDA is implemented through domain events (in-process), integration events (cross-service), and event sourcing (persisting state as a sequence of events).

## Event Types

| Type | Scope | Transport | Example |
|------|-------|-----------|---------|
| Domain Event | Single bounded context | In-process (mediator) | `OrderPlaced` within Order service |
| Integration Event | Cross-service | Message broker (RabbitMQ, etc.) | `OrderPlaced` to Shipping service |
| Notification Event | Thin notification | Broker or webhook | `{ orderId: "abc" }` -- consumer fetches details |
| Event-Carried State Transfer | Fat event with data | Broker | Full order snapshot in the event payload |

## Domain Events
```csharp
// Base domain event
public abstract record DomainEvent
{
    public Guid EventId { get; init; } = Guid.NewGuid();
    public DateTime OccurredAt { get; init; } = DateTime.UtcNow;
}

// Concrete domain events
public sealed record OrderPlaced(
    Guid OrderId,
    string CustomerId,
    decimal Total,
    IReadOnlyList<OrderLineItem> Items) : DomainEvent;

public sealed record OrderShipped(
    Guid OrderId,
    string TrackingNumber,
    DateTime ShippedAt) : DomainEvent;

public sealed record OrderLineItem(string ProductId, int Quantity, decimal UnitPrice);

// Aggregate root with domain events
public abstract class AggregateRoot
{
    private readonly List<DomainEvent> _domainEvents = new();
    public IReadOnlyList<DomainEvent> DomainEvents => _domainEvents.AsReadOnly();

    protected void RaiseDomainEvent(DomainEvent domainEvent)
        => _domainEvents.Add(domainEvent);

    public void ClearDomainEvents() => _domainEvents.Clear();
}

public class Order : AggregateRoot
{
    public Guid Id { get; private set; }
    public string CustomerId { get; private set; } = default!;
    public OrderStatus Status { get; private set; }
    public decimal Total { get; private set; }

    public static Order Place(string customerId, List<OrderLineItem> items)
    {
        var order = new Order
        {
            Id = Guid.NewGuid(),
            CustomerId = customerId,
            Status = OrderStatus.Placed,
            Total = items.Sum(i => i.Quantity * i.UnitPrice)
        };

        order.RaiseDomainEvent(new OrderPlaced(order.Id, customerId, order.Total, items));
        return order;
    }

    public void Ship(string trackingNumber)
    {
        if (Status != OrderStatus.Placed)
            throw new InvalidOperationException("Only placed orders can be shipped.");

        Status = OrderStatus.Shipped;
        RaiseDomainEvent(new OrderShipped(Id, trackingNumber, DateTime.UtcNow));
    }
}

public enum OrderStatus { Placed, Shipped, Delivered, Cancelled }
```

## Dispatching Domain Events via EF Core
```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    private readonly IMediator _mediator;

    public AppDbContext(DbContextOptions<AppDbContext> options, IMediator mediator)
        : base(options)
    {
        _mediator = mediator;
    }

    public DbSet<Order> Orders => Set<Order>();

    public override async Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        var domainEvents = ChangeTracker.Entries<AggregateRoot>()
            .SelectMany(e => e.Entity.DomainEvents)
            .ToList();

        var result = await base.SaveChangesAsync(ct);

        foreach (var domainEvent in domainEvents)
        {
            await _mediator.Publish(domainEvent, ct);
        }

        foreach (var entry in ChangeTracker.Entries<AggregateRoot>())
        {
            entry.Entity.ClearDomainEvents();
        }

        return result;
    }
}
```

## Domain Event Handlers
```csharp
public interface IDomainEventHandler<in TEvent> where TEvent : DomainEvent
{
    Task HandleAsync(TEvent domainEvent, CancellationToken ct = default);
}

public sealed class SendOrderConfirmationEmail : IDomainEventHandler<OrderPlaced>
{
    private readonly IEmailService _email;

    public SendOrderConfirmationEmail(IEmailService email) => _email = email;

    public async Task HandleAsync(OrderPlaced evt, CancellationToken ct = default)
    {
        await _email.SendAsync(
            evt.CustomerId,
            "Order Confirmed",
            $"Your order {evt.OrderId} for {evt.Total:C} has been placed.",
            ct);
    }
}

public sealed class UpdateInventory : IDomainEventHandler<OrderPlaced>
{
    private readonly IInventoryService _inventory;

    public UpdateInventory(IInventoryService inventory) => _inventory = inventory;

    public async Task HandleAsync(OrderPlaced evt, CancellationToken ct = default)
    {
        foreach (var item in evt.Items)
        {
            await _inventory.ReserveAsync(item.ProductId, item.Quantity, ct);
        }
    }
}
```

## Integration Events
```csharp
// Integration event for cross-service communication
public sealed record OrderPlacedIntegrationEvent(
    Guid EventId,
    DateTime OccurredAt,
    Guid OrderId,
    string CustomerId,
    decimal Total);

// Publisher: converts domain event to integration event
public sealed class PublishOrderPlacedIntegration : IDomainEventHandler<OrderPlaced>
{
    private readonly IEventBus _eventBus;

    public PublishOrderPlacedIntegration(IEventBus eventBus) => _eventBus = eventBus;

    public async Task HandleAsync(OrderPlaced evt, CancellationToken ct = default)
    {
        var integrationEvent = new OrderPlacedIntegrationEvent(
            evt.EventId, evt.OccurredAt, evt.OrderId, evt.CustomerId, evt.Total);

        await _eventBus.PublishAsync(integrationEvent, ct);
    }
}

// Event bus abstraction
public interface IEventBus
{
    Task PublishAsync<TEvent>(TEvent @event, CancellationToken ct = default);
}
```

## Event Sourcing Basics
```csharp
public abstract class EventSourcedAggregate
{
    private readonly List<DomainEvent> _uncommittedEvents = new();
    public int Version { get; private set; } = -1;

    public IReadOnlyList<DomainEvent> UncommittedEvents => _uncommittedEvents.AsReadOnly();

    protected void Apply(DomainEvent @event)
    {
        When(@event);
        Version++;
        _uncommittedEvents.Add(@event);
    }

    public void Load(IEnumerable<DomainEvent> history)
    {
        foreach (var @event in history)
        {
            When(@event);
            Version++;
        }
    }

    public void ClearUncommittedEvents() => _uncommittedEvents.Clear();

    protected abstract void When(DomainEvent @event);
}

public class EventSourcedOrder : EventSourcedAggregate
{
    public Guid Id { get; private set; }
    public OrderStatus Status { get; private set; }
    public decimal Total { get; private set; }

    public static EventSourcedOrder Place(string customerId, decimal total)
    {
        var order = new EventSourcedOrder();
        order.Apply(new OrderPlaced(Guid.NewGuid(), customerId, total, Array.Empty<OrderLineItem>()));
        return order;
    }

    public void Ship(string trackingNumber)
    {
        if (Status != OrderStatus.Placed)
            throw new InvalidOperationException("Cannot ship.");
        Apply(new OrderShipped(Id, trackingNumber, DateTime.UtcNow));
    }

    protected override void When(DomainEvent @event)
    {
        switch (@event)
        {
            case OrderPlaced e:
                Id = e.OrderId;
                Total = e.Total;
                Status = OrderStatus.Placed;
                break;
            case OrderShipped:
                Status = OrderStatus.Shipped;
                break;
        }
    }
}
```

## Outbox Pattern
```csharp
// Store events in the same transaction as state changes
public class OutboxMessage
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string EventType { get; set; } = default!;
    public string Payload { get; set; } = default!;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? ProcessedAt { get; set; }
}

public class OutboxDbContext : DbContext
{
    public DbSet<OutboxMessage> OutboxMessages => Set<OutboxMessage>();

    public async Task AddToOutboxAsync<TEvent>(TEvent @event, CancellationToken ct)
    {
        OutboxMessages.Add(new OutboxMessage
        {
            EventType = typeof(TEvent).AssemblyQualifiedName!,
            Payload = JsonSerializer.Serialize(@event)
        });
        await SaveChangesAsync(ct);
    }
}

// Background worker publishes outbox messages
public class OutboxProcessor : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly IEventBus _eventBus;

    public OutboxProcessor(IServiceScopeFactory scopeFactory, IEventBus eventBus)
    {
        _scopeFactory = scopeFactory;
        _eventBus = eventBus;
    }

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            using var scope = _scopeFactory.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<OutboxDbContext>();

            var pending = await db.OutboxMessages
                .Where(m => m.ProcessedAt == null)
                .OrderBy(m => m.CreatedAt)
                .Take(50)
                .ToListAsync(ct);

            foreach (var message in pending)
            {
                var type = Type.GetType(message.EventType)!;
                var @event = JsonSerializer.Deserialize(message.Payload, type)!;
                await _eventBus.PublishAsync(@event, ct);
                message.ProcessedAt = DateTime.UtcNow;
            }

            await db.SaveChangesAsync(ct);
            await Task.Delay(TimeSpan.FromSeconds(5), ct);
        }
    }
}
```

## Best Practices
- Make all events immutable using C# `record` types with `init`-only properties; events represent facts that have already occurred and must not change.
- Name events in past tense (`OrderPlaced`, `PaymentProcessed`) to clearly communicate that they describe something that already happened.
- Separate domain events (in-process, within a bounded context) from integration events (cross-service, via message broker) to control coupling boundaries.
- Include a unique `EventId` and `OccurredAt` timestamp on every event for idempotency checks and temporal ordering.
- Use the Outbox pattern to publish integration events in the same database transaction as state changes, preventing lost events from dual-write failures.
- Design event handlers to be idempotent so that reprocessing the same event (due to retries or at-least-once delivery) produces the same result.
- Dispatch domain events after `SaveChangesAsync` succeeds to ensure handlers only react to persisted state changes.
- Keep event payloads focused: include enough context for consumers to act without calling back, but avoid leaking internal domain details.
- Version events explicitly (e.g., `OrderPlacedV2`) when making breaking changes; support both old and new versions during migration periods.
- Monitor event processing lag and dead-letter queues in production; set up alerts for consumers that fall behind or repeatedly fail on specific events.
