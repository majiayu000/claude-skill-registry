---
name: dotnet-api-auth
description: Authentication and authorization patterns for ASP.NET Core Web APIs
---

# .NET API Authentication Skill

Patterns and implementations for securing ASP.NET Core Web APIs with authentication and authorization.

## JWT Bearer Authentication

Configure JWT Bearer authentication in `Program.cs`:

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]!))
        };
    });

// Add after building the app
app.UseAuthentication();
app.UseAuthorization();
```

Required `appsettings.json` configuration:

```json
{
  "Jwt": {
    "Key": "your-256-bit-secret-key-here-min-32-chars",
    "Issuer": "https://yourdomain.com",
    "Audience": "https://yourdomain.com"
  }
}
```

## API Key Authentication

Custom middleware for API key validation:

```csharp
public class ApiKeyMiddleware
{
    private const string ApiKeyHeaderName = "X-API-Key";
    private readonly RequestDelegate _next;

    public ApiKeyMiddleware(RequestDelegate next) => _next = next;

    public async Task InvokeAsync(HttpContext context, IConfiguration config)
    {
        if (!context.Request.Headers.TryGetValue(ApiKeyHeaderName, out var extractedApiKey))
        {
            context.Response.StatusCode = 401;
            await context.Response.WriteAsync("API Key is missing");
            return;
        }

        var apiKey = config["ApiKey"];
        if (!apiKey.Equals(extractedApiKey))
        {
            context.Response.StatusCode = 401;
            await context.Response.WriteAsync("Invalid API Key");
            return;
        }

        await _next(context);
    }
}

// Register in Program.cs
app.UseMiddleware<ApiKeyMiddleware>();
```

## Policy-Based Authorization

Define and register authorization policies:

```csharp
builder.Services.AddAuthorizationBuilder()
    .AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"))
    .AddPolicy("PremiumUser", policy => policy.RequireClaim("Subscription", "Premium"))
    .AddPolicy("MinimumAge", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(18)));

// Register custom handlers
builder.Services.AddSingleton<IAuthorizationHandler, MinimumAgeHandler>();
```

Apply policies to endpoints:

```csharp
[Authorize(Policy = "AdminOnly")]
[HttpDelete("{id}")]
public IActionResult Delete(int id) { /* ... */ }

// Or with minimal APIs
app.MapDelete("/admin/users/{id}", () => Results.Ok())
    .RequireAuthorization("AdminOnly");
```

## Claims and Roles

Access claims in controllers:

```csharp
[Authorize]
[HttpGet("profile")]
public IActionResult GetProfile()
{
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    var email = User.FindFirst(ClaimTypes.Email)?.Value;
    var roles = User.FindAll(ClaimTypes.Role).Select(c => c.Value);

    return Ok(new { userId, email, roles });
}

// Check roles
if (User.IsInRole("Admin"))
{
    // Admin-specific logic
}
```

Generate tokens with claims:

```csharp
public string GenerateToken(User user)
{
    var claims = new List<Claim>
    {
        new(ClaimTypes.NameIdentifier, user.Id.ToString()),
        new(ClaimTypes.Email, user.Email),
        new(ClaimTypes.Role, user.Role),
        new("CustomClaim", "CustomValue")
    };

    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_config["Jwt:Key"]!));
    var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

    var token = new JwtSecurityToken(
        issuer: _config["Jwt:Issuer"],
        audience: _config["Jwt:Audience"],
        claims: claims,
        expires: DateTime.UtcNow.AddHours(1),
        signingCredentials: credentials);

    return new JwtSecurityTokenHandler().WriteToken(token);
}
```

## Resource-Based Authorization

Authorize access to specific resources:

```csharp
public class DocumentAuthorizationHandler :
    AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document resource)
    {
        var userId = context.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

        if (requirement.Name == Operations.Read.Name && resource.OwnerId == userId)
        {
            context.Succeed(requirement);
        }

        if (requirement.Name == Operations.Update.Name &&
            (resource.OwnerId == userId || context.User.IsInRole("Admin")))
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}
```

Use in a controller:

```csharp
public class DocumentsController : ControllerBase
{
    private readonly IAuthorizationService _authService;

    [HttpGet("{id}")]
    public async Task<IActionResult> Get(int id)
    {
        var document = await _repository.GetAsync(id);
        var result = await _authService.AuthorizeAsync(User, document, Operations.Read);

        if (!result.Succeeded)
            return Forbid();

        return Ok(document);
    }
}
```

## CORS Configuration

Configure CORS for API access:

```csharp
builder.Services.AddCors(options =>
{
    // Named policy for specific origins
    options.AddPolicy("AllowSpecificOrigin", policy =>
    {
        policy.WithOrigins("https://example.com", "https://app.example.com")
              .AllowAnyMethod()
              .AllowAnyHeader()
              .AllowCredentials();
    });

    // Development policy (more permissive)
    options.AddPolicy("Development", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

// Apply globally
app.UseCors("AllowSpecificOrigin");

// Or per-endpoint
app.MapGet("/api/public", () => "Hello")
    .RequireCors("AllowSpecificOrigin");
```

## Quick Reference

| Pattern | Use Case | Key Components |
|---------|----------|----------------|
| JWT Bearer | Token-based auth | `AddJwtBearer`, `TokenValidationParameters` |
| API Key | Simple service auth | Custom middleware, header validation |
| Policy-Based | Role/claim requirements | `AddPolicy`, `[Authorize(Policy)]` |
| Resource-Based | Per-resource permissions | `IAuthorizationService`, custom handlers |
| CORS | Cross-origin requests | `AddCors`, `UseCors` |

## Additional Resources

- See `examples/jwt-setup-example.cs` for complete JWT configuration
- See `examples/policy-auth-example.cs` for custom authorization requirements
