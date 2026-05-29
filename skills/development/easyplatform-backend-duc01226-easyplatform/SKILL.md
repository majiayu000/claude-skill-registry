---
name: easyplatform-backend
description: "[Implementation] Complete Easy.Platform backend development for EasyPlatform. Covers CQRS commands/queries, entities, validation, migrations, background jobs, and message bus. Use for any .NET backend task in this monorepo."
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Easy.Platform Backend Development

Complete backend development patterns for EasyPlatform .NET 9 microservices. All patterns consolidated inline for efficient context loading.

## Summary

**Goal:** Comprehensive .NET 9 CQRS backend patterns — commands, queries, entities, events, migrations, jobs, message bus — with zero external references.

**Coverage:** 7 major patterns, 850+ lines of inline examples, anti-patterns catalog, complete fluent API reference.

| Pattern | File Location | Key Classes |
|---------|---------------|-------------|
| CQRS Commands | `UseCaseCommands/{Feature}/` | `PlatformCqrsCommand`, `PlatformCqrsCommandApplicationHandler` |
| CQRS Queries | `UseCaseQueries/{Feature}/` | `PlatformCqrsPagedQuery`, `GetQueryBuilder` |
| Entities | `{Service}.Domain/Entities/` | `RootEntity`, `RootAuditedEntity`, static expressions |
| Event Handlers | `UseCaseEvents/{Feature}/` | `PlatformCqrsEntityEventApplicationHandler` |
| Migrations | `DataMigrations/`, `Migrations/` | `PlatformDataMigrationExecutor`, `PlatformMongoMigrationExecutor` |
| Background Jobs | `BackgroundJobs/` | `PlatformApplicationPagedBackgroundJobExecutor` |
| Message Bus | `MessageBusProducers/`, `MessageBusConsumers/` | `PlatformApplicationMessageBusConsumer` |

**Critical Rules:**
1. **Validation:** `PlatformValidationResult` fluent API (`.And()`, `.AndAsync()`) — NEVER throw exceptions
2. **Side Effects:** Entity Event Handlers in `UseCaseEvents/` — NEVER in command handlers
3. **Cross-Service:** Message bus only — NEVER direct database access
4. **DTO Mapping:** DTOs own mapping via `MapToEntity()` — NEVER in handlers
5. **File Structure:** Command + Result + Handler in ONE file

---

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

---

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

---

# §1. CQRS Commands

**File:** `UseCaseCommands/{Feature}/Save{Entity}Command.cs` (Command + Result + Handler in ONE file)

## Basic Command Template

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

---

## Command Validation Patterns

### Sync Validation (in Command class)

```csharp
public override PlatformValidationResult<IPlatformCqrsRequest> Validate()
{
    return base.Validate()
        .And(_ => Name.IsNotNullOrEmpty(), "Name required")
        .And(_ => StartDate <= EndDate, "Invalid range")
        .And(_ => Items.Count > 0, "At least one item required")
        .Of<IPlatformCqrsRequest>();
}
```

### Async Validation (in Handler)

```csharp
protected override async Task<PlatformValidationResult<SaveCommand>> ValidateRequestAsync(
    PlatformValidationResult<SaveCommand> validation, CancellationToken ct)
{
    return await validation
        // Validate all IDs exist
        .AndAsync(req => repository.GetByIdsAsync(req.RelatedIds, ct)
            .ThenValidateFoundAllAsync(req.RelatedIds, ids => $"Not found: {ids}"))
        // Validate uniqueness
        .AndNotAsync(req => repository.AnyAsync(e => e.Code == req.Code && e.Id != req.Id, ct),
            "Code already exists")
        // Validate business rule
        .AndAsync(req => ValidateBusinessRuleAsync(req, ct));
}
```

### Chained Validation with Of<>

```csharp
return this.Validate(p => p.Id.IsNotNullOrEmpty(), "Id required")
    .And(p => p.Status != Status.Deleted, "Cannot modify deleted")
    .Of<IPlatformCqrsRequest>();
```

---

## Repository Extensions

```csharp
// Extension pattern
public static async Task<Employee> GetByEmailAsync(
    this IPlatformQueryableRootRepository<Employee> repo, string email, CancellationToken ct = default)
    => await repo.FirstOrDefaultAsync(Employee.ByEmailExpr(email), ct).EnsureFound();

public static async Task<List<Entity>> GetByIdsValidatedAsync(
    this IPlatformQueryableRootRepository<Entity, string> repo, List<string> ids, CancellationToken ct = default)
    => await repo.GetAllAsync(p => ids.Contains(p.Id), ct).EnsureFoundAllBy(p => p.Id, ids);

public static async Task<string> GetIdByCodeAsync(
    this IPlatformQueryableRootRepository<Entity, string> repo, string code, CancellationToken ct = default)
    => await repo.FirstOrDefaultAsync(q => q.Where(Entity.CodeExpr(code)).Select(p => p.Id), ct).EnsureFound();

// Projection
await repo.FirstOrDefaultAsync(q => q.Where(expr).Select(e => e.Id), ct);
```

---

## Fluent Helpers

```csharp
// Mutation & transformation
await repo.GetByIdAsync(id).With(e => e.Name = newName).WithIf(cond, e => e.Status = Active);
await repo.GetByIdAsync(id).Then(e => e.Process()).ThenAsync(e => e.ValidateAsync(svc, ct));
await repo.GetByIdAsync(id).EnsureFound($"Not found: {id}");
await repo.GetByIdsAsync(ids, ct).EnsureFoundAllBy(x => x.Id, ids);

// Parallel operations
var (entity, files) = await (
    repo.CreateOrUpdateAsync(entity, ct),
    files.ParallelAsync(f => fileService.UploadAsync(f, ct))
);
var ids = await repo.GetByIdsAsync(ids, ct).ThenSelect(e => e.Id);
await items.ParallelAsync(item => ProcessAsync(item, ct), maxConcurrent: 10);

// Conditional actions
await repo.GetByIdAsync(id).PipeActionIf(cond, e => e.Update()).PipeActionAsyncIf(() => svc.Any(), e => e.Sync());
```

