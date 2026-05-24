---
name: lang-dotnet-dev
description: Foundational .NET patterns covering runtime, project structure, dependency injection, configuration, metaprogramming, and cross-platform development. Use when working with .NET projects or CLI tools. This is the entry point for .NET development.
---

# .NET Development Skill

Comprehensive foundational patterns for .NET development, covering runtime fundamentals, project structure, dependency injection, configuration management, logging, middleware, metaprogramming, and cross-platform development.

## Table of Contents

- [.NET Runtime and SDK](#net-runtime-and-sdk)
- [Project Structure](#project-structure)
- [CLI Tools](#cli-tools)
- [Project Types](#project-types)
- [Dependency Injection](#dependency-injection)
- [Configuration](#configuration)
- [Logging](#logging)
- [Middleware Patterns](#middleware-patterns)
- [NuGet Packages](#nuget-packages)
- [Cross-Platform Development](#cross-platform-development)
- [Metaprogramming](#metaprogramming)
- [Best Practices](#best-practices)
- [Cross-Cutting Patterns](#cross-cutting-patterns)

## .NET Runtime and SDK

### Runtime Components

The .NET runtime provides the execution environment for .NET applications.

```csharp
// Runtime information
using System;
using System.Runtime.InteropServices;

public class RuntimeInfo
{
    public static void DisplayRuntimeInfo()
    {
        // Framework description
        Console.WriteLine($"Framework: {RuntimeInformation.FrameworkDescription}");

        // OS description
        Console.WriteLine($"OS: {RuntimeInformation.OSDescription}");

        // Architecture
        Console.WriteLine($"Architecture: {RuntimeInformation.OSArchitecture}");

        // Process architecture
        Console.WriteLine($"Process: {RuntimeInformation.ProcessArchitecture}");

        // Runtime identifier
        Console.WriteLine($"RID: {RuntimeInformation.RuntimeIdentifier}");
    }
}
```

### SDK vs Runtime

```bash
# Check installed SDKs
dotnet --list-sdks

# Check installed runtimes
dotnet --list-runtimes

# Check SDK version
dotnet --version

# Display all info
dotnet --info
```

### Global.json Configuration

```json
{
  "sdk": {
    "version": "8.0.0",
    "rollForward": "latestMinor",
    "allowPrerelease": false
  }
}
```

```bash
# Create global.json with specific SDK version
dotnet new globaljson --sdk-version 8.0.100

# Roll forward policies:
# - patch: Use latest patch version
# - feature: Use latest feature band
# - minor: Use latest minor version
# - major: Use latest major version
# - latestPatch: Use latest patch (default)
# - latestMinor: Use latest minor
# - latestMajor: Use latest major
# - disable: Use exact version
```

### .NET Standard vs .NET

```csharp
// Target Framework Monikers (TFM)

// Modern .NET (cross-platform)
// <TargetFramework>net8.0</TargetFramework>
// <TargetFramework>net7.0</TargetFramework>
// <TargetFramework>net6.0</TargetFramework>

// .NET Standard (compatibility layer)
// <TargetFramework>netstandard2.1</TargetFramework>
// <TargetFramework>netstandard2.0</TargetFramework>

// .NET Framework (Windows only)
// <TargetFramework>net48</TargetFramework>
// <TargetFramework>net472</TargetFramework>

// Multi-targeting
// <TargetFrameworks>net8.0;net6.0;netstandard2.0</TargetFrameworks>

// Conditional compilation
#if NET8_0_OR_GREATER
    // Code for .NET 8+
#elif NET6_0_OR_GREATER
    // Code for .NET 6+
#elif NETSTANDARD2_0
    // Code for .NET Standard 2.0
#endif
```

### Runtime Configuration

```json
// runtimeconfig.json
{
  "runtimeOptions": {
    "tfm": "net8.0",
    "framework": {
      "name": "Microsoft.NETCore.App",
      "version": "8.0.0"
    },
    "configProperties": {
      "System.GC.Server": true,
      "System.GC.Concurrent": true,
      "System.GC.RetainVM": true,
      "System.Runtime.Serialization.EnableUnsafeBinaryFormatterSerialization": false
    }
  }
}
```

## Project Structure

### Project File (.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <!-- Basic Properties -->
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <OutputType>Exe</OutputType>
    <RootNamespace>MyCompany.MyProduct</RootNamespace>
    <AssemblyName>MyProduct</AssemblyName>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <!-- Package Properties -->
  <PropertyGroup>
    <PackageId>MyCompany.MyProduct</PackageId>
    <Version>1.0.0</Version>
    <Authors>Your Name</Authors>
    <Company>MyCompany</Company>
    <Product>MyProduct</Product>
    <Description>Package description</Description>
    <Copyright>Copyright © 2024</Copyright>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
    <PackageProjectUrl>https://github.com/mycompany/myproduct</PackageProjectUrl>
    <RepositoryUrl>https://github.com/mycompany/myproduct</RepositoryUrl>
    <RepositoryType>git</RepositoryType>
    <PackageTags>tag1;tag2;tag3</PackageTags>
    <GeneratePackageOnBuild>false</GeneratePackageOnBuild>
  </PropertyGroup>

  <!-- Build Properties -->
  <PropertyGroup>
    <Configuration Condition=" '$(Configuration)' == '' ">Debug</Configuration>
    <Platform Condition=" '$(Platform)' == '' ">AnyCPU</Platform>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
    <WarningsAsErrors />
    <NoWarn>CS1591</NoWarn>
    <GenerateDocumentationFile>true</GenerateDocumentationFile>
  </PropertyGroup>

  <!-- Debug Configuration -->
  <PropertyGroup Condition="'$(Configuration)' == 'Debug'">
    <DebugType>full</DebugType>
    <DebugSymbols>true</DebugSymbols>
    <Optimize>false</Optimize>
    <DefineConstants>DEBUG;TRACE</DefineConstants>
  </PropertyGroup>

  <!-- Release Configuration -->
  <PropertyGroup Condition="'$(Configuration)' == 'Release'">
    <DebugType>pdbonly</DebugType>
    <DebugSymbols>true</DebugSymbols>
    <Optimize>true</Optimize>
    <DefineConstants>TRACE</DefineConstants>
  </PropertyGroup>

  <!-- Package References -->
  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
    <PackageReference Include="Microsoft.Extensions.Configuration" Version="8.0.0" />
    <PackageReference Include="Microsoft.Extensions.Logging" Version="8.0.0" />
  </ItemGroup>

  <!-- Project References -->
  <ItemGroup>
    <ProjectReference Include="..\MyLibrary\MyLibrary.csproj" />
  </ItemGroup>

  <!-- Conditional Package References -->
  <ItemGroup Condition="'$(TargetFramework)' == 'net8.0'">
    <PackageReference Include="System.Text.Json" Version="8.0.0" />
  </ItemGroup>

  <!-- Content Files -->
  <ItemGroup>
    <Content Include="appsettings.json">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    </Content>
    <Content Include="appsettings.*.json">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
      <DependentUpon>appsettings.json</DependentUpon>
    </Content>
  </ItemGroup>

  <!-- Embedded Resources -->
  <ItemGroup>
    <EmbeddedResource Include="Resources\*.txt" />
  </ItemGroup>

  <!-- None Items -->
  <ItemGroup>
    <None Include="README.md" Pack="true" PackagePath="\" />
    <None Include="LICENSE" Pack="true" PackagePath="\" />
  </ItemGroup>

</Project>
```

### Solution File (.sln)

```bash
# Create a new solution
dotnet new sln -n MySolution

# Add projects to solution
dotnet sln add src/MyApp/MyApp.csproj
dotnet sln add src/MyLibrary/MyLibrary.csproj
dotnet sln add tests/MyApp.Tests/MyApp.Tests.csproj

# List projects in solution
dotnet sln list

# Remove project from solution
dotnet sln remove src/OldProject/OldProject.csproj
```

### Directory Structure

```
MySolution/
├── .gitignore
├── .editorconfig
├── global.json
├── MySolution.sln
├── Directory.Build.props         # Shared properties for all projects
├── Directory.Build.targets       # Shared targets for all projects
├── Directory.Packages.props      # Central package management
├── src/
│   ├── MyApp/
│   │   ├── MyApp.csproj
│   │   ├── Program.cs
│   │   ├── appsettings.json
│   │   ├── appsettings.Development.json
│   │   └── Controllers/
│   │       └── WeatherController.cs
│   └── MyLibrary/
│       ├── MyLibrary.csproj
│       ├── Class1.cs
│       └── Interfaces/
│           └── IMyService.cs
├── tests/
│   ├── MyApp.Tests/
│   │   ├── MyApp.Tests.csproj
│   │   └── UnitTest1.cs
│   └── MyLibrary.Tests/
│       ├── MyLibrary.Tests.csproj
│       └── Class1Tests.cs
├── docs/
│   └── README.md
└── tools/
    └── build.ps1
```

### Directory.Build.props

```xml
<Project>

  <!-- Common properties for all projects -->
  <PropertyGroup>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>

  <!-- Version properties -->
  <PropertyGroup>
    <VersionPrefix>1.0.0</VersionPrefix>
    <VersionSuffix Condition="'$(Configuration)' == 'Debug'">dev</VersionSuffix>
  </PropertyGroup>

  <!-- Source Link (for debugging) -->
  <PropertyGroup>
    <PublishRepositoryUrl>true</PublishRepositoryUrl>
    <EmbedUntrackedSources>true</EmbedUntrackedSources>
    <IncludeSymbols>true</IncludeSymbols>
    <SymbolPackageFormat>snupkg</SymbolPackageFormat>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.SourceLink.GitHub" Version="8.0.0" PrivateAssets="All" />
  </ItemGroup>

</Project>
```

### Directory.Packages.props (Central Package Management)

```xml
<Project>

  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>

  <ItemGroup>
    <!-- Common packages -->
    <PackageVersion Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
    <PackageVersion Include="Microsoft.Extensions.Configuration" Version="8.0.0" />
    <PackageVersion Include="Microsoft.Extensions.Logging" Version="8.0.0" />

    <!-- Test packages -->
    <PackageVersion Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageVersion Include="xunit" Version="2.6.2" />
    <PackageVersion Include="xunit.runner.visualstudio" Version="2.5.4" />
    <PackageVersion Include="coverlet.collector" Version="6.0.0" />
  </ItemGroup>

</Project>
```

## CLI Tools

### dotnet new

```bash
# List available templates
dotnet new list

# Common templates
dotnet new console -n MyConsoleApp
dotnet new classlib -n MyLibrary
dotnet new web -n MyWebApp
dotnet new webapi -n MyApi
dotnet new mvc -n MyMvcApp
dotnet new razor -n MyRazorApp
dotnet new blazorserver -n MyBlazorApp
dotnet new blazorwasm -n MyBlazorWasmApp
dotnet new worker -n MyWorkerService
dotnet new xunit -n MyTests
dotnet new nunit -n MyNUnitTests
dotnet new mstest -n MyMSTests

# Create with options
dotnet new console -n MyApp -f net8.0 -o src/MyApp
dotnet new webapi -n MyApi --use-controllers --auth Individual

# Install templates
dotnet new install Amazon.Lambda.Templates
dotnet new install Microsoft.AspNetCore.SpaTemplates

# Uninstall templates
dotnet new uninstall Amazon.Lambda.Templates

# Create from template with language
dotnet new console -n MyApp -lang "F#"
dotnet new classlib -n MyLib -lang "VB"
```

### dotnet build

```bash
# Build project
dotnet build

# Build with configuration
dotnet build -c Release
dotnet build --configuration Debug

# Build specific framework
dotnet build -f net8.0

# Build with no dependencies
dotnet build --no-dependencies

# Build with no restore
dotnet build --no-restore

# Build with specific runtime
dotnet build -r win-x64
dotnet build -r linux-x64
dotnet build -r osx-x64
dotnet build -r osx-arm64

# Build verbosity
dotnet build -v quiet
dotnet build -v minimal
dotnet build -v normal
dotnet build -v detailed
dotnet build -v diagnostic

# Build and output to directory
dotnet build -o ./output
```

### dotnet run

```bash
# Run project
dotnet run

# Run with configuration
dotnet run -c Release

# Run with framework
dotnet run -f net8.0

# Run with arguments
dotnet run -- arg1 arg2
dotnet run --project ./src/MyApp/MyApp.csproj

# Run with environment
dotnet run --environment Production
ASPNETCORE_ENVIRONMENT=Production dotnet run

# Run without build
dotnet run --no-build

# Run without restore
dotnet run --no-restore

# Run with launch profile
dotnet run --launch-profile "Production"
```

### dotnet publish

```bash
# Publish for deployment
dotnet publish

# Publish with configuration
dotnet publish -c Release

# Publish with runtime (self-contained)
dotnet publish -r win-x64 --self-contained
dotnet publish -r linux-x64 -p:PublishSingleFile=true
dotnet publish -r osx-arm64 --self-contained

# Publish framework-dependent
dotnet publish -r win-x64 --self-contained false

# Publish with trimming
dotnet publish -c Release -r linux-x64 --self-contained -p:PublishTrimmed=true
dotnet publish -c Release -p:PublishTrimmed=true -p:TrimMode=full

# Publish as single file
dotnet publish -r win-x64 -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfContained=true

# Publish ReadyToRun
dotnet publish -c Release -r win-x64 -p:PublishReadyToRun=true

# Publish to folder
dotnet publish -o ./publish

# Publish with version
dotnet publish -p:Version=1.2.3
```

### dotnet restore

```bash
# Restore dependencies
dotnet restore

# Restore with specific source
dotnet restore --source https://api.nuget.org/v3/index.json
dotnet restore -s ./local-packages

# Restore for specific runtime
dotnet restore -r win-x64

# Restore with locked mode (use packages.lock.json)
dotnet restore --locked-mode

# Force evaluation of all dependencies
dotnet restore --force

# Restore without cache
dotnet restore --no-cache
```

### dotnet test

```bash
# Run tests
dotnet test

# Run tests with configuration
dotnet test -c Release

# Run tests with verbosity
dotnet test -v normal
dotnet test --verbosity detailed

# Run tests with filter
dotnet test --filter FullyQualifiedName~MyNamespace
dotnet test --filter Category=Unit
dotnet test --filter "Priority=1|Category=Smoke"

# Run tests with coverage
dotnet test --collect:"XPlat Code Coverage"
dotnet test /p:CollectCoverage=true

# Run tests with logger
dotnet test --logger "trx;LogFileName=test-results.trx"
dotnet test --logger "html;LogFileName=test-results.html"

# Run tests without build
dotnet test --no-build
```

### dotnet clean

```bash
# Clean build outputs
dotnet clean

# Clean with configuration
dotnet clean -c Release

# Clean specific framework
dotnet clean -f net8.0

# Clean and remove obj folder
dotnet clean
rm -rf **/obj
```

### dotnet pack

```bash
# Create NuGet package
dotnet pack

# Pack with configuration
dotnet pack -c Release

# Pack with version
dotnet pack -p:Version=1.2.3

# Pack without build
dotnet pack --no-build

# Pack to output directory
dotnet pack -o ./packages

# Include symbols
dotnet pack -p:IncludeSymbols=true -p:SymbolPackageFormat=snupkg
```

### dotnet add/remove

```bash
# Add package
dotnet add package Microsoft.Extensions.Logging
dotnet add package Newtonsoft.Json --version 13.0.3

# Add package from source
dotnet add package MyPackage --source ./local-packages

# Add package to specific project
dotnet add src/MyApp/MyApp.csproj package Serilog

# Remove package
dotnet remove package Newtonsoft.Json

# Add project reference
dotnet add reference ../MyLibrary/MyLibrary.csproj

# Remove project reference
dotnet remove reference ../MyLibrary/MyLibrary.csproj
```

### dotnet list

```bash
# List packages
dotnet list package
dotnet list package --outdated
dotnet list package --deprecated
dotnet list package --vulnerable

# List project references
dotnet list reference

# List projects in solution
dotnet sln list
```

### dotnet tool

```bash
# Install global tool
dotnet tool install -g dotnet-ef
dotnet tool install -g dotnet-format

# Install local tool
dotnet new tool-manifest
dotnet tool install dotnet-ef

# List tools
dotnet tool list -g
dotnet tool list

# Update tool
dotnet tool update -g dotnet-ef
dotnet tool update dotnet-ef

# Uninstall tool
dotnet tool uninstall -g dotnet-ef
dotnet tool uninstall dotnet-ef

# Run tool
dotnet ef --version
dotnet format
```

## Project Types

### Console Application

```csharp
// Program.cs (Top-level statements)
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

var builder = Host.CreateApplicationBuilder(args);

// Configure services
builder.Services.AddTransient<IMyService, MyService>();
builder.Services.AddLogging(logging =>
{
    logging.AddConsole();
    logging.AddDebug();
});

var host = builder.Build();

// Run application
var service = host.Services.GetRequiredService<IMyService>();
await service.RunAsync();

await host.RunAsync();

// Service implementation
public interface IMyService
{
    Task RunAsync();
}

public class MyService : IMyService
{
    private readonly ILogger<MyService> _logger;

    public MyService(ILogger<MyService> logger)
    {
        _logger = logger;
    }

    public async Task RunAsync()
    {
        _logger.LogInformation("Service started at {Time}", DateTime.UtcNow);
        await Task.Delay(1000);
        _logger.LogInformation("Service completed at {Time}", DateTime.UtcNow);
    }
}
```

### Class Library

```csharp
// MyLibrary.csproj
/*
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
*/

namespace MyLibrary;

/// <summary>
/// Calculator service for basic arithmetic operations.
/// </summary>
public class Calculator
{
    /// <summary>
    /// Adds two numbers.
    /// </summary>
    /// <param name="a">First number</param>
    /// <param name="b">Second number</param>
    /// <returns>Sum of a and b</returns>
    public int Add(int a, int b) => a + b;

    /// <summary>
    /// Subtracts two numbers.
    /// </summary>
    /// <param name="a">First number</param>
    /// <param name="b">Second number</param>
    /// <returns>Difference of a and b</returns>
    public int Subtract(int a, int b) => a - b;
}
```

### Web API

```csharp
// Program.cs
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// CORS
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors();
app.UseAuthorization();
app.MapControllers();

app.Run();

// Controllers/WeatherController.cs
using Microsoft.AspNetCore.Mvc;

namespace MyApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class WeatherController : ControllerBase
{
    private static readonly string[] Summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild",
        "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    private readonly ILogger<WeatherController> _logger;

    public WeatherController(ILogger<WeatherController> logger)
    {
        _logger = logger;
    }

    [HttpGet]
    public IEnumerable<WeatherForecast> Get()
    {
        _logger.LogInformation("Getting weather forecast");

        return Enumerable.Range(1, 5).Select(index => new WeatherForecast
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            TemperatureC = Random.Shared.Next(-20, 55),
            Summary = Summaries[Random.Shared.Next(Summaries.Length)]
        })
        .ToArray();
    }

    [HttpGet("{id}")]
    public ActionResult<WeatherForecast> GetById(int id)
    {
        if (id < 1 || id > 5)
            return NotFound();

        return new WeatherForecast
        {
            Date = DateOnly.FromDateTime(DateTime.Now.AddDays(id)),
            TemperatureC = Random.Shared.Next(-20, 55),
            Summary = Summaries[Random.Shared.Next(Summaries.Length)]
        };
    }

    [HttpPost]
    public ActionResult<WeatherForecast> Create(WeatherForecast forecast)
    {
        _logger.LogInformation("Creating weather forecast");
        return CreatedAtAction(nameof(GetById), new { id = 1 }, forecast);
    }
}

public record WeatherForecast
{
    public DateOnly Date { get; init; }
    public int TemperatureC { get; init; }
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
    public string? Summary { get; init; }
}
```

### Worker Service

```csharp
// Program.cs
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);
builder.Services.AddHostedService<Worker>();

var host = builder.Build();
await host.RunAsync();

// Worker.cs
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

public class Worker : BackgroundService
{
    private readonly ILogger<Worker> _logger;

    public Worker(ILogger<Worker> logger)
    {
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);
            await Task.Delay(10000, stoppingToken);
        }
    }

    public override async Task StartAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Worker starting");
        await base.StartAsync(cancellationToken);
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        _logger.LogInformation("Worker stopping");
        await base.StopAsync(cancellationToken);
    }
}
```

## Dependency Injection

### Service Lifetimes

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

// Transient: Created each time requested
builder.Services.AddTransient<ITransientService, TransientService>();

// Scoped: Created once per scope (request in web apps)
builder.Services.AddScoped<IScopedService, ScopedService>();

// Singleton: Created once for application lifetime
builder.Services.AddSingleton<ISingletonService, SingletonService>();

// Singleton instance
builder.Services.AddSingleton<IConfigService>(new ConfigService("config"));

// Singleton factory
builder.Services.AddSingleton<IFactoryService>(sp =>
{
    var logger = sp.GetRequiredService<ILogger<FactoryService>>();
    return new FactoryService(logger);
});

var host = builder.Build();
```

### Service Registration Patterns

```csharp
using Microsoft.Extensions.DependencyInjection;

public static class ServiceCollectionExtensions
{
    // Extension method for clean registration
    public static IServiceCollection AddMyServices(
        this IServiceCollection services)
    {
        services.AddTransient<IMyService, MyService>();
        services.AddScoped<IDataService, DataService>();
        services.AddSingleton<ICacheService, CacheService>();

        return services;
    }

    // Generic registration
    public static IServiceCollection AddRepository<TEntity>(
        this IServiceCollection services)
        where TEntity : class
    {
        services.AddScoped<IRepository<TEntity>, Repository<TEntity>>();
        return services;
    }

    // Conditional registration
    public static IServiceCollection AddConditionalService(
        this IServiceCollection services,
        bool condition)
    {
        if (condition)
        {
            services.AddTransient<IService, ServiceA>();
        }
        else
        {
            services.AddTransient<IService, ServiceB>();
        }

        return services;
    }

    // TryAdd - only adds if not already registered
    public static IServiceCollection AddDefaultServices(
        this IServiceCollection services)
    {
        services.TryAddTransient<IMyService, MyService>();
        services.TryAddScoped<IDataService, DataService>();
        services.TryAddSingleton<ICacheService, CacheService>();

        return services;
    }

    // Replace service
    public static IServiceCollection ReplaceService(
        this IServiceCollection services)
    {
        services.Replace(ServiceDescriptor.Transient<IMyService, NewMyService>());
        return services;
    }

    // Remove service
    public static IServiceCollection RemoveService(
        this IServiceCollection services)
    {
        var descriptor = services.FirstOrDefault(d => d.ServiceType == typeof(IMyService));
        if (descriptor != null)
        {
            services.Remove(descriptor);
        }

        return services;
    }
}
```

### Constructor Injection

```csharp
public interface IEmailService
{
    Task SendEmailAsync(string to, string subject, string body);
}

public interface ILogger<T>
{
    void LogInformation(string message);
}

public class UserService
{
    private readonly IEmailService _emailService;
    private readonly ILogger<UserService> _logger;
    private readonly IConfiguration _configuration;

    // Constructor injection
    public UserService(
        IEmailService emailService,
        ILogger<UserService> logger,
        IConfiguration configuration)
    {
        _emailService = emailService ?? throw new ArgumentNullException(nameof(emailService));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _configuration = configuration ?? throw new ArgumentNullException(nameof(configuration));
    }

    public async Task CreateUserAsync(string email, string name)
    {
        _logger.LogInformation("Creating user {Name}", name);

        var welcomeMessage = _configuration["Messages:Welcome"] ?? "Welcome!";
        await _emailService.SendEmailAsync(email, "Welcome", welcomeMessage);
    }
}
```

### Service Resolution

```csharp
using Microsoft.Extensions.DependencyInjection;

public class ServiceResolver
{
    private readonly IServiceProvider _serviceProvider;

    public ServiceResolver(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public void ResolveServices()
    {
        // Get required service (throws if not found)
        var requiredService = _serviceProvider.GetRequiredService<IMyService>();

        // Get service (returns null if not found)
        var optionalService = _serviceProvider.GetService<IOptionalService>();

        // Get all implementations
        var allServices = _serviceProvider.GetServices<IMyService>();

        // Create scope
        using var scope = _serviceProvider.CreateScope();
        var scopedService = scope.ServiceProvider.GetRequiredService<IScopedService>();

        // Resolve with keyed services (.NET 8+)
        var keyedService = _serviceProvider.GetRequiredKeyedService<ICache>("redis");
        var anotherKeyedService = _serviceProvider.GetKeyedService<ICache>("memory");
    }
}

// Keyed services (.NET 8+)
public static class KeyedServiceExtensions
{
    public static IServiceCollection AddKeyedServices(
        this IServiceCollection services)
    {
        services.AddKeyedSingleton<ICache, RedisCache>("redis");
        services.AddKeyedSingleton<ICache, MemoryCache>("memory");

        return services;
    }
}

public class ServiceUsingKeyedDependencies
{
    private readonly ICache _redisCache;
    private readonly ICache _memoryCache;

    public ServiceUsingKeyedDependencies(
        [FromKeyedServices("redis")] ICache redisCache,
        [FromKeyedServices("memory")] ICache memoryCache)
    {
        _redisCache = redisCache;
        _memoryCache = memoryCache;
    }
}
```

## Configuration

### appsettings.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=mydb;User Id=sa;Password=P@ssw0rd;",
    "Redis": "localhost:6379"
  },
  "AppSettings": {
    "ApplicationName": "My Application",
    "Version": "1.0.0",
    "Features": {
      "EnableFeatureA": true,
      "EnableFeatureB": false
    }
  },
  "Email": {
    "SmtpServer": "smtp.example.com",
    "SmtpPort": 587,
    "FromAddress": "noreply@example.com",
    "EnableSsl": true
  },
  "Cache": {
    "SlidingExpiration": "00:30:00",
    "AbsoluteExpiration": "01:00:00"
  },
  "ApiClients": {
    "ExternalApi": {
      "BaseUrl": "https://api.example.com",
      "Timeout": "00:00:30",
      "ApiKey": ""
    }
  }
}
```

### Environment-Specific Configuration

```json
// appsettings.Development.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft.AspNetCore": "Debug"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=mydb_dev;User Id=dev;Password=dev123;"
  }
}

// appsettings.Production.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft.AspNetCore": "Error"
    }
  }
}

// appsettings.Staging.json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  }
}
```

### Configuration Options Pattern

```csharp
// AppSettings.cs
public class AppSettings
{
    public const string SectionName = "AppSettings";

