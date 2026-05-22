---
name: pipeline-behaviors
description: "Generates MediatR Pipeline Behaviors for cross-cutting concerns like logging, validation, exception handling, caching, and performance monitoring. Implements the decorator pattern around handlers."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: MediatR, FluentValidation
pattern: Decorator, Chain of Responsibility
---

# MediatR Pipeline Behaviors

## Overview

Pipeline Behaviors implement cross-cutting concerns that execute before/after every command or query handler:

- **Validation** - Validate requests before handler executes
- **Logging** - Log request/response details
- **Exception Handling** - Convert exceptions to Results
- **Transaction** - Wrap handlers in database transactions
- **Caching** - Cache query results
- **Performance** - Monitor slow operations

## Quick Reference

| Behavior | Purpose | Order |
|----------|---------|-------|
| LoggingBehavior | Log requests | First (outer) |
| ValidationBehavior | Validate input | Second |
| ExceptionHandlingBehavior | Convert exceptions | Third |
| TransactionBehavior | Database transaction | Fourth |
| CachingBehavior | Cache responses | Fifth (inner) |

---

## Behavior Structure

```
/Application/Abstractions/Behaviors/
├── LoggingBehavior.cs
├── ValidationBehavior.cs
├── ExceptionHandlingBehavior.cs
├── TransactionBehavior.cs
├── QueryCachingBehavior.cs
└── PerformanceBehavior.cs
```

---

## Template: Logging Behavior

```csharp
// src/{name}.application/Abstractions/Behaviors/LoggingBehavior.cs
using MediatR;
using Microsoft.Extensions.Logging;
using Serilog.Context;

namespace {name}.application.abstractions.behaviors;

/// <summary>
/// Logs all requests and responses with timing information
/// </summary>
public sealed class LoggingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        var requestName = typeof(TRequest).Name;
        var requestId = Guid.NewGuid();

        using (LogContext.PushProperty("RequestId", requestId))
        using (LogContext.PushProperty("RequestName", requestName))
        {
            _logger.LogInformation(
                "Handling {RequestName} ({RequestId})",
                requestName,
                requestId);

            var stopwatch = System.Diagnostics.Stopwatch.StartNew();

            try
            {
                var response = await next();

                stopwatch.Stop();

                _logger.LogInformation(
                    "Handled {RequestName} ({RequestId}) in {ElapsedMs}ms",
                    requestName,
                    requestId,
                    stopwatch.ElapsedMilliseconds);

                return response;
            }
            catch (Exception ex)
            {
                stopwatch.Stop();

                _logger.LogError(
                    ex,
                    "Error handling {RequestName} ({RequestId}) after {ElapsedMs}ms",
                    requestName,
                    requestId,
                    stopwatch.ElapsedMilliseconds);

                throw;
            }
        }
    }
}
```

---

## Template: Validation Behavior

```csharp
// src/{name}.application/Abstractions/Behaviors/ValidationBehavior.cs
using FluentValidation;
using MediatR;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.behaviors;

/// <summary>
/// Validates requests using FluentValidation validators
/// Returns ValidationResult with errors instead of throwing
/// </summary>
public sealed class ValidationBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        if (!_validators.Any())
        {
            return await next();
        }

        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        var errors = validationResults
            .SelectMany(result => result.Errors)
            .Where(failure => failure is not null)
            .Select(failure => new Error(
                failure.PropertyName,
                failure.ErrorMessage))
            .Distinct()
            .ToArray();

        if (errors.Length != 0)
        {
            return CreateValidationResult<TResponse>(errors);
        }

        return await next();
    }

    private static TResponse CreateValidationResult<TResponse>(Error[] errors)
    {
        // Handle Result type
        if (typeof(TResponse) == typeof(Result))
        {
            return (TResponse)(object)ValidationResult.WithErrors(errors);
        }

        // Handle Result<T> type
        var resultType = typeof(TResponse);

        if (resultType.IsGenericType &&
            resultType.GetGenericTypeDefinition() == typeof(Result<>))
        {
            var valueType = resultType.GetGenericArguments()[0];

            var validationResultType = typeof(ValidationResult<>).MakeGenericType(valueType);

            var validationResult = Activator.CreateInstance(
                validationResultType,
                BindingFlags.Instance | BindingFlags.NonPublic,
                null,
                new object[] { errors },
                null);

            return (TResponse)validationResult!;
        }

        throw new InvalidOperationException(
            $"Cannot create validation result for type {typeof(TResponse).Name}");
    }
}
```

---

## Template: Exception Handling Behavior

