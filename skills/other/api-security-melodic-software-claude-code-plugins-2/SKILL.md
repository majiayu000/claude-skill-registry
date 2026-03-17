---
name: api-security
description: Comprehensive API security guidance covering authentication methods, rate limiting, input validation, CORS, security headers, and protection against OWASP API Top 10 vulnerabilities. Use when designing API authentication, implementing rate limiting, configuring CORS, setting security headers, or reviewing API security.
allowed-tools: Read, Glob, Grep, Task
---

# API Security

Comprehensive guidance for securing APIs, covering authentication, authorization, rate limiting, validation, and protection against common API attacks.

## When to Use This Skill

Use this skill when:

- Choosing API authentication methods
- Implementing rate limiting
- Configuring CORS policies
- Setting security headers
- Validating API inputs
- Preventing data exposure
- Protecting against BOLA/IDOR attacks
- Implementing request signing
- Securing API gateways

## OWASP API Security Top 10 (2023)

| Rank | Vulnerability | Description | Mitigation |
|------|--------------|-------------|------------|
| API1 | Broken Object Level Authorization | Access to unauthorized objects | Object-level authorization checks |
| API2 | Broken Authentication | Authentication flaws | Strong authentication, MFA |
| API3 | Broken Object Property Level Authorization | Excessive data exposure, mass assignment | Response filtering, allowlists |
| API4 | Unrestricted Resource Consumption | DoS via resource exhaustion | Rate limiting, pagination |
| API5 | Broken Function Level Authorization | Access to unauthorized functions | Function-level authz checks |
| API6 | Unrestricted Access to Sensitive Business Flows | Abuse of business logic | Rate limiting, fraud detection |
| API7 | Server Side Request Forgery (SSRF) | Server makes malicious requests | URL validation, allowlists |
| API8 | Security Misconfiguration | Improper configuration | Security hardening, automation |
| API9 | Improper Inventory Management | Unknown/unmanaged APIs | API inventory, versioning |
| API10 | Unsafe Consumption of APIs | Trusting third-party APIs | Validate external responses |

## API Authentication Methods

### Method Comparison

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| API Keys | Simple services, internal APIs | Easy to implement | No user context, hard to rotate |
| OAuth 2.0 Bearer Tokens | User-delegated access | Standard, scoped | Token management complexity |
| JWT | Stateless authentication | Self-contained, scalable | Size, revocation challenges |
| mTLS | Service-to-service | Strong identity, encryption | Certificate management |
| HMAC Signatures | Request integrity | Tamper-proof | Implementation complexity |

### API Key Security

```csharp
using System.Security.Cryptography;
using Microsoft.AspNetCore.Http;

/// <summary>
/// API key authentication handler using ASP.NET Core middleware.
/// Uses CryptographicOperations.FixedTimeEquals for timing-safe comparison.
/// </summary>
public sealed class ApiKeyAuthenticationHandler(
    IApiKeyValidator validator,
    ILogger<ApiKeyAuthenticationHandler> logger)
{
    private const string ApiKeyHeader = "X-API-Key";
    private const string ClientIdHeader = "X-Client-ID";

    public async Task<bool> ValidateAsync(HttpContext context, CancellationToken ct = default)
    {
        if (!context.Request.Headers.TryGetValue(ApiKeyHeader, out var apiKeyHeader))
        {
            logger.LogWarning("API key required but not provided");
            return false;
        }

        var apiKey = apiKeyHeader.ToString();
        var clientId = context.Request.Headers[ClientIdHeader].ToString();

        // Hash the provided key
        var providedHash = SHA256.HashData(System.Text.Encoding.UTF8.GetBytes(apiKey));

        // Retrieve stored hash for this client
        var storedHash = await validator.GetKeyHashAsync(clientId, ct);
        if (storedHash is null)
        {
            logger.LogWarning("No stored key found for client {ClientId}", clientId);
            return false;
        }

        // Timing-safe comparison to prevent timing attacks
        if (!CryptographicOperations.FixedTimeEquals(providedHash, storedHash))
        {
            logger.LogWarning("Invalid API key for client {ClientId}", clientId);
            return false;
        }

        return true;
    }
}

public interface IApiKeyValidator
{
    Task<byte[]?> GetKeyHashAsync(string clientId, CancellationToken ct = default);
}

// Best practices for API keys:
// 1. Use sufficiently long, random keys (32+ bytes)
// 2. Transmit only over HTTPS
// 3. Store hashed, not plaintext
// 4. Implement key rotation
// 5. Scope keys to specific operations
// 6. Rate limit per key
```