    public string ApplicationName { get; set; } = string.Empty;
    public string Version { get; set; } = string.Empty;
    public FeatureSettings Features { get; set; } = new();
}

public class FeatureSettings
{
    public bool EnableFeatureA { get; set; }
    public bool EnableFeatureB { get; set; }
}

public class EmailSettings
{
    public const string SectionName = "Email";

    public string SmtpServer { get; set; } = string.Empty;
    public int SmtpPort { get; set; }
    public string FromAddress { get; set; } = string.Empty;
    public bool EnableSsl { get; set; }
}

// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Bind configuration sections to strongly-typed options
builder.Services.Configure<AppSettings>(
    builder.Configuration.GetSection(AppSettings.SectionName));

builder.Services.Configure<EmailSettings>(
    builder.Configuration.GetSection(EmailSettings.SectionName));

// Using IOptions<T>
public class MyService
{
    private readonly AppSettings _appSettings;
    private readonly EmailSettings _emailSettings;

    public MyService(
        IOptions<AppSettings> appOptions,
        IOptions<EmailSettings> emailOptions)
    {
        _appSettings = appOptions.Value;
        _emailSettings = emailOptions.Value;
    }

    public void DoSomething()
    {
        Console.WriteLine(_appSettings.ApplicationName);
        Console.WriteLine(_emailSettings.SmtpServer);
    }
}

