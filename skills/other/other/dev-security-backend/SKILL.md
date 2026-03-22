---
version: 1.2.0
name: dev-security-backend
description: >
  Security checklist for C#/.NET backend (ASP.NET Core, EF Core, Event Sourcing).
  Covers secrets management, input validation, SQL injection, authentication,
  authorization, rate limiting, security headers, sensitive data handling,
  Problem Details (RFC 7807), and event sourcing security.
  Invoked via /dev-security (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
context: fork
argument-hint: "[--checklist | --scan | --full]"
---

# Security Review — Backend (.NET)

Security checklist for ASP.NET Core and EF Core backend code.

> **Reference:** [OWASP Top 10:2025](https://owasp.org/Top10/2025/)

## When to Activate

- Implementing authentication or authorization
- Handling user input or file uploads
- Creating new API endpoints
- Working with secrets or credentials
- Before deploying to production
- Integrating third-party APIs

## 1. Secrets Management

### Never do this
```csharp
var connectionString = "Server=prod-db;Password=secret123";
var apiKey = "sk-proj-xxxxx";
```

### Always do this
```csharp
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
var apiKey = builder.Configuration["ExternalApi:Key"];

// Verify at startup
if (string.IsNullOrEmpty(apiKey))
    throw new InvalidOperationException("ExternalApi:Key not configured");
```

### Azure Key Vault (Production)
```csharp
// Azure Key Vault integration
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{vaultName}.vault.azure.net/"),
    new DefaultAzureCredential());
```

**Checklist:**
- [ ] No hardcoded connection strings, API keys, or passwords
- [ ] Secrets in User Secrets (dev), Azure Key Vault / env vars (prod)
- [ ] Azure Key Vault configured for production deployments
- [ ] `appsettings.Development.json` in `.gitignore`
- [ ] No secrets in git history (`git log -p -S "password"`)

## 2. Input Validation

### Result-Based Validation (Results)
```csharp
public static Result<CreateOrderRequest> ValidateOrder(CreateOrderRequest request)
{
    return ValidationBuilder.Create()
        .ValidateNotNullOrWhiteSpace(request.Items?.FirstOrDefault()?.Sku, "Items[0].Sku")
        .ValidateRange(request.Items?.Count ?? 0, 1, int.MaxValue, "Items.Count")
        .Build()
        .Bind(_ => ValidateItems(request));
}

private static Result<CreateOrderRequest> ValidateItems(CreateOrderRequest request)
{
    var results = request.Items.Select(item =>
        ValidationBuilder.Create()
            .ValidateNotNullOrWhiteSpace(item.Sku, nameof(item.Sku))
            .ValidateRange(item.Quantity, 1, 1000, nameof(item.Quantity))
            .ValidateRange(item.Price, 0.01m, decimal.MaxValue, nameof(item.Price))
            .Build());

    return ResultCombinators.Combine(results).Map(_ => request);
}

// In endpoint — converts Result to TypedResults automatically
app.MapPost("/api/orders", (CreateOrderRequest request) =>
    ValidateOrder(request)
        .Bind(r => orderService.CreateAsync(r))
        .ToCreatedHttpResult(o => $"/api/orders/{o.Id}"));
```
```

### File Upload Validation
```csharp
[HttpPost("upload")]
public async Task<IActionResult> Upload(IFormFile file)
{
    if (file.Length > 5 * 1024 * 1024)
        return BadRequest("File too large (max 5MB)");

    var allowedTypes = new[] { "image/jpeg", "image/png", "application/pdf" };
    if (!allowedTypes.Contains(file.ContentType))
        return BadRequest("Invalid file type");

    var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
    if (!new[] { ".jpg", ".jpeg", ".png", ".pdf" }.Contains(ext))
        return BadRequest("Invalid extension");

    // Use a generated filename, never the user-provided one
    var safeName = $"{Guid.NewGuid()}{ext}";
    // ...
}
```

**Checklist:**
- [ ] All API inputs validated with Result-based validation (Results) or DataAnnotations
- [ ] File uploads restricted (size, type, extension)
- [ ] Never trust client-side validation alone — always validate server-side
- [ ] Error messages don't leak internal details

## 3. SQL Injection Prevention

> **Note:** If using Event Sourcing (e.g., EventSourcing with Azure Blob Storage),
> SQL injection is not applicable. Focus on blob key validation and event stream access control instead.

### Never do this
```csharp
var sql = $"SELECT * FROM Users WHERE Email = '{email}'";
await context.Database.ExecuteSqlRawAsync(sql);
```

### Always do this
```csharp
// EF Core — parameterized automatically
var user = await context.Users.FirstOrDefaultAsync(u => u.Email == email);

// If raw SQL is needed — parameterized
await context.Database.ExecuteSqlInterpolatedAsync(
    $"SELECT * FROM Users WHERE Email = {email}");

// Or explicit parameters
await context.Database.ExecuteSqlRawAsync(
    "SELECT * FROM Users WHERE Email = @p0", email);
```

**Checklist:**
- [ ] All queries use EF Core LINQ or parameterized SQL
- [ ] No string concatenation in any SQL
- [ ] `ExecuteSqlInterpolatedAsync` over `ExecuteSqlRawAsync`
- [ ] For Event Sourcing: blob keys validated and sanitized
- [ ] For Event Sourcing: event stream access scoped per tenant/user

## 4. Authentication & Authorization

```csharp
// Enforce auth on endpoints
app.MapGet("/api/orders", GetOrders).RequireAuthorization();

// Role-based
app.MapDelete("/api/orders/{id}", DeleteOrder).RequireAuthorization("AdminOnly");

// Policy-based authorization
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("AdminOnly", p => p.RequireRole("Admin"))
    .AddPolicy("CanManageOrders", p => p.RequireClaim("permission", "orders:manage"));
```

### Cookie Configuration
```csharp
builder.Services.AddAuthentication().AddCookie(options =>
{
    options.Cookie.HttpOnly = true;
    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
    options.Cookie.SameSite = SameSiteMode.Strict;
    options.ExpireTimeSpan = TimeSpan.FromHours(1);
    options.SlidingExpiration = true;
});
```

**Checklist:**
- [ ] All endpoints require authentication (opt-out, not opt-in)
- [ ] Authorization checks before sensitive operations
- [ ] Tokens in HttpOnly cookies (not exposed to JavaScript)
- [ ] Cookie: HttpOnly, Secure, SameSite=Strict

## 5. Security Headers

```csharp
app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    context.Response.Headers.Append("X-XSS-Protection", "0"); // Use CSP instead
    context.Response.Headers.Append("Content-Security-Policy",
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'");
    await next();
});
```

**Checklist:**
- [ ] CSP headers configured
- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY`
- [ ] HTTPS enforced (`UseHttpsRedirection()`)

## 6. CSRF Protection

```csharp
// Enabled by default for Razor Pages and MVC
// For minimal APIs with cookie auth:
builder.Services.AddAntiforgery();
app.UseAntiforgery();
```

**Checklist:**
- [ ] Anti-forgery tokens on state-changing operations
- [ ] SameSite=Strict on all cookies

## 7. Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("api", opt =>
    {
        opt.PermitLimit = 100;
        opt.Window = TimeSpan.FromMinutes(1);
    });

    options.AddFixedWindowLimiter("expensive", opt =>
    {
        opt.PermitLimit = 10;
        opt.Window = TimeSpan.FromMinutes(1);
    });
});

