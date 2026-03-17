---
name: dotnet-efcore-guidelines
description: Entity Framework Core best practices for Clean Architecture projects. Covers DbContext, entity configurations, repository pattern, migrations, and PostgreSQL-specific features.
type: domain
enforcement: suggest
priority: high
---

# .NET + Entity Framework Core Guidelines

> **Project-Agnostic EF Core Patterns**
>
> Placeholders use `{Placeholder}` syntax - see [docs/TEMPLATE_GLOSSARY.md](../../../docs/TEMPLATE_GLOSSARY.md).

## Purpose

This skill provides comprehensive best practices for using Entity Framework Core with PostgreSQL in Clean Architecture projects. It details conventions for DbContext, entity configurations, repository patterns, migrations, and PostgreSQL-specific features.

## When This Skill Activates

**Triggered by**:
- Keywords: "ef core", "entity framework", "dbcontext", "repository", "migration", "database", "postgres", "postgresql"
- File patterns: `**/Persistence/**/*.cs`, `**/Repositories/**/*.cs`, `**/*DbContext.cs`, `**/Configurations/**/*.cs`

## EF Core Architecture

The persistence layer (`{Project}.Persistence`) is responsible for data access and storage. It implements interfaces defined in the Application layer, adhering to Clean Architecture principles.

```mermaid
graph TD
    subgraph Application Layer
        A[I{Entity}Repository] --> B[{Entity}]
        B[{Entity}] --> C[Domain Layer]
    end

    subgraph Persistence Layer
        D[{DbContext}] --> B
        E[{Entity}Repository] --> D
        E --> A
    end

    A -- Implemented by --> E
    C -- Used by --> B
    D -- Configures --> B
```

## Resources

*For more detailed examples, refer to the `resources/` folder within this skill.*

| Resource | Description |
|----------|-------------|
| [dbcontext-patterns.md](resources/dbcontext-patterns.md) | DbContext configuration, `SaveChangesAsync` override |
| [entity-configuration.md](resources/entity-configuration.md) | `IEntityTypeConfiguration`, TPT, PostgreSQL functions |
| [repository-pattern.md](resources/repository-pattern.md) | `GenericRepository`, custom repositories |
| [querying-patterns.md](resources/querying-patterns.md) | `Include`, `Select`, projections, performance |
| [migrations.md](resources/migrations.md) | Creating and applying migrations |

## Quick Reference

### 1. DbContext Pattern

The `{DbContext}` manages database interactions.

```csharp
// File: {Project}.Persistence/{DbContext}.cs
public class {DbContext} : DbContext
{
    public {DbContext}(DbContextOptions<{DbContext}> options) : base(options) { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        // Automatically applies all IEntityTypeConfiguration<T> from the assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof({DbContext}).Assembly);
    }

    // Override SaveChangesAsync for cross-cutting concerns like auditing or soft deletes
    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Example: Audit logging or automatic timestamp updates
        foreach (var entry in ChangeTracker.Entries())
        {
            // Handle CreatedAt, UpdatedAt logic
        }
        return base.SaveChangesAsync(cancellationToken);
    }

    public DbSet<{Entity}> {Entities} { get; set; } = null!;
    public DbSet<{ParentEntity}> {ParentEntities} { get; set; } = null!;
    // ... other DbSets
}
```

*For more details, see [dbcontext-patterns.md](resources/dbcontext-patterns.md).*

### 2. Entity Configuration

All entity-specific configurations are done using `IEntityTypeConfiguration<T>` in separate classes.

```csharp
// File: {Project}.Persistence/Configurations/Entities/{Entity}Configuration.cs
public class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        // Project Standard: Table Per Type (TPT) inheritance strategy
        builder.UseTptMappingStrategy();

        // Project Standard: UUIDv7 primary keys for main entities
        builder.Property(e => e.Id).HasDefaultValueSql("uuidv7()");

        // Database-level defaults are acceptable here, not in domain entities
        builder.Property(e => e.ViewCount).HasDefaultValue(0);

        builder.Property(e => e.Title).HasMaxLength(200).IsRequired();
        builder.Property(e => e.Description).HasMaxLength(5000);

        // Example relationship configuration
        builder.HasOne(e => e.{ParentEntity})
            .WithMany()
            .HasForeignKey(e => e.{ParentEntity}Id)
            .OnDelete(DeleteBehavior.Restrict);
    }
}
```