// Using IOptionsSnapshot<T> (reloads on change, scoped)
public class MyReloadableService
{
    private readonly IOptionsSnapshot<AppSettings> _appSettings;

    public MyReloadableService(IOptionsSnapshot<AppSettings> appSettings)
    {
        _appSettings = appSettings;
    }

    public void DoSomething()
    {
        // Gets current value (reloaded if config changed)
        Console.WriteLine(_appSettings.Value.ApplicationName);
    }
}

// Using IOptionsMonitor<T> (reloads on change, singleton)
public class MyMonitoredService
{
    private readonly IOptionsMonitor<AppSettings> _appSettings;

    public MyMonitoredService(IOptionsMonitor<AppSettings> appSettings)
    {
        _appSettings = appSettings;

        // Subscribe to changes
        _appSettings.OnChange(settings =>
        {
            Console.WriteLine("Configuration changed!");
        });
    }

    public void DoSomething()
    {
        Console.WriteLine(_appSettings.CurrentValue.ApplicationName);
    }
}
```

### Configuration Sources

```csharp
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

// Clear default sources
builder.Configuration.Sources.Clear();

// Add configuration sources in order (later sources override earlier ones)
builder.Configuration
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true, reloadOnChange: true)
    .AddXmlFile("config.xml", optional: true, reloadOnChange: true)
    .AddIniFile("config.ini", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables()
    .AddEnvironmentVariables(prefix: "MYAPP_")
    .AddCommandLine(args)
    .AddUserSecrets<Program>() // Development only
    .AddInMemoryCollection(new Dictionary<string, string?>
    {
        ["Key1"] = "Value1",
        ["Key2"] = "Value2"
    });

var host = builder.Build();
```

### User Secrets (Development)

```bash
# Initialize user secrets
dotnet user-secrets init

# Set secret
dotnet user-secrets set "ApiKey" "my-secret-key"
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=localhost;Database=mydb;"

# List secrets
dotnet user-secrets list

# Remove secret
dotnet user-secrets remove "ApiKey"

# Clear all secrets
dotnet user-secrets clear
```

### Environment Variables

```bash
# Windows (PowerShell)
$env:ASPNETCORE_ENVIRONMENT = "Development"
$env:ConnectionStrings__DefaultConnection = "Server=localhost;Database=mydb;"
$env:AppSettings__ApplicationName = "My App"

# Linux/macOS
export ASPNETCORE_ENVIRONMENT=Development
export ConnectionStrings__DefaultConnection="Server=localhost;Database=mydb;"
export AppSettings__ApplicationName="My App"

# Note: __ (double underscore) represents nested configuration sections
# AppSettings__Features__EnableFeatureA maps to AppSettings:Features:EnableFeatureA
```

## Logging

### ILogger Interface

```csharp
using Microsoft.Extensions.Logging;

public class MyService
{
    private readonly ILogger<MyService> _logger;

    public MyService(ILogger<MyService> logger)
    {
        _logger = logger;
    }

    public void DoWork()
    {
        // Log levels
        _logger.LogTrace("Trace message");
        _logger.LogDebug("Debug message");
        _logger.LogInformation("Information message");
        _logger.LogWarning("Warning message");
        _logger.LogError("Error message");
        _logger.LogCritical("Critical message");

        // Structured logging with parameters
        var userId = 123;
        var userName = "John Doe";
        _logger.LogInformation("User {UserId} logged in: {UserName}", userId, userName);

        // Exception logging
        try
        {
            throw new InvalidOperationException("Something went wrong");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "An error occurred while processing user {UserId}", userId);
        }

        // Log with event ID
        _logger.LogInformation(new EventId(1001, "UserLogin"),
            "User {UserId} logged in", userId);

        // Conditional logging
        if (_logger.IsEnabled(LogLevel.Debug))
        {
            var expensiveData = GetExpensiveDebugData();
            _logger.LogDebug("Debug data: {Data}", expensiveData);
        }

        // Log scopes
        using (_logger.BeginScope("Processing user {UserId}", userId))
        {
            _logger.LogInformation("Starting process");
            _logger.LogInformation("Process step 1");
            _logger.LogInformation("Process step 2");
            _logger.LogInformation("Completed process");
        }
    }

    private string GetExpensiveDebugData() => "expensive data";
}
```

### Configure Logging

```csharp
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Hosting;