### Request Signing (HMAC)

```csharp
using System.Security.Cryptography;
using System.Text;

/// <summary>
/// HMAC-SHA256 request signer for API authentication.
/// Generates and verifies request signatures for tamper-proof requests.
/// </summary>
public sealed class RequestSigner
{
    private readonly string _apiKey;
    private readonly byte[] _secretKey;

    public RequestSigner(string apiKey, string secretKey)
    {
        _apiKey = apiKey;
        _secretKey = Encoding.UTF8.GetBytes(secretKey);
    }

    /// <summary>
    /// Generate signature headers for a request.
    /// </summary>
    public Dictionary<string, string> SignRequest(string method, string path, string body = "")
    {
        var timestamp = DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString();
        var stringToSign = $"{method}\n{path}\n{timestamp}\n{body}";

        using var hmac = new HMACSHA256(_secretKey);
        var signature = hmac.ComputeHash(Encoding.UTF8.GetBytes(stringToSign));

        return new Dictionary<string, string>
        {
            ["X-API-Key"] = _apiKey,
            ["X-Timestamp"] = timestamp,
            ["X-Signature"] = Convert.ToBase64String(signature)
        };
    }
}

/// <summary>
/// Verifies HMAC-SHA256 request signatures.
/// </summary>
public sealed class SignatureVerifier(ISecretKeyProvider secretProvider)
{
    private static readonly TimeSpan MaxClockSkew = TimeSpan.FromMinutes(5);

    /// <summary>
    /// Verify request signature with timing-safe comparison.
    /// </summary>
    public async Task<bool> VerifyAsync(
        string apiKey,
        string timestamp,
        string signature,
        string method,
        string path,
        string body = "",
        CancellationToken ct = default)
    {
        // Check timestamp freshness (5-minute window)
        if (!long.TryParse(timestamp, out var requestTime))
            return false;

        var requestDateTime = DateTimeOffset.FromUnixTimeSeconds(requestTime);
        if (Math.Abs((DateTimeOffset.UtcNow - requestDateTime).TotalSeconds) > MaxClockSkew.TotalSeconds)
            return false;

        // Retrieve secret key for this API key
        var secretKey = await secretProvider.GetSecretAsync(apiKey, ct);
        if (secretKey is null)
            return false;

        // Regenerate expected signature
        var stringToSign = $"{method}\n{path}\n{timestamp}\n{body}";
        using var hmac = new HMACSHA256(secretKey);
        var expected = hmac.ComputeHash(Encoding.UTF8.GetBytes(stringToSign));

        // Timing-safe comparison to prevent timing attacks
        var provided = Convert.FromBase64String(signature);
        return CryptographicOperations.FixedTimeEquals(expected, provided);
    }
}

public interface ISecretKeyProvider
{
    Task<byte[]?> GetSecretAsync(string apiKey, CancellationToken ct = default);
}
```

## Rate Limiting

### Rate Limiting Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Fixed Window | Count requests in fixed time windows | Simple, predictable |
| Sliding Window | Rolling window of requests | Smoother limits |
| Token Bucket | Tokens replenish over time | Allow bursts |
| Leaky Bucket | Requests processed at fixed rate | Smooth traffic |

### Implementation (Token Bucket with ASP.NET Core)

