---
name: jwt-authentication
description: "Configures JWT Bearer authentication for .NET APIs. Includes token generation, validation, refresh tokens, and user context extraction from claims."
version: 1.1.0
language: C#
framework: .NET 8+
dependencies: Microsoft.AspNetCore.Authentication.JwtBearer, System.IdentityModel.Tokens.Jwt
---

# JWT Authentication Setup

## Overview

This skill implements JWT (JSON Web Token) authentication for .NET APIs:

- **Access Token** - Short-lived JWT returned in response body
- **Refresh Token** - Stored in HttpOnly cookie (secure, not accessible via JavaScript)
- **Options Pattern** - Configurable expiration via JwtOptions
- **Token Rotation** - New refresh token issued on each refresh
- **Security Audit** - Comprehensive event tracking for compliance
- **Token generation** - Create access and refresh tokens
- **Token validation** - Validate incoming tokens
- **User context** - Extract user info from claims

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| `IJwtService` | Token generation interface | Application/Abstractions |
| `JwtService` | Token generation implementation | Infrastructure/Authentication |
| `JwtOptions` | configuration (expiration, issuer, etc.) | Infrastructure/Authentication |
| `JwtBearerOptionsSetup` | Configure JWT validation | Infrastructure/Authentication |
| `IUserContext` | Current user info | Application/Abstractions |
| `UserContext` | Extract from HttpContext | Infrastructure/Authentication |
| `IRefreshTokenRepository` | Refresh token storage | Domain/Identity |
| `CookieSettings` | Cookie configuration | Infrastructure/Authentication |

---

## Authentication Structure

```
/Application/Abstractions/
├── Authentication/
│   ├── IJwtService.cs
│   ├── IUserContext.cs
│   ├── TokenResponse.cs
│   └── AuthenticationErrors.cs

/Infrastructure/
├── Authentication/
│   ├── JwtOptions.cs
│   ├── JwtService.cs
│   ├── JwtBearerOptionsSetup.cs
│   ├── UserContext.cs
│   ├── CookieSettings.cs
│   └── RefreshTokenCookieManager.cs
```

---

## Template: JWT Configuration Options

```csharp
// src/{name}.infrastructure/Authentication/JwtOptions.cs
namespace {name}.infrastructure.authentication;

public sealed class JwtOptions
{
    public const string SectionName = "Jwt";

    public string Issuer { get; init; } = string.Empty;
    public string Audience { get; init; } = string.Empty;
    public string SecretKey { get; init; } = string.Empty;
    public int AccessTokenExpirationMinutes { get; init; } = 60;
    public int RefreshTokenExpirationDays { get; init; } = 7;
    public CookieSettings Cookie { get; init; } = new();
}

public sealed class CookieSettings
{
    /// <summary>
    /// Name of the refresh token cookie
    /// </summary>
    public string Name { get; init; } = "X-Refresh-Token";

    /// <summary>
    /// Cookie domain (leave empty for current domain)
    /// </summary>
    public string? Domain { get; init; }

    /// <summary>
    /// Cookie path
    /// </summary>
    public string Path { get; init; } = "/api/v1/auth";

    /// <summary>
    /// SameSite policy (Strict recommended for healthcare)
    /// </summary>
    public SameSiteMode SameSite { get; init; } = SameSiteMode.Strict;

    /// <summary>
    /// Require HTTPS (always true in production)
    /// </summary>
    public bool SecureOnly { get; init; } = true;
}
```

### appsettings.json

```json
{
  "Jwt": {
    "Issuer": "your-app-name",
    "Audience": "your-app-name",
    "SecretKey": "your-secret-key-at-least-32-characters-long-for-security",
    "AccessTokenExpirationMinutes": 60,
    "RefreshTokenExpirationDays": 7,
    "Cookie": {
      "Name": "X-Refresh-Token",
      "Domain": "",
      "Path": "/api/v1/auth",
      "SameSite": "Strict",
      "SecureOnly": true
    }    
  }
}
```

---

## Template: JWT Service Interface

