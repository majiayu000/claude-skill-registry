---
name: csharp-dotnet-best-practice
description: Master comprehensive C# and .NET best practices covering Clean Architecture, async/await, dependency injection, Entity Framework Core, modern C# 12+ features, testing, error handling, and performance optimization. Use PROACTIVELY for .NET development, code review, or establishing team standards.
---

# C# and .NET Best Practices

Master comprehensive C# and .NET development practices for building robust, maintainable, secure, and performant enterprise applications following modern standards (2024-2026).

## When to Use This Skill

- Developing new .NET APIs, services, or applications
- Reviewing C# code for quality and performance
- Establishing team coding standards and guidelines
- Implementing Clean Architecture patterns
- Optimizing .NET application performance
- Setting up dependency injection properly
- Writing comprehensive unit and integration tests
- Migrating to modern C# features (12+) and .NET 8/9

## Core Concepts

### 1. Clean Architecture Structure

```
src/
├── Domain/                     # Core business logic (no external dependencies)
│   ├── Entities/               # Business entities
│   ├── ValueObjects/           # Immutable value types
│   ├── Enums/                  # Domain enumerations
│   ├── Exceptions/             # Domain-specific exceptions
│   ├── Interfaces/             # Repository and service interfaces
│   └── Events/                 # Domain events
├── Application/                # Use cases and orchestration
│   ├── Common/
│   │   ├── Interfaces/         # Application service interfaces
│   │   ├── Behaviors/          # MediatR pipeline behaviors
│   │   └── Mappings/           # AutoMapper profiles
│   ├── Features/               # Vertical slices by feature
│   │   └── Orders/
│   │       ├── Commands/
│   │       ├── Queries/
│   │       └── DTOs/
│   └── DependencyInjection.cs
├── Infrastructure/             # External concerns implementation
│   ├── Data/
│   │   ├── AppDbContext.cs
│   │   ├── Configurations/     # EF Core configurations
│   │   └── Repositories/
│   ├── Services/
│   │   ├── DateTimeService.cs
│   │   └── EmailService.cs
│   └── DependencyInjection.cs
└── Api/                        # Presentation layer
    ├── Controllers/            # Or Minimal API endpoints
    ├── Middleware/
    ├── Filters/
    └── Program.cs
```

### 2. Modern C# 12+ Features

```csharp
// Primary Constructors (C# 12)
public class UserService(
    IUserRepository repository,
    ILogger<UserService> logger,
    IOptions<UserOptions> options)
{
    private readonly UserOptions _options = options.Value;

    public async Task<User?> GetByIdAsync(string id, CancellationToken ct = default)
    {
        logger.LogInformation("Fetching user {UserId}", id);
        return await repository.GetByIdAsync(id, ct);
    }
}

// Records for immutable data and DTOs
public record UserDto(
    string Id,
    string Name,
    string Email,
    DateTimeOffset CreatedAt);

// Record with computed property
public record OrderSummary(
    string OrderId,
    List<OrderItemDto> Items,
    decimal DiscountPercent)
{
    public decimal Subtotal => Items.Sum(i => i.Quantity * i.UnitPrice);
    public decimal Total => Subtotal * (1 - DiscountPercent);
}

// Collection expressions (C# 12)
List<int> numbers = [1, 2, 3, 4, 5];
int[] moreNumbers = [.. numbers, 6, 7, 8];  // Spread operator
ReadOnlySpan<string> names = ["Alice", "Bob", "Charlie"];

// Required members (C# 11)
public class Configuration
{
    public required string ConnectionString { get; init; }
    public required string ApiKey { get; init; }
    public int Timeout { get; init; } = 30;
}

// File-scoped namespaces and types
file class InternalHelper  // Only visible in this file
{
    public static string Format(string input) => input.Trim().ToLower();
}

// Pattern matching enhancements
public static string GetDiscount(object customer) => customer switch
{
    { } c when c is PremiumCustomer { LoyaltyYears: > 5 } => "30%",
    PremiumCustomer { LoyaltyYears: > 2 } => "20%",
    PremiumCustomer => "10%",
    RegisteredCustomer => "5%",
    _ => "0%"
};

// List patterns (C# 11)
public static decimal CalculateAverage(int[] numbers) => numbers switch
{
    [] => 0,
    [var single] => single,
    [var first, .. var rest] => (first + rest.Sum()) / (1 + rest.Length)
};

// Raw string literals
var json = """
    {
        "name": "John",
        "email": "john@example.com",
        "roles": ["admin", "user"]
    }
    """;

// Interpolated raw strings
var sql = $"""
    SELECT Id, Name, Email
    FROM Users
    WHERE IsActive = 1
    AND CreatedAt > '{DateTime.UtcNow:yyyy-MM-dd}'
    """;
```