```csharp
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.RateLimiting;
using StackExchange.Redis;
using System.Threading.RateLimiting;

/// <summary>
/// Token bucket rate limiting result.
/// </summary>
public sealed record RateLimitResult(
    bool IsAllowed,
    int Remaining,
    long ResetTimeUnix,
    int RetryAfterSeconds = 0);

/// <summary>
/// Token bucket rate limiter using Redis for distributed rate limiting.
/// </summary>
public sealed class TokenBucketRateLimiter(IConnectionMultiplexer redis, int rate, int capacity)
{
    private readonly IDatabase _db = redis.GetDatabase();

    private const string LuaScript = """
        local key = KEYS[1]
        local rate = tonumber(ARGV[1])
        local capacity = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        local bucket = redis.call('HMGET', key, 'tokens', 'last_update')
        local tokens = tonumber(bucket[1]) or capacity
        local last_update = tonumber(bucket[2]) or now

        local elapsed = now - last_update
        tokens = math.min(capacity, tokens + (elapsed * rate))

        local allowed = 0
        if tokens >= 1 then
            tokens = tokens - 1
            allowed = 1
        end

        redis.call('HMSET', key, 'tokens', tokens, 'last_update', now)
        redis.call('EXPIRE', key, math.ceil(capacity / rate) + 1)

        return {allowed, math.floor(tokens), math.ceil((1 - tokens) / rate)}
        """;

    public async Task<RateLimitResult> CheckAsync(string key, CancellationToken ct = default)
    {
        var now = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
        var bucketKey = $"ratelimit:{key}";

        var result = (RedisResult[]?)await _db.ScriptEvaluateAsync(
            LuaScript,
            keys: [bucketKey],
            values: [rate, capacity, now]);

        if (result is null || result.Length < 3)
            return new RateLimitResult(false, 0, now, 60);

        var allowed = (int)result[0] == 1;
        var remaining = (int)result[1];
        var retryAfter = (int)result[2];

        return new RateLimitResult(
            IsAllowed: allowed,
            Remaining: remaining,
            ResetTimeUnix: now + (capacity - remaining) / rate,
            RetryAfterSeconds: allowed ? 0 : retryAfter);
    }
}

/// <summary>
/// ASP.NET Core rate limiting middleware.
/// </summary>
public sealed class RateLimitingMiddleware(RequestDelegate next, TokenBucketRateLimiter limiter)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var identifier = context.Request.Headers["X-API-Key"].FirstOrDefault()
            ?? context.Connection.RemoteIpAddress?.ToString()
            ?? "unknown";

        var result = await limiter.CheckAsync(identifier, context.RequestAborted);

        context.Response.Headers["X-RateLimit-Remaining"] = result.Remaining.ToString();
        context.Response.Headers["X-RateLimit-Reset"] = result.ResetTimeUnix.ToString();

        if (!result.IsAllowed)
        {
            context.Response.Headers["Retry-After"] = result.RetryAfterSeconds.ToString();
            context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
            await context.Response.WriteAsJsonAsync(new { error = "Rate limit exceeded" });
            return;
        }

        await next(context);
    }
}

// Alternatively, use built-in ASP.NET Core Rate Limiting (.NET 7+)
// In Program.cs:
// builder.Services.AddRateLimiter(options =>
// {
//     options.AddTokenBucketLimiter("api", config =>
//     {
//         config.TokenLimit = 100;
//         config.ReplenishmentPeriod = TimeSpan.FromSeconds(1);
//         config.TokensPerPeriod = 10;
//         config.QueueLimit = 0;
//     });
// });
```

## Input Validation

### Schema Validation

```csharp
using System.ComponentModel.DataAnnotations;
using System.Text.RegularExpressions;

/// <summary>
/// Request model with validation - prevents mass assignment via explicit properties.
/// </summary>
public sealed partial class CreateUserRequest : IValidatableObject
{
    [Required]
    [StringLength(30, MinimumLength = 3)]
    [RegularExpression(@"^[a-zA-Z0-9_]+$", ErrorMessage = "Username must be alphanumeric with underscores only")]
    public required string Username { get; init; }

    [Required]
    [EmailAddress]
    public required string Email { get; init; }

    [Required]
    [StringLength(128, MinimumLength = 12)]
    public required string Password { get; init; }

    [RegularExpression(@"^(user|admin|moderator)$")]
    public string Role { get; init; } = "user";

    public IEnumerable<ValidationResult> Validate(ValidationContext validationContext)
    {
        // Password strength validation
        if (!UppercasePattern().IsMatch(Password))
            yield return new ValidationResult("Password must contain uppercase letter", [nameof(Password)]);

        if (!LowercasePattern().IsMatch(Password))
            yield return new ValidationResult("Password must contain lowercase letter", [nameof(Password)]);

        if (!DigitPattern().IsMatch(Password))
            yield return new ValidationResult("Password must contain digit", [nameof(Password)]);

        if (!SpecialCharPattern().IsMatch(Password))
            yield return new ValidationResult("Password must contain special character", [nameof(Password)]);
    }

    [GeneratedRegex(@"[A-Z]")]
    private static partial Regex UppercasePattern();

    [GeneratedRegex(@"[a-z]")]
    private static partial Regex LowercasePattern();

    [GeneratedRegex(@"\d")]
    private static partial Regex DigitPattern();

    [GeneratedRegex(@"[!@#$%^&*(),.?"":{}|<>]")]
    private static partial Regex SpecialCharPattern();
}

// Usage in ASP.NET Core Minimal API
// app.MapPost("/users", async (CreateUserRequest request) =>
// {
//     // Model is auto-validated, extra fields are ignored (only defined properties bound)
//     return Results.Created($"/users/{request.Username}", new { message = "User created", username = request.Username });
// });

// For strict mass assignment prevention, use JsonSerializerOptions:
// builder.Services.ConfigureHttpJsonOptions(options =>
// {
//     options.SerializerOptions.UnmappedMemberHandling = JsonUnmappedMemberHandling.Disallow;
// });
```

