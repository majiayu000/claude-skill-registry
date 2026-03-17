---
name: dotnet-ef-migrations
description: Master Entity Framework Core migrations with code-first approach, migration strategies, data seeding, rollback procedures, and production deployment patterns. Use when managing database schema changes in .NET applications.
---

# .NET Entity Framework Core Migrations

Master EF Core migrations for .NET 8+ with code-first database management.

## Setup

```bash
# Install EF Core tools
dotnet tool install --global dotnet-ef
dotnet tool update --global dotnet-ef

# Add EF Core packages
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
# Or PostgreSQL
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
```

## DbContext Configuration

```csharp
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<Order> Orders { get; set; }
    public DbSet<Customer> Customers { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);

        // Global query filters
        modelBuilder.Entity<Order>().HasQueryFilter(o => !o.IsDeleted);

        base.OnModelCreating(modelBuilder);
    }
}

// Entity Configuration
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");

        builder.HasKey(o => o.Id);

        builder.Property(o => o.OrderNumber)
            .IsRequired()
            .HasMaxLength(20);

        builder.Property(o => o.TotalAmount)
            .HasColumnType("decimal(18,2)");

        builder.HasIndex(o => o.OrderNumber)
            .IsUnique();

        builder.HasOne(o => o.Customer)
            .WithMany(c => c.Orders)
            .HasForeignKey(o => o.CustomerId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasMany(o => o.Items)
            .WithOne(i => i.Order)
            .HasForeignKey(i => i.OrderId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

## Migration Commands

```bash
# Add migration
dotnet ef migrations add InitialCreate
dotnet ef migrations add AddOrderStatus
dotnet ef migrations add UpdateCustomerEmail

# Update database
dotnet ef database update

# Update to specific migration
dotnet ef database update AddOrderStatus

# Rollback migration
dotnet ef database update PreviousMigration

# Remove last migration (if not applied)
dotnet ef migrations remove

# Generate SQL script
dotnet ef migrations script
dotnet ef migrations script InitialCreate AddOrderStatus

# Generate idempotent script
dotnet ef migrations script --idempotent

# List migrations
dotnet ef migrations list

# Drop database
dotnet ef database drop --force
```

## Migration File Structure

```csharp
public partial class AddOrderStatus : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<int>(
            name: "Status",
            table: "Orders",
            type: "int",
            nullable: false,
            defaultValue: 0);

        migrationBuilder.CreateIndex(
            name: "IX_Orders_Status",
            table: "Orders",
            column: "Status");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropIndex(
            name: "IX_Orders_Status",
            table: "Orders");

        migrationBuilder.DropColumn(
            name: "Status",
            table: "Orders");
    }
}
```

## Data Seeding

```csharp
// In OnModelCreating
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<OrderStatus>().HasData(
        new OrderStatus { Id = 1, Name = "Pending" },
        new OrderStatus { Id = 2, Name = "Processing" },
        new OrderStatus { Id = 3, Name = "Shipped" },
        new OrderStatus { Id = 4, Name = "Delivered" }
    );
}

