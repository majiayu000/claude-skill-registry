---
name: outbox-pattern
description: "Implements the Outbox pattern for reliable domain event processing. Ensures events are persisted in the same transaction as the aggregate changes and processed asynchronously with guaranteed delivery."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Entity Framework Core, Quartz.NET, MediatR
pattern: Transactional Outbox, Guaranteed Delivery
---

# Outbox Pattern Implementation

## Overview

The Outbox pattern ensures reliable event processing:

- **Atomic persistence** - Events saved in same transaction as aggregate
- **Guaranteed delivery** - Events processed even if app crashes
- **Eventual consistency** - Async processing with retry
- **Idempotency** - Handle duplicate processing gracefully

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `OutboxMessage` | Persisted event entity |
| `OutboxMessageConfiguration` | EF Core mapping |
| `ProcessOutboxMessagesJob` | Background processor (Quartz) |
| `IdempotentDomainEventHandler` | Deduplicated handler wrapper |
| `OutboxConsumer` | Alternative direct DB poller |

---

## Outbox Structure

```
/Infrastructure/
├── Outbox/
│   ├── OutboxMessage.cs
│   ├── OutboxMessageConfiguration.cs
│   ├── ProcessOutboxMessagesJob.cs
│   ├── ProcessOutboxMessagesJobSetup.cs
│   └── IdempotentDomainEventHandler.cs
└── ApplicationDbContext.cs
```

---

## Template: Outbox Message Entity

```csharp
// src/{name}.infrastructure/Outbox/OutboxMessage.cs
namespace {name}.infrastructure.outbox;

/// <summary>
/// Represents a domain event stored for reliable delivery
/// </summary>
public sealed class OutboxMessage
{
    public OutboxMessage()
    {
    }

    public OutboxMessage(Guid id, string type, string content, DateTime occurredOnUtc)
    {
        Id = id;
        Type = type;
        Content = content;
        OccurredOnUtc = occurredOnUtc;
    }

    /// <summary>
    /// Unique identifier for this message
    /// </summary>
    public Guid Id { get; set; }

    /// <summary>
    /// Assembly-qualified type name of the domain event
    /// </summary>
    public string Type { get; set; } = string.Empty;

    /// <summary>
    /// JSON-serialized event content
    /// </summary>
    public string Content { get; set; } = string.Empty;

    /// <summary>
    /// When the event originally occurred
    /// </summary>
    public DateTime OccurredOnUtc { get; set; }

    /// <summary>
    /// When the message was successfully processed (null if not yet processed)
    /// </summary>
    public DateTime? ProcessedOnUtc { get; set; }

    /// <summary>
    /// Error message if processing failed
    /// </summary>
    public string? Error { get; set; }

    /// <summary>
    /// Number of processing attempts
    /// </summary>
    public int RetryCount { get; set; }
}
```

---

## Template: EF Core Configuration

```csharp
// src/{name}.infrastructure/Outbox/OutboxMessageConfiguration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace {name}.infrastructure.outbox;

internal sealed class OutboxMessageConfiguration 
    : IEntityTypeConfiguration<OutboxMessage>
{
    public void Configure(EntityTypeBuilder<OutboxMessage> builder)
    {
        builder.ToTable("outbox_message");

        builder.HasKey(o => o.Id);

        builder.Property(o => o.Id)
            .ValueGeneratedNever();

        builder.Property(o => o.Type)
            .HasMaxLength(500)
            .IsRequired();

        builder.Property(o => o.Content)
            .HasColumnType("jsonb")  // PostgreSQL JSONB
            .IsRequired();

        builder.Property(o => o.OccurredOnUtc)
            .IsRequired();

        builder.Property(o => o.ProcessedOnUtc);

        builder.Property(o => o.Error)
            .HasColumnType("text");

        builder.Property(o => o.RetryCount)
            .HasDefaultValue(0);

        // Index for efficient polling of unprocessed messages
        builder.HasIndex(o => o.ProcessedOnUtc)
            .HasFilter("processed_on_utc IS NULL")
            .HasDatabaseName("ix_outbox_message_unprocessed");

        // Index for cleanup of old processed messages
        builder.HasIndex(o => o.ProcessedOnUtc)
            .HasFilter("processed_on_utc IS NOT NULL")
            .HasDatabaseName("ix_outbox_message_processed");
    }
}
```

---

## Template: DbContext Integration

