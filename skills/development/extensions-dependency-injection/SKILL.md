---
name: extensions-dependency-injection
description: >
  USE FOR: Registering and resolving services in the built-in .NET DI container, configuring
  service lifetimes (singleton, scoped, transient), keyed services, factory-based registrations,
  decorator patterns, and organizing registrations in extension methods. DO NOT USE FOR: Advanced
  DI features like interception, convention-based registration, or child containers (use Autofac
  or similar), or service locator anti-patterns.
license: MIT
metadata:
  displayName: "Dependency Injection"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: ".NET Dependency Injection Documentation"
    url: "https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection"
  - title: "Microsoft.Extensions.DependencyInjection NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.DependencyInjection"
  - title: ".NET Runtime GitHub Repository"
    url: "https://github.com/dotnet/runtime"
---

# Microsoft.Extensions.DependencyInjection

## Overview

`Microsoft.Extensions.DependencyInjection` is the built-in dependency injection (DI) container for .NET applications. It provides constructor injection, service lifetime management (singleton, scoped, transient), and a registration API through `IServiceCollection`. The container is deeply integrated with the .NET hosting model, ASP.NET Core, Entity Framework Core, and virtually all Microsoft.Extensions libraries.

The built-in container is intentionally simple and fast. It supports constructor injection but not property injection, interception, or convention-based registration. For those advanced features, third-party containers like Autofac or Microsoft.Extensions.DependencyInjection.Abstractions-compatible containers can be plugged in as replacements.

## Basic Service Registration

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

// Register by interface and implementation
builder.Services.AddSingleton<IClock, SystemClock>();
builder.Services.AddScoped<IOrderRepository, SqlOrderRepository>();
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();

// Register a concrete type directly
builder.Services.AddScoped<OrderService>();

var app = builder.Build();
await app.RunAsync();
```

## Service Lifetimes

Understanding when to use each lifetime is critical for correctness.

```csharp
using Microsoft.Extensions.DependencyInjection;

public static class ServiceRegistration
{
    public static IServiceCollection AddApplicationServices(
        this IServiceCollection services)
    {
        // Singleton: one instance for the entire application lifetime.
        // Use for stateless services, configuration, caches, and connection pools.
        services.AddSingleton<IConnectionPool, RedisConnectionPool>();

        // Scoped: one instance per scope (per HTTP request in ASP.NET Core).
        // Use for DbContext, Unit of Work, and request-scoped state.
        services.AddScoped<IUnitOfWork, EfUnitOfWork>();
        services.AddScoped<IUserContext, HttpUserContext>();

        // Transient: a new instance every time it is requested.
        // Use for lightweight, stateless services with no shared state.
        services.AddTransient<IValidator<Order>, OrderValidator>();
        services.AddTransient<INotificationBuilder, NotificationBuilder>();

        return services;
    }
}
```

| Lifetime | Instance Created | Disposed | Use When |
|---|---|---|---|
| Singleton | Once per application | At app shutdown | Stateless, thread-safe, or expensive to create |
| Scoped | Once per scope/request | At scope end | Request-specific state, DbContext |
| Transient | Every resolution | When scope ends (if IDisposable) | Lightweight, no shared state |

## Factory-Based Registration

Use a factory delegate when construction requires runtime logic.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;

public static class ServiceRegistration
{
    public static IServiceCollection AddStorageServices(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddSingleton<IBlobStorage>(sp =>
        {
            string provider = configuration["Storage:Provider"] ?? "local";

            return provider switch
            {
                "azure" => new AzureBlobStorage(
                    configuration["Storage:Azure:ConnectionString"]!),
                "aws" => new S3BlobStorage(
                    configuration["Storage:Aws:Region"]!,
                    configuration["Storage:Aws:BucketName"]!),
                _ => new LocalBlobStorage(
                    configuration["Storage:Local:Path"] ?? "/data")
            };
        });

        return services;
    }
}
```

## Keyed Services (.NET 8+)

Keyed services allow registering multiple implementations of the same interface, differentiated by a key.

```csharp
using Microsoft.Extensions.DependencyInjection;

public static class ServiceRegistration
{
    public static IServiceCollection AddNotificationServices(
        this IServiceCollection services)
    {
        services.AddKeyedSingleton<INotificationSender, EmailSender>("email");
        services.AddKeyedSingleton<INotificationSender, SmsSender>("sms");
        services.AddKeyedSingleton<INotificationSender, PushSender>("push");

        return services;
    }
}
```

```csharp
using Microsoft.Extensions.DependencyInjection;

public sealed class NotificationService
{
    private readonly INotificationSender _emailSender;
    private readonly INotificationSender _smsSender;

    public NotificationService(
        [FromKeyedServices("email")] INotificationSender emailSender,
        [FromKeyedServices("sms")] INotificationSender smsSender)
    {
        _emailSender = emailSender;
        _smsSender = smsSender;
    }

    public async Task NotifyAsync(string userId, string message, CancellationToken ct)
    {
        await _emailSender.SendAsync(userId, message, ct);
        await _smsSender.SendAsync(userId, message, ct);
    }
}
```

## Multiple Implementations of the Same Interface

When multiple implementations are registered, inject `IEnumerable<T>` to receive all of them.

