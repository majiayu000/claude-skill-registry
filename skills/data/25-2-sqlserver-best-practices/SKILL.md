---
name: sqlserver-best-practices
description: "SQL Server database design best practices, naming conventions, indexing strategies, and performance optimization for .NET applications using Microsoft.Data.SqlClient and EF Core."
version: 1.0.0
language: SQL/C#
framework: SQL Server 2019+, .NET 8+
dependencies: Microsoft.EntityFrameworkCore.SqlServer
---

# SQL Server Best Practices for .NET

## Overview

Best practices for SQL Server database design, naming conventions, indexing, and performance optimization when using with .NET and Entity Framework Core.

## Quick Reference

| Category | Best Practice |
|----------|---------------|
| **Naming** | PascalCase for tables/columns |
| **Primary Keys** | Use `uniqueidentifier` (Guid) with `NEWSEQUENTIALID()` or `int`/`bigint` IDENTITY |
| **Timestamps** | Use `datetimeoffset` with UTC |
| **Indexes** | Index foreign keys, unique constraints |
| **Strings** | Use `nvarchar(n)` with explicit lengths |
| **JSON** | Use `nvarchar(max)` with JSON functions (SQL Server 2016+) |

---

## Naming Conventions

### PascalCase Standard

SQL Server convention is **PascalCase** for all identifiers:

```sql
-- PascalCase (SQL Server convention)
CREATE TABLE UserProfiles (
    UserId uniqueidentifier PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    FirstName nvarchar(100) NOT NULL,
    LastName nvarchar(100) NOT NULL,
    CreatedAt datetimeoffset NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedAt datetimeoffset NOT NULL DEFAULT SYSUTCDATETIME()
);
```

### EF Core Setup

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseSqlServer(connectionString);
    // EF Core uses PascalCase by default — matches SQL Server convention
});
```

### Naming Patterns

| Object | Pattern | Example |
|--------|---------|---------|
| Tables | `PascalCase` (plural) | `UserProfiles`, `OrderItems` |
| Columns | `PascalCase` | `FirstName`, `CreatedAt` |
| Primary Keys | `PK_{Table}` | `PK_Users`, `PK_Orders` |
| Foreign Keys | `FK_{Table}_{RefTable}` | `FK_Orders_Users` |
| Indexes | `IX_{Table}_{Column(s)}` | `IX_Users_Email` |
| Unique Indexes | `UIX_{Table}_{Column(s)}` | `UIX_Users_Email` |
| Check Constraints | `CK_{Table}_{Column}` | `CK_Users_Age` |
| Default Constraints | `DF_{Table}_{Column}` | `DF_Users_CreatedAt` |
| Schemas | `PascalCase` | `dbo`, `Sales`, `Identity` |

---

## Data Types

### Recommended Types

| C# Type | SQL Server Type | Notes |
|---------|-----------------|-------|
| `Guid` | `uniqueidentifier` | Use `NEWSEQUENTIALID()` to avoid index fragmentation |
| `string` | `nvarchar(n)` | Always specify length; Unicode by default |
| `string` (large) | `nvarchar(max)` | Only when > 4000 characters needed |
| `int` | `int` | 4 bytes, -2B to +2B |
| `long` | `bigint` | 8 bytes |
| `decimal` | `decimal(p,s)` | Exact precision for money |
| `double` | `float` | Floating point |
| `bool` | `bit` | 0/1 |
| `DateTime` | `datetimeoffset` | Always use with time zone |
| `DateTime` (date only) | `date` | When time is not needed |
| `byte[]` | `varbinary(max)` | Binary data |
| `byte[]` (concurrency) | `rowversion` | Auto-increment on update |

### nvarchar vs varchar

```sql
-- nvarchar: Unicode (2 bytes per char) - PREFERRED
CREATE TABLE Products (
    Id uniqueidentifier PRIMARY KEY,
    Name nvarchar(200) NOT NULL,        -- Supports international characters
    Description nvarchar(2000)
);