---

# §2. CQRS Queries

**File:** `UseCaseQueries/{Feature}/Get{Entity}ListQuery.cs`

## Paged Query Template

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

---

## GetQueryBuilder (Reusable Queries)

```csharp
var queryBuilder = repository.GetQueryBuilder((uow, q) => q
    .Where(e => e.CompanyId == RequestContext.CurrentCompanyId())
    .WhereIf(req.Statuses.Any(), e => req.Statuses.Contains(e.Status))
    .WhereIf(req.FilterIds.IsNotNullOrEmpty(), e => req.FilterIds!.Contains(e.Id))
    .WhereIf(req.FromDate.HasValue, e => e.CreatedDate >= req.FromDate)
    .WhereIf(req.ToDate.HasValue, e => e.CreatedDate <= req.ToDate)
    .PipeIf(req.SearchText.IsNotNullOrEmpty(), q =>
        searchService.Search(q, req.SearchText, Entity.DefaultFullTextSearchColumns())));
```

---

## Parallel Tuple Queries

```csharp
var (total, items) = await (
    repository.CountAsync((uow, q) => queryBuilder(uow, q), ct),
    repository.GetAllAsync((uow, q) => queryBuilder(uow, q)
        .OrderByDescending(e => e.CreatedDate)
        .PageBy(req.SkipCount, req.MaxResultCount), ct,
        e => e.RelatedEntity,     // Eager load
        e => e.AnotherRelated)
);
```

---

## Full-Text Search

```csharp
// In entity - define searchable columns
public static Expression<Func<Entity, object?>>[] DefaultFullTextSearchColumns()
    => [e => e.Name, e => e.Code, e => e.Description, e => e.Email];

// In query handler
.PipeIf(req.SearchText.IsNotNullOrEmpty(), q =>
    searchService.Search(
        q,
        req.SearchText,
        Entity.DefaultFullTextSearchColumns(),
        fullTextAccurateMatch: true,      // true=exact phrase, false=fuzzy
        includeStartWithProps: Entity.DefaultFullTextSearchColumns()  // For autocomplete
    ))
```

---

## Single Entity Query

```csharp
protected override async Task<GetEntityByIdQueryResult> HandleAsync(
    GetEntityByIdQuery req, CancellationToken ct)
{
    var entity = await repository.GetByIdAsync(req.Id, ct,
        e => e.RelatedEntity,
        e => e.Children)
        .EnsureFound($"Entity not found: {req.Id}");

    return new GetEntityByIdQueryResult
    {
        Entity = new EntityDto(entity)
            .WithRelated(entity.RelatedEntity)
            .WithChildren(entity.Children)
    };
}
```

---

## Aggregation Query

```csharp
var (total, items, statusCounts) = await (
    repository.CountAsync((uow, q) => queryBuilder(uow, q), ct),
    repository.GetAllAsync((uow, q) => queryBuilder(uow, q).PageBy(skip, take), ct),
    repository.GetAllAsync((uow, q) => queryBuilder(uow, q)
        .GroupBy(e => e.Status)
        .Select(g => new { Status = g.Key, Count = g.Count() }), ct)
);
```

---

## Query Patterns Summary

| Pattern | Usage | Example |
|---------|-------|---------|
| `GetQueryBuilder` | Reusable query | `repository.GetQueryBuilder((uow, q) => ...)` |
| `WhereIf` | Conditional filter | `.WhereIf(ids.Any(), e => ids.Contains(e.Id))` |
| `PipeIf` | Conditional transform | `.PipeIf(text != null, q => searchService.Search(...))` |
| `PageBy` | Pagination | `.PageBy(skip, take)` |
| Tuple await | Parallel queries | `var (count, items) = await (q1, q2)` |
| Eager load | Load relations | `GetByIdAsync(id, ct, e => e.Related)` |
| `.EnsureFound()` | Validate exists | `await repo.GetByIdAsync(id).EnsureFound()` |
| `.ThenValidateFoundAllAsync()` | Validate all IDs | `repo.GetByIdsAsync(ids).ThenValidateFoundAllAsync(ids, ...)` |

---

# §3. Entity Development

**File:** `{Service}.Domain/Entities/{Entity}.cs`

## Entity Base Classes

### Non-Audited Entity

```csharp
public class Employee : RootEntity<Employee, string>
{
    // No CreatedBy, UpdatedBy, CreatedDate, etc.
}
```

### Audited Entity (With Audit Trail)

```csharp
public class AuditedEmployee : RootAuditedEntity<AuditedEmployee, string, string>
{
    // Includes: CreatedBy, UpdatedBy, CreatedDate, UpdatedDate
}
```

---

## Complete Entity Template

