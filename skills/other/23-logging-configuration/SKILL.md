---
name: logging-configuration
description: "Configures structured logging with ILogger<T> and ILoggerFactory following Microsoft best practices. Includes Serilog setup, log enrichment, and logging source generators for high-performance logging."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Microsoft.Extensions.Logging, Serilog, Serilog.AspNetCore
---

# Logging Configuration for .NET

## Overview

This skill configures structured logging following Microsoft best practices:

- **ILogger<T>** - Inject into services for category-based logging
- **ILoggerFactory** - Create loggers dynamically when needed
- **Structured Logging** - Preserve log properties for analysis
- **Source Generators** - High-performance compile-time logging
- **Serilog Integration** - Enhanced sinks and enrichers

## Quick Reference

| Interface | Lifetime | Use Case |
|-----------|----------|----------|
| `ILogger<T>` | Singleton | Standard service logging |
| `ILoggerFactory` | Singleton | Create loggers dynamically |
| `ILogger` | - | Non-generic (avoid in DI) |

---

## Logging Structure

```
/Infrastructure/Logging/
├── LoggerConfiguration.cs
├── LogEvents.cs           # LoggerMessage source generators
├── LogEnrichers/
│   ├── UserContextEnricher.cs
│   └── CorrelationIdEnricher.cs
└── Sinks/
    └── CustomSink.cs
```

---

## Template: Service with ILogger<T>

```csharp
// src/{name}.application/Services/OrderService.cs
using Microsoft.Extensions.Logging;

namespace {name}.application.services;

/// <summary>
/// Services should inject ILogger<T> for category-based logging.
/// The category is automatically set to the full type name.
/// </summary>
public sealed class OrderService : IOrderService
{
    private readonly ILogger<OrderService> _logger;
    private readonly IOrderRepository _orderRepository;

    public OrderService(
        ILogger<OrderService> logger,
        IOrderRepository orderRepository)
    {
        _logger = logger;
        _orderRepository = orderRepository;
    }

    public async Task<Result<Order>> ProcessOrderAsync(
        Guid orderId,
        CancellationToken cancellationToken)
    {
        // ═══════════════════════════════════════════════════════════════
        // STRUCTURED LOGGING - Use placeholders, not string interpolation
        // ═══════════════════════════════════════════════════════════════
        _logger.LogInformation(
            "Processing order {OrderId}",
            orderId);

        try
        {
            var order = await _orderRepository.GetByIdAsync(orderId, cancellationToken);

            if (order is null)
            {
                _logger.LogWarning(
                    "Order {OrderId} not found",
                    orderId);

                return Result.Failure<Order>(OrderErrors.NotFound(orderId));
            }

            // Log with multiple properties
            _logger.LogInformation(
                "Order {OrderId} retrieved. Status: {Status}, Total: {Total}",
                orderId,
                order.Status,
                order.Total);

            return Result.Success(order);
        }
        catch (Exception ex)
        {
            // Always log exceptions with the exception parameter first
            _logger.LogError(
                ex,
                "Error processing order {OrderId}",
                orderId);

            throw;
        }
    }
}
```

---

## Template: ILoggerFactory Usage

```csharp
// src/{name}.infrastructure/Services/DynamicLoggerService.cs
using Microsoft.Extensions.Logging;

namespace {name}.infrastructure.services;

/// <summary>
/// Use ILoggerFactory when you need to create loggers dynamically.
/// Common use cases:
/// - Factory classes that create multiple types
/// - Plugin systems where type isn't known at compile time
/// - Base classes that want child-specific categories
/// </summary>
public sealed class PluginManager
{
    private readonly ILoggerFactory _loggerFactory;

    public PluginManager(ILoggerFactory loggerFactory)
    {
        _loggerFactory = loggerFactory;
    }

    public IPlugin LoadPlugin(string pluginName, Type pluginType)
    {
        // Create a logger with a dynamic category
        var logger = _loggerFactory.CreateLogger(pluginType);

        logger.LogInformation(
            "Loading plugin {PluginName} of type {PluginType}",
            pluginName,
            pluginType.Name);

        // Or with a string category
        var customLogger = _loggerFactory.CreateLogger($"Plugins.{pluginName}");

        customLogger.LogDebug(
            "Plugin {PluginName} initialized",
            pluginName);

        return CreatePlugin(pluginType, customLogger);
    }
}
```

---

## Template: High-Performance Logging with Source Generators

