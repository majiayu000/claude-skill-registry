---
name: koan-bootstrap
description: Auto-registration via KoanAutoRegistrar, minimal Program.cs, "Reference = Intent" pattern
---

# Koan Bootstrap & Auto-Registration

## Core Principle

**`services.AddKoan()` is the ONLY line needed in Program.cs.** The framework discovers and registers everything through auto-registration. No manual service registration. No manual configuration. Just add package references and everything wires up automatically.

## Revolutionary "Reference = Intent" Pattern

Adding a package reference **automatically enables functionality**:

```xml
<!-- Add MongoDB connector -->
<PackageReference Include="Koan.Data.Connector.Mongo" Version="0.6.3" />
<!-- Now MongoDB is discovered, configured, and available automatically -->

<!-- Add AI capabilities -->
<PackageReference Include="Koan.AI" Version="0.6.3" />
<!-- Now AI services are auto-registered and ready to use -->
```

No manual registration in Program.cs. The framework handles everything.

## Minimal Program.cs Template

```csharp
using Koan.Core;

var builder = WebApplication.CreateBuilder(args);

// ONE LINE - framework handles all dependencies
builder.Services.AddKoan();

var app = builder.Build();

// Middleware auto-configured by framework
app.Run();
```

**That's it.** 8 lines total. No manual service registration. No manual middleware configuration. The framework discovers:
- Data adapters
- AI providers
- Authentication providers
- Entity controllers
- Background services
- Message queues
- Everything else

## When This Skill Applies

Invoke this skill when:
- ✅ Setting up new projects
- ✅ Debugging initialization issues
- ✅ Adding framework modules
- ✅ Troubleshooting boot failures
- ✅ Creating application-specific services
- ✅ Understanding assembly discovery

## KoanAutoRegistrar Pattern

### What It Is

`KoanAutoRegistrar` is how you register **application-specific services** (not framework services - those auto-register). Create one per application/module.

### When to Create One

Create `KoanAutoRegistrar` when you have:
- Application-specific business logic services
- Custom background workers
- Domain-specific infrastructure
- Third-party service integrations

### Template

```csharp
// File: /Initialization/KoanAutoRegistrar.cs
using Koan.Core;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;

namespace MyApp.Initialization;

public sealed class KoanAutoRegistrar : IKoanAutoRegistrar
{
    public string ModuleName => "MyApp";

    public string? ModuleVersion =>
        typeof(KoanAutoRegistrar).Assembly.GetName().Version?.ToString();

    public void Initialize(IServiceCollection services)
    {
        // Register application-specific services here
        services.AddScoped<ITodoService, TodoService>();
        services.AddScoped<IEmailService, EmailService>();
        services.AddSingleton<ICacheService, RedisCacheService>();
        services.AddHostedService<BackgroundCleanupWorker>();
    }

    public void Describe(BootReport report, IConfiguration cfg, IHostEnvironment env)
    {
        report.AddModule(ModuleName, ModuleVersion);
        report.AddNote("Application services registered");
        report.AddNote($"Environment: {env.EnvironmentName}");
    }
}
```

### Discovery Rules

The framework automatically discovers `IKoanAutoRegistrar` implementations:

1. **Assembly Scanning**: Scans all loaded assemblies at startup
2. **Interface Detection**: Finds types implementing `IKoanAutoRegistrar`
3. **Instantiation**: Creates instance and calls `Initialize()`
4. **Boot Reporting**: Calls `Describe()` to populate boot report

**You don't call it.** The framework finds and executes it automatically.

## What NOT to Do

### ❌ WRONG: Manual Service Registration in Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

// ❌ DON'T DO THIS - breaks auto-registration pattern
builder.Services.AddScoped<ITodoRepository, TodoRepository>();
builder.Services.AddDbContext<MyDbContext>();
builder.Services.AddScoped<ITodoService, TodoService>();

builder.Services.AddKoan(); // Too late, order matters
```

**Why wrong?**
- Breaks "Reference = Intent" pattern
- Creates registration order dependencies
- Duplicates framework auto-registration
- Makes Program.cs grow uncontrollably

### ✅ CORRECT: Use KoanAutoRegistrar

```csharp
// Program.cs stays minimal
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddKoan();
var app = builder.Build();
app.Run();

