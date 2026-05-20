---
name: audit-trail
description: "Generates audit trail infrastructure for entities. Implements IAuditable interface, EF Core SaveChanges interceptor, and automatic population of CreatedAt, UpdatedAt, CreatedBy, and UpdatedBy fields."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Entity Framework Core
pattern: Auditing, Change Tracking
---

# Audit Trail Generator

## Overview

Automatic audit trail tracking for entities:

- **IAuditable interface** - Standard audit fields
- **SaveChanges interceptor** - Automatic field population
- **User context integration** - Track who made changes
- **Soft delete support** - Track deletions without removing

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `IAuditable` | Interface for auditable entities |
| `AuditableEntity` | Base class with audit fields |
| `AuditSaveChangesInterceptor` | Auto-populates audit fields |
| `SoftDeletable` | Interface for soft delete |

---

## Audit Structure

```
/Domain/Abstractions/
├── IAuditable.cs
├── ISoftDeletable.cs
└── AuditableEntity.cs

/Infrastructure/
├── Interceptors/
│   └── AuditSaveChangesInterceptor.cs
└── ApplicationDbContext.cs
```

---

## Template: Audit Interfaces

```csharp
// src/{name}.domain/Abstractions/IAuditable.cs
namespace {name}.domain.abstractions;

/// <summary>
/// Interface for entities that track creation and modification metadata
/// </summary>
public interface IAuditable
{
    /// <summary>
    /// UTC timestamp when the entity was created
    /// </summary>
    DateTime CreatedAtUtc { get; }

    /// <summary>
    /// ID of the user who created the entity
    /// </summary>
    Guid? CreatedBy { get; }

    /// <summary>
    /// UTC timestamp when the entity was last modified
    /// </summary>
    DateTime? UpdatedAtUtc { get; }

    /// <summary>
    /// ID of the user who last modified the entity
    /// </summary>
    Guid? UpdatedBy { get; }
}
```

```csharp
// src/{name}.domain/Abstractions/ISoftDeletable.cs
namespace {name}.domain.abstractions;

/// <summary>
/// Interface for entities that support soft delete
/// </summary>
public interface ISoftDeletable
{
    /// <summary>
    /// Whether the entity has been soft deleted
    /// </summary>
    bool IsDeleted { get; }

    /// <summary>
    /// UTC timestamp when the entity was deleted
    /// </summary>
    DateTime? DeletedAtUtc { get; }

    /// <summary>
    /// ID of the user who deleted the entity
    /// </summary>
    Guid? DeletedBy { get; }
}
```

---

## Template: Auditable Entity Base Class

```csharp
// src/{name}.domain/Abstractions/AuditableEntity.cs
namespace {name}.domain.abstractions;

/// <summary>
/// Base class for entities that track audit information
/// </summary>
public abstract class AuditableEntity : Entity, IAuditable, ISoftDeletable
{
    // ═══════════════════════════════════════════════════════════════
    // AUDIT FIELDS (IAuditable)
    // ═══════════════════════════════════════════════════════════════
    
    public DateTime CreatedAtUtc { get; private set; }
    public Guid? CreatedBy { get; private set; }
    public DateTime? UpdatedAtUtc { get; private set; }
    public Guid? UpdatedBy { get; private set; }

    // ═══════════════════════════════════════════════════════════════
    // SOFT DELETE FIELDS (ISoftDeletable)
    // ═══════════════════════════════════════════════════════════════
    
    public bool IsDeleted { get; private set; }
    public DateTime? DeletedAtUtc { get; private set; }
    public Guid? DeletedBy { get; private set; }

    protected AuditableEntity() : base()
    {
    }

    protected AuditableEntity(Guid id) : base(id)
    {
    }

    // ═══════════════════════════════════════════════════════════════
    // AUDIT METHODS (called by interceptor or manually)
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Sets creation audit fields. Called automatically by interceptor.
    /// </summary>
    internal void SetCreatedAudit(DateTime utcNow, Guid? userId)
    {
        CreatedAtUtc = utcNow;
        CreatedBy = userId;
    }

    /// <summary>
    /// Sets modification audit fields. Called automatically by interceptor.
    /// </summary>
    internal void SetModifiedAudit(DateTime utcNow, Guid? userId)
    {
        UpdatedAtUtc = utcNow;
        UpdatedBy = userId;
    }

    /// <summary>
    /// Soft deletes the entity
    /// </summary>
    public virtual void SoftDelete(DateTime utcNow, Guid? userId)
    {
        if (IsDeleted)
        {
            return;
        }

        IsDeleted = true;
        DeletedAtUtc = utcNow;
        DeletedBy = userId;
    }

    /// <summary>
    /// Restores a soft-deleted entity
    /// </summary>
    public virtual void Restore()
    {
        IsDeleted = false;
        DeletedAtUtc = null;
        DeletedBy = null;
    }
}
```

