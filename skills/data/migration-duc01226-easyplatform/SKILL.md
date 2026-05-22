---
name: migration
description: "[Implementation] ⚡⚡ Create or run database migrations"
argument-hint: [add <name> | update | list | rollback | migration-description]
infer: true
---

# Migration: $ARGUMENTS

Create or run database migrations following EasyPlatform patterns.

## Summary

**Goal:** Create idempotent data or schema migrations following EasyPlatform conventions (EF Core, PlatformDataMigration, MongoDB).

| Step | Action | Key Notes |
|------|--------|-----------|
| 1 | Analyze requirements | Identify migration type: EF Core schema, data, or MongoDB |
| 2 | Design migration | Plan rollback, paging for large datasets, performance |
| 3 | Generate migration | Follow `YYYYMMDDHHMMSS_Name` naming convention |
| 4 | Verify | Idempotent, paged, proper error handling, `OnlyForDbsCreatedBeforeDate` set |
| 5 | Wait for approval | Present design before creating files |

**Key Principles:**
- Use paging (200-500 page size) for large datasets with `dismissSendEvent: true`
- Migrations must be idempotent (safe to run multiple times)
- Never create files without explicit user approval

## Quick Commands (db-migrate)

Parse `$ARGUMENTS` for quick operations:
- `add <name>` → Create new EF Core migration
- `update` → Apply pending migrations
- `list` → List all migrations and status
- `rollback` → Revert last migration
- No argument or description → Create new migration (proceed to Phase 1)

**Database providers:**
- SQL Server: `PlatformExampleApp.TextSnippet.Persistence`
- PostgreSQL: `PlatformExampleApp.TextSnippet.Persistence.PostgreSql`
- MongoDB: Uses `PlatformMongoMigrationExecutor` (code-based, runs on startup)
  - Location: `*.Persistence.Mongo/Migrations/`

**EF Core quick commands:**
```bash
# Add migration
cd src/Backend/PlatformExampleApp.TextSnippet.Persistence
dotnet ef migrations add <MigrationName> --startup-project ../PlatformExampleApp.TextSnippet.Api

# Apply migrations
dotnet ef database update --startup-project ../PlatformExampleApp.TextSnippet.Api

# List migrations
dotnet ef migrations list --startup-project ../PlatformExampleApp.TextSnippet.Api
```

**Safety:** Warn before applying to production. Show pending changes. Recommend backup before destructive operations.

---

## Phase 1: Analyze Requirements

1. **Parse migration description** from: $ARGUMENTS
2. **Identify migration type:**
    - Schema migration (EF Core) - for SQL Server/PostgreSQL table changes
    - Data migration (PlatformDataMigrationExecutor) - for data transformations
    - MongoDB migration (PlatformMongoMigrationExecutor) - for MongoDB changes

3. **Search for existing patterns:**
    - `src/Backend/*/Persistence/Migrations/` for schema migrations
    - Search for `PlatformDataMigrationExecutor` implementations

## Phase 2: Design Migration

1. **Determine affected entities and tables**
2. **Plan rollback strategy if applicable**
3. **Consider data volume and performance:**
    - Use paging for large datasets (PageSize: 200-500)
    - Set `dismissSendEvent: true` if entity events not needed
    - Use `checkDiff: false` for bulk updates

## Phase 3: Generate Migration

Follow naming convention: `YYYYMMDDHHMMSS_MigrationName`

**For EF Core Schema Migration:**

```bash
dotnet ef migrations add MigrationName --project src/Backend/Service}.Persistence
```

**For Data Migration (SQL Server/PostgreSQL):**

```csharp
public class YYYYMMDDHHMMSS_MigrationName : PlatformDataMigrationExecutor<{Service}DbContext>
{
    public override string Name => "YYYYMMDDHHMMSS_MigrationName";
    public override DateTime? OnlyForDbsCreatedBeforeDate => new(YYYY, MM, DD);
    public override bool AllowRunInBackgroundThread => true;

    public override async Task Execute({Service}DbContext dbContext)
    {
        var queryBuilder = repository.GetQueryBuilder(q => q.Where(FilterExpr()));
        await RootServiceProvider.ExecuteInjectScopedPagingAsync(
            maxItemCount: await repository.CountAsync(q => queryBuilder(q)),
            pageSize: 200,
            ExecutePaging,
            queryBuilder);
    }

    private static async Task<List<Entity>> ExecutePaging(
        int skip, int take,
        Func<IQueryable<Entity>, IQueryable<Entity>> qb,
        IRepo<Entity> repo,
        IPlatformUnitOfWorkManager uow)
    {
        using var unitOfWork = uow.Begin();
        var items = await repo.GetAllAsync(q => qb(q).OrderBy(e => e.Id).Skip(skip).Take(take));
        // Apply transformations
        await repo.UpdateManyAsync(items, dismissSendEvent: true, checkDiff: false);
        await unitOfWork.CompleteAsync();
        return items;
    }
}
```

**For MongoDB Migration:**

```csharp
internal sealed class YYYYMMDDHHMMSS_MigrationName : PlatformMongoMigrationExecutor<{Service}DbContext>
{
    public override string Name => "YYYYMMDDHHMMSS_MigrationName";
    public override DateTime? OnlyForDbInitBeforeDate => new(YYYY, MM, DD);
    public override DateTime? ExpirationDate => new(YYYY, MM, DD); // Optional: auto-delete after date

    public override async Task Execute({Service}DbContext dbContext)
    {
        // Ensure indexes
        await dbContext.EnsureInboxBusMessageCollectionIndexesAsync(true);
        await dbContext.EnsureOutboxBusMessageCollectionIndexesAsync(true);

        // Or custom index/data operations
        var collection = dbContext.GetCollection<Entity>();
        await collection.Indexes.CreateOneAsync(
            new CreateIndexModel<Entity>(
                Builders<Entity>.IndexKeys.Ascending(e => e.Field),
                new CreateIndexOptions { Unique = true }));
    }
}
```

## Phase 4: Verify

- [ ] Migration is idempotent (safe to run multiple times)
- [ ] Large datasets use paging
- [ ] Proper error handling
- [ ] Unit of work for transactions
- [ ] `OnlyForDbsCreatedBeforeDate` set correctly
- [ ] Tested with sample data

## Phase 5: Wait for Approval

**CRITICAL:** Present your migration design and wait for explicit user approval before creating files.

---

Use `backend-data-migration` skill for detailed guidance.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