var builder = Host.CreateApplicationBuilder(args);

builder.Logging.ClearProviders(); // Remove default providers

// Add providers
builder.Logging.AddConsole();
builder.Logging.AddDebug();
builder.Logging.AddEventSourceLogger();

// Set minimum level
builder.Logging.SetMinimumLevel(LogLevel.Information);

// Add filtering
builder.Logging.AddFilter("Microsoft", LogLevel.Warning);
builder.Logging.AddFilter("System", LogLevel.Warning);
builder.Logging.AddFilter("MyApp", LogLevel.Debug);

// Configure from appsettings.json
builder.Logging.AddConfiguration(builder.Configuration.GetSection("Logging"));

var host = builder.Build();
```

### Logging Configuration in appsettings.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information",
      "Microsoft.EntityFrameworkCore": "Warning",
      "MyApp": "Debug"
    },
    "Console": {
      "IncludeScopes": true,
      "LogLevel": {
        "Default": "Information"
      }
    },
    "Debug": {
      "LogLevel": {
        "Default": "Debug"
      }
    }
  }
}
```

### Third-Party Logging (Serilog Example)

```csharp
// Install packages:
// dotnet add package Serilog.AspNetCore
// dotnet add package Serilog.Sinks.Console
// dotnet add package Serilog.Sinks.File
// dotnet add package Serilog.Sinks.Seq

using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
builder.Host.UseSerilog((context, configuration) =>
{
    configuration
        .ReadFrom.Configuration(context.Configuration)
        .Enrich.FromLogContext()
        .Enrich.WithMachineName()
        .Enrich.WithThreadId()
        .WriteTo.Console()
        .WriteTo.File(
            path: "logs/log-.txt",
            rollingInterval: RollingInterval.Day,
            retainedFileCountLimit: 30)
        .WriteTo.Seq("http://localhost:5341");
});

var app = builder.Build();

// Add Serilog request logging
app.UseSerilogRequestLogging();

app.Run();
```

