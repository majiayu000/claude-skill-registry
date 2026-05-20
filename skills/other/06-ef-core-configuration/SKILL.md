---
name: ef-core-configuration
description: "Generates Entity Framework Core configurations using Fluent API. Maps domain entities to database tables with proper relationships, constraints, and conventions."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Entity Framework Core, Npgsql (PostgreSQL)
---

# EF Core Configuration Generator

## Overview

This skill generates Entity Framework Core configurations using Fluent API:

- **IEntityTypeConfiguration<T>** - Per-entity configuration classes
- **Fluent API over attributes** - Keep domain clean
- **Snake case naming** - PostgreSQL convention
- **Relationships** - One-to-Many, Many-to-Many, One-to-One
- **Value Objects** - Owned types mapping

## Quick Reference

| Configuration | Use |
|---------------|-----|
| `ToTable()` | Table name |
| `HasKey()` | Primary key |
| `Property()` | Column configuration |
| `HasOne/HasMany()` | Relationships |
| `OwnsOne()` | Value objects |
| `HasIndex()` | Database indexes |

---

## Configuration Structure

```
/Infrastructure/Configurations/
├── {Entity}Configuration.cs
├── {ChildEntity}Configuration.cs
├── {ValueObject}Configuration.cs
└── OutboxMessageConfiguration.cs
```

---

## Template: Basic Entity Configuration

```csharp
// src/{name}.infrastructure/Configurations/{Entity}Configuration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.domain.{aggregate};

namespace {name}.infrastructure.configurations;

internal sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        // ═══════════════════════════════════════════════════════════════
        // TABLE MAPPING
        // ═══════════════════════════════════════════════════════════════
        builder.ToTable("{entity}");  // snake_case table name

        // ═══════════════════════════════════════════════════════════════
        // PRIMARY KEY
        // ═══════════════════════════════════════════════════════════════
        builder.HasKey(e => e.Id);
        
        builder.Property(e => e.Id)
            .ValueGeneratedNever();  // App generates GUIDs

        // ═══════════════════════════════════════════════════════════════
        // PROPERTIES
        // ═══════════════════════════════════════════════════════════════
        builder.Property(e => e.Name)
            .HasMaxLength(100)
            .IsRequired();

        builder.Property(e => e.Description)
            .HasColumnType("text");  // Unlimited length

        builder.Property(e => e.IsActive)
            .HasDefaultValue(true)
            .IsRequired();

        builder.Property(e => e.CreatedAt)
            .IsRequired()
            .HasDefaultValueSql("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'");

        builder.Property(e => e.UpdatedAt)
            .IsRequired()
            .HasDefaultValueSql("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'");

        // ═══════════════════════════════════════════════════════════════
        // INDEXES
        // ═══════════════════════════════════════════════════════════════
        builder.HasIndex(e => e.Name)
            .IsUnique();

        builder.HasIndex(e => e.OrganizationId);

        builder.HasIndex(e => new { e.OrganizationId, e.Name })
            .IsUnique();
    }
}
```

---

## Template: Entity with Relationships

```csharp
// src/{name}.infrastructure/Configurations/{Entity}Configuration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.domain.{aggregate};

namespace {name}.infrastructure.configurations;

internal sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        builder.ToTable("{entity}");
        builder.HasKey(e => e.Id);

        // ═══════════════════════════════════════════════════════════════
        // FOREIGN KEY PROPERTIES
        // ═══════════════════════════════════════════════════════════════
        builder.Property(e => e.OrganizationId)
            .IsRequired();

        builder.Property(e => e.ParentId);  // Nullable FK

        // ═══════════════════════════════════════════════════════════════
        // ONE-TO-MANY: Parent has many children
        // ═══════════════════════════════════════════════════════════════
        builder.HasMany(e => e.{ChildEntities})
            .WithOne(c => c.{Entity})
            .HasForeignKey(c => c.{Entity}Id)
            .OnDelete(DeleteBehavior.Cascade);

        // ═══════════════════════════════════════════════════════════════
        // MANY-TO-ONE: Entity belongs to Organization
        // ═══════════════════════════════════════════════════════════════
        builder.HasOne(e => e.Organization)
            .WithMany(o => o.{Entities})
            .HasForeignKey(e => e.OrganizationId)
            .OnDelete(DeleteBehavior.Restrict);  // Prevent cascade delete

        // ═══════════════════════════════════════════════════════════════
        // SELF-REFERENCING: Entity has optional parent
        // ═══════════════════════════════════════════════════════════════
        builder.HasOne(e => e.Parent)
            .WithMany(e => e.Children)
            .HasForeignKey(e => e.ParentId)
            .OnDelete(DeleteBehavior.Restrict)
            .IsRequired(false);
    }
}
```

