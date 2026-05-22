---
name: backend-csharp-patterns
description: Use when editing C# backend files (.cs) in src/Backend/, src/Platform/, or src/PlatformExampleApp/. Provides CQRS patterns, repository patterns, validation patterns, entity patterns, background jobs, message bus consumers, data migrations, and fluent helpers for EasyPlatform .NET 9 development.
---

# Backend C# Code Patterns

When implementing backend C# code in EasyPlatform, follow these patterns exactly.

## Full Pattern Reference

See the complete code patterns with examples: [backend-code-patterns.md](.ai/docs/backend-code-patterns.md)

## Quick Reference

### Pattern Index

| #   | Pattern            | Key Interface/Contract                                                                             |
| --- | ------------------ | -------------------------------------------------------------------------------------------------- |
| 1   | Clean Architecture | Domain → Application → Persistence → Api layers                                                    |
| 2   | Repository         | `IPlatformQueryableRootRepository<TEntity, TKey>` + static expression extensions                   |
| 3   | Repository API     | `CreateAsync`, `GetByIdAsync`, `GetAllAsync`, `FirstOrDefaultAsync`, `CountAsync`                  |
| 4   | Validation         | `PlatformValidationResult.And().AndAsync()` fluent chain, never throw                              |
| 5   | Cross-Service      | `PlatformCqrsEntityEventBusMessageProducer` + `PlatformApplicationMessageBusConsumer`              |
| 6   | Full-Text Search   | `searchService.Search(q, text, Entity.SearchColumns())` in query builder                           |
| 7   | CQRS Command       | Command + Result + Handler in ONE file, `PlatformCqrsCommandApplicationHandler`                    |
| 8   | Query              | `PlatformCqrsPagedQuery` + `GetQueryBuilder()` + parallel count/items                              |
| 9   | Side Effects       | Entity Event Handlers in `UseCaseEvents/`, never in command handlers                               |
| 10  | Entity             | `RootEntity<T, TKey>`, static expressions, `[TrackFieldUpdatedDomainEvent]`, navigation properties |
| 11  | DTO                | `PlatformEntityDto<T, TKey>.MapToEntity()`, DTO owns mapping, constructor from entity              |
| 12  | Fluent Helpers     | `.With()`, `.Then()`, `.EnsureFound()`, `.EnsureValid()`, `.ParallelAsync()`                       |
| 13  | Background Jobs    | `PlatformApplicationPagedBackgroundJobExecutor`, `[PlatformRecurringJob("cron")]`                  |
| 14  | Message Bus        | `PlatformApplicationMessageBusConsumer<TMessage>`, `TryWaitUntilAsync()` for deps                  |
| 15  | Data Migration     | `PlatformDataMigrationExecutor<TDbContext>`, `OnlyForDbsCreatedBeforeDate`                         |
| 16  | Multi-Database     | `PlatformEfCorePersistenceModule` / `PlatformMongoDbPersistenceModule`                             |

## Critical Rules

1. **Repository:** Use `IPlatformQueryableRootRepository<TEntity, TKey>` - NEVER generic `IPlatformRootRepository`
2. **Validation:** Use `PlatformValidationResult` fluent API (`.And()`, `.AndAsync()`) - NEVER `throw ValidationException`
3. **Side Effects:** Handle in Entity Event Handlers (`UseCaseEvents/`) - NEVER in command handlers
4. **DTO Mapping:** DTOs own mapping via `MapToEntity()` or `MapToObject()` - NEVER map in handlers
5. **Command Structure:** Command + Result + Handler in ONE file under `UseCaseCommands/{Feature}/`
6. **Cross-Service:** Use RabbitMQ message bus - NEVER direct database access

## Anti-Patterns

```csharp
// ❌ Direct cross-service DB access → ✅ Use message bus
// ❌ Custom repository interface → ✅ Use platform repo + extensions
// ❌ Manual validation throw → ✅ Use PlatformValidationResult fluent API
// ❌ Side effects in handler → ✅ Use entity event handlers
// ❌ DTO mapping in handler → ✅ DTO owns mapping via MapToObject()/MapToEntity()
```

## Templates

### CQRS Command Template

```csharp
public sealed class Save{Entity}Command : PlatformCqrsCommand<Save{Entity}CommandResult>
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";

    public override PlatformValidationResult<IPlatformCqrsRequest> Validate()
        => base.Validate().And(_ => Name.IsNotNullOrEmpty(), "Name required");
}

public sealed class Save{Entity}CommandResult : PlatformCqrsCommandResult
{
    public {Entity}Dto Entity { get; set; } = null!;
}

internal sealed class Save{Entity}CommandHandler : PlatformCqrsCommandApplicationHandler<Save{Entity}Command, Save{Entity}CommandResult>
{
    protected override async Task<Save{Entity}CommandResult> HandleAsync(Save{Entity}Command req, CancellationToken ct)
    {
        var entity = req.Id.IsNullOrEmpty()
            ? req.MapToNewEntity().With(e => e.CreatedBy = RequestContext.UserId())
            : await repo.GetByIdAsync(req.Id, ct).Then(e => req.UpdateEntity(e));
        await entity.ValidateAsync(repo, ct).EnsureValidAsync();
        var saved = await repo.CreateOrUpdateAsync(entity, ct);
        return new Save{Entity}CommandResult { Entity = new {Entity}Dto(saved) };
    }
}
```

## Detailed Instructions

For task-specific guidance, also reference:

- [backend-dotnet.instructions.md](instructions/backend-dotnet.instructions.md) - .NET patterns
- [cqrs-patterns.instructions.md](instructions/cqrs-patterns.instructions.md) - CQRS handlers
- [entity-development.instructions.md](instructions/entity-development.instructions.md) - Entity design
- [validation.instructions.md](instructions/validation.instructions.md) - Validation patterns
- [repository.instructions.md](instructions/repository.instructions.md) - Repository patterns
- [message-bus.instructions.md](instructions/message-bus.instructions.md) - Message bus
- [background-jobs.instructions.md](instructions/background-jobs.instructions.md) - Background jobs
- [migrations.instructions.md](instructions/migrations.instructions.md) - Data migrations