### OpenAPI Schema Validation

```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: Secure API
  version: 1.0.0

paths:
  /users:
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        '201':
          description: User created

components:
  schemas:
    CreateUser:
      type: object
      required:
        - username
        - email
        - password
      additionalProperties: false  # Prevent mass assignment
      properties:
        username:
          type: string
          minLength: 3
          maxLength: 30
          pattern: '^[a-zA-Z0-9_]+$'
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 12
          maxLength: 128
        role:
          type: string
          enum: [user, admin, moderator]
          default: user
```

## CORS Configuration

### Secure CORS Setup

```csharp
// In Program.cs - ASP.NET Core CORS configuration

// WRONG: Allow all origins (insecure)
// builder.Services.AddCors(options => options.AddDefaultPolicy(policy => policy.AllowAnyOrigin()));

// CORRECT: Whitelist specific origins
builder.Services.AddCors(options =>
{
    options.AddPolicy("SecurePolicy", policy =>
    {
        policy.WithOrigins(
                "https://app.example.com",
                "https://admin.example.com")
            .WithMethods("GET", "POST", "PUT", "DELETE")
            .WithHeaders("Content-Type", "Authorization", "X-Request-ID")
            .WithExposedHeaders("X-RateLimit-Remaining", "X-Request-ID")
            .AllowCredentials()
            .SetPreflightMaxAge(TimeSpan.FromHours(24));
    });
});

// Apply to specific endpoints
app.MapControllers().RequireCors("SecurePolicy");

// Or apply globally
app.UseCors("SecurePolicy");
```

### CORS Headers Explained

| Header | Purpose | Secure Value |
|--------|---------|--------------|
| Access-Control-Allow-Origin | Allowed origins | Specific domains (not `*`) |
| Access-Control-Allow-Methods | Allowed HTTP methods | Only needed methods |
| Access-Control-Allow-Headers | Allowed request headers | Specific headers |
| Access-Control-Allow-Credentials | Allow cookies/auth | true only with specific origin |
| Access-Control-Max-Age | Preflight cache time | 86400 (24 hours) |
| Access-Control-Expose-Headers | Headers client can read | Custom headers |

### Dynamic CORS with Validation

```csharp
using Microsoft.AspNetCore.Cors.Infrastructure;

/// <summary>
/// Custom CORS policy provider that validates origins dynamically.
/// </summary>
public sealed class DynamicCorsPolicyProvider(IConfiguration configuration) : ICorsPolicyProvider
{
    private static readonly FrozenSet<string> AllowedOrigins = new HashSet<string>
    {
        "https://app.example.com",
        "https://admin.example.com",
        "https://staging.example.com",
    }.ToFrozenSet();

    public Task<CorsPolicy?> GetPolicyAsync(HttpContext context, string? policyName)
    {
        var origin = context.Request.Headers.Origin.ToString();

        // Load additional origins from config (optional)
        var configuredOrigins = configuration.GetSection("Cors:AllowedOrigins")
            .Get<string[]>() ?? [];

        var allAllowed = AllowedOrigins.Union(configuredOrigins).ToHashSet();

        if (string.IsNullOrEmpty(origin) || !allAllowed.Contains(origin))
        {
            return Task.FromResult<CorsPolicy?>(null);  // No CORS headers
        }

        var policy = new CorsPolicyBuilder()
            .WithOrigins(origin)
            .WithMethods("GET", "POST", "PUT", "DELETE")
            .WithHeaders("Content-Type", "Authorization", "X-Request-ID")
            .AllowCredentials()
            .Build();

        return Task.FromResult<CorsPolicy?>(policy);
    }
}

// Registration in Program.cs:
// builder.Services.AddSingleton<ICorsPolicyProvider, DynamicCorsPolicyProvider>();
// builder.Services.AddCors();
// app.UseCors();
```