```csharp
using Microsoft.Extensions.DependencyInjection;

// Registration
builder.Services.AddSingleton<IHealthCheck, DatabaseHealthCheck>();
builder.Services.AddSingleton<IHealthCheck, RedisHealthCheck>();
builder.Services.AddSingleton<IHealthCheck, ExternalApiHealthCheck>();
```

```csharp
// Consumption
public sealed class HealthCheckService
{
    private readonly IEnumerable<IHealthCheck> _checks;

    public HealthCheckService(IEnumerable<IHealthCheck> checks)
    {
        _checks = checks;
    }

    public async Task<HealthReport> CheckAllAsync(CancellationToken ct)
    {
        var results = new List<HealthCheckResult>();

        foreach (IHealthCheck check in _checks)
        {
            HealthCheckResult result = await check.CheckAsync(ct);
            results.Add(result);
        }

        return new HealthReport(results);
    }
}
```

## Decorator Pattern

Wrap an existing registration with additional behavior.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

public static class ServiceRegistration
{
    public static IServiceCollection AddDecoratedRepository(
        this IServiceCollection services)
    {
        // Register the base implementation
        services.AddScoped<SqlOrderRepository>();

        // Register the decorator, resolving the inner service from the container
        services.AddScoped<IOrderRepository>(sp =>
        {
            var inner = sp.GetRequiredService<SqlOrderRepository>();
            var logger = sp.GetRequiredService<ILogger<LoggingOrderRepository>>();
            return new LoggingOrderRepository(inner, logger);
        });

        return services;
    }
}

public sealed class LoggingOrderRepository : IOrderRepository
{
    private readonly IOrderRepository _inner;
    private readonly ILogger<LoggingOrderRepository> _logger;

    public LoggingOrderRepository(IOrderRepository inner, ILogger<LoggingOrderRepository> logger)
    {
        _inner = inner;
        _logger = logger;
    }

    public async Task<Order?> GetByIdAsync(int id, CancellationToken ct)
    {
        _logger.LogDebug("Getting order {OrderId}", id);
        var order = await _inner.GetByIdAsync(id, ct);
        _logger.LogDebug("Order {OrderId} found: {Found}", id, order is not null);
        return order;
    }

    // ... delegate remaining methods to _inner
}
```

## Organizing Registrations with Extension Methods

```csharp
using Microsoft.Extensions.DependencyInjection;

public static class DataAccessExtensions
{
    public static IServiceCollection AddDataAccess(
        this IServiceCollection services, string connectionString)
    {
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlServer(connectionString));
        services.AddScoped<IOrderRepository, SqlOrderRepository>();
        services.AddScoped<IProductRepository, SqlProductRepository>();
        services.AddScoped<ICustomerRepository, SqlCustomerRepository>();
        return services;
    }
}

public static class MessagingExtensions
{
    public static IServiceCollection AddMessaging(this IServiceCollection services)
    {
        services.AddSingleton<IMessageBus, RabbitMqMessageBus>();
        services.AddTransient<IEmailSender, SmtpEmailSender>();
        return services;
    }
}
```

```csharp
// Program.cs stays clean
var builder = Host.CreateApplicationBuilder(args);

builder.Services
    .AddDataAccess(builder.Configuration.GetConnectionString("Default")!)
    .AddMessaging();

var app = builder.Build();
await app.RunAsync();
```

## Validating the Container

Detect missing registrations at startup rather than at runtime.

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

builder.Services.AddApplicationServices();

// In Development, validate that all services can be resolved
if (builder.Environment.IsDevelopment())
{
    builder.Host.UseDefaultServiceProvider(options =>
    {
        options.ValidateScopes = true;   // Detect scoped-in-singleton bugs
        options.ValidateOnBuild = true;  // Verify all registrations resolve
    });
}

var app = builder.Build();
await app.RunAsync();
```

## Best Practices

1. Organize service registrations into focused `IServiceCollection` extension methods grouped by feature or layer (e.g., `AddDataAccess`, `AddMessaging`) and call them from `Program.cs`.
2. Choose lifetimes based on state: use singleton for stateless or thread-safe services, scoped for request-specific state like `DbContext`, and transient only for lightweight, no-state objects.
3. Never inject a scoped service into a singleton service -- this causes the scoped service to act as a singleton (captive dependency); enable `ValidateScopes` in development to detect this.
4. Enable `ValidateOnBuild` in development environments to catch missing registrations at startup rather than discovering them at runtime through `InvalidOperationException`.
5. Prefer constructor injection over `IServiceProvider.GetService` (service locator pattern); injecting `IServiceProvider` hides dependencies and makes code harder to test.
6. Use keyed services (`.AddKeyedSingleton`, `[FromKeyedServices]`) in .NET 8+ instead of custom factory patterns when the same interface has multiple implementations selected by name.
7. Register `IDisposable` and `IAsyncDisposable` services through the container rather than creating them manually, so the container manages their disposal at the correct time.
8. Inject `IEnumerable<T>` to receive all registered implementations of an interface, useful for plugin systems, validation chains, and health checks.
9. Avoid registering services with both a concrete type and an interface separately if they should share the same instance; use a forwarding registration pattern instead.
10. Write integration tests that build the real `IServiceProvider` from your registration code and call `GetRequiredService<T>` for critical services to verify the container is wired correctly.
