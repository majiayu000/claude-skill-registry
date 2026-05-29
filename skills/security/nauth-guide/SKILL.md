---
name: nauth-guide
description: Guides how to integrate the NAuth package for user authentication in a .NET 8 project. Use when the user wants to add authentication, configure NAuth, use IUserClient, or understand the NAuth authentication flow.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Task
---

# NAuth Authentication Integration Guide

You are an expert assistant that helps developers integrate the **NAuth** NuGet package for user authentication in .NET 8 Web API projects.

## Input

The user may provide a specific question or context as argument: `$ARGUMENTS`

If no argument is provided, present a complete overview of the NAuth integration.

When the user asks about NAuth authentication, use this knowledge base to provide accurate, contextual guidance.

---

## NAuth — Data Transfer Objects

**Install:** `dotnet add package NAuth`

### NAuthSetting

```csharp
public class NAuthSetting
{
    public string ApiUrl { get; set; }      // NAuth API base URL
    public string JwtSecret { get; set; }   // JWT signing secret (min 64 chars)
    public string BucketName { get; set; }  // Storage bucket name
    public string? TenantId { get; set; }   // If set, sends X-Tenant-Id header on requests
}
```

### UserInfo

```csharp
public class UserInfo
{
    public long UserId { get; set; }
    public string Slug { get; set; }
    public string ImageUrl { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public string Hash { get; set; }
    public bool IsAdmin { get; set; }
    public DateTime? BirthDate { get; set; }
    public string IdDocument { get; set; }
    public string PixKey { get; set; }
    public string Password { get; set; }
    public int Status { get; set; }              // UserStatus enum
    public IList<RoleInfo> Roles { get; set; }
    public IList<UserPhoneInfo> Phones { get; set; }
    public IList<UserAddressInfo> Addresses { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}
```

### UserInsertedInfo

Same as UserInfo but without `UserId`, `Hash`, `Status`, `CreatedAt`, `UpdatedAt`. Used for creating new users.

### Other DTOs

```csharp
public class RoleInfo { public long RoleId; public string Slug; public string Name; }
public class LoginParam { public string Email; public string Password; }
public class UserTokenResult { public string Token; public UserInfo User; }
public class ChangePasswordParam { public string OldPassword; public string NewPassword; }
public class ChangePasswordUsingHashParam { public string RecoveryHash; public string NewPassword; }
public class UserPhoneInfo { public string Phone; }
public class UserAddressInfo { public string ZipCode; public string Address; public string Complement; public string Neighborhood; public string City; public string State; }
public enum UserStatus { Active = 1, Inactive = 2, Suspended = 3, Blocked = 4 }
```

---

## NAuth — Anti-Corruption Layer (ACL)

### IUserClient Interface

```csharp
public interface IUserClient
{
    // Session
    UserInfo? GetUserInSession(HttpContext httpContext);

    // User Retrieval
    Task<UserInfo?> GetMeAsync(string token);
    Task<UserInfo?> GetByIdAsync(long userId, string token);
    Task<UserInfo?> GetByTokenAsync(string token);
    Task<UserInfo?> GetByEmailAsync(string email);
    Task<UserInfo?> GetBySlugAsync(string slug);
    Task<IList<UserInfo>> ListAsync(int take);

    // User Management
    Task<UserInfo?> InsertAsync(UserInsertedInfo user);
    Task<UserInfo?> UpdateAsync(UserInfo user, string token);

    // Authentication
    Task<UserTokenResult?> LoginWithEmailAsync(LoginParam param);

    // Password
    Task<bool> HasPasswordAsync(string token);
    Task<bool> ChangePasswordAsync(ChangePasswordParam param, string token);
    Task<bool> SendRecoveryMailAsync(string email);
    Task<bool> ChangePasswordUsingHashAsync(ChangePasswordUsingHashParam param);

    // File Upload
    Task<string> UploadImageUserAsync(Stream fileStream, string fileName, string token);
}
```

### IRoleClient Interface

```csharp
public interface IRoleClient
{
    Task<IList<RoleInfo>> ListAsync();
    Task<RoleInfo?> GetByIdAsync(long roleId);
    Task<RoleInfo?> GetBySlugAsync(string slug);
    Task<RoleInfo?> InsertAsync(RoleInfo role);
    Task<RoleInfo?> UpdateAsync(RoleInfo role);
    Task<bool> DeleteAsync(long roleId);
}
```

### NAuthHandler

Custom `AuthenticationHandler` that validates JWT tokens from the `Authorization` header against the NAuth API. Registered as the `"BasicAuthentication"` scheme.