// Or in migration
protected override void Up(MigrationBuilder migrationBuilder)
{
    migrationBuilder.InsertData(
        table: "OrderStatuses",
        columns: new[] { "Id", "Name" },
        values: new object[,]
        {
            { 1, "Pending" },
            { 2, "Processing" },
            { 3, "Shipped" },
            { 4, "Delivered" }
        });
}
```

## Custom SQL in Migrations

```csharp
protected override void Up(MigrationBuilder migrationBuilder)
{
    // Execute raw SQL
    migrationBuilder.Sql(@"
        CREATE INDEX IX_Orders_CreatedAt_Status
        ON Orders (CreatedAt, Status)
        WHERE IsDeleted = 0
    ");

    // Create stored procedure
    migrationBuilder.Sql(@"
        CREATE PROCEDURE GetOrdersByCustomer
            @CustomerId uniqueidentifier
        AS
        BEGIN
            SELECT * FROM Orders
            WHERE CustomerId = @CustomerId
            AND IsDeleted = 0
        END
    ");

    // Create view
    migrationBuilder.Sql(@"
        CREATE VIEW vw_ActiveOrders AS
        SELECT o.*, c.Name AS CustomerName
        FROM Orders o
        INNER JOIN Customers c ON o.CustomerId = c.Id
        WHERE o.IsDeleted = 0
    ");
}

protected override void Down(MigrationBuilder migrationBuilder)
{
    migrationBuilder.Sql("DROP VIEW IF EXISTS vw_ActiveOrders");
    migrationBuilder.Sql("DROP PROCEDURE IF EXISTS GetOrdersByCustomer");
    migrationBuilder.Sql("DROP INDEX IF EXISTS IX_Orders_CreatedAt_Status ON Orders");
}
```

## Production Deployment

```csharp
// Program.cs - Apply migrations on startup (development only)
if (app.Environment.IsDevelopment())
{
    using var scope = app.Services.CreateScope();
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await db.Database.MigrateAsync();
}

// Production - Generate SQL scripts
// dotnet ef migrations script --idempotent --output migrations.sql
// Review and apply scripts manually

// Or use migration bundles (EF Core 6+)
// dotnet ef migrations bundle --self-contained -r linux-x64
// ./efbundle --connection "Server=..."
```

## Migration Strategies

### 1. Script-Based (Recommended for Production)
```bash
# Generate script
dotnet ef migrations script --idempotent --output migration.sql

# Review script
# Apply via SQL tool or deployment pipeline
```

### 2. Runtime Migration
```csharp
// Only in development/staging
await dbContext.Database.MigrateAsync();
```

### 3. Migration Bundles
```bash
# Create bundle
dotnet ef migrations bundle --self-contained -r linux-x64

# Deploy and run
./efbundle --connection "Server=prod;Database=MyDb;..."
```

## Handling Migration Conflicts

```csharp
// Multiple developers scenario:
// 1. Pull latest code
git pull origin main

// 2. If migration conflicts, remove your migration
dotnet ef migrations remove

// 3. Create new migration
dotnet ef migrations add YourFeature

// 4. Test migration
dotnet ef database update
```

## Rolling Back Migrations

```bash
# Rollback to specific migration
dotnet ef database update PreviousMigration

# Rollback all
dotnet ef database update 0

# Generate rollback script
dotnet ef migrations script CurrentMigration PreviousMigration --output rollback.sql
```

## Best Practices

1. **Never Modify Applied Migrations** - Create new migration instead
2. **Review Generated Migrations** - Check SQL before applying
3. **Test Migrations** - Test on copy of production data
4. **Use Transactions** - Migrations run in transactions by default
5. **Backup Before Migration** - Always backup production database
6. **Idempotent Scripts** - Use `--idempotent` flag for production
7. **Version Control** - Commit migrations with code changes
8. **Data Migration** - Separate data migrations from schema migrations

## Common Patterns

```csharp
// Adding nullable column then making it required
protected override void Up(MigrationBuilder migrationBuilder)
{
    // Step 1: Add nullable column
    migrationBuilder.AddColumn<string>(
        name: "Email",
        table: "Customers",
        nullable: true);

    // Step 2: Update existing rows
    migrationBuilder.Sql("UPDATE Customers SET Email = 'unknown@example.com' WHERE Email IS NULL");

    // Step 3: Make column required
    migrationBuilder.AlterColumn<string>(
        name: "Email",
        table: "Customers",
        nullable: false);
}

// Renaming column
migrationBuilder.RenameColumn(
    name: "OldName",
    table: "TableName",
    newName: "NewName");

// Changing column type
migrationBuilder.AlterColumn<decimal>(
    name: "Price",
    table: "Products",
    type: "decimal(18,2)",
    nullable: false,
    oldClrType: typeof(float));
```
