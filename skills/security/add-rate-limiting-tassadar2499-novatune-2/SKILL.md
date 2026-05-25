---
description: Configure rate limiting policies for API endpoints with sliding window limits
---
# Add Rate Limiting Skill

Configure rate limiting for NovaTune API endpoints.

## Project Context

- Configuration: `src/NovaTuneApp/NovaTuneApp.ApiService/appsettings.json`
- Rate limit setup: `src/NovaTuneApp/NovaTuneApp.ApiService/Program.cs`
- Policies: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/RateLimiting/`

## Steps

### 1. Add Configuration Section

Location: `appsettings.json`

```json
{
  "RateLimiting": {
    "Auth": {
      "LoginPerIp": { "PermitLimit": 10, "WindowMinutes": 1 },
      "LoginPerAccount": { "PermitLimit": 5, "WindowMinutes": 1 },
      "RegisterPerIp": { "PermitLimit": 10, "WindowMinutes": 1 },
      "RefreshPerIp": { "PermitLimit": 20, "WindowMinutes": 1 }
    },
    "Upload": {
      "PerUser": { "PermitLimit": 20, "WindowMinutes": 60 },
      "BurstPerUser": { "PermitLimit": 5, "WindowMinutes": 1 }
    },
    "Streaming": {
      "PerUser": { "PermitLimit": 60, "WindowMinutes": 1 },
      "PerTrack": { "PermitLimit": 10, "WindowMinutes": 1 }
    },
    "Telemetry": {
      "PerDevice": { "PermitLimit": 120, "WindowMinutes": 1 }
    }
  }
}
```

### 2. Create Rate Limit Settings Classes

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Configuration/RateLimitSettings.cs`

```csharp
public class RateLimitSettings
{
    public const string SectionName = "RateLimiting";

    public AuthRateLimits Auth { get; set; } = new();
    public UploadRateLimits Upload { get; set; } = new();
    public StreamingRateLimits Streaming { get; set; } = new();
    public TelemetryRateLimits Telemetry { get; set; } = new();
}

public class AuthRateLimits
{
    public RateLimitPolicy LoginPerIp { get; set; } = new(10, 1);
    public RateLimitPolicy LoginPerAccount { get; set; } = new(5, 1);
    public RateLimitPolicy RegisterPerIp { get; set; } = new(10, 1);
    public RateLimitPolicy RefreshPerIp { get; set; } = new(20, 1);
}

public class UploadRateLimits
{
    public RateLimitPolicy PerUser { get; set; } = new(20, 60);
    public RateLimitPolicy BurstPerUser { get; set; } = new(5, 1);
}

public class StreamingRateLimits
{
    public RateLimitPolicy PerUser { get; set; } = new(60, 1);
    public RateLimitPolicy PerTrack { get; set; } = new(10, 1);
}

public class TelemetryRateLimits
{
    public RateLimitPolicy PerDevice { get; set; } = new(120, 1);
}

public record RateLimitPolicy(int PermitLimit, int WindowMinutes);
```

### 3. Configure Rate Limiting in Program.cs

```csharp
using System.Threading.RateLimiting;

var rateLimitSettings = builder.Configuration
    .GetSection(RateLimitSettings.SectionName)
    .Get<RateLimitSettings>() ?? new();

builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;

    // Global policy for unmatched endpoints
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
        RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: context.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1),
                SegmentsPerWindow = 4
            }));

    // Auth: Login per IP
    options.AddPolicy("auth-login-ip", context =>
        RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: context.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = rateLimitSettings.Auth.LoginPerIp.PermitLimit,
                Window = TimeSpan.FromMinutes(rateLimitSettings.Auth.LoginPerIp.WindowMinutes),
                SegmentsPerWindow = 4
            }));

    // Auth: Login per account (extracted from request body - needs custom logic)
    options.AddPolicy("auth-login-account", context =>
        RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: GetAccountKeyFromRequest(context),
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = rateLimitSettings.Auth.LoginPerAccount.PermitLimit,
                Window = TimeSpan.FromMinutes(rateLimitSettings.Auth.LoginPerAccount.WindowMinutes),
                SegmentsPerWindow = 4
            }));

    // Auth: Register per IP
    options.AddPolicy("auth-register", context =>
        RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: context.Connection.RemoteIpAddress?.ToString() ?? "unknown",
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = rateLimitSettings.Auth.RegisterPerIp.PermitLimit,
                Window = TimeSpan.FromMinutes(rateLimitSettings.Auth.RegisterPerIp.WindowMinutes),
                SegmentsPerWindow = 4
            }));

    // Upload per user
    options.AddPolicy("upload-user", context =>
        RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: context.User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "anonymous",
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = rateLimitSettings.Upload.PerUser.PermitLimit,
                Window = TimeSpan.FromMinutes(rateLimitSettings.Upload.PerUser.WindowMinutes),
                SegmentsPerWindow = 6
            }));

    // Streaming per user
    options.AddPolicy("streaming-user", context =>
        RateLimitPartition.GetSlidingWindowLimiter(
            partitionKey: context.User.FindFirstValue(ClaimTypes.NameIdentifier) ?? "anonymous",
            factory: _ => new SlidingWindowRateLimiterOptions
            {
                PermitLimit = rateLimitSettings.Streaming.PerUser.PermitLimit,
                Window = TimeSpan.FromMinutes(rateLimitSettings.Streaming.PerUser.WindowMinutes),
                SegmentsPerWindow = 4
            }));

    // On rejected: add Retry-After header
    options.OnRejected = async (context, token) =>
    {
        context.HttpContext.Response.StatusCode = StatusCodes.Status429TooManyRequests;

        if (context.Lease.TryGetMetadata(MetadataName.RetryAfter, out var retryAfter))
        {
            context.HttpContext.Response.Headers.RetryAfter =
                ((int)retryAfter.TotalSeconds).ToString();
        }

        // Return Problem Details
        await context.HttpContext.Response.WriteAsJsonAsync(new ProblemDetails
        {
            Type = "https://novatune.example/errors/rate-limit-exceeded",
            Title = "Rate Limit Exceeded",
            Status = StatusCodes.Status429TooManyRequests,
            Detail = "Too many requests. Please try again later."
        }, token);

        // Log the violation
        var logger = context.HttpContext.RequestServices
            .GetRequiredService<ILogger<Program>>();
        logger.LogWarning(
            "Rate limit exceeded for {Endpoint} from {IP}",
            context.HttpContext.Request.Path,
            context.HttpContext.Connection.RemoteIpAddress);
    };
});

// Helper to extract email from login request
static string GetAccountKeyFromRequest(HttpContext context)
{
    // For login endpoint, extract email from request
    // This requires request body buffering
    if (context.Items.TryGetValue("login-email", out var email) && email is string emailStr)
        return emailStr.ToLowerInvariant();

    return context.Connection.RemoteIpAddress?.ToString() ?? "unknown";
}
```

