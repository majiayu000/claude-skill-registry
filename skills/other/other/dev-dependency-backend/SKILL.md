---
version: 1.2.0
name: dev-dependency-backend
description: >
  Audit and update NuGet packages for C#/.NET projects. Detects outdated packages,
  security vulnerabilities, and breaking changes. Groups updates by risk level,
  runs verification after each batch, and pauses for user confirmation before any
  major version bump or .NET framework upgrade.
  Invoked via /dev-dependency (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
argument-hint: "[--audit | --patch | --minor | --major | --security | --interactive | --cpm]"
---

# Dependency Update — Backend (.NET)

Audit and update NuGet packages safely, with breaking change detection.

> **Stack:** C#/.NET (NuGet, EF Core, ASP.NET Core)

## When to Use

- Routine NuGet dependency maintenance
- Security vulnerability response (`dotnet list package --vulnerable`)
- .NET framework upgrades (.NET 8→9, EF Core major bumps)
- Before starting a new feature (ensure clean baseline)

## Core Principle

**Never apply major version bumps without user confirmation.** Major versions mean breaking changes — API removals, behavioral changes, migration steps. Always show what changed and ask before proceeding.

## Workflow

```
1. AUDIT       → dotnet list package --outdated / --vulnerable / --deprecated
2. TRIAGE      → Classify as patch / minor / major / security
3. UPDATE      → Patch → verify → Minor → verify → Major → ASK → verify
4. VERIFY      → dotnet build && dotnet test after each batch
```

## Phase 0: Central Package Management (CPM) Conversion

**Triggered by:** `--cpm` flag or when `Directory.Packages.props` is missing in a multi-project solution.

### Detection

```bash
# Check if CPM is already enabled
test -f Directory.Packages.props && echo "CPM: enabled" || echo "CPM: not enabled"

# Check project count (CPM makes sense for 3+ projects)
find . -name "*.csproj" -not -path "*/bin/*" -not -path "*/obj/*" | wc -l
```

### Conversion Workflow

```
1. BASELINE   → Capture binlog for comparison
2. AUDIT      → Collect all package versions across projects
3. CREATE     → Generate Directory.Packages.props
4. STRIP      → Remove Version= from all .csproj PackageReferences
5. REBUILD    → Restore, build, compare binlogs
6. VERIFY     → Run tests
```

**Step 1 — Baseline binlog:**
```bash
dotnet build /bl:before-cpm.binlog 2>&1 | tail -10
```

**Step 2 — Audit all versions:**
```bash
dotnet list package --format json > package-audit.json
```

Review for version conflicts — same package with different versions across projects. **Ask the user** which version to standardize on for each conflict.

**Step 3 — Create Directory.Packages.props:**
```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
    <CentralPackageTransitivePinningEnabled>true</CentralPackageTransitivePinningEnabled>
  </PropertyGroup>
  <ItemGroup>
    <!-- One PackageVersion per unique package -->
    <PackageVersion Include="PackageName" Version="X.Y.Z" />
  </ItemGroup>
</Project>
```

**Step 4 — Strip versions from csproj files:**

For each `.csproj`, change:
```xml
<PackageReference Include="Serilog" Version="3.1.1" />
```
To:
```xml
<PackageReference Include="Serilog" />
```

**Step 5 — Rebuild and compare:**
```bash
dotnet restore
dotnet build /bl:after-cpm.binlog 2>&1 | tail -10
```

Compare package versions in both binlogs to ensure no version changed unexpectedly.

**Step 6 — Verify:**
```bash
dotnet test 2>&1 | tail -30
```

**Cleanup:**
```bash
rm -f before-cpm.binlog after-cpm.binlog package-audit.json
```

## Phase 1: Audit

```bash
# Outdated packages — safe updates only (patch)
dotnet list package --outdated --highest-patch

# Outdated packages — minor updates included
dotnet list package --outdated --highest-minor

# Outdated packages — all (includes major bumps)
dotnet list package --outdated

# Security vulnerabilities (including transitive)
dotnet list package --vulnerable --include-transitive

# Deprecated packages
dotnet list package --deprecated
```

### Optional tools

```bash
# dotnet-outdated (richer output with color-coded risk)
# Install: dotnet tool install -g dotnet-outdated-tool
dotnet outdated
```

## Phase 2: Triage

Present a report to the user:

```
DEPENDENCY UPDATE REPORT — Backend (.NET)
==========================================

Patch (safe):
  Serilog                  3.1.0 → 3.1.2
  Results    1.0.0 → 1.0.2

Minor (review):
  Polly                    8.2.0 → 8.4.0
  Mapster                  7.3.0 → 7.4.0

Major (BREAKING — needs confirmation):
  ⚠ EF Core                8.0.4 → 9.0.1
  ⚠ xUnit                  2.7.0 → 3.0.0

Security:
  🔒 Newtonsoft.Json       13.0.1 → 13.0.3  (CVE-2024-XXXX)

Deprecated:
  ⚠ Microsoft.AspNetCore.Mvc.NewtonsoftJson → use System.Text.Json
```

### Risk levels

| Level | SemVer | Risk | Action |
|-------|--------|------|--------|
| **Patch** | `X.Y.Z+` | Minimal — bug fixes | Apply automatically |
| **Minor** | `X.Y+.Z` | Low — backward-compatible | Apply, run tests |
| **Major** | `X+.Y.Z` | High — breaking changes | **ASK the user first** |
| **Security** | Any | Depends on severity | Prioritize |

## Phase 3: Update

### Step 1: Security fixes (urgent)

```bash
dotnet add package <PackageName> --version <safe-version>
```

**→ Run verification (`dotnet build && dotnet test`)**

### Step 2: Patch updates (safe)

```bash
dotnet add package <PackageName> --version <latest-patch>
```

**→ Run verification**

### Step 3: Minor updates (review)

Apply one by one. Check release notes for deprecation warnings:

```bash
dotnet add package <PackageName> --version <latest-minor>
```

**→ Run verification**

### Step 4: Major updates (STOP AND ASK)

**Never auto-apply.** For each major bump:

1. **Show the user what's changing:**
   ```
   ⚠ MAJOR VERSION UPDATE: EF Core 8.0.4 → 9.0.1

   Breaking changes:
   - Discriminator column renamed from 'Discriminator' to '$type'
   - ExcludeFromMigrations behavior changed
   - New migration required after upgrade

   Impact: 23 files import Microsoft.EntityFrameworkCore
   Migration guide: https://learn.microsoft.com/ef/core/what-is-new/ef-core-9.0/breaking-changes

   Files likely needing changes:
   - Data/AppDbContext.cs
   - Data/Migrations/*.cs (will need new migration)
   - Services/*Repository.cs (if using raw SQL)

   Proceed? (yes/no/skip)
   ```

2. **If user confirms:** apply, check compiler errors, run tests, report failures

### Impact Analysis

```bash
# How many files use this package?
grep -rn "using <Namespace>" --include="*.cs" src/ | wc -l

# Which files?
grep -rln "using <Namespace>" --include="*.cs" src/
```

## Breaking Change Detection

### How to identify

1. **SemVer major bump** → always assume breaking
2. **Check Microsoft docs:**
   - EF Core: `learn.microsoft.com/ef/core/what-is-new/ef-core-{version}/breaking-changes`
   - ASP.NET Core: `learn.microsoft.com/aspnet/core/migration/{from}-to-{to}`
   - .NET runtime: `learn.microsoft.com/dotnet/core/compatibility/{version}`
3. **Build after update** — compiler errors reveal API changes
4. **Deprecation scan** — `dotnet list package --deprecated`

### Common breaking changes by package

| Package | Watch for |
|---------|-----------|
| **EF Core** | Discriminator changes, migration format, provider API, query translation |
| **ASP.NET Core** | Middleware ordering, auth changes, minimal API updates, hosting model |
| **xUnit** | Assert API changes, runner configuration, `IAsyncLifetime` |
| **Results** | ValidationBuilder API, Result\<T\> combinators, TypedResults integration |
| **Polly** | V7→V8 complete rewrite (resilience pipelines replace policies) |
| **Serilog** | Sink configuration, enricher API |
| **Mapster/Mapster.Tool** | TypeAdapterConfig, code-gen output, mapping registration |

## .NET Framework Upgrade

Framework upgrades require a specific order:

```
1. Update global.json → new SDK version
2. Update TargetFramework in all .csproj files
3. Update all Microsoft.* packages to matching version
4. Run dotnet build → fix compiler errors
5. Check for behavioral changes (runtime breaking changes)
6. Run tests → fix failures
7. Update Dockerfile if applicable
8. Update CI/CD pipeline SDK version
```

**Always update .NET version BEFORE updating dependent packages.**

## Verification

After each batch:

```bash
dotnet build --no-restore 2>&1 | tail -20
dotnet test 2>&1 | tail -30
```

## Rollback

```bash
# Revert specific package
dotnet add package <PackageName> --version <previous-version>

# Restore from lock file (if using central package management)
dotnet restore

# Nuclear option
git checkout -- *.csproj
dotnet restore
```

## Flags

| Flag | Behavior |
|------|----------|
| `--audit` | Report only, no changes (default) |
| `--patch` | Apply patch updates only |
| `--minor` | Apply patch + minor updates |
| `--major` | Full update including major (always asks) |
| `--security` | Security fixes only |
| `--interactive` | Step through each package one by one |
| `--cpm` | Convert to Central Package Management (Phase 0) |

## Anti-Patterns

- **Updating everything at once** — one major bump breaks, but which one?
- **Ignoring deprecation warnings** — today's warning is next version's error
- **Skipping tests after updates** — "it compiled" ≠ "it works"
- **Pinning exact versions forever** — security vulnerabilities accumulate
- **Mixing .NET version with mismatched Microsoft.* packages** — version alignment matters
