---
name: dotnet-aot-analysis
description: Analyzes and configures a .NET project or solution for Native AOT compatibility. Orchestrates source generator skills and applies AOT settings.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob Grep AskUserQuestion
---

Analyze and configure a .NET project or solution for Native AOT compatibility, applying source generators and AOT settings.

## When to Use

- User wants to enable Native AOT
- User wants to check AOT compatibility
- User wants to optimize for AOT deployment

## Workflow

### Step 1: Ask Scope

Ask user: **Solution-wide** or **Specific project(s)**?

### Step 2: Detect Project Types

For each project:
- Check for ASP.NET Core (`Microsoft.AspNetCore` refs, `WebApplication`, `CreateBuilder`)
- Check for Blazor Server (`Microsoft.AspNetCore.Components.Server`)
- Check for MVC (`AddControllersWithViews`, `AddMvc`)

### Step 3: Warn About Unsupported Scenarios

| Scenario | Documentation |
|----------|---------------|
| Blazor Server | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot |
| MVC | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot |
| Session state | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot |
| SPA middleware | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot |

Ask user: Continue with compatible projects or abort?

### Step 4: Invoke Sub-Skills

For each compatible project, invoke:
1. `dotnet-source-gen-json` - JSON serialization AOT readiness (includes polymorphic types)
2. `dotnet-source-gen-options-validation` - Options pattern AOT readiness
3. `dotnet-source-gen-regex` - Regex AOT readiness
4. `dotnet-source-gen-logging` - Logging AOT readiness

### Step 5: Configure AOT Settings

**If solution-wide:**

Check for `src/Directory.Build.props`, otherwise use solution root. Add/merge:
```xml
<Project>
  <PropertyGroup>
    <!-- Advisory flag for tooling/analyzers; does not make code AOT-compatible -->
    <IsAotCompatible>true</IsAotCompatible>
    <EnableTrimAnalyzer>true</EnableTrimAnalyzer>
    <EnableSingleFileAnalyzer>true</EnableSingleFileAnalyzer>
    <EnableAotAnalyzer>true</EnableAotAnalyzer>
  </PropertyGroup>
</Project>
```

**If project-specific:**

Add to each `.csproj`:
```xml
<PropertyGroup>
  <PublishAot>true</PublishAot>
</PropertyGroup>
```

### Step 6: ASP.NET Core Specific

For ASP.NET Core projects:
- Recommend `CreateSlimBuilder()` over `CreateBuilder()`
- **Enable Request Delegate Generator (RDG)** for Minimal APIs:
  ```xml
  <PropertyGroup>
    <EnableRequestDelegateGenerator>true</EnableRequestDelegateGenerator>
  </PropertyGroup>
  ```
- **System.Text.Json**: Handled by `dotnet-source-gen-json` skill
- Warn about HTTPS/HTTP3 if needed (not included in `CreateSlimBuilder`)
- Ask user if they want to see generated code. If so, add `<EmitCompilerGeneratedFiles>true</EmitCompilerGeneratedFiles>`

### Step 7: Verify

Run `dotnet build` and check for AOT warnings.

## Key Documentation Links

| Topic | URL |
|-------|-----|
| Native AOT Overview | https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot |
| ASP.NET Core AOT | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/native-aot |
| Request Delegate Generator | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/aot/request-delegate-generator/rdg |
| AOT Limitations | https://learn.microsoft.com/en-us/dotnet/core/deploying/native-aot/?tabs=windows#limitations-of-native-aot-deployment |
| Trimming Libraries | https://learn.microsoft.com/en-us/dotnet/core/deploying/trimming/prepare-libraries-for-trimming |

## Notes

- Requires .NET 8+
- ASP.NET Core: Use `CreateSlimBuilder()` for optimal size
- Minimal APIs: Enable Request Delegate Generator (RDG) for optimal AOT performance
- Eliminate runtime reflection from hot paths; use source generators where reflection would otherwise be required
- System.Text.Json: Register all types in `JsonSerializerContext`