---

## Template: SaveChanges Interceptor

```csharp
// src/{name}.infrastructure/Interceptors/AuditSaveChangesInterceptor.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;
using Microsoft.EntityFrameworkCore.Diagnostics;
using {name}.application.abstractions.authentication;
using {name}.domain.abstractions;

namespace {name}.infrastructure.interceptors;

/// <summary>
/// Interceptor that automatically populates audit fields on SaveChanges
/// </summary>
public sealed class AuditSaveChangesInterceptor : SaveChangesInterceptor
{
    private readonly IUserContext _userContext;

    public AuditSaveChangesInterceptor(IUserContext userContext)
    {
        _userContext = userContext;
    }

    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        if (eventData.Context is not null)
        {
            UpdateAuditFields(eventData.Context);
        }

        return base.SavingChangesAsync(eventData, result, cancellationToken);
    }

    public override InterceptionResult<int> SavingChanges(
        DbContextEventData eventData,
        InterceptionResult<int> result)
    {
        if (eventData.Context is not null)
        {
            UpdateAuditFields(eventData.Context);
        }

        return base.SavingChanges(eventData, result);
    }

    private void UpdateAuditFields(DbContext context)
    {
        var utcNow = DateTime.UtcNow;
        var userId = GetCurrentUserId();

        foreach (var entry in context.ChangeTracker.Entries<IAuditable>())
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    SetCreatedAudit(entry, utcNow, userId);
                    break;

                case EntityState.Modified:
                    SetModifiedAudit(entry, utcNow, userId);
                    break;
            }
        }

        // Handle soft delete
        foreach (var entry in context.ChangeTracker.Entries<ISoftDeletable>())
        {
            if (entry.State == EntityState.Deleted)
            {
                // Convert hard delete to soft delete
                entry.State = EntityState.Modified;
                
                if (entry.Entity is AuditableEntity auditableEntity)
                {
                    auditableEntity.SoftDelete(utcNow, userId);
                }
            }
        }
    }

    private void SetCreatedAudit(EntityEntry<IAuditable> entry, DateTime utcNow, Guid? userId)
    {
        if (entry.Entity is AuditableEntity auditableEntity)
        {
            auditableEntity.SetCreatedAudit(utcNow, userId);
        }
        else
        {
            // For entities implementing IAuditable but not inheriting AuditableEntity
            entry.Property(nameof(IAuditable.CreatedAtUtc)).CurrentValue = utcNow;
            entry.Property(nameof(IAuditable.CreatedBy)).CurrentValue = userId;
        }
    }

    private void SetModifiedAudit(EntityEntry<IAuditable> entry, DateTime utcNow, Guid? userId)
    {
        if (entry.Entity is AuditableEntity auditableEntity)
        {
            auditableEntity.SetModifiedAudit(utcNow, userId);
        }
        else
        {
            entry.Property(nameof(IAuditable.UpdatedAtUtc)).CurrentValue = utcNow;
            entry.Property(nameof(IAuditable.UpdatedBy)).CurrentValue = userId;
        }
    }

    private Guid? GetCurrentUserId()
    {
        try
        {
            return _userContext.IsAuthenticated ? _userContext.UserId : null;
        }
        catch
        {
            // User context may not be available in background jobs
            return null;
        }
    }
}
```

---

## Template: EF Core Configuration for Audit Fields