## Security Headers

### Essential Security Headers

```csharp
using Microsoft.AspNetCore.Http;

/// <summary>
/// Middleware that adds security headers to all responses.
/// </summary>
public sealed class SecurityHeadersMiddleware(RequestDelegate next)
{
    public async Task InvokeAsync(HttpContext context)
    {
        // Add security headers before response is sent
        context.Response.OnStarting(() =>
        {
            var headers = context.Response.Headers;

            // Prevent MIME type sniffing
            headers["X-Content-Type-Options"] = "nosniff";

            // Clickjacking protection
            headers["X-Frame-Options"] = "DENY";

            // XSS filter (legacy browsers)
            headers["X-XSS-Protection"] = "1; mode=block";

            // Strict Transport Security
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload";

            // Content Security Policy (for API responses)
            headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'";

            // Referrer Policy
            headers["Referrer-Policy"] = "strict-origin-when-cross-origin";

            // Permissions Policy
            headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()";

            // Cache control for authenticated requests
            if (context.Request.Headers.ContainsKey("Authorization"))
            {
                headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private";
                headers["Pragma"] = "no-cache";
            }

            return Task.CompletedTask;
        });

        await next(context);
    }
}

// Extension method for cleaner registration
public static class SecurityHeadersExtensions
{
    public static IApplicationBuilder UseSecurityHeaders(this IApplicationBuilder app)
        => app.UseMiddleware<SecurityHeadersMiddleware>();
}

// Usage in Program.cs:
// app.UseSecurityHeaders();
```

### Header Configuration by Response Type

| Header | API Response | Error Response | File Download |
|--------|--------------|----------------|---------------|
| Content-Type | application/json | application/json | Specific MIME |
| X-Content-Type-Options | nosniff | nosniff | nosniff |
| Cache-Control | no-store (sensitive) | no-store | varies |
| Content-Disposition | - | - | attachment |

## Protecting Against BOLA/IDOR

### Object-Level Authorization

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;

/// <summary>
/// Authorization filter for object-level access control (BOLA/IDOR protection).
/// </summary>
[AttributeUsage(AttributeTargets.Method | AttributeTargets.Class)]
public sealed class AuthorizeResourceAttribute(string resourceType, string paramName = "id")
    : Attribute, IAsyncAuthorizationFilter
{
    public async Task OnAuthorizationAsync(AuthorizationFilterContext context)
    {
        var userId = context.HttpContext.User.FindFirst("sub")?.Value;
        if (userId is null)
        {
            context.Result = new UnauthorizedResult();
            return;
        }

        // Get resource ID from route data
        if (!context.RouteData.Values.TryGetValue(paramName, out var resourceIdObj)
            || resourceIdObj is not string resourceId)
        {
            context.Result = new BadRequestObjectResult(new { error = "Resource ID required" });
            return;
        }

        // Resolve authorization service from DI
        var authService = context.HttpContext.RequestServices
            .GetRequiredService<IResourceAuthorizationService>();

        if (!await authService.CanAccessAsync(userId, resourceType, resourceId))
        {
            context.Result = new ForbidResult();
        }
    }
}

/// <summary>
/// Service for checking resource-level access.
/// </summary>
public interface IResourceAuthorizationService
{
    Task<bool> CanAccessAsync(string userId, string resourceType, string resourceId);
}

public sealed class ResourceAuthorizationService(ApplicationDbContext db) : IResourceAuthorizationService
{
    public async Task<bool> CanAccessAsync(string userId, string resourceType, string resourceId)
    {
        return resourceType switch
        {
            "document" => await db.Documents.AnyAsync(d =>
                d.Id == resourceId &&
                (d.OwnerId == userId || d.SharedWithUsers.Any(u => u.Id == userId))),

            "account" => await db.Accounts.AnyAsync(a =>
                a.Id == resourceId && a.UserId == userId),

            _ => false
        };
    }
}

