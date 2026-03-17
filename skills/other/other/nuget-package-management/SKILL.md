---
name: nuget-package-management
description: Manage NuGet packages using Central Package Management (CPM) and dotnet CLI. Never edit .csproj or Directory.Packages.props XML directly - use dotnet add/remove/list commands. Use shared version variables for related packages. Covers workspaces, security audits, and version management.
user-invocable: false
allowed-tools: Read Grep Glob Bash
metadata:
  author: Saturate
  version: "1.0"
---

# NuGet Package Management

Manage .NET dependencies using dotnet CLI with Central Package Management (CPM) for multi-project solutions.

## Golden Rule

**Always use `dotnet` CLI commands to manage packages. Never manually edit `.csproj` or `Directory.Packages.props` files.**

Why CLI commands are required:
- **Validation**: Checks package exists on NuGet before adding
- **Transitive dependencies**: Correctly resolves dependency graphs
- **Lock file integrity**: Updates `packages.lock.json` with proper checksums
- **XML correctness**: Prevents malformed XML and syntax errors
- **CPM integration**: Seamlessly works with centralized version management

Manual XML editing bypasses validation and causes broken builds, version conflicts, and package restore failures.

## Detect Package Management Style

**Check for Central Package Management (CPM):**

```bash
# Look for Directory.Packages.props at solution root
if [ -f "Directory.Packages.props" ]; then
    echo "Using CPM"
else
    echo "Using traditional per-project versions"
fi

# Check if CPM is enabled
grep -r "ManagePackageVersionsCentrally" Directory.Packages.props 2>/dev/null
```

**Project structure indicators:**
- `Directory.Packages.props` → CPM enabled
- `Directory.Build.props` → Shared MSBuild properties
- `global.json` → .NET SDK version pinning
- `NuGet.config` → Custom package sources
- `*.sln` → Solution file (multi-project)

**Version detection:**
```bash
# Check .NET SDK version
dotnet --version

# CPM requires .NET SDK 6.0.300+
```

## Quick Command Reference

### Package Operations

| Task | Command |
|------|---------|
| Add package | `dotnet add package <Name>` |
| Add specific version | `dotnet add package <Name> --version <Version>` |
| Remove package | `dotnet remove package <Name>` |
| List packages | `dotnet list package` |
| List transitive | `dotnet list package --include-transitive` |
| List outdated | `dotnet list package --outdated` |
| List vulnerable | `dotnet list package --vulnerable` |
| Restore packages | `dotnet restore` |
| Clean packages | `dotnet nuget locals all --clear` |

### Solution-Wide

| Task | Command |
|------|---------|
| List all packages | `dotnet list <solution.sln> package` |
| Check vulnerabilities | `dotnet list <solution.sln> package --vulnerable --include-transitive` |
| Restore solution | `dotnet restore <solution.sln>` |
| Restore (CI/CD) | `dotnet restore --locked-mode` |

For complete command reference: [references/commands.md](references/commands.md)

## Central Package Management (CPM)

CPM centralizes all package versions in a single `Directory.Packages.props` file at the solution root, eliminating version conflicts across multiple projects.

**Basic setup:**
```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>

  <ItemGroup>
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageVersion Include="Serilog" Version="3.1.1" />
  </ItemGroup>
</Project>
```

**Project files reference WITHOUT versions:**
```xml
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" />
  <PackageReference Include="Serilog" />
</ItemGroup>
```

**When to use CPM:**
- ✅ Multi-project solutions
- ✅ Need version consistency
- ✅ .NET SDK 6.0.300+

**When NOT to use:**
- ❌ Single project (little benefit)
- ❌ Need version ranges
- ❌ Legacy .NET Framework projects

For complete CPM setup guide: [references/cpm-setup.md](references/cpm-setup.md)

## Security

**Check for vulnerabilities:**
```bash
# Current project
dotnet list package --vulnerable --include-transitive

# Entire solution
dotnet list <solution.sln> package --vulnerable --include-transitive

# CI/CD integration
dotnet list package --vulnerable --include-transitive || exit 1
```

