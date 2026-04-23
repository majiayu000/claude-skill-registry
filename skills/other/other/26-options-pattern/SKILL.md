---
name: options-pattern
description: "Implements the Options pattern for strongly-typed configuration in .NET. Covers IOptions<T>, IOptionsSnapshot<T>, and IOptionsMonitor<T> with validation and reload support."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Microsoft.Extensions.Options
inspiration: "johnpuksta/clean-architecture-agents (https://github.com/johnpuksta/clean-architecture-agents)"
---

# Options Pattern for .NET Configuration

## Overview

The Options pattern provides strongly-typed access to configuration groups:

- **IOptions<T>** - Singleton, read once at startup
- **IOptionsSnapshot<T>** - Scoped, reloads per request
- **IOptionsMonitor<T>** - Singleton, real-time change notifications

## Quick Reference

| Interface | Lifetime | Supports Reload | Named Options | Use Case |
|-----------|----------|-----------------|---------------|----------|
| `IOptions<T>` | Singleton | No | No | Static config |
| `IOptionsSnapshot<T>` | Scoped | Yes | Yes | Request-scoped config |
| `IOptionsMonitor<T>` | Singleton | Yes | Yes | Singleton services, change notifications |

---

## Options Structure

```
/Application/Options/
├── DatabaseOptions.cs
├── JwtOptions.cs
├── CacheOptions.cs
├── EmailOptions.cs
└── FeatureFlagOptions.cs
```

---

## Template: Basic Options Class

```csharp
// src/{name}.application/Options/DatabaseOptions.cs
namespace {name}.application.options;

/// <summary>
/// Options classes should:
/// - Use the "Options" suffix
/// - Have public getters and setters
/// - Include validation via data annotations or IValidateOptions
/// </summary>
public sealed class DatabaseOptions
{
    /// <summary>
    /// Configuration section name in appsettings.json
    /// </summary>
    public const string SectionName = "Database";

    /// <summary>
    /// Connection string for the primary database
    /// </summary>
    public required string ConnectionString { get; set; }

    /// <summary>
    /// Maximum number of connections in the pool
    /// </summary>
    public int MaxPoolSize { get; set; } = 100;

    /// <summary>
    /// Minimum number of connections in the pool
    /// </summary>
    public int MinPoolSize { get; set; } = 5;

    /// <summary>
    /// Connection timeout in seconds
    /// </summary>
    public int ConnectionTimeout { get; set; } = 30;

    /// <summary>
    /// Enable connection pooling
    /// </summary>
    public bool EnablePooling { get; set; } = true;

    /// <summary>
    /// Enable query logging for debugging
    /// </summary>
    public bool EnableQueryLogging { get; set; } = false;
}
```

### Corresponding appsettings.json

```json
{
  "Database": {
    "ConnectionString": "Host=localhost;Database=mydb;Username=postgres;Password=secret",
    "MaxPoolSize": 100,
    "MinPoolSize": 5,
    "ConnectionTimeout": 30,
    "EnablePooling": true,
    "EnableQueryLogging": false
  }
}
```

---

## Template: Options with Data Annotation Validation

```csharp
// src/{name}.application/Options/JwtOptions.cs
using System.ComponentModel.DataAnnotations;

namespace {name}.application.options;

public sealed class JwtOptions
{
    public const string SectionName = "Jwt";

    [Required(ErrorMessage = "JWT Secret is required")]
    [MinLength(32, ErrorMessage = "JWT Secret must be at least 32 characters")]
    public required string Secret { get; set; }

    [Required(ErrorMessage = "JWT Issuer is required")]
    public required string Issuer { get; set; }

    [Required(ErrorMessage = "JWT Audience is required")]
    public required string Audience { get; set; }

    [Range(1, 1440, ErrorMessage = "Access token expiration must be between 1 and 1440 minutes")]
    public int AccessTokenExpirationMinutes { get; set; } = 15;

    [Range(1, 43200, ErrorMessage = "Refresh token expiration must be between 1 and 43200 minutes")]
    public int RefreshTokenExpirationMinutes { get; set; } = 10080; // 7 days
}
```

---

## Template: Options with Custom Validation