---

## Template: Child Entity Configuration

```csharp
// src/{name}.infrastructure/Configurations/{ChildEntity}Configuration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.domain.{aggregate};

namespace {name}.infrastructure.configurations;

internal sealed class {ChildEntity}Configuration : IEntityTypeConfiguration<{ChildEntity}>
{
    public void Configure(EntityTypeBuilder<{ChildEntity}> builder)
    {
        builder.ToTable("{child_entity}");
        
        builder.HasKey(c => c.Id);
        
        builder.Property(c => c.Id)
            .ValueGeneratedNever();

        builder.Property(c => c.{Parent}Id)
            .IsRequired();

        builder.Property(c => c.Name)
            .HasMaxLength(100)
            .IsRequired();

        builder.Property(c => c.SortOrder)
            .IsRequired()
            .HasDefaultValue(0);

        builder.Property(c => c.CreatedAt)
            .IsRequired()
            .HasDefaultValueSql("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'");

        // Relationship defined from parent side, but can also define here
        builder.HasOne(c => c.{Parent})
            .WithMany(p => p.{ChildEntities})
            .HasForeignKey(c => c.{Parent}Id)
            .OnDelete(DeleteBehavior.Cascade);

        // Composite unique constraint
        builder.HasIndex(c => new { c.{Parent}Id, c.Name })
            .IsUnique();

        builder.HasIndex(c => new { c.{Parent}Id, c.SortOrder });
    }
}
```

---

## Template: Many-to-Many Relationship

```csharp
// src/{name}.infrastructure/Configurations/User{Entity}Configuration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.domain.{aggregate};

namespace {name}.infrastructure.configurations;

// Join entity for many-to-many
internal sealed class User{Entity}Configuration : IEntityTypeConfiguration<User{Entity}>
{
    public void Configure(EntityTypeBuilder<User{Entity}> builder)
    {
        builder.ToTable("user_{entity}");

        // Composite primary key
        builder.HasKey(ue => new { ue.UserId, ue.{Entity}Id });

        // Or with separate ID
        // builder.HasKey(ue => ue.Id);
        // builder.HasIndex(ue => new { ue.UserId, ue.{Entity}Id }).IsUnique();

        builder.Property(ue => ue.UserId)
            .IsRequired();

        builder.Property(ue => ue.{Entity}Id)
            .IsRequired();

        builder.Property(ue => ue.IsManager)
            .HasDefaultValue(false);

        builder.Property(ue => ue.CreatedAt)
            .HasDefaultValueSql("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'");

        // Relationships
        builder.HasOne(ue => ue.User)
            .WithMany(u => u.User{Entities})
            .HasForeignKey(ue => ue.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasOne(ue => ue.{Entity})
            .WithMany(e => e.User{Entities})
            .HasForeignKey(ue => ue.{Entity}Id)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

---

## Template: Value Object as Owned Type

```csharp
// src/{name}.infrastructure/Configurations/{Entity}Configuration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.domain.{aggregate};

namespace {name}.infrastructure.configurations;