```csharp
// src/{name}.infrastructure/Configurations/AuditableEntityConfiguration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.domain.abstractions;

namespace {name}.infrastructure.configurations;

/// <summary>
/// Base configuration for auditable entities
/// Apply using: builder.ApplyConfiguration(new AuditableEntityConfiguration<YourEntity>());
/// </summary>
public class AuditableEntityConfiguration<TEntity> : IEntityTypeConfiguration<TEntity>
    where TEntity : AuditableEntity
{
    public virtual void Configure(EntityTypeBuilder<TEntity> builder)
    {
        // ═══════════════════════════════════════════════════════════════
        // AUDIT FIELDS
        // ═══════════════════════════════════════════════════════════════
        
        builder.Property(e => e.CreatedAtUtc)
            .HasColumnName("created_at_utc")
            .IsRequired();

        builder.Property(e => e.CreatedBy)
            .HasColumnName("created_by");

        builder.Property(e => e.UpdatedAtUtc)
            .HasColumnName("updated_at_utc");

        builder.Property(e => e.UpdatedBy)
            .HasColumnName("updated_by");

        // ═══════════════════════════════════════════════════════════════
        // SOFT DELETE FIELDS
        // ═══════════════════════════════════════════════════════════════
        
        builder.Property(e => e.IsDeleted)
            .HasColumnName("is_deleted")
            .HasDefaultValue(false)
            .IsRequired();

        builder.Property(e => e.DeletedAtUtc)
            .HasColumnName("deleted_at_utc");

        builder.Property(e => e.DeletedBy)
            .HasColumnName("deleted_by");

        // ═══════════════════════════════════════════════════════════════
        // GLOBAL QUERY FILTER (Soft Delete)
        // ═══════════════════════════════════════════════════════════════
        
        builder.HasQueryFilter(e => !e.IsDeleted);

        // ═══════════════════════════════════════════════════════════════
        // INDEXES
        // ═══════════════════════════════════════════════════════════════
        
        builder.HasIndex(e => e.CreatedAtUtc)
            .HasDatabaseName($"ix_{typeof(TEntity).Name.ToLower()}_created_at");

        builder.HasIndex(e => e.IsDeleted)
            .HasDatabaseName($"ix_{typeof(TEntity).Name.ToLower()}_is_deleted")
            .HasFilter("is_deleted = true");
    }
}
```

---

## Template: Using Auditable Entity

```csharp
// src/{name}.domain/Users/User.cs
using {name}.domain.abstractions;
using {name}.domain.users.events;

namespace {name}.domain.users;

public sealed class User : AuditableEntity
{
    public string Name { get; private set; } = string.Empty;
    public Email Email { get; private set; } = null!;
    public Guid OrganizationId { get; private set; }
    public bool IsActive { get; private set; }

    private User() : base()
    {
    }

    private User(
        Guid id,
        string name,
        Email email,
        Guid organizationId)
        : base(id)
    {
        Name = name;
        Email = email;
        OrganizationId = organizationId;
        IsActive = true;
    }

    public static Result<User> Create(
        string name,
        string email,
        Guid organizationId)
    {
        var emailResult = Email.Create(email);
        if (emailResult.IsFailure)
        {
            return Result.Failure<User>(emailResult.Error);
        }

        var user = new User(
            Guid.NewGuid(),
            name,
            emailResult.Value,
            organizationId);

        user.RaiseDomainEvent(new UserCreatedDomainEvent(user.Id));

        return user;
        // CreatedAtUtc and CreatedBy will be set automatically by interceptor
    }

    public Result UpdateName(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            return Result.Failure(UserErrors.NameRequired);
        }

        Name = name;
        // UpdatedAtUtc and UpdatedBy will be set automatically by interceptor

        return Result.Success();
    }

    public void Deactivate()
    {
        IsActive = false;
        RaiseDomainEvent(new UserDeactivatedDomainEvent(Id));
    }
}
```

---

## Template: Entity Configuration Using Auditable Base

```csharp
// src/{name}.infrastructure/Configurations/UserConfiguration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.domain.users;

namespace {name}.infrastructure.configurations;

internal sealed class UserConfiguration : AuditableEntityConfiguration<User>
{
    public override void Configure(EntityTypeBuilder<User> builder)
    {
        // Call base configuration for audit fields
        base.Configure(builder);

        builder.ToTable("users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Name)
            .HasColumnName("name")
            .HasMaxLength(100)
            .IsRequired();

        builder.OwnsOne(u => u.Email, emailBuilder =>
        {
            emailBuilder.Property(e => e.Value)
                .HasColumnName("email")
                .HasMaxLength(255)
                .IsRequired();

            emailBuilder.HasIndex(e => e.Value)
                .IsUnique();
        });

        builder.Property(u => u.OrganizationId)
            .HasColumnName("organization_id")
            .IsRequired();

        builder.Property(u => u.IsActive)
            .HasColumnName("is_active")
            .HasDefaultValue(true)
            .IsRequired();

        builder.HasIndex(u => u.OrganizationId)
            .HasDatabaseName("ix_users_organization_id");
    }
}
```

---

## Template: DbContext Registration