```csharp
[TrackFieldUpdatedDomainEvent]  // Track all field changes
public sealed class Entity : RootEntity<Entity, string>
{
    // ═══════════════════════════════════════════════════════════════════════════
    // CORE PROPERTIES
    // ═══════════════════════════════════════════════════════════════════════════

    [TrackFieldUpdatedDomainEvent]  // Track specific field changes
    public string Name { get; set; } = "";

    public string Code { get; set; } = "";
    public string CompanyId { get; set; } = "";
    public EntityStatus Status { get; set; }
    public DateTime? EffectiveDate { get; set; }

    // ═══════════════════════════════════════════════════════════════════════════
    // NAVIGATION PROPERTIES
    // ═══════════════════════════════════════════════════════════════════════════

    [JsonIgnore]
    public Company? Company { get; set; }

    [JsonIgnore]
    public List<EntityChild>? Children { get; set; }

    // ═══════════════════════════════════════════════════════════════════════════
    // COMPUTED PROPERTIES (MUST have empty set { })
    // ═══════════════════════════════════════════════════════════════════════════

    [ComputedEntityProperty]
    public bool IsActive
    {
        get => Status == EntityStatus.Active && !IsDeleted;
        set { }  // Required empty setter for EF Core
    }

    [ComputedEntityProperty]
    public string DisplayName
    {
        get => $"{Code} - {Name}".Trim();
        set { }  // Required empty setter
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // STATIC EXPRESSIONS (For Repository Queries)
    // ═══════════════════════════════════════════════════════════════════════════

    // Simple filter expression
    public static Expression<Func<Entity, bool>> OfCompanyExpr(string companyId)
        => e => e.CompanyId == companyId;

    // Unique constraint expression
    public static Expression<Func<Entity, bool>> UniqueExpr(string companyId, string code)
        => e => e.CompanyId == companyId && e.Code == code;

    // Filter by status list
    public static Expression<Func<Entity, bool>> FilterByStatusExpr(List<EntityStatus> statuses)
    {
        var statusSet = statuses.ToHashSet();
        return e => e.Status.HasValue && statusSet.Contains(e.Status.Value);
    }

    // Composite expression with conditional
    public static Expression<Func<Entity, bool>> ActiveInCompanyExpr(string companyId, bool includeInactive = false)
        => OfCompanyExpr(companyId).AndAlsoIf(!includeInactive, () => e => e.IsActive);

    // Full-text search columns
    public static Expression<Func<Entity, object?>>[] DefaultFullTextSearchColumns()
        => [e => e.Name, e => e.Code, e => e.Description];

    // ═══════════════════════════════════════════════════════════════════════════
    // ASYNC EXPRESSIONS (When External Dependencies Needed)
    // ═══════════════════════════════════════════════════════════════════════════

    public static async Task<Expression<Func<Entity, bool>>> FilterWithLicenseExprAsync(
        IRepository<License> licenseRepo,
        string companyId,
        CancellationToken ct = default)
    {
        var hasLicense = await licenseRepo.HasLicenseAsync(companyId, ct);
        return hasLicense ? PremiumFilterExpr() : StandardFilterExpr();
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // VALIDATION METHODS
    // ═══════════════════════════════════════════════════════════════════════════

    public PlatformValidationResult ValidateCanBeUpdated()
    {
        return PlatformValidationResult.Valid()
            .And(() => !IsDeleted, "Entity is deleted")
            .And(() => Status != EntityStatus.Locked, "Entity is locked");
    }

    public async Task<PlatformValidationResult> ValidateAsync(
        IRepository<Entity> repository,
        CancellationToken ct = default)
    {
        return await PlatformValidationResult.Valid()
            .And(() => Name.IsNotNullOrEmpty(), "Name is required")
            .And(() => Code.IsNotNullOrEmpty(), "Code is required")
            .AndNotAsync(async () => await repository.AnyAsync(
                e => e.Id != Id && e.CompanyId == CompanyId && e.Code == Code, ct),
                "Code already exists");
    }

    // ═══════════════════════════════════════════════════════════════════════════
    // INSTANCE METHODS
    // ═══════════════════════════════════════════════════════════════════════════

    public void Activate() => Status = EntityStatus.Active;
    public void Deactivate() => Status = EntityStatus.Inactive;
}
```

---

## Expression Composition

| Pattern | Usage | Example |
|---------|-------|---------|
| `AndAlso` | Combine with AND | `expr1.AndAlso(expr2)` |
| `OrElse` | Combine with OR | `expr1.OrElse(expr2)` |
| `AndAlsoIf` | Conditional AND | `.AndAlsoIf(condition, () => expr)` |
| `OrElseIf` | Conditional OR | `.OrElseIf(condition, () => expr)` |

```csharp
// Composing multiple expressions
var expr = Entity.OfCompanyExpr(companyId)
    .AndAlso(Entity.FilterByStatusExpr(statuses))
    .AndAlsoIf(deptIds.Any(), () => Entity.FilterByDeptExpr(deptIds))
    .AndAlsoIf(searchText.IsNotNullOrEmpty(), () => Entity.SearchExpr(searchText));

// Complex expression
public static Expression<Func<E, bool>> ComplexExpr(int s, string c, int? m)
    => BaseExpr(s, c)
        .AndAlso(e => e.User!.IsActive)
        .AndAlsoIf(m != null, () => e => e.Start <= Clock.UtcNow.AddMonths(-m!.Value));
```

---

## Computed Property Rules

**MUST have empty setter `set { }`**

```csharp
// CORRECT
[ComputedEntityProperty]
public bool IsRoot
{
    get => Id == RootId;
    set { }  // Required for EF Core mapping
}

// WRONG - No setter causes EF Core issues
[ComputedEntityProperty]
public bool IsRoot => Id == RootId;
```

---

## DTO Mapping