internal sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        builder.ToTable("{entity}");
        builder.HasKey(e => e.Id);

        // ═══════════════════════════════════════════════════════════════
        // VALUE OBJECT: Email (stored in same table)
        // ═══════════════════════════════════════════════════════════════
        builder.OwnsOne(e => e.Email, emailBuilder =>
        {
            emailBuilder.Property(email => email.Value)
                .HasColumnName("email")
                .HasMaxLength(255)
                .IsRequired();

            emailBuilder.HasIndex(email => email.Value)
                .IsUnique();
        });

        // ═══════════════════════════════════════════════════════════════
        // VALUE OBJECT: Address (multiple columns)
        // ═══════════════════════════════════════════════════════════════
        builder.OwnsOne(e => e.Address, addressBuilder =>
        {
            addressBuilder.Property(a => a.Street)
                .HasColumnName("address_street")
                .HasMaxLength(200);

            addressBuilder.Property(a => a.City)
                .HasColumnName("address_city")
                .HasMaxLength(100);

            addressBuilder.Property(a => a.State)
                .HasColumnName("address_state")
                .HasMaxLength(50);

            addressBuilder.Property(a => a.ZipCode)
                .HasColumnName("address_zip_code")
                .HasMaxLength(20);

            addressBuilder.Property(a => a.Country)
                .HasColumnName("address_country")
                .HasMaxLength(100);
        });

        // ═══════════════════════════════════════════════════════════════
        // VALUE OBJECT: Money
        // ═══════════════════════════════════════════════════════════════
        builder.OwnsOne(e => e.Price, priceBuilder =>
        {
            priceBuilder.Property(m => m.Amount)
                .HasColumnName("price_amount")
                .HasColumnType("numeric(18,2)")
                .IsRequired();

            priceBuilder.Property(m => m.Currency)
                .HasColumnName("price_currency")
                .HasMaxLength(3)
                .IsRequired();
        });
    }
}
```

---

## Template: Enum Mapping

```csharp
// src/{name}.infrastructure/Configurations/{Entity}Configuration.cs
internal sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        // ═══════════════════════════════════════════════════════════════
        // ENUM AS STRING
        // ═══════════════════════════════════════════════════════════════
        builder.Property(e => e.Status)
            .HasConversion<string>()  // Store as string
            .HasMaxLength(50)
            .IsRequired();

        // ═══════════════════════════════════════════════════════════════
        // ENUM AS INTEGER (default)
        // ═══════════════════════════════════════════════════════════════
        builder.Property(e => e.Priority)
            .HasConversion<int>();  // Store as int

        // ═══════════════════════════════════════════════════════════════
        // CUSTOM CONVERSION
        // ═══════════════════════════════════════════════════════════════
        builder.Property(e => e.Type)
            .HasConversion(
                v => v.ToString().ToLowerInvariant(),
                v => Enum.Parse<EntityType>(v, true))
            .HasMaxLength(50);
    }
}
```

---

## Template: Audit Fields with Shadow Properties

```csharp
// src/{name}.infrastructure/Configurations/{Entity}Configuration.cs
internal sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        builder.ToTable("{entity}");

        // ═══════════════════════════════════════════════════════════════
        // SHADOW PROPERTIES (not on domain entity)
        // ═══════════════════════════════════════════════════════════════
        builder.Property<DateTime>("CreatedAt")
            .IsRequired()
            .HasDefaultValueSql("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'");

        builder.Property<DateTime>("UpdatedAt")
            .IsRequired()
            .HasDefaultValueSql("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'");

        builder.Property<string>("CreatedBy")
            .HasMaxLength(100);

        builder.Property<string>("UpdatedBy")
            .HasMaxLength(100);

        builder.Property<uint>("Version")
            .IsRowVersion();  // Concurrency token
    }
}
```

---

## Template: Soft Delete Configuration

```csharp
// src/{name}.infrastructure/Configurations/{Entity}Configuration.cs
internal sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        builder.ToTable("{entity}");

        // Soft delete property
        builder.Property(e => e.IsDeleted)
            .HasDefaultValue(false)
            .IsRequired();

        builder.Property(e => e.DeletedAt);

        // ═══════════════════════════════════════════════════════════════
        // GLOBAL QUERY FILTER (excludes soft-deleted)
        // ═══════════════════════════════════════════════════════════════
        builder.HasQueryFilter(e => !e.IsDeleted);

        // Index for soft delete queries
        builder.HasIndex(e => e.IsDeleted);
    }
}
```

---

## Template: JSON Column (PostgreSQL)

```csharp
// src/{name}.infrastructure/Configurations/{Entity}Configuration.cs
internal sealed class {Entity}Configuration : IEntityTypeConfiguration<{Entity}>
{
    public void Configure(EntityTypeBuilder<{Entity}> builder)
    {
        builder.ToTable("{entity}");

        // ═══════════════════════════════════════════════════════════════
        // JSON COLUMN (PostgreSQL JSONB)
        // ═══════════════════════════════════════════════════════════════
        builder.Property(e => e.Metadata)
            .HasColumnType("jsonb")
            .HasConversion(
                v => JsonSerializer.Serialize(v, (JsonSerializerOptions?)null),
                v => JsonSerializer.Deserialize<Dictionary<string, object>>(v, (JsonSerializerOptions?)null)!);

        // Or for owned types in JSON
        builder.OwnsOne(e => e.Settings, settingsBuilder =>
        {
            settingsBuilder.ToJson();  // EF Core 7+
            settingsBuilder.Property(s => s.NotificationsEnabled);
            settingsBuilder.Property(s => s.Theme);
        });
    }
}
```

---

## Template: Outbox Message Configuration

```csharp
// src/{name}.infrastructure/Configurations/OutboxMessageConfiguration.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {name}.infrastructure.outbox;

namespace {name}.infrastructure.configurations;

