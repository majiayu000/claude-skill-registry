---
name: postgresql-best-practices
description: "PostgreSQL database design best practices, naming conventions, indexing strategies, and performance optimization for .NET applications using Npgsql and EF Core."
version: 1.0.0
language: SQL/C#
framework: PostgreSQL 14+, .NET 8+
dependencies: Npgsql.EntityFrameworkCore.PostgreSQL, EFCore.NamingConventions
inspiration: "johnpuksta/clean-architecture-agents (https://github.com/johnpuksta/clean-architecture-agents)"
---

# PostgreSQL Best Practices for .NET

## Overview

Best practices for PostgreSQL database design, naming conventions, indexing, and performance optimization when using with .NET and Entity Framework Core.

## Quick Reference

| Category | Best Practice |
|----------|---------------|
| **Naming** | snake_case for tables/columns |
| **Primary Keys** | Use `uuid` (Guid) or `bigserial` |
| **Timestamps** | Use `timestamptz` with UTC |
| **Indexes** | Index foreign keys, unique constraints |
| **Text** | Use `text` not `varchar` unless limit needed |
| **JSON** | Use `jsonb` not `json` |

---

## Naming Conventions

### Snake Case Standard

PostgreSQL convention is **snake_case** for all identifiers:

```sql
-- ✅ CORRECT: Snake case
CREATE TABLE user_profiles (
    user_id uuid PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updated_at timestamptz NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

-- ❌ WRONG: PascalCase or camelCase
CREATE TABLE UserProfiles (
    UserId uuid PRIMARY KEY,
    firstName text NOT NULL
);
```

### EF Core Snake Case Setup

```csharp
// DependencyInjection.cs
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseNpgsql(connectionString)
           .UseSnakeCaseNamingConvention();  // Converts C# PascalCase to snake_case
});
```

```bash
# Install package
dotnet add package EFCore.NamingConventions
```

### Naming Patterns

| Object | Pattern | Example |
|--------|---------|---------|
| Tables | `snake_case` (plural) | `user_profiles`, `order_items` |
| Columns | `snake_case` | `first_name`, `created_at` |
| Primary Keys | `pk_{table}` | `pk_users`, `pk_orders` |
| Foreign Keys | `fk_{table}_{ref_table}` | `fk_orders_users` |
| Indexes | `ix_{table}_{column(s)}` | `ix_users_email` |
| Unique Indexes | `uix_{table}_{column(s)}` | `uix_users_email` |
| Check Constraints | `ck_{table}_{column}` | `ck_users_age` |
| Sequences | `seq_{table}_{column}` | `seq_orders_order_number` |

---

## Data Types

### Recommended Types

| C# Type | PostgreSQL Type | Notes |
|---------|-----------------|-------|
| `Guid` | `uuid` | Preferred for primary keys |
| `string` (unlimited) | `text` | More flexible than varchar |
| `string` (limited) | `varchar(n)` | Only when length limit needed |
| `int` | `integer` | 4 bytes, -2B to +2B |
| `long` | `bigint` | 8 bytes |
| `decimal` | `numeric(p,s)` | Exact precision |
| `double` | `double precision` | Floating point |
| `bool` | `boolean` | true/false/null |
| `DateTime` | `timestamptz` | Always use with time zone |
| `byte[]` | `bytea` | Binary data |
| `Dictionary<string,object>` | `jsonb` | Structured data |
| `string[]` | `text[]` | Array type |

### Text vs Varchar

```sql
-- ✅ PREFERRED: Use text for most string columns
CREATE TABLE products (
    id uuid PRIMARY KEY,
    name text NOT NULL,
    description text
);

-- ⚠️ USE SPARINGLY: Only when you need to enforce length
CREATE TABLE users (
    id uuid PRIMARY KEY,
    email varchar(255) NOT NULL  -- Email has practical length limit
);
```

**Why text?**
- No performance difference in PostgreSQL
- More flexible (no arbitrary limits)
- Easier to modify (no migration needed to change length)

### Timestamps