-- varchar: Non-Unicode (1 byte per char) - only for ASCII-only data
CREATE TABLE AuditLogs (
    Id bigint IDENTITY PRIMARY KEY,
    Action varchar(50) NOT NULL          -- Known ASCII values like 'INSERT', 'UPDATE'
);
```

**Always specify length:**
- `nvarchar(max)` can't be indexed and has performance implications
- Use the smallest length that fits the domain (email: 256, name: 100, etc.)

### Timestamps

```sql
-- datetimeoffset with UTC default
CreatedAt datetimeoffset NOT NULL CONSTRAINT DF_Users_CreatedAt DEFAULT SYSUTCDATETIME(),
UpdatedAt datetimeoffset NOT NULL CONSTRAINT DF_Users_UpdatedAt DEFAULT SYSUTCDATETIME()

-- datetime2 alternative (no timezone, but higher precision than datetime)
CreatedAt datetime2(7) NOT NULL DEFAULT SYSUTCDATETIME()

-- AVOID legacy datetime type
-- CreatedAt datetime NOT NULL  -- Lower precision, limited range
```

```csharp
// EF Core configuration
builder.Property(e => e.CreatedAt)
    .HasColumnType("datetimeoffset")
    .IsRequired()
    .HasDefaultValueSql("SYSUTCDATETIME()");
```

### JSON Support (SQL Server 2016+)

```sql
-- Store JSON in nvarchar(max)
CREATE TABLE Products (
    Id uniqueidentifier PRIMARY KEY,
    Metadata nvarchar(max) NULL,
    CONSTRAINT CK_Products_Metadata_JSON CHECK (ISJSON(Metadata) = 1)
);

-- Query JSON
SELECT Id, JSON_VALUE(Metadata, '$.category') AS Category
FROM Products
WHERE JSON_VALUE(Metadata, '$.isActive') = 'true';
```

```csharp
// EF Core configuration
builder.Property(e => e.Metadata)
    .HasColumnType("nvarchar(max)");

// EF Core 7+ owned types as JSON
builder.OwnsOne(e => e.Settings, settingsBuilder =>
{
    settingsBuilder.ToJson();
});
```

---

## Primary Keys

### Sequential GUID - Recommended

```sql
-- NEWSEQUENTIALID() avoids index fragmentation (page splits)
CREATE TABLE Users (
    Id uniqueidentifier PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    Email nvarchar(256) NOT NULL
);
```

```csharp
// EF Core - let SQL Server generate sequential GUIDs
builder.Property(e => e.Id)
    .HasDefaultValueSql("NEWSEQUENTIALID()");

// In domain entity - app generates (use sequential GUID library)
public static User Create(...)
{
    return new User(Guid.NewGuid(), ...);  // Or use RT.Comb for sequential
}
```

**Why NEWSEQUENTIALID() over NEWID()?**
- `NEWID()` generates random GUIDs causing clustered index fragmentation
- `NEWSEQUENTIALID()` generates sequential GUIDs for efficient inserts
- 16 bytes vs 4 bytes (int) — tradeoff for global uniqueness

### IDENTITY Alternative

```sql
-- Auto-increment (best for clustered index performance)
CREATE TABLE Orders (
    Id int IDENTITY(1,1) PRIMARY KEY,
    OrderNumber nvarchar(20) NOT NULL
);

-- bigint for high-volume tables
CREATE TABLE AuditLogs (
    Id bigint IDENTITY(1,1) PRIMARY KEY
);
```

```csharp
// EF Core
builder.Property(e => e.Id)
    .UseIdentityColumn();  // SQL Server IDENTITY