## Middleware Patterns

### Built-in Middleware

```csharp
using Microsoft.AspNetCore.Builder;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Order matters! Middleware executes in order added

// Exception handling (should be first)
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

// HTTPS redirection
app.UseHttpsRedirection();

// Static files
app.UseStaticFiles();
app.UseStaticFiles(new StaticFileOptions
{
    FileProvider = new PhysicalFileProvider(
        Path.Combine(builder.Environment.ContentRootPath, "StaticFiles")),
    RequestPath = "/files"
});

// Routing
app.UseRouting();

// CORS (must be after routing, before authorization)
app.UseCors();

// Authentication
app.UseAuthentication();

// Authorization (must be after authentication)
app.UseAuthorization();

// Response caching
app.UseResponseCaching();

// Response compression
app.UseResponseCompression();

// Session
app.UseSession();

// Endpoints (should be last)
app.MapControllers();
app.MapRazorPages();

app.Run();
```

### Custom Middleware (Inline)

```csharp
var app = builder.Build();

// Use method
app.Use(async (context, next) =>
{
    // Before next middleware
    Console.WriteLine($"Before: {context.Request.Path}");

    await next(context);

    // After next middleware
    Console.WriteLine($"After: {context.Response.StatusCode}");
});

// Run method (terminal middleware)
app.Run(async context =>
{
    await context.Response.WriteAsync("Hello World!");
});

// Map method (branch pipeline)
app.Map("/api", apiApp =>
{
    apiApp.Use(async (context, next) =>
    {
        Console.WriteLine("API middleware");
        await next(context);
    });

    apiApp.Run(async context =>
    {
        await context.Response.WriteAsync("API Response");
    });
});

// MapWhen method (conditional branch)
app.MapWhen(
    context => context.Request.Query.ContainsKey("branch"),
    branchApp =>
    {
        branchApp.Run(async context =>
        {
            await context.Response.WriteAsync("Branch pipeline");
        });
    });

app.Run();
```

### Custom Middleware Class

```csharp
// RequestLoggingMiddleware.cs
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var startTime = DateTime.UtcNow;

        _logger.LogInformation(
            "Incoming request: {Method} {Path}",
            context.Request.Method,
            context.Request.Path);

        try
        {
            await _next(context);
        }
        finally
        {
            var elapsed = DateTime.UtcNow - startTime;

            _logger.LogInformation(
                "Completed request: {Method} {Path} - Status: {StatusCode} - Duration: {Duration}ms",
                context.Request.Method,
                context.Request.Path,
                context.Response.StatusCode,
                elapsed.TotalMilliseconds);
        }
    }
}

// Extension method for registration
public static class RequestLoggingMiddlewareExtensions
{
    public static IApplicationBuilder UseRequestLogging(
        this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<RequestLoggingMiddleware>();
    }
}

// Usage in Program.cs
var app = builder.Build();
app.UseRequestLogging();
app.Run();
```

### Exception Handling Middleware

```csharp
public class GlobalExceptionHandlerMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<GlobalExceptionHandlerMiddleware> _logger;

    public GlobalExceptionHandlerMiddleware(
        RequestDelegate next,
        ILogger<GlobalExceptionHandlerMiddleware> logger)
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
            _logger.LogError(ex, "An unhandled exception occurred");
            await HandleExceptionAsync(context, ex);
        }
    }

    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.ContentType = "application/json";
        context.Response.StatusCode = exception switch
        {
            ArgumentException => StatusCodes.Status400BadRequest,
            UnauthorizedAccessException => StatusCodes.Status401Unauthorized,
            KeyNotFoundException => StatusCodes.Status404NotFound,
            _ => StatusCodes.Status500InternalServerError
        };

        var response = new
        {
            statusCode = context.Response.StatusCode,
            message = exception.Message,
            detailed = exception.ToString() // Only in development!
        };

        await context.Response.WriteAsJsonAsync(response);
    }
}
```

## NuGet Packages

### Common Packages

```bash
# Core Microsoft packages
dotnet add package Microsoft.Extensions.DependencyInjection
dotnet add package Microsoft.Extensions.Configuration
dotnet add package Microsoft.Extensions.Configuration.Json
dotnet add package Microsoft.Extensions.Logging
dotnet add package Microsoft.Extensions.Hosting
dotnet add package Microsoft.Extensions.Options

# ASP.NET Core
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package Microsoft.AspNetCore.Mvc.NewtonsoftJson
dotnet add package Swashbuckle.AspNetCore

# Entity Framework Core
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Sqlite
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package Microsoft.EntityFrameworkCore.Tools

# Testing
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk
dotnet add package Moq
dotnet add package FluentAssertions
dotnet add package coverlet.collector

# Serialization
dotnet add package System.Text.Json
dotnet add package Newtonsoft.Json

# HTTP
dotnet add package Microsoft.Extensions.Http
dotnet add package Microsoft.Extensions.Http.Polly
dotnet add package Polly

# Validation
dotnet add package FluentValidation
dotnet add package FluentValidation.AspNetCore

# Mapping
dotnet add package AutoMapper
dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection

# Logging
dotnet add package Serilog
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package Serilog.Sinks.File

# Authentication
dotnet add package Microsoft.AspNetCore.Identity.EntityFrameworkCore
dotnet add package Microsoft.AspNetCore.Authentication.OpenIdConnect
```

### Package Management

```bash
# List installed packages
dotnet list package

# List outdated packages
dotnet list package --outdated

# List deprecated packages
dotnet list package --deprecated

# List vulnerable packages
dotnet list package --vulnerable

# Update package
dotnet add package PackageName --version 2.0.0

# Remove package
dotnet remove package PackageName

# Restore packages
dotnet restore

# Clear NuGet cache
dotnet nuget locals all --clear
```