```sql
-- ✅ CORRECT: timestamptz with UTC default
created_at timestamptz NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
updated_at timestamptz NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')

-- ❌ WRONG: timestamp without time zone
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
```

```csharp
// EF Core configuration
builder.Property(e => e.CreatedAt)
    .HasColumnType("timestamptz")
    .IsRequired()
    .HasDefaultValueSql("CURRENT_TIMESTAMP AT TIME ZONE 'UTC'");
```

### JSONB for Flexible Data

```sql
-- ✅ Use jsonb (binary JSON, faster, indexable)
metadata jsonb

-- ❌ Don't use json (text-based, slower)
metadata json
```

```csharp
// EF Core configuration
builder.Property(e => e.Metadata)
    .HasColumnType("jsonb");

// Or for owned types (EF Core 7+)
builder.OwnsOne(e => e.Settings, settingsBuilder =>
{
    settingsBuilder.ToJson();  // Stores as jsonb
});
```

---

## Primary Keys

### UUID (Guid) - Recommended

```sql
-- ✅ RECOMMENDED: UUID primary keys
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text NOT NULL
);
```

```csharp
// EF Core - App generates GUIDs
builder.Property(e => e.Id)
    .ValueGeneratedNever();  // Don't let DB generate

// In domain entity
public static User Create(...)
{
    return new User(Guid.NewGuid(), ...);  // App generates
}
```

**Benefits:**
- Globally unique (no collisions across databases)
- Can generate client-side
- Easier for distributed systems
- No sequential enumeration security risk

### Serial/BigSerial Alternative

```sql
-- Alternative: Auto-increment
CREATE TABLE orders (
    id bigserial PRIMARY KEY,
    order_number text NOT NULL
);
```

```csharp
// EF Core
builder.Property(e => e.Id)
    .UseIdentityColumn();  // PostgreSQL IDENTITY
```

---

## Indexing Strategies

### Index Foreign Keys

```sql
-- ✅ ALWAYS index foreign keys
CREATE INDEX ix_orders_user_id ON orders(user_id);
CREATE INDEX ix_order_items_order_id ON order_items(order_id);
```

EF Core creates these automatically, but verify:

```csharp
builder.HasIndex(o => o.UserId);
```

### Unique Indexes

```sql
-- ✅ Unique constraints
CREATE UNIQUE INDEX uix_users_email ON users(email);
CREATE UNIQUE INDEX uix_users_username ON users(username);
```

```csharp
builder.HasIndex(u => u.Email).IsUnique();
```

### Composite Indexes

```sql
-- ✅ Composite indexes for common query patterns
CREATE INDEX ix_orders_user_status ON orders(user_id, status);
CREATE INDEX ix_orders_created_status ON orders(created_at DESC, status);
```

