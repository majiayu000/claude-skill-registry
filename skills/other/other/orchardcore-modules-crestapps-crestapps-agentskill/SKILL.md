---
name: orchardcore-modules
description: Skill for creating and structuring Orchard Core modules. Covers module scaffolding, feature registration, dependency management, startup configuration, and manifest conventions.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Modules - Prompt Templates

## Create a Module

You are an Orchard Core expert. Generate the scaffolding for a new Orchard Core module.

### Guidelines

- Module names should be PascalCase and typically prefixed with the organization name (e.g., `CrestApps.MyModule`).
- Every module must have a `Manifest.cs` file declaring its features.
- Each feature must have a unique ID and should declare its dependencies.
- Use `Startup` classes to register services, routes, and navigation.
- Follow the Orchard Core convention of placing migrations in a `Migrations` folder or file.
- Use `[RequireFeatures]` attribute when a service depends on an optional feature.
- Third-party modules (CrestApps, Lombiq, or any non-OrchardCore-direct modules) must be installed as NuGet packages or project references in the **web project** (the startup project of the solution), not just in the module project.
- Always seal classes.

### Installing Third-Party Modules

Third-party modules are installed by adding NuGet packages or project references to the web project:

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <ItemGroup>
    <!-- Orchard Core base -->
    <PackageReference Include="OrchardCore.Application.Cms.Targets" Version="2.*" />

    <!-- Third-party modules must be in the web project -->
    <PackageReference Include="CrestApps.OrchardCore.AI" Version="1.*" />
    <PackageReference Include="Lombiq.HelpfulExtensions.OrchardCore" Version="1.*" />
  </ItemGroup>
</Project>
```

For local module projects:

```xml
<ItemGroup>
  <ProjectReference Include="../ThirdParty.Module/ThirdParty.Module.csproj" />
</ItemGroup>
```

### Manifest Pattern

```csharp
using OrchardCore.Modules.Manifest;

[assembly: Module(
    Name = "{{ModuleName}}",
    Author = "{{Author}}",
    Website = "{{Website}}",
    Version = "1.0.0",
    Description = "{{Description}}",
    Category = "{{Category}}"
)]

[assembly: Feature(
    Id = "{{ModuleName}}",
    Name = "{{FeatureName}}",
    Description = "{{FeatureDescription}}",
    Dependencies = new[]
    {
        "OrchardCore.ContentManagement"
    },
    Category = "{{Category}}"
)]
```

### Startup Pattern

```csharp
using Microsoft.Extensions.DependencyInjection;
using OrchardCore.Modules;

namespace {{ModuleName}}
{
    public sealed class Startup : StartupBase
    {
        public override void ConfigureServices(IServiceCollection services)
        {
            // Register services here
        }
    }
}
```

### Project File Pattern

```xml
<Project Sdk="Microsoft.NET.Sdk.Razor">

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <AddRazorSupportForMvc>true</AddRazorSupportForMvc>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="OrchardCore.Module.Targets" Version="2.*" />
  </ItemGroup>

</Project>
```

### Module Folder Structure

```
MyModule/
├── Manifest.cs
├── Startup.cs
├── MyModule.csproj
├── Controllers/
├── Drivers/
├── Handlers/
├── Migrations/
├── Models/
├── Services/
├── ViewModels/
├── Views/
└── wwwroot/
```
