---
name: easyplatform-backend
description: Complete Easy.Platform backend development for EasyPlatform. Covers CQRS commands/queries, entities, validation, migrations, background jobs, and message bus. Use for any .NET backend task in this monorepo.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Easy.Platform Backend Development

Complete backend development patterns for EasyPlatform .NET 9 microservices.

## Quick Decision Tree

```
[Backend Task]
├── API endpoint?
│   ├── Creates/Updates/Deletes data → CQRS Command (§1)
│   └── Reads data → CQRS Query (§2)
│
├── Business entity?
│   └── Entity Development (§3)
│
├── Side effects (notifications, emails, external APIs)?
│   └── Entity Event Handler (§4) - NEVER in command handlers!
│
├── Data transformation/backfill?
│   └── Migration (§5)
│
├── Scheduled/recurring task?
│   └── Background Job (§6)
│
└── Cross-service sync?
    └── Message Bus (§7) - NEVER direct DB access!
```

## File Organization

```
{Service}.Application/
├── UseCaseCommands/{Feature}/Save{Entity}Command.cs     # Command+Handler+Result
├── UseCaseQueries/{Feature}/Get{Entity}ListQuery.cs     # Query+Handler+Result
├── UseCaseEvents/{Feature}/*EntityEventHandler.cs       # Side effects
├── BackgroundJobs/{Feature}/*Job.cs                     # Scheduled tasks
├── MessageBusProducers/*Producer.cs                     # Outbound events
├── MessageBusConsumers/{Entity}/*Consumer.cs            # Inbound events
└── DataMigrations/*DataMigration.cs                     # Data migrations

{Service}.Domain/
└── Entities/{Entity}.cs                                 # Domain entities
```

## Critical Rules

1. **Repository:** Use service-specific repos (`IPlatformQueryableRootRepository<T>`, `IPlatformQueryableRootRepository<T>`)
2. **Validation:** Use `PlatformValidationResult` fluent API - NEVER throw exceptions
3. **Side Effects:** Handle in Entity Event Handlers - NEVER in command handlers
4. **DTO Mapping:** DTOs own mapping via `PlatformEntityDto<T,K>.MapToEntity()`
5. **Cross-Service:** Use message bus - NEVER direct database access

---

## §1. CQRS Commands

**File:** `UseCaseCommands/{Feature}/Save{Entity}Command.cs` (Command + Result + Handler in ONE file)

```csharp
public sealed class SaveEmployeeCommand : PlatformCqrsCommand<SaveEmployeeCommandResult>
{
    public string? Id { get; set; }
    public string Name { get; set; } = "";

    public override PlatformValidationResult<IPlatformCqrsRequest> Validate()
        => base.Validate().And(_ => Name.IsNotNullOrEmpty(), "Name required");
}

public sealed class SaveEmployeeCommandResult : PlatformCqrsCommandResult
{
    public EmployeeDto Entity { get; set; } = null!;
}

internal sealed class SaveEmployeeCommandHandler :
    PlatformCqrsCommandApplicationHandler<SaveEmployeeCommand, SaveEmployeeCommandResult>
{
    protected override async Task<SaveEmployeeCommandResult> HandleAsync(
        SaveEmployeeCommand req, CancellationToken ct)
    {
        var entity = req.Id.IsNullOrEmpty()
            ? req.MapToNewEntity().With(e => e.CreatedBy = RequestContext.UserId())
            : await repository.GetByIdAsync(req.Id, ct)
                .EnsureFound().Then(e => req.UpdateEntity(e));

        await entity.ValidateAsync(repository, ct).EnsureValidAsync();
        await repository.CreateOrUpdateAsync(entity, ct);
        return new SaveEmployeeCommandResult { Entity = new EmployeeDto(entity) };
    }
}
```

**See:** `references/cqrs-patterns.md` for validation, async validation, parallel operations

---

## §2. CQRS Queries

**File:** `UseCaseQueries/{Feature}/Get{Entity}ListQuery.cs`

```csharp
public sealed class GetEmployeeListQuery : PlatformCqrsPagedQuery<GetEmployeeListQueryResult, EmployeeDto>
{
    public List<Status> Statuses { get; set; } = [];
    public string? SearchText { get; set; }
}

internal sealed class GetEmployeeListQueryHandler :
    PlatformCqrsQueryApplicationHandler<GetEmployeeListQuery, GetEmployeeListQueryResult>
{
    protected override async Task<GetEmployeeListQueryResult> HandleAsync(
        GetEmployeeListQuery req, CancellationToken ct)
    {
        var qb = repository.GetQueryBuilder((uow, q) => q
            .Where(e => e.CompanyId == RequestContext.CurrentCompanyId())
            .WhereIf(req.Statuses.Any(), e => req.Statuses.Contains(e.Status))
            .PipeIf(req.SearchText.IsNotNullOrEmpty(), q =>
                searchService.Search(q, req.SearchText, Employee.DefaultFullTextSearchColumns())));

        var (total, items) = await (
            repository.CountAsync((uow, q) => qb(uow, q), ct),
            repository.GetAllAsync((uow, q) => qb(uow, q)
                .OrderByDescending(e => e.CreatedDate)
                .PageBy(req.SkipCount, req.MaxResultCount), ct)
        );
        return new GetEmployeeListQueryResult(items.SelectList(e => new EmployeeDto(e)), total, req);
    }
}
```

