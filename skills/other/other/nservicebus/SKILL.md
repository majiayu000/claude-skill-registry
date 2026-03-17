---
name: nservicebus
description: |
  Use when building enterprise-grade distributed systems with NServiceBus for reliable messaging, sagas, and recoverability in .NET.
  USE FOR: enterprise messaging, durable message handling, saga orchestration, message routing, recoverability and error queues, long-running business processes
  DO NOT USE FOR: simple in-process mediator (use mediatr), lightweight open-source bus (use masstransit or rebus), actor-model concurrency (use akka-net)
license: MIT
metadata:
  displayName: "NServiceBus"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "NServiceBus Official Documentation"
    url: "https://docs.particular.net/nservicebus/"
  - title: "NServiceBus GitHub Repository"
    url: "https://github.com/Particular/NServiceBus"
  - title: "NServiceBus NuGet Package"
    url: "https://www.nuget.org/packages/NServiceBus"
---

# NServiceBus

## Overview
NServiceBus is a commercial enterprise service bus for .NET by Particular Software. It provides reliable messaging with automatic retries, error queues, sagas for long-running workflows, message routing, and built-in monitoring via the Particular Platform (ServicePulse, ServiceInsight, ServiceControl). NServiceBus abstracts over multiple transports (RabbitMQ, Azure Service Bus, Amazon SQS, MSMQ, SQL Server) and supports various persistence stores for saga and outbox state.

## NuGet Packages
- `NServiceBus` -- core library
- `NServiceBus.Extensions.Hosting` -- Generic Host integration
- `NServiceBus.RabbitMQ` -- RabbitMQ transport
- `NServiceBus.Transport.AzureServiceBus` -- Azure Service Bus transport
- `NServiceBus.AmazonSQS` -- Amazon SQS transport
- `NServiceBus.Persistence.Sql` -- SQL persistence for sagas and outbox
- `NServiceBus.NHibernate` -- NHibernate persistence
- `NServiceBus.Testing` -- unit testing utilities

## Endpoint Configuration
```csharp
using NServiceBus;

var builder = Host.CreateApplicationBuilder(args);

var endpointConfiguration = new EndpointConfiguration("Sales");

// Transport
var transport = endpointConfiguration.UseTransport<RabbitMQTransport>();
transport.ConnectionString("host=localhost");
transport.UseConventionalRoutingTopology(QueueType.Quorum);

// Persistence
var persistence = endpointConfiguration.UsePersistence<SqlPersistence>();
persistence.ConnectionBuilder(() =>
    new SqlConnection(builder.Configuration.GetConnectionString("NServiceBus")));
persistence.SqlDialect<SqlDialect.MsSqlServer>();

// Serialization
endpointConfiguration.UseSerialization<SystemJsonSerializer>();

// Recoverability
endpointConfiguration.Recoverability()
    .Immediate(i => i.NumberOfRetries(3))
    .Delayed(d => d.NumberOfRetries(2).TimeIncrease(TimeSpan.FromSeconds(30)));

endpointConfiguration.EnableInstallers();
endpointConfiguration.AuditProcessedMessagesTo("audit");
endpointConfiguration.SendFailedMessagesTo("error");

builder.UseNServiceBus(endpointConfiguration);

var app = builder.Build();
app.Run();
```

## Message Contracts
```csharp
using NServiceBus;

// Commands (sent to a specific endpoint)
public class PlaceOrder : ICommand
{
    public Guid OrderId { get; set; }
    public string CustomerId { get; set; } = default!;
    public decimal Total { get; set; }
}

// Events (published to all subscribers)
public class OrderPlaced : IEvent
{
    public Guid OrderId { get; set; }
    public string CustomerId { get; set; } = default!;
    public decimal Total { get; set; }
    public DateTime PlacedAt { get; set; }
}

public class OrderBilled : IEvent
{
    public Guid OrderId { get; set; }
    public decimal Amount { get; set; }
}

// Messages (neither command nor event)
public class CancelOrder : IMessage
{
    public Guid OrderId { get; set; }
    public string Reason { get; set; } = default!;
}
```

## Message Handlers
```csharp
using NServiceBus;

public class PlaceOrderHandler : IHandleMessages<PlaceOrder>
{
    private readonly IOrderRepository _repository;
    private readonly ILogger<PlaceOrderHandler> _logger;

    public PlaceOrderHandler(IOrderRepository repository,
        ILogger<PlaceOrderHandler> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task Handle(PlaceOrder message, IMessageHandlerContext context)
    {
        _logger.LogInformation("Placing order {OrderId}", message.OrderId);

        await _repository.CreateAsync(new Order
        {
            Id = message.OrderId,
            CustomerId = message.CustomerId,
            Total = message.Total
        });

        // Publish event
        await context.Publish(new OrderPlaced
        {
            OrderId = message.OrderId,
            CustomerId = message.CustomerId,
            Total = message.Total,
            PlacedAt = DateTime.UtcNow
        });
    }
}

// Event handler in a different endpoint
public class OrderPlacedHandler : IHandleMessages<OrderPlaced>
{
    public async Task Handle(OrderPlaced message, IMessageHandlerContext context)
    {
        // Send a command to the billing endpoint
        await context.Send(new BillOrder
        {
            OrderId = message.OrderId,
            Amount = message.Total
        });
    }
}
```

## Message Routing
```csharp
var transport = endpointConfiguration.UseTransport<RabbitMQTransport>();
transport.ConnectionString("host=localhost");

var routing = transport.Routing();

// Route commands to specific endpoints
routing.RouteToEndpoint(typeof(PlaceOrder), "Sales");
routing.RouteToEndpoint(typeof(BillOrder), "Billing");
routing.RouteToEndpoint(typeof(ShipOrder), "Shipping");

// Alternatively, route by assembly or namespace
routing.RouteToEndpoint(typeof(PlaceOrder).Assembly, "Sales");
```