```csharp
public class EmployeeDto : PlatformEntityDto<Employee, string>
{
    public EmployeeDto() { }
    public EmployeeDto(Employee e, User? u) : base(e) { FullName = e.FullName ?? u?.FullName ?? ""; }

    public string? Id { get; set; }
    public string FullName { get; set; } = "";
    public OrganizationDto? Company { get; set; }

    public EmployeeDto WithCompany(OrganizationalUnit c) { Company = new OrganizationDto(c); return this; }

    protected override object? GetSubmittedId() => Id;
    protected override string GenerateNewId() => Ulid.NewUlid().ToString();
    protected override Employee MapToEntity(Employee e, MapToEntityModes mode) { e.FullName = FullName; return e; }
}

// Value object DTO
public sealed class ConfigDto : PlatformDto<ConfigValue>
{
    public string ClientId { get; set; } = "";
    public override ConfigValue MapToObject() => new() { ClientId = ClientId };
}

// Usage
var dtos = employees.SelectList(e => new EmployeeDto(e, e.User).WithCompany(e.Company!));
```

---

## Static Validation Method

```csharp
public static List<string> ValidateEntity(Entity? e)
    => e == null ? ["Not found"] : !e.IsActive ? ["Inactive"] : [];
```

---

# §4. Entity Event Handlers (Side Effects)

**CRITICAL:** NEVER call side effects in command handlers!

**File:** `UseCaseEvents/{Feature}/Send{Action}On{Event}{Entity}EntityEventHandler.cs`

## Implementation Pattern

```csharp
internal sealed class SendNotificationOnCreateEntityEntityEventHandler
    : PlatformCqrsEntityEventApplicationHandler<Entity>  // Single generic parameter!
{
    private readonly INotificationService notificationService;
    private readonly IServiceRootRepository<Entity> repository;

    public SendNotificationOnCreateEntityEntityEventHandler(
        ILoggerFactory loggerFactory,
        IPlatformUnitOfWorkManager unitOfWorkManager,
        IServiceProvider serviceProvider,
        IPlatformRootServiceProvider rootServiceProvider,
        INotificationService notificationService,
        IServiceRootRepository<Entity> repository)
        : base(loggerFactory, unitOfWorkManager, serviceProvider, rootServiceProvider)
    {
        this.notificationService = notificationService;
        this.repository = repository;
    }

    // Filter: Which events to handle
    // NOTE: Must be public override async Task<bool> - NOT protected, NOT bool!
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Entity> @event)
    {
        // Skip during test data seeding
        if (@event.RequestContext.IsSeedingTestingData()) return false;

        // Only handle specific CRUD actions
        return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
    }

    protected override async Task HandleAsync(
        PlatformCqrsEntityEvent<Entity> @event,
        CancellationToken ct)
    {
        var entity = @event.EntityData;

        // Load additional data if needed
        var relatedData = await repository.GetByIdAsync(entity.Id, ct, e => e.Related);

        // Execute side effect
        await notificationService.SendAsync(new NotificationRequest
        {
            EntityId = entity.Id,
            EntityName = entity.Name,
            Action = "Created",
            UserId = @event.RequestContext.UserId()
        });
    }
}
```

---

## CRUD Action Filtering

### Single Action

```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Entity> @event)
{
    return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
}
```

### Multiple Actions

```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Entity> @event)
{
    return @event.CrudAction is PlatformCqrsEntityEventCrudAction.Created
        or PlatformCqrsEntityEventCrudAction.Updated;
}
```

### Updated with Specific Condition

```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Entity> @event)
{
    return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Updated
        && @event.EntityData.Status == Status.Published;
}
```

### Skip Test Data Seeding

```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Entity> @event)
{
    if (@event.RequestContext.IsSeedingTestingData()) return false;
    return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
}
```

---

## Accessing Event Data

| Property | Description |
|----------|-------------|
| `@event.EntityData` | The entity that triggered the event |
| `@event.CrudAction` | Created, Updated, or Deleted |
| `@event.RequestContext` | Request context with user/company info |
| `@event.RequestContext.UserId()` | User who triggered the change |
| `@event.RequestContext.CurrentCompanyId()` | Company context |

---

# §5. Data Migrations

## Migration Type Decision

```
Is this a schema change?
├── YES → EF Core Migration
│   ├── SQL Server: dotnet ef migrations add {Name}
│   └── PostgreSQL: dotnet ef migrations add {Name}
│
└── NO → Data Migration
    ├── MongoDB (simple, NO DI needed):
    │   └── PlatformMongoMigrationExecutor<TDbContext>
    │       ⚠️ NO constructor injection, NO RootServiceProvider
    │       Receives dbContext in Execute(TDbContext dbContext)
    │       Use for: field renames, index recreation, simple updates
    │
    ├── MongoDB (needs DI / cross-DB / paging):
    │   └── PlatformDataMigrationExecutor<MongoDbContext>
    │       ✅ Full DI via constructor, RootServiceProvider available
    │       Place in same project as MongoDbContext (scanned by assembly)
    │       Use for: cross-DB sync, complex transforms, service injection
    │
    ├── SQL/PostgreSQL:
    │   └── PlatformDataMigrationExecutor<EfCoreDbContext>
    │
    └── MongoDB index recreation only:
        └── PlatformMongoMigrationExecutor → dbContext.InternalEnsureIndexesAsync(recreate: true)
```

> **CRITICAL:** `PlatformMongoMigrationExecutor` uses `Activator.CreateInstance` — NO DI support.
> If you need DI (inject other DbContexts, repositories, services), use `PlatformDataMigrationExecutor<MongoDbContext>` instead.

---

## Pattern 1: EF Core Schema Migration

```bash
# Navigate to persistence project
cd src/Services/bravoGROWTH/Growth.Persistence

# Add migration
dotnet ef migrations add AddEmployeePhoneNumber

# Apply migration
dotnet ef database update

# Rollback last migration
dotnet ef migrations remove
```