```csharp
// src/{name}.application/Abstractions/Authentication/IJwtService.cs
using {name}.domain.users;

namespace {name}.application.abstractions.authentication;

public interface IJwtService
{
    /// <summary>
    /// Generate access and refresh tokens for a user
    /// </summary>
    TokenGenerationResult GenerateTokens(
        User user, 
        IEnumerable<string> roles,
        IEnumerable<string>? permissions = null);

    /// <summary>
    /// Generate tokens with custom claims
    /// </summary>
    TokenGenerationResult GenerateTokens(
        Guid userId,
        string email,
        IEnumerable<string> roles,
        IDictionary<string, string>? additionalClaims = null);

    /// <summary>
    /// Hash a refresh token for secure database storage
    /// </summary>
    string HashRefreshToken(string refreshToken);

    /// <summary>
    /// Verify a plain refresh token against its hash
    /// </summary>
    bool VerifyRefreshToken(string plainToken, string hashedToken);

    /// <summary>
    /// Get access token expiration time
    /// </summary>
    DateTime GetAccessTokenExpiry();

    /// <summary>
    /// Get refresh token expiration time
    /// </summary>
    DateTime GetRefreshTokenExpiry();
}
```

---

## Template: Token Response

```csharp
// src/{name}.application/Abstractions/Authentication/TokenResponse.cs
namespace {name}.application.abstractions.authentication;

/// <summary>
/// Response containing access token (refresh token is set via HttpOnly cookie)
/// </summary>
public sealed record TokenResponse(
    string AccessToken,
    DateTime AccessTokenExpiration,
    string TokenType = "Bearer");

/// <summary>
/// Internal response including refresh token (for cookie setting)
/// </summary>
public sealed record TokenGenerationResult(
    string AccessToken,
    string RefreshToken,
    DateTime AccessTokenExpiration,
    DateTime RefreshTokenExpiration);
```

---

## Template: JWT Service Implementation