**Order matters!** Index on `(user_id, status)` helps:
- `WHERE user_id = ? AND status = ?` ✅
- `WHERE user_id = ?` ✅
- `WHERE status = ?` ❌ (doesn't use index)

### Partial Indexes

```sql
-- ✅ Index only relevant rows
CREATE INDEX ix_orders_pending ON orders(created_at) 
WHERE status = 'Pending';

CREATE INDEX ix_users_active_email ON users(email) 
WHERE is_deleted = false;
```

```csharp
// EF Core
builder.HasIndex(o => o.CreatedAt)
    .HasFilter("status = 'Pending'");
```

### Covering Indexes (INCLUDE)

```sql
-- ✅ Include frequently accessed columns
CREATE INDEX ix_users_email_include ON users(email) 
INCLUDE (first_name, last_name);
```

### Full-Text Search Indexes

```sql
-- ✅ GIN index for full-text search
ALTER TABLE products 
ADD COLUMN search_vector tsvector 
GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))
) STORED;

CREATE INDEX ix_products_search ON products USING GIN(search_vector);
```

### JSONB Indexes

```sql
-- ✅ GIN index for JSONB queries
CREATE INDEX ix_products_metadata ON products USING GIN(metadata);

-- Specific path index
CREATE INDEX ix_products_metadata_tags ON products USING GIN((metadata -> 'tags'));
```

### When NOT to Index

❌ Don't index:
- Very small tables (< 1000 rows)
- Columns rarely used in WHERE/JOIN
- Columns with low cardinality (few distinct values)
- Columns that change frequently

---

## Constraints

### Primary Key Constraints

```sql
-- ✅ Named primary key
CONSTRAINT pk_users PRIMARY KEY (id)
```

```csharp
// EF Core names automatically: pk_{table}
builder.HasKey(u => u.Id);
```

### Foreign Key Constraints

```sql
-- ✅ Named foreign keys with appropriate delete behavior
CONSTRAINT fk_orders_users 
    FOREIGN KEY (user_id) 
    REFERENCES users(id) 
    ON DELETE RESTRICT;  -- Prevent orphans

CONSTRAINT fk_order_items_orders 
    FOREIGN KEY (order_id) 
    REFERENCES orders(id) 
    ON DELETE CASCADE;  -- Delete items with order
```

```csharp
builder.HasOne(o => o.User)
    .WithMany(u => u.Orders)
    .HasForeignKey(o => o.UserId)
    .OnDelete(DeleteBehavior.Restrict);
```

### Check Constraints

```sql
-- ✅ Enforce business rules at database level
CONSTRAINT ck_users_age CHECK (age >= 18 AND age <= 120)
CONSTRAINT ck_products_price CHECK (price >= 0)
CONSTRAINT ck_orders_quantity CHECK (quantity > 0)
```

```csharp
builder.ToTable(t => t.HasCheckConstraint(
    "ck_products_price", 
    "price >= 0"));
```

### Unique Constraints

```sql
-- ✅ Composite unique constraints
CONSTRAINT uq_user_profiles_user_type UNIQUE (user_id, profile_type)
```

```csharp
builder.HasIndex(p => new { p.UserId, p.ProfileType }).IsUnique();
```

---

## Performance Optimization

### Connection Pooling

```csharp
// Connection string with pooling (default enabled)
"Host=localhost;Database=mydb;Username=postgres;Password=pass;Pooling=true;MinPoolSize=1;MaxPoolSize=100"
```

### Prepared Statements

Npgsql automatically uses prepared statements for repeated queries.

```csharp
// EF Core automatically prepares statements
var users = await context.Users
    .Where(u => u.Email == email)  // Prepared on first execution
    .ToListAsync();
```

### Batch Operations

```csharp
// ✅ Batch inserts
context.Users.AddRange(users);
await context.SaveChangesAsync();  // Single round-trip

// ❌ Individual inserts
foreach (var user in users)
{
    context.Users.Add(user);
    await context.SaveChangesAsync();  // Multiple round-trips!
}
```

### AsNoTracking for Read-Only Queries

```csharp
// ✅ Read-only queries
var users = await context.Users
    .AsNoTracking()  // Faster, no change tracking
    .ToListAsync();

// ✅ Write operations (default)
var user = await context.Users.FindAsync(id);
user.Update(...);
await context.SaveChangesAsync();
```

### Compiled Queries

```csharp
// Define once
private static readonly Func<ApplicationDbContext, string, Task<User?>> GetUserByEmail =
    EF.CompileAsyncQuery((ApplicationDbContext context, string email) =>
        context.Users.FirstOrDefault(u => u.Email == email));

// Use many times (faster)
var user = await GetUserByEmail(context, email);
```

### Pagination

```sql
-- ✅ Efficient pagination
SELECT * FROM users 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 0;
```

```csharp
// ✅ EF Core pagination
var users = await context.Users
    .OrderByDescending(u => u.CreatedAt)
    .Skip(pageNumber * pageSize)
    .Take(pageSize)
    .ToListAsync();
```

### Avoid N+1 Queries

```csharp
// ❌ N+1 problem
var orders = await context.Orders.ToListAsync();
foreach (var order in orders)
{
    var user = await context.Users.FindAsync(order.UserId);  // N queries!
}

// ✅ Eager loading
var orders = await context.Orders
    .Include(o => o.User)  // Single query with JOIN
    .ToListAsync();

// ✅ Split query for multiple collections
var orders = await context.Orders
    .Include(o => o.Items)
    .Include(o => o.Payments)
    .AsSplitQuery()  // Separate queries, avoids cartesian explosion
    .ToListAsync();
```

---

## Maintenance

### Analyze and Vacuum

```sql
-- Analyze tables (update statistics)
ANALYZE users;
ANALYZE VERBOSE;  -- All tables

-- Vacuum (reclaim space)
VACUUM users;
VACUUM ANALYZE users;  -- Both operations
```

### Autovacuum Configuration

PostgreSQL runs autovacuum automatically, but tune if needed:

```sql
-- Check autovacuum settings
SHOW autovacuum;
SHOW autovacuum_naptime;

-- Per-table autovacuum tuning
ALTER TABLE high_traffic_table SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_analyze_scale_factor = 0.02
);
```

### Monitor Index Usage

```sql
-- Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Find missing indexes (sequential scans on large tables)
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan AS avg_seq_tup
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;
```

### Table Bloat

```sql
-- Check table bloat
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS external_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## Security Best Practices

### Connection Security

```csharp
// ✅ Use SSL/TLS
"Host=prod-server;Database=mydb;Username=app_user;Password=pass;SSL Mode=Require"

// ✅ Use connection pooling limits
"Host=localhost;Database=mydb;Username=postgres;Password=pass;MaxPoolSize=50;Timeout=30"
```

### Least Privilege

```sql
-- ✅ Create application-specific user
CREATE USER app_user WITH PASSWORD 'secure_password';

-- Grant only necessary permissions
GRANT CONNECT ON DATABASE mydb TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- ❌ Don't use superuser for application
-- Don't grant ALL PRIVILEGES
```

### Parameterized Queries

```csharp
// ✅ EF Core uses parameters automatically (safe from SQL injection)
var users = await context.Users
    .Where(u => u.Email == email)  // Parameterized
    .ToListAsync();

// ✅ Dapper with parameters
var users = await connection.QueryAsync<User>(
    "SELECT * FROM users WHERE email = @Email",
    new { Email = email });

// ❌ NEVER concatenate SQL
var sql = $"SELECT * FROM users WHERE email = '{email}'";  // SQL INJECTION!
```

---

## PostgreSQL Extensions

### Recommended Extensions

```sql
-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- gen_random_uuid()

-- Full-text search
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Trigram matching

-- Case-insensitive text
CREATE EXTENSION IF NOT EXISTS "citext";

-- Additional types
CREATE EXTENSION IF NOT EXISTS "hstore";  -- Key-value store
CREATE EXTENSION IF NOT EXISTS "ltree";   -- Hierarchical data
```

### Using Extensions

```sql
-- UUID generation
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid()
);