**Enable package lock files:**
```xml
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
</PropertyGroup>
```

For security best practices: [references/security.md](references/security.md)

## Multi-Project Solutions

**Typical structure:**
```
MySolution/
├── MySolution.sln
├── Directory.Packages.props          # CPM versions
├── Directory.Build.props             # Shared properties
├── NuGet.config                      # Package sources
├── src/
│   ├── Project1/
│   └── Project2/
└── tests/
    └── Project1.Tests/
```

**Directory.Build.props for shared configuration:**
```xml
<Project>
  <PropertyGroup>
    <LangVersion>latest</LangVersion>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
```

For multi-project guide: [references/multi-project.md](references/multi-project.md)

## Common Issues

### Package Not Found
```bash
dotnet nuget locals all --clear
dotnet restore --verbosity detailed
```

### Version Conflicts
```bash
# Show dependency tree
dotnet list package --include-transitive

# Force specific version in CPM
# Edit Directory.Packages.props
```

### CPM Not Working
```bash
# Check SDK version (need 6.0.300+)
dotnet --version

# Verify CPM enabled
grep "ManagePackageVersionsCentrally" Directory.Packages.props

# Check for inline versions (should be none)
grep -r "PackageReference.*Version=" --include="*.csproj" .
```

For complete troubleshooting: [references/troubleshooting.md](references/troubleshooting.md)

## Anti-Patterns to Avoid

### ❌ Manual XML Editing
```xml
<!-- ❌ Don't edit XML directly -->
<PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
```

```bash
# ✅ Use CLI instead
dotnet add package Newtonsoft.Json
```

### ❌ Mixing CPM and Inline Versions
```xml
<!-- ❌ Bad - inconsistent approach -->
<PackageReference Include="Package1" Version="1.0.0" />  <!-- inline -->
<PackageReference Include="Package2" />                   <!-- CPM -->
```

Pick one approach: CPM (centralized) or traditional (inline).

### ❌ Using Wildcard Versions
```xml
<!-- ❌ Bad - unpredictable -->
<PackageVersion Include="Newtonsoft.Json" Version="*" />

<!-- ✅ Good - explicit -->
<PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
```

### ❌ Not Using Lock Files
```xml
<!-- ✅ Always enable for applications -->
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
</PropertyGroup>
```

### ❌ Committing Packages to Git
```bash
# Add to .gitignore
packages/
*.nupkg
```

Lock files provide reproducibility without committing binaries.

## Migration

**Traditional → CPM:**
1. Create `Directory.Packages.props`
2. Extract versions from `.csproj` files
3. Add versions to `Directory.Packages.props`
4. Remove inline versions from `.csproj`
5. Restore and verify

**CPM → Traditional:**
1. Add versions back to each `.csproj`
2. Remove `Directory.Packages.props`
3. Restore and verify

For complete migration guide: [references/migration.md](references/migration.md)

## References

**Setup and Configuration:**
- [CPM Setup & Patterns](references/cpm-setup.md) - Central Package Management setup, shared versions, when to use
- [Multi-Project Solutions](references/multi-project.md) - Directory.Build.props, solution structure, shared configuration

**Commands and Operations:**
- [CLI Commands](references/commands.md) - Complete dotnet CLI reference, package sources, version management

**Security and Maintenance:**
- [Security Best Practices](references/security.md) - Vulnerability scanning, lock files, trusted signers, CI/CD
- [Troubleshooting](references/troubleshooting.md) - Common issues, debugging, clean slate approach

**Migration:**
- [Migration Strategies](references/migration.md) - Traditional ↔ CPM migration, gradual migration, rollback

**External Documentation:**
- [NuGet documentation](https://docs.microsoft.com/en-us/nuget/)
- [Central Package Management](https://devblogs.microsoft.com/nuget/introducing-central-package-management/)
- [dotnet CLI reference](https://docs.microsoft.com/en-us/dotnet/core/tools/)
