---
name: extensions-logging
description: >
  Guidance for Microsoft.Extensions.Logging and LoggerMessage source generators.
  USE FOR: ILogger abstraction, LoggerMessage source-generated logging, structured logging with event IDs, log filtering and configuration, high-performance logging patterns.
  DO NOT USE FOR: Serilog-specific sinks and enrichers (use serilog), NLog-specific targets and routing (use nlog), OpenTelemetry log export (use otlp-logging).
license: MIT
metadata:
  displayName: "Microsoft.Extensions.Logging"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Logging in .NET Documentation"
    url: "https://learn.microsoft.com/en-us/dotnet/core/extensions/logging"
  - title: "Microsoft.Extensions.Logging NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.Logging"
  - title: "Compile-Time Logging Source Generation"
    url: "https://learn.microsoft.com/en-us/dotnet/core/extensions/logger-message-generator"
---

# Microsoft.Extensions.Logging

## Overview

`Microsoft.Extensions.Logging` is the built-in logging abstraction for .NET. It provides the `ILogger`, `ILogger<T>`, and `ILoggerFactory` interfaces that decouple application logging from the underlying provider (Console, Debug, EventLog, or third-party sinks like Serilog and NLog). Starting with .NET 6, the `LoggerMessage` source generator enables compile-time generation of high-performance, strongly-typed logging methods that avoid boxing and string allocation at the call site.

This abstraction is integrated into the generic host, ASP.NET Core, and all `Microsoft.Extensions.*` libraries, making it the default choice for any .NET application.

## Basic ILogger Usage

Inject `ILogger<T>` through constructor injection. The type parameter sets the log category name.

```csharp
using Microsoft.Extensions.Logging;

namespace MyApp.Services;

public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public OrderService(ILogger<OrderService> logger)
    {
        _logger = logger;
    }

    public void ProcessOrder(string orderId, decimal total)
    {
        _logger.LogInformation(
            "Processing order {OrderId} with total {Total:C}",
            orderId, total);

        try
        {
            // Business logic here
            _logger.LogDebug(
                "Order {OrderId} validated successfully", orderId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to process order {OrderId}", orderId);
            throw;
        }
    }
}
```

## LoggerMessage Source Generator

The source generator creates optimized logging methods at compile time. Each method avoids boxing, string interpolation, and allocation when the log level is disabled.

```csharp
using Microsoft.Extensions.Logging;

namespace MyApp.Logging;

public static partial class LogMessages
{
    [LoggerMessage(
        EventId = 1001,
        Level = LogLevel.Information,
        Message = "Processing order {OrderId} for customer {CustomerId}")]
    public static partial void OrderProcessing(
        ILogger logger, string orderId, string customerId);

    [LoggerMessage(
        EventId = 1002,
        Level = LogLevel.Information,
        Message = "Order {OrderId} completed in {ElapsedMs}ms")]
    public static partial void OrderCompleted(
        ILogger logger, string orderId, long elapsedMs);

    [LoggerMessage(
        EventId = 2001,
        Level = LogLevel.Error,
        Message = "Order {OrderId} failed")]
    public static partial void OrderFailed(
        ILogger logger, string orderId, Exception exception);

    [LoggerMessage(
        EventId = 3001,
        Level = LogLevel.Warning,
        Message = "Inventory low for product {ProductId}: {Remaining} units")]
    public static partial void InventoryLow(
        ILogger logger, string productId, int remaining);
}
```

Use the generated methods:

```csharp
using Microsoft.Extensions.Logging;
using MyApp.Logging;

namespace MyApp.Services;

public class OrderProcessor
{
    private readonly ILogger<OrderProcessor> _logger;

    public OrderProcessor(ILogger<OrderProcessor> logger)
    {
        _logger = logger;
    }

    public void Process(string orderId, string customerId)
    {
        LogMessages.OrderProcessing(_logger, orderId, customerId);
        var sw = System.Diagnostics.Stopwatch.StartNew();

        try
        {
            // Process order...
            sw.Stop();
            LogMessages.OrderCompleted(
                _logger, orderId, sw.ElapsedMilliseconds);
        }
        catch (Exception ex)
        {
            LogMessages.OrderFailed(_logger, orderId, ex);
            throw;
        }
    }
}
```

## Log Scopes

