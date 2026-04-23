---
name: rate-limiting
description: "Implements ASP.NET Core rate limiting middleware for API protection. Covers fixed window, sliding window, token bucket, and concurrency limiters with custom policies."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Microsoft.AspNetCore.RateLimiting
---

# Rate Limiting Middleware for ASP.NET Core

## Overview

Built-in rate limiting middleware (ASP.NET Core 7+) protects APIs from abuse:

- **Fixed Window** - Reset counter at fixed intervals
- **Sliding Window** - Smoothed fixed window
- **Token Bucket** - Allow bursts, refill over time
- **Concurrency** - Limit simultaneous requests

## Quick Reference

| Algorithm | Best For | Characteristics |
|-----------|----------|-----------------|
| Fixed Window | Simple rate limits | Counter resets at interval boundary |
| Sliding Window | Smoother limiting | Weighted average across segments |
| Token Bucket | Burst tolerance | Allows bursts up to bucket size |
| Concurrency | Resource protection | Limits parallel requests |

---

## Rate Limiting Structure

```
/API/RateLimiting/
├── RateLimitingConfiguration.cs
├── Policies/
│   ├── UserRateLimitPolicy.cs
│   └── IpRateLimitPolicy.cs
└── Middleware/
    └── RateLimitExceededHandler.cs
```

---

## Template: Basic Rate Limiting Configuration

```csharp
// src/{name}.api/Program.cs
using System.Threading.RateLimiting;
using Microsoft.AspNetCore.RateLimiting;

var builder = WebApplication.CreateBuilder(args);

// ═══════════════════════════════════════════════════════════════
// RATE LIMITING CONFIGURATION
// ═══════════════════════════════════════════════════════════════
builder.Services.AddRateLimiter(options =>
{
    // Global limiter settings
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;

    // ═══════════════════════════════════════════════════════════════
    // FIXED WINDOW POLICY
    // Allows N requests per time window, resets at window boundary
    // ═══════════════════════════════════════════════════════════════
    options.AddFixedWindowLimiter("fixed", limiterOptions =>
    {
        limiterOptions.PermitLimit = 100;                           // Requests per window
        limiterOptions.Window = TimeSpan.FromMinutes(1);            // Window duration
        limiterOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        limiterOptions.QueueLimit = 10;                             // Queue when limit exceeded
    });

    // ═══════════════════════════════════════════════════════════════
    // SLIDING WINDOW POLICY
    // Smoother rate limiting with segments
    // ═══════════════════════════════════════════════════════════════
    options.AddSlidingWindowLimiter("sliding", limiterOptions =>
    {
        limiterOptions.PermitLimit = 100;
        limiterOptions.Window = TimeSpan.FromMinutes(1);
        limiterOptions.SegmentsPerWindow = 6;                       // 6 segments = 10s each
        limiterOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        limiterOptions.QueueLimit = 10;
    });

    // ═══════════════════════════════════════════════════════════════
    // TOKEN BUCKET POLICY
    // Allows bursts, then rate-limited
    // ═══════════════════════════════════════════════════════════════
    options.AddTokenBucketLimiter("token", limiterOptions =>
    {
        limiterOptions.TokenLimit = 100;                            // Maximum tokens (bucket size)
        limiterOptions.ReplenishmentPeriod = TimeSpan.FromSeconds(1);
        limiterOptions.TokensPerPeriod = 10;                        // Tokens added per period
        limiterOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        limiterOptions.QueueLimit = 10;
        limiterOptions.AutoReplenishment = true;
    });

    // ═══════════════════════════════════════════════════════════════
    // CONCURRENCY LIMITER
    // Limits simultaneous requests (not rate)
    // ═══════════════════════════════════════════════════════════════
    options.AddConcurrencyLimiter("concurrency", limiterOptions =>
    {
        limiterOptions.PermitLimit = 50;                            // Max concurrent requests
        limiterOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        limiterOptions.QueueLimit = 25;
    });

    // Custom response for rejected requests
    options.OnRejected = async (context, cancellationToken) =>
    {
        if (context.Lease.TryGetMetadata(MetadataName.RetryAfter, out var retryAfter))
        {
            context.HttpContext.Response.Headers.RetryAfter =
                ((int)retryAfter.TotalSeconds).ToString();
        }

        context.HttpContext.Response.StatusCode = StatusCodes.Status429TooManyRequests;
        await context.HttpContext.Response.WriteAsJsonAsync(new
        {
            error = "Too many requests",
            message = "Rate limit exceeded. Please try again later.",
            retryAfterSeconds = retryAfter?.TotalSeconds ?? 60
        }, cancellationToken);
    };
});

var app = builder.Build();

// ═══════════════════════════════════════════════════════════════
// MIDDLEWARE ORDER - Rate limiting before authentication
// ═══════════════════════════════════════════════════════════════
app.UseRateLimiter();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();
```

