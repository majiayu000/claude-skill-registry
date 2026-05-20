---
name: domain-events-generator
description: "Generates Domain Events and their handlers following DDD patterns. Implements event raising in entities, MediatR notification handlers, and the Outbox pattern for reliable event processing."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: MediatR
pattern: Domain-Driven Design, Event Sourcing
---

# Domain Events Generator

## Overview

Domain Events capture something significant that happened in the domain:

- **Raised by entities** - When state changes occur
- **Handled by notification handlers** - React to events
- **Outbox pattern** - Reliable event delivery
- **Decoupled** - Publisher doesn't know subscribers

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| `IDomainEvent` | Marker interface | Domain/Abstractions |
| `{Entity}{Action}DomainEvent` | Event record | Domain/{Aggregate}/Events |
| `{Event}DomainEventHandler` | Event handler | Application/{Feature} |
| `OutboxMessage` | Persisted event | Infrastructure/Outbox |

---

## Event Structure

```
/Domain/
├── Abstractions/
│   └── IDomainEvent.cs
└── {Aggregate}/
    └── Events/
        ├── {Entity}CreatedDomainEvent.cs
        ├── {Entity}UpdatedDomainEvent.cs
        └── ...

/Application/
└── {Feature}/
    └── EventHandlers/
        ├── {Event}Handler.cs
        └── ...

/Infrastructure/
└── Outbox/
    ├── OutboxMessage.cs
    ├── OutboxMessageConfiguration.cs
    └── ProcessOutboxMessagesJob.cs
```

---

## Template: Domain Event Interface

```csharp
// src/{name}.domain/Abstractions/IDomainEvent.cs
using MediatR;

namespace {name}.domain.abstractions;

/// <summary>
/// Marker interface for domain events.
/// Domain events represent something significant that happened in the domain.
/// </summary>
public interface IDomainEvent : INotification
{
    /// <summary>
    /// Unique identifier for this event instance
    /// </summary>
    Guid Id { get; }

    /// <summary>
    /// When the event occurred
    /// </summary>
    DateTime OccurredOnUtc { get; }
}
```

---

## Template: Base Domain Event Record

```csharp
// src/{name}.domain/Abstractions/DomainEvent.cs
namespace {name}.domain.abstractions;

/// <summary>
/// Base record for domain events with common properties
/// </summary>
public abstract record DomainEvent : IDomainEvent
{
    public Guid Id { get; init; } = Guid.NewGuid();
    public DateTime OccurredOnUtc { get; init; } = DateTime.UtcNow;
}
```

---

## Template: Specific Domain Events

```csharp
// src/{name}.domain/{Aggregate}/Events/{Entity}CreatedDomainEvent.cs
using {name}.domain.abstractions;

namespace {name}.domain.{aggregate}.events;

/// <summary>
/// Raised when a new {Entity} is created
/// </summary>
public sealed record {Entity}CreatedDomainEvent(
    Guid {Entity}Id) : DomainEvent;

// src/{name}.domain/{Aggregate}/Events/{Entity}UpdatedDomainEvent.cs
/// <summary>
/// Raised when a {Entity} is updated
/// </summary>
public sealed record {Entity}UpdatedDomainEvent(
    Guid {Entity}Id,
    string PropertyName,
    string? OldValue,
    string? NewValue) : DomainEvent;

// src/{name}.domain/{Aggregate}/Events/{Entity}DeactivatedDomainEvent.cs
/// <summary>
/// Raised when a {Entity} is deactivated
/// </summary>
public sealed record {Entity}DeactivatedDomainEvent(
    Guid {Entity}Id,
    string Reason) : DomainEvent;

// src/{name}.domain/{Aggregate}/Events/{Entity}DeletedDomainEvent.cs
/// <summary>
/// Raised when a {Entity} is deleted
/// </summary>
public sealed record {Entity}DeletedDomainEvent(
    Guid {Entity}Id) : DomainEvent;
```

---

## Template: Rich Domain Events

