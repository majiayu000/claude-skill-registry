---
version: 1.0.0
name: dev-dotnet-build
description: >
  MSBuild diagnosis and optimization for .NET projects. Covers binlog analysis,
  incremental build fixes, common MSBuild antipatterns, and Directory.Build.props/targets
  organization. Referenced by dev-verification-backend and dotnet-build-resolver agent.
disable-model-invocation: true
user-invocable: false
context: fork
---

# MSBuild Diagnosis & Optimization

Diagnose and fix .NET build failures, slow builds, and MSBuild configuration issues.

> **Stack:** C#/.NET (MSBuild, NuGet, SDK-style projects)

## When to Use

- Build failures that aren't simple compilation errors
- Slow builds / broken incremental builds
- Complex multi-project solution MSBuild issues
- Directory.Build.props/targets configuration problems
- MSBuild property/target ordering issues

## Core Workflow

```
1. DIAGNOSE   → Identify the error category
2. BINLOG     → Generate and analyze binary log
3. FIX        → Apply targeted fix
4. VERIFY     → Rebuild and confirm
```

## Phase 1: Generate Binary Log

Always start with a binlog for non-trivial build issues:

```bash
# Generate binlog
dotnet build /bl:build.binlog 2>&1 | tail -30

# Named binlog for before/after comparison
dotnet build /bl:before.binlog
# ... apply fix ...
dotnet build /bl:after.binlog
```

The binlog captures the full MSBuild evaluation — every property, item, target, and task. See [binlog-analysis.md](references/binlog-analysis.md) for deep analysis techniques.

## Phase 2: Error Classification

| Error prefix | Category | Approach |
|-------------|----------|----------|
| `CS****` | C# compiler | Read error location, fix code |
| `MSB****` | MSBuild engine | Check project files, SDK, imports |
| `NU****` | NuGet | Check packages, sources, versions |
| `NETSDK****` | .NET SDK | Check SDK version, target framework |
| No prefix | Target/task failure | Check custom targets, tools |

## Phase 3: Common Diagnosis Patterns

### Missing or Wrong SDK

```bash
# Check installed SDKs
dotnet --list-sdks

# Check global.json pin
cat global.json

# Fix: update global.json or install correct SDK
dotnet new globaljson --sdk-version <version> --force
```

### Property Override Issues

Properties set in the wrong order get overwritten. Check evaluation order:

```bash
# See the fully evaluated project (all imports resolved)
dotnet msbuild <project.csproj> -preprocess > evaluated.xml
```

Look for the same property being set multiple times — last one wins.

### Target Ordering

```bash
# List all targets and their dependencies
dotnet msbuild <project.csproj> -targets 2>&1 | head -50
```

### NuGet Resolution Failures

```bash
# Clear NuGet caches (resolves stale package issues)
dotnet nuget locals all --clear

# Restore with detailed verbosity
dotnet restore --verbosity detailed 2>&1 | tail -50
```

### Missing Project References

```bash
# List all project references
dotnet list reference

# Check for broken references
find . -name "*.csproj" -exec grep -l "ProjectReference" {} + | \
  xargs grep "ProjectReference" | grep -v "^Binary"
```

## Phase 4: Fix and Verify

After applying a fix:

```bash
# Clean rebuild (eliminates stale artifacts)
dotnet clean
dotnet build 2>&1 | tail -30

# If build succeeds, run tests
dotnet test 2>&1 | tail -30
```

## Build Performance

For slow builds, check:

```bash
# Performance summary
dotnet build /clp:PerformanceSummary 2>&1 | tail -40

# Detailed timing
dotnet build /bl:perf.binlog
# Analyze target execution times in the binlog
```

See [incremental-builds.md](references/incremental-builds.md) for fixing broken incremental builds.

## Reference Docs

- [binlog-analysis.md](references/binlog-analysis.md) — Binary log generation, reading, and comparison
- [incremental-builds.md](references/incremental-builds.md) — Fix broken incremental builds
- [msbuild-antipatterns.md](references/msbuild-antipatterns.md) — 15+ common MSBuild mistakes
- [directory-build-organization.md](references/directory-build-organization.md) — Props/targets hierarchy and organization