### 3. Async/Await Best Practices

```csharp
// ✅ CORRECT: Async all the way down
public async Task<Order> GetOrderAsync(int id, CancellationToken ct = default)
{
    return await _repository.GetByIdAsync(id, ct);
}

// ✅ CORRECT: Parallel execution with WhenAll
public async Task<(Customer Customer, List<Order> Orders)> GetCustomerWithOrdersAsync(
    int customerId,
    CancellationToken ct = default)
{
    var customerTask = _customerRepository.GetByIdAsync(customerId, ct);
    var ordersTask = _orderRepository.GetByCustomerIdAsync(customerId, ct);

    await Task.WhenAll(customerTask, ordersTask);

    return (await customerTask, await ordersTask);
}

// ✅ CORRECT: ValueTask for hot paths
public ValueTask<Product?> GetCachedProductAsync(string id)
{
    if (_cache.TryGetValue(id, out Product? product))
    {
        return ValueTask.FromResult(product);
    }

    return new ValueTask<Product?>(LoadFromDatabaseAsync(id));
}

// ✅ CORRECT: ConfigureAwait in libraries
public async Task<T> LibraryMethodAsync<T>(string url, CancellationToken ct = default)
{
    var response = await _httpClient.GetAsync(url, ct).ConfigureAwait(false);
    response.EnsureSuccessStatusCode();
    return await response.Content.ReadFromJsonAsync<T>(ct).ConfigureAwait(false);
}

// ✅ CORRECT: Cancellation token usage
public async Task ProcessBatchAsync(
    IEnumerable<string> items,
    CancellationToken ct = default)
{
    foreach (var item in items)
    {
        ct.ThrowIfCancellationRequested();
        await ProcessItemAsync(item, ct);
    }
}

// ❌ WRONG: Blocking on async (causes deadlock)
public User GetUser(int id)
{
    // NEVER DO THIS
    return GetUserAsync(id).Result;
    // OR
    return GetUserAsync(id).GetAwaiter().GetResult();
}

// ❌ WRONG: async void (except event handlers)
public async void ProcessOrder(Order order)  // Exceptions are lost!
{
    await _orderService.ProcessAsync(order);
}

// ❌ WRONG: Unnecessary Task.Run
await Task.Run(async () => await GetDataAsync());  // Wastes a thread
```

### 4. Dependency Injection Patterns