```csharp
public partial class AddEmployeePhoneNumber : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<string>(
            name: "PhoneNumber",
            table: "Employees",
            type: "nvarchar(50)",
            maxLength: 50,
            nullable: true);

        migrationBuilder.CreateIndex(
            name: "IX_Employees_PhoneNumber",
            table: "Employees",
            column: "PhoneNumber");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropIndex(
            name: "IX_Employees_PhoneNumber",
            table: "Employees");

        migrationBuilder.DropColumn(
            name: "PhoneNumber",
            table: "Employees");
    }
}
```

---

## Pattern 2: Data Migration (SQL/PostgreSQL)

```csharp
public sealed class MigrateEmployeePhoneNumbers : PlatformDataMigrationExecutor<GrowthDbContext>
{
    public override string Name => "20251015000000_MigrateEmployeePhoneNumbers";
    public override DateTime? OnlyForDbsCreatedBeforeDate => new(2025, 10, 15);
    public override bool AllowRunInBackgroundThread => true;

    private readonly IGrowthRootRepository<Employee> employeeRepo;
    private const int PageSize = 200;

    public override async Task Execute(GrowthDbContext dbContext)
    {
        var queryBuilder = employeeRepo.GetQueryBuilder((uow, q) =>
            q.Where(e => e.PhoneNumber == null && e.LegacyPhone != null));

        var totalCount = await employeeRepo.CountAsync((uow, q) => queryBuilder(uow, q));

        if (totalCount == 0)
        {
            Logger.LogInformation("No employees need phone migration");
            return;
        }

        Logger.LogInformation("Migrating phone numbers for {Count} employees", totalCount);

        await RootServiceProvider.ExecuteInjectScopedPagingAsync(
            maxItemCount: totalCount,
            pageSize: PageSize,
            processingDelegate: ExecutePaging,
            queryBuilder);
    }

    private static async Task<List<Employee>> ExecutePaging(
        int skip,
        int take,
        Func<IPlatformUnitOfWork, IQueryable<Employee>, IQueryable<Employee>> queryBuilder,
        IGrowthRootRepository<Employee> repo,
        IPlatformUnitOfWorkManager uowManager)
    {
        using var unitOfWork = uowManager.Begin();

        var employees = await repo.GetAllAsync((uow, q) =>
            queryBuilder(uow, q)
                .OrderBy(e => e.Id)
                .Skip(skip)
                .Take(take));

        if (employees.IsEmpty()) return employees;

        foreach (var employee in employees)
        {
            employee.PhoneNumber = NormalizePhoneNumber(employee.LegacyPhone);
        }

        await repo.UpdateManyAsync(
            employees,
            dismissSendEvent: true,
            checkDiff: false);

        await unitOfWork.CompleteAsync();

        return employees;
    }
}
```

---

## Pattern 3: MongoDB Migration (Simple — No DI)

> **⚠️ `PlatformMongoMigrationExecutor` has NO constructor injection and NO `RootServiceProvider`.**
> Access collections via `dbContext` (e.g., `dbContext.UserCollection`, `dbContext.GetCollection<T>()`).

```csharp
// Field rename migration — access collections via dbContext parameter
public sealed class MigrateFieldName : PlatformMongoMigrationExecutor<SurveyPlatformMongoDbContext>
{
    public override string Name => "20251015_MigrateFieldName";
    public override DateTime? OnlyForDbInitBeforeDate => new DateTime(2025, 10, 15);

    public override async Task Execute(SurveyPlatformMongoDbContext dbContext)
    {
        var collection = dbContext.GetCollection<BsonDocument>("distributions");
        var filter = Builders<BsonDocument>.Filter.Exists("OldFieldName");

        var pipeline = PipelineDefinition<BsonDocument, BsonDocument>.Create(
            [new BsonDocument("$set", new BsonDocument("NewFieldName", "$OldFieldName"))]);

        await collection.UpdateManyAsync(filter, pipeline);
    }
}

// Index recreation migration — simplest pattern
public sealed class RecreateIndexes : PlatformMongoMigrationExecutor<SurveyPlatformMongoDbContext>
{
    public override string Name => "20251015_RecreateIndexes";
    public override DateTime? OnlyForDbInitBeforeDate => new DateTime(2025, 10, 15);

    public override async Task Execute(SurveyPlatformMongoDbContext dbContext)
    {
        await dbContext.InternalEnsureIndexesAsync(recreate: true);
    }
}
```

---

## Pattern 4: Cross-Service Data Sync (One-Time)

```csharp
public sealed class SyncEmployeesFromAccounts : PlatformDataMigrationExecutor<GrowthDbContext>
{
    public override string Name => "20251015000000_SyncEmployeesFromAccounts";
    public override DateTime? OnlyForDbsCreatedBeforeDate => new(2025, 10, 15);

    public override async Task Execute(GrowthDbContext dbContext)
    {
        var sourceEmployees = await accountsDbContext.Employees
            .Where(e => e.CreatedDate < OnlyForDbsCreatedBeforeDate)
            .AsNoTracking()
            .ToListAsync();

        Logger.LogInformation("Syncing {Count} employees from Accounts", sourceEmployees.Count);

        var targetEmployees = sourceEmployees.Select(MapToGrowthEmployee).ToList();

        await RootServiceProvider.ExecuteInjectScopedPagingAsync(
            maxItemCount: targetEmployees.Count,
            pageSize: 100,
            async (skip, take, repo, uow) =>
            {
                var batch = targetEmployees.Skip(skip).Take(take).ToList();
                await repo.CreateManyAsync(batch, dismissSendEvent: true);
                return batch;
            });
    }
}
```

---

