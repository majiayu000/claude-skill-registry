---
name: easyplatform-backend
description: Complete Easy.Platform backend development for EasyPlatform. Covers CQRS commands/queries, entities, validation, migrations, background jobs, and message bus. Use for any .NET backend task in this monorepo.
infer: true
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
├── Business entity? → Entity Development (§3)
├── Side effects (notifications, emails)? → Entity Event Handler (§4) - NEVER in command handlers!
├── Data transformation/backfill? → Migration (§5)
├── Scheduled/recurring task? → Background Job (§6)
└── Cross-service sync? → Message Bus (§7) - NEVER direct DB access!
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

1. **Repository:** `IPlatformQueryableRootRepository<T>` -- NEVER throw exceptions for validation
2. **Validation:** `PlatformValidationResult` fluent API
3. **Side Effects:** Entity Event Handlers -- NEVER in command handlers
4. **DTO Mapping:** DTOs own mapping via `PlatformEntityDto<T,K>.MapToEntity()`
5. **Cross-Service:** Message bus -- NEVER direct database access

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

**⚠️ MUST READ:** [references/cqrs-patterns.md](references/cqrs-patterns.md) — full CQRS command patterns

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
                .OrderByDescending(e => e.CreatedDate).PageBy(req.SkipCount, req.MaxResultCount), ct)
        );
        return new GetEmployeeListQueryResult(items.SelectList(e => new EmployeeDto(e)), total, req);
    }
}
```

**⚠️ MUST READ:** [references/cqrs-patterns.md](references/cqrs-patterns.md) — full CQRS query patterns

---

## §3. Entity Development

**File:** `{Service}.Domain/Entities/{Entity}.cs`

```csharp
[TrackFieldUpdatedDomainEvent]
public sealed class Employee : RootAuditedEntity<Employee, string, string>
{
    [TrackFieldUpdatedDomainEvent] public string Name { get; set; } = "";
    public string CompanyId { get; set; } = "";

    [ComputedEntityProperty]
    public string DisplayName { get => $"{Code} - {Name}"; set { } }

    public static Expression<Func<Employee, bool>> OfCompanyExpr(string companyId) => e => e.CompanyId == companyId;
    public static Expression<Func<Employee, bool>> UniqueExpr(string companyId, string code) => e => e.CompanyId == companyId && e.Code == code;
    public static Expression<Func<Employee, object?>>[] DefaultFullTextSearchColumns() => [e => e.Name, e => e.Code];

    public async Task<PlatformValidationResult> ValidateAsync(IRepository<Employee> repo, CancellationToken ct)
        => await PlatformValidationResult.Valid()
            .And(() => Name.IsNotNullOrEmpty(), "Name required")
            .AndNotAsync(() => repo.AnyAsync(e => e.Id != Id && e.Code == Code, ct), "Code exists");
}
```

**⚠️ MUST READ:** [references/entity-patterns.md](references/entity-patterns.md) — full entity patterns

---

## §4. Entity Event Handlers (Side Effects)

**CRITICAL:** NEVER call side effects in command handlers!

**File:** `UseCaseEvents/{Feature}/Send{Action}On{Event}{Entity}EntityEventHandler.cs`

```csharp
internal sealed class SendNotificationOnCreateEmployeeEntityEventHandler
    : PlatformCqrsEntityEventApplicationHandler<Employee>
{
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Employee> @event)
        => !@event.RequestContext.IsSeedingTestingData()
           && @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;

    protected override async Task HandleAsync(PlatformCqrsEntityEvent<Employee> @event, CancellationToken ct)
        => await notificationService.SendAsync(@event.EntityData.Id);
}
```

**⚠️ MUST READ:** [references/side-effects-patterns.md](references/side-effects-patterns.md) — side effects patterns

## §5-7. Migrations, Jobs, Message Bus

**⚠️ MUST READ:** [migration-patterns.md](references/migration-patterns.md) | [job-patterns.md](references/job-patterns.md) | [messaging-patterns.md](references/messaging-patterns.md)

---

## Anti-Patterns

| Don't                             | Do                                              |
| --------------------------------- | ----------------------------------------------- |
| `throw new ValidationException()` | `PlatformValidationResult` fluent API           |
| Side effects in command handler   | Entity Event Handler in `UseCaseEvents/`        |
| Direct cross-service DB access    | Message bus                                     |
| DTO mapping in handler            | `PlatformEntityDto.MapToEntity()`               |
| Separate Command/Handler files    | ONE file: Command + Result + Handler            |
| `protected bool HandleWhen()`     | `public override async Task<bool> HandleWhen()` |

## Checklist

- [ ] Service-specific repository, fluent validation (`.And()`, `.AndAsync()`)
- [ ] No side effects in command handlers, DTO mapping in DTO class
- [ ] Cross-service uses message bus, jobs have `maxConcurrent`, migrations use `dismissSendEvent: true`


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
