---
description: Add authentication endpoints (register, login, refresh, logout) to NovaTune
---
# Add Authentication Endpoint Skill

Add authentication endpoints (register, login, refresh, logout) to NovaTune.

## Project Context

- Auth endpoints go in: `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/AuthEndpoints.cs`
- Auth services go in: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/`
- DTOs go in: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Auth/`

## Steps

### 1. Create Request/Response DTOs

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Auth/`

```csharp
// RegisterRequest.cs
public record RegisterRequest(
    string Email,
    string DisplayName,
    string Password);

// LoginRequest.cs
public record LoginRequest(
    string Email,
    string Password);

// RefreshRequest.cs
public record RefreshRequest(string RefreshToken);

// AuthResponse.cs
public record AuthResponse(
    string AccessToken,
    string RefreshToken,
    int ExpiresIn,
    string TokenType = "Bearer");

// UserResponse.cs
public record UserResponse(
    string UserId,
    string Email,
    string DisplayName);
```

### 2. Create Auth Service Interface

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/IAuthService.cs`

```csharp
public interface IAuthService
{
    Task<UserResponse> RegisterAsync(RegisterRequest request, CancellationToken ct);
    Task<AuthResponse> LoginAsync(LoginRequest request, CancellationToken ct);
    Task<AuthResponse> RefreshAsync(RefreshRequest request, CancellationToken ct);
    Task LogoutAsync(string userId, string refreshToken, CancellationToken ct);
}
```

### 3. Create Auth Endpoints

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/AuthEndpoints.cs`

```csharp
public static class AuthEndpoints
{
    public static void MapAuthEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/auth")
            .WithTags("Authentication")
            .WithOpenApi();

        group.MapPost("/register", Register)
            .WithName("Register")
            .Produces<UserResponse>(StatusCodes.Status201Created)
            .ProducesProblem(StatusCodes.Status400BadRequest)
            .ProducesProblem(StatusCodes.Status409Conflict);

        group.MapPost("/login", Login)
            .WithName("Login")
            .Produces<AuthResponse>(StatusCodes.Status200OK)
            .ProducesProblem(StatusCodes.Status401Unauthorized)
            .ProducesProblem(StatusCodes.Status403Forbidden);

        group.MapPost("/refresh", Refresh)
            .WithName("RefreshToken")
            .Produces<AuthResponse>(StatusCodes.Status200OK)
            .ProducesProblem(StatusCodes.Status401Unauthorized);

        group.MapPost("/logout", Logout)
            .WithName("Logout")
            .RequireAuthorization()
            .Produces(StatusCodes.Status204NoContent);
    }

    private static async Task<IResult> Register(
        RegisterRequest request,
        IAuthService authService,
        CancellationToken ct)
    {
        var user = await authService.RegisterAsync(request, ct);
        return TypedResults.Created($"/users/{user.UserId}", user);
    }

    private static async Task<IResult> Login(
        LoginRequest request,
        IAuthService authService,
        CancellationToken ct)
    {
        var response = await authService.LoginAsync(request, ct);
        return TypedResults.Ok(response);
    }

    private static async Task<IResult> Refresh(
        RefreshRequest request,
        IAuthService authService,
        CancellationToken ct)
    {
        var response = await authService.RefreshAsync(request, ct);
        return TypedResults.Ok(response);
    }

    private static async Task<IResult> Logout(
        ClaimsPrincipal user,
        IAuthService authService,
        CancellationToken ct)
    {
        var userId = user.FindFirstValue(ClaimTypes.NameIdentifier);
        await authService.LogoutAsync(userId!, ct);
        return TypedResults.NoContent();
    }
}
```

### 4. Register in Program.cs

```csharp
// Register services
builder.Services.AddScoped<IAuthService, AuthService>();

// Map endpoints (after app.Build())
app.MapAuthEndpoints();
```

## Error Handling

Return RFC 7807 Problem Details for auth errors:

```csharp
public static IResult InvalidCredentials() =>
    TypedResults.Problem(
        title: "Invalid Credentials",
        detail: "The email or password provided is incorrect.",
        statusCode: StatusCodes.Status401Unauthorized,
        type: "https://novatune.example/errors/invalid-credentials");

public static IResult AccountDisabled() =>
    TypedResults.Problem(
        title: "Account Disabled",
        detail: "This account has been disabled.",
        statusCode: StatusCodes.Status403Forbidden,
        type: "https://novatune.example/errors/account-disabled");

public static IResult EmailExists() =>
    TypedResults.Problem(
        title: "Email Already Registered",
        detail: "An account with this email already exists.",
        statusCode: StatusCodes.Status409Conflict,
        type: "https://novatune.example/errors/email-exists");
```

## Rate Limiting

Apply rate limiting to auth endpoints:

```csharp
group.MapPost("/login", Login)
    .RequireRateLimiting("auth-login");  // 10/min per IP, 5/min per account

group.MapPost("/register", Register)
    .RequireRateLimiting("auth-register");  // 10/min per IP
```

## Testing

- Unit tests: `src/unit_tests/AuthServiceTests.cs`
- Integration tests: `src/integration_tests/.../AuthEndpointsTests.cs`

Key test scenarios:
- Successful registration creates user with Active status
- Login returns JWT with correct claims
- Refresh rotates tokens and invalidates old one
- Logout revokes only current session
- Disabled user cannot login (403)
- Rate limit returns 429 with Retry-After header