internal sealed class OutboxMessageConfiguration : IEntityTypeConfiguration<OutboxMessage>
{
    public void Configure(EntityTypeBuilder<OutboxMessage> builder)
    {
        builder.ToTable("outbox_message");

        builder.HasKey(o => o.Id);

        builder.Property(o => o.Id)
            .ValueGeneratedNever();

        builder.Property(o => o.OccurredOnUtc)
            .IsRequired();

        builder.Property(o => o.Type)
            .HasMaxLength(500)
            .IsRequired();

        builder.Property(o => o.Content)
            .HasColumnType("jsonb")
            .IsRequired();

        builder.Property(o => o.ProcessedOnUtc);

        builder.Property(o => o.Error)
            .HasColumnType("text");

        // Index for processing unprocessed messages
        builder.HasIndex(o => o.ProcessedOnUtc)
            .HasFilter("processed_on_utc IS NULL");
    }
}
```

---

## PostgreSQL Specific Configurations

### Snake Case Naming Convention

```csharp
// In DependencyInjection.cs
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseNpgsql(connectionString)
           .UseSnakeCaseNamingConvention();  // Requires EFCore.NamingConventions
});
```

### Column Types Reference

| C# Type | PostgreSQL Type | Configuration |
|---------|-----------------|---------------|
| `string` | `text` | `.HasColumnType("text")` |
| `string` (limited) | `varchar(n)` | `.HasMaxLength(n)` |
| `decimal` | `numeric(p,s)` | `.HasColumnType("numeric(18,2)")` |
| `DateTime` | `timestamp` | `.HasColumnType("timestamp")` |
| `DateTimeOffset` | `timestamptz` | `.HasColumnType("timestamptz")` |
| `Guid` | `uuid` | (automatic) |
| `bool` | `boolean` | (automatic) |
| `byte[]` | `bytea` | (automatic) |
| `Dictionary` | `jsonb` | `.HasColumnType("jsonb")` |

---

## ApplicationDbContext Setup

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
        // Apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(ApplicationDbContext).Assembly);

        base.OnModelCreating(modelBuilder);
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Add domain events to outbox
        AddDomainEventsAsOutboxMessages();
        
        // Update audit fields
        UpdateAuditFields();

        return await base.SaveChangesAsync(cancellationToken);
    }

    private void UpdateAuditFields()
    {
        var entries = ChangeTracker.Entries()
            .Where(e => e.State is EntityState.Added or EntityState.Modified);

        foreach (var entry in entries)
        {
            if (entry.State == EntityState.Added)
            {
                entry.Property("CreatedAt").CurrentValue = DateTime.UtcNow;
            }

            entry.Property("UpdatedAt").CurrentValue = DateTime.UtcNow;
        }
    }
}
```

---

## Critical Rules

1. **Use Fluent API, not attributes** - Keep domain clean
2. **Configuration per entity** - One file per `IEntityTypeConfiguration<T>`
3. **Snake case for PostgreSQL** - Use naming convention package
4. **ValueGeneratedNever for GUIDs** - App generates IDs
5. **Explicit column types** - Don't rely on conventions
6. **Configure relationships from one side** - Avoid duplication
7. **Use delete behaviors thoughtfully** - Cascade vs Restrict
8. **Index foreign keys** - EF Core doesn't auto-index FKs
9. **Use query filters for soft delete** - Consistent filtering
10. **Value objects as owned types** - OwnsOne for value objects

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Data annotations on domain
public class User
{
    [Key]
    public Guid Id { get; set; }
    
    [Required]
    [MaxLength(100)]
    public string Name { get; set; }  // Pollutes domain!
}

// ✅ CORRECT: Fluent API in configuration
builder.Property(u => u.Name).HasMaxLength(100).IsRequired();

// ❌ WRONG: Not specifying string length
builder.Property(e => e.Name);  // Defaults to MAX!

// ✅ CORRECT: Always specify max length
builder.Property(e => e.Name).HasMaxLength(100);

// ❌ WRONG: Auto-increment for GUIDs
builder.Property(e => e.Id).ValueGeneratedOnAdd();

// ✅ CORRECT: App generates GUIDs
builder.Property(e => e.Id).ValueGeneratedNever();

// ❌ WRONG: No cascade strategy
builder.HasMany(e => e.Children).WithOne();

// ✅ CORRECT: Explicit delete behavior
builder.HasMany(e => e.Children)
    .WithOne(c => c.Parent)
    .OnDelete(DeleteBehavior.Cascade);
```

---

## Related Skills

- `domain-entity-generator` - Generate entities to configure
- `repository-pattern` - Use configurations with repositories
- `dotnet-clean-architecture` - Infrastructure layer placement