-- Case-insensitive email
CREATE TABLE users (
    id uuid PRIMARY KEY,
    email citext UNIQUE NOT NULL
);

-- Trigram similarity search
CREATE INDEX ix_products_name_trgm ON products USING GIN(name gin_trgm_ops);

SELECT * FROM products 
WHERE name % 'search term'  -- Similarity operator
ORDER BY similarity(name, 'search term') DESC;
```

---

## High Concurrency Patterns

### Optimistic Concurrency with xmin System Column

PostgreSQL has hidden system columns including `xmin` which holds the transaction ID of the last update. This is ideal for optimistic concurrency:

```csharp
// src/{name}.domain/{Entity}/{Entity}.cs
public class Order
{
    public Guid Id { get; private set; }
    public string Status { get; private set; }

    // Concurrency token - maps to PostgreSQL xmin system column
    public uint RowVersion { get; private set; }
}
```

```csharp
// src/{name}.infrastructure/Configurations/OrderConfiguration.cs
internal sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("orders");
        builder.HasKey(o => o.Id);

        // ═══════════════════════════════════════════════════════════════
        // OPTIMISTIC CONCURRENCY WITH xmin
        // PostgreSQL xmin system column auto-updates on every row change
        // ═══════════════════════════════════════════════════════════════
        builder.Property(o => o.RowVersion)
            .IsRowVersion();  // Npgsql maps this to xmin automatically
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
        // Another user modified this row since we loaded it
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
        throw new ConcurrencyException("Order was modified by another user. Please refresh and try again.");
    }
}
```

### Retry with Exponential Backoff (Polly)

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
using Polly;
using Polly.Retry;

// Configure retry policy for transient database errors
services.AddResiliencePipeline("database", builder =>
{
    builder.AddRetry(new RetryStrategyOptions
    {
        ShouldHandle = new PredicateBuilder()
            .Handle<DbUpdateConcurrencyException>()
            .Handle<NpgsqlException>(ex => ex.IsTransient),
        MaxRetryAttempts = 3,
        Delay = TimeSpan.FromMilliseconds(200),
        BackoffType = DelayBackoffType.Exponential,
        UseJitter = true,  // Adds randomness to prevent thundering herd
        OnRetry = static args =>
        {
            Console.WriteLine($"Retry attempt {args.AttemptNumber} after {args.RetryDelay}");
            return default;
        }
    });
});
```