```csharp
// src/{name}.infrastructure/Authentication/JwtService.cs
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using {name}.application.Abstractions.Authentication;
using {name}.application.Abstractions.Clock;
using {name}.domain.identity;

namespace {name}.infrastructure.authentication;

internal sealed class JwtService : IJwtService
{
    private readonly JwtOptions _options;
    private readonly IDateTimeProvider _dateTimeProvider;
    private readonly SigningCredentials _signingCredentials;
    private readonly JwtSecurityTokenHandler _tokenHandler;

    public JwtService(
        IOptions<JwtOptions> options,
        IDateTimeProvider dateTimeProvider)
    {
        _options = options.Value;
        _dateTimeProvider = dateTimeProvider;

        var securityKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_options.SecretKey));

        _signingCredentials = new SigningCredentials(
            securityKey,
            SecurityAlgorithms.HmacSha256);

        _tokenHandler = new JwtSecurityTokenHandler();
    }

    public TokenGenerationResult GenerateTokens(
        User user,
        IEnumerable<string> roles,
        IEnumerable<string>? permissions = null)
    {
        var additionalClaims = new Dictionary<string, string>
        {
            ["name"] = $"{user.FirstName} {user.LastName}".Trim()
        };

        return GenerateTokensInternal(
            user.Id,
            user.Email,
            roles,
            permissions,
            additionalClaims);
    }

    public TokenGenerationResult GenerateTokens(
        Guid userId,
        string email,
        IEnumerable<string> roles,
        IDictionary<string, string>? additionalClaims = null)
    {
        return GenerateTokensInternal(userId, email, roles, null, additionalClaims);
    }

    private TokenGenerationResult GenerateTokensInternal(
        Guid userId,
        string email,
        IEnumerable<string> roles,
        IEnumerable<string>? permissions,
        IDictionary<string, string>? additionalClaims)
    {
        var now = _dateTimeProvider.UtcNow;
        var accessTokenExpiration = now.AddMinutes(_options.AccessTokenExpirationMinutes);
        var refreshTokenExpiration = now.AddDays(_options.RefreshTokenExpirationDays);

        // Generate access token
        var accessToken = GenerateAccessToken(
            userId,
            email,
            roles,
            permissions,
            additionalClaims,
            now,
            accessTokenExpiration);

        // Generate opaque refresh token
        var refreshToken = GenerateRefreshToken();

        return new TokenGenerationResult(
            accessToken,
            refreshToken,
            accessTokenExpiration,
            refreshTokenExpiration);
    }

    private string GenerateAccessToken(
        Guid userId,
        string email,
        IEnumerable<string> roles,
        IEnumerable<string>? permissions,
        IDictionary<string, string>? additionalClaims,
        DateTime now,
        DateTime expiration)
    {
        var claims = new List<Claim>
        {
            new(JwtRegisteredClaimNames.Sub, userId.ToString()),
            new(JwtRegisteredClaimNames.Email, email),
            new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new(JwtRegisteredClaimNames.Iat,
                new DateTimeOffset(now).ToUnixTimeSeconds().ToString(),
                ClaimValueTypes.Integer64)
        };

        // Add roles
        foreach (var role in roles)
        {
            claims.Add(new Claim(ClaimTypes.Role, role));
        }

        // Add permissions
        if (permissions is not null)
        {
            foreach (var permission in permissions)
            {
                claims.Add(new Claim("permission", permission));
            }
        }

        // Add additional claims
        if (additionalClaims is not null)
        {
            foreach (var (key, value) in additionalClaims)
            {
                if (!string.IsNullOrEmpty(value))
                {
                    claims.Add(new Claim(key, value));
                }
            }
        }

        var token = new JwtSecurityToken(
            issuer: _options.Issuer,
            audience: _options.Audience,
            claims: claims,
            notBefore: now,
            expires: expiration,
            signingCredentials: _signingCredentials);

        return _tokenHandler.WriteToken(token);
    }

    private static string GenerateRefreshToken()
    {
        var randomBytes = new byte[64];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomBytes);
        return Convert.ToBase64String(randomBytes);
    }

    public string HashRefreshToken(string refreshToken)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(refreshToken));
        return Convert.ToHexString(bytes).ToLowerInvariant();
    }

    public bool VerifyRefreshToken(string plainToken, string hashedToken)
    {
        var computedHash = HashRefreshToken(plainToken);
        return string.Equals(computedHash, hashedToken, StringComparison.OrdinalIgnoreCase);
    }

    public DateTime GetAccessTokenExpiry()
    {
        return _dateTimeProvider.UtcNow.AddMinutes(_options.AccessTokenExpirationMinutes);
    }

    public DateTime GetRefreshTokenExpiry()
    {
        return _dateTimeProvider.UtcNow.AddDays(_options.RefreshTokenExpirationDays);
    }
}
```

---

## Template: Refresh Token Cookie Manager

```csharp
// src/{name}.infrastructure/Authentication/RefreshTokenCookieManager.cs
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Options;

namespace {name}.infrastructure.authentication;

public interface IRefreshTokenCookieManager
{
    void SetRefreshTokenCookie(HttpResponse response, string refreshToken, DateTime expiry);
    string? GetRefreshTokenFromCookie(HttpRequest request);
    void ClearRefreshTokenCookie(HttpResponse response);
}

internal sealed class RefreshTokenCookieManager : IRefreshTokenCookieManager
{
    private readonly JwtOptions _options;

    public RefreshTokenCookieManager(IOptions<JwtOptions> options)
    {
        _options = options.Value;
    }

    public void SetRefreshTokenCookie(HttpResponse response, string refreshToken, DateTime expiry)
    {
        var cookieOptions = new CookieOptions
        {
            HttpOnly = true,                          // Not accessible via JavaScript (XSS protection)
            Secure = _options.Cookie.SecureOnly,      // HTTPS only
            SameSite = _options.Cookie.SameSite,      // CSRF protection
            Expires = expiry,
            Path = _options.Cookie.Path,
            Domain = string.IsNullOrEmpty(_options.Cookie.Domain) 
                ? null 
                : _options.Cookie.Domain,
            IsEssential = true                        // Required for GDPR compliance
        };

        response.Cookies.Append(_options.Cookie.Name, refreshToken, cookieOptions);
    }

    public string? GetRefreshTokenFromCookie(HttpRequest request)
    {
        return request.Cookies.TryGetValue(_options.Cookie.Name, out var token) 
            ? token 
            : null;
    }

    public void ClearRefreshTokenCookie(HttpResponse response)
    {
        var cookieOptions = new CookieOptions
        {
            HttpOnly = true,
            Secure = _options.Cookie.SecureOnly,
            SameSite = _options.Cookie.SameSite,
            Expires = DateTime.UtcNow.AddDays(-1),    // Expire immediately
            Path = _options.Cookie.Path,
            Domain = string.IsNullOrEmpty(_options.Cookie.Domain) 
                ? null 
                : _options.Cookie.Domain
        };

        response.Cookies.Append(_options.Cookie.Name, string.Empty, cookieOptions);
    }
}
```

