---
description: Add KafkaFlow consumer handlers for processing Kafka/Redpanda messages (project)
---
# Add Kafka Consumer Skill

Add KafkaFlow consumer handlers for processing Kafka/Redpanda messages in NovaTune.

## Project Context

- Handlers location: `src/NovaTuneApp/NovaTuneApp.Workers.{Name}/Handlers/`
- Message types: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Messaging/Messages/`
- Topic naming: `{prefix}-{topic-name}` (e.g., `dev-track-deletions`)

## Steps

### 1. Create Message Type (if needed)

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Messaging/Messages/{EventName}.cs`

```csharp
namespace NovaTuneApp.ApiService.Infrastructure.Messaging.Messages;

/// <summary>
/// Event published when a track is soft-deleted.
/// </summary>
public record TrackDeletedEvent
{
    public int SchemaVersion { get; init; } = 2;
    public required string TrackId { get; init; }
    public required string UserId { get; init; }
    public required string ObjectKey { get; init; }
    public string? WaveformObjectKey { get; init; }
    public required long FileSizeBytes { get; init; }
    public required DateTimeOffset DeletedAt { get; init; }
    public required DateTimeOffset ScheduledDeletionAt { get; init; }
    public required string CorrelationId { get; init; }
    public required DateTimeOffset Timestamp { get; init; }
}
```

### 2. Create Handler Class

Location: `src/NovaTuneApp/NovaTuneApp.Workers.{Name}/Handlers/{EventName}Handler.cs`

```csharp
using KafkaFlow;
using NovaTuneApp.ApiService.Infrastructure.Messaging.Messages;

namespace NovaTuneApp.Workers.Lifecycle.Handlers;

/// <summary>
/// Handles TrackDeletedEvent messages for immediate cache invalidation.
/// </summary>
public class TrackDeletedHandler : IMessageHandler<TrackDeletedEvent>
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<TrackDeletedHandler> _logger;

    public TrackDeletedHandler(
        IServiceProvider serviceProvider,
        ILogger<TrackDeletedHandler> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    public async Task Handle(IMessageContext context, TrackDeletedEvent message)
    {
        using var scope = _serviceProvider.CreateScope();

        _logger.LogInformation(
            "Processing TrackDeletedEvent for track {TrackId}, user {UserId}",
            message.TrackId,
            message.UserId);

        try
        {
            // Get services from scoped container
            var cacheService = scope.ServiceProvider.GetRequiredService<ICacheService>();

            // Perform idempotent operations
            await cacheService.InvalidateTrackCacheAsync(
                message.TrackId,
                message.UserId,
                context.ConsumerContext.WorkerStopped);

            _logger.LogDebug(
                "Successfully processed TrackDeletedEvent for {TrackId}, scheduled deletion at {ScheduledAt}",
                message.TrackId,
                message.ScheduledDeletionAt);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to process TrackDeletedEvent for track {TrackId}",
                message.TrackId);

            // Re-throw to trigger retry/DLQ behavior
            throw;
        }
    }
}
```

### 3. Register Consumer in Program.cs

```csharp
var topicPrefix = builder.Configuration["NovaTune:TopicPrefix"] ?? "dev";
var bootstrapServers = builder.Configuration.GetConnectionString("messaging")
    ?? "localhost:9092";

builder.Services.AddKafka(kafka => kafka
    .UseMicrosoftLog()
    .AddCluster(cluster =>
    {
        cluster.WithBrokers([bootstrapServers]);

        // Register consumer for track deletions
        cluster.AddConsumer(consumer => consumer
            .Topic($"{topicPrefix}-track-deletions")
            .WithGroupId($"{topicPrefix}-lifecycle-worker")
            .WithBufferSize(100)
            .WithWorkersCount(2)
            .WithAutoOffsetReset(KafkaFlow.AutoOffsetReset.Earliest)
            .WithConsumerConfig(new ConsumerConfig
            {
                SessionTimeoutMs = 45000,
                SocketTimeoutMs = 30000,
                ReconnectBackoffMs = 1000
            })
            .AddMiddlewares(m => m
                .AddDeserializer<JsonCoreDeserializer>()
                .AddTypedHandlers(h => h.AddHandler<TrackDeletedHandler>())
            )
        );
    })
);

// Register handler in DI
builder.Services.AddTransient<TrackDeletedHandler>();
```

### 4. Add KafkaFlow Hosted Service

```csharp
builder.Services.AddHostedService<KafkaFlowHostedService>();
```

The hosted service manages the KafkaFlow bus lifecycle:

