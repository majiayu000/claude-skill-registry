---
name: aspnet-identity
description: >
  Guidance for ASP.NET Core Identity authentication and user management.
  USE FOR: user registration, login/logout flows, password management, two-factor authentication,
  role-based authorization, external login providers, account confirmation, token generation.
  DO NOT USE FOR: fine-grained policy-based authorization (use Enforcer/Casbin), API key management,
  OAuth2 server implementation (use Duende IdentityServer), or cryptographic operations (use CryptoNet).
license: MIT
metadata:
  displayName: "ASP.NET Core Identity"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Introduction to Identity on ASP.NET Core"
    url: "https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity"
  - title: "Microsoft.AspNetCore.Identity.EntityFrameworkCore NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.AspNetCore.Identity.EntityFrameworkCore"
---

# ASP.NET Core Identity

## Overview

ASP.NET Core Identity is Microsoft's built-in membership system for adding authentication and user management to ASP.NET Core applications. It provides a complete framework for user registration, login, password hashing, two-factor authentication (2FA), external login providers, role management, and token-based account operations. Starting with .NET 8, Identity also ships with built-in API endpoints for token-based authentication in SPAs and mobile applications.

## Service Registration and Configuration

Register Identity services in `Program.cs` with the appropriate stores and options.

```csharp
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("Default")));

builder.Services.AddIdentityCore<AppUser>(options =>
{
    options.Password.RequiredLength = 12;
    options.Password.RequireDigit = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = true;
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.User.RequireUniqueEmail = true;
    options.SignIn.RequireConfirmedEmail = true;
})
.AddRoles<IdentityRole>()
.AddEntityFrameworkStores<AppDbContext>()
.AddDefaultTokenProviders()
.AddApiEndpoints();

var app = builder.Build();
app.MapIdentityApi<AppUser>();
app.Run();
```

## Custom User Entity

Extend `IdentityUser` with application-specific properties and configure the DbContext.

```csharp
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

public class AppUser : IdentityUser
{
    public string DisplayName { get; set; } = string.Empty;
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
    public string? AvatarUrl { get; set; }
}

public class AppDbContext : IdentityDbContext<AppUser>
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options) { }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);
        builder.Entity<AppUser>(entity =>
        {
            entity.Property(u => u.DisplayName).HasMaxLength(100);
            entity.HasIndex(u => u.Email).IsUnique();
        });
    }
}
```

## User Registration and Login

Use `UserManager<T>` for account operations and `SignInManager<T>` for authentication flows.

```csharp
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

public class AccountController : ControllerBase
{
    private readonly UserManager<AppUser> _userManager;
    private readonly SignInManager<AppUser> _signInManager;

    public AccountController(
        UserManager<AppUser> userManager,
        SignInManager<AppUser> signInManager)
    {
        _userManager = userManager;
        _signInManager = signInManager;
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register(RegisterRequest request)
    {
        var user = new AppUser
        {
            UserName = request.Email,
            Email = request.Email,
            DisplayName = request.DisplayName
        };

        IdentityResult result = await _userManager.CreateAsync(user, request.Password);
        if (!result.Succeeded)
            return BadRequest(result.Errors);

        string token = await _userManager.GenerateEmailConfirmationTokenAsync(user);
        // Send confirmation email with token
        return Ok(new { Message = "Registration successful. Check email to confirm." });
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login(LoginRequest request)
    {
        var result = await _signInManager.PasswordSignInAsync(
            request.Email,
            request.Password,
            isPersistent: request.RememberMe,
            lockoutOnFailure: true);

        if (result.Succeeded)
            return Ok();
        if (result.IsLockedOut)
            return Problem("Account locked. Try again later.", statusCode: 423);
        if (result.RequiresTwoFactor)
            return Ok(new { RequiresTwoFactor = true });

        return Unauthorized();
    }
}
```

## Two-Factor Authentication

Enable and verify TOTP-based two-factor authentication.