// Usage in controller
[ApiController]
[Route("api/documents")]
public sealed class DocumentsController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet("{id}")]
    [Authorize]
    [AuthorizeResource("document", "id")]
    public async Task<IActionResult> GetDocument(string id)
    {
        // If we reach here, user is authorized
        var document = await db.Documents.FindAsync(id);
        return Ok(document);
    }
}
```

### Preventing Enumeration

```csharp
using System.ComponentModel.DataAnnotations;

// Option 1: Use UUIDs (Recommended)
// EF Core entity with GUID as primary key
public sealed class Document
{
    [Key]
    public Guid Id { get; init; } = Guid.NewGuid();

    public required string Title { get; set; }
    public required string OwnerId { get; init; }
}

// Option 2: Hashids for obfuscating sequential IDs
// NuGet: HashidsNet
using HashidsNet;

/// <summary>
/// ID obfuscation service to prevent enumeration attacks.
/// </summary>
public sealed class IdObfuscator
{
    private readonly Hashids _hashids;

    public IdObfuscator(IConfiguration config)
    {
        var salt = config["Security:HashidsSalt"]
            ?? throw new InvalidOperationException("HashidsSalt not configured");
        _hashids = new Hashids(salt, minHashLength: 8);
    }

    public string Encode(int id) => _hashids.Encode(id);
    public string Encode(long id) => _hashids.EncodeLong(id);

    public int? DecodeInt(string hash)
    {
        var result = _hashids.Decode(hash);
        return result.Length > 0 ? result[0] : null;
    }

    public long? DecodeLong(string hash)
    {
        var result = _hashids.DecodeLong(hash);
        return result.Length > 0 ? result[0] : null;
    }
}

// Usage in controller
[ApiController]
[Route("api/documents")]
public sealed class DocumentsController(
    ApplicationDbContext db,
    IdObfuscator idObfuscator) : ControllerBase
{
    [HttpGet("{hashId}")]
    public async Task<IActionResult> GetDocument(string hashId)
    {
        var docId = idObfuscator.DecodeInt(hashId);
        if (docId is null)
            return BadRequest(new { error = "Invalid ID" });

        var document = await db.Documents.FindAsync(docId.Value);
        if (document is null)
            return NotFound();

        // ... authorization check
        return Ok(document);
    }
}

// Registration in Program.cs:
// builder.Services.AddSingleton<IdObfuscator>();
```

## Preventing Data Exposure

### Response Filtering

```csharp
using System.Text.Json.Serialization;

// Full entity (internal - stored in database)
public sealed class UserEntity
{
    public required string Id { get; init; }
    public required string Email { get; set; }
    public required string PasswordHash { get; set; }  // Never expose!
    public required string Role { get; set; }
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
    public DateTime LastLogin { get; set; }
    public int FailedLoginAttempts { get; set; }
    public string? InternalNotes { get; set; }
}

// Public response DTO (limited fields)
public sealed record UserResponse(
    string Id,
    string Email,
    string Role,
    DateTime CreatedAt);

// Admin response DTO (extended fields)
public sealed record UserAdminResponse(
    string Id,
    string Email,
    string Role,
    DateTime CreatedAt,
    DateTime LastLogin,
    int FailedLoginAttempts) : UserResponse(Id, Email, Role, CreatedAt);

// Mapper extensions
public static class UserMapper
{
    public static UserResponse ToPublicResponse(this UserEntity user) =>
        new(user.Id, user.Email, user.Role, user.CreatedAt);

    public static UserAdminResponse ToAdminResponse(this UserEntity user) =>
        new(user.Id, user.Email, user.Role, user.CreatedAt, user.LastLogin, user.FailedLoginAttempts);
}

// Controller with role-based response filtering
[ApiController]
[Route("api/users")]
[Authorize]
public sealed class UsersController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet("{userId}")]
    public async Task<IActionResult> GetUser(string userId)
    {
        var user = await db.Users.FindAsync(userId);
        if (user is null)
            return NotFound();

        // Return different views based on role
        var isAdmin = User.IsInRole("admin");
        return Ok(isAdmin ? user.ToAdminResponse() : user.ToPublicResponse());
    }
}