```

---

## Indexing Strategies

### Index Foreign Keys

```sql
-- SQL Server does NOT auto-create FK indexes (unlike some ORMs)
CREATE NONCLUSTERED INDEX IX_Orders_UserId ON Orders(UserId);
CREATE NONCLUSTERED INDEX IX_OrderItems_OrderId ON OrderItems(OrderId);
```

```csharp
builder.HasIndex(o => o.UserId);
```

### Unique Indexes

```sql
CREATE UNIQUE NONCLUSTERED INDEX UIX_Users_Email ON Users(Email);
```

```csharp
builder.HasIndex(u => u.Email).IsUnique();
```

### Composite Indexes

```sql
-- Composite indexes for common query patterns
CREATE NONCLUSTERED INDEX IX_Orders_UserId_Status ON Orders(UserId, Status);
CREATE NONCLUSTERED INDEX IX_Orders_CreatedAt_Status ON Orders(CreatedAt DESC, Status);
```

**Order matters!** Index on `(UserId, Status)` helps:
- `WHERE UserId = @id AND Status = @status` - uses index
- `WHERE UserId = @id` - uses index
- `WHERE Status = @status` - does NOT use index

### Filtered Indexes

```sql
-- Index only relevant rows (equivalent to PostgreSQL partial indexes)
CREATE NONCLUSTERED INDEX IX_Orders_Pending 
ON Orders(CreatedAt) 
WHERE Status = 'Pending';

CREATE NONCLUSTERED INDEX IX_Users_Active_Email 
ON Users(Email) 
WHERE IsDeleted = 0;
```

```csharp
// EF Core
builder.HasIndex(o => o.CreatedAt)
    .HasFilter("[Status] = 'Pending'");
```

### Covering Indexes (INCLUDE)

```sql
-- Include frequently accessed columns to avoid key lookups
CREATE NONCLUSTERED INDEX IX_Users_Email_Include 
ON Users(Email) 
INCLUDE (FirstName, LastName);
```

```csharp
// EF Core 7+
builder.HasIndex(u => u.Email)
    .IncludeProperties(u => new { u.FirstName, u.LastName });
```

### Full-Text Search Indexes

```sql
-- Create full-text catalog and index
CREATE FULLTEXT CATALOG ProductSearch AS DEFAULT;

CREATE FULLTEXT INDEX ON Products(Name, Description)
KEY INDEX PK_Products
WITH CHANGE_TRACKING AUTO;

-- Query using CONTAINS or FREETEXT
SELECT * FROM Products
WHERE CONTAINS((Name, Description), '"search term" OR FORMSOF(INFLECTIONAL, "search")');

SELECT * FROM Products
WHERE FREETEXT((Name, Description), 'search term');
```

### Columnstore Indexes (Analytics)

```sql
-- Nonclustered columnstore for analytical queries on OLTP tables
CREATE NONCLUSTERED COLUMNSTORE INDEX NCCI_Orders_Analytics
ON Orders(CreatedAt, Status, TotalAmount, UserId);

-- Ideal for aggregation queries
SELECT Status, COUNT(*) AS OrderCount, SUM(TotalAmount) AS Total
FROM Orders
GROUP BY Status;
```

### When NOT to Index

Do not index:
- Very small tables (< 1000 rows)
- Columns rarely used in WHERE/JOIN/ORDER BY
- Columns with low cardinality (few distinct values like bit columns)
- Columns that change frequently (high write overhead)
- Wide columns (nvarchar(max), varbinary(max))

---

## Constraints

### Primary Key Constraints

```sql
CONSTRAINT PK_Users PRIMARY KEY CLUSTERED (Id)
```

```csharp
builder.HasKey(u => u.Id);
```

### Foreign Key Constraints

```sql
-- Named foreign keys with appropriate delete behavior
CONSTRAINT FK_Orders_Users 
    FOREIGN KEY (UserId) 
    REFERENCES Users(Id) 
    ON DELETE NO ACTION,  -- Prevent orphans (SQL Server default)

CONSTRAINT FK_OrderItems_Orders 
    FOREIGN KEY (OrderId) 
    REFERENCES Orders(Id) 
    ON DELETE CASCADE     -- Delete items with order