---

## Template: Policy-Based Rate Limiting

```csharp
// src/{name}.api/RateLimiting/RateLimitPolicies.cs
namespace {name}.api.ratelimiting;

public static class RateLimitPolicies
{
    // Policy names
    public const string Anonymous = "anonymous";
    public const string Authenticated = "authenticated";
    public const string Premium = "premium";
    public const string Api = "api";
    public const string Upload = "upload";
}
```

```csharp
// src/{name}.api/RateLimiting/RateLimitingConfiguration.cs
using System.Threading.RateLimiting;
using Microsoft.AspNetCore.RateLimiting;

namespace {name}.api.ratelimiting;

public static class RateLimitingConfiguration
{
    public static IServiceCollection AddRateLimitingPolicies(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var settings = configuration
            .GetSection("RateLimiting")
            .Get<RateLimitSettings>() ?? new RateLimitSettings();

        services.AddRateLimiter(options =>
        {
            options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;

            // ═══════════════════════════════════════════════════════════════
            // ANONYMOUS USERS - Stricter limits
            // ═══════════════════════════════════════════════════════════════
            options.AddFixedWindowLimiter(RateLimitPolicies.Anonymous, limiterOptions =>
            {
                limiterOptions.PermitLimit = settings.AnonymousRequestsPerMinute;
                limiterOptions.Window = TimeSpan.FromMinutes(1);
                limiterOptions.QueueLimit = 5;
            });

            // ═══════════════════════════════════════════════════════════════
            // AUTHENTICATED USERS - More generous limits
            // ═══════════════════════════════════════════════════════════════
            options.AddTokenBucketLimiter(RateLimitPolicies.Authenticated, limiterOptions =>
            {
                limiterOptions.TokenLimit = settings.AuthenticatedBurstLimit;
                limiterOptions.ReplenishmentPeriod = TimeSpan.FromSeconds(1);
                limiterOptions.TokensPerPeriod = settings.AuthenticatedTokensPerSecond;
                limiterOptions.QueueLimit = 20;
            });

            // ═══════════════════════════════════════════════════════════════
            // PREMIUM USERS - Highest limits
            // ═══════════════════════════════════════════════════════════════
            options.AddTokenBucketLimiter(RateLimitPolicies.Premium, limiterOptions =>
            {
                limiterOptions.TokenLimit = settings.PremiumBurstLimit;
                limiterOptions.ReplenishmentPeriod = TimeSpan.FromSeconds(1);
                limiterOptions.TokensPerPeriod = settings.PremiumTokensPerSecond;
                limiterOptions.QueueLimit = 50;
            });

            // ═══════════════════════════════════════════════════════════════
            // API ENDPOINTS - Per-endpoint limiting
            // ═══════════════════════════════════════════════════════════════
            options.AddSlidingWindowLimiter(RateLimitPolicies.Api, limiterOptions =>
            {
                limiterOptions.PermitLimit = settings.ApiRequestsPerMinute;
                limiterOptions.Window = TimeSpan.FromMinutes(1);
                limiterOptions.SegmentsPerWindow = 6;
                limiterOptions.QueueLimit = 10;
            });

            // ═══════════════════════════════════════════════════════════════
            // FILE UPLOADS - Concurrency limited
            // ═══════════════════════════════════════════════════════════════
            options.AddConcurrencyLimiter(RateLimitPolicies.Upload, limiterOptions =>
            {
                limiterOptions.PermitLimit = settings.MaxConcurrentUploads;
                limiterOptions.QueueLimit = settings.UploadQueueSize;
            });

            // Global rejection handler
            options.OnRejected = HandleRejection;
        });

        return services;
    }

    private static async ValueTask HandleRejection(
        OnRejectedContext context,
        CancellationToken cancellationToken)
    {
        var response = context.HttpContext.Response;

        // Set retry-after header if available
        if (context.Lease.TryGetMetadata(MetadataName.RetryAfter, out var retryAfter))
        {
            response.Headers.RetryAfter = ((int)retryAfter.TotalSeconds).ToString();
        }

        // Log the rejection
        var logger = context.HttpContext.RequestServices
            .GetRequiredService<ILogger<RateLimitingConfiguration>>();

        var clientIp = context.HttpContext.Connection.RemoteIpAddress?.ToString() ?? "unknown";
        var path = context.HttpContext.Request.Path;

        logger.LogWarning(
            "Rate limit exceeded for client {ClientIp} on path {Path}",
            clientIp,
            path);

        response.StatusCode = StatusCodes.Status429TooManyRequests;
        response.ContentType = "application/json";

        await response.WriteAsJsonAsync(new
        {
            type = "https://tools.ietf.org/html/rfc6585#section-4",
            title = "Too Many Requests",
            status = 429,
            detail = "Rate limit exceeded. Please slow down your requests.",
            retryAfter = retryAfter?.TotalSeconds ?? 60
        }, cancellationToken);
    }
}
```

