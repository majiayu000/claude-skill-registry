---
name: dotnet-csharp
description: "Build .NET 8+ applications with C#. Covers ASP.NET Core, Minimal APIs, Entity Framework Core, dependency injection, and testing. Use for .NET development, C# programming, and Azure backend services."
---

# .NET & C# Development Skill

> Expert guidance for building modern .NET 8+ applications with C#, ASP.NET Core, Entity Framework Core, and best practices.

## Triggers

Use this skill when:
- Building .NET 8+ applications with C#
- Creating ASP.NET Core Web APIs or MVC applications
- Working with Minimal APIs for lightweight endpoints
- Implementing Entity Framework Core for data access
- Setting up dependency injection and service registration
- Configuring authentication and authorization (JWT, policies)
- Writing background services and hosted services
- Testing with xUnit, NUnit, Moq, and FluentAssertions
- Keywords: dotnet, csharp, asp.net core, minimal api, entity framework, ef core, dependency injection, jwt authentication, xunit, nuget

---

## Quick Reference

### .NET CLI Commands

| Command                           | Description                |
| --------------------------------- | -------------------------- |
| `dotnet new webapi`               | Create new Web API project |
| `dotnet new mvc`                  | Create new MVC project     |
| `dotnet new classlib`             | Create class library       |
| `dotnet new xunit`                | Create xUnit test project  |
| `dotnet build`                    | Build the project          |
| `dotnet run`                      | Run the application        |
| `dotnet test`                     | Run tests                  |
| `dotnet publish -c Release`       | Publish for deployment     |
| `dotnet ef migrations add <Name>` | Create EF migration        |
| `dotnet ef database update`       | Apply migrations           |

### Project Templates

| Template       | Use Case                                  |
| -------------- | ----------------------------------------- |
| `webapi`       | REST API with controllers or minimal APIs |
| `web`          | Empty ASP.NET Core project                |
| `mvc`          | MVC web application                       |
| `razor`        | Razor Pages application                   |
| `blazorserver` | Blazor Server app                         |
| `blazorwasm`   | Blazor WebAssembly app                    |
| `worker`       | Background service                        |
| `grpc`         | gRPC service                              |

### C# 12 Features (.NET 8+)

| Feature                   | Example                                             |
| ------------------------- | --------------------------------------------------- |
| Primary Constructors      | `class Person(string name, int age)`                |
| Collection Expressions    | `int[] nums = [1, 2, 3];`                           |
| Alias Any Type            | `using Point = (int X, int Y);`                     |
| Default Lambda Parameters | `var add = (int a, int b = 1) => a + b;`            |
| Inline Arrays             | `[InlineArray(10)] struct Buffer { int _element; }` |

---

## Project Setup

### Solution Structure

```
MySolution/
├── src/
│   ├── MyApp.Api/              # Web API project
│   │   ├── Controllers/
│   │   ├── Endpoints/          # Minimal API endpoints
│   │   ├── Middleware/
│   │   ├── Program.cs
│   │   └── appsettings.json
│   ├── MyApp.Core/             # Domain/business logic
│   │   ├── Entities/
│   │   ├── Interfaces/
│   │   └── Services/
│   ├── MyApp.Infrastructure/   # Data access, external services
│   │   ├── Data/
│   │   ├── Repositories/
│   │   └── Services/
│   └── MyApp.Shared/           # Shared DTOs, utilities
│       ├── DTOs/
│       └── Extensions/
├── tests/
│   ├── MyApp.UnitTests/
│   ├── MyApp.IntegrationTests/
│   └── MyApp.FunctionalTests/
├── Directory.Build.props       # Shared build properties
├── Directory.Packages.props    # Central package management
└── MySolution.sln
```

### Directory.Build.props

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
  </PropertyGroup>