```csharp
// src/{name}.infrastructure/ApplicationDbContext.cs
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using {name}.domain.abstractions;
using {name}.infrastructure.outbox;

namespace {name}.infrastructure;

public sealed class ApplicationDbContext : DbContext, IUnitOfWork
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = false
    };

    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<OutboxMessage> OutboxMessages => Set<OutboxMessage>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // ═══════════════════════════════════════════════════════════════
        // CRITICAL: Add domain events to outbox BEFORE SaveChanges
        // This ensures atomic persistence - events saved in same transaction
        // ═══════════════════════════════════════════════════════════════
        ConvertDomainEventsToOutboxMessages();

        return await base.SaveChangesAsync(cancellationToken);
    }

    private void ConvertDomainEventsToOutboxMessages()
    {
        // Get all entities with domain events
        var entitiesWithEvents = ChangeTracker
            .Entries<Entity>()
            .Where(e => e.Entity.GetDomainEvents().Any())
            .Select(e => e.Entity)
            .ToList();

        // Extract all domain events
        var domainEvents = entitiesWithEvents
            .SelectMany(e => e.GetDomainEvents())
            .ToList();

        // Clear events from entities (they're now in outbox)
        foreach (var entity in entitiesWithEvents)
        {
            entity.ClearDomainEvents();
        }

        // Convert to outbox messages
        foreach (var domainEvent in domainEvents)
        {
            var outboxMessage = new OutboxMessage
            {
                Id = Guid.NewGuid(),
                Type = domainEvent.GetType().AssemblyQualifiedName!,
                Content = JsonSerializer.Serialize(
                    domainEvent,
                    domainEvent.GetType(),
                    JsonOptions),
                OccurredOnUtc = DateTime.UtcNow
            };

            OutboxMessages.Add(outboxMessage);
        }
    }
}
```

---

## Template: Outbox Processor Job (Quartz)

```csharp
// src/{name}.infrastructure/Outbox/ProcessOutboxMessagesJob.cs
using System.Text.Json;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Quartz;
using {name}.domain.abstractions;

namespace {name}.infrastructure.outbox;

/// <summary>
/// Background job that processes outbox messages
/// Uses Quartz for scheduling with configurable interval
/// </summary>
[DisallowConcurrentExecution]  // Prevent parallel execution
public sealed class ProcessOutboxMessagesJob : IJob
{
    private const int BatchSize = 20;
    private const int MaxRetries = 3;

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    private readonly ApplicationDbContext _dbContext;
    private readonly IPublisher _publisher;
    private readonly ILogger<ProcessOutboxMessagesJob> _logger;

    public ProcessOutboxMessagesJob(
        ApplicationDbContext dbContext,
        IPublisher publisher,
        ILogger<ProcessOutboxMessagesJob> logger)
    {
        _dbContext = dbContext;
        _publisher = publisher;
        _logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        _logger.LogDebug("Starting outbox message processing...");

        var messages = await GetUnprocessedMessages(context.CancellationToken);

        if (!messages.Any())
        {
            _logger.LogDebug("No outbox messages to process");
            return;
        }

        _logger.LogInformation(
            "Processing {Count} outbox messages",
            messages.Count);

        foreach (var message in messages)
        {
            await ProcessMessage(message, context.CancellationToken);
        }

        await _dbContext.SaveChangesAsync(context.CancellationToken);

        _logger.LogInformation("Completed outbox message processing");
    }

    private async Task<List<OutboxMessage>> GetUnprocessedMessages(
        CancellationToken cancellationToken)
    {
        return await _dbContext.OutboxMessages
            .Where(m => m.ProcessedOnUtc == null)
            .Where(m => m.RetryCount < MaxRetries)
            .OrderBy(m => m.OccurredOnUtc)
            .Take(BatchSize)
            .ToListAsync(cancellationToken);
    }

    private async Task ProcessMessage(
        OutboxMessage message,
        CancellationToken cancellationToken)
    {
        try
        {
            _logger.LogDebug(
                "Processing outbox message {MessageId} of type {Type}",
                message.Id,
                message.Type);

            // Resolve the event type
            var eventType = Type.GetType(message.Type);

            if (eventType is null)
            {
                _logger.LogError(
                    "Could not resolve type {Type} for message {MessageId}",
                    message.Type,
                    message.Id);

                message.Error = $"Could not resolve type: {message.Type}";
                message.ProcessedOnUtc = DateTime.UtcNow;
                return;
            }

            // Deserialize the event
            var domainEvent = JsonSerializer.Deserialize(
                message.Content,
                eventType,
                JsonOptions) as IDomainEvent;

            if (domainEvent is null)
            {
                _logger.LogError(
                    "Could not deserialize message {MessageId}",
                    message.Id);

                message.Error = "Could not deserialize message content";
                message.ProcessedOnUtc = DateTime.UtcNow;
                return;
            }

            // Publish to MediatR handlers
            await _publisher.Publish(domainEvent, cancellationToken);

            // Mark as processed
            message.ProcessedOnUtc = DateTime.UtcNow;
            message.Error = null;

            _logger.LogInformation(
                "Successfully processed outbox message {MessageId}",
                message.Id);
        }
        catch (Exception ex)
        {
            _logger.LogError(
                ex,
                "Error processing outbox message {MessageId}. Retry count: {RetryCount}",
                message.Id,
                message.RetryCount);

            message.RetryCount++;
            message.Error = ex.ToString();

            // Mark as processed if max retries exceeded
            if (message.RetryCount >= MaxRetries)
            {
                message.ProcessedOnUtc = DateTime.UtcNow;
                
                _logger.LogError(
                    "Outbox message {MessageId} exceeded max retries and has been marked as failed",
                    message.Id);
            }
        }
    }
}
```