```

```csharp
builder.HasOne(o => o.User)
    .WithMany(u => u.Orders)
    .HasForeignKey(o => o.UserId)
    .OnDelete(DeleteBehavior.Restrict);
```

### Check Constraints

```sql
-- Enforce business rules at database level
CONSTRAINT CK_Users_Age CHECK (Age >= 18 AND Age <= 120),
CONSTRAINT CK_Products_Price CHECK (Price >= 0),
CONSTRAINT CK_Orders_Quantity CHECK (Quantity > 0)
```

```csharp
builder.ToTable(t => t.HasCheckConstraint(
    "CK_Products_Price", 
    "[Price] >= 0"));
```

### Unique Constraints

```sql
-- Composite unique constraints
CONSTRAINT UQ_UserProfiles_UserType UNIQUE (UserId, ProfileType)
```

```csharp
builder.HasIndex(p => new { p.UserId, p.ProfileType }).IsUnique();
```

---

## Performance Optimization

### Connection Pooling

```csharp
// Connection string with pooling (enabled by default)
"Server=localhost;Database=MyDb;User Id=app_user;Password=pass;Encrypt=True;TrustServerCertificate=True;Min Pool Size=5;Max Pool Size=100"
```

### Batch Operations

```csharp
// EF Core batches SaveChanges automatically in SQL Server
context.Users.AddRange(users);
await context.SaveChangesAsync();  // Batched into fewer round-trips

// Do NOT save one at a time
foreach (var user in users)
{
    context.Users.Add(user);
    await context.SaveChangesAsync();  // Multiple round-trips!
}
```

### AsNoTracking for Read-Only Queries

```csharp
// Read-only queries
var users = await context.Users
    .AsNoTracking()  // Faster, no change tracking overhead
    .ToListAsync();
```

### Compiled Queries

```csharp
// Define once
private static readonly Func<ApplicationDbContext, string, Task<User?>> GetUserByEmail =
    EF.CompileAsyncQuery((ApplicationDbContext context, string email) =>
        context.Users.FirstOrDefault(u => u.Email == email));

// Use many times (faster — skips query compilation)
var user = await GetUserByEmail(context, email);
```

### Pagination

```sql
-- Efficient pagination (SQL Server 2012+)
SELECT * FROM Users
ORDER BY CreatedAt DESC
OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY;
```

```csharp
// EF Core pagination
var users = await context.Users
    .OrderByDescending(u => u.CreatedAt)
    .Skip(pageNumber * pageSize)
    .Take(pageSize)
    .ToListAsync();
```

### Avoid N+1 Queries

```csharp
// N+1 problem
var orders = await context.Orders.ToListAsync();
foreach (var order in orders)
{
    var user = await context.Users.FindAsync(order.UserId);  // N queries!
}

// Eager loading
var orders = await context.Orders
    .Include(o => o.User)  // Single query with JOIN
    .ToListAsync();

// Split query for multiple collections
var orders = await context.Orders
    .Include(o => o.Items)
    .Include(o => o.Payments)
    .AsSplitQuery()  // Separate queries, avoids cartesian explosion
    .ToListAsync();
```

### Query Hints

```csharp
// NOLOCK (read uncommitted) — use sparingly, only for non-critical reads
var reports = await context.Orders
    .TagWith("OPTION (MAXDOP 4)")
    .AsNoTracking()
    .ToListAsync();

// Using raw SQL with hints
var orders = await context.Orders
    .FromSqlRaw("SELECT * FROM Orders WITH (NOLOCK) WHERE Status = {0}", status)
    .ToListAsync();
```

---

## Maintenance

### Update Statistics

```sql
-- Update statistics for a table
UPDATE STATISTICS Users;

-- Update all statistics in the database
EXEC sp_updatestats;

