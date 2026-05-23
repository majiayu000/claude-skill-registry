---
name: noisy-neighbor-prevention
description: Resource isolation and fair usage patterns for multi-tenant systems. Covers rate limiting, resource governors, and tenant throttling.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Noisy Neighbor Prevention Skill

## When to Use This Skill

Use this skill when:

- **Noisy Neighbor Prevention tasks** - Working on resource isolation and fair usage patterns for multi-tenant systems. covers rate limiting, resource governors, and tenant throttling
- **Planning or design** - Need guidance on Noisy Neighbor Prevention approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Patterns for preventing one tenant from consuming excessive resources and impacting others.

In multi-tenant systems, a "noisy neighbor" is a tenant whose resource consumption negatively impacts other tenants. This skill covers strategies to detect, prevent, and mitigate noisy neighbor scenarios across compute, database, storage, and network resources.

## Resource Isolation Spectrum

```text
+------------------------------------------------------------------+
|                    Isolation Strategies                           |
+------------------------------------------------------------------+
| Low Isolation                                   High Isolation    |
| (Shared, Governed)                             (Dedicated)        |
+------------------------------------------------------------------+
|  +----------+  +----------+  +----------+  +----------+          |
|  | Quotas   |  | Rate     |  | Resource |  | Dedicated|          |
|  | Only     |  | Limiting |  | Pools    |  | Infra    |          |
|  +----------+  +----------+  +----------+  +----------+          |
|  Low cost       Medium cost   Higher cost   Highest cost         |
|  Low isolation  Good isolation Better        Full isolation      |
+------------------------------------------------------------------+
```

## Rate Limiting

### Tenant-Aware Rate Limiter

```csharp
public sealed class TenantRateLimiter(
    ITenantContextAccessor tenantContext,
    ITenantLimitService limits,
    IDistributedCache cache)
{
    public async Task<RateLimitResult> CheckLimitAsync(
        string resource,
        CancellationToken ct = default)
    {
        var tenantId = tenantContext.Current?.TenantId
            ?? throw new InvalidOperationException("No tenant context");

        var limit = await limits.GetLimitAsync(tenantId, resource, ct);
        var key = $"ratelimit:{tenantId}:{resource}";

        var current = await cache.GetAsync<int>(key, ct);

        if (current >= limit.MaxRequests)
        {
            return RateLimitResult.Exceeded(limit.WindowSeconds);
        }

        await cache.IncrementAsync(key, limit.WindowSeconds, ct);

        return RateLimitResult.Allowed(limit.MaxRequests - current - 1);
    }
}
```

### Rate Limit Configuration

```csharp
public sealed record TenantRateLimits
{
    public required Guid TenantId { get; init; }

    // API limits
    public int ApiRequestsPerMinute { get; init; } = 100;
    public int ApiRequestsPerHour { get; init; } = 1000;

    // Resource limits
    public int ConcurrentConnections { get; init; } = 10;
    public int MaxUploadSizeMb { get; init; } = 100;
    public int BackgroundJobsPerHour { get; init; } = 50;

    // Feature limits
    public int MaxProjects { get; init; } = 10;
    public int MaxUsersPerProject { get; init; } = 5;
    public long StorageLimitBytes { get; init; } = 1_073_741_824; // 1 GB
}
```

### ASP.NET Core Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddPolicy("tenant-api", context =>
    {
        var tenantId = context.GetTenantId();

        return RateLimitPartition.GetTokenBucketLimiter(
            partitionKey: tenantId,
            factory: _ => new TokenBucketRateLimiterOptions
            {
                TokenLimit = 100,
                QueueProcessingOrder = QueueProcessingOrder.OldestFirst,
                QueueLimit = 10,
                ReplenishmentPeriod = TimeSpan.FromMinutes(1),
                TokensPerPeriod = 100,
                AutoReplenishment = true
            });
    });
});
```

## Database Resource Governors

### SQL Server Resource Governor

```sql
-- Create workload groups for tenant tiers
CREATE RESOURCE POOL TenantStandard
WITH (
    MIN_CPU_PERCENT = 0,
    MAX_CPU_PERCENT = 25,
    MIN_MEMORY_PERCENT = 0,
    MAX_MEMORY_PERCENT = 25
);