</Project>
```

### Central Package Management (Directory.Packages.props)

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <PackageVersion Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
    <PackageVersion Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />
    <PackageVersion Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageVersion Include="FluentValidation" Version="11.9.0" />
    <PackageVersion Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageVersion Include="xunit" Version="2.6.4" />
    <PackageVersion Include="Moq" Version="4.20.70" />
  </ItemGroup>
</Project>
```

---

## ASP.NET Core

### Program.cs (Modern Setup)

```csharp
using MyApp.Api.Middleware;
using MyApp.Core.Interfaces;
using MyApp.Infrastructure.Data;
using MyApp.Infrastructure.Services;

var builder = WebApplication.CreateBuilder(args);

// Configuration
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true)
    .AddEnvironmentVariables()
    .AddUserSecrets<Program>(optional: true);

// Services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Database
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Application services
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddScoped<IEmailService, EmailService>();

// Health checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>();

var app = builder.Build();

// Middleware pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthentication();
app.UseAuthorization();

app.UseMiddleware<ExceptionHandlingMiddleware>();

app.MapControllers();
app.MapHealthChecks("/health");

app.Run();

// Make Program class accessible for integration tests
public partial class Program { }
```

### Controller Pattern

```csharp
using Microsoft.AspNetCore.Mvc;

namespace MyApp.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUserService userService, ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    /// <summary>
    /// Gets all users with optional filtering
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<UserDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers(
        [FromQuery] string? search = null,
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        CancellationToken cancellationToken = default)
    {
        var users = await _userService.GetUsersAsync(search, page, pageSize, cancellationToken);
        return Ok(users);
    }

    /// <summary>
    /// Gets a specific user by ID
    /// </summary>
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<UserDto>> GetUser(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        var user = await _userService.GetByIdAsync(id, cancellationToken);

        if (user is null)
        {
            return NotFound();
        }

        return Ok(user);
    }

    /// <summary>
    /// Creates a new user
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<UserDto>> CreateUser(
        [FromBody] CreateUserRequest request,
        CancellationToken cancellationToken = default)
    {
        var user = await _userService.CreateAsync(request, cancellationToken);

        _logger.LogInformation("Created user {UserId}", user.Id);

        return CreatedAtAction(
            nameof(GetUser),
            new { id = user.Id },
            user);
    }

    /// <summary>
    /// Updates an existing user
    /// </summary>
    [HttpPut("{id:guid}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<UserDto>> UpdateUser(
        Guid id,
        [FromBody] UpdateUserRequest request,
        CancellationToken cancellationToken = default)
    {
        var user = await _userService.UpdateAsync(id, request, cancellationToken);

        if (user is null)
        {
            return NotFound();
        }

        return Ok(user);
    }

    /// <summary>
    /// Deletes a user
    /// </summary>
    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> DeleteUser(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        var deleted = await _userService.DeleteAsync(id, cancellationToken);

        if (!deleted)
        {
            return NotFound();
        }

        return NoContent();
    }
}
```

---

## Minimal APIs

### Basic Setup

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddScoped<IUserService, UserService>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// Map endpoints
app.MapUserEndpoints();
app.MapProductEndpoints();

app.Run();
```

### Organized Endpoints

```csharp
namespace MyApp.Api.Endpoints;

public static class UserEndpoints
{
    public static void MapUserEndpoints(this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/users")
            .WithTags("Users")
            .WithOpenApi();

        group.MapGet("/", GetUsers)
            .WithName("GetUsers")
            .WithSummary("Gets all users");

        group.MapGet("/{id:guid}", GetUserById)
            .WithName("GetUserById")
            .WithSummary("Gets a user by ID");

        group.MapPost("/", CreateUser)
            .WithName("CreateUser")
            .WithSummary("Creates a new user")
            .AddEndpointFilter<ValidationFilter<CreateUserRequest>>();

        group.MapPut("/{id:guid}", UpdateUser)
            .WithName("UpdateUser")
            .RequireAuthorization();

        group.MapDelete("/{id:guid}", DeleteUser)
            .WithName("DeleteUser")
            .RequireAuthorization("AdminOnly");
    }