```csharp
// src/{name}.application/Options/CacheOptions.cs
namespace {name}.application.options;

public sealed class CacheOptions
{
    public const string SectionName = "Cache";

    public bool Enabled { get; set; } = true;
    public string? RedisConnectionString { get; set; }
    public int DefaultExpirationMinutes { get; set; } = 5;
    public int SlidingExpirationMinutes { get; set; } = 2;
    public string KeyPrefix { get; set; } = string.Empty;
}

// src/{name}.application/Options/Validation/CacheOptionsValidator.cs
using Microsoft.Extensions.Options;

namespace {name}.application.options.validation;

/// <summary>
/// Custom validation using IValidateOptions for complex rules
/// </summary>
public sealed class CacheOptionsValidator : IValidateOptions<CacheOptions>
{
    public ValidateOptionsResult Validate(string? name, CacheOptions options)
    {
        var failures = new List<string>();

        if (options.Enabled && string.IsNullOrWhiteSpace(options.RedisConnectionString))
        {
            failures.Add("RedisConnectionString is required when caching is enabled");
        }

        if (options.DefaultExpirationMinutes < 1)
        {
            failures.Add("DefaultExpirationMinutes must be at least 1");
        }

        if (options.SlidingExpirationMinutes >= options.DefaultExpirationMinutes)
        {
            failures.Add("SlidingExpirationMinutes must be less than DefaultExpirationMinutes");
        }

        return failures.Count > 0
            ? ValidateOptionsResult.Fail(failures)
            : ValidateOptionsResult.Success;
    }
}
```

---

## Template: Registration in DependencyInjection

```csharp
// src/{name}.application/DependencyInjection.cs
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using {name}.application.options;
using {name}.application.options.validation;

namespace {name}.application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // ═══════════════════════════════════════════════════════════════
        // BASIC OPTIONS BINDING
        // ═══════════════════════════════════════════════════════════════
        services.Configure<DatabaseOptions>(
            configuration.GetSection(DatabaseOptions.SectionName));

        // ═══════════════════════════════════════════════════════════════
        // OPTIONS WITH DATA ANNOTATION VALIDATION
        // Validates at startup - fails fast if invalid
        // ═══════════════════════════════════════════════════════════════
        services.AddOptions<JwtOptions>()
            .Bind(configuration.GetSection(JwtOptions.SectionName))
            .ValidateDataAnnotations()
            .ValidateOnStart();  // Validates immediately at startup

        // ═══════════════════════════════════════════════════════════════
        // OPTIONS WITH CUSTOM VALIDATION
        // ═══════════════════════════════════════════════════════════════
        services.AddOptions<CacheOptions>()
            .Bind(configuration.GetSection(CacheOptions.SectionName))
            .ValidateDataAnnotations()
            .ValidateOnStart();

        services.AddSingleton<IValidateOptions<CacheOptions>, CacheOptionsValidator>();

        // ═══════════════════════════════════════════════════════════════
        // OPTIONS WITH POST-CONFIGURE
        // Modify options after binding
        // ═══════════════════════════════════════════════════════════════
        services.PostConfigure<DatabaseOptions>(options =>
        {
            // Apply environment-specific modifications
            if (string.IsNullOrEmpty(options.ConnectionString))
            {
                options.ConnectionString = Environment.GetEnvironmentVariable("DATABASE_URL")
                    ?? throw new InvalidOperationException("Database connection string not configured");
            }
        });

        return services;
    }
}
```

---

## Template: Using IOptions<T> (Singleton Services)

```csharp
// src/{name}.infrastructure/Services/JwtTokenService.cs
using Microsoft.Extensions.Options;
using {name}.application.options;

namespace {name}.infrastructure.services;

/// <summary>
/// Use IOptions<T> for:
/// - Singleton services
/// - Configuration that doesn't change at runtime
/// - Best performance (read once, cached forever)
/// </summary>
public sealed class JwtTokenService : IJwtTokenService
{
    private readonly JwtOptions _options;

    public JwtTokenService(IOptions<JwtOptions> options)
    {
        // .Value reads the options once
        _options = options.Value;
    }

    public string GenerateAccessToken(User user)
    {
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_options.Secret));

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, user.Email.Value),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
        };

        var token = new JwtSecurityToken(
            issuer: _options.Issuer,
            audience: _options.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_options.AccessTokenExpirationMinutes),
            signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256));

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

---

## Template: Using IOptionsSnapshot<T> (Scoped Services)

```csharp
// src/{name}.application/Features/Email/SendEmail/SendEmailHandler.cs
using Microsoft.Extensions.Options;
using {name}.application.options;

namespace {name}.application.features.email;

/// <summary>
/// Use IOptionsSnapshot<T> for:
/// - Scoped services (per-request in web apps)
/// - Configuration that may change between requests
/// - Named options support
///
/// NOTE: Cannot inject into singleton services!
/// </summary>
public sealed class SendEmailHandler : ICommandHandler<SendEmailCommand, Result>
{
    private readonly EmailOptions _options;
    private readonly IEmailSender _emailSender;

    public SendEmailHandler(
        IOptionsSnapshot<EmailOptions> options,
        IEmailSender emailSender)
    {
        // Gets fresh value for each request
        _options = options.Value;
        _emailSender = emailSender;
    }