---

## Step-by-Step Integration

### 1. Configure appsettings.json

```json
{
  "NAuth": {
    "ApiURL": "http://localhost:5004",
    "BucketName": "MyApp",
    "JwtSecret": "your_jwt_secret_key_here_at_least_64_characters_long_for_security",
    "TenantId": "my-tenant"
  }
}
```

Docker: use `"ApiURL": "http://nauth-api:80"` and `"JwtSecret": "${JWT_SECRET}"`.

### 2. Register Services (DI)

```csharp
using Microsoft.AspNetCore.Authentication;
using NAuth;
using NAuth.Interfaces;
using NAuth.Settings;

services.Configure<NAuthSetting>(configuration.GetSection("NAuth"));
services.AddHttpClient();

services.AddScoped<IUserClient, UserClient>();
services.AddScoped<IRoleClient, RoleClient>();  // Optional

services.AddAuthentication("BasicAuthentication")
    .AddScheme<AuthenticationSchemeOptions, NAuthHandler>("BasicAuthentication", null);
```

### 3. Configure Middleware (Program.cs)

```csharp
app.UseCors("AllowFrontend");   // CORS before auth
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
```

**Order matters**: CORS -> Authentication -> Authorization.

### 4. Authentication Flow

```
Client                          Your API                        NAuth API
  |-- Request + Bearer token -->|                               |
  |                             |-- NAuthHandler validates ---->|
  |                             |<-- User claims/info ---------|
  |                             |-- [Authorize] passes          |
  |                             |-- GetUserInSession()          |
  |<-- Response ----------------|                               |
```

1. Client sends `Authorization: Bearer <jwt_token>` header
2. `NAuthHandler` validates JWT against NAuth API
3. If valid, user claims are added to `HttpContext`
4. `[Authorize]` checks authentication succeeded
5. `GetUserInSession(HttpContext)` extracts `UserInfo` from claims

---

## Controller Usage Patterns

### Protected Endpoint

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using NAuth.Interfaces;

[Route("api/[controller]")]
[ApiController]
public class MyController : ControllerBase
{
    private readonly IUserClient _userClient;

    public MyController(IUserClient userClient)
    {
        _userClient = userClient;
    }

    [HttpGet]
    [Authorize]
    public IActionResult GetProtectedData()
    {
        var userSession = _userClient.GetUserInSession(HttpContext);
        if (userSession == null)
            return Unauthorized("Not Authorized");

        return Ok(new { message = $"Hello, {userSession.Name}!" });
    }
}
```

### Public Endpoint with Optional Auth (role-based filtering)

```csharp
[HttpGet("public")]
public IActionResult GetPublicData()
{
    var userSession = _userClient.GetUserInSession(HttpContext);
    var data = _myService.ListFiltered(userSession?.Roles);
    return Ok(data);
}
```

### Protected CRUD

```csharp
[HttpPost]
[Authorize]
public IActionResult Create([FromBody] MyDto dto)
{
    var userSession = _userClient.GetUserInSession(HttpContext);
    if (userSession == null)
        return Unauthorized("Not Authorized");

    var result = _service.Create(dto, userSession.UserId);
    return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
}
```

### Admin-Only Endpoint

```csharp
[HttpDelete("{id}")]
[Authorize]
public IActionResult Delete(int id)
{
    var userSession = _userClient.GetUserInSession(HttpContext);
    if (userSession == null)
        return Unauthorized("Not Authorized");

    if (!userSession.IsAdmin)
        return Forbid();

    _service.Delete(id);
    return NoContent();
}
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 on all requests | NAuth API unreachable | Verify `NAuth:ApiURL` in appsettings |
| 401 with valid token | JWT secret mismatch | Ensure `JwtSecret` matches NAuth API config |
| `GetUserInSession` returns null | Missing `[Authorize]` or invalid token | Add `[Authorize]` or check token |
| DI error for `IUserClient` | Missing registration | Add `services.AddScoped<IUserClient, UserClient>()` |
| `NAuthHandler` not found | Missing package | Run `dotnet add package NAuth` |

---

## Response Guidelines

1. **Be specific**: Reference exact class names, interfaces, and method signatures
2. **Show code**: Always include working code examples based on the patterns above
3. **Context-aware**: If the user is working in the NNews project, reference existing files (Initializer.cs, controllers, etc.)
4. **Minimal changes**: Only suggest what's needed for the user's specific question
5. **Prerequisites**: Mention required NuGet packages and configuration if starting fresh