---

## Template: Job Configuration

```csharp
// src/{name}.infrastructure/Outbox/ProcessOutboxMessagesJobSetup.cs
using Microsoft.Extensions.Options;
using Quartz;

namespace {name}.infrastructure.outbox;

internal sealed class ProcessOutboxMessagesJobSetup 
    : IConfigureOptions<QuartzOptions>
{
    public void Configure(QuartzOptions options)
    {
        var jobKey = JobKey.Create(nameof(ProcessOutboxMessagesJob));

        options
            .AddJob<ProcessOutboxMessagesJob>(jobBuilder =>
                jobBuilder.WithIdentity(jobKey))
            .AddTrigger(triggerBuilder =>
                triggerBuilder
                    .ForJob(jobKey)
                    .WithSimpleSchedule(schedule =>
                        schedule
                            .WithIntervalInSeconds(10)  // Poll every 10 seconds
                            .RepeatForever()));
    }
}
```

---

## Template: Idempotent Event Handler Wrapper

```csharp
// src/{name}.infrastructure/Outbox/IdempotentDomainEventHandler.cs
using MediatR;
using Microsoft.EntityFrameworkCore;
using {name}.domain.abstractions;

namespace {name}.infrastructure.outbox;

/// <summary>
/// Wrapper that ensures domain events are processed only once
/// Uses a separate tracking table to detect duplicates
/// </summary>
public abstract class IdempotentDomainEventHandler<TEvent> 
    : INotificationHandler<TEvent>
    where TEvent : IDomainEvent
{
    private readonly ApplicationDbContext _dbContext;

    protected IdempotentDomainEventHandler(ApplicationDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task Handle(TEvent notification, CancellationToken cancellationToken)
    {
        var handlerName = GetType().Name;
        var eventId = notification.Id;

        // Check if already processed
        var alreadyProcessed = await _dbContext
            .Set<OutboxMessageConsumer>()
            .AnyAsync(
                c => c.EventId == eventId && c.HandlerName == handlerName,
                cancellationToken);

        if (alreadyProcessed)
        {
            return;  // Skip duplicate processing
        }

        // Process the event
        await HandleAsync(notification, cancellationToken);

        // Mark as processed
        _dbContext.Set<OutboxMessageConsumer>().Add(new OutboxMessageConsumer
        {
            Id = Guid.NewGuid(),
            EventId = eventId,
            HandlerName = handlerName,
            ProcessedOnUtc = DateTime.UtcNow
        });

        await _dbContext.SaveChangesAsync(cancellationToken);
    }

    protected abstract Task HandleAsync(TEvent notification, CancellationToken cancellationToken);
}

/// <summary>
/// Tracks which handlers have processed which events
/// </summary>
public sealed class OutboxMessageConsumer
{
    public Guid Id { get; set; }
    public Guid EventId { get; set; }
    public string HandlerName { get; set; } = string.Empty;
    public DateTime ProcessedOnUtc { get; set; }
}
```

---

## Template: Cleanup Job

```csharp
// src/{name}.infrastructure/Outbox/CleanupOutboxMessagesJob.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Quartz;

namespace {name}.infrastructure.outbox;

/// <summary>
/// Cleans up old processed outbox messages
/// Runs daily to prevent table bloat
/// </summary>
[DisallowConcurrentExecution]
public sealed class CleanupOutboxMessagesJob : IJob
{
    private const int RetentionDays = 7;
    private const int BatchSize = 1000;

    private readonly ApplicationDbContext _dbContext;
    private readonly ILogger<CleanupOutboxMessagesJob> _logger;

    public CleanupOutboxMessagesJob(
        ApplicationDbContext dbContext,
        ILogger<CleanupOutboxMessagesJob> logger)
    {
        _dbContext = dbContext;
        _logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        var cutoffDate = DateTime.UtcNow.AddDays(-RetentionDays);

        _logger.LogInformation(
            "Cleaning up outbox messages processed before {CutoffDate}",
            cutoffDate);

        var totalDeleted = 0;
        int deletedInBatch;

        do
        {
            deletedInBatch = await _dbContext.OutboxMessages
                .Where(m => m.ProcessedOnUtc != null)
                .Where(m => m.ProcessedOnUtc < cutoffDate)
                .Take(BatchSize)
                .ExecuteDeleteAsync(context.CancellationToken);

            totalDeleted += deletedInBatch;

        } while (deletedInBatch == BatchSize);

        _logger.LogInformation(
            "Cleaned up {Count} old outbox messages",
            totalDeleted);
    }
}
```