```csharp
// Service registration extension
public static class DependencyInjection
{
    public static IServiceCollection AddApplicationServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Scoped: One instance per HTTP request
        services.AddScoped<IOrderService, OrderService>();
        services.AddScoped<ICustomerRepository, CustomerRepository>();

        // Singleton: One instance for entire application lifetime
        services.AddSingleton<IConnectionMultiplexer>(_ =>
            ConnectionMultiplexer.Connect(configuration["Redis:Connection"]!));
        services.AddSingleton<ICacheService, RedisCacheService>();

        // Transient: New instance every time resolved
        services.AddTransient<IValidator<CreateOrderCommand>, CreateOrderValidator>();

        // Options pattern
        services.Configure<EmailOptions>(configuration.GetSection("Email"));
        services.AddOptions<DatabaseOptions>()
            .Bind(configuration.GetSection("Database"))
            .ValidateDataAnnotations()
            .ValidateOnStart();

        // Keyed services (.NET 8+)
        services.AddKeyedScoped<IPaymentProcessor, StripeProcessor>("stripe");
        services.AddKeyedScoped<IPaymentProcessor, PayPalProcessor>("paypal");

        // Factory pattern for conditional resolution
        services.AddScoped<IPricingStrategy>(sp =>
        {
            var options = sp.GetRequiredService<IOptions<PricingOptions>>().Value;
            return options.UseNewEngine
                ? sp.GetRequiredService<NewPricingStrategy>()
                : sp.GetRequiredService<LegacyPricingStrategy>();
        });

        // Decorator pattern
        services.AddScoped<IUserRepository, UserRepository>();
        services.Decorate<IUserRepository, CachedUserRepository>();

        return services;
    }
}

// Usage with keyed services
public class CheckoutService(
    [FromKeyedServices("stripe")] IPaymentProcessor stripeProcessor,
    [FromKeyedServices("paypal")] IPaymentProcessor paypalProcessor)
{
    public async Task<bool> ProcessAsync(string provider, decimal amount)
    {
        var processor = provider switch
        {
            "stripe" => stripeProcessor,
            "paypal" => paypalProcessor,
            _ => throw new ArgumentException($"Unknown provider: {provider}")
        };

        return await processor.ChargeAsync(amount);
    }
}

// Options pattern with validation
public class EmailOptions
{
    public const string SectionName = "Email";

    [Required]
    public string SmtpServer { get; init; } = string.Empty;

    [Range(1, 65535)]
    public int Port { get; init; } = 587;

    [Required, EmailAddress]
    public string FromAddress { get; init; } = string.Empty;

    public bool UseSsl { get; init; } = true;
}
```

### 5. Entity Framework Core Best Practices

```csharp
// DbContext configuration
public class AppDbContext(DbContextOptions<AppDbContext> options)
    : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Product> Products => Set<Product>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);

        // Global query filters
        modelBuilder.Entity<Order>().HasQueryFilter(o => !o.IsDeleted);

        // Indexes
        modelBuilder.Entity<Customer>()
            .HasIndex(c => c.Email)
            .IsUnique();
    }

    public override async Task<int> SaveChangesAsync(CancellationToken ct = default)
    {
        // Audit tracking
        foreach (var entry in ChangeTracker.Entries<IAuditable>())
        {
            switch (entry.State)
            {
                case EntityState.Added:
                    entry.Entity.CreatedAt = DateTime.UtcNow;
                    break;
                case EntityState.Modified:
                    entry.Entity.ModifiedAt = DateTime.UtcNow;
                    break;
            }
        }

        return await base.SaveChangesAsync(ct);
    }
}

// Entity configuration
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");

        builder.HasKey(o => o.Id);

        builder.Property(o => o.Id)
            .HasConversion<OrderId.EfCoreValueConverter>();

        builder.Property(o => o.TotalAmount)
            .HasPrecision(18, 2);

        builder.Property(o => o.Status)
            .HasConversion<string>()
            .HasMaxLength(50);

        // Owned type for value object
        builder.OwnsOne(o => o.ShippingAddress, address =>
        {
            address.Property(a => a.Street).HasMaxLength(200);
            address.Property(a => a.City).HasMaxLength(100);
            address.Property(a => a.PostalCode).HasMaxLength(20);
        });

        builder.HasMany(o => o.Items)
            .WithOne()
            .HasForeignKey(i => i.OrderId)
            .OnDelete(DeleteBehavior.Cascade);

        builder.HasIndex(o => new { o.CustomerId, o.CreatedAt });
    }
}

// Repository with EF Core
public class OrderRepository(AppDbContext context) : IOrderRepository
{
    // ✅ CORRECT: AsNoTracking for read-only queries
    public async Task<Order?> GetByIdAsync(OrderId id, CancellationToken ct = default)
    {
        return await context.Orders
            .AsNoTracking()
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }

    // ✅ CORRECT: Projection to DTO
    public async Task<List<OrderSummaryDto>> GetSummariesAsync(
        int customerId,
        CancellationToken ct = default)
    {
        return await context.Orders
            .AsNoTracking()
            .Where(o => o.CustomerId == customerId)
            .Select(o => new OrderSummaryDto(
                o.Id.Value,
                o.TotalAmount,
                o.Status,
                o.CreatedAt))
            .ToListAsync(ct);
    }

    // ✅ CORRECT: Efficient bulk operations (EF Core 7+)
    public async Task<int> DeactivateOldOrdersAsync(
        DateTime cutoff,
        CancellationToken ct = default)
    {
        return await context.Orders
            .Where(o => o.CreatedAt < cutoff && o.Status == OrderStatus.Draft)
            .ExecuteUpdateAsync(s => s
                .SetProperty(o => o.IsDeleted, true)
                .SetProperty(o => o.DeletedAt, DateTime.UtcNow),
                ct);
    }

    // ❌ WRONG: Loading entire entity when only need ID
    // var order = await context.Orders.FirstOrDefaultAsync(o => o.CustomerId == id);
    // return order?.Id;
}
```