    private static async Task<IResult> GetUsers(
        IUserService userService,
        [AsParameters] PaginationQuery pagination,
        CancellationToken cancellationToken)
    {
        var users = await userService.GetUsersAsync(
            pagination.Page,
            pagination.PageSize,
            cancellationToken);

        return Results.Ok(users);
    }

    private static async Task<IResult> GetUserById(
        Guid id,
        IUserService userService,
        CancellationToken cancellationToken)
    {
        var user = await userService.GetByIdAsync(id, cancellationToken);

        return user is null
            ? Results.NotFound()
            : Results.Ok(user);
    }

    private static async Task<IResult> CreateUser(
        CreateUserRequest request,
        IUserService userService,
        CancellationToken cancellationToken)
    {
        var user = await userService.CreateAsync(request, cancellationToken);

        return Results.CreatedAtRoute(
            "GetUserById",
            new { id = user.Id },
            user);
    }

    private static async Task<IResult> UpdateUser(
        Guid id,
        UpdateUserRequest request,
        IUserService userService,
        CancellationToken cancellationToken)
    {
        var user = await userService.UpdateAsync(id, request, cancellationToken);

        return user is null
            ? Results.NotFound()
            : Results.Ok(user);
    }

    private static async Task<IResult> DeleteUser(
        Guid id,
        IUserService userService,
        CancellationToken cancellationToken)
    {
        var deleted = await userService.DeleteAsync(id, cancellationToken);

        return deleted
            ? Results.NoContent()
            : Results.NotFound();
    }
}

// Parameter binding class
public record PaginationQuery(
    [FromQuery] int Page = 1,
    [FromQuery] int PageSize = 10);
```

### Typed Results (Better OpenAPI)

```csharp
public static class UserEndpoints
{
    public static void MapUserEndpoints(this IEndpointRouteBuilder routes)
    {
        routes.MapGet("/api/users/{id:guid}", GetUserById);
    }

    private static async Task<Results<Ok<UserDto>, NotFound>> GetUserById(
        Guid id,
        IUserService userService,
        CancellationToken cancellationToken)
    {
        var user = await userService.GetByIdAsync(id, cancellationToken);

        return user is null
            ? TypedResults.NotFound()
            : TypedResults.Ok(user);
    }
}
```

---

## Entity Framework Core

### DbContext

```csharp
using Microsoft.EntityFrameworkCore;

namespace MyApp.Infrastructure.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    public DbSet<User> Users => Set<User>();
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(AppDbContext).Assembly);

        // Global query filters
        modelBuilder.Entity<User>()
            .HasQueryFilter(u => !u.IsDeleted);

        base.OnModelCreating(modelBuilder);
    }

    public override async Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default)
    {
        // Audit trail
        foreach (var entry in ChangeTracker.Entries<IAuditable>())
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    entry.Entity.CreatedAt = DateTime.UtcNow;
                    break;
                case EntityState.Modified:
                    entry.Entity.UpdatedAt = DateTime.UtcNow;
                    break;
            }
        }

        return await base.SaveChangesAsync(cancellationToken);
    }
}
```

### Entity Configuration

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace MyApp.Infrastructure.Data.Configurations;

public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("Users");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Id)
            .ValueGeneratedOnAdd();

        builder.Property(u => u.Email)
            .IsRequired()
            .HasMaxLength(256);

        builder.Property(u => u.FirstName)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(u => u.LastName)
            .IsRequired()
            .HasMaxLength(100);

        builder.Property(u => u.PasswordHash)
            .IsRequired();

        // Indexes
        builder.HasIndex(u => u.Email)
            .IsUnique();

        // Relationships
        builder.HasMany(u => u.Orders)
            .WithOne(o => o.User)
            .HasForeignKey(o => o.UserId)
            .OnDelete(DeleteBehavior.Cascade);

        // Value objects
        builder.OwnsOne(u => u.Address, address =>
        {
            address.Property(a => a.Street).HasMaxLength(200);
            address.Property(a => a.City).HasMaxLength(100);
            address.Property(a => a.ZipCode).HasMaxLength(20);
            address.Property(a => a.Country).HasMaxLength(100);
        });

        // Seed data
        builder.HasData(
            new User
            {
                Id = Guid.Parse("11111111-1111-1111-1111-111111111111"),
                Email = "admin@example.com",
                FirstName = "Admin",
                LastName = "User"
            });
    }
}
```

