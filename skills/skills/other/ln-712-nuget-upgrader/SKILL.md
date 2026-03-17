---
name: ln-712-nuget-upgrader
description: Upgrades .NET NuGet packages with breaking change handling
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-712-nuget-upgrader

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-710-dependency-upgrader

Upgrades .NET NuGet packages with automatic breaking change detection and migration.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Solution/project path |
| **Output** | Updated .csproj files, migration report |
| **Supports** | .NET 6, 7, 8, 9, 10 |

---

## Workflow

See [diagram.html](diagram.html) for visual workflow.

**Phases:** Pre-flight → Find Projects → Security Audit → Check Outdated → Identify Breaking → Apply Upgrades → Restore & Build → Report

---

## Phase 0: Pre-flight Checks

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| .csproj file(s) | Yes | Block upgrade |
| .sln file | No | Use csproj discovery instead |

> Workers assume coordinator (ln-710) already verified git state and created backup.

---

## Phase 1: Find Projects

### Discovery Methods

| Method | Command |
|--------|---------|
| Find .csproj | `Get-ChildItem -Recurse -Filter *.csproj` |
| From solution | `dotnet sln list` |

---

## Phase 2: Security Audit

### Commands

| Check | Command |
|-------|---------|
| Vulnerable packages | `dotnet list package --vulnerable` |
| Outdated packages | `dotnet list package --outdated` |

### Actions

| Severity | Action |
|----------|--------|
| Critical | Block upgrade, report |
| High | Warn, continue |
| Moderate/Low | Log only |

---

## Phase 3: Check Outdated

### Using dotnet-outdated

| Step | Command |
|------|---------|
| Install tool | `dotnet tool install --global dotnet-outdated-tool` |
| Check | `dotnet outdated --output json` |

---

## Phase 4: Identify Breaking Changes

### Detection

1. Compare current vs latest major versions
2. Check [breaking_changes_patterns.md](../ln-710-dependency-upgrader/references/breaking_changes_patterns.md)
3. Use MCP tools (see below) for migration guides

### Common Breaking Changes

| Package | Breaking Version | Key Changes |
|---------|------------------|-------------|
| Microsoft.EntityFrameworkCore | 8 → 9 | Query changes, migration format |
| Serilog.AspNetCore | 7 → 8 | Configuration format |
| Swashbuckle.AspNetCore | 6 → 7 | Minimal API support |

---

## MCP Tools for Migration Search

### Priority Order (Fallback Strategy)

| Priority | Tool | When to Use |
|----------|------|-------------|
| 1 | mcp__context7__query-docs | First choice for library docs |
| 2 | mcp__Ref__ref_search_documentation | Official Microsoft docs |
| 3 | WebSearch | Latest info, community solutions |

### Context7 Usage

| Step | Tool | Parameters |
|------|------|------------|
| 1. Find library | mcp__context7__resolve-library-id | libraryName: "EntityFrameworkCore" |
| 2. Query docs | mcp__context7__query-docs | query: "EF Core 8 to 9 migration breaking changes" |

### MCP Ref Usage

| Action | Tool | Query Example |
|--------|------|---------------|
| Search | mcp__Ref__ref_search_documentation | "dotnet EntityFrameworkCore 9 migration guide" |
| Read | mcp__Ref__ref_read_url | URL from search results |

### WebSearch Fallback

Use when Context7/Ref return no results:
- `"<package> .NET <version> breaking changes migration"`
- `"<error code> <package> fix"`

---

## Phase 5: Apply Upgrades

### Priority Order

| Priority | Package Type |
|----------|--------------|
| 1 | SDK/Runtime (Microsoft.NET.Sdk) |
| 2 | Framework (Microsoft.AspNetCore.*) |
| 3 | EF Core (affects migrations) |
| 4 | Logging (Serilog.*) |
| 5 | Other packages |

### Commands

| Action | Command |
|--------|---------|
| Update specific | `dotnet add package <name> --version <ver>` |
| Update all | `dotnet outdated --upgrade` |

---

## Phase 6: Restore & Build

### Commands

| Step | Command |
|------|---------|
| Restore | `dotnet restore` |
| Build | `dotnet build --configuration Release` |
| Test | `dotnet test` |

### On Failure

1. Identify failing package from error
2. Search Context7/Ref for migration guide
3. If unresolved: rollback package, continue

---

## Phase 7: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| solution | Solution path |
| projects[] | Updated projects |
| duration | Total time |
| upgrades[] | Applied upgrades |
| buildVerification | PASSED or FAILED |
| testResults | X passed, Y failed |

---

## Configuration

```yaml
Options:
  # Upgrade scope
  upgradeType: major          # major | minor | patch

  # Security
  auditLevel: high
  minimumReleaseAge: 14

  # .NET specific
  includePrerelease: false
  targetFramework: net10.0

  # Verification
  runTests: true
  runBuild: true
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| CS0246 | Missing type | Search for replacement API |
| NU1605 | Downgrade detected | Check package constraints |
| Build fail | Breaking change | Apply migration via Context7 |

---

## References

- [breaking_changes_patterns.md](../ln-710-dependency-upgrader/references/breaking_changes_patterns.md)
- [dotnet_version_matrix.md](references/dotnet_version_matrix.md)

---

## Definition of Done

- All .csproj files discovered (via solution or recursive scan)
- Security audit completed (`dotnet list package --vulnerable`)
- Outdated packages identified via dotnet-outdated
- Breaking changes detected via breaking_changes_patterns.md and MCP tools
- Upgrades applied in priority order (SDK > Framework > EF Core > other)
- `dotnet restore`, `dotnet build`, `dotnet test` all pass
- Report returned with projects updated, upgrades applied, and build/test status

---

**Version:** 1.1.0
**Last Updated:** 2026-01-10