---

## Template: Refresh Token Entity

```csharp
// src/{name}.domain/identity/RefreshToken.cs
namespace {name}.domain.identity;

public sealed class RefreshToken
{
    public Guid Id { get; private set; }
    public Guid UserId { get; private set; }
    public string TokenHash { get; private set; } = string.Empty;
    public DateTime CreatedAt { get; private set; }
    public DateTime ExpiresAt { get; private set; }
    public DateTime? RevokedAt { get; private set; }
    public string? ReplacedByTokenHash { get; private set; }
    public string? DeviceInfo { get; private set; }
    public string? IpAddress { get; private set; }

    public bool IsExpired => DateTime.UtcNow >= ExpiresAt;
    public bool IsRevoked => RevokedAt.HasValue;
    public bool IsActive => !IsRevoked && !IsExpired;

    private RefreshToken() { }

    public static RefreshToken Create(
        Guid userId,
        string tokenHash,
        DateTime expiresAt,
        string? deviceInfo = null,
        string? ipAddress = null)
    {
        return new RefreshToken
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            TokenHash = tokenHash,
            CreatedAt = DateTime.UtcNow,
            ExpiresAt = expiresAt,
            DeviceInfo = deviceInfo,
            IpAddress = ipAddress
        };
    }

    public void Revoke(string? replacedByTokenHash = null)
    {
        RevokedAt = DateTime.UtcNow;
        ReplacedByTokenHash = replacedByTokenHash;
    }
}
```

---

## Template: JWT Bearer Options Setup

```csharp
// src/{name}.infrastructure/Authentication/JwtBearerOptionsSetup.cs
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

namespace {name}.infrastructure.authentication;

internal sealed class JwtBearerOptionsSetup 
    : IConfigureNamedOptions<JwtBearerOptions>
{
    private readonly JwtOptions _jwtOptions;

    public JwtBearerOptionsSetup(IOptions<JwtOptions> jwtOptions)
    {
        _jwtOptions = jwtOptions.Value;
    }

    public void Configure(JwtBearerOptions options)
    {
        Configure(JwtBearerDefaults.AuthenticationScheme, options);
    }

    public void Configure(string? name, JwtBearerOptions options)
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = _jwtOptions.Issuer,
            
            ValidateAudience = true,
            ValidAudience = _jwtOptions.Audience,
            
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(_jwtOptions.SecretKey)),
            
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero,  // No tolerance for expiration
            
            // Ensure we get the user ID from the token
            NameClaimType = "sub",
            RoleClaimType = "role"
        };

        options.Events = new JwtBearerEvents
        {
            OnAuthenticationFailed = context =>
            {
                if (context.Exception is SecurityTokenExpiredException)
                {
                    context.Response.Headers.Append(
                        "Token-Expired",
                        "true");
                }
                return Task.CompletedTask;
            },
            OnChallenge = context =>
            {
                // Custom response for 401
                return Task.CompletedTask;
            },
            OnForbidden = context =>
            {
                // Custom response for 403
                return Task.CompletedTask;
            }
        };
    }
}
```

---

## Template: User Context Interface

```csharp
// src/{name}.application/Abstractions/Authentication/IUserContext.cs
namespace {name}.application.abstractions.authentication;

public interface IUserContext
{
    /// <summary>
    /// Current authenticated user's ID
    /// </summary>
    Guid UserId { get; }

    /// <summary>
    /// Current user's email
    /// </summary>
    string Email { get; }

    /// <summary>
    /// Current user's organization ID
    /// </summary>
    Guid? OrganizationId { get; }

    /// <summary>
    /// Current user's roles
    /// </summary>
    IReadOnlyList<string> Roles { get; }

    /// <summary>
    /// Check if user is authenticated
    /// </summary>
    bool IsAuthenticated { get; }

    /// <summary>
    /// Check if user has a specific role
    /// </summary>
    bool IsInRole(string role);

    /// <summary>
    /// Get a custom claim value
    /// </summary>
    string? GetClaimValue(string claimType);
}
```