```csharp
// src/{name}.application/Logging/LogEvents.cs
using Microsoft.Extensions.Logging;

namespace {name}.application.logging;

/// <summary>
/// LoggerMessage source generators provide the best logging performance.
/// Benefits:
/// - Zero allocation for disabled log levels
/// - Compile-time validation of message templates
/// - Strongly typed parameters
/// </summary>
public static partial class LogEvents
{
    // ═══════════════════════════════════════════════════════════════
    // INFORMATION LEVEL
    // ═══════════════════════════════════════════════════════════════

    [LoggerMessage(
        EventId = 1000,
        Level = LogLevel.Information,
        Message = "Processing request {RequestName} with ID {RequestId}")]
    public static partial void LogRequestProcessing(
        this ILogger logger,
        string requestName,
        Guid requestId);

    [LoggerMessage(
        EventId = 1001,
        Level = LogLevel.Information,
        Message = "Request {RequestName} completed in {ElapsedMs}ms")]
    public static partial void LogRequestCompleted(
        this ILogger logger,
        string requestName,
        long elapsedMs);

    [LoggerMessage(
        EventId = 1002,
        Level = LogLevel.Information,
        Message = "User {UserId} authenticated successfully")]
    public static partial void LogUserAuthenticated(
        this ILogger logger,
        Guid userId);

    // ═══════════════════════════════════════════════════════════════
    // WARNING LEVEL
    // ═══════════════════════════════════════════════════════════════

    [LoggerMessage(
        EventId = 2000,
        Level = LogLevel.Warning,
        Message = "Slow request detected: {RequestName} took {ElapsedMs}ms")]
    public static partial void LogSlowRequest(
        this ILogger logger,
        string requestName,
        long elapsedMs);

    [LoggerMessage(
        EventId = 2001,
        Level = LogLevel.Warning,
        Message = "Cache miss for key {CacheKey}")]
    public static partial void LogCacheMiss(
        this ILogger logger,
        string cacheKey);

    [LoggerMessage(
        EventId = 2002,
        Level = LogLevel.Warning,
        Message = "Rate limit exceeded for client {ClientId}")]
    public static partial void LogRateLimitExceeded(
        this ILogger logger,
        string clientId);

    // ═══════════════════════════════════════════════════════════════
    // ERROR LEVEL
    // ═══════════════════════════════════════════════════════════════

    [LoggerMessage(
        EventId = 3000,
        Level = LogLevel.Error,
        Message = "Error processing request {RequestName}")]
    public static partial void LogRequestError(
        this ILogger logger,
        Exception exception,
        string requestName);

    [LoggerMessage(
        EventId = 3001,
        Level = LogLevel.Error,
        Message = "Database operation failed for entity {EntityType} with ID {EntityId}")]
    public static partial void LogDatabaseError(
        this ILogger logger,
        Exception exception,
        string entityType,
        Guid entityId);

    [LoggerMessage(
        EventId = 3002,
        Level = LogLevel.Error,
        Message = "External service {ServiceName} returned error: {ErrorCode}")]
    public static partial void LogExternalServiceError(
        this ILogger logger,
        string serviceName,
        string errorCode);

    // ═══════════════════════════════════════════════════════════════
    // DEBUG LEVEL
    // ═══════════════════════════════════════════════════════════════

    [LoggerMessage(
        EventId = 4000,
        Level = LogLevel.Debug,
        Message = "Executing query: {QueryName}")]
    public static partial void LogQueryExecution(
        this ILogger logger,
        string queryName);

    [LoggerMessage(
        EventId = 4001,
        Level = LogLevel.Debug,
        Message = "Cache hit for key {CacheKey}")]
    public static partial void LogCacheHit(
        this ILogger logger,
        string cacheKey);
}
```

### Using Source Generated Logs

```csharp
// src/{name}.application/Features/Orders/ProcessOrder/ProcessOrderHandler.cs
public sealed class ProcessOrderHandler : ICommandHandler<ProcessOrderCommand, Guid>
{
    private readonly ILogger<ProcessOrderHandler> _logger;

    public async Task<Result<Guid>> Handle(
        ProcessOrderCommand command,
        CancellationToken cancellationToken)
    {
        // Use extension method from LogEvents
        _logger.LogRequestProcessing("ProcessOrder", command.OrderId);

        var stopwatch = Stopwatch.StartNew();

        try
        {
            // ... process order ...

            stopwatch.Stop();
            _logger.LogRequestCompleted("ProcessOrder", stopwatch.ElapsedMilliseconds);

            return Result.Success(command.OrderId);
        }
        catch (Exception ex)
        {
            _logger.LogRequestError(ex, "ProcessOrder");
            throw;
        }
    }
}
```

---

## Template: Serilog Configuration