```csharp
// src/{name}.infrastructure/ApplicationDbContext.cs
using Microsoft.EntityFrameworkCore;
using {name}.domain.abstractions;

namespace {name}.infrastructure;

public sealed class ApplicationDbContext : DbContext, IUnitOfWork
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        
        base.OnModelCreating(modelBuilder);
    }
}

// Registration in DependencyInjection.cs
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration configuration)
{
    services.AddDbContext<ApplicationDbContext>((sp, options) =>
    {
        options.UseNpgsql(configuration.GetConnectionString("Database"));
        options.AddInterceptors(sp.GetRequiredService<AuditSaveChangesInterceptor>());
    });

    services.AddScoped<AuditSaveChangesInterceptor>();

    return services;
}
```

---

## Template: Audit Log Entity (Optional - Full History)

```csharp
// src/{name}.domain/Auditing/AuditLog.cs
namespace {name}.domain.auditing;

/// <summary>
/// Stores complete audit history of changes
/// </summary>
public sealed class AuditLog
{
    public Guid Id { get; set; }
    public string EntityName { get; set; } = string.Empty;
    public string EntityId { get; set; } = string.Empty;
    public string Action { get; set; } = string.Empty;  // Created, Modified, Deleted
    public string? OldValues { get; set; }  // JSON
    public string? NewValues { get; set; }  // JSON
    public string? AffectedColumns { get; set; }  // JSON array
    public DateTime OccurredAtUtc { get; set; }
    public Guid? UserId { get; set; }
    public string? UserName { get; set; }
    public string? IpAddress { get; set; }
}
```

```csharp
// src/{name}.infrastructure/Interceptors/AuditLogInterceptor.cs
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;
using Microsoft.EntityFrameworkCore.Diagnostics;
using {name}.application.abstractions.authentication;
using {name}.domain.auditing;

namespace {name}.infrastructure.interceptors;

/// <summary>
/// Interceptor that logs complete change history to AuditLog table
/// </summary>
public sealed class AuditLogInterceptor : SaveChangesInterceptor
{
    private readonly IUserContext _userContext;

    public AuditLogInterceptor(IUserContext userContext)
    {
        _userContext = userContext;
    }

    public override async ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        if (eventData.Context is ApplicationDbContext context)
        {
            await CreateAuditLogs(context, cancellationToken);
        }

        return await base.SavingChangesAsync(eventData, result, cancellationToken);
    }

    private async Task CreateAuditLogs(ApplicationDbContext context, CancellationToken ct)
    {
        context.ChangeTracker.DetectChanges();

        var auditLogs = new List<AuditLog>();
        var utcNow = DateTime.UtcNow;
        var userId = _userContext.IsAuthenticated ? _userContext.UserId : (Guid?)null;

        foreach (var entry in context.ChangeTracker.Entries())
        {
            if (entry.Entity is AuditLog || 
                entry.State == EntityState.Detached || 
                entry.State == EntityState.Unchanged)
            {
                continue;
            }

            var auditLog = new AuditLog
            {
                Id = Guid.NewGuid(),
                EntityName = entry.Entity.GetType().Name,
                EntityId = GetPrimaryKeyValue(entry),
                OccurredAtUtc = utcNow,
                UserId = userId
            };

            switch (entry.State)
            {
                case EntityState.Added:
                    auditLog.Action = "Created";
                    auditLog.NewValues = SerializeProperties(entry, p => p.CurrentValue);
                    break;

                case EntityState.Modified:
                    auditLog.Action = "Modified";
                    auditLog.OldValues = SerializeProperties(entry, p => p.OriginalValue, true);
                    auditLog.NewValues = SerializeProperties(entry, p => p.CurrentValue, true);
                    auditLog.AffectedColumns = JsonSerializer.Serialize(
                        entry.Properties
                            .Where(p => p.IsModified)
                            .Select(p => p.Metadata.Name)
                            .ToList());
                    break;

                case EntityState.Deleted:
                    auditLog.Action = "Deleted";
                    auditLog.OldValues = SerializeProperties(entry, p => p.OriginalValue);
                    break;
            }

            auditLogs.Add(auditLog);
        }

        if (auditLogs.Any())
        {
            await context.Set<AuditLog>().AddRangeAsync(auditLogs, ct);
        }
    }

    private static string GetPrimaryKeyValue(EntityEntry entry)
    {
        var keyProperty = entry.Properties.FirstOrDefault(p => p.Metadata.IsPrimaryKey());
        return keyProperty?.CurrentValue?.ToString() ?? "unknown";
    }

    private static string? SerializeProperties(
        EntityEntry entry,
        Func<PropertyEntry, object?> valueSelector,
        bool onlyModified = false)
    {
        var properties = entry.Properties
            .Where(p => !p.Metadata.IsPrimaryKey())
            .Where(p => !onlyModified || p.IsModified)
            .ToDictionary(
                p => p.Metadata.Name,
                p => valueSelector(p));

        return properties.Any() 
            ? JsonSerializer.Serialize(properties) 
            : null;
    }
}
```