## Pattern 5: Cross-DB Data Migration to MongoDB (DI-Supported)

> **Use when:** You need to read from a SQL/PostgreSQL DB and write to MongoDB.
> Must be placed in the **same project** as the MongoDbContext (assembly scanning).

```csharp
// Real example: bravoSURVEYS — backfill UserCompany.IsActive from Accounts
public sealed class MigrateUserCompanyIsActiveFromAccountsDbMigration
    : PlatformDataMigrationExecutor<SurveyPlatformMongoDbContext>  // ← MongoDB context
{
    private const int PageSize = 100;
    private readonly AccountsPlatformDbContext accountsPlatformDbContext;  // ← DI works!

    public MigrateUserCompanyIsActiveFromAccountsDbMigration(
        IPlatformRootServiceProvider rootServiceProvider,
        AccountsPlatformDbContext accountsPlatformDbContext)  // ← Constructor injection
        : base(rootServiceProvider)
    {
        this.accountsPlatformDbContext = accountsPlatformDbContext;
    }

    public override string Name => "20260206000001_MigrateUserCompanyIsActiveFromAccountsDb";
    public override DateTime? OnlyForDbsCreatedBeforeDate => new(2026, 02, 06);
    public override bool AllowRunInBackgroundThread => true;

    public override async Task Execute(SurveyPlatformMongoDbContext dbContext)
    {
        var totalCount = await accountsPlatformDbContext
            .GetQuery<AccountUserCompanyInfo>()
            .EfCoreCountAsync();

        if (totalCount == 0) return;

        await RootServiceProvider.ExecuteInjectScopedPagingAsync(
            maxItemCount: totalCount,
            pageSize: PageSize,
            MigrateUserCompanyIsActivePaging);  // Static method, DI-resolved params
    }

    // Static paging: first 2 params MUST be (int skipCount, int pageSize)
    private static async Task MigrateUserCompanyIsActivePaging(
        int skipCount,
        int pageSize,
        AccountsPlatformDbContext accountsPlatformDbContext,  // ← DI-resolved
        SurveyPlatformMongoDbContext surveyDbContext)          // ← DI-resolved
    {
        // 1. Read from SQL/PostgreSQL
        var userCompanyInfos = await accountsPlatformDbContext
            .GetQuery<AccountUserCompanyInfo>()
            .OrderBy(p => p.Id)
            .Skip(skipCount)
            .Take(pageSize)
            .EfCoreToListAsync();

        if (userCompanyInfos.Count == 0) return;

        // 2. Group for efficient lookup
        var infoByUserId = userCompanyInfos
            .GroupBy(p => p.UserId)
            .ToDictionary(g => g.Key, g => g.ToList());

        // 3. Read matching users from MongoDB
        var userIds = infoByUserId.Keys.ToList();
        var filter = Builders<User>.Filter.In(u => u.ExternalId, userIds);
        var users = await surveyDbContext.UserCollection.Find(filter).ToListAsync();

        // 4. Build bulk update operations
        var bulkUpdates = new List<WriteModel<User>>();

        foreach (var user in users)
        {
            if (!infoByUserId.TryGetValue(user.ExternalId, out var companyInfos)) continue;

            var updated = false;
            foreach (var company in user.Companies)
            {
                var match = companyInfos.FirstOrDefault(ci => ci.CompanyId == company.CompanyId);
                if (match != null && company.IsActive != match.IsActive)
                {
                    company.IsActive = match.IsActive;
                    updated = true;
                }
            }

            if (updated)
            {
                bulkUpdates.Add(new UpdateOneModel<User>(
                    Builders<User>.Filter.Eq(u => u.Id, user.Id),
                    Builders<User>.Update.Set(u => u.Companies, user.Companies)));
            }
        }

        // 5. Batch write to MongoDB
        if (bulkUpdates.Count > 0)
            await surveyDbContext.UserCollection.BulkWriteAsync(bulkUpdates);
    }
}
```

---

## Scrolling vs Paging

```csharp
// PAGING: When skip/take stays consistent (items don't disappear)
await RootServiceProvider.ExecuteInjectScopedPagingAsync(...);

// SCROLLING: When processed items excluded from next query
await UnitOfWorkManager.ExecuteInjectScopedScrollingPagingAsync(...);
```

---

## Key Migration Options

| Option | Purpose | When to Use |
|--------|---------|-------------|
| `OnlyForDbsCreatedBeforeDate` | Target specific DBs | Migrating existing data only |
| `AllowRunInBackgroundThread` | Non-blocking | Large migrations that can run async |
| `dismissSendEvent: true` | Skip entity events | Data migrations (avoid event storms) |
| `checkDiff: false` | Skip change detection | Bulk updates (performance) |

---

# §6. Background Jobs

## Job Type Decision Tree

```
Does processing affect the query result?
├── NO → Simple Paged (skip/take stays consistent)
│   └── Use: PlatformApplicationPagedBackgroundJobExecutor
│
└── YES → Scrolling needed (processed items excluded)
    │
    └── Is this multi-tenant (company-based)?
        ├── YES → Batch Scrolling (batch by company, scroll within)
        │   └── Use: PlatformApplicationBatchScrollingBackgroundJobExecutor
        │
        └── NO → Simple Scrolling
            └── Use: ExecuteInjectScopedScrollingPagingAsync
```

---

## Pattern 1: Simple Paged Job