### 6. Error Handling and Validation

```csharp
// Global exception handler (Minimal API)
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;

    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    {
        _logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext context,
        Exception exception,
        CancellationToken ct)
    {
        _logger.LogError(exception, "Unhandled exception occurred");

        var problemDetails = exception switch
        {
            ValidationException ve => new ProblemDetails
            {
                Status = StatusCodes.Status400BadRequest,
                Title = "Validation Error",
                Detail = string.Join("; ", ve.Errors.Select(e => e.ErrorMessage)),
                Type = "https://tools.ietf.org/html/rfc7231#section-6.5.1"
            },
            NotFoundException nf => new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "Not Found",
                Detail = nf.Message,
                Type = "https://tools.ietf.org/html/rfc7231#section-6.5.4"
            },
            UnauthorizedException => new ProblemDetails
            {
                Status = StatusCodes.Status401Unauthorized,
                Title = "Unauthorized",
                Type = "https://tools.ietf.org/html/rfc7235#section-3.1"
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "Internal Server Error",
                Type = "https://tools.ietf.org/html/rfc7231#section-6.6.1"
            }
        };

        context.Response.StatusCode = problemDetails.Status ?? 500;
        await context.Response.WriteAsJsonAsync(problemDetails, ct);

        return true;
    }
}

// Result pattern for business logic
public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }
    public string? ErrorCode { get; }

    private Result(bool isSuccess, T? value, string? error, string? errorCode)
    {
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
        ErrorCode = errorCode;
    }

    public static Result<T> Success(T value) => new(true, value, null, null);
    public static Result<T> Failure(string error, string? code = null)
        => new(false, default, error, code);

    public Result<TNew> Map<TNew>(Func<T, TNew> mapper) =>
        IsSuccess
            ? Result<TNew>.Success(mapper(Value!))
            : Result<TNew>.Failure(Error!, ErrorCode);

    public TResult Match<TResult>(
        Func<T, TResult> success,
        Func<string, TResult> failure) =>
        IsSuccess ? success(Value!) : failure(Error!);
}

// FluentValidation
public class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator(IProductRepository productRepository)
    {
        RuleFor(x => x.CustomerId)
            .NotEmpty()
            .WithMessage("Customer ID is required");

        RuleFor(x => x.Items)
            .NotEmpty()
            .WithMessage("Order must contain at least one item");

        RuleForEach(x => x.Items).SetValidator(new OrderItemValidator());

        RuleFor(x => x.ShippingAddress)
            .NotNull()
            .SetValidator(new AddressValidator());

        // Async validation (use sparingly)
        RuleForEach(x => x.Items)
            .MustAsync(async (item, ct) =>
            {
                var product = await productRepository.GetByIdAsync(item.ProductId, ct);
                return product?.Stock >= item.Quantity;
            })
            .WithMessage("Insufficient stock for product {PropertyValue}");
    }
}
```

### 7. Testing Patterns

