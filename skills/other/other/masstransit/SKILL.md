---
name: masstransit
description: |
  Use when building message-based distributed systems with MassTransit for pub/sub, request/response, sagas, and outbox patterns in .NET.
  USE FOR: distributed messaging, pub/sub consumers, request/response over message brokers, saga orchestration, outbox pattern, RabbitMQ/Azure Service Bus/Amazon SQS integration
  DO NOT USE FOR: in-process mediator without a transport (use mediatr), actor-based concurrency (use akka-net), simple HTTP-based communication (use aspnet-core)
license: MIT
metadata:
  displayName: "MassTransit"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "MassTransit Official Documentation"
    url: "https://masstransit.io/"
  - title: "MassTransit GitHub Repository"
    url: "https://github.com/MassTransit/MassTransit"
  - title: "MassTransit NuGet Package"
    url: "https://www.nuget.org/packages/MassTransit"
---

# MassTransit

## Overview
MassTransit is a mature, open-source distributed application framework for .NET that provides a consistent abstraction over message transports (RabbitMQ, Azure Service Bus, Amazon SQS, ActiveMQ, and in-memory). It handles message routing, serialization, consumer lifecycle, retry policies, saga state machines, and transactional outbox patterns. MassTransit integrates natively with Microsoft.Extensions.DependencyInjection and ASP.NET Core.

## NuGet Packages
- `MassTransit` -- core library with in-memory transport
- `MassTransit.RabbitMQ` -- RabbitMQ transport
- `MassTransit.Azure.ServiceBus.Core` -- Azure Service Bus transport
- `MassTransit.AmazonSQS` -- Amazon SQS/SNS transport
- `MassTransit.EntityFrameworkCore` -- EF Core saga persistence and outbox
- `MassTransit.MongoDb` -- MongoDB saga persistence

## Basic Setup
```csharp
using MassTransit;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddMassTransit(cfg =>
{
    cfg.AddConsumer<OrderSubmittedConsumer>();
    cfg.AddConsumer<OrderShippedConsumer>();

    cfg.UsingRabbitMq((context, bus) =>
    {
        bus.Host("localhost", "/", h =>
        {
            h.Username("guest");
            h.Password("guest");
        });

        bus.ConfigureEndpoints(context);
    });
});

var app = builder.Build();
app.Run();
```

## Message Contracts
```csharp
// Events (past tense, things that happened)
public record OrderSubmitted(Guid OrderId, string CustomerId, decimal Total);
public record OrderShipped(Guid OrderId, string TrackingNumber);

// Commands (imperative, actions to perform)
public record ProcessPayment(Guid OrderId, decimal Amount);
public record SendNotification(string UserId, string Message);
```

## Consumers
```csharp
using MassTransit;

public class OrderSubmittedConsumer : IConsumer<OrderSubmitted>
{
    private readonly IOrderRepository _repository;
    private readonly ILogger<OrderSubmittedConsumer> _logger;

    public OrderSubmittedConsumer(IOrderRepository repository,
        ILogger<OrderSubmittedConsumer> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task Consume(ConsumeContext<OrderSubmitted> context)
    {
        var message = context.Message;
        _logger.LogInformation("Processing order {OrderId} for {CustomerId}",
            message.OrderId, message.CustomerId);

        await _repository.CreateAsync(new Order
        {
            Id = message.OrderId,
            CustomerId = message.CustomerId,
            Total = message.Total,
            Status = "Received"
        });

        // Publish a follow-up event
        await context.Publish(new ProcessPayment(message.OrderId, message.Total));
    }
}
```

## Publishing and Sending
```csharp
// Publishing events (fan-out to all subscribers)
app.MapPost("/orders", async (OrderRequest request, IPublishEndpoint publisher) =>
{
    var orderId = Guid.NewGuid();
    await publisher.Publish(new OrderSubmitted(orderId, request.CustomerId, request.Total));
    return Results.Accepted($"/orders/{orderId}", new { orderId });
});

// Sending commands (point-to-point to specific endpoint)
app.MapPost("/orders/{id}/ship", async (Guid id, ISendEndpointProvider sender) =>
{
    var endpoint = await sender.GetSendEndpoint(
        new Uri("queue:shipping-service"));
    await endpoint.Send(new ShipOrder(id));
    return Results.Accepted();
});
```

## Request/Response
```csharp
// Request and response contracts
public record CheckInventory(string ProductId, int Quantity);
public record InventoryResult(bool Available, int CurrentStock);

// Consumer as responder
public class CheckInventoryConsumer : IConsumer<CheckInventory>
{
    private readonly IInventoryService _inventory;

    public CheckInventoryConsumer(IInventoryService inventory)
        => _inventory = inventory;

    public async Task Consume(ConsumeContext<CheckInventory> context)
    {
        var stock = await _inventory.GetStockAsync(context.Message.ProductId);
        await context.RespondAsync(new InventoryResult(
            stock >= context.Message.Quantity, stock));
    }
}

// Client requesting
app.MapGet("/inventory/{productId}", async (string productId,
    IRequestClient<CheckInventory> client) =>
{
    var response = await client.GetResponse<InventoryResult>(
        new CheckInventory(productId, 1));
    return Results.Ok(response.Message);
});
```