```csharp
// src/{name}.domain/Users/Events/UserRegisteredDomainEvent.cs
using {name}.domain.abstractions;

namespace {name}.domain.users.events;

/// <summary>
/// Raised when a new user registers
/// </summary>
public sealed record UserRegisteredDomainEvent : DomainEvent
{
    public Guid UserId { get; init; }
    public string Email { get; init; } = string.Empty;
    public string Name { get; init; } = string.Empty;
    public Guid OrganizationId { get; init; }

    public UserRegisteredDomainEvent(
        Guid userId,
        string email,
        string name,
        Guid organizationId)
    {
        UserId = userId;
        Email = email;
        Name = name;
        OrganizationId = organizationId;
    }
}

// src/{name}.domain/Assessments/Events/AssessmentCompletedDomainEvent.cs
/// <summary>
/// Raised when a user completes an assessment
/// </summary>
public sealed record AssessmentCompletedDomainEvent : DomainEvent
{
    public Guid AssessmentId { get; init; }
    public Guid UserId { get; init; }
    public Guid OrganizationId { get; init; }
    public string AssessmentType { get; init; } = string.Empty;
    public decimal Score { get; init; }
    public DateTime CompletedAt { get; init; }

    public AssessmentCompletedDomainEvent(
        Guid assessmentId,
        Guid userId,
        Guid organizationId,
        string assessmentType,
        decimal score,
        DateTime completedAt)
    {
        AssessmentId = assessmentId;
        UserId = userId;
        OrganizationId = organizationId;
        AssessmentType = assessmentType;
        Score = score;
        CompletedAt = completedAt;
    }
}
```

---

## Template: Raising Events in Entity

```csharp
// src/{name}.domain/{Aggregate}/{Entity}.cs
using {name}.domain.abstractions;
using {name}.domain.{aggregate}.events;

namespace {name}.domain.{aggregate};

public sealed class {Entity} : Entity
{
    // ... properties

    private {Entity}(
        Guid id,
        string name,
        Guid organizationId,
        DateTime createdAt)
        : base(id)
    {
        Name = name;
        OrganizationId = organizationId;
        CreatedAt = createdAt;
    }

    /// <summary>
    /// Factory method - raises Created event
    /// </summary>
    public static Result<{Entity}> Create(
        string name,
        Guid organizationId,
        DateTime createdAt)
    {
        // Validation...

        var {entity} = new {Entity}(
            Guid.NewGuid(),
            name,
            organizationId,
            createdAt);

        // Raise domain event
        {entity}.RaiseDomainEvent(new {Entity}CreatedDomainEvent({entity}.Id));

        return {entity};
    }

    /// <summary>
    /// Update method - raises Updated event
    /// </summary>
    public Result Update(string name, DateTime updatedAt)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            return Result.Failure({Entity}Errors.NameRequired);
        }

        var oldName = Name;
        Name = name;
        UpdatedAt = updatedAt;

        // Raise domain event with change details
        RaiseDomainEvent(new {Entity}UpdatedDomainEvent(
            Id,
            nameof(Name),
            oldName,
            name));

        return Result.Success();
    }

    /// <summary>
    /// Deactivate method - raises Deactivated event
    /// </summary>
    public Result Deactivate(string reason, DateTime deactivatedAt)
    {
        if (!IsActive)
        {
            return Result.Failure({Entity}Errors.AlreadyDeactivated);
        }

        IsActive = false;
        UpdatedAt = deactivatedAt;

        RaiseDomainEvent(new {Entity}DeactivatedDomainEvent(Id, reason));

        return Result.Success();
    }
}
```

---

## Template: Domain Event Handler

```csharp
// src/{name}.application/{Feature}/EventHandlers/{Entity}CreatedDomainEventHandler.cs
using MediatR;
using Microsoft.Extensions.Logging;
using {name}.domain.{aggregate}.events;

namespace {name}.application.{feature}.eventhandlers;

/// <summary>
/// Handles {Entity}CreatedDomainEvent
/// </summary>
internal sealed class {Entity}CreatedDomainEventHandler
    : INotificationHandler<{Entity}CreatedDomainEvent>
{
    private readonly ILogger<{Entity}CreatedDomainEventHandler> _logger;

    public {Entity}CreatedDomainEventHandler(
        ILogger<{Entity}CreatedDomainEventHandler> logger)
    {
        _logger = logger;
    }

    public Task Handle(
        {Entity}CreatedDomainEvent notification,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            "{Entity} created: {EntityId} at {OccurredOn}",
            notification.{Entity}Id,
            notification.OccurredOnUtc);

        // Add any side effects here:
        // - Send notifications
        // - Update read models
        // - Trigger workflows
        // - Publish to external systems

        return Task.CompletedTask;
    }
}
```

---

## Template: Event Handler with Side Effects