// Alternatively, use JsonIgnore for simple cases (not recommended for complex scenarios)
// public sealed class UserDto
// {
//     [JsonIgnore]
//     public string PasswordHash { get; init; } = null!;  // Never serialized
// }
```

### GraphQL Security

```csharp
// Using Hot Chocolate GraphQL server (NuGet: HotChocolate.AspNetCore)
using HotChocolate;
using HotChocolate.Authorization;
using HotChocolate.Data;
using HotChocolate.Resolvers;

// GraphQL type with field-level authorization
public sealed class UserType
{
    public string Id { get; init; } = null!;

    // Field resolver with conditional masking
    public string? GetEmail([Service] IHttpContextAccessor httpContext)
    {
        var currentUserId = httpContext.HttpContext?.User.FindFirst("sub")?.Value;
        var isAdmin = httpContext.HttpContext?.User.IsInRole("admin") ?? false;

        // Only show email if viewing own profile or is admin
        if (currentUserId == Id || isAdmin)
            return Email;

        return null;  // Mask for other users
    }

    // Don't expose: PasswordHash, InternalNotes, etc.
    // Simply don't include them in the GraphQL type

    [GraphQLIgnore]
    public string Email { get; init; } = null!;
}

// Query with pagination limits and authorization
public sealed class Query
{
    [UseDbContext(typeof(ApplicationDbContext))]
    [UsePaging(MaxPageSize = 100, DefaultPageSize = 25)]  // Limit results
    [UseFiltering]
    [UseSorting]
    [Authorize]  // Require authentication
    public IQueryable<UserType> GetUsers([ScopedService] ApplicationDbContext db)
        => db.Users.Select(u => new UserType { Id = u.Id, Email = u.Email });

    [UseDbContext(typeof(ApplicationDbContext))]
    [Authorize]
    public async Task<UserType?> GetUser(
        [ScopedService] ApplicationDbContext db,
        string id)
    {
        var user = await db.Users.FindAsync(id);
        return user is null ? null : new UserType { Id = user.Id, Email = user.Email };
    }
}

// Registration in Program.cs:
// builder.Services
//     .AddGraphQLServer()
//     .AddQueryType<Query>()
//     .AddAuthorization()
//     .AddFiltering()
//     .AddSorting()
//     .AddProjections()
//     .SetPagingOptions(new PagingOptions { MaxPageSize = 100, DefaultPageSize = 25 });
```

## Quick Decision Tree

**What API security concern do you have?**

1. **Choosing authentication method** → See Authentication Methods table
2. **Implementing rate limiting** → Token bucket with Redis (most flexible)
3. **Configuring CORS** → Whitelist specific origins, never use `*`
4. **Setting security headers** → Apply all essential headers
5. **Validating input** → Use DataAnnotations/FluentValidation with strict binding
6. **Preventing BOLA** → Object-level authorization on every endpoint
7. **Preventing data exposure** → Response filtering with typed models

## Security Checklist

### Authentication

- [ ] Strong authentication for all endpoints
- [ ] API keys stored hashed, not plaintext
- [ ] Request signing for sensitive operations
- [ ] Token expiration and rotation

### Authorization

- [ ] Object-level authorization checks
- [ ] Function-level authorization checks
- [ ] No sequential IDs (use UUIDs or hashing)
- [ ] Response filtering based on permissions

### Rate Limiting

- [ ] Rate limiting on all endpoints
- [ ] Per-client rate limits
- [ ] Appropriate limits for each endpoint type
- [ ] Retry-After header on 429 responses

### Input Validation

- [ ] Schema validation on all inputs
- [ ] Reject extra fields (mass assignment protection)
- [ ] File upload validation (size, type, content)
- [ ] SQL injection prevention (parameterized queries)

### Headers and CORS

- [ ] CORS whitelist (no wildcard)
- [ ] Security headers on all responses
- [ ] HTTPS enforced (HSTS)
- [ ] Cache control for sensitive data

## References

- [Rate Limiting Patterns](references/rate-limiting.md) - Advanced rate limiting strategies
- [API Headers Reference](references/api-headers.md) - Complete header configuration

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `authentication-patterns` | JWT, OAuth implementation details |
| `authorization-models` | RBAC, ABAC for API authorization |
| `secure-coding` | Input validation, injection prevention |

## Version History

- v1.0.0 (2025-12-26): Initial release with OWASP API Top 10, authentication, rate limiting, CORS, headers

---

**Last Updated:** 2025-12-26