```csharp
// src/{name}.api/Program.cs
using Serilog;
using Serilog.Events;

var builder = WebApplication.CreateBuilder(args);

// ═══════════════════════════════════════════════════════════════
// SERILOG CONFIGURATION
// ═══════════════════════════════════════════════════════════════
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .MinimumLevel.Override("Microsoft.Hosting.Lifetime", LogEventLevel.Information)
    .MinimumLevel.Override("Microsoft.EntityFrameworkCore", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithEnvironmentName()
    .Enrich.WithProperty("Application", "MyApp")
    .WriteTo.Console(outputTemplate:
        "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}")
    .WriteTo.File(
        path: "logs/log-.txt",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 30,
        outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}")
    .CreateLogger();

builder.Host.UseSerilog();

// ... rest of configuration ...

var app = builder.Build();

// Request logging middleware
app.UseSerilogRequestLogging(options =>
{
    options.MessageTemplate = "HTTP {RequestMethod} {RequestPath} responded {StatusCode} in {Elapsed:0.0000}ms";
    options.EnrichDiagnosticContext = (diagnosticContext, httpContext) =>
    {
        diagnosticContext.Set("RequestHost", httpContext.Request.Host.Value);
        diagnosticContext.Set("UserAgent", httpContext.Request.Headers["User-Agent"].ToString());
    };
});
```

---

## Template: appsettings.json Logging Configuration

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information",
      "Microsoft.EntityFrameworkCore": "Warning",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning"
    }
  },
  "Serilog": {
    "Using": ["Serilog.Sinks.Console", "Serilog.Sinks.File", "Serilog.Sinks.Seq"],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.EntityFrameworkCore": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "theme": "Serilog.Sinks.SystemConsole.Themes.AnsiConsoleTheme::Code, Serilog.Sinks.Console"
        }
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/log-.txt",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 30
        }
      },
      {
        "Name": "Seq",
        "Args": {
          "serverUrl": "http://localhost:5341"
        }
      }
    ],
    "Enrich": ["FromLogContext", "WithMachineName", "WithEnvironmentName"],
    "Properties": {
      "Application": "MyApp"
    }
  }
}
```

---

## Template: Correlation ID Enricher

```csharp
// src/{name}.infrastructure/Logging/CorrelationIdEnricher.cs
using Serilog.Core;
using Serilog.Events;

namespace {name}.infrastructure.logging;

/// <summary>
/// Enriches all logs with a correlation ID for request tracing.
/// </summary>
public sealed class CorrelationIdEnricher : ILogEventEnricher
{
    private readonly IHttpContextAccessor _httpContextAccessor;
    private const string CorrelationIdHeader = "X-Correlation-ID";
    private const string CorrelationIdProperty = "CorrelationId";