**Key patterns:** `GetQueryBuilder`, `WhereIf`, `PipeIf`, tuple await for parallel queries

**See:** `references/cqrs-patterns.md` for full-text search, aggregation, eager loading

---

## §3. Entity Development

**File:** `{Service}.Domain/Entities/{Entity}.cs`

```csharp
[TrackFieldUpdatedDomainEvent]
public sealed class Employee : RootAuditedEntity<Employee, string, string>
{
    // Properties
    [TrackFieldUpdatedDomainEvent]
    public string Name { get; set; } = "";
    public string CompanyId { get; set; } = "";

    [JsonIgnore]
    public Company? Company { get; set; }

    // Computed (MUST have empty set { })
    [ComputedEntityProperty]
    public string DisplayName { get => $"{Code} - {Name}"; set { } }

    // Static expressions
    public static Expression<Func<Employee, bool>> OfCompanyExpr(string companyId)
        => e => e.CompanyId == companyId;

    public static Expression<Func<Employee, bool>> UniqueExpr(string companyId, string code)
        => e => e.CompanyId == companyId && e.Code == code;

    public static Expression<Func<Employee, object?>>[] DefaultFullTextSearchColumns()
        => [e => e.Name, e => e.Code, e => e.Email];

    // Validation
    public async Task<PlatformValidationResult> ValidateAsync(IRepository<Employee> repo, CancellationToken ct)
        => await PlatformValidationResult.Valid()
            .And(() => Name.IsNotNullOrEmpty(), "Name required")
            .AndNotAsync(() => repo.AnyAsync(e => e.Id != Id && e.Code == Code, ct), "Code exists");
}
```

**Expression composition:** `.AndAlso()`, `.OrElse()`, `.AndAlsoIf(condition, () => expr)`

**See:** `references/entity-patterns.md` for computed properties, async expressions, audited entities

---

## §4. Entity Event Handlers (Side Effects)

**CRITICAL:** NEVER call side effects in command handlers - use Entity Event Handlers!

**File:** `UseCaseEvents/{Feature}/Send{Action}On{Event}{Entity}EntityEventHandler.cs`

```csharp
internal sealed class SendNotificationOnCreateEmployeeEntityEventHandler
    : PlatformCqrsEntityEventApplicationHandler<Employee>  // Single generic param!
{
    // Must be: public override async Task<bool>
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Employee> @event)
    {
        if (@event.RequestContext.IsSeedingTestingData()) return false;
        return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
    }

    protected override async Task HandleAsync(PlatformCqrsEntityEvent<Employee> @event, CancellationToken ct)
    {
        await notificationService.SendAsync(@event.EntityData.Id, @event.RequestContext.UserId());
    }
}
```

**See:** `references/side-effects-patterns.md` for CRUD filtering, accessing event data

---

## §5. Data Migrations

**Decision:** Schema change → EF Core. Data transformation → PlatformDataMigrationExecutor.

```csharp
public sealed class MigratePhoneNumbers : PlatformDataMigrationExecutor<GrowthDbContext>
{
    public override string Name => "20251015000000_MigratePhoneNumbers";
    public override DateTime? OnlyForDbsCreatedBeforeDate => new(2025, 10, 15);
    public override bool AllowRunInBackgroundThread => true;

    public override async Task Execute(GrowthDbContext dbContext)
    {
        await RootServiceProvider.ExecuteInjectScopedPagingAsync(
            maxItemCount: await repository.CountAsync(q => q.Where(FilterExpr())),
            pageSize: 200,
            processingDelegate: async (skip, take, repo, uow) => {
                using var unit = uow.Begin();
                var items = await repo.GetAllAsync(q => q.OrderBy(e => e.Id).Skip(skip).Take(take));
                await repo.UpdateManyAsync(items, dismissSendEvent: true, checkDiff: false);
                await unit.CompleteAsync();
                return items;
            });
    }
}
```

**See:** `references/migration-patterns.md` for EF Core, MongoDB, scrolling patterns

---