```csharp
// Usage in handler
public class UpdateOrderHandler : ICommandHandler<UpdateOrderCommand, Unit>
{
    private readonly ResiliencePipeline _pipeline;

    public async Task<Unit> HandleAsync(UpdateOrderCommand command, CancellationToken ct)
    {
        await _pipeline.ExecuteAsync(async token =>
        {
            var order = await _repository.GetByIdAsync(command.OrderId, token);
            order.Update(command.Status);
            await _repository.UpdateAsync(order, token);
        }, ct);

        return Unit.Value;
    }
}
```

### DbContext Pooling for High Performance

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
services.AddDbContextPool<ApplicationDbContext>(options =>
{
    options.UseNpgsql(connectionString)
           .UseSnakeCaseNamingConvention();
}, poolSize: 128);  // Default is 1024, tune based on load

// For even higher performance, use PooledDbContextFactory
services.AddPooledDbContextFactory<ApplicationDbContext>(options =>
{
    options.UseNpgsql(connectionString)
           .UseSnakeCaseNamingConvention();
});
```

```csharp
// Usage with PooledDbContextFactory (avoids DI overhead)
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
var connectionString = new NpgsqlConnectionStringBuilder
{
    Host = "localhost",
    Database = "mydb",
    Username = "app_user",
    Password = "secret",

    // ═══════════════════════════════════════════════════════════════
    // CONNECTION POOLING SETTINGS
    // ═══════════════════════════════════════════════════════════════
    Pooling = true,
    MinPoolSize = 10,           // Keep 10 connections warm
    MaxPoolSize = 100,          // Maximum concurrent connections
    ConnectionIdleLifetime = 300, // Close idle connections after 5 min
    ConnectionPruningInterval = 10, // Check for idle every 10 sec

    // ═══════════════════════════════════════════════════════════════
    // TIMEOUT SETTINGS
    // ═══════════════════════════════════════════════════════════════
    Timeout = 30,               // Connection timeout in seconds
    CommandTimeout = 60,        // Query timeout in seconds

    // ═══════════════════════════════════════════════════════════════
    // PERFORMANCE SETTINGS
    // ═══════════════════════════════════════════════════════════════
    MaxAutoPrepare = 20,        // Auto-prepare frequently used queries
    AutoPrepareMinUsages = 5,   // Prepare after 5 uses
    WriteBufferSize = 16384,    // 16KB write buffer
    ReadBufferSize = 16384,     // 16KB read buffer

    // ═══════════════════════════════════════════════════════════════
    // MULTIPLEXING (Npgsql 6.0+)
    // ═══════════════════════════════════════════════════════════════
    Multiplexing = true,        // Share connections for multiple commands

    // ═══════════════════════════════════════════════════════════════
    // SSL FOR PRODUCTION
    // ═══════════════════════════════════════════════════════════════
    SslMode = SslMode.Require,
    TrustServerCertificate = false
}.ConnectionString;
```

### Row-Level Locking for Critical Operations

```sql
-- ✅ SELECT FOR UPDATE - Lock rows during transaction
SELECT * FROM accounts WHERE id = $1 FOR UPDATE;