-- Full scan for more accurate statistics
UPDATE STATISTICS Users WITH FULLSCAN;
```

### Index Maintenance

```sql
-- Check index fragmentation
SELECT 
    OBJECT_NAME(ips.object_id) AS TableName,
    i.name AS IndexName,
    ips.avg_fragmentation_in_percent,
    ips.page_count
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
INNER JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 10
    AND ips.page_count > 1000
ORDER BY ips.avg_fragmentation_in_percent DESC;

-- Reorganize (< 30% fragmentation)
ALTER INDEX IX_Orders_UserId ON Orders REORGANIZE;

-- Rebuild (> 30% fragmentation)
ALTER INDEX IX_Orders_UserId ON Orders REBUILD WITH (ONLINE = ON);

-- Rebuild all indexes on a table
ALTER INDEX ALL ON Orders REBUILD WITH (ONLINE = ON);
```

### Monitor Index Usage

```sql
-- Find unused indexes
SELECT 
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    ius.user_seeks,
    ius.user_scans,
    ius.user_lookups,
    ius.user_updates
FROM sys.indexes i
LEFT JOIN sys.dm_db_index_usage_stats ius 
    ON i.object_id = ius.object_id AND i.index_id = ius.index_id
WHERE OBJECTPROPERTY(i.object_id, 'IsUserTable') = 1
    AND i.type_desc = 'NONCLUSTERED'
    AND ISNULL(ius.user_seeks, 0) + ISNULL(ius.user_scans, 0) + ISNULL(ius.user_lookups, 0) = 0
ORDER BY ius.user_updates DESC;

-- Find missing indexes (suggested by query optimizer)
SELECT TOP 20
    OBJECT_NAME(mid.object_id) AS TableName,
    migs.avg_user_impact,
    migs.user_seeks,
    mid.equality_columns,
    mid.inequality_columns,
    mid.included_columns
FROM sys.dm_db_missing_index_groups mig
INNER JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
INNER JOIN sys.dm_db_missing_index_details mid ON mig.index_handle = mid.index_handle
ORDER BY migs.avg_user_impact * migs.user_seeks DESC;
```

### Database Size

```sql
-- Check table sizes
SELECT 
    t.name AS TableName,
    s.row_count AS RowCount,
    CAST(SUM(a.total_pages) * 8 / 1024.0 AS DECIMAL(10,2)) AS TotalSpaceMB,
    CAST(SUM(a.used_pages) * 8 / 1024.0 AS DECIMAL(10,2)) AS UsedSpaceMB
FROM sys.tables t
INNER JOIN sys.indexes i ON t.object_id = i.object_id
INNER JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
LEFT JOIN sys.dm_db_partition_stats s ON p.partition_id = s.partition_id AND p.index_id = s.index_id
GROUP BY t.name, s.row_count
ORDER BY SUM(a.total_pages) DESC;
```

---

## Security Best Practices

### Connection Security

```csharp
// Use encryption
"Server=prod-server;Database=MyDb;User Id=app_user;Password=pass;Encrypt=True;TrustServerCertificate=False"

// Windows Authentication (preferred in domain environments)
"Server=localhost;Database=MyDb;Integrated Security=True;Encrypt=True"

// Azure SQL with Managed Identity
"Server=myserver.database.windows.net;Database=MyDb;Authentication=Active Directory Managed Identity"
```

### Least Privilege

```sql
-- Create application-specific login and user
CREATE LOGIN app_login WITH PASSWORD = 'SecurePassword123!';
CREATE USER app_user FOR LOGIN app_login;

-- Grant only necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO app_user;

-- For EF Core migrations (separate admin user)
CREATE USER migration_user FOR LOGIN migration_login;
ALTER ROLE db_ddladmin ADD MEMBER migration_user;

-- Do NOT use sa or db_owner for application
```

### Parameterized Queries

```csharp
// EF Core uses parameters automatically (safe from SQL injection)
var users = await context.Users
    .Where(u => u.Email == email)  // Parameterized
    .ToListAsync();