```csharp
// Unit test with xUnit and Moq
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _repositoryMock;
    private readonly Mock<IStockService> _stockServiceMock;
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _repositoryMock = new Mock<IOrderRepository>();
        _stockServiceMock = new Mock<IStockService>();

        _sut = new OrderService(
            _repositoryMock.Object,
            _stockServiceMock.Object,
            NullLogger<OrderService>.Instance);
    }

    [Fact]
    public async Task CreateOrder_WithValidData_ReturnsSuccess()
    {
        // Arrange
        var command = new CreateOrderCommand
        {
            CustomerId = 1,
            Items = [new OrderItemDto("PROD-1", 2, 10.00m)]
        };

        _stockServiceMock
            .Setup(x => x.CheckStockAsync("PROD-1", 2, It.IsAny<CancellationToken>()))
            .ReturnsAsync(true);

        _repositoryMock
            .Setup(x => x.CreateAsync(It.IsAny<Order>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(new Order { Id = new OrderId(Guid.NewGuid()) });

        // Act
        var result = await _sut.CreateOrderAsync(command);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.NotNull(result.Value);

        _repositoryMock.Verify(
            x => x.CreateAsync(
                It.Is<Order>(o => o.CustomerId == 1),
                It.IsAny<CancellationToken>()),
            Times.Once);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(-100)]
    public async Task CreateOrder_WithInvalidQuantity_ReturnsFailure(int quantity)
    {
        // Arrange
        var command = new CreateOrderCommand
        {
            CustomerId = 1,
            Items = [new OrderItemDto("PROD-1", quantity, 10.00m)]
        };

        // Act
        var result = await _sut.CreateOrderAsync(command);

        // Assert
        Assert.False(result.IsSuccess);
        Assert.Equal("VALIDATION_ERROR", result.ErrorCode);
    }
}

// Integration tests with WebApplicationFactory
public class OrdersApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;
    private readonly WebApplicationFactory<Program> _factory;

    public OrdersApiTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace with in-memory database
                services.RemoveAll<DbContextOptions<AppDbContext>>();
                services.AddDbContext<AppDbContext>(options =>
                    options.UseInMemoryDatabase($"TestDb-{Guid.NewGuid()}"));

                // Replace external services with mocks
                services.RemoveAll<IEmailService>();
                services.AddSingleton<IEmailService, FakeEmailService>();
            });
        });

        _client = _factory.CreateClient();
    }

    [Fact]
    public async Task GetOrder_WhenExists_ReturnsOrder()
    {
        // Arrange
        await SeedTestData();

        // Act
        var response = await _client.GetAsync("/api/orders/1");

        // Assert
        response.EnsureSuccessStatusCode();
        var order = await response.Content.ReadFromJsonAsync<OrderDto>();
        Assert.Equal(1, order!.Id);
    }

    private async Task SeedTestData()
    {
        using var scope = _factory.Services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        context.Orders.Add(new Order { Id = new OrderId(1), CustomerId = 100 });
        await context.SaveChangesAsync();
    }
}
```

### 8. Performance Optimization