### Repository Pattern

```csharp
namespace MyApp.Core.Interfaces;

public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<T>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<T> AddAsync(T entity, CancellationToken cancellationToken = default);
    Task UpdateAsync(T entity, CancellationToken cancellationToken = default);
    Task DeleteAsync(T entity, CancellationToken cancellationToken = default);
}

public interface IUserRepository : IRepository<User>
{
    Task<User?> GetByEmailAsync(string email, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<User>> GetActiveUsersAsync(CancellationToken cancellationToken = default);
}
```

```csharp
namespace MyApp.Infrastructure.Repositories;

public class Repository<T> : IRepository<T> where T : class
{
    protected readonly AppDbContext _context;
    protected readonly DbSet<T> _dbSet;

    public Repository(AppDbContext context)
    {
        _context = context;
        _dbSet = context.Set<T>();
    }

    public virtual async Task<T?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        return await _dbSet.FindAsync([id], cancellationToken);
    }

    public virtual async Task<IReadOnlyList<T>> GetAllAsync(
        CancellationToken cancellationToken = default)
    {
        return await _dbSet.ToListAsync(cancellationToken);
    }

    public virtual async Task<T> AddAsync(
        T entity,
        CancellationToken cancellationToken = default)
    {
        await _dbSet.AddAsync(entity, cancellationToken);
        await _context.SaveChangesAsync(cancellationToken);
        return entity;
    }

    public virtual async Task UpdateAsync(
        T entity,
        CancellationToken cancellationToken = default)
    {
        _dbSet.Update(entity);
        await _context.SaveChangesAsync(cancellationToken);
    }

    public virtual async Task DeleteAsync(
        T entity,
        CancellationToken cancellationToken = default)
    {
        _dbSet.Remove(entity);
        await _context.SaveChangesAsync(cancellationToken);
    }
}

public class UserRepository : Repository<User>, IUserRepository
{
    public UserRepository(AppDbContext context) : base(context)
    {
    }

    public async Task<User?> GetByEmailAsync(
        string email,
        CancellationToken cancellationToken = default)
    {
        return await _dbSet
            .FirstOrDefaultAsync(u => u.Email == email, cancellationToken);
    }

    public async Task<IReadOnlyList<User>> GetActiveUsersAsync(
        CancellationToken cancellationToken = default)
    {
        return await _dbSet
            .Where(u => u.IsActive)
            .OrderBy(u => u.LastName)
            .ThenBy(u => u.FirstName)
            .ToListAsync(cancellationToken);
    }
}
```

---

## Dependency Injection

### Service Registration