```csharp
[PlatformRecurringJob("0 3 * * *")]  // Daily at 3 AM
public sealed class ProcessPendingItemsJob : PlatformApplicationPagedBackgroundJobExecutor
{
    private readonly IServiceRepository<Item> repository;

    protected override int PageSize => 50;

    private IQueryable<Item> QueryBuilder(IQueryable<Item> query)
        => query.Where(x => x.Status == Status.Pending);

    protected override async Task<int> MaxItemsCount(
        PlatformApplicationPagedBackgroundJobParam<object?> param)
    {
        return await repository.CountAsync((uow, q) => QueryBuilder(q));
    }

    protected override async Task ProcessPagedAsync(
        int? skip,
        int? take,
        object? param,
        IServiceProvider serviceProvider,
        IPlatformUnitOfWorkManager unitOfWorkManager)
    {
        var items = await repository.GetAllAsync((uow, q) =>
            QueryBuilder(q)
                .OrderBy(x => x.CreatedDate)
                .PageBy(skip, take));

        await items.ParallelAsync(async item =>
        {
            item.Process();
            await repository.UpdateAsync(item);
        }, maxConcurrent: 5);
    }
}
```

---

## Pattern 2: Batch Scrolling Job (Multi-Tenant)

```csharp
[PlatformRecurringJob("0 0 * * *")]  // Daily at midnight
public sealed class SyncCompanyDataJob
    : PlatformApplicationBatchScrollingBackgroundJobExecutor<Entity, string>
{
    protected override int BatchKeyPageSize => 50;   // Companies per page
    protected override int BatchPageSize => 25;       // Entities per company batch

    protected override IQueryable<Entity> EntitiesQueryBuilder(
        IQueryable<Entity> query,
        object? param,
        string? batchKey = null)
    {
        return query
            .Where(e => e.NeedsSync)
            .WhereIf(batchKey != null, e => e.CompanyId == batchKey)
            .OrderBy(e => e.Id);
    }

    protected override IQueryable<string> EntitiesBatchKeyQueryBuilder(
        IQueryable<Entity> query,
        object? param,
        string? batchKey = null)
    {
        return EntitiesQueryBuilder(query, param, batchKey)
            .Select(e => e.CompanyId)
            .Distinct();
    }

    protected override async Task ProcessEntitiesAsync(
        List<Entity> entities,
        string batchKey,  // CompanyId
        object? param,
        IServiceProvider serviceProvider)
    {
        await entities.ParallelAsync(async entity =>
        {
            entity.MarkSynced();
            await repository.UpdateAsync(entity);
        }, maxConcurrent: 1);
    }
}
```

---

## Pattern 3: Master Job (Schedules Child Jobs)

```csharp
[PlatformRecurringJob("0 6 * * *")]
public sealed class MasterSchedulerJob : PlatformApplicationBackgroundJobExecutor
{
    public override async Task ProcessAsync(object? param)
    {
        var companies = await companyRepo.GetAllAsync(c => c.IsActive);
        var dateRange = DateRangeBuilder.BuildDateRange(
            Clock.UtcNow.AddDays(-7),
            Clock.UtcNow);

        await companies.ParallelAsync(async company =>
        {
            await dateRange.ParallelAsync(async date =>
            {
                await BackgroundJobScheduler.Schedule<ChildProcessingJob, ChildJobParam>(
                    Clock.UtcNow,
                    new ChildJobParam
                    {
                        CompanyId = company.Id,
                        ProcessDate = date
                    });
            });
        }, maxConcurrent: 10);
    }
}
```

---

## Cron Schedule Reference

| Schedule | Cron Expression | Description |
|----------|-----------------|-------------|
| Every 5 min | `*/5 * * * *` | Every 5 minutes |
| Hourly | `0 * * * *` | Top of every hour |
| Daily midnight | `0 0 * * *` | 00:00 daily |
| Daily 3 AM | `0 3 * * *` | 03:00 daily |
| Weekly Sunday | `0 0 * * 0` | Midnight Sunday |
| Monthly 1st | `0 0 1 * *` | Midnight, 1st day |

---

## Job Attributes

```csharp
// Basic recurring job
[PlatformRecurringJob("0 3 * * *")]

// With startup execution
[PlatformRecurringJob("5 0 * * *", executeOnStartUp: true)]

// Disabled (for manual or event-triggered)
[PlatformRecurringJob(isDisabled: true)]
```

---

# §7. Message Bus

## Message Definition

```csharp
// In PlatformExampleApp.Shared/CrossServiceMessages/
public sealed class EmployeeEntityEventBusMessage
    : PlatformCqrsEntityEventBusMessage<EmployeeEventData, string>
{
    public EmployeeEntityEventBusMessage() { }

    public EmployeeEntityEventBusMessage(
        PlatformCqrsEntityEvent<Employee> entityEvent,
        EmployeeEventData entityData)
        : base(entityEvent, entityData)
    {
    }
}

public sealed class EmployeeEventData
{
    public string Id { get; set; } = "";
    public string FullName { get; set; } = "";
    public string Email { get; set; } = "";
    public string CompanyId { get; set; } = "";
    public bool IsDeleted { get; set; }

    public EmployeeEventData() { }
    public EmployeeEventData(Employee entity) { Id = entity.Id; FullName = entity.FullName; }

    public TargetEmployee ToEntity() => new TargetEmployee { SourceId = Id, FullName = FullName };
    public TargetEmployee UpdateEntity(TargetEmployee existing) { existing.FullName = FullName; return existing; }
}
```

---

## Entity Event Producer