### Creating NuGet Packages

```xml
<!-- MyLibrary.csproj -->
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>

    <!-- Package metadata -->
    <PackageId>MyCompany.MyLibrary</PackageId>
    <Version>1.0.0</Version>
    <Authors>Your Name</Authors>
    <Company>MyCompany</Company>
    <Description>Library description here</Description>
    <PackageTags>library;utility;helpers</PackageTags>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
    <PackageProjectUrl>https://github.com/mycompany/mylibrary</PackageProjectUrl>
    <RepositoryUrl>https://github.com/mycompany/mylibrary</RepositoryUrl>
    <RepositoryType>git</RepositoryType>
    <PackageReadmeFile>README.md</PackageReadmeFile>
    <PackageIcon>icon.png</PackageIcon>

    <!-- Include symbols -->
    <IncludeSymbols>true</IncludeSymbols>
    <SymbolPackageFormat>snupkg</SymbolPackageFormat>
  </PropertyGroup>

  <ItemGroup>
    <None Include="README.md" Pack="true" PackagePath="\" />
    <None Include="icon.png" Pack="true" PackagePath="\" />
  </ItemGroup>

</Project>
```

```bash
# Create package
dotnet pack -c Release

# Create package with version
dotnet pack -c Release -p:PackageVersion=1.0.1

# Publish to NuGet.org
dotnet nuget push bin/Release/MyLibrary.1.0.0.nupkg --api-key YOUR_API_KEY --source https://api.nuget.org/v3/index.json

# Publish to private feed
dotnet nuget push bin/Release/MyLibrary.1.0.0.nupkg --source http://myfeed.example.com/nuget
```

## Cross-Platform Development

### Runtime Identifiers (RIDs)

```bash
# Common RIDs
# Windows
win-x64           # Windows 64-bit
win-x86           # Windows 32-bit
win-arm64         # Windows ARM64

# Linux
linux-x64         # Linux 64-bit
linux-arm         # Linux ARM
linux-arm64       # Linux ARM64
linux-musl-x64    # Alpine Linux

# macOS
osx-x64           # macOS Intel
osx-arm64         # macOS Apple Silicon

# Publish for specific runtime
dotnet publish -r win-x64 --self-contained
dotnet publish -r linux-x64 --self-contained
dotnet publish -r osx-arm64 --self-contained
```

### Platform-Specific Code

```csharp
using System.Runtime.InteropServices;

public class PlatformService
{
    public string GetPlatformInfo()
    {
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
        {
            return "Running on Windows";
        }
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
        {
            return "Running on Linux";
        }
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
        {
            return "Running on macOS";
        }
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.FreeBSD))
        {
            return "Running on FreeBSD";
        }

        return "Unknown platform";
    }

    public string GetArchitecture()
    {
        return RuntimeInformation.OSArchitecture switch
        {
            Architecture.X64 => "x64",
            Architecture.X86 => "x86",
            Architecture.Arm => "ARM",
            Architecture.Arm64 => "ARM64",
            _ => "Unknown"
        };
    }
}

// Conditional compilation
public class PlatformSpecificFeature
{
    public void DoSomething()
    {
#if WINDOWS
        WindowsSpecificCode();
#elif LINUX
        LinuxSpecificCode();
#elif OSX
        MacOSSpecificCode();
#endif
    }

    private void WindowsSpecificCode() { }
    private void LinuxSpecificCode() { }
    private void MacOSSpecificCode() { }
}
```

### Path Handling

```csharp
using System.IO;

public class PathHelper
{
    public void HandlePaths()
    {
        // Use Path.Combine for cross-platform paths
        var configPath = Path.Combine("config", "appsettings.json");

        // Get directory separator (\ on Windows, / on Unix)
        var separator = Path.DirectorySeparatorChar;

        // Get path separator (; on Windows, : on Unix)
        var pathSeparator = Path.PathSeparator;

        // Get temp path
        var tempPath = Path.GetTempPath();

        // Get user profile directory
        var userProfile = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);

        // Get application data directory
        var appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
    }
}
```

## Metaprogramming

### Reflection

Reflection allows runtime inspection and manipulation of types, methods, and properties.

```csharp
using System;
using System.Reflection;

public class User
{
    public string Name { get; set; }
    public int Age { get; set; }

    public void Greet() => Console.WriteLine($"Hello, I'm {Name}");
}

public class ReflectionExamples
{
    public void InspectType()
    {
        // Get type information
        Type type = typeof(User);
        Type type2 = user.GetType();
        Type type3 = Type.GetType("Namespace.User");

        // Get type properties
        Console.WriteLine($"Name: {type.Name}");
        Console.WriteLine($"FullName: {type.FullName}");
        Console.WriteLine($"Namespace: {type.Namespace}");
        Console.WriteLine($"IsClass: {type.IsClass}");
        Console.WriteLine($"IsPublic: {type.IsPublic}");

        // Get properties
        foreach (PropertyInfo prop in type.GetProperties())
        {
            Console.WriteLine($"{prop.Name}: {prop.PropertyType}");
        }

        // Get methods
        foreach (MethodInfo method in type.GetMethods())
        {
            Console.WriteLine($"{method.Name}");
        }
    }

    public void CreateInstance()
    {
        Type type = typeof(User);

        // Create instance with parameterless constructor
        object instance = Activator.CreateInstance(type);

        // Create instance with constructor parameters
        object instance2 = Activator.CreateInstance(
            type,
            new object[] { "Alice", 30 }
        );

        // Generic version
        User user = Activator.CreateInstance<User>();
    }

    public void AccessMembers()
    {
        var user = new User { Name = "Alice", Age = 30 };
        Type type = typeof(User);

        // Get property value
        PropertyInfo nameProp = type.GetProperty("Name");
        string name = (string)nameProp.GetValue(user);

        // Set property value
        nameProp.SetValue(user, "Bob");

        // Invoke method
        MethodInfo greetMethod = type.GetMethod("Greet");
        greetMethod.Invoke(user, null);

        // Access private members
        FieldInfo privateField = type.GetField(
            "_privateField",
            BindingFlags.NonPublic | BindingFlags.Instance
        );
        privateField?.SetValue(user, "secret");
    }
}
```

### Attributes

Attributes provide metadata about code elements that can be queried at runtime or compile time.

```csharp
using System;

// Built-in attributes
[Obsolete("Use NewMethod instead")]
public void OldMethod() { }

[Serializable]
public class DataModel { }

[AttributeUsage(AttributeTargets.Method)]
public class LoggableAttribute : Attribute
{
    public string Message { get; set; }
    public LogLevel Level { get; set; }

    public LoggableAttribute(string message = "", LogLevel level = LogLevel.Info)
    {
        Message = message;
        Level = level;
    }
}

// Custom attribute with multiple targets
[AttributeUsage(
    AttributeTargets.Class | AttributeTargets.Method,
    AllowMultiple = true,
    Inherited = true
)]
public class AuthorAttribute : Attribute
{
    public string Name { get; }
    public string Date { get; set; }

    public AuthorAttribute(string name)
    {
        Name = name;
    }
}

// Usage
public class MyService
{
    [Loggable("Processing data", LogLevel.Debug)]
    [Author("Alice", Date = "2024-01-01")]
    public void ProcessData()
    {
        // Method implementation
    }
}

// Reading attributes
public class AttributeReader
{
    public void ReadMethodAttributes()
    {
        var method = typeof(MyService).GetMethod("ProcessData");

        // Get single attribute
        var loggable = method.GetCustomAttribute<LoggableAttribute>();
        if (loggable != null)
        {
            Console.WriteLine($"Log: {loggable.Message} at {loggable.Level}");
        }

        // Get all attributes of a type
        var authors = method.GetCustomAttributes<AuthorAttribute>();
        foreach (var author in authors)
        {
            Console.WriteLine($"Author: {author.Name} on {author.Date}");
        }

        // Check if attribute is present
        bool isLoggable = method.IsDefined(typeof(LoggableAttribute));
    }
}
```

### Source Generators (C# 9+)