```csharp
namespace MyApp.Api.Extensions;

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(
        this IServiceCollection services)
    {
        // Transient - new instance every time
        services.AddTransient<IEmailService, EmailService>();

        // Scoped - one instance per request
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<IOrderService, OrderService>();
        services.AddScoped(typeof(IRepository<>), typeof(Repository<>));

        // Singleton - one instance for app lifetime
        services.AddSingleton<ICacheService, MemoryCacheService>();

        return services;
    }

    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Database
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlServer(
                configuration.GetConnectionString("DefaultConnection"),
                sqlOptions =>
                {
                    sqlOptions.EnableRetryOnFailure(
                        maxRetryCount: 3,
                        maxRetryDelay: TimeSpan.FromSeconds(30),
                        errorNumbersToAdd: null);
                    sqlOptions.CommandTimeout(30);
                }));

        // Repositories
        services.AddScoped<IUserRepository, UserRepository>();
        services.AddScoped<IOrderRepository, OrderRepository>();

        // HTTP clients
        services.AddHttpClient<IExternalApiClient, ExternalApiClient>(client =>
        {
            client.BaseAddress = new Uri(configuration["ExternalApi:BaseUrl"]!);
            client.Timeout = TimeSpan.FromSeconds(30);
        })
        .AddPolicyHandler(GetRetryPolicy())
        .AddPolicyHandler(GetCircuitBreakerPolicy());

        return services;
    }

    private static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy()
    {
        return HttpPolicyExtensions
            .HandleTransientHttpError()
            .WaitAndRetryAsync(3, retryAttempt =>
                TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
    }

    private static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy()
    {
        return HttpPolicyExtensions
            .HandleTransientHttpError()
            .CircuitBreakerAsync(5, TimeSpan.FromSeconds(30));
    }
}
```

### Keyed Services (.NET 8+)

```csharp
// Registration
services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");
services.AddKeyedScoped<INotificationService, PushNotificationService>("push");

// Injection
public class NotificationController : ControllerBase
{
    public NotificationController(
        [FromKeyedServices("email")] INotificationService emailService,
        [FromKeyedServices("sms")] INotificationService smsService)
    {
        // Use specific implementations
    }
}
```

---

## Authentication & Authorization

### JWT Authentication

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

public static class AuthenticationExtensions
{
    public static IServiceCollection AddJwtAuthentication(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var jwtOptions = configuration
            .GetSection(JwtOptions.SectionName)
            .Get<JwtOptions>()!;

        services.AddAuthentication(options =>
        {
            options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
            options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
        })
        .AddJwtBearer(options =>
        {
            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,
                ValidIssuer = jwtOptions.Issuer,
                ValidAudience = jwtOptions.Audience,
                IssuerSigningKey = new SymmetricSecurityKey(
                    Encoding.UTF8.GetBytes(jwtOptions.Secret)),
                ClockSkew = TimeSpan.Zero
            };

            options.Events = new JwtBearerEvents
            {
                OnAuthenticationFailed = context =>
                {
                    if (context.Exception is SecurityTokenExpiredException)
                    {
                        context.Response.Headers.Append(
                            "Token-Expired", "true");
                    }
                    return Task.CompletedTask;
                }
            };
        });

        return services;
    }
}
```

### Token Service

```csharp
public interface ITokenService
{
    string GenerateAccessToken(User user);
    string GenerateRefreshToken();
    ClaimsPrincipal? ValidateToken(string token);
}

public class TokenService : ITokenService
{
    private readonly JwtOptions _options;

    public TokenService(IOptions<JwtOptions> options)
    {
        _options = options.Value;
    }

