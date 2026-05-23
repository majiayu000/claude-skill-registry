---
name: data-migration
description: Use when creating data migrations, schema migrations, or data transformation scripts for MongoDB or SQL databases.
---

# Data Migration Development Workflow

## When to Use This Skill
- Schema changes (add/remove columns, tables)
- Data transformation (backfill, format changes)
- Cross-database data sync (one-time)
- Cleanup/maintenance migrations

## Migration Type Decision

```
Is this a schema change?
├── YES → EF Core Migration
│   ├── SQL Server: dotnet ef migrations add {Name}
│   └── PostgreSQL: dotnet ef migrations add {Name}
│
└── NO → Data Migration
    ├── MongoDB: PlatformMongoMigrationExecutor<TDbContext>
    └── SQL/PostgreSQL: PlatformDataMigrationExecutor<TDbContext>
```

## File Locations

### EF Core Schema Migrations
```
{Service}.Persistence/
└── Migrations/
    └── {Timestamp}_{MigrationName}.cs
```

### Data Migrations
```
{Service}.Application/
└── DataMigrations/
    └── {Date}_{MigrationName}DataMigration.cs
```

## Pattern 1: EF Core Schema Migration

```bash
# Navigate to persistence project
cd src/PlatformExampleApp/PlatformExampleApp.TextSnippet.Persistence

# Add migration
dotnet ef migrations add AddEntityPhoneNumber

# Apply migration
dotnet ef database update

# Rollback last migration
dotnet ef migrations remove
```

```csharp
// Generated migration (customize if needed)
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

        // Add index
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

## Pattern 2: Data Migration (SQL/PostgreSQL)

```csharp
public sealed class MigrateEntityData : PlatformDataMigrationExecutor<YourDbContext>
{
    // Migration identifier (format: YYYYMMDDHHMMSS_Name)
    public override string Name => "20251015000000_MigrateEntityData";

    // Only run on databases created before this date
    public override DateTime? OnlyForDbsCreatedBeforeDate => new(2025, 10, 15);

    // Can run in background thread (won't block startup)
    public override bool AllowRunInBackgroundThread => true;

    private readonly IPlatformQueryableRootRepository<Entity, string> entityRepo;
    private const int PageSize = 200;

    public MigrateEntityData(
        ILoggerFactory loggerFactory,
        IPlatformRootServiceProvider rootServiceProvider,
        IPlatformQueryableRootRepository<Entity, string> entityRepo)
        : base(loggerFactory, rootServiceProvider)
    {
        this.entityRepo = entityRepo;
    }

    public override async Task Execute(YourDbContext dbContext)
    {
        // Build filter for items needing migration
        var queryBuilder = entityRepo.GetQueryBuilder((uow, q) =>
            q.Where(e => e.NewField == null && e.LegacyField != null));

        var totalCount = await entityRepo.CountAsync((uow, q) => queryBuilder(uow, q));

        if (totalCount == 0)
        {
            Logger.LogInformation("No entities need migration");
            return;
        }

        Logger.LogInformation("Migrating data for {Count} entities", totalCount);

        // Process in pages
        await RootServiceProvider.ExecuteInjectScopedPagingAsync(
            maxItemCount: totalCount,
            pageSize: PageSize,
            processingDelegate: ExecutePaging,
            queryBuilder);
    }

    private static async Task<List<Entity>> ExecutePaging(
        int skip,
        int take,
        Func<IPlatformUnitOfWork, IQueryable<Entity>, IQueryable<Entity>> queryBuilder,
        IPlatformQueryableRootRepository<Entity, string> repo,
        IPlatformUnitOfWorkManager uowManager)
    {
        using var unitOfWork = uowManager.Begin();

        var entities = await repo.GetAllAsync((uow, q) =>
            queryBuilder(uow, q)
                .OrderBy(e => e.Id)
                .Skip(skip)
                .Take(take));

        if (entities.IsEmpty()) return entities;

        // Transform data
        foreach (var entity in entities)
        {
            entity.NewField = TransformData(entity.LegacyField);
        }

        // Update without sending events (data migration)
        await repo.UpdateManyAsync(
            entities,
            dismissSendEvent: true,
            checkDiff: false);

        await unitOfWork.CompleteAsync();

        return entities;
    }

    private static string TransformData(string? legacyField)
    {
        if (string.IsNullOrEmpty(legacyField)) return "";
        // Transformation logic
        return legacyField.Trim();
    }
}
```

## Pattern 3: MongoDB Migration

```csharp
public sealed class MigrateDocumentSchema : PlatformMongoMigrationExecutor<ServiceDbContext>
{
    public override string Name => "20251015_MigrateDocumentSchema";

    private readonly IMongoCollection<BsonDocument> collection;
    private const int BatchSize = 100;

