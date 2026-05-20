---
name: dotnet-csharp
description: "Build .NET 8+ applications with C#. Covers ASP.NET Core, Minimal APIs, Entity Framework Core, dependency injection, and testing. Use for .NET development, C# programming, and Azure backend services."
---

# .NET & C# Development Skill

> Expert guidance for building modern .NET 8+ applications with C#, ASP.NET Core, Entity Framework Core, and best practices.

---

## 📑 Table of Contents

- [Quick Reference](#-quick-reference)
- [Project Setup](#-project-setup)
- [ASP.NET Core](#-aspnet-core)
- [Minimal APIs](#-minimal-apis)
- [Entity Framework Core](#-entity-framework-core)
- [Dependency Injection](#-dependency-injection)
- [Configuration & Options](#-configuration--options)
- [Middleware & Filters](#-middleware--filters)
- [Authentication & Authorization](#-authentication--authorization)
- [Background Services](#-background-services)
- [Testing](#-testing)
- [Common Patterns](#-common-patterns)
- [Best Practices](#-best-practices)

---

## 📋 Quick Reference

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

## 🚀 Project Setup

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

## 🌐 ASP.NET Core

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

## ⚡ Minimal APIs

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

## 🗄️ Entity Framework Core

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

### Specification Pattern

```csharp
namespace MyApp.Core.Specifications;

public abstract class Specification<T>
{
    public abstract Expression<Func<T, bool>> ToExpression();

    public bool IsSatisfiedBy(T entity)
    {
        var predicate = ToExpression().Compile();
        return predicate(entity);
    }

    public Specification<T> And(Specification<T> specification)
    {
        return new AndSpecification<T>(this, specification);
    }

    public Specification<T> Or(Specification<T> specification)
    {
        return new OrSpecification<T>(this, specification);
    }
}

public class ActiveUserSpecification : Specification<User>
{
    public override Expression<Func<User, bool>> ToExpression()
    {
        return user => user.IsActive && !user.IsDeleted;
    }
}

public class UserByEmailSpecification : Specification<User>
{
    private readonly string _email;

    public UserByEmailSpecification(string email)
    {
        _email = email;
    }

    public override Expression<Func<User, bool>> ToExpression()
    {
        return user => user.Email == _email;
    }
}
```

---

## 💉 Dependency Injection

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

### Factory Pattern

```csharp
public interface IPaymentProcessorFactory
{
    IPaymentProcessor Create(PaymentMethod method);
}

public class PaymentProcessorFactory : IPaymentProcessorFactory
{
    private readonly IServiceProvider _serviceProvider;

    public PaymentProcessorFactory(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public IPaymentProcessor Create(PaymentMethod method)
    {
        return method switch
        {
            PaymentMethod.CreditCard => _serviceProvider
                .GetRequiredService<CreditCardProcessor>(),
            PaymentMethod.PayPal => _serviceProvider
                .GetRequiredService<PayPalProcessor>(),
            PaymentMethod.BankTransfer => _serviceProvider
                .GetRequiredService<BankTransferProcessor>(),
            _ => throw new ArgumentException($"Unknown payment method: {method}")
        };
    }
}

// Registration
services.AddScoped<IPaymentProcessorFactory, PaymentProcessorFactory>();
services.AddScoped<CreditCardProcessor>();
services.AddScoped<PayPalProcessor>();
services.AddScoped<BankTransferProcessor>();
```

---

## ⚙️ Configuration & Options

### appsettings.json Structure

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Trusted_Connection=true;",
    "Redis": "localhost:6379"
  },
  "Jwt": {
    "Secret": "your-secret-key-here",
    "Issuer": "MyApp",
    "Audience": "MyApp",
    "ExpirationMinutes": 60
  },
  "Email": {
    "SmtpServer": "smtp.example.com",
    "Port": 587,
    "UseSsl": true,
    "FromAddress": "noreply@example.com",
    "FromName": "MyApp"
  },
  "Features": {
    "EnableNewDashboard": true,
    "MaxUploadSizeMb": 10
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  }
}
```

### Options Pattern

```csharp
namespace MyApp.Core.Options;

public class JwtOptions
{
    public const string SectionName = "Jwt";

    public string Secret { get; set; } = string.Empty;
    public string Issuer { get; set; } = string.Empty;
    public string Audience { get; set; } = string.Empty;
    public int ExpirationMinutes { get; set; } = 60;
}

public class EmailOptions
{
    public const string SectionName = "Email";

    public string SmtpServer { get; set; } = string.Empty;
    public int Port { get; set; } = 587;
    public bool UseSsl { get; set; } = true;
    public string FromAddress { get; set; } = string.Empty;
    public string FromName { get; set; } = string.Empty;
}
```

### Options Validation

```csharp
public class JwtOptionsValidator : IValidateOptions<JwtOptions>
{
    public ValidateOptionsResult Validate(string? name, JwtOptions options)
    {
        var failures = new List<string>();

        if (string.IsNullOrWhiteSpace(options.Secret))
        {
            failures.Add("JWT Secret is required");
        }
        else if (options.Secret.Length < 32)
        {
            failures.Add("JWT Secret must be at least 32 characters");
        }

        if (string.IsNullOrWhiteSpace(options.Issuer))
        {
            failures.Add("JWT Issuer is required");
        }

        if (options.ExpirationMinutes <= 0)
        {
            failures.Add("JWT ExpirationMinutes must be positive");
        }

        return failures.Count > 0
            ? ValidateOptionsResult.Fail(failures)
            : ValidateOptionsResult.Success;
    }
}

// Registration
services.AddOptions<JwtOptions>()
    .Bind(configuration.GetSection(JwtOptions.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart();

services.AddSingleton<IValidateOptions<JwtOptions>, JwtOptionsValidator>();
```

### Using Options

```csharp
public class TokenService : ITokenService
{
    private readonly JwtOptions _jwtOptions;

    // Use IOptions for singleton-scoped options
    public TokenService(IOptions<JwtOptions> jwtOptions)
    {
        _jwtOptions = jwtOptions.Value;
    }

    // Use IOptionsSnapshot for scoped options (reloads on change)
    public TokenService(IOptionsSnapshot<JwtOptions> jwtOptions)
    {
        _jwtOptions = jwtOptions.Value;
    }

    // Use IOptionsMonitor for singleton services that need to react to changes
    public TokenService(IOptionsMonitor<JwtOptions> jwtOptions)
    {
        _jwtOptions = jwtOptions.CurrentValue;
        jwtOptions.OnChange(newOptions =>
        {
            // React to configuration changes
        });
    }
}
```

---

## 🔧 Middleware & Filters

### Custom Middleware

```csharp
namespace MyApp.Api.Middleware;

public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(
        RequestDelegate next,
        ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }

    private async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        _logger.LogError(exception, "An unhandled exception occurred");

        var (statusCode, message) = exception switch
        {
            NotFoundException => (StatusCodes.Status404NotFound, exception.Message),
            ValidationException validationEx => (
                StatusCodes.Status400BadRequest,
                string.Join("; ", validationEx.Errors)),
            UnauthorizedAccessException => (
                StatusCodes.Status401Unauthorized,
                "Unauthorized"),
            ForbiddenException => (
                StatusCodes.Status403Forbidden,
                "Forbidden"),
            _ => (
                StatusCodes.Status500InternalServerError,
                "An error occurred processing your request")
        };

        context.Response.StatusCode = statusCode;
        context.Response.ContentType = "application/problem+json";

        var problemDetails = new ProblemDetails
        {
            Status = statusCode,
            Title = GetTitle(statusCode),
            Detail = message,
            Instance = context.Request.Path
        };

        await context.Response.WriteAsJsonAsync(problemDetails);
    }

    private static string GetTitle(int statusCode) => statusCode switch
    {
        400 => "Bad Request",
        401 => "Unauthorized",
        403 => "Forbidden",
        404 => "Not Found",
        _ => "Server Error"
    };
}

// Extension method
public static class MiddlewareExtensions
{
    public static IApplicationBuilder UseExceptionHandling(
        this IApplicationBuilder app)
    {
        return app.UseMiddleware<ExceptionHandlingMiddleware>();
    }
}
```

### Request Logging Middleware

```csharp
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();
        var requestId = Activity.Current?.Id ?? context.TraceIdentifier;

        _logger.LogInformation(
            "Request started: {Method} {Path} [{RequestId}]",
            context.Request.Method,
            context.Request.Path,
            requestId);

        try
        {
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();

            _logger.LogInformation(
                "Request completed: {Method} {Path} [{RequestId}] - {StatusCode} in {ElapsedMs}ms",
                context.Request.Method,
                context.Request.Path,
                requestId,
                context.Response.StatusCode,
                stopwatch.ElapsedMilliseconds);
        }
    }
}
```

### Action Filters

```csharp
namespace MyApp.Api.Filters;

public class ValidationFilter : IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(
        ActionExecutingContext context,
        ActionExecutionDelegate next)
    {
        if (!context.ModelState.IsValid)
        {
            var errors = context.ModelState
                .Where(x => x.Value?.Errors.Count > 0)
                .ToDictionary(
                    x => x.Key,
                    x => x.Value!.Errors.Select(e => e.ErrorMessage).ToArray());

            context.Result = new BadRequestObjectResult(
                new ValidationProblemDetails(context.ModelState));
            return;
        }

        await next();
    }
}

// Minimal API filter
public class ValidationFilter<T> : IEndpointFilter where T : class
{
    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var validator = context.HttpContext.RequestServices
            .GetService<IValidator<T>>();

        if (validator is null)
        {
            return await next(context);
        }

        var argument = context.Arguments
            .OfType<T>()
            .FirstOrDefault();

        if (argument is null)
        {
            return await next(context);
        }

        var validationResult = await validator.ValidateAsync(argument);

        if (!validationResult.IsValid)
        {
            return Results.ValidationProblem(
                validationResult.ToDictionary());
        }

        return await next(context);
    }
}
```

### Exception Filter

```csharp
public class GlobalExceptionFilter : IExceptionFilter
{
    private readonly ILogger<GlobalExceptionFilter> _logger;
    private readonly IHostEnvironment _environment;

    public GlobalExceptionFilter(
        ILogger<GlobalExceptionFilter> logger,
        IHostEnvironment environment)
    {
        _logger = logger;
        _environment = environment;
    }

    public void OnException(ExceptionContext context)
    {
        _logger.LogError(context.Exception, "Unhandled exception occurred");

        var problemDetails = new ProblemDetails
        {
            Status = StatusCodes.Status500InternalServerError,
            Title = "An error occurred",
            Detail = _environment.IsDevelopment()
                ? context.Exception.Message
                : "An error occurred processing your request"
        };

        context.Result = new ObjectResult(problemDetails)
        {
            StatusCode = StatusCodes.Status500InternalServerError
        };

        context.ExceptionHandled = true;
    }
}

// Registration
services.AddControllers(options =>
{
    options.Filters.Add<GlobalExceptionFilter>();
});
```

---

## 🔐 Authentication & Authorization

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

// Custom requirement
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public int MinimumAge { get; }

    public MinimumAgeRequirement(int minimumAge)
    {
        MinimumAge = minimumAge;
    }
}

// Custom handler
public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var birthDateClaim = context.User.FindFirst("birthdate");

        if (birthDateClaim is null)
        {
            return Task.CompletedTask;
        }

        if (DateTime.TryParse(birthDateClaim.Value, out var birthDate))
        {
            var age = DateTime.Today.Year - birthDate.Year;
            if (birthDate > DateTime.Today.AddYears(-age))
            {
                age--;
            }

            if (age >= requirement.MinimumAge)
            {
                context.Succeed(requirement);
            }
        }

        return Task.CompletedTask;
    }
}
```

### Resource-Based Authorization

```csharp
public class DocumentAuthorizationHandler :
    AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document resource)
    {
        var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);

        if (userId is null)
        {
            return Task.CompletedTask;
        }

        // Owner can do anything
        if (resource.OwnerId.ToString() == userId)
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        // Admins can do anything
        if (context.User.IsInRole("Admin"))
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        // Check specific operations for shared documents
        if (requirement.Name == Operations.Read.Name &&
            resource.SharedWith.Contains(Guid.Parse(userId)))
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}

// Usage in controller
public class DocumentsController : ControllerBase
{
    private readonly IAuthorizationService _authorizationService;

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(Guid id)
    {
        var document = await _documentService.GetByIdAsync(id);

        if (document is null)
        {
            return NotFound();
        }

        var authResult = await _authorizationService.AuthorizeAsync(
            User, document, Operations.Delete);

        if (!authResult.Succeeded)
        {
            return Forbid();
        }

        await _documentService.DeleteAsync(id);
        return NoContent();
    }
}
```

---

## ⚡ Background Services

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

### Queue Processing Service

```csharp
public class EmailQueueService : BackgroundService
{
    private readonly Channel<EmailMessage> _channel;
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<EmailQueueService> _logger;

    public EmailQueueService(
        Channel<EmailMessage> channel,
        IServiceScopeFactory scopeFactory,
        ILogger<EmailQueueService> logger)
    {
        _channel = channel;
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var message in _channel.Reader.ReadAllAsync(stoppingToken))
        {
            try
            {
                using var scope = _scopeFactory.CreateScope();
                var emailService = scope.ServiceProvider
                    .GetRequiredService<IEmailService>();

                await emailService.SendAsync(message, stoppingToken);

                _logger.LogInformation(
                    "Sent email to {Recipient}",
                    message.To);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,
                    "Failed to send email to {Recipient}",
                    message.To);
            }
        }
    }
}

// Channel setup
services.AddSingleton(Channel.CreateUnbounded<EmailMessage>(
    new UnboundedChannelOptions
    {
        SingleReader = true,
        SingleWriter = false
    }));

services.AddHostedService<EmailQueueService>();

// Producer service
public class EmailQueueProducer
{
    private readonly Channel<EmailMessage> _channel;

    public EmailQueueProducer(Channel<EmailMessage> channel)
    {
        _channel = channel;
    }

    public async Task QueueEmailAsync(EmailMessage message)
    {
        await _channel.Writer.WriteAsync(message);
    }
}
```

### Timed Background Service with Health Check

```csharp
public class HealthCheckBackgroundService : BackgroundService, IHealthCheck
{
    private volatile bool _isHealthy = true;
    private DateTime _lastSuccessfulRun = DateTime.UtcNow;
    private readonly TimeSpan _maxTimeBetweenRuns = TimeSpan.FromMinutes(5);

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await DoWorkAsync(stoppingToken);
                _lastSuccessfulRun = DateTime.UtcNow;
                _isHealthy = true;
            }
            catch (Exception)
            {
                _isHealthy = false;
            }

            await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
        }
    }

    private Task DoWorkAsync(CancellationToken stoppingToken)
    {
        // Work implementation
        return Task.CompletedTask;
    }

    public Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        if (!_isHealthy)
        {
            return Task.FromResult(HealthCheckResult.Unhealthy(
                "Background service is unhealthy"));
        }

        if (DateTime.UtcNow - _lastSuccessfulRun > _maxTimeBetweenRuns)
        {
            return Task.FromResult(HealthCheckResult.Degraded(
                $"Last successful run was {_lastSuccessfulRun}"));
        }

        return Task.FromResult(HealthCheckResult.Healthy());
    }
}

// Registration
services.AddHostedService<HealthCheckBackgroundService>();
services.AddHealthChecks()
    .AddCheck<HealthCheckBackgroundService>("background-service");
```

---

## 🧪 Testing

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

    [Fact]
    public async Task CreateUser_WithValidData_ReturnsCreated()
    {
        // Arrange
        var request = new CreateUserRequest
        {
            Email = "new@test.com",
            FirstName = "New",
            LastName = "User"
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/users", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);

        var user = await response.Content.ReadFromJsonAsync<UserDto>();

        user.Should().NotBeNull();
        user!.Email.Should().Be("new@test.com");

        response.Headers.Location.Should().NotBeNull();
    }

    [Fact]
    public async Task CreateUser_WithInvalidData_ReturnsBadRequest()
    {
        // Arrange
        var request = new CreateUserRequest
        {
            Email = "invalid-email",
            FirstName = "",
            LastName = ""
        };

        // Act
        var response = await _client.PostAsJsonAsync("/api/users", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.BadRequest);
    }
}
```

### Test with Authentication

```csharp
public class AuthenticatedTestsBase : IClassFixture<CustomWebApplicationFactory<Program>>
{
    protected readonly HttpClient _client;
    protected readonly CustomWebApplicationFactory<Program> _factory;

    public AuthenticatedTestsBase(CustomWebApplicationFactory<Program> factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
    }

    protected void AuthenticateAs(string role = "User")
    {
        var token = GenerateTestToken(role);
        _client.DefaultRequestHeaders.Authorization =
            new AuthenticationHeaderValue("Bearer", token);
    }

    private string GenerateTestToken(string role)
    {
        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, Guid.NewGuid().ToString()),
            new Claim(ClaimTypes.Email, "test@example.com"),
            new Claim(ClaimTypes.Role, role)
        };

        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes("test-secret-key-at-least-32-characters"));
        var credentials = new SigningCredentials(
            key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: "test-issuer",
            audience: "test-audience",
            claims: claims,
            expires: DateTime.UtcNow.AddHours(1),
            signingCredentials: credentials);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}

public class ProtectedEndpointTests : AuthenticatedTestsBase
{
    public ProtectedEndpointTests(CustomWebApplicationFactory<Program> factory)
        : base(factory)
    {
    }

    [Fact]
    public async Task AdminEndpoint_WithoutAuth_ReturnsUnauthorized()
    {
        // Act
        var response = await _client.GetAsync("/api/admin/dashboard");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Unauthorized);
    }

    [Fact]
    public async Task AdminEndpoint_WithUserRole_ReturnsForbidden()
    {
        // Arrange
        AuthenticateAs("User");

        // Act
        var response = await _client.GetAsync("/api/admin/dashboard");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Forbidden);
    }

    [Fact]
    public async Task AdminEndpoint_WithAdminRole_ReturnsSuccess()
    {
        // Arrange
        AuthenticateAs("Admin");

        // Act
        var response = await _client.GetAsync("/api/admin/dashboard");

        // Assert
        response.EnsureSuccessStatusCode();
    }
}
```

### NUnit Alternative

```csharp
using NUnit.Framework;
using Moq;
using FluentAssertions;

namespace MyApp.UnitTests.Services;

[TestFixture]
public class UserServiceNUnitTests
{
    private Mock<IUserRepository> _userRepositoryMock = null!;
    private Mock<IEmailService> _emailServiceMock = null!;
    private UserService _sut = null!;

    [SetUp]
    public void Setup()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _emailServiceMock = new Mock<IEmailService>();

        _sut = new UserService(
            _userRepositoryMock.Object,
            _emailServiceMock.Object);
    }

    [Test]
    public async Task GetByIdAsync_WithValidId_ReturnsUser()
    {
        // Arrange
        var userId = Guid.NewGuid();
        var expectedUser = new User { Id = userId, Email = "test@example.com" };

        _userRepositoryMock
            .Setup(r => r.GetByIdAsync(userId, It.IsAny<CancellationToken>()))
            .ReturnsAsync(expectedUser);

        // Act
        var result = await _sut.GetByIdAsync(userId);

        // Assert
        result.Should().NotBeNull();
        result!.Id.Should().Be(userId);
    }

    [TestCase("")]
    [TestCase(" ")]
    [TestCase(null)]
    public async Task CreateAsync_WithInvalidEmail_ThrowsException(string? email)
    {
        // Arrange
        var request = new CreateUserRequest { Email = email! };

        // Act & Assert
        await _sut.Invoking(s => s.CreateAsync(request))
            .Should().ThrowAsync<ValidationException>();
    }

    [Test]
    [TestCaseSource(nameof(GetTestUsers))]
    public async Task GetByIdAsync_ReturnsExpectedUser(Guid id, string email)
    {
        // Arrange
        _userRepositoryMock
            .Setup(r => r.GetByIdAsync(id, It.IsAny<CancellationToken>()))
            .ReturnsAsync(new User { Id = id, Email = email });

        // Act
        var result = await _sut.GetByIdAsync(id);

        // Assert
        result!.Email.Should().Be(email);
    }

    private static IEnumerable<TestCaseData> GetTestUsers()
    {
        yield return new TestCaseData(
            Guid.Parse("11111111-1111-1111-1111-111111111111"),
            "user1@test.com");
        yield return new TestCaseData(
            Guid.Parse("22222222-2222-2222-2222-222222222222"),
            "user2@test.com");
    }
}
```

---

## 🔄 Common Patterns

### Result Pattern

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }
    public IReadOnlyList<string> Errors { get; }

    private Result(bool isSuccess, T? value, string? error, IEnumerable<string>? errors)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
        Errors = errors?.ToList() ?? [];
    }

    public static Result<T> Success(T value) =>
        new(true, value, null, null);

    public static Result<T> Failure(string error) =>
        new(false, default, error, [error]);

    public static Result<T> Failure(IEnumerable<string> errors) =>
        new(false, default, errors.FirstOrDefault(), errors);

    public TResult Match<TResult>(
        Func<T, TResult> onSuccess,
        Func<IReadOnlyList<string>, TResult> onFailure)
    {
        return IsSuccess ? onSuccess(Value!) : onFailure(Errors);
    }
}

// Usage
public async Task<Result<UserDto>> CreateUserAsync(CreateUserRequest request)
{
    var validationResult = await _validator.ValidateAsync(request);

    if (!validationResult.IsValid)
    {
        return Result<UserDto>.Failure(
            validationResult.Errors.Select(e => e.ErrorMessage));
    }

    var existingUser = await _repository.GetByEmailAsync(request.Email);

    if (existingUser is not null)
    {
        return Result<UserDto>.Failure("Email already exists");
    }

    var user = new User
    {
        Email = request.Email,
        FirstName = request.FirstName,
        LastName = request.LastName
    };

    await _repository.AddAsync(user);

    return Result<UserDto>.Success(user.ToDto());
}

// Controller usage
[HttpPost]
public async Task<IActionResult> CreateUser(CreateUserRequest request)
{
    var result = await _userService.CreateUserAsync(request);

    return result.Match<IActionResult>(
        onSuccess: user => CreatedAtAction(nameof(GetUser), new { id = user.Id }, user),
        onFailure: errors => BadRequest(new { Errors = errors }));
}
```

### CQRS Pattern

```csharp
// Command
public record CreateUserCommand(
    string Email,
    string FirstName,
    string LastName) : IRequest<Result<Guid>>;

// Command Handler
public class CreateUserCommandHandler : IRequestHandler<CreateUserCommand, Result<Guid>>
{
    private readonly IUserRepository _repository;
    private readonly IValidator<CreateUserCommand> _validator;

    public CreateUserCommandHandler(
        IUserRepository repository,
        IValidator<CreateUserCommand> validator)
    {
        _repository = repository;
        _validator = validator;
    }

    public async Task<Result<Guid>> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        var validationResult = await _validator.ValidateAsync(
            request, cancellationToken);

        if (!validationResult.IsValid)
        {
            return Result<Guid>.Failure(
                validationResult.Errors.Select(e => e.ErrorMessage));
        }

        var user = new User
        {
            Email = request.Email,
            FirstName = request.FirstName,
            LastName = request.LastName
        };

        await _repository.AddAsync(user, cancellationToken);

        return Result<Guid>.Success(user.Id);
    }
}

// Query
public record GetUserByIdQuery(Guid Id) : IRequest<UserDto?>;

// Query Handler
public class GetUserByIdQueryHandler : IRequestHandler<GetUserByIdQuery, UserDto?>
{
    private readonly IUserRepository _repository;

    public GetUserByIdQueryHandler(IUserRepository repository)
    {
        _repository = repository;
    }

    public async Task<UserDto?> Handle(
        GetUserByIdQuery request,
        CancellationToken cancellationToken)
    {
        var user = await _repository.GetByIdAsync(request.Id, cancellationToken);
        return user?.ToDto();
    }
}

// Controller
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly IMediator _mediator;

    public UsersController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpGet("{id:guid}")]
    public async Task<ActionResult<UserDto>> GetUser(Guid id)
    {
        var user = await _mediator.Send(new GetUserByIdQuery(id));
        return user is null ? NotFound() : Ok(user);
    }

    [HttpPost]
    public async Task<IActionResult> CreateUser(CreateUserCommand command)
    {
        var result = await _mediator.Send(command);

        return result.Match<IActionResult>(
            onSuccess: id => CreatedAtAction(nameof(GetUser), new { id }, null),
            onFailure: errors => BadRequest(new { Errors = errors }));
    }
}
```

### Unit of Work Pattern

```csharp
public interface IUnitOfWork : IDisposable
{
    IUserRepository Users { get; }
    IOrderRepository Orders { get; }
    IProductRepository Products { get; }
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
    Task BeginTransactionAsync(CancellationToken cancellationToken = default);
    Task CommitTransactionAsync(CancellationToken cancellationToken = default);
    Task RollbackTransactionAsync(CancellationToken cancellationToken = default);
}

public class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext _context;
    private IDbContextTransaction? _transaction;

    public UnitOfWork(
        AppDbContext context,
        IUserRepository users,
        IOrderRepository orders,
        IProductRepository products)
    {
        _context = context;
        Users = users;
        Orders = orders;
        Products = products;
    }

    public IUserRepository Users { get; }
    public IOrderRepository Orders { get; }
    public IProductRepository Products { get; }

    public async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        return await _context.SaveChangesAsync(cancellationToken);
    }

    public async Task BeginTransactionAsync(CancellationToken cancellationToken = default)
    {
        _transaction = await _context.Database
            .BeginTransactionAsync(cancellationToken);
    }

    public async Task CommitTransactionAsync(CancellationToken cancellationToken = default)
    {
        if (_transaction is not null)
        {
            await _transaction.CommitAsync(cancellationToken);
            await _transaction.DisposeAsync();
            _transaction = null;
        }
    }

    public async Task RollbackTransactionAsync(CancellationToken cancellationToken = default)
    {
        if (_transaction is not null)
        {
            await _transaction.RollbackAsync(cancellationToken);
            await _transaction.DisposeAsync();
            _transaction = null;
        }
    }

    public void Dispose()
    {
        _transaction?.Dispose();
        _context.Dispose();
    }
}

// Usage
public class OrderService : IOrderService
{
    private readonly IUnitOfWork _unitOfWork;

    public OrderService(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<Order> CreateOrderAsync(CreateOrderRequest request)
    {
        await _unitOfWork.BeginTransactionAsync();

        try
        {
            var user = await _unitOfWork.Users.GetByIdAsync(request.UserId);

            if (user is null)
            {
                throw new NotFoundException("User not found");
            }

            var order = new Order
            {
                UserId = user.Id,
                OrderDate = DateTime.UtcNow,
                Items = request.Items.Select(i => new OrderItem
                {
                    ProductId = i.ProductId,
                    Quantity = i.Quantity,
                    Price = i.Price
                }).ToList()
            };

            await _unitOfWork.Orders.AddAsync(order);

            // Update product stock
            foreach (var item in request.Items)
            {
                var product = await _unitOfWork.Products.GetByIdAsync(item.ProductId);
                product!.Stock -= item.Quantity;
                await _unitOfWork.Products.UpdateAsync(product);
            }

            await _unitOfWork.SaveChangesAsync();
            await _unitOfWork.CommitTransactionAsync();

            return order;
        }
        catch
        {
            await _unitOfWork.RollbackTransactionAsync();
            throw;
        }
    }
}
```

---

## ✅ Best Practices

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

## 📚 Additional Resources

- [.NET Documentation](https://docs.microsoft.com/dotnet/)
- [ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core/)
- [EF Core Documentation](https://docs.microsoft.com/ef/core/)
- [C# Language Reference](https://docs.microsoft.com/dotnet/csharp/)
- [.NET Architecture Guides](https://dotnet.microsoft.com/learn/aspnet/architecture)

---

> **Note**: This skill covers .NET 8+ patterns and best practices. For earlier versions, some features may not be available.
