---
name: vvvv-node-libraries
description: Helps set up C# library projects that provide nodes to vvvv gamma — project directory structure, Initialization.cs with AssemblyInitializer, service registration via RegisterService, IResourceProvider factories, ImportAsIs namespace/category configuration, .csproj setup, and dynamic node factories via RegisterNodeFactory. Use when creating a new library project, registering services or node factories, configuring ImportAsIs parameters, or setting up .csproj.
license: CC-BY-SA-4.0
compatibility: Designed for coding AI agents assisting with vvvv gamma development
metadata:
  author: Tebjan Halm
  version: "1.0"
---

# Creating vvvv gamma Node Libraries

A node library is a project that provides multiple nodes to vvvv gamma as a distributable package. This skill covers the project-level concerns: directory structure, naming conventions, category organization, service registration, and node factories.

For writing individual node classes (ProcessNode, Update, pins, change detection), see vvvv-custom-nodes. For consuming services inside node constructors (IFrameClock, Game, logging), see vvvv-custom-nodes/services.md.

## Library Recognition Pattern

vvvv recognizes a directory as a library when the **folder name, .vl file, and .nuspec all share the same name**:

```
VL.MyLibrary/                       # Folder name = package name
├── VL.MyLibrary.vl                 # .vl document — MUST match folder name
├── VL.MyLibrary.nuspec             # NuGet spec — MUST match folder name
├── lib/
│   └── net8.0/                     # Compiled DLLs go here
│       └── VL.MyLibrary.dll
├── src/
│   ├── Initialization.cs           # [assembly:] attributes + AssemblyInitializer
│   ├── Nodes/
│   │   ├── MyProcessNode.cs        # [ProcessNode] classes
│   │   └── MyOperations.cs         # Static methods (stateless nodes)
│   ├── Services/
│   │   └── MyService.cs            # Per-app singletons
│   └── VL.MyLibrary.csproj
├── shaders/                         # Optional: SDSL shaders (auto-discovered)
│   └── MyEffect_TextureFX.sdsl
└── help/                            # Optional: .vl help patches
    └── HowTo Use MyNode.vl
```

**Critical conventions**:
- Folder name, `.vl` file, and `.nuspec` must be identical (e.g., all `VL.MyLibrary`)
- The `.csproj` must output DLLs to `lib/net8.0/` relative to the package root
- No `.vl` file within a package should reference a `.csproj` — this forces the package into editable mode
- The library directory must be in a configured **package-repository** directory for vvvv to find it

### .csproj Output Path

The `.csproj` must compile into the library's `lib/net8.0/` folder:

```xml
<PropertyGroup>
  <TargetFramework>net8.0</TargetFramework>
  <OutputPath>..\..\lib\net8.0\</OutputPath>
  <AppendTargetFrameworkToOutputPath>false</AppendTargetFrameworkToOutputPath>
</PropertyGroup>
```

## Initialization.cs — The Entry Point

Every node library needs assembly-level attributes. Combine in one file:

```csharp
using VL.Core;
using VL.Core.CompilerServices;
using VL.Core.Import;

// Required: tells vvvv to scan this assembly for nodes
[assembly: ImportAsIs(Namespace = "MyCompany.MyLibrary", Category = "MyLibrary")]

// Optional: register services before any node runs
[assembly: AssemblyInitializer(typeof(MyCompany.MyLibrary.Initialization))]

namespace MyCompany.MyLibrary;

public sealed class Initialization : AssemblyInitializer<Initialization>
{
    public override void Configure(AppHost appHost)
    {
        var services = appHost.Services;

        // Register per-app singletons (created lazily on first access)
        services.RegisterService<MyService>(serviceProvider =>
        {
            return new MyService(serviceProvider);
        });
    }
}
```

### ImportAsIs and Category Naming

| Parameter | Purpose | Example |
|---|---|---|
| `Namespace` | C# namespace to scan for public types | `"VL.MyLibrary"` |
| `Category` | Node browser category for all discovered nodes | `"MyLibrary"` |

Without parameters (`[assembly: ImportAsIs]`), vvvv scans all namespaces and strips one namespace level to derive the category. The parameterized form gives explicit control over library organization.