// Dapper with parameters
var users = await connection.QueryAsync<User>(
    "SELECT * FROM Users WHERE Email = @Email",
    new { Email = email });

// NEVER concatenate SQL
var sql = $"SELECT * FROM Users WHERE Email = '{email}'";  // SQL INJECTION!
```

---

## SQL Server Features

### Temporal Tables (System-Versioned)

```sql
-- Automatic history tracking (SQL Server 2016+)
CREATE TABLE Products (
    Id uniqueidentifier PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    Name nvarchar(200) NOT NULL,
    Price decimal(18,2) NOT NULL,
    SysStartTime datetime2 GENERATED ALWAYS AS ROW START NOT NULL,
    SysEndTime datetime2 GENERATED ALWAYS AS ROW END NOT NULL,
    PERIOD FOR SYSTEM_TIME (SysStartTime, SysEndTime)
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.ProductsHistory));

-- Query historical data
SELECT * FROM Products FOR SYSTEM_TIME AS OF '2024-01-15T10:00:00';

-- Query changes in a range
SELECT * FROM Products FOR SYSTEM_TIME BETWEEN '2024-01-01' AND '2024-02-01';
```

```csharp
// EF Core 6+ temporal table support
builder.ToTable("Products", b => b.IsTemporal());

// Query historical data
var historicalProducts = await context.Products
    .TemporalAsOf(DateTime.UtcNow.AddDays(-7))
    .ToListAsync();
```

### Sequences

```sql
-- Create a sequence for order numbers
CREATE SEQUENCE dbo.OrderNumberSequence
    AS int
    START WITH 1000
    INCREMENT BY 1;

-- Use in table
CREATE TABLE Orders (
    Id uniqueidentifier PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    OrderNumber int NOT NULL DEFAULT NEXT VALUE FOR dbo.OrderNumberSequence
);
```

```csharp
// EF Core
builder.Property(o => o.OrderNumber)
    .HasDefaultValueSql("NEXT VALUE FOR dbo.OrderNumberSequence");

// Register sequence
modelBuilder.HasSequence<int>("OrderNumberSequence")
    .StartsAt(1000)
    .IncrementsBy(1);
```

### Computed Columns

```sql
-- Persisted computed column (stored on disk, indexable)
ALTER TABLE Orders ADD TotalWithTax AS (TotalAmount * 1.21) PERSISTED;

-- Non-persisted computed column (calculated on read)
ALTER TABLE Users ADD FullName AS (FirstName + ' ' + LastName);
```

```csharp
// EF Core
builder.Property(o => o.TotalWithTax)
    .HasComputedColumnSql("[TotalAmount] * 1.21", stored: true);

builder.Property(u => u.FullName)
    .HasComputedColumnSql("[FirstName] + ' ' + [LastName]");
```

---

## High Concurrency Patterns

### Optimistic Concurrency with rowversion

```csharp
// src/{name}.domain/{Entity}/{Entity}.cs
public class Order
{
    public Guid Id { get; private set; }
    public string Status { get; private set; }