```csharp
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

[Authorize]
public class TwoFactorController : ControllerBase
{
    private readonly UserManager<AppUser> _userManager;
    private readonly SignInManager<AppUser> _signInManager;

    public TwoFactorController(
        UserManager<AppUser> userManager,
        SignInManager<AppUser> signInManager)
    {
        _userManager = userManager;
        _signInManager = signInManager;
    }

    [HttpPost("enable-2fa")]
    public async Task<IActionResult> EnableTwoFactor()
    {
        var user = await _userManager.GetUserAsync(User);
        string key = await _userManager.GetAuthenticatorKeyAsync(user!);

        if (string.IsNullOrEmpty(key))
        {
            await _userManager.ResetAuthenticatorKeyAsync(user!);
            key = (await _userManager.GetAuthenticatorKeyAsync(user!))!;
        }

        string uri = $"otpauth://totp/MyApp:{user!.Email}?secret={key}&issuer=MyApp";
        return Ok(new { SharedKey = key, AuthenticatorUri = uri });
    }

    [HttpPost("verify-2fa")]
    public async Task<IActionResult> VerifyTwoFactor(string code)
    {
        var user = await _userManager.GetUserAsync(User);
        bool isValid = await _userManager.VerifyTwoFactorTokenAsync(
            user!,
            _userManager.Options.Tokens.AuthenticatorTokenProvider,
            code);

        if (!isValid)
            return BadRequest("Invalid verification code.");

        await _userManager.SetTwoFactorEnabledAsync(user!, true);
        return Ok("Two-factor authentication enabled.");
    }
}
```

## Role-Based Authorization

Assign roles and use them for authorization checks.

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;

// Seed roles at startup
public static class RoleSeeder
{
    public static async Task SeedRolesAsync(IServiceProvider services)
    {
        var roleManager = services.GetRequiredService<RoleManager<IdentityRole>>();
        string[] roles = ["Admin", "Editor", "Viewer"];

        foreach (string role in roles)
        {
            if (!await roleManager.RoleExistsAsync(role))
                await roleManager.CreateAsync(new IdentityRole(role));
        }
    }
}

// Assign role to user
await _userManager.AddToRoleAsync(user, "Editor");

// Protect endpoints with roles
[Authorize(Roles = "Admin")]
[HttpDelete("users/{id}")]
public async Task<IActionResult> DeleteUser(string id)
{
    var user = await _userManager.FindByIdAsync(id);
    if (user is null) return NotFound();
    await _userManager.DeleteAsync(user);
    return NoContent();
}
```

## Identity Option Comparison

| Option | Default | Recommended | Notes |
|--------|---------|-------------|-------|
| Password.RequiredLength | 6 | 12+ | NIST recommends 8 minimum |
| Password.RequireNonAlphanumeric | true | true | Increases entropy |
| Lockout.MaxFailedAccessAttempts | 5 | 5 | Balance security and usability |
| Lockout.DefaultLockoutTimeSpan | 5 min | 15 min | Escalating lockouts preferred |
| User.RequireUniqueEmail | false | true | Prevents duplicate accounts |
| SignIn.RequireConfirmedEmail | false | true | Verify email ownership |
| Tokens.AuthenticatorTokenProvider | TOTP | TOTP | Standard for 2FA apps |

## Best Practices

1. **Set password requirements to NIST guidelines**: require minimum 12 characters, check against breached password lists using `IPasswordValidator<TUser>`, and avoid arbitrary complexity rules that frustrate users.
2. **Always enable account lockout**: configure `MaxFailedAccessAttempts` (5) and `DefaultLockoutTimeSpan` (15 minutes) to mitigate brute-force attacks while avoiding permanent lockout.
3. **Require email confirmation before login**: set `SignIn.RequireConfirmedEmail = true` and send confirmation tokens via `GenerateEmailConfirmationTokenAsync` to verify account ownership.
4. **Use the built-in token providers**: never implement custom password reset or confirmation token generation; use `GeneratePasswordResetTokenAsync` and `GenerateEmailConfirmationTokenAsync`.
5. **Scope DbContext per request**: register `AppDbContext` as scoped to prevent concurrency issues; never share a single DbContext across multiple requests.
6. **Prefer `AddIdentityCore<T>` over `AddIdentity<T>`** in API projects to avoid pulling in cookie-based UI dependencies you do not need.
7. **Use `MapIdentityApi<T>()` for SPA and mobile backends**: the built-in Identity API endpoints (available in .NET 8+) provide standardized token flows without manual controller code.
8. **Store sensitive Identity configuration in user secrets or a vault**: never hardcode connection strings, token signing keys, or external provider credentials in `appsettings.json`.
9. **Enable two-factor authentication for elevated roles**: require 2FA for admin accounts by combining `RequiresTwoFactor` checks with role-based policies.
10. **Audit authentication events**: subscribe to `SecurityStampChanged` and log all sign-in attempts (success, failure, lockout) for compliance and incident response.