```csharp
// src/{name}.application/Abstractions/Behaviors/ExceptionHandlingBehavior.cs
using MediatR;
using Microsoft.Extensions.Logging;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.behaviors;

/// <summary>
/// Catches unhandled exceptions and converts them to Result.Failure
/// </summary>
public sealed class ExceptionHandlingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
    where TResponse : Result
{
    private readonly ILogger<ExceptionHandlingBehavior<TRequest, TResponse>> _logger;

    public ExceptionHandlingBehavior(
        ILogger<ExceptionHandlingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        try
        {
            return await next();
        }
        catch (Exception ex)
        {
            var requestName = typeof(TRequest).Name;

            _logger.LogError(
                ex,
                "Unhandled exception for request {RequestName}",
                requestName);

            return CreateExceptionResult<TResponse>(ex);
        }
    }

    private static TResponse CreateExceptionResult<TResponse>(Exception exception)
    {
        var error = new Error(
            "Error.Unhandled",
            exception.Message);

        if (typeof(TResponse) == typeof(Result))
        {
            return (TResponse)(object)Result.Failure(error);
        }

        var resultType = typeof(TResponse);

        if (resultType.IsGenericType &&
            resultType.GetGenericTypeDefinition() == typeof(Result<>))
        {
            var valueType = resultType.GetGenericArguments()[0];

            var failureMethod = typeof(Result)
                .GetMethod(nameof(Result.Failure), new[] { typeof(Error) })!
                .MakeGenericMethod(valueType);

            return (TResponse)failureMethod.Invoke(null, new object[] { error })!;
        }

        throw new InvalidOperationException(
            $"Cannot create exception result for type {typeof(TResponse).Name}");
    }
}
```

---

## Template: Transaction Behavior

```csharp
// src/{name}.application/Abstractions/Behaviors/TransactionBehavior.cs
using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using {name}.application.abstractions.messaging;
using {name}.infrastructure;

namespace {name}.application.abstractions.behaviors;

/// <summary>
/// Wraps command handlers in database transactions
/// Only applies to commands (write operations)
/// </summary>
public sealed class TransactionBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : ICommand<TResponse>  // Only commands
{
    private readonly ApplicationDbContext _dbContext;
    private readonly ILogger<TransactionBehavior<TRequest, TResponse>> _logger;

    public TransactionBehavior(
        ApplicationDbContext dbContext,
        ILogger<TransactionBehavior<TRequest, TResponse>> logger)
    {
        _dbContext = dbContext;
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        var requestName = typeof(TRequest).Name;

        // Check if already in a transaction
        if (_dbContext.Database.CurrentTransaction is not null)
        {
            return await next();
        }

        await using var transaction = await _dbContext.Database
            .BeginTransactionAsync(cancellationToken);

        _logger.LogInformation(
            "Beginning transaction for {RequestName}",
            requestName);

        try
        {
            var response = await next();

            await transaction.CommitAsync(cancellationToken);

            _logger.LogInformation(
                "Committed transaction for {RequestName}",
                requestName);

            return response;
        }
        catch (Exception ex)
        {
            await transaction.RollbackAsync(cancellationToken);

            _logger.LogError(
                ex,
                "Rolled back transaction for {RequestName}",
                requestName);

            throw;
        }
    }
}
```

---

## Template: Query Caching Behavior

```csharp
// src/{name}.application/Abstractions/Caching/ICachedQuery.cs
namespace {name}.application.abstractions.caching;

/// <summary>
/// Marker interface for queries that should be cached
/// </summary>
public interface ICachedQuery
{
    string CacheKey { get; }
    TimeSpan? CacheDuration { get; }
}

/// <summary>
/// Strongly-typed cached query
/// </summary>
public interface ICachedQuery<TResponse> : IQuery<TResponse>, ICachedQuery
{
}
```

```csharp
// src/{name}.application/Abstractions/Behaviors/QueryCachingBehavior.cs
using MediatR;
using Microsoft.Extensions.Caching.Distributed;
using Microsoft.Extensions.Logging;
using System.Text.Json;
using {name}.application.abstractions.caching;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.behaviors;

/// <summary>
/// Caches query results using distributed cache
/// Only applies to queries implementing ICachedQuery
/// </summary>
public sealed class QueryCachingBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : ICachedQuery<TResponse>
    where TResponse : class
{
    private readonly IDistributedCache _cache;
    private readonly ILogger<QueryCachingBehavior<TRequest, TResponse>> _logger;

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    public QueryCachingBehavior(
        IDistributedCache cache,
        ILogger<QueryCachingBehavior<TRequest, TResponse>> logger)
    {
        _cache = cache;
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        var cacheKey = request.CacheKey;

        // Try to get from cache
        var cachedValue = await _cache.GetStringAsync(cacheKey, cancellationToken);

        if (!string.IsNullOrEmpty(cachedValue))
        {
            _logger.LogInformation(
                "Cache hit for {CacheKey}",
                cacheKey);

            return JsonSerializer.Deserialize<TResponse>(cachedValue, JsonOptions)!;
        }

        _logger.LogInformation(
            "Cache miss for {CacheKey}",
            cacheKey);

        // Execute query
        var response = await next();

        // Cache the result if successful
        if (response is Result { IsSuccess: true })
        {
            var cacheOptions = new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = request.CacheDuration ?? TimeSpan.FromMinutes(5)
            };

            var serialized = JsonSerializer.Serialize(response, JsonOptions);

            await _cache.SetStringAsync(
                cacheKey,
                serialized,
                cacheOptions,
                cancellationToken);

            _logger.LogInformation(
                "Cached response for {CacheKey}",
                cacheKey);
        }

        return response;
    }
}
```