    public string GenerateAccessToken(User user)
    {
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id.ToString()),
            new(ClaimTypes.Email, user.Email),
            new(ClaimTypes.Name, $"{user.FirstName} {user.LastName}"),
            new("role", user.Role.ToString())
        };

        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_options.Secret));
        var credentials = new SigningCredentials(
            key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: _options.Issuer,
            audience: _options.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_options.ExpirationMinutes),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    public string GenerateRefreshToken()
    {
        var randomBytes = new byte[64];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomBytes);
        return Convert.ToBase64String(randomBytes);
    }

    public ClaimsPrincipal? ValidateToken(string token)
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.UTF8.GetBytes(_options.Secret);

        try
        {
            return tokenHandler.ValidateToken(token,
                new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(key),
                    ValidateIssuer = true,
                    ValidIssuer = _options.Issuer,
                    ValidateAudience = true,
                    ValidAudience = _options.Audience,
                    ValidateLifetime = false // Allow expired tokens for refresh
                }, out _);
        }
        catch
        {
            return null;
        }
    }
}
```

### Authorization Policies

```csharp
public static class AuthorizationExtensions
{
    public static IServiceCollection AddAuthorizationPolicies(
        this IServiceCollection services)
    {
        services.AddAuthorization(options =>
        {
            // Role-based policies
            options.AddPolicy("AdminOnly", policy =>
                policy.RequireRole("Admin"));

            options.AddPolicy("ManagerOrAdmin", policy =>
                policy.RequireRole("Manager", "Admin"));

            // Claim-based policies
            options.AddPolicy("VerifiedEmail", policy =>
                policy.RequireClaim("email_verified", "true"));

            // Custom requirement policies
            options.AddPolicy("MinimumAge", policy =>
                policy.AddRequirements(new MinimumAgeRequirement(18)));

            // Resource-based authorization
            options.AddPolicy("OwnerOnly", policy =>
                policy.AddRequirements(new ResourceOwnerRequirement()));

            // Combined policies
            options.AddPolicy("PremiumFeature", policy =>
                policy.RequireRole("Premium", "Admin")
                      .RequireClaim("subscription_active", "true"));
        });

        // Register handlers
        services.AddScoped<IAuthorizationHandler, MinimumAgeHandler>();
        services.AddScoped<IAuthorizationHandler, ResourceOwnerHandler>();

        return services;
    }
}
```

---

## Background Services

### Hosted Service

```csharp
namespace MyApp.Api.Services;

public class CleanupBackgroundService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<CleanupBackgroundService> _logger;
    private readonly TimeSpan _period = TimeSpan.FromHours(1);

    public CleanupBackgroundService(
        IServiceScopeFactory scopeFactory,
        ILogger<CleanupBackgroundService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Cleanup service starting");

        using var timer = new PeriodicTimer(_period);

        while (!stoppingToken.IsCancellationRequested &&
               await timer.WaitForNextTickAsync(stoppingToken))
        {
            try
            {
                await DoCleanupAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during cleanup");
            }
        }
    }

    private async Task DoCleanupAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Starting cleanup task");

        using var scope = _scopeFactory.CreateScope();
        var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        var cutoffDate = DateTime.UtcNow.AddDays(-30);

        var deletedCount = await dbContext.AuditLogs
            .Where(l => l.CreatedAt < cutoffDate)
            .ExecuteDeleteAsync(stoppingToken);

        _logger.LogInformation("Deleted {Count} old audit logs", deletedCount);
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Cleanup service stopping");
        await base.StopAsync(cancellationToken);
    }
}

// Registration
services.AddHostedService<CleanupBackgroundService>();
```

---

## Testing

### Unit Test Structure (xUnit)

```csharp
using Xunit;
using Moq;
using FluentAssertions;

namespace MyApp.UnitTests.Services;

public class UserServiceTests
{
    private readonly Mock<IUserRepository> _userRepositoryMock;
    private readonly Mock<IEmailService> _emailServiceMock;
    private readonly Mock<ILogger<UserService>> _loggerMock;
    private readonly UserService _sut; // System Under Test

    public UserServiceTests()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _emailServiceMock = new Mock<IEmailService>();
        _loggerMock = new Mock<ILogger<UserService>>();

