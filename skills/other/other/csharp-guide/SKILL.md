---
name: csharp-guide
description: |
  C# language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with C# files (.cs, .csx), .csproj, .sln, or when the user mentions C#/.NET.
  Provides nullable reference types, async/await patterns, LINQ guidelines,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: csharp
  extensions: ".cs,.csx"
---

# C# Guide

> Applies to: C# 12+, .NET 8+, ASP.NET Core, Console Apps, Libraries

## Core Principles

1. **Type Safety**: Enable nullable reference types project-wide; treat warnings as errors
2. **Immutability First**: Prefer records, `readonly`, and `init` properties for data types
3. **Async All The Way**: Use `async`/`await` end-to-end; never block on async code
4. **Dependency Injection**: Constructor injection via `IServiceCollection`; no service locator
5. **Fail Fast**: Validate inputs at boundaries; use guard clauses and `ArgumentException`

## Guardrails

### Version & Dependencies

- Target .NET 8+ with C# 12+ language features
- Use `<Nullable>enable</Nullable>` and `<ImplicitUsings>enable</ImplicitUsings>` in `.csproj`
- Pin package versions explicitly in `.csproj` (avoid floating `*` versions)
- Run `dotnet restore` before committing after dependency changes
- Audit new packages with `dotnet list package --vulnerable` before adding

### Code Style