```csharp
// src/{name}.application/Users/EventHandlers/UserRegisteredDomainEventHandler.cs
using MediatR;
using Microsoft.Extensions.Logging;
using {name}.application.abstractions.email;
using {name}.domain.users.events;

namespace {name}.application.users.eventhandlers;

/// <summary>
/// Sends welcome email when user registers
/// </summary>
internal sealed class UserRegisteredSendWelcomeEmailHandler
    : INotificationHandler<UserRegisteredDomainEvent>
{
    private readonly IEmailService _emailService;
    private readonly ILogger<UserRegisteredSendWelcomeEmailHandler> _logger;

    public UserRegisteredSendWelcomeEmailHandler(
        IEmailService emailService,
        ILogger<UserRegisteredSendWelcomeEmailHandler> logger)
    {
        _emailService = emailService;
        _logger = logger;
    }

    public async Task Handle(
        UserRegisteredDomainEvent notification,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            "Sending welcome email to user {UserId}",
            notification.UserId);

        await _emailService.SendWelcomeEmailAsync(
            notification.Email,
            notification.Name,
            cancellationToken);
    }
}

/// <summary>
/// Creates default settings when user registers
/// </summary>
internal sealed class UserRegisteredCreateDefaultSettingsHandler
    : INotificationHandler<UserRegisteredDomainEvent>
{
    private readonly IUserSettingsRepository _settingsRepository;
    private readonly IUnitOfWork _unitOfWork;

    public UserRegisteredCreateDefaultSettingsHandler(
        IUserSettingsRepository settingsRepository,
        IUnitOfWork unitOfWork)
    {
        _settingsRepository = settingsRepository;
        _unitOfWork = unitOfWork;
    }

    public async Task Handle(
        UserRegisteredDomainEvent notification,
        CancellationToken cancellationToken)
    {
        var settings = UserSettings.CreateDefault(notification.UserId);

        _settingsRepository.Add(settings);

        await _unitOfWork.SaveChangesAsync(cancellationToken);
    }
}
```

---

## Template: Outbox Pattern Implementation

### Outbox Message Entity

```csharp
// src/{name}.infrastructure/Outbox/OutboxMessage.cs
namespace {name}.infrastructure.outbox;

/// <summary>
/// Represents a domain event stored for reliable delivery
/// </summary>
public sealed class OutboxMessage
{
    public Guid Id { get; set; }
    public string Type { get; set; } = string.Empty;
    public string Content { get; set; } = string.Empty;
    public DateTime OccurredOnUtc { get; set; }
    public DateTime? ProcessedOnUtc { get; set; }
    public string? Error { get; set; }
}
```

### Outbox Configuration

```csharp
// src/{name}.infrastructure/Configurations/OutboxMessageConfiguration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.infrastructure.outbox;

namespace {name}.infrastructure.configurations;

internal sealed class OutboxMessageConfiguration
    : IEntityTypeConfiguration<OutboxMessage>
{
    public void Configure(EntityTypeBuilder<OutboxMessage> builder)
    {
        builder.ToTable("outbox_message");

        builder.HasKey(o => o.Id);

        builder.Property(o => o.Type)
            .HasMaxLength(500)
            .IsRequired();

        builder.Property(o => o.Content)
            .HasColumnType("jsonb")
            .IsRequired();

        builder.Property(o => o.OccurredOnUtc)
            .IsRequired();

        builder.Property(o => o.ProcessedOnUtc);

        builder.Property(o => o.Error)
            .HasColumnType("text");

        // Index for efficient querying of unprocessed messages
        builder.HasIndex(o => o.ProcessedOnUtc)
            .HasFilter("processed_on_utc IS NULL");
    }
}
```

### Adding Events to Outbox in DbContext

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
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
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
        // Convert domain events to outbox messages before saving
        AddDomainEventsAsOutboxMessages();

        return await base.SaveChangesAsync(cancellationToken);
    }

    private void AddDomainEventsAsOutboxMessages()
    {
        var entities = ChangeTracker
            .Entries<Entity>()
            .Where(e => e.Entity.GetDomainEvents().Any())
            .Select(e => e.Entity)
            .ToList();

        var domainEvents = entities
            .SelectMany(e => e.GetDomainEvents())
            .ToList();

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

        foreach (var entity in entities)
        {
            entity.ClearDomainEvents();
        }
    }
}
```

### Outbox Processor Job (Quartz)

```csharp
// src/{name}.infrastructure/Outbox/ProcessOutboxMessagesJob.cs
using System.Text.Json;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Quartz;
using {name}.domain.abstractions;

namespace {name}.infrastructure.outbox;

[DisallowConcurrentExecution]
internal sealed class ProcessOutboxMessagesJob : IJob
{
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
        _logger.LogInformation("Processing outbox messages...");

        var messages = await _dbContext
            .OutboxMessages
            .Where(m => m.ProcessedOnUtc == null)
            .OrderBy(m => m.OccurredOnUtc)
            .Take(20)
            .ToListAsync(context.CancellationToken);