## Consumer Configuration (Retry, Concurrency)
```csharp
builder.Services.AddMassTransit(cfg =>
{
    cfg.AddConsumer<OrderSubmittedConsumer>(consumerCfg =>
    {
        consumerCfg.UseMessageRetry(r => r.Exponential(
            retryLimit: 5,
            minInterval: TimeSpan.FromMilliseconds(200),
            maxInterval: TimeSpan.FromSeconds(30),
            intervalDelta: TimeSpan.FromMilliseconds(500)));

        consumerCfg.UseConcurrencyLimit(10);
    });

    cfg.UsingRabbitMq((context, bus) =>
    {
        bus.PrefetchCount = 32;
        bus.ConfigureEndpoints(context);
    });
});
```

## Transactional Outbox
```csharp
using MassTransit;
using Microsoft.EntityFrameworkCore;

builder.Services.AddDbContext<AppDbContext>(opts =>
    opts.UseSqlServer(builder.Configuration.GetConnectionString("Default")));

builder.Services.AddMassTransit(cfg =>
{
    cfg.AddConsumer<OrderSubmittedConsumer>();

    cfg.AddEntityFrameworkOutbox<AppDbContext>(o =>
    {
        o.UseSqlServer();
        o.UseBusOutbox();      // enables transactional outbox
        o.QueryDelay = TimeSpan.FromSeconds(1);
    });

    cfg.UsingRabbitMq((context, bus) =>
    {
        bus.ConfigureEndpoints(context);
    });
});
```

## Saga State Machine
```csharp
using MassTransit;

public class OrderState : SagaStateMachineInstance
{
    public Guid CorrelationId { get; set; }
    public string CurrentState { get; set; } = default!;
    public string CustomerId { get; set; } = default!;
    public decimal Total { get; set; }
}

public class OrderSaga : MassTransitStateMachine<OrderState>
{
    public OrderSaga()
    {
        InstanceState(x => x.CurrentState);

        Event(() => Submitted, x => x.CorrelateById(ctx => ctx.Message.OrderId));
        Event(() => PaymentDone, x => x.CorrelateById(ctx => ctx.Message.OrderId));

        Initially(
            When(Submitted)
                .Then(ctx =>
                {
                    ctx.Saga.CustomerId = ctx.Message.CustomerId;
                    ctx.Saga.Total = ctx.Message.Total;
                })
                .Publish(ctx => new ProcessPayment(ctx.Saga.CorrelationId, ctx.Saga.Total))
                .TransitionTo(AwaitingPayment));

        During(AwaitingPayment,
            When(PaymentDone)
                .TransitionTo(Paid)
                .Finalize());

        SetCompletedWhenFinalized();
    }

    public State AwaitingPayment { get; private set; } = default!;
    public State Paid { get; private set; } = default!;

    public Event<OrderSubmitted> Submitted { get; private set; } = default!;
    public Event<PaymentProcessed> PaymentDone { get; private set; } = default!;
}

public record PaymentProcessed(Guid OrderId, string TransactionId);
```

## Transport Comparison

| Transport | Package | Use Case |
|-----------|---------|----------|
| In-Memory | `MassTransit` | Testing, single-process development |
| RabbitMQ | `MassTransit.RabbitMQ` | On-premises, high-throughput messaging |
| Azure Service Bus | `MassTransit.Azure.ServiceBus.Core` | Azure-native cloud messaging |
| Amazon SQS/SNS | `MassTransit.AmazonSQS` | AWS-native cloud messaging |
| ActiveMQ | `MassTransit.ActiveMQ` | Legacy or JMS-compatible environments |

## Testing
```csharp
using MassTransit.Testing;
using Microsoft.Extensions.DependencyInjection;

[Fact]
public async Task Should_consume_order_submitted()
{
    await using var provider = new ServiceCollection()
        .AddMassTransitTestHarness(cfg =>
        {
            cfg.AddConsumer<OrderSubmittedConsumer>();
        })
        .BuildServiceProvider(true);

    var harness = provider.GetRequiredService<ITestHarness>();
    await harness.Start();

    await harness.Bus.Publish(new OrderSubmitted(Guid.NewGuid(), "cust-1", 50m));

    Assert.True(await harness.Consumed.Any<OrderSubmitted>());

    var consumerHarness = harness.GetConsumerHarness<OrderSubmittedConsumer>();
    Assert.True(await consumerHarness.Consumed.Any<OrderSubmitted>());
}
```

## Best Practices
- Use `Publish` for events (fan-out to all interested consumers) and `Send` for commands (point-to-point to a specific queue) to maintain clear messaging semantics.
- Enable the transactional outbox (`AddEntityFrameworkOutbox` + `UseBusOutbox`) to guarantee at-least-once delivery of messages published within a database transaction.
- Design consumers to be idempotent so that retried or redelivered messages produce the same result without side effects.
- Use `ITestHarness` from `MassTransit.Testing` for integration tests rather than mocking `IPublishEndpoint` or `IBus` directly.
- Configure message retry with exponential backoff on consumers to handle transient failures without overwhelming downstream services.
- Keep message contracts in a shared contract assembly referenced by both producer and consumer projects; avoid sharing implementation code.
- Use saga state machines for long-running workflows spanning multiple messages rather than trying to coordinate state across independent consumers.
- Set `PrefetchCount` and concurrency limits per consumer based on workload characteristics to avoid overwhelming databases or downstream APIs.
- Prefer the in-memory transport for local development and unit tests; switch to a real broker (RabbitMQ, Azure SB) via configuration for staging and production.
- Always call `ConfigureEndpoints(context)` on the bus configuration to let MassTransit automatically wire consumer endpoints using conventions.