CREATE RESOURCE POOL TenantPremium
WITH (
    MIN_CPU_PERCENT = 10,
    MAX_CPU_PERCENT = 50,
    MIN_MEMORY_PERCENT = 10,
    MAX_MEMORY_PERCENT = 50
);

-- Create workload groups
CREATE WORKLOAD GROUP StandardTenants
WITH (
    IMPORTANCE = LOW,
    REQUEST_MAX_CPU_TIME_SEC = 30,
    REQUEST_MAX_MEMORY_GRANT_PERCENT = 10,
    MAX_DOP = 2
)
USING TenantStandard;

CREATE WORKLOAD GROUP PremiumTenants
WITH (
    IMPORTANCE = HIGH,
    REQUEST_MAX_CPU_TIME_SEC = 120,
    REQUEST_MAX_MEMORY_GRANT_PERCENT = 25,
    MAX_DOP = 8
)
USING TenantPremium;

-- Classifier function
CREATE FUNCTION dbo.TenantClassifier()
RETURNS SYSNAME
WITH SCHEMABINDING
AS
BEGIN
    DECLARE @TenantTier SYSNAME;

    SELECT @TenantTier = CASE
        WHEN APP_NAME() LIKE '%Premium%' THEN 'PremiumTenants'
        ELSE 'StandardTenants'
    END;

    RETURN @TenantTier;
END;
```

### Query Timeout by Tenant

```csharp
public sealed class TenantQueryInterceptor(
    ITenantContextAccessor tenantContext) : DbCommandInterceptor
{
    public override InterceptionResult<DbDataReader> ReaderExecuting(
        DbCommand command,
        CommandEventData eventData,
        InterceptionResult<DbDataReader> result)
    {
        var timeout = GetTenantTimeout(tenantContext.Current?.TenantId);
        command.CommandTimeout = timeout;
        return result;
    }

    private static int GetTenantTimeout(Guid? tenantId)
    {
        // Default 30 seconds, premium tenants get 120
        return tenantId.HasValue ? 30 : 120;
    }
}
```

## Compute Isolation

### Thread Pool Partitioning

```csharp
public sealed class TenantThreadPool
{
    private readonly ConcurrentDictionary<Guid, SemaphoreSlim> _tenantSemaphores = new();

    public async Task<T> ExecuteAsync<T>(
        Guid tenantId,
        Func<Task<T>> work,
        int maxConcurrency = 10,
        CancellationToken ct = default)
    {
        var semaphore = _tenantSemaphores.GetOrAdd(
            tenantId,
            _ => new SemaphoreSlim(maxConcurrency));

        await semaphore.WaitAsync(ct);
        try
        {
            return await work();
        }
        finally
        {
            semaphore.Release();
        }
    }
}
```

### Background Job Queues

```csharp
public sealed class TenantJobQueue(IBackgroundJobClient jobs)
{
    public void EnqueueTenantJob<T>(Guid tenantId, Expression<Action<T>> job)
    {
        var queueName = GetQueueForTenant(tenantId);
        jobs.Enqueue(queueName, job);
    }