### 4. Apply Rate Limiting Middleware

```csharp
// After app.Build()
app.UseRateLimiter();

// Apply to auth endpoints
app.MapPost("/auth/login", Login)
    .RequireRateLimiting("auth-login-ip");

app.MapPost("/auth/register", Register)
    .RequireRateLimiting("auth-register");

// Apply to upload endpoints
app.MapPost("/tracks/upload/initiate", InitiateUpload)
    .RequireRateLimiting("upload-user");

// Apply to streaming endpoints
app.MapPost("/tracks/{id}/stream", GetStreamUrl)
    .RequireRateLimiting("streaming-user");
```

### 5. Create Middleware for Account-Based Rate Limiting

For login endpoint, extract email before rate limiting:

```csharp
public class LoginRateLimitMiddleware
{
    private readonly RequestDelegate _next;

    public LoginRateLimitMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context)
    {
        if (context.Request.Path.StartsWithSegments("/auth/login") &&
            context.Request.Method == "POST")
        {
            context.Request.EnableBuffering();

            using var reader = new StreamReader(context.Request.Body, leaveOpen: true);
            var body = await reader.ReadToEndAsync();
            context.Request.Body.Position = 0;

            try
            {
                var login = JsonSerializer.Deserialize<LoginRequest>(body);
                if (login?.Email != null)
                {
                    context.Items["login-email"] = login.Email;
                }
            }
            catch { /* Ignore parse errors */ }
        }

        await _next(context);
    }
}

// Register before rate limiter
app.UseMiddleware<LoginRateLimitMiddleware>();
app.UseRateLimiter();
```

## Default Rate Limits (NF-2.5)

| Endpoint | Per IP | Per Account/User | Window |
|----------|--------|------------------|--------|
| `/auth/login` | 10 | 5 | 1 min |
| `/auth/register` | 10 | N/A | 1 min |
| `/auth/refresh` | 20 | N/A | 1 min |
| `/tracks/upload/initiate` | N/A | 20 (burst: 5/min) | 1 hour |
| `/tracks/{id}/stream` | N/A | 60 | 1 min |
| `/telemetry/*` | N/A | 120/device | 1 min |

## Response Format

When rate limited, return HTTP 429 with:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
Content-Type: application/problem+json

{
  "type": "https://novatune.example/errors/rate-limit-exceeded",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "Too many requests. Please try again later."
}
```

## Testing

```csharp
[Fact]
public async Task Login_Returns429_WhenRateLimitExceeded()
{
    // Make 11 requests (limit is 10)
    for (int i = 0; i < 11; i++)
    {
        var response = await _client.PostAsJsonAsync("/auth/login", new
        {
            Email = "test@example.com",
            Password = "wrong"
        });

        if (i < 10)
        {
            response.StatusCode.Should().NotBe(HttpStatusCode.TooManyRequests);
        }
        else
        {
            response.StatusCode.Should().Be(HttpStatusCode.TooManyRequests);
            response.Headers.Should().ContainKey("Retry-After");
        }
    }
}
```

## Observability

Log rate limit violations for monitoring:

```csharp
logger.LogWarning(
    "Rate limit exceeded: Endpoint={Endpoint}, IP={IP}, Policy={Policy}",
    context.Request.Path,
    context.Connection.RemoteIpAddress,
    policyName);
```

Add metrics:

```csharp
_meter.CreateCounter<long>("rate_limit_exceeded_total")
    .Add(1, new KeyValuePair<string, object?>("endpoint", endpoint));
```