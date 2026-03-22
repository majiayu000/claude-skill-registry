---
name: aspnet-core
description: |
  ASP.NET Core framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with ASP.NET Core projects, or when the user mentions ASP.NET Core.
  Provides Minimal APIs, EF Core, authentication, middleware, and deployment guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: csharp
  extensions: ".cs"
---

# ASP.NET Core Guide

> Applies to: ASP.NET Core 8.x (LTS), C# 12, Minimal APIs, MVC, Web APIs

## Core Principles

1. **Clean Architecture**: Separate API, Core (domain), Infrastructure, and Contracts layers
2. **Dependency Injection**: Built-in DI container for all service registrations
3. **Minimal APIs First**: Prefer Minimal APIs for new endpoints; use controllers for complex scenarios
4. **Async Everywhere**: All I/O-bound operations must be async with CancellationToken
5. **Records for DTOs**: Immutable data transfer objects using C# records

## Guardrails

### Version & Dependencies

- Target `net8.0` (LTS) with `<Nullable>enable</Nullable>` and `<ImplicitUsings>enable</ImplicitUsings>`
- Enable `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` in `Directory.Build.props`
- Use Central Package Management (`Directory.Packages.props`) for version consistency
- Include StyleCop.Analyzers with `<AnalysisLevel>latest-recommended</AnalysisLevel>`

### Code Style

- File-scoped namespaces: `namespace MyApp.Core.Entities;`
- Primary constructors for DI: `public class UserService(IUserRepository repo, IMapper mapper)`
- Use `required` keyword for mandatory properties on entities
- Records for all request/response DTOs
- Avoid `async void` -- always return `Task` or `Task<T>`

### Error Handling

- Use a global exception middleware (not per-controller try/catch)
- Define domain exception hierarchy: `DomainException` -> `NotFoundException`, `ConflictException`, `ValidationException`
- Map domain exceptions to HTTP status codes in middleware
- Log unhandled exceptions at Error level; log expected exceptions at Warning
- Never expose stack traces in production responses

### Security

- Never hardcode connection strings or secrets (use `appsettings.json` + environment overrides)
- Always validate JWT `Issuer`, `Audience`, `Lifetime`, and `IssuerSigningKey`
- Use `[Authorize]` attribute on all endpoints that require authentication
- Role-based authorization: `[Authorize(Roles = "Admin")]`
- Use HTTPS in production; enforce with `UseHttpsRedirection()`

## Project Structure

```
MyApp/
├── MyApp.Api/                    # Web API project
│   ├── Controllers/              # API controllers (MVC pattern)
│   ├── Endpoints/                # Minimal API endpoints (alternative)
│   ├── Middleware/                # Custom middleware
│   ├── Filters/                  # Action filters
│   ├── Validators/               # FluentValidation validators
│   ├── Mappings/                 # Mapster/AutoMapper configurations
│   ├── Extensions/               # Service collection extensions
│   ├── Program.cs                # Entry point and DI configuration
│   ├── appsettings.json          # Configuration
│   └── appsettings.Development.json
├── MyApp.Core/                   # Domain/business logic (no dependencies)
│   ├── Entities/                 # Domain entities
│   ├── Interfaces/               # Repository and service interfaces
│   ├── Services/                 # Business logic implementations
│   └── Exceptions/               # Domain exception types
├── MyApp.Infrastructure/         # Data access, external services
│   ├── Data/                     # DbContext and EF configurations
│   │   └── Configurations/       # IEntityTypeConfiguration<T>
│   └── Repositories/             # Repository implementations
├── MyApp.Contracts/              # DTOs, API contracts (shared)
│   ├── Requests/                 # Input DTOs
│   └── Responses/                # Output DTOs
├── tests/
│   ├── MyApp.UnitTests/          # xUnit + Moq + FluentAssertions
│   └── MyApp.IntegrationTests/   # WebApplicationFactory + Testcontainers
├── MyApp.sln
├── Directory.Build.props         # Shared build settings
├── Directory.Packages.props      # Central package management
└── docker-compose.yml
```

**Layer rules:**
- `Core` has zero external dependencies (no EF Core, no ASP.NET references)
- `Infrastructure` references `Core` only
- `Api` references `Core`, `Infrastructure`, and `Contracts`
- `Contracts` has no project references (shareable with clients)

## Minimal APIs

### Endpoint Group Pattern