### Settings Class

```csharp
// src/{name}.api/RateLimiting/RateLimitSettings.cs
namespace {name}.api.ratelimiting;

public sealed class RateLimitSettings
{
    public int AnonymousRequestsPerMinute { get; set; } = 30;
    public int AuthenticatedBurstLimit { get; set; } = 100;
    public int AuthenticatedTokensPerSecond { get; set; } = 10;
    public int PremiumBurstLimit { get; set; } = 500;
    public int PremiumTokensPerSecond { get; set; } = 50;
    public int ApiRequestsPerMinute { get; set; } = 60;
    public int MaxConcurrentUploads { get; set; } = 5;
    public int UploadQueueSize { get; set; } = 10;
}
```

### appsettings.json

```json
{
  "RateLimiting": {
    "AnonymousRequestsPerMinute": 30,
    "AuthenticatedBurstLimit": 100,
    "AuthenticatedTokensPerSecond": 10,
    "PremiumBurstLimit": 500,
    "PremiumTokensPerSecond": 50,
    "ApiRequestsPerMinute": 60,
    "MaxConcurrentUploads": 5,
    "UploadQueueSize": 10
  }
}
```

---

## Template: User-Based Rate Limiting (Partitioned)

```csharp
// src/{name}.api/Program.cs
builder.Services.AddRateLimiter(options =>
{
    // ═══════════════════════════════════════════════════════════════
    // PARTITIONED BY USER ID
    // Each user has their own rate limit bucket
    // ═══════════════════════════════════════════════════════════════
    options.AddPolicy("per-user", httpContext =>
    {
        var userId = httpContext.User.FindFirstValue(ClaimTypes.NameIdentifier);

        if (string.IsNullOrEmpty(userId))
        {
            // Anonymous users - stricter limit, partition by IP
            var clientIp = httpContext.Connection.RemoteIpAddress?.ToString() ?? "anonymous";

            return RateLimitPartition.GetFixedWindowLimiter(
                partitionKey: clientIp,
                factory: _ => new FixedWindowRateLimiterOptions
                {
                    PermitLimit = 30,
                    Window = TimeSpan.FromMinutes(1)
                });
        }

        // Authenticated users - more generous
        return RateLimitPartition.GetTokenBucketLimiter(
            partitionKey: userId,
            factory: _ => new TokenBucketRateLimiterOptions
            {
                TokenLimit = 100,
                ReplenishmentPeriod = TimeSpan.FromSeconds(1),
                TokensPerPeriod = 10
            });
    });

    // ═══════════════════════════════════════════════════════════════
    // PARTITIONED BY SUBSCRIPTION TIER
    // Different limits based on user's subscription
    // ═══════════════════════════════════════════════════════════════
    options.AddPolicy("tier-based", httpContext =>
    {
        var userId = httpContext.User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "anonymous";
        var tier = httpContext.User.FindFirstValue("subscription_tier") ?? "free";

        return tier switch
        {
            "enterprise" => RateLimitPartition.GetNoLimiter(userId),

            "premium" => RateLimitPartition.GetTokenBucketLimiter(
                partitionKey: userId,
                factory: _ => new TokenBucketRateLimiterOptions
                {
                    TokenLimit = 500,
                    ReplenishmentPeriod = TimeSpan.FromSeconds(1),
                    TokensPerPeriod = 50
                }),

            "basic" => RateLimitPartition.GetTokenBucketLimiter(
                partitionKey: userId,
                factory: _ => new TokenBucketRateLimiterOptions
                {
                    TokenLimit = 100,
                    ReplenishmentPeriod = TimeSpan.FromSeconds(1),
                    TokensPerPeriod = 10
                }),

            _ => RateLimitPartition.GetFixedWindowLimiter(
                partitionKey: userId,
                factory: _ => new FixedWindowRateLimiterOptions
                {
                    PermitLimit = 20,
                    Window = TimeSpan.FromMinutes(1)
                })
        };
    });
});
```

