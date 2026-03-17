---
name: dotnet
description: |
  Configures .NET 10 projects, builds, and manages C# runtime.
  Use when: building/running the solution, adding projects, managing NuGet packages, configuring Docker containers, or troubleshooting build issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Dotnet Skill

VanDaemon targets **.NET 10** across all projects. The solution uses a Clean Architecture layout with separate projects for API, Application, Core, Infrastructure, Plugins, and Frontend (Blazor WASM). All projects share consistent nullable reference types, JSON enum serialization, and structured logging patterns.

## Quick Start

### Build and Run

```bash
# Build entire solution
dotnet build VanDaemon.sln

# Run API (terminal 1)
cd src/Backend/VanDaemon.Api && dotnet run

# Run Blazor frontend (terminal 2)
cd src/Frontend/VanDaemon.Web && dotnet run

# Run tests
dotnet test VanDaemon.sln
```

### Create New Project

```bash
# Create class library in plugins folder
dotnet new classlib -n VanDaemon.Plugins.NewPlugin -o src/Backend/VanDaemon.Plugins/NewPlugin

# Add to solution
dotnet sln VanDaemon.sln add src/Backend/VanDaemon.Plugins/NewPlugin/VanDaemon.Plugins.NewPlugin.csproj

# Add project reference
dotnet add src/Backend/VanDaemon.Api/VanDaemon.Api.csproj reference src/Backend/VanDaemon.Plugins/NewPlugin/VanDaemon.Plugins.NewPlugin.csproj
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Target Framework | All projects use net10.0 | `<TargetFramework>net10.0</TargetFramework>` |
| Nullable Types | Enabled globally | `<Nullable>enable</Nullable>` |
| Implicit Usings | Enabled for cleaner code | `<ImplicitUsings>enable</ImplicitUsings>` |
| JSON Enums | Strings via converter | `JsonStringEnumConverter` in serializer options |
| CancellationToken | All async methods accept optional token | `Task<T> GetAsync(CancellationToken ct = default)` |

## Common Patterns

### Project Reference Chain

```
VanDaemon.Api
  ├── VanDaemon.Application
  │     └── VanDaemon.Core
  ├── VanDaemon.Plugins.Abstractions
  └── VanDaemon.Plugins.* (each plugin)
        └── VanDaemon.Plugins.Abstractions
```

### NuGet Package Management

```bash
# Add package to specific project
dotnet add src/Backend/VanDaemon.Api/VanDaemon.Api.csproj package Serilog.AspNetCore

# Update all packages in solution
dotnet outdated --upgrade
```

### Configuration Binding

```csharp
// appsettings.json section
builder.Services.Configure<MqttLedDimmerOptions>(
    builder.Configuration.GetSection("MqttLedDimmer"));
```

## See Also

- [patterns](references/patterns.md) - Project structure, DI, and build patterns
- [workflows](references/workflows.md) - Build, test, and deployment workflows

## Related Skills

- See the **csharp** skill for language patterns and coding conventions
- See the **aspnet-core** skill for API configuration and middleware
- See the **blazor** skill for frontend project setup
- See the **docker** skill for containerization
- See the **xunit** skill for test project configuration