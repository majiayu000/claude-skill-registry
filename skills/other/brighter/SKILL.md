---
name: brighter
description: |
  Use when implementing CQRS command dispatching, request pipelines, and asynchronous task queues with Paramore Brighter in .NET.
  USE FOR: command dispatching, CQRS command side, request handler pipelines, async task queues, policy-based retry and circuit breaker on handlers
  DO NOT USE FOR: simple in-process mediator without policies (use mediatr), full service bus with transport abstraction (use masstransit or nservicebus), event sourcing storage (use akka-net persistence)
license: MIT
metadata:
  displayName: "Brighter"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "Brighter Official Website"
    url: "https://www.goparamore.io/"
  - title: "Brighter GitHub Repository"
    url: "https://github.com/BrighterCommand/Brighter"
  - title: "Paramore.Brighter NuGet Package"
    url: "https://www.nuget.org/packages/Paramore.Brighter"
---

# Brighter (Paramore.Brighter)

## Overview
Paramore Brighter is a command dispatcher and processor library for .NET implementing the Command pattern with a pipeline of handlers. It supports synchronous dispatch, asynchronous task queues (via Paramore Darker for queries), attribute-based policies (retry, circuit breaker, timeout), and integration with external message brokers for decoupled messaging. Brighter separates command dispatch from handling and enables cross-cutting concerns through a decorator pipeline.

## NuGet Packages
- `Paramore.Brighter` -- core command processor and handler infrastructure
- `Paramore.Brighter.Extensions.DependencyInjection` -- Microsoft DI integration
- `Paramore.Brighter.Extensions.Hosting` -- hosted service for message pump
- `Paramore.Brighter.MessagingGateway.RMQ` -- RabbitMQ transport
- `Paramore.Brighter.MessagingGateway.AzureServiceBus` -- Azure Service Bus transport
- `Paramore.Darker` -- query processor (read side of CQRS)
- `Paramore.Darker.AspNetCore` -- ASP.NET Core integration for queries

## Commands and Events
```csharp
using Paramore.Brighter;

// Command: intent to perform an action (one handler)
public class CreateOrder : Command
{
    public string CustomerId { get; init; }
    public decimal Total { get; init; }

    public CreateOrder(string customerId, decimal total)
        : base(Guid.NewGuid())
    {
        CustomerId = customerId;
        Total = total;
    }
}

// Event: notification of something that happened (multiple handlers)
public class OrderCreated : Event
{
    public Guid OrderId { get; init; }
    public string CustomerId { get; init; }

    public OrderCreated(Guid orderId, string customerId)
        : base(Guid.NewGuid())
    {
        OrderId = orderId;
        CustomerId = customerId;
    }
}
```

## Request Handlers
```csharp
using Paramore.Brighter;
using Paramore.Brighter.Policies.Attributes;

public class CreateOrderHandler : RequestHandlerAsync<CreateOrder>
{
    private readonly IOrderRepository _repository;
    private readonly IAmACommandProcessor _processor;

    public CreateOrderHandler(IOrderRepository repository, IAmACommandProcessor processor)
    {
        _repository = repository;
        _processor = processor;
    }

    [RequestLogging(step: 1, timing: HandlerTiming.Before)]
    [UsePolicy(CommandProcessor.RETRYPOLICYASYNC, step: 2)]
    public override async Task<CreateOrder> HandleAsync(
        CreateOrder command,
        CancellationToken ct = default)
    {
        var order = new Order(command.CustomerId, command.Total);
        await _repository.AddAsync(order, ct);

        await _processor.PostAsync(
            new OrderCreated(order.Id, order.CustomerId), cancellationToken: ct);

        return await base.HandleAsync(command, ct);
    }
}

// Event handler (subscriber)
public class OrderCreatedNotificationHandler : RequestHandlerAsync<OrderCreated>
{
    private readonly INotificationService _notifications;

    public OrderCreatedNotificationHandler(INotificationService notifications)
        => _notifications = notifications;

    public override async Task<OrderCreated> HandleAsync(
        OrderCreated @event,
        CancellationToken ct = default)
    {
        await _notifications.SendAsync(
            @event.CustomerId, $"Order {@event.OrderId} confirmed.", ct);

        return await base.HandleAsync(@event, ct);
    }
}
```