Scopes attach contextual properties to all log entries within a block, which is essential for correlating logs in distributed systems.

```csharp
using Microsoft.Extensions.Logging;

namespace MyApp.Services;

public class PaymentService
{
    private readonly ILogger<PaymentService> _logger;

    public PaymentService(ILogger<PaymentService> logger)
    {
        _logger = logger;
    }

    public async Task ProcessPaymentAsync(
        string orderId, string transactionId)
    {
        using (_logger.BeginScope(
            new Dictionary<string, object>
            {
                ["OrderId"] = orderId,
                ["TransactionId"] = transactionId
            }))
        {
            _logger.LogInformation("Payment initiated");
            // All logs within this scope include
            // OrderId and TransactionId
            await ChargeAsync();
            _logger.LogInformation("Payment completed");
        }
    }

    private Task ChargeAsync() => Task.CompletedTask;
}
```

## Configuration and Filtering

Configure log levels per category in `appsettings.json`:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning",
      "MyApp.Services": "Debug",
      "MyApp.Services.PaymentService": "Trace"
    },
    "Console": {
      "LogLevel": {
        "Default": "Information"
      },
      "FormatterName": "json",
      "FormatterOptions": {
        "IncludeScopes": true,
        "TimestampFormat": "yyyy-MM-dd HH:mm:ss "
      }
    }
  }
}
```

Register providers programmatically:

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

var builder = WebApplication.CreateBuilder(args);

builder.Logging
    .ClearProviders()
    .AddConsole()
    .AddDebug()
    .SetMinimumLevel(LogLevel.Debug)
    .AddFilter("Microsoft", LogLevel.Warning)
    .AddFilter<Microsoft.Extensions.Logging.Console.ConsoleLoggerProvider>(
        "MyApp", LogLevel.Debug);

var app = builder.Build();
app.Run();
```

## Log Level Reference

| Level | Value | Use Case |
|---|---|---|
| Trace | 0 | Detailed diagnostic data, never in production |
| Debug | 1 | Developer-facing diagnostic information |
| Information | 2 | General application flow events |
| Warning | 3 | Abnormal or unexpected events that do not cause failure |
| Error | 4 | Failures in the current operation (not app-wide) |
| Critical | 5 | Application-wide failures requiring immediate attention |
| None | 6 | Disables logging for a category |

## LoggerMessage vs Manual Logging

| Aspect | `LoggerMessage` Source Gen | Manual `_logger.LogX(...)` |
|---|---|---|
| Performance | Zero-alloc when level disabled | Allocates params array |
| Boxing | Avoided via generated code | Occurs for value types |
| Compile-time validation | Message template checked | Runtime only |
| Event ID management | Enforced by attribute | Easy to forget |
| Code organization | Centralized in partial class | Scattered across codebase |
| Discoverability | Searchable by event ID | Grep for string patterns |

## Best Practices

1. **Use `LoggerMessage` source generators** for all logging in hot paths and production services to eliminate allocation overhead when the target log level is disabled.
2. **Assign unique `EventId` values** to each log message and document them; event IDs enable precise log filtering and alerting without relying on fragile string matching.
3. **Use structured log templates** (`"Order {OrderId} processed"`) instead of string interpolation (`$"Order {orderId} processed"`) so log aggregators can index and query named properties.
4. **Configure log levels per category** in `appsettings.json` rather than in code, so operations teams can adjust verbosity without redeploying the application.
5. **Use `BeginScope`** to attach correlation IDs, request IDs, and tenant IDs to all log entries within a logical operation for distributed tracing.
6. **Never log sensitive data** (passwords, tokens, PII) even at `Trace` level; use the `[LogProperties(OmitReferenceName = true)]` attribute or redact explicitly.
7. **Set `Microsoft.AspNetCore` and `Microsoft.EntityFrameworkCore`** to `Warning` or higher in production to reduce noise from framework-internal logs.
8. **Organize `LoggerMessage` methods** in a single static partial class per bounded context (e.g., `OrderLogMessages`, `PaymentLogMessages`) with contiguous event ID ranges.
9. **Test that critical error paths produce the expected log entries** by injecting `Microsoft.Extensions.Logging.Testing.FakeLogger` or a similar test double in unit tests.
10. **Prefer `ILogger<T>` over `ILogger`** for constructor injection because the generic version automatically sets the category name to the fully-qualified type name.