*For more details, see [entity-configuration.md](resources/entity-configuration.md).*

### 3. Repository Pattern

Repositories abstract data access. Interfaces reside in the Application layer, and implementations are in the Persistence layer.

**CRITICAL RULE**: Repositories **MUST** return **DOMAIN ENTITIES**, not DTOs. DTO mapping always happens in the Application layer handlers via AutoMapper.

```csharp
// File: {Project}.Application/Contracts/Persistence/I{Entity}Repository.cs (Application Layer)
public interface I{Entity}Repository : IGenericRepository<{Entity}, {IdType}>
{
    Task<List<{Entity}>> Get{Entities}WithDetails(); // Returns List<{Entity}>
    Task<{Entity}?> Get{Entity}WithDetails({IdType} id); // Returns {Entity}?
}

// File: {Project}.Persistence/Repositories/{Entity}Repository.cs (Persistence Layer)
public class {Entity}Repository : GenericRepository<{Entity}, {IdType}>, I{Entity}Repository
{
    private readonly {DbContext} _dbContext;

    public {Entity}Repository({DbContext} dbContext) : base(dbContext) => _dbContext = dbContext;

    public async Task<List<{Entity}>> Get{Entities}WithDetails()
    {
        return await _dbContext.{Entities}
            .Include(e => e.{LookupEntity})
            .Include(e => e.{RelatedEntity1})
            .Include(e => e.{RelatedEntity2})
            .ToListAsync(); // Returns entities
    }
}
```

*For more details, see [repository-pattern.md](resources/repository-pattern.md).*

### 4. Querying Patterns

Efficient querying is crucial for performance. Avoid N+1 issues by using eager loading (`Include`) and projections (`Select`).

```csharp
// Example: Query with eager loading and projection to DTO (in Application Layer Handler)
public async Task<List<{Entity}ListDto>> Handle(Get{Entity}ListRequest request, CancellationToken cancellationToken)
{
    var {entities} = await _{entity}Repository.Get{Entities}WithDetails(); // Repository returns entities
    return _mapper.Map<List<{Entity}ListDto>>({entities}); // Handler maps to DTOs
}

// Example: Using AsNoTracking for read-only queries (in Repository)
public async Task<List<{Entity}>> Get{Entities}ReadOnly()
{
    return await _dbContext.{Entities}
        .AsNoTracking() // Disables change tracking for performance
        .Include(e => e.{ParentEntity})
        .ToListAsync();
}
```

*For more details, see [querying-patterns.md](resources/querying-patterns.md).*

### 5. Migrations

Database schema changes are managed through EF Core migrations.

```powershell
# Create a new migration for schema changes
dotnet ef migrations add AddNewFieldTo{Entity} --project {Project}.Persistence

# Apply pending migrations to the database
dotnet ef database update --project {Project}.Persistence

# Generate SQL script for production deployment
dotnet ef migrations script --idempotent --output migrations/release.sql --project {Project}.Persistence
```

*For more details, see [migrations.md](resources/migrations.md).*

## Key Principles & Conventions

*   **IDs**: All primary keys are `Guid` (or `{IdType}`), except for lookup tables which use `int` (or `{LookupIdType}`).
*   **Numeric Types**: Use `int` instead of `long` unless explicitly required for large values (e.g., file sizes, pagination cursors).
*   **Default Values**: **DO NOT** add default values in domain entity property initializers (e.g., `public int ViewCount { get; set; } = 0;`). Set defaults in application handlers or use database-level defaults via `IEntityTypeConfiguration`.
*   **Link Tables**: Navigation properties on link/mapping tables are **readonly for queries only**. Writes must go through the link table's repository directly.
*   **PostgreSQL Features**: Leverage PostgreSQL-specific features like `UUIDv7` for primary keys and PostGIS for spatial data handling.

---

**Related Documentation**:
- [`docs/DOMAIN.md`](../../../docs/DOMAIN.md) - Conceptual domain model.
- [`docs/ARCHITECTURE.md`](../../../docs/ARCHITECTURE.md) - Overall system architecture.
- [`clean-architecture-rules`](../clean-architecture-rules/SKILL.md) - Dependency enforcement.