```csharp
internal sealed class EmployeeEntityEventBusMessageProducer
    : PlatformCqrsEntityEventBusMessageProducer<EmployeeEntityEventBusMessage, Employee, string>
{
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Employee> @event)
    {
        if (@event.RequestContext.IsSeedingTestingData()) return false;
        return @event.EntityData.IsActive || @event.CrudAction == PlatformCqrsEntityEventCrudAction.Deleted;
    }

    protected override Task<EmployeeEntityEventBusMessage> BuildMessageAsync(
        PlatformCqrsEntityEvent<Employee> @event,
        CancellationToken ct)
    {
        return Task.FromResult(new EmployeeEntityEventBusMessage(
            @event,
            new EmployeeEventData(@event.EntityData)));
    }
}
```

---

## Entity Event Consumer

```csharp
internal sealed class UpsertOrDeleteEmployeeOnEmployeeEntityEventBusConsumer
    : PlatformApplicationMessageBusConsumer<EmployeeEntityEventBusMessage>
{
    private readonly ITargetServiceRepository<TargetEmployee> employeeRepo;
    private readonly ITargetServiceRepository<Company> companyRepo;

    public override async Task<bool> HandleWhen(
        EmployeeEntityEventBusMessage message,
        string routingKey) => true;

    public override async Task HandleLogicAsync(
        EmployeeEntityEventBusMessage message,
        string routingKey)
    {
        var payload = message.Payload;
        var entityData = payload.EntityData;

        // Wait for dependencies
        var companyMissing = await Util.TaskRunner
            .TryWaitUntilAsync(
                () => companyRepo.AnyAsync(c => c.Id == entityData.CompanyId),
                maxWaitSeconds: message.IsForceSyncDataRequest() ? 30 : 300)
            .Then(found => !found);

        if (companyMissing) return;

        // Handle delete
        if (payload.CrudAction == PlatformCqrsEntityEventCrudAction.Deleted ||
            (payload.CrudAction == PlatformCqrsEntityEventCrudAction.Updated && entityData.IsDeleted))
        {
            await employeeRepo.DeleteAsync(entityData.Id);
            return;
        }

        // Handle create/update
        var existing = await employeeRepo.FirstOrDefaultAsync(e => e.SourceId == entityData.Id);

        if (existing == null)
        {
            await employeeRepo.CreateAsync(
                entityData.ToEntity()
                    .With(e => e.LastMessageSyncDate = message.CreatedUtcDate));
        }
        else if (existing.LastMessageSyncDate <= message.CreatedUtcDate)
        {
            await employeeRepo.UpdateAsync(
                entityData.UpdateEntity(existing)
                    .With(e => e.LastMessageSyncDate = message.CreatedUtcDate));
        }
    }
}
```

---

## Message Naming Convention

| Type | Producer Role | Pattern | Example |
|------|---------------|---------|---------|
| Event | Leader | `<ServiceName><Feature><Action>EventBusMessage` | `CandidateJobBoardApiSyncCompletedEventBusMessage` |
| Request | Follower | `<ConsumerServiceName><Feature>RequestBusMessage` | `JobCreateNonexistentJobsRequestBusMessage` |

**Consumer Naming:** Consumer class name = Message class name + `Consumer` suffix

---

## Key Message Bus Patterns

### Wait for Dependencies

```csharp
var found = await Util.TaskRunner.TryWaitUntilAsync(
    () => companyRepo.AnyAsync(c => c.Id == companyId),
    maxWaitSeconds: 300);

if (!found) return;
```

### Prevent Race Conditions

```csharp
if (existing.LastMessageSyncDate <= message.CreatedUtcDate)
{
    await repository.UpdateAsync(existing.With(e =>
        e.LastMessageSyncDate = message.CreatedUtcDate));
}
```

---

# Anti-Patterns Catalog

| Don't | Do | Pattern |
|-------|-----|---------|
| `throw new ValidationException()` | `PlatformValidationResult` fluent API | Commands |
| Side effects in command handler | Entity Event Handler in `UseCaseEvents/` | Side Effects |
| Direct cross-service DB access | Message bus | Cross-Service |
| DTO mapping in handler | `PlatformEntityDto.MapToEntity()` | DTOs |
| Separate Command/Handler files | ONE file: Command + Result + Handler | CQRS |
| `protected bool HandleWhen()` | `public override async Task<bool> HandleWhen()` | Events |
| Two generic parameters in event handler | Single generic: `<Entity>` | Events |
| Computed property without `set { }` | Add empty setter | Entities |
| Missing `[JsonIgnore]` on navigation | Add `[JsonIgnore]` | Entities |
| No dependency waiting in consumer | `TryWaitUntilAsync` | Message Bus |
| No race condition handling | Check `LastMessageSyncDate` | Message Bus |
| Only check `Deleted` action | Also check soft delete flag | Message Bus |
| Use `PlatformMongoMigrationExecutor` with DI | Use `PlatformDataMigrationExecutor<MongoDbContext>` | Migrations |
| Unbounded parallelism | `maxConcurrent: 5` | Jobs |
| Wrong pagination for changing data | Use scrolling pattern | Jobs |

---

## Checklist

- [ ] Service-specific repository (`IPlatformQueryableRootRepository<T>`)
- [ ] Fluent validation (`.And()`, `.AndAsync()`) — NEVER throw
- [ ] No side effects in command handlers (use Entity Event Handlers)
- [ ] DTO mapping in DTO class (`MapToEntity()`, `MapToObject()`)
- [ ] Cross-service uses message bus (NEVER direct DB access)
- [ ] Jobs have `maxConcurrent` parameter for parallelism
- [ ] Migrations use `dismissSendEvent: true`, `checkDiff: false`
- [ ] MongoDB migrations: `PlatformMongoMigrationExecutor` (simple) vs `PlatformDataMigrationExecutor<MongoDbContext>` (DI)
- [ ] Database indexes configured for Entity static expression properties (see `.ai/docs/backend-code-patterns.md` Pattern 17)

---

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