```csharp
// Span and Memory for zero-allocation parsing
public static class HighPerformanceParser
{
    public static bool TryParseOrderId(ReadOnlySpan<char> input, out int orderId)
    {
        // Format: "ORD-12345"
        if (input.Length < 5 || !input.StartsWith("ORD-"))
        {
            orderId = 0;
            return false;
        }

        return int.TryParse(input[4..], out orderId);
    }

    public static IEnumerable<ReadOnlyMemory<char>> SplitLines(ReadOnlyMemory<char> text)
    {
        var span = text.Span;
        int start = 0;

        for (int i = 0; i < span.Length; i++)
        {
            if (span[i] == '\n')
            {
                yield return text[start..i];
                start = i + 1;
            }
        }

        if (start < span.Length)
        {
            yield return text[start..];
        }
    }
}

// ArrayPool for temporary buffers
public class BufferedProcessor
{
    public async Task<byte[]> ProcessAsync(Stream input)
    {
        byte[] buffer = ArrayPool<byte>.Shared.Rent(8192);
        try
        {
            using var output = new MemoryStream();
            int bytesRead;

            while ((bytesRead = await input.ReadAsync(buffer)) > 0)
            {
                // Process buffer...
                await output.WriteAsync(buffer.AsMemory(0, bytesRead));
            }

            return output.ToArray();
        }
        finally
        {
            ArrayPool<byte>.Shared.Return(buffer);
        }
    }
}

// Caching with IMemoryCache
public class CachedProductService(
    IProductRepository repository,
    IMemoryCache cache,
    ILogger<CachedProductService> logger)
{
    private static readonly TimeSpan CacheDuration = TimeSpan.FromMinutes(5);

    public async Task<Product?> GetByIdAsync(string id, CancellationToken ct = default)
    {
        var cacheKey = $"product:{id}";

        if (cache.TryGetValue(cacheKey, out Product? cached))
        {
            logger.LogDebug("Cache hit for {CacheKey}", cacheKey);
            return cached;
        }

        logger.LogDebug("Cache miss for {CacheKey}", cacheKey);
        var product = await repository.GetByIdAsync(id, ct);

        if (product is not null)
        {
            var options = new MemoryCacheEntryOptions()
                .SetSlidingExpiration(CacheDuration)
                .SetSize(1);

            cache.Set(cacheKey, product, options);
        }

        return product;
    }
}

// Compiled regex for performance
public static partial class Validators
{
    [GeneratedRegex(@"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")]
    public static partial Regex EmailRegex();

    [GeneratedRegex(@"^\d{4}-\d{2}-\d{2}$")]
    public static partial Regex DateRegex();

    public static bool IsValidEmail(string email) => EmailRegex().IsMatch(email);
}
```

## Quick Reference

### Lifetime Guidelines

| Service Type             | Lifetime  | Use Case                    |
| ------------------------ | --------- | --------------------------- |
| DbContext                | Scoped    | Database access per request |
| HttpClient (via factory) | Singleton | HTTP connections            |
| Repositories             | Scoped    | Data access per request     |
| Business Services        | Scoped    | Request-scoped operations   |
| Validators               | Transient | Stateless validation        |
| Configuration            | Singleton | IOptions<T>                 |
| Caches                   | Singleton | Shared cache state          |

### EF Core Performance Checklist

- [ ] Use `AsNoTracking()` for read-only queries
- [ ] Use projections (`Select`) instead of loading full entities
- [ ] Avoid N+1 queries with proper `Include` usage
- [ ] Use raw SQL or Dapper for complex read queries
- [ ] Use `ExecuteUpdate`/`ExecuteDelete` for bulk operations
- [ ] Add appropriate indexes in configurations
- [ ] Use compiled queries for hot paths

## Common Pitfalls

| Pitfall            | Problem                      | Solution                           |
| ------------------ | ---------------------------- | ---------------------------------- |
| Captive dependency | Singleton holding Scoped     | Use factory pattern or make scoped |
| Blocking async     | `.Result` deadlock           | Async all the way                  |
| Over-fetching      | Loading full entities        | Use projections                    |
| No cancellation    | Long operations can't cancel | Pass CancellationToken             |
| Hardcoded config   | Difficult to change          | Use IOptions pattern               |
| Generic exceptions | `catch (Exception)`          | Catch specific types               |

## Best Practices Summary

### DO

1. Use async/await throughout the call stack
2. Pass CancellationToken to all async methods
3. Use records for DTOs and immutable data
4. Apply IOptions pattern for configuration
5. Use Result types for expected business failures
6. Write unit tests for business logic
7. Use FluentValidation for input validation
8. Apply global exception handling
9. Use AsNoTracking for read-only EF queries
10. Cache aggressively with proper invalidation

### DON'T

1. Block on async with .Result or .Wait()
2. Use async void (except event handlers)
3. Catch generic Exception without logging
4. Hardcode configuration values
5. Expose EF entities in API responses
6. Ignore CancellationToken parameters
7. Create HttpClient manually (use IHttpClientFactory)
8. Use service locator pattern
9. Mix sync and async code unnecessarily
10. Skip validation at API boundaries


## Parent Hub
- [_backend-mastery](../_backend-mastery/SKILL.md)