    public CorrelationIdEnricher(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public void Enrich(LogEvent logEvent, ILogEventPropertyFactory propertyFactory)
    {
        var correlationId = GetCorrelationId();

        var property = propertyFactory.CreateProperty(CorrelationIdProperty, correlationId);
        logEvent.AddPropertyIfAbsent(property);
    }

    private string GetCorrelationId()
    {
        var context = _httpContextAccessor.HttpContext;

        if (context is null)
        {
            return Guid.NewGuid().ToString();
        }

        // Try to get from header first
        if (context.Request.Headers.TryGetValue(CorrelationIdHeader, out var headerValue))
        {
            return headerValue.ToString();
        }

        // Generate and store in context
        if (!context.Items.ContainsKey(CorrelationIdProperty))
        {
            context.Items[CorrelationIdProperty] = Guid.NewGuid().ToString();
        }

        return context.Items[CorrelationIdProperty]!.ToString()!;
    }
}
```

---

## Template: User Context Enricher

```csharp
// src/{name}.infrastructure/Logging/UserContextEnricher.cs
using Serilog.Core;
using Serilog.Events;

namespace {name}.infrastructure.logging;

/// <summary>
/// Enriches logs with current user information.
/// </summary>
public sealed class UserContextEnricher : ILogEventEnricher
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public UserContextEnricher(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public void Enrich(LogEvent logEvent, ILogEventPropertyFactory propertyFactory)
    {
        var context = _httpContextAccessor.HttpContext;

        if (context?.User.Identity?.IsAuthenticated != true)
        {
            return;
        }

        var userId = context.User.FindFirst("sub")?.Value
                  ?? context.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

        if (!string.IsNullOrEmpty(userId))
        {
            var property = propertyFactory.CreateProperty("UserId", userId);
            logEvent.AddPropertyIfAbsent(property);
        }

        var userName = context.User.Identity.Name;
        if (!string.IsNullOrEmpty(userName))
        {
            var property = propertyFactory.CreateProperty("UserName", userName);
            logEvent.AddPropertyIfAbsent(property);
        }
    }
}
```

---

## Template: Dependency Injection Registration

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
using Microsoft.Extensions.DependencyInjection;
using Serilog;

namespace {name}.infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // ═══════════════════════════════════════════════════════════════
        // LOGGING CONFIGURATION
        // ═══════════════════════════════════════════════════════════════
        services.AddLogging(loggingBuilder =>
        {
            loggingBuilder.ClearProviders();
            loggingBuilder.AddSerilog(dispose: true);
        });

        // Register enrichers
        services.AddSingleton<CorrelationIdEnricher>();
        services.AddSingleton<UserContextEnricher>();

        return services;
    }
}
```

---

## Template: Scoped Logging with BeginScope

```csharp
// src/{name}.application/Features/Orders/ProcessOrder/ProcessOrderHandler.cs
public sealed class ProcessOrderHandler : ICommandHandler<ProcessOrderCommand, Guid>
{
    private readonly ILogger<ProcessOrderHandler> _logger;

    public async Task<Result<Guid>> Handle(
        ProcessOrderCommand command,
        CancellationToken cancellationToken)
    {
        // ═══════════════════════════════════════════════════════════════
        // SCOPED LOGGING - All logs within scope include these properties
        // ═══════════════════════════════════════════════════════════════
        using (_logger.BeginScope(new Dictionary<string, object>
        {
            ["OrderId"] = command.OrderId,
            ["UserId"] = command.UserId,
            ["Operation"] = "ProcessOrder"
        }))
        {
            _logger.LogInformation("Starting order processing");

            // All logs within this scope automatically include OrderId, UserId, Operation
            await ValidateOrder(command);
            await CalculateTotals(command);
            await ProcessPayment(command);

            _logger.LogInformation("Order processing completed");
        }

        return Result.Success(command.OrderId);
    }
}
```

---

## Log Levels Guide

| Level | Use For |
|-------|---------|
| `Trace` | Detailed debugging (not in production) |
| `Debug` | Development debugging |
| `Information` | General flow, important events |
| `Warning` | Unexpected but handled events |
| `Error` | Failures requiring attention |
| `Critical` | System failures requiring immediate action |

---

## Critical Rules

1. **Always use ILogger<T>** - Category-based logging for traceability
2. **Use structured logging** - `{Property}` placeholders, not string interpolation
3. **Include context** - Add relevant IDs and data to logs
4. **Log at appropriate levels** - Don't use Error for normal flow
5. **Use source generators** - For high-performance hot paths
6. **Don't log sensitive data** - No passwords, tokens, or PII
7. **Include correlation IDs** - For request tracing across services
8. **Configure per-namespace levels** - Reduce noise from frameworks
9. **Use scopes for operations** - Group related logs together
10. **Always pass exceptions first** - `LogError(ex, "Message")` not in message

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: String interpolation
_logger.LogInformation($"Processing order {orderId}");

// ✅ CORRECT: Structured logging with placeholders
_logger.LogInformation("Processing order {OrderId}", orderId);

// ❌ WRONG: Logging sensitive data
_logger.LogInformation("User {Email} logged in with password {Password}", email, password);

// ✅ CORRECT: Redact sensitive data
_logger.LogInformation("User {Email} logged in", email);

// ❌ WRONG: Exception in message
_logger.LogError($"Error: {exception.Message}");

// ✅ CORRECT: Exception as first parameter
_logger.LogError(exception, "Error processing request");

// ❌ WRONG: Injecting ILoggerFactory when ILogger<T> suffices
public class OrderService
{
    private readonly ILogger _logger;
    public OrderService(ILoggerFactory factory)
    {
        _logger = factory.CreateLogger<OrderService>();  // Unnecessary!
    }
}

// ✅ CORRECT: Inject ILogger<T> directly
public class OrderService
{
    private readonly ILogger<OrderService> _logger;
    public OrderService(ILogger<OrderService> logger)
    {
        _logger = logger;
    }
}

// ❌ WRONG: Checking log level unnecessarily (with source generators)
if (_logger.IsEnabled(LogLevel.Debug))
{
    _logger.LogDebug("Value: {Value}", expensiveOperation());
}

// ✅ CORRECT: Source generators handle this automatically
_logger.LogQueryExecution("GetOrderById");  // No-op if Debug disabled
```

---

## Packages Required

```bash
# Core logging
dotnet add package Microsoft.Extensions.Logging

# Serilog (recommended)
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package Serilog.Sinks.File
dotnet add package Serilog.Enrichers.Environment
dotnet add package Serilog.Enrichers.Process

# Optional: Centralized logging
dotnet add package Serilog.Sinks.Seq          # Seq server
dotnet add package Serilog.Sinks.Elasticsearch # Elasticsearch
dotnet add package Serilog.Sinks.ApplicationInsights # Azure
```

---

## Related Skills

- `10-pipeline-behaviors` - Logging behavior for all requests
- `17-health-checks` - Application monitoring
- `01-dotnet-clean-architecture` - Overall architecture