---

## Template: User Context Implementation

```csharp
// src/{name}.infrastructure/Authentication/UserContext.cs
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Microsoft.AspNetCore.Http;
using {name}.application.abstractions.authentication;

namespace {name}.infrastructure.authentication;

internal sealed class UserContext : IUserContext
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public UserContext(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    private ClaimsPrincipal? User => _httpContextAccessor.HttpContext?.User;

    public bool IsAuthenticated => User?.Identity?.IsAuthenticated ?? false;

    public Guid UserId
    {
        get
        {
            var userIdClaim = User?.FindFirst(JwtRegisteredClaimNames.Sub)?.Value
                ?? User?.FindFirst(ClaimTypes.NameIdentifier)?.Value;

            return Guid.TryParse(userIdClaim, out var userId)
                ? userId
                : throw new InvalidOperationException("User ID not found in claims");
        }
    }

    public string Email
    {
        get
        {
            return User?.FindFirst(JwtRegisteredClaimNames.Email)?.Value
                ?? User?.FindFirst(ClaimTypes.Email)?.Value
                ?? string.Empty;
        }
    }

    public Guid? OrganizationId
    {
        get
        {
            var orgIdClaim = User?.FindFirst("organization_id")?.Value;
            return Guid.TryParse(orgIdClaim, out var orgId) ? orgId : null;
        }
    }

    public IReadOnlyList<string> Roles
    {
        get
        {
            return User?.FindAll(ClaimTypes.Role)
                .Select(c => c.Value)
                .ToList()
                ?? new List<string>();
        }
    }

    public bool IsInRole(string role)
    {
        return User?.IsInRole(role) ?? false;
    }

    public string? GetClaimValue(string claimType)
    {
        return User?.FindFirst(claimType)?.Value;
    }
}
```

---

## Template: Authentication Registration

```csharp
// src/{name}.infrastructure/Authentication/AuthenticationExtensions.cs
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using {name}.application.abstractions.authentication;

namespace {name}.infrastructure.authentication;

public static class AuthenticationExtensions
{
    public static IServiceCollection AddJwtAuthentication(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Bind JWT options
        services.Configure<JwtOptions>(
            configuration.GetSection(JwtOptions.SectionName));

        // Register JWT Bearer authentication
        services
            .AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultScheme = JwtBearerDefaults.AuthenticationScheme;
            })
            .AddJwtBearer();

        // Configure JWT Bearer options
        services.ConfigureOptions<JwtBearerOptionsSetup>();

        // Register services
        services.AddHttpContextAccessor();
        services.AddScoped<IJwtService, JwtService>();
        services.AddScoped<IUserContext, UserContext>();

        return services;
    }
}
```

---

## Template: Login Command Handler