## Registration and Configuration
```csharp
using Paramore.Brighter.Extensions.DependencyInjection;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddBrighter(options =>
    {
        options.PolicyRegistry = GetPolicies();
    })
    .AutoFromAssemblies();

builder.Services.AddScoped<IOrderRepository, OrderRepository>();

var app = builder.Build();

app.MapPost("/orders", async (CreateOrder cmd, IAmACommandProcessor processor) =>
{
    await processor.SendAsync(cmd);
    return Results.Accepted();
});

app.Run();

static PolicyRegistry GetPolicies()
{
    var registry = new PolicyRegistry
    {
        {
            CommandProcessor.RETRYPOLICYASYNC,
            Policy.Handle<Exception>()
                  .WaitAndRetryAsync(3, retry => TimeSpan.FromMilliseconds(100 * Math.Pow(2, retry)))
        },
        {
            CommandProcessor.CIRCUITBREAKERASYNC,
            Policy.Handle<Exception>()
                  .CircuitBreakerAsync(5, TimeSpan.FromSeconds(30))
        }
    };
    return registry;
}
```

## Query Side with Darker
```csharp
using Paramore.Darker;

// Query and result
public class GetOrderById : IQuery<OrderResult>
{
    public Guid OrderId { get; init; }
}

public class OrderResult
{
    public Guid Id { get; init; }
    public string CustomerId { get; init; } = default!;
    public decimal Total { get; init; }
    public string Status { get; init; } = default!;
}

// Query handler
public class GetOrderByIdHandler : QueryHandlerAsync<GetOrderById, OrderResult>
{
    private readonly IOrderRepository _repository;

    public GetOrderByIdHandler(IOrderRepository repository)
        => _repository = repository;

    public override async Task<OrderResult> ExecuteAsync(
        GetOrderById query,
        CancellationToken ct = default)
    {
        var order = await _repository.GetByIdAsync(query.OrderId, ct);
        return new OrderResult
        {
            Id = order.Id,
            CustomerId = order.CustomerId,
            Total = order.Total,
            Status = order.Status
        };
    }
}

// Registration
builder.Services.AddDarker()
    .AddHandlersFromAssemblies(typeof(GetOrderByIdHandler).Assembly);
```

## Async Messaging with RabbitMQ
```csharp
using Paramore.Brighter.MessagingGateway.RMQ;

builder.Services.AddBrighter(options =>
    {
        options.PolicyRegistry = GetPolicies();
    })
    .UseExternalBus(new RmqProducerRegistryFactory(
        new RmqMessagingGatewayConnection
        {
            AmpqUri = new AmqpUriSpecification(new Uri("amqp://guest:guest@localhost:5672")),
            Exchange = new Exchange("orders.exchange")
        },
        new[]
        {
            new RmqPublication
            {
                Topic = new RoutingKey("order.created"),
                RequestType = typeof(OrderCreated),
                WaitForConfirmsTimeOutInMilliseconds = 1000
            }
        }).Create())
    .AutoFromAssemblies();
```

## Brighter vs MediatR vs MassTransit

| Feature | Brighter | MediatR | MassTransit |
|---------|----------|---------|-------------|
| Command dispatch | Yes (Send) | Yes (Send) | Yes (via consumers) |
| Event publish | Yes (Post/Publish) | Yes (Publish) | Yes (Publish) |
| Policy pipeline | Attribute-based (retry, CB) | Pipeline behaviors | Middleware filters |
| External messaging | RabbitMQ, Azure SB, Kafka | None (in-process) | RabbitMQ, Azure SB, SQS |
| Query support | Via Darker | Yes (IRequest<T>) | No built-in query |
| Outbox pattern | Built-in | Not built-in | Built-in |

## Best Practices
- Use `Command` for operations handled by exactly one handler and `Event` for notifications that may have zero or more subscribers.
- Apply `[UsePolicy]` attributes to handlers for retry and circuit-breaker logic rather than wrapping handler code in try/catch with manual retry loops.
- Call `SendAsync` for commands (single handler expected) and `PublishAsync` for events (fan-out to multiple handlers).
- Register handlers using `AutoFromAssemblies()` for automatic discovery rather than manually wiring each handler to its command type.
- Keep handlers single-purpose; extract shared logic into services injected via the constructor instead of duplicating code across handlers.
- Use the Outbox pattern (`DepositPostAsync` + `ClearOutboxAsync`) when publishing events after a database write to ensure at-least-once delivery without dual-write issues.
- Pair Brighter (command side) with Darker (query side) in CQRS architectures to maintain a clean separation of reads and writes.
- Define policy registries centrally (retry, circuit breaker, timeout) and reference them by name in handler attributes for consistency across the application.
- Use `PostAsync` (internal dispatch) for in-process event fans and `PublishAsync` (external) when events must cross service boundaries via a message broker.
- Test handlers in isolation by mocking `IAmACommandProcessor` and repository dependencies, verifying that commands produce the expected downstream events.