```csharp
internal class KafkaFlowHostedService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<KafkaFlowHostedService> _logger;
    private IKafkaBus? _kafkaBus;

    private const int MaxRetries = 30;
    private static readonly TimeSpan RetryDelay = TimeSpan.FromSeconds(2);

    public KafkaFlowHostedService(
        IServiceProvider serviceProvider,
        ILogger<KafkaFlowHostedService> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Starting KafkaFlow bus...");
        await Task.Delay(TimeSpan.FromSeconds(2), stoppingToken);

        for (var attempt = 1; attempt <= MaxRetries; attempt++)
        {
            try
            {
                _kafkaBus = _serviceProvider.CreateKafkaBus();
                await _kafkaBus.StartAsync(stoppingToken);
                _logger.LogInformation("KafkaFlow bus started on attempt {Attempt}", attempt);

                await Task.Delay(Timeout.Infinite, stoppingToken);
                return;
            }
            catch (OperationCanceledException)
            {
                _logger.LogInformation("KafkaFlow bus stopping due to cancellation");
                return;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex,
                    "Failed to start KafkaFlow bus (attempt {Attempt}/{Max})",
                    attempt, MaxRetries);

                if (attempt < MaxRetries)
                    await Task.Delay(RetryDelay, stoppingToken);
                else
                    _logger.LogError(ex, "Failed after {Max} attempts", MaxRetries);
            }
        }
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        if (_kafkaBus is not null)
        {
            _logger.LogInformation("Stopping KafkaFlow bus...");
            await _kafkaBus.StopAsync();
        }
        await base.StopAsync(cancellationToken);
    }
}
```

## Consumer Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `WithBufferSize` | Internal message buffer size | 100 |
| `WithWorkersCount` | Parallel message processors | 1-4 |
| `WithAutoOffsetReset` | Starting position for new consumers | `Earliest` |
| `SessionTimeoutMs` | Consumer session timeout | 45000 |
| `SocketTimeoutMs` | Socket timeout | 30000 |

## Handler Patterns

### Simple Handler

```csharp
public class SimpleHandler : IMessageHandler<MyEvent>
{
    public Task Handle(IMessageContext context, MyEvent message)
    {
        // Process message
        return Task.CompletedTask;
    }
}
```

### Handler with Scoped Services

```csharp
public class ScopedHandler : IMessageHandler<MyEvent>
{
    private readonly IServiceProvider _serviceProvider;

    public ScopedHandler(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task Handle(IMessageContext context, MyEvent message)
    {
        using var scope = _serviceProvider.CreateScope();
        var dbSession = scope.ServiceProvider.GetRequiredService<IAsyncDocumentSession>();

        // Use scoped services
        await dbSession.SaveChangesAsync(context.ConsumerContext.WorkerStopped);
    }
}
```

### Handler with Retry/DLQ

```csharp
public async Task Handle(IMessageContext context, MyEvent message)
{
    try
    {
        // Process message
    }
    catch (TransientException ex)
    {
        // Will be retried based on consumer config
        throw;
    }
    catch (PermanentException ex)
    {
        // Log and swallow - don't retry
        _logger.LogError(ex, "Permanent failure for message");
    }
}
```

## Best Practices

1. **Make handlers idempotent** - Messages may be delivered more than once
2. **Use scoped services** - Create scope for each message
3. **Handle cancellation** - Use `context.ConsumerContext.WorkerStopped`
4. **Log appropriately** - Info for processing, Debug for success, Error for failures
5. **Re-throw for retries** - Only swallow permanent failures
6. **Keep handlers focused** - One handler per message type

## Testing

```csharp
[Fact]
public async Task Handler_Should_InvalidateCache_OnTrackDeleted()
{
    // Arrange
    var cacheService = Substitute.For<ICacheService>();
    var serviceProvider = BuildServiceProvider(cacheService);
    var handler = new TrackDeletedHandler(serviceProvider, _logger);

    var message = new TrackDeletedEvent
    {
        TrackId = "01HXK...",
        UserId = "user123",
        ObjectKey = "tracks/01HXK...",
        FileSizeBytes = 1024,
        DeletedAt = DateTimeOffset.UtcNow,
        ScheduledDeletionAt = DateTimeOffset.UtcNow.AddDays(30),
        CorrelationId = Guid.NewGuid().ToString(),
        Timestamp = DateTimeOffset.UtcNow
    };

    // Act
    await handler.Handle(_mockContext, message);

    // Assert
    await cacheService.Received(1)
        .InvalidateTrackCacheAsync(message.TrackId, message.UserId, Arg.Any<CancellationToken>());
}
```

## Topic Naming Convention

| Topic | Purpose | Producer | Consumer |
|-------|---------|----------|----------|
| `{prefix}-audio-events` | Audio upload notifications | Upload flow | Audio processor |
| `{prefix}-track-deletions` | Track deletion events | API service | Lifecycle worker |
| `{prefix}-minio-events` | MinIO bucket events | MinIO | Upload ingestor |