app.UseRateLimiter();
app.MapGet("/api/search", Search).RequireRateLimiting("expensive");
```

**Checklist:**
- [ ] Rate limiting on all API endpoints
- [ ] Stricter limits on expensive operations (search, AI calls, file uploads)
- [ ] `429 Too Many Requests` response with `Retry-After` header

## 8. Sensitive Data

```csharp
// WRONG: logging secrets
_logger.LogInformation("User login: {Email} {Password}", email, password);

// CORRECT: redact sensitive fields
_logger.LogInformation("User login: {Email}", email);

// WRONG: exposing internals
catch (Exception ex)
{
    return Problem(detail: ex.ToString()); // Stack trace to client!
}

// CORRECT: generic error
catch (Exception ex)
{
    _logger.LogError(ex, "Order creation failed");
    return Problem("An error occurred. Please try again.");
}
```

**Checklist:**
- [ ] No passwords, tokens, or connection strings in logs
- [ ] Error messages generic for clients, detailed in server logs only
- [ ] No stack traces exposed to users
- [ ] PII handled per GDPR/compliance requirements

## 9. Problem Details (RFC 7807)

```csharp
// Configure Problem Details
builder.Services.AddProblemDetails(options =>
{
    options.CustomizeProblemDetails = context =>
    {
        context.ProblemDetails.Extensions["traceId"] =
            Activity.Current?.Id ?? context.HttpContext.TraceIdentifier;
    };
});