    public async Task<Result> Handle(
        SendEmailCommand command,
        CancellationToken cancellationToken)
    {
        if (!_options.Enabled)
        {
            return Result.Success(); // Email disabled
        }

        await _emailSender.SendAsync(
            to: command.To,
            subject: command.Subject,
            body: command.Body,
            from: _options.FromAddress);

        return Result.Success();
    }
}
```

---

## Template: Using IOptionsMonitor<T> (Singleton with Change Notifications)

```csharp
// src/{name}.infrastructure/Services/FeatureFlagService.cs
using Microsoft.Extensions.Options;
using {name}.application.options;

namespace {name}.infrastructure.services;

/// <summary>
/// Use IOptionsMonitor<T> for:
/// - Singleton services that need updated configuration
/// - Real-time configuration changes without restart
/// - Background services and hosted services
/// </summary>
public sealed class FeatureFlagService : IFeatureFlagService, IDisposable
{
    private readonly IOptionsMonitor<FeatureFlagOptions> _optionsMonitor;
    private readonly ILogger<FeatureFlagService> _logger;
    private readonly IDisposable? _changeListener;

    public FeatureFlagService(
        IOptionsMonitor<FeatureFlagOptions> optionsMonitor,
        ILogger<FeatureFlagService> logger)
    {
        _optionsMonitor = optionsMonitor;
        _logger = logger;

        // ═══════════════════════════════════════════════════════════════
        // CHANGE NOTIFICATION
        // Subscribe to configuration changes
        // ═══════════════════════════════════════════════════════════════
        _changeListener = _optionsMonitor.OnChange((options, name) =>
        {
            _logger.LogInformation(
                "Feature flags updated. DarkMode: {DarkMode}, BetaFeatures: {BetaFeatures}",
                options.EnableDarkMode,
                options.EnableBetaFeatures);
        });
    }

    public bool IsEnabled(string featureName)
    {
        // Always gets current value
        var options = _optionsMonitor.CurrentValue;

        return featureName switch
        {
            "DarkMode" => options.EnableDarkMode,
            "BetaFeatures" => options.EnableBetaFeatures,
            "NewCheckout" => options.EnableNewCheckout,
            _ => false
        };
    }

    public void Dispose()
    {
        _changeListener?.Dispose();
    }
}
```

---

## Template: Named Options

```csharp
// src/{name}.application/Options/StorageOptions.cs
namespace {name}.application.options;

public sealed class StorageOptions
{
    public const string SectionName = "Storage";

    // Named option keys
    public const string LocalStorage = "Local";
    public const string CloudStorage = "Cloud";

    public required string BasePath { get; set; }
    public int MaxFileSizeMb { get; set; } = 10;
    public string[] AllowedExtensions { get; set; } = Array.Empty<string>();
}
```

### appsettings.json for Named Options

```json
{
  "Storage": {
    "Local": {
      "BasePath": "./uploads",
      "MaxFileSizeMb": 50,
      "AllowedExtensions": [".jpg", ".png", ".pdf"]
    },
    "Cloud": {
      "BasePath": "https://storage.blob.core.windows.net/uploads",
      "MaxFileSizeMb": 100,
      "AllowedExtensions": [".jpg", ".png", ".pdf", ".zip"]
    }
  }
}
```

### Registration

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
services.Configure<StorageOptions>(
    StorageOptions.LocalStorage,
    configuration.GetSection($"{StorageOptions.SectionName}:{StorageOptions.LocalStorage}"));

services.Configure<StorageOptions>(
    StorageOptions.CloudStorage,
    configuration.GetSection($"{StorageOptions.SectionName}:{StorageOptions.CloudStorage}"));
```

### Usage with Named Options

```csharp
// src/{name}.infrastructure/Services/FileUploadService.cs
public sealed class FileUploadService : IFileUploadService
{
    private readonly StorageOptions _localOptions;
    private readonly StorageOptions _cloudOptions;

    public FileUploadService(IOptionsSnapshot<StorageOptions> optionsSnapshot)
    {
        // Access named options
        _localOptions = optionsSnapshot.Get(StorageOptions.LocalStorage);
        _cloudOptions = optionsSnapshot.Get(StorageOptions.CloudStorage);
    }

    public async Task<string> UploadAsync(
        Stream file,
        string fileName,
        StorageTarget target)
    {
        var options = target switch
        {
            StorageTarget.Local => _localOptions,
            StorageTarget.Cloud => _cloudOptions,
            _ => throw new ArgumentOutOfRangeException(nameof(target))
        };

        // Validate file size
        if (file.Length > options.MaxFileSizeMb * 1024 * 1024)
        {
            throw new InvalidOperationException(
                $"File exceeds maximum size of {options.MaxFileSizeMb}MB");
        }

        // Validate extension
        var extension = Path.GetExtension(fileName).ToLowerInvariant();
        if (!options.AllowedExtensions.Contains(extension))
        {
            throw new InvalidOperationException(
                $"File extension {extension} is not allowed");
        }

        // Upload to appropriate storage
        return await UploadToStorage(file, fileName, options.BasePath);
    }
}
```