```csharp
public static class UserEndpoints
{
    public static IEndpointRouteBuilder MapUserEndpoints(
        this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/users")
            .WithTags("Users")
            .WithOpenApi();

        group.MapGet("/", GetAll)
            .RequireAuthorization()
            .Produces<PagedResponse<UserResponse>>();

        group.MapGet("/{id:long}", GetById)
            .RequireAuthorization()
            .Produces<UserResponse>()
            .Produces(StatusCodes.Status404NotFound);

        group.MapPost("/", Create)
            .Produces<UserResponse>(StatusCodes.Status201Created)
            .Produces(StatusCodes.Status400BadRequest);

        return routes;
    }

    private static async Task<IResult> GetById(
        long id, IUserService service, CancellationToken ct)
    {
        var user = await service.GetByIdAsync(id, ct);
        return Results.Ok(user);
    }

    private static async Task<IResult> Create(
        CreateUserRequest request,
        IUserService service,
        IValidator<CreateUserRequest> validator,
        CancellationToken ct)
    {
        var validation = await validator.ValidateAsync(request, ct);
        if (!validation.IsValid)
            return Results.BadRequest(validation.Errors);

        var user = await service.CreateAsync(request, ct);
        return Results.Created($"/api/users/{user.Id}", user);
    }
}
```

Register in `Program.cs`: `app.MapUserEndpoints();`

## Controllers

### Standard REST Controller

```csharp
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly IValidator<CreateUserRequest> _validator;

    public UsersController(
        IUserService userService,
        IValidator<CreateUserRequest> validator)
    {
        _userService = userService;
        _validator = validator;
    }

    [HttpGet("{id:long}")]
    [Authorize]
    [ProducesResponseType(typeof(UserResponse), 200)]
    [ProducesResponseType(404)]
    public async Task<ActionResult<UserResponse>> GetById(
        long id, CancellationToken ct)
    {
        var user = await _userService.GetByIdAsync(id, ct);
        return Ok(user);
    }

    [HttpPost]
    [ProducesResponseType(typeof(UserResponse), 201)]
    [ProducesResponseType(400)]
    public async Task<ActionResult<UserResponse>> Create(
        [FromBody] CreateUserRequest request, CancellationToken ct)
    {
        var validation = await _validator.ValidateAsync(request, ct);
        if (!validation.IsValid)
            return BadRequest(validation.Errors);

        var user = await _userService.CreateAsync(request, ct);
        return CreatedAtAction(nameof(GetById), new { id = user.Id }, user);
    }
}
```

**Guidelines:**
- Always use `[ApiController]` for automatic model binding and validation
- Use `CancellationToken` on every async action
- Annotate with `[ProducesResponseType]` for OpenAPI documentation
- Use route constraints: `{id:long}`, `{slug:alpha}`, `{page:int:min(1)}`

## Entity Framework Core

### DbContext

```csharp
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options) { }

    public DbSet<User> Users => Set<User>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(AppDbContext).Assembly);
    }

    public override Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default)
    {
        foreach (var entry in ChangeTracker.Entries<User>())
        {
            if (entry.State == EntityState.Modified)
                entry.Entity.UpdatedAt = DateTime.UtcNow;
        }
        return base.SaveChangesAsync(cancellationToken);
    }
}
```

### Entity Configuration

```csharp
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        builder.ToTable("users");
        builder.HasKey(u => u.Id);
        builder.Property(u => u.Email).HasMaxLength(255).IsRequired();
        builder.HasIndex(u => u.Email).IsUnique();
        builder.Property(u => u.Role).HasConversion<string>().HasMaxLength(50);
        builder.Property(u => u.Active).HasDefaultValue(true);
    }
}
```

**EF Core rules:**
- Use `IEntityTypeConfiguration<T>` for all configurations (not inline in `OnModelCreating`)
- Use `AsNoTracking()` for read-only queries
- Always include `CancellationToken` in async EF methods
- Use snake_case for database column names via configuration

## Middleware

### Exception Handling Middleware

```csharp
public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionMiddleware> _logger;

    public ExceptionMiddleware(
        RequestDelegate next, ILogger<ExceptionMiddleware> logger)
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

    private async Task HandleExceptionAsync(
        HttpContext context, Exception exception)
    {
        var (statusCode, response) = exception switch
        {
            NotFoundException ex => (404, new { ex.Message }),
            ConflictException ex => (409, new { ex.Message }),
            ValidationException ex => (400, new { ex.Message, ex.Errors }),
            _ => (500, (object)new { Message = "An unexpected error occurred" })
        };

        if (statusCode == 500)
            _logger.LogError(exception, "Unhandled exception");

        context.Response.ContentType = "application/json";
        context.Response.StatusCode = statusCode;
        await context.Response.WriteAsJsonAsync(response);
    }
}
```

Register: `app.UseMiddleware<ExceptionMiddleware>();` (first in pipeline)

## Dependency Injection & Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((ctx, cfg) =>
    cfg.ReadFrom.Configuration(ctx.Configuration));

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.AddValidatorsFromAssemblyContaining<Program>();

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
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Secret"]!))
        };
    });