```csharp
// src/{name}.application/Users/Login/LoginUserCommandHandler.cs
using {name}.application.Abstractions.Authentication;
using {name}.application.Abstractions.Messaging;
using {name}.domain.abstractions;
using {name}.domain.identity;

namespace {name}.application.users.login;

public sealed record LoginUserCommand(
    string Email,
    string Password,
    string? DeviceInfo = null,
    string? IpAddress = null) : ICommand<TokenResponse>;

internal sealed class LoginUserCommandHandler
    : ICommandHandler<LoginUserCommand, TokenResponse>
{
    private readonly IUserRepository _userRepository;
    private readonly IPasswordHasher _passwordHasher;
    private readonly IJwtService _jwtService;
    private readonly IRoleRepository _roleRepository;
    private readonly IRefreshTokenRepository _refreshTokenRepository;
    private readonly IUnitOfWork _unitOfWork;

    public LoginUserCommandHandler(
        IUserRepository userRepository,
        IPasswordHasher passwordHasher,
        IJwtService jwtService,
        IRoleRepository roleRepository,
        IRefreshTokenRepository refreshTokenRepository,
        IUnitOfWork unitOfWork)
    {
        _userRepository = userRepository;
        _passwordHasher = passwordHasher;
        _jwtService = jwtService;
        _roleRepository = roleRepository;
        _refreshTokenRepository = refreshTokenRepository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<TokenResponse>> Handle(
        LoginUserCommand request,
        CancellationToken cancellationToken)
    {
        // Find user by email
        var user = await _userRepository.GetByEmailAsync(
            request.Email,
            cancellationToken);

        if (user is null)
        {
            return Result.Failure<TokenResponse>(UserErrors.InvalidCredentials);
        }

        // Verify password
        if (!_passwordHasher.Verify(request.Password, user.PasswordHash))
        {
            return Result.Failure<TokenResponse>(UserErrors.InvalidCredentials);
        }

        // Check if user is active
        if (!user.IsActive)
        {
            return Result.Failure<TokenResponse>(UserErrors.AccountDeactivated);
        }

        // Get user roles and permissions
        var roles = await _roleRepository.GetRolesByUserIdAsync(user.Id, cancellationToken);
        var roleNames = roles.Select(r => r.Name);
        var permissions = roles.SelectMany(r => r.Permissions).Distinct();

        // Generate tokens
        var tokenResult = _jwtService.GenerateTokens(user, roleNames, permissions);

        // Store hashed refresh token in database
        var refreshTokenEntity = RefreshToken.Create(
            userId: user.Id,
            tokenHash: _jwtService.HashRefreshToken(tokenResult.RefreshToken),
            expiresAt: tokenResult.RefreshTokenExpiration,
            deviceInfo: request.DeviceInfo,
            ipAddress: request.IpAddress);

        _refreshTokenRepository.Add(refreshTokenEntity);
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        // Return access token (refresh token will be set in cookie by controller)
        return new TokenResponse(
            tokenResult.AccessToken,
            tokenResult.AccessTokenExpiration);
    }
}
```

---

## Template: Refresh Token Command Handler

```csharp
// src/{name}.application/Users/RefreshToken/RefreshTokenCommandHandler.cs
using {name}.application.Abstractions.Authentication;
using {name}.application.Abstractions.Messaging;
using {name}.domain.abstractions;
using {name}.domain.identity;

namespace {name}.application.users.refreshToken;

public sealed record RefreshTokenCommand(
    string RefreshToken,
    string? DeviceInfo = null,
    string? IpAddress = null) : ICommand<TokenGenerationResult>;

internal sealed class RefreshTokenCommandHandler
    : ICommandHandler<RefreshTokenCommand, TokenGenerationResult>
{
    private readonly IJwtService _jwtService;
    private readonly IUserRepository _userRepository;
    private readonly IRoleRepository _roleRepository;
    private readonly IRefreshTokenRepository _refreshTokenRepository;
    private readonly IUnitOfWork _unitOfWork;

    public RefreshTokenCommandHandler(
        IJwtService jwtService,
        IUserRepository userRepository,
        IRoleRepository roleRepository,
        IRefreshTokenRepository refreshTokenRepository,
        IUnitOfWork unitOfWork)
    {
        _jwtService = jwtService;
        _userRepository = userRepository;
        _roleRepository = roleRepository;
        _refreshTokenRepository = refreshTokenRepository;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<TokenGenerationResult>> Handle(
        RefreshTokenCommand request,
        CancellationToken cancellationToken)
    {
        // Hash the incoming token to find it in database
        var tokenHash = _jwtService.HashRefreshToken(request.RefreshToken);

        // Find the stored refresh token
        var storedToken = await _refreshTokenRepository.GetByHashAsync(
            tokenHash,
            cancellationToken);

        if (storedToken is null || !storedToken.IsActive)
        {
            return Result.Failure<TokenGenerationResult>(UserErrors.InvalidRefreshToken);
        }

        // Get user
        var user = await _userRepository.GetByIdAsync(
            storedToken.UserId,
            cancellationToken);

        if (user is null || !user.IsActive)
        {
            // Revoke the token if user is invalid
            storedToken.Revoke();
            await _unitOfWork.SaveChangesAsync(cancellationToken);
            return Result.Failure<TokenGenerationResult>(UserErrors.InvalidRefreshToken);
        }

        // Get current roles and permissions
        var roles = await _roleRepository.GetRolesByUserIdAsync(user.Id, cancellationToken);
        var roleNames = roles.Select(r => r.Name);
        var permissions = roles.SelectMany(r => r.Permissions).Distinct();

        // Generate new tokens
        var tokenResult = _jwtService.GenerateTokens(user, roleNames, permissions);

        // Rotate refresh token: revoke old, create new
        var newTokenHash = _jwtService.HashRefreshToken(tokenResult.RefreshToken);
        storedToken.Revoke(replacedByTokenHash: newTokenHash);

        var newRefreshToken = Domain.Identity.RefreshToken.Create(
            userId: user.Id,
            tokenHash: newTokenHash,
            expiresAt: tokenResult.RefreshTokenExpiration,
            deviceInfo: request.DeviceInfo,
            ipAddress: request.IpAddress);

        _refreshTokenRepository.Add(newRefreshToken);
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        return tokenResult;
    }
}
```

