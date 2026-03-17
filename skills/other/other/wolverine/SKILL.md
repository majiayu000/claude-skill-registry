---
name: wolverine
description: |
  Use when building .NET applications with Wolverine for command/event handling, messaging, and HTTP endpoint integration with minimal ceremony.
  USE FOR: command and event handling, messaging with RabbitMQ/Azure Service Bus/Amazon SQS, HTTP endpoint generation, durable outbox, saga orchestration, compound handler pipelines
  DO NOT USE FOR: simple in-process mediator only (use mediatr), actor-based concurrency (use akka-net), heavy enterprise ESB features (use nservicebus)
license: MIT
metadata:
  displayName: "Wolverine"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "Wolverine Official Documentation"
    url: "https://wolverinefx.net/"
  - title: "Wolverine GitHub Repository"
    url: "https://github.com/JasperFx/wolverine"
  - title: "WolverineFx NuGet Package"
    url: "https://www.nuget.org/packages/WolverineFx"
---

# Wolverine

## Overview
Wolverine is a next-generation .NET messaging and command execution framework by Jeremy Miller (creator of Marten and Lamar). It combines in-process command/query handling (like MediatR) with full distributed messaging (like MassTransit) in a single framework. Wolverine uses runtime code generation to produce optimized handlers with minimal allocations, supports durable outbox messaging, saga orchestration, and can generate ASP.NET Core HTTP endpoints directly from message handlers. It integrates tightly with Marten (PostgreSQL document DB / event store) and supports RabbitMQ, Azure Service Bus, and Amazon SQS transports.

## NuGet Packages
- `WolverineFx` -- core framework (commands, events, local queues)
- `WolverineFx.Http` -- ASP.NET Core HTTP endpoint generation
- `WolverineFx.RabbitMQ` -- RabbitMQ transport
- `WolverineFx.AzureServiceBus` -- Azure Service Bus transport
- `WolverineFx.AmazonSqs` -- Amazon SQS transport
- `WolverineFx.Marten` -- Marten (PostgreSQL) integration for persistence and event sourcing
- `WolverineFx.EntityFrameworkCore` -- EF Core outbox integration

## Basic Setup
```csharp
using Wolverine;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseWolverine(opts =>
{
    // Local queuing for in-process messaging
    opts.LocalQueue("important")
        .UseDurableInbox();

    // Optional: configure external transport
    opts.UseRabbitMq(rabbit =>
    {
        rabbit.HostName = "localhost";
    }).AutoProvision();
});

var app = builder.Build();
app.MapWolverineEndpoints(); // generates HTTP endpoints from handlers
app.Run();
```

## Message Handlers (Convention-Based)
```csharp
// Wolverine discovers handlers by convention: static or instance Handle/Consume methods
// No interfaces required!

public static class OrderHandlers
{
    // Command handler - method name "Handle" + message type parameter
    public static async Task<OrderPlaced> Handle(
        PlaceOrder command,
        AppDbContext db,
        ILogger logger)
    {
        logger.LogInformation("Placing order {OrderId}", command.OrderId);

        var order = new Order
        {
            Id = command.OrderId,
            CustomerId = command.CustomerId,
            Total = command.Total,
            Status = OrderStatus.Placed
        };

        db.Orders.Add(order);
        await db.SaveChangesAsync();

        // Returning a message cascades it (publishes as an event)
        return new OrderPlaced(command.OrderId, command.CustomerId, command.Total);
    }
}

// Message contracts
public sealed record PlaceOrder(Guid OrderId, string CustomerId, decimal Total);
public sealed record OrderPlaced(Guid OrderId, string CustomerId, decimal Total);
```

## Cascading Messages
```csharp
// Wolverine cascades return values as outgoing messages automatically

public static class PaymentHandlers
{
    // Returns multiple cascaded messages
    public static (PaymentProcessed, SendReceipt) Handle(
        ProcessPayment command,
        IPaymentGateway gateway)
    {
        var result = gateway.Charge(command.OrderId, command.Amount);

        return (
            new PaymentProcessed(command.OrderId, result.TransactionId),
            new SendReceipt(command.OrderId, result.TransactionId, command.Amount)
        );
    }
}

public sealed record ProcessPayment(Guid OrderId, decimal Amount);
public sealed record PaymentProcessed(Guid OrderId, string TransactionId);
public sealed record SendReceipt(Guid OrderId, string TransactionId, decimal Amount);
```

## HTTP Endpoint Generation
```csharp
using Wolverine.Http;

// Wolverine.Http generates ASP.NET Core endpoints from handler methods

public static class OrderEndpoints
{
    [WolverinePost("/api/orders")]
    public static async Task<(CreationResponse, OrderPlaced)> Create(
        PlaceOrder command,
        AppDbContext db)
    {
        var order = new Order
        {
            Id = command.OrderId,
            CustomerId = command.CustomerId,
            Total = command.Total
        };

        db.Orders.Add(order);
        await db.SaveChangesAsync();

        // CreationResponse returns 201 with Location header
        return (
            new CreationResponse($"/api/orders/{order.Id}"),
            new OrderPlaced(order.Id, order.CustomerId, order.Total)
        );
    }

    [WolverineGet("/api/orders/{id}")]
    public static async Task<OrderDto?> Get(
        Guid id,
        AppDbContext db)
    {
        return await db.Orders
            .AsNoTracking()
            .Where(o => o.Id == id)
            .Select(o => new OrderDto(o.Id, o.CustomerId, o.Total, o.Status.ToString()))
            .FirstOrDefaultAsync();
    }
}

public sealed record OrderDto(Guid Id, string CustomerId, decimal Total, string Status);
```