        foreach (var message in messages)
        {
            try
            {
                var type = Type.GetType(message.Type);

                if (type is null)
                {
                    _logger.LogWarning(
                        "Could not resolve type {Type} for outbox message {MessageId}",
                        message.Type,
                        message.Id);

                    message.Error = $"Could not resolve type: {message.Type}";
                    message.ProcessedOnUtc = DateTime.UtcNow;
                    continue;
                }

                var domainEvent = JsonSerializer.Deserialize(
                    message.Content,
                    type,
                    JsonOptions) as IDomainEvent;

                if (domainEvent is null)
                {
                    _logger.LogWarning(
                        "Could not deserialize outbox message {MessageId}",
                        message.Id);

                    message.Error = "Could not deserialize message content";
                    message.ProcessedOnUtc = DateTime.UtcNow;
                    continue;
                }

                await _publisher.Publish(domainEvent, context.CancellationToken);

                message.ProcessedOnUtc = DateTime.UtcNow;

                _logger.LogInformation(
                    "Processed outbox message {MessageId} of type {Type}",
                    message.Id,
                    message.Type);
            }
            catch (Exception ex)
            {
                _logger.LogError(
                    ex,
                    "Error processing outbox message {MessageId}",
                    message.Id);

                message.Error = ex.ToString();
            }
        }

        await _dbContext.SaveChangesAsync(context.CancellationToken);
    }
}
```

### Registering Quartz Job

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
private static void AddBackgroundJobs(IServiceCollection services)
{
    services.AddQuartz(configure =>
    {
        var jobKey = new JobKey(nameof(ProcessOutboxMessagesJob));

        configure
            .AddJob<ProcessOutboxMessagesJob>(jobKey)
            .AddTrigger(trigger =>
                trigger
                    .ForJob(jobKey)
                    .WithSimpleSchedule(schedule =>
                        schedule.WithIntervalInSeconds(10).RepeatForever()));
    });

    services.AddQuartzHostedService();
}
```

---

## Event Naming Conventions

| Event Type | Naming Pattern | Example |
|------------|----------------|---------|
| Created | `{Entity}CreatedDomainEvent` | `UserCreatedDomainEvent` |
| Updated | `{Entity}UpdatedDomainEvent` | `UserUpdatedDomainEvent` |
| Deleted | `{Entity}DeletedDomainEvent` | `UserDeletedDomainEvent` |
| Status Change | `{Entity}{Status}DomainEvent` | `OrderShippedDomainEvent` |
| Action | `{Entity}{Action}DomainEvent` | `PaymentProcessedDomainEvent` |

---

## Critical Rules

1. **Events are immutable** - Use `record` types
2. **Events are past tense** - Something that *happened*
3. **Events are raised in domain** - Not in handlers
4. **Handlers are independent** - Can fail independently
5. **Use Outbox for reliability** - Events survive crashes
6. **Don't await handlers** - Fire and forget (via MediatR)
7. **Idempotent handlers** - May process same event twice
8. **Events include context** - Enough data to act without queries
9. **One aggregate per event** - Clear ownership
10. **No return values** - Events are notifications

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Events with behavior
public record UserCreatedEvent
{
    public void SendEmail() { }  // Events should be data only!
}

// ✅ CORRECT: Pure data event
public record UserCreatedDomainEvent(Guid UserId, string Email) : DomainEvent;

// ❌ WRONG: Raising events in handler
internal sealed class CreateUserHandler : ICommandHandler<CreateUser, Guid>
{
    public async Task<Result<Guid>> Handle(...)
    {
        // Don't raise events here!
        await _publisher.Publish(new UserCreatedEvent(user.Id));
    }
}

// ✅ CORRECT: Raise events in entity
public static Result<User> Create(...)
{
    var user = new User(...);
    user.RaiseDomainEvent(new UserCreatedDomainEvent(user.Id, user.Email));
    return user;
}

// ❌ WRONG: Handler depends on other handler's result
internal sealed class Handler1 : INotificationHandler<Event>
{
    public async Task Handle(Event e, CancellationToken ct)
    {
        // Waiting for Handler2 to complete - bad!
        while (!await _service.IsHandler2Complete()) { }
    }
}

// ✅ CORRECT: Handlers are independent
internal sealed class Handler1 : INotificationHandler<Event>
{
    public Task Handle(Event e, CancellationToken ct)
    {
        // Does its own work, doesn't care about other handlers
        return DoWork(e, ct);
    }
}
```

---

## Related Skills

- `domain-entity-generator` - Entities that raise events
- `pipeline-behaviors` - Event publishing behavior
- `dotnet-clean-architecture` - Infrastructure layer setup
- `cqrs-command-generator` - Commands that trigger events