- Follow [.NET naming conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- Public members: `PascalCase` | Private fields: `_camelCase` with underscore prefix
- Interfaces: `IServiceName` | Async methods: suffix with `Async`
- Use `var` when the type is obvious from the right side; explicit types otherwise
- One class per file; filename matches class name
- Use file-scoped namespaces (`namespace MyApp.Services;`)
- Configure `.editorconfig` for consistent formatting across the team
- Run `dotnet format` before every commit

### Nullable Reference Types

- Enable globally: `<Nullable>enable</Nullable>` in every `.csproj`
- Never suppress warnings with `#pragma warning disable` unless documented
- Use `[NotNullWhen]`, `[MaybeNullWhen]`, `[NotNull]` attributes for complex nullability
- Use the null-forgiving operator `!` sparingly and only with a justifying comment
- Prefer `is not null` over `!= null` for null checks
- Use `??` and `??=` for default values; `?.` for conditional access

```csharp
// Good: explicit nullability contract
public User? FindByEmail(string email)
{
    ArgumentException.ThrowIfNullOrWhiteSpace(email);
    return _users.FirstOrDefault(u => u.Email == email);
}

// Good: guard clause with null-coalescing
public void Process(Order order)
{
    var customer = order.Customer
        ?? throw new InvalidOperationException("Order must have a customer.");
    // ...
}
```

### Async/Await

- Use `async`/`await` end-to-end; never call `.Result` or `.Wait()` (deadlock risk)
- Suffix all async methods with `Async`: `GetUserAsync`, `SaveOrderAsync`
- Use `ValueTask<T>` for hot paths that frequently complete synchronously
- Use `ConfigureAwait(false)` in library code (not in ASP.NET Core controllers)
- Use `CancellationToken` in all async method signatures that perform I/O
- Use `IAsyncEnumerable<T>` for streaming large result sets
- Set timeouts on all external calls with `CancellationTokenSource`

```csharp
public async Task<User> GetUserAsync(
    int id, CancellationToken cancellationToken = default)
{
    return await _dbContext.Users
        .AsNoTracking()
        .FirstOrDefaultAsync(u => u.Id == id, cancellationToken)
        ?? throw new NotFoundException(nameof(User), id);
}
```

### LINQ

- Prefer method syntax over query syntax for consistency
- Never put side effects inside LINQ queries (no mutations, no I/O)
- Use `AsNoTracking()` for read-only EF Core queries
- Materialize queries with `ToListAsync()` / `ToArrayAsync()` before returning
- Avoid `Count()` when `Any()` suffices
- Use `Select` to project only needed fields (avoid loading full entities)

```csharp
// Good: projection, no-tracking, materialized
var activeEmails = await _dbContext.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .Select(u => u.Email)
    .ToListAsync(cancellationToken);

// Bad: side effect in LINQ
var results = items.Select(i => { i.Processed = true; return i; }); // Don't do this
```

## Project Structure

```
MySolution/
├── MySolution.sln
├── src/
│   ├── MySolution.Api/            # ASP.NET Core host / entry point
│   │   ├── Controllers/
│   │   ├── Middleware/
│   │   ├── Program.cs
│   │   └── MySolution.Api.csproj
│   ├── MySolution.Application/    # Use cases, commands, queries (CQRS)
│   │   ├── Commands/
│   │   ├── Queries/
│   │   ├── Interfaces/
│   │   └── MySolution.Application.csproj
│   ├── MySolution.Domain/         # Entities, value objects, domain events
│   │   ├── Entities/
│   │   ├── ValueObjects/
│   │   ├── Exceptions/
│   │   └── MySolution.Domain.csproj
│   └── MySolution.Infrastructure/ # EF Core, external services, file I/O
│       ├── Persistence/
│       ├── Services/
│       └── MySolution.Infrastructure.csproj
├── tests/
│   ├── MySolution.UnitTests/
│   │   └── MySolution.UnitTests.csproj
│   ├── MySolution.IntegrationTests/
│   │   └── MySolution.IntegrationTests.csproj
│   └── MySolution.ArchTests/      # Architecture rule tests (optional)
│       └── MySolution.ArchTests.csproj
├── .editorconfig
├── Directory.Build.props          # Shared build properties
└── README.md
```

- Domain project has zero external dependencies (pure C#)
- Application depends only on Domain
- Infrastructure depends on Application and Domain
- Api depends on all projects (composition root)
- Test projects mirror `src/` structure

## Key Patterns

### Nullable Reference Types & Guard Clauses

```csharp
public sealed class OrderService
{
    private readonly IOrderRepository _repository;

    public OrderService(IOrderRepository repository)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
    }

    public async Task<OrderSummary> GetSummaryAsync(
        int orderId, CancellationToken ct = default)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(orderId);

        var order = await _repository.GetByIdAsync(orderId, ct)
            ?? throw new NotFoundException(nameof(Order), orderId);

        return new OrderSummary(order.Id, order.Total, order.Status);
    }
}
```

### Pattern Matching

```csharp
// Switch expression with property patterns
public decimal CalculateDiscount(Customer customer) => customer switch
{
    { MembershipLevel: "Gold", YearsActive: > 5 } => 0.20m,
    { MembershipLevel: "Gold" } => 0.15m,
    { MembershipLevel: "Silver" } => 0.10m,
    { TotalOrders: > 100 } => 0.05m,
    _ => 0m,
};

// Relational and logical patterns
public string ClassifyTemperature(double temp) => temp switch
{
    < 0 => "Freezing",
    >= 0 and < 15 => "Cold",
    >= 15 and < 25 => "Moderate",
    >= 25 and < 35 => "Warm",
    >= 35 => "Hot",
};

// Type pattern in is-expression
public static string Describe(object value) => value switch
{
    int n when n < 0 => $"Negative integer: {n}",
    int n => $"Positive integer: {n}",
    string { Length: 0 } => "Empty string",
    string s => $"String of length {s.Length}",
    null => "null",
    _ => $"Unknown: {value.GetType().Name}",
};
```

### Records & Immutable Data

```csharp
// Record for DTOs and value objects (value equality, immutable)
public sealed record OrderSummary(int Id, decimal Total, OrderStatus Status);

// Record with validation
public sealed record EmailAddress
{
    public string Value { get; }

    public EmailAddress(string value)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(value);
        if (!value.Contains('@'))
            throw new ArgumentException("Invalid email format.", nameof(value));
        Value = value;
    }
}

// Record struct for high-performance value types (no heap allocation)
public readonly record struct Coordinate(double Latitude, double Longitude);

// Nondestructive mutation with `with`
var updated = original with { Status = OrderStatus.Shipped };
```

### Async Streams

```csharp
// Producing an async stream
public async IAsyncEnumerable<LogEntry> StreamLogsAsync(
    DateTime since,
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var batch in _logSource.ReadBatchesAsync(since, ct))
    {
        foreach (var entry in batch.Entries)
        {
            ct.ThrowIfCancellationRequested();
            yield return entry;
        }
    }
}

// Consuming an async stream
await foreach (var log in StreamLogsAsync(DateTime.UtcNow.AddHours(-1), ct))
{
    Console.WriteLine($"[{log.Timestamp}] {log.Message}");
}
```

### Dependency Injection

```csharp
// Registration in Program.cs (or a ServiceCollectionExtensions class)
public static IServiceCollection AddApplicationServices(
    this IServiceCollection services)
{
    services.AddScoped<IOrderRepository, OrderRepository>();
    services.AddScoped<IOrderService, OrderService>();
    services.AddSingleton<IClock, SystemClock>();
    services.AddHttpClient<IPaymentGateway, StripePaymentGateway>(client =>
    {
        client.BaseAddress = new Uri("https://api.stripe.com/");
        client.Timeout = TimeSpan.FromSeconds(10);
    });

    return services;
}

// Constructor injection (no service locator, no static access)
public sealed class OrderService : IOrderService
{
    private readonly IOrderRepository _repository;
    private readonly IClock _clock;

    public OrderService(IOrderRepository repository, IClock clock)
    {
        _repository = repository;
        _clock = clock;
    }
}
```

## Testing

### Standards

- Framework: **xUnit** (preferred), with `[Fact]` and `[Theory]`
- Mocking: **NSubstitute** or **Moq** (pick one per project, stay consistent)
- Assertions: **FluentAssertions** for readable assertion syntax
- Test naming: `MethodName_Scenario_ExpectedResult`
- One assertion concept per test (multiple `Should` calls for same concept OK)
- Use `[Theory]` with `[InlineData]` for parameterized tests
- Coverage target: >80% for business logic, >60% overall

### Unit Test Example

```csharp
public sealed class OrderServiceTests
{
    private readonly IOrderRepository _repository = Substitute.For<IOrderRepository>();
    private readonly IClock _clock = Substitute.For<IClock>();
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _sut = new OrderService(_repository, _clock);
    }

    [Fact]
    public async Task GetSummaryAsync_ExistingOrder_ReturnsSummary()
    {
        // Arrange
        var order = new Order { Id = 1, Total = 99.99m, Status = OrderStatus.Pending };
        _repository.GetByIdAsync(1, Arg.Any<CancellationToken>()).Returns(order);

        // Act
        var result = await _sut.GetSummaryAsync(1);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().Be(1);
        result.Total.Should().Be(99.99m);
        result.Status.Should().Be(OrderStatus.Pending);
    }

    [Fact]
    public async Task GetSummaryAsync_MissingOrder_ThrowsNotFoundException()
    {
        // Arrange
        _repository.GetByIdAsync(99, Arg.Any<CancellationToken>())
            .Returns((Order?)null);

        // Act
        var act = () => _sut.GetSummaryAsync(99);

        // Assert
        await act.Should().ThrowAsync<NotFoundException>()
            .WithMessage("*Order*99*");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-100)]
    public async Task GetSummaryAsync_InvalidId_ThrowsArgumentException(int invalidId)
    {
        var act = () => _sut.GetSummaryAsync(invalidId);

        await act.Should().ThrowAsync<ArgumentOutOfRangeException>();
    }
}
```

### Integration Test Example

```csharp
public sealed class OrdersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public OrdersApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace real DB with in-memory for tests
                services.RemoveAll<DbContextOptions<AppDbContext>>();
                services.AddDbContext<AppDbContext>(opts =>
                    opts.UseInMemoryDatabase("TestDb"));
            });
        }).CreateClient();
    }

    [Fact]
    public async Task GetOrder_ReturnsOk_WhenOrderExists()
    {
        var response = await _client.GetAsync("/api/orders/1");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var body = await response.Content.ReadFromJsonAsync<OrderSummary>();
        body.Should().NotBeNull();
        body!.Id.Should().Be(1);
    }
}
```

## Tooling

### Essential Commands

```bash
dotnet new sln                           # Create solution
dotnet new webapi -n MyApp.Api           # New Web API project
dotnet sln add src/MyApp.Api             # Add project to solution
dotnet restore                           # Restore packages
dotnet build --no-restore                # Build
dotnet test --no-build --verbosity normal # Run tests
dotnet test --collect:"XPlat Code Coverage" # With coverage
dotnet format                            # Format code
dotnet publish -c Release -o ./publish   # Publish for deployment
```

### Analyzers & EditorConfig

```xml
<!-- Directory.Build.props (shared across all projects) -->
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers"
                      Version="8.0.0" PrivateAssets="all" />
    <PackageReference Include="SonarAnalyzer.CSharp"
                      Version="9.32.0" PrivateAssets="all" />
  </ItemGroup>
</Project>
```

```ini
# .editorconfig (key settings)
[*.cs]
indent_style = space
indent_size = 4
dotnet_sort_system_directives_first = true
csharp_style_namespace_declarations = file_scoped:warning
csharp_style_var_for_built_in_types = false:suggestion
csharp_style_var_when_type_is_apparent = true:suggestion
csharp_style_prefer_switch_expression = true:suggestion
csharp_style_prefer_pattern_matching = true:suggestion
csharp_prefer_simple_using_statement = true:suggestion
dotnet_style_prefer_is_null_check_over_reference_equality_method = true:warning
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Async patterns, DI registration, LINQ examples

## External References

- [C# Language Reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/)
- [.NET Naming Conventions](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [Nullable Reference Types](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references)
- [Async/Await Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
- [xUnit Documentation](https://xunit.net/docs/getting-started/netcore/cmdline)
- [FluentAssertions](https://fluentassertions.com/)
- [NSubstitute](https://nsubstitute.github.io/)
- [.NET Architecture Guides](https://dotnet.microsoft.com/en-us/learn/aspnet/architecture)