### Using Cached Query

```csharp
// src/{name}.application/{Feature}/Get{Entity}ById/Get{Entity}ByIdQuery.cs
public sealed record Get{Entity}ByIdQuery(Guid Id) 
    : ICachedQuery<{Entity}Response>
{
    public string CacheKey => $"{Entity}:{Id}";
    public TimeSpan? CacheDuration => TimeSpan.FromMinutes(10);
}
```

---

## Template: Performance Behavior

```csharp
// src/{name}.application/Abstractions/Behaviors/PerformanceBehavior.cs
using System.Diagnostics;
using MediatR;
using Microsoft.Extensions.Logging;

namespace {name}.application.abstractions.behaviors;

/// <summary>
/// Logs a warning for slow requests (>500ms by default)
/// </summary>
public sealed class PerformanceBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    private readonly ILogger<PerformanceBehavior<TRequest, TResponse>> _logger;
    private readonly Stopwatch _timer;
    private const int SlowRequestThresholdMs = 500;

    public PerformanceBehavior(
        ILogger<PerformanceBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
        _timer = new Stopwatch();
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        _timer.Start();

        var response = await next();

        _timer.Stop();

        var elapsedMs = _timer.ElapsedMilliseconds;

        if (elapsedMs > SlowRequestThresholdMs)
        {
            var requestName = typeof(TRequest).Name;

            _logger.LogWarning(
                "Long running request: {RequestName} ({ElapsedMs}ms) - {@Request}",
                requestName,
                elapsedMs,
                request);
        }

        return response;
    }
}
```

---

## Template: Idempotency Behavior

```csharp
// src/{name}.application/Abstractions/Idempotency/IIdempotentCommand.cs
namespace {name}.application.abstractions.idempotency;

/// <summary>
/// Marker interface for commands that support idempotency
/// </summary>
public interface IIdempotentCommand
{
    Guid IdempotencyKey { get; }
}
```

```csharp
// src/{name}.application/Abstractions/Behaviors/IdempotencyBehavior.cs
using MediatR;
using Microsoft.Extensions.Logging;
using {name}.application.abstractions.idempotency;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.behaviors;

/// <summary>
/// Prevents duplicate command execution using idempotency keys
/// </summary>
public sealed class IdempotencyBehavior<TRequest, TResponse>
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IIdempotentCommand, IRequest<TResponse>
    where TResponse : Result
{
    private readonly IIdempotencyService _idempotencyService;
    private readonly ILogger<IdempotencyBehavior<TRequest, TResponse>> _logger;

    public IdempotencyBehavior(
        IIdempotencyService idempotencyService,
        ILogger<IdempotencyBehavior<TRequest, TResponse>> logger)
    {
        _idempotencyService = idempotencyService;
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        // Check if already processed
        if (await _idempotencyService.ExistsAsync(
            request.IdempotencyKey,
            cancellationToken))
        {
            _logger.LogInformation(
                "Duplicate request detected with key {IdempotencyKey}",
                request.IdempotencyKey);

            // Return cached response or success
            return await _idempotencyService
                .GetResponseAsync<TResponse>(request.IdempotencyKey, cancellationToken)
                ?? CreateSuccessResult<TResponse>();
        }

        var response = await next();

        // Store the response
        await _idempotencyService.SaveAsync(
            request.IdempotencyKey,
            response,
            cancellationToken);

        return response;
    }

    private static TResponse CreateSuccessResult<TResponse>()
    {
        if (typeof(TResponse) == typeof(Result))
        {
            return (TResponse)(object)Result.Success();
        }

        var resultType = typeof(TResponse);

        if (resultType.IsGenericType &&
            resultType.GetGenericTypeDefinition() == typeof(Result<>))
        {
            // Return default success - caller should use cached response instead
            throw new InvalidOperationException(
                "Cannot create default success for generic Result. " +
                "Cached response should be used.");
        }

        throw new InvalidOperationException(
            $"Cannot create success result for type {typeof(TResponse).Name}");
    }
}
```