---

## Template: Query Including Deleted Records

```csharp
// When you need to include soft-deleted records:
public async Task<User?> GetByIdIncludingDeletedAsync(
    Guid id,
    CancellationToken cancellationToken)
{
    return await _dbContext.Users
        .IgnoreQueryFilters()  // Include soft-deleted records
        .FirstOrDefaultAsync(u => u.Id == id, cancellationToken);
}

// Query only deleted records:
public async Task<IReadOnlyList<User>> GetDeletedUsersAsync(
    CancellationToken cancellationToken)
{
    return await _dbContext.Users
        .IgnoreQueryFilters()
        .Where(u => u.IsDeleted)
        .OrderByDescending(u => u.DeletedAtUtc)
        .ToListAsync(cancellationToken);
}
```

---

## Database Migration

```sql
-- Add audit columns to existing table
ALTER TABLE users
ADD COLUMN created_at_utc TIMESTAMP NOT NULL DEFAULT NOW(),
ADD COLUMN created_by UUID NULL,
ADD COLUMN updated_at_utc TIMESTAMP NULL,
ADD COLUMN updated_by UUID NULL,
ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
ADD COLUMN deleted_at_utc TIMESTAMP NULL,
ADD COLUMN deleted_by UUID NULL;

-- Create indexes
CREATE INDEX ix_users_created_at ON users (created_at_utc);
CREATE INDEX ix_users_is_deleted ON users (is_deleted) WHERE is_deleted = TRUE;

-- Audit log table (if using full history)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY,
    entity_name VARCHAR(255) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    old_values JSONB NULL,
    new_values JSONB NULL,
    affected_columns JSONB NULL,
    occurred_at_utc TIMESTAMP NOT NULL,
    user_id UUID NULL,
    user_name VARCHAR(255) NULL,
    ip_address VARCHAR(50) NULL
);

CREATE INDEX ix_audit_log_entity ON audit_log (entity_name, entity_id);
CREATE INDEX ix_audit_log_occurred_at ON audit_log (occurred_at_utc DESC);
CREATE INDEX ix_audit_log_user_id ON audit_log (user_id);
```

---

## Critical Rules

1. **UTC timestamps always** - Never use local time
2. **Interceptor order matters** - Register after other interceptors
3. **Handle null user context** - Background jobs have no user
4. **Query filters are global** - Use `IgnoreQueryFilters()` when needed
5. **Audit fields are readonly** - Only interceptor should modify
6. **Index audit columns** - CreatedAtUtc, IsDeleted commonly queried
7. **Soft delete by default** - Convert hard delete to soft
8. **Keep audit log table lean** - Archive old records periodically

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Setting audit fields manually
user.CreatedAtUtc = DateTime.Now;  // Let interceptor handle it!

// ✅ CORRECT: Interceptor handles automatically
var user = User.Create(...);
await _unitOfWork.SaveChangesAsync();  // Audit fields set by interceptor

// ❌ WRONG: Using local time
builder.Property(e => e.CreatedAtUtc)
    .HasDefaultValueSql("NOW()");  // Could be local time!

// ✅ CORRECT: Explicitly UTC
builder.Property(e => e.CreatedAtUtc)
    .HasDefaultValueSql("NOW() AT TIME ZONE 'UTC'");

// ❌ WRONG: Forgetting query filters exist
var allUsers = await _dbContext.Users.ToListAsync();  // Missing deleted users might be intentional, but be aware!

// ✅ CORRECT: Explicit about including deleted
var allUsersIncludingDeleted = await _dbContext.Users
    .IgnoreQueryFilters()
    .ToListAsync();
```

---

## Related Skills

- `domain-entity-generator` - Entity base classes
- `ef-core-configuration` - Entity configuration
- `jwt-authentication` - IUserContext for tracking user
- `repository-pattern` - Repository methods with soft delete