        _sut = new UserService(
            _userRepositoryMock.Object,
            _emailServiceMock.Object,
            _loggerMock.Object);
    }

    [Fact]
    public async Task GetByIdAsync_WithValidId_ReturnsUser()
    {
        // Arrange
        var userId = Guid.NewGuid();
        var expectedUser = new User
        {
            Id = userId,
            Email = "test@example.com",
            FirstName = "John",
            LastName = "Doe"
        };

        _userRepositoryMock
            .Setup(r => r.GetByIdAsync(userId, It.IsAny<CancellationToken>()))
            .ReturnsAsync(expectedUser);

        // Act
        var result = await _sut.GetByIdAsync(userId);

        // Assert
        result.Should().NotBeNull();
        result!.Id.Should().Be(userId);
        result.Email.Should().Be("test@example.com");

        _userRepositoryMock.Verify(
            r => r.GetByIdAsync(userId, It.IsAny<CancellationToken>()),
            Times.Once);
    }

    [Fact]
    public async Task GetByIdAsync_WithInvalidId_ReturnsNull()
    {
        // Arrange
        var userId = Guid.NewGuid();

        _userRepositoryMock
            .Setup(r => r.GetByIdAsync(userId, It.IsAny<CancellationToken>()))
            .ReturnsAsync((User?)null);

        // Act
        var result = await _sut.GetByIdAsync(userId);

        // Assert
        result.Should().BeNull();
    }

    [Theory]
    [InlineData("")]
    [InlineData(" ")]
    [InlineData(null)]
    public async Task CreateAsync_WithInvalidEmail_ThrowsValidationException(
        string? email)
    {
        // Arrange
        var request = new CreateUserRequest
        {
            Email = email!,
            FirstName = "John",
            LastName = "Doe"
        };

        // Act
        var act = () => _sut.CreateAsync(request);

        // Assert
        await act.Should().ThrowAsync<ValidationException>()
            .WithMessage("*email*");
    }

    [Fact]
    public async Task CreateAsync_WithValidRequest_SendsWelcomeEmail()
    {
        // Arrange
        var request = new CreateUserRequest
        {
            Email = "test@example.com",
            FirstName = "John",
            LastName = "Doe"
        };

        _userRepositoryMock
            .Setup(r => r.AddAsync(It.IsAny<User>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync((User u, CancellationToken _) => u);

        // Act
        await _sut.CreateAsync(request);

        // Assert
        _emailServiceMock.Verify(
            e => e.SendWelcomeEmailAsync(
                request.Email,
                It.IsAny<CancellationToken>()),
            Times.Once);
    }
}
```

### Integration Tests with WebApplicationFactory

```csharp
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace MyApp.IntegrationTests;

public class CustomWebApplicationFactory<TProgram>
    : WebApplicationFactory<TProgram> where TProgram : class
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // Remove existing DbContext registration
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));

            if (descriptor != null)
            {
                services.Remove(descriptor);
            }

            // Add in-memory database
            services.AddDbContext<AppDbContext>(options =>
            {
                options.UseInMemoryDatabase("TestDb");
            });

            // Replace external services with mocks
            services.AddScoped<IEmailService, FakeEmailService>();

            // Build service provider and ensure database is created
            var sp = services.BuildServiceProvider();
            using var scope = sp.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            db.Database.EnsureCreated();

            // Seed test data
            SeedTestData(db);
        });

        builder.UseEnvironment("Testing");
    }

    private static void SeedTestData(AppDbContext context)
    {
        context.Users.AddRange(
            new User
            {
                Id = Guid.Parse("11111111-1111-1111-1111-111111111111"),
                Email = "admin@test.com",
                FirstName = "Admin",
                LastName = "User"
            },
            new User
            {
                Id = Guid.Parse("22222222-2222-2222-2222-222222222222"),
                Email = "user@test.com",
                FirstName = "Regular",
                LastName = "User"
            });

        context.SaveChanges();
    }
}