// Application services in KoanAutoRegistrar
public sealed class KoanAutoRegistrar : IKoanAutoRegistrar
{
    public void Initialize(IServiceCollection services)
    {
        services.AddScoped<ITodoService, TodoService>();
    }
}
```

### ❌ WRONG: Multiple AddKoan() Calls

```csharp
// ❌ DON'T DO THIS
builder.Services.AddKoan();
builder.Services.AddKoanData();    // Redundant
builder.Services.AddKoanWeb();     // Redundant
builder.Services.AddKoanAI();      // Redundant
```

**Why wrong?** `AddKoan()` already discovers and registers ALL Koan modules automatically.

### ✅ CORRECT: Single AddKoan()

```csharp
builder.Services.AddKoan(); // Discovers and registers everything
```

## Boot Report & Diagnostics

### Viewing Boot Report

```csharp
// In Development environment
if (KoanEnv.IsDevelopment)
{
    var logger = app.Services.GetRequiredService<ILogger<Program>>();
    KoanEnv.DumpSnapshot(logger);
}
```

**Output shows:**
```
[INFO] Koan:discover postgresql: server=localhost;database=myapp... OK
[INFO] Koan:modules data→postgresql
[INFO] Koan:modules web→controllers
[INFO] Koan:modules ai→openai
[INFO] Koan:modules MyApp v1.0.0
```

### Boot Report Structure

```csharp
public void Describe(BootReport report, IConfiguration cfg, IHostEnvironment env)
{
    // Add module to report
    report.AddModule(ModuleName, ModuleVersion);

    // Add informational notes
    report.AddNote("Services registered: TodoService, EmailService");
    report.AddNote($"Data source: {cfg["Koan:Data:Sources:Default:Adapter"]}");

    // Add warnings if needed
    if (!cfg.GetSection("Email:Smtp").Exists())
    {
        report.AddWarning("Email configuration missing - notifications disabled");
    }
}
```

## Environment Detection

Use `KoanEnv` for environment-aware logic:

```csharp
public void Initialize(IServiceCollection services)
{
    // Development-only services
    if (KoanEnv.IsDevelopment)
    {
        services.AddScoped<ISeedService, DevelopmentSeedService>();
    }

    // Production-only services
    if (KoanEnv.IsProduction)
    {
        services.AddSingleton<IEmailService, SendGridEmailService>();
    }

    // Container-specific configuration
    if (KoanEnv.InContainer)
    {
        services.AddSingleton<IHealthCheckService, ContainerHealthCheck>();
    }

    // Dangerous operations gated by flag
    if (KoanEnv.AllowMagicInProduction)
    {
        services.AddScoped<IAdminService, AdminService>();
    }
}
```

## Configuration Reading

Use framework configuration helpers:

```csharp
public void Initialize(IServiceCollection services)
{
    var sp = services.BuildServiceProvider();
    var cfg = sp.GetRequiredService<IConfiguration>();

    // Read with fallback chain: setting → env var → default
    var apiKey = Configuration.Read(
        cfg,
        defaultValue: "dev-key",
        "App:ApiKey",           // Config path
        "APP_API_KEY"           // Environment variable
    );

    services.AddSingleton(new ExternalApiClient(apiKey));
}
```

## Debugging Bootstrap Issues

### Symptom: Service Not Found

```
System.InvalidOperationException: Unable to resolve service for type 'ITodoService'
```

**Cause:** `KoanAutoRegistrar` not discovered or not registering service

**Solution:**
1. Verify file exists at `/Initialization/KoanAutoRegistrar.cs`
2. Verify class implements `IKoanAutoRegistrar`
3. Verify class is `public` and not `internal`
4. Check boot logs for module registration

### Symptom: Provider Not Available

```
[ERROR] Koan:discover mongodb: connection failed
[INFO] Koan:modules data→json (fallback)
```

**Cause:** Provider package referenced but connection failed

**Solution:**
1. Verify connection string in `appsettings.json`
2. Check service is running (Docker, local install)
3. Verify network connectivity
4. Check boot report for detailed error

### Symptom: Assembly Not Loaded

```
[WARNING] Koan:modules MyModule not discovered
```

**Cause:** Assembly not referenced or not loaded at startup

**Solution:**
1. Verify `<ProjectReference>` or `<PackageReference>` exists
2. Check assembly is copied to output directory
3. Add explicit assembly reference if needed:
   ```csharp
   var assembly = Assembly.Load("MyModule");
   ```

## Bundled Templates

- `templates/Program.cs.template` - Minimal Program.cs
- `templates/KoanAutoRegistrar.cs.template` - Complete registrar template
- `templates/KoanAutoRegistrar-with-options.cs.template` - Registrar with configuration options
- `templates/appsettings.json.template` - Koan configuration structure

## Reference Documentation

- **Full Guide:** `docs/guides/deep-dive/bootstrap-lifecycle.md`
- **Troubleshooting:** `docs/guides/troubleshooting/bootstrap-failures.md`
- **Auto-Provisioning:** `docs/guides/deep-dive/auto-provisioning-system.md`
- **Sample:** `samples/S0.ConsoleJsonRepo/Program.cs` (Minimal 20-line bootstrap)
- **Sample:** `samples/S1.Web/Program.cs` (Web bootstrap with lifecycle)

## Advanced: Module Loading Order

Modules load in this order:

1. **Core** - Foundation services
2. **Data** - Repository abstractions
3. **Adapters** - Concrete providers (Mongo, Postgres, etc.)
4. **Domain** - Entity registrations
5. **Web** - Controllers, middleware
6. **Application** - Your `KoanAutoRegistrar`

Dependencies are resolved automatically. You never need to specify order manually.

## Advanced: Conditional Registration

```csharp
public void Initialize(IServiceCollection services)
{
    var sp = services.BuildServiceProvider();
    var cfg = sp.GetRequiredService<IConfiguration>();

    // Feature flags
    if (cfg.GetValue<bool>("Features:EmailNotifications"))
    {
        services.AddScoped<INotificationService, EmailNotificationService>();
    }
    else
    {
        services.AddScoped<INotificationService, NoOpNotificationService>();
    }

    // Provider-specific services
    var dataProvider = cfg["Koan:Data:Sources:Default:Adapter"];
    if (dataProvider == "mongodb")
    {
        services.AddSingleton<IMongoIndexManager, MongoIndexManager>();
    }
}
```

## Framework Compliance

Bootstrap patterns are **mandatory** in Koan Framework:

- ✅ Use `AddKoan()` for all framework registration
- ✅ Use `KoanAutoRegistrar` for application services
- ✅ Keep Program.cs minimal (under 20 lines)
- ❌ Never manually register framework services
- ❌ Never duplicate framework configuration
- ❌ Never call `AddDbContext`, `AddControllers`, etc. manually

The framework handles everything through auto-discovery.
