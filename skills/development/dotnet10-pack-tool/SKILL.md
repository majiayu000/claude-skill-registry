---
name: dotnet10-pack-tool
version: 1.0.0
description: Creates hybrid Native AOT + CoreCLR .NET 10 tool packages using ToolPackageRuntimeIdentifiers. Use for building high-performance CLI tools with Native AOT on supported platforms and CoreCLR fallback for universal compatibility.
source_urls:
  - https://github.com/richlander/dotnet10-hybrid-tool
  - https://github.com/richlander/dotnet10-hybrid-tool/blob/main/build-packages.sh
---

# .NET 10 Hybrid Pack Tool

## Purpose

Guides you through creating hybrid .NET 10 tool packages that combine Native AOT for maximum performance on select platforms with CoreCLR fallback for universal compatibility.

## When I Activate

I automatically load when you mention:

- "pack .NET tool" or "dotnet pack AOT"
- "Native AOT tool" or "hybrid .NET tool"
- "ToolPackageRuntimeIdentifiers"
- ".NET 10 tool packaging"
- "cross-platform .NET tool with AOT"

## What I Do

1. Configure your .csproj with `ToolPackageRuntimeIdentifiers` and `PublishAot=true`
2. Generate the pointer package (metapackage)
3. Build Native AOT packages for each target RID
4. Create CoreCLR fallback with `-r any`
5. Validate package structure

## Quick Start

### Step 1: Configure .csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net10.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>

    <!-- Package as .NET Tool -->
    <PackAsTool>true</PackAsTool>
    <ToolCommandName>your-tool-name</ToolCommandName>

    <!-- RIDs: CoreCLR fallback + Native AOT targets -->
    <ToolPackageRuntimeIdentifiers>any;osx-arm64;linux-arm64;linux-x64</ToolPackageRuntimeIdentifiers>

    <!-- Enable Native AOT -->
    <PublishAot>true</PublishAot>
  </PropertyGroup>

  <!-- Native AOT optimizations -->
  <PropertyGroup Condition="'$(PublishAot)' == 'true'">
    <InvariantGlobalization>true</InvariantGlobalization>
    <OptimizationPreference>Size</OptimizationPreference>
    <StripSymbols>true</StripSymbols>
  </PropertyGroup>
</Project>
```

### Step 2: Build Packages

```bash
# 1. Create pointer package (no binaries, just metadata)
dotnet pack -o ./packages

# 2. Build Native AOT for each target platform
dotnet pack -r osx-arm64 -o ./packages      # On macOS
dotnet pack -r linux-arm64 -o ./packages    # On Linux ARM or container
dotnet pack -r linux-x64 -o ./packages      # On Linux x64 or container

# 3. Create CoreCLR fallback for all other platforms
dotnet pack -r any -p:PublishAot=false -o ./packages
```

### Step 3: Install & Run

```bash
dotnet tool install -g your-tool-name
your-tool-name  # Auto-selects best package for platform
```

## Key Concepts

| Concept                           | Description                                           |
| --------------------------------- | ----------------------------------------------------- |
| **Pointer Package**               | Metapackage that references RID-specific packages     |
| **ToolPackageRuntimeIdentifiers** | Lists RIDs, creates pointer structure (no auto-build) |
| **`-r any`**                      | CoreCLR fallback for unlisted platforms               |
| **`-p:PublishAot=false`**         | Disables AOT for CoreCLR fallback                     |

## Why This Pattern Works

- `PublishAot=true` disables automatic RID package generation (AOT can't cross-compile OSes)
- `ToolPackageRuntimeIdentifiers` creates the pointer package structure
- Manual `-r <RID>` builds produce AOT binaries per platform
- `-r any -p:PublishAot=false` creates portable CoreCLR fallback

## Documentation

- [reference.md](./reference.md): Complete build script, container builds, CI/CD patterns
- [examples.md](./examples.md): Real-world examples and troubleshooting

## Requirements

- .NET 10 SDK installed
- Docker (for cross-platform Linux builds from macOS/Windows)
- AOT-compatible container: `mcr.microsoft.com/dotnet/sdk:10.0-noble-aot`