Source generators create code at compile time, providing compile-time metaprogramming.

```csharp
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.Text;
using System.Text;

// Source generator
[Generator]
public class AutoNotifyGenerator : ISourceGenerator
{
    public void Initialize(GeneratorInitializationContext context)
    {
        // Register syntax receiver
        context.RegisterForSyntaxNotifications(() => new SyntaxReceiver());
    }

    public void Execute(GeneratorExecutionContext context)
    {
        if (context.SyntaxReceiver is not SyntaxReceiver receiver)
            return;

        foreach (var field in receiver.CandidateFields)
        {
            var model = context.Compilation.GetSemanticModel(field.SyntaxTree);
            var fieldSymbol = model.GetDeclaredSymbol(field) as IFieldSymbol;

            if (fieldSymbol == null)
                continue;

            var classSymbol = fieldSymbol.ContainingType;
            var namespaceName = classSymbol.ContainingNamespace.ToDisplayString();

            var source = GeneratePropertySource(
                namespaceName,
                classSymbol.Name,
                fieldSymbol.Name
            );

            context.AddSource(
                $"{classSymbol.Name}_{fieldSymbol.Name}_AutoNotify.g.cs",
                SourceText.From(source, Encoding.UTF8)
            );
        }
    }

    private string GeneratePropertySource(
        string namespaceName,
        string className,
        string fieldName)
    {
        var propertyName = char.ToUpper(fieldName[1]) + fieldName.Substring(2);

        return $@"
using System.ComponentModel;

namespace {namespaceName}
{{
    public partial class {className} : INotifyPropertyChanged
    {{
        public event PropertyChangedEventHandler? PropertyChanged;

        public {fieldName.TrimStart('_')} {propertyName}
        {{
            get => {fieldName};
            set
            {{
                if ({fieldName} != value)
                {{
                    {fieldName} = value;
                    PropertyChanged?.Invoke(
                        this,
                        new PropertyChangedEventArgs(nameof({propertyName}))
                    );
                }}
            }}
        }}
    }}
}}";
    }

    class SyntaxReceiver : ISyntaxReceiver
    {
        public List<FieldDeclarationSyntax> CandidateFields { get; } = new();

        public void OnVisitSyntaxNode(SyntaxNode syntaxNode)
        {
            if (syntaxNode is FieldDeclarationSyntax fieldDeclaration &&
                fieldDeclaration.AttributeLists.Count > 0)
            {
                CandidateFields.Add(fieldDeclaration);
            }
        }
    }
}

// Usage in consuming code
public partial class Person
{
    [AutoNotify]
    private string _name = "";

    // Property is generated by source generator
}
```

### Expression Trees

Expression trees represent code as data structures for runtime code generation and analysis.

```csharp
using System;
using System.Linq.Expressions;

public class ExpressionTreeExamples
{
    public void BasicExpressions()
    {
        // Lambda expression
        Expression<Func<int, int, int>> add = (a, b) => a + b;

        // Compile and execute
        var compiled = add.Compile();
        int result = compiled(2, 3); // 5

        // Inspect expression tree
        Console.WriteLine(add.Body);        // (a + b)
        Console.WriteLine(add.Parameters);  // [a, b]
    }

    public void BuildExpressionTree()
    {
        // Build expression: (a, b) => a + b
        var paramA = Expression.Parameter(typeof(int), "a");
        var paramB = Expression.Parameter(typeof(int), "b");
        var body = Expression.Add(paramA, paramB);

        var lambda = Expression.Lambda<Func<int, int, int>>(
            body,
            paramA,
            paramB
        );

        var compiled = lambda.Compile();
        int result = compiled(2, 3); // 5
    }

    public void ComplexExpressions()
    {
        // Build: user => user.Name == "Alice" && user.Age > 18
        var param = Expression.Parameter(typeof(User), "user");

        var nameProperty = Expression.Property(param, "Name");
        var nameEquals = Expression.Equal(
            nameProperty,
            Expression.Constant("Alice")
        );

        var ageProperty = Expression.Property(param, "Age");
        var ageGreater = Expression.GreaterThan(
            ageProperty,
            Expression.Constant(18)
        );

        var condition = Expression.AndAlso(nameEquals, ageGreater);

        var lambda = Expression.Lambda<Func<User, bool>>(
            condition,
            param
        );

        // Use with LINQ
        var users = new List<User>();
        var filtered = users.AsQueryable().Where(lambda);
    }

    public void DynamicPropertyAccess()
    {
        // Build property accessor dynamically
        var param = Expression.Parameter(typeof(User), "user");
        var property = Expression.Property(param, "Name");
        var lambda = Expression.Lambda<Func<User, string>>(property, param);

        var accessor = lambda.Compile();
        var user = new User { Name = "Alice" };
        string name = accessor(user); // "Alice"
    }
}
```

### IL Emit (Reflection.Emit)

Generate IL code dynamically at runtime for maximum performance and flexibility.

```csharp
using System;
using System.Reflection;
using System.Reflection.Emit;

public class ILEmitExamples
{
    public void CreateDynamicMethod()
    {
        // Create dynamic method: int Add(int a, int b) => a + b
        var method = new DynamicMethod(
            "Add",
            typeof(int),
            new[] { typeof(int), typeof(int) }
        );

        ILGenerator il = method.GetILGenerator();

        // IL: ldarg.0 (load first argument)
        il.Emit(OpCodes.Ldarg_0);
        // IL: ldarg.1 (load second argument)
        il.Emit(OpCodes.Ldarg_1);
        // IL: add (add top two stack values)
        il.Emit(OpCodes.Add);
        // IL: ret (return)
        il.Emit(OpCodes.Ret);

        // Create delegate
        var add = (Func<int, int, int>)method.CreateDelegate(
            typeof(Func<int, int, int>)
        );

        int result = add(2, 3); // 5
    }

    public void CreateDynamicType()
    {
        // Create assembly
        var assemblyName = new AssemblyName("DynamicAssembly");
        var assemblyBuilder = AssemblyBuilder.DefineDynamicAssembly(
            assemblyName,
            AssemblyBuilderAccess.Run
        );

        // Create module
        var moduleBuilder = assemblyBuilder.DefineDynamicModule("MainModule");

        // Create type
        var typeBuilder = moduleBuilder.DefineType(
            "DynamicType",
            TypeAttributes.Public
        );

        // Add field
        var fieldBuilder = typeBuilder.DefineField(
            "_value",
            typeof(int),
            FieldAttributes.Private
        );

        // Add property
        var propertyBuilder = typeBuilder.DefineProperty(
            "Value",
            PropertyAttributes.HasDefault,
            typeof(int),
            null
        );

        // Add getter
        var getterBuilder = typeBuilder.DefineMethod(
            "get_Value",
            MethodAttributes.Public | MethodAttributes.SpecialName,
            typeof(int),
            Type.EmptyTypes
        );

        var getterIL = getterBuilder.GetILGenerator();
        getterIL.Emit(OpCodes.Ldarg_0);
        getterIL.Emit(OpCodes.Ldfld, fieldBuilder);
        getterIL.Emit(OpCodes.Ret);

        propertyBuilder.SetGetMethod(getterBuilder);

        // Create type
        Type dynamicType = typeBuilder.CreateType();
        object instance = Activator.CreateInstance(dynamicType);
    }
}
```

### Dynamic Language Runtime (DLR)

The DLR provides dynamic typing and late binding for .NET.