**Namespace → Category mapping**: C# namespaces map to dot-separated node browser categories. Classes in `VL.MyLibrary.Particles` appear under `MyLibrary.Particles` in the node browser (the root namespace specified in `ImportAsIs` is stripped).

### Per-Type Category Override

Override the category for individual types:

```csharp
[assembly: ImportType(typeof(SpecialNode), Category = "MyLibrary.Advanced")]
```

Use this to place specific nodes into different categories than their namespace would suggest.

## Service Registration Patterns

Services are registered in `Configure(AppHost)` and consumed by nodes via `NodeContext`. This section covers registration only — for consumption patterns, see vvvv-custom-nodes/services.md.

### Direct Singleton (Recommended)

```csharp
services.RegisterService<MyService>(serviceProvider =>
{
    // Created lazily on first GetService<MyService>() call
    return new MyService(serviceProvider);
});
```

### IResourceProvider Pattern (For Managed Lifecycle)

When the service wraps a resource that needs explicit disposal:

```csharp
services.RegisterService<IResourceProvider<MyGPUService>>(serviceProvider =>
{
    var gameProvider = serviceProvider.GetService<IResourceProvider<Game>>();
    return gameProvider.Bind(game =>
    {
        var service = MyGPUService.Create(game);
        return ResourceProvider.Return(service, disposeAction: s => s?.Dispose());
    });
});
```

## Dynamic Node Factories

Register programmatic node generation for dynamic node sets:

```csharp
public override void Configure(AppHost appHost)
{
    // Dynamic node factory from shader files or other sources
    appHost.RegisterNodeFactory("VL.MyLibrary.ShaderNodes",
        init: MyShaderNodeFactory.Init);
}
```

Use node factories when nodes are generated from external files (shaders, configs) rather than written as C# classes. For details, see the [vvvv Node Factories docs](https://thegraybook.vvvv.org/reference/extending/node-factories.html).

## Extension Methods for Service Access

Provide typed accessors for your services:

```csharp
public static class MyLibraryExtensions
{
    public static MyService? GetMyService(this ServiceRegistry services)
        => services.GetService(typeof(MyService)) as MyService;

    public static MyService? GetMyService(this IServiceProvider services)
        => services.GetService(typeof(MyService)) as MyService;
}
```

## .csproj Essentials

Full library `.csproj` with output to `lib/net8.0/`:

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <OutputPath>..\..\lib\net8.0\</OutputPath>
    <AppendTargetFrameworkToOutputPath>false</AppendTargetFrameworkToOutputPath>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="VL.Core" Version="2025.7.*" />
    <PackageReference Include="VL.Core.Import" Version="2025.7.*" />
    <!-- For Stride integration: -->
    <PackageReference Include="VL.Stride.Runtime" Version="2025.7.*" />
  </ItemGroup>
</Project>
```

Match VL package versions to your vvvv installation version. The `OutputPath` places compiled DLLs in the library's `lib/net8.0/` folder where vvvv expects to find them.

## Real-World Example: Custom Rendering Library

Library initialization with service registration and node factory:

```csharp
[assembly: AssemblyInitializer(typeof(Initialization))]
[assembly: ImportAsIs(Namespace = "VL.MyRendering", Category = "MyRendering")]

public sealed class Initialization : AssemblyInitializer<Initialization>
{
    public override void Configure(AppHost appHost)
    {
        appHost.Services.RegisterService<CustomGameSystem>(sp =>
        {
            var vlGame = sp.GetService<VLGame>();
            if (vlGame == null) return null!;
            var customGame = CustomGameSystem.Create(vlGame, sp);
            vlGame.GameSystems.Add(customGame);
            return customGame;
        });

        // Dynamic node factory from shader files
        appHost.RegisterNodeFactory("VL.MyRendering.ShaderNodes",
            init: ShaderNodeFactory.Init);
    }
}
```

For naming conventions, pin rules, aspects, and standard types, see [design-guidelines.md](design-guidelines.md).
For publishing NuGets, help patches, and library structure, see [publishing.md](publishing.md).
For complete real-world examples (VL.IO.MQTT, VL.Audio), see [examples.md](examples.md).
