---
version: 1.0.0
name: dev-dotnet-migrate
description: >
  .NET version migration assistant. Guides migration between .NET versions (8→9, 9→10, 10→11),
  nullable reference type adoption, and AOT compatibility preparation. Provides step-by-step
  checklists and automated detection of breaking changes.
disable-model-invocation: true
user-invocable: true
context: fork
argument-hint: "[8-to-9 | 9-to-10 | 10-to-11 | nullable | aot]"
---

# .NET Version Migration Assistant

Guides incremental migration between .NET versions with breaking change detection and verification.

> **Stack:** C#/.NET (ASP.NET Core, EF Core, NuGet)

## When to Use

- Planning a .NET version upgrade (8→9, 9→10, 10→11)
- Adopting nullable reference types across a codebase
- Preparing a project for Native AOT compilation
- Assessing migration risk before committing to an upgrade

## Core Principle

**Migrate incrementally. One project at a time, verify at each step.** Never upgrade the entire solution in one commit. Build confidence through small, verified steps.

## Argument Routing

| Argument | Action |
|----------|--------|
| `8-to-9` | Read `references/migrate-dotnet8-to-9.md` — .NET 8 LTS → .NET 9 STS |
| `9-to-10` | Read `references/migrate-dotnet9-to-10.md` — .NET 9 STS → .NET 10 LTS |
| `10-to-11` | Read `references/migrate-dotnet10-to-11.md` — .NET 10 LTS → .NET 11 STS |
| `nullable` | Read `references/nullable-references.md` — adopt `<Nullable>enable</Nullable>` |
| `aot` | Read `references/aot-compatibility.md` — prepare for Native AOT |
| *(none)* | Detect current version, suggest target, show pre-migration checklist |

## Universal Migration Steps

These apply to **every** .NET version upgrade:

### Pre-Migration Checklist

```
[ ] All tests passing on current version
[ ] Dependencies checked for target version support
[ ] Binlog baseline captured (dotnet build /bl:baseline.binlog)
[ ] Git branch created for migration
[ ] CI pipeline supports new SDK version
```

### Step-by-Step Upgrade

```
1. UPDATE SDK        → global.json → new SDK version
2. TARGET FRAMEWORK  → <TargetFramework>net{version}</TargetFramework> in csproj
3. PACKAGES          → Update all Microsoft.* packages to matching version
4. BUILD             → dotnet build 2>&1 | tee build-output.txt
5. FIX ERRORS        → Address compiler errors from breaking changes
6. TEST              → dotnet test — fix behavioral changes
7. INFRASTRUCTURE    → Update Dockerfile, CI/CD pipeline SDK versions
8. DEPRECATED APIS   → dotnet build /p:TreatWarningsAsErrors=true — catch obsolete usage
```

### Upgrade Order (multi-project solutions)

```
1. Shared libraries (no project dependencies)
2. Domain / Core projects
3. Infrastructure / Data access
4. Application / Service layer
5. API / Web host
6. Test projects (last — they depend on everything)
```

**After each project:** `dotnet build` the entire solution to catch cross-project breaks.

## Version Detection

```bash
# Current SDK
dotnet --version

# Current target frameworks
grep -rh '<TargetFramework>' --include="*.csproj" . | sort -u

# Global.json SDK pin
cat global.json 2>/dev/null || echo "No global.json (using latest installed SDK)"

# Installed SDKs
dotnet --list-sdks
```

## Post-Migration Verification

After completing the migration, run the full verification loop:

1. `dotnet build` — clean compile
2. `dotnet test` — all tests pass
3. `dotnet build /bl:post-migration.binlog` — capture for comparison
4. Invoke `dev-verification-backend --full` for comprehensive checks

## Rollback

If migration fails and can't be fixed in reasonable time:

```bash
# Revert all migration changes
git checkout -- .

# Or selectively revert
git checkout -- global.json
git checkout -- '*.csproj'
dotnet restore
```

## Reference Docs

- [migrate-dotnet8-to-9.md](references/migrate-dotnet8-to-9.md) — .NET 8 → 9 breaking changes and new features
- [migrate-dotnet9-to-10.md](references/migrate-dotnet9-to-10.md) — .NET 9 → 10 breaking changes and new features
- [migrate-dotnet10-to-11.md](references/migrate-dotnet10-to-11.md) — .NET 10 → 11 (preview guidance)
- [nullable-references.md](references/nullable-references.md) — Nullable reference type adoption strategy
- [aot-compatibility.md](references/aot-compatibility.md) — Native AOT preparation guide
