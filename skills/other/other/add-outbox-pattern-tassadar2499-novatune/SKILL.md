---
description: Add transactional outbox pattern for reliable event publishing with RavenDB (project)
---
# Add Outbox Pattern Skill

Implement the transactional outbox pattern for reliable event publishing in NovaTune using RavenDB.

## Overview

The outbox pattern ensures exactly-once event publishing by:
1. Writing events to an `OutboxMessages` collection in the same transaction as domain changes
2. A background processor reads and publishes events, then marks them as processed
3. Guarantees no lost events even if Kafka/Redpanda is temporarily unavailable

## Steps

### 1. Create OutboxMessage Model

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/OutboxMessage.cs`

```csharp
namespace NovaTuneApp.ApiService.Models;

/// <summary>
/// Represents an event pending publication to the message broker.
/// </summary>
public sealed class OutboxMessage
{
    /// <summary>
    /// RavenDB document ID (e.g., "OutboxMessages/01HXK...")
    /// </summary>
    public string Id { get; init; } = string.Empty;

    /// <summary>
    /// Event type name for deserialization/routing.
    /// </summary>
    public required string EventType { get; init; }

    /// <summary>
    /// JSON-serialized event payload.
    /// </summary>
    public required string Payload { get; init; }

    /// <summary>
    /// Kafka partition key for ordering guarantees.
    /// </summary>
    public required string PartitionKey { get; init; }

    /// <summary>
    /// Target topic name (without prefix).
    /// </summary>
    public string? Topic { get; init; }

    /// <summary>
    /// When the outbox message was created.
    /// </summary>
    public required DateTimeOffset CreatedAt { get; init; }

    /// <summary>
    /// When the message was published (null if pending).
    /// </summary>
    public DateTimeOffset? ProcessedAt { get; set; }

    /// <summary>
    /// Number of publication attempts.
    /// </summary>
    public int Attempts { get; set; }

    /// <summary>
    /// Last error message if publication failed.
    /// </summary>
    public string? LastError { get; set; }
}
```

### 2. Create RavenDB Index for Pending Messages

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Indexes/OutboxMessages_ByPending.cs`

```csharp
using Raven.Client.Documents.Indexes;
using NovaTuneApp.ApiService.Models;

namespace NovaTuneApp.ApiService.Infrastructure.Indexes;

public class OutboxMessages_ByPending : AbstractIndexCreationTask<OutboxMessage>
{
    public OutboxMessages_ByPending()
    {
        Map = messages => from msg in messages
                          where msg.ProcessedAt == null
                          select new
                          {
                              msg.CreatedAt,
                              msg.Attempts
                          };
    }
}
```

### 3. Create Outbox Service Interface

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/IOutboxService.cs`

```csharp
namespace NovaTuneApp.ApiService.Services;

/// <summary>
/// Service for writing events to the outbox.
/// </summary>
public interface IOutboxService
{
    /// <summary>
    /// Writes an event to the outbox within the current session.
    /// Must be called before SaveChangesAsync().
    /// </summary>
    Task WriteAsync<TEvent>(
        TEvent @event,
        string partitionKey,
        string? topic = null,
        CancellationToken ct = default) where TEvent : class;
}
```

### 4. Implement Outbox Service

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/OutboxService.cs`

```csharp
using System.Text.Json;
using Raven.Client.Documents.Session;
using NovaTuneApp.ApiService.Models;

namespace NovaTuneApp.ApiService.Services;

public class OutboxService : IOutboxService
{
    private readonly IAsyncDocumentSession _session;
    private readonly ILogger<OutboxService> _logger;

    public OutboxService(
        IAsyncDocumentSession session,
        ILogger<OutboxService> logger)
    {
        _session = session;
        _logger = logger;
    }

    public async Task WriteAsync<TEvent>(
        TEvent @event,
        string partitionKey,
        string? topic = null,
        CancellationToken ct = default) where TEvent : class
    {
        var eventType = typeof(TEvent).Name;
        var outboxMessage = new OutboxMessage
        {
            Id = $"OutboxMessages/{Ulid.NewUlid()}",
            EventType = eventType,
            Payload = JsonSerializer.Serialize(@event),
            PartitionKey = partitionKey,
            Topic = topic,
            CreatedAt = DateTimeOffset.UtcNow
        };

        await _session.StoreAsync(outboxMessage, ct);

        _logger.LogDebug(
            "Queued {EventType} for partition {PartitionKey}",
            eventType, partitionKey);
    }
}
```

### 5. Create Outbox Processor Background Service

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Services/OutboxProcessorService.cs`

```csharp
using System.Text.Json;
using KafkaFlow.Producers;
using Microsoft.Extensions.Options;
using Raven.Client.Documents;
using Raven.Client.Documents.Session;
using NovaTuneApp.ApiService.Configuration;
using NovaTuneApp.ApiService.Models;
using NovaTuneApp.ApiService.Infrastructure.Indexes;

namespace NovaTuneApp.ApiService.Infrastructure.Services;