## §6. Background Jobs

**Decision Tree:**
- Data doesn't change during processing → Paged (`PlatformApplicationPagedBackgroundJobExecutor`)
- Data changes, multi-tenant → Batch Scrolling (`PlatformApplicationBatchScrollingBackgroundJobExecutor`)
- Data changes, single-tenant → Scrolling (`ExecuteInjectScopedScrollingPagingAsync`)

```csharp
[PlatformRecurringJob("0 3 * * *")]  // Daily 3 AM
public sealed class ProcessPendingJob : PlatformApplicationPagedBackgroundJobExecutor
{
    protected override int PageSize => 50;

    protected override async Task<int> MaxItemsCount(PlatformApplicationPagedBackgroundJobParam<object?> param)
        => await repository.CountAsync(q => q.Where(FilterExpr()));

    protected override async Task ProcessPagedAsync(int? skip, int? take, object? param,
        IServiceProvider sp, IPlatformUnitOfWorkManager uow)
    {
        var items = await repository.GetAllAsync(q => FilterExpr().OrderBy(e => e.Id).PageBy(skip, take));
        await items.ParallelAsync(ProcessItem, maxConcurrent: 5);
    }
}
```

**See:** `references/job-patterns.md` for batch scrolling, master-child coordination, cron reference

---

## §7. Message Bus (Cross-Service)

**CRITICAL:** Cross-service data sync uses message bus - NEVER direct database access!

### Producer (Source Service)

```csharp
internal sealed class EmployeeEntityEventBusMessageProducer
    : PlatformCqrsEntityEventBusMessageProducer<EmployeeEntityEventBusMessage, Employee, string>
{
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Employee> @event)
        => !@event.RequestContext.IsSeedingTestingData();

    protected override Task<EmployeeEntityEventBusMessage> BuildMessageAsync(
        PlatformCqrsEntityEvent<Employee> @event, CancellationToken ct)
        => Task.FromResult(new EmployeeEntityEventBusMessage(@event, new EmployeeEventData(@event.EntityData)));
}
```

### Consumer (Target Service)

```csharp
internal sealed class UpsertEmployeeOnEmployeeEventConsumer
    : PlatformApplicationMessageBusConsumer<EmployeeEntityEventBusMessage>
{
    public override async Task HandleLogicAsync(EmployeeEntityEventBusMessage msg, string routingKey)
    {
        // Wait for dependencies (prevents FK violations)
        var companyExists = await Util.TaskRunner.TryWaitUntilAsync(
            () => companyRepo.AnyAsync(c => c.Id == msg.Payload.EntityData.CompanyId),
            maxWaitSeconds: msg.IsForceSyncDataRequest() ? 30 : 300);
        if (!companyExists) return;

        // Handle delete (both hard delete and soft delete)
        if (msg.Payload.CrudAction == Deleted ||
            (msg.Payload.CrudAction == Updated && msg.Payload.EntityData.IsDeleted))
        {
            await repository.DeleteAsync(msg.Payload.EntityData.Id);
            return;
        }

        // Upsert with race condition prevention
        var existing = await repository.FirstOrDefaultAsync(e => e.SourceId == msg.Payload.EntityData.Id);
        if (existing == null)
            await repository.CreateAsync(msg.Payload.EntityData.ToEntity()
                .With(e => e.LastMessageSyncDate = msg.CreatedUtcDate));
        else if (existing.LastMessageSyncDate <= msg.CreatedUtcDate)
            await repository.UpdateAsync(msg.Payload.EntityData.UpdateEntity(existing)
                .With(e => e.LastMessageSyncDate = msg.CreatedUtcDate));
    }
}
```

**See:** `references/messaging-patterns.md` for message definitions, custom messages, naming conventions

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| `throw new ValidationException()` | Use `PlatformValidationResult` fluent API |
| Side effects in command handler | Entity Event Handler in `UseCaseEvents/` |
| `IPlatformRootRepository<T>` | Service-specific: `IPlatformQueryableRootRepository<T>` |
| Direct cross-service DB access | Message bus |
| DTO mapping in handler | `PlatformEntityDto.MapToEntity()` |
| Separate Command/Handler files | ONE file: Command + Result + Handler |
| `protected bool HandleWhen()` | `public override async Task<bool> HandleWhen()` |

---

## Verification Checklist

- [ ] Uses service-specific repository (`I{Service}RootRepository<T>`)
- [ ] Validation uses fluent API (`.And()`, `.AndAsync()`)
- [ ] No side effects in command handlers
- [ ] DTO mapping in DTO class
- [ ] Cross-service uses message bus
- [ ] Background jobs have `maxConcurrent` limit
- [ ] Migrations use `dismissSendEvent: true`