```csharp
using System;
using System.Dynamic;

public class DynamicExamples
{
    public void UseDynamic()
    {
        // Dynamic variables
        dynamic obj = "Hello";
        obj = 42;                    // OK - type can change
        obj = new { Name = "Alice" }; // OK - anonymous type

        Console.WriteLine(obj.Name); // Late binding

        // Dynamic method calls
        dynamic calculator = new Calculator();
        var result = calculator.Add(2, 3); // Resolved at runtime
    }

    public void ExpandoObject()
    {
        // Dynamic object with runtime properties
        dynamic person = new ExpandoObject();
        person.Name = "Alice";
        person.Age = 30;
        person.Greet = (Action)(() => Console.WriteLine($"Hello, I'm {person.Name}"));

        person.Greet(); // Call dynamic method

        // Can enumerate properties
        var dict = (IDictionary<string, object>)person;
        foreach (var kvp in dict)
        {
            Console.WriteLine($"{kvp.Key}: {kvp.Value}");
        }
    }
}

// Custom dynamic object
public class DynamicDictionary : DynamicObject
{
    private readonly Dictionary<string, object> _data = new();

    public override bool TryGetMember(GetMemberBinder binder, out object result)
    {
        return _data.TryGetValue(binder.Name, out result);
    }

    public override bool TrySetMember(SetMemberBinder binder, object value)
    {
        _data[binder.Name] = value;
        return true;
    }

    public override bool TryInvokeMember(
        InvokeMemberBinder binder,
        object[] args,
        out object result)
    {
        if (_data.TryGetValue(binder.Name, out var value) && value is Delegate del)
        {
            result = del.DynamicInvoke(args);
            return true;
        }

        result = null;
        return false;
    }
}
```

### Proxy and Interception Patterns

Use DispatchProxy for dynamic proxy generation.

```csharp
using System;
using System.Reflection;

public interface IUserService
{
    User GetUser(int id);
    void SaveUser(User user);
}

public class LoggingProxy<T> : DispatchProxy
{
    private T _target;
    private ILogger _logger;

    public static T Create(T target, ILogger logger)
    {
        var proxy = Create<T, LoggingProxy<T>>() as LoggingProxy<T>;
        proxy._target = target;
        proxy._logger = logger;
        return (T)(object)proxy;
    }

    protected override object Invoke(MethodInfo targetMethod, object[] args)
    {
        _logger.LogInformation(
            "Calling {Method} with {Args}",
            targetMethod.Name,
            args
        );

        try
        {
            var result = targetMethod.Invoke(_target, args);

            _logger.LogInformation(
                "Completed {Method} with result {Result}",
                targetMethod.Name,
                result
            );

            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(
                ex,
                "Error in {Method}",
                targetMethod.Name
            );
            throw;
        }
    }
}

// Usage
var userService = new UserService();
var logger = new ConsoleLogger();
var proxy = LoggingProxy<IUserService>.Create(userService, logger);

proxy.GetUser(1); // Logged automatically
```

**See also:** `patterns-metaprogramming-dev` for cross-language metaprogramming patterns

## Best Practices

### Nullable Reference Types

```csharp
#nullable enable

public class UserService
{
    // Non-nullable reference type
    private readonly ILogger<UserService> _logger;

    // Nullable reference type
    private string? _cachedData;

    public UserService(ILogger<UserService> logger)
    {
        _logger = logger;
    }

    // Return nullable
    public string? FindUser(int id)
    {
        return id > 0 ? $"User{id}" : null;
    }

    // Parameter nullable
    public void UpdateCache(string? data)
    {
        _cachedData = data;
    }

    // Null-forgiving operator
    public void ProcessData()
    {
        var data = GetData();
        Console.WriteLine(data!.Length); // I know it's not null!
    }

    private string? GetData() => _cachedData;
}
```

### Async/Await Patterns

```csharp
public class AsyncPatterns
{
    // Async method naming (suffix with Async)
    public async Task<string> GetDataAsync()
    {
        await Task.Delay(100);
        return "data";
    }

    // Avoid async void (except event handlers)
    public async void HandleClick(object sender, EventArgs e)
    {
        await ProcessAsync();
    }

    // ConfigureAwait(false) in libraries
    public async Task<string> LibraryMethodAsync()
    {
        var data = await GetDataAsync().ConfigureAwait(false);
        return data;
    }

    // Parallel async operations
    public async Task<string[]> GetMultipleAsync()
    {
        var task1 = GetDataAsync();
        var task2 = GetDataAsync();
        var task3 = GetDataAsync();

        return await Task.WhenAll(task1, task2, task3);
    }

    // Cancellation support
    public async Task<string> ProcessWithCancellationAsync(
        CancellationToken cancellationToken)
    {
        await Task.Delay(1000, cancellationToken);
        cancellationToken.ThrowIfCancellationRequested();
        return "completed";
    }

    // ValueTask for performance
    public async ValueTask<int> GetCachedValueAsync(int key)
    {
        // Return cached value synchronously if available
        if (_cache.TryGetValue(key, out var value))
        {
            return value;
        }

        // Otherwise fetch asynchronously
        return await FetchValueAsync(key);
    }

    private readonly Dictionary<int, int> _cache = new();
    private async Task<int> FetchValueAsync(int key) => await Task.FromResult(key);
    private async Task ProcessAsync() => await Task.CompletedTask;
}
```

### Disposal Patterns

```csharp
// IDisposable implementation
public class ResourceHandler : IDisposable
{
    private bool _disposed;
    private readonly Stream _stream;

    public ResourceHandler(Stream stream)
    {
        _stream = stream;
    }

    public void DoWork()
    {
        ObjectDisposedException.ThrowIf(_disposed, this);
        // Do work
    }

    public void Dispose()
    {
        Dispose(disposing: true);
        GC.SuppressFinalize(this);
    }

    protected virtual void Dispose(bool disposing)
    {
        if (_disposed)
            return;

        if (disposing)
        {
            // Dispose managed resources
            _stream?.Dispose();
        }

        // Free unmanaged resources

        _disposed = true;
    }
}

// IAsyncDisposable implementation
public class AsyncResourceHandler : IAsyncDisposable
{
    private readonly HttpClient _httpClient;

    public AsyncResourceHandler(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async ValueTask DisposeAsync()
    {
        // Perform async cleanup
        _httpClient?.Dispose();
        await Task.CompletedTask;
    }
}

// Using statement
public class ResourceUser
{
    public void UseResource()
    {
        using var handler = new ResourceHandler(Stream.Null);
        handler.DoWork();
    } // Dispose called automatically

    public async Task UseResourceAsync()
    {
        await using var handler = new AsyncResourceHandler(new HttpClient());
        // Use handler
    } // DisposeAsync called automatically
}
```

### Record Types

```csharp
// Immutable record
public record Person(string FirstName, string LastName, int Age);

// Record with additional members
public record User(int Id, string Email)
{
    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;

    public string FullInfo => $"{Id}: {Email} (Created: {CreatedAt})";
}

// Record inheritance
public record Employee(int Id, string Email, string Department)
    : User(Id, Email);

// With expressions (non-destructive mutation)
public class RecordExample
{
    public void Example()
    {
        var person = new Person("John", "Doe", 30);
        var olderPerson = person with { Age = 31 };

        // Value equality
        var person2 = new Person("John", "Doe", 30);
        Console.WriteLine(person == person2); // True
    }
}
```

### Pattern Matching

```csharp
public class PatternMatchingExamples
{
    public string Describe(object obj)
    {
        return obj switch
        {
            null => "null",
            int i => $"int: {i}",
            string s => $"string: {s}",
            Person { Age: >= 18 } => "Adult person",
            Person { Age: < 18 } p => $"Minor: {p.FirstName}",
            IEnumerable<int> numbers => $"Number sequence: {numbers.Count()}",
            _ => "Unknown type"
        };
    }

    public decimal CalculateDiscount(Customer customer)
    {
        return customer switch
        {
            { IsPremium: true, YearsOfMembership: > 5 } => 0.20m,
            { IsPremium: true } => 0.15m,
            { YearsOfMembership: > 3 } => 0.10m,
            _ => 0.05m
        };
    }
}

public record Customer(bool IsPremium, int YearsOfMembership);
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-metaprogramming-dev` - Reflection, attributes, source generators, IL emit, dynamic types
- `patterns-concurrency-dev` - Async/await, tasks, parallel programming, thread safety
- `patterns-serialization-dev` - JSON serialization, validation, configuration binding

---

This skill provides foundational .NET patterns for modern cross-platform development. These patterns cover the .NET runtime, project structure, CLI tools, dependency injection, configuration management, logging, middleware, metaprogramming, NuGet packages, and best practices for building robust .NET applications.