---

## Template: Options in Background Services

```csharp
// src/{name}.infrastructure/BackgroundJobs/OutboxProcessorJob.cs
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Options;
using {name}.application.options;

namespace {name}.infrastructure.backgroundjobs;

/// <summary>
/// Background services are singletons - use IOptionsMonitor<T>
/// to get configuration updates without restart.
/// </summary>
public sealed class OutboxProcessorJob : BackgroundService
{
    private readonly IOptionsMonitor<OutboxOptions> _optionsMonitor;
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<OutboxProcessorJob> _logger;

    public OutboxProcessorJob(
        IOptionsMonitor<OutboxOptions> optionsMonitor,
        IServiceScopeFactory scopeFactory,
        ILogger<OutboxProcessorJob> logger)
    {
        _optionsMonitor = optionsMonitor;
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            // Get current options - may have changed since last iteration
            var options = _optionsMonitor.CurrentValue;

            if (!options.Enabled)
            {
                _logger.LogDebug("Outbox processor is disabled");
                await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
                continue;
            }

            try
            {
                await ProcessOutboxMessages(options.BatchSize, stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing outbox messages");
            }

            // Interval can change at runtime
            await Task.Delay(
                TimeSpan.FromSeconds(options.ProcessingIntervalSeconds),
                stoppingToken);
        }
    }

    private async Task ProcessOutboxMessages(int batchSize, CancellationToken ct)
    {
        using var scope = _scopeFactory.CreateScope();
        var processor = scope.ServiceProvider.GetRequiredService<IOutboxProcessor>();
        await processor.ProcessAsync(batchSize, ct);
    }
}
```

---

## Decision Matrix: Which Interface to Use?

```
┌────────────────────────────────────────────────────────────────┐
│                    Which Options Interface?                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Is your service a Singleton?                                   │
│       │                                                         │
│       ├── YES ──► Do you need config updates at runtime?        │
│       │               │                                         │
│       │               ├── YES ──► Use IOptionsMonitor<T>        │
│       │               │                                         │
│       │               └── NO ───► Use IOptions<T>               │
│       │                                                         │
│       └── NO ──► Use IOptionsSnapshot<T>                        │
│                  (works for Scoped and Transient)               │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Critical Rules

1. **Define SectionName constant** - Single source of truth for config path
2. **Validate on startup** - Use `.ValidateOnStart()` to fail fast
3. **Use required keyword** - For mandatory configuration (.NET 7+)
4. **Match interface to lifetime** - IOptions for singleton, IOptionsSnapshot for scoped
5. **Use IOptionsMonitor for background services** - They're singletons
6. **Prefer data annotations** - Simpler than custom validators
7. **Don't inject IOptions into scoped services** - Won't see changes
8. **Use named options for multiple configs** - Same type, different values
9. **Document options** - XML comments for IntelliSense
10. **Set sensible defaults** - Minimize required configuration

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Accessing configuration directly
public class OrderService
{
    public OrderService(IConfiguration configuration)
    {
        var connectionString = configuration["Database:ConnectionString"];
    }
}

// ✅ CORRECT: Use strongly-typed options
public class OrderService
{
    public OrderService(IOptions<DatabaseOptions> options)
    {
        var connectionString = options.Value.ConnectionString;
    }
}

// ❌ WRONG: IOptionsSnapshot in singleton service
public class SingletonService  // Registered as Singleton!
{
    public SingletonService(IOptionsSnapshot<MyOptions> options) // Will fail at runtime!
    {
    }
}

// ✅ CORRECT: Use IOptionsMonitor for singletons that need updates
public class SingletonService
{
    public SingletonService(IOptionsMonitor<MyOptions> options)
    {
        var current = options.CurrentValue;
    }
}

// ❌ WRONG: Not validating options
services.Configure<JwtOptions>(configuration.GetSection("Jwt"));

// ✅ CORRECT: Validate options at startup
services.AddOptions<JwtOptions>()
    .Bind(configuration.GetSection("Jwt"))
    .ValidateDataAnnotations()
    .ValidateOnStart();

// ❌ WRONG: Magic strings for section names
services.Configure<JwtOptions>(configuration.GetSection("Jwt"));
services.Configure<JwtOptions>(configuration.GetSection("JWT"));  // Inconsistent!

// ✅ CORRECT: Use constant for section name
services.Configure<JwtOptions>(configuration.GetSection(JwtOptions.SectionName));
```

---

## Related Skills

- `23-logging-configuration` - Logging configuration using options
- `12-jwt-authentication` - JWT options example
- `15-quartz-background-jobs` - Background services with options
- `01-dotnet-clean-architecture` - Application layer placement