    private static string GetQueueForTenant(Guid tenantId)
    {
        // Hash to distribute across queues
        var bucket = Math.Abs(tenantId.GetHashCode()) % 10;
        return $"tenant-queue-{bucket}";
    }
}
```

## Storage Quotas

### Tenant Storage Tracking

```csharp
public sealed class TenantStorageService(
    IDbContext db,
    IBlobStorage storage,
    ITenantLimitService limits)
{
    public async Task<UploadResult> UploadAsync(
        Guid tenantId,
        Stream content,
        string fileName,
        CancellationToken ct)
    {
        var usage = await GetUsageAsync(tenantId, ct);
        var limit = await limits.GetStorageLimitAsync(tenantId, ct);

        if (usage.TotalBytes + content.Length > limit)
        {
            return UploadResult.QuotaExceeded(limit, usage.TotalBytes);
        }

        var blob = await storage.UploadAsync(tenantId, content, fileName, ct);

        // Track usage
        await db.TenantStorageUsage.AddAsync(new StorageUsageEntry
        {
            TenantId = tenantId,
            BlobId = blob.Id,
            SizeBytes = content.Length,
            CreatedAt = DateTimeOffset.UtcNow
        }, ct);

        await db.SaveChangesAsync(ct);

        return UploadResult.Success(blob);
    }
}
```

## Monitoring and Alerting

### Resource Usage Metrics

```csharp
public sealed class TenantMetricsCollector(
    IMeterFactory meterFactory,
    ITenantContextAccessor tenantContext)
{
    private readonly Meter _meter = meterFactory.Create("TenantMetrics");

    public void RecordApiRequest(int durationMs)
    {
        var histogram = _meter.CreateHistogram<int>("tenant.api.duration");
        histogram.Record(durationMs, new TagList
        {
            { "tenant_id", tenantContext.Current?.TenantId.ToString() ?? "unknown" }
        });
    }

    public void RecordResourceUsage(string resource, double value)
    {
        var gauge = _meter.CreateGauge<double>($"tenant.{resource}.usage");
        gauge.Record(value, new TagList
        {
            { "tenant_id", tenantContext.Current?.TenantId.ToString() ?? "unknown" }
        });
    }
}
```

### Noisy Neighbor Detection

```csharp
public sealed class NoisyNeighborDetector(
    IMetricsQuery metrics,
    IAlertService alerts)
{
    public async Task CheckAsync(CancellationToken ct)
    {
        // Get top resource consumers
        var topConsumers = await metrics.GetTopTenantsAsync(
            metric: "cpu_usage",
            period: TimeSpan.FromMinutes(5),
            limit: 10,
            ct);

        foreach (var consumer in topConsumers)
        {
            if (consumer.Usage > consumer.Limit * 0.9) // 90% threshold
            {
                await alerts.SendAsync(new NoisyNeighborAlert
                {
                    TenantId = consumer.TenantId,
                    Resource = "cpu",
                    Usage = consumer.Usage,
                    Limit = consumer.Limit
                }, ct);
            }
        }
    }
}
```

## Tier-Based Limits

```text
Resource Limits by Tier:
+------------------------------------------------------------------+
| Resource          | Free    | Starter | Pro     | Enterprise     |
+-------------------+---------+---------+---------+----------------+
| API req/min       | 10      | 100     | 1000    | 10000          |
| Concurrent conn   | 2       | 10      | 50      | Unlimited      |
| Storage (GB)      | 0.5     | 10      | 100     | Custom         |
| Upload size (MB)  | 10      | 50      | 100     | 500            |
| Query timeout (s) | 5       | 30      | 60      | 120            |
| Background jobs/h | 5       | 50      | 500     | Unlimited      |
+-------------------+---------+---------+---------+----------------+
```

## Best Practices

```text
Noisy Neighbor Prevention Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Rate limit at edge          | Block abuse early                  |
| Database resource governors | Prevent query monopolization       |
| Tier-based limits           | Fair resource allocation           |
| Real-time monitoring        | Early detection                    |
| Graceful degradation        | Maintain service for others        |
| Clear limit communication   | User understands constraints       |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| No limits | One tenant monopolizes | Implement quotas |
| Hard failures | Bad UX at limit | Graceful degradation |
| Global limits only | Unfair allocation | Per-tenant limits |
| No visibility | Users surprised | Show usage/limits |
| Static limits | Can't adjust | Tier-based configuration |

## Related Skills

- `tenancy-models` - Architecture impact on isolation
- `subscription-models` - Tier-based limit configuration
- `sharding-strategies` - Physical isolation

## MCP Research

For current patterns:

```text
perplexity: "noisy neighbor prevention multi-tenant 2024" "rate limiting ASP.NET Core"
microsoft-learn: "Azure rate limiting" "SQL Server resource governor"
```