    // Concurrency token - SQL Server rowversion auto-increments on update
    public byte[] RowVersion { get; private set; }
}
```

```csharp
// src/{name}.infrastructure/Configurations/OrderConfiguration.cs
internal sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");
        builder.HasKey(o => o.Id);

        // ═══════════════════════════════════════════════════════════════
        // OPTIMISTIC CONCURRENCY WITH rowversion
        // SQL Server rowversion auto-increments on every row update
        // ═══════════════════════════════════════════════════════════════
        builder.Property(o => o.RowVersion)
            .IsRowVersion();  // Maps to SQL Server rowversion type
    }
}
```

### Handling Concurrency Conflicts

```csharp
// src/{name}.infrastructure/Repositories/OrderRepository.cs
public async Task UpdateAsync(Order order, CancellationToken cancellationToken)
{
    try
    {
        context.Orders.Update(order);
        await context.SaveChangesAsync(cancellationToken);
    }
    catch (DbUpdateConcurrencyException ex)
    {
        var entry = ex.Entries.Single();
        var databaseValues = await entry.GetDatabaseValuesAsync(cancellationToken);

        if (databaseValues is null)
        {
            throw new EntityNotFoundException("Order was deleted by another user");
        }

        // Option 1: Client wins - overwrite database values
        // entry.OriginalValues.SetValues(databaseValues);
        // await context.SaveChangesAsync(cancellationToken);

        // Option 2: Database wins - throw and let caller retry
        throw new ConcurrencyException(
            "Order was modified by another user. Please refresh and try again.");
    }
}
```

### Retry with Exponential Backoff (Polly)

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
using Polly;
using Polly.Retry;
using Microsoft.Data.SqlClient;

services.AddResiliencePipeline("database", builder =>
{
    builder.AddRetry(new RetryStrategyOptions
    {
        ShouldHandle = new PredicateBuilder()
            .Handle<DbUpdateConcurrencyException>()
            .Handle<SqlException>(ex => ex.IsTransient()),
        MaxRetryAttempts = 3,
        Delay = TimeSpan.FromMilliseconds(200),
        BackoffType = DelayBackoffType.Exponential,
        UseJitter = true,
        OnRetry = static args =>
        {
            Console.WriteLine($"Retry attempt {args.AttemptNumber} after {args.RetryDelay}");
            return default;
        }
    });
});

// SQL Server built-in retry (EF Core)
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(5),
            errorNumbersToAdd: null);  // Retries on transient errors
    });
});
```

### DbContext Pooling for High Performance

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
services.AddDbContextPool<ApplicationDbContext>(options =>
{
    options.UseSqlServer(connectionString);
}, poolSize: 128);

// For even higher performance, use PooledDbContextFactory
services.AddPooledDbContextFactory<ApplicationDbContext>(options =>
{
    options.UseSqlServer(connectionString);
});
```

```csharp
// Usage with PooledDbContextFactory
public class HighPerformanceQueryHandler
{
    private readonly IDbContextFactory<ApplicationDbContext> _contextFactory;

    public async Task<List<Order>> GetOrdersAsync(CancellationToken ct)
    {
        await using var context = await _contextFactory.CreateDbContextAsync(ct);

        return await context.Orders
            .AsNoTracking()
            .Where(o => o.Status == "Active")
            .ToListAsync(ct);
    }
}
```

### Connection Pooling Configuration

```csharp
// Optimized connection string for high concurrency
var connectionString = new SqlConnectionStringBuilder
{
    DataSource = "localhost",
    InitialCatalog = "MyDb",
    UserID = "app_user",
    Password = "secret",

    // ═══════════════════════════════════════════════════════════════
    // CONNECTION POOLING SETTINGS
    // ═══════════════════════════════════════════════════════════════
    Pooling = true,
    MinPoolSize = 10,
    MaxPoolSize = 100,

    // ═══════════════════════════════════════════════════════════════
    // TIMEOUT SETTINGS
    // ═══════════════════════════════════════════════════════════════
    ConnectTimeout = 30,
    CommandTimeout = 60,

    // ═══════════════════════════════════════════════════════════════
    // RELIABILITY SETTINGS
    // ═══════════════════════════════════════════════════════════════
    ConnectRetryCount = 3,
    ConnectRetryInterval = 10,

    // ═══════════════════════════════════════════════════════════════
    // ENCRYPTION
    // ═══════════════════════════════════════════════════════════════
    Encrypt = SqlConnectionEncryptOption.Mandatory,
    TrustServerCertificate = false
}.ConnectionString;
```

### Row-Level Locking for Critical Operations

```sql
-- UPDLOCK + ROWLOCK - Lock rows during transaction
SELECT * FROM Accounts WITH (UPDLOCK, ROWLOCK) WHERE Id = @Id;