---

## Template: Auth Controller

```csharp
// src/{name}.api/Controllers/Auth/AuthController.cs
using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using {name}.application.abstractions.authentication;
using {name}.application.users.login;
using {name}.application.users.refreshToken;
using {name}.infrastructure.authentication;

namespace {name}.api.Controllers.Auth;

[ApiController]
[Route("api/v1/auth")]
public class AuthController : ControllerBase
{
    private readonly ISender _sender;
    private readonly IRefreshTokenCookieManager _cookieManager;

    public AuthController(
        ISender sender,
        IRefreshTokenCookieManager cookieManager)
    {
        _sender = sender;
        _cookieManager = cookieManager;
    }

    [HttpPost("login")]
    [AllowAnonymous]
    public async Task<IActionResult> LoginFull(
        [FromBody] LoginRequest request,
        CancellationToken cancellationToken)
    {
        var command = new LoginUserCommand(
            request.Email,
            request.Password,
            DeviceInfo: Request.Headers.UserAgent,
            IpAddress: HttpContext.Connection.RemoteIpAddress?.ToString());

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return Unauthorized(new { error = result.Error.Code, message = result.Error.Message });
        }

        // Set refresh token in HttpOnly cookie
        _cookieManager.SetRefreshTokenCookie(
            Response,
            result.Value.RefreshToken,
            result.Value.RefreshTokenExpiration);

        // Return only access token in response body
        return Ok(new TokenResponse(
            result.Value.AccessToken,
            result.Value.AccessTokenExpiration));
    }

    [HttpPost("refresh")]
    [AllowAnonymous]
    public async Task<IActionResult> RefreshToken(CancellationToken cancellationToken)
    {
        // Get refresh token from HttpOnly cookie
        var refreshToken = _cookieManager.GetRefreshTokenFromCookie(Request);

        if (string.IsNullOrEmpty(refreshToken))
        {
            return Unauthorized(new { error = "invalid_token", message = "Refresh token not found" });
        }

        var command = new RefreshTokenCommand(
            refreshToken,
            DeviceInfo: Request.Headers.UserAgent,
            IpAddress: HttpContext.Connection.RemoteIpAddress?.ToString());

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            // Clear invalid cookie
            _cookieManager.ClearRefreshTokenCookie(Response);
            return Unauthorized(new { error = result.Error.Code, message = result.Error.Message });
        }

        // Set new refresh token in HttpOnly cookie (rotation)
        _cookieManager.SetRefreshTokenCookie(
            Response,
            result.Value.RefreshToken,
            result.Value.RefreshTokenExpiration);

        // Return only access token in response body
        return Ok(new TokenResponse(
            result.Value.AccessToken,
            result.Value.AccessTokenExpiration));
    }

    [HttpPost("logout")]
    [Authorize]
    public async Task<IActionResult> Logout(CancellationToken cancellationToken)
    {
        // Get refresh token from cookie and revoke it
        var refreshToken = _cookieManager.GetRefreshTokenFromCookie(Request);

        if (!string.IsNullOrEmpty(refreshToken))
        {
            var command = new RevokeRefreshTokenCommand(refreshToken);
            await _sender.Send(command, cancellationToken);
        }

        // Clear the cookie
        _cookieManager.ClearRefreshTokenCookie(Response);

        return NoContent();
    }

    [HttpGet("me")]
    [Authorize]
    public IActionResult GetCurrentUser([FromServices] IUserContext userContext)
    {
        return Ok(new
        {
            UserId = userContext.UserId,
            Email = userContext.Email,
            Name = userContext.Name,
            PatientId = userContext.PatientId,
            Roles = userContext.Roles,
            Permissions = userContext.Permissions
        });
    }
}

public sealed record LoginRequest(string Email, string Password);
```