---

## Registering Behaviors

```csharp
// src/{name}.application/DependencyInjection.cs
using FluentValidation;
using Microsoft.Extensions.DependencyInjection;
using {name}.application.abstractions.behaviors;

namespace {name}.application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(configuration =>
        {
            configuration.RegisterServicesFromAssembly(typeof(DependencyInjection).Assembly);

            // Register behaviors in order (outer to inner)
            // Logging is outermost - sees everything
            configuration.AddOpenBehavior(typeof(LoggingBehavior<,>));

            // Performance monitoring
            configuration.AddOpenBehavior(typeof(PerformanceBehavior<,>));

            // Validation - reject invalid requests early
            configuration.AddOpenBehavior(typeof(ValidationBehavior<,>));

            // Exception handling - convert exceptions to Results
            configuration.AddOpenBehavior(typeof(ExceptionHandlingBehavior<,>));

            // Transaction - wrap commands in transactions
            // Note: Only add if using EF Core directly in Application layer
            // configuration.AddOpenBehavior(typeof(TransactionBehavior<,>));
        });

        services.AddValidatorsFromAssembly(typeof(DependencyInjection).Assembly);

        return services;
    }
}
```

---

## Behavior Execution Order

```
Request
    │
    ▼
┌─────────────────────┐
│  LoggingBehavior    │  ← Outermost: logs request start
│  ┌─────────────────┐│
│  │ PerformanceBeh. ││  ← Starts timer
│  │ ┌─────────────┐ ││
│  │ │ Validation  │ ││  ← Validates request
│  │ │ ┌─────────┐ │ ││
│  │ │ │Exception│ │ ││  ← Catches exceptions
│  │ │ │ ┌─────┐ │ │ ││
│  │ │ │ │Trans.│ │ │ ││  ← Begins transaction
│  │ │ │ │ ┌─┐ │ │ │ ││
│  │ │ │ │ │H│ │ │ │ ││  ← Handler executes
│  │ │ │ │ └─┘ │ │ │ ││
│  │ │ │ └─────┘ │ │ ││  ← Commits/Rolls back
│  │ │ └─────────┘ │ ││  ← Catches, converts to Result
│  │ └─────────────┘ ││  ← Stops timer, logs slow
│  └─────────────────┘│
└─────────────────────┘  ← Logs request end
    │
    ▼
Response
```

---

## Critical Rules

1. **Register order matters** - First registered is outermost
2. **Generic constraints** - Use `where TRequest : ICommand` for command-only behaviors
3. **Don't swallow exceptions** - Log and rethrow or convert to Result
4. **Keep behaviors focused** - One responsibility per behavior
5. **Use open generics** - `typeof(Behavior<,>)` not `typeof(Behavior<Cmd, Resp>)`
6. **Async all the way** - Never block with `.Result` or `.Wait()`
7. **Don't modify request** - Behaviors are observers, not transformers
8. **Transaction behavior last** - Before handler, after validation
9. **Cache reads, not writes** - Only cache query results
10. **Log at appropriate level** - Info for normal, Warning for slow, Error for failures

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Behavior that modifies request
public async Task<TResponse> Handle(...)
{
    request.ModifiedAt = DateTime.UtcNow;  // Don't modify!
    return await next();
}

// ✅ CORRECT: Behaviors observe, don't modify
public async Task<TResponse> Handle(...)
{
    _logger.LogInformation("Processing at {Time}", DateTime.UtcNow);
    return await next();
}

// ❌ WRONG: Swallowing exceptions silently
try { return await next(); }
catch { return default!; }  // Silent failure!

// ✅ CORRECT: Log and convert or rethrow
try { return await next(); }
catch (Exception ex)
{
    _logger.LogError(ex, "Error in handler");
    return CreateFailureResult(ex);
}

// ❌ WRONG: Blocking async code
var result = next().Result;  // Deadlock risk!

// ✅ CORRECT: Await properly
var result = await next();

// ❌ WRONG: Caching commands
public sealed class CachingBehavior<TRequest, TResponse>
    where TRequest : ICommand<TResponse>  // Commands shouldn't be cached!

// ✅ CORRECT: Cache only queries
public sealed class CachingBehavior<TRequest, TResponse>
    where TRequest : ICachedQuery<TResponse>
```

---

## Related Skills

- `cqrs-command-generator` - Commands that flow through behaviors
- `cqrs-query-generator` - Queries that flow through behaviors
- `result-pattern` - Result types used by behaviors
- `dotnet-clean-architecture` - Application layer placement