## Middleware (Before/After methods)
```csharp
// Wolverine supports middleware via Before/After methods on handler classes

public class OrderHandlerMiddleware
{
    // Runs before the handler; returning a problem stops execution
    public static ProblemDetails? Before(PlaceOrder command, AppDbContext db)
    {
        if (command.Total <= 0)
        {
            return new ProblemDetails
            {
                Title = "Invalid order",
                Detail = "Order total must be greater than zero.",
                Status = 400
            };
        }
        return null; // continue to handler
    }

    // Runs after the handler
    public static void After(PlaceOrder command, ILogger logger)
    {
        logger.LogInformation("Completed processing order {OrderId}", command.OrderId);
    }
}
```

## Durable Outbox with Marten
```csharp
using Wolverine;
using Wolverine.Marten;
using Marten;

builder.Host.UseWolverine(opts =>
{
    opts.Services.AddMarten(marten =>
    {
        marten.Connection(builder.Configuration.GetConnectionString("Postgres")!);
        marten.DatabaseSchemaName = "orders";
    }).IntegrateWithWolverine();

    opts.Policies.AutoApplyTransactions(); // automatic outbox
});

// Handler with Marten outbox
public static class MartenOrderHandlers
{
    public static async Task Handle(
        PlaceOrder command,
        IDocumentSession session)
    {
        var order = new Order
        {
            Id = command.OrderId,
            CustomerId = command.CustomerId,
            Total = command.Total
        };

        session.Store(order);

        // Published in the same transaction as the document store
        session.PublishMessage(new OrderPlaced(
            command.OrderId, command.CustomerId, command.Total));

        // SaveChangesAsync is called automatically by Wolverine
    }
}
```

## Saga Orchestration
```csharp
using Wolverine;
using Wolverine.Persistence.Sagas;

public class OrderSaga : Saga
{
    public Guid Id { get; set; }
    public bool Billed { get; set; }
    public bool Shipped { get; set; }

    // Starts the saga
    public static (OrderSaga, ProcessPayment) Start(OrderPlaced @event)
    {
        var saga = new OrderSaga { Id = @event.OrderId };
        var command = new ProcessPayment(@event.OrderId, @event.Total);
        return (saga, command);
    }

    // Continue the saga
    public ShipOrder? Handle(PaymentProcessed @event)
    {
        Billed = true;
        return new ShipOrder(Id);
    }

    public OrderCompleted? Handle(ShipmentConfirmed @event)
    {
        Shipped = true;
        if (Billed && Shipped)
        {
            MarkCompleted();
            return new OrderCompleted(Id);
        }
        return null;
    }
}

public sealed record ShipmentConfirmed(Guid OrderId);
public sealed record OrderCompleted(Guid OrderId);
```

## RabbitMQ Configuration
```csharp
builder.Host.UseWolverine(opts =>
{
    opts.UseRabbitMq(rabbit =>
    {
        rabbit.HostName = "localhost";
        rabbit.UserName = "guest";
        rabbit.Password = "guest";
    })
    .AutoProvision()
    .AutoPurgeOnStartup(); // dev only

    opts.PublishMessage<OrderPlaced>()
        .ToRabbitExchange("orders", exchange =>
        {
            exchange.ExchangeType = ExchangeType.Fanout;
        });

    opts.ListenToRabbitQueue("order-service", queue =>
    {
        queue.PurgeOnStartup = false;
        queue.TimeToLive(TimeSpan.FromHours(1));
    });
});
```

## Wolverine vs MediatR vs MassTransit

| Feature | Wolverine | MediatR | MassTransit |
|---------|-----------|---------|-------------|
| In-process commands | Yes (convention-based) | Yes (interface-based) | No (consumer-based) |
| Distributed messaging | RabbitMQ, Azure SB, SQS | No | RabbitMQ, Azure SB, SQS |
| HTTP endpoints | Built-in generation | No | No |
| Outbox pattern | Built-in (Marten, EF Core) | No | Built-in (EF Core) |
| Handler discovery | Convention (no interfaces) | Interfaces required | Interfaces required |
| Code generation | Runtime (optimized) | None | None |
| Sagas | Built-in | No | Built-in |

## Best Practices
- Use convention-based handlers (static `Handle` or `Consume` methods) rather than implementing interfaces; Wolverine discovers them automatically and generates optimized dispatch code.
- Return messages from handlers to cascade them as outgoing events or commands instead of injecting `IMessageBus` to publish manually.
- Use tuple returns `(Response, Event)` to return both an HTTP response and a cascaded message from a single handler method.
- Enable `AutoApplyTransactions()` with Marten or EF Core to get automatic transactional outbox behavior without manual `SaveChangesAsync` calls.
- Use `WolverinePost`/`WolverineGet` attributes with `MapWolverineEndpoints()` to generate ASP.NET Core endpoints directly from handler methods, reducing boilerplate.
- Leverage Before/After middleware methods for cross-cutting concerns (validation, logging) scoped to specific message types without a global pipeline.
- Use `IntegrateWithWolverine()` on Marten for durable inbox/outbox messaging backed by PostgreSQL, ensuring messages survive process restarts.
- Use Wolverine sagas with `Saga` base class and `Start`/`Handle` methods for orchestrating multi-step workflows with minimal ceremony.
- Configure `UseDurableInbox()` on local queues for messages that must not be lost during application restarts.
- Test handlers as plain methods by calling them directly with mock dependencies; Wolverine handlers are just methods, making them straightforward to unit test.