## Sagas
```csharp
using NServiceBus;

public class OrderSagaData : ContainSagaData
{
    public Guid OrderId { get; set; }
    public bool Billed { get; set; }
    public bool Shipped { get; set; }
}

public class OrderSaga : Saga<OrderSagaData>,
    IAmStartedByMessages<OrderPlaced>,
    IHandleMessages<OrderBilled>,
    IHandleMessages<OrderShipped>,
    IHandleTimeouts<OrderTimeout>
{
    protected override void ConfigureHowToFindSaga(SagaPropertyMapper<OrderSagaData> mapper)
    {
        mapper.MapSaga(saga => saga.OrderId)
            .ToMessage<OrderPlaced>(msg => msg.OrderId)
            .ToMessage<OrderBilled>(msg => msg.OrderId)
            .ToMessage<OrderShipped>(msg => msg.OrderId);
    }

    public async Task Handle(OrderPlaced message, IMessageHandlerContext context)
    {
        Data.OrderId = message.OrderId;

        await RequestTimeout<OrderTimeout>(context, TimeSpan.FromDays(7));
        await context.Send(new BillOrder { OrderId = message.OrderId, Amount = message.Total });
    }

    public async Task Handle(OrderBilled message, IMessageHandlerContext context)
    {
        Data.Billed = true;
        await CheckCompletion(context);
    }

    public async Task Handle(OrderShipped message, IMessageHandlerContext context)
    {
        Data.Shipped = true;
        await CheckCompletion(context);
    }

    public async Task Timeout(OrderTimeout state, IMessageHandlerContext context)
    {
        if (!Data.Billed || !Data.Shipped)
        {
            await context.Publish(new OrderTimedOut { OrderId = Data.OrderId });
            MarkAsComplete();
        }
    }

    private async Task CheckCompletion(IMessageHandlerContext context)
    {
        if (Data.Billed && Data.Shipped)
        {
            await context.Publish(new OrderCompleted { OrderId = Data.OrderId });
            MarkAsComplete();
        }
    }
}

public class OrderTimeout { }
public class OrderTimedOut { public Guid OrderId { get; set; } }
public class OrderCompleted { public Guid OrderId { get; set; } }
public class BillOrder : ICommand { public Guid OrderId { get; set; } public decimal Amount { get; set; } }
public class ShipOrder : ICommand { public Guid OrderId { get; set; } }
public class OrderShipped : IEvent { public Guid OrderId { get; set; } }
```

## Outbox
```csharp
var endpointConfiguration = new EndpointConfiguration("Sales");

// Enable outbox for exactly-once message processing
endpointConfiguration.EnableOutbox();

var persistence = endpointConfiguration.UsePersistence<SqlPersistence>();
persistence.ConnectionBuilder(() =>
    new SqlConnection(connectionString));
```

## Testing Handlers
```csharp
using NServiceBus.Testing;

[Fact]
public async Task PlaceOrder_should_publish_OrderPlaced()
{
    var handler = new PlaceOrderHandler(
        new FakeOrderRepository(),
        NullLogger<PlaceOrderHandler>.Instance);

    var context = new TestableMessageHandlerContext();

    await handler.Handle(new PlaceOrder
    {
        OrderId = Guid.NewGuid(),
        CustomerId = "cust-1",
        Total = 100m
    }, context);

    Assert.Single(context.PublishedMessages);
    var published = context.PublishedMessages[0].Message as OrderPlaced;
    Assert.NotNull(published);
    Assert.Equal("cust-1", published.CustomerId);
}
```

## Transport Comparison

| Transport | Deployment | Strengths |
|-----------|------------|-----------|
| RabbitMQ | Self-hosted or cloud | High throughput, flexible routing |
| Azure Service Bus | Azure PaaS | Managed, sessions, dead-lettering |
| Amazon SQS/SNS | AWS PaaS | Managed, auto-scaling |
| SQL Server | On-premises | No extra infra, uses existing DB |
| Learning Transport | Local dev | File-based, zero-config for development |

## Best Practices
- Use `ICommand` for point-to-point messages sent to a specific endpoint and `IEvent` for pub/sub messages consumed by multiple subscribers.
- Configure explicit routing for all commands (`RouteToEndpoint`) so the sender does not need to know endpoint addresses at runtime.
- Enable the Outbox on endpoints that write to a database and publish messages to guarantee exactly-once message processing semantics.
- Use sagas for coordinating multi-step business processes; map saga properties with `ConfigureHowToFindSaga` so NServiceBus can correlate messages to the correct saga instance.
- Configure recoverability with immediate retries (for transient errors) and delayed retries (for infrastructure recovery) before messages move to the error queue.
- Use `SendFailedMessagesTo("error")` and `AuditProcessedMessagesTo("audit")` for observability; deploy ServiceControl to monitor and replay failed messages.
- Keep message contracts in a shared assembly with no dependencies beyond `NServiceBus`; avoid leaking implementation types into contracts.
- Use `RequestTimeout` in sagas for time-based business rules (e.g., cancel unpaid orders after 7 days) instead of external scheduling systems.
- Test handlers using `TestableMessageHandlerContext` from `NServiceBus.Testing` to assert published events, sent commands, and replied messages without a real transport.
- Call `MarkAsComplete()` in sagas when the workflow is finished to release persistence resources and prevent saga state from growing indefinitely.
