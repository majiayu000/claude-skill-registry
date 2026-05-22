---
description: Set up JWT Bearer authentication with token service and authorization policies
---
# Configure JWT Authentication Skill

Set up JWT Bearer authentication for NovaTune API.

## Project Context

- Configuration: `src/NovaTuneApp/NovaTuneApp.ApiService/appsettings.json`
- Auth setup: `src/NovaTuneApp/NovaTuneApp.ApiService/Program.cs`
- Token service: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/TokenService.cs`

## Steps

### 1. Add Configuration Section

Location: `appsettings.json`

```json
{
  "Jwt": {
    "Issuer": "https://novatune.example",
    "Audience": "novatune-api",
    "AccessTokenExpirationMinutes": 15,
    "RefreshTokenExpirationMinutes": 60,
    "SigningAlgorithm": "HS256"
  }
}
```

> Note: SigningKey should be in environment variable `JWT_SIGNING_KEY` or secrets manager.

### 2. Create JWT Configuration Class

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Configuration/JwtSettings.cs`

```csharp
public class JwtSettings
{
    public const string SectionName = "Jwt";

    public required string Issuer { get; set; }
    public required string Audience { get; set; }
    public int AccessTokenExpirationMinutes { get; set; } = 15;
    public int RefreshTokenExpirationMinutes { get; set; } = 60;
    public string SigningAlgorithm { get; set; } = "HS256";
}
```

### 3. Create Token Service

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/TokenService.cs`

```csharp
public interface ITokenService
{
    string GenerateAccessToken(ApplicationUser user);
    string GenerateRefreshToken();
    ClaimsPrincipal? ValidateToken(string token);
}

public class TokenService : ITokenService
{
    private readonly JwtSettings _settings;
    private readonly byte[] _signingKey;

    public TokenService(IOptions<JwtSettings> settings, IConfiguration config)
    {
        _settings = settings.Value;
        _signingKey = Encoding.UTF8.GetBytes(
            config["JWT_SIGNING_KEY"]
            ?? throw new InvalidOperationException("JWT_SIGNING_KEY not configured"));
    }

    public string GenerateAccessToken(ApplicationUser user)
    {
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, user.UserId),
            new(JwtRegisteredClaimNames.Email, user.Email),
            new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new("status", user.Status.ToString())
        };

        // Add role claims
        foreach (var role in user.Roles)
        {
            claims.Add(new Claim("roles", role.ToLowerInvariant()));
        }

        var key = new SymmetricSecurityKey(_signingKey);
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: _settings.Issuer,
            audience: _settings.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_settings.AccessTokenExpirationMinutes),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    public string GenerateRefreshToken()
    {
        var randomBytes = new byte[32];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomBytes);
        return Convert.ToBase64String(randomBytes);
    }

    public ClaimsPrincipal? ValidateToken(string token)
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = new SymmetricSecurityKey(_signingKey);

        try
        {
            var principal = tokenHandler.ValidateToken(token, new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidIssuer = _settings.Issuer,
                ValidateAudience = true,
                ValidAudience = _settings.Audience,
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = key,
                ValidateLifetime = true,
                ClockSkew = TimeSpan.Zero
            }, out _);

            return principal;
        }
        catch
        {
            return null;
        }
    }
}
```

### 4. Configure Authentication in Program.cs

```csharp
// Bind settings
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection(JwtSettings.SectionName));

// Register token service
builder.Services.AddSingleton<ITokenService, TokenService>();

// Configure JWT authentication
var jwtSettings = builder.Configuration
    .GetSection(JwtSettings.SectionName)
    .Get<JwtSettings>()!;

var signingKey = Encoding.UTF8.GetBytes(
    builder.Configuration["JWT_SIGNING_KEY"]
    ?? throw new InvalidOperationException("JWT_SIGNING_KEY not configured"));

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = jwtSettings.Issuer,
            ValidateAudience = true,
            ValidAudience = jwtSettings.Audience,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(signingKey),
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });

builder.Services.AddAuthorization();

// After app.Build()
app.UseAuthentication();
app.UseAuthorization();
```

### 5. Configure Authorization Policies

```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("Listener", policy =>
        policy.RequireAuthenticatedUser());

    options.AddPolicy("Admin", policy =>
        policy.RequireClaim("roles", "admin"));

    options.AddPolicy("ActiveUser", policy =>
        policy.Requirements.Add(new ActiveUserRequirement()));
});
```

### 6. Create ActiveUser Authorization Requirement

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Authorization/ActiveUserRequirement.cs`

```csharp
public class ActiveUserRequirement : IAuthorizationRequirement { }

public class ActiveUserHandler : AuthorizationHandler<ActiveUserRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        ActiveUserRequirement requirement)
    {
        var statusClaim = context.User.FindFirstValue("status");

        if (statusClaim == UserStatus.Active.ToString())
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}
```

## Required NuGet Packages

```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package System.IdentityModel.Tokens.Jwt
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `JWT_SIGNING_KEY` | Secret key for token signing (min 32 chars) | Yes |

## Security Checklist

- [ ] Signing key is NOT in appsettings.json
- [ ] Signing key is at least 256 bits (32 characters)
- [ ] `ClockSkew` is set to `TimeSpan.Zero`
- [ ] Access token TTL is short (15 minutes)
- [ ] `jti` claim is included for revocation support
- [ ] Token never logged (add to redaction policy)

## Testing

```csharp
[Fact]
public void GenerateAccessToken_IncludesRequiredClaims()
{
    var user = new ApplicationUser
    {
        UserId = "01HQ3K...",
        Email = "test@example.com",
        Roles = ["Listener"]
    };

    var token = _tokenService.GenerateAccessToken(user);
    var principal = _tokenService.ValidateToken(token);

    principal.Should().NotBeNull();
    principal!.FindFirstValue(JwtRegisteredClaimNames.Sub).Should().Be(user.UserId);
    principal.FindFirstValue("roles").Should().Be("listener");
}
```