builder.Services.AddAuthorization();
builder.Services.AddHealthChecks().AddDbContextCheck<AppDbContext>();

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();
app.UseSerilogRequestLogging();
app.UseAuthentication();
app.UseAuthorization();
app.MapUserEndpoints();
app.MapHealthChecks("/health");
app.Run();

public partial class Program { } // For integration test access
```

**DI lifetimes:**
- `Scoped`: repositories, services, DbContext (per-request)
- `Singleton`: configuration objects, mapping configs, HttpClient factories
- `Transient`: lightweight stateless services

## Validation (FluentValidation)

```csharp
public class CreateUserRequestValidator
    : AbstractValidator<CreateUserRequest>
{
    public CreateUserRequestValidator()
    {
        RuleFor(x => x.Email)
            .NotEmpty().EmailAddress().MaximumLength(255);
        RuleFor(x => x.Password)
            .NotEmpty().MinimumLength(8)
            .Matches("[A-Z]").WithMessage("Must contain uppercase")
            .Matches("[0-9]").WithMessage("Must contain digit")
            .Matches("[^a-zA-Z0-9]").WithMessage("Must contain special char");
        RuleFor(x => x.FirstName).NotEmpty().MaximumLength(100);
    }
}
```

Register: `builder.Services.AddValidatorsFromAssemblyContaining<Program>();`

## Testing

### Unit Test Pattern (xUnit + Moq + FluentAssertions)

```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _repoMock = new();
    private readonly Mock<IMapper> _mapperMock = new();
    private readonly Mock<ILogger<UserService>> _loggerMock = new();
    private readonly UserService _sut;

    public UserServiceTests()
    {
        _sut = new UserService(
            _repoMock.Object, _mapperMock.Object, _loggerMock.Object);
    }

    [Fact]
    public async Task GetByIdAsync_WhenNotFound_ThrowsNotFoundException()
    {
        _repoMock.Setup(r => r.GetByIdAsync(999, It.IsAny<CancellationToken>()))
            .ReturnsAsync((User?)null);

        var act = () => _sut.GetByIdAsync(999);

        await act.Should().ThrowAsync<NotFoundException>();
    }
}
```

### Integration Tests (WebApplicationFactory + Testcontainers)

```csharp
public class UsersControllerTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres = new PostgreSqlBuilder()
        .WithImage("postgres:15-alpine").Build();
    private WebApplicationFactory<Program> _factory = null!;
    private HttpClient _client = null!;

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();
        _factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.ConfigureServices(services =>
                services.AddDbContext<AppDbContext>(opt =>
                    opt.UseNpgsql(_postgres.GetConnectionString()))));
        _client = _factory.CreateClient();
    }

    public async Task DisposeAsync()
    {
        await _factory.DisposeAsync();
        await _postgres.DisposeAsync();
    }

    [Fact]
    public async Task Create_ValidRequest_ReturnsCreated()
    {
        var request = new CreateUserRequest("test@example.com", "Password123!", "John", "Doe");
        var response = await _client.PostAsJsonAsync("/api/users", request);
        response.StatusCode.Should().Be(HttpStatusCode.Created);
    }
}
```

## Commands

```bash
# Restore and build
dotnet restore
dotnet build

# Run with hot reload
dotnet watch run --project MyApp.Api

# Run tests
dotnet test
dotnet test --collect:"XPlat Code Coverage"

# EF Core migrations
dotnet tool install --global dotnet-ef
dotnet ef migrations add MigrationName -p MyApp.Infrastructure -s MyApp.Api
dotnet ef database update -p MyApp.Infrastructure -s MyApp.Api

# Format and lint
dotnet format

# Publish and containerize
dotnet publish -c Release -o ./publish
docker build -t myapp:latest .
```

## Best Practices

**DO:** Central Package Management | `CancellationToken` everywhere | Records for DTOs |
FluentValidation | Clean Architecture layers | Health checks (`/health`) | Serilog structured logging | Testcontainers for integration tests

**DON'T:** Expose entities in API responses | Synchronous DB calls | Catch-and-swallow exceptions |
Hardcode secrets | Skip API validation | Magic strings (use `nameof()`)

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- EF Core advanced patterns, Identity/Security, SignalR, Blazor integration, testing strategies, deployment

## External References

- [ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
- [Entity Framework Core](https://docs.microsoft.com/ef/core)
- [FluentValidation](https://docs.fluentvalidation.net/)
- [Serilog](https://serilog.net/)
- [xUnit](https://xunit.net/)
- [FluentAssertions](https://fluentassertions.com/)
- [Testcontainers for .NET](https://dotnet.testcontainers.org/)