---

## Template: Applying Rate Limits to Endpoints

### Minimal API Endpoints

```csharp
// src/{name}.api/Endpoints/OrderEndpoints.cs
public static class OrderEndpoints
{
    public static void MapOrderEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders")
            .WithTags("Orders")
            .RequireAuthorization();

        // ═══════════════════════════════════════════════════════════════
        // APPLY RATE LIMIT TO SINGLE ENDPOINT
        // ═══════════════════════════════════════════════════════════════
        group.MapGet("/", GetOrders)
            .RequireRateLimiting(RateLimitPolicies.Api);

        group.MapGet("/{id:guid}", GetOrderById)
            .RequireRateLimiting(RateLimitPolicies.Api);

        // ═══════════════════════════════════════════════════════════════
        // STRICTER LIMIT FOR WRITE OPERATIONS
        // ═══════════════════════════════════════════════════════════════
        group.MapPost("/", CreateOrder)
            .RequireRateLimiting(RateLimitPolicies.Authenticated);

        // ═══════════════════════════════════════════════════════════════
        // DISABLE RATE LIMITING FOR SPECIFIC ENDPOINT
        // ═══════════════════════════════════════════════════════════════
        group.MapGet("/health", () => Results.Ok())
            .DisableRateLimiting();
    }
}
```

### Controllers

```csharp
// src/{name}.api/Controllers/OrdersController.cs
using Microsoft.AspNetCore.RateLimiting;

namespace {name}.api.controllers;

[ApiController]
[Route("api/[controller]")]
[EnableRateLimiting(RateLimitPolicies.Api)]  // Apply to all actions
public sealed class OrdersController : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> GetOrders()
    {
        // Uses controller-level rate limit
    }

    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetOrderById(Guid id)
    {
        // Uses controller-level rate limit
    }

    [HttpPost]
    [EnableRateLimiting(RateLimitPolicies.Authenticated)]  // Override for this action
    public async Task<IActionResult> CreateOrder([FromBody] CreateOrderRequest request)
    {
        // Uses action-level rate limit
    }

    [HttpGet("export")]
    [EnableRateLimiting(RateLimitPolicies.Premium)]  // Expensive operation
    public async Task<IActionResult> ExportOrders()
    {
        // Uses premium rate limit
    }

    [HttpGet("health")]
    [DisableRateLimiting]  // Health checks shouldn't be rate limited
    public IActionResult Health()
    {
        return Ok();
    }
}
```

### Group-Level Rate Limiting

```csharp
// src/{name}.api/Endpoints/PublicApiEndpoints.cs
public static void MapPublicApiEndpoints(this IEndpointRouteBuilder app)
{
    // Apply rate limit to entire group
    var group = app.MapGroup("/api/public")
        .RequireRateLimiting(RateLimitPolicies.Anonymous);

    group.MapGet("/products", GetProducts);
    group.MapGet("/categories", GetCategories);
}
```