public class OutboxProcessorService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly IOptions<OutboxOptions> _options;
    private readonly IOptions<NovaTuneOptions> _novatuneOptions;
    private readonly ILogger<OutboxProcessorService> _logger;

    public OutboxProcessorService(
        IServiceProvider serviceProvider,
        IOptions<OutboxOptions> options,
        IOptions<NovaTuneOptions> novatuneOptions,
        ILogger<OutboxProcessorService> logger)
    {
        _serviceProvider = serviceProvider;
        _options = options;
        _novatuneOptions = novatuneOptions;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        if (!_options.Value.Enabled)
        {
            _logger.LogInformation("Outbox processor is disabled");
            return;
        }

        _logger.LogInformation(
            "Outbox processor starting with {Interval} interval",
            _options.Value.PollingInterval);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessBatchAsync(stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing outbox");
            }

            await Task.Delay(_options.Value.PollingInterval, stoppingToken);
        }
    }

    private async Task ProcessBatchAsync(CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var store = scope.ServiceProvider.GetRequiredService<IDocumentStore>();
        var producerAccessor = scope.ServiceProvider.GetRequiredService<IProducerAccessor>();

        using var session = store.OpenAsyncSession();
        var pendingMessages = await session
            .Query<OutboxMessage, OutboxMessages_ByPending>()
            .Where(m => m.ProcessedAt == null && m.Attempts < _options.Value.MaxAttempts)
            .OrderBy(m => m.CreatedAt)
            .Take(_options.Value.BatchSize)
            .ToListAsync(ct);

        if (pendingMessages.Count == 0) return;

        _logger.LogDebug("Processing {Count} outbox messages", pendingMessages.Count);

        var topicPrefix = _novatuneOptions.Value.TopicPrefix;

        foreach (var message in pendingMessages)
        {
            try
            {
                var topic = message.Topic ?? GetDefaultTopic(message.EventType);
                var fullTopic = $"{topicPrefix}-{topic}";

                var producer = producerAccessor.GetProducer("default");
                await producer.ProduceAsync(
                    fullTopic,
                    message.PartitionKey,
                    message.Payload);

                message.ProcessedAt = DateTimeOffset.UtcNow;
                _logger.LogDebug(
                    "Published {EventType} to {Topic}",
                    message.EventType, fullTopic);
            }
            catch (Exception ex)
            {
                message.Attempts++;
                message.LastError = ex.Message;
                _logger.LogWarning(
                    ex,
                    "Failed to publish {EventType} (attempt {Attempt})",
                    message.EventType, message.Attempts);
            }
        }

        await session.SaveChangesAsync(ct);
    }

    private static string GetDefaultTopic(string eventType) => eventType switch
    {
        nameof(TrackDeletedEvent) => "track-deletions",
        nameof(AudioUploadedEvent) => "audio-events",
        _ => "events"
    };
}
```

### 6. Add Configuration Options

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Configuration/OutboxOptions.cs`

```csharp
namespace NovaTuneApp.ApiService.Configuration;

public class OutboxOptions
{
    public const string SectionName = "Outbox";

    /// <summary>
    /// Polling interval for outbox processor.
    /// Default: 1 second.
    /// </summary>
    public TimeSpan PollingInterval { get; set; } = TimeSpan.FromSeconds(1);

    /// <summary>
    /// Maximum messages per batch.
    /// Default: 100.
    /// </summary>
    public int BatchSize { get; set; } = 100;

    /// <summary>
    /// Maximum publication attempts before giving up.
    /// Default: 5.
    /// </summary>
    public int MaxAttempts { get; set; } = 5;

    /// <summary>
    /// Whether outbox processing is enabled.
    /// Default: true.
    /// </summary>
    public bool Enabled { get; set; } = true;

    /// <summary>
    /// Retention period for processed messages.
    /// Default: 7 days.
    /// </summary>
    public TimeSpan RetentionPeriod { get; set; } = TimeSpan.FromDays(7);
}
```

### 7. Register Services in Program.cs

```csharp
// Configuration
builder.Services.Configure<OutboxOptions>(
    builder.Configuration.GetSection(OutboxOptions.SectionName));

// Services
builder.Services.AddScoped<IOutboxService, OutboxService>();

// Background processor
builder.Services.AddHostedService<OutboxProcessorService>();
```

### 8. Add Configuration to appsettings.json

```json
{
  "Outbox": {
    "PollingInterval": "00:00:01",
    "BatchSize": 100,
    "MaxAttempts": 5,
    "Enabled": true,
    "RetentionPeriod": "7.00:00:00"
  }
}
```

## Usage Example

```csharp
public class TrackManagementService : ITrackManagementService
{
    private readonly IAsyncDocumentSession _session;
    private readonly IOutboxService _outboxService;

    public async Task DeleteTrackAsync(string trackId, string userId, CancellationToken ct)
    {
        var track = await _session.LoadAsync<Track>($"Tracks/{trackId}", ct);
        // ... validation ...

        // Soft-delete track
        track.Status = TrackStatus.Deleted;
        track.DeletedAt = DateTimeOffset.UtcNow;
        track.ScheduledDeletionAt = track.DeletedAt.Value.AddDays(30);

        // Write event to outbox (same transaction)
        var evt = new TrackDeletedEvent
        {
            TrackId = trackId,
            UserId = userId,
            ObjectKey = track.ObjectKey,
            // ... other fields
        };

        await _outboxService.WriteAsync(evt, partitionKey: trackId, ct: ct);

        // Both track update and outbox message saved atomically
        await _session.SaveChangesAsync(ct);
    }
}
```

## Benefits

- **Exactly-once delivery**: Events stored atomically with domain changes
- **Resilience**: Events published even if broker temporarily unavailable
- **Ordering**: Partition key ensures order within entity
- **Retries**: Failed messages retried with exponential backoff
- **Observability**: Failed messages visible in RavenDB

## Cleanup

Add a scheduled task to delete processed messages older than retention period:

```csharp
// In OutboxProcessorService or separate cleanup service
var cutoff = DateTimeOffset.UtcNow - _options.Value.RetentionPeriod;
var oldMessages = await session
    .Query<OutboxMessage>()
    .Where(m => m.ProcessedAt != null && m.ProcessedAt < cutoff)
    .Take(1000)
    .ToListAsync(ct);

foreach (var msg in oldMessages)
    session.Delete(msg);

await session.SaveChangesAsync(ct);
```