---

## Template: Registration

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
private static void AddBackgroundJobs(
    IServiceCollection services,
    IConfiguration configuration)
{
    services.AddQuartz(configure =>
    {
        // Use persistent job store for production
        configure.UsePersistentStore(options =>
        {
            options.UsePostgres(configuration.GetConnectionString("Database")!);
            options.UseJsonSerializer();
        });
    });

    services.AddQuartzHostedService(options =>
    {
        options.WaitForJobsToComplete = true;
    });

    // Register job configurations
    services.ConfigureOptions<ProcessOutboxMessagesJobSetup>();
    services.ConfigureOptions<CleanupOutboxMessagesJobSetup>();
}
```

---

## Database Migration

```sql
-- Create outbox_message table
CREATE TABLE outbox_message (
    id UUID PRIMARY KEY,
    type VARCHAR(500) NOT NULL,
    content JSONB NOT NULL,
    occurred_on_utc TIMESTAMP NOT NULL,
    processed_on_utc TIMESTAMP NULL,
    error TEXT NULL,
    retry_count INTEGER NOT NULL DEFAULT 0
);

-- Index for unprocessed messages (most important)
CREATE INDEX ix_outbox_message_unprocessed 
ON outbox_message (occurred_on_utc) 
WHERE processed_on_utc IS NULL;

-- Index for cleanup of old messages
CREATE INDEX ix_outbox_message_processed 
ON outbox_message (processed_on_utc) 
WHERE processed_on_utc IS NOT NULL;

-- Optional: Consumer tracking table for idempotency
CREATE TABLE outbox_message_consumer (
    id UUID PRIMARY KEY,
    event_id UUID NOT NULL,
    handler_name VARCHAR(500) NOT NULL,
    processed_on_utc TIMESTAMP NOT NULL
);

CREATE UNIQUE INDEX ix_outbox_consumer_event_handler 
ON outbox_message_consumer (event_id, handler_name);
```

---

## Critical Rules

1. **Same transaction** - Events saved with aggregate in one transaction
2. **Idempotent handlers** - Must handle duplicate delivery
3. **Order not guaranteed** - Events may process out of order
4. **Retry with backoff** - Don't hammer failing events
5. **Cleanup old messages** - Prevent table bloat
6. **Monitor failures** - Alert on max retries exceeded
7. **Type serialization** - Use `AssemblyQualifiedName` for deserialize
8. **JSON serialization** - Consistent options for serialize/deserialize
9. **Batch processing** - Don't process one at a time
10. **Disable concurrent execution** - Prevent duplicate processing

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Publishing events directly (not reliable)
await _publisher.Publish(new UserCreatedEvent(user.Id));
await _unitOfWork.SaveChangesAsync();  // Event lost if save fails!

// ✅ CORRECT: Events converted to outbox in SaveChanges
user.RaiseDomainEvent(new UserCreatedEvent(user.Id));
await _unitOfWork.SaveChangesAsync();  // Events saved atomically

// ❌ WRONG: Non-idempotent handler
public async Task Handle(UserCreatedEvent e, CancellationToken ct)
{
    await _emailService.SendWelcomeEmail(e.UserId);  // Sent twice on retry!
}

// ✅ CORRECT: Idempotent handler
public async Task Handle(UserCreatedEvent e, CancellationToken ct)
{
    if (await _emailLog.ExistsAsync(e.UserId, "welcome"))
        return;  // Already sent
    
    await _emailService.SendWelcomeEmail(e.UserId);
    await _emailLog.RecordAsync(e.UserId, "welcome");
}

// ❌ WRONG: Processing one message at a time
foreach (var message in allMessages)  // Could be millions!
{
    await ProcessMessage(message);
}

// ✅ CORRECT: Batch with limit
var messages = await _dbContext.OutboxMessages
    .Where(m => m.ProcessedOnUtc == null)
    .Take(20)  // Batch size
    .ToListAsync();
```

---

## Related Skills

- `domain-events-generator` - Domain events that go into outbox
- `quartz-background-jobs` - Background job scheduling
- `dotnet-clean-architecture` - Infrastructure layer setup