---

## Template: Distributed Rate Limiting with Redis

```csharp
// src/{name}.api/RateLimiting/RedisRateLimitingConfiguration.cs
using System.Threading.RateLimiting;
using StackExchange.Redis;

namespace {name}.api.ratelimiting;

/// <summary>
/// For distributed systems, implement custom rate limiter with Redis
/// to share rate limit state across multiple instances.
/// </summary>
public static class RedisRateLimitingConfiguration
{
    public static IServiceCollection AddDistributedRateLimiting(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var redisConnection = configuration.GetConnectionString("Redis");

        services.AddSingleton<IConnectionMultiplexer>(
            ConnectionMultiplexer.Connect(redisConnection!));

        services.AddRateLimiter(options =>
        {
            options.AddPolicy("distributed", context =>
            {
                var redis = context.RequestServices
                    .GetRequiredService<IConnectionMultiplexer>();

                var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier)
                    ?? context.Connection.RemoteIpAddress?.ToString()
                    ?? "anonymous";

                return RateLimitPartition.Get(
                    partitionKey: userId,
                    factory: key => new RedisRateLimiter(
                        redis: redis,
                        partitionKey: key,
                        options: new RedisRateLimiterOptions
                        {
                            PermitLimit = 100,
                            Window = TimeSpan.FromMinutes(1)
                        }));
            });
        });

        return services;
    }
}

/// <summary>
/// Custom rate limiter using Redis for distributed state
/// </summary>
public sealed class RedisRateLimiter : RateLimiter
{
    private readonly IConnectionMultiplexer _redis;
    private readonly string _partitionKey;
    private readonly RedisRateLimiterOptions _options;

    public RedisRateLimiter(
        IConnectionMultiplexer redis,
        string partitionKey,
        RedisRateLimiterOptions options)
    {
        _redis = redis;
        _partitionKey = partitionKey;
        _options = options;
    }

    public override TimeSpan? IdleDuration => null;

    public override RateLimiterStatistics? GetStatistics() => null;

    protected override async ValueTask<RateLimitLease> AcquireAsyncCore(
        int permitCount,
        CancellationToken cancellationToken)
    {
        var db = _redis.GetDatabase();
        var key = $"rate_limit:{_partitionKey}";
        var now = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
        var windowStart = now - (long)_options.Window.TotalSeconds;

        // Remove old entries outside the window
        await db.SortedSetRemoveRangeByScoreAsync(key, 0, windowStart);

        // Count current requests in window
        var currentCount = await db.SortedSetLengthAsync(key);

        if (currentCount >= _options.PermitLimit)
        {
            // Get oldest entry to calculate retry-after
            var oldest = await db.SortedSetRangeByRankWithScoresAsync(key, 0, 0);
            var retryAfter = oldest.Length > 0
                ? TimeSpan.FromSeconds(oldest[0].Score + _options.Window.TotalSeconds - now)
                : _options.Window;

            return new RedisRateLimitLease(false, retryAfter);
        }

        // Add new request
        await db.SortedSetAddAsync(key, Guid.NewGuid().ToString(), now);
        await db.KeyExpireAsync(key, _options.Window.Add(TimeSpan.FromMinutes(1)));

        return new RedisRateLimitLease(true, null);
    }

    protected override RateLimitLease AttemptAcquireCore(int permitCount)
    {
        // Synchronous not supported for Redis
        return new RedisRateLimitLease(false, _options.Window);
    }
}

public sealed class RedisRateLimitLease : RateLimitLease
{
    private readonly TimeSpan? _retryAfter;

    public RedisRateLimitLease(bool isAcquired, TimeSpan? retryAfter)
    {
        IsAcquired = isAcquired;
        _retryAfter = retryAfter;
    }

    public override bool IsAcquired { get; }

    public override IEnumerable<string> MetadataNames =>
        _retryAfter.HasValue ? new[] { MetadataName.RetryAfter.Name } : Array.Empty<string>();

    public override bool TryGetMetadata(string metadataName, out object? metadata)
    {
        if (metadataName == MetadataName.RetryAfter.Name && _retryAfter.HasValue)
        {
            metadata = _retryAfter.Value;
            return true;
        }

        metadata = null;
        return false;
    }
}

public sealed class RedisRateLimiterOptions
{
    public int PermitLimit { get; set; } = 100;
    public TimeSpan Window { get; set; } = TimeSpan.FromMinutes(1);
}
```

