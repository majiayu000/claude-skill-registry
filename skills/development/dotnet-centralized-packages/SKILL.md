---
name: dotnet-centralized-packages
description: Guide for Centralized Package Management (CPM) using Directory.Packages.props in .NET projects
type: domain
enforcement: suggest
priority: high
---

# Centralized Package Management (CPM)

This skill provides guidance for using **Central Package Management** (CPM) with `Directory.Packages.props` in this .NET 10 project. CPM manages all NuGet package versions in one central location.

## Table of Contents
1. [What is CPM](#what-is-cpm)
2. [Project Configuration](#project-configuration)
3. [Adding Packages](#adding-packages)
4. [Updating Packages](#updating-packages)
5. [Package Structure](#package-structure)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)
8. [Quick Reference](#quick-reference)

---

## What is CPM

### Overview

**Centralized Package Management** (CPM) is a NuGet feature that centralizes package version management in a single `Directory.Packages.props` file at the solution root.

**Benefits:**
- **Single source of truth** for package versions
- **No version conflicts** across projects
- **Easier updates** - change version in one place
- **Better dependency management**
- **Simpler project files**

### How It Works

**Traditional approach** (NOT used in this project):
```xml
<!-- Each .csproj specifies versions -->
<PackageReference Include="MSTest" Version="4.0.0-preview.25465.3" />
```

**CPM approach** (used in this project):
```xml
<!-- Directory.Packages.props defines versions -->
<PackageVersion Include="MSTest" Version="4.0.0-preview.25465.3" />

<!-- .csproj references WITHOUT version -->
<PackageReference Include="MSTest" />
```

---

## Project Configuration

### Directory.Packages.props

Located at solution root (`/Directory.Packages.props`):

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
  </PropertyGroup>

  <ItemGroup Label="Core Packages">
    <PackageVersion Include="Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation" Version="10.0.0-rc.2.25502.107" />
    <PackageVersion Include="Microsoft.AspNetCore.OpenApi" Version="10.0.0-rc.2.25502.107" />
  </ItemGroup>

  <ItemGroup Label="Testing Packages">
    <PackageVersion Include="MSTest" Version="4.0.0-preview.25465.3" />
    <PackageVersion Include="Microsoft.Playwright.MSTest.v4" Version="1.55.0-beta-4" />
  </ItemGroup>
</Project>
```

### Key Properties

**ManagePackageVersionsCentrally**: Enables CPM. All versions must be in Directory.Packages.props.

**CentralPackageTransitivePinningEnabled**: Pins transitive dependency versions to prevent unexpected updates.

### Directory.Build.props Integration

CPM works alongside `Directory.Build.props` which defines shared MSBuild properties:

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <Nullable>disable</Nullable>
    <ImplicitUsings>disable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
```

---

## Adding Packages

### Step-by-Step Process

**Step 1**: Add version to `Directory.Packages.props`

```xml
<ItemGroup Label="Your Category">
  <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
</ItemGroup>
```

**Step 2**: Add reference to `.csproj` (WITHOUT version)

```xml
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" />
</ItemGroup>
```

### Examples from This Project

**Adding MSTest (already in project):**
```xml
<!-- Directory.Packages.props -->
<PackageVersion Include="MSTest" Version="4.0.0-preview.25465.3" />

<!-- tests/ClaudeStack.Web.Tests/ClaudeStack.Web.Tests.csproj -->
<PackageReference Include="MSTest" />
```

**Adding Razor Runtime Compilation (already in project):**
```xml
<!-- Directory.Packages.props -->
<PackageVersion Include="Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation" Version="10.0.0-rc.2.25502.107" />

<!-- src/ClaudeStack.Web/ClaudeStack.Web.csproj -->
<PackageReference Include="Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation" />
```

### Common Mistakes

**WRONG - Adding Version to .csproj:**
```xml
<!-- This will FAIL with CPM enabled -->
<PackageReference Include="MSTest" Version="4.0.0-preview.25465.3" />
```

**Error message:**
```
error NU1008: Version information is not allowed for central package versions.
```

**CORRECT - No Version in .csproj:**
```xml
<PackageReference Include="MSTest" />
```

### Using dotnet add package

When using `dotnet add package`, you MUST add the version separately:

```bash
# Step 1: Add to Directory.Packages.props manually
# Edit Directory.Packages.props and add:
# <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />

# Step 2: Add reference to project
dotnet add src/ClaudeStack.Web/ClaudeStack.Web.csproj package Newtonsoft.Json

# OR manually add to .csproj:
# <PackageReference Include="Newtonsoft.Json" />
```

**Note**: `dotnet add package` may not automatically update Directory.Packages.props. Manual editing is often required.

---

## Updating Packages

### Update Single Package

Edit `Directory.Packages.props`:

```xml
<!-- Before -->
<PackageVersion Include="MSTest" Version="4.0.0-preview.25465.3" />

<!-- After -->
<PackageVersion Include="MSTest" Version="4.0.0" />
```

This updates the package across **all projects** that reference it.

### Update Multiple Packages

Edit versions in Directory.Packages.props. All projects will use the new versions automatically.

### Update All Packages to Latest

```bash
# List outdated packages
dotnet list package --outdated

# Update packages in Directory.Packages.props based on output
# (Manual process - edit Directory.Packages.props)

# Restore to apply changes
dotnet restore
```

### Version Ranges (Not Recommended)

CPM supports version ranges, but **not recommended** for this project:

```xml
<!-- Avoid this pattern -->
<PackageVersion Include="MSTest" Version="[4.0.0,5.0.0)" />
```

Use explicit versions for reproducibility.

---

## Package Structure

### Organizing with ItemGroup Labels

This project uses labeled ItemGroups for organization:

```xml
<ItemGroup Label="Core Packages">
  <!-- ASP.NET Core packages -->
</ItemGroup>

<ItemGroup Label="Testing Packages">
  <!-- MSTest, Playwright, etc. -->
</ItemGroup>

<ItemGroup Label="Analysis Packages">
  <!-- Code analysis tools -->
</ItemGroup>
```

Labels are optional but improve readability.

### Current Packages in Project

**Core Packages:**
- Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation: 10.0.0-rc.2.25502.107
- Microsoft.AspNetCore.OpenApi: 10.0.0-rc.2.25502.107

**Testing Packages:**
- MSTest: 4.0.0-preview.25465.3
- Microsoft.Playwright.MSTest.v4: 1.55.0-beta-4

### Viewing All Packages

```bash
# List all packages in solution
dotnet list package

# Include transitive dependencies
dotnet list package --include-transitive
```

---

## Troubleshooting

### Issue: "Version information is not allowed"

**Full Error:**
```
error NU1008: Version information is not allowed for central package versions.
```

**Cause**: PackageReference in .csproj includes Version attribute when CPM is enabled.

**Solution**: Remove Version from .csproj
```xml
<!-- WRONG -->
<PackageReference Include="MSTest" Version="4.0.0-preview.25465.3" />

<!-- CORRECT -->
<PackageReference Include="MSTest" />
```

### Issue: "Package not found" after adding to .csproj

**Cause**: Package version not defined in Directory.Packages.props.

**Solution**: Add to Directory.Packages.props:
```xml
<PackageVersion Include="PackageName" Version="x.y.z" />
```

### Issue: Different projects use different versions

**Symptom**: Project A uses v1.0, Project B uses v2.0 of same package.

**Cause**: With CPM, **all projects must use the same version**. This is by design.

**Solutions:**
1. **Preferred**: Standardize on one version across all projects
2. **Workaround** (not recommended): Disable CPM for specific packages using `VersionOverride`

```xml
<!-- In .csproj, override version (not recommended) -->
<PackageReference Include="MSTest" VersionOverride="3.0.0" />
```

### Issue: Transitive dependency conflicts

**Symptom**: Build errors about incompatible transitive dependencies.

**Solution**: Enable `CentralPackageTransitivePinningEnabled`:
```xml
<PropertyGroup>
  <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
</PropertyGroup>
```

Already enabled in this project.

### Issue: dotnet add package doesn't work

**Symptom**: `dotnet add package` adds reference but version is missing from Directory.Packages.props.

**Solution**: Manually add version to Directory.Packages.props (this is expected behavior).

### Issue: Restore fails after adding package

**Solution**: Ensure package exists on NuGet.org or configured feeds:
```bash
# Clear NuGet cache
dotnet nuget locals all --clear

# Restore
dotnet restore
```

---

## Best Practices

### 1. Always Edit Directory.Packages.props First

When adding a new package:
1. Add `<PackageVersion>` to Directory.Packages.props
2. Then add `<PackageReference>` to .csproj

### 2. Keep Versions Consistent

Avoid mixing preview and stable versions unnecessarily. This project uses preview packages because it targets .NET 10 RC 2.

### 3. Use Semantic Versioning

Understand version numbers: `Major.Minor.Patch[-Prerelease]`
- `10.0.0-rc.2.25502.107`: Major=10, Minor=0, Patch=0, Prerelease=rc.2.25502.107

### 4. Group Packages Logically

Use labeled ItemGroups:
- Core Packages
- Testing Packages
- Analysis Packages
- Development Packages

### 5. Review Transitive Dependencies

```bash
dotnet list package --include-transitive
```

Understand what indirect dependencies your project uses.

### 6. Update Carefully

When updating packages:
1. Test in development first
2. Update one package at a time (for critical packages)
3. Run full test suite after updates

### 7. Document Breaking Changes

When updating major versions, document breaking changes in commit messages or project documentation.

### 8. Avoid VersionOverride

Only use `VersionOverride` as a last resort. It defeats the purpose of CPM.

---

## Quick Reference

### File Locations

```
/Directory.Packages.props  - Package versions (central)
/Directory.Build.props     - Shared build properties
/**/*.csproj               - Package references (no versions)
```

### Adding a Package

```xml
<!-- Step 1: Directory.Packages.props -->
<PackageVersion Include="PackageName" Version="x.y.z" />

<!-- Step 2: ProjectFile.csproj -->
<PackageReference Include="PackageName" />
```

### Updating a Package

```xml
<!-- Directory.Packages.props - change version -->
<PackageVersion Include="PackageName" Version="x.y.z" />

<!-- All projects automatically use new version -->
```

### Common Commands

```bash
# List packages
dotnet list package

# List outdated packages
dotnet list package --outdated

# List transitive dependencies
dotnet list package --include-transitive

# Restore packages
dotnet restore

# Clear cache and restore
dotnet nuget locals all --clear && dotnet restore
```

### Directory.Packages.props Template

```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
  </PropertyGroup>

  <ItemGroup Label="Category Name">
    <PackageVersion Include="PackageName" Version="x.y.z" />
  </ItemGroup>
</Project>
```

### Error Reference

| Error | Cause | Solution |
|-------|-------|----------|
| NU1008 | Version in .csproj | Remove Version attribute |
| Package not found | Missing from Directory.Packages.props | Add PackageVersion |
| Version conflict | Different versions needed | Use single version or VersionOverride |

---

## Related Skills

- **mstest-testing-platform**: MSTest package configuration and usage
- **playwright-dotnet**: Playwright package setup and testing
- **dotnet-cli-essentials**: Package commands (list, add, restore)

---

## Additional Resources

- [Microsoft CPM Documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management)
- [NuGet Package Version Reference](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning)
- [Directory.Build.props Documentation](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory)

---

## Version Information

This project uses:
- **.NET SDK**: 10.0.100-rc.2.25502.107
- **NuGet CPM**: Supported in .NET 6.0+ SDK
- **MSBuild**: 17.0+

CPM is a stable NuGet feature as of .NET 6.0 SDK.