-- ✅ Skip locked rows (for queue processing)
SELECT * FROM jobs
WHERE status = 'pending'
ORDER BY created_at
LIMIT 10
FOR UPDATE SKIP LOCKED;

-- ✅ NOWAIT - Fail immediately if locked
SELECT * FROM accounts WHERE id = $1 FOR UPDATE NOWAIT;
```

```csharp
// EF Core equivalent using raw SQL
public async Task<Account?> GetForUpdateAsync(Guid id, CancellationToken ct)
{
    return await context.Accounts
        .FromSqlInterpolated($"SELECT * FROM accounts WHERE id = {id} FOR UPDATE")
        .FirstOrDefaultAsync(ct);
}

// Queue processing with SKIP LOCKED
public async Task<List<Job>> GetPendingJobsAsync(int batchSize, CancellationToken ct)
{
    return await context.Jobs
        .FromSqlInterpolated($@"
            SELECT * FROM jobs
            WHERE status = 'pending'
            ORDER BY created_at
            LIMIT {batchSize}
            FOR UPDATE SKIP LOCKED")
        .ToListAsync(ct);
}
```

### Advisory Locks for Distributed Coordination

```sql
-- Application-level locks (not row-level)
-- Lock is held until session ends or explicitly released

-- Acquire blocking lock
SELECT pg_advisory_lock(12345);

-- Try to acquire (returns true/false immediately)
SELECT pg_try_advisory_lock(12345);

-- Release lock
SELECT pg_advisory_unlock(12345);
```

```csharp
// EF Core advisory lock helper
public class AdvisoryLockService
{
    private readonly ApplicationDbContext _context;

    public async Task<bool> TryAcquireLockAsync(long lockId, CancellationToken ct)
    {
        var result = await _context.Database
            .SqlQuery<bool>($"SELECT pg_try_advisory_lock({lockId})")
            .FirstAsync(ct);
        return result;
    }

    public async Task ReleaseLockAsync(long lockId, CancellationToken ct)
    {
        await _context.Database
            .ExecuteSqlAsync($"SELECT pg_advisory_unlock({lockId})", ct);
    }
}

// Usage for distributed singleton operations
public async Task ProcessDailyReportAsync(CancellationToken ct)
{
    const long DAILY_REPORT_LOCK = 1001;

    if (!await _lockService.TryAcquireLockAsync(DAILY_REPORT_LOCK, ct))
    {
        _logger.LogInformation("Another instance is processing the daily report");
        return;
    }

    try
    {
        // Only one instance executes this
        await GenerateReportAsync(ct);
    }
    finally
    {
        await _lockService.ReleaseLockAsync(DAILY_REPORT_LOCK, ct);
    }
}
```

### Disable Thread Safety Checks (High Performance)

```csharp
// ⚠️ Only after thorough testing!
// Saves ~50ns per operation but removes safety checks
services.AddDbContext<ApplicationDbContext>(options =>
{
    options.UseNpgsql(connectionString)
           .UseSnakeCaseNamingConvention()
           .EnableThreadSafetyChecks(false);  // Disable in production
});
```

---

## Critical Rules

1. **Use snake_case** - PostgreSQL standard, use EFCore.NamingConventions
2. **Use text over varchar** - Unless you need length enforcement
3. **Always use timestamptz** - Store times in UTC
4. **Index foreign keys** - EF Core does this automatically
5. **Use uuid for PKs** - Better for distributed systems
6. **Use jsonb not json** - Binary format is faster
7. **Parameterize queries** - Prevent SQL injection
8. **Monitor index usage** - Drop unused indexes
9. **Use connection pooling** - Enabled by default
10. **Run ANALYZE regularly** - Keep statistics current
11. **Use xmin for optimistic concurrency** - Auto-updates on every row change
12. **Implement retry with backoff** - Handle transient failures gracefully

---

## Related Skills

- `06-ef-core-configuration` - EF Core entity configurations
- `05-repository-pattern` - Data access patterns
- `19-dapper-query-builder` - Raw SQL with Dapper
- `01-dotnet-clean-architecture` - Overall architecture