---

## Algorithm Selection Guide

```
┌────────────────────────────────────────────────────────────────┐
│                Which Rate Limiting Algorithm?                   │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Need to limit concurrent requests (not rate)?                  │
│       │                                                         │
│       └── YES ──► Use Concurrency Limiter                       │
│                   (file uploads, heavy operations)              │
│                                                                 │
│  Need to allow bursts?                                          │
│       │                                                         │
│       └── YES ──► Use Token Bucket                              │
│                   (API calls, user actions)                     │
│                                                                 │
│  Need smooth rate limiting?                                     │
│       │                                                         │
│       └── YES ──► Use Sliding Window                            │
│                   (API rate limits, quota enforcement)          │
│                                                                 │
│  Simple time-based limit?                                       │
│       │                                                         │
│       └── YES ──► Use Fixed Window                              │
│                   (login attempts, simple limits)               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Critical Rules

1. **Choose the right algorithm** - Token bucket for bursts, sliding window for smooth limits
2. **Partition by user** - Avoid IP-only partitioning (NAT issues)
3. **Set queue limits** - Prevent memory exhaustion
4. **Include Retry-After header** - Help clients back off properly
5. **Log rejections** - Monitor for abuse patterns
6. **Test under load** - Verify limits work as expected
7. **Use distributed state** - Redis for multi-instance deployments
8. **Exempt health checks** - Don't rate limit monitoring endpoints
9. **Different limits per tier** - Premium users get higher limits
10. **Middleware order matters** - Place before auth for anonymous limits

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Partition only by IP (NAT can share IPs)
options.AddPolicy("bad", context =>
    RateLimitPartition.GetFixedWindowLimiter(
        context.Connection.RemoteIpAddress?.ToString() ?? "unknown",
        _ => new FixedWindowRateLimiterOptions { /* ... */ }));

// ✅ CORRECT: Prefer user ID, fallback to IP
options.AddPolicy("good", context =>
{
    var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);
    var partitionKey = userId ?? context.Connection.RemoteIpAddress?.ToString() ?? "anonymous";
    return RateLimitPartition.GetFixedWindowLimiter(partitionKey, /* ... */);
});

// ❌ WRONG: No queue limit (memory exhaustion risk)
options.AddFixedWindowLimiter("bad", limiter =>
{
    limiter.PermitLimit = 100;
    limiter.Window = TimeSpan.FromMinutes(1);
    // Missing QueueLimit!
});

// ✅ CORRECT: Always set queue limit
options.AddFixedWindowLimiter("good", limiter =>
{
    limiter.PermitLimit = 100;
    limiter.Window = TimeSpan.FromMinutes(1);
    limiter.QueueLimit = 10;  // Bounded queue
});

// ❌ WRONG: Rate limiting health endpoints
app.MapGet("/health", () => Results.Ok())
    .RequireRateLimiting("api");

// ✅ CORRECT: Exempt health checks
app.MapGet("/health", () => Results.Ok())
    .DisableRateLimiting();

// ❌ WRONG: Same limits for all users
options.AddFixedWindowLimiter("api", limiter =>
{
    limiter.PermitLimit = 100;  // Same for everyone
});

// ✅ CORRECT: Tier-based limits
options.AddPolicy("api", context =>
{
    var tier = context.User.FindFirstValue("tier") ?? "free";
    var limit = tier switch { "premium" => 500, "basic" => 100, _ => 20 };
    return RateLimitPartition.GetFixedWindowLimiter(/* ... */);
});
```

---

## Related Skills

- `07-minimal-api-endpoints` - Apply rate limits to endpoints
- `12-jwt-authentication` - User identification for partitioning
- `24-logging-configuration` - Log rate limit events
- `17-health-checks` - Exempt from rate limiting
