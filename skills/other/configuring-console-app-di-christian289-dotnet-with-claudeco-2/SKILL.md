---
name: configuring-console-app-di
description: "Implements dependency injection using GenericHost in .NET Console Applications. Use when building console applications that require DI, hosted services, or background tasks."
---

# Console Application DI Pattern

A guide for implementing dependency injection using GenericHost in .NET Console Application.

## 1. Required NuGet Package

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.Hosting" Version="9.0.*" />
</ItemGroup>
```

## 2. Basic Implementation

### 2.1 Program.cs

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {
        services.AddSingleton<IMyService, MyService>();
        services.AddSingleton<App>();
    })
    .Build();

var app = host.Services.GetRequiredService<App>();
await app.RunAsync();
```

### 2.2 App.cs

```csharp
namespace MyApp;

public sealed class App(IMyService myService)
{
    private readonly IMyService _myService = myService;

    public async Task RunAsync()
    {
        await _myService.DoWorkAsync();
    }
}
```

## 3. Service Lifetime

| Lifetime | Description | Use When |
|----------|-------------|----------|
| `Singleton` | Single instance for entire app | Stateless services |
| `Scoped` | Single instance per request | DbContext |
| `Transient` | New instance per injection | Lightweight services |

## 4. Configuration Integration

```csharp
var host = Host.CreateDefaultBuilder(args)
    .ConfigureAppConfiguration((context, config) =>
    {
        config.AddJsonFile("appsettings.json", optional: true);
    })
    .ConfigureServices((context, services) =>
    {
        services.Configure<AppSettings>(
            context.Configuration.GetSection("AppSettings"));
        services.AddSingleton<App>();
    })
    .Build();
```

## 5. Logging Integration

```csharp
public sealed class App(ILogger<App> logger)
{
    public Task RunAsync()
    {
        logger.LogInformation("Application started");
        return Task.CompletedTask;
    }
}
```

## 6. Important Notes

### ⚠️ Avoid Service Locator Pattern

```csharp
// ❌ Bad example
public sealed class BadService(IServiceProvider provider)
{
    public void DoWork()
    {
        var service = provider.GetRequiredService<IMyService>();
    }
}

// ✅ Good example
public sealed class GoodService(IMyService myService)
{
    public void DoWork() { }
}
```

### ⚠️ Captive Dependency

- Singleton should not inject Scoped/Transient dependencies

## 7. References

- [.NET Generic Host](https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host)