    public override async Task Execute()
    {
        var filter = Builders<BsonDocument>.Filter.Exists("oldFieldName");

        var totalCount = await collection.CountDocumentsAsync(filter);
        var processed = 0;

        while (processed < totalCount)
        {
            var documents = await collection
                .Find(filter)
                .Limit(BatchSize)
                .ToListAsync();

            if (documents.Count == 0) break;

            var bulkOps = documents.Select(doc =>
            {
                var update = Builders<BsonDocument>.Update
                    .Set("newFieldName", doc["oldFieldName"])
                    .Unset("oldFieldName");

                return new UpdateOneModel<BsonDocument>(
                    Builders<BsonDocument>.Filter.Eq("_id", doc["_id"]),
                    update);
            }).ToList();

            await collection.BulkWriteAsync(bulkOps);

            processed += documents.Count;
            Logger.LogInformation("Migrated {Processed}/{Total} documents",
                processed, totalCount);
        }
    }
}
```

## Pattern 4: Cross-Service Data Sync (One-Time)

```csharp
public sealed class SyncDataFromSourceToTarget : PlatformDataMigrationExecutor<TargetDbContext>
{
    public override string Name => "20251015000000_SyncDataFromSourceToTarget";

    // Only for DBs created before sync was implemented
    public override DateTime? OnlyForDbsCreatedBeforeDate => new(2025, 10, 15);

    public override async Task Execute(TargetDbContext dbContext)
    {
        // Get source data (from source service via shared connection or API)
        var sourceEntities = await sourceDbContext.Entities
            .Where(e => e.CreatedDate < OnlyForDbsCreatedBeforeDate)
            .AsNoTracking()
            .ToListAsync();

        Logger.LogInformation("Syncing {Count} entities from source", sourceEntities.Count);

        // Map and create in target
        var targetEntities = sourceEntities.Select(MapToTargetEntity).ToList();

        await RootServiceProvider.ExecuteInjectScopedPagingAsync(
            maxItemCount: targetEntities.Count,
            pageSize: 100,
            async (skip, take, repo, uow) =>
            {
                var batch = targetEntities.Skip(skip).Take(take).ToList();

                await repo.CreateManyAsync(batch, dismissSendEvent: true);

                return batch;
            });
    }

    private TargetEntity MapToTargetEntity(SourceEntity source) => new TargetEntity
    {
        Id = source.Id,
        Name = source.Name,
        Email = source.Email,
        // ... map other fields
    };
}
```

## Key Options & Flags

| Option                        | Purpose               | When to Use                          |
| ----------------------------- | --------------------- | ------------------------------------ |
| `OnlyForDbsCreatedBeforeDate` | Target specific DBs   | When migrating existing data only    |
| `AllowRunInBackgroundThread`  | Non-blocking          | Large migrations that can run async  |
| `dismissSendEvent: true`      | Skip entity events    | Data migrations (avoid event storms) |
| `checkDiff: false`            | Skip change detection | Bulk updates (performance)           |

## Scrolling vs Paging

```csharp
// PAGING: When skip/take stays consistent
// (items don't disappear from query after processing)
await RootServiceProvider.ExecuteInjectScopedPagingAsync(...);

// SCROLLING: When processed items excluded from next query
// (e.g., status change means item no longer matches filter)
await UnitOfWorkManager.ExecuteInjectScopedScrollingPagingAsync(...);
```

## Anti-Patterns to AVOID

:x: **No paging for large datasets**
```csharp
// WRONG - memory issues
var all = await repo.GetAllAsync();
foreach (var item in all) { }

// CORRECT - paged processing
await RootServiceProvider.ExecuteInjectScopedPagingAsync(...);
```

:x: **Sending events during migration**
```csharp
// WRONG - event storm, triggers consumers
await repo.UpdateManyAsync(items);

// CORRECT - suppress events
await repo.UpdateManyAsync(items, dismissSendEvent: true, checkDiff: false);
```

:x: **Missing unit of work**
```csharp
// WRONG - no transaction control
await repo.UpdateAsync(item);
await repo.UpdateAsync(anotherItem);

// CORRECT - explicit transaction
using var uow = uowManager.Begin();
await repo.UpdateManyAsync(items);
await uow.CompleteAsync();
```

:x: **Wrong migration for ongoing sync**
```csharp
// WRONG - using data migration for continuous sync
// Data migrations run once at startup

// CORRECT - use message bus consumers for ongoing sync
```

## Verification Checklist
- [ ] Migration name follows format: `{YYYYMMDDHHMMSS}_{Name}`
- [ ] `OnlyForDbsCreatedBeforeDate` set appropriately
- [ ] `AllowRunInBackgroundThread` considered for large migrations
- [ ] Paging/scrolling strategy appropriate for data changes
- [ ] `dismissSendEvent: true` used to prevent event storms
- [ ] Unit of work used for transaction control
- [ ] Logging added for progress monitoring
- [ ] Rollback strategy documented (if applicable)
