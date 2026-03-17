---
name: dotnet
description: |
  Configures .NET SDK, build processes, and project structure for BotMind mod.
  Use when: building, configuring projects, managing dependencies, or troubleshooting MSBuild.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Dotnet Skill

BotMind uses a multi-target .NET setup: client plugin targets `netstandard2.1` for BepInEx compatibility, server mod targets `net9.0` for SPT server. The `SPT_PATH` environment variable controls reference assembly resolution and auto-copy of build outputs.

## Quick Start

### Build Client Plugin

```bash
# Set SPT path for reference DLLs
$env:SPT_PATH = "H:\SPT"

# Build debug
dotnet build src/client/Blackhorse311.BotMind.csproj

# Build release
dotnet build src/client/Blackhorse311.BotMind.csproj -c Release
```

### Build Server Mod

```bash
dotnet build src/server/Blackhorse311.BotMind.Server.csproj
```

### Run Tests

```bash
dotnet test src/tests/Blackhorse311.BotMind.Tests.csproj
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Target Framework | Client uses netstandard2.1, server uses net9.0 | `<TargetFramework>netstandard2.1</TargetFramework>` |
| SPT_PATH | Environment variable for SPT installation | `$env:SPT_PATH = "H:\SPT"` |
| Auto-copy | Build outputs copy to SPT folders when SPT_PATH set | Client → `BepInEx/plugins/` |
| Reference Assemblies | EFT DLLs resolved from SPT_PATH | `$(SPT_PATH)\EscapeFromTarkov_Data\Managed\` |

## Common Patterns

### Conditional Reference Paths

**When:** Resolving game assemblies for local development

```xml
<PropertyGroup>
  <SPTPath Condition="'$(SPT_PATH)' != ''">$(SPT_PATH)</SPTPath>
  <ManagedPath>$(SPTPath)\EscapeFromTarkov_Data\Managed</ManagedPath>
</PropertyGroup>

<ItemGroup>
  <Reference Include="Assembly-CSharp">
    <HintPath>$(ManagedPath)\Assembly-CSharp.dll</HintPath>
    <Private>false</Private>
  </Reference>
</ItemGroup>
```

### Post-Build Copy

**When:** Automatically deploying built DLL to SPT

```xml
<Target Name="CopyToSPT" AfterTargets="Build" Condition="'$(SPT_PATH)' != ''">
  <Copy SourceFiles="$(TargetPath)" 
        DestinationFolder="$(SPT_PATH)\BepInEx\plugins\Blackhorse311-BotMind\" />
</Target>
```

### Multi-Project Solution

**When:** Building both client and server

```bash
# Build all projects
dotnet build Blackhorse311.BotMind.sln

# Or individually
dotnet build src/client/Blackhorse311.BotMind.csproj && \
dotnet build src/server/Blackhorse311.BotMind.Server.csproj
```

## See Also

- [patterns](references/patterns.md) - Project configuration patterns
- [workflows](references/workflows.md) - Build and deployment workflows

## Related Skills

- See the **csharp** skill for C# language patterns
- See the **bepinex** skill for plugin configuration
- See the **xunit** skill for test project setup
- See the **unity** skill for Unity assembly references