---

## Template: Dependency Injection Registration

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
private static void AddAuthentication(IServiceCollection services, IConfiguration configuration)
{
    // Configure JWT options with nested cookie settings
    services.Configure<JwtOptions>(configuration.GetSection(JwtOptions.SectionName));

    // Register authentication services
    services.AddScoped<IJwtService, JwtService>();
    services.AddScoped<IRefreshTokenCookieManager, RefreshTokenCookieManager>();

    // Register HttpContextAccessor for UserContext
    services.AddHttpContextAccessor();
    services.AddScoped<IUserContext, UserContext>();

    // Configure JWT Bearer authentication
    services
        .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddJwtBearer();

    services.ConfigureOptions<JwtBearerOptionsSetup>();

    // Configure authorization
    services.AddAuthorization();
}
```

---

## Critical Rules

1. **Secret key length** - At least 32 characters for HMAC-SHA256
2. **Store secrets securely** - Use Azure Key Vault, AWS Secrets, etc.
3. **Short access tokens** - 15-60 minutes typical
4. **Longer refresh tokens** - 7-30 days typical
5. **Validate all claims** - Issuer, audience, signature, expiration
6. **No clock skew** - Set `ClockSkew = TimeSpan.Zero`
7. **HTTPS only** - Never transmit tokens over HTTP
8. **HttpOnly cookies** - Refresh tokens should never be accessible via JavaScript
9. **Token rotation** - Issue new refresh token on each use
10. **Revoke on logout** - Always revoke refresh token on logout
11. **Use IUserContext** - Don't access HttpContext directly in handlers

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Returning refresh token in response body
return Ok(new { accessToken, refreshToken });  // Exposed to XSS!

// ✅ CORRECT: Set refresh token in HttpOnly cookie
_cookieManager.SetRefreshTokenCookie(Response, refreshToken, expiry);
return Ok(new { accessToken });

// ❌ WRONG: Storing plain refresh token
await _db.RefreshTokens.AddAsync(new { Token = refreshToken });

// ✅ CORRECT: Store hashed token
await _db.RefreshTokens.AddAsync(new { TokenHash = _jwtService.HashRefreshToken(refreshToken) });

// ❌ WRONG: Short secret key
"SecretKey": "abc123"  // Too short, insecure!

// ✅ CORRECT: Strong secret key
"SecretKey": "your-secret-key-at-least-32-characters-long-for-security"

// ❌ WRONG: Accessing HttpContext in handler
public class Handler
{
    private readonly IHttpContextAccessor _accessor;
    var userId = _accessor.HttpContext.User.FindFirst("sub");  // Don't!
}

// ✅ CORRECT: Use IUserContext abstraction
public class Handler
{
    private readonly IUserContext _userContext;
    var userId = _userContext.UserId;
}

// ❌ WRONG: Never expiring refresh tokens
ExpiresAt = DateTime.MaxValue  // Security risk!

// ✅ CORRECT: Configured expiration
ExpiresAt = DateTime.UtcNow.AddDays(_options.RefreshTokenExpirationDays)


// ❌ WRONG: Never expiring tokens
expires: DateTime.MaxValue  // Security risk!

// ✅ CORRECT: Short-lived tokens with refresh
expires: DateTime.UtcNow.AddMinutes(60)
```

---

## Related Skills

- `permission-authorization` - Permission-based access control
- `api-controller-generator` - Protected API endpoints
- `dotnet-clean-architecture` - Infrastructure layer setup