public class UsersControllerTests : IClassFixture<CustomWebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly CustomWebApplicationFactory<Program> _factory;

    public UsersControllerTests(CustomWebApplicationFactory<Program> factory)
    {
        _factory = factory;
        _client = factory.CreateClient(new WebApplicationFactoryClientOptions
        {
            AllowAutoRedirect = false
        });
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessAndUsers()
    {
        // Act
        var response = await _client.GetAsync("/api/users");

        // Assert
        response.EnsureSuccessStatusCode();

        var users = await response.Content
            .ReadFromJsonAsync<IEnumerable<UserDto>>();

        users.Should().NotBeNull();
        users.Should().HaveCountGreaterThan(0);
    }

    [Fact]
    public async Task GetUserById_WithValidId_ReturnsUser()
    {
        // Arrange
        var userId = "11111111-1111-1111-1111-111111111111";

        // Act
        var response = await _client.GetAsync($"/api/users/{userId}");

        // Assert
        response.EnsureSuccessStatusCode();

        var user = await response.Content.ReadFromJsonAsync<UserDto>();

        user.Should().NotBeNull();
        user!.Email.Should().Be("admin@test.com");
    }

    [Fact]
    public async Task GetUserById_WithInvalidId_ReturnsNotFound()
    {
        // Arrange
        var userId = Guid.NewGuid();

        // Act
        var response = await _client.GetAsync($"/api/users/{userId}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.NotFound);
    }
}
```

---

## Best Practices

### Code Organization

| Practice           | Description                                               |
| ------------------ | --------------------------------------------------------- |
| Clean Architecture | Separate concerns into layers (Core, Infrastructure, API) |
| Vertical Slices    | Organize by feature for complex applications              |
| SOLID Principles   | Single responsibility, dependency injection, etc.         |
| DTOs               | Never expose entities directly to API responses           |

### Performance

| Practice                  | Description                           |
| ------------------------- | ------------------------------------- |
| Async/Await               | Use async for I/O operations          |
| CancellationToken         | Pass through all async chains         |
| IQueryable vs IEnumerable | Filter at database level              |
| Compiled Queries          | For frequently executed queries       |
| Caching                   | Use IMemoryCache or IDistributedCache |

### Security

| Practice              | Description                         |
| --------------------- | ----------------------------------- |
| Input Validation      | Validate all user input             |
| Parameterized Queries | Prevent SQL injection               |
| HTTPS                 | Always use HTTPS in production      |
| Secrets Management    | Use User Secrets/Key Vault          |
| CORS                  | Configure properly for your domains |

### Error Handling

```csharp
// Custom exception types
public class NotFoundException : Exception
{
    public NotFoundException(string message) : base(message) { }
    public NotFoundException(string name, object key)
        : base($"Entity \"{name}\" ({key}) was not found.") { }
}

public class ValidationException : Exception
{
    public IReadOnlyList<string> Errors { get; }

    public ValidationException(IEnumerable<string> errors)
        : base("One or more validation errors occurred.")
    {
        Errors = errors.ToList();
    }
}

public class ForbiddenException : Exception
{
    public ForbiddenException(string message = "Access denied")
        : base(message) { }
}
```

### Logging Best Practices

```csharp
// Structured logging with semantic values
_logger.LogInformation(
    "User {UserId} created order {OrderId} for {Amount:C}",
    userId, orderId, amount);

// Log levels
_logger.LogTrace("Detailed debugging info");
_logger.LogDebug("Debugging info");
_logger.LogInformation("General info");
_logger.LogWarning("Something unexpected but not an error");
_logger.LogError(ex, "An error occurred");
_logger.LogCritical(ex, "A critical failure");

// Scopes for correlation
using (_logger.BeginScope(new Dictionary<string, object>
{
    ["UserId"] = userId,
    ["OrderId"] = orderId
}))
{
    _logger.LogInformation("Processing order");
    // All logs within scope include UserId and OrderId
}
```

### Health Checks

```csharp
services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>("database")
    .AddRedis(connectionString, "redis")
    .AddUrlGroup(new Uri("https://api.example.com/health"), "external-api")
    .AddCheck<CustomHealthCheck>("custom");

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // Just returns healthy if app is running
});
```

---

## Additional Resources

- [.NET Documentation](https://docs.microsoft.com/dotnet/)
- [ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core/)
- [EF Core Documentation](https://docs.microsoft.com/ef/core/)
- [C# Language Reference](https://docs.microsoft.com/dotnet/csharp/)
- [.NET Architecture Guides](https://dotnet.microsoft.com/learn/aspnet/architecture)

---

> **Note**: This skill covers .NET 8+ patterns and best practices. For earlier versions, some features may not be available.