-- READPAST - Skip locked rows (for queue processing)
SELECT TOP (@BatchSize) * 
FROM Jobs WITH (UPDLOCK, READPAST)
WHERE Status = 'Pending'
ORDER BY CreatedAt;

-- NOWAIT - Fail immediately if locked
SELECT * FROM Accounts WITH (UPDLOCK, NOWAIT) WHERE Id = @Id;
```

```csharp
// EF Core equivalent using raw SQL
public async Task<Account?> GetForUpdateAsync(Guid id, CancellationToken ct)
{
    return await context.Accounts
        .FromSqlInterpolated(
            $"SELECT * FROM Accounts WITH (UPDLOCK, ROWLOCK) WHERE Id = {id}")
        .FirstOrDefaultAsync(ct);
}

// Queue processing with READPAST
public async Task<List<Job>> GetPendingJobsAsync(int batchSize, CancellationToken ct)
{
    return await context.Jobs
        .FromSqlInterpolated($@"
            SELECT TOP ({batchSize}) * 
            FROM Jobs WITH (UPDLOCK, READPAST)
            WHERE Status = 'Pending'
            ORDER BY CreatedAt")
        .ToListAsync(ct);
}
```

### Application Locks (sp_getapplock)

```csharp
// SQL Server application-level locks (equivalent to PostgreSQL advisory locks)
public class AppLockService
{
    private readonly ApplicationDbContext _context;

    public async Task<bool> TryAcquireLockAsync(
        string resourceName, int timeoutMs, CancellationToken ct)
    {
        var result = await _context.Database
            .SqlQuery<int>($@"
                DECLARE @result int;
                EXEC @result = sp_getapplock 
                    @Resource = {resourceName}, 
                    @LockMode = 'Exclusive', 
                    @LockTimeout = {timeoutMs};
                SELECT @result")
            .FirstAsync(ct);

        return result >= 0;  // 0 = granted, 1 = granted after wait
    }

    public async Task ReleaseLockAsync(string resourceName, CancellationToken ct)
    {
        await _context.Database
            .ExecuteSqlAsync($"EXEC sp_releaseapplock @Resource = {resourceName}", ct);
    }
}

// Usage for distributed singleton operations
public async Task ProcessDailyReportAsync(CancellationToken ct)
{
    if (!await _lockService.TryAcquireLockAsync("DailyReport", timeoutMs: 0, ct))
    {
        _logger.LogInformation("Another instance is processing the daily report");
        return;
    }

    try
    {
        await GenerateReportAsync(ct);
    }
    finally
    {
        await _lockService.ReleaseLockAsync("DailyReport", ct);
    }
}
```

---

## Critical Rules

1. **Use PascalCase** - SQL Server convention for identifiers
2. **Use nvarchar with explicit lengths** - Avoid nvarchar(max) unless needed
3. **Always use datetimeoffset** - Store times in UTC, avoid legacy datetime
4. **Index foreign keys** - SQL Server does NOT auto-create FK indexes
5. **Use NEWSEQUENTIALID() for GUID PKs** - Avoids clustered index fragmentation
6. **Use rowversion for concurrency** - Auto-increments on every row update
7. **Parameterize queries** - Prevent SQL injection
8. **Monitor index fragmentation** - Reorganize at 10%, rebuild at 30%
9. **Use connection pooling** - Enabled by default, tune pool size
10. **Use EnableRetryOnFailure** - Built-in transient fault handling
11. **Name all constraints** - PK_, FK_, CK_, DF_, IX_ prefixes
12. **Use temporal tables for audit** - Built-in history tracking

---

## Related Skills

- `06-ef-core-configuration` - EF Core entity configurations
- `05-repository-pattern` - Data access patterns
- `19-dapper-query-builder` - Raw SQL with Dapper
- `01-dotnet-clean-architecture` - Overall architecture
- `25.1-postgresql-best-practices` - PostgreSQL equivalent patterns