// Custom exception handler
public class DomainExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext context, Exception exception, CancellationToken ct)
    {
        var (statusCode, title) = exception switch
        {
            ArgumentException => (400, "Bad Request"),
            KeyNotFoundException => (404, "Not Found"),
            InvalidOperationException => (409, "Conflict"),
            UnauthorizedAccessException => (403, "Forbidden"),
            _ => (500, "Internal Server Error")
        };

        context.Response.StatusCode = statusCode;
        await context.Response.WriteAsJsonAsync(new ProblemDetails
        {
            Status = statusCode,
            Title = title,
            Detail = exception is not InvalidOperationException ? null : exception.Message
        }, ct);
        return true;
    }
}
```

**Checklist:**
- [ ] `AddProblemDetails()` configured with trace ID extension
- [ ] `IExceptionHandler` implemented for domain exceptions
- [ ] Error responses use `application/problem+json` content type
- [ ] No internal details leaked in Problem Details responses

## 10. Event Sourcing Security

When using Event Sourcing (e.g., EventSourcing with Azure Blob Storage), additional security considerations apply.

### Event Stream Isolation
- Event streams must be scoped per tenant/user — never allow cross-read between tenants
- Validate stream IDs to prevent path traversal in blob storage keys
- Use container-level access policies to enforce tenant boundaries

### Projection Security
- Projection rebuilds should require admin authorization
- Log all projection rebuild requests with actor identity and timestamp
- Consider read-only replicas for projections to limit blast radius

### PII in Events
- Events are immutable — plan for GDPR before storing PII
- Use crypto-shredding: encrypt PII fields per user, delete the key on erasure request
- Mark events containing PII with metadata for auditing
- Consider separating PII into a linked, deletable store

**Checklist:**
- [ ] Event streams scoped per tenant/user
- [ ] Blob storage keys validated and sanitized (no path traversal)
- [ ] Projection rebuilds require admin authorization
- [ ] PII handling strategy documented (crypto-shredding or separation)
- [ ] Event metadata tracks PII presence for GDPR compliance

## 11. Supply Chain Security (OWASP A03:2025)

Software supply chain attacks target NuGet packages, build pipelines, and transitive dependencies.

**Checklist:**
- [ ] `dotnet list package --vulnerable` and `--deprecated` clean
- [ ] Package sources restricted to trusted feeds (nuget.org, private feed)
- [ ] Lock file (`packages.lock.json`) committed when using `RestorePackagesWithLockFile`
- [ ] No wildcard version ranges in `.csproj` (pin exact or minor range)
- [ ] CI/CD pipeline dependencies pinned (no `latest` tags for tools/images)
- [ ] Review transitive dependencies for known-compromised packages

## 12. Exceptional Condition Handling (OWASP A10:2025)

Mishandled errors, edge cases, and unexpected states can expose data or cause cascading failures.

**Checklist:**
- [ ] All async methods have proper `try/catch` — no unhandled task exceptions
- [ ] Global exception handler (`IExceptionHandler`) catches everything
- [ ] Empty catch blocks either log or have explicit justification
- [ ] Null/empty collection edge cases handled (no `FirstOrDefault()` without null check)
- [ ] Cancellation tokens propagated through async chains
- [ ] Timeout policies configured for external calls (Polly, `HttpClient.Timeout`)
- [ ] Circuit breaker patterns for downstream service failures

## Pre-Deployment Checklist

### OWASP Top 10:2025 Coverage
- [ ] **A01 Broken Access Control**: All endpoints require auth, role/policy checks on sensitive ops
- [ ] **A02 Security Misconfiguration**: Security headers set, HTTPS enforced, debug disabled in prod
- [ ] **A03 Supply Chain**: Dependencies audited, lock files committed, no vulnerable packages
- [ ] **A04 Cryptographic Failures**: Secrets in Key Vault, no hardcoded credentials, TLS enforced
- [ ] **A05 Injection**: All queries parameterized, no string concatenation in SQL/commands
- [ ] **A06 Insecure Design**: Rate limiting on all endpoints, stricter on expensive operations
- [ ] **A07 Authentication Failures**: HttpOnly cookies, SameSite=Strict, session timeout configured
- [ ] **A08 Integrity Failures**: Anti-forgery tokens, CI/CD pipeline integrity
- [ ] **A09 Logging & Alerting**: No secrets in logs, structured logging with alerts on auth failures
- [ ] **A10 Exceptional Conditions**: Global error handler, no unhandled exceptions, Problem Details (RFC 7807)

### Stack-Specific
- [ ] **Event Sourcing**: Stream isolation, projection auth, PII strategy (if applicable)
- [ ] **Dependencies**: `dotnet list package --vulnerable` clean

## Flags

| Flag | Behavior |
|------|----------|
| `--checklist` | Print the pre-deployment checklist only |
| `--scan` | Run automated scans (secret grep, `dotnet list package --vulnerable`, Aspire runtime errors) |
| `--full` | Full review: checklist + scans + runtime checks + code review of changed files |

## Aspire Runtime Security Checks (--scan / --full)

If the Aspire AppHost is running, the `--scan` and `--full` flags include runtime security checks:

**Step 1 — Check for leaked error details:**
```
mcp__aspire__list_structured_logs  resourceName: "api"
```
Scan for responses that leak stack traces, internal paths, or sensitive data in error messages. Production APIs should return Problem Details (RFC 7807) without internal details.

**Step 2 — Check for auth failures in logs:**
Filter structured logs for `401`/`403` responses. A high volume may indicate misconfigured auth, missing policies, or endpoints that should require auth but don't.

**Step 3 — Check console for security warnings:**
```
mcp__aspire__list_console_logs  resourceName: "api"
```
Look for:
- CORS policy warnings
- Certificate validation failures
- Auth middleware errors
- Rate limiting rejections (confirm they're working)

Skip if Aspire is not running.
